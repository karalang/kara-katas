# 213. House Robber II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/house-robber-ii](https://leetcode.com/problems/house-robber-ii/)

Houses are arranged in a **circle**. Robbing two adjacent houses trips the alarm, and because the layout is circular the **first and last houses are also adjacent**. Return the maximum amount that can be robbed without alerting the police.

```
[2,3,2]    ->  3    (rob house 1; can't take both ends)
[1,2,3,1]  ->  4    (houses 0 and 2)
[5]        ->  5
```

**Constraints:** `1 ≤ nums.length ≤ 100`, `0 ≤ nums[i] ≤ 1000`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **two linear DP runs** ★ | [`house_robber_ii.kara`](house_robber_ii.kara) | [`house_robber_ii.py`](house_robber_ii.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

The only new wrinkle over [#198](../../101-200/198-house-robber/) is that the ends touch. Since you can never rob both the first and last house, split into two ordinary (non-circular) House Robber problems: one that **excludes the last house** (rob within `[0, n-1)`) and one that **excludes the first** (rob within `[1, n)`). The circular optimum is whichever linear run pays more.

Each linear run is the O(1)-space rolling DP: sweep left to right holding the best total up to the previous two houses; at each house choose to **skip** it (carry the running best) or **take** it (best from two houses back plus this house). Single-house and empty inputs short-circuit before the split. O(n) time, O(1) space.

## Kāra features exercised

- **`Slice[i64]` with an explicit `[lo, hi)` window** — the two runs reuse one `rob_linear` over index ranges instead of allocating sub-slices, so no copying and no slice-of-slice.
- **`if`-expression in value position** — `let next = if take > cur { take } else { cur }` folds the max inline.
- **Rolling two-variable DP** — `prev` / `cur` advance in lockstep; overflow-checked `i64` accumulation.

## Running

```bash
karac run   house_robber_ii.kara
karac build house_robber_ii.kara && ./house_robber_ii
python3 house_robber_ii.py
diff <(karac run house_robber_ii.kara) <(python3 house_robber_ii.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
