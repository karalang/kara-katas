# 1123. Lowest Common Ancestor of Deepest Leaves

Given the `root` of a binary tree, return the lowest common ancestor of
its deepest leaves.

Recall that:

- The node of a binary tree is a leaf if and only if it has no children.
- The depth of the root of the tree is `0`. If the depth of a node is
  `d`, the depth of each of its children is `d + 1`.
- The lowest common ancestor of a set `S` of nodes is the node `A` with
  the largest depth such that every node in `S` is in the subtree with
  root `A`.

```
root = [3,5,1,6,2,0,8,null,null,7,4]  ->  [2,7,4]
root = [1]                            ->  [1]
root = [0,1,3,null,2]                 ->  [2]
```

**Constraints:** the number of nodes in the tree is in the range `[1,
1000]`; `0 <= Node.val <= 1000`; the values of the tree are unique.

The arms are `fn lca_deepest_leaves(root: Option[TreeNode]) ->
Option[TreeNode]`, where `TreeNode` is a `shared struct` with `mut`
fields: LeetCode's Rust `Option<Rc<RefCell<TreeNode>>>` is Kāra's
`Option[TreeNode]`, and the answer is a node of the tree itself, printed
as its subtree in LeetCode's level-order form.

## Approaches

| file | mechanism |
|---|---|
| `lca_deepest_leaves.kara` ★ | one walk from the root: each call returns its subtree's depth and the ancestor of its deepest leaves, the node itself when its two sides are as deep, otherwise the deeper side's. O(n) |
| `lca_deepest_leaves_two_pass.kara` | two passes: the tree's depth first, then a walk that returns a deepest leaf it finds at that depth, or the node itself when both its sides found one. O(n) |
| `lca_deepest_leaves_levels.kara` | level by level from the root, each node's parent kept in a `Map` by value (the values are distinct), then the last level climbed one level at a time, duplicates dropped through a `Set`, until its nodes meet in one. O(n) |
| `lca_deepest_leaves_stack.kara` | the ★ arm's walk without recursion: a post-order stack, each node pushed once to open it and once more to close it, its depth and ancestor kept in a `Map` by value until its parent closes. O(n) |
| `lca_deepest_leaves_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `Rc<RefCell<TreeNode>>`, a nested `fn dfs` returning the depth and the ancestor, `Rc::clone` for the node itself), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: the answers for LeetCode's three
examples and five more (two deepest leaves under the root, one deepest
leaf down a long branch, a full tree, a chain to the left, the deepest
leaves in one subtree), then over 2000 random trees of up to 1000 nodes,
LeetCode's limit, every other one grown with long branches, the sizes of
the answers' subtrees summed and a checksum (`2000 random trees: 102689
nodes under the answers, checksum 722294004`). `lca_deepest_leaves.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every leaf's depth found, the deepest ones kept, and of the
nodes whose subtree holds all of them, the deepest in the tree. Each arm
answers a fresh copy of the tree, and answers are compared by value,
which is distinct within a tree. It checks 2000 problems in four kinds
of 500: up to 12 nodes hung at random; one to three nodes; a chain of up
to 20, each node to a random side; and a complete tree of up to 31.
Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | by a second reading: the answer's subtree holds every deepest leaf, and neither of its children's does |
| P3 | the tree mirrored gives the same node |
| P4 | the tree hung below a new root gives the same node |
| P5 | a child hung on one deepest leaf is the answer alone |
| P6 | every leaf above the greatest depth cut off gives the same node |

All 60,000 checks pass on every arm: `2000 problems: checksum 774748360,
60000 checks over 5 arms: 0 failures`. A Python reading of the same
problems, the statement read literally with sets of values, gives the
same checksum.

## Mutation testing

Twenty-five edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All twenty-five are caught. Nineteen are kept, no two
failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a leaf never its own answer | P1 1372, P2 1372, P5 2000 |
| M2 | ★: a deeper left side answered by the node itself | P1 1177, P2 1177, P3 1378, P5 2000 |
| M3 | ★: a deeper right side one level short | P1 152, P2 152, P3 604, P5 41, P6 106 |
| M4 | ★: the left side walked for the right | P1 1378, P2 1378, P4 2000, P5 2000 |
| M5 | ★: a deeper left side answered by the right side's answer | P1 1177, P2 1177, P3 807, P5 2000, P6 167 |
| M6 | two-pass: the depth counted down the left side only | P1 939, P2 939, P3 1263, P4 2000, P5 968, P6 30 |
| M7 | two-pass: a node one level up taken as a deepest leaf | P1 1323, P2 1323, P4 271, P5 2000, P6 409 |
| M8 | two-pass: the right side's depth not stepped | P1 1496, P2 1496, P3 962, P4 1032, P5 968 |
| M9 | two-pass: the root counted at depth 0 | P1 2000, P2 2000, P5 2000 |
| M10 | levels: the right children never met | P1 1496, P2 1496, P3 1729, P4 2000, P5 968, P6 135 |
| M11 | levels: the climb stops at two nodes | P1 628, P2 628, P3 628 |
| M12 | levels: the walk stops at the first level of two or more | P1 516, P2 516, P5 892, P6 189 |
| M13 | levels: the answer's parent returned | P1 1378, P2 1378, P4 622, P5 2000 |
| M14 | stack: a left side alone answered by the node | P1 938, P2 938, P3 1172, P5 2000, P6 191 |
| M15 | stack: a right side alone answered by the node | P1 870, P2 870, P3 1172, P4 2000, P5 907, P6 114 |
| M16 | stack: a deeper left side answered by the right side's answer | P1 406, P2 406, P3 516, P5 811, P6 204 |
| M17 | solution: a deeper left side one level short | P1 508, P2 508, P3 604, P5 759, P6 220 |
| M18 | solution: a deeper right side answered by the left side's answer | P1 934, P2 934, P3 807, P4 1195, P5 968, P6 152 |
| M19 | solution: the shallower side's answer taken | P1 1572, P2 1572, P4 952, P5 2000, P6 321 |

