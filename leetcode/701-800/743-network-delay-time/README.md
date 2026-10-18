# 743. Network Delay Time

A network has `n` nodes, labelled 1 to `n`, and `times` lists its
directed edges as `(u, v, w)`: a signal at `u` reaches `v` after `w`
units of time. A signal is sent from node `k`. Return the least time it
takes for all `n` nodes to receive it, or -1 if some node never does.

```
times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]], n = 4, k = 2  ->   2
times = [[1, 2, 1]], n = 2, k = 1                        ->   1
times = [[1, 2, 1]], n = 2, k = 2                        ->  -1
```

**Constraints:** 1 <= `k` <= `n` <= 100; 1 to 6000 edges; 1 <= `u`, `v`
<= `n` and `u != v`; 0 <= `w` <= 100; no pair `(u, v)` appears twice.

## Approaches

A node hears the signal at the time of its quickest way from `k`, so the
answer is the largest of the shortest times from `k`, or -1 when some
node has no way at all. No edge takes negative time, so Dijkstra's
settling order applies. The arms take the edges as a vector of `(u, v,
w)` tuples.

| file | mechanism |
|---|---|
| `network_delay_time.kara` ★ | Dijkstra with a smallest-first `PriorityQueue` of (time, node) over adjacency lists built for each call; an entry for a node already settled is skipped, and the last node settled gives the answer; O(E log E) |
| `network_delay_time_dense.kara` | Dijkstra on an (n + 1) x (n + 1) matrix of edge times: each of n rounds scans every node for the unsettled one heard earliest, settles it and improves its neighbours through its row; O(n^2) |
| `network_delay_time_bellman.kara` | Bellman and Ford: up to n - 1 passes over the edge list, lowering a node's time whenever an edge offers an earlier one, and stopping after a pass that changes nothing; O(n E) |
| `network_delay_time_floyd.kara` | Floyd and Warshall: the shortest time between every pair, improved by letting the ways stop at node 1, then also at node 2, and so on; the answer reads `k`'s row; O(n^3) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the three LeetCode examples; a way
of two short edges that beats one long edge; a way round a cycle; edges
that take no time; a graph with a node no edge reaches; sources 1 to
20 of a random graph of 100 nodes and 6,000 edges, the most LeetCode
allows, and of a ring of 100 nodes with 300 more random edges, each with
how many sources reach every node and the sum of their answers; the
start and the middle of a path of 100 nodes; and 300 random graphs of
2 to 8 nodes, with how many reach every node, the sum of their answers
and a checksum. The harness asks 20 sources of the large graphs rather
than 100 so that the Floyd arm, which pays O(n^3) for every call, stays
well inside the corpus's 60 s limit under `karac __mir-run`.
`network_delay_time.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which walks every simple path out of `k`, keeping each node's earliest
arrival, and takes the latest of those, or -1 when some node has no
path. 3,000 random graphs are checked, each of 2 to 6 nodes with 1 to
n(n - 1) distinct edges of 0 to 9 units, so that ties and edges that
take no time are common, and with `k` a random node; in 1,110 of them
some node is never reached, and the answers of the rest sum to 12,742.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the nodes renamed by a random order, `k` with them, give the same answer |
| P3 | every edge taking three times as long triples the answer, and -1 stays -1 |
| P4 | when every node is reached, one edge added that was not there, of 0 to 19 units, gives an answer no later than before, and the same answer when the edge takes at least as long as the old answer |

It prints `3000 graphs (1110 with a node never reached, answers sum to
12742), 4 arms, 41464 checks, 0 failures` under `karac __mir-run` and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: never -1, the last time returned whatever was reached | P1 1110, P4 454 |
| M2 | ★: an arrival timed by its last edge alone | P1 1052, P2 53, P4 27 |
| M3 | ★: a stale entry for a settled node settling it again | P1 1183, P2 13, P4 180 |
| M4 | dense: the latest unsettled node chosen, not the earliest | P1 1150, P2 8, P4 65 |
| M5 | dense: a chosen node never marked settled | P1 2943 |
| M6 | dense: the first offer for a node kept, never improved | P1 585, P2 22, P4 140 |
| M7 | bellman: one pass fewer | P1 565 |
| M8 | bellman: the earliest time kept as the answer, not the latest | P1 1833 |
| M9 | bellman: stopping after the first pass that changes something | P1 723 |
| M10 | floyd: a node not reaching itself at time 0 | P1 1057 |
| M11 | floyd: the last node never a stop on the way | P1 291, P2 418 |
| M12 | floyd: a stop skipped when it cannot reach i, not when i cannot reach it | P1 331, P2 150, P4 19 |
| E1 | ★: settled neighbours queued too | 0 |
| E2 | dense: settled nodes offered times too | 0 |
| E3 | bellman: an edge from a node never reached relaxed too | 0 |

P1 kills all twelve. P3 kills none: every edit here treats all times
alike, so tripling every edge triples the wrong answer too, and P3 is
there to catch an arm that adds or compares times in some other way.
P2 sees the edits whose answer depends on the order the nodes are tried
in or numbered: M2, M3, M4 and M6 give answers that depend on the order
in which the nodes settle, which among equal times follows the node
numbers; M11 leaves node n out as a stop, and renaming changes which
node that is; and M12 skips stops by the wrong test, which depends on
how the nodes are numbered. P4 sees M1, whose answer is never -1 and so
meets the new edges in graphs where the true answer is, and
M2, M3, M4, M6 and M12, whose answers can grow when an edge is added.
M5 never marks a node settled and so settles `k` n times and answers
0; M8 keeps the earliest time, 0 whenever every node is reached. E1 and
E2 offer times to nodes already settled, which can never improve them
since no time is negative; E3 lets a node never reached pass on its
placeholder time, which is too large ever to win.

## Verification

Every arm prints the same output as `network_delay_time.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`1d96cab833`, whose last compiler change is `afe886a96d`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at a `*` over a vector's `iter()`
(`*t` over the edge tuples), since legacy gives those by value where
v2 gives references. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes a
random graph of 100 nodes and 6,000 edges of 0 to 100 units, the largest
LeetCode allows, and in each of 12 rounds gives 50 random edges new
times and asks for every node as `k`, 1,200 queries in all. Each query
builds its adjacency lists, its arrival times and its queue afresh as
growable arrays, as the ★ arm does; C and Go use a hand-written binary
heap ordered by time and then node, as the others' are, Rust a
`BinaryHeap` of `Reverse` pairs and Python `heapq`. Every implementation
prints `12 rounds of 100 queries on 100 nodes and 6000 edges: answers
sum to 18820`, the Kāra program under `karac __mir-run` included (in
134 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.28 to 0.31 s |
| Rust (`rustc -O`) | 0.30 to 0.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.29 to 0.34 s |
| Go | 0.63 to 0.66 s |
| Python | 2.5 to 2.6 s |
| Kāra (`karac build --mir`) | 0.62 to 0.71 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.8 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 2.3 times
as long as C (0.66 s against 0.29) and 2.1 times as long as Rust
(0.31, or 0.33 under overflow checks), and is level with Go
(0.64). Under valgrind's cachegrind it runs 4.1 billion instructions
against C's 1.9 and Rust's 1.8, 0.70 billion branches against 0.23 and
0.19, and 46 million mispredicted branches against 13 for each. Under
half of v2's instructions are in `main` itself, where the ★ arm is
inlined, and nearly as many again are in code without symbols, which was
not traced further; `malloc` and `free` take 7%. The legacy backends
refuse the program. To have a legacy time at all, the bench was
rewritten for legacy alone with indexed loops in place of the two
`iter()` loops: the legacy build of that copy ran 0.55 to 0.60 s and the
v2 build of the same copy 0.71 to 0.73 s, so v2 takes about 1.3 times as
long as legacy, inside M2's limit of twice legacy; that copy is a
measurement only and is not in the kata, and new katas' benches are
outside M2's frozen set in any case. The comparison with C and Rust
waits until after M4.

## Compiler findings

None new.
