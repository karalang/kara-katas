# 2415. Reverse Odd Levels of Binary Tree

Given the `root` of a **perfect** binary tree, reverse the node values at
each **odd** level of the tree.

- For example, suppose the node values at level 3 are
  `[2,1,3,4,7,11,29,18]`, then it should become `[18,29,11,7,4,3,1,2]`.

Return *the root of the reversed tree.*

A binary tree is **perfect** if all parent nodes have two children and
all leaves are on the same level.

The **level** of a node is the number of edges along the path between it
and the root node.

```
root = [2,3,5,8,13,21,34]                 ->  [2,5,3,8,13,21,34]
root = [7,13,11]                          ->  [7,11,13]
root = [0,1,2,0,0,0,0,1,1,1,1,2,2,2,2]    ->  [0,2,1,0,0,0,0,2,2,2,2,1,1,1,1]
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 2^14]`; `0 <= Node.val <= 10^5`; `root` is a **perfect** binary
tree.

Reversing a level swaps each node with the one in the mirror place, and
the mirror of a left child's left child is the right child's right
child. So the pairs to swap can be walked down together, two subtrees at
a time, without ever listing a level.

## Approaches

| file | mechanism |
|---|---|
| `reverse.kara` ★ | mirror pairs: the root's two children walked down together, the outer pair and the inner pair of their children next, each pair's values swapped on an odd level. O(n) |
| `reverse_bfs.kara` | level by level: a breadth-first walk keeps one level's nodes, swaps the i-th and the i-th from the end on an odd level, then gathers the next. O(n) |
| `reverse_array.kara` | an array: the nodes listed in level order, the values read out, each odd level's run, from `2^d - 1` for `2^d` places, reversed by `reverse()` on a slice, and written back. O(n) |
| `reverse_stack.kara` | the ★ arm's pairs without recursion: an explicit stack of pairs and their levels. O(n) |
| `reverse_iter.kara` | iterators: each level the last one's children by `flat_map` over `chain`, an odd level's values written back by `zip` against them by `rev`. O(n) |
| `reverse_solution.kara` | LeetCode's Rust template: `Option<Rc<RefCell<TreeNode>>>` in and out, a `dfs` nested in the method walking the pairs through `borrow()` and `borrow_mut()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

The harness's node is LeetCode's own, `shared struct TreeNode` with an
`i32` value, and each arm reverses the tree in place, as LeetCode's
does. Every arm prints the same 7 lines: LeetCode's three examples; one
node; the values 0 to 14 in order; a random tree of the constraints'
largest, `2^14 - 1` nodes, and one of the values 0 to `2^14 - 2` in
order, each by a digest of the answer in level order; then 2000 random
trees of 0 to 6 levels below the root, values below 1 to 50, with a
checksum of the digests and the total of the root's left child less its
right. `reverse.py` mirrors the ★ arm and its output is byte-identical,
and the mirror was checked on 5000 random trees of up to 7 levels
below the root against reversing every odd level of the level order
list.

`check` first reports 10 errors on the template, and `karac fix`
carries it in one call, reporting 41 edits: the two `use` lines
deleted; each `Option<Rc<RefCell<TreeNode>>>` given brackets and then
written `Option[TreeNode]`, since a `shared struct` is itself the
counted, writable handle; every `borrow()` and `borrow_mut()` dropped;
both `!odd` written `not odd`; the nested `dfs` moved above the `impl`,
since Kāra has no nested items and it captured nothing; and `struct
Solution;` given its braces. The `.clone()` of each child and of
`root`, a count on a shared handle, stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a walk down the tree gathers every level's values from left
to right, each odd level's list is reversed, and the lists are read off
in order. No mirror pairs and no level-order positions. It checks 300
random perfect trees of 0 to 6 levels below the root, values below 1 to
50; then 30 of up to 12 levels, values up to `10^5`; then 30 of up to
12 levels, values below 4. All 360 are drawn before any arm answers, and
every arm gets a tree built afresh for every question.

| | property |
|---|---|
| P1 | the answer, read in level order, is the literal reading's |
| P2 | the arm run again on its own answer: the original tree |
| P3 | the tree mirrored, every level reversed: the answer mirrored |
| P4 | every value raised by 7: every value of the answer raised by 7 |
| P5 | every even level as it was, and every odd level holding the same values, sorted, as before |
| P6 | each arm agrees with at least three of the other five |

