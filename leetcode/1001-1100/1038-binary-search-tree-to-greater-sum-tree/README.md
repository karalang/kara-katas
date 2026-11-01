# 1038. Binary Search Tree to Greater Sum Tree

Given the `root` of a Binary Search Tree (BST), convert it to a Greater
Tree such that every key of the original BST is changed to the original
key plus the sum of all keys greater than the original key in BST.

As a reminder, a binary search tree is a tree that satisfies these
constraints:

- The left subtree of a node contains only nodes with keys less than
  the node's key.
- The right subtree of a node contains only nodes with keys greater
  than the node's key.
- Both the left and right subtrees must also be binary search trees.

```
root = [4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]
    ->  [30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
root = [0,null,1]  ->  [1,null,1]
```

**Constraints:** the number of nodes is in `[1, 100]`;
`0 <= Node.val <= 100`; all the values are unique; `root` is
guaranteed to be a valid binary search tree.

This is the same problem as kata 538 at smaller sizes (100 nodes, keys
0 to 100, where 538 has 10,000 nodes from -10,000 to 10,000). The arms
here are different ones, chosen to use what is new: the small key
range, a tree that is rebuilt rather than changed, and a sort.

Every arm is `fn bst_to_gst(root: Option[TreeNode]) -> Option[TreeNode]`
over the harness's `shared struct TreeNode` with a `mut val`, as in
kata 538.

## Approaches

| file | mechanism |
|---|---|
| `gst.kara` ★ | reverse in order, the running sum passed and returned: each call takes the sum of every key above its subtree and returns it grown by the subtree's own keys, so a node's new value is its right subtree's result plus its key. O(n), O(h) stack |
| `gst_rebuild.kara` | a new tree: the nodes are read into an immutable `shared enum`, rebuilt from the largest key down by a function returning the new subtree and the sum, and written out as fresh nodes. The tree passed in keeps its keys. O(n), O(n) for the copies |
| `gst_counts.kara` | a table of the keys: one preorder walk with a stack marks which of 0 to 100 are present, a pass from 100 down gives each key the sum of every key at least it, and a second walk writes that into each node. The search-tree order is never used. O(n + 101) |
| `gst_sorted.kara` | the nodes sorted: gathered level by level, sorted with `sort_by` from the largest key down, and given the running sum. O(n log n) |
| `gst_prune.kara` | a search for each node: the sum of the keys at least `v` is found from the root, taking a node and its whole right subtree when the key is at least `v` and going right otherwise; every node's sum is found on the old keys, then written back in preorder. O(n * h) with the right subtrees summed again each time |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 13 lines: ten trees in LeetCode's level-order
form with their answers, both examples among them, with one node, both
ends of the key range, and a full tree of 15; a checksum over 300
random trees, three of each size from 1 to 100 nodes, each written in
level order and parsed back before it is converted; and the deepest
trees of 100 nodes, 0 to 99 as a rising chain and 100 down to 1 as a
falling one. `gst.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: in the same tree, every key becomes itself plus the sum
of all the keys greater than it, summed over the list of keys. Each
case is an insertion order of distinct keys from 0 to 100, built into a
search tree afresh for every arm and every property. It checks 450
trees: every insertion order of five keys (120 orders, all 42 shapes of
five nodes), and 330 random trees of 1 to 20 keys, with one in ten of
1 to 100 keys. Each arm's answer is read as the tree level by level,
and as a map from each old key to its new value.

| | property |
|---|---|
| P1 | the statement read literally, the tree level by level |
| P2 | in order the new values never rise, the smallest key's is the sum of every key, and the largest key keeps its own |
| P3 | moving every key up by `c` (as far as 100 allows) adds `c` once for each key at least as large |
| P4 | in the mirror image, every key `k` turned into `100 - k`, the new value of `100 - k` is `100` times the number of keys at most `k`, less those keys, which the old answer gives |
| P5 | a key not in the tree, inserted as a new leaf, adds itself to every smaller key's value, changes no other, and gets itself plus the keys above it |
| P6 | each arm agrees with at least two of the other four |

The differential prints `450 trees, 5475 nodes: checksum 748235077,
13500 checks over 5 arms: 0 failures` under `karac __mir-run` (9.0 s),
`karac __mir-llvm-run` and `karac __mir-llvm-asan` with no error, and
the same line under `karac run` and from a `karac build` binary.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three
to each arm. All fifteen are killed, each fails the same checks under
both backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the keys strictly greater | P1 450, P2 450, P3 357, P4 450, P5 447, P6 450 |
| M2 | ★: the sum started at 1 | P1 450, P2 450, P5 450, P6 450 |
| M3 | ★: the right subtree never walked | P1 431, P2 431, P3 339, P4 440, P5 445, P6 431 |
| M4 | rebuild: the children swapped | P1 440, P2 439, P3 438, P4 440, P5 450, P6 440 |
| M5 | rebuild: right subtrees dropped on reading | P1 431, P2 431, P3 431, P4 440, P5 445, P6 431 |
| M6 | rebuild: the left subtree written on both sides | P1 440, P2 440, P3 417, P4 440, P5 441, P6 440 |
| M7 | counts: key 100 never summed | P1 46, P2 46, P3 58, P4 63, P5 49, P6 46 |
| M8 | counts: the marking walk never goes left | P1 427, P2 427, P3 335, P4 440, P5 355, P6 427 |
| M9 | counts: the writing walk never goes left | P1 428, P2 428, P3 335, P4 440, P5 441, P6 428 |
| M10 | sorted: sorted smallest first | P1 440, P2 440, P3 347, P4 440, P5 450, P6 440 |
| M11 | sorted: the value written before the key is added | P1 450, P2 450, P3 357, P4 450, P5 450, P6 450 |
| M12 | sorted: the largest key counted twice | P1 450, P2 450, P3 357, P4 417, P5 450, P6 450 |
| M13 | prune: the right subtree summed on the left side | P1 427, P2 222, P3 335, P4 440, P5 352, P6 427 |
| M14 | prune: a smaller key searched left | P1 431, P2 376, P3 339, P4 440, P5 396, P6 431 |
| M15 | prune: the root never written | P1 376, P2 376, P3 294, P4 440, P5 243, P6 376 |

Every property kills every kept edit but one: P3 and P4 miss M2, a
sum started at 1, because the extra 1 is in both answers they compare,
and each relation still holds. Most edits fail nearly every tree; 440
is every tree but the ten of one node, which several edits leave
right. The one edit that fails rarely is M7, key 100 never summed: P1
sees the 46 trees that hold key 100, and P4 sees 63, since the mirror
image turns a key 0 into a 100, so trees holding 0 can fail it too (80
trees hold 0 or 100).

Fifteen other edits were tried and set aside. None is equivalent; all
were killed, beyond three per arm. Five fail exactly as M10 does,
every tree of two or more nodes wrong: ★ losing the sum at every empty
subtree and not giving the left subtree the node's sum, the rebuild
arm returning the old tree, and the sorted arm missing the last node's
children and leaving the smallest key alone. Two fail as M1 does (the counts
and prune arms taking only the keys strictly greater), two as M11 (the
counts arm counting an absent key as 1 and not marking leaves), two as
M3 (the rebuild arm not counting the right subtree's keys, and the
sorted arm missing right children), two alike, `P1 336, P2 336, P3 252,
P4 391, P5 301, P6 336` (the rebuild arm not passing the left
subtree's keys up, and the prune arm's totals leaving out left
subtrees), and one as M9 (the prune arm searching from the node rather
than the root). The last, ★ walking the left subtree first, walks it
twice, and the values it compounds overflow: `integer overflow` under
both backends.

## Verification

Every arm prints the same output as `gst.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reported nothing
on any arm or the differential as committed. The release build is kara
`6697158faf`, with runtime archives rebuilt at that commit. Under
`karac __mir-run` the arms take 0.85 s (★, sorted) to 1.6 s (prune).

