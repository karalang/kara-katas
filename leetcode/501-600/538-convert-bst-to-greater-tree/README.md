# 538. Convert BST to Greater Tree

Given the `root` of a Binary Search Tree (BST), convert it to a Greater
Tree such that every key of the original BST is changed to the original
key plus the sum of all keys greater than the original key in BST.

```
root = [4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]
    ->  [30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
root = [0,null,1]  ->  [1,null,1]
```

**Constraints:** the number of nodes in the tree is in the range `[0,
10^4]`; `-10^4 <= Node.val <= 10^4`; all the values in the tree are
unique; `root` is guaranteed to be a valid binary search tree.

## Approaches

Every arm is `fn convert_bst(root: Option[TreeNode]) ->
Option[TreeNode]` over a `shared struct TreeNode` with a `mut val`
(as in kata 530). Each changes the values in place and returns the
root it was given. The new value of a node is the sum of every value at
least its own, so the arms meet the values from the largest down and
keep a running sum.

| file | mechanism | extra space |
|---|---|---|
| `convert_bst.kara` ★ | reverse in order, recursively: right subtree, node, left subtree, with the running sum in a `mut ref` | O(h) stack |
| `convert_bst_stack.kara` | the same walk with an explicit stack of nodes | O(h) |
| `convert_bst_morris.kara` | reverse Morris traversal: the leftmost node of each right subtree is threaded back to its parent, and the thread is cut on the way back | O(1) |
| `convert_bst_suffix.kara` | the nodes listed in order, then one pass from the end writing suffix sums | O(n) |
| `differential.kara` | the four arms against the definition, five properties | |

