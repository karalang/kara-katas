# 559. Maximum Depth of N-ary Tree

Given an n-ary tree, find its maximum depth: the number of nodes along
the longest path from the root node down to the farthest leaf node. The
input is serialized in level order, each group of children separated by
a `null`.

```
root = [1,null,3,2,4,null,5,6]  ->  3
root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]  ->  5
```

**Constraints:** the total number of nodes is in the range `[0, 10^4]`;
the depth of the tree is at most 1000.

## Approaches

Every arm is `fn max_depth(root: Option[Node]) -> i64` over kata 429's
`struct Node { val: i64, children: Vec[Node] }`. The parameter is bare,
so it borrows the tree: no arm copies or takes it apart.

| file | mechanism |
|---|---|
| `maximum_depth.kara` ★ | recursion: a node's depth is one more than its deepest child's; O(n), the recursion as deep as the tree |
| `maximum_depth_chain.kara` | the same as one expression, `1 + node.children.iter().map(\|c\| depth(c)).max().unwrap_or(0)`, and `root.as_ref().map(..)` for the root |
| `maximum_depth_levels.kara` | breadth first: a `Vec[ref Node]` of one level's nodes replaced by all of their children until it comes out empty, the levels counted |
| `maximum_depth_stack.kara` | depth first without recursion: a stack of `(ref Node, i64)`, a node with its depth, the deepest popped kept |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 8 lines: the two LeetCode examples, an empty
tree, one node, a path of 1,000 nodes (the problem's deepest), a root
with 9,999 leaves (its widest), a tree whose deepest node is under the
last child, and the depths of 300 random trees of 0 to 60 nodes.
`maximum_depth.py` mirrors the ★ arm and its output is byte-identical.

The levels and stack arms hold references to the tree's nodes in a
`Vec`, which the spec allows (`Vec[ref T]` is a view, design.md §
Views), and the chain arm uses `Option.as_ref`, which
docs/library/core-types.md lists. Three of the arms do not pass `karac
check` today; see Verification and Compiler findings. They are kept as
written; where a result below comes from a copy outside this directory
with one change, it says so.

## Differential

`differential.kara` holds copies of the four arms, with the node type
defined once, and the definition: a node's depth is its parent's plus
one, and the answer is the largest. Each of 1,000 random trees has 0 to
40 nodes (every tenth is empty), each node after the first hung under
one of the `reach` nodes before it, so a reach of 1 is a path and a
large one a bushy tree.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | it is 0 exactly for the empty tree, and at most the number of nodes |
| P3 | a new root above the tree adds one |
| P4 | one more leaf under the root gives the larger of the answer and 2 |
| P5 | the answer is one more than the deepest child subtree's |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`; `karac check` refuses it, for the chain, levels and
stack arms' reasons below. Until kara B-2026-10-14-11 was fixed
(`188b79d9a4`) it did not run on the MIR backends either, and the copy
the mutants below were run on walks each level with `while let
Some(node) = level.pop()` in place of `for node in level`. Rechecked at
kara `680733538b`.

## Mutation testing

Twelve edits to that copy, two to each arm that change its answers and
one to each that does not, each run under `karac __mir-run`. All eight
that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the node itself not counted | P1 871, P2 871, P3 1000, P4 1000, P5 871 |
| M2 | ★: the children's depths added, not maximized | P1 751, P4 850, P5 639 |
| M3 | chain: the shallowest child taken | P1 725, P4 439, P5 548 |
| M4 | chain: an empty tree given depth 1 | P1 129, P2 129, P3 129 |
| M5 | levels: stops at a level of one node | P1 871, P2 871, P3 1000, P4 1000, P5 871 |
| M6 | levels: leaves never queued | P1 850, P3 21, P4 57, P5 36 |
| M7 | stack: children pushed at their parent's depth | P1 850, P3 871, P4 871, P5 850 |
| M8 | stack: the last depth popped kept, not the deepest | P1 547, P5 268 |
| E1 | ★: the children walked through `iter()` | 0 |
| E2 | chain: the largest found with a fold | 0 |
| E3 | levels: `not is_empty()` for the loop test | 0 |
| E4 | stack: children pushed in reverse | 0 |

The root's level has one node, so M5 stops before counting anything and
fails exactly as M1 does: 0 for every tree of 871 that is not empty,
which P3 and P4 then see on all 1,000 cases since they always add a
node. M4 is wrong only on the 129 empty trees. M6 comes out one short on
every tree of more than one node (850); the properties that compare two
of its answers see it only where one of the two trees is a single node,
which it gets right, since elsewhere both answers are one short. E4 is
safe because the order the stack takes the nodes in does not change the
deepest.

## Verification

Under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer):

