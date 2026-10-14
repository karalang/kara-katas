# 589. N-ary Tree Preorder Traversal

Given the `root` of an n-ary tree, return the preorder traversal of its
nodes' values. The input is serialized in level order, each group of
children separated by a `null`.

```
root = [1,null,3,2,4,null,5,6]  ->  [1,3,5,6,2,4]
root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]  ->  [1,2,3,6,7,11,14,4,8,12,5,9,13,10]
```

**Constraints:** the number of nodes in the tree is in the range
`[0, 10^4]`; `0 <= Node.val <= 10^4`; the height of the n-ary tree is
less than or equal to 1000. **Follow up:** recursive solution is
trivial, could you do it iteratively?

## Approaches

Every arm is `fn preorder(root: Option[Node]) -> Vec[i64]` over kata
429's `struct Node { val: i64, children: Vec[Node] }`. The parameter is
bare, so it borrows the tree: no arm copies or takes it apart. The stack
and frames arms are the follow-up's iterative answers.

| file | mechanism |
|---|---|
| `preorder.kara` ★ | recursion: a node's value, then each child's walk in turn, pushed onto one list passed down as a `mut ref`; O(n), the recursion as deep as the tree |
| `preorder_stack.kara` | a `Vec[ref Node]` of nodes still to visit: each one popped gives its value and pushes its children last first, so the first child comes off next; O(n) |
| `preorder_frames.kara` | the recursion's frames kept by hand: a `Vec[(ref Node, i64)]` of each node with the index of its next child; a node's value is taken when its frame is pushed, and the top frame enters its next child or is popped; O(n) |
| `preorder_concat.kara` | each node returns its own list, its value with its children's lists appended; O(n * depth), since every value is copied once for each node above it |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, an empty
tree, one node, a tree that repeats its values, one whose deepest node
is under the last child, a path of 1,000 nodes (the problem's deepest)
and a root with 9,999 leaves (its widest), those two as a count, the
first five values and a checksum, and a count and checksum over
300 random trees of 0 to 60 nodes. `preorder.py` mirrors the ★ arm and
its output is byte-identical.

The frames arm does not build today; see Compiler findings. It is kept
as written. A copy outside this directory that keeps the frames as two
stacks side by side, a `Vec[ref Node]` and a `Vec[i64]`, the only
change, prints the same output.

## Differential

`differential.kara` holds copies of the four arms, with the node type
defined once, and the definition, which does not walk the tree: each
node gets its path from the root, the index of the child taken at each
step, and preorder lists the nodes in the order of their paths, a path
before every longer path it begins and otherwise by the first index
where two paths differ. Each of 1,000 random trees has 0 to 40 nodes
(every tenth is empty) with values from 0 to 9, so most repeat some,
each node after the first hung under one of the `reach` nodes before it,
so a reach of 1 is a path and a large one a bushy tree.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | it holds the tree's values, each as often as the tree does, the root's first |
| P3 | a new root above the tree puts its value in front |
| P4 | the answer is the root's value, then each child subtree's answer in turn |
| P5 | one more leaf, the root's last child, puts its value at the end |

Since the frames arm does not build, the differential does not either:
both MIR backends stop at its copy of that arm, though `karac check`
passes it. The copy outside this directory with the workaround copy of
the frames arm prints `1000 cases, 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to that copy, two to each arm that change its answers and
one to each that does not, each run under `karac __mir-run`. All eight
that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the children walked last first | P1 758, P4 649, P5 852 |
| M2 | ★: the root's own value left out | P1 878, P2 878, P3 1000, P4 854, P5 122 |
| M3 | stack: the children pushed first first | P1 758, P4 649, P5 852 |
| M4 | stack: the oldest node taken, not the newest | P1 757, P4 640, P5 852 |
| M5 | frames: only a node's first child entered | P1 762, P2 762, P4 650, P5 852 |
| M6 | frames: the root's value left out | P1 878, P2 878, P3 1000, P4 854, P5 122 |
| M7 | concat: each child's list put in front, value by value | P1 831, P3 848, P4 831, P5 852 |
| M8 | concat: only each child's own value kept | P1 828, P2 828, P3 852, P4 828 |
| E1 | ★: the children walked through `iter()` | 0 |
| E2 | stack: the loop tested by `is_empty()` | 0 |
| E3 | frames: `>=` for the last-child test | 0 |
| E4 | concat: each child's list pushed value by value | 0 |

M1 and M3 give the same wrong answer, every node's children in reverse,
so they fail on the same cases. P2 sees only the mutants that lose
values, M2, M5, M6 and M8, since the others put the right values in the
wrong order. P5 is the weakest on M2 and M6: with the root's value left
out, a last leaf still comes last, so P5 fails them only on the
122 empty trees (every tenth, and 22 more whose random size came out
0), where a leaf alone must be listed and is not. The 878 that P2 sees
are the rest. M8 keeps each child's own value and drops what lies below
it, and the new leaf has nothing below it, so P5 never sees it. E3 is
safe because the index never passes the number of children.

## Verification

The ★, stack and concat arms print the same output as `preorder.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. `karac check` passes on all four arms, the differential and the
bench program. Both MIR backends refuse the frames arm and the
differential (B-2026-10-14-29). The workaround copy of the frames arm
prints the same output under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`. All of it
at kara `555c29b44e`.

The frozen legacy backends refuse every arm, the differential and the
bench program under `karac run --interp`, `karac run` and `karac build`.
The ★, stack and concat arms stop at the harness's `show_long`, which
slices `got[0..5]` and passes `got` to `checksum_of` in one line: legacy
moves `got` into the call, where v2's bare parameter borrows it ("cannot
move `got` while a slice borrow into it is still live"). The frames arm
and the differential stop at type checking on the `(ref Node,
i64)` frames, legacy reading `(node, 0)` as a `(Node, i64)` and
`frames[top]` as a move. The bench program moves `trees[(round * 7 + g)
% count]` out of the index where v2 borrows it. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random trees of
10,000 nodes (the problem's most) once, as kata 559's bench does, each
node after the first hung under one of 2 to 1,001 nodes before it, and
then 30 times over lists every tree in preorder, a fresh list each call,
and folds every value listed into a checksum. Every implementation
prints `100 trees of 10000 nodes, 30 rounds: 30000000 values listed,
checksum 795453516`, the Kāra program under `karac __mir-run` included
(44 s).

Each implementation returns a fresh list from every call, grown as it
fills: a `Vec` in Rust, a slice appended to in Go, a list in Python, and
in C an array that doubles from 4 slots and is freed after the fold.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.70 to 0.76 s |
| Rust (`rustc -O`) | 1.59 to 1.62 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.60 to 1.67 s |
| Go | 1.44 to 1.47 s |
| Python | 13.7 to 13.9 s |
| Kāra (`karac build --mir`) | 1.69 to 1.74 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`555c29b44e`. Under `karac __mir-llvm-run` the program prints the same
line in 3.2 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about 1.07 times Rust's and 1.2 times Go's. C's tree
holds each node's children in one array of exactly the right size, which
the Rust, Go and Kāra trees, built by pushing, do not; kata 559 measured
what that layout is worth on the same trees, and it is not measured
again here. Where the rest of the gap comes from is not measured.

## Compiler findings

One filed from this kata: **B-2026-10-14-29**. The frames arm reads its
top frame with `let (node, next) = frames[top];` from a `Vec[(ref Node,
i64)]`, then pops the frame or bumps its index while it goes on using
`node`. Both MIR backends refuse that with "mutable borrow of _3 while
it is borrowed" (E0516): the borrow checker keeps the vector borrowed
for as long as the `ref Node` copied out of its element is live.
core-semantics §1.1 makes such a tuple `Copy`, and a copied reference
keeps the origin of what it points at, the tree, not of the vector it
was read from. The same read out of a `Vec[ref Node]` runs, and `karac
check` passes both. The arm keeps the natural spelling.

The stack and frames arms would not have passed `karac check` a few
hours earlier: pushing a `ref Node` from `iter()` into a `Vec[ref
Node]`, and the `(ref Node, i64)` pushes and index read, were
B-2026-10-14-10, filed from kata 559 and fixed in kara `8139c5e826`. The
legacy failures above are not filed because legacy is frozen.
