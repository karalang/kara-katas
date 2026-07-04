# 59. Spiral Matrix II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Matrix, Simulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/spiral-matrix-ii](https://leetcode.com/problems/spiral-matrix-ii/)

Given a positive integer `n`, generate an `n × n` matrix filled with the numbers `1 … n²` in clockwise spiral order.

```
n = 1  →  [[1]]
n = 2  →  [[1, 2],
           [4, 3]]
n = 3  →  [[1, 2, 3],
           [8, 9, 4],
           [7, 6, 5]]
```

**Constraints:** `1 ≤ n ≤ 20` (so `n² ≤ 400`, well inside i64).

This is the **inverse of [kata #54](../54-spiral-matrix/)**: #54 *reads* an existing matrix in spiral order, this one *writes* `1…n²` along the same traversal.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Boundary shrinking** — fill top/right/bottom/left edges of each ring, then shrink the four bounds inward | O(n²) time, O(n²) grid | [`spiral_matrix_ii.kara`](spiral_matrix_ii.kara) ✓ via `karac run` / `karac build` | [`spiral_matrix_ii.py`](spiral_matrix_ii.py) ✓ |
| **Direction-vector simulation** — walk a turtle, turn right when the next cell is out of bounds or already filled | O(n²) time, O(n²) grid | [`spiral_matrix_ii_sim.kara`](spiral_matrix_ii_sim.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output for `n = 1…5`, and both approaches agree with each other and with the Python mirror.

## Why two solvers?

**Boundary shrinking** ([`spiral_matrix_ii.kara`](spiral_matrix_ii.kara)) is the direct form: keep `top`, `bottom`, `left`, `right` and fill one ring per outer iteration — top row L→R, right column T→B, bottom row R→L, left column B→T — shrinking each bound as its edge is consumed. The two `if` guards (fill the bottom row only if `top <= bottom`, the left column only if `left <= right`) are the whole correctness subtlety: on an **odd** `n` the center cell is filled by the top-row sweep alone, and without the guards the bottom/left sweeps would re-walk it or run backwards over an empty span. This mirrors kata #54's reader ring-with-guards exactly — the write version has the same edge cases as the read version.

**Direction simulation** ([`spiral_matrix_ii_sim.kara`](spiral_matrix_ii_sim.kara)) drops the boundary bookkeeping: hold a position and a direction index into the clockwise cycle `right → down → left → up`, write the value, then peek one step ahead — if it would leave the grid *or* land on an already-filled (nonzero) cell, turn right before stepping. The already-filled test is what closes the spiral inward. The out-of-bounds checks are ordered **before** the `grid[nr][nc] != 0` read and joined with `or`, so short-circuit evaluation guarantees the grid is never indexed out of range — the same discipline as kata #28's `j < nn and h[i + j] == nee[j]`.

## Kāra features exercised

- **Mutable `Vec[Vec[i64]]` grid with nested index-store** — `grid[r][c] = v`, the read/write of an inner heap `Vec` element through an outer `Vec` index. This is the historically delicate path (borrow-elided read of `v[i]` on a `Vec[Vec]`, and index-store of a heap `Vec` element — B-2026-06-19-6/7); both write and read-back are exact here on `karac run`, `karac build`, and the default auto-par build.
- **Grid construction via `Vec.filled(n, 0i64)` per row** — `n` rows each a fresh zero-filled inner `Vec`, pushed into the outer `Vec` (each row is an independent allocation, not an aliased shared buffer — the 2D-fill aliasing bug B-2026-06-19-8 is fixed).
- **Nested index-read as a guard** (sim) — `grid[nr][nc] != 0i64` behind a short-circuiting `or` chain of bounds checks, so an out-of-range `(nr, nc)` never reaches the read.
- **Fixed-size `Array[i64, 4]` direction tables** (sim) — `let dr: Array[i64, 4] = [0, 1, 0, -1];` indexed by the direction cursor `dr[dir]`, with `dir = (dir + 1i64) % 4i64` wrapping the clockwise cycle.
- **`for row in g.iter()` + inner `for x in row.iter()`** — nested iteration over the `Vec[Vec[i64]]` to render each row, building the line with an f-string accumulator.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   spiral_matrix_ii.kara
karac build spiral_matrix_ii.kara && ./spiral_matrix_ii

# The simulation approach (identical output):
karac run spiral_matrix_ii_sim.kara

# Python
python3 spiral_matrix_ii.py

# Verify they all agree
diff <(karac run spiral_matrix_ii.kara) <(python3 spiral_matrix_ii.py)             && echo OK
diff <(karac run spiral_matrix_ii.kara) <(karac run spiral_matrix_ii_sim.kara)     && echo OK
```
