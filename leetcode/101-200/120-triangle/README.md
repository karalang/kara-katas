# 120. Triangle

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/triangle](https://leetcode.com/problems/triangle/)

Given a `triangle` array, return the **minimum path sum** from top to bottom. Each step you may move to an **adjacent** number of the row below — from index `j` you go to `j` or `j+1`. The O(n)-space trick is a **bottom-up rolling row**, a close cousin of [#119](../119-pascals-triangle-ii/): where #119 rolled one row forward with `+`, this one rolls it *upward* with `min`.

```
triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]

    2          the minimum path is  2 -> 3 -> 5 -> 1  =  11
   3 4
  6 5 7
 4 1 8 3

one rolling row, collapsed upward:   dp[k] = triangle[i][k] + min(dp[k], dp[k+1])
```

**Constraints:** `1 ≤ triangle.length ≤ 200`, `-10⁴ ≤ triangle[i][j] ≤ 10⁴` — every path sum fits a signed 64-bit integer.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Bottom-up rolling row** ★ | [`triangle.kara`](triangle.kara) ✓ | [`triangle.py`](triangle.py) ✓ |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the Kāra solver agrees with the Python mirror. An independent **ground-truth check** confirms the answer three ways: the bottom-up rolling recurrence equals an independent top-down DP *and* a brute-force minimum over all top-to-bottom paths, on many random triangles. Zero disagreements. The solver compiles with zero diagnostics and is valgrind-clean.

## The mechanism

**Bottom-up rolling** ([`triangle.kara`](triangle.kara), the ★): seed a single `Vec[i64]` `dp` with the triangle's **base row**, then for each row `i` from the second-to-last **up** to the apex, collapse it in place — `dp[k] = triangle[i][k] + min(dp[k], dp[k+1])` for `k` in `0..=i`. Rolling upward keeps each `dp[k]` valid: when row `i` reads `dp[k]` and `dp[k+1]`, both still hold the best sums from the row below. `dp[0]` is the answer. O(n) space, O(n²) time — the `triangle` (a `Vec[Vec[i64]]`) is read-only and the surface is **nested indexing** `triangle[i][k]` feeding a rolling-1D **min**-DP (distinct from #119's single-row add-roll).

## Kāra features exercised

- **Nested index read** — `triangle[i][k]` double-indexes a `Vec[Vec[i64]]` on the hot path; kāra's bounds-check elision proves `k ≤ i < n` and `k < triangle[i].len()` from the `while k <= i` guard and drops the inner checks (see Benchmarks).
- **Rolling-1D min-DP** — `dp[k] = triangle[i][k] + min(dp[k], dp[k+1])`, an in-place collapse that reads two neighbours and writes one back, the `min` lowering to a branchless conditional-move.
- **Row-by-row nested-`Vec` construction** — the triangle is built with `while … { let mut row = Vec.new(); …; tri.push(row) }`. That natural shape surfaced a spurious RC fallback on the freshly-`let` loop-local `row` — fixed in the compiler ([kara `B-2026-07-17-16`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)), not worked around here.

**v1 note.** Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; agrees with the Python mirror and the top-down + brute-force ground truth, and is valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   triangle.kara
karac build triangle.kara && ./triangle

# Python
python3 triangle.py

# Verify they agree
diff <(karac run triangle.kara) <(python3 triangle.py) && echo OK

# Ground truth: bottom-up == top-down == brute force
python3 ground_truth.py
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`triangle.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** The canonical numbers below are the corpus's **Apple M5 Pro** run (6P+12E, Darwin 25.6.0; **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). Against the 2026-07-27 legacy-backend M5 feed: kāra is flat against every comparator (each move under this session's ~10 % noise band): kāra/Rust 0.81× → 0.79×, kāra/equal-safety Rust 0.87× → 0.85×, kāra/C 3.53× → 3.51×, kāra/Go 0.93× → 0.93×. This is not a compiler regression: the seq (`KARAC_AUTO_PAR=0`) MIR build's instructions and cycles are identical to legacy dd86e3955's (6.884G vs 6.880G instructions). The default (auto-par) build is slower; see [Bug ledger](#bug-ledger). An earlier shared **x86-64 Linux cloud-container** run, which this section originally reported as canonical, is kept below as history ([`bench/results.container-x86.json`](bench/results.container-x86.json)); absolute times/sizes/RSS are **not** comparable across the two hosts, only within-file cross-language ratios are the signal.

**Workload.** A **build-once + punch** design: build one `Vec[Vec[i64]]` triangle of `N = 200` rows once, then run the O(N²) min-path DP **K = 20,000** times with a **data-dependent seed** (`seed = acc % 97`, perturbing the base row *non-uniformly* — `dp[j] = base[j] + (seed+j)%7` — so the winning path shifts each rep and the DP can't be hoisted), folding every result. Dominated by the O(N²) `dp[k] = triangle[i][k] + min(dp[k], dp[k+1])` collapse — the rolling-1D min-DP regime, over read-only nested indexing.

**Node representation & equal safety.** Kāra `Vec[Vec[i64]]`, Rust `Vec<Vec<i64>>`, Go `[][]int64`, C a `long*[]` (one `malloc` per row). Kāra checks integer overflow **and** array bounds by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on overflow.

**Apple M5 Pro numbers, karac g6697158fa, 2026-11-01** (canonical; seq lane, `KARAC_AUTO_PAR=0`; hyperfine, 30 runs; sink `487297205` agreed by all five mirrors). All single-threaded, ~99.5 % CPU (the seq build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`); Go 102 %).

