# 2492. Minimum Score of a Path Between Two Cities

You are given a positive integer `n` representing `n` cities numbered
from `1` to `n`. You are also given a 2D array `roads` where
`roads[i] = [ai, bi, distancei]` indicates that there is a
**bidirectional** road between cities `ai` and `bi` with a distance
equal to `distancei`. The cities graph is not necessarily connected.

The **score** of a path between two cities is defined as the
**minimum** distance of a road in this path.

Return *the **minimum** possible score of a path between cities* `1`
*and* `n`.

**Note:**

- A path is a sequence of roads between two cities.
- It is allowed for a path to contain the same road **multiple** times,
  and you can visit cities `1` and `n` multiple times along the path.
- The test cases are generated such that there is **at least** one path
  between `1` and `n`.

```
n = 4, roads = [[1,2,9],[2,3,6],[2,4,5],[1,4,7]]  ->  5
n = 4, roads = [[1,2,2],[1,3,4],[3,4,7]]          ->  2
```

**Constraints:** `2 <= n <= 10^5`; `1 <= roads.length <= 10^5`;
`roads[i].length == 3`; `1 <= ai, bi <= n`; `ai != bi`;
`1 <= distancei <= 10^4`; there are no repeated edges; there is at
least one path between `1` and `n`.

A path may use a road as often as it likes, so a path from 1 to `n`
can go out to any road of the part of the map that holds 1, cross it,
come back, and go on to `n`, which that same part holds. Its score is
then the least distance anywhere in that part, and no path does better,
since a path never leaves it. The approaches differ in how they find
the part.

## Approaches

| file | mechanism |
|---|---|
| `score.kara` ★ | a breadth-first search from 1 over adjacency lists, a `Vec` as the queue, the least distance kept on every road looked at. O(n + m) |
| `score_rec.kara` | a recursive depth-first search: each city, once marked, gives the least distance among its own roads and what the unmarked cities beyond them give. O(n + m), O(n) deep |
| `score_union.kara` | union-find: every road joins its two cities' sets, roots found with path halving and joined by size; then the least distance among the roads in 1's set. O(m α(n)) |
| `score_stack.kara` | an explicit stack over a `Map` of roads: the cities reached from 1 gathered in a `Set`, then the least distance on a road out of any of them. O(n + m) expected |
| `score_iter.kara` | iterators: waves of the breadth-first walk, each the last one `flat_map`ped to its roads' cities and `filter`ed to those not yet seen; then the roads `filter`ed to the reached cities, `map`ped to distances, and the `min` taken. O(n + m) |
| `score_solution.kara` | LeetCode's Rust template: `n: i32` and `Vec<Vec<i32>>` in, `i32` out; adjacency lists by `vec![vec![]; n + 1]`, a `std::collections::VecDeque` breadth-first search from 1; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and five
more; then 2000 random maps of 2 to 50 cities, each a path from 1 to
`n` through a random few cities and up to 60 more roads, with distances
to `10^4` and 2000 with distances to 5, each as a checksum; then the
constraints' largest, `10^5` cities: a chain from 1 to `n`; a star
round 1 whose least road joins two of its leaves; and a random map of
all but three cities with distances from 2, joined to `n` by a road of
5000 and beside a road of distance 1 between the other two, which no
path from 1 can reach. `score.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 5000 random maps against
a union-find that keeps the least distance of every set as it joins,
and the two agreed on every map.

`check` first reports 9 errors on the template: the `use
std::collections::VecDeque;` line, `struct Solution;`, `Vec<Vec<i32>>`,
the two `&` borrows and the `&` before the loop's pattern,
`VecDeque::new` and `i32::MAX`, and `!vis[v]`. `karac fix` carries it
in one call, reporting 18 edits: the `use` line deleted, since
`VecDeque` is in the prelude; `struct Solution {}`; the brackets; the
three `as usize` casts become `as i64`; `vec![vec![]; n + 1]` and
`vec![false; n + 1]` become `Vec.filled(n + 1, Vec.new())` and
`Vec.filled(n + 1, false)`; `&roads` and `&g[u]` become `ref roads` and
`ref g[u]`, and the pattern loses its `&`; the two paths take `.`;
`!vis[v]` becomes `not vis[v]`; and the wrapper's `as i64` on the
template's answer is dropped, since an `i32` widens to `i64` on its
own.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a road can be on a path from 1 to `n` when one of its cities
can be reached from 1 and the other can reach `n`, each found by
sweeping the roads until nothing more is reached, and the score is the
least distance on such a road. No adjacency list is built. It checks
300 random maps of 2 to 10 cities with up to 12 more roads, distances
to 3 or to 20; then 20 of two cities, and 40 of 30 to 60 cities with 20
to 80 more roads, distances to `10^4`. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the score is the statement read literally |
| P2 | the score is a road's distance, at most the least on a road at 1 |
| P3 | the roads in the other order: the same score |
| P4 | the cities numbered backwards, 1 and `n` changing places: the same score |
| P5 | a road of distance 1 added from `n` to 1: the score is 1 |
| P6 | each arm agrees with at least three of the other five |

P4 holds because the part that holds 1 holds `n` too, so renaming the
two ends does not change which part is searched. P5 holds because the
new road touches 1, and no distance is less than 1.

The differential prints `360 cases: checksum 28020503, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and sweeps the same way. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only roads to new cities counted | P1 126, P2 70, P3 127, P4 77, P5 144, P6 126 |
| M3 | ★: every other city taken off the queue | P1 68, P3 46, P4 122, P6 68 |
| M6 | ★: the last road's distance kept | P1 241, P2 210, P3 193, P4 118, P5 208, P6 241 |
| M8 | rec: a city's own roads not counted | P1 360, P2 360, P5 360, P6 360 |
| M9 | rec: roads of distance 2 or less never followed | P1 14, P4 23, P6 14 |
| M11 | rec: the least begun at 20 | P1 32, P2 32, P6 32 |
| M13 | union: the first road never joined | P1 25, P3 30, P4 75, P6 25 |
| M14 | union: the home set found at 2 | P1 68, P2 64, P4 54, P5 66, P6 68 |
| M15 | union: the city joined, not its root | P1 42, P2 8, P3 46, P4 59, P6 42 |
| M18 | stack: only the roads at 1 counted | P1 127, P4 183, P6 127 |
| M19 | stack: the walk from the last road's city | P1 18, P2 11, P3 18, P4 61, P5 58, P6 18 |
| M20 | stack: the roads out of unreached cities | P1 356, P2 345, P5 354, P6 356 |
| M23 | iter: the greatest taken | P1 333, P2 318, P5 351, P6 333 |
| M25 | iter: the first wave only | P1 71, P4 102, P6 71 |
| M26 | iter: a city read for the distance | P1 165, P2 163, P4 146, P6 165 |
| M30 | solution: the search stopped at n | P1 12, P4 36, P6 12 |
| M31 | solution: the least begun at 30 | P1 25, P2 25, P6 25 |

