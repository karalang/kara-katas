# 2493. Divide Nodes Into the Maximum Number of Groups

You are given a positive integer `n` representing the number of nodes
in an **undirected** graph. The nodes are labeled from `1` to `n`.

You are also given a 2D integer array `edges`, where
`edges[i] = [ai, bi]` indicates that there is a **bidirectional** edge
between nodes `ai` and `bi`. **Notice** that the given graph may be
disconnected.

Divide the nodes of the graph into `m` groups (**1-indexed**) such
that:

- Each node in the graph belongs to exactly one group.
- For every pair of nodes in the graph that are connected by an edge
  `[ai, bi]`, if `ai` belongs to the group with index `x`, and `bi`
  belongs to the group with index `y`, then `|y - x| = 1`.

Return *the maximum number of groups (i.e., maximum* `m`*) into which
you can divide the nodes*. Return `-1` *if it is impossible to group
the nodes with the given conditions*.

```
n = 6, edges = [[1,2],[1,4],[1,5],[2,6],[2,3],[4,6]]  ->  4
n = 3, edges = [[1,2],[2,3],[3,1]]                    ->  -1
```

**Constraints:** `1 <= n <= 500`; `1 <= edges.length <= 10^4`;
`edges[i].length == 2`; `1 <= ai, bi <= n`; `ai != bi`; there is at
most one edge between any pair of vertices.

Every group is nonempty, or `m` could grow without end. An edge joins
groups one apart, so the groups along an edge alternate in parity, and
an odd cycle makes any division impossible. Otherwise, for any node of
a connected part, numbering every node of the part by one more than its
distance from that node is a division, and no division does better:
the groups along a shortest path step by at most one, so a part
reaching from group 1 to group `k` needs a node from which some other
is `k - 1` away. So each part gives one more than the greatest distance
from its best node, and parts, which share no edge, stack their groups
one after another. The approaches differ in how they find the parts
and rule out odd cycles.

## Approaches

| file | mechanism |
|---|---|
| `groups.kara` ★ | a breadth-first search from every node, a `Vec` as the queue; an edge between two nodes at one distance answers -1, and each part's most levels are kept at its least node and added up. O(n (n + m)) |
| `groups_rec.kara` | a recursive two-colouring: a depth-first search gives every node a side and its part's label, an edge between two nodes of one side answering -1; then a breadth-first search from every node counts its levels. O(n (n + m)) |
| `groups_union.kara` | union-find with parity: each node knows whether it sits on its root's side, so an edge inside one set between nodes of one side answers -1; then a breadth-first search from every node, each set's root taking its most levels. O(m α(n) + n (n + m)) |
| `groups_map.kara` | over `Map`s: neighbour lists in a `Map`, a `VecDeque` search from every node with its distances in a `Map`, and each part's most groups in a `Map` keyed by its least node, the `values()` summed. O(n (n + m)) expected |
| `groups_iter.kara` | iterators: from every node, the waves of a breadth-first walk, each the last one `flat_map`ped to its neighbours and `filter`ed to nodes not yet given a level; the part's edges asked by `all` to join levels one apart, the part named by the `min` of its nodes, and the parts' most waves `sum`med. O(n (n + m)) |
| `groups_solution.kara` | LeetCode's Rust template: `n: i32` and `Vec<Vec<i32>>` in, `i32` out; 0-based `usize` nodes, a `VecDeque` search from every node with `-1` for unseen, an edge whose ends are not one apart answering -1, each part's best in a `HashMap` keyed by its least node; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's two examples and seven
more; then 2000 random graphs of 2 to 40 nodes and up to 60 tries at an
edge, each across a random cut, and 2000 drawn freely, as a count of
those that divide and a checksum; then the constraints' largest, 500
nodes: a path; a 20 by 25 grid; every node of 1 to 100 joined to every
node of 101 to 200, `10^4` edges, the other 300 alone; and `10^4` tries
at an edge across a random cut. `groups.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked on 1500 random
graphs of 2 to 6 nodes and any number of edges against every way of
giving the nodes groups, and the two agreed on every graph.

`check` first reports 8 errors on the template: the `use
std::collections::{HashMap, VecDeque};` line, `struct Solution;`,
`Vec<Vec<i32>>`, `HashMap<usize, i32>` and `HashMap::new`,
`VecDeque::new`, and the `&` before the loop's pattern and before
`g[u]`. `karac fix` carries it in one call, reporting 22 edits: the
`use` line deleted, since `Map` and `VecDeque` are in the prelude;
`struct Solution {}`; the brackets; `HashMap` becomes `Map`; the three
`as usize` casts become `as i64`, and with them the `usize` key; the
two `vec![...]` become `Vec.filled(...)`; the paths take `.`;
`for &v in &g[u]` becomes `for v in ref g[u]`; `let mut far = 0;`
becomes `let mut far: i32 = 0;`, since an unannotated literal keeps
the default `i64` and `far + 1` goes into the `Map[i64, i32]`; and the
wrapper's `as i64` on the template's answer is dropped, since an `i32`
widens to `i64` on its own. The message on `HashMap<..>` suggests
`HashMap[..]`, where the edit writes `Map[..]`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way of giving each node a group from 1 to `n` is
tried, node by node, a node's group one apart from that of each earlier
neighbour; a full assignment counts when its groups are exactly 1 to
`m`, and the answer is the greatest such `m`, -1 if none. No distance is
measured. It checks 300 random graphs of 2 to 6 nodes and up to 12
tries at an edge, half across a random cut and half drawn freely; then
20 of two nodes; and 40 of 7 or 8 nodes, a random tree with up to three
more edges. All 360 are drawn before any arm answers, and 298 of them
divide.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | -1, or at least 2 and at most `n` groups |
| P3 | the edges in the other order, each end for end: the same answer |
| P4 | the nodes numbered backwards: the same answer |
| P5 | a second copy of the graph beside it: -1 again, or twice as many |
| P6 | each arm agrees with at least three of the other five |

P2 holds because there is at least one edge, whose ends need two
groups, and no group is empty. P5 holds because the copy shares no
edge with the graph, so its parts stack after the graph's, and it
holds an odd cycle exactly when the graph does.

The differential prints `360 cases, 298 divide: checksum 654564239,
12960 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python
reading that builds the same cases and tries the same assignments. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the greatest part, not their sum | P1 142, P5 298, P6 142 |
| M5 | ★: the search from node 1 only | P1 184, P2 33, P4 155, P5 301, P6 184 |
| M6 | ★: edges one way only | P1 239, P2 218, P3 286, P4 286, P6 239 |
| M8 | rec: the levels counted from 0 | P1 298, P2 168, P6 298 |
| M10 | rec: an odd cycle passed over | P1 62, P2 26, P3 30, P4 24, P6 62 |
| M11 | rec: the level of the first node queued | P1 298, P2 156, P6 298 |
| M12 | union: parity not carried down the path | P1 15, P6 15 |
| M14 | union: a clash on opposite sides | P1 61, P3 14, P6 61 |
| M16 | union: the set named by the parent, not the root | P1 81, P2 81, P3 72, P6 81 |
| M17 | map: the far end counted one further | P1 298, P2 258, P6 298 |
| M18 | map: the last search's count kept | P1 38, P4 82, P6 38 |
| M19 | map: the queue taken from the back | P1 6, P3 1, P6 6 |
| M23 | iter: every edge asked, not the part's | P1 142, P5 156, P6 142 |
| M24 | iter: edges within a level let through | P1 62, P6 62 |
| M26 | iter: only the first neighbour of each node | P1 96, P2 11, P3 43, P4 20, P6 96 |
| M28 | solution: the part named by the last node popped | P1 298, P2 298, P3 4, P6 298 |
| M31 | solution: only the first half searched from | P1 157, P2 3, P4 84, P5 274, P6 157 |