| arm | `karac check` | MIR backends |
|---|---|---|
| ★ | passes | same output as the mirror, clean |
| chain | refuses `as_ref` (B-2026-10-14-12) | same output, clean |
| levels | refuses `next.push(child)` (B-2026-10-14-10) | same output, clean, since B-2026-10-14-11 was fixed |
| stack | refuses the `(ref Node, i64)` pushes (B-2026-10-14-10) | same output, clean |

Before B-2026-10-14-11 was fixed, `__mir-run` refused the levels arm's
`for node in level` as invalid MIR, and `__mir-llvm-run` exited 101 with
no message, where ASan found a stack-buffer-overflow; a copy with `while
let Some(node) = level.pop()` printed the same output. Rechecked at kara
`680733538b`: the arm as written prints the same output on both MIR
backends and runs clean under ASan. `karac check` still refuses its
`next.push(child)`. A copy of the chain arm whose `max_depth` matches on
the root passes `karac check` and prints the same output. `karac check`
passes on the bench program.

The frozen legacy backends: `karac run --interp` prints the same output
for the ★ and levels arms. `karac run` and `karac build` stop the ★ arm
at module verification on the harness's `show` call ("Call parameter
type does not match function signature"), and the levels arm at `for
node in level` ("for-loop over this iterable is not lowered"). All three
refuse the chain arm (`as_ref`), the stack arm and the differential (the
tuple pushes), and `karac build` refuses the bench program, which moves
`trees[(round * 7 + g) % count]` out of the index where v2 borrows it.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random trees of
10,000 nodes (the problem's most) once, each node after the first hung
under one of 2 to 1,001 nodes before it, and then 50 times over finds
every tree's depth. Every implementation prints `100 trees of
10000 nodes, 50 rounds: depths sum to 832100, checksum 770463254`, the
Kāra program under `karac __mir-run` included (50 s).

Rust and Go build each node's children by pushing onto a fresh vector as
the Kāra program does; C mallocs each node's child array at its exact
size before building the children into it. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.65 to 0.67 s |
| Rust (`rustc -O`) | 1.97 to 2.05 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.07 to 2.18 s |
| Go | 1.43 to 1.60 s |
| Python | 9.9 to 10.7 s |
| Kāra (`karac build --mir`) | 2.29 to 2.32 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`5b82548ad6`. Under `karac __mir-llvm-run` the program prints the same
line in 3.7 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

Building the trees takes about 0.2 s; the rest is the walk, which reads
50 million nodes and waits on memory, so where the build put the nodes
decides the time. With `Vec::with_capacity(kids[i].len())` in its build,
the Rust program runs in 0.82 to 0.87 s, near C. The same change to the
Kāra program changes nothing (2.37 and 2.45 s), because
`Vec.with_capacity` reserves nothing on the compiled backend (kara
B-2026-10-14-14). That presizing helps through the layout is inferred
from these timings, not profiled. As written, the Kāra row is about
1.15 times Rust's.

## Compiler findings

Five filed from this kata, four open:

- **B-2026-10-14-10.** `karac check` does not treat the elements of a
  `Vec[ref T]` as the `Copy` references the spec makes them. Pushing a
  `ref Node` from `.iter()` is refused with `borrow_projection_copy`,
  pushing `(child, d + 1)` onto a `Vec[(ref Node, i64)]` adds "expected
  '(ref Node, i64)', found '(Node, i64)'", and `let a = v[0];` is
  refused as a move out of an index. The MIR backends run the pushes.
  The levels and stack arms.
- **B-2026-10-14-11**, fixed in kara `188b79d9a4`. `for n in v` over a
  `Vec[ref Node]` was lowered as if the elements were `Node`s:
  `__mir-run` stopped at MIR validation, and the compiled backend ran it
  anyway, copying 32 bytes into an 8-byte slot, which ASan reported as
  a stack-buffer-overflow. The levels arm now runs as written.
- **B-2026-10-14-12.** `karac check` has no `Option.as_ref`, which the
  library spec lists and both MIR backends run. The chain arm, where it
  is the way to `map` over the borrowed root.
- **B-2026-10-14-13.** Pushing an owned `Node` local into a
  `Vec[ref Node]` is accepted as a move of the `Node`, and `__mir-run`
  then reports the tree leaked. Found while reducing B-2026-10-14-11.
- **B-2026-10-14-14.** `Vec.with_capacity(n)` and
  `String.with_capacity(n)` reserve nothing on the compiled backend:
  `capacity()` prints 0 there and `n` under `__mir-run`. Found through
  the bench, above.

The legacy failures above are not filed because legacy is frozen.
