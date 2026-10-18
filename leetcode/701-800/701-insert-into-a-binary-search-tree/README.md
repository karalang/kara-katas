# 701. Insert into a Binary Search Tree

You are given the `root` node of a binary search tree and a `value` to
insert into it. Return the root node of the tree after the insertion. It
is guaranteed that the new value does not exist in the original tree.
There may be several valid ways to insert, as long as the tree remains a
binary search tree after insertion; any of them may be returned.

```
root = [4,2,7,1,3], val = 5
    ->  [4,2,7,1,3,5]
root = [40,20,60,10,30,50,70], val = 25
    ->  [40,20,60,10,30,50,70,null,null,25]
```

**Constraints:** the number of nodes is in [0, 10^4]; -10^8 <=
`Node.val` <= 10^8; all values are unique; -10^8 <= `val` <= 10^8; `val`
is not in the tree.

## Approaches

Every arm is `fn insert_into_bst(root: Option[TreeNode], val: i64) ->
Option[TreeNode]` over `shared struct TreeNode { mut val, mut left, mut
right }`. Every arm hangs the new value as a leaf where a search for it
falls off the tree, the usual answer, so all four give the same tree and
the output can be compared exactly.

| file | mechanism |
|---|---|
| `insert_into_a_binary_search_tree.kara` ★ | recursion: an empty tree becomes the leaf, otherwise the side one comparison picks is replaced by its own answer; O(height) time and stack |
| `insert_into_a_binary_search_tree_loop.kara` | a loop down to the node whose side is empty, and one link set there; O(height) time, O(1) space |
| `insert_into_a_binary_search_tree_path.kara` | path copying: the nodes from the root to the new leaf are copied and everything off the path is shared, so the given tree is left as it was; O(height) time and new nodes |
| `insert_into_a_binary_search_tree_preorder.kara` | the tree's preorder with `val` appended, inserted one by one into an empty tree, which builds the same tree with the new leaf; O(nodes x height) time |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 16 lines: the LeetCode examples (the third is
the first with trailing nulls) and an empty tree; one node, given a
value on either side; a tree of nine, given values below the smallest,
above the largest and under nodes at depths two to four on either side,
each answer in LeetCode's level order; the even numbers below
20,000 inserted in a random order, the problem's largest, then 50 odd
values inserted one after another, with size, height and checksum before
and after; a chain of 3,000 given a leaf past its far end and then a
left child of its root; and 1,000 random trees of up to 20 values from
-50 to 49, each given a value not in it, into a checksum.
`insert_into_a_binary_search_tree.py` mirrors the ★ arm and its output
is byte-identical. The chain is 3,000 long rather than 10,000 because
the preorder arm rebuilds it in quadratic time.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: the tree that
inserting the values one by one builds, given by partition rather than
by walking down, so the first value is the root, the later smaller
values build its left subtree in their order and the later larger ones
its right. The answer must be the definition's tree for the values with
`val` appended. 3,000 random trees are checked, each from up to
25 values from 0 to a random 1 to 50 (repeats skipped), so some are
empty, some small and dense and some spread out, and `val` is a value
from -2 to the top + 1 that is not among them. Each arm gets a tree of
its own, since three of them change the tree they are given.

| | property |
|---|---|
| P1 | the answer, in level order, is the definition's |
| P2 | read in order, the answer is the old values and `val`, sorted |
| P3 | `val` is a leaf, and with it read as missing the answer is the old tree |
| P4 | the tree of the negated values given `-val` is the answer mirrored left to right and negated |

