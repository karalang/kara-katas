# 882. Reachable Nodes In Subdivided Graph

You are given an undirected graph (the "original graph") with `n` nodes
labeled from `0` to `n - 1`. You decide to subdivide each edge in the
graph into a chain of nodes, with the number of new nodes varying
between each edge. The graph is given as a 2D array of `edges` where
`edges[i] = [u, v, cnt]` indicates that there is an edge between nodes
`u` and `v` in the original graph, and `cnt` is the total number of new
nodes that you will subdivide the edge into. Note that `cnt == 0` means
you will not subdivide the edge. To subdivide the edge `[u, v]`, replace
it with `cnt + 1` new edges and `cnt` new nodes. The new nodes are `x1`,
`x2`, ..., `xcnt`, and the new edges are `[u, x1]`, `[x1, x2]`, ...,
`[xcnt, v]`. In this new graph, you want to know how many nodes are
reachable from node `0`, where a node is reachable if the distance is
`maxMoves` or less. Given the original graph and `maxMoves`, return the
number of nodes that are reachable from node `0` in the new graph.

```
edges = [[0,1,10],[0,2,1],[1,2,2]], maxMoves = 6, n = 3  ->  13
edges = [[0,1,4],[1,2,6],[0,2,8],[1,3,1]], maxMoves = 10, n = 4  ->  23
edges = [[1,2,4],[1,4,5],[1,3,1],[2,3,4],[3,4,5]], maxMoves = 17, n = 5  ->  1
```

**Constraints:** `0 <= edges.length <= min(n * (n - 1) / 2, 10^4)`,
`edges[i].length == 3`, `0 <= u < v < n`, there are no multiple edges in
the graph, `0 <= cnt <= 10^4`, `0 <= maxMoves <= 10^9`,
`1 <= n <= 3000`.

## Approaches

| file | mechanism |
|---|---|
| `reachable_nodes.kara` ★ | Dijkstra with a priority queue: an edge of cnt new nodes is a path of length cnt + 1 between its ends, so Dijkstra over the original nodes alone gives the moves that reach each of them. An original node counts when that is at most `maxMoves`; on each edge the walk from one end covers `maxMoves` less that end's distance of the new nodes, the walk from the other end the same, together at most cnt. A distance above `maxMoves` is never kept. O(E log E) |
| `reachable_nodes_dense.kara` | Dijkstra by scanning: the same distances with no queue, each round settling the nearest node not yet settled, found by scanning all n, until no node within `maxMoves` is left. O(n^2 + E) |
| `reachable_nodes_queue.kara` | shortest paths by a work queue (Bellman-Ford in queue order): a node whose distance falls goes on a `VecDeque`, unless it is on it already, and its edges are relaxed when it comes off; a node can be relaxed more than once. O(n E) at worst |
| `reachable_nodes_heap.kara` | Dijkstra with a hand-built heap: the ★ arm's search with its queue written out as a binary min-heap in a `Vec`, each entry a distance and a node packed into one number, `distance * 4096 + node`. O(E log E) |
| `reachable_nodes_moves_left.kara` | the moves left: the search keeps the most moves still left on reaching each original node and takes the node with the most next, from a max-first queue; from a node with `left` moves an edge is walked `min(left, cnt)` of the way, and its other end reached with `left - cnt - 1` when that is not negative. O(E log E) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples and six
more (one node and no edges; an edge of 3 new nodes with 0, 4 and 2
moves; a path of three edges with no new nodes and 2 moves; and an edge
of 10^4 new nodes with 10^9 moves); the nodes reached in 2,000 cases of
up to 8 nodes, 12,051 in all; and in 12 cases of 1,000 to 3,000 nodes
with up to 10^4 edges of up to 10^4 new nodes, a third of them with up
to 10^9 moves and the rest up to 10^5, with a checksum.
`reachable_nodes.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the new graph built, each edge replaced by its chain of new
nodes, and a breadth-first search from node 0 counting the nodes at most
`maxMoves` away. It checks 2,040 cases: 2,000 of up to 8 nodes, 13
edges of up to 6 new nodes and 19 moves, against the statement; and 40
of 100 to 500 nodes with up to 2,000 edges of up to 100 new nodes and up
to 2,999 moves, against the other properties. The ★ arm's counts sum to
3,823,379.

| | property |
|---|---|
| P1 | the statement's count, on up to 8 nodes |
| P2 | node 0 at least, and at most every node, original and new |
| P3 | the same graph with nodes 1 to n - 1 relabelled, the edges in another order and each turned round half the time |
| P4 | one more move never reaches fewer nodes, and moves enough to walk every edge reach all of node 0's component |
| P5 | an edge of extra new nodes from node 0 to a node of its own adds the new nodes walked, and that node when the walk reaches it |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `2040 cases, nodes
reached sum to 3823379, 61000 checks over 5 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an edge of cnt new nodes weighing cnt | P1 344, P5 66, P6 346 |
| M2 | ★: a node reached with every move used not counted | P1 272, P2 109, P4 854, P5 69, P6 273 |
| M3 | ★: new nodes walked from both ends counted twice | P1 1106, P2 968, P4 1357, P5 684, P6 1146 |
| M4 | dense: the farthest node settled first | P1 5, P3 6, P4 7, P6 21 |
| M5 | dense: both walks taken from the first end | P1 379, P3 361, P4 51, P5 1186, P6 381 |
| M6 | dense: a walk from an end out of reach counted as negative | P1 703, P2 318, P3 296, P4 390, P6 704 |
| M7 | queue: a node queued only when it is queued already | P1 449, P4 752, P6 489 |
| M8 | queue: a node never queued a second time | P1 2, P3 3, P6 4 |
| M9 | queue: an edge weighing one more | P1 403, P4 421, P5 69, P6 405 |
| M10 | heap: the last entry dropped instead of the top | P1 180, P3 17, P4 380, P5 54, P6 220 |
| M11 | heap: an edge holding one more new node than it has | P1 1106, P2 720, P4 1357, P5 684, P6 1146 |
| M12 | heap: the node left pushed instead of the node reached | P1 449, P4 752, P6 489 |
| M13 | moves-left: crossing an edge costing cnt moves | P1 344, P5 66, P6 346 |
| M14 | moves-left: a node taken again each time it comes off the queue | P1 127, P2 133, P3 41, P4 245, P6 167 |
| M15 | moves-left: both ends' walks kept in one place | P1 445, P4 493, P5 325, P6 447 |

