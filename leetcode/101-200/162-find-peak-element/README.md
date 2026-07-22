# 162. Find Peak Element

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Binary Search &nbsp;·&nbsp; **Source:** [leetcode.com/problems/find-peak-element](https://leetcode.com/problems/find-peak-element/)

Return the index of **any** peak — an element strictly greater than its neighbours (with virtual `-∞` off both ends). O(log n).

```
[1,2,3,1]           ->  2   (nums[2]=3)
[1,2,1,3,5,6,4]     ->  5   (nums[5]=6; any peak is accepted)
[1]                 ->  0
[1,2]               ->  1
[2,1]               ->  0
[1,3,2,4,1]         ->  3
```

**Constraints:** `1 ≤ n ≤ 1000`, adjacent elements differ, `nums[-1] = nums[n] = -∞`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **slope binary search** ★ | [`find_peak.kara`](find_peak.kara) ✓ | [`find_peak.py`](find_peak.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Binary search on the local slope. If `nums[mid] < nums[mid+1]` the array is ascending at `mid`, so a peak must lie strictly to the right (keep climbing) — `lo = mid + 1`. Otherwise `mid` sits on a non-ascending slope and a peak lies at `mid` or to its left — `hi = mid`. The invariant "a peak exists in `[lo, hi]`" holds because the ends act as `-∞`, so the walls always rise inward; when `lo == hi` that index is a peak. The kata's oracle fixes one deterministic peak per input (any valid peak would be accepted on LeetCode).

## Kāra features exercised

- **Overflow-safe midpoint** `lo + (hi - lo) / 2` and a `nums[mid] < nums[mid + 1]` neighbour compare driving the binary search.

## Running

```bash
karac run   find_peak.kara
karac build find_peak.kara && ./find_peak
python3 find_peak.py
diff <(karac run find_peak.kara) <(python3 find_peak.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only (O(log n) search).
