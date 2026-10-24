# 951. Flip Equivalent Binary Trees

For a binary tree **T**, we can define a **flip operation** as follows:
choose any node, and swap the left and right child subtrees.

A binary tree **X** is *flip equivalent* to a binary tree **Y** if and
only if we can make **X** equal to **Y** after some number of flip
operations.

Given the roots of two binary trees `root1` and `root2`, return `true`
if the two trees are flip equivalent or `false` otherwise.

```
root1 = [1,2,3,4,5,6,null,null,null,7,8],
root2 = [1,3,2,null,6,4,5,null,null,null,null,8,7]  ->  true
root1 = [], root2 = []                              ->  true
root1 = [], root2 = [1]                             ->  false
```

**Constraints:** the number of nodes in each tree is in the range
`[0, 100]`; each tree will have **unique node values** in the range
`[0, 99]`.

## Approaches

| file | mechanism |
|---|---|
| `flip_equiv.kara` ★ | both pairings tried: two trees are flip equivalent when both are empty, or their roots hold the same value and their children are flip equivalent either as they stand or crossed. With unique values at most one pairing can match at each node, and the other fails at its first comparison. O(n) time, O(height) stack |
| `flip_equiv_strings.kara` | each tree written out in a canonical form, every node's children in a fixed order whatever flips were made: the child with the smaller value first, an empty child before any value. Flips change only which child is left, so the trees are flip equivalent exactly when the strings are the same. O(n^2) at worst for the strings |
| `flip_equiv_parents.kara` | a flip never changes which node a node hangs from. With unique values the trees are flip equivalent exactly when they hold the same values and every value has the same parent in both, the root none: the parents fix each node's two children, and so the tree up to the order of every pair. Each value's parent is recorded in an array of 100. O(n) |
| `flip_equiv_choose.kara` | at each pair of nodes with the same value, the pairing of their children chosen before recursing: as they stand when the left children hold the same value (or are both empty), crossed otherwise, so only one pairing is ever explored. O(n) time, O(height) stack |
| `flip_equiv_queue.kara` | the two trees walked together breadth first, a queue of pairs of nodes that must match: both empty, or the same value with the same two children as an unordered pair of values, the children then queued in the pairing that matches. O(n) time, O(width) space |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's three examples and six
more (one node twice, two different single nodes, a child on either
side, the same grandchild under a child on either side, a grandchild
under different children, and two children against a child and a
grandchild); for 300 random pairs, the
first tree of 0 to 12 nodes, 1,856 nodes in all, how many are flip
equivalent, by the kind of second tree, and a checksum; one pair of
each kind of LeetCode's largest trees, 100 nodes; and a path of 100
nodes against its mirror. The second tree of a pair is a randomly
flipped copy of the first, the same with two values swapped, with a
leaf moved or with a leaf taken off, or another random tree of the same
values. `flip_equiv.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a flip swaps the children of a node, and the first tree is
flip equivalent to the second when some flips make it equal to the
second. Flips at different nodes can be made in any order and a flip
made twice undoes itself, so every set of nodes of the first tree is
flipped in turn and the result compared with the second. It checks
3,200 random pairs of the same five kinds: 3,000 with a first tree of up
to 8 nodes, against the statement, and 200 of up to 100 nodes, against
the other properties; 22,307 nodes in the first trees, 1,573 pairs flip
equivalent.

| | property |
|---|---|
| P1 | the statement's answer, on the small pairs |
| P2 | each tree flip equivalent to itself, and the same answer with the trees the other way round |
| P3 | both trees flipped at random nodes give the same answer |
| P4 | both trees' values renamed the same way give the same answer |
| P5 | when the answer is yes, every value is at the same depth in both trees |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 pairs of trees of 22307 nodes, 1573 flip equivalent,
checksum 902741528, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` (13 s) and `karac __mir-llvm-run`, and the same
under `karac __mir-llvm-asan` with no error.

The leaf taken off was added to the second trees after a first run of
mutants: before it, no pair had one tree empty and the other not, so
queue accepting one empty side (M15 below) survived.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the crossed pairing | P1 714, P2 2539, P3 301, P4 271, P6 752 |
| M2 | ★: the crossed pairing checking one side | P1 392, P2 590, P3 449, P4 456, P5 413, P6 462 |
| M3 | ★: an empty tree matching any tree | P1 952, P5 907, P6 1022 |
| M4 | strings: the value left out of the form | P1 315, P4 98, P5 324, P6 348 |
| M5 | strings: the left child ordered against the node | P1 487, P3 304, P4 418, P6 524 |
| M6 | strings: a child keyed by its last digit | P1 45, P3 42, P4 93, P6 64 |
| M7 | parents: the first root's parent recorded as 0 | P1 1219, P2 2884, P6 1257 |
| M8 | parents: right subtrees never recorded | P1 794, P3 751, P4 713, P5 204, P6 842 |
| M9 | parents: a left child recorded under its grandparent | P1 683, P3 319, P4 325, P5 14, P6 720 |
| M10 | choose: the left child matched against the right | P1 939, P2 2539, P6 977 |
| M11 | choose: the values never compared | P1 264, P3 160, P4 173, P5 276, P6 298 |
| M12 | choose: only the left children checked as they stand | P1 379, P3 455, P4 471, P5 407, P6 451 |
| M13 | queue: the right pair never queued as they stand | P1 111, P3 202, P4 203, P5 155, P6 165 |
| M14 | queue: unmatched children accepted | P1 1253, P5 1271, P6 1411 |
| M15 | queue: one empty side accepted | P1 64, P5 65, P6 65 |

