# 2846. Minimum Edge Weight Equilibrium Queries in a Tree

There is an undirected tree with `n` nodes labeled from `0` to `n -
1`. You are given the integer `n` and a 2D integer array `edges` of
length `n - 1`, where `edges[i] = [ui, vi, wi]` indicates that there is
an edge between nodes `ui` and `vi` with weight `wi` in the tree.

You are also given a 2D integer array `queries` of length `m`, where
`queries[i] = [ai, bi]`. For each query, find the **minimum number of
operations** required to make the weight of every edge on the path
from `ai` to `bi` equal. In one operation, you can choose any edge of
the tree and change its weight to any value.

**Note** that queries are **independent** of each other, meaning that
the tree returns to its **initial state** on each new query; the path
from `ai` to `bi` is a sequence of **distinct** nodes starting with
node `ai` and ending with node `bi` such that every two adjacent nodes
in the sequence share an edge in the tree.

Return *an array* `answer` *of length* `m` *where* `answer[i]` *is the
answer to the* `ith` *query*.

```
n = 7, edges = [[0,1,1],[1,2,1],[2,3,1],[3,4,2],[4,5,2],[5,6,2]],
queries = [[0,3],[3,6],[2,6],[0,6]]                      ->  [0,0,1,3]
n = 8, edges = [[1,2,6],[1,3,4],[2,4,6],[2,5,3],[3,6,6],[3,0,8],[7,0,2]],
queries = [[4,6],[0,4],[6,5],[7,4]]                      ->  [1,2,2,3]
```

**Constraints:** `1 <= n <= 10^4`; `edges.length == n - 1`;
`edges[i].length == 3`; `0 <= ui, vi < n`; `1 <= wi <= 26`; the input
is generated such that `edges` represents a valid tree; `1 <=
queries.length == m <= 2 * 10^4`; `queries[i].length == 2`; `0 <= ai,
bi < n`.

## Approaches

| file | mechanism |
|---|---|
| `equilibrium.kara` ★ | the tree rooted at 0 by a breadth-first walk over a `VecDeque`, each node holding the count of every weight on its path from the root; each query's lowest common ancestor by binary lifting in a closure, so the path's count of a weight is two nodes' counts less twice the ancestor's, and every edge but those of the commonest weight changes |
| `equilibrium_walk.kara` | each path walked: parents, depths and the weight above each node by a depth-first walk with a stack; the deeper end climbs until the two meet, the weights counted in an `Array[i64, 27]`; O(n) a query, for the harness's sizes |
| `equilibrium_euler.kara` | an Euler tour by recursion with `mut ref` tables, and the lowest common ancestor as the shallowest node of the tour between two nodes' first places, read from a sparse table of minima in O(1) |
| `equilibrium_tarjan.kara` | every ancestor offline by Tarjan's method: a depth-first walk with an explicit stack of (node, next edge) frames, a finished node joining its parent's set in a union-find held by a struct with a path-halving `find(mut ref self, ..)` method |
| `equilibrium_solution.kara` | a Rust solution as LeetCode's Rust users write it: `vec![vec![]; n]` adjacency of `(usize, usize)`, a `fn dfs` nested in the method taking `&mut Vec<..>` tables, `[i32; 27]` counts copied down by assignment, binary lifting with `std::mem::swap`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one node;
a path of 2000 nodes, its weights in runs of 300, asked end to end, the
other way, from a node to itself and from the middle; then 2000 random
trees of 1 to 10 nodes with weights up to 3, 5 queries each, and 20 of
up to 2000 nodes with weights up to 26, 500 queries each, as totals and
checksums. `equilibrium.py` mirrors the ★ arm and its output is
byte-identical.

