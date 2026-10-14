# 623. Add One Row to Tree

Given the root of a binary tree and two integers `val` and `depth`, add
a row of nodes with value `val` at the given depth, the root being at
depth 1. Every node at depth `depth - 1` gets two new children of value
`val`: its old left subtree becomes the left subtree of the new left
child, and its old right subtree the right subtree of the new right
child. When `depth` is 1, a new root of value `val` is made with the
whole tree as its left subtree.

```
root = [4,2,6,3,1,5], val = 1, depth = 2  ->  [4,1,1,2,null,null,6,3,1,5]
root = [4,2,null,3,1], val = 1, depth = 3  ->  [4,2,null,1,1,3,null,null,1]
```

**Constraints:** 1 to 10,000 nodes; node values from -100 to 100; `val`
from -100,000 to 100,000; `depth` from 1 to one more than the tree's
depth.

## Approaches

Every arm is `fn add_one_row(root: Option[TreeNode], val: i64, depth:
i64) -> Option[TreeNode]` over a `shared struct TreeNode` with `mut`
fields, and handles depth 1 with a new root.

| file | mechanism |
|---|---|
| `add_one_row.kara` ★ | a recursion down from the root carrying the level, which at every node one level above `depth` hangs the two new nodes; changes the tree in place; O(nodes above the new row) |
| `add_one_row_levels.kara` | the nodes collected a level at a time, each level a `Vec` of the children of the one before, down to the level above `depth`, whose nodes then get their new children; in place; O(nodes above the new row) |
| `add_one_row_stack.kara` | the recursion's walk with a `Vec` of (node, level) pairs as the stack; in place; O(nodes above the new row) |
| `add_one_row_copy.kara` | a new tree, leaving the input alone, built by one function that carries which side a subtree hangs on: at depth 1 it makes the new node and hangs the subtree on that side, and otherwise it copies the node and goes down a level; O(nodes in the tree) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: the two LeetCode examples; six more
(a single node with a row at depth 1 and at depth 2, a new root over a
tree, a row under the deepest level, a row in the middle of a chain down
the right, and a row where some nodes above it have one child or none),
each tree in LeetCode's level order; a length and checksum over the
level orders of 300 random trees of 1 to 40 nodes, leaning left with
chance 20, 50 or 80 in 100, each with a row of a random value at a
random depth from 1 to one below its deepest level; and the same for two
trees of 10,000 nodes, with a row at depth 3 and a row one below the
deepest level. `add_one_row.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which works on paths: every node is named by its path from the root, a
string of `L` and `R`. A node fewer than `depth - 1` steps down keeps
its path; a node deeper down has the step it takes out of level `depth -
1` doubled, since it now passes through the new node on that side, and
at depth 1 gains a leading `L`; and every node at level `depth - 1` gets
new nodes of value `val` at both its child paths. Each of 1,000 random
cases is a tree of 1 to 12 nodes, a depth from 1 to one below its
deepest level, and a row value, values from -9 to 9; every call gets a
fresh tree, since three arms change theirs.

| | property |
|---|---|
| P1 | the tree is the definition's |
| P2 | it has one node more at depth 1, and otherwise two more for every node at level `depth - 1` |
| P3 | taking the row out again, each node above it getting back its left child's left subtree and its right child's right subtree, gives the tree back |
| P4 | the new level holds that many nodes, all of value `val` |
| P5 | below depth 1, the mirror image of the tree gives the mirror image of the answer |

P5 holds only below depth 1: there the old tree goes on the left of the
new root, so the problem is not symmetric. At depth 1 the check is
counted as passed.

It prints `1000 cases (2620 new nodes), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the new right node taking the old right subtree as its left | P1 429, P3 429, P5 542 |
| M2 | ★: the row put one level too deep | P1 778, P2 568, P3 535, P4 778 |
| M3 | levels: one level too many walked down | P1 778, P2 568, P3 535, P4 778 |
| M4 | levels: right children never walked down to | P1 485, P2 485, P3 270, P4 485, P5 492 |
| M5 | stack: the old left subtree hung on the new left node's right | P1 416, P3 416, P5 542 |
| M6 | stack: a new root with the tree on its right | P1 222, P3 222 |
| M7 | copy: a right child's subtree hung on the left side | P1 429, P3 429, P5 542 |
| M8 | copy: the row on the left side one level too high | P1 778, P2 669, P3 705, P4 771, P5 767 |
| E1 | ★: the level test as `level + 1 == depth` | 0 |
| E2 | levels: no early stop on an empty level | 0 |
| E3 | stack: the level test as `depth - level == 1` | 0 |
| E4 | copy: the subtree below the row shared, not copied | 0 |

P1 and P3 kill all eight. M1 and M7 both hang the old right subtree on
the left of the new right node, and M2 and M3 both put the row one level
too deep, so each pair fails the same counts. P2 and P4, which count the
new nodes and read their values, miss the mutants that build the row
right and attach the old subtrees wrong: M1, M5, M6 and M7. P5 sees the
mutants that treat the two sides differently, M1, M4, M5, M7 and M8, and
misses M2 and M3, which are wrong the same way on both sides, and
M6, which goes wrong only at depth 1, where P5 is not checked.

## Verification

Every arm prints the same output as `add_one_row.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `6b1086b1fa` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends refuse every file at type checking. They
still hold the old rule that an argument which is already a `mut ref`,
as `seed` is inside `random_tree`, drops its call-site `mut` marker, and
they type the items of a `SortedMap`'s `iter()` by value, so the
differential's `*v` is an error. Legacy is frozen, so these are noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. Adding a row makes a tree bigger, so a
bench that only added rows would measure a tree that keeps growing;
instead each round adds a row and the bench's own `undo` takes it out
again, the inverse walk, counting the row's nodes and putting their
values into a checksum. It makes 20 random trees of 10,000 nodes, the
problem's most, leaning left with chance 30 to 70 in 100, once; then
4,000 times adds a row at depth 2 to 21 to one of them, both picked by
the round, and takes it out. Every implementation prints `20 trees,
4000 rounds: 3997260 row nodes, checksum 17440327`, the Kāra program
under `karac __mir-run` included (in 91 s).

Each implementation is the ★ arm's recursion and the same `undo`: Rust
with `Option<Rc<RefCell<TreeNode>>>`, Go with pointers and the garbage
collector, C with `malloc` and an `undo` that frees the two nodes of
each pair it takes out, and Python with a class with `__slots__`. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.50 to 0.53 s |
| Rust (`rustc -O`) | 0.84 to 0.92 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.89 to 0.94 s |
| Go | 0.62 to 0.64 s |
| Python | 7.2 to 7.5 s |
| Kāra (`karac build --mir`) | 0.95 to 1.05 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the `mut`
markers; that edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
2.4 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

The Kāra row is about 1.1 times Rust's and twice C's. It is not profiled
here.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
