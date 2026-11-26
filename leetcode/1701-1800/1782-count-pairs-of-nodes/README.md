# 1782. Count Pairs Of Nodes

You are given an undirected graph defined by an integer `n`, the number
of nodes, and a 2D integer array `edges`, the edges in the graph, where
`edges[i] = [u_i, v_i]` indicates that there is an undirected edge
between `u_i` and `v_i`. You are also given an integer array `queries`.
Let `incident(a, b)` be defined as the number of edges that are
connected to either node `a` or `b`. The answer to the `j`th query is
the number of pairs of nodes `(a, b)` that satisfy both of the following
conditions: `a < b`, and `incident(a, b) > queries[j]`. Return an array
`answers` such that `answers.length == queries.length` and `answers[j]`
is the answer of the `j`th query. Note that there can be multiple edges
between the same two nodes.

```
n = 4, edges = [[1,2],[2,4],[1,3],[2,3],[2,1]], queries = [2,3]                      ->  [6,5]
n = 5, edges = [[1,5],[1,5],[3,4],[2,5],[1,3],[5,1],[2,3],[2,5]], queries = [1,2,3,4,5]  ->  [10,10,9,8,6]
```

**Constraints:** `2 <= n <= 2 * 10^4`, `1 <= edges.length <= 10^5`, `1
<= u_i, v_i <= n`, `u_i != v_i`, `1 <= queries.length <= 20`, and `0 <=
queries[j] < edges.length`.

The arms are `fn count_pairs(n: i32, edges: Vec[Vec[i32]], queries:
Vec[i32]) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `count_pairs.kara` ★ | the pairs whose degrees sum above the query, counted by two pointers over the sorted degrees, less each joined pair that only passes by counting its shared edges in both degrees; the shared edges are counted in a `Map` keyed by the ordered pair. O(n log n + q (n + m)) |
| `count_pairs_binary.kara` | the sorted degrees searched with `partition_point`: for each node, the nodes after it whose degree is enough, then the joined pairs corrected as in the ★ arm. O(n log n + q (n log n + m)) |
| `count_pairs_counting.kara` | how many nodes have at least each degree, so that a node's partners above the query are one lookup; every pair is found from both its ends, so the total is halved. O(n + m + q (n + m)) |
| `count_pairs_runs.kara` | no map: the edges as ordered pairs, sorted, so that each joined pair's shared edges are one run; the pairs above the query counted by two pointers as in the ★ arm. O(m log m + n log n + q (n + m)) |
| `count_pairs_solution.kara` | a Rust solution as LeetCode's Rust users write it (`use std::collections::HashMap`, `usize` nodes, `std::mem::swap`, `for (&(u, v), &c) in &cnt`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`[6, 5] [10,
10, 9, 8, 6]`); four edges, two nodes and one edge, one edge three times
over, nodes with no edge, and a star (`[1, 0] [1, 1, 0] [5] [10, 4]`);
the constraints' most, 20000 nodes with 100000 random edges and 20
queries, then 100000 edges among the first 50 nodes so that pairs share
many, each answer list digested (`the most: 911111053 448084960`); and
3000 random cases of 2 to 10 nodes, 1 to 15 edges and 1 to 5 queries
(`3000 random cases: checksum 256381157`). `count_pairs.py` mirrors the
★ arm, and its output is byte-identical. The arms only sum over the
`Map`'s pairs, so its order does not reach the output. Every arm gives
the same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★, binary, counting and runs arms check clean as
first written. The Rust solution takes one round of 47 fixes by `karac
fix`'s count, and its diff is: the `use std::collections::HashMap;` line
deleted, since `Map` is in the prelude, and `HashMap<(usize, usize),
i32>` and `HashMap::new()` to `Map[(i64, i64), i32]` and `Map.new()`;
`struct Solution;` to `struct Solution {}`; `Vec<..>` to `Vec[..]` in
both signatures; `n as usize` and each `as usize` to `as i64`; `vec![0;
n + 1]` to `Vec.filled(n + 1, 0)`; `for e in &edges` and `for &q in
&queries` to `for e in ref edges` and `for q in ref queries`; `let (mut
u, mut v)` and `let (mut l, mut r)` to `let mut (u, v)` and `let mut (l,
r)`; `std::mem::swap(&mut u, &mut v)` to `swap(mut u, mut v)`;
`Vec::with_capacity` to `Vec.with_capacity`, with the binding typed
`Vec[i32]` and `res` typed `i32`; `for (&(u, v), &c) in &cnt` to `for
((u, v), c) in ref cnt`; `&&` to `and`; and `Solution::` to `Solution.`.
Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair `a < b`, the edges touching `a` or `b` counted
from the list, and the pairs above each query. LeetCode's examples, the
edges, and 1994 random cases of 2 to 8 nodes, 1 to 12 edges and 1 to 5
queries. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | one answer per query, each from 0 to every pair, and a larger query never more |
| P3 | each edge written the other way round, and the list reversed, give the same answers |
| P4 | the nodes numbered from the other end give the same answers |
| P5 | a node with no edge added pairs with each node whose degree is above the query |
| P6 | the ★ arm's answer |

`karac fix` dropped an `as i32` on the differential's own count of
pairs, already an `i32`, as redundant, 1 fix. All 60,000 checks pass on
every arm: `2000 cases: checksum 959113176, 60000 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, counting every pair's edges from the
list, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: one pair too few counted at each step of the pointers | P1 1995, P2 254, P5 816, P6 7980 |
| M2 | ★: every joined pair above the query taken off | P1 1952, P6 7808 |
| M3 | binary: a degree sum equal to the query counted | P1 1202, P2 38, P5 1401, P6 1202 |
| M4 | binary: each node paired with itself | P1 1997, P2 1574, P6 1997 |
| M5 | counting: a node counted as its own partner | P1 1975, P2 1387, P6 1975 |
| M6 | counting: each pair counted from both its ends | P1 1995, P2 1837, P5 1837, P6 1995 |
| M7 | runs: the edges grouped by their first node alone | P1 879, P4 789, P6 879 |
| M8 | runs: each joined pair taken to share one edge | P1 395, P6 395 |
| M9 | solution: each joined pair's first edge counted twice | P1 1384, P6 1384 |
| M10 | solution: the smallest degree never paired | P1 1911, P2 32, P5 1199, P6 1911 |

## Benchmarks

The bench builds 10 graphs of 20000 nodes and 100000 edges once, the
edges among the first 50 to 20000 nodes, and runs the ★ arm on each with
20 queries up to twice the graph's mean degree sum, drawn from the
checksum so far. C has no map, so its mirror keeps the shared edges in
an open-addressing hash table of its own and walks every slot of it per
query. Every implementation prints `10 graphs of 100000 edges: checksum
691493276`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.19 s against Rust's 0.17 s (0.18 s with overflow checks
on), C's 0.28 s and Go's 0.35 s; Python takes 3.0 s.
