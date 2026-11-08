# 1522. Diameter of N-Ary Tree

Given the root of an N-ary tree, return the length of its diameter: the
number of edges on the longest path between any two nodes. The path may
or may not pass through the root.

```
root = [1,null,3,2,4,null,5,6]           ->  3
root = [1,null,2,null,3,4,null,5,null,6] ->  4
root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
                                         ->  7
```

The tree is given in LeetCode's level-order form: the root, a null, then
each node's children followed by a null, in level order.

**Constraints:** the depth is at most 1000; `1 <= n <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `diameter.kara` ★ | a depth-first walk returns each node's height, the edges down to its deepest leaf. The longest path that turns at a node goes down through its two highest children, so the walk keeps the top two and the best sum. O(n) |
| `diameter_order.kara` | without recursion: the nodes are listed parents before children, then taken in reverse, so every height is final before it is passed up; each node keeps its top two children's heights. O(n) |
| `diameter_bfs.kara` | two breadth-first searches over the tree numbered into an undirected adjacency list: the node farthest from any start is one end of a longest path, and the node farthest from it is the other. O(n) |
| `diameter_iter.kara` | the ★ arm with iterator adapters: the children's heights by `map`, folded into the top two by `fold` |
| `differential.kara` | the four arms against the statement read literally, six properties |

LeetCode offers no Rust template for this problem, so there is no Rust
arm.

Every arm prints the same 8 lines: LeetCode's three examples and a single
node, then checksums of the diameters of 3000 random trees of 1 to 10
nodes, 300 of 1 to 300, 300 of 1 to 300 hung deep (each node's parent one
of the 3 before it), and 3 of 1 to 10000 (parents within 30).
`diameter.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for every two nodes, the edges between them, counted by walking
the deeper one up until they meet, and the most of them. It checks 3000
trees of 1 to 10 nodes, each node after the first the child of a random
earlier one, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every node's children reversed leave the answer |
| P3 | the tree hung from a random node instead leaves the answer |
| P4 | the answer is at least the root's height, at most twice it, and at most the number of nodes less one |
| P5 | a new root above the old one changes the answer only to the old root's height plus one, when that is longer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 34682948, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Ten are killed, each the
same way under both backends; two survive, and both are equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the old highest not moved to second | P1 264, P2 910, P3 252, P6 264 |
| M3 | ★: the best path taken as the height alone | P1 1973, P3 1512, P6 1973 |
| M4 | order: nodes taken parents first | P1 2686, P4 2686, P5 3000, P6 2686 |
| M5 | order: second highest updated only when above the highest | P1 950, P2 1347, P3 942, P6 950 |
| M6 | order: the path through a node passed up as its height | P1 1352, P3 881, P4 349, P5 2214, P6 1352 |
| M7 | bfs: the second search from the root again | P1 1973, P3 1512, P6 1973 |
| M8 | bfs: edges only from parent to child | P1 2686, P4 2686, P5 3000, P6 2686 |
| M9 | bfs: the queue popped from the back | P1 577, P2 1138, P3 308, P4 120, P5 1151, P6 577 |
| M10 | iter: a new highest keeps the old second | P1 264, P2 910, P3 252, P6 264 |
| M11 | iter: second never raised | P1 1539, P2 1347, P3 1302, P6 1539 |

The survivors: `>=` for `>` in the ★ and iterator arms' test against the
highest (M2, M12), since a child as high as the highest becomes the
highest and the old one the second, the same two numbers.

## Benchmarks

The bench builds 1000 random trees of 1 to 2000 nodes once (each node's
parent one of the 1 to 64 before it) and answers each 20 times by the ★
arm, in all five languages. Rust holds the nodes as `Rc<Node>`, as Kāra's
`shared struct` is; Go as pointers; C as one array of nodes per tree, each
with an array of child pointers. Every implementation prints `20 passes
over 1000 trees of up to 2000 nodes: diameters sum to 3066240, checksum
903629712`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `38553609c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.555 s |
| Go | 0.706 s |
| Rust (`rustc -O`) | 1.177 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.183 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.184 s |
| Kāra (`karac build`) | 1.255 s |
| Python | 5.72 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (1.20 s and 1.24 s on one run).

Kāra is 1.00x Rust under overflow checks by median. Not traced. The walk
does little arithmetic per node, so the time is likely the pointer chase
through about a million nodes; C's nodes sit in one array per tree and
Go's come from its bump allocator, while Rust's and Kāra's are separate
`malloc` blocks.

## Verification

All four arms print the same output as `diameter.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change.

## Writing it

All four arms were written in Kāra. The breadth-first arm's first draft
named its queue `Deque`, and `karac check` said only `undefined name
'Deque'`, with no pointer to `VecDeque`, though it points `HashMap` at
`Map` and a typo like `VecDequ` at `VecDeque`. That is kara
`B-2026-11-08-59`. With `VecDeque`, `karac fix` had nothing to change on
any arm.
