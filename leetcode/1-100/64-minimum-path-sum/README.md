# 64. Minimum Path Sum

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/minimum-path-sum](https://leetcode.com/problems/minimum-path-sum/)

The per-cell-cost sequel to katas [#62](../62-unique-paths/) (count paths) and [#63](../63-unique-paths-ii/) (count paths around obstacles). Same `m × n` grid, same **right**/**down** moves — but now every cell carries a non-negative **cost**, and instead of *counting* paths we want the single path whose costs sum to the **least**.

```
[[1,3,1],          →  7     the route 1 → 3 → 1 → 1 → 1  (right, right, down, down)
 [1,5,1],                    sums to 7 — no other right/down path is cheaper
 [4,2,1]]

[[1,2,3],          →  12    1 → 2 → 3 → 6
 [4,5,6]]
```

**Constraints:** `1 ≤ m, n ≤ 200`; `0 ≤ grid[i][j] ≤ 200`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Rolling 1-D DP** ★ — one array spanning the columns, `dp[c] = grid[i][c] + min(dp[c], dp[c-1])` | O(m·n) time, O(n) space | [`minimum_path_sum.kara`](minimum_path_sum.kara) ✓ via `karac run` / `karac build` | [`minimum_path_sum.py`](minimum_path_sum.py) ✓ |
| **Full 2-D DP table** — materialise every cell, `best[i][j] = grid[i][j] + min(best[i-1][j], best[i][j-1])` | O(m·n) time, O(m·n) space | [`minimum_path_sum_2d.kara`](minimum_path_sum_2d.kara) ✓ | — |
| **In place** — reuse the grid itself as the DP table, `grid[i][j] += min(grid[i-1][j], grid[i][j-1])` | O(m·n) time, **O(1) extra** space | [`minimum_path_sum_inplace.kara`](minimum_path_sum_inplace.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all twelve test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and all three approaches agree with each other and with the Python mirror.

## The recurrence — swap `+` for `cost + min`

Katas #62 and #63 *summed* over both in-neighbours (count every way to arrive). Minimum Path Sum instead *chooses* the cheaper in-neighbour and pays the current cell's cost:

```
best[i][j] = grid[i][j] + min(best[i-1][j], best[i][j-1])
```

with the borders forced, since a border cell has only **one** in-neighbour:

```
best[0][0] = grid[0][0]
best[0][j] = best[0][j-1] + grid[0][j]     top row: only reachable from the left
best[i][0] = best[i-1][0] + grid[i][0]     left column: only reachable from above
```

This is exactly the generalisation #62's README flagged as forcing the DP: *"add per-cell costs (#64) and there is no closed form — the recurrence becomes mandatory."* There is no binomial and no axis symmetry to exploit; the `min` turns the problem into a shortest-path over a DAG that a single row-by-row scan solves, because every edge points right or down (so a fixed scan order always visits a cell's predecessors first).

**Rolling 1-D DP** ([`minimum_path_sum.kara`](minimum_path_sum.kara)) is the ★. As in #62/#63 the recurrence only reads the row directly above, so a **single array**, updated in place left to right, suffices:

```
dp[c]  currently holds  best[i-1][c]   (the cell above, this column)
dp[c] = grid[i][c] + min(dp[c], dp[c-1])
                         ^^^^^  ^^^^^^^
                         above   left (already advanced to this row)
```

At the instant `dp[c]` is read it still holds the row-above value (not yet overwritten this pass), while `dp[c-1]` was already advanced to the current row — the two in-neighbours the `min` chooses between. The left column has no left neighbour, so `dp[0]` just accumulates downward (`dp[0] += grid[i][0]`). Like #63, obstacles/costs break any symmetry, so the buffer spans the real column count `n` — **O(n) space**.

**Full 2-D table** ([`minimum_path_sum_2d.kara`](minimum_path_sum_2d.kara)) is the textbook form: keep the whole `Vec[Vec[i64]]` best-cost grid. It has **no aliasing subtlety** — every cell is written once, and the two it reads (`best[i-1][j]` in the finished previous row, `best[i][j-1]` earlier in this row) are final before it is reached; the borders are explicit single-in-neighbour branches. Its cost is the O(m·n) grid the rolling form trades away.

**In place** ([`minimum_path_sum_inplace.kara`](minimum_path_sum_inplace.kara)) drops the extra buffer entirely: it overwrites the **grid itself**, since a cell's predecessors (above, left) are always converted to best-costs before the cell is reached in a top-to-bottom, left-to-right scan. After the scan `grid[i][j]` holds `best[i][j]` and `grid[m-1][n-1]` is the answer — **O(1) extra** space. It is the only solver here that *writes* a `Vec[Vec[i64]]` in place (nested index-assignment `grid[i][j] = …`, the write-side counterpart to the read-only double-indexing the 2-D form uses), so it exercises a distinct codegen surface; the shared `report` harness hands each solver an owned grid, so consuming it is free.

## Kāra features exercised

- **`Vec[i64]` rolling buffer with `min`** — `Vec.new()` + `push` to seed the top row, then in-place `dp[c] = grid[i][c] + imin(dp[c], dp[c - 1])` read-modify-write indexing. The `cost + min` body is the delta from #62/#63's pure-sum RMW scan.
- **`ref Vec[Vec[i64]]` read vs owned-grid *write*** — the rolling and 2-D solvers borrow the grid (`grid: ref Vec[Vec[i64]]`) and read `grid[i][c]`; the in-place solver takes the grid **by value**, rebinds it `let mut g = grid`, and mutates nested elements `g[r][c] = …`. Read-side double-indexing is shared with katas [#54](../54-spiral-matrix/)/[#48](../48-rotate-image/); the write-side nested index-assignment is the surface #64 adds.
- **Nested array literals as test input** — `report([[1, 3, 1], [1, 5, 1], [4, 2, 1]], mut s)` builds the `Vec[Vec[i64]]` cost grids inline, the same literal-grid harness shape as katas [#54](../54-spiral-matrix/) and [#63](../63-unique-paths-ii/).
- **Shared `report`/`sums:` harness** — one answer per line plus a folded `sums:` checksum, the byte-for-byte diff anchor used across katas [#53](../53-maximum-subarray/), [#62](../62-unique-paths/), and [#63](../63-unique-paths-ii/); all three solvers and the Python mirror print it identically. The call site `min_path_sum(grid)` is verbatim across all three — an owned argument passed to a `ref` param borrows implicitly, and passed to an owned param moves, so the same call compiles against both signatures.

**v1 note — no `i64.min` / `min()` yet.** Kāra v1 has neither an `i64.min` method nor a free `min()` function: `a.min(b)` is rejected `no method 'min' on type 'i64'` and `min(a, b)` is rejected `undefined name 'min'`, both **identically under `karac run` and `karac build`** (a consistent absence — a clean diagnostic, not a run/build divergence). The corpus convention, used across katas [#42](../42-trapping-rain-water/) and [#45](../45-jump-game-ii/), is a local `fn imin(a, b) { if a < b { a } else { b } }` helper, which is what all three solvers here use. The recurrence is written in its natural `cost + min(above, left)` shape; only the `min` spelling routes through the helper. (Costs ≤ 200 with m, n ≤ 200 bound the answer to ≤ 80,000, so i64 never approaches overflow.)

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   minimum_path_sum.kara
karac build minimum_path_sum.kara && ./minimum_path_sum

# The alternative approaches (identical output):
karac run minimum_path_sum_2d.kara
karac run minimum_path_sum_inplace.kara

# Python
python3 minimum_path_sum.py

# Verify they all agree
diff <(karac run minimum_path_sum.kara) <(python3 minimum_path_sum.py)             && echo OK
diff <(karac run minimum_path_sum.kara) <(karac run minimum_path_sum_2d.kara)      && echo OK
diff <(karac run minimum_path_sum.kara) <(karac run minimum_path_sum_inplace.kara) && echo OK
```