P1 and P6 kill all seventeen, P2 ten, P3 seven, P4 six, and P5 four.

Fourteen are not kept, and none survives. Five fail exactly as a kept
one: the ★ and template arms' no odd cycle ever found (M1, M27) as the
iter arm's edges within a level let through (M24), all three wrong on
just the 62 graphs that do not divide; the ★ arm's start's own level
not counted (M3) as the rec arm's levels counted from 0 (M8); the union
arm's roots joined on one side (M13) as its parity not carried down the
path (M12), both missing an odd cycle that closes inside one set on 15
graphs; and the template's last search's count kept (M29) as the map
arm's (M18). Eight fail as one another, in three sets: the ★ and rec
arms' each start its own part (M2, M9), which counts every node's best
and so passes `n`; the union arm's deepest one level short and the
template's far end one short (M15, M30); and four wrong on all 298
graphs that divide and on none of the rest: the rec arm's neighbour
given the same side, the map arm's road back a level refused and
neighbour put at the same distance, all three of which answer -1 for
every graph, and the iter arm's one wave too many (M7, M20, M21, M22).
Each could have stood for one kept edit of its arm, but no two of a set
can be kept together, and each arm keeps three that fail apart from
every other. One ends in a crash: the iter arm's start's level left
unset (M25) gives a node with no edge no level at all, so no node
passes the `filter` that names its part, `min()` gives `None`, and the
`unwrap()` panics under both backends.

## Verification

Every arm prints the same output as `groups.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 4.0 to 12.6 s, but for the iter arm's 33 s, which reads every edge once more for each node it searches from, and the differential 6.7 s; under `karac __mir-llvm-asan` the arms take 1.2 to 1.8 s, but for the iter arm's 7.4 s, and the differential 2.4 s; and under `karac run` the differential takes 0.8 s.

## Benchmarks

The bench builds one graph of 500 nodes once from its own generator:
8000 tries at an edge across a random cut, 3947 of them taken. It then
makes 38 passes; each asks on all but the last few edges, as many as
the checksum so far chooses, below 100, and folds the answer plus the
pass into the checksum. Every graph divides, so every answer builds its
neighbour lists afresh and searches from all 500 nodes. The bench uses
the ★ arm in all five languages: C with the lists in compressed rows
and the edges asked as a count, Rust and Go with a growable list per
node and the asked edges copied, as the Kāra and Python ones are. Every
implementation prints `38 passes over 500 nodes and 3947 edges:
checksum 186261830`.

BENCHTAB
