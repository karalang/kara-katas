# 163. Missing Ranges

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array &nbsp;·&nbsp; **Source:** [leetcode.com/problems/missing-ranges](https://leetcode.com/problems/missing-ranges/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Given a **sorted** array `nums` of distinct integers all within the inclusive bounds `[lower, upper]`, return the smallest sorted list of ranges that cover **every number in `[lower, upper]` missing from `nums`**. A range prints as `"a"` for a single number, else `"a->b"`.

```
nums=[0,1,3,50,75], lower=0, upper=99  ->  2, 4->49, 51->74, 76->99
nums=[],            lower=1, upper=1   ->  1
nums=[-1,0,1,2],    lower=-1, upper=2  ->  (nothing missing)
```

**Constraints:** `nums` sorted ascending, distinct, all in `[lower, upper]`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **cursor sweep + upper sentinel** ★ | [`missing_ranges.kara`](missing_ranges.kara) ✓ | [`missing_ranges.py`](missing_ranges.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Track `prev` — the last number accounted for — initialised to `lower - 1`. Sweep each element, plus a virtual `upper + 1` sentinel at the end. Whenever the gap `cur - prev` is at least 2, the numbers strictly between them are missing, so emit the range `[prev+1, cur-1]`; then advance `prev = cur`. The sentinel makes the trailing gap up to `upper` fall out of the same rule with no special case. O(n) time.

## Kāra features exercised

- **`Vec[String]` accumulation** — each range is formatted and pushed; the caller joins them with `", "` via `String.push_str`. Exercises heap-`String`-element `Vec` growth and cleanup (the reassign/leak class this corpus stress-tests) — verified valgrind-clean.
- **`f"{lo}->{hi}"` interpolation** and the `"a"` single-number branch.
- **`if`-expression** for the sentinel: `let cur = if i < n { nums[i] } else { upper + 1 }`.
- **`Slice[i64]` parameter** fed from `Array[i64, N]` literals, including the empty-array `Array[i64, 0]` case.

## Running

```bash
karac run   missing_ranges.kara
karac build missing_ranges.kara && ./missing_ranges
python3 missing_ranges.py
diff <(karac run missing_ranges.kara) <(python3 missing_ranges.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
