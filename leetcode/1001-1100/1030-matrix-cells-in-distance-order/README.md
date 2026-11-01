# 1030. Matrix Cells in Distance Order

Given four integers `rows`, `cols`, `rCenter` and `cCenter`, there is a
`rows x cols` matrix and you are on the cell `(rCenter, cCenter)`.
Return the coordinates of all cells in the matrix, sorted by their
distance from `(rCenter, cCenter)` from the smallest distance to the
largest. You may return the answer in any order that satisfies this
condition. The distance between two cells `(r1, c1)` and `(r2, c2)` is
`|r1 - r2| + |c1 - c2|`.

```
rows = 1, cols = 2, rCenter = 0, cCenter = 0  ->  [[0,0],[0,1]]
rows = 2, cols = 2, rCenter = 0, cCenter = 1  ->  [[0,1],[0,0],[1,1],[1,0]]
rows = 2, cols = 3, rCenter = 1, cCenter = 2  ->  [[1,2],[0,2],[1,1],[0,1],[1,0],[0,0]]
```

**Constraints:** `rows` and `cols` are from 1 to 100; `rCenter` is
from 0 to `rows - 1` and `cCenter` from 0 to `cols - 1`.

## Approaches

| file | mechanism |
|---|---|
| `cells_order.kara` ★ | sorted by distance: list the cells row by row, then `sort_by_key` on each cell's distance. O(R C log(R C)) |
| `cells_order_bfs.kara` | breadth-first from the centre: with no walls, a cell's distance is its number of steps from the centre, so a `VecDeque` queue reaches the cells in order of distance; a cell is marked when it joins the queue. O(R C) |
| `cells_order_buckets.kara` | a bucket per distance: distances run from 0 to `(rows - 1) + (cols - 1)`, so drop each cell in its bucket and read the buckets out nearest first. A counting sort with no comparison of two cells. O(R C) |
| `cells_order_rings.kara` | walking the rings: the cells at distance `d` lie on a diamond, so for each row offset `dr` from `-d` to `d` take the columns `cCenter ∓ (d - |dr|)`, one when that is 0, from `d = 0` out to the farthest corner, keeping the cells inside the grid. O((R + C)^2) |
| `cells_order_merge.kara` | merging the rows: every row lists its cells nearest first in the same column order (the centre's column, then one step left and right, then two), so each row is already sorted by distance, and a `PriorityQueue` keyed by `(distance, row, index)` merges them. O(R C log R) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Any order among cells at the same distance is accepted, and the arms
leave ties in different orders, so the harness checks that an answer's
distances never fall and then prints it in a canonical form, each run
of equal distances in row-major order. Every arm prints the same 18
lines: eight grids in full, LeetCode's three examples among them, each
marked in order; for six groups of random grids (3,000 up to 3 by 3
down to 10 up to 1 by 100), each from a random centre, the cell count,
how many answers were out of order, and a checksum of the canonical
answers; and the 100 by 100 grid from two corners, the middle and the
top edge, with its farthest cell and a checksum. `cells_order.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each distance from 0 to `rows + cols - 2`, every cell at
that distance, row by row, which is already in canonical form. It checks
940 grids: every grid up to 4 by 4 from every centre (100), then 800
random grids up to 10 by 10 and 40 up to 60 by 60, each from a random
centre. Each grid is also asked with the centre's row mirrored top to
bottom, transposed, and with one more row.

| | property |
|---|---|
| P1 | the canonical form is the statement read literally: every cell once, at its distance |
| P2 | the distances never fall along the answer |
| P3 | mirrored back, the answer from the mirrored centre has the same canonical form |
| P4 | transposed back, the answer on the transposed grid has the same canonical form |
| P5 | on a grid one row taller, the cells of this grid come in order of distance and have this answer's canonical form |
| P6 | each arm's canonical form agrees with at least two of the other four |

The differential prints `940 cases: checksum 472841878, 28200 checks
over 5 arms: 0 failures` under `karac __mir-run` (23.2 s), `karac
__mir-llvm-run` (1.1 s) and `karac __mir-llvm-asan` (6.2 s) with no
error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`. Fifteen are kept, three to each arm. All fifteen
are killed, each fails the same checks under both backends, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the row measured from the centre's column | P2 653, P5 653 |
| M2 | ★: the last column left out | P1 940, P4 934, P6 940 |
| M3 | ★: the first row left out | P1 940, P3 836, P4 934, P6 940 |
| M4 | bfs: a stack, not a queue | P2 825, P5 825 |
| M5 | bfs: the last row never reached | P1 922, P3 836, P4 926, P5 922, P6 922 |
| M6 | bfs: the centre never marked | P1 934, P2 934, P5 940, P6 934 |
| M7 | buckets: read from the farthest bucket | P2 934, P5 934 |
| M8 | buckets: the nearest bucket never read | P1 940, P6 940 |
| M9 | buckets: the column's distance halved | P2 807, P5 807 |
| M10 | rings: out only as far as the corner (0, 0) | P1 603, P3 764, P6 603 |
| M11 | rings: the bottom tip of each ring left out | P1 940, P3 836, P4 858, P6 940 |
| M12 | rings: the column offset from the signed row offset | P1 652, P2 512, P3 836, P4 859, P5 512, P6 652 |
| M13 | merge: every row starts at distance 0 | P2 773, P5 773 |
| M14 | merge: each row's farthest cell dropped | P1 854, P4 934, P6 854 |
| M15 | merge: only half the steps out | P1 577, P4 778, P6 577 |

P1 and P6 kill the ten that lose or repeat a cell. P2 kills seven: the
five that keep every cell but break the order, and M6 and M12, which
also lose cells. Together they kill all fifteen. P1 cannot see order, since it compares canonical forms. P5
fails wherever P2 does, and also sees M5: on a grid one row taller, the
arm reaches the row it misses on the grid itself. P3 sees the five
edits that treat the top and bottom of the grid differently. P4 sees
the seven that treat rows and columns differently, among them M2 and M14.
Neither sees M6, M8 or the five order-breaking edits, which go as
wrong on the mirrored or transposed grid as on the grid itself.

Fifteen other edits were tried and set aside. One stops on an index out
of bounds (exit 101) under both backends: buckets measuring the column
from the centre's row gives distances past the last bucket. The other
fourteen were killed too, beyond three per arm. Three fail exactly as
M2 does: buckets leaving out the last column, rings listing the tips of
each ring twice, and rings never listing the first column. Buckets
putting each cell in front fails as M7. Two pairs fail alike: ★ sorting
farthest first and merge using a max-first heap (`P2 836, P5 836`), and
bfs never stepping right and merge leaving the last column out of its
order (`P1 675, P4 858, P6 675`). The other six fail on their own: ★
sorting by the row's distance alone or never sorting; bfs taking a
diagonal step too or never reaching the first column; rings listing a
row past the grid; and merge never counting the column's distance.

## Verification

Every arm prints the same output as `cells_order.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. The differential prints its line under all three. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` flagged C-style operators in three of
the drafts: `!` for `not` in the ★ arm's harness and in bfs, `&&` for
`and` in bfs and rings, and `||` for `or` in rings. Each came with a
machine-applicable replacement, and `karac fix` applied all eight, after
which every file checks clean. The release build is kara `6697158faf`,
with runtime archives rebuilt at that commit. Under `karac __mir-run`
the arms take 1.1 s (rings) to 4.2 s (merge). No compiler gap turned up.

## Benchmarks

The bench draws 300 random centres on a 100 by 100 grid (LeetCode's
largest) once, in all five languages, and answers each with the ★ arm:
10,000 cells listed row by row and sorted by distance. It folds each
answer by its distances in order, `Σ (i + 1) · d_i`, which no order
among ties changes, into a sum and a checksum. Kāra and Rust build a
`Vec` of two-element `Vec`s and sort it with the stable `sort_by_key`.
Go builds a slice of `[]int64` and sorts it with `sort.SliceStable`, and
Python builds a list of lists and uses `list.sort`. C fills one
`malloc`'d array of pairs and sorts it with `qsort`, which is not stable
and calls its comparator through a pointer. Every implementation prints
`300 centres on a 100x100 grid: sum 1265172407622, checksum 769033585`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.195 to 0.278 s | 0.204 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.239 to 0.299 s | 0.252 s |
| C (`clang -O3`) | 0.256 to 0.297 s | 0.267 s |
| Kāra (`karac build`) | 0.398 to 0.495 s | 0.409 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.400 to 0.467 s | 0.414 s |
| Python | 1.1 s | |
| Go | 1.827 to 2.031 s | 1.951 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time equals its real time) and runs as fast as the sequential
one.

v2 took 1.64 times Rust's median time under overflow checks and 1.55
times C's. C trails Rust here. Rust's sort is generic over its key,
while `qsort` calls its comparator through a pointer, which may be the
difference. Go took longer than Python, whose sort runs in C. We did
not measure where C's, Go's or Kāra's time goes.