Every arm prints the same 11 lines: both examples (inserted as `4, 1,
6, 0, 2, 5, 7, 3, 8` and `0, 1`, which build the trees shown, and
written level by level as LeetCode writes them), one node, no nodes,
only negative values, both ends of the range, a falling and a rising
chain; then for 300 random trees of 0 to 80 distinct values from
-10,000 to 10,000 a checksum over the converted trees; and last two
trees of 10,000 nodes (the problem's most), -5,000 to 4,999 inserted
in a random order, and 1 to 10,000 in a chain, each node the right
child of the one before, as deep as such a tree can be.
`convert_bst.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
a node's new value is the sum of the original values at least its own,
added up over the whole list of values. Each arm converts a freshly
built tree for each of 1,000 random cases of 0 to 40 distinct values
from -10,000 to 10,000, or one time in three from -20 to 20, where the
sums cross zero often, and is held to the properties below. The walks
that read a converted tree stop after as many nodes as it had, so a
thread left in it cannot send them round for ever.

| | property |
|---|---|
| P1 | every node's new value is the definition's |
| P2 | the tree keeps its nodes and its shape (read in pre-order), and its root is returned |
| P3 | the smallest node ends with the sum of every value, and the largest keeps its own |
| P4 | with every value moved up by 10,001, so that all are positive, the new values fall in order |
| P5 | the new values sum to each original value times its rank from the bottom: the smallest counted once, the next twice, and so on |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the node's own value left out of its new value | P1 976, P3 976, P5 972 |
| M2 | ★: the right subtree never walked | P1 939, P3 939, P4 939, P5 939 |
| M3 | stack: the walk never turns to a left child | P1 937, P3 928, P4 937, P5 937 |
| M4 | stack: no running sum, each node keeps its own value | P1 952, P3 943, P4 952, P5 952 |
| M5 | morris: the thread never cut | P1 939, P2 939, P3 939, P4 939, P5 939 |
| M6 | morris: a missing thread read as one already there | P1 939, P3 939, P4 939, P5 939 |
| M7 | suffix: the running sum taken from the smallest up | P1 952, P3 952, P4 952, P5 952 |
| M8 | suffix: each node put at the front of the list, not the back | P1 952, P3 952, P4 952, P5 952 |
| E1 | ★: the greater values added to the node's own | 0 |
| E2 | stack: the left child taken with an explicit `clone()` | 0 |
| E3 | morris: the right child already in hand used for the next step | 0 |
| E4 | suffix: the list given room for 64 nodes up front | 0 |

M2 and M6 are one mistake in two arms. With the test turned round, the
Morris arm takes every node as if its right subtree were done already,
so it never goes right either; both leave every right subtree as it was,
and fail in the same 939 cases. M7 and M8 are also one mistake: the list
built back to front and then walked from its end is the list walked from
its start. M1 still passes P4, since the sums of the strictly greater
values fall too. P2 sees only M5, the one edit that changes the tree's
shape.

## Verification

Every arm prints the same output as `convert_bst.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak, the 10,000-deep
chain included. The differential prints `20000 checks, 0 failures` on
the first two and runs clean under the third. `karac check` passes on
every arm, the differential and the bench program.

The frozen legacy backends do worse. `karac run --interp` gives the
right output for the recursive, stack and suffix arms, and stops on the
Morris arm's `ref_eq` ("method 'ref_eq' not found on type 'TreeNode'").
`karac run` and `karac build` fail on every arm: on `ref_eq` for the
Morris arm, and on the others with an LLVM module that does not verify
(the harness's `show` called with a mismatched argument). The
differential stops at type checking on a `*` over a `Vec`'s `iter()`
items, which legacy types by value. The legacy `karac build` does build
the bench program, and the binary dies at once with a segmentation
fault. Legacy is frozen, so all of this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random search trees of
10,000 distinct values (the problem's most) from -10,000 to 10,000
once, listing each tree's nodes; then 50 times over every tree has its
values put back from the list and is converted. Every implementation
prints `100 trees of 10000 values, 50 times each: total 82384464850,
checksum 951458667`, the Kāra program under `karac __mir-run` included
(in 141 s).

The bench program puts the values back with `nodes[i].val = values[i]`,
`nodes` being `ref lists[t]`. A `mut` field of a shared value is
writable through any handle (`docs/core-semantics.md` §5.9). The MIR
borrow checker refused that write until kara B-2026-10-13-33 was fixed
(in kara `554093e8e5`); the program as written now runs under every
v2 command. The legacy `karac build` still builds a binary that crashes
(see Verification), so `bench.sh` builds the Kāra program with `karac
build --mir`, the v2 compiled backend; that edit is by hand, on top of
the `scripts/new-bench.sh` output. The Kāra row used to time a copy that
took the node out first, `let node = nodes[i]; node.val = values[i];`;
it times the program as written now, which runs clean under `karac
__mir-llvm-asan` too.

The Rust mirror's tree is `Rc<RefCell<TreeNode>>`, the closest match to
a `shared struct`; C and Go use plain pointers and never free. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.96 to 0.99 s |
| Rust (`rustc -O`) | 1.58 to 1.65 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.68 to 1.70 s |
| Go | 1.06 to 1.07 s |
| Python | 11.6 to 11.7 s |
| Kāra (`karac build --mir`) | 1.55 to 1.58 s |

The Kāra row is timed at kara `af2123abc5`, two commits after the fix.
Under `karac __mir-llvm-run` the program prints the same line in 3.1 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

## Compiler findings

kara B-2026-10-13-33, filed from this kata and fixed in kara
`554093e8e5`: a field write through an element of a borrowed `Vec` of
shared values, `nodes[i].val = v` with `nodes` a `ref Vec[TreeNode]` or
a bare `Vec[TreeNode]` parameter, was refused by the MIR borrow checker
("mutable borrow of ... through a shared reference [E0517]") under
`__mir-run`, `__mir-llvm-run` and `build --mir`, while `karac check`
passed it. The same write through an owned `Vec`, through `for n in
nodes.iter()`, or through `nodes.first().unwrap()` ran right. It blocked
the bench program, which now runs as written.
