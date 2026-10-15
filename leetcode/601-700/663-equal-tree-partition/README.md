# 663. Equal Tree Partition

Given the root of a binary tree, return whether removing exactly one
edge can split it into two trees with equal sums of values.

```
root = [5,10,10,null,null,2,3]  ->  true
root = [1,2,10,null,null,2,20]  ->  false
```

In the first, cutting the edge above the right 10 leaves 5 and 10 on one
side and 10, 2 and 3 on the other, 15 each.

**Constraints:** 1 to 10,000 nodes; values from -100,000 to 100,000.

## Approaches

Every arm is `fn check_equal_tree(root: Option[TreeNode]) -> bool`, with
`TreeNode` a `shared struct`. Cutting the edge above a node splits off
that node's subtree, so the answer is whether some subtree other than
the whole tree sums to half the total. The catch is a total of 0, whose
half is the whole tree's own sum, and which only another subtree summing
to 0 can split.

| file | mechanism |
|---|---|
| `equal_tree_partition.kara` ★ | every subtree's sum listed on one walk from the bottom up, the root's, listed last, taken off; O(nodes) |
| `equal_tree_partition_count.kara` | every subtree's sum counted in a `Map`, then one taken back for the root's own; O(nodes) |
| `equal_tree_partition_stack.kara` | the same sums without recursion: a stack of nodes to visit, each marked once its children are pushed, and a stack of finished sums; O(nodes) |
| `equal_tree_partition_inplace.kara` | each node's value replaced by its subtree's sum, then the tree below the root searched for half the total; it changes the tree it is given; O(nodes) |
| `differential.kara` | the four arms against a definition that cuts every edge in turn and adds up both sides, five properties |

Every arm prints the same 13 lines: the two LeetCode examples; one node,
which has no edge to cut; four trees of two or three nodes, three of
them summing to 0, where the whole tree's own sum is half the total and
must not count; a chain of the problem's largest, 10,000 nodes of
1, which splits in the middle, and the same with its last node 2, an odd
total; how many of 300 random trees at most 10 levels deep split, with a
checksum; and three trees of 10,000 nodes or 9,999: one grown at random,
a root of 0 over a tree of 4,999 and its copy, and the same with one
value in the copy raised by 2. Every check is given a tree of its own,
since the in-place arm writes into the tree it is given.
`equal_tree_partition.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which cuts each edge in turn and adds up the two trees it leaves,
O(nodes^2). Each of 1,000 random trees is 1 to 8 levels deep, each child
there with chance 30 to 100 in 100, with values from -3 to 3 so that
equal halves are common: 197 of the trees split. Each arm is handed its
own copy of each tree, since the in-place arm writes into it.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the mirrored tree splits just the same |
| P3 | so does the tree with every value negated |
| P4 | the tree and a copy under a new root of 0 always split |
| P5 | a tree that splits has an even total, so with its root raised by 1 it cannot |

It prints `1000 trees (16502 nodes, 197 split), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the root's own sum not left out | P1 57 |
| M2 | ★: an odd total not turned away | P1 224, P5 341 |
| M3 | count: the root's own sum not taken back out | P1 57 |
| M4 | count: each sum counted once however often it occurs | P1 25, P4 82 |
| M5 | stack: a node's sum without its right subtree's | P1 261, P2 294, P4 693 |
| M6 | stack: the first sum finished left out rather than the root's | P1 51, P2 15 |
| M7 | inplace: the root's right subtree never searched | P1 78, P2 149 |
| M8 | inplace: a node's value written without its right subtree's | P1 255, P2 293, P4 694 |
| E1 | ★: twice the sum compared with the total | 0 |
| E2 | count: the root taken back out when the total is 0 | 0 |
| E3 | stack: the total read without popping it | 0 |
| E4 | inplace: the subtrees searched before the node | 0 |

P1 kills all eight. P2, the mirror, sees the four that treat a node's
two sides differently: M5 and M8 drop a right subtree's sum, M7 never
searches the root's right subtree, and M6 leaves out whichever sum the
walk finishes first, a leaf on the left. P4, two copies under a 0, sees
M5 and M8, and M4, which counts a sum once however often it occurs: when
a copy sums to 0, so do the other copy and the whole tree, and taking
the whole tree's back leaves none. P5 sees M2, which says yes to an odd
total whose rounded-down half some subtree sums to. M1 and M3, which
keep the whole tree's own sum, fail only P1, since they go wrong only on
a total of 0 that no other subtree matches. P3, every value negated,
sees none: negating a tree negates every sum and the total together, and
none of the eight treats the two signs differently; it stays as a check
on the arms themselves. The four survivors cannot change an answer: with
an even total, twice a sum equals it exactly when the sum equals its
half; half the total equals the total only when the total is 0; the last
sum finished is the total whether or not it is popped; and `or` finds a
match in any order.

## Verification

Every arm prints the same output as `equal_tree_partition.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `72739d54d6` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness hands `seed`, already a `mut ref` parameter, on
with the `mut` marker design.md asks for, and the ★ and count arms read
through `*` a value that `iter()` and `get` hand them, which legacy
types as a plain `i64`. Legacy rejects both. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes eight trees once: four of the
problem's largest, 10,000 nodes grown at random, and four of a root of
0 over a tree of 4,999 nodes and its copy, which split. Then each of
4,000 rounds checks one, picked by the round, and puts the answer into a
checksum. Every implementation prints `8 trees of 10000 nodes,
4000 rounds: 2000 split, checksum 317271135`, the Kāra program under
`karac __mir-run` included (in 111 s).

Each implementation is the same walk, each check making a new list of
sums: Kāra's and Rust's a `Vec`, Go's a slice, Python's a list, and C's
a `malloc`ed array grown by `realloc`. Kāra's nodes are a `shared
struct`, Rust's `Rc<RefCell<TreeNode>>`, C's `malloc`ed, and Go's and
Python's collected. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine),
each including making the trees:

| | time |
|---|---|
| C (`clang -O3`) | 0.55 to 0.62 s |
| Rust (`rustc -O`) | 1.09 to 1.18 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.01 to 1.03 s |
| Go | 1.54 to 1.61 s |
| Python | 8.2 to 10.1 s |
| Kāra (`karac build --mir`) | 1.09 to 1.24 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking, for `*s` and the same `mut` marker. That edit
is by hand, on top of the `scripts/new-bench.sh` output. A copy outside
the kata without either builds under legacy and takes 0.93 to 0.98 s.
Under `karac __mir-llvm-run` the program prints the same line in 2.1 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build takes about 1.2 times legacy's time, inside the M2 bar,
and is level with Rust, whose nodes are reference counted too, at about
twice C. The comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
