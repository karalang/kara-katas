# 1724. Checking Existence of Edge Length Limited Paths II

An undirected graph of `n` nodes is defined by `edgeList`, where
`edgeList[i] = [ui, vi, disi]` denotes an edge between nodes `ui` and
`vi` with distance `disi`. Note that there may be **multiple** edges
between two nodes, and the graph may not be connected.

Implement the `DistanceLimitedPathsExist` class:

- `DistanceLimitedPathsExist(int n, int[][] edgeList)` Initializes the
  class with an undirected graph.
- `boolean query(int p, int q, int limit)` Returns `true` if there
  exists a path from `p` to `q` such that each edge on the path has a
  distance **strictly less than** `limit`, and otherwise `false`.

```
n = 6, edgeList = [[0,2,4],[0,3,2],[1,2,3],[2,3,1],[4,5,5]]
query(2, 3, 2)  ->  true     (the edge 2-3 of 1)
query(1, 3, 3)  ->  false    (1-2 is 3, not below 3)
query(2, 0, 3)  ->  true     (2-3-0, 1 and 2)
query(0, 5, 6)  ->  false    (no path at all)
```

**Constraints:** `2 <= n <= 10^4`; `0 <= edgeList.length <= 10^4`;
`0 <= ui, vi, p, q <= n - 1`; `ui != vi`, `p != q`;
`1 <= disi, limit <= 10^9`; at most `10^4` calls to `query`.

LeetCode marks the problem premium, so there is no Rust template to carry
over: all four arms are Kāra written for it.

## Approaches

| file | mechanism |
|---|---|
| `dist.kara` ★ | a union-find that remembers when each link was made: the edges joined by weight, by rank and never compressed, each node keeping the weight of the edge that hung it under its parent. Those weights grow towards a root, so the root of p's part under the limit is where the climb meets a link not below it; p and q are joined when those roots match. O(m log m) to build, O(log n) a query |
| `dist_search.kara` | nothing prepared: the graph as lists of (neighbour, weight), and each query a breadth-first walk from p over the edges below the limit. O(n + m) a query |
| `dist_lifting.kara` | Kruskal's minimum spanning forest keeps, between any two nodes, a path whose heaviest edge is as light as any; each tree rooted by a breadth-first walk, binary lifting keeps the heaviest edge to each 2^j-th ancestor, and a query is the heaviest edge on the tree path, below the limit. O(log n) a query |
| `dist_tree.kara` | a Kruskal reconstruction tree: each join of two parts makes a new node, weighted by the edge, over the parts' tops; a node's ancestors grow in weight, so binary lifting climbs p and q to their highest ancestors below the limit and compares them. O(log n) a query |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's example, the same graph
asked at a limit equal to an edge's weight and one above it; then the
paths found and a checksum of every answer for 3000 random graphs of up
to 8 nodes and 10 edges, asked 10 questions each, 100 of up to 1000
nodes and 1500 edges, asked 100 each, and 4 of up to 3000 nodes and
`10^4` edges, asked 1000 each. `dist.py` mirrors the ★ arm and its
output is byte-identical.

```
true
false
true
false
false
true
3000 graphs of up to 8 nodes and 10 edges, 10 queries each: 11307 paths, checksum 337852457
100 graphs of up to 1000 nodes and 1500 edges, 100 queries each: 4067 paths, checksum 725066428
4 graphs of up to 3000 nodes and 10000 edges, 1000 queries each: 1278 paths, checksum 888140900
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a path from p to q whose every edge is strictly below the
limit, sought by trying every path that visits no node twice, edge by
edge. It checks 3000 random problems: a graph of 2 to 6 nodes and up to
8 edges of weight 1 to 5, asked 6 questions of two different nodes and
a limit of 1 to 6. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | the edges listed in reverse, each turned round, give the same answers |
| P3 | every weight doubled, and every limit L made 2L - 1, give the same answers |
| P4 | each question asked from q to p gives the same answer |
| P5 | each arm agrees with at least two of the other three |

P3 holds because a weight w is below L exactly when 2w is below
2L - 1, so it catches an arm that lets an edge equal to the limit
through. The differential prints `3000 problems: checksum 702484237,
60000 checks over 4 arms: 0 failures` under every lane in Verification,
and a Python reading of the statement, a flood fill over the edges below
each limit, gives the same checksum. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M2, the link's weight hung on
the new root `a` rather than on `b`, was replaced because it hangs: a
root then carries a weight below the limit, and the climb, at a node
that is its own parent, never ends. M1, M4 and M9 each let an edge equal
to the limit through, and all three fail the very same checks: P3, with
weights doubled and the limit made odd, is the property built to catch
it.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a link equal to the limit climbed | P1 1360, P3 1360, P5 1360 |
| M2 | ★: each link weighed one more than its edge | P1 1400, P5 1400 |
| M3 | ★: the edges joined in the order given, not by weight | P1 970, P2 1211, P5 970 |
| M4 | search: an edge equal to the limit walked | P1 1360, P3 1360, P5 1360 |
| M5 | search: each edge listed only from its first node | P1 1486, P2 1815, P4 1815, P5 1486 |
| M6 | lifting: the last steps to the common ancestor left out of the heaviest edge | P1 409, P2 95, P5 409 |
| M7 | lifting: two nodes in different trees not refused | P1 1310, P5 1310 |
| M8 | lifting: a jump of 2^j keeping only its first half's heaviest edge | P1 196, P2 34, P5 196 |
| M9 | tree: an ancestor of weight equal to the limit climbed | P1 1360, P3 1360, P5 1360 |
| M10 | tree: the jumps tried smallest first | P1 225, P2 131, P5 225 |

## Benchmarks

The bench draws 20 random graphs of `10^4` nodes and `10^4` edges of
weight up to `10^9`, each with `10^4` queries, LeetCode's largest, all of
them first; then 50 times over, each graph is built anew by the ★ arm
and asked all its queries, in all five languages. Every implementation
prints `20 graphs of 10000 nodes and 10000 edges, 10000 queries each, 50
rounds: 1638550 paths, checksum 22505057`. The build's sort is most of
the work: Kāra's and Rust's `sort_by_key` and Go's `sort.SliceStable`
are stable sorts, Python's `sorted` too, and C's `qsort` is not; the
answers do not depend on the order of edges of equal weight. The C
build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.964 s |
| Kāra (`karac build`) | 0.991 s |
| Rust (`rustc -O`) | 1.122 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.124 s |
| C (`clang -O3`) | 1.436 s |
| Go | 6.386 s |
| Python | 11 s |

The sequential Kāra build is 14% faster than Rust and 14% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.990 s and 1.008 s on one
run).

## Verification

All four arms print the same output as `dist.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm checked clean as first written: a `struct` with a `new` that
takes the edges by reference and sorts a `clone()`, and `query` and
`root_below` taking `self`, which borrows.

The other three took one `karac fix` each. The search and tree arms had
two `p as i64` and `q as i64` casts each that `lossless_cast` dropped,
the `i32` widening by itself where an `i64` is wanted. The lifting arm
was written `let (mut a, mut b) = (p as i64, q as i64);`, as Rust has
it; the parser's E0001 says that `mut` goes before the whole pattern in
Kāra and its fix wrote `let mut (a, b) = ...`.

The bench first passed `edge_list.clone()` to `new`; `redundant_clone`
said the parameter only borrows it, and the fix dropped the clone.

The differential's literal reading first cast its `i32` nodes to `i64`
the same way; the same warning named them, and they were dropped in
the generator's source, from which the file is made.
`arm_name` in it indexes a list of string literals for a `Str`, as
#1662's does (B-2026-11-19-131).
