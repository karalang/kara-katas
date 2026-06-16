# 30. Substring with Concatenation of All Words

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Hash Table, String, Sliding Window &nbsp;·&nbsp; **Source:** [leetcode.com/problems/substring-with-concatenation-of-all-words](https://leetcode.com/problems/substring-with-concatenation-of-all-words/)

Given a string `s` and an array `words` of strings that are **all the same length** `L`, return the start index of every substring of `s` that is a concatenation of each word in `words` exactly once, in any order, with no characters in between. With `K = words.len()`, every such substring has length `L·K`.

**Example:** `s = "barfoothefoobarman"`, `words = ["foo","bar"]` → `[0, 9]` (`"barfoo"` at 0, `"foobar"` at 9). `words` may contain duplicates, in which case a valid window must contain each word the matching number of times (`["a","b","a"]` over `"abababab"` needs two `a`s and one `b` per window → `[0, 2, 4]`).

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Brute force (fresh tally per start) | O((n − L·K)·K) time, O(L·K) space | [`brute_force.kara`](brute_force.kara) ✓ | [`brute_force.py`](brute_force.py) ✓ |
| Sliding window (L residue phases) | O(n) time, O(L·K) space | [`sliding_window.kara`](sliding_window.kara) ✓ | [`sliding_window.py`](sliding_window.py) ✓ |

Both build a `need` multiset (word → required count) once. They differ only in how they test each candidate window; their output is byte-identical.

### Brute force

For every start `i` in `0 ..= n − L·K`, chop the window into `K` consecutive `L`-byte pieces and tally them into a fresh `seen` map, bailing the instant a piece is (a) not a word in `need` or (b) already seen more often than `need` allows. Because a window holds exactly `K` pieces and the required counts sum to `K`, "no piece overflowed its allowance" is equivalent to "every word matched exactly once" — so any window that survives all `K` pieces is a hit. Simple and obviously correct, but it re-tallies from scratch at every byte offset.

### Sliding window — O(n)

The key observation: every valid window starts at an offset whose value mod `L` is fixed, and within one residue class `r` (`0 ≤ r < L`) all word boundaries line up — each candidate window is a run of whole `L`-byte words at `r, r+L, r+2L, …`. So run `L` independent passes, one per residue, each a classic variable-width sliding window over *words* (step `L`):

- **Extend right** by one word. If it isn't in `need`, the window is dead — clear it and restart just past the offending word.
- Otherwise add it to `seen`; while that word now appears more often than `need` wants, **drop words off the left** until it's balanced.
- When the window holds exactly `K` words, record `left`, then drop the leftmost word so the search continues for the next window.

Each byte of `s` enters and leaves a window at most once per phase, so total work is O(n) regardless of `K`. The `L` phases discover hits out of order, so the result is sorted before returning to match the brute force's left-to-right order.

## Output format

Each test case prints the match **count**, then each start index on its own line, in ascending order. (Reporting indices rather than the matched substrings mirrors sibling string katas like [#5](../5-longest-palindromic-substring/README.md#output-format) — the substring is recoverable as `s[idx .. idx + L·K]`, and indices are trivially diffable across the Kāra / Python pair.)

## Kāra features exercised

- **`Map[String, i64]` as a multiset** — `need` and `seen` are count maps. `match m.get(k) { Some(c) => c, None => 0 }` is the read-default-to-zero idiom; `m.insert(k, c + 1)` / `m.insert(k, c - 1)` are the increment/decrement; `m.clear()` resets a dead window.
- **Borrowed String-slice map keys `m.get(s[a .. b])`** — a slice expression written *inline in a map-key slot* lowers to a borrowed `{ptr, len, cap = 0}` view into `s` — no allocation for lookups, and a deep-copy only when `insert` adds a genuinely new key. This is the headline performance idiom for the kata; see [§ Why the slice is written inline](#why-the-slice-is-written-inline).
- **`words: Slice[String]`** — the read-only sequence-parameter convention shared with [#1](../1-two-sum/) / [#15](../15-3sum/); a `Vec[String]` argument coerces to it at the call site. Indexed access `words[idx]` yields the element `String` directly, so `need` is keyed on the words themselves (`words[idx].clone()` — the one owned-key site, run once per call).
- **`Vec[i64].sort_by(|a, b| a.cmp(b))`** — the sliding-window result is sorted before return so the two approaches print identically.
- **`for idx in 0..k` index iteration** + nested `while` loops over scalar cursors (`i`, `j`, `left`, `count`).

## Why the slice is written inline

The hot loop writes `need.get(s[j .. j+wl])` rather than `let piece = s[j .. j+wl]; need.get(piece)`, and that choice is what makes the kata fast.

A `String` slice expression in a **map-key position** (`get` / `contains_key` / `remove` / `insert`) lowers to a *borrowed* view — a `{ptr, len, cap = 0}` struct that points straight into `s`'s buffer, with no `malloc`/`memcpy`. For the lookups (`get`), that view is hashed and compared and then discarded — it is never retained, so the borrow is always sound. For `insert`, the runtime **deep-copies** the bytes into an owned key only on a *fresh* insertion; an existing key just updates its count. So a counter/window map allocates **once per distinct word**, not once per window position — exactly what Rust's `&str` keys and C's packed-`u32` keys achieve.

Binding the slice to a `let` first (`let piece = s[…]`) takes the **owned** path instead: `karac_string_slice` allocates a fresh `String` every time. That is correct but is the per-window-allocation cost this kata exists to avoid. (Extending the borrow to a `let`-bound slice used only as a key needs escape analysis, which is a later slice.)

This idiom landed as two karac changes the kata drove (it was the "simulated demand"): borrowed String-slice map keys, and a fix to `Map.clear()` so it frees its heap key buffers instead of leaking them (the sliding window clears `seen` on every dead window). See [§ Benchmarks](#benchmarks) for the before/after.

## Running

```bash
karac run sliding_window.kara
python3 sliding_window.py
diff <(karac run sliding_window.kara) <(python3 sliding_window.py) && echo OK
# the two approaches agree, too:
diff <(karac run brute_force.kara) <(karac run sliding_window.kara) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go mirror with `go build`, and the Kāra file with `karac build` (all cached in `bench/target/`, gitignored), then runs runtime, compile-cost (cold), binary-size, and peak-RSS passes.

| File | What it does |
|---|---|
| [`bench/concat_words.kara`](bench/concat_words.kara) | Build a 50 000-word text once (LCG-chosen from a 16-word vocabulary), then run the O(n) sliding-window search 40 times for 40 different 4-word targets; sink = Σ(match indices + counts) |
| [`bench/concat_words.py`](bench/concat_words.py) | Algorithmic mirror — same vocabulary, LCG, search, sink |
| [`bench/concat_words.rs`](bench/concat_words.rs) | Algorithmic mirror; `&str` slice keys (no per-piece allocation); `rustc -O` |
| [`bench/concat_words.c`](bench/concat_words.c) | Algorithmic mirror; the 4-byte words pack into a `u32` key (no string hashing); `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; `map[string]int` over string slices; `go build` |

Each implementation builds the identical text from the classic glibc LCG (`a = 1103515245, c = 12345, m = 2³¹`, seeded 1), picking each slot's word from the **high** bits (`state / 131072 % 16` — this LCG's low bits have a short period) so the slot stream is well-distributed. Every mirror runs the identical search and prints the same sink (`67841397`); `bench.sh` fails loudly on any mismatch. This is a **seq-only kata** — the search is strictly serial.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-06-08, hyperfine `--warmup 5 --runs 30 --shell=none`. All four compiled mirrors single-threaded:

| Run | Mean ± σ | Gap |
|---|---|---|
| c    concat_words (clang -O3) | 25.5 ± 0.9 ms | 4.6× ahead of kāra |
| rust concat_words | 68.7 ± 2.9 ms | 1.72× ahead of kāra |
| **kāra concat_words (codegen)** | **118.4 ± 1.0 ms** | — |
| go   concat_words | 173.2 ± 2.4 ms | kāra 1.46× ahead of Go |

This kata was the *driver* for two karac changes, and the table above is the after. **Before** them (binding each window slice to a `let`, so every `s[j..j+L]` heap-allocated a fresh `String`), idiomatic Kāra ran this in **199 ms — 3.1× behind Rust — with 10.0 MiB peak RSS** from ~8 million `malloc`/`free` pairs. The two fixes:

1. **Borrowed String-slice map keys.** A slice written inline as a map key is now a borrowed view into `s` (no allocation); `insert` deep-copies only on a fresh key (see [§ Why the slice is written inline](#why-the-slice-is-written-inline)). Allocation drops from once-per-window to once-per-*distinct*-word — the same thing Rust's `&str` keys and C's packed `u32` keys do.
2. **`Map.clear()` frees its heap keys.** The sliding window clears `seen` on every dead window; `karac_map_clear` previously only zeroed the bucket status and *leaked* the owned key buffers. Fixed, RSS drops from 10.0 MiB to **1.4 MiB — at parity with Rust's 1.4 MiB** (see [peak-RSS table](#runtime-memory-peak)).

Net: **199 → 118 ms (1.69× faster) and 10.0 → 1.4 MiB (7× less)**, landing at **1.72× Rust on runtime and ~parity on memory**, and **1.46× ahead of Go**. The remaining runtime gap to Rust is the honest cost of staying leak-free: `seen.clear()` now actually *frees* the keys it used to leak (~2 M `free()` calls over the run), and Rust's borrowed `&str` keys mean it never allocated or freed them in the first place. C's 4.6× lead is its zero-hashing packed-`u32` key — a representation no general string solution gets.

That the backend was never the bottleneck shows in the other columns: Kāra **compiles this 2.3× faster than `rustc -O`** and ships a binary **38 % smaller than Rust's**.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara concat_words` (codegen) | 118.4 ± 1.0 ms |
| `rust concat_words` | 68.7 ± 2.9 ms |
| `py concat_words` | 638.3 ± 18.1 ms |

Kāra codegen is **~5.3× faster than CPython** — CPython allocates a `str` per slice *and* dispatches every map operation through the interpreter.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-08, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build concat_words.kara` | 90.5 ± 0.7 ms | 295.7 KiB |
| `rustc -O concat_words.rs` | 205.1 ± 1.8 ms | 473.6 KiB |
| `clang -O3 concat_words.c` | 59.4 ± 0.6 ms | 32.9 KiB |
| `go build` | — | 2434.3 KiB |

Kāra compiles this kata **2.3× faster than `rustc -O`** (1.52× slower than C) and produces a binary **38 % smaller than Rust's**. The 295 KiB is the `Map`/`String` runtime floor — this workload pulls in the hash-map and string-slice runtime, so it does not reach the lean ~33 KiB scalar floor that sibling katas like [#27](../27-remove-element/README.md) and [#29](../29-divide-two-integers/README.md) hit.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `c    concat_words` | 1.2 MiB |
| `rust concat_words` | 1.4 MiB |
| `kara concat_words` (codegen) | 1.4 MiB |
| `py concat_words` | 7.8 MiB |
| `go   concat_words` | 9.5 MiB |

Kāra now sits **at parity with Rust** and an order of magnitude below Go's GC arena — the live set is tiny (a few count maps + the 200 KB text), and with the `Map.clear` leak fixed there is no allocator high-water from churned keys. Before the fix this row read 10.0 MiB; it is the clearest single-number evidence that the two changes worked.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (and, here, what zero-allocation *and* zero-hashing keying buys), Go is the cross-runtime data point, and Python is the ergonomic foil.
