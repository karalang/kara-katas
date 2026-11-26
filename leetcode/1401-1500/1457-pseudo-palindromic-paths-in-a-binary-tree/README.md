# 1457. Pseudo-Palindromic Paths in a Binary Tree

Given a binary tree where node values are digits from 1 to 9. A path in
the binary tree is said to be pseudo-palindromic if at least one
permutation of the node values in the path is a palindrome. Return the
number of pseudo-palindromic paths going from the root node to leaf
nodes.

```
root = [2,3,1,3,1,null,1]                        ->  2
root = [2,1,1,1,3,null,null,null,null,null,1]    ->  1
root = [9]                                       ->  1
```

**Constraints:** the number of nodes in the tree is in the range `[1,
10^5]`, and `1 <= Node.val <= 9`.

The arms are `fn pseudo_palindromic_paths(root: Option[TreeNode]) ->
i32`, over `shared struct TreeNode { mut val: i32, mut left:
Option[TreeNode], mut right: Option[TreeNode] }`.

## Approaches

| file | mechanism |
|---|---|
| `pseudo_palindromic_paths.kara` ★ | a walk down by recursion carrying an `i32` mask with bit v set when the value v is on the path an odd number of times, each node's bit flipped by `^`: at a leaf the path rearranges into a palindrome when at most one bit is set, `seen & (seen - 1) == 0`. O(n), as deep as the tree |
| `pseudo_palindromic_paths_counts.kara` | backtracking over an `Array[i32, 10]` of the values' counts on the path, passed down by `mut ref`, each node counted on the way down and taken off on the way back; at a leaf the odd counts are counted by `iter().filter(..).count()`. O(9n) |
| `pseudo_palindromic_paths_stack.kara` | the walk without recursion, each node on a `Vec` used as a stack with the mask of the path to it, itself included, `while let` taking each pair off and a `match` on the pair of children telling a leaf, `(None, None)`, from the rest. O(n) |
| `pseudo_palindromic_paths_queue.kara` | a breadth-first walk from a `VecDeque[(Option[TreeNode], u32)]`, each child queued, present or not, with its parent's mask, `let .. else` passing over a missing one; a leaf counts through `(seen.count_ones() <= 1) as i32`. O(n) |
| `pseudo_palindromic_paths_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn dfs` nested in the method over `&Option<Rc<RefCell<TreeNode>>>`, the node read through `n.borrow()` inside `if let`, and the mask's lowest bit cleared to test for at most one odd value), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and four
more, a chain of 10^4 nodes all valued 1 and one cycling through 1 to 9,
and a full tree of 2^16 - 1 nodes by level cycling through 1 to 9 and
with all one value (`2 1 1 1 0 372 32768`); the constraints' most, 10^5
nodes with values from 1 to 9, each hung on a random empty place (`10^5
nodes: 593`); and 2000 random trees of 1 to 300 nodes with values from 1
to top, top from 1 to 9 (`2000 random trees: 35354 paths, checksum
606032499`). `pseudo_palindromic_paths.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ and stack arms check clean as first written. The
counts arm declared its parameter `counts: mut ref [i32; 10]`, Rust's
array type, which `karac check` refuses and `karac fix` writes
`Array[i32, 10]`, 2 fixes by its count. The queue arm added a `bool as
i32` to `let mut found = 0;` and returned it in the `i32` count, which
`karac check` refuses, saying `found` is an `i64` because its literal
kept the default, and `karac fix` declares it `found: i32`, 1 fix. The
Rust solution takes one round of 22 fixes by `karac fix`'s count: the
two `use` lines deleted, `Option<Rc<RefCell<TreeNode>>>` to
`Option[TreeNode]`, the `&` on `dfs`'s parameter and on each argument
dropped, the nested `fn dfs` moved above the `impl`, `let n =
n.borrow();` deleted, and `&&` to `and`. Every arm's output matches on
the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every path from the root to a leaf, kept when a rearrangement
of its values reads the same both ways, the rearrangement made (the
values sorted, each run of equal ones paired off into the first half, at
most one left for the middle) and checked to read the same backwards and
to hold the path's values, while there are at most 300 nodes. LeetCode's
examples, six edge cases (one node, two nodes of one value and of two,
three nodes with the children equal and not, and four nodes all one
value), the two chains and the two full trees above, the constraints'
most, and 1989 random trees drawn as the harness draws them.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 300 nodes |
| P2 | each node's children swapped gives the same count |
| P3 | the values renamed, v to v % 9 + 1, gives the same count |
| P4 | two new nodes valued 9 above the root give the same count |
| P5 | from 0 to the number of leaves, and every leaf when the tree has one value |
| P6 | the ★ arm's answer |

All 60,065 checks pass on every arm: `2003 cases: checksum 388016042,
60065 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by an explicit
stack counting each path's values in a `Counter`, gives the same
checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a value's bit set on the way down, never cleared, so the mask says seen rather than odd | P1 1612, P4 344, P6 6456 |
| M2 | ★: a node with one child taken for a leaf | P1 1687, P4 1723, P5 214, P6 6756 |
| M3 | counts: a path with one value there an odd number of times refused | P1 1827, P5 235, P6 1828 |
| M4 | counts: a node never taken off the path on the way back up | P1 1468, P2 1481, P6 1470 |
| M5 | stack: the right child's own value left out of its mask | P1 1567, P2 1582, P4 1627, P6 1569 |
| M6 | stack: the root's value left out of the mask | P1 1470, P4 1851, P6 1472 |
| M7 | queue: a path with every value there an even number of times refused | P1 1306, P5 228, P6 1310 |
| M8 | queue: the right child queued with the mask above its parent | P1 1569, P2 1550, P4 1927, P6 1571 |
| M9 | solution: the walk started with the bit for value 0 already set | P1 1827, P5 235, P6 1828 |
| M10 | solution: the test for one bit at most written with `mask + 1` | P1 1827, P5 235, P6 1828 |

## Benchmarks

The bench builds 50 trees of 10^4 nodes with values from 1 to 9, once
from its own generator, as kata 1448's does: half with each node hung on
a random empty place, half filled level by level with gaps; then makes
50 passes, each setting one node of every tree from the checksum so far,
so no answer carries over, answering it with the ★ arm and folding the
count plus the pass into the checksum. The nodes are `shared struct`s in
Kāra and LeetCode's own `Rc<RefCell<TreeNode>>` in Rust, each read
through `borrow()`. Every implementation prints `50 passes over 50 trees
of 10^4: checksum 38787108`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.48 s against Rust's 0.67 s (0.73 s with
overflow checks on), C's 0.37 s and Go's 0.40 s; Python takes 5.7 s.
