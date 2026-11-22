# 2714. Find Shortest Path with K Hops

You are given a positive integer `n` which is the number of nodes of a
**0-indexed undirected weighted connected** graph and a **0-indexed 2D
array** `edges` where `edges[i] = [u_i, v_i, w_i]` indicates that there
is an edge between nodes `u_i` and `v_i` with weight `w_i`.

You are also given two nodes `s` and `d`, and a positive integer `k`,
your task is to find the **shortest** path from `s` to `d`, but you can
hop over **at most** `k` edges. In other words, make the weight of
**at most** `k` edges `0` and then find the **shortest** path from `s`
to `d`.

Return *the length of the **shortest** path from* `s` *to* `d` *with the
given condition*.

```
n = 4, edges = [[0,1,4],[0,2,2],[2,3,6]], s = 1, d = 3, k = 2                          ->  2
n = 7, edges = [[3,1,9],[3,2,4],[4,0,9],[0,5,6],[3,6,2],[6,0,4],[1,2,4]], s = 4, d = 1, k = 2  ->  6
n = 5, edges = [[0,4,2],[0,1,3],[0,2,1],[2,1,4],[1,3,4],[3,4,7]], s = 2, d = 3, k = 1        ->  3
```

**Constraints:** `2 <= n <= 500`, `n - 1 <= edges.length <= min(10^4,
n * (n - 1) / 2)`, `edges[i].length = 3`, `0 <= edges[i][0],
edges[i][1] <= n - 1`, `1 <= edges[i][2] <= 10^6`, `0 <= s, d, k <= n -
1`, `s != d`; the graph is connected and has no self-loops or repeated
edges. A premium problem.

## Approaches

| file | mechanism |
|---|---|
| `hops.kara` ★ | a state is a node and the hops spent reaching it; an edge either costs its weight and keeps the hops, or is hopped over for nothing and spends one. Dijkstra's search over the states, a `PriorityQueue` of (distance, node, hops), smallest first, stops at the first state popped at d. O((k + 1) E log((k + 1) V)) |
| `hops_layers.kara` | k + 1 rounds of Dijkstra's search on the plain graph: layer 0 from s alone; each later layer starts every node at the best of its own distance in the layer before and its neighbours' there, one hop spent on the edge between, and then relaxes by weights. The answer is d's distance in the last layer. O((k + 1) E log V) |
| `hops_dense.kara` | the edges in an n by n matrix of weights, 0 for none, and the same k + 1 layers, each settled by Dijkstra's search without a heap: every step scans the nodes for the nearest one not yet settled and relaxes along its row. O((k + 1) V^2) |
| `hops_queue.kara` | the states relaxed by a first-in, first-out `VecDeque` of those whose distance fell, each re-queued only when it is not already waiting, until no distance falls (Bellman, Ford and Moore's queue); the answer is the least distance at d over every count of hops |
| `hops_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `BinaryHeap` of `Reverse((dist, node, used))`, `usize` nodes, a `vec![vec![i64::MAX; k + 1]; n]` table and `while let Some(Reverse(..))`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; a path of
500 nodes, LeetCode's most, each edge `10^6`, end to end with no hops
and with 10; a path of 50 end to end with 49, every edge hopped; 500
nodes and about `10^4` edges, near LeetCode's most, with 1 hop; then the
lengths summed and a checksum for 1000 random connected graphs of 2 to
10 nodes with weights up to 20, and 20 of up to 100 nodes and 1000 edges
with weights up to `10^6`. Each random graph is a random tree, each node
after the first joined to one before it, and then more edges between
pairs not yet joined. `hops.py` mirrors the ★ arm and its output is
byte-identical.

```
2
6
3
499000000
489000000
0
9584 edges: 12002
1000 small graphs: lengths sum to 3341, checksum 718791634
20 graphs up to 100 nodes: lengths sum to 1904804, checksum 649140421
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every simple path from s to d walked, each priced at its
weights with its k heaviest hopped over for nothing, and the cheapest
path wins, with no search over states. A walk that repeats a node costs
at least the simple path left when its loop is cut out, since dropping
edges never raises the sum of all but the k heaviest. It checks 1000
random connected graphs of 2 to 6 nodes with weights up to 9, then 20 of
up to 60 nodes with weights up to `10^6`. Every case is drawn before any
arm answers.

| | property |
|---|---|
| P1 | up to 6 nodes, the answer is the literal reading's |
| P2 | s and d swapped: the same answer |
| P3 | n - 1 hops: 0 |
| P4 | every weight doubled: the answer doubled |
| P5 | one hop more: no larger; and no hops at all: no smaller |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1020 cases: checksum 53232401, 30600 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same 1000 small cases over simple paths gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. Two first choices were replaced. The dense
arm's matrix filled one way only left d out of reach, and the arm's
answer of `i64.MAX` overflowed when P4 doubled it, a crash rather than a
wrong answer. The solution's hops counted against k + 1 behind a bounds
guard was equivalent, the guard doing what the bound did.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a hop costs the edge's weight too | P1 696, P3 1020, P6 715 |
| M2 | ★: the search stops at the first neighbour of d it relaxes | P1 670, P2 210, P3 1020, P5 5, P6 690 |
| M3 | layers: a layer starts from its neighbours only, not itself | P1 89, P3 175, P5 85, P6 89 |
| M4 | layers: the last layer's search skipped | P1 34, P2 58, P6 34 |
| M5 | dense: a node settled only once over every layer | P1 35, P2 60, P6 36 |
| M6 | dense: a hop taken only toward a higher-numbered node | P1 390, P2 701, P3 585, P6 406 |
| M7 | queue: a state never queued again once taken | P1 194, P2 200, P3 297, P6 202 |
| M8 | queue: the answer d's distance with every hop spent | P1 89, P3 175, P5 85, P6 89 |
| M9 | solution: a hop costs 1 | P1 696, P3 1020, P4 715, P6 715 |
| M10 | solution: each edge stored one way only | P1 510, P2 815, P3 430, P4 430, P6 514 |

## Benchmarks

The bench draws 50 graphs of 500 nodes, LeetCode's most, each a random
tree and then up to 9501 more edges, weights up to `10^6`, with 0 to 49
hops and random s and d, all of them first, then answers each 10 times
by the ★ arm in all five languages. The heap is each language's own:
Kāra's `PriorityQueue` and Rust's `BinaryHeap` of `Reverse` tuples, Go's
`container/heap`, Python's `heapq`, and in C a binary heap of its own on
the same lexicographic order; C keeps the adjacency in one flat array
by node. Every implementation prints `50 graphs of 500 nodes, 10 rounds:
lengths sum to 264810, checksum 799703757`.

BENCHTAB

## Verification

All five arms print the same output as `hops.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

The harness keeps away from the dense arm's worst case: its first draft
ran the path of 500 with 250 and 499 hops, 500 layers of `500^2` scans,
which took two minutes under the interpreter.

## Writing it

The four arms of our own checked clean as first written.

LeetCode's Rust template took one `karac fix` of 39 edits, the wrapper
included. The two `use` lines went, `Reverse` because Kāra's
`PriorityQueue` already pops the smallest first; `BinaryHeap::new()`
became `PriorityQueue.new()`, and every `Reverse((..))` became the bare
tuple, in the pushes and in the `while let Some(Reverse((dd, u, t)))`
pattern. `usize` became `i64`, `vec![vec![i64::MAX; k + 1]; n]` became
`Vec.filled(n, Vec.filled(k + 1, i64.MAX))`, `for &(v, w)` dropped its
`&`, `&&` became `and`, and `Solution::` became `Solution.`.
