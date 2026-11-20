# 2368. Reachable Nodes With Restrictions

There is an undirected tree with `n` nodes labeled from `0` to `n - 1`
and `n - 1` edges. You are given a 2D integer array `edges` of length
`n - 1` where `edges[i] = [ai, bi]` indicates that there is an edge
between nodes `ai` and `bi` in the tree. You are also given an integer
array `restricted` which represents **restricted** nodes.

Return *the **maximum** number of nodes you can reach from node* `0`
*without visiting a restricted node.*

Note that node `0` will **not** be a restricted node.

```
n = 7, edges = [[0,1],[1,2],[3,1],[4,0],[0,5],[5,6]], restricted = [4,5]  ->  4
n = 7, edges = [[0,1],[0,2],[0,5],[0,4],[3,2],[6,5]], restricted = [4,2,1]  ->  3
```

**Constraints:** `2 <= n <= 10^5`; `edges.length == n - 1`;
`0 <= ai, bi < n`; `ai != bi`; `edges` is a valid tree;
`1 <= restricted.length < n`; `1 <= restricted[i] < n`; the values of
`restricted` are unique.

The nodes reachable from 0 are those of its piece once the restricted
nodes and their edges are taken out of the tree, so any search from 0
that never enters a restricted node counts them.

## Approaches

