# 14. Longest Common Prefix

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** String, Trie &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-common-prefix](https://leetcode.com/problems/longest-common-prefix/)

Given an array of strings `strs`, return the longest common prefix shared by all of them. If there is no common prefix, return the empty string `""`.

**Constraints:** `1 ≤ strs.length ≤ 200`, `0 ≤ strs[i].length ≤ 200`, `strs[i]` consists of lowercase English letters.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Vertical scanning (column-by-column) | O(S) time, O(1) extra (+ output) | [`vertical.kara`](vertical.kara) ✓ | [`vertical.py`](vertical.py) ✓ |

`✓` runs end-to-end today under `karac run` (tree-walk) **and** `karac build` (AOT, default auto-par and `KARAC_AUTO_PAR=0` alike), byte-identical to the Python mirror. `S` is the total number of characters scanned, bounded by `min-length × count`.

> **Compiler bug surfaced & fixed by this kata.** The `String.push(char)` prefix-rebuild loop (and the bench's `make_string` char-push loop) was mis-lowered through the Vec *tabulate* reduction path under `karac build`: a `String` shares `Vec`'s `{ptr,len,cap}` layout, so the lowering reserved `trip_count × 1` bytes and did fixed-stride element stores, but each `push` writes a 4-byte char slot — a silent 3-bytes-per-char heap-buffer-overflow (valgrind: `Invalid write of size 4`). It ran clean only under the interpreter, so this row was previously marked `✓ via karac run` only. Fixed in the compiler ([kara `B-2026-07-18-15`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)) — a String accumulator now bails out of the tabulate/Collect lowerings to the correct per-push codegen. The kata now builds and is valgrind/ASAN-clean.

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
# Kāra — interpreter and codegen produce the same output today.
karac run   vertical.kara
karac build vertical.kara && ./vertical

# Python (3.10+ for PEP 604 union syntax)
python3 vertical.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`vertical.{kara,rs,c,py}`, `go-seq/main.go`, and the par-lane mirrors `rayon/`, `go-par/`, `vertical_par.c`).

**Workload.** M = 8 distinct test cases, each a `Vec[String]` of N = 16 strings sharing a prefix of a different length (0, 2, 4, 7, 10, 13, 16, 20). Built once into a `Vec[Vec[String]]` before the timed loop. Each case's N strings begin with the first `prefix_len` letters of the alphabet, then string `s` diverges with six copies of its signature letter (the `s`-th letter), so the strings agree on exactly `prefix_len` columns and the LCP is exactly `prefix_len`. K = 1,000,000 outer iterations rotate `idx = k % M` and call `longest_common_prefix` on that case, so the call is never loop-invariant (LLVM can't hoist it) and the input distribution sweeps the full range of prefix lengths the vertical scan can hit. The sink is the running total of every returned prefix's length = `(K / M) × (0+2+4+7+10+13+16+20)` = `125000 × 72` = **9,000,000**; all five mirrors must agree before any timing begins. This is the same shape class as kata 13 / 71 (per-iter work + one small output `String` alloc per call), so cross-kata wall-time comparisons stay meaningful.

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + r.len()` accumulator is the slice-1 allow-list reduction shape, so `karac build` may emit a `karac_par_reduce` dispatch by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — and reports them in separate tables per the two-lane discipline.

### Runtime — seq lane

M5 Pro, measured 2026-10-31 with karac `g6697158fa` (the v2/MIR backend; [`bench/results.json`](bench/results.json) `measured_at` 2026-11-01T00:56Z UTC), hyperfine `--warmup 5 --runs 30 --shell=none`. All comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time |
|---|---|
| go   vertical            | **65.5 ± 2.9 ms** |
| c    vertical (clang -O3)| 72.4 ± 4.3 ms |
| rust vertical (overflow-checks=on) | 85.2 ± 3.3 ms |
| rust vertical            | 85.3 ± 4.8 ms |
| **kāra vertical (seq)**  | **95.6 ± 4.3 ms** |

Kāra runs **1.12× of Rust** (both `rustc -O` and the equal-safety `overflow-checks=on` row), **1.32× of clang -O3** and **1.46× of Go** on the seq lane. Against the previous feed (legacy backend, 2026-07-28: 1.01× Rust, 1.23× C, 1.40× Go) that is a slip of 1.10× relative to Rust but only 1.07× relative to C and 1.04× relative to Go — **borderline**: right at the 10% line against one comparator and inside noise against the other two, so it is not clear from this run alone that MIR is slower here. Every comparator ran 2–8% slower this session (machine state), so compare ratios, not ms. *(History: the 2026-06-05 legacy snapshot read ~1.2× of Rust / ~1.4× of clang, and 2026-05-29 read 1.12× / 1.37× from byte-identical rust/c binaries — the ratio has drifted batch-to-batch across that whole range.)* The workload is String-construction-heavy — every call rebuilds the prefix one `char` at a time via `String.push` over a `chars()` iterator, and the column scan calls `.bytes()` on each `Vec[String]` element per inner iteration. The gap to Rust is the per-`char` push + iterator-advance cost through the runtime's `String` machinery (Rust's `String::push` over `chars()` lowers to a tighter inlined loop); the gap to C/Go adds the absence of a raw `memcpy`-style prefix copy. These are general-runtime costs the kata exercises heavily, not per-kata regressions.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible; the default `karac build` recognizes it and emits a `karac_par_reduce` dispatch — verified in the emitted IR (`KARAC_MIR_LL`): the default build carries a call of `karac_mir_task_spawn` and the `KARAC_AUTO_PAR=0` twin does not. NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported against in-lane parallel comparators (`rayon::par_iter`, C pthreads, goroutines + WaitGroup over the same outer reduction), hyperfine `--runs 50`:

| Implementation | Wall time | User-CPU |
|---|---|---|
| c    vertical (pthreads) | **11.5 ± 1.0 ms** | 135.7 ms |
| go   vertical (goroutines + WaitGroup) | 11.8 ± 0.7 ms | 87.5 ms |
| rust vertical (rayon `par_iter`) | 13.5 ± 1.5 ms | 180.5 ms |
| **kāra vertical (auto-par default)** | **15.4 ± 1.4 ms** | 171.9 ms |

Kāra is last in the par lane: **1.15× of rayon**, **1.35× of C pthreads**, **1.31× of Go**. Against the 2026-07-28 feed (1.06× rayon, 1.23× C, 1.49× Go) it gained on Go and slipped 8–10% against rayon and C, near the noise line on a ~15 ms workload.

The auto-par binary is **6.2× faster than the kāra seq binary** (95.6 → 15.4 ms), spreading the K=1M case-rotation reduction across the cores (~11× user-CPU-to-wall ratio on M5 Pro). This is the legitimate-win case (BENCH.md kata #4 path): a real wall-time speedup at the cost of the `karac_par_reduce` machinery's +81.3 KiB binary and +1.0 MiB peak RSS.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py vertical` (K=100k) | 298.6 ± 1.1 ms *(last measured 2026-06-05, not re-run)* |

