# 617. Merge Two Binary Trees

Given the roots of two binary trees, merge them into one: where both
trees have a node, the merged tree has a node holding the sum of their
values; where only one has a node, the merged tree has that node. Start
from the roots and return the root of the merged tree.

```
root1 = [1,3,2,5], root2 = [2,1,3,null,4,null,7]  ->  [3,4,5,5,4,null,7]
root1 = [1],       root2 = [1,2]                  ->  [2,2]
```

**Constraints:** 0 to 2,000 nodes in each tree; values from -10,000 to
10,000.

## Approaches

Every arm is `fn merge_trees(root1: Option[TreeNode],
root2: Option[TreeNode]) -> Option[TreeNode]` over a `shared struct
TreeNode` with `mut` fields.

| file | mechanism |
|---|---|
| `merge_trees.kara` ★ | one `match` on the pair: a new node with the sum and both pairs of children merged in turn where both are there, and otherwise whichever tree is there, as it is; O(nodes both trees share) |
| `merge_trees_inplace.kara` | the second tree added into the first by recursion: the first's node takes the sum and its children are merged in turn, and a subtree only the second has is hung on the first; no node is made; O(nodes both share) |
| `merge_trees_stack.kara` | the same merge into the first tree without recursion, a `Vec` of node pairs as the stack; a child both have is pushed as a pair, and one only the second has is hung on the first; O(nodes both share) |
| `merge_trees_copy.kara` | a tree of new nodes only, built breadth first from a `VecDeque` holding each new node with the nodes of the two trees at its place, either of which may be missing; neither input is changed or shared; O(nodes in both) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: the two LeetCode examples; six more
(both trees empty, one empty either way, two trees with no place in
common below the root, chains down opposite sides, and sums of zero),
each in LeetCode's level order; a length and checksum over the level
orders of 300 random pairs of trees of 0 to 40 nodes, leaning left with
chance 20, 50 or 80 in 100; and the same for two trees of 2,000 nodes,
one leaning left and one right. `merge_trees.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every node is named by its path from the root, a string of `L` and `R`,
and the merged tree holds a node at every path either tree has, with the
sum of the values there. Each of 1,000 random cases is three trees of
0 to 12 nodes with values from -9 to 9. Each arm gets fresh trees for
every call, since three of them return nodes of their inputs and two
change the first tree.

| | property |
|---|---|
| P1 | the tree is the definition's |
| P2 | the trees in the other order give the same tree |
| P3 | an empty tree on either side changes nothing |
| P4 | the values add up to both trees' values |
| P5 | merging a third tree in gives the same tree either way round |

With B-2026-10-14-40 fixed it should print `1000 cases (8999 merged
nodes), 4 arms, 20000 checks, 0 failures`, which is what a copy with `*v
?? 0` in `total` prints under `karac __mir-run` and `karac
__mir-llvm-run`, running clean under `karac __mir-llvm-asan`. As written
it stops at that `??` (see Compiler findings).

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first tree's right subtree kept as it is | P1 678, P2 805, P4 650 |
| M2 | ★: a node only the second tree has dropped | P1 728, P2 981, P3 920, P4 702, P5 416 |
| M3 | inplace: the second tree's value replacing the first's | P1 829, P2 824, P4 805 |
| M4 | inplace: an empty first tree giving an empty tree | P1 728, P2 981, P3 920, P4 702, P5 416 |
| M5 | stack: a left child only the second has hung on the right | P1 461, P2 735, P4 224, P5 461 |
| M6 | stack: right children both trees have left unmerged | P1 525, P2 529, P4 506 |
| M7 | copy: a left child holding only the first tree's value | P1 767, P2 932, P3 767, P4 743 |
| M8 | copy: a left child made only where the first tree has one | P1 622, P2 919, P3 781, P4 591, P5 278 |
| E1 | ★: the sum written the other way round | 0 |
| E2 | inplace: the left children merged into the second tree's | 0 |
| E3 | stack: the sum added with `+=` | 0 |
| E4 | copy: the empty case tested as `not (.. or ..)` | 0 |

P1, P2 and P4 kill all eight: each mutant changes the tree for some
pair, the change is not the same with the trees swapped, and each loses
some value. P3 sees the mutants that go wrong where one tree has
nothing: M2 and M4 give no node wherever the first tree has none, at
every depth, so they fail the same counts, and M7 and M8 lose the second
tree's left values or left children. P5 is the weakest. It tests that
merging is associative, and M1, M3, M6 and M7 change the merge into one
that still is: keeping the first tree's right subtree or a left child's
first value, or letting the last value win, gives the same tree
whichever pair is merged first.

## Verification

Every arm prints the same output as `merge_trees.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. All at kara
`ea2a2da2be` for the debug build and `486b322baf` for the release build
that runs `check` and `__mir-run`.

The frozen legacy backends refuse every file at type checking. They
still hold the old rule that an argument which is already a `mut ref`,
as `seed` is inside `random_tree`, drops its call-site `mut` marker;
design.md § Call-site `mut` markers now marks every such argument.
Before the markers were written in, legacy ran the ★ arm right under
`karac run --interp`, and the program `karac run` and `karac build` made
for it aborted with "malloc(): unaligned tcache chunk detected". Legacy
is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random trees of
2,000 nodes, the problem's most, leaning left with chance 30 to 70 in
100, once; then 10,000 times merges two of them, picked by the round,
and walks the merged tree counting its nodes and putting each value into
a checksum. Every implementation prints `20 trees, 10000 rounds:
29973000 nodes, checksum 397156125`, the Kāra program under `karac
__mir-run` included (in 165 s).

Each implementation merges as the ★ arm does, making a node where both
trees have one and sharing the subtree where only one does, so the
inputs are never changed: Rust with `Option<Rc<RefCell<TreeNode>>>`, Go
with pointers and the garbage collector, C with `malloc` and a list of
each round's new nodes freed after the walk, and Python with a class
with `__slots__`. Spot timings on a shared 4-core container, three runs
each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.61 to 0.62 s |
| Rust (`rustc -O`) | 1.05 to 1.12 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.20 to 1.28 s |
| Go | 0.95 to 1.02 s |
| Python | 10.7 s |
| Kāra (`karac build --mir`) | 1.41 to 1.42 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the `mut`
markers; that edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
3.2 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

The Kāra row is about 1.3 times Rust's and 2.3 times C's. It is not
profiled here.

## Compiler findings

B-2026-10-14-40, filed from here and open: `??` on a `ref Option[i64]`
is refused by both MIR backends, though `karac check` accepts it and
design.md reads a `ref T` of a `Copy` `T` as a `T` wherever one is
expected. The differential's `total` sums a level order with `for v in
values.iter() { sum += v ?? 0; }`, the natural spelling, and keeps it,
with the row cited in a comment. So the differential does not run under
`karac __mir-run`, `karac __mir-llvm-run` or `karac __mir-llvm-asan`; a
copy kept outside this directory that writes `*v ?? 0` instead is what
was run.
