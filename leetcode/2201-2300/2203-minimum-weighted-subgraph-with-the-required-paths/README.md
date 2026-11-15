# 2203. Minimum Weighted Subgraph With the Required Paths

You are given an integer `n` denoting the number of nodes of a
**weighted directed** graph. The nodes are numbered from `0` to `n - 1`.

You are also given a 2D integer array `edges` where `edges[i] = [fromi,
toi, weighti]` denotes that there exists a **directed** edge from
`fromi` to `toi` with weight `weighti`.

Lastly, you are given three **distinct** integers `src1`, `src2`, and
`dest` denoting three distinct nodes of the graph.

Return *the **minimum weight** of a subgraph of the graph such that it is
**possible** to reach* `dest` *from both* `src1` *and* `src2` *via a set
of edges of this subgraph*. In case such a subgraph does not exist,
return `-1`.

A **subgraph** is a graph whose vertices and edges are subsets of the
original graph. The **weight** of a subgraph is the sum of weights of
its constituent edges.

```
n = 6, edges = [[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],[4,5,1]],
src1 = 0, src2 = 1, dest = 5  ->  9
n = 3, edges = [[0,1,1],[2,1,1]], src1 = 0, src2 = 1, dest = 2  ->  -1
```

**Constraints:** `3 <= n <= 10^5`; `0 <= edges.length <= 10^5`;
`edges[i].length == 3`; `0 <= fromi, toi, src1, src2, dest <= n - 1`;
`fromi != toi`; `src1`, `src2`, and `dest` are pairwise distinct; `1 <=
weight[i] <= 10^5`.

In a least subgraph the two paths meet at some node and run on together
to `dest`, so the answer is the least, over every node v, of the
distance from `src1` to v, from `src2` to v and from v to `dest`. Three
Dijkstras find them, the last over the edges turned round. O((n + m) log
m).

## Approaches

