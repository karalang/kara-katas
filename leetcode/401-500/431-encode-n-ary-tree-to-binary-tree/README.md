# 431. Encode N-ary Tree to Binary Tree

Design an algorithm to encode an N-ary tree into a binary tree and
decode the binary tree back to the original N-ary tree. An N-ary tree
is a rooted tree in which each node has no more than N children;
similarly, a binary tree is a rooted tree in which each node has no
more than 2 children. There is no restriction on how the algorithm
works; it only has to turn an N-ary tree into a binary tree and that
binary tree back into the original N-ary tree.

```
        1                      1
     /  |  \                  /
    3   2   4       ->       3
   / \                      / \
  5   6                    5   2
                            \   \
                             6   4
```

**Constraints:** the number of nodes is in `[0, 10^4]`;
`0 <= Node.val <= 10^4`; the height of the tree is at most 1000. Do
not use class members or global variables to store state.

## Approaches

The N-ary node is a `struct` holding its value and a `Vec[Node]` of
children, as in katas 428 and 429. The binary node is a
`shared struct` with `mut left` and `mut right` links, the binary tree
type the other katas use: an encoder makes a node and then fills in
its links. Each arm is a pair `encode(root) -> Option[TreeNode]` and
`decode(root) -> Option[Node]`.

| file | encoding | how |
|---|---|---|
| `encode.kara` ★ | left child, right sibling: a node's first child is its left child, and each child's next sibling is that child's right child (the drawing above) | one recursive walk each way |
| `encode_mirror.kara` | right child, left sibling: the mirror image | one recursive walk each way |
| `encode_iter.kara` | left child, right sibling | no recursion: encoding takes the tree by value and goes breadth first, moving each node's children into the next level; decoding is depth first with an explicit stack of frames |
| `encode_spine.kara` | a spine of link nodes valued -1: a node's left child starts a chain of links, one per child, each link's left child that child's encoding and its right child the next link. 2n - 1 binary nodes | one recursive walk each way |
| `differential.kara` | the four arms on 1,500 random trees, five properties |

All four run in O(n) both ways.

Every arm prints the same 9 lines: for each tree, the decoded tree
drawn as `value(child child ...)`, marked `FAILED` if it differs from
the original or if encoding it again gives a different binary tree.
The trees are the two LeetCode examples, six edge cases (the empty
tree, one node of each extreme value, a chain of 5, a root with 12
children, and a tree of 0s), and 300 random trees of 0 to 60 nodes,
summarized as a node count, a failure count and a checksum of the
drawings. The encoding never shows in the output, so the four arms
print the same lines. `encode.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms, with the two node
types defined once before them. Each of 1,500 random cases is a tree
of 0 to 39 nodes, wide or deep, with values below 10 or up to 10,000,
generated as a table of values and child lists:

| | property |
|---|---|
| P1 | decoding the encoding gives back the same tree |
| P2 | encoding the decoded tree gives back the same binary tree |
| P3 | the binary tree has n nodes (2n - 1 for the spine arm) and holds the tree's values, each once |
| P4 | the binary tree is the one the arm describes, drawn straight from the generator's table without building either tree |
| P5 | the empty tree encodes to no binary tree and back; a star of 1 to 200 leaves valued 0 and 10,000, and a chain of 2 to 201 nodes, come back |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, one to each arm's encoder and one
to its decoder, each run under `karac __mir-run`. All eight are
killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | left child, right sibling: each later sibling hangs left of the one before | P1 1272, P3 1215, P4 1272, P5 1493 |
| M2 | left child, right sibling: the decoder stops after a node's first child | P1 1272, P2 1272, P5 1493 |
| M3 | mirror: the first child hangs left | P1 1438, P2 1438, P3 1215, P4 1438, P5 1500 |
| M4 | mirror: the decoder skips each node's first child | P1 1438, P2 1438, P5 1500 |
| M5 | iterative: each later child replaces the left child | P1 1272, P3 1272, P4 1272, P5 1493 |
| M6 | iterative: the decoder drops every child after the first | P1 1272, P2 1272, P5 1493 |
| M7 | spine: link nodes valued 0 | P3 1438, P4 1438 |
| M8 | spine: the decoder puts each child first | P1 1271, P2 1271, P5 769 |

P3 and P4 look only at the binary tree, so they cannot see a decoder
mutant (M2, M4, M6, M8). P2 misses the encoder mutants M1 and M5: the
encoder is wrong the same way both times, and decoding its output
loses or reorders nodes in a way the second encoding reproduces. M7
is the one only the encoding properties catch: the link nodes are
still recognized by position, so every tree decodes correctly, and
only the values in the binary tree are wrong. One first pick was
replaced: a mirror decoder following the right link for siblings
decodes every subtree once for each of its ancestors, and the run was
killed when it exhausted memory.

## Verification

All four arms print the same output as `encode.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp` (the legacy tree-walk interpreter), and
`karac check` passes on every file. The differential prints
`30000 checks, 0 failures` under `karac __mir-run` and
`karac __mir-llvm-run`. The four arms and the differential also run
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends:

- LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build` match on
  the recursive, mirror and spine arms. The iterative arm, which moves
  each node's children out with `node.children.into_iter()` into a
  queue of `(Node, TreeNode)` pairs, aborts on all three with
  `free(): double free detected in tcache 2`. The bench program, the ★
  arm on 10,000-node trees, dies with a segmentation fault under
  `karac build`.
- The differential does not typecheck there: its harness passes
  `node.children[i]` to a bare, borrowing parameter, which the legacy
  checker reads as a move out of an index (`E_INDEX_MOVE_NON_COPY`).

Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. Each of 100 rounds builds a random
tree of 10,000 nodes (the problem's limit), each node hung under one of
the last 10 to 1,009 nodes before it, encodes it to a binary tree,
decodes that back, and folds the decoded tree's values in preorder
into a checksum. Every implementation prints `100 rounds of 10000
nodes: 1000000 decoded, checksum 803721566`; a 5-round cut of the Kāra
program under `karac __mir-run` prints the same as the C program cut
the same way.

The mirrors keep the Kāra program's memory model where the language
has one: Rust's binary nodes are `Rc<RefCell<TreeNode>>`, as a Kāra
`shared struct` is reference counted, and its n-ary nodes owned
values. C mallocs and frees both trees with no counts; Go leaves them
to its collector. Spot timings on a shared 4-core container, three runs
each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 0.26 to 0.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.27 to 0.33 s |
| Go | 0.27 to 0.31 s |
| C (`clang -O3`) | 0.30 to 0.34 s |
| Python | 2.8 to 2.9 s |

The frozen legacy `karac build` program crashes (see Verification), so
there is no legacy time. The Kāra program prints the same line under
`karac __mir-llvm-run` in 1.0 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings. The differential's harness first bound
`let ks = table.kids[i]`, a move out of an index that is refused
(`E_INDEX_MOVE_NON_COPY`). The diagnostic offers a borrow
(`ref table.kids[i]`), a copy or a swap; `karac fix` takes the copy,
`table.kids[i].clone()`, which is always correct and here allocates a
list per node where a borrow serves. The harness uses the borrow,
written by hand.
