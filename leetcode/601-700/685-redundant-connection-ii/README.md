# 685. Redundant Connection II

A rooted tree is a directed graph with exactly one vertex, the root,
that every other vertex descends from, every other vertex having exactly
one parent and the root none. A graph started as a rooted tree with `n`
vertices numbered 1 to `n`, and one more directed edge was added,
between two different vertices and not one already there. Given its `n`
edges as `edges[i] = [u, v]`, `u` a parent of `v`, return an edge that
can be removed so that what is left is a rooted tree of `n` vertices; if
there are several, return the one that comes last in the input.

```
edges = [[1, 2], [1, 3], [2, 3]]                  ->  [2, 3]
edges = [[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]]  ->  [4, 1]
```

**Constraints:** `n` = `edges.length`; 3 <= `n` <= 1000; 1 <= `u`, `v`
<= `n`; `u` != `v`.

## Approaches

Every arm is `fn find_redundant_directed_connection(edges:
Vec[(i64, i64)]) -> (i64, i64)`.

| file | mechanism |
|---|---|
| `redundant_connection_ii.kara` ★ | the new edge either gives some vertex two parents, whose two incoming edges are then the only candidates, or closes a cycle through the root; add every edge but the later candidate to a disjoint-set forest: no cycle means the later candidate, a cycle means the earlier candidate if there is one, else the edge that closed it |
| `redundant_connection_ii_peel.kara` | forget the directions and peel leaves off until only the one cycle is left; the answer is the candidate on it, the later if both are, or with no candidates the cycle's last edge in the input |
| `redundant_connection_ii_walk.kara` | keep each vertex's parent, skipping the later candidate, and find a cycle by walking up from every vertex, colouring the vertices on the current walk |
| `redundant_connection_ii_removal.kara` | from the last edge back, leave the edge out and check that the rest has one root, no vertex with two parents, and every vertex reached from the root |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 13 lines: the two LeetCode examples; nine
corners, among them a cycle through the root with no vertex of two
parents, a cycle of two vertices, a vertex with two parents and no
cycle, the two parents' edges of one vertex with the cycle through
either of them, and one of 10 vertices; every rooted tree on 3 to
5 vertices with every edge it does not have added, 10,612 graphs in all,
each with its edges in order and reversed, with a checksum; and
200 random graphs of up to 1,000 vertices, with a checksum.
`redundant_connection_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: the last edge in the
input without which exactly one vertex has no parent, none has two, and
that vertex reaches every vertex, by the transitive closure of the other
edges. The removal arm asks the same question by a search, so it is the
arm nearest the definition. 1,500 random rooted trees with one more edge
are checked, two thirds of 3 to 10 vertices and a third of 3 to 102; the
1,035 of up to 10 vertices go against the definition. Half the time the
new edge is aimed up the tree, since a random edge seldom closes a
cycle, and the run counts the three kinds it made: edges into the root,
edges up the tree to an ancestor, and edges across.

| | property |
|---|---|
| P1 | the answer is the definition's (up to 10 vertices) |
| P2 | renaming the vertices renames the answer |
| P3 | the answer moved to the end of the input is still the answer |
| P4 | the answer follows from how the graph was built: an edge into the root makes it the last edge of the cycle it closes; an edge up the tree, the new edge; an edge across, the later of the two edges into its end |

It prints `1500 graphs (668 into the root, 258 up the tree, 574 across),
4 arms, 22140 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the later candidate taken when a cycle is found | P1 62, P4 119 |
| M2 | ★: the later candidate added like any other edge | P1 443, P3 832, P4 713 |
| M3 | peel: the earlier candidate asked whether it is on the cycle | P1 136, P4 258 |
| M4 | peel: an edge with one end on the cycle counted as on it | P1 274, P4 423 |
| M5 | walk: the earlier candidate taken when there is no cycle | P1 443, P3 832, P4 713 |
| M6 | walk: an edge with one end on the cycle counted as on it | P1 212, P4 304 |
| M7 | removal: the last edge never tried | P1 458, P2 25, P3 1500, P4 490 |
| M8 | removal: children counted, not parents | P1 1035, P2 1500, P3 1500, P4 1500 |
| E1 | ★: no path halving | 0 |
| E2 | peel: a neighbour of degree 1 left as it is | 0 |
| E3 | walk: the clean-up walk goes on past vertices not yet seen | 0 |
| E4 | removal: a graph with no root searched anyway | 0 |

