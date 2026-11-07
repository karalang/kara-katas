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

A `String` slice expression in a **map-key position** (`get` / `contains_key` / `remove` / `insert`) lowers to a *borrowed* view — a `{ptr, len, cap = 0}` struct that points straight into `s`'s buffer, with no `malloc`/`memcpy`. For the lookups (`get`), that view is hashed and compared and then discarded — it is never retained, so the borrow is always sound. For `insert`, the runtime **deep-copies** the bytes into an owned key only on a *fresh* insertion; an existing key just updates its count. So a counter/window map allocates **once per distinct word**, not once per window position — exactly what Rust's `&str` keys, Go's string slices, and C's `(ptr, len)` key views achieve.

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

M5 Pro, 2026-10-31 (`results.json` `measured_at` 2026-11-01T01:52Z), karac 0.9.0-dev.14057+g6697158fa (v2/MIR backend), hyperfine `--warmup 5 --runs 30 --shell=none`. All four compiled mirrors single-threaded:

| Run | Mean ± σ | Gap |
|---|---|---|
| c    concat_words (clang -O3, hashed `(ptr, len)` keys) | 60.6 ± 1.8 ms | 2.50× ahead of kāra |
| rust concat_words | 72.6 ± 1.7 ms | 2.09× ahead of kāra |
| rust concat_words (`overflow-checks=on`) | 72.8 ± 1.5 ms | 2.08× ahead of kāra |
| **kāra concat_words (codegen)** | **151.7 ± 4.1 ms** | — |
| go   concat_words | 209.5 ± 6.1 ms | kāra 1.38× ahead of Go |

The ratios are flat against the 2026-09-08 legacy feed (Kāra/Rust 2.09× → 2.09×, Kāra/C 2.47× → 2.50×, Kāra/Go 0.77× → 0.72×); every comparator ran 10–18% slower in absolute ms this session, so compare ratios, not milliseconds. The rest of this subsection is the history of how the kata got here.

This kata was the *driver* for two karac changes, and the 2026-06-08 snapshot (kāra 118.4 ms, Rust 68.7 ms, Go 173.2 ms) was the after. **Before** them (binding each window slice to a `let`, so every `s[j..j+L]` heap-allocated a fresh `String`), idiomatic Kāra ran this in **199 ms — 3.1× behind Rust — with 10.0 MiB peak RSS** from ~8 million `malloc`/`free` pairs. The two fixes:

