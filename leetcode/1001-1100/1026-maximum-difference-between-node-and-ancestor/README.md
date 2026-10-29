# 1026. Maximum Difference Between Node and Ancestor

Given the root of a binary tree, find the largest value `v` for which
there are different nodes `a` and `b` with `v = |a.val - b.val|` and `a`
an ancestor of `b`. A node `a` is an ancestor of `b` if a child of `a`
is `b`, or a child of `a` is an ancestor of `b`.

```
root = [8,3,10,1,6,null,14,null,null,4,7,13]  ->  7   (|8 - 1|)
root = [1,null,2,null,0,3]                    ->  3   (|0 - 3|)
```

**Constraints:** the tree has 2 to 5,000 nodes, each value from 0 to
100,000.

## Approaches

Along the path from the root to a node, the largest difference between
the node and an ancestor is with the least or the greatest value above
it. The node type is a `shared struct`, Kāra's reference-counted form,
as in kata 1022.

| file | mechanism |
|---|---|
| `max_ancestor_diff.kara` ★ | recursion: carry the least and greatest value on the path down; at a missing child the path is complete, and its greatest less its least is the best difference along it. O(n) |
| `max_ancestor_diff_stack.kara` | an explicit stack: depth first without recursion, each node pushed with the least and greatest value above it; a node popped is compared with both and pushes its children with the range widened by its value. O(n) |
| `max_ancestor_diff_bfs.kara` | level by level: breadth first over a `VecDeque` of nodes with their ancestors' range, each compared with both ends as it is taken off. O(n) |
| `max_ancestor_diff_bottom_up.kara` | bottom up: turn the question round, so each node is compared with the least and greatest value in the subtrees below it; a post-order recursion returns each subtree's range as a tuple and folds the node's differences into a `mut ref` best. O(n) |
| `max_ancestor_diff_path.kara` | every ancestor: the statement as written, keeping the values on the path from the root in a `Vec`, pushed on the way down and popped on the way back, and comparing every node with every one of them. O(n * height) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for seven trees in
LeetCode's level order (with -1 for a missing child), LeetCode's two
examples among them; for six groups of random trees (7 to 5,000 nodes,
with values below 2 to 100,000), the sum of the answers, the largest and
a checksum; and the answers for two chains of 5,000 nodes, one with
values rising by 20 and one zigzagging between low and high. A random
tree hangs each new node at the end of a random walk from the root.
`max_ancestor_diff.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: over every pair of different nodes `a` and `b`, test whether
`a` is an ancestor of `b` by the definition, searching down from `a`'s
children with `ref_eq`, and take the largest `|a.val - b.val|`. It
checks 2,495 trees: every shape of 1 to 7 nodes, each with three draws
of values below 4 (1,875), 600 random trees of 8 to 40 nodes and 20 of
300 to 2,000, with values below 10, 100, 1,000 or 100,000. The 2,475
trees of at most 40 nodes are searched in full. Each tree is also asked
with every value doubled and 3 added, with every value `v` turned into
`100000 - v`, mirrored, and hung below a new root of a random value.

| | property |
|---|---|
| P1 | the statement read literally, on the trees of at most 40 nodes |
| P2 | with every value doubled and 3 added, the answer doubles |
| P3 | with every value `v` turned into `100000 - v`, the answer does not change |
| P4 | the mirror image keeps every ancestor, and the answer |
| P5 | below a new root of value `r`, every node gains `r` as an ancestor, so the answer is the old one or `r`'s difference with the least or the greatest value in the tree, whichever is largest |
| P6 | each arm agrees with at least two of the other four |

The differential prints `2495 trees (2475 searched in full): checksum
793689375, 74750 checks over 5 arms: 0 failures` under `karac __mir-run`
(15 s) and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all fifteen
are killed, each fails the same checks under both, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a path's greatest value taken for its difference | P1 888, P2 2495, P3 2495, P5 593, P6 901 |
| M2 | ★: the least value never updated | P1 1749, P3 2353, P5 2434, P6 1768 |
| M3 | ★: right subtrees never searched | P1 1816, P4 2129, P5 1264, P6 1836 |
| M4 | stack: only the least ancestor compared | P1 663, P3 1354, P5 1739, P6 673 |
| M5 | stack: a right child's range not widened by its parent | P1 404, P4 821, P5 15, P6 409 |
| M6 | stack: the ancestors' range compared, not the node | P1 801, P5 427, P6 808 |
| M7 | bfs: only the least ancestor compared | P1 828, P3 1698, P5 2360, P6 838 |
| M8 | bfs: max for min in the least value | P1 675, P3 1354, P5 31, P6 681 |
| M9 | bfs: children's range not widened by their parent | P1 1054, P5 82, P6 1073 |
| M10 | bottom up: the last child's greatest value passed up | P1 342, P3 709, P4 170, P5 19, P6 348 |
| M11 | bottom up: a subtree's own range taken | P1 679, P5 2430, P6 692 |
| M12 | bottom up: the least value starting at 0 | P1 754, P2 2405, P3 2492, P5 594, P6 767 |
| M13 | path: values never popped | P1 450, P6 463 |
| M14 | path: a value pushed only after its subtrees | P1 2470, P5 2495, P6 2490 |
| M15 | path: the root never compared | P1 483, P5 2396, P6 484 |

P1 and P6 kill all fifteen, P5 fourteen, P3 seven, P4 three and P2 two.
Each of P2 to P4 sees one kind of edit. P2 sees the two whose answer
holds a value rather than a difference only, M1 answering a value and
M12 a value less 0, since a value doubled with 3 added is not doubled.
P3, which swaps the least and greatest values, sees the seven that
treat the two ends differently. P4 sees the three that treat the two
children differently. M13 compares each node with every node before it
in preorder, so it answers the spread of the whole tree, which all four
transformations keep in step; only the statement and the other arms see
it. M14 always answers 0, since the path is empty whenever a node is
compared with it. M9 compares each node with the root alone. The checks
draw a random number for every tree whatever the answers, so every
mutant sees the same trees and their counts can be compared.

Fifteen other edits were tried and set aside. Two change no answer: bfs
starting the root's greatest value at 0, since no value is below 0, and
bfs taking nodes off the back of its queue, since the order nodes are
taken in changes no node's ancestors. The other thirteen were killed
too, beyond three per arm. Seven fail exactly as a kept one: ★ and stack
starting the least value at 0, as M1; stack taking `min` for `max` in
the greatest value, as M4; bfs and path never reading right children,
as M3; path counting only larger descendants, as M7; and path comparing
each node only with the root, as M9. Stack and bottom up never reading
left children fail alike. And four fail on their own: ★ forgetting the
greatest value at each node, ★ taking `min` for `max` over the children,
bottom up comparing each node only with the least value below it, and
bottom up not passing the least value up.

## Verification

Every arm prints the same output as `max_ancestor_diff.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error; the differential prints its line under all three. `karac check
--output=json` reports no diagnostic for the five arms, the differential
and the bench program. `karac run` and a `karac build` binary print the
same output for every arm and the differential. The release build is
kara `56c60bdf7c`, with runtime archives rebuilt at `ce706dd131`, the
last commit before it to change the runtime. Under `karac __mir-run` the arms take
5.6 s (★) to 23.4 s (path).