P1 and P4 kill all eight. P3 sees M2 and M5, which answer the earlier of
two parents' edges when the later is the one to remove: moved to the
end, that edge becomes the later. It also sees M7, which never tries the
last edge, and M8. M2 and M5 fail exactly the same checks: both answer
the earlier candidate whenever the later one is right. M5 does so
directly. M2 puts the later candidate in the forest, and the two edges
into one vertex then always close the graph's one undirected cycle or
lie on it, so a cycle is always found and the earlier candidate
answered. P2 sees only M7 and M8, the arms' answers otherwise not
depending on the vertices' numbers; M7 fails it when the last edge is
the only one to remove and it answers (0, 0), which P2 counts as a
failure, inferred from the counts, not shown. The four survivors change
no answer. Path halving only shortens later searches; two leaves are
next to each other only in a graph of two vertices; the clean-up walk
stops at the same vertex either way, since every vertex on the walk was
marked; and with no root the search starts at vertex 0, which has no
children, so one vertex is reached and the graph is still refused. One
more edit was tried and also survived: checking that n - 1 vertices are
reached, not n. A part the root cannot reach holds a cycle of at least
two vertices, so a search reaching n - 1 has reached them all.

## Verification

Every arm prints the same output as `redundant_connection_ii.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`e765966014` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends print the same output for the ★ arm and the
walk arm under the interpreter, the JIT and `karac build`, with and
without `KARAC_AUTO_PAR=1`. They refuse the peel and removal arms and
the differential at type checking, at `*w`, since legacy gives the items
of `adj[v].iter()` by value where v2 gives references. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random rooted trees of
20,000 vertices once, each with one more random edge and its edges
shuffled, then answers every graph in each of 30 rounds, putting each
answer into a checksum. Every implementation prints `3000 graphs
answered, checksum 937926238`, the Kāra program under `karac __mir-run`
included (in 159 s).

Each implementation is the same union-find, with path halving, after a
pass that finds a vertex with two parents, on two freshly allocated
arrays per graph. Spot timings on a shared 4-core container, six runs
each, three of them interleaved (two for Python; `bench.sh` timings need
a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.91 to 0.94 s |
| Rust (`rustc -O`) | 0.68 to 0.92 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.67 to 0.80 s |
| Go | 1.01 to 1.16 s |
| Python | 33.0 to 34.6 s |
| Kāra (`karac build --mir`) | 0.83 to 0.95 s |
| Kāra, legacy (`karac build`, a copy) | 0.72 to 0.80 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking:
`find_redundant_directed_connection(graphs[c])` moves an element out of
`graphs` under legacy, where a bare parameter is owned, but v2 borrows
it. That edit is by hand, on top of the `scripts/new-bench.sh` output. A
copy outside the kata whose parameter is `ref Vec[(i64, i64)]` builds
under legacy, and its row is above. Under `karac __mir-llvm-run` the
program prints the same line in 3.6 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

So the v2 build is level with C and ahead of Go here, and about a sixth
behind legacy and Rust. Under callgrind it runs 4.99G instructions to
legacy's 3.70G, and `memcpy` takes 0.23G of them, where legacy's profile
does not list it at all. That `memcpy` count is exactly the one kata
684's bench shows, and the one thing the two benches share is a
20,001-element `Vec` grown by `push` 3,000 times, so the copies are
probably that `Vec` growing; that is inferred, not traced. The gap is
under the M2 bar of 1.5x legacy, so it is noted, not filed. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
