# 971. Flip Binary Tree To Match Preorder Traversal

You are given the `root` of a binary tree with `n` nodes, where each
node is uniquely assigned a value from `1` to `n`. You are also given a
sequence of `n` values `voyage`, which is the desired pre-order
traversal of the binary tree. Any node in the binary tree can be flipped
by swapping its left and right subtrees. Flip the smallest number of
nodes so that the pre-order traversal of the tree matches `voyage`.

Return a list of the values of all flipped nodes. You may return the
answer in any order. If it is impossible to flip the nodes in the tree
to make the pre-order traversal match `voyage`, return the list `[-1]`.

```
root = [1,2],   voyage = [2,1]    ->  [-1]
root = [1,2,3], voyage = [1,3,2]  ->  [1]
root = [1,2,3], voyage = [1,2,3]  ->  []
```

**Constraints:** the number of nodes in the tree is `n`;
`n == voyage.length`; `1 <= n <= 100`; `1 <= Node.val, voyage[i] <= n`;
all the values in the tree are unique, and all the values in `voyage`
are unique.

## Approaches

| file | mechanism |
|---|---|
| `flip_match_voyage.kara` ★ | one walk, flipping where the voyage says: walk the tree in preorder alongside the voyage. A node must be the voyage's next value, and its left child, if there is one, must come next; if the voyage names some other value there, the only hope is to flip the node and visit its right child first. Each flip is forced, so the walk finds the fewest, or a mismatch shows that none work. O(n) |
| `flip_match_voyage_stack.kara` | the same walk on an explicit stack: popping a node checks it against the voyage, then pushes its children so that the one the voyage names next is popped first, flipping the node when that is its right child |
| `flip_match_voyage_sizes.kara` | no shared cursor: a subtree occupies exactly its size's worth of the voyage, so a node at voyage index i has its first child at i + 1 and its second at i + 1 plus the first's size. The child whose value is `voyage[i + 1]` goes first, and the node flips when that is the right one. The sizes are counted once, keyed by value |
| `flip_match_voyage_rebuild.kara` | flip a copy, then compare: walk a copy of the tree, each node's voyage index found from subtree sizes, and swap the children of every node whose left child is not the value the voyage names next, checking nothing on the way; then read the copy's preorder and compare it with the voyage whole. O(n · height) |
| `flip_match_voyage_ranges.kara` | a stretch of the voyage for each subtree: a subtree must be one contiguous stretch starting with its root. A table gives each value's place in the voyage, so a node with two children splits its stretch at its second child's place, the child at the stretch's second place taking the part before. A node with one child hands it the rest, and a missing child's stretch must be empty |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples and seven
more (a single node, a lone right child, the complete tree of seven
read three ways, needing three flips, one flip and no flips possible,
a tree whose root has a lone child, and a path that no flip
reorders); for 300 random trees of 1 to
12 nodes, 1,944 in all, how many matched (188) with how many flips
(139), and a checksum of the answers; and three cases of 100 nodes,
LeetCode's largest: a random tree with a voyage that matches after 20
flips, the same voyage with its last two values swapped, and the
complete tree read as its mirror image, which needs all 49 nodes with
two children flipped. A random tree hangs each new node below the root,
going left or right at random down to the first empty place, with the
values in random order. Half the voyages are the tree's preorder with
each node's children taken in a random order, a quarter are those with
two values swapped, and a quarter are random orders. Each answer is
sorted before it is printed. `flip_match_voyage.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of nodes, fewest first, flipped in a copy of the
tree until the copy's preorder is the voyage. It checks 3,200 random
trees, with voyages made as above: 3,000 of up to 8 nodes against the
statement, and 200 of up to 100 nodes against the other properties;
22,898 nodes in all, 2,090 matched with 1,713 flips. Every arm's answer
is sorted before it is compared.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | an answer other than `[-1]` names nodes with two children, each once, and the tree with them flipped reads as the voyage |
| P3 | the mirror image of the tree needs exactly the other nodes with two children flipped, and `[-1]` stays `[-1]` |
| P4 | relabelling every value v as n + 1 - v, in the tree and the voyage, relabels the answer |
| P5 | the tree's own preorder needs no flip, and the preorder after flipping a random set of nodes with two children needs exactly that set |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 trees of 22898 nodes: 2090 matched with 1713 flips,
checksum 405980626, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (11.6 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run` with the same results; fifteen are kept, three to
each arm, and all fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node never checked against the voyage | P1 1020, P2 1110, P3 842, P6 1110 |
| M2 | ★: the flip test inverted | P1 1384, P2 267, P3 267, P5 2547, P6 1492 |
| M3 | ★: a flip recorded but the left child still visited first | P1 713, P3 823, P5 1430, P6 814 |
| M4 | stack: the right child first when no flip is needed | P1 713, P3 823, P5 2166, P6 813 |
| M5 | stack: a lone left child dropped | P1 437, P2 63, P3 57, P5 1089, P6 533 |
| M6 | stack: a mismatch skipped | P1 1020, P2 1110, P3 825, P6 1110 |
| M7 | sizes: every size one short | P1 1119, P5 2166, P6 1225 |
| M8 | sizes: a lone right child never checked | P1 62, P2 75, P3 101, P5 90, P6 75 |
| M9 | sizes: a node never checked against the voyage | P1 1020, P2 1110, P3 592, P6 1110 |
| M10 | rebuild: the right child's place counted past the right subtree | P1 371, P2 165, P3 376, P5 1033, P6 473 |
| M11 | rebuild: the tree itself flipped, not a copy | P1 713, P2 4048, P3 4481, P4 3256, P5 1430, P6 814 |
| M12 | rebuild: the copy a mirror image | P1 1119, P2 1225, P5 2166, P6 1225 |
| M13 | ranges: a lone left child given one place too few | P1 882, P5 1673, P6 985 |
| M14 | ranges: a flip never recorded | P1 713, P2 814, P3 1225, P5 1430, P6 814 |
| M15 | ranges: a lone right child starting at its parent's place | P1 1980, P5 3200, P6 2090 |

