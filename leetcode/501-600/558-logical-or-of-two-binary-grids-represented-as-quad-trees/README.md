# 558. Logical OR of Two Binary Grids Represented as Quad-Trees

A binary matrix is represented by a quad tree (kata 427): a node is a
leaf with the value of its whole region, or splits the region into four
equal quarters, top left, top right, bottom left and bottom right, each
a child node. Given `quadTree1` and `quadTree2`, two quad trees for `n *
n` binary matrices, return a quad tree for the matrix that is the
bitwise OR of the two. A leaf's region has one value throughout, and a
node whose region has one value must be a leaf.

The trees are serialized level by level as in kata 427, each node as
`[isLeaf, val]` and a missing child as `null`:

```
quadTree1 = [[0,1],[1,1],[1,1],[1,0],[1,0]]
quadTree2 = [[0,1],[1,1],[0,1],[1,1],[1,0],null,null,null,null,
             [1,0],[1,0],[1,1],[1,1]]
  ->  [[0,0],[1,1],[1,1],[1,1],[1,0]]
quadTree1 = [[1,0]], quadTree2 = [[1,0]]  ->  [[1,0]]
```

**Constraints:** both trees represent `n * n` grids; `n == 2^x` where
`0 <= x <= 9`.

## Approaches

Every arm is `fn intersect(a: Quad, b: Quad) -> Quad`, LeetCode's name
for it. The tree is kata 427's `shared enum Quad { Leaf(bool),
Split(Quad, Quad, Quad, Quad) }`, a reference-counted handle, so an
answer can share whole subtrees with the trees it came from. A split's
value means nothing and the enum has no field for it.

| file | mechanism |
|---|---|
| `quad_tree_or.kara` ★ | recursion: a leaf of 1 is the answer, a leaf of 0 gives the other tree, and two splits are ORed quarter by quarter, four leaves of one value merging into one; O(nodes) |
| `quad_tree_or_pair.kara` | the same recursion as one `match` on the pair `(a, b)`, the leaf cases as patterns `(Quad.Leaf(true), _)` and so on, the merge as a guard |
| `quad_tree_or_node.kara` | on LeetCode's own node: a `shared struct` with `is_leaf`, `val` and an `Option[Node]` per child, the recursion LeetCode's solutions write on it, the trees converted from and back to `Quad` |
| `quad_tree_or_grid.kara` | the plain reading: both trees painted into grids of the deeper one's side, ORed cell by cell, and the tree of the result built bottom up a level of 2 by 2 merges at a time; O(n^2) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, six edge
cases (a leaf of 1 and a leaf of 0 against a checkerboard, a
checkerboard and its complement, whose OR merges back up to one leaf, a
cell in each of two 2 by 2 grids, kata 427's second example ORed with
itself, and a 1 in each of two 64 by 64 grids side by side, which splits
at every level down to them), and for 300 random pairs of grids of side
1 to 64 the number of nodes and leaves in the answers and a checksum of
their serializations. `quad_tree_or.py` mirrors the ★ arm and its output
is byte-identical.

The harness builds each tree from its grid with kata 427's construction.
A split prints as `[0,1]`, as in kata 427; LeetCode's first example
prints its answer's root as `[0,0]`, and both values are accepted for a
split.

## Differential

`differential.kara` holds copies of the four arms, with the tree type
defined once, and the definition: OR the two grids cell by cell and
build the tree of the result. Each arm is held to the properties below
on 1,000 random pairs of grids of side 1 to 32, made of blocks of a
random power-of-two side, each one value, with up to three cells
flipped; every fourth pair is one grid twice.

| | property |
|---|---|
| P1 | the answer serializes as the definition's tree |
| P2 | no split in the answer has four leaves of one value under it |
| P3 | the answer's cells are the two grids' cells ORed |
| P4 | `intersect(b, a)` serializes as `intersect(a, b)` |
| P5 | ORing the first tree into the answer again changes nothing |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a leaf of 1 gives the other tree | P1 582, P3 582, P4 551, P5 393 |
| M2 | ★: three leaves of one value merge | P1 141, P3 141, P5 189 |
| M3 | pair: a leaf of 1 on the right gives the left | P1 242, P3 242, P4 393 |
| M4 | pair: nothing merges | P1 134, P2 134 |
| M5 | node: a leaf of 0 on the right is kept | P1 403, P3 403, P4 551, P5 396 |
| M6 | node: the last child's value not compared | P1 141, P3 141, P5 189 |
| M7 | grid: the cells ANDed | P1 684, P3 684 |
| M8 | grid: the bottom-right quarter painted bottom left | P1 678, P3 678, P5 282 |
| E1 | ★: only leaves of 1 merge | 0 |
| E2 | pair: any left leaf gives the right tree, after the case for 1 | 0 |
| E3 | node: a split's value written false | 0 |
| E4 | grid: painted at twice the side | 0 |

Only M4 leaves a split that should have merged, so only it fails P2; it
gives the right cells, so P3 passes. M2 and M6 merge too much, which
P2 cannot see, and lose a cell, which P3 does. The asymmetric mutants
M1, M3 and M5 are the ones P4 catches. E1 is safe because the trees are
built merged: two splits whose quarters OR to four leaves of 0 would
each have had four leaves of 0 already. E2 is safe because the case
before it has taken every leaf of 1, and E4 because the finer grid
merges back to the same tree.

## Verification

Every arm prints the same output as `quad_tree_or.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends: no arm finishes. Under `karac run --interp`
the ★, pair, node and grid arms print the first seven lines and are
still on the 64 by 64 case when stopped at 300 s; `--interp` copies a
`shared enum` on every alias (kara B-2026-10-02-58). `karac run` and
`karac build` of the ★, pair and node arms do not finish within 300 s,
`karac build` while still compiling, and both stop the grid arm and the
differential at `level[2 * r][2 * c].clone()` ("chained indexed
receivers ... are deferred to v1.x"). The bench program, which has no
harness, builds and runs under the legacy `karac build` (see
Benchmarks). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 200 trees once from random
64 by 64 grids, each painted with blocks of a random power-of-two side
up to 16, a third of them 1, and then 40 cells flipped; then 300 times
over, every tree is ORed with another and the nodes of the answer
counted. Every implementation prints `200 trees, 300 rounds:
126990996 nodes, checksum 82023648`, the Kāra program under `karac
__mir-run` included (179 s).

Each mirror shares subtrees as the Kāra `shared enum` does: Rust with
`Rc<Quad>`, C with a reference count in each `malloc`'d node, released
when the answer has been counted, Go with pointers the collector frees,
and Python with tuples. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.51 to 1.59 s |
| Rust (`rustc -O`) | 1.69 to 1.89 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.75 to 1.83 s |
| Go | 2.09 to 2.27 s |
| Python | 9.9 to 10.1 s |
| Kāra (`karac build`, legacy) | 2.38 to 2.48 s |
| Kāra (`karac build --mir`) | 2.62 to 2.87 s |

The legacy `karac build` builds the bench program and prints the same
line, so `bench.sh` is as `scripts/new-bench.sh` wrote it. The `--mir`
row is timed at kara `af2123abc5` and is outside `bench.sh`. Under
`karac __mir-llvm-run` the program prints the same line in 3.8 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

The legacy row is about 1.35 times Rust's and the `--mir` row about
1.5 times. Counting the nodes alone, with no OR, takes 1.49 to 1.62 s on
`--mir` against 0.98 to 1.04 s for Rust: matching a `Split` binds its
four children with a count taken on each and a release call at the end
of the arm, though the match only reads them (kara
B-2026-10-14-9, below). Rust with the same four `Rc` clones forced into
its walk takes 1.31 s.

## Compiler findings

kara B-2026-10-14-9 (open), filed from this kata: on the MIR compiled
backend, matching a borrowed `shared enum` retains every handle the
pattern binds and releases each at the end of the arm, so a read-only
walk such as this kata's `count` pays a count up and an out-of-line
`drop.shared` call per child. Kara's `count(q: Quad)` borrows `q`; the
bindings out of it could be views.

The legacy failures above are not filed because legacy is frozen.
