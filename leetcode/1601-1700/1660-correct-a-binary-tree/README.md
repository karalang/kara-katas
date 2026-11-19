# 1660. Correct a Binary Tree

You have a binary tree with a small defect. There is **exactly one**
invalid node where its right child incorrectly points to another node at
the **same depth** but to the **invalid node's right**.

Given the root of the binary tree with this defect, `root`, return *the
root of the binary tree after **removing** this invalid node **and every
node underneath it** (minus the node it incorrectly points to).*

**Custom testing:** the test input is read as three lines: `TreeNode
root`, `int fromNode` (not available to `correctBinaryTree`), and `int
toNode` (not available to `correctBinaryTree`). After the binary tree
rooted at `root` is parsed, the `TreeNode` with value of `fromNode` will
have its right child pointer pointing to the `TreeNode` with a value of
`toNode`. Then, `root` is passed to `correctBinaryTree`.

```
root = [1,2,3], fromNode = 2, toNode = 3                                ->  [1,null,3]
root = [8,3,1,7,null,9,4,2,null,null,null,5,6], fromNode = 7, toNode = 4  ->  [8,3,1,null,null,9,4,null,null,5,6]
```

**Constraints:** the number of nodes in the tree is in the range
`[3, 10^4]`; `-10^9 <= Node.val <= 10^9`; all `Node.val` are unique;
`fromNode != toNode`; `fromNode` and `toNode` will exist in the tree
and will be on the same depth; `toNode` is to the right of `fromNode`;
`fromNode.right` is `null` in the initial tree from the test data.

## Approaches

| file | mechanism |
|---|---|
| `correct.kara` ★ | a preorder walk, right before left, keeping the values met in a `Set`. The node the bad link points to is to the right of the bad node, so the walk has met it by the time it reaches the bad node: the first node whose right child is already in the set is the bad one, and its parent drops it. O(n) time and space |
| `correct_levels.kara` | breadth first a whole level at a time, each node kept with its parent. A node's real children are on the level below, so the one whose right child is on its own level is the bad one; its parent lets go of it, whichever side it hangs on. O(n) time, O(width) space |
| `correct_parents.kara` | breadth first, recording every link into each node and each node's distance from the root. The node the bad link points to is the only one with two links in, its real parent one level up and the bad node on its own level; the farther one is the bad node, and its own parent drops it. O(n) |
| `correct_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Rc<RefCell<TreeNode>>`, a `VecDeque` of (node, parent) pairs drained a level at a time, right child before left, `Rc::ptr_eq` to find the bad node's side), carried by `karac fix`, which made 33 changes in one pass |
| `differential.kara` | the four arms against the statement read literally, five properties |

The node is a `shared struct TreeNode` with `Option[TreeNode]` children,
so the bad link is one more reference to a node the tree already holds.
The bad link makes the tree a graph with one node reached twice, never a
cycle, so the reference counts free it.

