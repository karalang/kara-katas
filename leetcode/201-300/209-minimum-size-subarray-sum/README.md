# 209. Minimum Size Subarray Sum

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Sliding Window · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/minimum-size-subarray-sum](https://leetcode.com/problems/minimum-size-subarray-sum/)

Given a positive integer `target` and an array of **positive** integers, return the minimal length of a contiguous subarray whose sum is `≥ target`. If no such subarray exists, return `0`.

```
target = 7,  [2,3,1,2,4,3]   ->  2    ([4,3])
target = 4,  [1,4,4]         ->  1    ([4])
target = 11, [1,1,1,1,1,1,1,1]  ->  0    (total is only 8)
```

**Constraints:** `1 ≤ target ≤ 10⁹`, `1 ≤ nums.length ≤ 10⁵`, `1 ≤ nums[i] ≤ 10⁴`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **two-pointer sliding window** ★ | [`min_subarray.kara`](min_subarray.kara) | [`min_subarray.py`](min_subarray.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

All elements are **positive**, which is what makes a single sliding window sufficient: extending the window can only *raise* the sum and contracting it can only *lower* the sum, so the two pointers never need to backtrack. Advance `right`, adding each value to a running sum; as soon as the window sum reaches `target`, it's a candidate — record its length, then advance `left`, subtracting the departing value, shrinking as far as the sum stays `≥ target`. The minimal length ever recorded is the answer (`0` if the window never qualifies). Each index enters and leaves the window exactly once, so the whole scan is O(n).

## Kāra features exercised

- **`Slice[i64]` parameter** — the array is borrowed as a slice; `Array[i64, N]` literals in `main` pass straight through with no copy.
- **Nested `while` sliding window** — an outer expand loop and an inner shrink loop sharing `sum` / `left`, the canonical two-pointer shape.
- **Sentinel-guarded minimum** — `best = -1` distinguishes "no window yet" from a real length without a separate found flag, and overflow-checked `i64` arithmetic keeps the running sum honest.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`58776`). Workload: one 200k positive-int array built once; run the O(n) sliding window for 290 targets (data-dependent shrink loop); sink = sum of answers.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 427.1 ms | 0.93× |
| Go | 444.6 ms | 0.96× |
| **Kāra (codegen)** | 461.2 ms | 1.00× |
| Rust `-O` | 540.4 ms | 1.17× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 570.3 ms | 1.24× |
| Python (scale lane) | 9.27 s | 20.09× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   min_subarray.kara
karac build min_subarray.kara && ./min_subarray
python3 min_subarray.py
diff <(karac run min_subarray.kara) <(python3 min_subarray.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
