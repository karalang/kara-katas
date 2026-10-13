# 450. Delete Node in a BST

Given the root of a binary search tree and a key, delete the node with
that key and return the root of the tree, which may change. If the key
is not in the tree, return the tree as it is.

```
root = [5,3,6,2,4,null,7], key = 3  ->  [5,4,6,2,null,null,7]  (or [5,2,6,null,4,null,7])
root = [5,3,6,2,4,null,7], key = 0  ->  [5,3,6,2,4,null,7]
root = [], key = 0                  ->  []
```

**Constraints:** the tree has `0` to `10^4` nodes;
`-10^5 <= Node.val, key <= 10^5`; values are unique; `root` is a valid
binary search tree.
**Follow-up:** can you do it in O(height of tree) time?

## Approaches

Every arm is `fn delete_node(root: Option[TreeNode], key: i64) ->
Option[TreeNode]` over the same `shared struct TreeNode` with `mut`
fields, and runs in O(height) time. More than one tree is a correct
answer, and the arms give different shapes, so the harness checks what
every correct answer shares: the values left, in order, and that the
result is a search tree.

| file | mechanism |
|---|---|
| `delete_node.kara` ★ | recursive: walk down to the key; a node with at most one child is replaced by that child, and a node with two takes its successor's value (the smallest in its right subtree), which is then deleted from the right subtree. O(height) stack |
| `delete_node_splice.kara` | iterative: find the node and its parent with a loop, then replace the node by its right subtree after hanging its left subtree under the smallest node of the right one. No value moves, but the tree can grow taller. O(1) extra space |
| `delete_node_predecessor.kara` | the mirror image of the ★ arm: a node with two children takes its predecessor's value, the largest in its left subtree |
| `delete_node_relink.kara` | like the ★ arm, but nodes keep their values: the successor node itself is unlinked and takes the deleted node's place, adopting both subtrees. The form to use when a node carries more than a value that is cheap to copy |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 10 lines: the LeetCode examples, deleting
the root, a leaf, the only node and either end of a chain, a node with
two children in a ten-node tree, each with the values left and whether
the result is a search tree; then, for 300 random trees of 0 to 100
values from 0 to 199 (inserted in random order, or one time in five in
ascending order, which makes a chain) with 20 random keys deleted from
each in turn, the keys found and missed, the nodes left, whether every
result was a search tree, and a checksum of the values left after each
delete. `delete_node.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random search trees of distinct values from 0 to `3n + 2`: up to
2, 19 or 119 values, inserted in random order or one time in five in
ascending order.

| | property |
|---|---|
| P1 | deleting a key (one of the values at least one time in two) leaves the other values, in order |
| P2 | the result is a search tree |
| P3 | deleting an absent key leaves the tree as it was, shape included |
| P4 | deleting every value in a random order keeps, at each step, a search tree of the values left, and ends with the empty tree |
| P5 | deleting a leaf gives the tree that inserting the values without it gives |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | successor: the value copied in is the left subtree's smallest | P1 128, P2 128, P4 645 |
| M2 | successor: a node without a left child is deleted with its right subtree | P1 303, P4 934 |
| M3 | splice: the left subtree is hung on the right of the lowest node | P1 270, P2 128, P4 858 |
| M4 | splice: deleting an absent key empties the tree | P1 472, P3 1307 |
| M5 | predecessor: the value copied in is the left subtree's smallest | P1 87, P2 87, P4 589 |
| M6 | predecessor: a node without a right child is deleted with its left subtree | P1 154, P4 694 |
| M7 | relink: the successor's right subtree is dropped | P1 184, P4 755 |
| M8 | relink: an equal key is looked for on the left | P1 835, P4 1307, P5 1307 |

P2 sees only the mutants that put a value in the wrong place (M1, M3,
M5); dropping a subtree still leaves a search tree. P3 sees only M4,
since every other mutant is on the path taken when the key is found,
and P4 misses M4 because it deletes only keys that are present. P5 sees
only M8: a leaf has no children, so the mutants that mishandle children
behave correctly on it.

## Verification

All four arms print the same output as `delete_node.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`. The splice and predecessor arms also match under
LLJIT and `karac build`, with and without `KARAC_AUTO_PAR=1`. The ★ arm
corrupts the heap there and aborts (`malloc(): unaligned tcache chunk
detected`), and the relink arm crashes with a segmentation fault, under
LLJIT and `karac build` alike; the bench program builds and aborts the
same way (`malloc_consolidate(): unaligned fastbin chunk detected`)
before it prints. The differential does not finish within 900 s under
`karac run --interp` (it takes 39 s under `karac __mir-run`), and
`karac build` stops on the
differential's index into an array literal ("Index operator applied to
non-array type"). Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds one random search tree of
1,000,000 values once (a shuffle of the even numbers below 2,000,000),
then deletes 1,000,000 random keys below 2,000,000; odd keys are never
present, and 393,577 of the deletes find their key. Every implementation prints `1000000 deletes from 1000000
values: 606423 nodes left, checksum 946057793`, the Kāra program under
`karac __mir-run` included (in 94 s).

The mirrors keep the ★ arm's structure: recursive delete, successor's
value copied in. Rust's tree is `Rc<RefCell<TreeNode>>`, the closest
match to a `shared struct`; C frees each deleted node, Go leaves it to
the collector. Spot timings on a shared 4-core container, three runs
each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.7 to 1.9 s |
| Rust (`rustc -O`) | 2.5 to 2.6 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.6 s |
| Go | 1.5 s |
| Python | 8.2 s |

The legacy `karac build` binary aborts (above), so there is no compiled
Kāra time. The Kāra program prints the same line under
`karac __mir-llvm-run` in 4.3 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark.

## Compiler findings

- B-2026-10-12-27 (fixed in kara `c07dbf5094`): `karac check` refused
  `let (successor, rest) = take_smallest(right); successor.left = node.left;`
  ("cannot assign through `successor` — declared without `mut`"),
  though a `mut` field of a shared value is writable through any
  handle. `delete_node_relink.kara` (and its copy in the differential)
  wrote `let mut (successor, rest)`, the form `karac fix` gives, until
  the fix; both are back to `let (successor, rest)`.
