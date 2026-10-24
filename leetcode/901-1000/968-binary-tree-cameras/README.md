# 968. Binary Tree Cameras

You are given the `root` of a binary tree. We install cameras on the tree
nodes where each camera at a node can monitor its parent, itself, and its
immediate children. Return the minimum number of cameras needed to
monitor all nodes of the tree.

```
root = [0,0,null,0,0]                ->  1
root = [0,0,null,0,null,0,null,null,0]  ->  2
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 1000]`; `Node.val == 0`.

## Approaches

| file | mechanism |
|---|---|
| `min_camera_cover.kara` ★ | greedy from the leaves: a leaf's parent should hold the camera that covers the leaf, since it covers at least as much. Walk the tree bottom up, each subtree reporting its root's state: 0 not yet covered, 1 holds a camera, 2 covered without one. A node with an uncovered child takes a camera, a node with a camera below is covered, any other waits for its parent, and an uncovered root takes one itself. O(n) time, O(height) stack |
| `min_camera_cover_stack.kara` | the same states without recursion: a stack of nodes, each pushed again under its children so it is decided once both are, and a second stack of finished subtrees' states |
| `min_camera_cover_dp.kara` | three costs per subtree, no greedy choice: the fewest cameras that watch all of a subtree below its root when the root holds a camera, when it holds none but a child's camera covers it, and when it holds none and nothing below covers it, so its parent must. Each comes from the children's three costs, and the answer is the better of the first two at the root |
| `min_camera_cover_levels.kara` | the greedy on arrays: the nodes listed in level order with their parents, then walked backwards, so every node comes after its children. A node its children left uncovered puts a camera on its parent, covering the node, the parent and the parent's parent; an uncovered root takes one itself |
| `min_camera_cover_peel.kara` | the deepest uncovered node: a camera on its parent covers it and as much else as any camera that could cover it. The nodes are sorted by depth once, deepest first, and each one still uncovered when its turn comes puts a camera on its parent (the root on itself), marking that node, its parent and its children covered. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and eight
more (one node, two nodes, three nodes, a path of four, the complete tree
of seven, a tree whose subtrees are paths, a fuller tree of eight nodes,
and a right-leaning path of five); for 300 random trees of 1 to 12 nodes,
1,879 nodes in all, the cameras they need in total and a checksum; and
three trees of 1,000 nodes, LeetCode's largest: a random tree (371
cameras), the complete tree (288) and a path (334). A random tree hangs
each new node below the root, going left or right at random down to the
first empty place. `min_camera_cover.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of nodes tried, the smallest one that watches every
node. It checks 3,200 random trees: 3,000 of up to 8 nodes against the
statement, and 200 of up to 400 nodes against the other properties;
52,282 nodes in all, which need 19,893 cameras.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | a camera watches at most four nodes, so at least n / 4 are needed, and a tree of two or more nodes never needs more than n / 2 |
| P3 | the same answer for the mirror |
| P4 | a new leaf at the end of the leftmost path adds at most one camera and never saves one |
| P5 | two copies of the tree under a new root need between twice as many less two and twice as many plus one, and a path of n nodes needs n / 3 rounded up |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 trees of 52282 nodes: 19893 cameras, checksum 240660142,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (8.8 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Twenty-three edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run` with the same failures; fifteen are
kept, three to each arm, and all fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a missing child counted as uncovered | P1 2626, P2 2826, P5 2826, P6 2826 |
| M2 | ★: a camera only when both children are uncovered | P1 1753, P2 1419, P5 2076, P6 1952 |
| M3 | ★: an uncovered root left so | P1 500, P2 376, P5 1213, P6 561 |
| M4 | stack: a missing left child counted as uncovered | P1 2233, P2 2351, P3 1845, P5 802, P6 2433 |
| M5 | stack: the root given a camera when it holds one | P1 1852, P2 1634, P4 1209, P5 2423, P6 1997 |
| M6 | stack: covered only by a camera on the left | P1 434, P2 129, P3 661, P6 624 |
| M7 | dp: a missing child holding a free camera | P1 2751, P2 2650, P5 3200, P6 2951 |
| M8 | dp: a camera's children never left open | P1 1790, P2 1693, P5 2052, P6 1989 |
| M9 | dp: covered only by cameras on both children | P1 984, P2 514, P4 5, P5 2446, P6 1183 |
| M10 | levels: the root's first child never looked at | P1 282, P2 48, P3 570, P5 287, P6 287 |
| M11 | levels: a camera not covering its parent | P1 1258, P2 542, P5 2052, P6 1457 |
| M12 | levels: an uncovered root left so | P1 126, P2 2, P5 839, P6 187 |
| M13 | peel: shallowest first | P1 1551, P2 1430, P5 2446, P6 1750 |
| M14 | peel: a camera not covering its children | P1 757, P2 330, P6 953 |
| M15 | peel: the root's children watching themselves | P1 210, P2 189, P6 235 |

P1, P2 and P6 kill all fifteen, P5 twelve (all but M6, M14 and M15), P3
three (M4, M6, M10) and P4 two (M5, M9). P3 sees only edits that treat
left and right differently, and P4 only those whose answer can fall or
jump by two when one leaf is added; most wrong answers here are wrong in
the same direction on both trees. P5's path check catches every edit
that miscounts a path, and the three it misses count paths right.

Eight other edits were tried and set aside. Four failed exactly the same
checks as a kept one: dp letting the root stay open, as M3; peel putting
the camera on the node itself, as M8, not covering the camera's parent,
as M11, and giving every node a camera, as M1. Four were sound but beyond
three an arm: ★ covering a node only with two cameras below it and
letting a camera below excuse an uncovered child, stack calling for a
camera only for an uncovered left child, and levels not covering the
camera's own node. None was equivalent and none crashed.

## Verification

Every arm prints the same output as `min_camera_cover.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.19 s (levels) to 0.25 s (★ and stack), and the differential
9.8 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 200 random trees of 1,000 nodes once. In each of
200 rounds it runs the ★ arm on every tree, each round starting from a
different one, and folds the answers into a checksum. Every
implementation prints `200 rounds over 200 trees of 1000 nodes: 14644600
cameras, checksum 690102758`. The Rust tree is LeetCode's
`Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
`shared struct` is, and each visit borrows its node's `RefCell`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.54 to 0.60 s | 0.56 s |
| Rust (`rustc -O`) | 0.67 to 0.74 s | 0.68 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.66 to 0.74 s | 0.69 s |
| Go | 0.58 to 0.72 s | 0.62 s |
| Python | 8.4 s | |
| Kāra (`karac build --mir`) | 0.73 to 0.84 s | 0.75 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 15 times
C's.

v2 took 1.09 times Rust's median time under overflow checks and 1.34
times C's. Under valgrind's cachegrind v2 ran 2.26 billion instructions
and 193 million branches with 37.7 million mispredicted, Rust with
overflow checks 1.95 billion, 196 million and 33.8 million, and C 1.31
billion, 131 million and 37.3 million. Which child is missing, and which
state a subtree reports, are close to coin tosses on a random tree, so
every language spends most of its time on mispredicted branches.
