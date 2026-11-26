# 1786. Number of Restricted Paths From First to Last Node

There is an undirected, weighted, connected graph of `n` nodes labelled
`1` to `n`, given as `edges`, where `edges[i] = [u, v, w]` is an edge
between `u` and `v` of weight `w`. Let `distanceToLastNode(x)` be the
shortest distance from node `x` to node `n`. A restricted path is a path
from node `1` to node `n` along which `distanceToLastNode` strictly
decreases at every step. Return the number of restricted paths, modulo
`10^9 + 7`.

```
n = 5, edges = [[1,2,3],[1,3,3],[2,3,1],[1,4,2],[5,2,2],[3,5,1],[5,4,10]]          ->  3
n = 7, edges = [[1,3,1],[4,1,2],[7,3,4],[2,5,3],[5,6,1],[6,7,2],[7,5,3],[2,6,4]]    ->  1
```

**Constraints:** `1 <= n <= 2 * 10^4`, `n - 1 <= edges.length <= 4 *
10^4`, `1 <= w <= 10^5`, no two edges join the same pair of nodes, and
the graph is connected.

The arms are `fn count_restricted_paths(n: i32, edges: Vec[Vec[i32]]) ->
i32`.

## Approaches

| file | mechanism |
|---|---|
| `count_restricted_paths.kara` ★ | Dijkstra from node `n` with a smallest-first `PriorityQueue` of `(distance, node)`, a node settled the first time it is popped, so the nodes settle in order of their distance to `n`; in that order each node's restricted paths are the sum of its strictly nearer neighbours'. The distances pass `i32` (20000 edges of `10^5`), so they are `i64`. O(E log E) |
| `count_restricted_paths_memo.kara` | Dijkstra that keeps each node's best distance so far and skips stale entries, then a depth-first count from node 1, memoized: the paths from a node are the paths from each strictly nearer neighbour. O(E log E) |
| `count_restricted_paths_dense.kara` | Dijkstra without a heap, each round settling the nearest unsettled node by a scan of all of them; then the nodes sorted by distance with `sort_by_key` and summed as in the ★ arm. O(n^2 + E) |
| `count_restricted_paths_kahn.kara` | the distances by SPFA, Bellman-Ford with a `VecDeque` of the nodes whose distance just fell; then each edge pointed from its farther end to its nearer, a DAG, and the paths from node 1 carried forward in Kahn's topological order. O(n E) at worst |
| `count_restricted_paths_solution.kara` | a Rust solution as LeetCode's Rust users write it (`BinaryHeap` of `Reverse((d, u))` from `std::collections`, `vec![vec![]; n + 1]` indexed through `as usize`, `i64::MAX`, `sort_by_key(\|&i\| dist[i])`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`3 1`); four
edges, one node, two nodes, a triangle whose long edge is a second path,
and a square whose two middle nodes are as far from the end and joined
by an edge no restricted path takes (`1 1 2 2`); the constraints' most,
a line of 20000 nodes each edge `10^5`, whose distances pass `i32`, a
ladder of two rails of 10000 nodes with unit weights, which has one
restricted path for each rung, and a random graph of 20000 nodes and
40000 edges (`the most: 1 10000 16`); and 2000 random graphs of 1 to 12
nodes and up to 12 more edges, the weights from 1 to 4 so that distances
tie (`2000 random graphs: checksum 891211409`).
`count_restricted_paths.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, memo, dense and kahn arms check clean as first
written. The harness bound LeetCode's examples and the edge cases as
`let first = [[1, 2, 3], ...].to_vec();`, a `Vec[Vec[i64]]` by the
literals' default, and check refuses it where it is given to the arms'
`Vec[Vec[i32]]` parameter: "a number held inside a collection, an
`Option` or a tuple keeps its type". There is no machine fix, so the
four bindings take the annotation the message asks for, `let first:
Vec[Vec[i32]] = ...`; the same literal given straight to the call,
`count_restricted_paths(2, [[1, 2, 7]].to_vec())`, takes the parameter's
type. The line and the ladder push `[v, v + 1, 100000].to_vec()` for `v`
in a range of literals, an `i64`, so each range's first literal takes
the suffix the message asks for, `1i32..20000`; `karac fix` offers no
fix for it here. The Rust solution takes one round of 36 fixes by `karac
fix`'s count, and its diff is: the two `use` lines deleted, `struct
Solution;` to `struct Solution {}`, `Vec<..>` to `Vec[..]`, each `usize`
to `i64`, `vec![..; n]` to `Vec.filled(..)`, `i64::MAX` to `i64.MAX`,
`BinaryHeap::new()` to `PriorityQueue.new()` and each `Reverse(..)`
unwrapped, since Kāra's queue pops the smallest first, `0i64` to `0`,
`for e in &edges` to `for e in ref edges`, the `&` dropped from `for
&(v, w)` and `|&i|`, and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each node's distance to `n` by Floyd-Warshall over every
pair, then every path from 1 to `n` that visits no node twice tried, and
those whose distances fall at every step counted, while there are at
most 8 nodes. LeetCode's examples, the four edges, a line of 2000 nodes
each edge `10^5`, a ladder of two rails of 1000 nodes, a random graph of
2000 nodes and 4000 edges, and 1991 random graphs, seven in eight of 1
to 8 nodes and the rest of 9 to 40, with up to 8 more edges and weights
from 1 to 4. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, while there are at most 8 nodes |
| P2 | the nodes between the first and the last relabelled in reverse give the same answer |
| P3 | every weight doubled gives the same answer |
| P4 | the edges listed backwards, each written from its other end, give the same answer |
| P5 | a node past the last, joined to it alone, gives the same answer |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 58,745 checks pass
on every arm: `2000 cases: checksum 707916387, 58745 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the ★ arm's mirror over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a neighbour as far from n counted as nearer | P1 41, P2 86, P6 176 |
| M2 | ★: each edge's weight taken as 1 in the search | P1 390, P6 1816 |
| M3 | memo: no path counted on reaching n | P1 1749, P6 2000 |
| M4 | memo: a node queued at the distance it was reached from | P1 725, P5 888, P6 951 |
| M5 | dense: a settled node taken again as the nearest | P1 347, P5 756, P6 535 |
| M6 | dense: the nodes summed farthest first | P1 891, P5 842, P6 1126 |
| M7 | kahn: a node never queued again once it has left the queue | P6 1 |
| M8 | kahn: each edge into a node counted as one path | P1 607, P5 814, P6 689 |
| M9 | solution: the nodes summed from the last label down | P1 103, P2 521, P6 144 |
| M10 | solution: each edge's weight taken as 1 | P1 390, P6 454 |

## Benchmarks

The bench builds 200 random graphs of 2000 nodes and up to 4000 edges
once, weights up to `10^5`, and makes 1000 calls of the ★ arm, each
graph drawn from the checksum so far. It checks clean as first written.
Every implementation prints `1000 calls over 200 graphs: checksum
518086387`. The C mirror carries its own binary heap; the Go mirror uses
`container/heap`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.70 s against Rust's 0.67 s (0.76 s with overflow checks
on), C's 0.65 s and Go's 1.9 s; Python takes 6.1 s.
