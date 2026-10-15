# 654. Maximum Binary Tree

Given a list of distinct integers, build its maximum binary tree: the
root is the largest number, its left subtree is the maximum binary tree
of the numbers to the left of the largest, and its right subtree that of
the numbers to its right. Return the root.

```
nums = [3,2,1,6,0,5]  ->  [6,3,5,null,2,0,null,null,1]
nums = [3,2,1]        ->  [3,null,2,null,1]
```

**Constraints:** 1 to 1,000 numbers, each from 0 to 1,000, all distinct.

## Approaches

Every arm is `fn construct_maximum_binary_tree(nums: Vec[i64]) ->
Option[TreeNode]` over a `shared struct TreeNode`. The harness prints
trees in LeetCode's level order.

| file | mechanism |
|---|---|
| `maximum_binary_tree.kara` ★ | a stack of the tree's right edge; each new number pops the smaller nodes, takes the last popped as its left child, and becomes the right child of the node left on top; O(n) |
| `maximum_binary_tree_split.kara` | the definition, recursively: the largest of the range as the root, the two sides built the same way; O(n^2) on sorted numbers |
| `maximum_binary_tree_insert.kara` | each number inserted from the root, down the right edge to the first smaller node, which becomes its left subtree; O(n^2) on falling numbers |
| `maximum_binary_tree_table.kara` | the recursive definition with each range's largest found in O(1) from a sparse table of `Vec[Vec[i64]]`; O(n log n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: the two LeetCode examples; five more
lists (one number; rising numbers, a chain down the left; the largest in
the middle; a zigzag; and the largest value allowed), each with its tree
in level order; the total height and a checksum of 300 trees of random
orders of 1 to 50 numbers; and three lists of the problem's largest
size, 1,000 numbers, shuffled, rising and falling, each with its height
and checksum. `maximum_binary_tree.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which builds no tree: each number's parent is the smaller of the nearest
larger numbers to its left and right, and it is the right child of one
on its left and the left child of one on its right. The parents read off
each arm's tree are compared with these. Each of 1,000 random lists has
1 to 40 distinct numbers from 0 to 1,000.

| | property |
|---|---|
| P1 | every number has the definition's parent, on the definition's side |
| P2 | read in order, the tree gives back the list |
| P3 | each node is larger than its children |
| P4 | the list reversed gives the mirror image |
| P5 | the root's left subtree is the tree of the numbers before the largest |

P2 and P3 together pin the tree down: a tree whose in-order reading is
the list and whose every node beats its children is the maximum binary
tree, so they are a second definition.

It prints `1000 lists (19792 numbers), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the nodes popped dropped, not kept as the left child | P1 960, P2 960, P4 979, P5 894 |
| M2 | ★: the top of the stack taken as the root | P1 891, P2 891, P4 979, P5 903 |
| M3 | split: the smallest number taken as the root | P1 979, P3 979, P5 979 |
| M4 | split: the number just after the largest left out | P1 959, P2 959, P4 965 |
| M5 | insert: the walk going down past larger nodes' places | P1 979, P3 979, P5 979 |
| M6 | insert: the replaced subtree hung on the right | P1 960, P2 960, P4 979, P5 894 |
| M7 | table: the table holding where the smallest is | P1 979, P3 979, P5 979 |
| M8 | table: the number just before the largest left out | P1 960, P2 960, P4 965, P5 894 |
| E1 | ★: equal numbers popped too | 0 |
| E2 | split: the scan starting at the first number itself | 0 |
| E3 | insert: the walk passing equal nodes too | 0 |
| E4 | table: a range covered by two powers of two even when one would do | 0 |

P1 kills all eight. The mutants fall in two groups. M3, M5 and M7 build
the tree of the SMALLEST instead, which is just as consistent: its
in-order reading is still the list (P2 passes), its mirror is still the
tree of the reversed list (P4 passes), and the root's left subtree is
still the same arm's tree of what comes before (P5 fails only because
the root is no longer the largest); P3 sees every one. The others,
M1, M2, M4, M6 and M8, lose or misplace numbers, so P2 sees them, and
P4 too; P5 misses M4, which loses a number only to the right of the
largest. The four survivors cannot change an answer: the numbers are
distinct, so popping equal numbers, or passing equal nodes, never
happens; a scan that starts at the first number compares it with itself;
and two powers of two that each cover more than half the range cover it
however they overlap.

## Verification

Every arm prints the same output as `maximum_binary_tree.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `abbdbaf131` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the ★ and insert arms read `*x` from `nums.iter()` over a
`Vec[i64]`, which legacy types by value, and the harness of the other
two hands `seed`, already a `mut ref` parameter, on with the `mut`
marker design.md asks for, which legacy rejects. Legacy is frozen, so
these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes eight random orders of the
numbers 0 to 199,999 once; then 100 rounds each build the tree of one,
picked by the round, walk its left and right edges, and put their
lengths into a checksum, the tree being freed before the next is built.
Every implementation prints `8 orders of 200000, 100 rounds: checksum
568163464`, the Kāra program under `karac __mir-run` included (in
139 s).

Each implementation is the same stack. Kāra's nodes are a `shared
struct`, freed when the last handle goes; Rust's
`Rc<RefCell<TreeNode>>`, freed the same way; C's are `malloc`ed and
freed by a walk after each round; Go's and Python's are collected. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine), each including making the
lists:

| | time |
|---|---|
| C (`clang -O3`) | 0.93 to 1.05 s |
| Rust (`rustc -O`) | 1.21 to 1.38 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.22 to 1.31 s |
| Go | 1.05 to 1.10 s |
| Python | 52 to 53 s |
| Kāra (`karac build --mir`) | 1.29 to 1.32 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: it reads `*x` as above, and its parameters are still owned
rather than borrowed, so handing `lists[(r * 3) % inputs]` to
`construct_maximum_binary_tree` moves an element out of a `Vec`. That
edit is by hand, on top of the `scripts/new-bench.sh` output. A copy
outside the kata with `x` for `*x` and a `ref Vec[i64]` parameter builds
under legacy and takes 1.15 to 1.23 s. Under `karac __mir-llvm-run` the
program prints the same line in 4.0 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

So the v2 build is within 15 percent of legacy and level with Rust,
whose nodes are counted the same way. Most of the time is allocating and
freeing 20 million nodes.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
