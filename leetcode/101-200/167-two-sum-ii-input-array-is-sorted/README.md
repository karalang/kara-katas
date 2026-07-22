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

## Running

```bash
karac run   two_sum_ii.kara
karac build two_sum_ii.kara && ./two_sum_ii
python3 two_sum_ii.py
diff <(karac run two_sum_ii.kara) <(python3 two_sum_ii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
