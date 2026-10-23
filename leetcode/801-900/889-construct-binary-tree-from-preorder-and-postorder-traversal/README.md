# 889. Construct Binary Tree from Preorder and Postorder Traversal

Given two integer arrays, `preorder` and `postorder` where `preorder` is
the preorder traversal of a binary tree of distinct values and
`postorder` is the postorder traversal of the same tree, reconstruct and
return the binary tree. If there exist multiple answers, you can return
any of them.

```
preorder = [1,2,4,5,3,6,7], postorder = [4,5,2,6,7,3,1]  ->  [1,2,3,4,5,6,7]
preorder = [1], postorder = [1]  ->  [1]
```

**Constraints:** `1 <= preorder.length <= 30`, `1 <= preorder[i] <=
preorder.length`, all the values of `preorder` are unique, `postorder.length
== preorder.length`, `1 <= postorder[i] <= postorder.length`, all the
values of `postorder` are unique, and it is guaranteed that `preorder`
and `postorder` are the preorder and postorder traversals of the same
binary tree.

## Approaches

The two traversals fix every node's children except that of a node with
only one child, which they cannot place on a side. LeetCode accepts
either; every arm puts a lone child on the left, as LeetCode's own
answers do, so that all five print the same tree. The tree is a `shared
struct TreeNode`.

| file | mechanism |
|---|---|
| `construct_from_pre_post.kara` ★ | recursion with a table of postorder positions: after the root, the preorder holds the left child, whose position in the postorder ends the left subtree and so gives its size; the rest of the preorder after it is the right subtree. O(n) |
| `construct_from_pre_post_stack.kara` | one pass with a stack: each preorder value becomes a node hung under the node on top of the stack, on its left if that is free and otherwise on its right, after every node whose subtree is complete, the next value of the postorder, has come off. O(n) |
| `construct_from_pre_post_cursors.kara` | recursion with two cursors, one in each traversal: a call makes a node of the next preorder value and, while that node is not the next postorder value, gives it a left child and then a right child by the same call; when it is, its subtree is complete and the postorder cursor moves on. O(n) |
| `construct_from_pre_post_slices.kara` | recursion on copied slices: the left child is found in the postorder by a scan, both traversals are cut into a left part and a right part, copied, and each rebuilt. O(n^2) |
| `construct_from_pre_post_reverse.kara` | recursion from the right: the postorder ends with the root and, before it, the root of the last subtree under it, whose position in the preorder splits the rest; when it comes straight after the root it is the only child and goes on the left. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and five more
(one lone child; a path of three nodes; a root with two leaves; a lone
child under the root's left child; and a root whose left child has two
leaves and whose right child is a leaf), each tree in LeetCode's level order; and
for 3,000 random trees of up to 30 nodes, a third of them full (every
node with two children or none, which the traversals fix exactly), how
many come back as they were, 1,285, with a checksum of the trees
rebuilt. `construct_from_pre_post.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every binary tree with the given preorder, the root first and
the rest cut in each possible way into a left part and a right part,
kept when its postorder is the one given and no node has a right child
without a left one. It checks 3,200 random trees: 3,000 of up to 8 nodes
against the statement, and 200 of up to 30 against the other properties,
a third of them full. The ★ arm's trees hold 16,107 nodes in all.

| | property |
|---|---|
| P1 | exactly one tree the statement allows with lone children on the left, and the arm's tree is it, on up to 8 nodes |
| P2 | the tree's preorder and postorder are the ones given |
| P3 | no node has a right child without a left one, and a full tree comes back as it was |
| P4 | the values relabelled by a random permutation give the same tree relabelled |
| P5 | the left subtree is what the arm builds from the left part of the traversals alone, its values renumbered from 1; and a full tree's mirror image comes back as that mirror image |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every tree. It prints `3200 trees, 16107 nodes
in all, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left subtree hung on the right, where the right one replaces it | P1 2477, P2 2667, P3 1802, P5 2667, P6 2667 |
| M2 | ★: the right subtree's postorder starting one place late | P1 1165, P2 982, P3 1068, P5 375, P6 1335 |
| M3 | ★: a subtree of two nodes left a leaf | P1 1513, P2 1636, P5 245, P6 1636 |
| M4 | stack: a new node hung on the right while the right is free | P1 1942, P2 2123, P3 802, P5 1802, P6 2123 |
| M5 | stack: the postorder never moving on | P1 1404, P2 1577, P3 548, P5 1255, P6 1577 |
| M6 | stack: at most one finished node taken off | P1 1161, P2 1329, P3 375, P5 1255, P6 1329 |
| M7 | cursors: the second child put in the first one's place | P1 1942, P2 2123, P3 802, P5 1802, P6 2123 |
| M8 | cursors: the first child put on the right | P1 2477, P2 2123, P3 2667, P5 2667, P6 2667 |
| M9 | cursors: the right subtree built and dropped | P1 1942, P2 2123, P3 802, P5 802, P6 2123 |
| M10 | slices: the left side built from the right part | P1 2477, P2 2667, P3 802, P5 2667, P6 2667 |
| M11 | slices: a node with a lone child left a leaf | P1 1513, P2 1636, P5 245, P6 1636 |
| M12 | slices: the right side built from the left part | P1 2477, P2 2667, P3 802, P5 802, P6 2667 |
| M13 | reverse: a left subtree of one node taken for a lone child | P1 1437, P2 1593, P3 802, P5 1095, P6 1593 |
| M14 | reverse: a lone child put on the right | P1 1632, P3 1760, P5 865, P6 1760 |
| M15 | reverse: each node labelled with the first value of its postorder | P1 2477, P2 2667, P3 802, P5 802, P6 2667 |