P1 and P2 catch all nineteen, P5 eighteen, P3 and P6 twelve each, and
P4 nine. P2 fails exactly where P1 does: a node whose subtree holds
every deepest leaf while neither child's does is the lowest common
ancestor, so the second reading is a full one. P3 to P6 compare an arm
with itself, so each catches an edit only when its reshaping changes
the edit's mistake. P5 is the sharpest of them: with a child hung on one
deepest leaf there is one deepest leaf, the new child, so an edit that
never hands a lone deepest leaf up as the answer fails it on all 2000
problems, as nine of these do. M11 fails P1 to P3 alone: stopping the
climb at two nodes answers wrongly whenever two or more deepest leaves
are left, and P4 and P6 reshape the tree without changing its deepest
leaves, so the same wrong node comes back, while P5 leaves only one.

Of the six not kept, five fail as a kept edit: the two-pass arm
answering a lone left deepest leaf by the node as M2, the solution arm
walking the right side for the left as M4, the solution arm answering a
tie by the right side as M9, the stack arm never walking the right
children as M10, and the stack arm answering a tie by the left side as
M11. The levels arm climbing a parent once per child stops: the climb
reaches the root, which has no parent, and the map's index panics with
`key not found`. Three edits written first were dropped as equivalent,
not caught, since only the order of depths matters: the stack arm giving
a leaf depth 0 and stepping each depth twice, and the solution arm
counting an empty side one level deep.

## Verification

Every arm prints the same output as `lca_deepest_leaves.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found one gap, now fixed. The ★, two-pass and levels arms were
written as Kāra; the stack arm was too, but with Rust's `!closing`,
which `karac fix` made `not closing`. The solution arm, written as Rust,
went in five rounds: `Rc<RefCell<TreeNode>>` to `TreeNode` and the `use`
lines dropped, `&n.borrow().left` to `n.left`, `Rc::clone(n)` to `n`,
the nested `fn dfs` moved out of the `impl`, `struct Solution {}`
declared and `Solution::` to `Solution.`. The gap: `karac fix` wrote the
parameter `&Option<Rc<RefCell<TreeNode>>>` as `ref Option[TreeNode]`,
so the node matched out of it was a `ref TreeNode` and `Some(n)` an
`Option[ref TreeNode]`, which the function could not return as an
`Option[TreeNode]`: a type error with no fix, which also kept the lint
that drops a parameter's redundant `ref` from running. The fix now
drops the `&` of a parameter's `&Rc<RefCell<T>>` or
`&Option<Rc<RefCell<T>>>`, a shared struct's handle that a bare
parameter already borrows (B-2026-11-11-75).

## Benchmarks

The bench builds 16 random trees of 10^4 nodes once, values up to 10^5,
each node hung at a random free place below the ones before it. Each of
200 rounds hangs one more node on every tree the same way and solves it
with the ★ arm: 3200 walks of about 10^4 nodes. Every implementation
prints `200 rounds over 16 trees of 10^4 nodes: answers total 168345633,
checksum 199965951`. Rust's nodes are LeetCode's own
`Rc<RefCell<TreeNode>>`, Go's are on its collected heap, Python's are
objects with `__slots__`, and C `malloc`s each node.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `628eb9974d`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Go | 0.495 to 0.624 s | 0.560 s |
| C (`clang -O3`) | 0.573 to 0.714 s | 0.636 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.507 to 0.722 s | 0.649 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.963 to 1.126 s | 1.053 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.954 to 1.275 s | 1.095 s |
| Kāra (`karac build`) | 0.925 to 1.153 s | 1.098 s |
| Rust (`rustc -O`) | 1.002 to 1.149 s | 1.125 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.139 to 1.217 s | 1.187 s |
| Python | 4.140 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time equals its wall time), so its two rows differ by noise.
Kāra takes about 1.7x C's time and 2x Go's, and ties Rust, whose nodes
are reached through `Rc<RefCell<..>>` with a borrow flag checked on
every read; with overflow checks Rust is a little slower. Each call hands
a node back up as a reference-counted handle where C hands a pointer and
Go a collected one; the gap was not traced further. Python takes about
3.8x Kāra's time.
