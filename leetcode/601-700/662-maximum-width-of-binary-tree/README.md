# 662. Maximum Width of Binary Tree

Given the root of a binary tree, return its maximum width, the largest
width of any of its levels. A level's width is the length from its
leftmost node to its rightmost, counting the missing nodes between them
as if the tree were complete down to that level. The answer fits in a
32-bit signed integer.

```
root = [1,3,2,5,3,null,9]              ->  4
root = [1,3,2,5,null,null,9,6,null,7]  ->  7
root = [1,3,2,5]                       ->  2
```

**Constraints:** 1 to 3,000 nodes; values from -100 to 100.

## Approaches

Every arm is `fn width_of_binary_tree(root: Option[TreeNode]) ->
i64`, with `TreeNode` a `shared struct`. All number a level's places as
a full tree would, the children of place `p` at `2p` and `2p + 1`, but
places double at every level, so a deep tree's would not fit in 64 bits;
each arm keeps them small its own way.

| file | mechanism |
|---|---|
| `maximum_width_of_binary_tree.kara` ★ | a level at a time, each node with its place, each level's places counted from its first node's; O(nodes) |
| `maximum_width_of_binary_tree_dfs.kara` | a walk that goes left first, so it meets each depth's leftmost node first, keeps that node's place and measures every later node at the depth against it; O(nodes) |
| `maximum_width_of_binary_tree_queue.kara` | one first-in, first-out queue of nodes with their depths and places, the first out at each depth its leftmost; O(nodes) |
| `maximum_width_of_binary_tree_paths.kara` | each depth's leftmost and rightmost paths from the root, 0 for left and 1 for right, found by two walks and subtracted digit by digit; O(nodes + height^2) |
| `differential.kara` | the four arms against a definition that numbers places straight from the root, five properties |

Every arm prints the same 11 lines: the three LeetCode examples; one
node, and a full tree of four levels; two chains spreading out 30 levels
below the root, whose width, 1,073,741,824, is the widest of that shape
a 32-bit integer holds; two chains of 1,499 nodes growing toward each
other, 2 wide though their places need 1,499 binary digits; a zigzag
chain of 2,985 nodes with a full tree of four levels at its foot; a
checksum of the widths of 200 random trees at most 12 levels deep; and
two of the problem's largest, 3,000 nodes grown at random.
`maximum_width_of_binary_tree.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which numbers every node's place straight from the root and takes each
level's first and last. That works only while the places fit in 64 bits,
so each of 1,000 random trees is 1 to 9 levels deep, each child there
with chance 30 to 100 in 100.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the mirrored tree is as wide |
| P3 | the width is at least the most nodes on any level and at most the places on the deepest |
| P4 | under a new root as both its children, the width is the places on the tree's deepest level plus that level's width |
| P5 | hung at the foot of a chain of 100 random steps, where its places need over 100 binary digits, the tree is as wide |

It prints `1000 trees (25069 nodes), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each level's width taken to its second node, not its last | P1 395, P2 203, P3 341, P4 498 |
| M2 | ★: a right child numbered like a left one | P1 554, P3 554, P4 1000 |
| M3 | dfs: each width one short | P1 1000, P3 662, P4 1000 |
| M4 | dfs: a right child numbered one further right | P1 554, P3 306, P4 1000 |
| M5 | queue: a left child numbered from its parent's own place | P1 203, P2 261, P3 103, P4 197, P5 446 |
| M6 | queue: a right child numbered left of its sibling | P1 554, P3 554, P4 1000 |
| M7 | paths: the first step of every path skipped | P1 345, P3 303, P4 1000, P5 345 |
| M8 | paths: both walks going left first | P1 554, P3 554, P4 1000 |
| E1 | ★: both children numbered one further right | 0 |
| E2 | dfs: an empty subtree counted as width 1 | 0 |
| E3 | queue: the loop running until the head reaches the end | 0 |
| E4 | paths: a path kept whenever it is at least as deep as those kept | 0 |

P1, P3 and P4 each kill all eight. P2, the mirror, sees only M1 and
M5; the other six get a tree and its mirror image wrong by the same
amount. P5 sees the two whose error depends on how deep the tree sits:
M5, which numbers a left child from its parent's whole place rather than
from its level's first, and M7, which skips each path's first step, a
step every node under the chain shares. The four survivors cannot change
an answer: numbering both children one place further right moves every
place on a level alike; a tree with a node in it is at least 1 wide
anyway; the head never passes the queue's end; and a walk never gets
more than one level below the paths it has kept.

## Verification

Every arm prints the same output as `maximum_width_of_binary_tree.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints its line under all three. `karac check`
passes all four arms, the differential and the bench program. All with
the compiler at kara `8d40e1a762` for the debug build and `057e29e74f`
for the release build that runs `check` and `__mir-run`, with runtime
archives newer than the last `runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness hands `seed`, already a `mut ref` parameter, on
with the `mut` marker design.md asks for, and the ★ arm and the
differential read through `*` an element that `iter()` hands them, which
legacy types as a plain `i64`. Legacy rejects both. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It grows eight trees of the problem's
largest, 3,000 nodes each, at most 31 levels deep, once; then each of
20,000 rounds measures the width of one, picked by the round, and puts
it into a checksum. Every implementation prints `8 trees of 3000 nodes,
20000 rounds: checksum 95934472`, the Kāra program under `karac
__mir-run` included (in 215 s).

Each implementation is the same walk a level at a time, each level a new
list of nodes with their places. Kāra's nodes are a `shared struct`,
Rust's `Rc<RefCell<TreeNode>>`, C's `malloc`ed, with its levels
`malloc`ed and grown by `realloc`, and Go's and Python's collected. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine), each including growing the
trees:

| | time |
|---|---|
| C (`clang -O3`) | 0.44 to 0.46 s |
| Rust (`rustc -O`) | 0.69 to 0.77 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.62 to 0.89 s |
| Go | 1.97 to 2.19 s |
| Python | 6.9 to 8.0 s |
| Kāra (`karac build --mir`) | 0.66 to 0.71 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking, for `*place` and the same `mut` marker. That
edit is by hand, on top of the `scripts/new-bench.sh` output. A copy
outside the kata without either builds under legacy and takes 0.63 to
0.69 s. Under `karac __mir-llvm-run` the program prints the same line in
3.0 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is level with legacy and with Rust, whose nodes are
reference counted too, at about one and a half times C. Go's extra time
is likely in growing a new slice for every level and collecting them;
that is not profiled. The comparison with C and Rust waits until after
M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
