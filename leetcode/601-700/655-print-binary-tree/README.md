# 655. Print Binary Tree

Given the root of a binary tree, print it into a grid of strings. With
the tree's height `h` counted in edges, the grid has `h + 1` rows and
`2^(h + 1) - 1` columns. The root goes in the middle of the top row; a
node at row `r`, column `c` puts its left child at row `r + 1`, column
`c - 2^(h - r - 1)`, and its right child at column `c + 2^(h - r -
1)`. Every other cell is the empty string.

```
root = [1,2]          ->  [["","1",""],
                           ["2","",""]]
root = [1,2,3,null,4] ->  [["","","","1","","",""],
                           ["","2","","","","3",""],
                           ["","","4","","","",""]]
```

**Constraints:** 1 to 2^10 nodes, at most 10 levels deep, values from
-99 to 99.

## Approaches

Every arm is `fn print_tree(root: Option[TreeNode]) -> Vec[Vec[String]]`
over a `shared struct TreeNode`. The harness reads trees from LeetCode's
level order.

| file | mechanism |
|---|---|
| `print_binary_tree.kara` ★ | the definition: the height first, then one walk down the tree, each node placing its children `2^(h - r - 1)` columns to either side; O(rows * columns) |
| `print_binary_tree_levels.kara` | the same places found breadth first, a `VecDeque` holding each node with its row and column; O(rows * columns) |
| `print_binary_tree_halves.kara` | each node owns a span of columns and sits in its middle, its children splitting what is left; no step size computed; O(rows * columns) |
| `print_binary_tree_merge.kara` | bottom up: a subtree's grid is its value over its children's grids side by side, one empty column between; O(rows^2 * columns) |
| `differential.kara` | the four arms against a second definition, five properties |

Every arm prints the same 20 lines: the two LeetCode examples and three
more trees (one node; a chain down the right; a full tree of three
levels with the smallest and largest values), each with its grid; the
cells filled and a checksum of 200 random trees at most 1 to 6 levels
deep; and two trees of the problem's deepest, 10 levels, one full and
one sparse, each with its size and checksum. `print_binary_tree.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a second
definition, which computes no step size: each place in a full tree as
deep as the given one is written as its path from the root, `L` and `R`,
with `M` added, and the paths are sorted. Since `L` < `M` < `R`, that
puts every place after its left subtree and before its right one, so a
place's column is its rank in the sorted list and its row is its path's
length. Each of 500 random trees is 1 to 7 levels deep at most, each
child there with chance 30 to 100 in 100.

| | property |
|---|---|
| P1 | the grid is the definition's |
| P2 | as many rows as levels, and `2^rows - 1` columns in each |
| P3 | one filled cell for each node |
| P4 | the mirrored tree prints each row reversed |
| P5 | read column by column, the filled cells give the in-order reading |

It prints `500 trees (4649 nodes), 4 arms, 10000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left child placed to the right | P1 301, P3 249, P4 341, P5 301 |
| M2 | ★: the last row never filled | P1 341, P3 341, P5 341 |
| M3 | levels: a right child one column short | P1 310, P4 341 |
| M4 | levels: two columns too many | P1 500, P2 500, P3 500, P5 500 |
| M5 | halves: a node placed at the start of its span | P1 341, P4 341, P5 301 |
| M6 | halves: the right child's span taking the middle too | P1 310, P4 341 |
| M7 | merge: no empty column between the two halves | P1 341, P2 341, P3 341, P5 341 |
| M8 | merge: the right half printed on the left too | P1 341, P3 269, P4 341, P5 341 |
| E1 | ★: the root's column taken as half the width | 0 |
| E2 | levels: the empty cells made with `String.new()` | 0 |
| E3 | halves: the middle rounded up | 0 |
| E4 | merge: no rows for a depth of 0 or less | 0 |

P1 kills all eight. P2 sees the two that change the grid's size, M4 and
M7. P3 sees the five that lose a node or write over one:
M1, M2, M4, M7 and M8. P4 sees M1, M3, M5, M6 and M8, which put a node
where the mirror image does not. P5 misses M3 and M6, which move a right
child one column toward its parent but leave it to the right of
everything before it, so the column-by-column reading is still in order.
The four survivors cannot change an answer: the column count is odd, so
half of it rounded down is the middle; `String.new()` and an empty
string literal are both empty; every span is odd, so its middle needs no
rounding; and the merge never asks for a grid of no rows.

## Verification

Every arm prints the same output as `print_binary_tree.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `abbdbaf131` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness's `random_tree` hands `seed`, already a `mut ref`
parameter, on with the `mut` marker design.md asks for, which legacy
rejects. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes eight random trees once, up
to 10 levels deep, the problem's deepest, each child there with chance
85 in 100; then 10,000 rounds each print one, picked by the round, and
put its filled cells and their characters into a checksum. Every
implementation prints `8 trees, 10000 rounds: 102300000 cells, checksum
276538285`, the Kāra program under `karac __mir-run` included (in
219 s).

Each implementation is the same walk. Kāra's nodes are a `shared
struct`, freed when the last handle goes; Rust's
`Rc<RefCell<TreeNode>>`; C's are `malloc`ed, and its grid's strings
freed after each round; Go's and Python's are collected. Spot timings on
a shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine), each including making the trees:

| | time |
|---|---|
| C (`clang -O3`) | 0.60 to 0.63 s |
| Rust (`rustc -O`) | 0.53 to 0.62 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.66 to 0.85 s |
| Go | 0.60 to 0.63 s |
| Python | 5.6 to 5.9 s |
| Kāra (`karac build --mir`) | 1.28 to 1.38 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program for the same `mut` marker. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata without the
marker builds under legacy and takes 3.21 to 3.50 s. Under `karac
__mir-llvm-run` the program prints the same line in 4.1 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build takes well under half of legacy's time, inside the
M2 bar, and about twice Rust's. The rounds make 102 million cells, each
its own string, so most of the work is likely allocating and freeing
them. The comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
