# 428. Serialize and Deserialize N-ary Tree

Serialization is converting a data structure into a sequence of bits
so that it can be stored or sent, and reconstructed later. Design an
algorithm to serialize and deserialize an N-ary tree, a rooted tree in
which each node has no more than N children. There is no restriction
on how the algorithm works; it only has to turn a tree into a string
and that string back into the original tree.

LeetCode's own level-order format, for example, writes the tree

```
        1
     /  |  \
    3   2   4
   / \
  5   6
```

as `[1,null,3,2,4,null,5,6]`, each group of children closed by a
`null`. Any format will do.

**Constraints:** the number of nodes is in `[0, 10^4]`;
`0 <= Node.val <= 10^4`; the height of the tree is at most 1000. Do
not use class members or global variables to store state.

## Approaches

A node is a `struct` holding its value and a `Vec[Node]` of children:
the tree is an owned value, and each codec is a pair
`serialize(root: ref Option[Node]) -> String` and
`deserialize(data: Str) -> Option[Node]`. Each codec writes the empty
tree as the empty string.

| file | format | decoding |
|---|---|---|
| `codec.kara` ★ | preorder, each value followed by its number of children: `1 3 3 2 5 0 6 0 2 0 4 0` | one recursive read: a node's count says how many subtrees follow it |
| `codec_brackets.kara` | each value followed by its children in brackets: `1[3[5 6] 2 4]` | recursive descent over the bytes |
| `codec_markers.kara` | preorder, each node closed by `#`: `1 3 5 # 6 # # 2 # 4 # #` | a node takes children until it meets its own `#` |
| `codec_levels.kara` | LeetCode's level order: `1 null 3 2 4 null 5 6` | breadth first through a flat table of values and child indexes, then the tree assembled from the table |
| `differential.kara` | the four codecs on 1,500 random trees, five properties |

All four run in O(n) both ways. The level-order codec goes through a
table in both directions because a child is an owned value inside its
parent: there is no handle to a node to keep in a queue, so the
breadth-first order is worked out on indexes instead.

Every arm prints the same 9 lines: for each tree, the decoded tree
drawn as `value(child child ...)`, marked `FAILED` if it differs from
the original or if encoding it again gives different text. The trees
are the two LeetCode examples, six edge cases (the empty tree, one
node of each extreme value, a chain of 5, a root with 12 children, and
a tree of 0s), and 300 random trees of 0 to 60 nodes, summarized as a
node count, a failure count and a checksum of the drawings. The format
never shows in the output, so the four arms print the same lines.
`codec.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four codecs, with the node type
defined once before them; the harness clones trees, so that copy
derives `Clone`. Each of 1,500 random cases is a tree of 0 to 39 nodes,
wide or deep, with values below 10 or up to 10,000:

| | property |
|---|---|
| P1 | decoding the encoding gives back the same tree |
| P2 | encoding the decoded tree gives back the same text |
| P3 | two trees get the same text exactly when they are the same tree |
| P4 | the tree grafted 1 to 5 times under a new root comes back, each copy the same as the tree |
| P5 | the empty tree is the empty text and back; a star of 1 to 200 leaves valued 0 and 10,000, and a chain of 2 to 201 nodes, come back |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, one to each codec's encoder and
one to its decoder, each run under `karac __mir-run`. All eight are
killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | counts: the decoder reads one child too few | P1 1425, P2 1425, P4 1460, P5 1500 |
| M2 | counts: the encoder caps every count at 3 | P1 629, P2 629, P4 976, P5 1478 |
| M3 | brackets: the decoder reads digits in base 9 | P1 758, P2 758, P4 1500, P5 1492 |
| M4 | brackets: the encoder writes each value twice | P1 1456, P2 1456, P4 1500, P5 1500 |
| M5 | markers: the decoder leaves each node's `#` unread | P1 1255, P2 1255, P4 1420, P5 1492 |
| M6 | markers: the encoder writes children in reverse | P1 1253, P2 1253, P4 1253, P5 789 |
| M7 | levels: the decoder gives each child to the node before its parent | P1 1379, P2 1379, P4 1425, P5 1492 |
| M8 | levels: the encoder writes the parent's value for each child | P1 1425, P2 1373, P4 1460, P5 1500 |

No mutant fails P3, which compares each tree with one other random
tree: two random trees almost never collide, even under an encoder
that can (M8 writes both 1(2) and 1(3) as `1 null 1`).
Most first-choice edits to a decoder crash on malformed input (an
index past the end) rather than decode wrongly, so the decoder
mutants were picked to stay in bounds.

## Verification

All four arms print the same output as `codec.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp` (the legacy tree-walk interpreter), and
`karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on all three. The four arms and the
differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy compiled backends (LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`) cannot compile any arm or the
differential: each `deserialize(data: Str)` starts with
`data.len() == 0`, and legacy codegen has no `len()` on a `Str`
parameter (`no handler for method 'len' on variable 'data'`). Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ codec. Each of 100 rounds builds a
random tree of 10,000 nodes (the problem's limit), each node hung
under one of the last 1 to 1,000 nodes before it, encodes it, decodes
the text, and folds the text's length and the decoded tree's value sum
into a checksum. Every implementation prints `100 rounds of 10000
nodes: 6865085 characters, checksum 157317232`; a 5-round cut of the
Kāra program under `karac __mir-run` prints the same as the C program
cut the same way. The Kāra decoder's `split` makes a `String` of each
word, so the C and Rust mirrors copy each word out too; Go's
`strings.Split` and Python's `split` do what those languages do. Spot
timings on a shared 4-core container, three runs each (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O`) | 0.36 to 0.40 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.36 to 0.40 s |
| Go | 0.42 to 0.46 s |
| C (`clang -O3`) | 0.47 to 0.49 s |
| Python | 3.4 to 3.5 s |

C trails Rust here, likely on `snprintf` and a `malloc` per word (not
profiled). The frozen legacy `karac build` cannot build the program
(see Verification), so there is no legacy time. The Kāra program
prints the same line under `karac __mir-llvm-run` in 2.7 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

## Compiler findings

No new findings. Writing the harness's `tree(val, children)` helper
with a bare `children: Vec[Node]` parameter, and moving it into the
node, is refused under the borrow-by-default rule; `karac fix` rewrote
the parameter to `own Vec[Node]`, the Mend loop working as intended.
