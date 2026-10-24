# 958. Check Completeness of a Binary Tree

Given the `root` of a binary tree, determine if it is a *complete binary
tree*. In a **complete binary tree**, every level, except possibly the
last, is completely filled, and all nodes in the last level are as far
left as possible. It can have between `1` and `2^h` nodes inclusive at
the last level `h`.

```
root = [1,2,3,4,5,6]          ->  true
root = [1,2,3,4,5,null,7]     ->  false
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 100]`; `1 <= Node.val <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `is_complete_tree.kara` ★ | the first gap: the tree walked in level order with the missing children queued as gaps. In a complete tree every node comes before every gap, so a node after a gap means the tree is not complete. O(n) time, O(width) space |
| `is_complete_tree_index.kara` | heap numbers: the root 1 and the children of node i 2i and 2i + 1. The complete tree of n nodes is the one numbered 1 to n, and a tree's numbers are distinct, so a tree of n nodes is complete exactly when no number passes n. The walk stops at the first number past n, so the numbers stay small however deep the tree. O(n) |
| `is_complete_tree_heights.kara` | heights, from the bottom up: a tree is complete when it is empty, or its left subtree is perfect and its right complete with the same height, or its left complete and its right perfect and one shorter; perfect when both subtrees are perfect with the same height. Each subtree reports its height and both flags. O(n) time, O(height) stack |
| `is_complete_tree_levels.kara` | the statement level by level, each node with its place in its level, the children of place p at places 2p and 2p + 1: every level but the last must hold all 2^d places, checked before going down, so the places stay below 2^7; the last level's nodes must sit at places 0, 1, 2, ... in turn. O(n) |
| `is_complete_tree_kinds.kara` | node kinds in level order: nodes with two children, then at most one node with only a left child, then leaves, and never a node with only a right child. After the first node with fewer than two children, every node must be a leaf. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 18 lines: LeetCode's two examples and nine
more (one node, a left child, a right child, seven nodes, gaps in the
middle and at the start of the last level, eight nodes, a right child
alone on the last level, and a node below a level left unfilled); for
300 random trees of 1 to 12 nodes, 1,919 nodes in all, how many are
complete, by kind, and a checksum; one tree of each kind made from
LeetCode's largest size, 100 nodes; and a path of 100 left children. A tree of each
kind is the complete tree of n nodes; the same with its last node moved
to a random empty place, with a random leaf taken off, or with the
children of a random node swapped; or a random tree.
`is_complete_tree.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each node's depth and its place in its level, every level
above the deepest holding 2^d nodes and the deepest level's nodes at
places 0 to k - 1. It checks 3,200 random trees of the same five kinds:
3,000 of up to 8 nodes against the statement, and 200 of up to 100
nodes against the other properties; 22,938 nodes in all, 1,831 trees
complete.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | complete exactly when the tree has the shape of the complete tree of as many nodes |
| P3 | the tree and its mirror both complete exactly when the tree is perfect, 2^h - 1 nodes for height h |
| P4 | complete exactly when the left subtree is perfect and the right complete with the same height, or the left complete and the right perfect and one shorter, the arm asked about the subtrees |
| P5 | complete exactly when a node can be put at heap number n + 1 and the tree is complete with it |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 trees of 22938 nodes, 1831 complete, checksum
734603046, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(2.4 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-five edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a gap not remembered | P1 1239, P2 1369, P3 2305, P4 1149, P5 824, P6 1369 |
| M2 | ★: the right child queued before the left | P1 1123, P2 1188, P4 780, P5 1549, P6 1188 |
| M3 | ★: after a gap, only a node with a left child refused | P1 1114, P2 1208, P3 1910, P4 992, P5 723, P6 1208 |
| M4 | index: the number n itself refused | P1 1761, P2 1831, P3 895, P4 442, P6 1831 |
| M5 | index: the right child numbered 2i + 2 | P1 929, P2 995, P3 453, P4 568, P5 654, P6 995 |
| M6 | index: one number more than the nodes allowed | P1 613, P2 658, P3 706, P4 488, P5 812, P6 658 |
| M7 | heights: the right subtree required perfect in the first case | P1 168, P2 215, P4 178, P5 363, P6 215 |
| M8 | heights: equal heights in the second case | P1 872, P2 936, P4 400, P5 1289, P6 936 |
| M9 | heights: perfect without equal heights | P1 207, P2 252, P3 266, P4 233, P5 411, P6 252 |
| M10 | levels: places to the left of their turn allowed on the last level | P1 657, P2 699, P3 1635, P4 514, P5 475, P6 699 |
| M11 | levels: the widths of the upper levels not checked | P1 219, P2 241, P4 211, P5 264, P6 241 |
| M12 | levels: the right child at place 2p + 2 | P1 792, P2 853, P3 453, P4 432, P5 989, P6 853 |
| M13 | kinds: a right child alone taken as a left one | P1 289, P2 292, P3 386, P4 163, P5 292, P6 292 |
| M14 | kinds: a left child alone not ending the full nodes | P1 245, P2 266, P4 234, P5 362, P6 266 |
| M15 | kinds: a leaf not ending the full nodes | P1 156, P2 171, P3 221, P4 144, P5 174, P6 171 |

P1, P2, P4 and P6 kill all fifteen, P5 fourteen (all but M4) and P3
nine (M1, M3, M5, M6, M9, M10, M12, M13, M15).

Twenty other edits were tried and set aside. Four failed exactly the
same checks as a kept one: heights leaving the node out of the height,
as M1; heights calling the empty tree not perfect, as M4; index
numbering the left child 2i + 1, as M8; and ★ not queueing a missing
right child, as M14. Fourteen were sound but beyond three an arm: ★
walking with a stack and letting a second gap undo the first; index
numbering the root 0, not checking the right subtree and counting only
left subtrees; heights requiring the left subtree perfect in the second
case; levels growing the width by one, not checking the last level's
first place, putting the left child at place 2p + 1 and starting the
width at 2; and kinds allowing a full node or a left child alone after a
leaf, walking with a stack and queueing the right child first.

Two were equivalent. ★ starting the gap flag as whether the root is
empty: the root is never empty, and an empty one is a gap either way.
And heights taking the height from the left subtree alone: in a
complete tree the leftmost path reaches the deepest level, so the
leftmost depth is the height, and the arm trusts a height only when the
subtree is already perfect or complete.

## Verification

Every arm prints the same output as `is_complete_tree.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `46c2e7477d`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` heights and
kinds take 0.18 s, index 0.21 s, levels 0.23 s and ★ 0.29 s, and the
differential 2.4 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 200 trees of up to 100 nodes once, of the five
kinds in turn. In each of 4,000 rounds it runs the ★ arm on every tree,
each round starting from a different one, and folds the answers into a
checksum. Every implementation prints `4000 rounds over 200 trees of up
to 100 nodes: 328000 complete, checksum 638599356`. Each call makes a
new queue of possibly missing children: `VecDeque` in Kāra and Rust, a
slice in Go, a `deque` in Python, and in C a ring of 256 pointers on the
stack, so C allocates nothing per call. The Rust tree is LeetCode's
`Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
`shared struct` is.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `46c2e7477d`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.095 to 0.138 s | 0.114 s |
| Rust (`rustc -O`) | 0.49 to 0.59 s | 0.50 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.46 to 0.74 s | 0.55 s |
| Go | 1.64 to 2.05 s | 1.95 s |
| Python | 8.4 s | |
| Kāra (`karac build --mir`) | 1.08 to 1.32 s | 1.21 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 74 times
C's.

v2 took 2.2 times Rust's median time under overflow checks and 11 times
C's. Under valgrind's cachegrind v2 ran 11.31 billion instructions and
1.65 billion branches with 19.1 million mispredicted, Rust with overflow
checks 6.82 billion, 945 million and 17.1 million, and C 1.35 billion,
282 million and 1.77 million. Of v2's instructions 1.75 billion were in
`karac_mir_deque_push` and 1.16 billion in `memcpy`: a queue that grows
after its head has moved round moved its elements into the new buffer
one at a time, with a `memcpy` call for each. That is kara
B-2026-10-24-14, fixed in kara `d34614d017` by copying the ring's two
runs in bulk. With the runtime built with and without the fix at kara
`dcb1e820c2`, with the same compiler, the bench took 0.81 to 0.91 s
against 1.07 to 1.19 s, and 8.92 billion instructions against 11.31
billion, about 1.6 times Rust under overflow checks.
