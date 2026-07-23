# 154. Find Minimum in Rotated Sorted Array II

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · Binary Search &nbsp;·&nbsp; **Source:** [leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/)

A sorted array rotated at an unknown pivot, **with duplicates** — find the minimum.

```
[1,3,5]            ->  1
[2,2,2,0,1]        ->  0
[3,4,5,1,2]        ->  1
[2,2,2,2,2]        ->  2
[1]                ->  1
[10,1,10,10,10]    ->  1
```

**Constraints:** `1 ≤ n ≤ 5000`, `-5000 ≤ nums[i] ≤ 5000`; the array was originally sorted ascending then rotated `1..n` times, and may contain duplicates.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **binary search vs `nums[hi]`, tie-shrink** ★ | [`find_min.kara`](find_min.kara) ✓ | [`find_min.py`](find_min.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The minimum lives in the *unsorted* half. Compare `nums[mid]` to `nums[hi]`:

- `nums[mid] > nums[hi]` — the pivot is strictly right of `mid`, so `lo = mid + 1`.
- `nums[mid] < nums[hi]` — `mid` could be the minimum, so `hi = mid`.
- `nums[mid] == nums[hi]` — can't tell which half holds the pivot, so **shrink `hi` by one**. The discarded `nums[hi]` is duplicated at `mid`, so the minimum is never lost. This is the only difference from the duplicate-free [#153](../153-find-minimum-in-rotated-sorted-array/), and it degrades the worst case (all equal) to O(n); otherwise O(log n).

## Kāra features exercised

- **Overflow-safe midpoint** `lo + (hi - lo) / 2` and a three-way `if`/`else if`/`else` on the `nums[mid]` vs `nums[hi]` comparison.
- **`Vec[i64]` index reads** driving the search bounds.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`37458073070`). Workload: binary-search min of many PRNG rotated-with-duplicates arrays, sum of mins sink.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Rust `-O` | 372.8 ms | 0.95× |
| C `clang -O3` | 375.2 ms | 0.96× |
| **Kāra (codegen)** | 392.0 ms | 1.00× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 403.9 ms | 1.03× |
| Go | 759.0 ms | 1.94× |
| Python (scale lane) | 38.64 s | 98.55× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   find_min.kara
karac build find_min.kara && ./find_min
python3 find_min.py
diff <(karac run find_min.kara) <(python3 find_min.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only (a small O(log n) search, not a compute benchmark).