Every arm prints the same 8 lines: LeetCode's two examples and three
more (a leaf pointed at its cousin, a node with a left subtree pointed at
its brother, and a link past several nodes of a level), then the nodes
kept and a checksum of the corrected trees for 3000 random trees of 3 to
8 nodes, 300 of up to 1000 and 30 of up to `10^5`. A random tree holds 0
to n - 1 shuffled, each node hung on a random free child slot of the
nodes before it. It is broken once: of all the pairs of a node with no
right child and a node to its right on its level, one is drawn, and the
first is pointed at the second. A tree with no such pair is drawn again.
`correct.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the tree as it was before the bug, with the invalid node and
every node under it removed. It checks 3000 random trees of 3 to 8
nodes, each broken once. Every case is drawn before any arm answers, and
each arm is given a tree of its own, since every arm corrects the tree
it is given.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is a tree: a walk down it meets no node twice |
| P3 | the node the bad link pointed to is kept |
| P4 | every value raised by 1000 gives the same answer, raised |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 854305109, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. One first try was replaced: the levels
arm's bad node recognised only when its right child is on its own level
and it has no left child.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk goes left before right | P1 3000, P2 1858, P4 1858, P5 3000 |
| M2 | ★: the bad node kept, only its bad link cut | P1 3000, P5 3000 |
| M3 | ★: a node's value recorded only when it has a left child | P1 2198, P2 2079, P4 2079, P5 2198 |
| M4 | levels: the bad node taken for its parent's left child whenever there is one | P1 90, P2 90, P4 90, P5 90 |
| M5 | levels: the bad node kept, only its bad link cut | P1 950, P5 950 |
| M6 | levels: a bad node with a left child never found | P1 723, P2 606, P4 606, P5 723 |
| M7 | parents: the nearer of the two links in taken for the bad node | panics, "key not found" |
| M8 | parents: the links into even values never recorded | P1 796, P2 175, P4 175, P5 796 |
| M9 | template: the bad node taken for its parent's left child whenever there is one | P1 90, P2 90, P4 90, P5 90 |
| M10 | template: a bad right child dropped from the left | P1 521, P2 521, P4 521, P5 521 |

## Benchmarks

The bench draws 40 random trees of `10^5` nodes, ten times LeetCode's
largest, breaks each once, builds them all first, then corrects each by
the ★ arm in all five languages: Kāra's `shared struct` with a `Set`,
Rust's `Rc<RefCell<TreeNode>>` with a `HashSet`, pointer nodes with a map
in Go and a set in Python, and nodes from one array per tree in C with an
open-addressing hash set written out. Every implementation prints `40
trees of 100000 nodes: 3999912 nodes kept, checksum 930068907`. The C
build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.368 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.318 s |
| Kāra (`karac build`) | 1.363 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.378 s |
| Rust (`rustc -O`) | 1.392 s |
| Go | 1.794 s |
| Python | 30 s |

The sequential Kāra build is 5% faster than Rust and level with Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.368 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (1.261 s and
1.377 s on one run).

## Verification

All four arms print the same output as `correct.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `ee08f070a`.

## Writing it

The harness first wrote `items.push("null".to_string())` into a
`Vec[String]`, and `karac fix` dropped the `.to_string()`: a string
literal is taken where a `String` is wanted.

The parents arm took three fixes. `for child in [node.left,
node.right].iter()` lost its `.iter()`, since an array literal is walked
by value. `parents.entry(c.val).or_default()` became
`or_insert(Vec.new())`: Kāra's `Entry` puts in the value it is given.
And `let pair = parents[target.unwrap()]` became `let pair = ref
parents[..]`, since an index of a `Map` of `Vec`s is borrowed, not moved
out.

The levels arm first built each level below with an unannotated
`Vec.new()` and pushed `(right, Some(node))`, `node` borrowed from the
level being walked. The check inferred `Vec[(TreeNode, Option[ref
TreeNode])]`, and `level = below` was refused: a collection's element is
solved to a value from a borrow only for a `Copy` type (design.md §8), and
a shared handle is not one. The arm names the level's type, `let mut
below: Vec[(TreeNode, Option[TreeNode])]`. Written so, the push was still
refused, "expected '(TreeNode, Option[TreeNode])', found '(TreeNode,
Option[ref TreeNode])'": a `Some(node)` pushed alone copied the handle
in, and one inside a tuple did not. That was B-2026-11-19-91, fixed in kara `bd214fffc0`.

The template seeds its queue with `(root, None::<Rc<RefCell<TreeNode>>>)`,
Rust's typed `None`. `karac fix` rewrote the inner type to `TreeNode` and
then stopped at "Expected `)`, found `::`", with nothing to offer: the
turbofish after a function name was named and fixed, one after `None` was
not. That was B-2026-11-19-100, fixed in kara `ee08f070a`: the turbofish is now named
and fixed to Kāra's typed `None`, `Option[TreeNode].None`, and the whole
template carries in one pass.