P1 and P6 kill all seventeen, P4 twelve, P2 eleven, P5 seven, and P3
six.

Fourteen are not kept, and none survives. Four fail exactly as a kept
one: the ★ arm's greatest kept (M5) as the rec arm's own roads not
counted (M8), both wrong on every case and every answer too big; the rec
arm's cities beyond never asked (M7) as the stack arm's only the roads
at 1 counted (M18), since both see only the roads at 1; the union arm's
roads outside 1's set (M12) as the stack arm's roads out of unreached
cities (M20); and the stack arm's city pushed again for its neighbour
(M21) as the iter arm's first wave only (M25), since both stop one step
from 1. Seven fail as one another, in three sets, none of whose members
could be kept beside the kept edits of their arms: the ★, rec and
template arms' roads one way only (M4, M10, M28); the ★ and template
arms' walk from city 2 (M2, M29); and the union and template arms' one
more on every distance (M16, M27). Three end in a crash: the stack
arm's no new city pushed (M17) pushes every city already reached
instead, so the stack never empties and grows until the run is
stopped: by the runner's 900 s limit under `__mir-run`, and by a
SIGKILL (exit 137) under `__mir-llvm-run`; and the iter arm's only roads
from 1 and roads one way only (M22, M24) leave a map with no road out
of a reached city, so `min()` gives `None` and the `unwrap()` panics
under both backends.

Two edits were replaced before this table was drawn. The rec arm's
roads of distance 1 never followed survived every check: such a road
is counted before it is passed over, and once one is counted the
answer is 1 whatever lies beyond, so the edit changes nothing. It was
replaced by roads of distance 2 or less never followed (M9). The
template's least begun at 0 was refused by `check` and never ran: an
unannotated `let mut ans = 0;` keeps its literal's default `i64`, which
a method call does not change (`docs/design.md` §8 Literals), so `ans`
cannot be returned as the template's `i32`. It was replaced by the
least begun at an `i32` 30 (M31).

## Verification

Every arm prints the same output as `score.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 3.4 to 8.7 s and the differential 1.3 s; under `karac __mir-llvm-asan` the arms take 1.1 to 2.4 s and the differential 0.8 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds one map of `10^5` cities once from its own generator:
a road of `10^4` from 1 to `n`, then random roads of distance to `10^4`
between two different cities until there are `10^5`. It then makes 50
passes. Each sets one road's distance to a value chosen by the checksum
so far, asks, and puts it back, folding the answer plus the pass into
the checksum. Every answer builds its adjacency lists afresh and
searches the whole part that holds 1. The bench uses the ★ arm in all
five languages: C with the lists in compressed rows, Rust and Go with a
growable list per city. Every implementation prints `50 passes over
10^5 cities and 100000 roads: checksum 648357403`.

BENCHTAB