```
[0, 0, 1, 3]
[1, 2, 2, 3]
[0]
[1699, 1699, 0, 101]
2000 small trees: 4344 operations, checksum 744546879
20 large trees: 88733 operations, checksum 969085936
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: each query's path found by a breadth-first search from
a that remembers how each node was reached, the weights along it from
b back to a counted, and every edge but those of the commonest weight
changed. It draws 2000 random trees of 1 to 10 nodes with weights up to
3, then 50 of up to 500 nodes with weights up to 26, 10 queries each,
all before any arm answers.

| | property |
|---|---|
| P1 | the answers are the literal reading's |
| P2 | every query's ends the other way round: the same answers |
| P3 | every weight w made 27 - w: the same answers |
| P4 | every node v renamed n - 1 - v, so that the root moves: the same answers |
| P5 | each query's first end asked against itself: all 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 490032344, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the lifting table three levels deep | P1 15, P4 20, P6 15 |
| M2 | ★: the ancestor's counts taken once, not twice | P1 1361, P4 1396, P5 1438, P6 1361 |
| M3 | ★: the climb to equal depth one step short | P1 1241, P4 1348, P6 1241 |
| M4 | walk: the climbing end not the deeper one | killed under both: runtime error: index out of bounds |
| M5 | walk: the commonest weight not spared | P1 1825, P6 1825 |
| M6 | euler: the tour's range one short | killed under both: runtime error: index out of bounds |
| M7 | euler: the deeper of the two minima taken | P1 1245, P4 1265, P6 1245 |
| M8 | tarjan: a finished node's set not moved to its parent | P1 1825, P4 1534, P5 1822, P6 1825 |
| M9 | tarjan: a query answered while its other end is unfinished | P1 1423, P4 1487, P5 1438, P6 1423 |
| M10 | solution: the climb by the wrong bits | P1 1361, P4 1396, P5 1438, P6 1361 |

## Benchmarks

The bench draws 10 random trees of 10^4 nodes with 2 x 10^4 queries
each, LeetCode's most, all of them first, then answers each 5 times by
the ★ arm in all five languages, the tables built afresh each time. C
keeps the adjacency as one compressed array and the counts as one flat
table. Every implementation prints `10 trees of 10000, 20000 queries, 5
rounds: 12855710 operations, checksum 19422092`.

BENCHTAB

## Verification

All five arms print the same output as `equilibrium.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ arm, as first written, destructured `let (mut x, mut y) = ..`, as
Rust does, and `karac check` reported E0001 twice, "`mut x` inside a
pattern is Rust syntax -- in Kāra `mut` goes before the whole pattern";
`karac fix` wrote `let mut (x, y) = ..`. The Tarjan arm's method was
first written `fn find(self: mut ref Sets, ..)`, and E0001, "a
receiver's mode goes before `self`", was fixed to `fn find(mut ref
self, ..)`. The other arms checked clean.

LeetCode's Rust template took 97 `karac fix` edits in one run, the
wrapper included: the `fn dfs` nested in the method moved out to the
top level, its `&Vec<..>` and `&mut Vec<..>` parameters becoming `ref`
and `mut ref`, `[i32; 27]` becoming `Array[i32, 27]`, and its call
marking `mut up, mut depth, mut cnt`; `struct Solution {}` added for
the `impl`; `usize` became `i64` throughout, `as usize` `as i64`, and
`usize::MAX` `i64.MAX`; `vec![vec![]; n]` became `Vec.filled(n,
Vec.new())` and `vec![vec![0usize; n]; LOG]` `Vec.filled(LOG,
Vec.filled(n, 0))`; `for e in &edges` became `for e in ref edges` and
`for &(v, w) in &g[u]` `for (v, w) in ref g[u]`; the closure's `|mut a:
usize, mut b: usize| -> usize` became plain parameters rebound with
`let mut`, and `std::mem::swap(&mut a, &mut b)` `swap(mut a, mut b)`;
`let mut mx = 0` took `: i32`; in the wrapper the `-> Vec<Vec<i32>>`
closure's type moved to its binding, `|&x|` lost its `&`, and
`Solution::` took `.`. The copy `cnt[v] = cnt[u]` of an `Array[i32,
27]` element was accepted as written.
