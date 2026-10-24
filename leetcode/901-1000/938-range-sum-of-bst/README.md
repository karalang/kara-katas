# 938. Range Sum of BST

Given the `root` node of a binary search tree and two integers `low` and
`high`, return the sum of values of all nodes with a value in the
**inclusive** range `[low, high]`.

```
root = [10,5,15,3,7,null,18],          low = 7, high = 15  ->  32
root = [10,5,15,3,7,13,18,1,null,6],   low = 6, high = 10  ->  23
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 2 * 10^4]`; `1 <= Node.val <= 10^5`; `1 <= low <= high <= 10^5`;
all `Node.val` are **unique**.

## Approaches

| file | mechanism |
|---|---|
| `range_sum_bst.kara` ★ | recursion with a `match` on the node: one below `low` has nothing in range on its left, so only its right subtree is searched; one above `high` only its left; one in range adds its value and both subtrees. O(n) at worst, and O(h + k) for a tree of height `h` with `k` values in range |
| `range_sum_bst_stack.kara` | the same search with a stack of its own: a node pushes its left child unless it is below `low` and its right child unless it is above `high`, and adds its value when it is in range. O(n) at worst |
| `range_sum_bst_inorder.kara` | every value collected in order into a list by a recursive walk, then added up from the first at or above `low`, stopping at the first above `high`. O(n) |
| `range_sum_bst_morris.kara` | a Morris walk: in order with no stack, the last node of each left subtree pointed back at the node above it while the walk is inside, and the link removed on the way back, so the tree is left as it was. O(n) time, O(1) space |
| `range_sum_bst_split.kara` | down from the root to the first node in range, where the paths to `low` and to `high` part; on the way to `low`, a node at or above it adds itself and its whole right subtree, which lies between it and the split node; on the way to `high` the same the other way round. O(n) at worst |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and five
more (one node in range, one node out of it, a range holding every node,
a range between two nodes holding none, and a range of one value at the
smallest node); for 300 random trees of 1 to 200 values from 1 to
100,000 put in at random, a value already in the tree being left out,
each with a random range, the values drawn, the sums and a checksum; and
four of LeetCode's largest, 20,000 nodes: distinct values put in at
random, a chain to the right, a chain to the left, and a balanced tree.
`range_sum_bst.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every node of the tree visited level by level, whatever its
place, and the values from `low` to `high` added up. It checks 3,200
random trees, each made by putting in random values in the order drawn,
a value already there being left out, with a random range: 3,000 of up
to 12 values from 1 to 30 against the statement, and 200 of up to 2,000
values from 1 to 100,000 against the other properties, every fourth of
those put in in increasing order and cut to 300 values, which makes a
chain to the right; 171,027 nodes in all.

| | property |
|---|---|
| P1 | the statement's sum, on the small trees |
| P2 | from 0 to the sum of every value, which the range from 1 to 100,000 gives |
| P3 | the range cut in two at a random place gives two sums that add up to it |
| P4 | the sum up to `high`, less the sum up to `low - 1` |
| P5 | the same values put in again in a shuffled order, which makes a tree of another shape, give the same sum |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 trees of 171027 nodes, checksum 596555984, 95000 checks
over 5 arms: 0 failures` under `karac __mir-run` (18.5 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node equal to `low` taken as below | P1 585, P2 592, P3 441, P4 556, P6 591 |
| M2 | ★: a node in range searched on its left only | P1 1177, P2 2730, P3 665, P4 1158, P5 1256, P6 1348 |
| M3 | ★: an empty subtree summing to 1 | P1 3000, P2 3200, P3 2638, P4 3011, P6 3200 |
| M4 | stack: each value in range replacing the total | P1 1522, P2 2936, P3 988, P4 1709, P5 992, P6 1693 |
| M5 | stack: the right child pushed when not below `low` | P1 987, P3 422, P4 1158, P5 927, P6 1158 |
| M6 | stack: the last node on the stack never taken | P1 2282, P2 3200, P6 2454 |
| M7 | inorder: each value before its left subtree | P1 1037, P3 431, P4 842, P5 961, P6 1180 |
| M8 | inorder: each value after its right subtree | P1 1017, P3 440, P4 798, P5 1254, P6 1173 |
| M9 | inorder: each value in range replacing the total | P1 1522, P2 2936, P3 988, P4 1709, P6 1693 |
| M10 | morris: a node with no left child equal to `low` left out | P1 358, P2 592, P3 229, P4 325, P5 221, P6 360 |
| M11 | morris: a node with a left child added only when above `high` | P1 2352, P2 2712, P3 1854, P4 2346, P5 2348, P6 2501 |
| M12 | morris: a node with a left child adding its left child's value | P1 1663, P2 2712, P5 1756, P6 1812 |
| M13 | split: right subtrees on the way to `low` left out | P1 375, P2 1461, P3 322, P4 605, P5 693, P6 516 |
| M14 | split: a split node equal to `low` passed by | P1 287, P2 109, P3 373, P4 408, P5 171, P6 287 |
| M15 | split: the split node itself not counted | P1 2282, P2 3200, P3 988, P4 1709, P5 1179, P6 2454 |

P1 and P6 kill all fifteen, P3 and P4 thirteen, P2 twelve and P5
eleven. P2 misses M5, M7 and M8, which search too much or visit in the
wrong order: on the range from 1 to 100,000, its second question, every
value is in range and each still adds every value once.

P3 and P4 miss M6 and M12, whose answers still add up over the range.
M6 never pops the root, the only node on the stack at first, and so
answers 0 for every range. M12 adds, for a node with a left child, that
child's value in place of its own: the answer is still a sum over the
nodes in range of an amount fixed by the node, so the range cut in two,
or taken as a difference, adds up. P5, whose other tree changes which
nodes have left children, catches it.

P5 misses M1, M3, M6 and M9, whose answers are fixed by the values and
the range whatever the tree's shape. M1 leaves out `low` itself. M3 adds
1 for each empty subtree the search reaches, and a search reaches one
for each gap between the values in range and one past each end, one more
than the number of values in range, in a tree of any shape; P3 and P4
catch it, since cutting the range adds one more. M9, replacing the total
with each value in range, leaves the largest value in range, since the
values come in order; M4, the same edit to the stack arm, leaves the
last value the stack visits, which depends on the shape, and P5 catches
it.

Eight other edits were tried and set aside. Six failed exactly the same
checks as a kept mutant or as each other: ★ searching the right of a
node above `high` and stack pushing the left child when not above
`high`, both as M7; ★ searching the left of a node below `low`, as M5;
inorder leaving out `low` itself, as M1; and stack not adding a node
equal to `high` and inorder stopping at `high` itself, as each other.
Two were sound but beyond three an arm: split taking a node equal to
`high` as above, and split adding whole subtrees on the way to `low`
without their right side.

## Verification

Every arm prints the same output as `range_sum_bst.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 1.1 to 1.7 s each and the
differential 18.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The ★, stack and split arms print the same output under the frozen
legacy interpreter, the legacy JIT and both legacy builds, with and
without auto-par. Legacy refuses the inorder arm and the differential at
the first `*` on an element of a `Vec[i64]`'s `.iter()` ("unary '*'
requires 'ref T', ... found 'i64'"), legacy's older rule, under which
the element is a copy; under v2 it is a reference and the `*` is
required. It has no `ref_eq` for the morris arm: its interpreter stops
at run time ("method 'ref_eq' not found on type 'TreeNode'") and its
code generator refuses it ("no handler for method 'ref_eq'"). Legacy is
frozen, so none of this is filed.

## Benchmarks

The bench program builds 20 trees once, each of 20,000 distinct values
from 1 to 100,000, LeetCode's most, put in in random order, and 50
random ranges for each; in each of 20 rounds it runs the ★ arm on every
range of every tree, each round starting from a different tree, and
folds the sums into a checksum. Every implementation prints `20 rounds
over 20 trees of 20000 nodes, 50 ranges each: sums adding to
1442361705800, checksum 931851745`. Kāra's nodes are a `shared struct`
and Rust's are `Rc<RefCell<...>>`, both counted references; C's and
Go's are plain pointers, and Python's are objects.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, each run including building the
trees:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.13 to 1.21 s | 1.17 s |
| Rust (`rustc -O`) | 1.61 to 1.81 s | 1.68 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.57 to 1.72 s | 1.61 s |
| Go | 1.17 to 1.34 s | 1.23 s |
| Python | 15.0 s | |
| Kāra (`karac build --mir`) | 1.43 to 1.63 s | 1.49 s |
| Kāra (`karac build --legacy`) | 1.61 to 1.86 s | 1.73 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy builds it too, and its
binary prints the same line. Python's run is about 13 times C's.

v2 takes 0.93 times Rust's median time under overflow checks, 0.86
times legacy's and 1.27 times C's. Under valgrind's cachegrind v2 runs
4.66 billion instructions and 0.49 billion branches with 85.1 million
mispredicted, Rust with overflow checks 5.25 billion, 0.67 billion and
77.6 million, legacy 5.62 billion, 0.94 billion and 87.7 million, and C
3.05 billion, 0.38 billion and 80.1 million. All four mispredict about
as often, some 80 million times; that these are the turns left or right
in a tree built in random order, which no predictor can learn, and that
they and the cache misses of walking 20,000 scattered nodes set most of
the time, is inferred, not profiled.
