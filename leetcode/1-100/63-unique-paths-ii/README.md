# 63. Unique Paths II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/unique-paths-ii](https://leetcode.com/problems/unique-paths-ii/)

The obstacle sequel to kata [#62](../62-unique-paths/). A robot starts at the top-left of an `m × n` grid and may move only **right** or **down**, but some cells hold **obstacles** (marked `1`) it may not stand on (free cells are `0`). How many distinct paths reach the bottom-right corner?

```
[[0,0,0],          →  2     the center obstacle leaves exactly two routes:
 [0,1,0],                    right-right-down-down  and  down-down-right-right
 [0,0,0]]

[[0,1],            →  1     the only route is down-then-right
 [0,0]]

[[1,0],            →  0     the start cell is blocked — no path exists at all
 [0,0]]
```

**Constraints:** `1 ≤ m, n ≤ 100`; each cell is `0` or `1`; the answer is guaranteed to be `≤ 2·10⁹`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Rolling 1-D DP** ★ — one array spanning the columns, `dp[c] += dp[c-1]`, forced to `0` at an obstacle | O(m·n) time, O(n) space | [`unique_paths_ii.kara`](unique_paths_ii.kara) ✓ via `karac run` / `karac build` | [`unique_paths_ii.py`](unique_paths_ii.py) ✓ |
| **Full 2-D DP table** — materialise every cell, `paths[i][j] = paths[i-1][j] + paths[i][j-1]` (or `0` at an obstacle) | O(m·n) time, O(m·n) space | [`unique_paths_ii_2d.kara`](unique_paths_ii_2d.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all thirteen test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## The recurrence — #62's, plus one rule

Every cell still has exactly two in-neighbours — the robot arrives only from **above** or from the **left** — so the count is their sum, with one addition: a cell holding an obstacle has **zero** paths through it.

```
paths[i][j] = 0                              if grid[i][j] is an obstacle
paths[i][j] = paths[i-1][j] + paths[i][j-1]  otherwise
```

with `paths[0][0] = 1` when the start is clear (and `0` when it is blocked — then there are no paths at all). The change from kata #62 is small but it removes two things #62 relied on:

- **The top row and left column are no longer a blanket line of `1`s.** A straight run along the top row survives only up to the first obstacle; everything past it is cut off. The additive recurrence gets this for free — an obstacle zeroes `paths` there, and that `0` propagates rightward through the row-sum and downward through the column-sum, walling off exactly the unreachable region.
- **The axis symmetry `paths(m,n) == paths(n,m)` is gone.** Obstacles are not symmetric under transposition, so — unlike #62 — you cannot roll onto the *smaller* dimension; the array must span the real column count `n`. That is the one structural difference between this kata's ★ and #62's.

**Rolling 1-D DP** ([`unique_paths_ii.kara`](unique_paths_ii.kara)) is the ★. As in #62, the recurrence only ever reads the row directly above, so a **single array** updated in place, left to right, suffices:

```
dp[c]  currently holds  paths[i-1][c]   (the row above)
dp[c] += dp[c-1]        ->  paths[i-1][c] + paths[i][c-1] = paths[i][c]
```

At the instant `dp[c]` is read on the right it still holds the value from the row above (not yet overwritten this pass), while `dp[c-1]` was already advanced to the current row — exactly the two neighbours the recurrence wants. An obstacle overrides the sum with `dp[c] = 0`. The left-column cell `dp[0]` is seeded once to `1` (the single virtual path entering the corner) and thereafter is only touched to zero it at an obstacle — otherwise it carries straight down (the all-downs path). This is #62's read-before-overwrite left-to-right sweep with an obstacle guard threaded through it.

**Full 2-D table** ([`unique_paths_ii_2d.kara`](unique_paths_ii_2d.kara)) is the textbook form: keep the whole `Vec[Vec[i64]]` grid of path counts. It has **no aliasing subtlety at all** — every cell is written once, and the two cells it reads (`paths[i-1][j]` in the finished previous row, `paths[i][j-1]` earlier in this row) are final before it is reached. Absent neighbours (the top row's `i-1`, the left column's `j-1`) simply contribute `0`, so the single additive rule covers the borders too — no separate "seed the first row/column" pass, precisely because past the first obstacle those borders are *not* all-`1`s. Its cost is the O(m·n) grid the rolling form trades away for O(n); keeping it here shows the space optimisation as a diff and cross-checks the recurrence independently.

### Why there is no third (closed-form) approach

Kata #62 had a third solver — the closed-form binomial `C(m+n-2, m-1)` — that dropped the DP entirely. **That option is gone here, and its absence is the point.** With arbitrary obstacles there is no product formula for the count: which routes survive depends on *where* the obstacles sit, not just how many steps there are. This is exactly what #62's own closing note predicted — "add obstacles (#63) and there is no closed form — the recurrence becomes mandatory." So #63 is the kata that justifies why #62's ★ was the DP and not the one-line binomial: the DP is the form that *scales* to this variant, and the binomial is the form that does not.

## Kāra features exercised

- **`Vec[i64]` rolling buffer** — `Vec.new()` + `push` to seed the columns, then in-place `dp[c] = dp[c] + dp[c - 1]` read-modify-write indexing, with an `dp[c] = 0` obstacle override. The same rolling-DP shape as kata [#62](../62-unique-paths/) and the `Vec[bool]` reachability table of kata [#55](../55-jump-game/).
- **`ref Vec[Vec[i64]]` grid parameter + double-index reads** — the solver borrows the obstacle grid (`grid: ref Vec[Vec[i64]]`) and reads it with `grid[i][c]`, the 2-D borrow-and-index idiom shared with katas [#54](../54-spiral-matrix/) and [#48](../48-rotate-image/); the 2-D solver additionally *builds* a `Vec[Vec[i64]]` with nested `Vec.new()`/`push`.
- **Nested array literals as test input** — `report([[0, 0, 0], [0, 1, 0], [0, 0, 0]], mut s)` constructs the `Vec[Vec[i64]]` obstacle grids inline, the same literal-grid harness shape as kata [#54](../54-spiral-matrix/).
- **Obstacle guard threaded through the recurrence** — `if grid[i][c] == 1 { dp[c] = 0 } else if c > 0 { dp[c] += dp[c-1] }` is the whole delta from #62; the border-`0` propagation falls out of it with no special-casing.
- **Shared `report`/`sums:` harness** — one answer per line plus a folded `sums:` checksum, the byte-for-byte diff anchor used across katas [#53](../53-maximum-subarray/), [#54](../54-spiral-matrix/), and [#62](../62-unique-paths/); both solvers and the Python mirror print it identically.

**v1 note.** LeetCode guarantees the answer `≤ 2·10⁹` (it fits i32); the arithmetic is i64 for uniformity with the rest of the corpus. Every `dp[c]`/`paths[i][j]` is a partial path count and so is itself `≤` the final answer, so no intermediate overflows. Obstacle cells short-circuit to `0` before any addition, so a blocked start or a fully walled row collapses the whole count to `0` without special-case branches.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   unique_paths_ii.kara
karac build unique_paths_ii.kara && ./unique_paths_ii

# The full 2-D approach (identical output):
karac run unique_paths_ii_2d.kara

# Python
python3 unique_paths_ii.py

# Verify they all agree
diff <(karac run unique_paths_ii.kara) <(python3 unique_paths_ii.py)         && echo OK
diff <(karac run unique_paths_ii.kara) <(karac run unique_paths_ii_2d.kara)  && echo OK
```
