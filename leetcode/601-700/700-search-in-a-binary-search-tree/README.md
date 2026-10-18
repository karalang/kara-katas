# 700. Search in a Binary Search Tree

You are given the `root` of a binary search tree and an integer `val`.
Find the node whose value equals `val` and return the subtree rooted at
that node. If there is no such node, return `null`.

```
root = [4,2,7,1,3], val = 2  ->  [2,1,3]
root = [4,2,7,1,3], val = 5  ->  []
```

**Constraints:** the number of nodes is in [1, 5000]; 1 <= `Node.val` <=
10^7; `root` is a binary search tree; 1 <= `val` <= 10^7.

## Approaches

Every arm is `fn search_bst(root: Option[TreeNode], val: i64) ->
Option[TreeNode]` over `shared struct TreeNode { mut val, mut left, mut
right }`, and returns the node itself, not a copy, so its subtree comes
with it.

| file | mechanism |
|---|---|
| `search_in_a_binary_search_tree.kara` ★ | one comparison says which side `val` can be on; recurse into that side until the node holding it or an empty side; O(height) time and stack |
| `search_in_a_binary_search_tree_loop.kara` | the same walk as a loop, since the recursion is a tail call; O(height) time, O(1) space |
| `search_in_a_binary_search_tree_levels.kara` | the order ignored: every node from a queue, level by level, until one holds `val`; right for any binary tree; O(nodes) time, O(width) space |
| `search_in_a_binary_search_tree_inorder.kara` | an in-order walk with a stack lists the nodes sorted by value, and a binary search over the list finds `val`; O(nodes) time and space |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 16 lines: the two LeetCode examples; one node,
searched for its value and another; a tree of nine, searched for its
root, a leaf, values below the smallest and above the largest, and inner
nodes at depths two and three, each answer in LeetCode's level order;
0 to 4,999 inserted in a random order, its size, height and checksum,
and 400 searches of it into a checksum of every subtree found; a chain
of 5,000 searched at its far end, its root and past its end; and
1,000 random trees of up to 20 values, each searched once, into a
checksum. `search_in_a_binary_search_tree.py` mirrors the ★ arm and its
output is byte-identical. The random trees hold 0 and the differential's
negated trees hold values below it, outside LeetCode's range; no arm
depends on the sign of a value.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: look at every node
in preorder, without using the order of the tree, and answer the first
whose value is `val`. 3,000 random trees are checked, each from up to
25 values from 0 to a random 1 to 50, so some are small and dense with
repeated values and some spread out; half the time the value searched
for is one of them, otherwise any from -2 to 51.

| | property |
|---|---|
| P1 | the answer, in level order, is the definition's |
| P2 | nothing is found exactly when `val` was never inserted |
| P3 | searching the answer again for `val` finds the answer itself |
| P4 | in the tree built from the negated values, `-val` finds the answer mirrored left to right and negated |

It prints `3000 trees (1659 with val in them), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the two sides swapped | P1 1313, P2 1313 |
| M2 | ★: always the left side | P1 987, P2 987, P4 680 |
| M3 | ★: a copy of the node found, without its subtrees | P1 994 |
| M4 | loop: the two sides swapped | P1 1313, P2 1313 |
| M5 | loop: the whole tree when val is missing | P1 1214, P2 1214 |
| M6 | loop: stops at the first node not below val | P1 1392, P2 433, P4 2527 |
| M7 | levels: stops at the first node not below val | P1 1392, P2 433, P4 2527 |
| M8 | levels: left children never queued | P1 959, P2 959, P4 680 |
| M9 | levels: every other node in the queue skipped | P1 1114, P2 1114, P4 374 |
| M10 | inorder: right subtrees never walked | P1 987, P2 987, P4 680 |
| M11 | inorder: the search lands past the run of equal values | P1 1659, P2 1659 |
| M12 | inorder: the next larger node when val is missing | P1 433, P2 433, P4 1214 |

P1 kills all twelve. P2 sees all but M3: a copy of the right node
without its subtrees is still something found. P3 sees none: searching a
mutant's answer again makes the same mistake on a smaller tree, and
finds the same answer. P4 sees the mutants that treat the two sides of a
node unlike, because mirroring swaps them: always going left
(M2), stopping at a node not below `val` (M6, M7), never queuing left
children or walking right subtrees (M8, M10), skipping every other
queued node (M9), and the next larger node for a missing value
(M12), which mirrored becomes the next smaller.

## Verification

Every arm prints the same output as `search_in_a_binary_search_tree.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints its line under all three. `karac check`
passes all four arms, the differential and the bench program. All with
the compiler at kara `83fab1e1e8` for both the debug build and the
release build that runs `check` and `__mir-run`, with runtime archives
rebuilt after the last `runtime/src` change.

The frozen legacy backends refuse all four arms at type checking, at
`next_random(mut seed)` inside the harness's `shuffled`, whose `seed` is
already a `mut ref`: legacy wants the marker dropped, while on v2 the
marked forward is the spelling (kara B-2026-10-14-25). They refuse the
differential and the bench program at `*v` and `*q` on the items of
`.iter()`, which legacy gives by value. A copy of the bench program
without that `*` builds, and aborts in glibc's allocator
(`malloc_consolidate(): unaligned fastbin chunk detected`) before it
prints anything, so legacy has no time below. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the loop arm, the same in all five languages. It
builds 10 binary search trees of 50,000 nodes once, each from the even
numbers 0 to 99,998 inserted in its own random order; then in each of
5 rounds it searches every tree for the same 40,000 random values from
0 to 99,999, about half of them there, and puts every value found into a
checksum. Every implementation prints `5 rounds of 10 trees of
50000, 40000 searches each: 1002900 found, checksum 572034019`, the Kāra
program under `karac __mir-run` included (in 91 s).

Each tree node is a separate allocation in every language, made in the
order the values are inserted: `malloc` in C, `Box` in Rust, `*TreeNode`
in Go, an object in Python and a `shared struct` in Kāra. Spot timings
on a shared 4-core container, eight runs of each compiled program, five
of them interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.56 to 0.65 s |
| Rust (`rustc -O`) | 0.56 to 0.66 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.57 to 0.68 s |
| Go | 0.52 to 0.57 s |
| Python | 3.1 to 3.6 s |
| Kāra (`karac build --mir`) | 0.74 to 0.79 s |
| Kāra, legacy (`karac build`, the copy) | aborts |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.3 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is about 30% behind C and Rust here and 40% behind Go,
by median. Each step down the tree in Kāra copies a reference-counted
`shared` node, so it probably pays a count up on the new node and a
count down on the old one where the others copy a bare pointer; that is
inferred, not measured. The comparison with C and Rust waits until after
M4.

## Compiler findings

None on v2. `karac check` passed all four arms, the harness, the
differential and the bench program, once the bench passed each tree as
`search_bst(root, *q)` rather than `search_bst(*root, *q)`: `root` is
already a borrow of the `Option` in the vector, and v2 refuses moving it
out with `*` (`borrow_projection_copy`).
