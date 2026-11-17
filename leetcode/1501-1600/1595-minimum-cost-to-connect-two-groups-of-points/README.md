# 1595. Minimum Cost to Connect Two Groups of Points

You are given two groups of points where the first group has `size1`
points, the second group has `size2` points, and `size1 >= size2`.

The `cost` of the connection between any two points are given in an
`size1 x size2` matrix where `cost[i][j]` is the cost of connecting
point `i` of the first group and point `j` of the second group. The
groups are connected if each point in both groups is connected to one or
more points in the opposite group. In other words, each point in the
first group must be connected to at least one point in the second group,
and each point in the second group must be connected to at least one
point in the first group.

Return the minimum cost it takes to connect the two groups.

```
cost = [[15,96],[36,2]]                                ->  17
cost = [[1,3,5],[4,1,1],[1,5,3]]                       ->  4
cost = [[2,5,1],[3,4,7],[8,1,2],[6,2,4],[3,8,8]]       ->  10
```

**Constraints:** `size1 == cost.length`; `size2 == cost[i].length`;
`1 <= size1, size2 <= 12`; `size1 >= size2`; `0 <= cost[i][j] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `connect.kara` ★ | the first group in order over a mask of the second group's points joined: each first point takes one edge, and at the end each second point still alone takes its cheapest edge; one `Vec.filled(1 << n2, i32.MAX)` row per step. O(n1 n2 2^n2) |
| `connect_memo.kara` | the same choice top down: the cheapest way to finish from first point `i` with a mask joined, by recursion remembered in a `Map[(i64, i64), i32]`, and iterator chains (`filter`, `map`, `sum`, `min`) for each step. O(n1 n2 2^n2) |
| `connect_subsets.kara` | exactly, with no closing step: each first point takes a nonempty set of edges, a subset of the points still alone, perhaps with the cheapest edge back into the joined ones; each row's subset costs built by lowest bit, submasks walked by `(s - 1) & alone`. O(n1 3^n2) |
| `connect_solution.kara` | LeetCode's Rust template (a `vec![vec![i32::MAX; full]; m + 1]` table over `usize` masks, the column minima in a `Vec<i32>`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more (one point each, a first group of three with a costly cross, twelve
by twelve of 1, and twelve against one of 5), then the total and a
checksum for 3000 random problems of up to 4 points a group, 300 of up
to 8 and 10 of up to 12, costs from 0 to 100. `connect.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every set of edges, kept when each point of either group is
on one of them, and the cheapest kept. It checks 3000 problems of 1 to 3
points in the first group and 1 to that many in the second, costs from 0
to 20, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the first group in reverse order leaves the answer |
| P3 | the second group in reverse order leaves the answer |
| P4 | every cost doubled doubles the answer |
| P5 | the first cost made 0 lowers the answer by at most that cost |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 188971568, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, three to the ★ arm and the memo arm, two
to the others, each run under `karac __mir-run` and
`karac __mir-llvm-run`. All ten are killed, each the same way under both
backends.

The first M4, a memo looked up under first point 0, was equivalent: only
the outermost call is stored there, so the memo just never hit. Mutants
that leave a state unreachable were not used, since the doubled answer
of `i32.MAX` stops the differential with an overflow panic.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a step's table overwritten, not lowered | P1 769, P2 688, P3 1049, P6 769 |
| M2 | ★: the closing step skips the first second point | P1 269, P3 472, P6 269 |
| M3 | ★: a point's dearest edge taken as its cheapest | P1 20, P6 20 |
| M4 | memo: a state looked up under the next first point | P1 393, P2 502, P6 393 |
| M5 | memo: the last first point given no edge | P1 1269, P2 1500, P6 1269 |
| M6 | subsets: a subset costs only its lowest edge | P1 357, P3 453, P6 357 |
| M7 | subsets: the dearest edge back, not the cheapest | P1 206, P2 218, P6 206 |
| M8 | template: a column's minimum is its last cost | P1 13, P2 16, P6 13 |
| M9 | template: an edge never joins its point | P1 2823, P5 2416, P6 2823 |
| M10 | memo: every edge costs the first column's | P1 1150, P3 1152, P6 1150 |

## Benchmarks

The bench runs the ★ arm on 200 problems of 12 points against 12, costs
from 0 to 100, all drawn first, in all five languages. Every
implementation prints `200 problems of 12 by 12: total 23899, checksum
890030330`. The C mirror takes one edge per first point over a mask of
the second group's points joined, then each point still alone takes its
cheapest edge. Each problem is a malloc'd array of malloc'd rows and
each step's table a fresh malloc, as in Kāra.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| Kāra (`karac build`) | 0.113 s |
| C (`clang -O3`) | 0.116 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.116 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.123 s |
| Rust (`rustc -O`) | 0.127 s |
| Go | 0.203 s |
| Python | 6.3 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.104 s and 0.104 s on one
run).

## Verification

All four arms print the same output as `connect.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The ★, memo and subsets arms were written in Kāra and checked as
written. The differential's literal reading wrote `let mut total = 0`
and compared it with an `i32` by `min`; `karac fix` typed it
`total: i32`.

The Rust template took one `karac fix`, of 18 edits: `struct Solution;`
to `struct Solution {}`, `Vec<Vec<i32>>` to `Vec[Vec[i32]]`, each
`vec![..]` to `Vec.filled(..)`, `i32::MAX` to `i32.MAX`, the `1usize`
suffix dropped, `let mut extra = 0` typed `i32`, and `Solution::` to
`Solution.`. It then checks and agrees with no hand edit.
