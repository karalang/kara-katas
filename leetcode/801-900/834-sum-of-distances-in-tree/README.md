# 834. Sum of Distances in Tree

There is an undirected, connected tree with `n` nodes labelled `0` to
`n - 1` and `n - 1` edges, given as a list `edges` where `edges[i] = [a,
b]` is an edge between nodes `a` and `b`. Return a list `answer` of
length `n` where `answer[i]` is the sum of the distances between node
`i` and every other node.

```
n = 6, edges = [[0,1],[0,2],[2,3],[2,4],[2,5]]  ->  [8,12,6,10,10,10]
n = 1, edges = []                               ->  [0]
n = 2, edges = [[1,0]]                          ->  [1,1]
```

**Constraints:** `1 <= n <= 3 * 10^4`, `edges.length == n - 1`, `0 <= a,
b < n`, `a != b`, and the edges form a tree.

## Approaches

Every arm finds node 0's sum or some root's sum from the subtree sizes,
then moves the root along each edge: stepping from a node to a neighbour
brings the neighbour's side, `size` nodes, one step closer and the other
`n - size` one step further, so the neighbour's answer is the node's
less `size` plus `n - size`. They differ in how they order the nodes.

| file | mechanism |
|---|---|
| `sum_of_distances_in_tree.kara` ★ | rerooting with a stack: one walk from node 0 on an explicit stack records parents and a visiting order, taken backwards for the sizes and distance sums and forwards for the answers. O(n) |
| `sum_of_distances_in_tree_recursive.kara` | rerooting by recursion: the same two passes as two depth-first recursions from node 0 passing `mut ref` tables, recursion as deep as the tree. O(n) |
| `sum_of_distances_in_tree_bfs.kara` | rerooting in breadth-first order: a `VecDeque` from node 0 lists the nodes level by level with parents and depths; node 0's answer is the sum of the depths, and the list backwards gives the sizes. O(n) |
| `sum_of_distances_in_tree_peel.kara` | peeling leaves: no adjacency lists, each node keeping its degree and the XOR of its neighbours; leaves are peeled one at a time into their one remaining neighbour, the last node left is the root, and the peeled nodes taken backwards get their answers. O(n) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 10 lines: LeetCode's three examples; a path of
5, a star of 5 with its centre at node 3, and a full binary tree of 7;
three trees of LeetCode's greatest size, 30,000 nodes (a path, a star
and a random tree in which each node hangs from one of the three before
it), each shown by its least and greatest answer and a checksum; and 300
random trees of 1 to 60 nodes with their total and a checksum.
`sum_of_distances_in_tree.py` mirrors the ★ arm and its output is
byte-identical.

The path of 30,000 nodes makes the recursive arm recurse 30,000 deep,
and it runs on every backend below.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: from every node a breadth-first search, its distances summed.
Its 1,600 cases come in four kinds of 400: trees of 1 to 6 nodes; trees
of up to 80 nodes of any shape; paths and near-paths of up to 80 nodes,
each node hanging from one of the one or two before it; and bushy trees
of up to 80 nodes, each node hanging from any before it, stars among
them. The labels are shuffled and each edge is given either way round.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the tree with every node renamed gives the same answers, renamed |
| P3 | every edge turned round, the list reversed, gives the same answer |
| P4 | across each edge `(a, b)`, `n` less the difference of the two answers is twice the number of nodes on `a`'s side, an even number between 2 and `2 (n - 1)` |
| P5 | every answer lies between `n - 1` and `n (n - 1) / 2` |

