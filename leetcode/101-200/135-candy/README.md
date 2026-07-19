# 135. Candy

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · Greedy &nbsp;·&nbsp; **Source:** [leetcode.com/problems/candy](https://leetcode.com/problems/candy/)

Children in a line with `ratings`; each needs `≥ 1` candy, and any child with a strictly higher rating than a neighbour must get more than that neighbour. Return the minimum total candies.

```
[1,0,2]  ->  5   (2,1,2)
[1,2,2]  ->  4   (1,2,1)
```

**Constraints:** `1 ≤ n ≤ 2·10⁴`, `0 ≤ ratings[i] ≤ 2·10⁴`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Two greedy passes** ★ | O(n) time, O(n) space | [`candy.kara`](candy.kara) ✓ | [`candy.py`](candy.py) ✓ |

`✓` runs end-to-end today across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), agreeing with the Python mirror. Validated against known cases plus deterministic-LCG inputs. Zero diagnostics, valgrind-clean.

## The mechanism

Start everyone at `1`. A **left-to-right** pass enforces the "greater than my left neighbour" rule (`c[i] = c[i-1] + 1`). A **right-to-left** pass enforces "greater than my right neighbour" while keeping the left result — `c[i] = max(c[i], c[i+1] + 1)`. Because each constraint is only ever satisfied by *raising* a value, the two monotone passes converge on the minimum feasible assignment; the sum is the answer.

## Kāra features exercised

- **`Vec[i64]` candy array with index-assign** in both directions (`c[i] = c[i-1] + 1`, `c[i] = c[i+1] + 1`).
- **Descending loop** for the right-to-left pass (`i = n-2; while i >= 0 { … i = i - 1 }`) — the reverse-index shape whose bounds-check elision landed in kara `B-2026-07-17-1`.
- **Owned `Vec[i64]` input** consumed into the two-pass scan; `mut ref i64` sink via a `report` helper.

## Running

```bash
karac run   candy.kara
karac build candy.kara && ./candy
python3 candy.py
diff <(karac run candy.kara) <(python3 candy.py) && echo OK
```

## Notes

Dogfood-first greedy kata pairing a forward and a **descending** index-assign pass; verified on every surface.