P2 holds because reversing a level twice restores it, P3 because
mirroring reverses every level and reversal commutes with reversal, P4
because the values only move, and P5 because they move only within
their own odd level.

The differential prints `360 cases: checksum 393832534, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and puts each value at its mirror place on an odd level.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the inner pairs keeping their parity | P1 279, P5 274, P6 279 |
| M5 | ★: the inner pairs never visited | P1 230, P6 230 |
| M6 | ★: a pair whose left is 0 left alone | P1 117, P2 120, P3 165, P4 117, P6 117 |
| M8 | bfs: the even levels reversed | P1 315, P5 280, P6 315 |
| M9 | bfs: the right of each pair given one more | P1 322, P2 322, P3 322, P5 322, P6 322 |
| M11 | bfs: no level of 64 reversed | P1 31, P6 31 |
| M13 | array: half of each odd level reversed | P1 311, P3 232, P6 311 |
| M15 | array: the leaves never written back | P1 151, P6 151 |
| M16 | array: the odd levels past a quarter skipped | P1 309, P6 309 |
| M18 | stack: no pair below level 4 swapped | P1 145, P6 145 |
| M19 | stack: the outer pairs two levels down | P1 278, P5 275, P6 278 |
| M21 | stack: the walk stopping past 10 pairs waiting | P1 4, P6 4 |
| M22 | iter: every level from the first reversed | P1 280, P5 280, P6 280 |
| M23 | iter: no level reversed | P1 310, P6 310 |
| M25 | iter: a 0 written as 1 | P1 171, P2 171, P4 171, P5 171, P6 171 |
| M29 | solution: the outer pairs visited twice | P1 231, P6 231 |
| M30 | solution: a root of 0 left alone | P1 25, P4 25, P6 25 |

P1 and P6 kill all seventeen, P5 six, and P2, P3 and P4 three each.
Most mutants swap the wrong pairs or skip some, and such a reversal is
still undone by running it twice (P2), commutes with mirroring the tree
(P3), moves the values without changing them (P4), and often keeps each
odd level's values within that level (P5); only the reading against
the literal answer (P1) and the vote (P6) see them.

Of the thirty-one, fourteen were not kept. Seven fail the same checks
as a kept one: the even levels reversed in the ★ arm and the stack
arm's first pair at level 2 (M1, M17) as the bfs arm's even levels
reversed (M8); the left children gathered at the front (M10) as the
outer pairs visited twice (M29); the iter arm's last node never written
and only the first half read (M24, M26) as half of each odd level
reversed (M13); the left child paired with itself (M27) as no level
reversed (M23); and the template's left of each pair given one more
(M28) as the bfs arm's right of each pair given one more (M9). Seven
fail apart from every kept one and were left out because those arms
keep their share already: the ★ arm's pair copied, not swapped (M2) and
outer pairs matched left to left (M3); the bfs arm's middle pair never
swapped (M7); the array arm's odd level twice as far as the last (M12)
and values written back in reverse (M14); the stack arm's pair given
the left value (M20), which fails as M2 does; and the template's pair
rising by one left alone (M31).

## Verification

Every arm prints the same output as `reverse.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.3 to 2.2 s, most of it the two
trees of `2^14 - 1` nodes. The differential takes 34 s there, 5.1 s
under `karac __mir-llvm-asan` and 0.8 s under `karac run`.

## Benchmarks

The bench builds 10 perfect trees of `2^14 - 1` nodes, values below
`10^5`, once from the harness's generator, then makes 1000 passes, each
reversing every tree in place and folding its root's two children and
its leftmost and rightmost leaves, plus the pass, into the checksum,
with the ★ arm in all five languages. Every implementation prints `1000
passes over 10 trees of 2^14 - 1 nodes: checksum 239452265`. Kāra's
nodes are a `shared struct` and Rust's `Rc<RefCell<TreeNode>>`, both
counted handles; Kāra counts every child it reads out of a node, while
Rust borrows them, and on this container Kāra ran about 1.5 times as
long as Rust. C and Go walk plain pointers.

BENCHTAB
