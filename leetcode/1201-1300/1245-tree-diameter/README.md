# 1245. Tree Diameter

You are given an undirected tree of `n` nodes labeled `0` to `n - 1`,
as an array `edges` where `edges[i] = [a, b]` is an edge between `a` and
`b`. Return *the number of edges in the longest path in that tree*, its
diameter.

```
edges = [[0, 1], [0, 2]]                          ->  2   (1 - 0 - 2)
edges = [[0, 1], [1, 2], [2, 3], [1, 4], [4, 5]]  ->  4   (3 - 2 - 1 - 4 - 5)
```

**Constraints:** `n == edges.length + 1`; `1 <= n <= 10^4`;
`0 <= a, b < n`; `a != b`; the edges form a tree.

The arms are `fn tree_diameter(edges: Vec[Vec[i64]]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `tree_diameter.kara` ★ | two breadth-first searches over an adjacency list with a `VecDeque`: the node farthest from node 0 is one end of a longest path, and the farthest distance from it is the diameter |
| `tree_diameter_dfs.kara` | one recursive depth-first search from node 0 returning each node's height, a `mut ref` best updated with the sum of each node's two tallest children |
| `tree_diameter_stack.kara` | the same heights without recursion: an explicit stack records each node's parent and the order it was reached, and the order walked in reverse puts every child before its parent, with each node's two tallest children in two `Vec`s |
| `tree_diameter_peel.kara` | peeling leaves: each round takes off every current leaf by degree count, down to a centre of one or two nodes; the diameter is twice the rounds, plus one for a centre of two |
| `tree_diameter_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![vec![]; n]`, `usize` nodes, a `fn dfs` nested in the method with `&mut i32`, `usize::MAX` for no parent), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, four more properties |

Every arm prints the same 3 lines: LeetCode's two examples; the total of
the diameters and a checksum of them for 1000 random trees of 1 to 300
nodes (`total 32025, checksum 700085867`); and four trees of 10000
nodes, the constraints' top: a path, and one random tree of each shape.
A random tree hangs each node after the first from an earlier one,
anywhere, from one of the last three (a long stringy tree), or from one
of the first four (a bushy one), and then shuffles the labels.
`tree_diameter.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac run` and `karac build`,
and under the AddressSanitizer build. The path of 10000 nodes is a
recursion 10000 calls deep in the two recursive arms, which all four
builds run.

The Mend loop: the four Kāra arms checked clean as first written. The
solution arm takes one round of fixes, 24 by `karac fix`'s count, and
then checks clean: `struct Solution;` to `struct Solution {}`, `Vec<..>`
to `Vec[..]`, the nested `fn dfs` moved above the `impl` (Kāra has no
nested items, and a nested `fn` captures nothing, so it means the same
at the top level), `&Vec<Vec<usize>>` to a bare parameter, `&mut i32` to
`mut ref i32`, `let (mut d1, mut d2)` to `let mut (d1, d2)`, `for &v in
&graph[u]` to `for v in ref graph[u]`, `vec![vec![]; n]` to
`Vec.filled(n, Vec.new())`, `usize::MAX` to `usize.MAX`, and the `&`
and `&mut` on the arguments to none and `mut`.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms, renamed, and the
statement read literally: from every node, a breadth-first search over
the edge list itself, no adjacency built, and the longest distance any
of them reaches. 2000 random trees of 1 to 60 nodes, a third of each
shape.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the nodes renamed by a random permutation give the same diameter |
| P3 | the edges listed in reverse, each one turned round, give the same diameter |
| P4 | at most `n - 1`, and exactly `n - 1` when no node has more than two neighbours, a path |
| P5 | one more leaf, hung from a random node, adds at most one |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 trees: checksum 375765722,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the second search from node 0 again, not from the far end | P1 1404, P2 1391, P4 37, P6 5616 |
| S2 | ★: a node at distance 0, the start, counted as unvisited | P1 29, P2 8, P3 10, P4 27, P5 33, P6 116 |
| D1 | recursive: a taller child replaces the tallest without moving it to second | P1 295, P2 443, P3 1044, P4 5, P5 28, P6 295 |
| D2 | recursive: the best path a node's height, not its two children joined | P1 1404, P2 1391, P4 37, P6 1404 |
| T1 | stack: the order walked forwards, parents before children | P1 1969, P4 99, P6 1969 |
| T2 | stack: a parent's height taken from the child's second-tallest | P1 1702, P2 535, P4 65, P6 1702 |
| P1 | peel: the extra edge of a two-node centre left out | P1 1067, P4 54, P5 318, P6 1067 |
| P2 | peel: the rounds stopped at four nodes left | P1 259, P4 13, P5 49, P6 259 |
| L1 | solution: each edge down counted twice | P1 1969, P4 851, P5 619, P6 1969 |
| L2 | solution: the best path overwritten by each node's, not kept | P1 720, P2 918, P6 720 |

All ten are caught, every one by P1, the statement read literally, and
by P6, which fails on the other four arms too when the ★ arm is the one
mutated (S1, S2). S1 and D2 fail the same checks in the same numbers:
both give the farthest any node is from node 0, the height of the tree
rooted there. P2, the nodes renamed, catches every mutation whose answer
depends on which node is 0 or on the order of the adjacency lists (S1,
S2, D1, D2, T2, L2). P3, the edges reversed, catches the two whose
answer depends on the order children are met (S2, D1). P4 catches nine;
P5, one more leaf, catches the five that get a longest path's length
wrong by a fixed amount (S2, D1, P1, P2, L1). A first P2, the rounds run
while more than one node is left instead of two, survived: it is
equivalent, since two adjacent nodes left are both leaves and one more
round takes both, and twice the extra round less one is the one edge
the formula adds for them.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (two breadth-first searches over an adjacency list) on 100 random
trees of 10000 nodes built once, each asked 5 times; every diameter
folded into a checksum. Every program prints `5 rounds of 100 trees of
10000 nodes: checksum 773053661`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.407 to 0.478 s | 0.426 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.408 to 0.500 s | 0.441 s |
| Rust (`rustc -O`) | 0.412 to 0.472 s | 0.419 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.413 to 0.438 s | 0.423 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.408 to 0.492 s | 0.423 s |
| C (`clang -O3`) | 0.154 to 0.191 s | 0.163 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.151 to 0.193 s | 0.153 s |
| Go | 0.562 to 0.655 s | 0.579 s |
| Python | 4.135 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.423 s
against 0.441 s), and the two ranges overlap. Kāra takes about 2.7x C's
time (0.441 s against 0.163 s); Kāra is about 24% ahead of Go (0.441 s
against 0.579 s). Python takes about 9x Kāra's time. No profile was
taken.
