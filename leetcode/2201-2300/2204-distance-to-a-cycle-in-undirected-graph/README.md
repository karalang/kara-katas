# 2204. Distance to a Cycle in Undirected Graph

You are given a positive integer `n` representing the number of nodes in
a **connected** undirected graph containing **exactly one** cycle. The
nodes are numbered from `0` to `n - 1` (**inclusive**).

You are also given a 2D integer array `edges`, where `edges[i] = [node1i,
node2i]` denotes that there is a **bidirectional** edge connecting
`node1i` and `node2i` in the graph.

The distance between two nodes `a` and `b` is defined to be the
**minimum** number of edges that are needed to go from `a` to `b`.

Return *an integer array* `answer` *of size* `n`*, where* `answer[i]`
*is the **minimum** distance between the* `i`th *node and **any** node in
the cycle.*

```
n = 7, edges = [[1,2],[2,4],[4,3],[3,1],[0,1],[5,2],[6,5]]              ->  [1,0,0,0,0,1,2]
n = 9, edges = [[0,1],[1,2],[0,2],[2,6],[6,7],[6,8],[0,3],[3,4],[3,5]]  ->  [0,0,0,1,2,2,1,2,2]
```

**Constraints:** `3 <= n <= 10^5`; `edges.length == n`;
`edges[i].length == 2`; `0 <= node1i, node2i <= n - 1`; `node1i !=
node2i`; the graph is connected; the graph has exactly one cycle; there
is at most one edge between any pair of vertices.

A node off the cycle hangs in a tree, so peeling leaves until none is
left leaves exactly the cycle; one breadth-first search out from every
cycle node at once then gives each node its distance. O(n).

## Approaches

