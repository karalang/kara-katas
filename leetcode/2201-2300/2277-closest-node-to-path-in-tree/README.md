# 2277. Closest Node to Path in Tree

You are given a positive integer `n` representing the number of nodes
in a tree, numbered from `0` to `n - 1` (**inclusive**). You are also
given a 2D integer array `edges` of length `n - 1`, where `edges[i] =
[node1i, node2i]` denotes that there is a **bidirectional** edge
connecting `node1i` and `node2i` in the tree.

You are given a **0-indexed** integer array `query` of length `m` where
`query[i] = [starti, endi, nodei]` means that for the `i`th query, you
are tasked with finding the node on the path from `starti` to `endi`
that is **closest** to `nodei`.

Return *an integer array* `answer` *of length* `m`*, where* `answer[i]`
*is the answer to the* `i`*th query*.

```
n = 7, edges = [[0,1],[0,2],[0,3],[1,4],[2,5],[2,6]], query = [[5,3,4],[5,3,6]]  ->  [0,2]
n = 3, edges = [[0,1],[1,2]], query = [[0,1,2]]                                   ->  [1]
n = 3, edges = [[0,1],[1,2]], query = [[0,0,0]]                                   ->  [0]
```

**Constraints:** `1 <= n <= 1000`; `edges.length == n - 1`;
`edges[i].length == 2`; `0 <= node1i, node2i <= n - 1`; `node1i !=
node2i`; `1 <= query.length <= 1000`; `query[i].length == 3`; `0 <=
starti, endi, nodei <= n - 1`; the graph is a tree.

A node `u` is on the path from `s` to `e` exactly when it adds nothing
to their distance, `d(s, u) + d(u, e) = d(s, e)`, and in a tree the one
nearest `x` is unique. It is the median of the three: the one node on
all three paths between them, and so the deepest of their three pairwise
lowest common ancestors under any root. The answer is symmetric in
`start`, `end` and `node`. O(n^2 + q n) from all the distances, or
O((n + q) log n) by ancestors.

## Approaches

| file | mechanism |
|---|---|
| `closest.kara` ★ | a breadth-first search from every node for all the distances; per query, the node on the path with the least distance to the query's node |
| `closest_path.kara` | per query, a search from the start for parents and the path read back from the end, a search from the query's node for distances, and the nearest node on the path |
| `closest_lca.kara` | the tree rooted at 0, binary lifting over `up[k][v]`, a closure `lca`, and the deepest of lca(s, e), lca(s, x) and lca(e, x) |
| `closest_struct.kara` | `struct Rooted` of parents and depths from a stack search at 0; `meet` climbs the deeper node a step at a time, and `closest` takes the deepest of the three meetings |
| `closest_iter.kara` | in chains: neighbours by `filter` over the edges, each search's unseen neighbours by `filter`, and per query the path by `filter` and the nearest by `min_by_key` |
| `closest_solution.kara` | LeetCode's Rust template: `i32` and `Vec<Vec<i32>>` in, `Vec<i32>` out, nodes as `usize` with `usize::MAX` unseen; per query a stack search for parents, a `VecDeque` search for distances, and the walk back from the end; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (one node; a path of five asked both ways, `[2, 2, 1]`; a star,
`[0, 3]`), each with its answers; then 500 random trees of 1 to 30
nodes, each node joined to one of the 1, 3 or all before it, relabelled
and shuffled, with 1 to 10 queries, with a checksum; then the
constraints' largest, 1000 nodes and 1000 queries, on a random tree and
on a path, each with the sum of its answers (491646, 497496).
`closest.py` mirrors the ★ arm and its output is byte-identical.

The iter arm's search first walked `adj[v].iter().filter(|w| dist[w] <
0)` while setting `dist[w]` in the loop. `karac check` refuses it, as
Rust would: the filter's closure still borrows `dist` when the body
writes it (E0516). The arm now collects each step's unseen neighbours
first.

`karac fix` carries the template in one round, reporting 59 edits.
Among them: the generics' brackets, `n as usize` to `n as i64` and
`usize::MAX` to `i64.MAX`, `vec![vec![]; n]` to `Vec.filled(n,
Vec.new())`, `vec![usize::MAX; n]` to `Vec.filled(n, i64.MAX)`,
`vec![s]` to `[s]`, `Vec::with_capacity` to `Vec.with_capacity`,
`std::collections::VecDeque::new()` to `VecDeque.new()`, `for e in
&edges` to `for e in ref edges`, `for &v in &g[u]` to `for v in ref
g[u]`, `struct Solution;` to `struct Solution {}`, and in the adapter
`&Vec<Vec<i64>>` to a bare `Vec[Vec[i64]]`, the patterns `|&x|` to
`|x|`, `Solution::` to `Solution.` and the `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the path from `start` to `end` found by a depth-first walk
that returns the nodes it went through, each node on it measured to the
query's node by the same walk, the shortest kept. No distances table,
no rooting and no ancestors. It checks 300 random trees of 1 to 12
nodes, each node joined to one of the 1, 3 or all before it, with 1 to
6 queries; then 30 paths; then 30 stars. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answers are the literal reading's |
| P2 | each query's three nodes turned round, `[end, node, start]`: the same answers |
| P3 | the nodes relabelled `v` to `n - 1 - v`: the answers relabelled |
| P4 | each answer on its path, the query's node itself when that is on the path, and the start when the path is one node |
| P5 | each query's node replaced by its answer: the same answers |
| P6 | each arm agrees with at least three of the other five |

