# 217. Contains Duplicate

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · Hash Table · Set &nbsp;·&nbsp; **Source:** [leetcode.com/problems/contains-duplicate](https://leetcode.com/problems/contains-duplicate/)

Return `true` if any value appears **at least twice** in the array, and `false` if every element is distinct.

```
[1,2,3,1]              ->  true
[1,2,3,4]              ->  false
[1,1,1,3,3,4,3,2,4,2]  ->  true
```

**Constraints:** `1 ≤ nums.length ≤ 10⁵`, `-10⁹ ≤ nums[i] ≤ 10⁹`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **hash-set membership** ★ | [`contains_duplicate.kara`](contains_duplicate.kara) | [`contains_duplicate.py`](contains_duplicate.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Walk the array once, keeping a `Set[i64]` of the values seen so far. Before inserting each value, check whether it is already present — the first time that check succeeds you've found a repeat and can return `true` immediately. If the scan completes with every value inserted exactly once, there are no duplicates. O(n) time, O(n) space.

## Kāra features exercised

- **`Set[i64]`** — `Set.new()`, `contains(x) → bool` membership test, and `insert(x)`, the hash-set primitive (Set lowers to `Map[T, ()]` in the runtime).
- **Early-exit scan over a `Slice[i64]`** — returns on the first repeat rather than counting everything.

## Running

```bash
karac run   contains_duplicate.kara
karac build contains_duplicate.kara && ./contains_duplicate
python3 contains_duplicate.py
diff <(karac run contains_duplicate.kara) <(python3 contains_duplicate.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
