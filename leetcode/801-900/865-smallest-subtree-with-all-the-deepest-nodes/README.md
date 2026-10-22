# 865. Smallest Subtree with all the Deepest Nodes

Given the `root` of a binary tree, the depth of each node is the
shortest distance to the root. Return the smallest subtree such that it
contains all the deepest nodes in the original tree. A node is called
the deepest if it has the largest depth possible among any node in the
entire tree. The subtree of a node is that node, plus the set of all
descendants of that node.

```
root = [3,5,1,6,2,0,8,null,null,7,4]  ->  [2,7,4]
root = [1]                            ->  [1]
root = [0,1,3,null,2]                 ->  [2]
```

**Constraints:** the tree has 1 to 500 nodes; `0 <= Node.val <= 500`;
the values are unique. (The same problem as LeetCode 1123, Lowest Common
Ancestor of Deepest Leaves.)

## Approaches

| file | mechanism |
|---|---|
| `subtree_with_all_deepest.kara` ★ | one recursive pass: `deepest(node)` returns how deep the subtree under `node` goes and the root of the smallest subtree holding all of that subtree's deepest nodes. When both children go equally deep, deepest nodes lie on both sides and only the node itself holds them all; otherwise the answer is the deeper child's. O(n) time, O(height) stack |
| `subtree_with_all_deepest_depths.kara` | depths first, then the answer: one walk records every node's depth in a `Map` by value, and the largest; `answer(node)` returns the node when it is one of the deepest, the node when both children's answers exist, and otherwise the one that does. O(n) |
| `subtree_with_all_deepest_climb.kara` | a breadth-first search records every parent by value and ends on the deepest level; since those nodes all lie at one depth, moving each of them up a step at a time, shared parents kept once, reaches their lowest common ancestor exactly when one node is left. O(n) |
| `subtree_with_all_deepest_paths.kara` | a depth-first search keeps the path from the root and saves a copy at every leaf as deep as the deepest saved so far (clearing them at a deeper one); the answer is the last node every saved path shares. O(n * leaves) at worst |
| `subtree_with_all_deepest_iter.kara` | the ★ arm's pass without recursion: an explicit stack walks the tree in post-order, each node pushed once to be expanded and again to be finished, and a finished node's (height, answer) comes from its children's, kept in a `Map` by value |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's three examples; seven
more (a root with two leaves, a perfect tree of seven nodes, a chain to
the left and one to the right, two deepest nodes in different subtrees
of the root, two below one child of the root, and two below a node two
levels down); four random trees of 500 nodes, LeetCode's largest, with
the answer's value and size; and 1,000 random trees of 1 to 60 nodes,
whose answers hold 6,769 nodes in all, with a checksum of their level
orders. `subtree_with_all_deepest.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every node's depth, the nodes at the largest one, and, of the
nodes whose subtree holds every one of those, the one whose subtree has
the fewest nodes. Its 3,055 trees are every shape of one to eight nodes
(2,055 of them), each with its values shuffled, and 1,000 random trees
of up to 40 nodes; their answers hold 8,506 nodes in all.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the mirrored tree gives the same answer |
| P3 | every value raised by n raises the answer by n |
| P4 | a new leaf hung under a deepest node is the only deepest node, so it is the answer |
| P5 | a new leaf hung two or more levels above the deepest changes nothing (when the tree has a node there with a free side) |
| P6 | on the answer's own subtree the answer is its root |

It prints `3055 trees, answers of 8506 nodes in all, 91005 checks over 5
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: equal depths answered by the left side | P1 3055, P2 3055, P3 3055, P4 3055, P5 2926, P6 3055 |
| M2 | ★: the shallower side's answer kept | P1 2635, P2 2632, P3 2635, P4 3055, P5 2585 |
| M3 | ★: a right-heavy node given the left height | P1 1675, P2 1689, P3 1675, P4 1664, P5 1957, P6 322 |
| M4 | depths: deepest taken one level up | P1 2448, P2 2448, P3 2448, P4 3055, P5 2447, P6 2205 |
| M5 | depths: one side enough to join | P1 2868, P2 2868, P3 2868, P4 3055, P5 2799 |
| M6 | depths: the empty side's answer kept | P1 2846, P2 2850, P3 2846, P4 3055, P5 2784, P6 429 |
| M7 | climb: stopped at two nodes | P1 850, P2 850, P3 850, P5 817, P6 850 |
| M8 | climb: right children never visited | P1 2920, P2 2926, P3 2920, P4 2866, P5 2849, P6 850 |
| M9 | climb: a single deepest node not reached | P1 2602, P2 2602, P3 2602, P4 3055, P5 2424 |
| M10 | paths: a deeper leaf keeps the old paths | P1 1599, P2 1612, P3 1599, P4 1858, P5 2041, P6 50 |
| M11 | paths: one node past the shared part | P1 850, P2 850, P3 850, P5 817, P6 850 |
| M12 | paths: every leaf kept | P1 1575, P2 1563, P3 1575, P4 1896, P5 2028 |
| M13 | iter: equal heights answered by the right side | P1 850, P2 850, P3 850, P5 817, P6 850 |
| M14 | iter: a left-heavy node's height not counted | P1 1132, P2 1126, P3 1132, P4 1544, P5 1299, P6 289 |
| M15 | iter: the right height read from the left child | P1 2868, P2 2868, P3 2868, P4 3055, P5 2799 |

