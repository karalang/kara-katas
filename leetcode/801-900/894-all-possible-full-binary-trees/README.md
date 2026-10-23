# 894. All Possible Full Binary Trees

Given an integer `n`, return a list of all possible full binary trees
with `n` nodes. Each node of each tree in the answer must have
`Node.val == 0`.

Each element of the answer is the root node of one possible tree. You
may return the final list of trees in any order.

A full binary tree is a binary tree where each node has exactly `0` or
`2` children.

```
n = 7  ->  [[0,0,0,null,null,0,0,null,null,0,0],[0,0,0,null,null,0,0,0,0],
            [0,0,0,0,0,0,0],[0,0,0,0,0,null,null,null,null,0,0],
            [0,0,0,0,0,null,null,0,0]]
n = 3  ->  [[0,0,0]]
```

**Constraints:** `1 <= n <= 20`.

## Approaches

A full tree of `n` nodes is a single leaf, or a root over a full left
subtree of some odd size `l` and a full right subtree of `n - 1 - l`
nodes; so an even `n` has no full tree, and an odd one has the Catalan
number C((n - 1) / 2) of them, 4,862 for 19 nodes. The arms differ in
how they build them.

| file | mechanism |
|---|---|
| `all_possible_fbt.kara` ★ | recursion with a memo: the trees of `n` are a root over every pair of a tree of `l` nodes and one of `n - 1 - l`, for each odd `l`; each size is built once and kept in a `Map`, and the trees share those subtrees, as LeetCode's answers do. O(the trees of every size up to n) |
| `all_possible_fbt_plain.kara` | the same recursion with no memo: each call builds the trees of its size afresh, so the small trees are built over and over |
| `all_possible_fbt_table.kara` | a table built upwards: the trees of 1 node, then of 3, 5 and so on up to `n`, each size from the smaller ones already in a `Vec[Vec[TreeNode]]` |
| `all_possible_fbt_grow.kara` | leaves grown two at a time: every full tree of `n` nodes comes from one of `n - 2` by giving one leaf two children, so each leaf of each tree is grown in a copy, `(n - 1) / 2` times from a single node, and a `Set` of the copies' shapes, written in preorder, keeps each tree once |
| `all_possible_fbt_codes.kara` | every preorder code: a full tree written in preorder as 1 for a node with children and 0 for a leaf is a string of `n` symbols in which the subtrees still owed reach 0 only at the end; each such string is generated and decoded into a tree |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples and three
more (`n` = 1, 2 and 5), each list of trees in LeetCode's level order
and sorted, since LeetCode takes them in any order; the number of trees
for every `n` from 1 to 20, LeetCode's largest; and the 6,918 trees in
all with a checksum of their level orders. `all_possible_fbt.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every binary tree of `n` nodes, a root over each split of the
other `n - 1` between a left and a right subtree of any size including
none, kept when every node has 0 or 2 children. It asks every arm for
every `n` from 1 to 20, the statement for `n` up to 9.

| | property |
|---|---|
| P1 | the statement's trees, for `n` up to 9 |
| P2 | every tree has `n` nodes, every value 0, and every node 0 or 2 children |
| P3 | no tree twice, and C((n - 1) / 2) of them for odd `n`, none for even |
| P4 | the mirror image of every tree is among them |
| P5 | every left subtree is one of the arm's own trees of its size, and the trees whose left subtree has `l` nodes number the arm's trees of `l` times its trees of `n - 1 - l` |
| P6 | each arm agrees with at least two of the other four |

Trees are compared by their level orders, sorted. P2 to P6 are checked
for every `n`. It prints `n from 1 to 20, 6918 trees, 545 checks over 5
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed. The counts are of the
cases, one for each `n` and arm, that a property fails.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last split skipped | P1 4, P3 9, P5 1, P6 9 |
| M2 | ★: the left subtree used on both sides | P1 3, P2 8, P3 7, P5 7, P6 8 |
| M3 | ★: each size kept under the size two larger | P1 3, P2 8, P3 8, P4 6, P5 8, P6 8 |
| M4 | plain: the first split skipped | P1 4, P3 9, P5 1, P6 9 |
| M5 | plain: three nodes taken for a single leaf | P1 5, P2 10, P3 9, P5 18, P6 10 |
| M6 | plain: the right subtree one node short | P1 4, P3 9, P5 1, P6 9 |
| M7 | table: the answer read one size too low | P1 9, P2 10, P3 20, P5 17, P6 20 |
| M8 | table: no trees of 15 nodes or more | P3 3, P5 3, P6 3 |
| M9 | table: every other split skipped | P1 3, P3 8, P4 8, P5 8, P6 8 |
| M10 | grow: a tree grown twice kept twice | P1 2, P3 7, P5 7, P6 7 |
| M11 | grow: the last leaf never grown | P1 4, P3 9, P5 1, P6 9 |
| M12 | grow: the leaves passed never counted | P1 3, P2 8, P3 7, P5 7, P6 8 |
| M13 | codes: a code kept before it reaches `n` symbols | P1 4, P2 9, P3 9, P5 8, P6 9 |
| M14 | codes: the right child a second handle on the left | P1 3, P2 8, P3 7, P5 7, P6 8 |
| M15 | codes: no node given children | P1 4, P3 9, P5 1, P6 9 |