Writing the differential turned up one diagnostic worth noting, and it
was right: `shape.bytes().collect()` is refused, since `bytes()` gives a
slice and iterator adaptors need an explicit `.iter()`; the diagnostic
says so, and the differential indexes the slice instead. No compiler gap
turned up.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench builds 200 random trees of 2 to 5,000 nodes (LeetCode's
sizes, 494,126 nodes in all), with values from 0 to 100,000, once in all
five languages and answers each tree 50 times with the ★ arm, folding
the answers into a sum and a checksum: about 25 million node visits,
each a recursive call. The Rust version uses
`Option<Rc<RefCell<TreeNode>>>`, LeetCode's Rust signature, walked by
reference with a `borrow()` per node, C a `malloc` per node and Go a
pointer per child. Every implementation prints `200 trees, 494126
nodes, 50 rounds: sum 988519550, checksum 310729528`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.335 to 0.486 s | 0.388 s |
| Rust (`rustc -O`) | 1.201 to 1.460 s | 1.292 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.104 to 1.560 s | 1.234 s |
| Go | 0.371 to 0.484 s | 0.393 s |
| Python | 8.5 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.761 to 0.956 s | 0.816 s |
| Kāra (`karac build`) | 0.609 to 0.953 s | 0.807 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 0.66 times Rust's median time under overflow checks and 2.10
times C's; C and Go ran level. Kāra's and Rust's nodes are
reference-counted and C's and Go's are plain pointers, but we did not
measure how much of either gap that accounts for.
