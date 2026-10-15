# 684. Redundant Connection

A tree is an undirected graph that is connected and has no cycles. A
graph started as a tree with `n` vertices numbered 1 to `n`, and one
more edge was added, between two different vertices and not one already
there. Given its `n` edges as `edges[i] = [a, b]`, return an edge that
can be removed so that what is left is a tree of `n` vertices; if there
are several, return the one that comes last in the input.

```
edges = [[1, 2], [1, 3], [2, 3]]                  ->  [2, 3]
edges = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]  ->  [1, 4]
```

**Constraints:** `n` = `edges.length`; 3 <= `n` <= 1000; 1 <= `a` < `b`
<= `n`; no edge is repeated; the graph is connected.

## Approaches

Every arm is `fn find_redundant_connection(edges: Vec[(i64, i64)]) ->
(i64, i64)`.

| file | mechanism |
|---|---|
| `redundant_connection.kara` ★ | add the edges in order to a disjoint-set forest, with path halving and union by size; the first edge whose ends are already in one set closes the only cycle, and since the cycle is complete only once its last edge in the input is added, that edge is the answer |
| `redundant_connection_search.kara` | the same order with an adjacency list: before adding each edge, a depth-first search from one end for the other |
| `redundant_connection_peel.kara` | remove leaves over and over until only the cycle is left, every vertex of degree 2 or more; the answer is the last edge in the input with both ends on it |
| `redundant_connection_removal.kara` | from the last edge back, leave the edge out and check by a breadth-first search that the other edges still reach every vertex |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the two LeetCode examples; seven
corners, among them the triangle in other orders and written the other
way round, a cycle through all six vertices, a graph whose cycle closes
before its last edge and one of 10 vertices; every tree on 3 to
6 vertices with one more edge, 3,898 in all, each with its edges in
order and reversed, with a checksum; and 200 random graphs of up to
1,000 vertices, with a checksum. The harness shuffles the edges and
writes each either way round, so it also passes edges with `a > b`,
which LeetCode's constraints rule out; every arm answers with the edge
as given. `redundant_connection.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: the last edge in the
input whose removal leaves every vertex reachable from vertex 1, by the
transitive closure of the other edges. The removal arm asks the same
question by a search, so it is the arm nearest the definition.
1,500 random trees with one more edge are checked, two thirds of 3 to
10 vertices and a third of 3 to 102; the 1,044 of up to 10 vertices go
against the definition.

| | property |
|---|---|
| P1 | the answer is the definition's (up to 10 vertices) |
| P2 | renaming the vertices renames the answer |
| P3 | the answer moved to the end of the input is still the answer |
| P4 | a graph built round a known cycle answers the cycle edge last in the input |

It prints `1500 graphs, 4 arms, 22176 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second end's own label taken as its root | P1 957, P2 1403, P3 1409, P4 1435 |
| M2 | ★: a union that keeps the smaller root on its own | P1 1021, P2 1471, P3 1471, P4 1485 |
| M3 | search: each edge added in one direction only | P1 831, P2 1261, P3 1261, P4 1357 |
| M4 | search: a search that looks for its own start | P1 1044, P3 1500, P4 1500 |
| M5 | peel: an edge with one end on the cycle taken | P1 294, P4 380 |
| M6 | peel: no new leaf once a leaf is gone | P1 34, P4 81 |
| M7 | removal: each edge added in one direction only | P1 978, P2 1463, P3 1350, P4 1426 |
| M8 | removal: one vertex short counted as connected | P1 281, P2 100, P4 360 |
| E1 | ★: no path halving | 0 |
| E2 | search: the start not marked as seen | 0 |
| E3 | peel: a neighbour of degree 1 left as it is | 0 |
| E4 | removal: a stack, not a queue | 0 |

P1 and P4 kill all eight. P2 sees M1, M2, M3, M7 and M8. M1 takes a
vertex's number for its root, and M8 searches from vertex 1, so renaming
changes their answers; M2, M3 and M7 fail so many graphs that they
probably answer (0, 0) at times, which P2 counts as a failure; that is
inferred from the counts, not shown. P3 sees M1 to M4 and M7 and misses
M5, M6 and M8: like the right answer, each of those takes the last edge
in the input that passes some test, and moving that edge to the end
leaves it last. M4 always answers the first edge, which only P1, P3 and
P4 can tell from the right one. The four survivors change no answer.
Path halving only shortens later searches; a start not marked as seen is
pushed once more and searched from again; two leaves are next to each
other only in a graph of two vertices, and every graph here has a cycle;
and a stack reaches the same vertices as a queue.

## Verification

Every arm prints the same output as `redundant_connection.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`042e204d6c` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse every arm, the differential and the
bench program at type checking, at the first `*a` or `*w`, since legacy
gives the items of `edges.iter()` and `adj[v].iter()` by value where
v2 gives references. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random trees of
20,000 vertices once, each with one more edge, its edges shuffled and
each written either way round, then answers every graph in each of
30 rounds, putting each answer into a checksum. Every implementation
prints `3000 graphs answered, checksum 436900690`, the Kāra program
under `karac __mir-run` included (in 231 s).

Each implementation is the same union-find, with path halving and union
by size, on two freshly allocated arrays per graph. Spot timings on a
shared 4-core container, six runs each, three of them interleaved (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.03 to 1.26 s |
| Rust (`rustc -O`) | 1.02 to 1.13 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.00 to 1.04 s |
| Go | 1.23 to 1.38 s |
| Python | 28.9 to 29.2 s |
| Kāra (`karac build --mir`) | 1.21 to 1.37 s |
| Kāra, legacy (`karac build`, a copy) | 1.04 to 1.12 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking, as above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata that drops the
`*` and takes `ref Vec[(i64, i64)]`, since legacy owns a bare parameter,
builds under legacy, and its row is above. Under `karac __mir-llvm-run`
the program prints the same line in 3.9 s, compile included; that JITs
the MIR's IR without optimization passes, so it is not a benchmark.

So the v2 build is about a fifth behind legacy, C and Rust here, and
level with Go. Under callgrind it runs 4.94G instructions to legacy's
2.82G; building the graphs is 0.27G against 0.17G of that, so most of
the difference is in the 3,000 answers, and `memcpy` alone is 0.23G
against 0.03G. Why the time grows less than the instructions was not
looked into; the union-find's scattered reads may set it, which is
inferred, not measured. The gap is under the M2 bar of 1.5x legacy, so
it is noted, not filed. The comparison with C and Rust waits until after
M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