1. **Borrowed String-slice map keys.** A slice written inline as a map key is now a borrowed view into `s` (no allocation); `insert` deep-copies only on a fresh key (see [§ Why the slice is written inline](#why-the-slice-is-written-inline)). Allocation drops from once-per-window to once-per-*distinct*-word — the same thing Rust's `&str` keys and C's packed `u32` keys do.
2. **`Map.clear()` frees its heap keys.** The sliding window clears `seen` on every dead window; `karac_map_clear` previously only zeroed the bucket status and *leaked* the owned key buffers. Fixed, RSS drops from 10.0 MiB to **1.4 MiB — at parity with Rust's 1.4 MiB** (see [peak-RSS table](#runtime-memory-peak)).

Net: **199 → 118 ms (1.69× faster) and 10.0 → 1.4 MiB (7× less)**, landing on that snapshot at **1.72× Rust on runtime and ~parity on memory**, and **1.46× ahead of Go**. The remaining runtime gap to Rust is the honest cost of staying leak-free: `seen.clear()` now actually *frees* the keys it used to leak (~2 M `free()` calls over the run), and Rust's borrowed `&str` keys mean it never allocated or freed them in the first place. C's 4.6× lead in that snapshot (25.5 ms) was its zero-hashing packed-`u32` key — a representation no general string solution gets.

> ⚠️ **That C mirror has been replaced, and the 4.6× with it.** `3561607`
> (31 Jul 2026) found it was a cross-language parity violation, not a fast C
> implementation: it packed each length-4 word into a `u32` and linear-scanned a
> ≤64-entry id array, so **C alone skipped both the hash and the key
> comparison** that Kāra, Rust and Go all pay. It now runs an open-addressing
> table keyed on `(ptr, len)` views into the text — no per-piece allocation,
> matching Rust's `&str` and Go's string slices — shaped like the runtime map
> (capacity 16, power of two, linear probing, double-and-rehash at 3/4 load,
> FxHash under the compiler's seed). C-vs-C cost of the honest structure:
> 46.5 → 93.9 ms (2.02×). On the 4 Aug 2026 M5 feed C's lead over Kāra is
> **2.09×** (53.8 vs 112.2 ms), not 4.6×, and roughly half of the old figure
> was the mirror rather than the backend. The Rust and Go comparisons in this
> section are unaffected — Kāra sits at 1.77× behind `rustc -O` and 1.55× ahead
> of Go on that feed, both within a hair of the ratios quoted above.

Note (31 Oct 2026): the Rust ratio "quoted above" has since moved — Kāra was 2.09× behind `rustc -O` already on the 8 Sep 2026 legacy feed and is 2.09× on the v2/MIR feed in the table; the move from 1.77× happened between 4 Aug and 8 Sep on the legacy backend and has not been attributed.

Note (2026-11-07, karac g97681763d): re-benched with the seq row built `KARAC_AUTO_PAR=0` (the script left auto-par on before), Kāra reads 140.6 ms, 2.10× equal-safety Rust and 2.08× `rustc -O`. The 17.2 ms figure that briefly replaced it was a parallel run.

That the backend was never the bottleneck shows in the other columns: Kāra **compiles this 1.34× faster than `rustc -O`** and ships a binary **31 % smaller than Rust's** (2.3× and 38 % on the 2026-06-08 snapshot).

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara concat_words` (codegen) | 151.7 ± 4.1 ms |
| `rust concat_words` | 72.6 ± 1.7 ms |
| `py concat_words` — last measured 2026-06-08, not re-run | 638.3 ± 18.1 ms |

Python is not in the 2026-10-31 feed (the run did not set `KARA_BENCH_INCLUDE_PY`); the ratio here is from the 2026-06-08 snapshot, when Kāra codegen was **~5.3× faster than CPython** — CPython allocates a `str` per slice *and* dispatches every map operation through the interpreter.

### Compile time and binary size

M5 Pro, 2026-10-31, karac g6697158fa (v2/MIR backend), hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build concat_words.kara` | 161.2 ± 1.7 ms | 328.5 KiB |
| `rustc -O concat_words.rs` | 215.4 ± 3.1 ms | 473.6 KiB |
| `clang -O3 concat_words.c` | 70.1 ± 1.0 ms | 33.1 KiB |
| `go build` | — | 2434.3 KiB |

Kāra compiles this kata **1.34× faster than `rustc -O`** (2.30× slower than C) and produces a binary **31 % smaller than Rust's** (336,368 B). Every v2/MIR Kāra binary is ~300–390 KB where the legacy backend's lean katas were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md); this kata was never on the lean floor (legacy shipped 312.7 KiB on the 2026-09-08 feed), so MIR adds 16 KiB here. On the 2026-06-08 legacy snapshot Kāra compiled 2.3× faster than `rustc -O` (90.5 vs 205.1 ms) with a 295.7 KiB binary — the `Map`/`String` runtime floor: this workload pulls in the hash-map and string-slice runtime, so it did not reach the lean ~33 KiB scalar floor that sibling katas like [#27](../27-remove-element/README.md) and [#29](../29-divide-two-integers/README.md) hit on the legacy backend.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `c    concat_words` | 1.2 MiB |
| `kara concat_words` (codegen) | 1.4 MiB |
| `rust concat_words` | 1.4 MiB |
| `py concat_words` — last measured 2026-06-08, not re-run | 7.8 MiB |
| `go   concat_words` | 9.8 MiB |

Kāra now sits **at parity with Rust** (1,474,896 B vs 1,507,640 B; C 1,294,648 B) and an order of magnitude below Go's GC arena — the live set is tiny (a few count maps + the 200 KB text), and with the `Map.clear` leak fixed there is no allocator high-water from churned keys. Before the fix this row read 10.0 MiB; it is the clearest single-number evidence that the two changes worked.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor — since `3561607` on the same hash and the same growth policy as the runtime map, so it now measures the backend rather than a cheaper data structure — Go is the cross-runtime data point, and Python is the ergonomic foil.
