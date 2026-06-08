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
- **String slicing `s[a .. b]`** — `s[start .. start + wl]` produces a fresh `String` over the window's bytes (design.md § String slicing; lowered to `karac_string_slice`), used directly as a map key. The whole kata is map-lookup-driven — no manual byte indexing.
- **`words: Slice[String]`** — the read-only sequence-parameter convention shared with [#1](../1-two-sum/) / [#15](../15-3sum/); a `Vec[String]` argument coerces to it at the call site. Indexed access `words[idx]` yields the element `String` directly, so `need` is keyed on the words themselves (`words[idx].clone()`), no substring built.
- **`Vec[i64].sort_by(|a, b| a.cmp(b))`** — the sliding-window result is sorted before return so the two approaches print identically.
- **`for idx in 0..k` index iteration** + nested `while` loops over scalar cursors (`i`, `j`, `left`, `count`).

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
| c    concat_words (clang -O3) | 24.0 ± 0.6 ms | 8.3× ahead of kāra |
| rust concat_words | 64.3 ± 0.6 ms | 3.1× ahead of kāra |
| go   concat_words | 174.6 ± 1.5 ms | 1.14× ahead of kāra |
| **kāra concat_words (codegen)** | **199.0 ± 2.9 ms** | — |

**This kata is honest about a v1 cost, not a codegen win** — and that is the point of running it. The gap is **one specific thing: every window slice `s[j .. j+L]` heap-allocates a fresh `String`** (via `karac_string_slice`: `malloc` + `memcpy` + NUL-terminate), because Kāra v1 has no borrowed-string-slice that can serve as a `Map` key. Rust keys its map on `&str` slices that point straight into the text (zero allocation); C packs each 4-byte word into a `u32` and skips string hashing entirely; Go's `map[string]` hashes a cheap immutable slice. Kāra, by contrast, does ~8 million `malloc`/`free` pairs over the run — and the [peak-RSS table](#runtime-memory-peak) shows it: **10.0 MiB for Kāra vs 1.4 MiB for Rust**, the signature of allocation churn, not of a larger working set (the live set is tiny — a few count maps).

That the cost is allocation and *not* the backend is visible in the other columns: Kāra **compiles this kata 2.2× faster than `rustc -O`** and ships a binary **38 % smaller than Rust's** (see below). The instruction stream the backend produces is fine; it is being asked to allocate a string several million times because the language can't yet hand the map a borrowed view.

**The fix is a known v1 gap, now with a concrete target.** A borrowed `StringSlice` (or small-string-interning) usable as a `Map` key would let the idiomatic solution key on a view into `s` — the same move Rust makes — and should close most of the gap. This kata is the simulated demand for that feature; it is tracked alongside the `String.from_utf8` codegen hole (the two open "string-materialization" items). Until then the kata reports reality: on a string-window-hashing workload, idiomatic Kāra is ~3× behind idiomatic Rust, ~1.14× behind Go, and still **3.2× ahead of Python**.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara concat_words` (codegen) | 199.0 ± 2.9 ms |
| `rust concat_words` | 64.3 ± 0.6 ms |
| `py concat_words` | 628.3 ± 7.2 ms |

Even paying for every slice allocation, Kāra codegen is **~3.2× faster than CPython** — CPython also allocates a `str` per slice *and* dispatches every map operation through the interpreter.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-08, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build concat_words.kara` | 89.9 ± 1.8 ms | 295.2 KiB |
| `rustc -O concat_words.rs` | 197.4 ± 3.2 ms | 473.6 KiB |
| `clang -O3 concat_words.c` | 56.8 ± 0.5 ms | 32.9 KiB |
| `go build` | — | 2434.3 KiB |

Kāra compiles this kata **2.2× faster than `rustc -O`** (1.58× slower than C) and produces a binary **38 % smaller than Rust's**. The 295 KiB is the auto-par/`Map`/`String` runtime floor — this workload pulls in the hash-map and string-slice runtime, so it does not reach the lean ~33 KiB scalar floor that sibling katas like [#27](../27-remove-element/README.md) and [#29](../29-divide-two-integers/README.md) hit.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `c    concat_words` | 1.2 MiB |
| `rust concat_words` | 1.4 MiB |
| `py concat_words` | 7.7 MiB |
| `go   concat_words` | 9.5 MiB |
| `kara concat_words` (codegen) | 10.0 MiB |

Kāra's 10.0 MiB is **not** a large live set — it is allocator high-water from churning ~8 million short-lived slice `String`s through `malloc`/`free`. Rust and C never allocate in the hot loop (borrowed `&str` / packed `u32`), so they sit near their loaded-image floor. This row is the same story as the runtime gap, told in bytes: close the borrowed-slice-key gap and this drops toward the Rust/C floor.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (and, here, what zero-allocation keying buys), Go is the cross-runtime data point, and Python is the ergonomic foil.
