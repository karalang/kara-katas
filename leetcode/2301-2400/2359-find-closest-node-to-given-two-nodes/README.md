# 2359. Find Closest Node to Given Two Nodes

You are given a **directed** graph of `n` nodes numbered from `0` to
`n - 1`, where each node has **at most one** outgoing edge.

The graph is represented with a given **0-indexed** array `edges` of
size `n`, indicating that there is a directed edge from node `i` to
node `edges[i]`. If there is no outgoing edge from `i`, then
`edges[i] == -1`.

You are also given two integers `node1` and `node2`.

Return *the **index** of the node that can be reached from both*
`node1` *and* `node2`*, such that the **maximum** between the distance
from* `node1` *to that node, and from* `node2` *to that node is
**minimized***. If there are multiple answers, return the node with
the **smallest** index, and if no possible answer exists, return `-1`.

Note that `edges` may contain cycles.

```
edges = [2,2,3,-1], node1 = 0, node2 = 1  ->  2
edges = [1,2,-1],   node1 = 0, node2 = 2  ->  2
```

**Constraints:** `n == edges.length`; `2 <= n <= 10^5`;
`-1 <= edges[i] < n`; `edges[i] != i`; `0 <= node1, node2 < n`.

With one edge out of every node, the nodes a start reaches lie on one
path, which ends at `-1` or runs into a cycle. So each start's
distances come from a single walk that stops at the first repeated
node, and the answer is a scan over the nodes both walks marked.

## Approaches

| file | mechanism |
|---|---|
| `closest.kara` ★ | each start's path walked until it ends or repeats, its distances recorded, then every node both reach scanned for the least of the larger distance, the smaller index first. O(n) |
| `closest_lockstep.kara` | both starts walk one edge at a time together, each marking its own nodes; the first step at which either stands on a node the other has marked gives the answer, the smaller of the two if both do. No distances. O(n) |
| `closest_bfs.kara` | breadth-first search as for any graph: a list of neighbours built from the edges, each start's distances found with a queue, then the same scan. O(n) |
| `closest_naive.kara` | no tables: for each node, both starts walk at most `n` steps looking for it, and the node is kept when the larger count beats the best so far. O(n^2) |
| `closest_iter.kara` | iterators: each path by `scan` until it ends or repeats, written into a distance table by `enumerate` and `for_each`; the answer by `filter` and `min_by_key` on (larger distance, node) |
| `closest_solution.kara` | LeetCode's Rust template: the walk as a closure returning `Vec<i32>`, called for both starts, then the scan with `i32::MAX` as the first best; carried by `karac fix`, with one line by hand (below) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one node;
two nodes pointing at each other; a chain of 2000 from both ends; a
cycle of 2000 started half way round and from two other places; two
paths of 1000 into a shared tail; then 3000 random graphs of 1 to 30
nodes, each edge `-1` with a chance of 1 in 1 to 1 in 8, with two
random starts, a checksum and how many have an answer. `closest.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked against breadth-first search on 3000 random graphs.

The naive arm stands at `n^2` steps and takes 4.6 s under `karac
__mir-run` on the 3000-node merge; the rest of the harness is small.

The bfs arm was first written with `Deque`, and `karac fix` renamed it
`VecDeque` in 2 edits. The iter arm's `for_each` closure was first a
bare assignment, `|(d, node)| dist[node] = d`, which Kāra refuses as a
closure body; `karac fix` wrapped it in a block in 2 edits.

`check` first reports 8 errors on the template, and `karac fix` carries
it in one call, reporting 12 edits: `struct Solution;` given its braces,
`Vec<i32>` its brackets, `vec![-1; n]` written `Vec.filled(n, -1)`,
`&&` written `and`, `i32::MAX` and `Solution::` written with dots, and
the closure's return type `-> Vec<i32>`, which a Kāra closure does not
name, moved to the binding as `let walk: Fn(i32) -> Vec[i32] =
|start: i32| { ... }`. At first `karac fix` moved that type only when
the closure's tail was a `collect`, `sum` or `product`; here the tail is
the local `dist`, built from an unsuffixed literal, so the type was
deleted, `Vec.filled(n, -1)` defaulted to `Vec[i64]`, and `best_dist =
far` was refused as narrowing `i64` to `i32` with no fix
(B-2026-11-21-41, fixed). The template was carried again after the fix.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each start's path written out as the node after 0, 1, 2, ...
steps; then for `k = 0, 1, 2, ...` the nodes on both paths within `k`
steps, and the least of them at the first `k` that has any. No
distance tables. It checks 300 random graphs of 1 to 30 nodes, each
edge `-1` with a chance of 1 in 1 to 1 in 8; then 30 of up to 2000
nodes; then 30 of up to 300 nodes made of one cycle with trees hanging
off it, every node outside the cycle pointing at a lower one. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 40 nodes, the answer is the literal reading's |
| P2 | `-1` or a node that both starts reach |
| P3 | the two starts swapped: the same answer |
| P4 | the edge out of the answer cut: the same answer |
| P5 | both starts at `node1`: `node1` |
| P6 | each arm agrees with at least three of the other five |

P4 holds because the answer is reached from both starts before
anything past it, so cutting its edge takes away only nodes that are
farther from the start that walks through it, and changes no distance
to the nodes that stay. It was first written as every node neither
start reaches given no edge, which held as well but failed no edit at
all: in a graph where every node has one edge out, no arm, nor any
plausible slip in one, ever reads the edge of a node that neither start
reaches, so that check had nothing to catch. Even the edges reversed,
and both walks run from each node to the starts, which do read those
edges, gave the same answer on every case with the edges taken away.

The differential prints `360 cases: checksum 903194609, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and walks each path into a list. On a failure it prints
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
| M2 | ★: the smaller distance, not the larger | P1 25, P6 37 |
| M4 | ★: a node either start reaches | P1 266, P2 310, P4 62, P6 310 |
| M6 | ★: node 0 never considered | P1 25, P5 35, P6 25 |
| M8 | lockstep: node2's place returned for node1's hit | P1 46, P3 114, P6 58 |
| M9 | lockstep: node2's hits never seen | P1 47, P3 116, P6 58 |
| M10 | lockstep: node2's start never a hit for node1 | P1 30, P3 76, P6 37 |
| M12 | bfs: node1 searched twice | P1 241, P2 266, P3 325, P6 286 |
| M14 | bfs: the edges reversed | P1 108, P2 80, P4 95, P6 131 |
| M16 | bfs: the search one step deep | P1 69, P6 92 |
| M17 | naive: the walk capped at half the nodes | P1 15, P5 6, P6 15 |
| M18 | naive: each distance halved | P1 21, P5 139, P6 21 |
| M20 | naive: a path that ends taken as reaching | P1 164, P2 190, P4 167, P5 156, P6 190 |
| M23 | iter: the farthest node, not the closest | P1 103, P5 258, P6 126 |
| M24 | iter: a node only node1 reaches | P1 225, P2 266, P3 310, P4 20, P6 266 |
| M25 | iter: a path stopped at node 0 | P1 50, P5 35, P6 55 |
| M30 | solution: node1's start never counted | P1 69, P3 76, P5 360, P6 74 |
| M31 | solution: the node after the answer returned | P1 145, P2 124, P4 34, P5 360, P6 168 |

