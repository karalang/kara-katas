# 590. N-ary Tree Postorder Traversal

Given the `root` of an n-ary tree, return the postorder traversal of its
nodes' values. The input is serialized in level order, each group of
children separated by a `null`.

```
root = [1,null,3,2,4,null,5,6]  ->  [5,6,3,2,4,1]
root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]  ->  [2,6,14,11,7,3,12,8,4,13,9,10,5,1]
```

**Constraints:** the number of nodes in the tree is in the range
`[0, 10^4]`; `0 <= Node.val <= 10^4`; the height of the n-ary tree is
less than or equal to 1000. **Follow up:** recursive solution is
trivial, could you do it iteratively?

## Approaches

Every arm is `fn postorder(root: Option[Node]) -> Vec[i64]` over kata
429's `struct Node { val: i64, children: Vec[Node] }`. The parameter is
bare, so it borrows the tree: no arm copies or takes it apart. The
reversed and marks arms are the follow-up's iterative answers.

| file | mechanism |
|---|---|
| `postorder.kara` ★ | recursion: each child's walk in turn, then the node's value, pushed onto one list passed down as a `mut ref`; O(n), the recursion as deep as the tree |
| `postorder_reversed.kara` | a mirrored preorder, reversed: a `Vec[ref Node]` of nodes still to visit, each one popped giving its value and pushing its children first first, which lists every node before its descendants and the children right to left; the list turned round at the end is postorder; O(n) |
| `postorder_marks.kara` | a `Vec[(ref Node, bool)]` of each node and whether its children have been pushed: popped unmarked, a node goes back marked with its children above it last first; popped marked, it gives its value; O(n) |
| `postorder_concat.kara` | each node returns its own list, its children's lists appended with its value after them; O(n * depth), since every value is copied once for each node above it |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, an empty
tree, one node, a tree that repeats its values, one whose deepest node
is under the last child, a path of 1,000 nodes (the problem's deepest)
and a root with 9,999 leaves (its widest), those two as a count, the
first five values and a checksum, and a count and checksum over
300 random trees of 0 to 60 nodes. The harness is kata 589's with
`postorder` in place of `preorder`. `postorder.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, with the node type
defined once, and the definition, which does not walk the tree: each
node gets its path from the root, the index of the child taken at each
step, and postorder lists the nodes in the order of their paths, every
longer path a path begins before it and otherwise by the first index
where two paths differ. Each of 1,000 random trees has 0 to 40 nodes
(every tenth is empty) with values from 0 to 9, so most repeat some,
each node after the first hung under one of the `reach` nodes before it,
so a reach of 1 is a path and a large one a bushy tree.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | it holds the tree's values, each as often as the tree does, the root's last |
| P3 | a new root above the tree puts its value at the end |
| P4 | the answer is each child subtree's answer in turn, then the root's value |
| P5 | one more leaf, the root's first child, puts its value in front |

All four arms build, so the differential runs as it stands: `1000 cases,
4 arms, 20000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the children walked last first | P1 773, P4 659, P5 864 |
| M2 | ★: a leaf's value left out | P1 883, P2 883, P3 117, P4 19, P5 1000 |
| M3 | reversed: the list not reversed | P1 864, P2 783, P3 883, P4 860, P5 883 |
| M4 | reversed: the children pushed last first | P1 773, P4 659, P5 864 |
| M5 | marks: a node's value given when it is first popped | P1 864, P2 782, P3 883, P4 864, P5 883 |
| M6 | marks: the children pushed first first | P1 773, P4 659, P5 864 |
| M7 | concat: the node's value put first | P1 864, P2 782, P3 883, P4 864, P5 883 |
| M8 | concat: only each child's own value kept | P1 832, P2 832, P3 864, P4 832 |
| E1 | ★: the children walked through `iter()` | 0 |
| E2 | reversed: the loop tested by `is_empty()` | 0 |
| E3 | marks: a leaf's value given when first popped | 0 |
| E4 | concat: each child's list pushed value by value | 0 |

M1, M4 and M6 give the same wrong answer, every node's children in
reverse, and fail on the same cases; P2 does not see them, since their
values are right and the root still comes last. M5 and M7 both give
preorder, and M3 gives preorder with every node's children in reverse.
M2 drops every leaf, so P5's new leaf is always missing
(1,000). P3 fails it only on the 117 empty trees, where the new root is
itself a leaf, and P4, which builds its answer from the mutant's own
answers for the children, only on the 19 trees of one node, where the
root is a leaf. M8 keeps each child's own value and drops what lies
below it; the new leaf has nothing below it, so P5 never sees it. E3 is
safe because a leaf has no children to wait for.

## Verification

Every arm prints the same output as `postorder.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on all four arms, the differential and the bench program. All of
it at kara `6905651ffc`.

The frozen legacy backends refuse every arm, the differential and the
bench program under `karac run --interp`, `karac run` and `karac build`.
The ★, reversed and concat arms stop at the harness's `show_long`, as
kata 589's do: legacy moves `got` into `checksum_of`, where v2's bare
parameter borrows it, while `got[0..5]` still borrows it. The marks arm
and the differential stop at type checking on the `(ref Node, bool)`
entries, legacy reading `(node, false)` as a `(Node, bool)`. The bench
program moves `trees[(round * 7 + g) % count]` out of the index where
v2 borrows it. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, and is kata 589's with postorder in
place of preorder. It builds 100 random trees of 10,000 nodes (the
problem's most) once, as kata 559's bench does, each node after the
first hung under one of 2 to 1,001 nodes before it, and then 30 times
over lists every tree in postorder, a fresh list each call, and folds
every value listed into a checksum. Every implementation prints
`100 trees of 10000 nodes, 30 rounds: 30000000 values listed, checksum
12097363`, the Kāra program under `karac __mir-run` included (48 s).

Each implementation returns a fresh list from every call, grown as it
fills: a `Vec` in Rust, a slice appended to in Go, a list in Python, and
in C an array that doubles from 4 slots and is freed after the fold.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.69 to 0.73 s |
| Rust (`rustc -O`) | 1.65 to 1.76 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.61 to 1.66 s |
| Go | 1.35 to 1.52 s |
| Python | 13.2 to 13.7 s |
| Kāra (`karac build --mir`) | 1.69 to 1.74 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`6905651ffc`. Under `karac __mir-llvm-run` the program prints the same
line in 3.5 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is level with Rust's, and Go's is a little faster than
both. C's tree holds each node's children in one array of exactly the
right size, which the Rust, Go and Kāra trees, built by pushing, do not;
kata 559 measured what that layout is worth on the same trees, and it is
not measured again here.

## Compiler findings

None. The marks arm pops `(ref Node, bool)` entries whole with `while
let Some((node, expanded)) = stack.pop()`, so it never holds a reference
copied out of an element still in the stack, which is the shape kata
589's frames arm meets in kara B-2026-10-14-29. The legacy failures
above are not filed because legacy is frozen.
