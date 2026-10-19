# 802. Find Eventual Safe States

A directed graph of `n` nodes is given as `graph`, where `graph[i]`
lists the nodes that node `i` has an edge to. A node is a terminal node
if it has no edges out. A node is safe if every walk starting from it
leads to a terminal node, or to another safe node. Return all the safe
nodes in increasing order.

```
graph = [[1, 2], [2, 3], [5], [0], [5], [], []]   ->  [2, 4, 5, 6]
graph = [[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]  ->  [4]
```

**Constraints:** `1 <= n <= 10^4`, `0 <= graph[i].length <= n`, each
`graph[i]` is strictly increasing with values in `[0, n - 1]`, and the
graph has at most `4 · 10^4` edges. It may have edges from a node to
itself.

## Approaches

| file | mechanism |
|---|---|
| `eventual_safe_nodes.kara` ★ | depth first search in three colours from each node in turn: grey while a node's edges are followed, black once all are safe; meeting a grey node means a cycle, and every node on the way back up stays grey, kept for good as unsafe. O(n + e) |
| `eventual_safe_nodes_peel.kara` | count each node's edges out and turn every edge round; peel nodes off a queue starting from those with no edges out, counting down the nodes that point at each one; a node reaching zero is safe. O(n + e) |
| `eventual_safe_nodes_fixed.kara` | sweep the nodes over and over, marking a node safe once every edge out of it leads to a marked node, until a sweep marks nothing new. O(n · e) at worst |
| `eventual_safe_nodes_stack.kara` | the three-colour search with a stack of its own: each node on the search with how many of its edges have been tried; at a grey node the whole stack is left grey and emptied |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: LeetCode's two examples; a single
node with no edges, which is safe; a single node with an edge to itself,
which is not; a cycle of three with a way out to a terminal node, where
only the terminal node is safe; a chain of five, all safe; a graph whose
every node leads to a node with an edge to itself; and 300 random graphs
of up to 40 nodes, edges to themselves included, with how many safe
nodes they have and a checksum of them. `eventual_safe_nodes.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition. A
node is unsafe when some walk from it never ends, and a walk of `n`
steps on `n` nodes passes some node twice, so it has gone round a cycle
that it can go round for ever: a node is safe exactly when no walk of
`n` steps starts there. The definition works out, for `k` from 0 to `n`,
which nodes start a walk of `k` steps. Its 1,600 cases have 1 to 12
nodes and come in four kinds of 400: few edges; many; edges only forward
in a random order of the nodes, so that every node is safe; and few
edges with an edge to itself at a node or two.

| | property |
|---|---|
| P1 | the definition's nodes |
| P2 | in increasing order; every edge out of a node in the answer leads into it, and every node left out has an edge to another left out |
| P3 | with every node `v` renamed `n - 1 - v`, the answer renamed |
| P4 | a new node with no edges out and an edge to it from every node adds just the new node |

It prints `1600 cases (5561 safe), 4 arms, 25600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a grey node met again taken as safe | P1 1075, P3 1075, P4 1075 |
| M2 | ★: a node marked black before its edges are followed | P1 1075, P3 1075, P4 1075 |
| M3 | ★: an unsafe edge passed over rather than ending the search | P1 1075, P3 1075, P4 1075 |
| M4 | peel: a node with one edge out taken as an end | P1 913, P2 289, P3 913, P4 338 |
| M5 | peel: the edges not turned round | P1 756, P2 756, P3 756, P4 1190 |
| M6 | peel: each safe node counting down two edges | P1 904, P2 849, P3 904, P4 1533 |
| M7 | fixed: an edge from a node to itself ignored | P1 699, P3 699, P4 699 |
| M8 | fixed: a single sweep | P1 561, P2 561, P3 594, P4 1190 |
| M9 | fixed: a node with no edges out never marked | P1 1190, P2 1190, P3 1190, P4 1600 |
| M10 | stack: a black node met taken as a cycle | P1 605, P2 605, P3 573, P4 975 |
| M11 | stack: at a cycle only the top of the stack dropped | P1 570, P2 570, P3 544, P4 570 |
| M12 | stack: the last edge out of a node never tried | P1 943, P2 271, P3 940 |

P1 kills all twelve. The three ★ edits fail the same 1,075 cases, all
those with an unsafe node, and pass P2: each makes every node safe,
which leaves no node out and so meets P2's two rules. P2 holds for any
set of nodes that holds every terminal node and has no edge leaving it,
so it sees only the edits that put a node in the answer with an edge out
of it or leave out a node with every edge inside it: all three peel and
stack edits, and two of the three fixed ones. It misses M7, which
ignores an edge from a node to itself and so takes such a node and the
nodes leading only to it as safe, a set with no edge leaving it. P3 sees
every edit, and P4 all but M12: in P4's graph the last edge out of every
old node is the one to the new node, so an arm that never tries a last
edge skips just the added edges and gets that answer right.

## Verification

Every arm prints the same output as `eventual_safe_nodes.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`b95ac9a0c5`, whose last compiler change is `e6d52d2c4b`. The runtime
archives were built after the last runtime change, `216d20e28a`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy compiler refuses the four arms under all its lanes at
the harness's `text_list(graph[i])`, as a move out of an index, legacy
taking a bare parameter as owned rather than borrowed. Copies with the
graph and list parameters written `ref` and `graph[i]` bound by `ref`
first print the same output under the legacy interpreter (`karac run
--interp`), the legacy JIT (`karac run`), `karac build` and an auto-par
build. The differential prints its line under all four unchanged, with a
warning that `graph` is used after a move. Legacy refuses the bench
program the same way at `eventual_safe_nodes(graphs[r % 16])`; a copy
with `ref` parameters and the graph bound by `ref` first builds and
prints the same line, and the bench timing below is of it. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 16 graphs of
10,000 nodes, LeetCode's most, are made once. Each node has 0 to 4 edges
out, nearly all to one of the 50 nodes after it, and one edge in 1,000
back to one of the 50 before it, which makes a cycle there; about two
thirds of the nodes come out safe. Each of 4,000 rounds finds the safe
nodes of the next graph. Every implementation prints `4000 rounds of
10000 nodes: 25796250 safe nodes in all, checksum 593711483`, the Kāra
program under `karac __mir-run` included (in 206 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.50 to 1.75 s |
| Rust (`rustc -O`) | 1.79 to 1.99 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.81 to 2.23 s |
| Go | 2.48 to 2.77 s |
| Python | 15.83 to 17.44 s |
| Kāra (`karac build --mir`) | 1.92 to 2.60 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 4.7 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.95 s,
against C's 1.65, Rust's 1.90 (1.88 under overflow checks) and Go's
2.66. Under valgrind's cachegrind v2 runs 5.77 billion instructions and
1.11 billion branches, against Rust's 4.83 billion and 592 million and
C's 3.68 billion and 656 million. The legacy build of the copy ran 1.73
to 2.25 s, a median of 1.88 s in the interleaved runs, with 4.48 billion
instructions and 926 million branches, so v2 takes 1.04 times legacy.
All four mispredict 71 to 73 million branches, which is likely the
search's turns at the random edges; that is inferred, not read from the
assembly. The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
