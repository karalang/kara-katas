# 1325. Delete Leaves With a Given Value

Given a binary tree `root` and an integer `target`, delete all the leaf
nodes with value `target`. Once you delete a leaf node with value
`target`, if its parent node becomes a leaf node and has the value
`target`, it should also be deleted (you need to continue doing that until
you cannot).

```
root = [1,2,3,2,null,2,4], target = 2  ->  [1,null,3,null,4]
root = [1,3,3,3,2], target = 3         ->  [1,3,null,null,2]
root = [1,2,null,2,null,2], target = 2 ->  [1]
```

**Constraints:** the number of nodes in the tree is in the range `[1,
3000]`, and `1 <= Node.val, target <= 1000`.

The arms are `fn remove_leaf_nodes(root: Option[TreeNode], target: i32) ->
Option[TreeNode]`, over LeetCode's tree as a `shared struct TreeNode`.

## Approaches

| file | mechanism |
|---|---|
| `remove_leaf_nodes.kara` ★ | a recursive walk that settles both children first, so that a node whose children were both deleted is already a leaf when it is looked at; a leaf with the target's value is deleted by returning `None` in its place. O(n), as deep as the tree |
| `remove_leaf_nodes_stack.kara` | the same order, children before their parent, kept by hand on a stack of nodes, each with its parent, which side of it it hangs on, and whether its children are done; a node popped the second time with no children left and the target's value is cut from its parent. O(n), no recursion |
| `remove_leaf_nodes_rounds.kara` | the statement's own process, a round at a time: every leaf with the target's value at the start of a round is cut, and the rounds go on until one cuts nothing; a parent left a leaf by a cut waits for the next round. O(n h) for a tree h deep |
| `remove_leaf_nodes_levels.kara` | the nodes listed level by level with the index of each one's parent; walked from the end of the list back, every node comes after its children, so a node is deleted when its value is the target and none of its children is kept, a count of kept children per node telling which. The deleted nodes are then cut from their parents, found by `ref_eq`. O(n) |
| `remove_leaf_nodes_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Option<Rc<RefCell<TreeNode>>>`, each child taken out with `node.borrow_mut().left.take()`, settled by the recursive call and put back, and `None` returned for a leaf with the target's value), carried to Kāra by `karac fix` |
| `remove_leaf_nodes_match.kara` | a second Rust solution as LeetCode's Rust users write it (a `match` on the root, the children read with `node.borrow().left.clone()`, settled, and written back through `borrow_mut()` only when the node stays), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, a lone leaf
that is the target, a chain of 3000 nodes, the constraints' most, all the
target, the same chain under a root that is not, and a full tree of 2047
nodes, all the target but its root (`[1,null,3,null,4] [1,3,null,null,2]
[1] [] [] [6] [1]`); then 1000 random trees of 1 to 3000 nodes, most of
them small, with values up to 2, 3 or 1000, every other one run deep, the
answer folded as its level-order list (`1000 random trees: nodes left
156035, checksum 647356917`). `remove_leaf_nodes.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, stack and rounds arms checked clean as first
written. The levels arm first cut a deleted node from its parent's left
when `l === nodes[j]`, JavaScript's identity test. `karac fix` mended
the `===` to `==` as a machine fix, and the check then asked for
`#[derive(PartialEq)]` on `TreeNode`, a structural comparison, where a
`shared` handle's identity is `a.ref_eq(b)` (design.md § Shared types);
on a `shared struct` whose fields all compare, `karac fix` applied that
derive too, and a program that asked whether two handles were the same
object then asked whether their contents were equal. The arm is written
with `ref_eq`; the gap is B-2026-11-24-38, and the derive's line,
indented by the width of `shared `, is B-2026-11-24-39. Both are fixed
(kara a605738803, 8021d3ea6f): `==` on a `shared` handle is now refused
with both readings named, `a.ref_eq(b)` and the derive, and neither
applied, and a derive line above a `pub` or `shared` declaration lines
up with it. The first Rust arm takes one round of 36 fixes by `karac
fix`'s count, from 12 errors: its two `use` lines deleted, `struct
Solution;` to `struct Solution {}`, `Option<Rc<RefCell<TreeNode>>>` to
`Option[TreeNode]`, `Self::` to `Solution.`,
`node.borrow_mut().left.take()` to `node.left.take()`, `let mut n =
node.borrow_mut();` to `let n = node;`, `&&` to `and`, and `::` to `.`.
The second takes one round of 37 fixes from 12 errors: the same
rewrites, with every `node.borrow()` and `node.borrow_mut()` before a
field dropped, since a `shared struct`'s fields read and write directly.
Both outputs match on the first run.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the tree's nodes listed, and while some node still there has
the target's value and no child still there, the first such node
deleted; the deleted nodes are then cut from their parents. 2000 trees of
1 to 12 nodes, each new node hung on an empty child place chosen at
random, in four kinds, 500 each: values 1 to 2; 1 to 3; 1 to 2 with each
node hung, three times in four, on one of the two newest empty places, so
that the trees run deep; and every value the target but one. Every tree
and target is drawn before any arm answers, and each arm is handed a
fresh tree built from the level-order list, since every arm cuts the tree
it is given.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the tree mirrored: the answer mirrored |
| P3 | a target no node has: the tree as it was |
| P4 | a new root with the target's value above the old root: the new root kept above the answer, or deleted with it when the answer is empty |
| P5 | the answer asked again: nothing more to delete |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 trees: checksum 945736000,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Fourteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Two are left out: the rounds arm's
root never deleted fails exactly the checks of the stack arm's root
deletion never noticed (M4), and the match arm's node deleted when either
child is gone fails exactly the checks of the levels arm's node deleted
with one child still kept (M7). The twelve kept, two to each arm, are
each killed, fail the same way under both backends and not by a crash,
and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node looked at before its children are settled | P1 714, P4 52, P5 714, P6 3570 |
| M2 | ★: a node with no left child taken for a leaf | P1 886, P2 1037, P6 4430 |
| M3 | stack: every cut made on the parent's left | P1 1064, P2 1386, P6 1064 |
| M4 | stack: the root's deletion never noticed | P1 98, P4 98, P6 98 |
| M5 | rounds: a cut below a kept left child not counted, so the rounds can stop early | P1 405, P2 354, P4 380, P5 405, P6 405 |
| M6 | rounds: a right leaf cut whatever its value | P1 1050, P2 1664, P3 1424, P6 1050 |
| M7 | levels: a node deleted with one child still kept | P1 1332, P4 1036, P6 1332 |
| M8 | levels: a deleted node always cut from its parent's right | P1 874, P2 1340, P5 289, P6 874 |
| M9 | solution: the right child never put back | P1 1412, P2 1334, P3 1714, P6 1412 |
| M10 | solution: the left child put back unsettled | P1 1242, P2 742, P4 479, P6 1242 |
| M11 | match: the settled left child never written back | P1 874, P2 1340, P6 874 |
| M12 | match: the children written back on each other's sides | P1 1649, P3 1837, P4 1902, P5 1649, P6 1649 |

P1 and P6 kill all twelve, P2 eight, P4 six, P5 four and P3 three.
Mirroring the tree (P2) catches the edits that treat a left child and a
right one differently, and misses the four that do not: settling a node
before its children (M1), the root's deletion (M4), a kept child too many
(M7) and the children swapped, which a mirror swaps back (M12). A target
no node has (P3) must leave the tree as it was, so it catches only the
edits that change a tree with nothing to delete: a right leaf cut
whatever its value (M6), a right child dropped (M9) and the children
swapped (M12). Asking the answer again (P5) catches the edits that leave
something deletable behind: no cascade up from a deleted leaf (M1), the
rounds stopping early (M5), a deleted node left on its parent's left
(M8), and the swap, which swaps back.

## Benchmarks

The bench builds 30 trees of 3000 nodes, the constraints' most, with
values from 1 to 3, once from its own generator: each node hung on an
empty place chosen at random, or for every other tree, three times in
four one of the two newest, so that it runs deep. It then makes 300
passes, each setting one node of every tree and the target from the
checksum so far, so no answer carries over; linking every node back to
its children, since the last answer cut some away; answering it with the
★ arm; and folding the nodes left, the root's value and the pass into the
checksum. Rust takes LeetCode's own `Rc<RefCell<TreeNode>>`, as Kāra's
`shared struct` counts its handles. Every implementation prints `300
passes over 30 trees of 3000: checksum 925117320`.

BENCHTAB