P2 first swapped only the start and the end. Turning all three round
asks more of an arm, since the median does not care which node is
which, and it kills fifteen of the seventeen kept edits where the swap
killed eight of the fourteen it ran against.

The differential prints `360 cases: checksum 838900055, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that takes
breadth-first distances from every node and the path's nearest node by
`min`. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: each edge one way | P1 299, P2 272, P3 67, P4 267, P5 213, P6 299 |
| M4 | ★: node 0 never tried | P1 83, P2 116, P3 142, P4 59, P6 83 |
| M6 | ★: a nearer node needed by two | P1 235, P2 294, P3 87, P4 162, P5 1, P6 235 |
| M7 | path: the start never compared | P1 205, P2 289, P4 127, P6 205 |
| M8 | path: distances from the start | P1 280, P2 316, P4 210, P6 280 |
| M9 | path: the farthest kept | P1 316, P2 290, P4 264, P5 316, P6 316 |
| M12 | lca: the shallowest kept | P1 302, P3 290, P4 281, P6 302 |
| M13 | lca: only the meeting of start and end | P1 267, P2 261, P3 263, P4 223, P6 267 |
| M15 | lca: a lift that lands level skipped | P1 221, P3 244, P4 195, P5 33, P6 221 |
| M17 | struct: the meeting of start and end left out | P1 172, P2 261, P3 207, P4 172, P6 172 |
| M19 | struct: every depth 1 | P1 191, P2 200, P3 219, P4 132, P6 191 |
| M20 | struct: the deeper node climbed two at a time | P1 162, P2 158, P3 147, P4 150, P6 162 |
| M22 | iter: every node on the path | P1 271, P2 310, P4 271, P6 271 |
| M23 | iter: the farthest kept | P1 316, P2 289, P3 85, P4 264, P5 316, P6 316 |
| M24 | iter: each edge one way | P1 305, P2 270, P3 238, P4 286, P5 221, P6 305 |
| M28 | solution: one step toward the start | P1 280, P2 316, P4 210, P5 176, P6 280 |
| M29 | solution: every distance 0 | P1 275, P2 312, P4 222, P6 275 |

P1, P4 and P6 kill all seventeen, P2 fifteen, P3 eleven, and P5 seven.
P4 needs no literal reading: every edit either leaves the path or
misses a query's node standing on it. P2 misses only the lca arm's
shallowest kept and its lift that lands level skipped: that arm treats
the three nodes alike, so turning the query round cannot move them. P3 catches the edits that lean on the labels: the
root at 0, node 0 skipped, edges kept one way, ties broken by order.
P5 catches an answer that moves when the query's node is set to it,
which a nearest node never does.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Eight fail as a kept one does: the ★ arm's every
node on the path, the iter arm's nodes beside the path too and the
template's query's node returned (M1, M25, M31) as the iter arm's every
node on the path (M22), all returning the query's node; the ★ arm's
searches seeded at 1 and the iter arm's nearest to the start (M5, M26)
as the path arm's distances from the start (M8), all returning the
start; the template's farthest kept (M27) as the path arm's (M9); the
template's start never compared (M30) as the path arm's (M7); and the
struct arm's shallowest kept (M18) as the lca arm's (M12). Six fail in
ways of their own and are left out because their arms keep enough: the
★ arm's farthest kept (M2), the path arm's end never compared and its
distances' parity only (M10, M11), the lca arm's one level fewer and
its last step up skipped (M14, M16), and the struct arm's every parent
the root (M21).

Five edits of the first draft were replaced. Four were equivalent
because the answer is the median of the three nodes: the ★, struct and
template arms' end and query's node confused, and the path arm's start
and query's node confused. One stopped by `unwrap()` on `None` under
both backends: the iter arm's searches seeded at 2, which leaves some
paths with no node passing the filter. They are now M6, M11, M20, M25
and M28.

## Verification

Every arm prints the same output as `closest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the lca and struct arms take 0.6 s, the
differential 2.3 s, the ★ arm 4.7 s, the path arm 5.8 s, the template
6.0 s, and the iter arm 19.6 s, most of it the neighbours found by
filtering every edge for every node of the two 1000-node trees.

## Benchmarks

The bench answers 50 random trees of the constraints' largest, 1000
nodes, each node joined to a random node before it, with 1000 random
queries each, with the ★ arm in all five languages. Every
implementation prints `50 trees of 1000: checksum 68844683`. Each
builds its edges and queries from the same generator; C keeps the
neighbours in one array with offsets per node, and the distances in one
`n * n` block.

BENCHTAB