P1 and P6 kill all fifteen, P5 twelve (all but M1, M6 and M9), P3
eleven (all but M7, M12, M13 and M15), P2 ten (M1, M2, M5, M6, M8 to
M12, M14) and P4 one (M11). P5 misses the edits that only stop a
mismatch from being noticed, since every voyage it asks about matches.
P4 asks whether an answer depends on the values themselves, which no
edit here changes; it kills M11 only because that edit flips the
caller's tree in place, so every later call on the same tree, from any
arm, sees it flipped.

Fifteen other edits were tried and set aside. Seven failed exactly the
same checks as a kept one: sizes placing the second child one early, as
M4; sizes inverting the flip test, ranges putting every place one too
far, and rebuild testing the right child in place of the left and
reading the copy right child first, as M7; rebuild comparing only the
lengths, as M1; and rebuild recording a flip without making it, as M3.
Four were sound but beyond three an arm: ★ never recording a flip and
returning the flips so far on a mismatch, and stack never advancing in
the voyage and never recording a flip. Two were equivalent: rebuild
never flipping the node second from the end of the voyage, whose only
child is the last node, so a flip there could not make the copy match
anyway; and ranges letting a missing child take any stretch, because
the voyage is a permutation of the tree's n values and the stretches'
starts are n different places, so a longer stretch for a missing child
would leave a place no node starts at. Two crashed and were not
counted: sizes placing a flipped node's left child after the left
subtree, and sizes counting every size one too many; both read past
the end of the voyage.

## Verification

Every arm prints the same output as `flip_match_voyage.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.18 s (★) to 0.23 s (ranges), and the differential 11.6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 200 random trees of 100 nodes once, each with a
voyage that matches after some flips, and every fourth voyage with two
of its values swapped, so that most of those fail part way. In each of
1,000 rounds it runs the ★ arm on every tree, each round starting from a
different one, and folds every value returned, `-1` included, into a
checksum. Every implementation prints `1000 rounds over 200 trees of 100
nodes: 2819000 values, checksum 899431526`. The Rust tree is LeetCode's
`Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's `shared
struct` is, and each visit borrows its node's `RefCell`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.18 to 0.22 s | 0.20 s |
| Rust (`rustc -O`) | 0.31 to 0.45 s | 0.34 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.32 to 0.35 s | 0.35 s |
| Go | 0.28 to 0.32 s | 0.30 s |
| Python | 3.7 s | |
| Kāra (`karac build --mir`) | 0.28 to 0.35 s | 0.30 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 19 times
C's.

v2 took 0.86 times Rust's median time under overflow checks and 1.52
times C's. Under valgrind's cachegrind v2 ran 1.56 billion instructions
and 188 million branches with 18.6 million mispredicted, Rust with
overflow checks 1.69 billion, 189 million and 17.9 million, and C 865
million, 99 million and 17.4 million. All three mispredict about as
often: which child the voyage names next is close to a coin toss on
these trees.

