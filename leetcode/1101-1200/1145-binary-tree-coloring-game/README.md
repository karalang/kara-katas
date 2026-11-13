# 1145. Binary Tree Coloring Game

Two players play a turn based game on a binary tree. We are given the
`root` of this binary tree, and the number of nodes `n` in the tree. `n`
is odd, and each node has a distinct value from `1` to `n`.

Initially, the first player names a value `x` with `1 <= x <= n`, and the
second player names a value `y` with `1 <= y <= n` and `y != x`. The first
player colors the node with value `x` red, and the second player colors
the node with value `y` blue.

Then, the players take turns starting with the first player. In each
turn, that player chooses a node of their color (red if player 1, blue if
player 2) and colors an uncolored neighbor of the chosen node (either the
left child, right child, or parent of the chosen node.)

If (and only if) a player cannot choose such a node in this way, they
must pass their turn. If both players pass their turn, the game ends, and
the winner is the player that colored more nodes.

You are the second player. If it is possible to choose such a `y` to
ensure you win the game, return `true`. If it is not possible, return
`false`.

```
root = [1,2,3,4,5,6,7,8,9,10,11], n = 11, x = 3  ->  true
root = [1,2,3], n = 3, x = 1                      ->  false
```

**Constraints:** the number of nodes in the tree is `n`;
`1 <= x <= n <= 100`; `n` is odd; `1 <= Node.val <= n`; all the values of
the tree are unique.

The arms are `fn btree_game_winning_move(root: Option[TreeNode], n: i64,
x: i64) -> bool`, over LeetCode's tree as a `shared struct TreeNode` with
an `i32` value.

## Approaches

Red's node cuts the tree into at most three parts: its left subtree, its
right subtree, and everything above it. Blue, starting on red's neighbour
in one part, walls that part off and takes all of it, and red takes the
rest, so blue wins exactly when one part holds more than half the nodes.

| file | mechanism |
|---|---|
| `btree_game_winning_move.kara` ★ | one walk from the root counting every subtree; at red's node the sizes of its two subtrees go to a `mut ref (i64, i64)`, and the part above is what is left of `n`. O(n) |
| `btree_game_winning_move_find.kara` | red's node found first, then its two subtrees counted on their own; the three parts tested with `any`. O(n) |
| `btree_game_winning_move_stack.kara` | without recursion: the nodes taken off a stack, every node before its children, then read back from the end so each subtree's size comes from its children's, kept in a `Map` by value. O(n) |
| `btree_game_winning_move_flood.kara` | the tree as a graph, every edge in lists by value both ways; from each of red's neighbours a breadth-first flood that never enters red counts what blue would own. O(n) |
| `btree_game_winning_move_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `Rc<RefCell<TreeNode>>`, a nested `fn count` that fills red's two sides through `&mut i32`, `n / 2` as the half), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 12 lines: LeetCode's two examples; one node
(false); a chain of five with red in the middle (false) and at the top
(true); seven nodes full with red at the root (false) and at its left
child (true). Then over 2000 random trees of an odd 1 to 99 nodes, every
other one grown deep, red at a random node, how many blue wins and a
checksum (`2000 random trees: blue wins 1886, checksum 955219091`), and
four trees of 99 nodes, the largest odd count the constraints allow:
full with red at the root (true) and at its left child (false), a chain
with red in the middle (false), and a random tree with red at each node
in turn (blue loses only at one). `btree_game_winning_move.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each value blue could name, the game played out move by
move, red and blue each coloring an uncolored neighbour of one of their
nodes or passing when they have none, both playing their best, with the
positions remembered in a `Map`; the answer is whether some first node
lets blue end with more nodes. It checks 2000 trees of an odd 1 to 13
nodes in four kinds of 500: random with red anywhere; grown deep with red
anywhere; random with red at the root; and grown deep with red at a leaf.
Blue wins 1495 of them. Every random choice, P3's names, P4's leaf and
P6's node among them, is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | every node's children swapped gives the same answer |
| P3 | every value renamed, red's with it, gives the same answer |
| P4 | the same tree hung from one of its leaves gives the same answer |
| P5 | of every node red could take, exactly one leaves blue no win |
| P6 | the children swapped at one node gives the same answer |

P4 holds because the game is played on the tree's edges, which do not
change when another node is taken for the root. P5 holds because a tree
with an odd number of nodes has exactly one node whose removal leaves no
part of more than half; it is checked by asking the arm about every `x`.

