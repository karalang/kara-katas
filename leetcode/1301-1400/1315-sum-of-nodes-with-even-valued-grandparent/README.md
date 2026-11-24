# 1315. Sum of Nodes with Even-Valued Grandparent

Given the `root` of a binary tree, return the sum of values of nodes with
an **even-valued grandparent**. If there are no nodes with an
even-valued grandparent, return `0`.

A **grandparent** of a node is the parent of its parent if it exists.

```
root = [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]  ->  18
root = [1]                                          ->  0
```

**Constraints:** the number of nodes in the tree is in the range `[1,
10^4]`, `1 <= Node.val <= 100`.

The arms are `fn sum_even_grandparent(root: Option[TreeNode]) -> i32`,
with `TreeNode` a `shared struct`.

## Approaches

| file | mechanism |
|---|---|
| `sum_even_grandparent.kara` ★ | a recursive walk that hands each child its parent's and grandparent's values, 1 above the root, an odd stand-in for a node that is not there; a node counts when the grandparent it is handed is even. O(n), as deep as the tree |
| `sum_even_grandparent_grand.kara` | looked at from the other end: a breadth-first walk from a `VecDeque`, and every even node met adds up its own grandchildren, the children of its children. O(n) |
| `sum_even_grandparent_stack.kara` | the ★ arm's walk done by hand, each entry on a `Vec` used as a stack a node with its parent's and grandparent's values. O(n) |
| `sum_even_grandparent_parents.kara` | every node listed in breadth-first order beside the place of its parent in that list, -1 for the root; a node counts when its parent has a parent and that one's value is even. O(n) |
| `sum_even_grandparent_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn dfs(node: &Option<Rc<RefCell<TreeNode>>>, p: i32, gp: i32) -> i32` nested in the method, `let n = n.borrow();`, 1 handed down for a missing parent), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, a chain of
`10^4` nodes each the right child of the one before, every value even,
and a full tree of `2^13 - 1` nodes (`18 0 509802 206570`); then 2000
random trees of 1 to 300 nodes, each node hung on a random empty place,
with values from 1 to 100 (`2000 random trees: sums total 7491496,
checksum 843121609`). `sum_even_grandparent.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run` and `karac __mir-llvm-run`, the chain
taking the recursive arms `10^4` calls deep.

The Mend loop: the four Kāra arms checked clean as first written. The
Rust arm takes one round of 30 fixes by `karac fix`'s count, from 12
errors: its two `use` lines deleted, `struct Solution;` to `struct
Solution {}`, `Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, the
nested `fn dfs` moved out of the method to the top level, `&Option<..>`
to `Option[TreeNode]`, `let n = n.borrow();` dropped, since a `shared
struct`'s fields read directly, `let mut sum = 0` to `let mut sum: i32 =
0`, the calls' `&n.left` to `n.left`, and `::` to `.`. Its output matches
on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the tree kept as lists of values and child places, and for
every pair of nodes, a node's value added once for each node that has it
as a child of one of its children and is even. 2000 trees of 1 to 12
nodes, each new node hung on an empty child place chosen at random, in
four kinds, 500 each: values 1 to 4, so that even and odd mix; values up
to 100; values 1 to 4 with each node hung, three times in four, on one of
the two newest empty places, so that the trees run deep; and every value even but one in
four. Every tree and new root is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the tree mirrored: the same answer |
| P3 | every value raised by 2, which keeps its parity: the answer raised by 2 for every node with an even grandparent |
| P4 | a new root above the old one: the old root's children added when the new root is even |
| P5 | every value doubled, so that every grandparent is even: twice the sum of every node that has a grandparent |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 trees: checksum 238783253,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash, and no two fail the
same checks, so all ten are kept.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right child handed the two values the wrong way round | P1 1315, P2 1552, P3 849, P4 652, P5 1305, P6 5260 |
| M2 | ★: the missing parents above the root taken as even | P1 2000, P3 2000, P4 1826, P5 2000, P6 8000 |
| M3 | grandchildren: a right grandchild never added | P1 1191, P2 1344, P3 1191, P4 702, P5 1493, P6 1191 |
| M4 | grandchildren: the odd nodes' grandchildren added | P1 1596, P3 1468, P4 1843, P5 1648, P6 1596 |
| M5 | stack: a left child handed the wrong grandparent | P1 1123, P2 1366, P3 1009, P4 794, P5 1244, P6 1123 |
| M6 | stack: the parent's value tested, not the grandparent's | P1 1581, P3 1264, P4 887, P5 1843, P6 1581 |
| M7 | parent table: a right child given the next node's place as its parent | P1 1441, P2 1597, P3 1192, P4 702, P5 1402, P6 1441 |
| M8 | parent table: the root its own parent | P1 1116, P3 1116, P4 1512, P5 2000, P6 1116 |
| M9 | solution: only grandparents divisible by 4 | P1 1009, P3 1375, P4 460, P5 1249, P6 1009 |
| M10 | solution: the root's missing grandparent taken as 0 | P1 2000, P3 2000, P4 1736, P5 2000, P6 2000 |

P1, P3, P4, P5 and P6 kill all ten; P2 kills four. Mirroring the tree
(P2) swaps every left and right child, so it sees only the edits that
treat the two sides differently (M1, M3, M5, M7), and misses every edit
that gets a parity, a stand-in above the root or the root's own place
wrong on both sides alike. Raising every value by 2 (P3) keeps each
parity and so each counted node, adding 2 for each, and catches every
edit through the sum it then gets wrong. A new root (P4) moves the old
root's children down a level and makes them grandchildren, so it reaches
the edits about the stand-ins above the root (M2, M8, M10) and every edit
that miscounts once the tree is one level deeper. Doubling every value
(P5) makes every grandparent even, so the answer is fixed by the tree's
shape alone, and every edit that tests the wrong node or the wrong parity
shows there.

## Benchmarks

The bench builds 50 trees of `10^4` nodes, the constraints' most, with
values from 1 to 100, once from its own generator: half with each node
hung on a random empty place, half filled level by level with gaps. It
then makes 50 passes, each setting one node of every tree from the
checksum so far, so no answer carries over, answering it with the ★ arm
and folding the sum plus the pass into the checksum. Every implementation
prints `50 passes over 50 trees of 10^4: checksum 620118769`.

BENCHTAB
