# 1379. Find a Corresponding Node of a Binary Tree in a Clone of That Tree

Given two binary trees `original` and `cloned` and given a reference to
a node `target` in the original tree.

The `cloned` tree is a copy of the `original` tree.

Return a reference to the same node in the `cloned` tree.

Note that you are not allowed to change any of the two trees or the
`target` node and the answer must be a reference to a node in the
`cloned` tree.

```
tree = [7,4,3,null,null,6,19], target = 3                                   ->  3
tree = [7], target = 7                                                      ->  7
tree = [8,null,6,null,5,null,4,null,3,null,2,null,1], target = 4            ->  4
```

**Constraints:** the number of nodes in the tree is in the range `[1,
10^4]`, the values of the nodes of the tree are unique, and `target`
node is a node from the `original` tree and is not `null`. **Follow
up:** could you solve the problem if repeated values on the tree are
allowed?

The tree is a `shared struct TreeNode { mut val: i32, mut left:
Option[TreeNode], mut right: Option[TreeNode] }`, reference counted, so
a node is a handle and two handles are the same node when `ref_eq` says
so. Each arm is `fn get_target_copy(original: TreeNode, cloned:
TreeNode, target: TreeNode) -> TreeNode`. Every arm finds the node by
identity, never by value, so each answers the follow-up too.

## Approaches

| file | mechanism |
|---|---|
| `get_target_copy.kara` ★ | the two trees walked together, depth first, each step taken in both; the clone's node at the step where the original's is the target itself is the answer. O(n), as deep as the tree |
| `get_target_copy_bfs.kara` | the two trees walked together breadth first, a queue of pairs of the original's node and the clone's in the same place. O(n) |
| `get_target_copy_path.kara` | the original alone searched for the target, keeping the turns from the root, left or right; then the same turns taken in the clone. O(n) |
| `get_target_copy_rank.kara` | the original's nodes counted breadth first until the target, the k-th; then the clone's counted the same way to its k-th, a clone having the same shape. O(n) |
| `get_target_copy_solution.kara` | a Rust solution in the shape LeetCode's Rust users give tree problems (`Option<Rc<RefCell<TreeNode>>>` parameters, `?` on the options, `Rc::ptr_eq` for the same node, children read through `.borrow().left.clone()`, and `Self::` for the recursion), carried to Kāra by `karac fix`. LeetCode offers this problem in no Rust, so the signature is the one its other tree problems use |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, and 10^4
nodes, the constraints' most, in a chain of left children, the last node
asked for, and as a complete tree, its last node and a middle one asked
for (`3 7 4 1 10000 4322`, each without the `?` that marks an answer
that is not the target's own copy in the clone); and 2000 random trees
of 1 to 300 nodes, each holding different values and each node hung on
an empty child place chosen at random, on one of the last two opened, so
the tree runs deep, or on one of the first two still open, so it fills
level by level, a third of each, with a node of each asked for at random
(`2000 random trees: 2000 own copies found, checksum 830148289`).
`get_target_copy.py` mirrors the ★ arm, with `is` for the same node, and
its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the four Kāra arms check clean as first written. The Rust
solution takes one round of 37 fixes by `karac fix`'s count, from 12
errors: the `use std::cell::RefCell;` and `use std::rc::Rc;` lines
deleted, `struct Solution;` to `struct Solution {}`, each
`Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, `Rc::ptr_eq(&o,
target.as_ref()?)` to `o.ref_eq(target.as_ref()?)`, each `.borrow()`
dropped, and `Self::` and `Solution::` to `Solution.`. Its output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every node's place in a tree written as the turns from the
root, `L` and `R`; the target's place in the original found by identity,
and the clone's node at the same place returned. A tree of one node and
2001 trees of 1 to 30 nodes, drawn as above, a third of each kind, each
with a node asked for at random. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the statement read literally, the same node |
| P2 | a node of the clone, and none of the original |
| P3 | the target's value |
| P4 | every value made 1 in both trees: the node in the same place |
| P5 | the trees asked the other way round, for the target's own copy: the target |
| P6 | the ★ arm's node |

All 60,060 checks pass on every arm: `2002 cases: checksum 49485227,
60060 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, taking the
clone's node in the target's place, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks. Two first edits were replaced because they
crashed: a search that can come back empty ends in the `unwrap()` that
turns LeetCode's `Option` back into a node, so the ★ arm's right step
taken into the clone's left and the Rust solution's left result dropped
stopped both lanes there. P5 as first written crashed too, on the ★ arm
answering the original's node (M1): it asked the other way round for the
arm's own answer, and the clone holds no copy of an original node; it
now asks for the target's copy.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the original's node answered, not the clone's | P1 2002, P2 2002, P4 2002, P5 2002, P6 8008 |
| M2 | ★: a node matched by its value, not by identity | P4 1732 |
| M3 | bfs: the clone's node compared with the target, never equal, so the clone's root answered | P1 1732, P3 1732, P4 1732, P5 1732, P6 1732 |
| M4 | bfs: the original's left child paired with the clone's right | P1 1451, P3 1451, P4 1451, P5 1451, P6 1451 |
| M5 | path: the last turn left off, so the target's parent's copy answered | P1 1732, P3 1732, P4 1732, P5 1732, P6 1732 |
| M6 | path: the right subtree never searched | P1 1438, P3 1438, P4 1438, P5 1438, P6 1438 |
| M7 | rank: the target counted one place too far | P1 1931, P3 1931, P4 1931, P5 1931, P6 1931 |
| M8 | rank: the clone's nodes counted depth first | P1 1004, P3 1004, P4 1004, P5 1004, P6 1004 |
| M9 | solution: the original's node answered, not the clone's | P1 2002, P2 2002, P4 2002, P5 2002, P6 2002 |
| M10 | solution: a node matched by its value, not by identity | P4 1732 |

P4 kills all ten, P1, P5 and P6 eight each, P3 six and P2 two. Making
every value 1 (P4) is the follow-up, and the only property that catches
matching by value (M2, M10): with values unique, the node holding the
target's value is the target, and only repeated values tell them apart,
in the 1732 cases whose target is not the root. The original's node
answered (M1, M9) has the target's value and is the target itself, so
only P2, which asks for a node of the clone, and the identity checks see
it. Every other edit lands on the wrong node of the clone, whose value
differs (P3), and asked the other way round lands wrong again (P5). The
same mistake made in two arms fails as many checks in each (M2 and M10;
M1 and M9 but for P6, where a wrong ★ arm fails against every arm), and
the clone's root answered (M3) and the target's parent's copy (M5) both
fail exactly the cases whose target is not the root.

## Benchmarks

The bench builds 10 trees of 10^4 nodes, the constraints' most, once,
each node hung on an empty child place chosen at random, with their
clones and their nodes in the order they were hung. Then 3000 rounds,
each asking one tree's clone for the copy of one node, both drawn from
the checksum so far, with the ★ arm. Every implementation prints `3000
rounds over 10 trees of 10000 nodes: checksum 397514538`. The work is
the walk of both trees up to the target, the same in every language. The
Rust tree is `Rc<RefCell<TreeNode>>`, as LeetCode's Rust tree problems
have it, since a Kāra `shared struct` is reference counted too, and its
function takes `&Rc<..>` as the Kāra one borrows its handles; C and Go
compare pointers.

BENCHTAB
