# 426. Convert Binary Search Tree to Sorted Doubly Linked List

Convert a binary search tree to a sorted circular doubly linked list
in place. Think of the left and right pointers as the predecessor and
successor pointers of the list. The predecessor of the first element
is the last element, and the successor of the last element is the
first.

The transformation is done in place: after it, each node's left
pointer points to its predecessor and its right pointer to its
successor. Return the pointer to the smallest element of the list.

```
root = [4,2,5,1,3]  ->  [1,2,3,4,5]
root = [2,1,3]      ->  [1,2,3]
```

**Constraints:** the number of nodes is in `[0, 2000]`;
`-1000 <= Node.val <= 1000`; all the values are unique.

## Approaches

The node is a `shared struct` with `mut` link fields, so a node is a
reference-counted handle and every arm rewrites the tree's own links.

| file | mechanism |
|---|---|
| `tree_to_list.kara` ★ | in-order recursion: keep the first node visited and the last; link each new node after the last, and close the ring at the end. O(n) time, O(height) stack |
| `tree_to_list_stack.kara` | the same in-order linking with an explicit stack of the left spine |
| `tree_to_list_morris.kara` | Morris traversal: thread each node's in-order predecessor back to it instead of keeping a stack. O(1) extra space. The predecessor is found by comparing values, which are distinct |
| `tree_to_list_splice.kara` | convert both subtrees to rings, make the node a ring of one, and splice the three rings in order |
| `differential.kara` | the four arms on 1,500 random trees, five properties |

The Morris arm never clears its threads: a thread is the predecessor's
right link pointing at the node, which is the list's link already.

Every arm prints the same 11 lines: the two LeetCode examples, eight
edge cases (an empty tree, one node, a right spine, a left spine,
negative values, a full tree of 15, and the two three-node zigzags),
and for 2,000 random trees of 0 to 40 distinct values from -500 to 499
the node count and a checksum. Each ring is printed read right from
the head and read left from the head's left neighbour, and is marked
`BROKEN` if a step back does not undo a step forward or a walk does
not close. A ring of strong handles is never freed, so the harness
breaks every link after reading. `tree_to_list.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, with the node type
defined once before them. Each of 1,500 random cases is a binary
search tree of 0 to 29 distinct values from -100 to 99, inserted in
random order:

| | property |
|---|---|
| P1 | reading the ring right from its head gives the values sorted |
| P2 | every step left undoes a step right, and both walks are back at the head after n steps |
| P3 | the head holds the smallest value and its left neighbour the largest |
| P4 | the same values inserted in another order give the same ring |
| P5 | 1 to m inserted ascending (a right spine), descending (a left spine) and middle first (a balanced tree) all give 1 to m |

The differential's reader tolerates a broken ring: a missing link
fails the checks instead of stopping the run, so a mutant is counted
rather than crashing. It prints `1500 cases, 4 arms, 30000 checks,
0 failures` under `karac __mir-run`, and a count for each property
when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | recursive: the tail is not linked to the head | P2 1450, P5 1500 |
| M2 | recursive: every node becomes the head | P1 1402, P3 1402, P4 1402, P5 1428 |
| M3 | stack: the previous node is never advanced | P1 1450, P2 1450, P3 1450, P4 1450, P5 1500 |
| M4 | stack: no node links back to its predecessor | P2 1352, P5 1428 |
| M5 | morris: the left subtree is skipped | P1 1377, P2 740, P3 1339, P4 1372, P5 1428 |
| M6 | morris: the ring is left open at the tail | P2 1450, P5 1500 |
| M7 | splice: the joined head keeps its old tail | P1 1347, P2 1402, P3 1402, P4 1347, P5 1363 |
| M8 | splice: the node goes before its left subtree | P1 1377, P3 1339, P4 1372, P5 1428 |

M1, M4 and M6 break only the backward links or the ring's closing
link, so the values read forward are right and only P2 and P5's
closing check see them. M2 and M8 leave every link consistent and get
the order wrong, so P2 misses them.

## Verification

All four arms print the same output as `tree_to_list.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp`, and `karac check` passes on every file. The
differential prints `30000 checks, 0 failures` on those three.

The frozen legacy codegen fails both. The arms stop at
`split_whitespace()` on a `Str` parameter, which the harness's
`show(text: Str)` uses, as in katas 418, 419, 422 and 425. The
differential aborts under LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build` with `malloc(): unaligned tcache chunk
detected`, a heap corruption in the legacy backend, not narrowed
further. Legacy is frozen, so both are noted, not
filed. The bench program builds and runs there.

The four arms also run clean under `karac __mir-llvm-asan` (the M2
backend with AddressSanitizer and LeakSanitizer): output identical, no
error, no leak. With the harness's link breaking removed, the same
lane reports the rings: `2215640 byte(s) leaked in 39565
allocation(s)`, so the clean run is not vacuous.

## Benchmarks

The bench program uses the ★ arm. Each of 20 rounds shuffles the
values 0 to 49,999, inserts them into a binary search tree in that
order, converts the tree, and walks the ring once, folding the values
into a checksum and breaking each node's links so it is freed. Every
implementation prints `20 rounds on 50000 nodes: checksum 415111796`;
a 2-round cut of the Kāra program under `karac __mir-run` prints the
same as the C program cut the same way. The mirrors keep the Kāra
program's memory model as far as each language allows: C mallocs the
nodes and frees each one as the walk passes it, Rust uses
`Rc<RefCell<Node>>` (the reference-counted handle a `shared struct`
is) and breaks the links, Go and Python break the links and leave the
rest to their collectors. Building the tree is most of the work, and
its random walks down the tree are cache misses in every language.
Spot timings on a shared 4-core container, three runs each
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.33 s |
| Go | 0.36 to 0.40 s |
| Kāra (legacy `karac build`) | 0.44 to 0.51 s |
| Rust (`rustc -O`) | 0.45 to 0.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.44 to 0.47 s |
| Python | 2.4 to 2.8 s |

The Kāra program also prints the same line under
`karac __mir-llvm-run` in 1.3 s, compile included, and under
`karac __mir-run` in 50 s; `__mir-llvm-run` JITs the MIR's IR without
optimization passes, so it is not a benchmark. The `karac build` time
is the frozen legacy backend.

## Compiler findings

No new findings.
