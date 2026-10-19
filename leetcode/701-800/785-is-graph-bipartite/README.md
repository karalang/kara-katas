# 785. Is Graph Bipartite?

An undirected graph of `n` nodes, numbered from 0, is given as adjacency
lists: `graph[u]` holds the nodes `u` is joined to. It has no edge from
a node to itself and no edge twice, and it need not be connected. Return
whether it is bipartite: whether its nodes can be split into two sets so
that every edge joins a node of one set to a node of the other.

```
graph = [[1,2,3],[0,2],[0,1,3],[0,2]]  ->  false
graph = [[1,3],[0,2],[1,3],[0,2]]      ->  true
```

**Constraints:** `n` is from 1 to 100, and every list holds distinct
nodes other than its own, with `v` in `graph[u]` exactly when `u` is in
`graph[v]`.

## Approaches

A graph is bipartite exactly when it has no cycle of odd length, which
is when its nodes can be coloured with two colours so that every edge
joins different colours.

| file | mechanism |
|---|---|
| `is_bipartite.kara` ★ | two colours by breadth first search: each uncoloured node starts a search with a `VecDeque`, every neighbour taking the other colour, and an edge between two nodes of one colour ends it; O(n + e) |
| `is_bipartite_dfs.kara` | the same two-colouring by recursion, painting a node and then each uncoloured neighbour with the other colour; O(n + e) |
| `is_bipartite_neighbours.kara` | all the neighbours of a node must share a colour, the one the node lacks: each node's neighbours are joined into one set of a disjoint-set forest, and a node in the same set as a neighbour means an odd cycle; O(e α(n)) |
| `is_bipartite_parity.kara` | a disjoint-set forest with parity: each node keeps whether it has the other colour from its parent, every edge says its ends differ, and an edge inside one tree whose ends have the same parity means an odd cycle; O(e α(n)) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 13 lines: LeetCode's two examples; one node;
one edge; a triangle and a node on its own; a square with a triangle
beside it, and with a path beside it; cycles of 100 and 99 nodes; two
sides of 50 with every pair across them joined, and that with one more
edge inside a side; a random tree of 100 nodes; then 300 random graphs
of 1 to 100 nodes, with how many are bipartite and a checksum.
`is_bipartite.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every way of putting each node on one of two sides is tried, one subset
of the nodes at a time, for one with every edge going across. Its 1,600
random graphs are 1,200 of 1 to 12 nodes, where that search is cheap,
and 400 of 13 to 100. A quarter have edges only across a random split of
the nodes, a quarter that and one edge inside a side, a quarter any
pairs joined, and a quarter are a random tree with one more edge, which
closes a cycle of either length; the chance of an edge gives each node
about one to three.

| | property |
|---|---|
| P1 | the answer is the definition's (graphs up to 12 nodes) |
| P2 | the nodes renamed in a random order, and every list shuffled, give the same answer |
| P3 | with every edge split in two by a new node in its middle the graph is bipartite: the old nodes on one side, the new on the other |
| P4 | a triangle on three new nodes, numbered after the others, makes the graph not bipartite |

It prints `1600 graphs (1037 bipartite), 4 arms, 24000 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. Eleven are killed, and the twelfth, M6, cannot be.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only node 0's part searched | P1 13, P2 56, P4 1076 |
| M2 | ★: a neighbour given the same colour | P1 670, P3 1457 |
| M3 | ★: a coloured neighbour never checked | P1 387, P4 1600 |
| M4 | dfs: only clashes of colour 0 seen | P1 107, P2 191 |
| M5 | dfs: a failure deeper down ignored | P1 160, P2 224 |
| M6 | dfs: clashes seen only toward a lower node | none: equivalent |
| M7 | neighbours: the neighbours joined with the node itself | P1 670, P3 1457 |
| M8 | neighbours: a node compared only with itself | P1 387, P4 1600 |
| M9 | neighbours: the neighbour re-pointed, not its root | P1 3, P2 50 |
| M10 | parity: the flip not carried up the path | P1 293, P2 165 |
| M11 | parity: two trees joined with their ends alike | P1 670, P3 1457 |
| M12 | parity: the node re-pointed, not its root | P1 292, P2 257 |

M6 makes the recursion see a clash only toward a lower numbered node,
and it changes nothing. Take an edge whose two ends have one colour, and
say `u` was painted before `v`. Then `v` was painted while `u`'s loop
over its neighbours was still running, by the recursion from an earlier
neighbour, since `u`'s loop would otherwise have painted `v` itself with
the other colour. So `v`'s own loop, run as it is painted, finds `u`
coloured, and `u`'s loop later finds `v` coloured: the clash is looked
at from both ends, and one of them is the higher node. P1 kills the
other eleven. M2, M7 and M11 fail the same checks, each answering false
for every graph with an edge, and M3 and M8 answer true for every graph.
M9 is the weakest kill, with 53 failures: pointing the neighbour rather
than its root at the set loses the neighbour's earlier joins, which
matters only when it already had some.

## Verification

Every arm prints the same output as `is_bipartite.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at the type check: in `for v in graph[u].iter()` and
`for (a, b) in edges.iter()` they take the items for `i64` rather than
references, so `*v` is an error. Copies of the four arms with those `*`s
removed print the same output under the legacy interpreter (`karac run
--interp`), the legacy JIT (`karac run`), `karac build` and an auto-par
build, each build with warnings that a borrowed `graph` and `edges` are
used after a move, since legacy predates borrowed parameters. The bench
also needs its parameter written `ref Vec[Vec[i64]]`, as legacy refuses
`is_bipartite(graphs[r % 64])` as a move out of an index; the bench
timing below is of such a copy. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 graphs of 100
nodes, LeetCode's most, are built once: each node is put on a random
side and each pair across joined with chance 1 in 10, and every other
graph then has one edge added inside a side. Each of 500,000 rounds
answers the next graph. Every implementation prints `500000 rounds of
100-node graphs: 257812 bipartite, checksum 194783686`, the Kāra program
under `karac __mir-run` included (in 417 s).

Each round allocates a colour array and a queue and walks the graph
until it is coloured or a clash turns up. Kāra's and Rust's queues are a
`VecDeque`, C's a plain array as long as the graph, Go's a slice taken
from the front and Python's a `deque`. Spot timings on a shared 4-core
container, eight runs of each compiled program, five of them
interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.89 to 1.13 s |
| Rust (`rustc -O`) | 0.80 to 1.21 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.83 to 1.13 s |
| Go | 1.55 to 2.28 s |
| Python | 11.45 to 12.06 s |
| Kāra (`karac build --mir`) | 2.09 to 2.76 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 9.1 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.30 s,
against C's 0.98, Rust's 0.99 (0.93 under overflow checks) and Go's
1.82. Under valgrind's cachegrind v2 runs 12.5 billion instructions and
2.70 billion branches, against C's 2.75 billion and 0.67 billion and
Rust's 4.94 billion and 1.05 billion. Callgrind on a copy of 20,000
rounds puts 49% of v2's instructions in the runtime's `VecDeque` push
and pop, which the program calls rather than inlines; between them they
call `memcpy` 4.5 million times for their 3.3 million calls, copying the
8-byte elements, and that `memcpy` is 11% of the instructions on its
own. The legacy build of the copy ran 1.13 to 1.27 s, a median of 1.18 s
in the interleaved runs, and 4.64 billion instructions, so v2 takes 1.95
times legacy, just inside the 2 times above which a slower v2 is filed.
The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new.