It prints `1600 cases, 32000 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a child's answer with the two sides swapped | P1 1450, P2 1222, P5 593 |
| M2 | ★: each child adding 1, not its size, to the distance sum | P1 1425, P2 1222, P5 1293 |
| M3 | ★: the sizes summed in visiting order, not reverse | P1 1425, P2 1287, P5 1425 |
| M4 | recursive: a child's answer set after its subtree is visited | P1 1425, P2 1332, P4 1307, P5 1425 |
| M5 | recursive: subtree sizes not added up | P1 1425, P2 1332, P5 603 |
| M6 | recursive: the root's answer left at 0 | P1 1522, P2 1222, P5 1522 |
| M7 | bfs: a step adding the rest without taking the subtree off | P1 1522, P2 1373, P4 1522, P5 794 |
| M8 | bfs: the sizes summed in queue order, not reverse | P1 1273, P2 1244, P5 602 |
| M9 | bfs: node 0 taken as unvisited again | P1 1522, P2 1373, P3 845, P4 1522, P5 1522 |
| M10 | peel: the peeling stopped one node early | P1 1522, P2 1243, P4 1254, P5 1522 |
| M11 | peel: node 0 taken as the root, not the node left | P1 845, P2 861, P5 845 |
| M12 | peel: a node made a leaf only when it has no neighbour left | P1 1356, P2 896, P4 982, P5 1356 |

P1 and P2 kill all twelve. P3, the edges turned round, kills only M9,
the one edit whose answer depends on the order of a node's neighbours:
node 0 is queued again from one of its children, which one depending on
that order. P4 asks only that each edge's step be one some split of the
tree could give, so it misses the edits that leave the sizes wrong but
between 1 and `n` (M3, M5, M8) or the root's sum alone wrong (M2, M6,
M11), and M1, which swaps the two sides of every step and so turns each
split into its mirror image. P5 kills every edit, but with as few as 593
failures where an answer stays within the bounds.

Two edits were left out. The ★ arm with its stack made a queue (taking
from the front) is an equivalent mutant: any order that visits a parent
before its children works, and it survived every case. Edits to one end
of an edge only (the adjacency or the degree of one end) made the arms
index out of range rather than answer wrongly, so they were replaced by
the edits above.

## Verification

Every arm prints the same output as `sum_of_distances_in_tree.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `cd64cc58b3`, and the runtime archives are
current with them. Under `karac __mir-run` each arm takes 1.0 to 1.3 s
and the differential 9.9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run most of this kata. `karac run --interp`,
`karac run`, `karac build` and an auto-parallel build print the same
output for the ★, breadth-first and peeling arms. The legacy interpreter
does not finish the recursive arm within 60 s: it prints the six small
trees and stalls at the 30,000-node path, which recurses 30,000 deep
(most likely the depth, not traced); the other three legacy backends run
it. `karac build` warns on the recursive arm and the differential that
`adj` is moved into the first recursion and used again, which v2's
borrowing parameters do not do, and refuses the bench program as moving
a tree out of `trees[round % count]`. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 16
trees once, each of LeetCode's greatest size, 30,000 nodes: node `v > 0`
hangs from one of the `reach` nodes before it, `reach` running from 2 to
2^16 over the trees, so they go from near-paths to bushy ones, with the
labels shuffled. Each of 320 rounds solves the next tree and reads one
answer. Every implementation prints `320 rounds of 16 trees: answers
total 9320117610, checksum 40400206`, the Kāra program under `karac
__mir-run` included, in 67 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and four of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.84 to 1.01 s |
| Rust (`rustc -O`) | 1.07 to 1.25 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.17 to 1.38 s |
| Go | 1.57 to 1.96 s |
| Python | 8.1 to 10.0 s |
| Kāra (`karac build --mir`) | 0.95 to 1.11 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.04 s, against C's
0.90, Rust's 1.24 (1.21 under overflow checks) and Go's 1.67: 1.16 times
C's time, 0.86 times Rust's under overflow checks and 0.62 times Go's.
Under valgrind's cachegrind C runs 5.5 billion instructions and 1.26
billion branches, Rust 6.0 and 1.23 billion and v2 6.3 and 1.49 billion,
with branch mispredictions at 1.3 to 1.4 percent in all three. The work
is a walk over 30,000 short adjacency lists and four passes over tables
of 30,000, about the same in each language, and v2 is within 16 percent
of C. Built for `x86-64-v3`, the target `karac build` uses, C takes 0.87
to 0.98 s and Rust with overflow checks 1.15 to 1.29 s, against v2's
1.01 to 1.27 s in the same five interleaved runs. Python takes about 9
s, about 10 times C's time. The comparison with C and Rust waits until
after M4.

## Compiler findings

None on v2: every arm, the differential and the bench program pass
`karac check` and run on both v2 backends as written.
