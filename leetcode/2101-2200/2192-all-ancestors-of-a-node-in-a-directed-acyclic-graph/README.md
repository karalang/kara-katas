# 2192. All Ancestors of a Node in a Directed Acyclic Graph

You are given a positive integer `n` representing the number of nodes
of a **Directed Acyclic Graph** (DAG). The nodes are numbered from `0`
to `n - 1` (**inclusive**).

You are also given a 2D integer array `edges`, where `edges[i] =
[from_i, to_i]` denotes that there is a **unidirectional** edge from
`from_i` to `to_i` in the graph.

Return *a list* `answer`*, where* `answer[i]` *is the **list of
ancestors** of the* `i`th *node, sorted in **ascending order***.

A node `u` is an **ancestor** of another node `v` if `u` can reach `v`
via a set of edges.

```
n = 8, edges = [[0,3],[0,4],[1,3],[2,4],[2,7],[3,5],[3,6],[3,7],[4,6]]
  ->  [[],[],[],[0,1],[0,2],[0,1,3],[0,1,2,3,4],[0,1,2,3]]
n = 5, edges = [[0,1],[0,2],[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
  ->  [[],[0],[0,1],[0,1,2],[0,1,2,3]]
```

**Constraints:** `1 <= n <= 1000`; `0 <= edges.length <= min(2000, n *
(n - 1) / 2)`; `edges[i].length == 2`; `0 <= from_i, to_i <= n - 1`;
`from_i != to_i`; there are no duplicate edges; the graph is directed
and acyclic.

A walk down the edges from every node in turn reaches exactly its
descendants, and taking the starts in order fills each list sorted.
O(n (n + e)).

## Approaches

