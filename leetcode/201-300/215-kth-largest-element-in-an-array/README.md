# 215. Kth Largest Element in an Array

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Quickselect · Divide and Conquer &nbsp;·&nbsp; **Source:** [leetcode.com/problems/kth-largest-element-in-an-array](https://leetcode.com/problems/kth-largest-element-in-an-array/)

Return the **k-th largest** element in an array — by value, so duplicates count (the 2nd largest of `[3,2,3,1,2,4,5,5,6]` is `5`, not skipped). Do it without fully sorting.

```
[3,2,1,5,6,4],          k=2  ->  5
[3,2,3,1,2,4,5,5,6],    k=4  ->  4
[5,5,5,5],              k=2  ->  5
```

**Constraints:** `1 ≤ k ≤ nums.length ≤ 10⁵`, `-10⁴ ≤ nums[i] ≤ 10⁴`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **quickselect (Lomuto partition)** ★ | [`kth_largest.kara`](kth_largest.kara) | [`kth_largest.py`](kth_largest.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

In ascending order the k-th largest element lands at index `n - k`. Quickselect finds the value at a target index without sorting the rest: pick a pivot, **partition** the array so everything smaller sits left of the pivot and everything larger sits right, and note the pivot's final resting index `p`. If `p` is the target, that's the answer; otherwise recurse into **only** the side that contains the target. Discarding half the array each step gives average O(n) (worst case O(n²), fine at these sizes).

The pivot is the last element (fixed, so the run is deterministic and matches the mirror exactly). Partitioning swaps in place with Kāra's parallel assignment `a[i], a[j] = a[j], a[i]`.

## Kāra features exercised

- **In-place swap via parallel assignment** — `a[i], a[j] = a[j], a[i]` evaluates both right-hand values into temporaries before either write, a true swap of two `Vec` slots (design.md §5.13).
- **Recursion through a `mut ref Vec[i64]`** — `quickselect` and `partition` mutate one shared buffer; the fresh owned copy is passed with the call-site `mut` marker (`quickselect(mut a, …)`), while the recursive forwards carry the already-`mut ref` binding unmarked.
- **`Slice[i64]` input copied into an owned `Vec`** so the caller's array is never disturbed.

## Running

```bash
karac run   kth_largest.kara
karac build kth_largest.kara && ./kth_largest
python3 kth_largest.py
diff <(karac run kth_largest.kara) <(python3 kth_largest.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
