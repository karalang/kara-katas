# 536. Construct Binary Tree from String

You need to construct a binary tree from a string of parentheses and
integers. The whole string is a tree: an integer followed by zero, one
or two pairs of parentheses. The integer is the root's value, and each
pair of parentheses holds a child tree written the same way. The left
child comes first whenever there is one.

```
s = "4(2(3)(1))(6(5))"      ->  [4,2,6,3,1,5]
s = "4(2(3)(1))(6(5)(7))"   ->  [4,2,6,3,1,5,7]
s = "-4(2(3)(1))(6(5)(7))"  ->  [-4,2,6,3,1,5,7]
```

**Constraints:** `0 <= s.length <= 3 * 10^4`; `s` consists of digits,
`(`, `)` and `-` only.

## Approaches

Every arm is `fn str2tree(s: Str) -> Option[TreeNode]` over the
`shared struct TreeNode` of the other tree katas. A string with one
pair of parentheses after a number can only mean a left child, so a
node with a right child always has a left one.

| file | mechanism |
|---|---|
| `str2tree.kara` ★ | recursive descent: one position that every call moves on, reading a number and then a subtree for each `(`; O(n) |
| `str2tree_stack.kara` | one pass with a stack of the nodes whose parentheses are open: a number hangs under the top, on the left if free, and goes on the stack; `)` takes it off; O(n) |
| `str2tree_split.kara` | split and recurse: the left subtree's text runs to the `)` that closes the first `(`, the rest less its parentheses is the right's; O(n · height) |
| `str2tree_depth.kara` | depths: the `(` still open before a number is its depth, and in preorder its parent is the last node met one level up; O(n), nothing popped |
| `differential.kara` | the four arms against random trees written out, five properties |

Every arm prints the same 13 lines. Ten strings are read and shown
level by level, as LeetCode writes a tree, with whether the tree
written back is the string: the three examples, the empty string, one
node, `-0` (which reads as 0 and so is not written back the same),
zero and negative values, a left child only, a chain to the left, and
a tree of negative values. Then 300 random trees of 0 to 60 nodes with
values from -1000 to 1000 are written as the problem writes them and
read back, and last the largest cases: a random tree of 5,500 nodes
written in 29,672 characters, near the problem's most, and a chain of
5,000 nodes to the left, 4,999 deep. `str2tree.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each arm is held to
the properties below on 1,000 random trees of 0 to 40 nodes, written
as the problem writes them, with values from -1000 to 1000 three times
in four and from -10^7 to 10^7 otherwise.

| | property |
|---|---|
| P1 | the written form of a tree reads back as that tree |
| P2 | what is read, written as the problem writes it, is the string read |
| P3 | `v(A)(B)`, for two more random trees `A` (1 to 14 nodes) and `B` (0 to 14) and a value `v`, reads as `v` over what `A` and `B` read as |
| P4 | every number's sign turned turns every value's |
| P5 | one node per number, and as tall as the parentheses are deep |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the sign never read | P1 952, P2 952, P3 510, P4 981 |
| M2 | ★: the second subtree hung on the left too | P1 901, P2 901, P3 935, P5 901 |
| M3 | stack: a `)` takes nothing off | P1 901, P2 901, P3 935, P5 901 |
| M4 | stack: a child goes left while the right is free | P1 901, P2 901, P3 935, P5 901 |
| M5 | split: the left subtree's text built as the right | P1 957, P2 901, P3 1000, P5 901 |
| M6 | split: the right subtree's text taken as empty | P1 901, P2 901, P3 935, P5 901 |
| M7 | depth: every node hung from the last node at depth 0 | P1 930, P2 930, P3 997, P5 930 |
| M8 | depth: a `)` never closes a level | P1 901, P2 901, P3 935, P5 901 |
| E1 | ★: a child read whenever the next byte is not `)` | 0 |
| E2 | stack: the number read up to the next parenthesis | 0 |
| E3 | split: a right subtree looked for only past `j + 2` | 0 |
| E4 | depth: the deeper levels dropped before the node is kept | 0 |

Five of the mutants fail the same 901 trees: the ones with a node that
has two children, the only place a right subtree is read. M5 fails
every tree of two nodes or more on P1, since it builds every left
subtree on the right; written back, a lone right child reads the same
as a lone left one, so P2 sees only the 901. M7 fails every tree more
than two levels deep. P4 kills only M1: it compares an arm with itself
on a shape and on that shape's negation, so a mistake in the shape
cancels out. Every wrong shape fails P5, which counts nodes and depth
against the string alone. E1 to E3 change only what a well-formed
string never shows: after a number comes a `(`, a `)` or the end, and
a right subtree takes at least three characters. E4 drops entries that
are always written again before they are read.

## Verification

Every arm prints the same output as `str2tree.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `20000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program.

The frozen legacy backends refuse every file at type checking: legacy
cannot compare the harness's `String` with a `Str` ("cannot compare
'String' and 'StringSlice'"), takes the split arm's `s[0..i]` for a
move out of an index (`E_INDEX_MOVE_NON_COPY`), and types the items of
a slice's `iter()` by value, so it refuses the differential's `*c`.
The bench program passes its type checker and fails at codegen, "no
handler for method 'is_empty' on variable 's' in `str2tree`", a `Str`
parameter. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random trees of 5,500
nodes with values from -1000 to 1000 and writes each once, in near
30,000 characters, the problem's most; then it reads each string into a
tree in each of 100 rounds and walks the tree for a checksum. Every
implementation prints `20 strings, 100 rounds: 11000000 nodes, checksum
499657364`, the Kāra program under `karac __mir-run` included (in
117 s).

The Rust mirror uses LeetCode's tree type,
`Option<Rc<RefCell<TreeNode>>>`, as the reference-counted counterpart of
the ★ arm's `shared struct`; C mallocs each node and frees the tree
after the walk, and Go and Python leave it to their collectors. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.66 to 0.71 s |
| Rust (`rustc -O`) | 0.75 to 0.77 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.80 to 0.84 s |
| Go | 0.79 to 0.82 s |
| Python | 12.6 to 13.1 s |
| Kāra (`karac build --mir`) | 0.89 to 1.01 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`5fa208779d`.

Under `karac __mir-llvm-run` the program prints the same line in
2.9 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
