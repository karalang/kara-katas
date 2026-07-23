# 167. Two Sum II - Input Array Is Sorted

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Two Pointers · Binary Search &nbsp;·&nbsp; **Source:** [leetcode.com/problems/two-sum-ii-input-array-is-sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

Given a **1-indexed sorted** array with exactly one solution, return the two **1-based** indices whose values sum to `target`.

```
[2,7,11,15], target=9  ->  1 2
[2,3,4],     target=6  ->  1 3
[-1,0],      target=-1 ->  1 2
```

**Constraints:** `2 ≤ n`, sorted non-decreasing, exactly one solution, O(1) extra space.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **two-pointer sweep** ★ | [`two_sum_ii.kara`](two_sum_ii.kara) ✓ | [`two_sum_ii.py`](two_sum_ii.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Because the array is **sorted**, the classic hash-map [Two Sum](../../1-100/1-two-sum/) collapses to an O(1)-space two-pointer sweep. Start `lo` at the front, `hi` at the back. If `nums[lo] + nums[hi]` equals the target, we're done. If the sum is too **low**, the only way to increase it is to move `lo` right (to a larger value); if too **high**, move `hi` left. Each step discards a value that can't be part of any solution, so the pointers meet in O(n).

## Kāra features exercised

- **`Slice[i64]` two-pointer walk** with `.len()`-derived bounds — no allocation, O(1) space.
- **`Array[i64, 2]` return** of the 1-based index pair, printed with `f"{r[0]} {r[1]}"`.
- **`Array[i64, N]` → `Slice[i64]`** argument passing across several fixed-size literals.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`400987230`). Workload: build-once 20K-elem sorted PRNG array + 20K two-pointer two-sum sweeps for guaranteed-solution PRNG targets (loop-carried lo/hi convergence, data-dependent branch, non-vectorizing); sink = sum of 1-based index pairs.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Go | 156.2 ms | 0.32× |
| C `clang -O3` | 465.9 ms | 0.94× |
| Rust `-O` | 466.5 ms | 0.94× |
| **Kāra (codegen)** | 495.2 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 498.1 ms | 1.01× |
| Python (scale lane) | 9.38 s | 18.95× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   two_sum_ii.kara
karac build two_sum_ii.kara && ./two_sum_ii
python3 two_sum_ii.py
diff <(karac run two_sum_ii.kara) <(python3 two_sum_ii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