P1 and P6 kill all fifteen, P4 and P5 ten each, P3 nine and P2 four.

P2 kills M1, M2, M7 and M10. M1 and M10 fail a tree against itself
wherever a node has two different children, M1 trying only the crossed
pairing and M10 choosing it, and M7 fails any tree against itself, its
first root having a parent the second does not. M2 checks only one side
of the crossed pairing, which treats the two trees differently, so the
answer can change when they swap. The other eleven treat the two trees
alike and answer yes for a tree against itself.

P3 misses M3, M4, M7, M10, M14 and M15, whose answers do not depend on
which child is left: M3, M14 and M15 still look at both pairings or at
the two children as an unordered pair, M4's form still orders the
children by value, M7 compares parents, which flips never change, and
M10 answers yes only for trees with no node that has a child, where
flips change nothing. P4 misses the same ones less M4: M4 drops the
values from the form but still orders each pair of children by them, so
renaming the values reorders the children and changes the form. The
five P4 misses use the values only to compare them for equality, which
renaming keeps.

P5 misses M1, M5, M6, M7 and M10, whose mistakes only ever answer no
when the answer is yes: M1, M7 and M10 are stricter than the statement,
and the forms of M5 and M6, though not the same for every flip of a
tree, still each write out one flipped version of it, so two equal
forms mean flip equivalent trees. P5 looks only at yes answers. The ten
others can answer yes for trees that are not flip equivalent.

Thirteen other edits were tried and set aside. Nine failed exactly the
same checks as each other, in three groups, so none of them was kept:
four that try only the pairing as the children stand (★ dropping the
crossed pairing, strings never ordering the children, choose always
pairing them as they stand, and queue queueing a crossed match as they
stand); three that give an empty child the value 0, which a node can
hold too (strings, choose and queue); and strings comparing only the
lengths of the forms and parents making each value its own parent. Both
of those last two come down to comparing the values the trees hold: a
form's length depends only on how many values it has and their digits,
and no pair here has different values of the same count. Three were
sound but beyond three an arm: ★ never comparing values, ★ accepting
either side as the children stand, and parents reading a value missing
from the second tree as its root. One was equivalent: strings writing
an empty child as nothing. A subtree still starts with `(` and an empty
one is then just the space before what follows, so a form can still be
read back only one way.

## Verification

Every arm prints the same output as `flip_equiv.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara
`086f304909`. Under `karac __mir-run` the arms take 0.2 to 0.3 s each and
the differential 13 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program builds 20 pairs of trees of 100 nodes once, LeetCode's
largest: each first tree holds the values 0 to 99 in random order, hung
at random, and each second tree is a randomly flipped copy, every
second one with two values swapped. In each of 50,000 rounds it runs
the ★ arm on every pair, each round starting from a different one, and
folds the answers into a checksum. Every implementation prints `50000
rounds over 20 pairs of trees of 100 nodes: 500000 flip equivalent,
checksum 583706802`. The trees are reference counted in Kāra (a
`shared struct`) and in Rust (LeetCode's `Option<Rc<RefCell<TreeNode>>>`),
plain pointers in C and Go, and objects in Python.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.34 to 0.40 s | 0.37 s |
| Rust (`rustc -O`) | 0.47 to 0.54 s | 0.47 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.48 to 0.58 s | 0.52 s |
| Go | 0.44 to 0.53 s | 0.48 s |
| Python | 12.3 s | |
| Kāra (`karac build --mir`) | 1.24 to 1.39 s | 1.31 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 33 times
C's.

v2 takes 2.53 times Rust's median time under overflow checks and 3.52
times C's. Under valgrind's cachegrind v2 runs 9.55 billion
instructions and 1.40 billion branches with 131 million mispredicted,
Rust with overflow checks 5.25 billion, 0.62 billion and 98 million,
and C 3.99 billion, 0.46 billion and 75 million.

The gap is the `match (root1, root2)`. To build the tuple it matches on,
v2 counts both parameters' handles into it on every call and releases
them when the match ends (`clone.Option[shared TreeNode]` twice and one
tuple drop in the function's IR, kept with `KARAC_MIR_LL`), although
the parameters are borrowed and the arms only read them. Written with
nested matches instead (`match root1 { None => root2.is_none(),
Some(a) => match root2 { ... } }`), the same program prints the same
line in 0.38 to 0.40 s, with 3.79 billion instructions and no counts
left. This is kara `B-2026-10-23-13`, filed for kata 558 with the cost
there inferred to be small; the measurement here was sent to its owner.
The kata keeps the tuple match, the natural way to write the problem.
