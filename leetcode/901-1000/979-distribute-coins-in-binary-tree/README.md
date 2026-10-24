# 979. Distribute Coins in Binary Tree

You are given the `root` of a binary tree with `n` nodes where each
`node` in the tree has `node.val` coins. There are `n` coins in total
throughout the whole tree.

In one move, we may choose two adjacent nodes and move one coin from
one node to another. A move may be from parent to child, or from child
to parent.

Return the minimum number of moves required to make every node have
exactly one coin.

```
root = [3,0,0]  ->  2
root = [0,3,0]  ->  3
```

**Constraints:** the number of nodes is `n`, `1 <= n <= 100`;
`0 <= Node.val <= n`; the sum of all `Node.val` is `n`.

## Approaches

| file | mechanism |
|---|---|
| `distribute_coins.kara` ★ | excess from the leaves: the coins that cross the edge above a subtree are its excess, its coins less its nodes, in the direction its sign says, and no plan moves fewer. A walk from the leaves returns each subtree's excess, and each edge adds the absolute excess below it to the moves. O(n) time, O(height) stack |
| `distribute_coins_stack.kara` | the same excesses without recursion: each node is pushed, then pushed again under its children so it finishes after both, and a second stack holds finished subtrees' excesses for their parents to collect |
| `distribute_coins_levels.kara` | level order, backwards: the nodes listed in level order beside their parents' places, so each comes after its parent; walking the list backwards, each node's excess is complete at its turn, is added to the moves and handed to the parent. O(n) |
| `distribute_coins_recount.kara` | every edge counted afresh: each edge recounts its whole subtree's nodes and coins from scratch rather than reusing its children's counts. O(n * height) |
| `distribute_coins_peel.kara` | peeling leaves: the tree becomes numbered nodes with lists of neighbours, no root, and leaves are peeled one at a time; each settles its excess with its one remaining neighbour, which becomes a leaf when it has one neighbour left. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines. The first ten are LeetCode's two
examples and eight more: one node with its coin (0); [1, 0, 2] (2);
[0, 0, 3] (3); a node whose right child holds three coins (4); a path
of four with every coin at the far end (6) and at the top (6); and the
complete tree of seven with every coin on the root (10) and on the last
leaf (16). Then totals and checksums over random trees whose coins are
thrown at random nodes: 300 of 1 to 12 nodes (1,480 moves) and 3,000
of 1 to LeetCode's 100 (196,981). The last three are trees of 100
nodes: a random one (117), the complete tree with every coin on the
root (480), and a path with every coin at the far end (4,950, which is
1 + 2 + ... + 99). A random tree hangs each new node below the root,
going left or right at random down to the first empty place.
`distribute_coins.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a move takes one coin across one edge, and the answer is the
fewest moves from the given coins to one on every node, found by a
breadth-first search over every placement of the n coins on the n
nodes. That search is why the statement's trees are small: it checks
3,200 trees, 3,000 of 1 to 7 nodes against the statement and 200 of
LeetCode's 100 against the other properties. The coins are thrown at
random nodes, piled on one random node, or placed one to a node and
then a few moved at random, by turns.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 trees |
| P2 | the mirror image needs the same moves |
| P3 | every coin beyond the first on its node moves at least once, and none needs more than n - 1 moves |
| P4 | one coin moved across one edge, from a node that has a coin, changes the answer by exactly one, since only that edge's crossing count changes |
| P5 | a new leaf holding its own coin, hung at a random empty place, needs nothing, so the answer stays |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 trees of 31943 nodes: 73476 moves, checksum 52115496,
95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(12.9 s) and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twenty-eight edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the edges to right children never counted | P1 1859, P2 2068, P3 910, P4 1396, P6 2059 |
| M2 | ★: no node keeps a coin | P1 2290, P3 1462, P5 3200, P6 2490 |
| M3 | ★: the excesses counted with their signs | P1 1828, P3 1715, P6 2028 |
| M4 | stack: the two edges netted against each other | P1 1003, P3 353, P6 1202 |
| M5 | stack: the right excess never passed up | P1 1052, P2 1560, P4 653, P6 1249 |
| M6 | stack: the right excess left on the stack | P1 1786, P2 2109, P3 1104, P4 1100, P5 679, P6 1986 |
| M7 | levels: the root's first child never settled | P1 1855, P2 1210, P3 632, P4 997, P5 142, P6 2034 |
| M8 | levels: an excess taken from the parent | P1 1110, P3 238, P4 1042, P6 1293 |
| M9 | levels: the last node never settled | P1 1503, P2 526, P3 642, P4 752, P5 864, P6 1609 |
| M10 | recount: the right subtree's coins never counted | P1 880, P2 1370, P3 184, P4 653, P5 1346, P6 1066 |
| M11 | recount: the right edges never walked | P1 1925, P2 2019, P3 1429, P4 1789, P6 2125 |
| M12 | recount: only the root's edges counted | P1 1659, P3 862, P4 1332, P6 1859 |
| M13 | peel: the excesses counted with their signs | P1 1599, P2 768, P3 1550, P5 532, P6 1798 |
| M14 | peel: a neighbour never becomes a leaf | P1 1409, P3 768, P4 626, P5 1144, P6 1609 |
| M15 | peel: a shortage handed on as a surplus | P1 1121, P2 630, P3 323, P4 430, P5 706, P6 1319 |

P1 and P6 kill all fifteen, P3 fourteen (all but M5), P4 eleven (all but
M2, M3, M4 and M13), P2 nine (M1, M5, M6, M7, M9, M10, M11, M13, M15)
and P5 eight (M2, M6, M7, M9, M10, M13, M14, M15). P2 sees an edit that
treats left and right differently, which the mirror swaps. P5 sees an
edit that charges a balanced subtree, as M2 does when no node keeps a
coin and the new leaf hands its coin up. M3, the signs kept, is the same
edit in ★, levels and recount, and fails the same checks in all three;
in peel (M13) it also fails P2 and P5. Peel charges an edge from
whichever end comes off first, so the sign it adds depends on the order
the leaves come off, and the mirrored and grown trees peel in a
different order.

Thirteen other edits were tried and set aside. Five failed exactly the
same checks as a kept one: levels and recount keeping the signs, as
M3; levels and recount charging every node, by no node keeping a coin
and by never counting a subtree's root, as M2; and levels handing
right children to the root, as M5. Eight were sound but beyond three
an arm: ★ reading the left subtree for the right and never passing
the right excess up; stack keeping two coins at each node and counting
every node as a move; levels counting the parent's running excess and
handing left children to the root; peel keeping no coin at a node and
letting a leaf settle with peeled neighbours too.

## Verification

Every arm prints the same output as `distribute_coins.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 1.6 s (★) to 2.6 s (peel), and the differential 12.9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 2,000 random trees of 100 nodes, LeetCode's
largest, with their coins thrown at random nodes, once. In each of 200
rounds it runs the ★ arm on every tree, each round starting from a
different one, and folds the answers into a checksum. Every
implementation prints `200 rounds over 2000 trees of 100 nodes:
54574400 moves, checksum 735130014`. The Rust tree is LeetCode's
`Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
`shared struct` is, and each visit borrows its node's `RefCell`, as
kata 968's bench does.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.403 to 0.458 s | 0.417 s |
| Rust (`rustc -O`) | 0.520 to 0.599 s | 0.577 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.856 to 0.973 s | 0.899 s |
| Go | 0.423 to 0.478 s | 0.433 s |
| Python | 8.4 s | |
| Kāra (`karac build --mir`) | 0.685 to 0.796 s | 0.735 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 11 times
Kāra's.

v2 took 0.82 times Rust's median time under overflow checks and 1.76
times C's. Under valgrind's cachegrind v2 ran 3,199 million
instructions and 378 million branches with 32.9 million mispredicted,
Rust with overflow checks 2,838 million, 439 million and 51.9 million,
and C 1,434 million, 90 million and 26.4 million. The two Rust builds
differ only in overflow checks, which cost Rust 0.32 s here; that
build mispredicts 19 million times more than v2, which runs 361
million more instructions. Where v2's extra instructions go was not
measured.
