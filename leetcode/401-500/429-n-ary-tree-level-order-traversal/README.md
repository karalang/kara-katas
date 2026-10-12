# 429. N-ary Tree Level Order Traversal

Given an n-ary tree, return the level order traversal of its nodes'
values: a list of the levels from the root down, each level's values
from left to right.

```
        1
     /  |  \
    3   2   4
   / \
  5   6

root = [1,null,3,2,4,null,5,6]  ->  [[1],[3,2,4],[5,6]]
```

**Constraints:** the height of the tree is at most 1000; the number of
nodes is in `[0, 10^4]`.

## Approaches

A node is a `struct` holding its value and a `Vec[Node]` of children,
as in kata 428: the tree is an owned value, so there are no handles to
nodes to put in a queue. The arms differ in what they do instead.

| file | mechanism |
|---|---|
| `level_order.kara` ★ | breadth first, a level at a time, taking the tree by value (`own`): each node's children move into the next level, so nothing is copied |
| `level_order_depth.kara` | depth first, borrowing the tree: a preorder walk carrying the depth, each value appended to its depth's row. Preorder meets a level left to right |
| `level_order_stack.kara` | the depth-first walk with an explicit stack of (node, depth) pairs, taking the tree by value; children are pushed last first so the walk stays in preorder |
| `level_order_table.kara` | borrowing the tree: number the nodes into a table of values and child indexes, then walk the table breadth first with a queue of indexes |
| `differential.kara` | the four arms on 1,500 random trees, five properties |

All four are O(n).

Every arm prints the same 8 lines: the two LeetCode examples, five edge
cases (the empty tree, one node, a chain of 5, a root with 12
children, and a tree whose deepest node is under its last child), and
for 300 random trees of 0 to 60 nodes the node count, the level count
and a checksum of the answers. `level_order.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, with the node type
defined once before them; the harness clones the trees it hands to the
two arms that take theirs by value, so that copy derives `Clone`. Each
of 1,500 random cases is a tree of 0 to 39 nodes, wide or deep, with
values below 10 or up to 10,000:

| | property |
|---|---|
| P1 | the rows are those read off the generator's table: a preorder walk of the child lists, each value appended to its depth's row |
| P2 | the rows hold n values in all, one row per level |
| P3 | the tree under a new root gives that root's row, then the tree's rows |
| P4 | the tree mirrored gives every row reversed |
| P5 | a chain of m gives m rows of one; a star of m leaves gives the root's row and the leaves' row; the empty tree gives no rows |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | queue: each child goes to the front of the next level | P1 1239, P3 1239, P5 1439 |
| M2 | queue: a level of one node is not recorded | P1 1456, P2 1456, P3 1500, P5 1500 |
| M3 | depth: a child keeps its parent's depth | P1 1416, P2 1416, P3 1456, P4 1411, P5 1500 |
| M4 | depth: each value goes to the front of its row | P1 1241, P3 1241, P5 1439 |
| M5 | stack: children are pushed first child first | P1 1241, P3 1241, P5 1439 |
| M6 | stack: a child keeps its parent's depth | P1 1416, P2 1416, P3 1456, P4 1411, P5 1500 |
| M7 | table: the last node of each level is skipped | P1 1456, P2 1456, P3 1500, P5 1500 |
| M8 | table: every child is numbered under the root | P1 1359, P2 1359, P3 1416, P4 1349, P5 1385 |

P4 misses the three mutants that only reorder values within rows (M1,
M4, M5): each reorders a tree and its mirror image the same way, so
their wrong answers still stand in the mirror relation. M4 and M5, for
example, give every row reversed, and the mirror's reversed rows are
the tree's rows in order, which is what P4 expects. P2 misses them
too, since reordering loses no values. One first pick was
replaced: starting the next level one entry later than the last one
ended re-queued children at every level, and the queue grew until the
run was killed.

## Verification

All four arms print the same output as `level_order.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp` (the legacy tree-walk interpreter), and
`karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on all three. The four arms and the
differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

On the frozen legacy compiled backends:

- LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build` match on
  the depth, stack and table arms. The ★ arm, which moves each node's
  children out with `node.children.into_iter()`, aborts on all three
  with `free(): double free detected in tcache 2`, and the bench
  program, the same code, dies with a segmentation fault.
- The differential does not build there: `karac build` itself aborts
  on it, and `karac run` dies with `has overflowed its stack` before
  printing anything.

Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. Each of 200 rounds builds a random
tree of 10,000 nodes (the problem's limit), each node hung under one of
the last 10 to 1,009 nodes before it, so some trees are deep and some
wide; it takes the level order and folds each row's length, first and
last value into a checksum. Every implementation prints `200 rounds of
10000 nodes: 19922 levels, checksum 461757753`; a 10-round cut of the
Kāra program under `karac __mir-run` prints the same as the C program
cut the same way. The C and Rust mirrors, like the Kāra arm, move each
level's nodes into the next level rather than copying them. Spot
timings on a shared 4-core container, three runs each (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 0.28 to 0.29 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.28 to 0.30 s |
| C (`clang -O3`) | 0.33 to 0.35 s |
| Go | 0.35 to 0.39 s |
| Python | 3.5 to 3.6 s |

The frozen legacy `karac build` program crashes (see Verification), so
there is no legacy time. The Kāra program prints the same line under
`karac __mir-llvm-run` in 1.3 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark.

## Compiler findings

One, filed as kara B-2026-10-12-19. The ★ arm was first written with
bare loops, `for node in level` and `for child in node.children`, and
both moves out are refused. `karac fix` rewrote the first to
`level.into_iter()`, as the diagnostic suggests. For the second, a loop
over a field of the now-owned `node`, it instead added
`#[derive(Clone)]` to `Node` and, on a second pass,
`next.push(child.clone())`: the program then checks clean but copies
every subtree once per level.
`node.children.into_iter()`, written by hand, is accepted and is what
the arm uses.