| file | mechanism |
|---|---|
| `subgraph.kara` ★ | three Dijkstras over `Vec.filled` adjacency lists with a smallest-first `PriorityQueue` of (distance, node), a node settled when it is first popped, -1 for unreached; then the least sum over every node |
| `subgraph_relax.kara` | each distance by Bellman-Ford's relaxation driven by a `VecDeque` (SPFA): a node whose distance falls is queued, once at a time, until nothing falls. O(n m) at worst |
| `subgraph_ordered.kara` | Dijkstra with a `SortedSet` of (distance, node) as the queue, a node's entry taken out by `remove` and put back lower when a shorter path reaches it, popped by `pop_first` |
| `subgraph_struct.kara` | a `struct Graph` of `struct Edge`s, with `add`, `reversed` and `distances(from)`, each distance an `Option[i64]`, and the meeting found by matching three `Some`s |
| `subgraph_iter.kara` | the adjacency lists by `fold`, Dijkstra with a largest-first `PriorityQueue.max_first()` of `Reverse` distances (`import std.cmp.Reverse`), out-edges pushed by `filter` and `for_each`, and the meeting by `filter_map` and `min` |
| `subgraph_solution.kara` | LeetCode's Rust template: `i32`s and a `Vec<Vec<i32>>` in, `i64` out, the graphs as `vec![vec![]; n]` of `(usize, i64)`, a nested `fn dijkstra` over a `BinaryHeap` of `Reverse` pairs with `i64::MAX` for unreached; carried by `karac fix` in seven rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one path through the other source, two paths that only meet at `dest`,
parallel edges, and no edges at all), each with its weight; then the
count with no subgraph and a checksum for 2000 random graphs of 3 to 10
nodes and 0 to 20 edges weighing 1 to 10; then the constraints'
largest, 10^5 nodes and 10^5 edges weighing up to 10^5 at random, and
the same with a ring of 10^4 edges through every tenth node in place of
10^4 of them. `subgraph.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in seven rounds of 26, 3, 4, 4, 3, 8
and 3 edits: first Rust's spellings (`Vec<..>` to brackets, `&` borrows
to `ref`, `&(v, w)` to `(v, w)`, `::` to `.` in `i64::MAX` and
`BinaryHeap::new`, `&&` to `and`, `struct Solution;` to `struct Solution
{}`, and the `Reverse` import dropped); then the nested `fn dijkstra`
moved out to the top level and the `BinaryHeap` import dropped; then the
`BinaryHeap` of `Reverse` pairs turned into a smallest-first
`PriorityQueue` of the pairs; then `vec![i64.MAX; ..]` to `Vec.filled`,
`0i64` to `0` and the inner `vec![]` to `Vec.new()`; then the outer
`vec![..; n]` to `Vec.filled` and the `ref` parameter to a bare one;
then every `usize` to `i64`, since `len()` and indices are `i64` in
Kāra; and last the three `as i64` casts on the `i32` sources dropped,
since an `i32` widens to `i64` implicitly.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subset of the edges tried, kept when `dest` can be
reached in it from both `src1` and `src2`, and the least total weight
among those kept; no distance. It checks 300 random graphs of 3 to 6
nodes and 0 to 9 edges weighing up to 3, 10 and 10^5 in turn; then 30
that hold a path `src1 -> src2 -> dest`; then 30 of 7 or 8 nodes and 9
edges weighing up to 10^5. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the weight is the statement read literally |
| P2 | it is -1 exactly when `dest` cannot be reached from `src1` or from `src2`, and otherwise at most the weight of every edge |
| P3 | the edges listed in reverse: the same weight |
| P4 | `src1` and `src2` swapped: the same weight |
| P5 | every weight doubled: the weight doubled, or -1 still |
| P6 | each arm agrees with at least three of the other five |

The doubled edges are built with a typed binding in the closure: a list
literal a closure returns is a `Vec`, a closure cannot declare its
return type, and `collect` into a `Vec[Array[i64, 3]]` fails with no
fix; kara B-2026-11-15-38 asks for the closure's literal to follow the type
the `collect` wants.

The differential prints `360 cases: checksum 486429651, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
cases. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-three edits to the differential, six to the ★ arm, seven to the
ordered arm and five to each other arm, each run under `karac
__mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the reverse graph not turned round | P1 157, P2 79, P6 157 |
| M3 | ★: the edge's weight left off | P1 117, P5 122, P6 117 |
| M5 | ★: the second path from src1 | P1 99, P2 35, P4 177, P6 99 |
| M7 | relax: a shorter path not taken once reached | P1 27, P3 46, P6 27 |
| M8 | relax: a lowered node not queued again | P1 17, P2 8, P6 17 |
| M10 | relax: only the first out-edge relaxed | P1 48, P2 4, P3 82, P6 48 |
| M15 | ordered: the source's distance unset | P1 120, P2 34, P6 120 |
| M16 | ordered: the home distances from src2 | P1 180, P2 74, P4 206, P6 180 |
| M33 | ordered: a node's first out-edge skipped | P1 105, P2 81, P3 43, P6 105 |
| M18 | struct: an edge's weight doubled | P1 122, P2 26, P6 122 |
| M19 | struct: the last node never a meeting | P1 20, P2 3, P6 20 |
| M21 | struct: a node settled before it is popped | P1 42, P2 18, P3 38, P6 42 |
| M23 | iter: the queue largest first without the Reverse | P1 69, P6 69 |
| M24 | iter: the first meeting node, not the least | P1 67, P2 8, P6 67 |
| M26 | iter: the two paths' sum for the three | P1 42, P6 42 |
| M29 | solution: the weight truncated to 15 bits | P1 30, P5 32, P6 30 |
| M31 | solution: the adapter's dest one on | P1 156, P2 77, P6 156 |
[('P1', 17), ('P2', 12), ('P3', 4), ('P4', 2), ('P5', 2), ('P6', 17)]

P1 and P6 kill all seventeen, P2 twelve, P3 four, P4 two and P5 two. P2
misses the five that still find a subgraph exactly when one exists and
only weigh it wrongly (M3, M7, M23, M26, M29). P3 reorders the edges and
kills the four whose answer hangs on which out-edge comes first (M7,
M10, M21, M33). P4 swaps the sources and kills only the two that treat
them unequally (M5, M16). P5 doubles every weight and kills the two
that drop or cut a weight (M3, M29), whose answers do not double.

Of the thirty-three, sixteen were not kept. Four are equivalent: the
ordered arm's old entry left in the set (M12), which pops later with a
distance too large to lower anything, and the largest taken first
(M13), which still relaxes until nothing falls; the iter arm's settled
node's edges pushed again at the same distance (M25); and the template's
stale entry relaxed from its node's settled distance (M28). One never
ends: the ordered arm keeping a longer path over a shorter (M14), which
climbs a cycle for ever. Four fail as a kept one does: the reverse
graph built forward in the struct, iter and template arms (M17, M22,
M27) as M1, and the struct arm's first meeting kept (M20) as M24. Two
fail alike: the relax arm's tie and the template's largest sum (M11,
M30). M32 and M33 were added to the ordered arm when two of its first
five survived. Five fail their own way and are left out for the count:
the ★ arm's node settled twice, distance home left out and meetings only
at the three named nodes (M2, M4, M6), the relax arm's source at 1
(M9), and the ordered arm's lowered node keyed at its parent's distance
(M32).

## Verification

Every arm prints the same output as `subgraph.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the relax and ordered arms take 2.1 s and 2.8
s, the ★ and struct arms 4.3 s and 4.6 s, and the iter and template arms
6.9 s and 6.7 s; the two graphs of 10^5 nodes are most of it. The
differential takes 1.5 s.

## Benchmarks

The bench builds 4 graphs of 20000 nodes and 60000 random edges weighing
up to 10^5 once, then answers 4 triples of nodes on each 5 times over
with the ★ arm in all five languages. C and Go carry their own binary
heap of (distance, node) pairs; Rust uses `BinaryHeap` with `Reverse`;
each node's out-edges are a growable array in every language. Every
implementation prints `5 passes over 4 graphs: checksum 924226662`.

BENCHTAB