P1, P2, P3 and P5 each kill all fifteen. M7, M11 and M13 are one fault,
a node with deepest nodes on both sides answered by one child, and fail
the same 850 trees; P4 cannot see it, since after P4's new leaf only one
node is deepest. M5 and M15 are another, every node answering itself
where it should pass the question down. A first M15, a missing child
counted as tall as a leaf, survived: it raises every height by one
alike, so no comparison changes, and it was replaced.

## Verification

Every arm prints the same output as `subtree_with_all_deepest.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `3208abb724`. Under `karac
__mir-run` the arms take under a second each and the differential 9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The `depths` arm compares the depth `Map.get` returns with `(depth.get(
n.val) ?? 0) == most`, the spelling docs/library/collections.md gives
for a `Copy` value: `get` returns an `Option[ref i64]`, and `karac check`
refuses to compare it with `Some(most)`, an `Option[i64]`, which the
spec does not allow either.

The frozen legacy backends refuse all five arms and the differential at
a `*` on a `for` element or on an entry a `Map` returns, saying the
value is not a reference, where v2 yields a reference. Legacy `karac
build` builds the bench program, and the binary aborts before it
prints with `malloc_consolidate(): unaligned fastbin chunk detected`, a
corrupted heap. Legacy is frozen, so both are noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: a random tree
of 500 nodes, LeetCode's largest, built once, and 300,000 rounds that
each hang a new leaf on a random node with a free side, find the
smallest subtree with all the deepest nodes, and take the leaf off
again, so every round walks all 501 nodes. Rust uses LeetCode's tree
type, `Option<Rc<RefCell<TreeNode>>>`, and returns the answer as a cloned
`Rc`; C and Go use plain pointers. Every implementation prints `300000
rounds on 500 nodes: answers sum to 83595059, checksum 445492447`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.71 to 0.76 s | 0.73 s |
| Rust (`rustc -O`) | 0.93 to 0.98 s | 0.96 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.84 to 1.03 s | 0.89 s |
| Go | 0.62 to 0.67 s | 0.64 s |
| Python | 17.9 s | |
| Kāra (`karac build --mir`) | 1.37 to 1.47 s | 1.43 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 864's does. The frozen legacy `karac build`
binary aborts (see Verification), so there is no legacy time.

v2 takes 1.6 times Rust's median time under overflow checks, and 2.0
times C's. Under valgrind's callgrind nearly all of every program's
time is in the recursive `deepest`: C runs 6.46 billion instructions,
Rust with overflow checks 9.40 billion and v2 12.55 billion, with 545
million, 1,174 million and 1,693 million branches and almost no
indirect ones. Where v2's extra instructions go inside `deepest` was not
traced; the comparison with C and Rust waits until after M4.
