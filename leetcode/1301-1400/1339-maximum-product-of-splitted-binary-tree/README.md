# 1339. Maximum Product of Splitted Binary Tree

Given the `root` of a binary tree, split the binary tree into two
subtrees by removing one edge such that the product of the sums of the
subtrees is maximized. Return the maximum product of the sums of the two
subtrees. Since the answer may be too large, return it modulo 10^9 + 7.
Note that you need to maximize the answer before taking the mod and not
after taking it.

```
root = [1,2,3,4,5,6]                  ->  110
root = [1,null,2,3,4,null,null,5,6]   ->  90
```

**Constraints:** the number of nodes in the tree is in the range `[2, 5 *
10^4]`; `1 <= Node.val <= 10^4`.

The arms are `fn max_product(root: Option[TreeNode]) -> i32`, over a
`shared struct TreeNode` with `mut` fields.

## Approaches

| file | mechanism |
|---|---|
| `max_product.kara` ★ | cutting the edge above a node splits off that node's subtree, so the product is s * (total - s) for its sum s: one recursive walk finds the total, a second every subtree's sum, keeping the best product through a `mut ref i64`, taken modulo 10^9 + 7 only at the end. O(n), as deep as the tree |
| `max_product_stack.kara` | no recursion: a post-order walk from a `Vec` of (node, children done) pairs, and a second `Vec` of the sums finished and not yet claimed by their parent, so a node takes its children's sums off the top. O(n) |
| `max_product_closest.kara` | s * (total - s) grows as s nears half the total, so every subtree's sum is gathered by one walk and the one whose double is nearest the total is the cut; only that one product is made. O(n) |
| `max_product_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn sum(node: &Option<Rc<RefCell<TreeNode>>>, sums: &mut Vec<i64>) -> i64` nested in the method, a `match` on the node, `n.borrow()`, every subtree's sum pushed, and the best found by `map(\|&s\| s * (total - s)).max()`), carried to Kāra by `karac fix` |
| `max_product_twopass.kara` | a second Rust solution as LeetCode's Rust users write it (two nested functions, `total` and `dfs`, reading the node with `if let Some(n) = node { let n = n.borrow(); .. }`, the best kept through `best: &mut i64` and `(*best).max(..)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, two nodes, a
chain of 5 * 10^4 nodes, the constraints' most, each the right child of
the one before, and a full tree of 2^15 - 1 nodes, both with values up
to 10^4, so the best product passes 10^9 + 7 (`110 90 2 46014069
797168013`); and 1000 random trees of 2 to 2000 nodes, most of them
small, each node hung on a random empty place, with values up to 100 or
up to 10^4 (`1000 random trees: checksum 429480207`). `max_product.py`
mirrors the ★ arm, with an iterative walk since Python's recursion would
not reach the chain's depth, and its output is byte-identical. Every arm
gives the same output under `karac __mir-run`, `karac run` and `karac
__mir-llvm-run`.

The Mend loop: the three Kāra arms check clean. A first draft of the
stack arm kept each node's sum in a `Map[TreeNode, i64]`; `karac check`
refuses it (E0232), since a `shared struct` handle has no `Hash`, so the
arm keeps its sums on a second stack instead. The Rust solution takes one
round of 38 fixes by `karac fix`'s count, from 17 errors: the `use
std::rc::Rc;` and `use std::cell::RefCell;` lines deleted, the nested
`fn sum` hoisted to the top level, `&Option<Rc<RefCell<TreeNode>>>` to
`Option[TreeNode]` and `&mut Vec<i64>` to `mut ref Vec[i64]`, the
`n.borrow()` rebinding and the `as i64` casts removed, `&root` and
`&mut sums` at the calls to `root` and `mut sums`, `Vec::new()` to
`Vec.new()`, `|&s|` to `|s|`,
`struct Solution;` to `struct Solution {}` and `Solution::` to
`Solution.`. The second takes one round of 48 fixes from 20 errors, the
same kinds, with `dfs` hoisted above `total`. Both match on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the tree flattened to values and neighbours, each edge from a
node to its parent removed in turn, the two trees left summed by
separate walks, and the largest product kept before the modulo. 2000
trees of 2 to 12 nodes in four kinds, 500 each: values from 1 to 100
hung at random places; values from 1 to 3; every value 1, where many
cuts tie; and a chain, each node a random child of the one before. Every
tree is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the tree mirrored: the same answer |
| P3 | every value doubled: four times the answer |
| P4 | the same tree hung from its first leaf in preorder: the same answer |
| P5 | a new root of value 1 above it: no smaller than the answer, nor than the total |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 trees: checksum 957594384,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, with every subtree's sum from
one post-order walk, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a cut tried only above a leaf | P1 1609, P4 784, P6 6436 |
| M2 | ★: only the first cut's product kept | P1 1642, P2 650, P4 1199, P6 6568 |
| M3 | stack: a right child's sum never popped | P1 1862, P2 1862, P4 1809, P5 969, P6 1862 |
| M4 | stack: a node's own value left out of its sum | P1 2000, P5 2000, P6 2000 |
| M5 | closest: the distance measured to the total halved, rounded down | P1 76, P2 16, P3 76, P4 93, P6 76 |
| M6 | closest: the distance taken without its sign | P1 1670, P4 782, P6 1670 |
| M7 | solution: the right subtree walked but not added | P1 1862, P2 1856, P4 1779, P5 975, P6 1862 |
| M8 | solution: a leaf's sum never recorded | P1 320, P4 180, P6 320 |
| M9 | twopass: the right subtree's total read from the left | P1 1934, P2 1852, P4 1918, P5 244, P6 1934 |
| M10 | twopass: right subtrees summed without being tried as cuts | P1 1334, P2 1942, P4 1212, P6 1334 |

P1 and P6 kill all ten, P4 nine, P2 six, P5 four and P3 one. Mirroring
(P2) catches the edits that treat the two children differently: the
right child's sum lost (M3, M7), read from the left (M9) or never tried
(M10), and the first cut kept (M2), which is the leftmost leaf's.
Hanging the tree from a leaf (P4) keeps every edge but changes which
nodes are leaves and which side each subtree falls on, so it catches all
but M4, whose answer is 0 on every tree. The new root above (P5) adds a
cut worth the whole total, which catches the edits that lose a part of
the tree's sum (M3, M4, M7, M9). Doubling every value (P3) multiplies a
correct product by four and most wrong ones too; it catches only the
halving that rounds down (M5), since a doubled total is even and rounds
no more. M5 is the weakest: rounding the half down misleads only when
the total is odd and the two sums nearest half straddle it, 76 of the
2000 trees. M8 fails only where the best cut is above a leaf, as in
every two-node tree.

## Benchmarks

The bench builds 10 trees of 5 * 10^4 nodes, the constraints' most, with
values from 1 to 10^4, each node hung on a random empty place, once;
then makes 20 passes, each setting one node of every tree from the
checksum so far, so no answer carries over, answering every tree with
the ★ arm's two recursive walks and folding the answer plus the pass
into the checksum. Rust walks LeetCode's own `Rc<RefCell<TreeNode>>`.
Every implementation prints `20 passes over 10 trees of 5 * 10^4:
checksum 310473038`.

BENCHTAB
