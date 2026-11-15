# 2196. Create Binary Tree From Descriptions

You are given a 2D integer array `descriptions` where `descriptions[i] =
[parenti, childi, isLefti]` indicates that `parenti` is the **parent** of
`childi` in a **binary** tree of **unique** values. Furthermore,

- If `isLefti == 1`, then `childi` is the left child of `parenti`.
- If `isLefti == 0`, then `childi` is the right child of `parenti`.

Construct the binary tree described by `descriptions` and return *its
**root***.

The test cases will be generated such that the binary tree is **valid**.

```
descriptions = [[20,15,1],[20,17,0],[50,20,1],[50,80,0],[80,19,1]]  ->  [50,20,80,15,17,19]
descriptions = [[1,2,1],[2,3,0],[3,4,1]]                            ->  [1,2,null,null,3,4]
```

**Constraints:** `1 <= descriptions.length <= 10^4`;
`descriptions[i].length == 3`; `1 <= parenti, childi <= 10^5`;
`0 <= isLefti <= 1`; the binary tree described by `descriptions` is
valid.

One pass over the descriptions: each value's node made the first time it
is named and kept in a `Map`, the child hung on its parent's side, and
every child put in a `Set`; the root is the one parent never named as a
child. O(n).

## Approaches

| file | mechanism |
|---|---|
| `create.kara` ★ | each value's node made the first time it is named and kept in a `Map[i64, TreeNode]` by `node_of` (`mut ref` the map), the child hung on its parent's side, every child put in a `Set`; the root the first parent the set does not hold |
| `create_topdown.kara` | each parent's two children written into a `Map[i64, (i64, i64)]` of values (0 for none), the root found by `find` as the parent no pair names, and the tree built down from it by a recursive `build` |
| `create_table.kara` | each value's node at its own index of a `Vec[Option[TreeNode]]` as long as the largest value (`Vec.filled`), the root found by arithmetic: the sum of the distinct values less the sum of the children, since every value but the root is a child exactly once |
| `create_struct.kara` | a `struct Builder` of each value's node and each child's parent, both `Map`s, with `add` (`mut ref self`) hanging one description and `root` (`ref self`) climbing the parent links by `while let` from the first description's parent |
| `create_iter.kara` | every value's node made at once, each description `flat_map`ped to its two values and `collect`ed into a `Map`; the children `collect`ed into a `Set`; each description hung by `for_each`; the root by `find` and `and_then` |
| `create_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in, `Option<Rc<RefCell<TreeNode>>>` out, the nodes in a `HashMap` through `entry(..).or_insert_with(..)` and `Rc::new(RefCell::new(TreeNode::new(..)))`, each hung through `borrow_mut()`, the children in a `HashSet`; carried by `karac fix` in six rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one description, a chain of right children, a full tree given bottom
up, and a zigzag), each with its tree in LeetCode's level-order form;
then a checksum of the trees for 2000 random sets of 1 to 60
descriptions, with values up to 100 or up to 10^5 in turn; then the
constraints' largest, 10^4 descriptions of a random tree, and a chain of
10^4 alternating sides given from the bottom up. `create.py` mirrors the
★ arm and its output is byte-identical. The tree is a `shared struct
TreeNode`, so a node kept in the `Map` and the one hung on its parent
are one node.

`karac fix` carries the template in six rounds of 12, 7, 1, 1, 3 and 2
edits: first Rust's spellings (`Vec<..>` and `Option<..>` to brackets,
`HashMap::new()` and every other `::` call to `.`, `for d in
&descriptions` to `for d in ref descriptions`, `!children.contains(&d[0])`
to `not children.contains(d[0])`, `struct Solution;` to `struct Solution
{}`); then `Rc[RefCell[TreeNode]]` to `TreeNode`, since a `shared
struct` is already counted and mutable through any holder, which drops
`Rc.new(RefCell.new(..))` and each `borrow_mut()`; then the three `use`
lines one round each; then `HashMap` and `HashSet` to `Map` and `Set`;
and last the adapter's `vec![..]` to a list literal and the harness's
`"null".to_string()` to the literal, a style lint that `karac check`
does not show.

The ★ arm was first written `return nodes.get(d[0]);` from a `->
Option[TreeNode]`: `get` lends an `Option[ref TreeNode]`, and `karac
check` reported the bare mismatch with no fix, though `.cloned()` is the
mend it offers when the same two types meet at `==`. kara B-2026-11-15-37
adds it, so `karac fix` now writes `nodes.get(d[0]).cloned()`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the root is the one value never named as a child, and each
node's left and right children are read off the descriptions that name
it as the parent, the tree written out level by level; no map and no
set. It checks 300 random trees of 2 to 61 nodes with values up to 100
or up to 1000 in turn; then 30 chains, each node the only child of the
one before on a random side; then 30 of one description, with values up
to 10^5. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the tree, written in level order, is the statement read literally |
| P2 | it holds every value named, each once: one node more than the descriptions |
| P3 | the descriptions in reverse order: the same tree |
| P4 | every value v written m + 1 - v, for m the largest: the same tree with its values so written |
| P5 | every side swapped: the tree's mirror image |
| P6 | each arm agrees with at least three of the other five |

The renamed and swapped descriptions are each built by a `map` closure
over the case. The closure cannot return the list literal `[e[0], e[1],
1 - e[2]]` itself: with no type to follow, a literal is a `Vec`, a
closure cannot declare its return type, and the `collect` into a
`Vec[Array[i64, 3]]` fails with no fix. Each is bound with its type
first; kara B-2026-11-15-38 asks for the closure's literal to follow the
type the `collect` wants.

The differential prints `360 cases: checksum 389807938, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
cases. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
other arm, each run under `karac __mir-llvm-run` and `karac __mir-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends and
not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a node made anew each time it is named | P1 285, P2 285, P3 39, P4 265, P6 285 |
| M5 | ★: the first parent taken as the root | P1 297, P2 297, P3 312, P6 297 |
| M6 | ★: a right child put on the left when it is free | P1 274, P2 183, P3 238, P4 249, P5 314, P6 274 |
| M7 | topdown: the right child kept from the left | P1 344, P2 344, P3 276, P5 360, P6 344 |
| M9 | topdown: the right subtree built from the left | P1 290, P2 290, P5 290, P6 290 |
| M11 | topdown: a leaf's children read | P1 157, P2 157, P4 213, P5 228, P6 157 |
| M12 | table: the root one off | P1 360, P2 360, P4 89, P6 360 |
| M14 | table: the sides swapped | P1 360, P6 360 |
| M15 | table: a right child also on the left of a leaf | P1 267, P2 267, P4 239, P5 311, P6 267 |
| M17 | struct: the root one step short | P1 297, P2 297, P3 118, P6 297 |
| M19 | struct: the parent link the wrong way | P1 360, P2 360, P3 265, P6 360 |
| M20 | struct: a node remade when named twice | P1 311, P2 311, P3 80, P4 249, P6 311 |
| M22 | iter: the children's nodes left out | P1 360, P2 360, P6 360 |
| M23 | iter: the parents counted as children | P1 318, P2 318, P3 207, P6 318 |
| M25 | iter: the last description not hung | P1 360, P2 360, P3 325, P6 360 |
| M29 | solution: a child above 500 always on the left | P1 174, P2 139, P3 139, P4 171, P5 194, P6 174 |
| M30 | solution: the child a new node | P1 322, P2 322, P3 297, P6 322 |

P1 and P6 kill all seventeen, P2 sixteen, P3 eleven, P4 seven and P5
six. P2 misses only the sides swapped (M14), whose tree holds every
value once. P3 misses the six edits that go wrong the same way whatever
the order the descriptions come in: the right subtree built from the
left (M9), a leaf's children read (M11), the root one off (M12), the
sides swapped (M14), a right child also on the left (M15) and the
children's nodes left out (M22). P4 renames the values, and kills just
the seven edits that read a value: those keyed on a remainder (M2, M6,
M11, M15, M20, M29) and the table arm's root found by arithmetic (M12).
P5 swaps the sides, and kills the six that treat the two sides unlike
(M6, M7, M9, M11, M15, M29); an edit that swaps both, or neither, is
its own mirror.

Of the thirty-one, fourteen were not kept. Two are equivalent: the
topdown arm's root taken as the last parent no pair names (M10), since
only one parent is never a child; and the struct arm's climb started
from the first description's child (M18), which reaches the same root.
Two crash on an index out of bounds, in the table arm: a value summed
each time it is named (M13), and the table only as long as the largest
parent (M16). Six fail as a kept one does: the sides swapped in the ★,
struct and template arms (M1, M21, M27) as M14, and the parent put in
the set, the root's children dropped and the child put in the set as
the parent (M3, M24, M31) as M22, each giving no root or a lone one.
Four fail alike in pairs and are left out to keep three to an arm: the
root taken as a child (M4, M28), and a left child overwritten or set
only while the right is free (M8, M26). M15 replaces a first edit that
hung a child on both sides of its parent, whose trees double at every
level and ran the run out of memory.

## Verification

Every arm prints the same output as `create.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, struct, template and topdown arms take
2.6 s to 3.0 s and the iter arm 5.5 s; the table arm takes 41 s, filling
a table as long as the largest value, up to 10^5, for each of its 2002
trees. The differential takes 14 s.

## Benchmarks

The bench builds 20 random sets of 10^4 descriptions once, each a tree of
10^4 + 1 values from 1 to 10^5, then builds every tree 50 times over with
the ★ arm in all five languages; each tree is weighed by its node count
and the sum of its values times their depths, walked with a stack. Go,
Python and Kāra keep the nodes in their own map and set; Rust in a
`HashMap` and `HashSet` of `Rc<RefCell<TreeNode>>`; C in two
open-addressing tables, freeing each tree after it is weighed. Every
implementation prints `50 passes over 20 trees: checksum 413577243`.

BENCHTAB
