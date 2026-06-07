# 28. Find the Index of the First Occurrence in a String

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Two Pointers, String, String Matching &nbsp;·&nbsp; **Source:** [leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)

Return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`. An empty needle matches at index `0` (the C `strstr` / `std` convention).

**Constraints:** `1 ≤ haystack.length, needle.length ≤ 10⁴`, both consist of lowercase English letters.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Brute-force sliding window | O(hn · nn) time, O(1) extra space | [`brute_force.kara`](brute_force.kara) ✓ | [`brute_force.py`](brute_force.py) ✓ |
| Knuth-Morris-Pratt (KMP) | O(hn + nn) time, O(nn) extra space | [`kmp.kara`](kmp.kara) ✓ | [`kmp.py`](kmp.py) ✓ |

## Why two approaches

Brute force tries every start position and compares the needle against the window byte-for-byte, bailing on the first mismatch. On typical text it's effectively linear (mismatches happen early), but its worst case is O(hn · nn): a haystack of repeated `a` searched for `aa…ab` matches the whole needle-minus-one at every position before failing on the last byte.

**KMP** removes that worst case. It precomputes, for each needle prefix, the length of its longest proper prefix that is also a suffix (the **LPS** / failure function). On a mismatch at needle position `j`, the scan resets `j` to `lps[j − 1]` instead of `0`, reusing the already-matched overlap so the haystack cursor `i` never backs up — O(hn + nn) guaranteed, at the cost of an `nn`-sized table. The two files share an identical adversarial bench input precisely so the wall-time gap is visible (see Benchmarks).

## Kāra features exercised

- **`ref String` parameters + `.bytes()` / `.len()`** — the surface solutions take `ref String` and scan the zero-copy `Slice[u8]` view; the LeetCode lowercase-letter constraint means byte index = char index, so no `Vec[char]` snapshot is needed.
- **`-1` sentinel return on `i64`** — the not-found path returns a negative index, exercising signed-return plumbing.
- **Short-circuit `and` guarding an indexed read** — brute force's `j < nn and haystack[i + j] == needle[j]` relies on left-to-right evaluation so the indexed read is skipped once `j == nn`.
- **`Vec[i64]` built and indexed inside a helper** — KMP's `build_lps` allocates the failure table with `Vec.filled`, fills it with a non-trivial recurrence (the `len = lps[len − 1]` fallback), and returns it by value.
- **Two-cursor loop with asymmetric advance** — KMP advances `i`/`j` together on a match, rewinds only `j` on a mismatch, exercising the conditionally-updated-cursor shape.

## Running

```bash
karac run brute_force.kara
karac run kmp.kara
diff <(karac run kmp.kara) <(python3 kmp.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust files with `rustc -O`, the C files with `clang -O3`, the Go mirrors with `go build`, and the Kāra files with `karac build` (all cached in `bench/target/`, gitignored), then runs runtime, compile-cost (cold, via a `--prepare` delete step), binary-size, and peak-RSS passes.

| File | What it does |
|---|---|
| [`bench/brute_force.kara`](bench/brute_force.kara) | Adversarial input, O(hn · nn) sliding window |
| [`bench/kmp.kara`](bench/kmp.kara) | Same input, O(hn + nn) KMP |
| `bench/{brute_force,kmp}.{py,rs,c}`, `bench/go-seq/{brute_force,kmp}` | Algorithmic mirrors (Python, `rustc -O`, `clang -O3`, `go build`) |

**Workload (shared by both approaches):** haystack = `N − 1` `'a'` bytes + one `'b'` (N = 2_000_000), needle = `M − 1` `'a'` bytes + `'b'` (M = 16), K = 10 searches. The needle occurs only at the very end (index `N − M`), so every start position matches `M − 1` bytes before failing on the last — the **brute-force worst case** (O(N · M)) and a deep-partial-match stress for KMP's fallback. All five mirrors step identical bytes (97 = `'a'`, 98 = `'b'`) over a `Slice[u8]` so the O(N) setup is a uniform bulk fill, not a runtime-dependent per-byte append. Sink = `K × (N − M)` = 19_999_840, a real returned index that proves the full scan ran; bench.sh fails loudly on mismatch. The search is read-only (the per-call result would be loop-invariant), but bounds-checked indexing keeps it off LLVM's `readonly` list, so LICM leaves the K calls in the loop — the same property kata [#5](../5-longest-palindromic-substring/README.md)'s bench relies on. Python is benched on KMP only (pure-Python brute force at O(N · M) = 320M byte compares is minutes per run); kāra interp lanes are omitted (tree-walk over the adversarial scan is impractical — interp parity is covered by the kata-root `diff` test on the `String` form).

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-06-07, hyperfine `--warmup 5 --runs 30 --shell=none`. Seq-only kata — `strStr` is a read-only scan with a loop-carried needle cursor, no auto-par surface. (Light background load; the kāra≈rust≈c ratios are the load-immune signal.)

**Brute force** (O(N · M)):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    brute_force (clang -O3) | 29.9 ± 1.7 ms | kāra 1.02× |
| rust brute_force | 30.1 ± 1.8 ms | kāra 1.01× |
| **kāra brute_force (codegen)** | **30.5 ± 1.7 ms** | — |
| go   brute_force | 94.7 ± 1.8 ms | kāra 3.1× ahead |

**KMP** (O(N + M)):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    kmp (clang -O3) | 11.8 ± 1.2 ms | 1.30× ahead of kāra |
| rust kmp | 15.2 ± 1.3 ms | kāra 1.01× |
| **kāra kmp (codegen)** | **15.3 ± 1.3 ms** | — |
| go   kmp | 23.5 ± 1.2 ms | kāra 1.54× ahead |

**Brute force is a three-way kāra ≈ Rust ≈ C tie**, and **KMP is kāra ≈ Rust** with C 1.30× ahead (the no-bounds-check raw-pointer floor on the tight `lps[]`-indexed loop). Both hold *with* integer-overflow trapping on by default (design.md § Arithmetic Overflow) — the only arithmetic in either hot loop is cursor `i++`/`j++`, whose overflow checks fold (loop-bounded), so there's no trapping cost. The algorithmic point lands too: kāra brute 30.5 ms vs kāra KMP 15.3 ms — KMP is ~2× faster on this M = 16 input even though both stream the same 2M-byte haystack (the per-byte compare-count gap is larger; wall-time is bounded by the memory scan). Go trails on both — its per-element bounds checks aren't eliminated on these tight loops.

### Codegen vs Python (KMP)

| Run | Mean ± σ |
|---|---|
| `kara kmp` (codegen) | 15.3 ± 1.3 ms |
| `rust kmp` | 15.2 ± 1.3 ms |
| `py kmp` | 952.2 ± 5.7 ms |

Python is **~62× slower** than Kāra codegen on KMP — per-iteration CPython bytecode dispatch over a 2M-byte scan.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-07, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | brute_force | kmp | Binary (bf / kmp) |
|---|---|---|---|
| `karac build` | 69.1 ± 1.2 ms | 69.7 ± 1.4 ms | 32.9 / 33.0 KiB |
| `rustc -O` | 74.1 ± 0.8 ms | 81.8 ± 0.9 ms | 455.4 / 455.4 KiB |
| `clang -O3` | 41.5 ± 0.8 ms | 41.2 ± 0.7 ms | 32.8 / 32.8 KiB |
| `go build` | — | — | 2434.1 / 2434.1 KiB |

Kāra compiles **1.07–1.17× faster** than `rustc -O` and produces binaries **~93% smaller** than Rust's — **within 136–184 bytes of C** (the delta is the overflow-trap landing pads). Same lean profile as the array katas: the workload reaches `Vec.filled` + indexed read/write, `Slice[u8]` indexing, `println(i64)` — and nothing else; cross-archive LTO + DCE elides the rest of the runtime.

### Runtime memory (peak)

| Run | brute_force | kmp |
|---|---|---|
| `kara` (codegen) | 2.9 MiB | 2.9 MiB |
| `c` | 2.9 MiB | 2.9 MiB |
| `rust` | 3.0 MiB | 3.0 MiB |
| `go` | 4.6 MiB | 4.6 MiB |
| `python` | — | 10.6 MiB |

**Parity with C** — the working set is the 2M-byte haystack (≈2 MiB) plus the tiny needle and (KMP) a 16-entry `i64` LPS table. Go's +1.7 MiB is GC arena + runtime; Python's 10.6 MiB is the CPython baseline plus the `bytearray`.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (kāra ties it on brute force; C's 1.30× KMP lead is the no-bounds-check loop), Go is the cross-runtime data point, and Python is the ergonomic foil.
