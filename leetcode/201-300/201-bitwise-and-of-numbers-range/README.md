# 201. Bitwise AND of Numbers Range

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/bitwise-and-of-numbers-range](https://leetcode.com/problems/bitwise-and-of-numbers-range/)

Return the bitwise **AND** of all integers in the inclusive range `[left, right]`.

```
5, 7            ->  4     (5 & 6 & 7)
12, 15          ->  12
1, 2147483647   ->  0
```

**Constraints:** `0 ≤ left ≤ right ≤ 2³¹-1`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **common binary prefix** ★ | [`range_and.kara`](range_and.kara) | [`range_and.py`](range_and.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

ANDing the whole range one number at a time is O(range) — but the answer is just the **common binary prefix** of `left` and `right`. At any bit position where they differ, the lower bits sweep through every combination as you count from `left` to `right`, so that bit is `0` for at least one value and ANDs away. Shift both numbers right until they agree (stripping the differing low bits, counting the shifts), then shift the shared prefix back into place. O(log) — at most 31 shifts.

## Kāra features exercised

- **Bitwise shifts on `i64`** — `>>` to strip low bits, `<<` to restore the prefix — the whole kernel, no arithmetic that could overflow under Kāra's checked defaults.
- **Convergence loop** on `lo < hi` counting a shift amount.

## Running

```bash
karac run   range_and.kara
karac build range_and.kara && ./range_and
python3 range_and.py
diff <(karac run range_and.kara) <(python3 range_and.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