It prints `3000 trees (109 empty), 4 arms, 48000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Two more edits, E1 and
E2, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the two sides swapped | P1 2891, P2 2891 |
| M2 | ★: the left side's answer thrown away | P1 1439, P2 1439, P4 2891 |
| M3 | ★: the right subtree searched for a smaller value | P1 1902, P2 1902, P3 1902, P4 2702 |
| M4 | loop: the new leaf returned instead of the root, on the left | P1 1439, P2 1439, P3 1439, P4 2891 |
| M5 | loop: the new leaf put over the first right subtree met | P1 1756, P2 1756, P3 1756, P4 2450 |
| M6 | loop: an empty tree stays empty | P1 109, P2 109 |
| M7 | path: the right subtree left out of a copy | P1 1607, P2 1607, P3 1607, P4 2511 |
| M8 | path: the copy given the new value | P1 2110, P2 2110, P3 2110, P4 2891 |
| M9 | path: the copy's left side taken from the right | P1 1933, P2 1933, P3 1933, P4 2702 |
| M10 | preorder: the new value put first | P1 2891, P3 2891 |
| M11 | preorder: right children never collected | P1 2572, P2 2572, P3 2572, P4 2702 |
| M12 | preorder: a new left leaf hung on the right | P1 2743, P2 2743, P3 2631, P4 2891 |
| E1 | preorder: the left child walked before the right | 0 |
| E2 | loop: an equal value sent left | 0 |

P1 kills all twelve. P2 sees every mutant that loses a value or puts one
out of order, which is all but M10: a tree with `val` at its root still
holds the right values in the right order. P3 sees the mutants that
disturb a node already there: searching or copying the wrong subtree
(M3, M7, M9), returning the leaf instead of the root (M4), overwriting a
subtree (M5, M12), a copy taking the new value (M8), `val` made the root
(M10) or a subtree never collected (M11). It cannot see a leaf on the
wrong side of the right node (M1), a leaf lost (M2) or an empty tree
left empty (M6), since the rest of the tree is untouched. P4 sees the
mutants that treat the two sides unlike; swapping them everywhere
(M1), and the mutants that act only on an empty tree or only at the root
(M6, M10), mirror into the same mistake. E1 walks the preorder left
child first: any order with every node after its parent rebuilds the
same tree. E2 sends an equal value left, and the new value never equals
a node's.

## Verification

Every arm prints the same output as
`insert_into_a_binary_search_tree.py` under `karac __mir-run` (the
v2 MIR interpreter) and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output
identical, no error, no leak. The differential prints its line under all
three. `karac check` passes all four arms, the differential and the
bench program. All with the compiler at kara `83fab1e1e8` for the debug
build and `f5c72b653e` for the release build that runs `check` and
`__mir-run`, which differ in no `src` or `runtime` file, with runtime
archives rebuilt after the last `runtime/src` change.

The frozen legacy backends refuse all four arms at type checking, at
`next_random(mut seed)` inside the harness's `shuffled`, whose `seed` is
already a `mut ref`: legacy wants the marker dropped, while on v2 the
marked forward is the spelling (kara B-2026-10-14-25). They refuse the
differential and the bench program at `*v` on the items of `.iter()`,
which legacy gives by value. A copy of the bench program without that
`*` builds and prints the same line; its time is below. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the loop arm, the same in all five languages. It
shuffles 10 orders of the even numbers 0 to 99,998 once; then in each of
5 rounds it grows a tree from each order by inserting the values one at
a time, and puts the tree's height into a checksum. Every implementation
prints `5 rounds of 10 trees grown to 50000: heights sum to
1895, checksum 11202880`, the Kāra program under `karac __mir-run`
included (in 70 s).

Each tree node is a separate allocation in every language, made as its
value is inserted: `malloc` in C, `Box` in Rust, `*TreeNode` in Go, an
object in Python and a `shared struct` in Kāra; each tree is let go
before the next is grown, freed by hand in C, dropped when its root is
replaced in Rust and Kāra, and left to the collector in Go and Python.
Spot timings on a shared 4-core container, eight runs of each compiled
program and seven of the legacy copy, five of each interleaved, and two
of Python (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.58 to 0.68 s |
| Rust (`rustc -O`) | 0.49 to 0.63 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.49 to 0.64 s |
| Go | 0.49 to 0.58 s |
| Python | 3.7 s |
| Kāra (`karac build --mir`) | 0.67 to 0.79 s |
| Kāra, legacy (`karac build`, the copy) | 0.56 to 0.77 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.2 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is behind the others here: by median about 15% behind C
and the legacy build, and about 35% behind Rust and Go. As in kata
700, each step down the tree in Kāra copies a reference-counted `shared`
node, so it probably pays a count up and a count down per step where the
others copy a bare pointer; that is inferred, not measured. The
comparison with C and Rust waits until after M4.

## Compiler findings

None. `karac check` passed all four arms, the harness, the differential
and the bench program as first written.