P1 and P6 kill all fifteen. M3 and M11 are one fault in two arms, a
subtree of two nodes cut to one, and fail the same cases; M4 and M7 also
fail as many cases, as both leave the second child in the first one's
place. P4 kills none: every fault here depends on positions in the
traversals, never on the values themselves, so relabelling the values
moves it along with them. M14 is the one mutant whose trees still have
the given traversals, which is why P2 misses it: it only breaks the
convention that a lone child goes on the left.

Seven mutants were replaced because they crashed, with an index out of
range, rather than failing a property. Two in the ★ arm crashed in the
differential's first P5, which rebuilt each tree from its own
traversals: a wrong tree's traversals overran the arms' position tables,
and the check was empty anyway, since whenever P2 holds those traversals
are the arm's input again. P5 now checks the left subtree against the
left part of the traversals. The other five crashed in the arm itself:
in the slices and reverse arms, a cut moved by one, or traversals passed
the wrong way round, can send the next cut past the end.

## Verification

Every arm prints the same output as `construct_from_pre_post.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 1.6 to 2.0 s
each and the differential 37 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy interpreter prints the same output for all five arms
and the same line for the differential. Its JIT and `karac build
--legacy`, with and without auto-par, fail on every one: the ★ and
reverse arms and the differential stop with a vector index out of
bounds after a warning that `preorder` is moved and used again, and the
stack, cursors and slices arms abort in `free()` ("unaligned chunk
detected in tcache 2"). Legacy is frozen, so these are not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 4,000 random
trees of 1,000 nodes, or 999 for the half of them that are full, built
as the arms' harness builds its trees; each is walked for its preorder
and postorder, rebuilt, and the rebuilt tree read in level order into a
checksum. Kāra's tree is a `shared struct`, Rust's LeetCode's
`Option<Rc<RefCell<TreeNode>>>`, Go's a pointer struct, Python's an
object, and C mallocs each node and frees both trees after each case.
Every implementation prints `4000 trees of up to 1000 nodes: 3998000
nodes rebuilt, checksum 942871249`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.33 to 0.35 s | 0.34 s |
| Rust (`rustc -O`) | 0.58 to 0.72 s | 0.59 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.57 to 0.71 s | 0.61 s |
| Go | 0.60 to 0.80 s | 0.67 s |
| Python | 7.0 s | |
| Kāra (`karac build --mir`) | 0.54 to 0.76 s | 0.56 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 888's does. The legacy build of the bench
program aborts in `malloc` ("unaligned fastbin chunk detected") before
printing, much as the arms do (above), so it has no row.

v2 takes 0.91 times Rust's median time under overflow checks and 1.65
times C's. Under valgrind's cachegrind C runs 2.23 billion
instructions, Rust with overflow checks 4.89 billion and v2 4.99
billion. Kāra and Rust both count references on every node they link
and unlink, where C touches only the pointers; that most likely
accounts for most of C's lead (inferred from the counts and the
layouts, not profiled). The comparison with C and Rust waits until after
M4.