P1 and P6 kill all fifteen. M1 and M13 are one fault in two arms,
crossing an edge one move too cheaply, and fail the same cases; M7 and
M12 fail the same cases too, as both leave every node but 0 unexpanded.
M4 and M8 are the closest to surviving: a node settled out of order, or
taken off the queue for good, gives a wrong distance only when a longer
path to it is found first and a shorter one later, which few small
graphs arrange. No mutant was replaced, but three edits were not tried
because they are equivalent: in the heap arm, a heap that pops entries
out of order still settles every distance, since the search relaxes a
node again whenever its distance falls and skips only stale entries; so
does dropping that skip; and in the moves-left arm a walk recorded as up
to cnt + 1 counts the same, as each edge's two walks are capped at cnt.

## Verification

Every arm prints the same output as `reachable_nodes.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `89d76e3ff2` and the runtime
archives at `e903d5b111`, with no runtime change between them. Under
`karac __mir-run` the arms take 2 to 12 s each (the dense arm, scanning
every node each round, the slowest) and the differential 22 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends' JIT and `karac build --legacy`, with and
without auto-par, print the same output for all five arms and the
differential. Its interpreter prints the fixed cases right but other
totals for both sets of random cases, the same in every arm, and
another sum for the differential's cases (3,651,864) with 0 failures:
the arms agree with one another and with the statement there, so the
random graphs it draws most likely differ, not the arms (inferred, not
traced). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 600 graphs of
2,000 to 3,000 nodes, each node joined to the nodes three distinct
offsets on, so that no pair repeats and every graph has 3n edges, up to
9,000; each edge holds up to 10^4 new nodes and each search has up to
2 x 10^5 moves. Every graph is drawn from the same generator in each
language as it is solved. The edges are a `Vec` of `Vec`s in Kāra and
Rust, as LeetCode passes them, a slice of slices in Go and a list of
lists in Python; the queue is Kāra's `PriorityQueue`, Rust's
`BinaryHeap`, Go's `container/heap` and Python's `heapq`. C has no
queue, so its program writes a binary heap out, and it keeps the edges
in one flat array and the adjacency as one array indexed by node
offsets, where the others keep a list per node. Every implementation
prints `600 graphs of up to 3000 nodes: 18236308868 nodes reached,
checksum 994158081`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.23 to 0.26 s | 0.23 s |
| Rust (`rustc -O`) | 0.41 to 0.45 s | 0.43 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.41 to 0.49 s | 0.45 s |
| Go | 0.84 to 0.99 s | 0.89 s |
| Python | 7.4 s | |
| Kāra (`karac build --mir`) | 0.52 to 0.62 s | 0.55 s |
| Kāra legacy (`karac build --legacy`) | 0.53 to 0.58 s | 0.55 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 881's does.

v2 takes 1.22 times Rust's median time under overflow checks, 0.99
times legacy's and 2.34 times C's. Under valgrind's cachegrind C runs
1.23 billion instructions, Rust with overflow checks 4.57 billion,
legacy 5.61 billion and v2 5.24 billion. C's flat arrays most likely
account for much of its lead, as the others allocate a small `Vec` for
every edge and every node's list (inferred from the layouts and counts,
not profiled). The comparison with C and Rust waits until after M4.
