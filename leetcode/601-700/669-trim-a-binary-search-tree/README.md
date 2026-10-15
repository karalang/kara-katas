# 669. Trim a Binary Search Tree

Given the root of a binary search tree and the bounds `low` and `high`,
remove every node whose value lies outside them and return the root of
what is left. Each kept node keeps its descendants that are kept, in the
same order, so the answer is unique.

```
root = [1,0,2], low = 1, high = 2
    ->  [1,null,2]
root = [3,0,4,null,2,null,null,1], low = 1, high = 3
    ->  [3,2,null,1]
```

**Constraints:** 1 to 10,000 nodes with distinct values from 0 to
10,000; 0 <= `low` <= `high` <= 10,000.

## Approaches

Every arm is `fn trim_bst(root: Option[TreeNode], low: i64, high:
i64) -> Option[TreeNode]` over a `shared struct TreeNode`. Three of them
rewire the tree they are given; the copy arm builds a new one and leaves
its input as it was.

| file | mechanism |
|---|---|
| `trim_a_binary_search_tree.kara` ★ | recursion: a node below `low` gives way to its right subtree trimmed, one above `high` to its left, and one in range keeps both trimmed; in place, O(nodes) |
| `trim_a_binary_search_tree_edges.kara` | the new root found on the way down, then only the two paths that can hold nodes out of range, its leftmost and its rightmost, repaired; in place, O(height) |
| `trim_a_binary_search_tree_stack.kara` | every kept node taken from a stack, each child out of range spliced out until one in range takes its place; in place, O(nodes) |
| `trim_a_binary_search_tree_copy.kara` | the ★ arm's recursion building new nodes for the kept ones; O(nodes) |
| `differential.kara` | the four arms against a definition that hangs each kept node from its nearest kept ancestor, five properties |

Every arm prints the same 19 lines: the two LeetCode examples; eight
small cases (one node, kept and cut; a tree of seven kept whole, cut
whole, cut to one value, and cut with its root going from below and from
above; and a tree of nine), each before and after in LeetCode's level
order; a tree of the problem's largest size, 0 to 9,999 inserted in a
random order, and five trims of fresh copies of it, each with its size,
height and a checksum; a chain of 10,000, each node the right child of
the one before, trimmed two ways, which takes the ★ arm's recursion
nearly 10,000 deep; and a checksum of 1,000 random trees, each trimmed
to a random range. `trim_a_binary_search_tree.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which reads the answer straight off the problem's wording: each kept
node hangs from its nearest kept ancestor in the original tree, on the
side its value says, and the root is the kept node with none. It records
each kept node's value, parent and side, and the trimmed tree must
record the same. Each of 2,000 random trees inserts up to 15 values from
0 to 29, repeats skipped, and is trimmed to a random range that may
reach past either end. Every arm gets a fresh tree for every call, since
three of them rewire it.

| | property |
|---|---|
| P1 | every kept node has the parent and side the definition gives it |
| P2 | the tree's values in order are the original's within the range |
| P3 | it is a binary search tree with every value within the range |
| P4 | trimming it again to the same range changes nothing |
| P5 | it is the same as trimming to `[low, 1000]` and then to `[-1000, high]` |

It prints `2000 trees (13073 nodes), 4 arms, 40000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a node equal to low cut | P1 369, P2 369 |
| M2 | ★: a kept node's left subtree left untrimmed | P1 611, P2 611, P3 611, P5 247 |
| M3 | edges: a node below low cut with its right subtree | P1 183, P2 183, P5 119 |
| M4 | edges: a node equal to high cut on the right edge | P1 133, P2 133 |
| M5 | stack: a child below low replaced by its left subtree | P1 680, P2 680 |
| M6 | stack: left children never visited | P1 172, P2 172, P3 172, P5 195 |
| M7 | copy: a node below low dropped with its right subtree | P1 680, P2 680 |
| M8 | copy: a kept node's right subtree shared untrimmed | P1 474, P2 474, P3 474 |
| E1 | ★: above high as at least high + 1 | 0 |
| E2 | edges: below low as at most low - 1 | 0 |
| E3 | stack: each right child brought into range twice | 0 |
| E4 | copy: the left subtree trimmed to at most the node | 0 |

P1 and P2 kill all eight. P3, a search tree within the range, sees the
three that leave nodes out of range in place, M2, M6 and M8; the other
five only lose nodes that belonged or cut one at the edge of the range,
and what is left is still a search tree within it. P4, trimming twice,
sees none: each mutant leaves a tree on which it makes no further
change. P5 sees M2, M3 and M6, whose results differ when the two bounds
are applied one at a time. The four survivors cannot change an answer:
on whole numbers `>= high + 1` is `> high` and `<= low - 1` is `< low`;
a child already in range stays as it is; and a node's left subtree holds
only values below the node, so trimming it to at most the node's value
cuts nothing more.

## Verification

Every arm prints the same output as `trim_a_binary_search_tree.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `83b41fb1d0` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm at type checking: the
harness's `shuffled` hands `seed`, already a `mut ref` parameter, on
with the `mut` marker design.md asks for, which legacy rejects. Their
interpreter runs the differential to the same line, but the program
their `karac build` makes of it aborts in glibc's allocator every time,
with `malloc(): unaligned fastbin chunk detected 3`: heap corruption in
legacy code generation. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It shuffles 0 to 9,999 once; then each
of 300 rounds inserts them into a fresh tree of the problem's largest
size, trims it to a range picked by the round, and puts what is kept, in
preorder, into a checksum. Every implementation prints `10000 nodes,
300 rounds: checksum 212249304`, the Kāra program under `karac
__mir-run` included (in 53 s).

Each implementation is the same insertion and the same recursion, a tree
made afresh for each round. Kāra's nodes are a `shared struct` and
Rust's `Rc<RefCell<TreeNode>>`, both freeing a node when its last handle
goes; C's are `malloc`ed, and its trim frees the nodes it cuts away, the
same work; Go's and Python's are collected. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.42 to 0.53 s |
| Rust (`rustc -O`) | 0.60 to 0.74 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.59 to 0.63 s |
| Go | 0.42 to 0.47 s |
| Python | 2.9 to 3.3 s |
| Kāra (`karac build --mir`) | 0.50 to 0.63 s |
| Kāra, legacy (`karac build`) | 0.50 to 0.58 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 2.0 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy, a little ahead of Rust's
`Rc<RefCell<TreeNode>>`, and within about a fifth of C and Go, all of
them spending most of the time inserting 10,000 nodes each round. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy failures
above are not filed because legacy is frozen.