| Implementation | Wall time | Store |
|---|---|---|
| c    triangle (clang -O3)                    | 64.3 ± 1.5 ms | `long*[]` |
| **kāra triangle**                            | **225.8 ± 2.3 ms** | **`Vec[Vec[i64]]`** |
| go   triangle (`[][]int64`)                  | 243.8 ± 4.3 ms | `[][]int64` |
| rust triangle (rustc -O, overflow-checks=on) | 265.0 ± 12.2 ms | `Vec<Vec<i64>>` |
| rust triangle (rustc -O)                     | 286.0 ± 5.1 ms | `Vec<Vec<i64>>` |

**On the M5 (2026-11-01, v2/MIR) Kāra is second of five: ahead of Go and both Rust builds, far behind C.** Kāra is **0.79× `rustc -O`** (1.27× ahead), **0.85× the equal-safety Rust row** (1.17× ahead), **0.93× Go** (1.08× ahead) and **3.51× behind C** — the same ordering as the 2026-07-27 legacy-backend feed (0.81×, 0.87×, 0.93×, 3.53×). The C-parity result of the container analysis below does not hold on the M5. kāra holds **1.33 MiB** peak RSS (Rust 1.36, C 1.25; Go 9.5 MiB). Binary size: c 32.7 KiB, **kāra 295.8 KiB**, rust 455.6 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (the legacy M5 kāra binary here was 33.7 KiB), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Compile-cold on the M5 is clang 53.1 ms < rustc 107.1 ms < **karac 162.3 ms** (3.1× clang, 1.52× rustc).

**Default (auto-par) build.** Plain `karac build` is 1.10× slower than the seq lane (249.9 vs 228.2 ms, same session): auto-par takes `main`'s one-off 200-row triangle-build loop and adds ~2.0G instructions with 2 or more workers. Filed as [`B-2026-11-01-23`](../../../../kara/docs/bugs-v2.md); the harness therefore times the `KARAC_AUTO_PAR=0` build.

`--warmup 8 --runs 40`. All single-threaded. **x86-64 container numbers** (history: the earlier, undated container run this section first reported):

| Implementation | Wall time | Store |
|---|---|---|
| c    triangle (clang -O3)                    | 363 ± 10 ms | `long*[]` |
| **kāra triangle**                            | **367 ± 12 ms** | **`Vec[Vec[i64]]`** |
| go   triangle (`[][]int64`)                  | 564 ± 33 ms | `[][]int64` |
| rust triangle (rustc -O)                     | 574 ± 21 ms | `Vec<Vec<i64>>` |
| rust triangle (rustc -O, overflow-checks=on) | 653 ± 20 ms | `Vec<Vec<i64>>` |

**On the container Kāra tied C (1.01×) and was 1.56× ahead of `rustc -O` — even though kāra keeps both overflow *and* bounds checks and this Rust row keeps neither.** The win is bounds-check elision on the nested index. asm isolation of the hot min-collapse loop:

- **kāra** emits `mov dp[k+1]; cmp dp[k]; cmovl` (a **branchless** `min`), `add triangle[i][k]`, `jo <panic>` (the overflow check), `mov → dp[k]` — **no** `ja <panic>` bounds check on any of `dp[k]`, `dp[k+1]`, or `triangle[i][k]`. The `while k <= i` guard proves `k ≤ i < n ≤ dp.len()`, and `k ≤ i < triangle[i].len()`, so kāra's BCE drops all three inner checks; the whole binary carries 11 panic sites.
- **`rustc -O`** keeps the nested-`Vec<Vec>` bounds checks — indexing `tri[i]` then `[k]`, plus `dp[k]`/`dp[k+1]`, don't all fold through the `for k in 0..=i` range, so the inner loop retains bounds branches (the binary carries ~300 panic sites). That, not overflow, is the gap: the equal-safety `overflow-checks=on` row is only ~14% behind plain `-O`, while both trail kāra.

Verified correct (all compiled mirrors agree on the sink) and valgrind-clean. Python (pure-Python, ~20× slower per rep, run at a fraction of K, timed separately, not cross-checked) is not comparable and omitted from the table.

**Flagged for the M5 re-bench** — container orderings can shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)); treat the *margins* as data points. The load-bearing result — kāra at C parity, ahead of equal-safety Rust, because its BCE elides the nested-index checks Rust keeps — is an asm-level fact, not a microarchitectural quirk. (2026-11-01 note: on the M5 Kāra is still ahead of equal-safety Rust, 0.85×, but 3.51× behind C, not at parity; the asm analysis above was on the legacy backend and has not been re-checked on v2/MIR.)

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at a matched nested-index rolling min-DP (`Vec[Vec[i64]]` vs `Vec<Vec<i64>>`). This kata is a case where the ratio runs Kāra's way: its bounds-check elision proves the nested index in-range from the loop guard and drops the checks, landing at C parity on the container while idiomatic Rust keeps them (on the M5, 2026-11-01, v2/MIR: 0.79× Rust, 3.51× C). C's `long*[]` is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.

## Bug ledger

**Surfaced [`B-2026-11-01-23`](../../../../kara/docs/bugs-v2.md)** (perf, open). The default (auto-par) build parallelizes `main`'s one-off 200-row triangle-build loop (the task returns `Vec[Vec[i64]]`), not the punch loop, and with 2 or more workers runs ~2.0G extra instructions (6.88G → 8.89–9.00G, flat from 2 to 18 workers): 249.9 ms vs the `KARAC_AUTO_PAR=0` build's 228.2 ms (1.10× slower, 39 ms system time). Measured 2026-11-01 with karac g6697158fa.
