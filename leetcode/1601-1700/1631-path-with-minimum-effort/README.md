# 1631. Path With Minimum Effort

You are a hiker preparing for an upcoming hike. You are given `heights`,
a 2D array of size `rows x columns`, where `heights[row][col]` represents
the height of cell `(row, col)`. You are situated in the top-left cell,
`(0, 0)`, and you hope to travel to the bottom-right cell,
`(rows-1, columns-1)` (i.e., **0-indexed**). You can move **up**,
**down**, **left**, or **right**, and you wish to find a route that
requires the minimum **effort**.

A route's **effort** is the **maximum absolute difference** in heights
between two consecutive cells of the route.

Return *the minimum **effort** required to travel from the top-left cell
to the bottom-right cell.*

```
heights = [[1,2,2],[3,8,2],[5,3,5]]                                  ->  2
heights = [[1,2,3],[3,8,4],[5,3,5]]                                  ->  1
heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]  ->  0
```

**Constraints:** `rows == heights.length`;
`columns == heights[i].length`; `1 <= rows, columns <= 100`;
`1 <= heights[i][j] <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `effort.kara` ★ | Dijkstra's algorithm with a route's cost its largest step rather than its sum: a `PriorityQueue` (smallest first) of `(effort, row, column)`, each cell settled the first time it is popped, a neighbour's effort the larger of the route's and the step to it. O(rc log rc) |
| `effort_search.kara` | a binary search on the effort from 0 to the tallest height, each guess checked by a breadth-first flood over a `VecDeque` that takes only steps within it. O(rc log H) |
| `effort_kruskal.kara` | every step between neighbours sorted by size and joined in a union-find in turn, as Kruskal's algorithm would; the first step after which the two corners share a root is the answer. O(rc log rc) |
| `effort_solution.kara` | LeetCode's Rust template: Dijkstra on a `BinaryHeap` of `Reverse((effort, row, column))` with the four directions in a block `const`. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples, one cell
(0), and one row; then the efforts summed and a checksum for 2000 random
grids of up to 4 x 4 with heights up to 5, 200 of up to 20 x 20 with
heights up to 1000, and 5 of up to 100 x 100 with heights up to 30000.
`effort.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every route from the top-left cell to the bottom-right that
visits no cell twice, walked out in full, its effort the largest step
along it, and the least of those efforts. It checks 3000 random grids of
at most nine cells, every other one with heights 1 to 3, so ties are
common, and the rest 1 to 50. Every grid is drawn before any arm answers.

| | property |
|---|---|
| P1 | the effort is the statement read literally |
| P2 | the grid transposed leaves the effort |
| P3 | the grid turned half round, corners swapped, leaves the effort |
| P4 | every height doubled doubles the effort |
| P5 | the effort is at most that of going along the top row and down the last column, and at least the smallest step out of the start |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 38096742, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A route that never steps left (M3) is
the hardest to catch: in a grid of at most nine cells few best routes
need to, and only 10 problems show it to P1, 33 more to the transpose.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a neighbour's effort is its own step, not the route's largest | P1 1412, P2 2, P3 1961, P5 928, P6 1412 |
| M2 | ★: any cell of the last row ends the search | P1 1376, P2 2001, P3 810, P5 691, P6 1376 |
| M3 | ★: no step to the left | P1 10, P2 33, P6 10 |
| M4 | search: the halving stops one short | P1 1384, P4 1798, P5 688, P6 1384 |
| M5 | search: the flood takes only steps strictly under the guess | P1 2907, P4 2907, P5 2206, P6 2907 |
| M6 | search: the range tops out at half the tallest height | P1 1261, P4 861, P5 595, P6 1261 |
| M7 | kruskal: the steps joined in grid order, unsorted | P1 1520, P2 1129, P3 2040, P5 812, P6 1520 |
| M8 | kruskal: the cell, not its root, hung under the other root | P1 304, P2 87, P3 473, P5 123, P6 304 |
| M9 | template: a route's cost the sum of its steps | P1 2084, P5 1838, P6 2084 |
| M10 | template: the last row never entered | P1 2753, P5 2194, P6 2753 |

## Benchmarks

The bench draws 200 random grids of 100 x 100 with heights up to `10^6`,
all of them first, then finds each one's least effort by the ★ arm in
all five languages, each with its own priority queue: Kāra's
`PriorityQueue`, Rust's `BinaryHeap` of `Reverse`, Go's
`container/heap`, Python's `heapq`, and a binary heap written out in C.
Every implementation prints `200 grids of 100 x 100: efforts sum to
88738063, checksum 710492038`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.320 s |
| Kāra (`karac build`) | 0.327 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.331 s |
| Rust (`rustc -O`) | 0.345 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.372 s |
| Go | 0.712 s |
| Python | 4.2 s |

The sequential Kāra build is level with Rust and 11% faster than Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.320 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.318 s and
0.327 s on one run).

## Verification

All four arms print the same output as `effort.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `336218278`.

## Writing it

The ★ and Kruskal arms checked clean as first written, the ★ arm's
`while let Some((effort, r, c)) = queue.pop()` over a
`PriorityQueue[(i32, i64, i64)]` and its loop over a literal list of
direction tuples included. The search arm's `let mut low = 0` kept its
literal's default `i64`, so its midpoint was refused as the `i32` limit
`reachable` takes: `low + high` and `max` are an operator and a function,
and neither fixes a literal's type (design.md § Literals). `karac fix`
declares it `low: i32`.

LeetCode's Rust template takes one `karac fix` of 25 edits, among them
`BinaryHeap` with `Reverse` to Kāra's smallest-first `PriorityQueue`
without it, `vec![vec![i32::MAX; n]; m]` to nested `Vec.filled`, the
`usize` indices to `i64`, `[(i32, i32); 4]` to `Array[(i32, i32), 4]`,
and `&&`/`||` to `and`/`or`. It kept the block
`const DIRS: Array[(i32, i32), 4] = [..]` as a block constant (design.md
§ Constants), and then `DIRS.iter()` was refused as "undefined name
'DIRS'": a method call on a name reads as a path, and the pass that
hoists a block constant to module scope renamed only a bare use. Kara
`5228eca59` renames the path's first segment too, and the arm then checks
and agrees with no hand edit.
