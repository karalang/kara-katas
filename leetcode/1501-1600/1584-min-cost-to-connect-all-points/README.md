# 1584. Min Cost to Connect All Points

You are given an array `points` representing integer coordinates of some
points on a 2D-plane, where `points[i] = [x_i, y_i]`.

The cost of connecting two points `[x_i, y_i]` and `[x_j, y_j]` is the
Manhattan distance between them: `|x_i - x_j| + |y_i - y_j|`.

Return the minimum cost to make all points connected. All points are
connected if there is exactly one simple path between any two points.

```
points = [[0,0],[2,2],[3,10],[5,2],[7,0]]  ->  20
points = [[3,12],[-2,5],[-4,1]]            ->  18
```

**Constraints:** `1 <= points.length <= 1000`;
`-10^6 <= x_i, y_i <= 10^6`; all pairs `(x_i, y_i)` are distinct.

## Approaches

The answer is the weight of a minimum spanning tree of the complete
graph on the points.

| file | mechanism |
|---|---|
| `points.kara` ★ | Prim's algorithm with no edge list: each point outside the tree keeps its distance to the nearest point inside, the nearest of them joins, and the rest are lowered by their distance to it. O(n^2) time, O(n) space |
| `points_kruskal.kara` | Kruskal: all `n (n - 1) / 2` edges as `(cost, i, j)` tuples, sorted, taken cheapest first whenever they join two parts of a disjoint-set forest (a bare `Vec[i64]` of parents with path halving). O(n^2 log n) |
| `points_heap.kara` | lazy Prim: a `PriorityQueue` of `(cost, point)` pairs, smallest first, holding every edge out of the tree seen so far; a popped point already inside is skipped. O(n^2 log n) |
| `points_solution.kara` | LeetCode's Rust template (Prim over `i32` costs with `dist` and `visited` arrays, `usize::MAX` for no choice yet), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and three more
(one point, four points a step apart, and two at opposite corners of the
range), then the cost and a checksum for 3000 random problems of up to 6
distinct points within 5 of the origin, 300 of up to 100 within 1000, and
3 of up to 1000 across the whole range. `points.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every set of `n - 1` edges tried, the cheapest whose edges join
every point to point 0. It checks 3000 problems of 1 to 5 distinct points
with coordinates from -4 to 4, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the points in reverse order leave the answer |
| P3 | every point turned a quarter (`(x, y)` to `(-y, x)`) leaves the answer |
| P4 | every point scaled by 3 and moved triples the answer |
| P5 | a point one step right of a rightmost point adds 1 to the answer |
| P6 | each arm agrees with at least two of the other three |

P5 holds exactly: the new point's distance to any other is one more than
the rightmost point's, so no tree gains by passing through it.

The differential prints `3000 problems: checksum 233752605, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

Four first choices were replaced. Picking the farthest point in the ★ arm
was killed only by an overflow panic on `i64.MAX`. Three were equivalent:
taking an edge of cost 0 in Kruskal (the points are distinct, so there is
none), letting the heap arm's first round pop a point already inside, and
pushing the heap arm's edges to points already inside (they are skipped
when popped).

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a point's nearest distance replaced by the newest, not lowered | P1 894, P2 1262, P5 1543, P6 894 |
| M2 | ★: Chebyshev distance (`max` of the two) in place of Manhattan | P1 2197, P6 2197 |
| M3 | ★: the `y` difference not made absolute | P1 1709, P2 2234, P3 2054, P5 279, P6 1709 |
| M4 | kruskal: the edge from each point to the next in the list never listed | P1 2175, P5 2106, P6 2175 |
| M5 | kruskal: the point, not its root, linked to the other root | P1 268, P2 320, P5 506, P6 268 |
| M6 | kruskal: the edges sorted by their first point, not their cost | P1 1537, P2 1622, P5 1498, P6 1537 |
| M7 | heap: the queue pops the largest first | P1 1797, P5 2414, P6 1797 |
| M8 | heap: the loop stops one point short | P1 2414, P2 923, P5 1437, P6 2414 |
| M9 | template: the last point's distance always replaced | P1 413, P2 624, P5 498, P6 413 |
| M10 | template: an odd cost rounded down to even | P1 1855, P4 1855, P5 3000, P6 1855 |

## Benchmarks

The bench draws 100 problems of 1000 distinct points across the whole
range first (a hash set keeps them distinct; C scans instead), then
solves each by the ★ arm, in all five languages: 100 runs of an O(n^2)
Prim. Every implementation prints `100 problems of 1000 points: cost
5183389140, checksum 840740556`. Every point is its own allocation in
every language.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `76e5a13ad` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.268 s |
| C (`clang -O3`) | 0.317 s |
| Kāra (`karac build`) | 0.333 s |
| Go | 0.343 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.349 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.492 s |
| Python | 16.3 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (0.321 s and 0.327 s on one run).

Kāra is 0.71x Rust under overflow checks by median and 1.30x plain
`rustc -O`. The inner loop is two subtractions, two `abs` and an add a
pair; checked Rust tests each of those, and plain Rust tests none.

## Verification

All four arms print the same output as `points.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`76e5a13ad`.

## Writing it

The ★, Kruskal and heap arms were written in Kāra and checked as
written.

The Rust template took two rounds of `karac fix`:

1. eighteen edits: the `Vec<..>` types to `Vec[..]`, `i32::MAX` and
   `usize::MAX` to `i32.MAX` and `usize.MAX`, `!` to `not`, `&&` to
   `and`, `||` to `or`, the `|&x|` pattern to a plain name, and
   `Solution::` to `Solution.`;
2. `vec![i32.MAX; n]` and `vec![false; n]` to `Vec.filled(..)`,
   `let mut res = 0` given the type `i32`, `usize.MAX` to `i64.MAX`, and
   the wrapper's `as i64` dropped.

It then checks and agrees with no hand edit.
