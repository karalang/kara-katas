# 179. Largest Number

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · String · Greedy · Sorting · Comparator &nbsp;·&nbsp; **Source:** [leetcode.com/problems/largest-number](https://leetcode.com/problems/largest-number/)

Arrange a list of non-negative integers so their concatenation forms the **largest** possible number; return it as a string.

```
[10,2]          ->  "210"
[3,30,34,5,9]   ->  "9534330"
[0,0]           ->  "0"
```

**Constraints:** `1 ≤ n ≤ 100`, `0 ≤ nums[i] ≤ 2³¹-1`. The result can be very long, so it is returned as a string.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **concatenation-comparator sort** ★ | [`largest_number.kara`](largest_number.kara) | [`largest_number.py`](largest_number.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The entire problem is the **comparator**. To decide whether `a` should come before `b`, don't compare the numbers — compare the two concatenations: `a` precedes `b` iff `a·b ≥ b·a` (as strings). `"3"·"30" = "330"` beats `"30"·"3" = "303"`, so `3` sorts first. Because `a·b` and `b·a` are the same length, lexicographic string order equals numeric order, and this pairwise rule is a consistent total order. Sort the string forms descending under it, concatenate, and collapse the all-zeros case (a leading `"0"` means every value was 0, so the answer is just `"0"`).

## Kāra features exercised

- **Custom-comparator sort on `Vec[String]`** — an insertion sort whose comparison is `strs[j-1] + strs[j] < strs[j] + strs[j-1]` (two fresh `String` concatenations per compare) driving a **three-way element swap** `let tmp = strs[j-1]; strs[j-1] = strs[j]; strs[j] = tmp;`. That heap-`String`-element swap-in-a-loop is a known leak-class surface (the `Vec[String]` reassign family); verified valgrind-clean.
- **`String` `+` concatenation and `<` comparison** on indexed elements.
- **`f"{x}"` int→string** and `String.push_str` for the join.

## Running

```bash
karac run   largest_number.kara
karac build largest_number.kara && ./largest_number
python3 largest_number.py
diff <(karac run largest_number.kara) <(python3 largest_number.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
