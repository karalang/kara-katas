# 1372. Longest ZigZag Path in a Binary Tree

You are given the `root` of a binary tree.

A ZigZag path for a binary tree is defined as follows:

- Choose any node in the binary tree and a direction (right or left).
- If the current direction is right, move to the right child of the
  current node; otherwise, move to the left child.
- Change the direction from right to left or from left to right.
- Repeat the second and third steps until you can't move in the tree.

Zigzag length is defined as the number of nodes visited - 1. (A single
node has a length of 0.)

Return the longest ZigZag path contained in that tree.

```
root = [1,null,1,1,1,null,null,1,1,null,1,null,null,null,1]  ->  3
root = [1,1,1,null,1,null,null,1,1,null,1]                  ->  4
root = [1]                                                  ->  0
```

**Constraints:** the tree has 1 to 5 * 10^4 nodes, each valued from 1
to 100.

Each arm is `fn longest_zig_zag(root: Option[TreeNode]) -> i32`, over
`shared struct` nodes.

## Approaches

| file | mechanism |
|---|---|
| `longest_zig_zag.kara` ★ | one walk up from the leaves: each node reports the longest zigzag that starts at it going left and the longest going right, each one more than its child's longest going the other way; the best of all is the answer. O(n), as deep as the tree |
| `longest_zig_zag_topdown.kara` | one walk down from the root carrying the length of the zigzag that arrives at each node and the side it came from; a step to the other side extends it, a step to the same side starts afresh at 1. O(n), as deep as the tree |
| `longest_zig_zag_queue.kara` | the topdown walk breadth first, a `VecDeque` of (node, arrived from the left, length) triples. O(n) |
| `longest_zig_zag_order.kara` | the ★ arm's lengths without recursion: the nodes listed parents first with their parent's place and side, then the list read backwards, so every node is done before its parent and hands its lengths up. O(n) |
| `longest_zig_zag_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn dfs(node: &Option<Rc<RefCell<TreeNode>>>, is_left: bool, len: i32, ans: &mut i32)` nested in the method, `let n = n.borrow();`, called twice from the root), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples and a
zigzag of 10^4 nodes, each the left child of the one before and then
the right, by turns (`3 4 0 9999`); and 2000 random trees of 1 to 300
nodes, each node hung on a random empty child place, folded into a
checksum (`2000 random trees: lengths total 13178, checksum
968462040`). `longest_zig_zag.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`, the zigzag taking
the recursive arms 10^4 calls deep.

The Mend loop: the four Kāra arms check clean as first written. The
Rust solution takes one round of 39 fixes by `karac fix`'s count, from
18 errors: the two `use` lines deleted, `struct Solution;` to `struct
Solution {}`, `Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`,
the `&` on the tree dropped and `&mut i32` to `mut ref i32`, each `&n.left`
argument to `n.left` and `&mut ans` to `mut ans`, `let n = n.borrow();`
deleted, and the nested `fn dfs` lifted to the top level. Every arm
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: from every node, in both directions, the path walked
child by child, switching sides each step, as far as it goes, and the
longest of those. It checks the examples, 1500 random trees of 1 to 12
nodes and 500 of 1 to 200; each case also names a node from which to
look for an empty place for P4's new leaf.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the tree mirrored, the same length |
| P3 | the tree hung under a new root, at most 1 longer and never shorter |
| P4 | one leaf more, at most 1 longer and never shorter |
| P5 | no longer than the tree is tall, and at least 1 when there are two nodes |
| P6 | the ★ arm's length |

The literal reading walks a cursor down from each node, `for start in
nodes.iter() { let mut at = start; .. at = child; }`, and that loop,
written so, passes `karac check` and then stops every lane with invalid
MIR: `at` is a `ref TreeNode`, and the child handle the walk takes is
let through as a borrow it is not (B-2026-11-25-22). Until it is fixed,
the results below come from a copy whose one line reads `let mut at:
TreeNode = start;`: all 60,090 checks pass on every arm, `2003 cases:
checksum 853740259, 60090 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`. Python, with the ★
arm's recursion, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks. Two first edits were replaced: the ★ arm's left
step continued by the child's left failed as the queue arm's left
child taken as arriving from the right did, but for P6; and the order
arm's sides read the wrong way survived, since it computes the mirror
image, whose longest zigzag is the same.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node with no left child counted as going left 1 | P1 1268, P2 1487, P4 36, P5 441, P6 5072 |
| M2 | ★: only paths going left first counted | P1 762, P2 1487, P3 548, P5 92, P6 3048 |
| M3 | topdown: a step left after a left extends | P1 977, P2 1120, P6 977 |
| M4 | topdown: the root's right subtree skipped | P1 799, P2 1573, P3 725, P5 271, P6 799 |
| M5 | queue: a step right after a right extends | P1 974, P2 1120, P6 974 |
| M6 | queue: a left child taken as arriving from the right | P1 1098, P2 1186, P6 1098 |
| M7 | order: a left step counted twice | P1 1781, P2 805, P3 805, P4 292, P5 703, P6 1781 |
| M8 | order: the root's lengths never counted | P1 987, P5 175, P6 987 |
| M9 | solution: each length one short | P1 1873, P5 291, P6 1873 |
| M10 | solution: a step right after a left not counted | P1 1253, P2 682, P6 1253 |

P1 and P6 kill all ten, P2 eight, P5 six, P3 three and P4 two. Mirroring
the tree (P2) catches every edit that treats left and right differently,
which is all but the two that are blind to side: the root left out (M8)
and every length one short (M9). The height bound (P5) catches the edits
that overcount past it (M1, M7) or come up short of 1 on a tree of two
nodes (M2, M4, M8, M9). A new root above the tree (P3) catches the edits
whose answer falls, or grows by more than 1, when the whole tree becomes
a left subtree: only left-first paths (M2), the root's right subtree
skipped (M4), and a left step counted twice (M7). A new leaf (P4)
catches only the overcounting edits (M1, M7), whose answers jump by more
than 1.

## Benchmarks

The bench builds 20 trees of 5 * 10^4 nodes, the constraints' most,
each node hung on a random empty child place, once; then makes 300
rounds, each hanging one more leaf on one tree, on a place drawn from
the checksum so far, and finding that tree's longest zigzag with the ★
arm. Every implementation prints `300 rounds over 20 trees of 50000
nodes: checksum 619590004`. The work is the recursive walk over 5 *
10^4 nodes, the same in every language; C and Go use plain pointers,
Rust LeetCode's own `Rc<RefCell<TreeNode>>`.

BENCHTAB