P3 and P6 kill all fifteen, and P1 all but M8, whose fault starts above
the 9 nodes the statement is checked to. The mutants that leave trees
out (M1, M4, M6, M11, M15) all leave none at all from 3 nodes up, so
P3's count fails for the nine odd sizes from 3 to 19, while P2 and P4
hold, as an empty list has no tree of the wrong shape and is its own
mirror. Those that build trees of the wrong size or shape (M2, M5, M12,
M13, M14) fail P2. P4 kills only M3 and M9, the two that keep a
lopsided set of trees.

Two mutants were replaced. The first M9 made the right subtree as large
as the left in the table arm, so each size's trees were built from
trees twice as large as the size before, and the differential grew past
6 GB before it was stopped. The first M12 grew a leaf with only a left
child, and the arm's own `unwrap()` of the right child then stopped the
program, so the differential never reached a property.

## Verification

Every arm prints the same output as `all_possible_fbt.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 2.0 to 4.5 s
each (the grow arm, which builds every tree once for each of its leaves
and writes out each copy's shape, is the slow one) and the differential
25 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every frozen legacy lane, the interpreter, the JIT and `karac build
--legacy` with and without auto-par, refuses all five arms, the
differential and the bench program: `*l` on an element of `.iter()` is
rejected, because legacy's iterator gives the value itself. Legacy is
frozen, so this is not filed.

## Benchmarks

The bench program uses the ★ arm, recursion with a memo whose trees
share their subtrees, asked 1,500 times for every full tree of 19
nodes, the largest odd `n` LeetCode allows; each of the 4,862 trees is
walked in preorder into a checksum. The memo is a hash map in Kāra,
Rust, Go and Python and an array of 21 lists in C; it is consulted
about a hundred times a call, against the 6,918 nodes a call makes and
the 92,378 a call's walk visits. Kāra's nodes are a reference-counted
`shared struct`, Rust's LeetCode's `Rc<RefCell<TreeNode>>`, Go's
pointers left to its collector, and C's `malloc`'d nodes kept in a list
and freed together at the end of each call. Every implementation prints
`1500 calls for 19 nodes: 7293000 trees, checksum 311085398`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.87 to 1.00 s | 0.97 s |
| Rust (`rustc -O`) | 1.24 to 1.40 s | 1.28 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.10 to 1.31 s | 1.21 s |
| Go | 1.11 to 1.35 s | 1.22 s |
| Python | 18.7 s | |
| Kāra (`karac build --mir`) | 1.06 to 1.19 s | 1.13 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 893's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 0.93 times Rust's median time under overflow checks and 1.17
times C's. Under valgrind's cachegrind C runs 7.92 billion instructions
and mispredicts 3.4% of its branches, Rust with overflow checks 9.92
billion and 4.8%, and v2 9.64 billion and 4.2%. The two Rust builds'
ranges overlap, so the plain build's higher median is noise rather than
a cost of skipping the checks. Where the time goes inside each program
was not measured. The comparison with C and Rust waits until after M4.
