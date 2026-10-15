# 671. Second Minimum Node In a Binary Tree

In a non-empty binary tree of non-negative values, every node has either
no children or two, and a node with children holds the smaller of their
two values. Return the second smallest distinct value in the tree, or
-1 if there is none.

```
root = [2,2,5,null,null,5,7]  ->  5
root = [2,2,2]                ->  -1
```

**Constraints:** 1 to 25 nodes; values from 1 to 2^31 - 1.

## Approaches

Every arm is `fn find_second_minimum_value(root: Option[TreeNode]) ->
i64` over a `shared struct TreeNode`. The tree's rule makes the root the
smallest value, and each subtree's root the smallest in that subtree,
which lets three of the arms stop early.

| file | mechanism |
|---|---|
| `second_minimum_node_in_a_binary_tree.kara` ★ | a recursive walk: a node larger than the root is a candidate and ends the walk there; one equal to it sends the walk into both children; O(nodes) |
| `second_minimum_node_in_a_binary_tree_values.kara` | every value collected and sorted, the first larger than the smallest taken; the tree's rule unused; O(nodes log nodes) |
| `second_minimum_node_in_a_binary_tree_levels.kara` | the same pruning level by level, from a queue; O(nodes) |
| `second_minimum_node_in_a_binary_tree_children.kara` | at each node, the child with a larger value is a candidate and only the child with the node's own value is searched further, both when they are equal; O(nodes) |
| `differential.kara` | the four arms against a definition from the wording alone, five properties |

Every arm prints the same 13 lines: the two LeetCode examples; six more
small trees (one node; the second value on the right, deep down, or at
the largest value allowed; a tree of one value; and one where the second
value lies deep below copies of the root's while larger values sit
nearer the top); four full trees of 16 levels, far larger than the
problem allows, whose children differ from their parent never, rarely or
often; and a checksum of 1,000 random trees up to 6 levels deep, with
how many have no second value. `second_minimum_node_in_a_binary_tree.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which ignores the tree's shape: it finds the smallest value, then the
smallest value larger than that. Each of 2,000 random trees follows the
problem's rule, 1 to 7 levels deep, values from 1 to 5, a node having
two children with chance 70 in 100, one of them holding its value and
the other that plus 0 to 3.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the tree turned left to right gives the same answer |
| P3 | every value raised by 1,000 raises the answer by 1,000, or leaves it -1 |
| P4 | the answer is -1 exactly when the tree holds one value |
| P5 | otherwise it is a value in the tree, larger than the root's |

It prints `2000 trees (19160 nodes, 1171 with no second value), 4 arms,
40000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node equal to the root taken as a candidate | P1 2000, P4 1171, P5 2000 |
| M2 | ★: the larger of the two subtrees' candidates kept | P1 288 |
| M3 | values: the values left unsorted | P1 153, P2 226 |
| M4 | values: the first value no smaller than the first | P1 2000, P4 1171, P5 2000 |
| M5 | levels: the first candidate kept, not the smallest | P1 164, P2 33 |
| M6 | levels: left children never queued | P1 456, P2 667, P4 355 |
| M7 | children: equal children treated as differing | P1 827, P4 406, P5 827 |
| M8 | children: below a larger child, the search stopped | P1 79, P2 116 |
| E1 | ★: the smaller candidate by an if | 0 |
| E2 | values: larger than the first as different from it | 0 |
| E3 | levels: a candidate equal to the best taken again | 0 |
| E4 | children: the smaller child as at most the other | 0 |

P1 kills all eight. P2, the tree turned left to right, sees the four
whose answer depends on which side is which: M3 takes the first larger
value in the order of its walk, M5 the first candidate in level order,
M6 never looks left, and M8 stops searching on one side. P4 and P5 see
the three that can answer with the root's own value, M1, M4 and M7, and
P4 also sees M6, which misses a tree's only other value when it lies to
the left. P3, every value raised, sees none: no arm uses a value except
to compare it with another, so raising them all moves every answer,
right or wrong, by the same amount; it stays as a check on the arms
themselves. M2, which keeps the larger of two candidates, passes
everything but P1, since its answer is still a value in the tree larger
than the root's. The four survivors cannot change an answer: an `if`
picks the same smaller value as `min`; in sorted order, the first value
different from the first is the first larger one; a candidate equal to
the best changes nothing; and equal children are handled before the
comparison that E4 widens.

## Verification

Every arm prints the same output as
`second_minimum_node_in_a_binary_tree.py` under `karac __mir-run` (the
v2 MIR interpreter) and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output
identical, no error, no leak. The differential prints its line under all
three. `karac check` passes all four arms, the differential and the
bench program. All with the compiler at kara `8d40e1a762` for the debug
build and `85dccd703c` for the release build that runs `check` and
`__mir-run`, with runtime archives newer than the last `runtime/src`
change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness's `special` hands `seed`, already a `mut ref`
parameter, on with the `mut` marker design.md asks for, which legacy
rejects. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 16 full trees of 16 levels,
65,535 nodes each, once: in four of them every value is the same, so the
walk visits every node, and in the rest a child differs from its parent
half the time or more, so the walk stops early. Then each of
2,000 rounds asks one, picked by the round, and puts the answer into a
checksum. Every implementation prints `16 trees of 65535 nodes,
2000 rounds: checksum 409688974`, the Kāra program under `karac
__mir-run` included (in 60 s).

Each implementation is the same recursive walk over trees made once.
Kāra's nodes are a `shared struct`, Rust's `Rc<RefCell<TreeNode>>`, C's
`malloc`ed, and Go's and Python's collected. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine), each including making the trees:

| | time |
|---|---|
| C (`clang -O3`) | 0.19 to 0.20 s |
| Rust (`rustc -O`) | 0.24 to 0.27 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.25 to 0.29 s |
| Go | 0.22 s |
| Python | 4.9 to 5.5 s |
| Kāra (`karac build --mir`) | 0.30 to 0.33 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking: `special` hands `seed`, already a `mut ref`
parameter, on with the `mut` marker design.md asks for. That edit is by
hand, on top of the `scripts/new-bench.sh` output. A copy outside the
kata without those markers builds under legacy and takes 0.29 to 0.35 s.
Under `karac __mir-llvm-run` the program prints the same line in 1.5 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with legacy and within about a third of Rust, C
and Go, most of the time going to making the 16 trees and walking the
four whose values are all the same. The comparison with C and Rust waits
until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
