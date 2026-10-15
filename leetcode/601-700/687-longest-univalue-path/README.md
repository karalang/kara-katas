# 687. Longest Univalue Path

Given the root of a binary tree, return the length of the longest path
in which every node holds the same value. The path need not pass through
the root. Its length is the number of edges between its two ends.

```
root = [5,4,5,1,1,null,5]  ->  2    (5 - 5 - 5)
root = [1,4,5,4,4,null,5]  ->  2    (4 - 4 - 4)
```

**Constraints:** the tree has 0 to 10^4 nodes; -1000 <= `Node.val` <=
1000; the tree is at most 1000 levels deep.

## Approaches

Every arm is `fn longest_univalue_path(root: Option[TreeNode]) ->
i64`, over `shared struct TreeNode { mut val: i64, mut left:
Option[TreeNode], mut right: Option[TreeNode] }`. A node's arm is the
longest path going down from it through nodes of its own value.

| file | mechanism |
|---|---|
| `longest_univalue_path.kara` ★ | one walk bottom up: a node's arm is one more than a matching child's arm, the longer side; a path bends at most once, at its highest node, so the longest through a node is its two arms added, each counted only if the child matches |
| `longest_univalue_path_stack.kara` | the same arms without recursion: number the nodes in preorder with an explicit stack, then fill the arms from the last number back, which meets every child before its parent |
| `longest_univalue_path_naive.kara` | every node as the bend, with a fresh walk down each side to measure how far its value runs; nothing is shared between nodes, so O(nodes x height) |
| `longest_univalue_path_parts.kara` | keep only the edges between a parent and a child of one value, so the tree falls into pieces of one value, and take each piece's longest path with two searches: the farthest node from any node is one end of it |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 13 lines: the two LeetCode examples; six
corners: no tree, one node, a path that bends at the root, two runs of
one value split by another, the longest run below a root of another
value, and negative values; a zigzag of 1,000 nodes of one value, then
with node 600 changed; a full tree of 15 levels of one value; every tree
of 1 to 6 nodes over values 1 and 2, 10,066 in all, counted by answer,
with a checksum; and 1,000 random trees of up to 8 levels, with a
checksum. `longest_univalue_path.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: over every pair of
nodes, climb from both to their lowest common ancestor by parent links
and depths, and keep the longest path, in edges, whose nodes all hold
one value. 1,500 random trees are checked, two thirds of up to 5 levels
and a third of 6 to 10, with one to three values and each child there
with chance 40 to 99 in 100; the 1,000 of up to 5 levels go against the
definition.

| | property |
|---|---|
| P1 | the answer is the definition's (up to 5 levels) |
| P2 | the mirror image answers the same |
| P3 | every value moved by the same amount changes nothing |
| P4 | two trees joined under a root of 0, a value neither holds, answer the larger of their two answers |

It prints `1500 trees (1000 against the definition), 4 arms,
22000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node's arm taken as its bent path | P1 195 |
| M2 | ★: the right child counted when it differs | P1 522, P2 816, P4 731 |
| M3 | stack: a left child recorded as a right one | P1 352, P2 407 |
| M4 | stack: a node's arm only ever its left side | P1 159, P2 476 |
| M5 | naive: a run measured down the left only | P1 159, P2 476 |
| M6 | naive: the right subtree never searched | P1 89, P2 308, P4 431 |
| M7 | parts: the second search from the first start again | P1 256 |
| M8 | parts: a child joined to a parent of a value as large or larger | P1 265 |
| E1 | ★: a tie with the best taken again | 0 |
| E2 | stack: the arms started at -5 | 0 |
| E3 | naive: the two subtrees searched in the other order | 0 |
| E4 | parts: the first search's mark negative | 0 |

P1 kills all eight. P2 sees M2 to M6, the five that treat left and right
apart; M1, M7 and M8 treat both sides alike, so a mirror image changes
nothing for them. P3 sees none: every arm compares values only for
equality, and M8 for order, and a shift keeps both. P4 sees M2 and
M6. The new root's value differs from both its children's, so only a
mutant that counts a differing child, M2, gets the root itself wrong,
and only one that never searches a right subtree, M6, misses the second
tree; the others get each half wrong just as they do alone, so the
joined answer is still the larger of the two. M4 and M5 fail the same
trees, property by property: both measure a run down the left only,
M4 in the stack arm and M5 in the naive one. The four survivors change
no answer. A tie with the best leaves it as it is; every arm in the
stack arm is written before it is read, since a child's number comes
after its parent's, so the starting value is never seen; the larger of
two answers is the same whichever is found first; and a negative mark,
-2 - v, is still one that no other search uses, and never the -1 of a
node not yet seen.

## Verification

Every arm prints the same output as `longest_univalue_path.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`f8fe87fbe5` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy interpreter prints the same output for the ★ and stack
arms. On the naive arm it printed the first eight lines and was stopped
at the 60-second limit, in the zigzag of 1,000 nodes, which that arm
walks about half a million steps through. The legacy JIT and `karac
build` stop the ★, stack and naive arms with a segmentation fault, and
the `KARAC_AUTO_PAR=1` build's output differs too; where was not looked
into. The legacy backends refuse the parts arm and the differential at
type checking, at `*w`, since legacy gives the items of `adj[u].iter()`
by value where v2 gives references. Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random trees of up to
16 levels once, each child there with chance 88 in 100 and values 1 and
2, then answers every tree in each of 30 rounds, putting each answer
into a checksum. Every implementation prints `3000 trees answered,
checksum 778074371`, the Kāra program under `karac __mir-run` included
(in 101 s).

Each implementation is the same recursive walk over trees of linked
nodes built once. Spot timings on a shared 4-core container, six runs
each, three of them interleaved (two for Python; `bench.sh` timings need
a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.34 to 0.43 s |
| Rust (`rustc -O`) | 0.41 to 0.45 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.66 to 0.74 s |
| Go | 0.69 to 0.75 s |
| Python | 10.6 to 11.0 s |
| Kāra (`karac build --mir`) | 0.90 to 1.04 s |
| Kāra, legacy (`karac build`) | 0.82 to 0.93 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; drop `--mir` once that is the default. That edit is
by hand, on top of the `scripts/new-bench.sh` output. The legacy `karac
build` also builds the bench program and it prints the same line, though
the same arm stops with a segmentation fault in the kata's harness; its
row is above. Under `karac __mir-llvm-run` the program prints the same
line in 2.3 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is about 15% behind legacy here, about 2.5 times C and
1.35 times Rust with overflow checks; why was not looked into. Overflow
checks cost Rust about two thirds here, so they may account for part of
the gap to C, which is inferred, not measured. The gap to legacy is
under the M2 bar of 1.5x, so it is noted, not filed. The comparison with
C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