| file | mechanism |
|---|---|
| `ancestors.kara` ★ | a walk down the edges from every node in turn, by a `Vec` stack; every node it reaches gets the start as an ancestor, and since the starts go up from 0 each list comes out sorted |
| `ancestors_topo.kara` | the nodes in a topological order by Kahn's queue (a `VecDeque` of the nodes no edge still points into); each node, once taken, hands each child itself and every ancestor it has, gathered in a `SortedSet` per node; O(n e log n) |
| `ancestors_reverse.kara` | each node's ancestors found by a breadth-first walk up the edges, a `VecDeque` of the parents still to visit; the nodes met are marked and read off in order of number |
| `ancestors_struct.kara` | a `#[derive(Clone)] struct Bits`, a set of nodes as `u64` words, made `empty`, that `add`s a node and `absorb`s another set (`mut ref self`) and lists its `members` (`ref self`); each node's set filled by recursion up the edges, memoized in a `Vec[Option[Bits]]` passed `mut ref`; O(n e / 64) |
| `ancestors_iter.kara` | a topological order first, the ready nodes `filter`ed and `collect`ed into a `VecDeque`; then in that order each node's ancestors as one chain: its parents `flat_map`ped to `once(p).chain(..)` of the parent's own list, `collect`ed into a `SortedSet` and back by `into_iter` |
| `ancestors_solution.kara` | LeetCode's Rust template: `n: i32`, `Vec<Vec<i32>>`, `vec![vec![]; n]`, `vec![false; n]`, `vec![s]`, `n as usize`, `for e in &edges`, `for &v in &g[u]`, `!seen[v]`, `struct Solution;`, `Solution::`; carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one node, nodes with no edges, a chain numbered downward, and a DAG
whose edges are listed out of order), each with its lists; then the
ancestors' total and a checksum over 300 random DAGs of 1 to 25 nodes,
sparse and dense in turn, each edge from an earlier node to a later one
in a random order of the nodes and none drawn twice; then the
constraints' largest, 1000 nodes and 1990 edges (2000 drawn, the
repeats dropped), by its longest list and a checksum. `ancestors.py`
mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in four rounds of 12, 4, 5 and 1
edits: first Rust's spellings (`Vec<..>` to brackets, `for e in &edges`
and `for &v in &g[u]` to `ref`, `!` to `not`, `struct Solution;` to
`struct Solution {}`, `Solution::` to `.`); then the inner `vec![]` to
`Vec.new()`, `vec![false; n]` to `Vec.filled(n, false)` and `vec![s]` to
`[s]`; then `n as usize` to `as i64`, which lets the two outer
`vec![..; n]` become `Vec.filled(n, ..)`, and the index casts to `i64`;
then the index cast dropped, since `e[0]` is already an `i32` index.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: u is an ancestor of v when u can reach v along the edges,
found by closing a table of who reaches whom (Warshall's), with no walk
and no queue. It checks 300 random DAGs of 1 to 10 nodes, each pair of
nodes in a random order joined with a chance of 1 to 5 in 6; then 30
paths of up to 15 nodes in a random order; then 30 complete DAGs of up
to 12. The edges of each come in a random order, and all 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the lists are the statement read literally |
| P2 | each list rises strictly, within 0..n, and never holds its node |
| P3 | each list is its node's parents and their lists, and no more |
| P4 | the nodes renumbered v to n - 1 - v: the lists renumbered, sorted |
| P5 | the edges given in the reverse order: the same lists |
| P6 | each arm agrees with at least three of the other five |

P3 holds since an ancestor of v reaches v through one of v's parents,
and is that parent or one of its ancestors. P4 holds since a renumbering
keeps who reaches whom. P5 holds since the lists depend on the edges
and not on their order.

The differential prints `360 DAGs: checksum 419593486, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
DAGs. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-eight edits to the differential, seven to the ★ arm, six to the
topo, struct and template arms, five to the reverse and iter arms, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by
a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the starts from 1 | P1 183, P3 183, P4 262, P6 183 |
| M5 | ★: the node reached recorded, not the start | P1 181, P2 181, P3 181, P4 103, P5 90, P6 181 |
| M32 | ★: only later nodes reached | P1 271, P3 271, P4 293, P6 271 |
| M8 | topo: the child gets itself | P1 293, P2 293, P3 293, P6 293 |
| M9 | topo: only the first node ready | P1 128, P3 128, P4 137, P6 128 |
| M33 | topo: every node ready at once | P1 135, P3 135, P4 175, P6 135 |
| M11 | reverse: the node counts itself | P1 360, P2 360, P3 360, P6 360 |
| M14 | reverse: the list in the order met | P1 245, P2 245, P4 245, P6 245 |
| M15 | reverse: the last node never listed | P1 210, P3 210, P4 262, P6 210 |
| M19 | struct: the memo stored empty | P1 218, P3 218, P4 224, P6 218 |
| M20 | struct: absorbed by xor | P1 153, P3 153, P5 165, P6 153 |
| M35 | struct: only the first parent | P1 191, P3 191, P5 204, P6 191 |
| M21 | iter: the parent's own list left out | P1 181, P3 181, P6 181 |
| M22 | iter: the parents left out | P1 293, P3 293, P6 293 |
| M24 | iter: the waiting count one short | P1 154, P3 154, P4 78, P5 9, P6 154 |
| M37 | solution: the adapter's n one more | P1 360, P2 360, P3 360, P4 360, P6 360 |
| M38 | solution: the adapter's ancestors one more | P1 293, P2 273, P3 293, P4 293, P6 293 |

P1 and P6 kill all seventeen, P3 sixteen, P4 eleven, P2 six and P5
four. P3 misses only the list in the order met (M14), which holds the
right nodes in the wrong order; P2, which reads the order, kills it, and
otherwise sees only the edits that put a node in its own list (M8, M11)
or one out of range (M5, M37, M38). P4 renumbers the nodes, and kills
what reads the numbers: the starts from 1 (M4), only later nodes reached
(M32), the last node never listed (M15), the nodes taken in an order the
numbering sets (M9, M33, M24), the memo stored empty (M19), which
answers by the order the nodes are asked in, and the lists out of order
or out of range (M5, M14, M37, M38). P5 reverses the edges, and
kills only what reads their order: the node reached recorded (M5), the
xor (M20) and the first parent alone (M35), each of which sees a
different parent first, and the waiting count one short (M24). P5 has
no other way in, since a correct arm's lists do not depend on the
order.

Of the thirty-eight, twenty-one were not kept. Four are equivalent: the
★ arm's and the template's start never marked (M1, M27), since a walk in
a DAG never comes back to its start; the topo arm's child taken one
edge early (M7), which is taken again, and its children with it, each
time a parent finishes, so the sets still fill; and the struct arm's
top bit of a word never read (M18), which only a node from 63 up would
need, and the differential's DAGs stop at 15. One crashes: the
template's adapter's one node fewer (M28), out of bounds at the last
node's edges. Sixteen fail as a kept one does. Six fail every DAG in
which some node has an ancestor two edges up, as M21: the ★ arm's walk
one edge deep (M2) and the template's (M30), the topo arm's child given
only its parent (M6), the reverse arm's walk to the parents only
(M12), the struct arm's parent's set left out (M16), and the iter arm's
node's own list for its parent's (M23). Seven fail every DAG with an
edge, as M22: the ★ and reverse arms' edges walked the other way (M3,
M13), the iter arm's children taken as parents too (M25), the topo arm's parent given the child (M10) and child
given its parent's set but not the parent (M34), the struct arm's
parent itself left out (M17), and the template's adapter's edges
reversed (M26). The ★ arm's and the struct arm's node in its own list
(M31, M36) fail as M11, and the template's lists read back to front
(M29) as M14.


## Verification

Every arm prints the same output as `ancestors.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.5 s to 0.7 s, and the
differential 1.8 s.

## Benchmarks

The bench builds 20 DAGs of 1000 nodes and 2000 edges once, each edge
from an earlier node to a later one in a random order of the nodes (a
repeated edge is rare and kept; the walk does not mind it), then solves
2000 times over them in turn, with the ★ arm in all five languages. C
keeps the children in one flat array by offsets, and each node's
ancestors in a row of a flat table; Rust, Go, Python and Kāra keep a
list per node. Every implementation prints `2000 solves: checksum
415590010`.

BENCHTAB