All 60,000 checks pass on every arm: `2000 trees: checksum 452702585,
60000 checks over 5 arms: 0 failures`. A Python reading of the same
trees, by the same game search, with the six properties asserted against
the ★ arm's mirror, gives the same line.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-nine are caught; one is
equivalent: the ★ arm counting a part of exactly half the nodes as a win
(`>=` for `>`), which `n` odd never offers. Fifteen are kept, no two
failing the same checks; two of them stop the run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the part above red never taken | P1 962, P4 693, P5 1699 |
| M2 | ★: red counted in the part above | P1 394, P4 103, P5 1344 |
| M3 | ★: a right subtree counted at most one | P1 204, P2 294, P4 221, P5 693, P6 80 |
| M4 | find: the right side never searched | stops: `unwrap()` on `None` |
| M5 | find: the part above leaves out the right side | P1 67, P2 95, P4 55, P5 972, P6 17 |
| M6 | find: every part must hold more than half | P1 1495, P5 1699 |
| M7 | stack: sizes read before they are found | stops: key not found |
| M8 | stack: one more than half not enough | P1 419, P5 1515 |
| M9 | stack: a left subtree one too big | P1 205, P2 126, P4 148, P5 611, P6 30 |
| M10 | flood: the node valued 1 never linked to its children | P1 623, P3 687, P4 233, P5 1130 |
| M11 | flood: an edge only upward | P1 1084, P4 535, P5 1699 |
| M12 | flood: at most two neighbours of each node followed | P1 414, P2 332, P4 116, P5 1003, P6 40 |
| M13 | solution: the left side kept for the right | P1 177, P2 349, P4 198, P5 916, P6 47 |
| M14 | solution: a left subtree counted twice | P1 103, P2 62, P4 68, P5 634, P6 17 |
| M15 | solution: red found only with a left child | P1 39, P2 78, P4 39, P5 381, P6 16 |

P1 and P5 each catch all thirteen edits that let the run finish: an edit
that misjudges one red node almost always misjudges how many red nodes
lose. P4 catches eleven, all but the two that only move the line between
a win and a loss (M6, M8): re-rooting the tree changes which part is
"above" red and which sides are left and right, but not the three parts
themselves, so only an edit that misreads the parts can see it. P2
catches seven, the edits that treat a left side and a right side unlike
(M3, M5, M9, M12, M13, M14, M15), and P6, which swaps the children of one
node, catches the same seven on fewer trees. P3 catches only M10, the one
edit that looks at what a node is called. The edits that stop the run are
the search that never looks right, which finds no red node when red is
in a right subtree, and the stack arm reading its nodes from the root
down, which asks for a child's size before it is known.

Of the fourteen caught and not kept, eight fail exactly as a kept one:
the part above never taken in the stack and solution arms, as M1; red
counted with its parent's side in the solution arm, as M2; the left side
taken for both in the ★ arm and the left side counted twice in the find
arm, as M13; half rounded up in the solution arm, as M8; a red node with
no left child never found in the find arm, which stops as M4; and the
right children never reached in the stack arm, which stops as M7. Two
pairs fail alike: no node counted in the ★ arm and the flood passing
through red, which both make blue win wherever red has a neighbour; and a
size counting down the left only in the find and stack arms. The other
two, blue starting only at red's first neighbour and one less than half
a win in the flood arm, each fail in a way of their own and were not
needed.

## Verification

Every arm prints the same output as `btree_game_winning_move.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, find, stack and flood arms were written as Kāra and checked clean
as written. `karac fix` carried the solution arm in five rounds:
`Option<Rc<RefCell<TreeNode>>>` to `Option[Rc[RefCell[TreeNode]]]`, the
`&` and `&mut` at the calls dropped and `&mut i32` to `mut ref i32`,
`let (mut left, mut right)` to `let mut (left, right)`, `||` to `or` and
`Solution::` to `Solution.`; then `Rc[RefCell[TreeNode]]` to the shared
`TreeNode`, `rc.borrow()` to `rc` and the `RefCell` import dropped; then
the nested `fn count` lifted out of the method and the `Rc` import
dropped; then `struct Solution {}` declared; then `mut` at the recursive
calls and `0i32` on the pair's literals. In the harness, a tuple of a
case's tree, `n` and `x` read out of `cases.iter()` binds its numbers by
value, so `karac fix` drops the `*` from `*n` and `*x`, and the harness
is written without it.

The kata found one gap. The differential's `(1..n + 1).filter(|v| ..
*v ..)` was refused with "drop the `*`", as LeetCode's Rust habit would
write it and as Kāra lends a range's item to the predicate by value,
while the harness's `(1..100).filter(|x| .. *x ..)` was accepted: over a
range of bare literals the item was a literal no use had typed yet,
which was not taken for a copy, so the parameter kept the library's
`ref`. Now a literal item is a copy as an `i64`'s is, and both are
refused alike (B-2026-11-12-18, fixed).

## Benchmarks

The bench builds 20 random trees of 99 nodes once, the largest odd
count LeetCode allows. Each of 1000 rounds asks every tree about 99 first
moves for red drawn at random and answers each with the ★ arm: 1,980,000
calls, each a walk over all 99 nodes. Every implementation prints `1000
rounds over 20 trees of 99 nodes: blue wins 1960031, checksum 204130535`.
The tree is Kāra's `shared struct TreeNode`, LeetCode's own
`Rc<RefCell<TreeNode>>` in Rust, `malloc`'d nodes in C and pointers in
Go.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `18ea960272`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.778 to 0.835 s | 0.801 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.757 to 0.867 s | 0.803 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.827 to 0.866 s | 0.843 s |
| Kāra (`karac build`) | 0.833 to 0.871 s | 0.848 s |
| Go | 0.861 to 0.980 s | 0.890 s |
| Rust (`rustc -O`) | 1.162 to 1.253 s | 1.208 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.173 to 1.241 s | 1.209 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.136 to 1.266 s | 1.212 s |
| Python | 20.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. C takes about 0.95x Kāra's median time and Go about 1.06x. Rust
takes about 1.43x with or without overflow checks. Its walk does one
thing the others do not, a `borrow()` of each node's `RefCell` (a flag
counted up, tested and counted down again), but this README has not
measured how much of the difference that is. Python takes about 24x.
