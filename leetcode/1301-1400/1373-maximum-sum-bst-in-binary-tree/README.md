# 1373. Maximum Sum BST in Binary Tree

Given a binary tree `root`, return the maximum sum of all keys of any
sub-tree which is also a Binary Search Tree (BST).

Assume a BST is defined as follows:

- The left subtree of a node contains only nodes with keys less than
  the node's key.
- The right subtree of a node contains only nodes with keys greater
  than the node's key.
- Both the left and right subtrees must also be binary search trees.

```
root = [1,4,3,2,4,2,5,null,null,null,null,null,null,4,6]  ->  20
root = [4,3,null,1,2]                                     ->  2
root = [-4,-2,-5]                                         ->  0
```

**Constraints:** the tree has 1 to 4 * 10^4 nodes, each valued from
-4 * 10^4 to 4 * 10^4.

Each arm is `fn max_sum_bst(root: Option[TreeNode]) -> i32`, over
`shared struct` nodes.

## Approaches

| file | mechanism |
|---|---|
| `max_sum_bst.kara` ★ | one walk up from the leaves: each subtree reports whether it is a search tree, its smallest and largest key, and its sum, and a node heads a search tree when both children do and its key lies strictly between the left's largest and the right's smallest. O(n), as deep as the tree |
| `max_sum_bst_bounds.kara` | every node checked afresh as the head of a search tree, by a walk that keeps the open interval each key must lie in, and the subtree summed when it passes. O(n²) in the worst case |
| `max_sum_bst_inorder.kara` | one in-order walk lists the keys, each subtree a contiguous run whose bounds are recorded as it finishes; a subtree is a search tree exactly when its run strictly increases, which one backward pass of how far each increase reaches answers for every run, and prefix sums give its sum. O(n) |
| `max_sum_bst_order.kara` | the ★ arm's summaries without recursion: the nodes listed parents first with their parent's place and side, then the list read backwards, so every subtree is summed before its parent. O(n) |
| `max_sum_bst_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn dfs(node: &Option<Rc<RefCell<TreeNode>>>, ans: &mut i32) -> (bool, i32, i32, i32)` nested in the method, `i32::MAX` and `i32::MIN` for the empty tree, `let n = n.borrow();`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, two more
(`[2,1,3]` and `[5,4,8,3,null,6,3]`), and a chain of 10^4 nodes valued
1 to 10^4, each the right child of the one before (`20 2 0 6 7
50005000`); and 2000 random trees of 1 to 300 nodes valued from -10 to
10 or -10^4 to 10^4, half with each node hung on a random empty child
place and half search trees with up to 3 keys then changed, folded into
a checksum (`2000 random trees: sums total 90465435, checksum
861051424`). `max_sum_bst.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`, the chain taking
the recursive arms 10^4 calls deep.

The Mend loop: the ★ and order arms check clean as first written; the
bounds and inorder arms take one round of 1 fix each, an `as i64` on a
key that widens to `i64` by itself. The Rust solution takes one round
of 38 fixes by `karac fix`'s count, from 19 parse errors: the two `use`
lines deleted, `struct Solution;` to `struct Solution {}`,
`Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, the `&` on the
tree dropped and `&mut i32` to `mut ref i32`, `i32::MAX` to `i32.MAX`,
`&&` to `and`, each `&n.left` argument to `n.left` and `&mut ans` to
`mut ans`, `let n = n.borrow();` deleted, and the nested `fn dfs`
lifted to the top level. Every arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: for every node, the keys of its left subtree and of its
right subtree collected, all compared with its own, and its children
checked the same way down to the leaves; every node that passes has its
subtree's keys summed, and the answer is the largest sum, or 0 for the
empty tree. It checks the five examples, 1500 random trees of 1 to 12
nodes and 500 of 1 to 40, valued from -3 to 3, -10 to 10 or -10^4 to
10^4, half hung at random and half search trees with a few keys
changed; the narrow range makes equal keys, which no search tree may
hold, common.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the tree hung as the left child of a new root below every key, and as the right child of one above every key, the same sum |
| P3 | every key doubled, the sum doubled |
| P4 | every key shifted up until all are positive, a sum never smaller and at least 1 |
| P5 | at least 0 and every leaf's key, at most the sum of the positive keys |
| P6 | the ★ arm's sum |

All 60,150 checks pass on every arm: `2005 cases: checksum 309982007,
60150 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, collecting every subtree's
keys the same way, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks. One first edit was replaced: the ★ arm's search
tree taking its smallest key from its left subtree alone failed as the
bounds arm's right subtree bounded by the ancestors only did, but for
P6; both let a right subtree hold a key below the node above it.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal key allowed on the left | P1 32, P6 128 |
| M2 | ★: a node's own key not summed | P1 1591, P4 2005, P5 1516, P6 6364 |
| M3 | bounds: the right subtree bounded by the ancestors only | P1 326, P2 363, P6 326 |
| M4 | bounds: right subtrees never visited | P1 1274, P2 548, P4 538, P5 1168, P6 1274 |
| M5 | inorder: a node's key after its right subtree | P1 552, P2 127, P6 552 |
| M6 | inorder: an equal neighbour continuing a run | P1 76, P6 76 |
| M7 | order: a child's side read the wrong way | P1 818, P2 109, P6 818 |
| M8 | order: a search tree's largest key its root's | P1 10, P6 10 |
| M9 | solution: an equal key allowed on the right | P1 45, P6 45 |
| M10 | solution: the right subtree's keys not summed | P1 403, P6 403 |

P1 and P6 kill all ten, P2 four, P4 and P5 two each, and P3 none. A new
root above the tree (P2) catches the edits that read the right side
wrongly: the right subtree bounded by the ancestors only (M3), which
takes the root above every key for the head of a search tree with the
whole tree on its right; right subtrees never visited (M4), which then
never sees the tree at all; a key listed after its right subtree (M5);
and the sides swapped (M7). The shift and the bounds (P4, P5) catch the
two edits that lose whole sums, a node's own key (M2) and every right
subtree (M4), so that a leaf alone no longer counts. Doubling the keys
(P3) catches nothing: it keeps their order and doubles every sum, and
each edit's wrong answer doubles with it. The edits that let an equal
key through (M1, M6, M9) or misjudge a largest key (M8) are caught only
by the literal reading, on the narrow-range trees where equal keys are
common.

## Benchmarks

The bench builds 4 search trees of 4 * 10^4 nodes, the constraints'
most, keys from -4 * 10^4 to 4 * 10^4 put in one by one, a key already
there skipped, once; then makes 300 rounds, each giving one node of one
tree a new key, both drawn from the checksum so far, which may break
the order there, and finding that tree's largest search tree with the ★
arm. Every implementation prints `300 rounds over 4 trees of 40000
nodes: checksum 601163210`. The work is the recursive walk over 4 *
10^4 nodes, the same in every language; C and Go use plain pointers,
Rust LeetCode's own `Rc<RefCell<TreeNode>>`.

BENCHTAB
