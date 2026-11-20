# 1697. Checking Existence of Edge Length Limited Paths

An undirected graph of `n` nodes is defined by `edgeList`, where
`edgeList[i] = [ui, vi, disi]` denotes an edge between nodes `ui` and
`vi` with distance `disi`. Note that there may be **multiple** edges
between two nodes.

Given an array `queries`, where `queries[j] = [pj, qj, limitj]`, your
task is to determine for each `queries[j]` whether there is a path
between `pj` and `qj` such that each edge on the path has a distance
**strictly less than** `limitj`.

Return *a **boolean array*** `answer`*, where* `answer.length ==
queries.length` *and the* `jth` *value of* `answer` *is* `true` *if
there is a path for* `queries[j]` *is* `true`*, and* `false`
*otherwise*.

```
n = 3, edgeList = [[0,1,2],[1,2,4],[2,0,8],[1,0,16]],
       queries = [[0,1,2],[0,2,5]]               ->  [false,true]
n = 5, edgeList = [[0,1,10],[1,2,5],[2,3,9],[3,4,13]],
       queries = [[0,4,14],[1,4,13]]             ->  [true,false]
```

**Constraints:** `2 <= n <= 10^5`; `1 <= edgeList.length,
queries.length <= 10^5`; `edgeList[i].length == 3`;
`queries[j].length == 3`; `0 <= ui, vi, pj, qj <= n - 1`; `ui != vi`;
`pj != qj`; `1 <= disi, limitj <= 10^9`; there may be **multiple** edges
between two nodes.

## Approaches

| file | mechanism |
|---|---|
| `paths.kara` ★ | the queries answered offline: the edges sorted by length and the queries by limit, and before each query every edge shorter than its limit joined in a union-find with path compression; the query asks whether its nodes share a root. O((E + Q) log + (E + Q) α(n)) |
| `paths_bfs.kara` | a breadth-first search for each query over adjacency lists, by the edges shorter than its limit. O(Q * (n + E)) |
| `paths_forest.kara` | a minimum spanning forest by Kruskal's rule, rooted by a walk that records each node's parent, the length up to it and its depth; a query climbs both nodes to where they meet, keeping the longest length passed, and asks whether it is below the limit (the forest's path between two nodes has the least longest edge of any path). O(E log E + Q * h) |
| `paths_solution.kara` | a Rust solution as LeetCode's Rust users write it, `mut edge_list` sorted in place by `sort_unstable_by_key` and a recursive `find` nested in the method, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's two examples, a limit equal
to the only edge's length, and two nodes joined twice; then the answers
that are true and a checksum of every answer for 3000 random graphs of
up to 6 nodes with lengths up to 5, 300 of up to 100 nodes with lengths
up to 100, and 10 of up to 2000 nodes with lengths up to `10^9`, each
with up to twice as many edges as its bound on nodes and up to as many
queries. `paths.py` mirrors the ★ arm and its output is byte-identical.

```
[false, true]
[true, false]
[false, true]
[true, false]
3000 graphs of up to 6 nodes, lengths up to 5: 5007 true, checksum 618701383
300 graphs of up to 100 nodes, lengths up to 100: 6616 true, checksum 24606381
10 graphs of up to 2000 nodes, lengths up to 1000000000: 6632 true, checksum 101934422
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each query, every path from p that visits no node twice
is walked, edge by edge in both directions, and the query is true when
one reaches q with every edge strictly shorter than its limit. It checks
3000 random graphs of 2 to 6 nodes and 1 to 8 edges, with 1 to 6
queries, lengths and limits from 1 to 5. Every case is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | each query's two nodes swapped give the same answers |
| P3 | each limit raised by one turns no answer from true to false |
| P4 | the edges listed in reverse give the same answers |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 544281949, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, a search from p over the edges shorter than
the limit, gives the same checksum. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. None fails P3: every edit keeps a
larger limit from losing a path. M1 and M4 let an edge as long as the
limit count, and fail the same checks; so do M2 and M9, which join
nothing.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an edge as long as the limit joined | P1 1136, P5 1136 |
| M2 | ★: each set joined to itself | P1 1955, P5 1955 |
| M3 | ★: the queries in order of their first node, not their limit | P1 945, P2 735, P5 945 |
| M4 | bfs: an edge as long as the limit walked | P1 1136, P5 1136 |
| M5 | bfs: each edge walked one way only | P1 1208, P2 1544, P5 1208 |
| M6 | forest: every edge kept, cycles too | P1 310, P4 15, P5 310 |
| M7 | forest: the lengths climbed from p's side not kept | P1 1207, P2 1840, P4 47, P5 1207 |
| M8 | forest: the edges sorted by their first node, not their length | P1 789, P4 604, P5 789 |
| M9 | solution: each set joined to itself | P1 1955, P5 1955 |
| M10 | solution: only edges shorter than the limit less one joined | P1 1115, P5 1115 |

## Benchmarks

The bench draws 10 random graphs of `10^5` nodes, `10^5` edges and
`10^5` queries, LeetCode's largest, lengths and limits up to `10^9`, all
of them first, then answers each 5 times by the ★ arm in all five
languages: the sorts are each language's own (`sort_by_key` in Kāra and
Rust, `sorted` in Python, `qsort` in C, `slices.SortFunc` in Go), and
the answers do not depend on the order of equal lengths. Every
implementation prints `10 graphs of 100000 nodes, edges and queries, 5
rounds: 809125 true, checksum 124478703`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 1.687 s |
| Go | 1.730 s |
| Rust (`rustc -O`) | 1.743 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.761 s |
| Kāra (`karac build`) | 1.813 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.850 s |
| Python | 21 s |

The sequential Kāra build takes 1.06x Rust's time and 1.05x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 1.687 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.658 s and 1.720 s on one
run).

## Verification

All four arms print the same output as `paths.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and bfs arms checked clean as first written. The forest arm's
first draft bound its two climbing nodes `let (mut a, mut b) = ..`, as
Rust does; `karac fix` wrote `let mut (a, b) = ..`, Kāra's `mut` before
the whole pattern (3 edits).

LeetCode's Rust template took one `karac fix` of 45 edits. The nested
`fn find` was moved above the `impl` (Kāra has no nested items, and a
nested `fn` captures nothing, so it means the same there), with
`&mut Vec<usize>` written `mut ref Vec[i64]` and each `find(&mut
parent, ..)` written `find(mut parent, ..)`; `struct Solution {}` added;
`mut edge_list: Vec<..>` written `edge_list: own Vec[..]` with `let mut
edge_list = edge_list;` at the body's start (and the harness's wrapper
taking it `own` to match); each `sort_unstable_by_key` written
`sort_by_key`, `|&i|` written `|i|`, every `usize` and `as usize`
written as `i64`, `vec![false; ..]` written `Vec.filled(.., false)`, and
`&&` written `and`.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
