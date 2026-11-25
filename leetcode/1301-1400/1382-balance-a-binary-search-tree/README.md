# 1382. Balance a Binary Search Tree

Given the `root` of a binary search tree, return a balanced binary
search tree with the same node values. If there is more than one answer,
return any of them.

A binary search tree is balanced if the depth of the two subtrees of
every node never differs by more than `1`.

```
root = [1,null,2,null,3,null,4,null,null]  ->  [2,1,3,null,null,null,4]
root = [2,1,3]                             ->  [2,1,3]
```

**Constraints:** the number of nodes in the tree is in the range `[1,
10^4]`, and `1 <= Node.val <= 10^5`.

Each arm is `fn balance_bst(root: TreeNode) -> TreeNode` over the
harness's `shared struct TreeNode { mut val: i32, mut left:
Option[TreeNode], mut right: Option[TreeNode] }`, which has LeetCode's
`TreeNode::new` as `TreeNode.new`.

## Approaches

| file | mechanism |
|---|---|
| `balance_bst.kara` ★ | the values read off in order, then a new tree built with the middle value at the root and each half built the same way beneath it. O(n) |
| `balance_bst_relink.kara` | the nodes themselves gathered in order, with a stack rather than recursion, and linked up again the same way. No node is made. O(n) |
| `balance_bst_dsw.kara` | Day, Stout and Warren's: the tree turned into a vine, a chain down the right, by rotating each left child up; then the vine folded into a tree by rounds of left rotations of every other node, the first round just enough to leave a count one less than a power of two. In place, O(n) time and O(1) space |
| `balance_bst_avl.kara` | the values read off in order and put one by one into an AVL tree, which rotates wherever a node's two sides come to differ by two, then copied into `TreeNode`s. O(n log n) |
| `balance_bst_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Option<Rc<RefCell<TreeNode>>>` parameters, the values read through `.borrow()`, the middle of `l..=r` taken as `l + (r - l) / 2` on `i32`s, `TreeNode::new` filled in and wrapped in `Rc::new(RefCell::new(..))`, and `Self::` for the recursion), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, four more properties |

Any balanced tree of the values is an answer, and the arms give
different ones: the ★ arm puts the upper of two middles at the root, the
Rust solution the lower, and the fold and the AVL tree shapes of their
own. So each case prints the answer's height when the answer holds the
input's values in the same order and is balanced, and -1 otherwise.
Every arm prints the same 3 lines: LeetCode's two examples, one node, a
chain of 7 down the left, a zigzag of 6, and a tree already balanced (`3
2 1 3 3 3`); the constraints' most, 10^4 nodes, as a chain up the right
and as one down the left (`chains of 10000 nodes: heights 14 14`); and
2000 random search trees of 1 to 300 different values up to 10^5, put in
at random, hung rising, hung falling, and hung from both ends in turn
(`2000 random trees: 2000 balanced, heights 14697 in all, checksum
817329345`). Every arm's answer is as low as a tree of its values can
be, though the statement asks only for balance; for the AVL arm that
holds because its values go in rising, which Python confirms for every
count up to 10^4. `balance_bst.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean as first written. The Rust
solution takes one round of 53 fixes by `karac fix`'s count, from 26
errors: the `use std::cell::RefCell;` and `use std::rc::Rc;` lines
deleted, `struct Solution;` to `struct Solution {}`, each
`Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, `&[i32]` to
`Slice[i32]`, `&mut Vec<i32>` to `mut ref Vec[i32]`, each `&` and `&mut`
on an argument dropped or made `mut`, `Vec::new()` and `TreeNode::new`
to `Vec.new()` and `TreeNode.new`, `Rc::new(RefCell::new(node))` to
`node`, `let mut node` to `let node`, since a `shared struct`'s handle
writes its `mut` fields without one, the `let n = n.borrow();` line
deleted, and `Self::` to `Solution.`. Its output matches on the first
run. The harness's first `TreeNode` had no `new`, and the one error left
after the fixes was `TreeNode.new` not found; LeetCode's Rust gives
`TreeNode` that function, so the harness does too.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a binary search tree is one where each node's value is
greater than every value to its left and less than every one to its
right, and balanced is each node's two sides measured afresh and found
to differ by at most one. LeetCode's two examples and 2000 trees of 1 to
40 different values from 1 to 100, in five kinds of 400: put in at
random; hung rising; hung falling; hung from both ends in turn; and put
in from the middle out, already balanced. Every case is drawn before any
arm answers, and every arm is given a tree of its own, since two of them
rebuild the tree they are given.

| | property |
|---|---|
| P1 | the statement read literally: a binary search tree of the same values |
| P2 | the statement read literally: balanced |
| P3 | no taller than its values need be, as every arm here promises |
| P4 | every value raised by 1000: the same shape, each value raised by 1000 |
| P5 | the answer balanced again: the same values, balanced, and no taller |
| P6 | as tall as the ★ arm's answer |

All 60,060 checks pass on every arm: `2002 trees: checksum 845675545,
60060 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, drawing the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the root a third of the way along each run, not in its middle | P2 815, P3 1510, P5 815, P6 6040 |
| M2 | ★: each value read before its left side | P1 1537, P5 1886 |
| M3 | relink: each node's left side cut off | P1 1953, P2 1711, P3 1770, P5 1953, P6 1770 |
| M4 | relink: the last node of each run at its root | P2 1903, P3 1903, P5 1903, P6 1903 |
| M5 | DSW: the first round of rotations, the one that leaves a power of two less one, left out | P2 1528, P3 1528, P5 1528, P6 1528 |
| M6 | DSW: a right rotation drops the left child's right side | P1 1059, P3 930, P5 1818, P6 930 |
| M7 | AVL: a node's height taken from its lower side | P2 1903, P3 1903, P5 1903, P6 1903 |
| M8 | AVL: a left rotation leaves the lowered node's height as it was | P2 1607, P3 1607, P5 1607, P6 1607 |
| M9 | solution: the first value of each run at its root | P2 1903, P3 1903, P5 1903, P6 1903 |
| M10 | solution: each value read after its right side | P1 1549, P5 1907 |

P5 kills all ten, P3 and P6 eight, P2 seven, P1 four, and P4 none.
Balancing the answer again (P5) catches every edit: an edit that loses
or misorders values loses or misorders them again, and one that leaves a
tree unbalanced leaves it so again. The edits that read the values out
of order (M2, M10) or lose some (M3, M6) build trees as low and balanced
as the true arms, so only the literal reading (P1) and P5 see them, and
M2 and M10 escape P6 as well. M4, M7 and M9 fail the same counts in
three arms: each turns its answer into a chain, down the left for M4 and
down the right for the others, which is balanced only for one or two
values. Raising every value by 1000 (P4) kills none: every arm, and
every edit, compares values and never reads them as numbers, so the
shape it gives cannot change.

## Benchmarks

The bench builds 10 search trees of 10^4 different values up to 10^5,
the constraints' most, once, each put in at random. Then 500 rounds,
each balancing one tree, drawn from the checksum so far, with the ★ arm,
walking down the balanced tree by drawn turns, and keeping it in the old
one's place. Every implementation prints `500 rounds over 10 trees of
10000 nodes: checksum 421988138`. The work is a walk of 10^4 nodes, 10^4
new ones, and the old tree let go, a round. The Rust tree is
`Rc<RefCell<TreeNode>>`, as LeetCode's Rust tree problems have it, since
a Kāra `shared struct` is reference counted too; C frees the tree a
round replaces, and Go leaves it to its collector.

BENCHTAB