Two diagnostic gaps turned up, both filed:

- kara `B-2026-11-01-9`: the harness's level-order parser was first
  written with Rust's `trim_start_matches("[")`. It gets a bare E0236
  "no method 'trim_start_matches' on type 'String'" with no hint
  towards `strip_prefix`, and `trim_matches(|c| ..)` adds a cascaded
  E0208 on its closure; `to_owned()` is the same. The parser uses
  `strip_prefix` and `strip_suffix`.
- kara `B-2026-11-01-10`: the differential compared
  `new_shifted.get(k + c)` with `new_of.get(k).map(..)`, an
  `Option[ref i64]` with an `Option[i64]`. The refusal is the settled
  rule, but E0208 "cannot compare 'Option[ref i64]' and 'Option[i64]'"
  comes with no fix, even for `m.get(1) == Some(5)`, where the
  `.copied()` diagnostic already names `.cloned()`. `karac fix` wrote
  the three `ref results[i]` borrows; the four `.cloned()` calls were
  written by hand.

## Benchmarks

The bench program uses the ★ arm. It builds 10,000 random search trees
of 100 distinct keys from 0 to 100 (the problem's most) once, listing
each tree's nodes; then 50 times over, every tree has its keys put back
from the list and is converted, and the converted root's value is
added to a total and folded into a checksum. Every implementation
prints `10000 trees of 100 keys, 50 rounds: total 1683797150, checksum
728227694`. The Rust tree is `Rc<RefCell<TreeNode>>`, the closest match
to a `shared struct`; C and Go use plain pointers, and C never frees.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.542 to 0.621 s | 0.574 s |
| Go | 0.723 to 0.791 s | 0.746 s |
| Rust (`rustc -O`) | 0.804 to 0.952 s | 0.915 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.830 to 0.978 s | 0.917 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.125 to 1.354 s | 1.180 s |
| Kāra (`karac build`) | 1.045 to 1.309 s | 1.226 s |
| Python | 8.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(1.08 s real, 1.05 s user on one run) and its median is within the
spread of the sequential one.

Kāra took 1.29 times Rust's median time under overflow checks, both
counting references to every node. C and Go keep plain pointers, with
no count to change as a walk takes and drops a child, which is
inferred from the sources as the reason they lead, not profiled.
