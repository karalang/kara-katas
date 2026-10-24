# 988. Smallest String Starting From Leaf

You are given the `root` of a binary tree where each node has a value
in the range `[0, 25]` representing the letters `'a'` to `'z'`.

Return the **lexicographically smallest** string that starts at a leaf
of this tree and ends at the root.

As a reminder, any shorter prefix of a string is lexicographically
smaller. For example, `"ab"` is lexicographically smaller than `"aba"`.

A leaf of a node is a node that has no children.

```
root = [0,1,2,3,4,3,4]          ->  "dba"
root = [25,1,3,1,3,0,2]         ->  "adz"
root = [2,2,1,null,1,0,null,0]  ->  "abc"
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 8500]`; `0 <= Node.val <= 25`.

## Approaches

The tree is a `shared struct TreeNode` with `Option[TreeNode]` children,
as in kata 979. Taking the smaller of the two children's answers and
adding the node's letter is the trap every arm avoids: `"b"` is smaller
than `"ba"`, but under a root `z`, `"baz"` is smaller than `"bz"`.

| file | mechanism |
|---|---|
| `smallest_from_leaf.kara` ★ | a walk carrying the path: a walk down from the root keeps the letters of the path to where it is; at a leaf the path read backwards is that leaf's string, and the answer is the smallest. O(n h), h the height |
| `smallest_from_leaf_bfs.kara` | level by level, each node with its string: a breadth-first walk carries with every node the string from it to the root, its own letter followed by its parent's, and compares the strings it reaches at the leaves. O(n h) |
| `smallest_from_leaf_stack.kara` | a stack, and letters compared in place: a walk with its own stack keeps the path as letter numbers, cut back to each node's depth, and compares it with the best path from the far end letter by letter, so the only string built is the answer. O(n h) |
| `smallest_from_leaf_lists.kara` | every leaf's string, built from below: each subtree returns the strings from all its leaves up to its root, each node adds its letter to the end of every one, and the answer is the smallest string at the root. O(n h) |
| `smallest_from_leaf_suffix.kara` | the smallest below, given what lies above: the recursion is handed the letters above a node, a leaf returns its letter followed by them, and a node the smaller of its children's answers, each handed the node's letter followed by them. O(n h) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines. The first ten are LeetCode's three
examples and seven more: one node; the trap above (`"baz"`); a shorter
string beating one it begins (`"aa"` over `"aaaa"`); a deeper tree;
two leaves with the same string; a path with one leaf (`"wyz"`); and a
shallow leaf beating a deep one on a letter (`"bba"` over `"bbba"`).
Then two trees of LeetCode's largest size, 8,500 nodes: the complete
tree, whose answer has 13 letters, and a zigzag path, whose one string
has 8,500. Then totals over random trees, grown by hanging each node at
the first empty place of a random walk down: 300 of up to 10 nodes over
3 letters, 3,000 of up to 100 over 26, 300 of up to 300 over 2, where
long common prefixes are the rule, and three of 8,500 nodes.
`smallest_from_leaf.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every node is listed with its parent's place in the list,
and from each leaf the letters up the parents to the root make a
string; the answer is the smallest. It checks 3,200 random trees: 3,000
of up to 10 nodes over 3 letters against the statement, and 200 of up
to 500 nodes, over 2 letters and over 26 in turn, against the other
properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 trees |
| P2 | the mirror image has the same strings, so the same answer |
| P3 | a new root `a` above the tree adds `a` to the end of the answer |
| P4 | the answer spells a path from a leaf up to the root |
| P5 | the answer is no greater than the string from a leaf found by stepping down at random |
| P6 | each arm agrees with at least two of the other four |

P3 holds for `a` and not for other letters, which is the trap again:
under a new root `z` the answer `"b"` loses to `"ba"`. A string that
has the answer as a prefix and an `a` next is still beaten by the
answer and an `a`, which is a prefix of it, and any other string the
answer beat keeps losing in the same place. The first draft of the
differential used a random letter and failed P3 on 125 trees in every
arm.

It prints `3200 trees of 64281 nodes: 10264 letters, checksum
189211315, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (8.3 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-seven edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the path read from the root | P1 2064, P3 2837, P4 2057, P5 1039, P6 2250 |
| M2 | ★: a node with one child taken for a leaf | P1 1820, P3 3200, P4 1686, P5 494, P6 1959 |
| M3 | ★: the largest kept | P1 2078, P5 1485, P6 2277 |
| M4 | bfs: a left child's letter added at the far end | P1 1584, P2 2180, P3 1649, P4 1585, P5 462, P6 1769 |
| M5 | bfs: the first leaf kept | P1 1229, P2 1014, P5 654, P6 1422 |
| M6 | bfs: the root's letter dropped | P1 3000, P3 2151, P4 3200, P6 3200 |
| M7 | stack: the longer string taken for the smaller | P1 113, P3 80, P5 44, P6 130 |
| M8 | stack: the path never cut back | P1 1376, P2 2255, P4 1509, P5 356, P6 1570 |
| M9 | stack: the larger letter wins | P1 2031, P3 77, P5 1439, P6 2230 |
| M10 | lists: only the smallest string kept at each node | P1 175, P5 55, P6 216 |
| M11 | lists: a node's letter added twice | P1 3000, P3 3200, P4 3195, P5 1038, P6 3200 |
| M12 | lists: a node with one child starts a string too | P1 1047, P3 3200, P4 1103, P6 1103 |
| M13 | suffix: the left child ignored when both | P1 1293, P2 2246, P5 710, P6 1487 |
| M14 | suffix: a lone left child taken for a leaf | P1 1132, P2 1915, P4 1009, P5 282, P6 1215 |
| M15 | suffix: a lone right child taken for a leaf | P1 1139, P2 1915, P3 3200, P4 1005, P5 307, P6 1227 |

P1 and P6 kill all fifteen, P5 thirteen, P3 and P4 nine each, and P2
six.
M10 is the trap itself, keeping only the smallest string at each node,
and it is wrong on 175 of the 3,000 small trees. Its answer is a real
path, unchanged by the mirror and kept by a new root `a`, so P2, P3
and P4 pass it; P5 catches it on 55 trees, where a leaf found at random
beats it. The mirror keeps every string, so P2 sees only the mutants
that treat the left and the right differently: M4; M5, which keeps
whichever leaf the walk meets first; M8, whose uncut path holds every
node the walk has passed, in the order it passed them; and the three
suffix mutants. P5 misses M6 and M12. M6's answer is no greater than
any leaf's string with the root's letter cut off, a proper prefix and
so smaller than that leaf's string; M12 takes the smallest over more
strings than the leaves', so its answer can only be smaller.

Twelve other edits were tried and set aside. Four failed exactly the
same checks as a kept one: bfs keeping the largest, lists keeping the
largest and suffix taking the larger child, as M3; and suffix putting
the letters above first, as M1. Five were sound but beyond three an
arm: ★ never cutting the path back (which fails exactly M8's checks);
stack keeping the first leaf; stack reading the answer from the root;
lists dropping the right subtree's strings; suffix leaving a node's
own letter out. Two survived and are equivalent: ★
letting a tie replace the best, and suffix letting a tie go right; two
equal strings are the same answer. One crashed in both lanes: bfs never
queueing a right child finds no leaf at all in a tree whose leaves all
lie below right children, and unwraps `None`.

## Verification

Every arm prints the same output as `smallest_from_leaf.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 2.9 s (stack, which builds no
string until the end) to 4.5 s (★, which builds every leaf's string
from its path through an iterator), and the differential 8.3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program grows 20
random trees of LeetCode's largest size, 8,500 nodes over the first 4
letters, once. In each of 100 rounds it runs the arm on every tree,
each round starting from a different one, and folds every answer's
letters into a checksum. Every implementation prints `100 rounds over
20 trees of 8500 nodes: 26800 letters, checksum 835565311`. Each call
walks the tree and builds a fresh string at every leaf, about 3,160
leaves a tree, at a mean depth of 13.5 letters. The Rust tree is
LeetCode's `Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
`shared struct` is.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.348 to 0.530 s | 0.407 s |
| Rust (`rustc -O`) | 0.770 to 0.892 s | 0.815 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.760 to 0.971 s | 0.815 s |
| Go | 0.608 to 0.703 s | 0.671 s |
| Python | 5.3 s | |
| Kāra (`karac build --mir`) | 0.682 to 0.825 s | 0.754 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 7 times
Kāra's.

v2 took 0.93 times Rust's median time under overflow checks and 1.85
times C's. Under valgrind's cachegrind v2 ran 5,334 million
instructions and 974 million branches with 27.0 million mispredicted,
Rust with overflow checks 4,440 million, 712 million and 20.0 million,
and C 2,194 million, 285 million and 18.8 million. The C program keeps
the path as bytes and copies them backwards into each leaf's string,
where Kāra and Rust keep a list of `char` and collect it backwards
into a `String`, encoding each letter as UTF-8 on the way, which fits
their running twice C's instructions (inferred, not traced).
