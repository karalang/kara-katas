# 14. Longest Common Prefix

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** String, Trie &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-common-prefix](https://leetcode.com/problems/longest-common-prefix/)

Given an array of strings `strs`, return the longest common prefix shared by all of them. If there is no common prefix, return the empty string `""`.

**Constraints:** `1 ≤ strs.length ≤ 200`, `0 ≤ strs[i].length ≤ 200`, `strs[i]` consists of lowercase English letters.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Vertical scanning (column-by-column) | O(S) time, O(1) extra (+ output) | [`vertical.kara`](vertical.kara) ✓ via `karac run` | [`vertical.py`](vertical.py) ✓ |

`✓` runs end-to-end today. `S` is the total number of characters scanned, bounded by `min-length × count`.

### Why vertical scanning?

Walk the columns of the input strings left to right. At column `col` every string must agree on the same character; the first column where any string either ends early or disagrees is where the common prefix stops. This is the textbook formulation — it touches each character at most once, stops at the first mismatch, and needs no auxiliary structure beyond the returned prefix.

`strs[0].bytes()` is the reference column source — a zero-copy `Slice[u8]` view with O(1) positional access (the same primitive kata 13 uses for its Roman-numeral scan). Each other string's `bytes()` view is compared column-for-column. LeetCode #14 restricts inputs to lowercase English letters, so every character is a single ASCII byte and the byte column index equals the char index — the byte view is exact and no `Vec[char]` snapshot is needed for the scan. The output prefix is rebuilt from the first string's `chars()` in one O(prefix) pass, so the returned `String` is well-formed regardless of the runtime's storage encoding.

The `col >= other.len() or other[col] != c` guard leans on `or`'s short-circuit: when a string is shorter than the current column, the bound check is `true` and the `other[col]` indexed read is never evaluated — no separate out-of-bounds guard needed.

## Kāra features exercised

- **`Vec[String]` parameter** — `longest_common_prefix(strs: ref Vec[String])`; indexing `strs[0]` / `strs[s]` yields the element `String` which coerces to `ref String` at the `.bytes()` / `prefix_string` call sites.
- **`String.bytes()` → `Slice[u8]`** — zero-copy byte view with O(1) positional access for the column scan.
- **`String.chars()` iteration + `String.push(char)`** — rebuild the output prefix one character at a time.
- **`or` short-circuit** — guards the `other[col]` indexed read behind the `col >= other.len()` bound check on the same line.
- **Owned-`Vec[String]` literal construction** — `let mut a: Vec[String] = Vec.new(); a.push("flower"); …` then passed to a `ref Vec[String]` parameter.

## Running

```bash
# Kāra
karac run vertical.kara

# Python (3.10+ for PEP 604 union syntax)
python3 vertical.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`vertical.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** M = 8 distinct test cases, each a `Vec[String]` of N = 16 strings sharing a prefix of a different length (0, 2, 4, 7, 10, 13, 16, 20). Built once into a `Vec[Vec[String]]` before the timed loop. Each case's N strings begin with the first `prefix_len` letters of the alphabet, then string `s` diverges with six copies of its signature letter (the `s`-th letter), so the strings agree on exactly `prefix_len` columns and the LCP is exactly `prefix_len`. K = 1,000,000 outer iterations rotate `idx = k % M` and call `longest_common_prefix` on that case, so the call is never loop-invariant (LLVM can't hoist it) and the input distribution sweeps the full range of prefix lengths the vertical scan can hit. The sink is the running total of every returned prefix's length = `(K / M) × (0+2+4+7+10+13+16+20)` = `125000 × 72` = **9,000,000**; all five mirrors must agree before any timing begins. This is the same shape class as kata 13 / 71 (per-iter work + one small output `String` alloc per call), so cross-kata wall-time comparisons stay meaningful.

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + r.len()` accumulator is the slice-1 allow-list reduction shape, so `karac build` may emit a `karac_par_reduce` dispatch by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — and reports them in separate tables per the two-lane discipline.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-05-29, hyperfine `--warmup 5 --runs 30 --shell=none`. All four comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time |
|---|---|
| go   vertical            | **66.3 ± 4.3 ms** |
| c    vertical (clang -O3)| 67.1 ± 4.9 ms |
| rust vertical            | 81.9 ± 7.4 ms |
| **kāra vertical (seq)**  | **92.1 ± 2.9 ms** |

Kāra runs **1.12× of Rust** and **1.37× of clang -O3** on the seq lane. The workload is String-construction-heavy — every call rebuilds the prefix one `char` at a time via `String.push` over a `chars()` iterator, and the column scan calls `.bytes()` on each `Vec[String]` element per inner iteration. The gap to Rust is the per-`char` push + iterator-advance cost through the runtime's `String` machinery (Rust's `String::push` over `chars()` lowers to a tighter inlined loop); the gap to C/Go adds the absence of a raw `memcpy`-style prefix copy. These are general-runtime costs the kata exercises heavily, not per-kata regressions.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible; the default `karac build` recognizes it and emits a `karac_par_reduce` dispatch. NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported separately so the production-default Kāra behavior stays visible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra vertical (auto-par default)** | **14.1 ± 0.6 ms** | 132.2 ms |

The auto-par binary is **6.5× faster than the kāra seq binary** (92.1 → 14.1 ms), spreading the K=1M case-rotation reduction across the perf cores (~9× user-CPU-to-wall ratio on M5 Pro). This is the legitimate-win case (BENCH.md kata #4 path): a real wall-time speedup at the cost of the `karac_par_reduce` machinery's +280 KiB binary and +1.1 MiB peak RSS.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py vertical` (K=100k) | 336.5 ± 29.2 ms |

Python at K=100k is 336 ms; projecting to the compiled mirrors' K=1M (~3.37 s) puts it **~37× slower than kāra seq** — the algorithm-dominated regime where compiled-with-codegen languages put the same lap on CPython.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 vertical.c           | **57.4 ± 3.7 ms** |
| **karac build vertical.kara**  | **92.0 ± 6.4 ms** |
| rustc -O vertical.rs           | 120.7 ± 4.9 ms |

Kāra compiles **1.31× faster than `rustc -O`** and sits at **1.60× of clang -O3** — same shape as the rest of the corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    vertical            | 32.8 KiB |
| **kāra vertical (seq)**  | **81.5 KiB** |
| **kāra vertical (auto-par)** | **361.0 KiB** |
| rust vertical            | 455.9 KiB |
| go   vertical            | 2434.2 KiB |

The seq binary carries the `String` / `Vec[String]` / `Vec[Vec[String]]` runtime surface (81.5 KiB, ~2.5× C's hand-rolled char-buffer mirror). The auto-par binary adds the `karac_par_reduce` worker-pool machinery (+280 KiB → 361.0 KiB) — still well under Rust's 455.9 KiB.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    vertical            | 1.1 MiB |
| **kāra vertical (seq)**  | **1.1 MiB** |
| **kāra vertical (auto-par)** | **2.2 MiB** |
| rust vertical            | 1.2 MiB |
| go   vertical            | 9.0 MiB |

Kāra seq is **at parity with C** and below Rust on peak RSS. The auto-par regime's 2.2 MiB is the worker pool's per-thread scratch + partials.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 vertical.c          | 2.6 MiB |
| **karac build vertical.kara** | **10.9 MiB** |
| rustc -O vertical.rs          | 29.4 MiB |

Kāra's compile-memory footprint is ~4.2× clang's and ~2.7× lower than rustc's on this kata.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil.
