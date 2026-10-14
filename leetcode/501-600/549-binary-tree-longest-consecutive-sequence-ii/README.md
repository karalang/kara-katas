# 549. Binary Tree Longest Consecutive Sequence II

Given the `root` of a binary tree, return the length of the longest
consecutive path in the tree. A consecutive path is a path where the
values of the consecutive nodes in the path differ by one. This path can
be either increasing or decreasing: for example, `[1,2,3,4]` and
`[4,3,2,1]` are both considered valid, but the path `[1,2,4,3]` is not
valid. On the other hand, the path can be in the child-parent-child
order, where not necessarily be parent-child order.

```
root = [1,2,3]  ->  2   ([1,2] or [2,1])
root = [2,1,3]  ->  3   ([1,2,3] or [3,2,1])
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 3 * 10^4]`; `-3 * 10^4 <= Node.val <= 3 * 10^4`.

## Approaches

Every arm is `fn longest_consecutive(root: Option[TreeNode]) ->
i64` over a `shared struct TreeNode` with `val`, `left` and `right`.
Each finds, for every node, the longest run down from it whose values
rise by one a step and the longest that falls by one a step; a path
bending at the node is a falling run on one side and a rising run on the
other, so the two lengths less the node they share is a candidate.

| file | mechanism |
|---|---|
| `binary_tree_longest_consecutive_sequence_ii.kara` ★ | a recursive post-order walk returning the pair, the best so far in a `mut ref i64` |
| `binary_tree_longest_consecutive_sequence_ii_stack.kara` | the walk with its stack made explicit; each finished subtree leaves its value and its two lengths on a second stack |
| `binary_tree_longest_consecutive_sequence_ii_levels.kara` | the nodes laid out in level order with their children's places noted, then the order read from the back, children before parents, with no recursion and no stack |
| `binary_tree_longest_consecutive_sequence_ii_passes.kara` | one recursive walk for the rising lengths and one for the falling, each storing a length for every node at its pre-order number, then the two read side by side |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: both examples, one node, a falling
chain, a bend below the root, both children one higher, negative values,
and a run that skips a value, each with its answer; then for 300 random
trees of 1 to 80 nodes (values from 0 to 2, 0 to 4 or 0 to 9 in turn)
the number of nodes, the total of the answers and a checksum; and last
four trees of 30,000 nodes (the problem's most): a random one, a chain
rising down the left, a falling chain to the left of the root and a
rising one to the right, and a complete tree whose values are the
depths. `binary_tree_longest_consecutive_sequence_ii.py` mirrors the ★
arm and its output is byte-identical; it runs on a thread with a 512 MB
stack, since the walk recurses 30,000 deep.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: the tree as an undirected graph of
numbered nodes, and from every node the longest path along its edges
whose values rise by one a step. A falling path is a rising one read the
other way, so rising paths cover them all. Each arm is held to the
properties below on 1,000 random trees of 1 to 30 nodes, values from
0 to 1, 0 to 2 or 0 to 4 in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the tree mirrored left to right has the same answer |
| P3 | every value negated gives the same answer |
| P4 | every value raised by 1000 gives the same answer |
| P5 | at least 1, at most the nodes and at most the values there can be |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no bend, the longer of the two runs taken | P1 59 |
| M2 | ★: the right child's falling run not carried | P1 133, P2 173, P3 246 |
| M3 | stack: the left child's falling run taken on a rise | P1 614, P2 619, P3 598, P5 392 |
| M4 | stack: a finished node's runs left swapped | P1 587, P5 384 |
| M5 | levels: the order read from the front, parents first | P1 215 |
| M6 | levels: a falling run extended from the child's rising one | P1 433, P3 359, P5 275 |
| M7 | passes: a matching left child adds one but carries nothing | P1 98, P2 174 |
| M8 | passes: the falling walk run with a rising step | P1 779, P3 379, P5 429 |
| E1 | ★: the left child's fall tested even after a rise | 0 |
| E2 | stack: a missing child's value 1, not 0 | 0 |
| E3 | levels: the right child looked at first | 0 |
| E4 | passes: each slot started at 0, not 1 | 0 |

P2 and P3 catch the mistakes that favour one side or one direction:
mirroring swaps the children, so M2, M3 and M7 change their answer, and
negating swaps rising and falling, so M2, M3, M6 and M8 do. M1, M4 and
M5 treat both sides and both directions alike, so only the definition
sees M1 and M5; M4, M6 and M8 can also count more than there are values
(P5). P4 kills nothing: every arm compares values only by differences,
which a shift keeps. E1 is safe because a child cannot be one above and
one below its parent at once, E2 because a missing child's lengths are
0 and every test on its value checks the lengths first, and E4 because
every slot is written before it is read.

## Verification

Every arm prints the same output as
`binary_tree_longest_consecutive_sequence_ii.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak. `karac check` passes on every arm,
the differential and the bench program.

The frozen legacy backends: `karac run --interp` prints the same output
for the stack and levels arms, and does not finish the ★ and passes
arms, the two that recurse 30,000 deep, within the 300 s budget. `karac
run` and `karac build` fail every arm in codegen ("Call parameter type
does not match function signature" on `show("example 1", ...)`), and
stop the differential at type checking on `*to` over `iter()` of a
`Vec[i64]` ("unary '*' requires 'ref T' ... found 'i64'"). Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random trees of
30,000 nodes (the problem's most), tree g with values from 0 to 2 + g %
4, each new node walking down from the root at even chance, once,
keeping the first 16 nodes added. Then 60 times over every tree the
subtree at one of those 16, picked by the round and the tree, is
answered. Every implementation prints `20 trees, 60 rounds each: lengths
5284, checksum 991360672`, the Kāra program under `karac __mir-run`
included (37.0 s).

Rust uses LeetCode's `Option<Rc<RefCell<TreeNode>>>`, reference counted
as Kāra's `shared struct` is; C uses plain pointers into one array of
nodes, Go plain pointers, Python a class with `__slots__`. Spot timings
on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.20 to 0.23 s |
| Rust (`rustc -O`) | 0.40 to 0.42 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.40 to 0.43 s |
| Go | 0.28 to 0.30 s |
| Python | 4.45 to 4.47 s |
| Kāra (`karac build`, legacy) | 0.37 to 0.38 s |
| Kāra (`karac build --mir`) | 0.46 to 0.50 s |

The legacy `karac build` builds the bench program and prints the same
line, so `bench.sh` is the `scripts/new-bench.sh` output unchanged. The
`--mir` row is timed at kara `2b8238c108` and is outside `bench.sh`.
Under `karac __mir-llvm-run` the program prints the same line in 2.0 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark. The legacy row is level with Rust's and the
`--mir` row about 1.2 times Rust's.

## Compiler findings

None new. Nothing was filed from this kata; the legacy failures above
are not filed because legacy is frozen.
