# 1617. Count Subtrees With Max Distance Between Cities

There are `n` cities numbered from `1` to `n`. You are given an array
`edges` of size `n-1`, where `edges[i] = [ui, vi]` represents a
bidirectional edge between cities `ui` and `vi`. There exists a unique
path between each pair of cities. In other words, the cities form a
**tree**.

A **subtree** is a subset of cities where every city is reachable from
every other city in the subset, where the path between each pair passes
through only the cities from the subset. Two subtrees are different if
there is a city in one subtree that is not present in the other.

For each `d` from `1` to `n-1`, find the number of subtrees in which the
**maximum distance** between any two cities in the subtree is equal to
`d`.

Return *an array of size* `n-1` *where the* `dth` *element* ***(1-indexed)***
*is the number of subtrees in which the* ***maximum distance*** *between
any two cities is equal to* `d`.

**Notice** that the **distance** between the two cities is the number of
edges in the path between them.

```
n = 4, edges = [[1,2],[2,3],[2,4]]  ->  [3,4,0]
n = 2, edges = [[1,2]]              ->  [1]
n = 3, edges = [[1,2],[2,3]]        ->  [2,1]
```

**Constraints:** `2 <= n <= 15`; `edges.length == n-1`;
`edges[i].length == 2`; `1 <= ui, vi <= n`; all pairs `(ui, vi)` are
distinct.

## Approaches

| file | mechanism |
|---|---|
| `subtrees.kara` ★ | every set of cities as a bit mask: all pair distances first (Floyd-Warshall), then a mask of two or more cities is a subtree exactly when it holds one road fewer than it has cities (`count_ones`, the roads counted by `filter(..).count()`), and its largest distance is the largest over its pairs. O(2^n n^2) |
| `subtrees_bfs.kara` | each mask searched breadth first over a `VecDeque` from its lowest city (`trailing_zeros`), through roads with both ends in the mask; a subtree when the search reaches all of it, and its largest distance by a second search from the farthest city found (the two-search diameter of a tree). O(2^n n) |
| `subtrees_pairs.kara` | no masks: each subtree counted once at the pair of cities ending its diameter, the smallest such pair. For each pair at distance `d`, the cities allowed in are those within `d` of both ends (ties broken by number), the path between the ends must be in, and a recursive walk from one end multiplies, over allowed children, the child's count, plus one for leaving out a child off the path. O(n^4) |
| `subtrees_solution.kara` | a Rust solution as LeetCode's Rust users write it (Floyd-Warshall over `usize::MAX / 2`, each mask's cities collected with `filter(\|&i\| ..)`, its roads counted from the distance table), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (a path of 6, a star of 6, and a caterpillar of 7), then the cities,
the subtrees and a checksum of every count for 3000 random trees of 2 to
6 cities, 300 of 2 to 10, and 30 of 2 to 15. A random tree joins each city
after the first to one before it, then renames the cities at random.
`subtrees.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every set of two or more cities, counted up in binary over a
`Vec[bool]`; for each city of the set, the distances to the others by
roads with both ends in the set, grown until nothing changes; a set is a
subtree when every distance was found, and its largest is counted. It
checks 3000 random trees of 2 to 8 cities, every random choice drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the cities renamed at random leave the answer |
| P3 | the roads listed backwards, each turned round, leave the answer |
| P4 | the subtrees of largest distance 1 are the roads: `n - 1` of them |
| P5 | the last distance with a subtree is the tree's own diameter |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 367361723, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1, M8 and M9 escape P4: none of them
changes how many subtrees of largest distance 1 there are.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the distance table's "far" set to 2, so no distance passes 2 | P1 1964, P5 1964, P6 1964 |
| M2 | ★: masks of two cities skipped | P1 3000, P4 3000, P5 431, P6 3000 |
| M3 | ★: a distance's count set to 1, not added to | P1 2569, P4 2569, P6 2569 |
| M4 | bfs: the second search started from the mask's lowest city, not from the far end | P1 1975, P2 2029, P4 1963, P5 1238, P6 1975 |
| M5 | bfs: a mask kept whenever its search reaches two cities | P1 1964, P2 1660, P4 1964, P6 1964 |
| M6 | bfs: the search walking out of the mask | P1 2569, P4 2569, P6 2569 |
| M7 | pairs: the cities on the path allowed to be left out | P1 3000, P2 1058, P4 3000, P6 3000 |
| M8 | pairs: the tie at distance d from i broken against i, not j | P1 1638, P2 1029, P6 1638 |
| M9 | template: a pair at distance 2 counted as a road | P1 2143, P6 2143 |
| M10 | template: each city's last partner skipped | P1 3000, P4 3000, P5 3000, P6 3000 |

## Benchmarks

The bench makes 400 random trees of 15 cities, all of it first. Then:
Floyd-Warshall and every one of the 32767 masks, its roads counted and,
for a subtree, its largest pair distance, in all five languages. Every
implementation prints `400 trees of 15 cities: 463023 subtrees, checksum 940665783`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `428299b56e` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.198 s |
| Rust (`rustc -O`) | 0.224 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.741 s |
| Kāra (`karac build`) | 0.761 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.776 s |
| Go | 1.295 s |
| Python | 17 s |

Kāra is level with Rust under overflow checks, the equal-safety
comparison, and about three times plain Rust: the gap is the checked
`i64` adds in the Floyd-Warshall and mask loops, which `rustc -O` and
`clang -O3` leave unchecked.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (0.737 s and 0.750 s on one run).

## Verification

All four arms print the same output as `subtrees.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`428299b56e`.

## Writing it

The ★ and pairs arms were written in Kāra and checked as written, apart
from one `*x` on a copied `i32` in the harness, which `karac fix` took
off. The bfs arm wrote Rust's `let (mut far, mut reached) = (start, 0)`,
and `karac fix` made it `let mut (far, reached) = (start, 0)`, Kāra's
`mut` before the whole pattern. The differential wrote
`let diameter = within(..).iter().max().unwrap()`, which keeps a
reference into a temporary dropped at the `;`, and `karac fix` bound the
temporary first; it also took off three `as i64` casts of `i32`s.

The Rust template took one `karac fix` of 22 edits: `struct Solution;`
to `struct Solution {}`, the `<..>` types to `[..]`, every `as usize`
to `as i64`, `usize::MAX / 2` to `i64.MAX / 2`, both `vec![..]` to
`Vec.filled`, `for e in &edges` to `for e in ref edges`, `|&i|` to
`|i|`, `let mut max_d = 0` typed `i64`, and `Solution::` to `Solution.`.
It then checks and agrees with no hand edit.
