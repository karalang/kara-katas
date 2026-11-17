# 2236. Root Equals Sum of Children

You are given the `root` of a **binary tree** that consists of exactly
`3` nodes: the root, its left child, and its right child.

Return `true` *if the value of the root is equal to the **sum** of the
values of its two children, or* `false` *otherwise*.

```
root = [10, 4, 6]  ->  true    (4 + 6 = 10)
root = [5, 3, 1]   ->  false   (3 + 1 = 4)
```

**Constraints:** the tree consists only of the root, its left child,
and its right child; `-100 <= Node.val <= 100`.

The root and its two children matched in one `match` on the pair of
children, and the root's value compared with their sum. O(1).

## Approaches

The tree is LeetCode's `TreeNode`, declared in the harness as a
`shared struct` with `mut` fields: the reference-counted node that
Rust's `Rc<RefCell<TreeNode>>` is.

| file | mechanism |
|---|---|
| `check.kara` ★ | `match root`, then `match (node.left, node.right)` with the arm `(Some(left), Some(right))` |
| `check_walk.kara` | for any tree, not only one of three nodes: each child's value through a helper that reads a missing child as 0, with `if let Some(node) = root` |
| `check_levels.kara` | breadth first: the tree walked level by level from a `Vec` of nodes, each level's values summed, and the first level's sum against the second's |
| `check_struct.kara` | a `struct Family` of the three values, read off the tree by `from_tree` with `unwrap`, and `holds` (`ref self`) |
| `check_iter.kara` | the children as an array, each `map`ped through `Option.map` to its value and `unwrap_or(0)`, and `sum`med |
| `check_solution.kara` | LeetCode's Rust template: `Option<Rc<RefCell<TreeNode>>>` in, the root `unwrap`ped and `borrow`ed, each child read through `as_ref().unwrap().borrow().val`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five more
(all zero, both ends, the children cancelling, the sum one off, and the
children swapped), each with its answer; then, over every pair of
children from -100 to 100 under the roots one below, at and one above
their sum (those within -100 to 100), how many trees there are and how
many hold; then a checksum of 3000 random trees. `check.py` mirrors the
★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 13 edits: the two
`use` lines for `Rc` and `RefCell` deleted, `Option<Rc<RefCell<TreeNode>>>`
written `Option[TreeNode]`, every `.borrow()` dropped, `struct
Solution;` to `struct Solution {}`, and `Solution::check_tree` to
`Solution.check_tree`. The template's `let node = root.borrow();`
becomes `let node = root;`, a second name for the same node, which is
harmless; `as_ref()` stays, as Kāra's `Option` has it too.

The walk, levels, struct and iter arms were first written widening
each value `as i64`; `karac check` warned that `i32` widens to `i64`
implicitly there, and `karac fix` removed seven such casts. The iter
arm's `n.val as i64` inside `Option.map` stays, since there it fixes
the type the sum is taken in.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally on the three values as drawn, before any tree is built: the
root's value less the left child's is the right child's; no tree and no
`+`. It checks 300 random trees, the children from -50 to 50 and the
root one below, at or one above their sum, in turn; then 30 of the
values -100, 0 and 100 only; then 30 with a child of 0 and the root the
other child or its negation. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement's |
| P2 | the children swapped: the same answer |
| P3 | where it holds, the root one higher or one lower: it does not |
| P4 | every value negated: the same answer |
| P5 | the root replaced by the children's sum (when in range): it holds |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 126 holding: checksum 803663621,
12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds each tree as nested dicts and compares the
root's value with `sum()` over its children's. On a failure it prints
the first ten and then the count by property.

The last thirty cases first took a random root beside a child of 0.
Then the ★ arm comparing magnitudes, `node.val.abs() == (left.val +
right.val).abs()`, survived: no case had a root equal to the negated sum,
the one place that edit differs. The root was set to the other child or
its negation, and the edit is now killed (M6).

## Mutation testing

Thirty-two edits to the differential, six to the ★ arm, six to the
levels arm and five to each of the others, each run under `karac
__mir-llvm-run`, and the kept ones under `karac __mir-run` too.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends
and not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the answer inverted | P1 360, P3 234, P5 354, P6 360 |
| M5 | ★: at least the sum | P1 121, P3 247, P4 234, P6 121 |
| M6 | ★: magnitudes compared | P1 15, P6 15 |
| M7 | walk: the children's magnitudes | P1 96, P4 85, P5 249, P6 96 |
| M8 | walk: the left child twice | P1 128, P2 9, P5 349, P6 128 |
| M9 | walk: at most the sum | P1 113, P3 239, P4 234, P6 113 |
| M14 | levels: magnitudes summed | P1 70, P5 153, P6 70 |
| M15 | levels: one level only | P1 126, P5 354, P6 126 |
| M32 | levels: right children queued twice | P1 121, P2 35, P5 328, P6 121 |
| M17 | struct: the right child read as the first | P1 129, P2 9, P5 349, P6 129 |
| M18 | struct: a product | P1 133, P4 2, P5 352, P6 133 |
| M21 | struct: the second child read as 0 | P1 122, P2 39, P5 328, P6 122 |
| M24 | iter: the sum's magnitude | P1 68, P4 137, P5 170, P6 68 |
| M25 | iter: the first child skipped | P1 123, P2 39, P5 324, P6 123 |
| M26 | iter: the sum negated | P1 137, P5 343, P6 137 |
| M27 | solution: a difference | P1 122, P2 40, P5 328, P6 122 |
| M29 | solution: above the sum | P1 247, P3 121, P4 234, P5 354, P6 247 |

P1 and P6 kill all seventeen, P5 fourteen, P2 and P4 six each, and P3
four. P5 builds a tree that must hold, so it catches every edit that
answers a holding tree wrongly; the three it misses (M5, M6, M9) still
answer `true` there. P2 catches the edits that treat the two children
differently, P4 those that break the sign (magnitudes, a product, the
inequalities), and P3 the inequalities and the inverted answer, the
edits that hold for more than one root.

Of the thirty-two, fifteen were not kept, and none crashes, survives,
or differs between the backends. Thirteen fail as a kept one does: the
★ arm's difference (M1) as the template's (M27); the ★, iter and
template arms' left child twice (M2, M22, M28) as the walk arm's (M8);
the walk arm's each child one more (M10) as the levels arm's one level
only (M15); the walk arm's left child dropped, the levels arm's left
children never queued and last node only, and the template's left child
as 0 (M11, M13, M16, M31) as the iter arm's first child skipped (M25);
the levels arm's root at most the children (M12) as the walk arm's at
most the sum (M9); the struct arm's parent negated (M19) as the iter
arm's sum negated (M26); the iter arm's children's magnitudes (M23) as
the walk arm's (M7); and the template's inverted answer (M30) as the ★
arm's (M3). Two fail alike and their own way and are left out for the
count of three: the ★ arm's sum one too many and the struct arm's one
off (M4, M20).

## Verification

Every arm prints the same output as `check.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.5 s to 1.5 s, and the
differential 0.3 s.

## Benchmarks

The bench builds 10^6 trees of three nodes, the children from -50 to 50
and the root one below, at or one above their sum, and checks each, the
★ arm in all five languages; so it measures building and releasing
three nodes as much as the check. Rust builds LeetCode's
`Rc<RefCell<TreeNode>>`, C `malloc`s and frees each node, Go leaves
them to its collector, and Python builds objects. Every implementation
prints `10^6 trees: 332622 hold, checksum 254012139`.

BENCHTAB