| file | mechanism |
|---|---|
| `cycle.kara` ★ | the degrees counted, the leaves peeled through a `VecDeque`, each lowering its neighbours' degrees, and a breadth-first search from the nodes left |
| `cycle_dfs.kara` | a depth-first search on a `Vec` stack keeping each node's parent until an edge reaches a seen node that is not the parent; the cycle is that edge's two parent chains up to the ancestor they share |
| `cycle_union.kara` | the edges joined in a disjoint-set forest with path halving; the one whose ends are already joined closes the cycle, and a breadth-first search between its ends without it, following `back` links, finds the rest |
| `cycle_struct.kara` | a `struct Graph` that `peel`s itself into a `struct Peeling` of the nodes on the cycle, on a `Vec` stack, and answers its `layers` outward from them one round at a time |
| `cycle_iter.kara` | the lists by `fold`, the leaves peeled in rounds, each the last round's neighbours left with one live neighbour by `flat_map` and `filter`, then the distances by rounds outward |
| `cycle_solution.kara` | LeetCode's Rust template: an `i32` and a `Vec<Vec<i32>>` in, `Vec<i32>` out, the graph as `vec![vec![]; n]` of `usize`, leaves peeled through a `VecDeque`, `i32::MAX` for unreached; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and four
more (a triangle alone, a path hung off a triangle, a star of leaves on
a square, and the whole graph one ring), each with its distances; then
the farthest distance and a checksum for 2000 random graphs of 3 to 12
nodes with a cycle of 3 to all of them; then the constraints' largest,
10^5 nodes with a cycle of 3, of 1000 and of all of them, and a path of
99997 hung off a triangle. `cycle.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in three rounds of 14, 3 and 5 edits:
first Rust's spellings (`Vec<..>` to brackets, `VecDeque::new()` to
`VecDeque.new()`, `for &v in &g[u]` to `for v in ref g[u]`, `::` to
`.` in `i32::MAX`, `struct Solution;` to `struct Solution {}`, and the
`use` dropped); then `vec![x; n]` to `Vec.filled(n, x)` where `x` is
already Kāra, and the inner `vec![]` to `Vec.new()`; then the outer
`vec![..; n]` to `Vec.filled`, `0usize` to `0`, and `as usize` to `as
i64`, since indices are `i64` in Kāra.

The iter arm's first draft marked a round's leaves with `for_each(|v|
live[v] = false)`, an assignment as the whole closure body, which Kāra
refuses; `karac fix` writes the block `|v| { live[v] = false; }`. Its
first draft also took each round's leaves by scanning every node, which
on the path of 99997 is a round per node and ran 95 s; it now looks only
at the last round's neighbours.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a node is on the cycle when one of its edges leaves it and
comes back another way, found by a search with that edge taken out, and
each node's distance by its own breadth-first search to the nearest such
node. It checks 300 random graphs of 3 to 9 nodes with a cycle of 3 to
all of them; then 30 that are one ring; then 30 of 10 to 14 nodes on a
triangle. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the distances are the statement read literally |
| P2 | the nodes at 0 are 3 or more and the edges among them as many, and every other node has a neighbour one nearer |
| P3 | the edges listed in reverse, each with its ends swapped: the same |
| P4 | every node v renamed n - 1 - v: the distances in reverse |
| P5 | a new leaf hung on node 0: the same for the rest, and the leaf one farther than node 0 |
| P6 | each arm agrees with at least three of the other five |

The turned and renamed edges are built with a typed binding in each
closure: a list literal a closure returns is a `Vec`, a closure cannot
declare its return type, and `collect` into a `Vec[Array[i64, 2]]`
fails with no fix; kara B-2026-11-15-38 asks for the closure's literal to
follow the type the `collect` wants.

The differential prints `360 cases: checksum 554077482, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that finds
the cycle another way, by trying every simple path from a node back to
itself. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-three edits to the differential, six to the ★ arm, seven to the
union arm and five to each other arm, each run under `karac
__mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node of degree 2 taken as a leaf | P1 355, P2 355, P5 357, P6 355 |
| M2 | ★: a neighbour left at degree 1 not queued | P1 93, P5 70, P6 93 |
| M5 | ★: an edge counted on one end only | P1 327, P2 299, P3 301, P4 151, P5 128, P6 327 |
| M7 | dfs: the cycle taken from b alone | P1 360, P2 360, P3 360, P4 248, P6 360 |
| M8 | dfs: the meeting node left off the cycle | P1 360, P2 360, P4 316, P6 360 |
| M9 | dfs: the back edge taken to the parent too | P1 295, P2 295, P3 264, P4 307, P5 360, P6 295 |
| M14 | union: the path back stopping one short | P1 360, P2 360, P3 279, P6 360 |
| M16 | union: the closing edge's own end a not on the cycle | P1 360, P2 360, P3 302, P6 360 |
| M32 | union: the closing edge kept in the search between its ends | P1 360, P2 360, P3 360, P6 360 |
| M17 | struct: the degree one more | P1 220, P5 360, P6 220 |
| M19 | struct: a layer's depth counted before it is reached | P1 220, P2 220, P5 360, P6 220 |
| M20 | struct: the cycle marked -1 and the rest 0 | P1 360, P2 360, P5 360, P6 360 |
| M22 | iter: the first leaves by two neighbours | P1 360, P2 356, P5 360, P6 360 |
| M25 | iter: the depth from 0 at the first round | P1 220, P5 267, P6 220 |
| M26 | iter: the ring's neighbours on the cycle too | P1 143, P4 130, P5 122, P6 143 |
| M30 | solution: the adapter's edges with one end on node 0 | P1 360, P2 360, P4 360, P5 360, P6 360 |
| M31 | solution: the adapter's answer reversed | P1 208, P2 208, P5 360, P6 208 |
[('P1', 17), ('P2', 13), ('P3', 6), ('P4', 6), ('P5', 12), ('P6', 17)]

P1 and P6 kill all seventeen, P2 thirteen, P5 twelve, P3 six and P4
six. P2 misses the four whose distances still step down one at a time
to a set of 0s that closes on itself (M2, M17, M25, M26). P3 turns every
edge round and reverses the list, and kills the six whose cycle depends
on which end of which edge comes first: the ★ arm's edge counted on one
end, and every kept edit to the dfs and union arms (M5, M7, M9, M14,
M16, M32). P4 renames the nodes and kills the six whose answer depends
on a node's number (M5, M7, M8, M9, M26, M30). P5 hangs a new leaf on
node 0 and kills the twelve that answer a leaf or a tree differently.

Of the thirty-three, sixteen were not kept. Four are equivalent: the ★
arm's search outward depth first (M4), since each node off the cycle is
reached only through its parent; the union arm's first joined edge taken
as closing (M12), since the true closing edge comes later and overwrites
it, and its closing edge left out of the search outward (M13), since
both its ends are already at 0; and the template's popped leaf keeping
its degree (M28), which stays below 2. Two crash on an index out of
bounds: the dfs arm's meeting walked from `a`'s own side (M10), and the
union arm's roots never joined (M15). One never ends: the struct arm's
node reached twice kept at the later depth (M21), which bounces between
two layers. Five fail as a kept one does: the ★ arm's peeled nodes at 0
and the template's cycle at degree 3 or more (M6, M27) as M20; the
struct arm's leaf peeled without lowering its neighbours and the iter
arm's peel stopping after one round (M18, M24) as M2; and the iter arm's
two-neighbour nodes peeled (M23) as M19. Three fail alike, each step set
one farther than the cycle rather than one farther than its parent in
the ★, dfs and template arms (M3, M11, M29). M32 and M33 were added to
the union arm when three of its first five survived or crashed; M33 is
left out for the count.

## Verification

Every arm prints the same output as `cycle.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, dfs, union and struct arms take 5.2 s to
6.0 s, the template 10.0 s and the iter arm 15.5 s, which collects a
`Vec` for each round; the four graphs of 10^5 nodes are most of it. The
differential takes 1.4 s.

## Benchmarks

The bench builds 6 graphs of 10^5 nodes once, with cycles of 3, 10, 100,
1000, 10^4 and 10^5 nodes, then answers each 5 times over with the ★ arm
in all five languages; each answer is checked by its sum and its middle
distance. Every implementation prints `5 passes over 6 graphs: checksum
214002247`.

BENCHTAB
