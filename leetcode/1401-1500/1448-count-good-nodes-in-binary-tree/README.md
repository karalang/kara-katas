# 1448. Count Good Nodes in Binary Tree

Given a binary tree `root`, a node X in the tree is named good if in the
path from root to X there are no nodes with a value greater than X.
Return the number of good nodes in the binary tree.

```
root = [3,1,4,3,null,1,5]  ->  4
root = [3,3,null,4,2]      ->  3
root = [1]                 ->  1
```

**Constraints:** the number of nodes in the binary tree is in the range
`[1, 10^5]`, and each node's value is between `[-10^4, 10^4]`.

The arms are `fn good_nodes(root: Option[TreeNode]) -> i32`, over
`shared struct TreeNode { mut val: i32, mut left: Option[TreeNode], mut
right: Option[TreeNode] }`.

## Approaches

| file | mechanism |
|---|---|
| `good_nodes.kara` ★ | a walk down by recursion from `i32.MIN`, carrying the largest value on the path above each node: the node is good when it is at least as large, `let .. else` returning 0 for a missing child. O(n), as deep as the tree |
| `good_nodes_stack.kara` | the walk without recursion, each node on a `Vec` used as a stack with the largest value on the path above it, `while let` taking each pair off. O(n) |
| `good_nodes_queue.kara` | a breadth-first walk from a `VecDeque`, each node queued with the largest value on the path to it, itself included, so a node is good when it equals that value; the two children through `for child in [node.left, node.right]`. O(n) |
| `good_nodes_counts.kara` | the values on the path from the root counted in a `SortedMap[i32, i64]`, each added on the way down through `entry(..).or_insert(0)` and taken off on the way back: a node is good unless `path.last()`, the largest value above it, is larger, by a `match` with a guard. O(n log h) |
| `good_nodes_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn dfs` nested in the method over `&Option<Rc<RefCell<TreeNode>>>`, the node read through `n.borrow()`, a `match` on the node, and `i32::MIN` to start), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and four
more, a chain of 10^4 nodes rising by 2 and one falling by 2, and a full
tree of 2^16 - 1 nodes by level with values falling and with all one
value (`4 3 1 10000 1 4 65535`); the constraints' most, 10^5 nodes with
values from -10^4 to 10^4, each hung on a random empty place (`10^5
nodes: 5084`); and 2000 random trees of 1 to 300 nodes with values from
-top to top, top from 0 to 100 (`2000 random trees: 48728 good nodes,
checksum 517786613`). `good_nodes.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the stack and queue arms check clean as first written.
The ★ and counts arms set `let good = if n.val >= high { 1 } else { 0
};`, and a `match` of `0` and `1` in the counts arm, and returned it in
the `i32` count, which `karac check` refuses, saying `good` is an `i64`
because its literal kept the default, and `karac fix` declares it `good:
i32`, 1 fix each. The Rust solution takes one round of 24 fixes by
`karac fix`'s count: the two `use` lines deleted, `struct Solution;` to
`struct Solution {}`, `Option<Rc<RefCell<TreeNode>>>` to
`Option[TreeNode]`, the `&` on `dfs`'s parameter and on each argument
dropped, the nested `fn dfs` moved above the `impl`, `let n =
n.borrow();` deleted, `let good` declared `good: i32`, and `i32::MIN` to
`i32.MIN`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every node with the values on the path from the root to it,
kept when none of them is greater than its own, while there are at most
300 nodes. LeetCode's examples, four edge cases (one node of a negative
value, and two nodes with the child smaller, larger and the same), the
two chains and the two full trees above, the constraints' most, and 1991
random trees drawn as the harness draws them.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 300 nodes |
| P2 | each node's children swapped gives the same count |
| P3 | every value 7 more gives the same count |
| P4 | a new root above with the tree's smallest value gives one more |
| P5 | from 1 to n, and n exactly when every child is at least its parent |
| P6 | the ★ arm's answer |

All 60,065 checks pass on every arm: `2003 cases: checksum 30295923,
60065 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by an explicit
stack, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a node as large as the largest above it not counted | P1 1372, P4 102, P5 22, P6 5500 |
| M2 | ★: no right subtree counted | P1 1940, P2 1236, P5 26, P6 7776 |
| M3 | stack: only the parent's value carried down, not the largest above | P1 1924, P6 1926 |
| M4 | stack: the root started above its own value | P1 1998, P4 497, P5 116, P6 2003 |
| M5 | queue: every node counted | P1 1963, P5 1966, P6 1966 |
| M6 | queue: each child queued with its own value, not the largest above | P1 1963, P5 1966, P6 1966 |
| M7 | counts: a node as large as the largest above it not counted | P1 1372, P4 102, P5 22, P6 1375 |
| M8 | counts: a value never taken off the path once its count is 0 | P1 1784, P2 1542, P5 3, P6 1785 |
| M9 | solution: the walk started at 0, not the smallest number | P1 999, P3 504, P4 1971, P5 9, P6 1002 |
| M10 | solution: the smallest value carried down, not the largest | P1 1963, P5 1966, P6 1966 |

## Benchmarks

The bench builds 50 trees of 10^4 nodes with values from 1 to 100, once
from its own generator, as kata 1302's does: half with each node hung on
a random empty place, half filled level by level with gaps; then makes
50 passes, each setting one node of every tree from the checksum so far,
so no answer carries over, answering it with the ★ arm and folding the
count plus the pass into the checksum. The nodes are `shared struct`s in
Kāra and LeetCode's own `Rc<RefCell<TreeNode>>` in Rust, each read
through `borrow()`. Every implementation prints `50 passes over 50 trees
of 10^4: checksum 627241740`.

BENCHTAB

Kāra is ahead of Rust here, measured by hand at 0.49 to 0.51 s against
Rust's 0.62 to 0.64 s (0.64 to 0.67 s with overflow checks on), and
level with Go's 0.45 to 0.51 s; C takes 0.33 s and Python 5.8 s.
