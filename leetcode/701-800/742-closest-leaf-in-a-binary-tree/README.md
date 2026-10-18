# 742. Closest Leaf in a Binary Tree

Given the `root` of a binary tree whose values are unique and an integer
`k`, return the value of the leaf nearest to the node holding `k`.
Nearest means the fewest edges travelled in the tree, up through parents
as well as down through children, and a leaf is a node with no children.
LeetCode accepts any of several leaves at the same distance; these katas
return the one with the smallest value, so that every arm and every
language prints the same output.

```
root = [1, 3, 2], k = 1                     ->  2  (3 and 2 tie)
root = [1], k = 1                           ->  1
root = [1, 2, 3, 4, null, null, null, 5, null, 6], k = 2  ->  3
```

**Constraints:** 1 to 1000 nodes; 1 <= `Node.val` <= 1000; the values
are unique; some node holds `k`.

## Approaches

The nearest leaf can lie below `k` or past any of its ancestors, so the
arms must look upward as well as down. The trees come as a pool of nodes
in level order, each holding its value and the indices of its children,
which the harness builds from LeetCode's level-order array.

| file | mechanism |
|---|---|
| `closest_leaf_in_a_binary_tree.kara` ★ | give every node its parent, then search breadth first from `k` with children and parent as neighbours; the first layer that holds a leaf holds the nearest ones, and its smallest leaf is returned; O(n) |
| `closest_leaf_in_a_binary_tree_down.kara` | find every node's nearest leaf below it by recursion, and the path from the root to `k`; the answer is the best over `k`'s ancestors of the climb to the ancestor plus that ancestor's nearest leaf below |
| `closest_leaf_in_a_binary_tree_lca.kara` | give every node its parent and depth, and measure every leaf: the two depths less twice the depth of their lowest common ancestor, found by lifting the deeper node and then both; O(n h) |
| `closest_leaf_in_a_binary_tree_enum.kara` | turn the pool into a `shared enum` tree and walk it once; each subtree reports its nearest leaf below and how far its root is from `k`, and each ancestor of `k` offers the way up from `k` and down its other side |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the three LeetCode examples; a full
tree of seven nodes asked at its root and at a leaf; two long branches
asked where one leaf is nearer and where the two tie; a node whose two
leaves are both two edges down; every value of a random tree of
1,000 nodes, as a checksum; the top of a path of 1,000 nodes, whose only
leaf is 999 edges away; and 300 random trees of 1 to 15 nodes, as a
checksum. `closest_leaf_in_a_binary_tree.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which marks every parent and child one edge apart, finds every distance
by Floyd and Warshall's triple loop, and takes the nearest leaf, the
smaller value on a tie. 3,000 random trees are checked, each of 1 to
15 nodes valued by a random order of 1 to n, every node after the first
hung at a random free place under an earlier one, with `k` a random
value; in 1,326 of them `k` is itself a leaf.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the tree mirrored, every node's two children swapped, gives the same answer |
| P3 | every value v renamed 2v + 1, which keeps their order, renames the answer the same way |
| P4 | when `k` has exactly one child, a new leaf of value 100 hung in its free place is the answer exactly when no leaf was a child of `k`, and otherwise the answer stays |

It prints `3000 trees (1326 with k a leaf), 4 arms, 40356 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search never climbing to a parent | P1 103 |
| M2 | ★: the first leaf of the layer returned, not the smallest | P1 198, P2 282, P4 285 |
| M3 | ★: a left child's parent taken as itself | P1 50, P2 99 |
| M4 | down: the climb to an ancestor not counted | P1 326, P4 163 |
| M5 | down: the step to a child not counted | P1 396, P4 532 |
| M6 | down: the root never tried as the ancestor | P1 708, P3 662, P4 134 |
| M7 | lca: the common ancestor's depth taken off once | P1 326, P4 163 |
| M8 | lca: a tie going to the larger value | P1 386, P4 557 |
| M9 | lca: a node with one child taken for a leaf | P1 1402, P4 988 |
| M10 | enum: the step down the other side not counted | P1 99, P2 197, P4 46 |
| M11 | enum: the farther child's leaf taken as the nearest below | P1 1601, P3 551, P4 977 |
| M12 | enum: every climb from k counted one too many | P1 90 |
| E1 | ★: k not marked seen | 0 |
| E2 | down: the starting best holding value 1000000, not 0 | 0 |
| E3 | enum: an empty tree reporting value 7, not 0 | 0 |

P1 kills all twelve. M4 and M7 drop the climb from `k` in two arms and
fail exactly the same checks, since both then rank the leaves by the way
down from the meeting ancestor alone (M7's distance is the true one plus
that ancestor's depth, which differs from M4's by the depth of `k`, the
same for every leaf). P2 sees the edits that treat the two sides
unalike: M2 returns whichever nearest leaf comes first in the layer, and
mirroring changes which, M3 breaks only left children's parents, and
M10 is in the right-hand branch only. P3 sees M6 and M11, which can
return the placeholder value 0 of a search that found nothing (M6 when
`k` is the root and no ancestor is tried, M11 when the empty side of a
one-child node is taken as the nearer), and 0 does not rename to 1 as a
value would. P4 sees every edit that miscounts a distance or a tie,
since a leaf one edge from `k` should beat all others; it misses
M1, M3 and M12, which go wrong only when the nearest leaf lies above
`k`, where the new leaf never is. E1 lets the search return to `k`,
which is no leaf when the search gets that far; E2 and E3 change the
value paired with an unreachable distance, which every real leaf beats.

## Verification

Every arm prints the same output as `closest_leaf_in_a_binary_tree.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` and the release build that runs `check` and `__mir-run` are both
at kara `1d96cab833`, whose last compiler change is `afe886a96d`. The
runtime archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse the ★ arm, the differential and the
bench program at type checking, at a `*` over a vector's `iter()` (`*x`
over a layer's nodes), since legacy gives those by value where v2 gives
references. The other three arms type-check, but every legacy backend
stops at the harness's `to_string().as_str()`: the legacy interpreter
has no `as_str` on a `String`, and legacy code generation does not
support it, so `karac run` and `karac build` fail too. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes a
random tree of 1,000 nodes valued 1 to 1,000 once, each node after the
first hung at a random free place under an earlier one, and in each of
60 rounds swaps the values of two random nodes and asks for the closest
leaf to every value, 60,000 queries in all. Each query builds its parent
table, its marks and its layers afresh as growable arrays, as the ★ arm
does. Every implementation prints `60 rounds of 1000 queries on a
1000-node tree: answers sum to 27928613`, the Kāra program under `karac
__mir-run` included (in 58 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.13 to 0.20 s |
| Rust (`rustc -O`) | 0.17 to 0.21 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.17 to 0.21 s |
| Go | 0.74 to 0.76 s |
| Python | 6.6 s |
| Kāra (`karac build --mir`) | 0.21 to 0.25 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.1 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes about half
as long again as C (0.22 s against 0.15) and a fifth longer than Rust
with or without overflow checks (0.18), and it is well ahead of Go
(0.76). Under valgrind's cachegrind it runs 3.2 billion instructions
against C's 2.3 and Rust's 2.4, and 0.73 billion branches against
0.47 and 0.55, though it mispredicts no more of them (41 million,
against C's 44 and Rust's 41). The legacy build refuses the program, so
there is no legacy time to set against M2's limit; new katas' benches
are outside M2's frozen set in any case. The comparison with C and Rust
waits until after M4.

## Compiler findings

None new.