P1 and P6 kill all seventeen, P5 eight, P2 and P3 six each and P4 five.
P3, the starts swapped, fails the edits that treat one start unlike the
other: node1 walked or searched twice, a node only node1 reaches,
node1's start never counted, and the three lockstep slips, where each walker checks the other's marks.
P4, the edge out of the answer cut, fails the edits that answer with a
node whose own edge still matters: a node either start reaches, the
edges reversed, a path that ends taken as reaching, a node only node1
reaches and the node after the answer returned. P5, both starts at
node1, fails what loses a start's own place or the distances near it:
node 0 never considered, the walk capped or halved, a path that ends
taken as reaching, the farthest node, a path stopped at node 0, node1's
start never counted and the node after the answer returned.

Of the thirty-one, fourteen were not kept. A tie taken by the larger
node, in the ★, lockstep, bfs, iter and template arms (M1, M7, M13,
M26, M27), and the naive arm's best kept one step longer (M21) all fail
two cases of P1 and P6 alike: a tie between two nodes at the same
larger distance is rare in these graphs. The two distances added fail
alike in the ★ and iter arms (M3, M22); so do node1 walked twice in the
★ arm (M5) and searched twice in the bfs arm (M12), and a node only
node1 reaches in the bfs and iter arms (M15, M24). The lockstep arm's
node2 marked after node1 is checked (M11) fails nothing, since when both
walkers stand on one node at the same step the other check still finds
it and returns that node. The naive arm's smaller distance compared
(M19), and the template's node2 walked twice (M28) and walks capped at 5
steps (M29), fail apart from every kept one, and were left out to keep
three to an arm and two to the template.

## Verification

Every arm prints the same output as `closest.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

The differential takes 6.3 s under `karac __mir-run` and 0.59 s under
`karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 graphs of `10^5` nodes once from the harness's
generator: graph `a` shuffles the nodes into one line, cuts each link
with a chance of 1 in `2^(a + 4)`, and links the last node back to the
first when `a` is odd, and draws 20 random pairs of starts. It then
makes 10 passes, pass `p` folding each answer plus `p` into the
checksum, with the ★ arm in all five languages. Every implementation
prints `10 passes over 10 graphs of 10^5 nodes: checksum 671354281`.
Each call allocates its two distance tables, in every language alike,
since the tables are the algorithm.

BENCHTAB
