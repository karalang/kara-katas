# 872. Leaf-Similar Trees

Consider all the leaves of a binary tree, from left to right order: the
values of those leaves form a leaf value sequence. Two binary trees are
considered leaf-similar if their leaf value sequence is the same. Return
`true` if and only if the two given trees with head nodes `root1` and
`root2` are leaf-similar.

```
root1 = [3,5,1,6,2,9,8,null,null,7,4], root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]  ->  true
root1 = [1,2,3], root2 = [1,3,2]                                                                 ->  false
```

**Constraints:** the number of nodes in each tree is in the range
`[1, 200]`, and both trees have values in the range `[0, 200]`.

## Approaches

| file | mechanism |
|---|---|
| `leaf_similar_trees.kara` ★ | the leaves collected by recursion: a depth-first walk that goes left before right meets the leaves from left to right; each tree's walk pushes its leaves into a `Vec`, and the two `Vec`s are compared. O(n1 + n2) |
| `leaf_similar_trees_stack.kara` | the same walk with a stack: a `Vec` of nodes still to visit, the right child pushed before the left so the left comes off first. O(n1 + n2) |
| `leaf_similar_trees_lazy.kara` | the two sequences compared as they are walked: one stack per tree, and `next_leaf` pops nodes until it reaches its tree's next leaf. The walk stops at the first pair of leaves that differs, or when one tree runs out before the other, without storing either sequence. O(n1 + n2) time, O(height) space |
| `leaf_similar_trees_inorder.kara` | an in-order walk (left subtree, node, right subtree), which also lists the leaves from left to right, since a leaf has nothing on either side; a stack holds the nodes whose left subtree is being visited. O(n1 + n2) |
| `leaf_similar_trees_text.kara` | the sequences written out: each tree's leaves written into a `String` with a comma after every value, so that `[1, 23]` and `[12, 3]` read differently, and the two strings compared. O(n1 + n2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more (single nodes with equal and with different values; a root with one
child against a lone leaf; a left leaf against the same value as a right
leaf; leaves at different depths; a tree with one more leaf; leaves
`[12, 3]` against `[1, 23]`, which agree digit by digit; and LeetCode's
extreme values, 0 and 200); 3,000 random pairs of up to 12 nodes with
values below 4, half of them built leaf-similar, 1,527 leaf-similar in
all; and 200 pairs of 200 nodes, LeetCode's largest, with values up to
200: 100 built leaf-similar, 50 built so and then one leaf changed, and
50 drawn independently, with a checksum. `leaf_similar_trees.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every leaf with its path from the root, `L` for a left step
and `R` for a right one; no leaf's path is a prefix of another's, so
sorting the paths as words with `L` before `R` puts the leaves in order
from left to right, and the trees are leaf-similar when the values in
that order are equal. It checks 1,900 pairs of trees: 1,500 of up to 10
nodes with values below 3, so that pairs often match by chance; 200 of up
to 120 nodes with values up to 200; and 200 pairs whose leaves spell the
same digits cut into one- and two-digit numbers in two different ways.
In every group some trees are built on another's leaves, sometimes with a
leaf under a node that has one child. The ★ arm finds 683 pairs
leaf-similar.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the order of the two trees does not matter |
| P3 | a tree is leaf-similar to itself and to a random tree built on its leaves |
| P4 | both trees mirrored give the same answer |
| P5 | when the two trees are leaf-similar, changing one leaf of the second makes them not |
| P6 | a tree and its mirror are leaf-similar exactly when its leaves read the same both ways |

It prints `1900 pairs of trees, 683 leaf-similar, 50915 checks over 5
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node with one child counted as a leaf | P1 600, P3 1490, P5 93, P6 447 |
| M2 | ★: left subtrees never visited | P1 679, P3 848, P4 838, P5 510, P6 592 |
| M3 | ★: only the numbers of leaves compared | P1 289, P5 972, P6 1098 |
| M4 | stack: the right child pushed twice | P1 517, P3 1442, P4 194, P6 554 |
| M5 | stack: a node with no left child counted as a leaf | P1 523, P3 1391, P4 226, P6 586 |
| M6 | stack: the first tree compared with itself | P1 1217, P5 1900, P6 1098 |
| M7 | lazy: one tree running out counted as a match | P1 181, P4 256, P5 52 |
| M8 | lazy: leaves compared with `<` | P1 78, P2 160, P5 384 |
| M9 | lazy: right children never visited | P1 663, P3 814, P4 838, P5 499, P6 592 |
| M10 | inorder: the walk never moves to a right subtree | P1 663, P3 814, P4 838, P5 499, P6 592 |
| M11 | inorder: a node with only a left child counted as a leaf | P1 503, P3 1393, P4 226, P6 586 |
| M12 | inorder: a leaf reached with the stack empty left out | P1 359, P3 848, P4 405, P5 201, P6 376 |
| M13 | text: no separator after a value | P1 159, P4 156 |
| M14 | text: the left subtree written twice, the right never | P1 724, P3 1362, P4 589, P5 348, P6 637 |
| M15 | text: only the numbers of leaves compared | P1 274, P5 811, P6 1098 |

