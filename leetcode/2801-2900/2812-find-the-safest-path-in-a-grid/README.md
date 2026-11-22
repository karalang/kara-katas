# 2812. Find the Safest Path in a Grid

You are given a **0-indexed** 2D matrix `grid` of size `n x n`, where
`(r, c)` represents:

- A cell containing a thief if `grid[r][c] = 1`
- An empty cell if `grid[r][c] = 0`

You are initially positioned at cell `(0, 0)`. In one move, you can move
to any adjacent cell in the grid, including cells containing thieves.

The **safeness factor** of a path on the grid is defined as the
**minimum** manhattan distance from any cell in the path to any thief
in the grid.

Return *the **maximum safeness factor** of all paths leading to cell*
`(n - 1, n - 1)`.

An **adjacent** cell of cell `(r, c)` is one of the cells `(r, c + 1)`,
`(r, c - 1)`, `(r + 1, c)` and `(r - 1, c)` if it exists. The
**Manhattan distance** between two cells `(a, b)` and `(x, y)` is equal
to `|a - x| + |b - y|`.

```
grid = [[1,0,0],[0,0,0],[0,0,1]]                  ->  0
grid = [[0,0,1],[0,0,0],[0,0,0]]                  ->  2
grid = [[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]]  ->  2
```

**Constraints:** `1 <= grid.length == n <= 400`; `grid[i].length == n`;
`grid[i][j]` is either `0` or `1`; there is at least one thief in the
grid.

## Approaches

| file | mechanism |
|---|---|
| `safest.kara` ★ | each cell's distance to the nearest thief by one breadth-first search from every thief at once over a `VecDeque`, then a binary search on the answer, each guess s asked by a breadth-first search from the start over the cells at least s from every thief |
| `safest_heap.kara` | the widest path by Dijkstra's search: the same distances, then a `PriorityQueue` keyed by the safeness negated, each neighbour offered the smaller of the path's safeness and its own distance |
| `safest_union.kara` | union-find: the distances by the two-pass distance transform, from the top left and then the bottom right, then the cells added safest first, sorted, each joined to its added neighbours until the start and the end share a root |
| `safest_layers.kara` | layers and buckets: the distances one `Vec` layer at a time, then a bucket per safeness level emptied from the safest down, a neighbour offered to the bucket of the smaller of the level and its distance |
| `safest_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `VecDeque` search with `usize` cells and `i32` bounds checks, then a max-`BinaryHeap` of (safeness, row, column) with a `seen` table set on push, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; one cell
with the thief on it; 100 by 100 with one thief in the middle; 3000
random grids of 1 to 6 with a thief in about one cell of four; and 50
of up to 60 with one in about one cell of 200, the last two with the
sum of the answers and a checksum. `safest.py` mirrors the ★ arm and
its output is byte-identical.

```
0
2
2
0
49
3000 small grids: safeness sums to 803, checksum 320182498
50 large grids: safeness sums to 280, checksum 404938858
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every path from the top left to the bottom right that visits
no cell twice, walked by a depth-first search, each cell's safeness its
Manhattan distance to the nearest thief found by looking at every
thief, a path's the least of its cells', the answer the best path's; no
breadth-first search, no heap and no table of distances. It draws 2000
random grids of 1 to 4 with a thief in about one cell of four, then 50
of up to 40 with one in about one cell of 100, each with one more cell
for P5, all before any arm answers; the literal reading is asked only
of the first 2000.

| | property |
|---|---|
| P1 | up to 4 by 4, the answer is the literal reading's |
| P2 | from 0 to the start's and the end's own safeness, whichever is less |
| P3 | the grid transposed: the same answer |
| P4 | the grid turned a half turn: the same answer |
| P5 | one more thief: no larger; a thief on the start: 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 779944705, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Not run yet. On the karac release this batch was checked with
(`684b860a5`), the mutation runner stopped on a compiler crash before
any verdict; the table comes with a run on a newer build.

## Benchmarks

The bench draws 10 grids of 400 by 400, LeetCode's largest, with a
thief in about one cell of 2000, all of them first, then answers each 3
times by the ★ arm in all five languages: C's queues are two arrays of
n * n cells, Go's slices read from a head index, Rust's and Python's a
`VecDeque` and a `deque`. Every implementation prints `10 grids of 400,
3 rounds: safeness sums to 624, checksum 884137139`.

BENCHTAB

## Verification

All five arms print the same output as `safest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the harness checked clean as first written.

LeetCode's Rust template took 37 `karac fix` edits over two runs, the
wrapper included: `struct Solution {}` added for the `use` line;
`Vec<..>` became `Vec[..]`; `vec![vec![-1; n]; n]` became
`Vec.filled(n, Vec.filled(n, -1))`; `VecDeque::new` and `Solution::`
took `.`; `BinaryHeap::new()` became `PriorityQueue.max_first()`; the
`&(di, dj)` patterns and `&v` lost their `&`; `&&`, `||` and `!` became
`and`, `or` and `not`; the `as usize` casts and `0usize` suffixes went,
Kāra indexing by `i64`, and the `let (ni, nj) = (ni, nj);` they left
went with them by the `self_rebinding` lint's fix (kara 0d28296389,
B-2026-11-21-206); and the second run dropped the wrapper's `as
i64`, an `i32` widening implicitly.

It then still failed: `return d` of the popped `(dist[0][0], 0, 0)`
from `-> i32` was refused as a narrowing from `i64`, with no fix.
design.md §8 leaves the table's `-1` open until that return fixes it,
as Rust's inference does, but reading `dist[0][0]` into the pushed
tuple, and storing `dist[i][j] + 1` by an assignment, had each settled
it to `i64`. Fixed in kara (0d28296389, B-2026-11-21-201); the template then
needed no hand edit.
