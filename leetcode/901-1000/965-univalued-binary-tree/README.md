# 965. Univalued Binary Tree

A binary tree is **uni-valued** if every node in the tree has the same
value. Given the `root` of a binary tree, return `true` if the given tree
is uni-valued, or `false` otherwise.

```
root = [1,1,1,1,1,null,1]     ->  true
root = [2,2,2,5,2]            ->  false
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 100]`; `0 <= Node.val < 100`.

## Approaches

| file | mechanism |
|---|---|
| `is_unival_tree.kara` ★ | depth first: every node must hold the root's value, so each subtree is checked against the root's value recursively, stopping at the first node that differs. O(n) time, O(height) stack |
| `is_unival_tree_stack.kara` | the same walk without recursion: a `Vec` of nodes still to see, each compared with the root's value and its children pushed. O(n) time, O(n) space |
| `is_unival_tree_levels.kara` | level order: the tree walked from a `VecDeque`, every node compared with the root's value. O(n) time, O(width) space |
| `is_unival_tree_set.kara` | the set of values: every value gathered into a `Set[i64]`, and the tree is uni-valued exactly when the set holds one value. No early stop. O(n) time and space |
| `is_unival_tree_edges.kara` | every edge: since the tree is connected, it is uni-valued exactly when every parent holds its children's values, so each node is checked against its own children only, never against the root. O(n) time, O(height) stack |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 19 lines: LeetCode's two examples and ten more
(one node, a right child alone, a different right child, a different
root, a path down the left, a different value at the end of a full
deepest level, on a right child whose cousins are missing, at the end of
a right-leaning path and below a gap, and seven nodes all of the largest
value); for 300 random trees
of 1 to 12 nodes, 1,944 nodes in all, how many are uni-valued, by the
number of spoiled picks, and a checksum; one tree of 100 nodes, LeetCode's
largest, with none, one and two spoiled picks; and a path of 100 left
children, then the same path with its deepest node changed. A random
tree has n nodes in a random shape, every value v, except that each
spoiled pick, a node chosen at random with the root among them, is given
a random value from 0 to 99 instead, which may still be v; a single node
is therefore always uni-valued. `is_unival_tree.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair of nodes compared. It checks 3,200 random trees of
four kinds, every value the same, one or two spoiled picks, and every
value 0 or 1 at random: 3,000 of up to 8 nodes against the statement,
and 200 of up to 100 nodes against the other properties; 23,673 nodes in
all, 1,196 trees uni-valued.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | uni-valued exactly when the lowest value is the highest |
| P3 | the same answer for the mirror, and for the tree hung right of a new root holding the root's value |
| P4 | uni-valued exactly when each child holds the root's value and its subtree is uni-valued, the arm asked about the subtrees |
| P5 | a copy with every value made one value is uni-valued; a copy with the leaf at the end of the leftmost path given another value than the root's is not, unless that leaf is the root |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 trees of 23673 nodes, 1196 univalued, checksum
334132604, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(1.7 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac __mir-run`
and `karac __mir-llvm-run` with the same failures; fifteen are kept,
three to each arm, and all fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right subtree never walked | P1 260, P2 333, P3 897, P4 220, P5 365, P6 333 |
| M2 | ★: a larger value taken for the same | P1 857, P2 927, P4 633, P5 1969, P6 927 |
| M3 | ★: either side enough | P1 1206, P2 1285, P3 719, P4 897, P5 1706, P6 1285 |
| M4 | stack: right children never pushed | P1 806, P2 896, P3 1691, P4 563, P5 835, P6 896 |
| M5 | stack: only leaves compared | P1 335, P2 381, P4 247, P6 381 |
| M6 | stack: left children never pushed | P1 773, P2 860, P3 1130, P4 544, P5 1576, P6 860 |
| M7 | levels: a smaller value taken for the same | P1 849, P2 918, P4 646, P6 918 |
| M8 | levels: the last node in the queue never compared | P1 662, P2 669, P3 289, P4 583, P5 802, P6 669 |
| M9 | levels: only the root taken off the queue | P1 1852, P2 2004, P4 1396, P5 2809, P6 2004 |
| M10 | set: two values allowed | P1 1388, P2 1488, P4 1052, P5 1466, P6 1488 |
| M11 | set: leaves never gathered | P1 774, P2 808, P4 439, P5 1613, P6 808 |
| M12 | set: values gathered modulo 50 | P1 11, P2 12, P4 8, P6 12 |
| M13 | edges: the left child compared but not its subtree | P1 262, P2 333, P3 437, P4 218, P5 785, P6 333 |
| M14 | edges: a smaller right child taken for the same | P1 177, P2 186, P3 361, P4 109, P6 186 |
| M15 | edges: the right child compared but not its subtree | P1 241, P2 316, P3 1898, P4 217, P5 188, P6 316 |

P1, P2, P4 and P6 kill all fifteen, P5 eleven (all but M5, M7, M12 and
M14) and P3 eight (M1, M3, M4, M6, M8 and M13 to M15). P3 compares an
arm with itself on the mirror, so it sees only edits that treat the two
sides differently. P5 raises one leaf to the root's value plus one, which
an arm comparing only leaves, only one way round or modulo 50 still
catches; those four are wrong on other trees.

Ten other edits were tried and set aside. Six failed exactly the same
checks as a kept one: stack taking a larger value for the same, as M2;
levels and set leaving out left children, as M6; and levels, set and
edges leaving out the right side, as M4. Four were sound but beyond
three an arm: ★ never walking the left subtree and never comparing a
node with a left child, stack taking the root's value as 0, and levels
letting a 0 match any value. None was equivalent and none crashed.

## Verification

Every arm prints the same output as `is_unival_tree.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit; the build may have picked up an
uncommitted change to the auto-par verdict, which none of these lanes
runs. Under `karac __mir-run` every arm
takes 0.17 to 0.18 s and the differential 1.7 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 200 trees of 100 nodes once, of the four kinds
of the differential in turn, so one tree in four is uni-valued and walked
to the end, and the others stop at their first spoiled node. In each of
4,000 rounds it runs the ★ arm on every tree, each round starting from a
different one, and folds the answers into a checksum. Every
implementation prints `4000 rounds over 200 trees of 100 nodes: 200000
univalued, checksum 272195121`. The Rust tree is LeetCode's
`Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
`shared struct` is, and each visit borrows its node's `RefCell`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.21 to 0.26 s | 0.22 s |
| Rust (`rustc -O`) | 0.30 to 0.34 s | 0.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.30 to 0.32 s | 0.31 s |
| Go | 0.28 to 0.34 s | 0.30 s |
| Python | 4.4 s | |
| Kāra (`karac build --mir`) | 0.083 to 0.114 s | 0.097 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 20 times C's.

v2 took 0.32 times Rust's median time under overflow checks and 0.43
times C's. That is not fewer instructions: under valgrind's cachegrind
v2 ran 911 million instructions and 151 million branches with 28.2
million mispredicted, C 885 million, 149 million and 27.6 million, and
Rust with overflow checks 1.47 billion, 190 million and 29.5 million.
The simulated first-level cache misses do not explain it either, 31.0
million for v2 against 22.2 million for C. Whether a node has a left
child is a coin toss, so most of the time goes to branches cachegrind's
simple predictor misses about as often in every language; how the real
predictor fares on each program's branch layout was not measured, since
the container has no hardware counters.