P1 kills all fifteen. M9 and M10 are one fault in two arms, the right
subtrees never walked, and fail the same pairs. M13 survived the first
run, which had no digit-split pairs: without a separator `[12, 3]` and
`[1, 23]` both read `123`, and only pairs built to spell the same digits
meet that, so the third group of inputs was added for it, where P1 and
P4 catch it. Two reversal mutants tried first (the leaves of the stack
arm and of the in-order arm collected right to left) were equivalent:
both trees' sequences reverse together, so equal stays equal and unequal
stays unequal. They were replaced with M4 and M12.

## Verification

Every arm prints the same output as `leaf_similar_trees.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara
`e903d5b111`. Under `karac __mir-run` every arm and the differential
take 1 to 2 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends refuse all five arms and the bench program at
a `*` on a `for` element, saying the value is not a reference, where v2
yields a reference. They run the differential with no failure, but on
other trees: it prints 686 pairs leaf-similar and 50,930 checks under the
legacy interpreter, and 684 and 50,920 under the legacy JIT, `karac
build` and auto-par, where v2 prints 683 and 50,915 on every lane. The
same generators in the arms' harness print the same output on v2 as in
Python, so the v2 trees are the ones the generators describe. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 2,000 pairs of
random 200-node trees with values up to 200, LeetCode's largest; in half
of the pairs the second tree is a random tree built on the first one's
leaves, and in the other half it is drawn independently. It takes a
checksum of every second tree's leaves, so that each language is seen to
build the same trees, then compares every pair 50 times. The nodes are a
`shared struct` in Kāra, `Option<Rc<RefCell<TreeNode>>>` in Rust,
pointers in Go, objects in Python and `malloc`'d structs in C, and every
language collects the leaves into a growable array and compares the
arrays. Every implementation prints `100000 comparisons of 2000 pairs:
50000 leaf-similar, leaf checksum 134995963`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.84 to 0.93 s | 0.87 s |
| Rust (`rustc -O`) | 1.44 to 1.55 s | 1.49 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.39 to 1.54 s | 1.49 s |
| Go | 1.10 to 1.22 s | 1.17 s |
| Python | 8.1 s | |
| Kāra (`karac build --mir`) | 1.10 to 1.27 s | 1.16 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 871's does. Legacy refuses the bench program
(above), so it has no lane here.

v2 takes 0.78 times Rust's median time under overflow checks and 1.3
times C's. Under valgrind's cachegrind C runs 1.06 billion instructions,
Rust with overflow checks 2.17 billion and v2 1.76 billion, and all three
mispredict about 33 million branches, most likely the leaf test, whose
outcome a random tree makes unpredictable. Rust's extra instructions are
most likely `RefCell`'s borrow checks and `Rc`'s counts on every child it
follows (inferred, not profiled). The 4,000 trees hold 800,000 nodes,
well past the caches, so following the children is likely the larger
cost in every language (inferred from the timings, not traced). The
comparison with C and Rust waits until after M4.
