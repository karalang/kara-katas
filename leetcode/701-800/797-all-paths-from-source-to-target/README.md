# 797. All Paths From Source to Target

Given a directed acyclic graph of `n` nodes numbered 0 to `n - 1`, where
`graph[i]` lists the nodes with an edge from `i`, return every path from
node 0 to node `n - 1`, in any order.

```
graph = [[1, 2], [3], [3], []]               ->  [[0, 1, 3], [0, 2, 3]]
graph = [[4, 3, 1], [3, 2, 4], [3], [4], []]  ->  [[0, 4], [0, 3, 4], [0, 1, 3, 4], [0, 1, 2, 3, 4], [0, 1, 4]]
```

**Constraints:** 2 to 15 nodes; `graph[i]` holds distinct nodes other
than `i`; the graph has no cycle.

## Approaches

| file | mechanism |
|---|---|
| `all_paths_source_target.kara` ★ | depth first search from node 0 keeping the path so far, recording a copy of it at `n - 1` and taking each step back after trying it; O(2^n · n), the number of paths times their length |
| `all_paths_source_target_queue.kara` | breadth first search over paths: take a path off the front of a queue, record it if it ends at `n - 1`, otherwise put back one longer path for each next node of its end; O(2^n · n) |
| `all_paths_source_target_memo.kara` | the paths from a node are the node followed by each path from each of its next nodes, worked out once for each node and kept, so a node reached by many routes is not walked again; O(2^n · n) |
| `all_paths_source_target_stack.kara` | the depth first search without recursion, keeping beside each node on the path how many of its next nodes have been tried; O(2^n · n) |
| `differential.kara` | the four arms against the definition, four properties |

The arms give the paths in different orders, so the harness sorts them
before printing. Every arm prints the same 7 lines: LeetCode's two
examples; two nodes and one edge; two nodes and no edge; three nodes
with an edge from `n - 1` to node 1, which no path reaches; the graph on
15 nodes with every edge from a lower node to a higher one, whose 8,192
paths are counted with a checksum; and 300 random graphs of 2 to 12
nodes, with the paths in all and a checksum.
`all_paths_source_target.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition. A
path through a graph with no cycle goes through its nodes in the order
the graph was made in, so each path is one set of nodes holding 0 and
`n - 1`: the definition tries every such set, puts it in that order and
keeps it when each step is an edge. Its 1,600 cases have 2 to 10 nodes
in a random order, each edge going from earlier in it to later, in four
kinds of 400: few edges, many edges, every edge the order allows, and
some edges with 0 and `n - 1` anywhere in the order as long as 0 comes
before `n - 1`, so that edges may lead into 0 or away from `n - 1`. In
the first three 0 is first and `n - 1` last.

| | property |
|---|---|
| P1 | the paths, sorted, are the definition's |
| P2 | every path goes from 0 to `n - 1` along edges, and none comes twice |
| P3 | with every edge turned round and each node `v` renamed `n - 1 - v`, the paths are the old ones backwards and renamed |
| P4 | an edge from 0 straight to `n - 1` adds just the path `[0, n - 1]`, or nothing when the edge is there already |

It prints `1600 cases (32810 paths), 4 arms, 25600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the step back left out | P1 881, P2 881, P3 825, P4 1096 |
| M2 | ★: the path started without 0 | P1 1153, P2 1153, P3 1153, P4 1600 |
| M3 | ★: the walk ending at n - 2 | P1 1301, P2 1101, P3 1318, P4 1600 |
| M4 | queue: an answer recorded twice | P1 1153, P2 1153, P3 1153, P4 611 |
| M5 | queue: a path of two nodes not taken as an answer | P1 989, P3 989, P4 1600 |
| M6 | queue: the first path started at 1 | P1 1318, P2 1124, P3 1301, P4 1600 |
| M7 | memo: the node left off the front of its paths | P1 1153, P2 1153, P3 1153, P4 1600 |
| M8 | memo: the path from n - 1 left empty | P1 1153, P2 1153, P3 1153, P4 1600 |
| M9 | memo: a node's paths kept only at 0 | P1 1153, P3 1153, P4 1600 |
| M10 | stack: each new node's first next node skipped | P1 856, P3 876 |
| M11 | stack: every second next node skipped | P1 867, P3 798, P4 637 |
| M12 | stack: a path recorded after its last step is taken back | P1 1153, P2 1153, P3 1153, P4 1600 |

P1 and P3 kill all twelve. P4 kills eleven: skipping each new node's
first next node leaves node 0's own next nodes alone, so the edge it
adds from 0 is still found. P2 kills the eight that make a path that is
not one, or make one twice, and misses the four that only drop paths,
which P1 sees. 1,153 of the 1,600 cases have a path, and the mutations
that spoil every path fail all 1,153 in each of the first three
properties.

## Verification

Every arm prints the same output as `all_paths_source_target.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`5dee7bbc7c`, whose last compiler change is `e392d00704`. The runtime
archives were built after the last runtime change, `216d20e28a`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy checker refuses all four arms, the differential and
the bench program for the `*` on each node read from
`graph[node].iter()`, which it takes as a copied `i64` rather than a
reference. Copies without those `*`s print the same output under the
legacy interpreter (`karac run --interp`), the legacy JIT (`karac run`),
`karac build` and an auto-par build; for `show`'s use of `graph` to
print it after passing it to the arm they warn that `graph` is moved and
used again, and run it right regardless, as the differential does for
its graphs. The differential's copy prints its line under the legacy
interpreter, `karac build` and an auto-par build, and overflows the
stack under the legacy JIT. The bench program's copy also needs `graph`
written `ref Vec[Vec[i64]]` and each round's graph bound with `ref
graphs[r % 1024]` first, as legacy refuses the move out of an index and
a `ref` at a call; it then builds and prints the same line, and the
bench timing below is of it. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 1,024 graphs of
15 nodes, LeetCode's most, are made once: a random order of the nodes
with 0 first and 14 last, each edge from earlier in it to later taken
with a chance of 1 to 4 in 5. Each of 40,960 rounds lists every path of
the next graph, about 490 paths of 7.6 nodes on average, adding up the
paths, the nodes on them and a checksum of each path that does not
depend on their order. Every implementation prints `40960 graphs:
20164880 paths through 154049280 nodes, checksum 263348121`, the Kāra
program under `karac __mir-run` included (in 437 s). The C program keeps
each graph in fixed arrays of 15 and each path in its own allocation;
the others keep both in their growable arrays.

The bench measures a recursive walk that copies a short array into a
fresh allocation at each path's end and frees it after. Spot timings on
a shared 4-core container, eight runs of each compiled program, five of
them interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.68 to 1.83 s |
| Rust (`rustc -O`) | 1.80 to 2.30 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.83 to 1.99 s |
| Go | 2.35 to 2.64 s |
| Python | 19.77 to 19.87 s |
| Kāra (`karac build --mir`) | 1.83 to 2.21 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 7.1 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.95 s,
against C's 1.70, Rust's 1.90 (1.85 under overflow checks) and Go's
2.60. Under valgrind's cachegrind v2 runs 17.5 billion instructions and
2.84 billion branches, against C's 13.4 billion and 1.73 billion and
Rust's 14.5 billion and 2.09 billion, with 80 million branches
mispredicted against C's 67 million and Rust's 84 million. The legacy
build of the copy ran 1.56 to 1.93 s, a median of 1.62 s in the
interleaved runs, so v2 takes 1.20 times legacy. The comparison with C
and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
