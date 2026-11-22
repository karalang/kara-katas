# 2737. Find the Closest Marked Node

You are given a positive integer `n` which is the number of nodes of a
**0-indexed directed weighted** graph and a **0-indexed 2D array**
`edges` where `edges[i] = [u_i, v_i, w_i]` indicates that there is an
edge from node `u_i` to node `v_i` with weight `w_i`.

You are also given a node `s` and a node array `marked`; your task is to
find the **minimum** distance from `s` to **any** of the nodes in
`marked`.

Return *an integer denoting the minimum distance from* `s` *to any node
in* `marked` *or* `-1` *if there are no paths from s to any of the
marked nodes.*

```
n = 4, edges = [[0,1,1],[1,2,3],[2,3,2],[0,3,4]], s = 0, marked = [2,3]          ->  4
n = 5, edges = [[0,1,2],[0,2,4],[1,3,1],[2,3,3],[3,4,2]], s = 1, marked = [0,4]  ->  3
n = 4, edges = [[0,1,1],[1,2,3],[2,3,2]], s = 3, marked = [0,1]                  ->  -1
```

**Constraints:** `2 <= n <= 500`, `1 <= edges.length <= 10^4`,
`edges[i].length = 3`, `0 <= edges[i][0], edges[i][1] <= n - 1`,
`1 <= edges[i][2] <= 10^6`, `1 <= marked.length <= n - 1`,
`0 <= s, marked[i] <= n - 1`, `s != marked[i]`, `marked[i] != marked[j]`
for every `i != j`; the graph might have **repeated edges**; the graph is
generated such that it has no **self-loops**.

## Approaches

| file | mechanism |
|---|---|
| `closest.kara` ★ | Dijkstra from s over the directed edges, a `PriorityQueue` of (distance, node) whose stale entries are skipped; the first marked node taken off the queue is the closest. O((n + m) log m) |
| `closest_bellman.kara` | Bellman-Ford: every edge relaxed in rounds, at most n - 1 of them, stopping early when a round changes nothing; then the least distance among the marked nodes by `map` and `min`. O(n m) |
| `closest_dense.kara` | Dijkstra over an n by n matrix of the lightest edge between each two nodes, the nearest unsettled node found by a scan each step, no queue. O(n^2 + m) |
| `closest_reverse.kara` | the edges turned round and Dijkstra run from every marked node at once, each at distance 0, until s is settled; the queue a `SortedSet` of (distance, node) from which an entry is removed when its node gets closer. O((n + m) log n) |
| `closest_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `Vec<Vec<(usize, i64)>>`, a `BinaryHeap` of `Reverse((dist, node))` and a `HashSet` of the marked nodes, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's three examples; a chain of
500 nodes with the one marked node at its end; 2000 random graphs of 2
to 10 nodes and up to 20 edges weighing up to 20; and 20 of 500 nodes
and `10^4` edges, LeetCode's most, weighing up to `10^6`, each batch
with the sum of its answers and a checksum. `closest.py` mirrors the ★
arm and its output is byte-identical.

```
4
3
-1
499000000
2000 small graphs: distances sum to 11038, checksum 19358436
20 graphs of 500 nodes: distances sum to 1640798, checksum 392178856
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every simple path out of s walked depth first, and the
lightest that ends on a marked node kept, since a walk that repeats a
node is never lighter; no queue and no relaxing. It draws 1000 random
graphs of 2 to 7 nodes and up to 12 edges weighing up to 20, then 300 of
up to 60 nodes and 400 edges weighing up to `10^6`, all before any arm
answers; the literal reading is asked only of the first 1000.

| | property |
|---|---|
| P1 | up to 7 nodes, the answer is the literal reading's |
| P2 | the edges listed in reverse order, and the marked nodes too: the same answer |
| P3 | every weight doubled: the answer doubled, or -1 still |
| P4 | an edge from s straight to a marked node added, weighing w: the lesser of the answer and w, or w when the answer was -1 |
| P5 | the answer is -1 exactly when no marked node can be reached, by a breadth-first search that ignores weights |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1300 cases: checksum 186958077, 39000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same walk over every simple path gives
the same checksum. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M2 and M7 fail the same checks: each searches
the graph with its edges the wrong way round.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the weight left out of each queue entry | P1 616, P4 420, P6 880 |
| M2 | ★: the edges taken backwards | P1 745, P4 514, P5 320, P6 1019 |
| M3 | bellman: one round too few | P1 132, P2 14, P4 168, P5 137, P6 140 |
| M4 | bellman: a change never noted | P1 39, P2 128, P5 34, P6 88 |
| M5 | dense: the last of two parallel edges kept, not the lighter | P1 163, P2 342, P4 319, P6 242 |
| M6 | dense: the farthest node settled first | P1 2, P4 3, P6 29 |
| M7 | reverse: the edges never turned round | P1 745, P4 514, P5 320, P6 1019 |
| M8 | reverse: s answered when first reached, not when settled | P1 210, P2 301, P4 283, P6 396 |
| M9 | solution: the heap ordered by the last edge alone | P1 74, P4 9, P6 162 |
| M10 | solution: every edge weighing 1 | P1 549, P3 880, P4 501, P6 813 |

## Benchmarks

The bench draws 50 graphs of 500 nodes and `10^4` edges, LeetCode's
most, weighing up to `10^6`, with 1 to 3 marked nodes so that the search
goes far before it stops, all of them first, then answers each 20 times
by the ★ arm in all five languages. C keeps its own binary heap, Go uses
`container/heap`, Rust a `BinaryHeap` of `Reverse` pairs and Python
`heapq`. Every implementation prints `50 graphs of 500 nodes and 10000
edges, 20 rounds: distances sum to 291938040, checksum 528256059`.

BENCHTAB

## Verification

All five arms print the same output as `closest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The reverse arm seeds its queue with `queue.insert((0, v))` for each
marked node, `v` a `ref i64` from `marked.iter()`, and `karac check`
refused it, "expected '(i64, i64)', found '(i64, ref i64)'", where
`Vec.push` and `PriorityQueue.push` copy the same tuple in. That was
kara `B-2026-11-20-139`, fixed at `0d28296389`; the arm keeps the insert as
written. The other own arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 44 edits, the wrapper
included: the `use` lines became `struct Solution {}`, `Vec<..>` became
`Vec[..]`, `usize` became `i64` and the `as usize` indexes dropped,
`vec![vec![]; n]` and `vec![i64::MAX; n]` became `Vec.filled(..)`,
`HashSet<usize>` became `Set[i64]`, `BinaryHeap::new()` became
`PriorityQueue.new()` with every `Reverse(..)` dropped, since a
`PriorityQueue` gives its least first, `0i64` became `0`, the `&m`,
`&x` and `&(v, w)` patterns and `contains(&u)` dropped their `&`, and
`Solution::` became `Solution.` with the `as i64` dropped.
