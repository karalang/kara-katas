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

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts, only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** A **build-once + punch** design: build one `Vec[Vec[i64]]` triangle of `N = 200` rows once, then run the O(N²) min-path DP **K = 20,000** times with a **data-dependent seed** (`seed = acc % 97`, perturbing the base row *non-uniformly* — `dp[j] = base[j] + (seed+j)%7` — so the winning path shifts each rep and the DP can't be hoisted), folding every result. Dominated by the O(N²) `dp[k] = triangle[i][k] + min(dp[k], dp[k+1])` collapse — the rolling-1D min-DP regime, over read-only nested indexing.

**Node representation & equal safety.** Kāra `Vec[Vec[i64]]`, Rust `Vec<Vec<i64>>`, Go `[][]int64`, C a `long*[]` (one `malloc` per row). Kāra checks integer overflow **and** array bounds by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on overflow.

`--warmup 8 --runs 40`. All single-threaded. **x86-64 container numbers** (canonical M5 pending):

| Implementation | Wall time | Store |
|---|---|---|
| c    triangle (clang -O3)                    | 363 ± 10 ms | `long*[]` |
| **kāra triangle**                            | **367 ± 12 ms** | **`Vec[Vec[i64]]`** |
| go   triangle (`[][]int64`)                  | 564 ± 33 ms | `[][]int64` |
| rust triangle (rustc -O)                     | 574 ± 21 ms | `Vec<Vec<i64>>` |
| rust triangle (rustc -O, overflow-checks=on) | 653 ± 20 ms | `Vec<Vec<i64>>` |

**Kāra ties C here (1.01×) and is 1.56× ahead of `rustc -O` — even though kāra keeps both overflow *and* bounds checks and this Rust row keeps neither.** The win is bounds-check elision on the nested index. asm isolation of the hot min-collapse loop:

- **kāra** emits `mov dp[k+1]; cmp dp[k]; cmovl` (a **branchless** `min`), `add triangle[i][k]`, `jo <panic>` (the overflow check), `mov → dp[k]` — **no** `ja <panic>` bounds check on any of `dp[k]`, `dp[k+1]`, or `triangle[i][k]`. The `while k <= i` guard proves `k ≤ i < n ≤ dp.len()`, and `k ≤ i < triangle[i].len()`, so kāra's BCE drops all three inner checks; the whole binary carries 11 panic sites.
- **`rustc -O`** keeps the nested-`Vec<Vec>` bounds checks — indexing `tri[i]` then `[k]`, plus `dp[k]`/`dp[k+1]`, don't all fold through the `for k in 0..=i` range, so the inner loop retains bounds branches (the binary carries ~300 panic sites). That, not overflow, is the gap: the equal-safety `overflow-checks=on` row is only ~14% behind plain `-O`, while both trail kāra.

Verified correct (all compiled mirrors agree on the sink) and valgrind-clean. Python (pure-Python, ~20× slower per rep, run at a fraction of K, timed separately, not cross-checked) is not comparable and omitted from the table.

**Flagged for the M5 re-bench** — container orderings can shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)); treat the *margins* as data points. The load-bearing result — kāra at C parity, ahead of equal-safety Rust, because its BCE elides the nested-index checks Rust keeps — is an asm-level fact, not a microarchitectural quirk.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at a matched nested-index rolling min-DP (`Vec[Vec[i64]]` vs `Vec<Vec<i64>>`). This kata is a case where the ratio runs Kāra's way: its bounds-check elision proves the nested index in-range from the loop guard and drops the checks, landing at C parity while idiomatic Rust keeps them. C's `long*[]` is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
