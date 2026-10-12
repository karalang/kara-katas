# 430. Flatten a Multilevel Doubly Linked List

A doubly linked list has, besides its next and previous links, a child
link that may point to another doubly linked list. Those child lists
may have children of their own, and so on, producing a multilevel data
structure.

Given the head of the first level, flatten the list so that all the
nodes appear in a single-level doubly linked list: the nodes of a
node's child list come after that node and before its next node.
Return the head of the flattened list, with every child link cleared.

```
1 - 2 - 3 - 4 - 5 - 6
        |
        7 - 8 - 9 - 10
            |
            11 - 12

->  1 - 2 - 3 - 7 - 8 - 11 - 12 - 9 - 10 - 4 - 5 - 6
```

**Constraints:** the number of nodes is at most 1000;
`1 <= Node.val <= 10^5`.

## Approaches

A node is a `shared struct`: the list is made of nodes that several
links point at, so a node is a reference-counted value whose `prev`,
`next` and `child` fields are `mut`, and each arm rewires the nodes in
place.

| file | mechanism |
|---|---|
| `flatten.kara` ★ | recursion: walk a level, and at a node with a child flatten the child's level first, which returns its tail, then splice it in between the node and its next. O(n) time, O(depth) stack |
| `flatten_stack.kara` | one walk with a stack of the nodes that were next when the walk went down into a child; at the end of a level, pop one and link it after the current node. O(n) time, O(depth) stack |
| `flatten_splice.kara` | no recursion and no stack: at a node with a child, walk the child level to its tail and splice the whole level in; the walk carries on into it, so deeper children are spliced when it reaches them. Each node is walked at most twice, O(1) extra space |
| `flatten_collect.kara` | collect the nodes in flattened order with a depth-first walk into a `Vec[Node]`, then relink them as one list. O(n) time, O(n) space |
| `differential.kara` | the four arms on 1,500 random lists, five properties |

Each arm's harness builds a list from text, values separated by spaces
and a node's child list in parentheses straight after it, so
`1 2(3 4) 5` is 1, 2, 5 with 3, 4 hanging from 2. It reads the
flattened list forward and then back from the tail, marking it
`BROKEN` if a `prev` does not undo a `next`, a child link is left, or
the walk back disagrees. Neighbours hold each other strongly, so a
list is a cycle of reference counts; the harness breaks every link as
it reads, which frees the nodes.

Every arm prints the same 9 lines: the two LeetCode examples, the empty
list, one node, a chain of children 5 deep, a child at the last node,
a child under each of three nodes, and a list with negative values;
then for 300 random lists of 0 to 50 nodes, the node count and a
checksum of the flattened lists. `flatten.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms, with the node type
defined once before them. Each of 1,500 random cases is a list of 1 to
40 nodes with child levels up to 6 deep, valued 1, 2, 3, ... in the
order they appear once flattened, so the right answer is always the
values in ascending order:

| | property |
|---|---|
| P1 | the values read forward are 1 to n |
| P2 | the list is linked both ways: every `prev` undoes a `next`, no child is left, and the walk back from the tail gives the same values |
| P3 | the head returned is the head passed in |
| P4 | flattening the result again changes nothing |
| P5 | a single level of m, a chain of m nested children, and the empty list each flatten right |

P1 and P2 read the list after it has been flattened twice, which is
also what P4 compares with a single flattening. Both walks stop after
a fixed number of steps, so a mutant that links a cycle fails the
checks rather than hanging the run. It prints
`1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | recursive: the child level's head keeps no `prev` | P2 793, P5 1422 |
| M2 | recursive: a level ending in a child returns the node, not the child level's tail | P1 199 |
| M3 | stack: the node after a child is not saved | P1 589 |
| M4 | stack: a resumed node keeps its old `prev` | P2 589 |
| M5 | splice: the rest of the level is hung after the child's head | P1 503, P2 488 |
| M6 | splice: the child level's head gets its tail as `prev` | P2 793, P5 1422 |
| M7 | collect: child levels are not collected | P1 793, P5 1422 |
| M8 | collect: each node is its own `prev` | P2 1258, P5 1422 |

No mutant fails P3 or P4. Every arm returns the head it was given, and
the mutants leave that alone. P4 is vacuous for these mutants for a
subtler reason: each still clears every child link it passes, so the
first flattening leaves a single level, possibly wrong, and flattening
a single level changes nothing. M2 is the narrowest: its wrong tail
only matters when a level ends in a node with a child and that level
is itself a child with more nodes after its parent.

## Verification

All four arms print the same output as `flatten.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp` (the legacy tree-walk interpreter), and
`karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on all three. The four arms and the
differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak, so breaking the links as the harness reads does free every node.

On the frozen legacy compiled backends (LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`):

- No arm compiles: each harness's `show(text: Str)` calls
  `text.bytes()`, and legacy codegen has no `bytes()` on a `Str`
  parameter (`no handler for method 'bytes' on variable 'text'`).
- The differential and the bench program, which have no such call,
  compile; both die with a segmentation fault under `karac build`, and
  the differential prints nothing under `karac run`.

Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. Each of 2,000 rounds builds a
random multilevel list of 1,000 nodes (the problem's limit), each node
given a child level of 1 to 8 nodes with probability 1 in 4 while the
depth is under 6, valued in flattened order; it flattens the list, then
walks it, counting values out of place, folding each into a checksum
and breaking each node's links so it is freed. Every implementation
prints `2000 rounds of 1000 nodes: 0 misplaced, checksum 447489508`; a
20-round cut of the Kāra program under `karac __mir-run` prints the
same as the C program cut the same way.

The mirrors keep the Kāra program's memory model where the language
has one: Rust's nodes are `Rc<RefCell<Node>>` with strong links both
ways, as a Kāra `shared struct` is reference counted, and the walk
breaks them. C frees each node as the walk passes it and keeps no
counts; Go leaves the nodes to its collector. Spot timings on a
shared 4-core container, three runs each (`bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.06 to 0.08 s |
| Rust (`rustc -O`) | 0.09 to 0.11 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.09 s |
| Go | 0.10 s |
| Python | 1.4 to 1.6 s |

C's lead is the reference counting it does not do. The frozen legacy
`karac build` program crashes (see Verification), so there is no
legacy time. The Kāra program prints the same line under
`karac __mir-llvm-run` in 0.74 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings.