Python at K=100k is 299 ms; projecting to the compiled mirrors' K=1M (~2.99 s) puts it **~31× slower than kāra seq** (the 2026-06-05 Python figure against the 2026-10-31 kāra row, so cross-session) — the algorithm-dominated regime where compiled-with-codegen languages put the same lap on CPython.

### Compile elapsed (cold)

Same session, `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 vertical.c           | **57.2 ± 1.4 ms** |
| rustc -O vertical.rs           | 118.9 ± 2.0 ms |
| **karac build vertical.kara**  | **186.3 ± 2.3 ms** |

Kāra compiles **1.57× slower than `rustc -O`** and sits at **3.26× of clang -O3**. *(History, 2026-06-05, legacy backend: karac compiled in 83.8 ms, 1.43× faster than `rustc -O` and 1.57× of clang -O3.)*

### Binary size

| Implementation | Size |
|---|---|
| c    vertical            | 32.8 KiB |
| **kāra vertical (seq)**  | **295.8 KiB** |
| **kāra vertical (auto-par)** | **377.1 KiB** |
| rust vertical            | 455.9 KiB |
| go   vertical            | 2434.2 KiB |

Every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (tracked as kara ledger `B-2026-10-28-36`); the seq binary here — `String` / `Vec[String]` / `Vec[Vec[String]]` runtime surface included — is 295.8 KiB. The auto-par binary adds the `karac_par_reduce` worker-pool machinery (+81.3 KiB → 377.1 KiB) — still under Rust's 455.9 KiB. *(History, 2026-06-05, legacy backend: seq 33.5 KiB, +672 bytes over C's hand-rolled char-buffer mirror; auto-par +262.7 KiB → 296.2 KiB.)*

> **Correction vs the 2026-05-29 snapshot.** That snapshot read 81.5 KiB (seq) / 361.0 KiB (auto-par): the runtime archive linked that day had been rebuilt with plain `cargo build` (rlib + staticlib co-emit defeats fat-LTO DCE), so std's ~48 KiB DWARF backtrace symbolizer survived `-dead_strip` into both kāra binaries — an identical +49,616 B on each lane. Rebuilt per the documented `cargo rustc … --crate-type staticlib` discipline, both lanes shed exactly that delta. The 2026-06-05 numbers were the true legacy-backend floor.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    vertical            | 1.0 MiB |
| **kāra vertical (seq)**  | **1.1 MiB** |
| **kāra vertical (auto-par)** | **2.1 MiB** |
| rust vertical            | 1.1 MiB |
| go   vertical            | 8.5 MiB |

Kāra seq is **at parity with C and Rust** on peak RSS (1,130,832 vs 1,098,040 / 1,114,424 bytes — within two 16-KiB pages). The auto-par regime's 2.1 MiB is the worker pool's per-thread scratch + partials, between C pthreads' 1.9 MiB and rayon's 2.5 MiB (goroutines: 10.9 MiB).

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 vertical.c          | 2.6 MiB |
| rustc -O vertical.rs          | 29.3 MiB |
| **karac build vertical.kara** | **61.4 MiB** |

Kāra's compile-memory footprint is ~24× clang's and ~2.1× higher than rustc's on this kata. *(History, 2026-06-05, legacy backend: 13.9 MiB, ~2.1× lower than rustc.)*

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil.