| file | mechanism |
|---|---|
| `reach.kara` ★ | adjacency lists, the restricted nodes marked as seen, and a breadth-first search from 0 through a vector used as a queue; the answer is how many nodes the queue took. O(n) |
| `reach_dfs.kara` | depth first by a stack of (node, parent): a tree has no cycle, so a node needs no seen mark, only never stepping back to its parent or into a restricted node. O(n) |
| `reach_union.kara` | union-find: every edge between two open nodes joins their sets, and the answer is the size of node 0's set. Union by size, paths halved. O(n alpha(n)) |
| `reach_recursive.kara` | recursion: the nodes below `u` are `u` and those below each open child; one call per reached node, `10^5` deep on the harness's path |
| `reach_iter.kara` | iterators, level by level: the next level is the open children of this one by `flat_map` and `filter`, and a `Set` says which nodes are closed |
| `reach_solution.kara` | LeetCode's Rust template: adjacency lists of `usize` from `vec![vec![]; n]` and a breadth-first search through a `VecDeque`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one node; a
path of `10^5` nodes, open and cut at its middle; a star of `10^5` nodes
with every odd leaf restricted; then 2000 random trees of 2 to 40 nodes,
each node joined to an earlier one, with up to `n - 1` restricted nodes,
with a checksum and how many leave node 0 alone. One node and no
restricted node are outside the constraints, kept since the rule reads
the same for them. `reach.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random trees, their
edges shuffled and turned at random, against growing the reached nodes
by passes over the edges.

The iter arm was first written with the set of closed nodes read inside
the closure that `flat_map`'s closure returns. `check` refuses it
(E0235): a returned closure takes its captures by move, so each call
would move the set out of the outer closure. `karac fix` borrows it
before the statement, `let closed = ref closed;`, in 1 edit.

`check` first reports 12 errors on the template, and `karac fix`
carries it in one call, reporting 26 edits: the
`use std::collections::VecDeque` line deleted, since Kāra's `VecDeque`
is in the prelude; `struct Solution;` given its braces; each `Vec<..>`
its brackets; `usize` written `i64`, Kāra's index type, in the casts,
the list type and `0usize`; `vec![vec![]; n]` and `vec![false; n]`
written `Vec.filled`; `for e in &edges` written `for e in ref edges`,
and `for &r in &restricted` and `for &v in &adj[u]` the same with the
`&` of the pattern dropped; `r as usize` dropped from the index;
`VecDeque::new` written with a dot; and `!` written `not`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the nodes reached from 0 grown by passes over every edge, an
edge carrying the reach from a reached node to an open one, until a pass
adds nothing. No adjacency lists and no search order. It checks 300
random trees of 2 to 40 nodes, each node joined to an earlier one, with
up to `n - 1` restricted nodes; then 30 of up to 2000 nodes with up to
20 restricted; then 30 paths of up to 300 nodes in a random order with
up to 3 restricted. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | from 1 to `n` less the restricted nodes |
| P3 | every node `v` but 0 renamed `n - v`: the same answer |
| P4 | the edges listed backwards, each turned around: the same answer |
| P5 | a new node joined to node 0: one more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 904492816, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and searches from 0 by a stack. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the restricted nodes never marked | P1 340, P2 340, P6 340 |
| M4 | ★: only the first two neighbours followed | P1 257, P4 231, P5 329, P6 257 |
| M6 | ★: the search stopped after 20 nodes | P1 67, P4 39, P5 52, P6 67 |
| M8 | dfs: node 1 taken as node 0's parent | P1 213, P3 218, P6 213 |
| M10 | dfs: only even restricted nodes marked | P1 295, P2 168, P3 141, P6 295 |
| M11 | dfs: the first neighbour of each node never followed | P1 240, P4 279, P6 240 |
| M12 | union: each join adding one node | P4 213 |
| M13 | union: an edge skipped only when both ends are restricted | P1 340, P2 313, P6 340 |
| M14 | union: node 0's own size read, not its root's | P1 28, P4 299, P5 28, P6 28 |
| M17 | recursive: a node not counting itself | P1 360, P2 360, P5 360, P6 360 |
| M19 | recursive: each child replacing the count | P1 327, P5 360, P6 327 |
| M20 | recursive: the first restricted node left open | P1 334, P2 107, P6 334 |
| M22 | iter: at most three counted a level | P1 130, P5 135, P6 130 |
| M23 | iter: the node after each closed one taken as closed | P1 288, P2 25, P3 301, P6 288 |
| M26 | iter: each edge followed one way only | P1 327, P4 327, P5 360, P6 327 |
| M29 | solution: the count started at one | P1 360, P2 76, P6 360 |
| M31 | solution: node 1 never entered | P1 231, P3 238, P6 231 |

P1 and P6 kill sixteen, P2 and P5 seven, P4 six and P3 four. The union
arm's join adding one node (M12) fails P4 alone: every case lists its
edges in the order the tree grew, each joining a node not yet joined,
so adding one is right until P4 lists them backwards and an edge joins
two sets of more than one node. P3, the nodes renamed, fails only the
edits that read a node's name and not only the tree: node 1 taken as
node 0's parent or never entered, only even restricted nodes marked,
and the node after each closed one taken as closed.

Of the thirty-one, fourteen were not kept. Node 0 never marked fails
alike in the ★ arm and the template (M2, M27): node 0 is counted again
when a neighbour finds it. Each edge followed from its first end only
fails alike in the ★, recursive and template arms (M3, M21, M28). Each
followed from its second end only, in the depth-first and iter arms
(M9, M26), fails as the union arm's edges from node 0 never joined
(M16): every case writes an edge with the node drawn first as its
first end, so both reach only the nodes drawn before node 0 on its way
back to the first, none in a tree grown from node 0. The first
restricted node left open (M5, M24) fails as in the recursive arm
(M20), and the restricted nodes entered or never marked
(M7, M18, M30) as in the ★ arm (M1). The iter arm's walk stopped at a
level of one (M25) fails as a node not counting itself (M17), every
answer 0, and the union arm's first edge never joined (M15) fails
apart from every kept one, and was left out to keep three to an arm.

## Verification

Every arm prints the same output as `reach.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 to 2.6 s but the iter arm,
4.9 s, which builds a fresh vector for each level. The differential
takes 6.8 s there and 1.3 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 trees of `10^5` nodes once from the harness's
generator, tree `a` joining node `i` to one of the `4^a` nodes before it
and restricting each node but 0 with a chance of 1 in `2^(a + 4)`, then
makes 20 passes, pass `p` folding each answer plus `p` into the
checksum, with the ★ arm in all five languages. Every implementation
prints `20 passes over 10 trees of 10^5 nodes: checksum 683662470`.
Rust, Go and Python build a growable list per node as Kāra does. C has
no growable list in its standard library, so it lays the lists out in
one array by counting each node's degree first (compressed sparse rows):
the same search over a different layout, which the comparison should be
read with. Every implementation builds its lists afresh in each call.

BENCHTAB
