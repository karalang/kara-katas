# 427. Construct Quad Tree

Given an `n * n` matrix `grid` of 0s and 1s only, represent `grid`
with a Quad-Tree and return its root.

A Quad-Tree is a tree in which each internal node has exactly four
children. Each node has two attributes: `val`, the value of the grid
it represents (any value is accepted for a node that is not a leaf),
and `isLeaf`, true if the node has no children. To build it from a
square region: if the region's cells all have the same value, the node
is a leaf with that value; otherwise it is an internal node whose four
children are built from the region's top-left, top-right, bottom-left
and bottom-right quarters.

The output is the tree serialized level by level, each node as
`[isLeaf, val]` and a missing child as `null`:

```
grid = [[0,1],[1,0]]  ->  [[0,1],[1,0],[1,1],[1,1],[1,0]]
grid = [[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],
        [1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0]]
  ->  [[0,1],[1,1],[0,1],[1,1],[1,0],null,null,null,null,
       [1,0],[1,0],[1,1],[1,1]]
```

**Constraints:** `n == grid.length == grid[i].length`;
`n == 2^x` where `0 <= x <= 6`.

## Approaches

The tree is a `shared enum`: a region is either `Leaf(bool)` or
`Split(Quad, Quad, Quad, Quad)`. LeetCode's node carries a value on
a split and four children on a leaf, neither of which means anything,
so the enum has no field for them. A plain `enum` cannot hold itself
in v1 (`E_ENUM_NESTED_ENUM_PAYLOAD`, which suggests `shared`);
`shared` makes each node a reference-counted handle.

| file | mechanism |
|---|---|
| `quad_tree.kara` ★ | divide, then merge: build the four quarters first, and if all four came back as leaves of one value, return one leaf instead. Each cell is read once: O(n^2) |
| `quad_tree_uniform.kara` | check, then divide: scan the region, return a leaf if every cell matches, otherwise split. A cell is scanned once per level above its leaf: O(n^2 log n) |
| `quad_tree_prefix.kara` | the same top-down split with an O(1) test: a 2-D prefix sum gives the number of 1s in any square, and a square is a leaf when that is 0 or the whole area |
| `quad_tree_levels.kara` | bottom up without recursion: an n by n grid of one-cell leaves, each pass merging every 2 by 2 block into one node until one is left |
| `differential.kara` | the four arms on 1,500 random grids, five properties |

Every arm prints the same 10 lines: the two LeetCode examples, seven
edge cases (a 1 by 1 grid of each value, a uniform 2 by 2, a 2 by 2
with one cell different, a 4 by 4 checkerboard, a 4 by 4 of blocks
with one cell different, and a 64 by 64 grid of 0s with one 1, which
splits at every level down to it), and for 300 random grids of side 1
to 64 the number of nodes and leaves and a checksum of the
serializations. `quad_tree.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms, with the tree type
defined once before them. Each of 1,500 random cases is a grid of side
1 to 32, made of blocks of a random power-of-two side, each one value,
with up to three cells flipped:

| | property |
|---|---|
| P1 | the leaves tile the grid: every cell lies in exactly one leaf, and every leaf's square holds only the leaf's value |
| P2 | no split holds four leaves of one value |
| P3 | flipping every cell flips every leaf and keeps the shape |
| P4 | transposing the grid swaps every split's top right and bottom left |
| P5 | doubling each cell into a 2 by 2 block gives the same tree; a grid of one value is one leaf; one cell different in a grid of side 2^k gives 4k + 1 nodes |

P1 and P2 together pin the answer down: a tree whose leaves tile the
grid with uniform squares, and that never splits a square it could
merge, is the quad tree. It prints `1500 cases, 4 arms, 30000 checks,
0 failures` under `karac __mir-run`, and a count for each property
when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | merge: four leaves merge without comparing the last | P1 524, P5 321 |
| M2 | merge: a split stores top right and bottom left swapped | P1 943 |
| M3 | uniform: the scan skips the last column | P1 663, P2 235, P4 736, P5 956 |
| M4 | uniform: a leaf takes the opposite value | P1 1500 |
| M5 | prefix: the top right quarter is built from the bottom left | P1 948, P2 555, P4 939, P5 741 |
| M6 | prefix: a full square is compared with its side, not its area | P1 342, P2 778, P3 1115, P5 1327 |
| M7 | levels: a block's row is found with half the stride | P1 873, P4 838, P5 1116 |
| M8 | levels: the bottom two quadrants are swapped | P1 954, P4 1038 |

P1 kills all eight; the other properties are relations between two
runs of the same arm, so they miss a mutant that is wrong in the same
way on both grids. P3 sees only M6, the one mutant that treats 0s and
1s differently. P4 misses M2 because transposing the grid and swapping
top right with bottom left undo each other. Two first picks were
replaced: one prefix-sum mutant overflowed `i64` (its sums grow
exponentially), and one that miscounted a square sent a one-cell
square into a split of size 0 and indexed out of bounds.

## Verification

All four arms print the same output as `quad_tree.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms also run clean under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output
identical, no error, no leak.

On the frozen legacy backends:

- LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build` match on
  the merge, uniform and prefix arms. The levels arm, which keeps the
  nodes of a level in a `Vec[Quad]`, aborts in `karac build` with
  `malloc_consolidate(): unaligned fastbin chunk detected` and under
  `KARAC_AUTO_PAR=1` with `malloc(): unaligned tcache chunk detected`,
  and prints nothing under LLJIT.
- The differential does not typecheck there: `solve` passes its
  borrowed grid to each arm's `construct`, whose bare parameter
  borrows under the current rules but not under the legacy checker
  (`expected 'Vec[Vec[i64]]', found 'ref Vec[Vec[i64]]'`).
- `karac run --interp`, the tree-walk interpreter, takes 12 s on the
  8 by 8 example and 48 s on a 16 by 16 grid, so the arms' 64 by 64
  cases had not finished after 39 minutes.

Legacy is frozen, so these are noted, not filed. The bench program
builds and runs there.

## Benchmarks

The bench program uses the ★ arm. Each of 20,000 rounds paints one
random aligned block of a 64 by 64 grid (the problem's largest) a
random value, flips one random cell, rebuilds the tree and counts its
nodes into a checksum. Every implementation prints `20000 rounds on a
64 by 64 grid: 2120032 nodes, checksum 209247122`; a 200-round cut of
the Kāra program under `karac __mir-run` prints the same as the C
program cut the same way. The ★ arm makes a leaf for every cell before
merging, so a round allocates about 5,500 nodes whatever the tree's
final size; the mirrors keep that. C mallocs every node and frees four
merged leaves when it replaces them, Rust uses `Rc<Quad>` (the
reference-counted handle a `shared enum` is), Go uses pointers, and
Python tuples. Spot timings on a shared 4-core container, three runs
each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.69 to 1.73 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.16 to 2.25 s |
| Rust (`rustc -O`) | 2.24 to 2.33 s |
| Go | 4.1 to 4.2 s |
| Kāra (legacy `karac build`) | 13.4 to 18.6 s |
| Python | 14.0 to 15.3 s |

Allocation is likely most of every implementation's time (not
measured). The frozen legacy backend is far behind, level with
Python; it was not profiled, since legacy is frozen. The Kāra program
prints the same line under `karac __mir-llvm-run` in 3.8 s, compile
included; that JITs the MIR's IR without optimization passes, so it
is not a benchmark.

## Compiler findings

No new findings.
