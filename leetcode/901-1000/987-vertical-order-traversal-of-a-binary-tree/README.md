# 987. Vertical Order Traversal of a Binary Tree

Given the `root` of a binary tree, calculate the **vertical order
traversal** of the binary tree.

For each node at position `(row, col)`, its left and right children will
be at positions `(row + 1, col - 1)` and `(row + 1, col + 1)`
respectively. The root of the tree is at `(0, 0)`.

The **vertical order traversal** of a binary tree is a list of
top-to-bottom orderings for each column index starting from the leftmost
column and ending on the rightmost column. There may be multiple nodes
in the same row and same column. In such a case, sort these nodes by
their values.

Return the vertical order traversal of the binary tree.

```
root = [3,9,20,null,null,15,7]  ->  [[9],[3,15],[20],[7]]
root = [1,2,3,4,5,6,7]          ->  [[4],[2],[1,5,6],[3],[7]]
root = [1,2,3,4,6,5,7]          ->  [[4],[2],[1,5,6],[3],[7]]
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 1000]`; `0 <= Node.val <= 1000`.

## Approaches

The tree is a `shared struct TreeNode` with `Option[TreeNode]` children,
as in kata 979.

| file | mechanism |
|---|---|
| `vertical_traversal.kara` ★ | every node's place, sorted: a walk gives each node its column, row and value, and sorted as tuples they come in the answer's order, column by column, top to bottom, and by value where two nodes share a place; the answer cuts the sorted list where the column changes. O(n log n) |
| `vertical_traversal_bfs.kara` | level by level: a breadth-first walk takes one row at a time, sorts its nodes by column and then value, and adds each to the end of its column in a `SortedMap` from column to values, which gives the columns left to right. O(n log n) |
| `vertical_traversal_buckets.kara` | a bucket per column: a first walk finds the leftmost and rightmost columns, so each column gets a bucket in a `Vec`, a second walk drops every node's row and value in its bucket, and each bucket is sorted. O(n log n) |
| `vertical_traversal_merge.kara` | each subtree's columns, merged: a recursion returns a subtree's columns as rows and values, numbered from its root, by putting its left subtree's columns one place to the left and its right subtree's one to the right, a row lower; the whole tree's columns are sorted at the end. O(n h) for the copying, h the height |
| `vertical_traversal_map.kara` | a map of columns, filled from a stack: a walk with its own stack files every node's row and value under its column in a `Map` with `entry(..).or_insert(..)`; the map's columns come out in no order, so the answer sorts them, then each column. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines. The first ten are LeetCode's three
examples and seven more: one node; paths to the left and to the right;
a zigzag whose nodes return to their column; two nodes at one place,
sorted by value (`[[2], [1, 8, 9], [3]]`); a tree of equal values; and
a place shared under the root. Then two trees of LeetCode's largest
size, 1,000 nodes: the complete tree, 18 columns of up to 175 nodes,
and a path to the left, 1,000 columns of one. Then totals over random
trees, grown by hanging each node at the first empty place of a random
walk down: 300 of up to 8 nodes with values below 10, so places and
values are often shared, 3,000 of up to 100 with values up to 1,000,
and three of 1,000 nodes. `vertical_traversal.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally. Every node's row and column are read off the path to it, a
row per step down and a column to the left or right per step that way;
then for each column from the leftmost, and each row from the top, the
values at that place are gathered smallest first by insertion. It checks
3,200 random trees: 3,000 of up to 8 nodes with values below 10 against
the statement, and 200 of up to 300 nodes with values up to LeetCode's
1,000 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 trees |
| P2 | the mirror image gives the same columns in reverse |
| P3 | every value raised by a random amount raises the answer's values by it |
| P4 | the answer holds every node's value once |
| P5 | a new root above, with the tree as its left child, goes at the top of the column to the right of the old root's, or in a new column at the right end |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 trees of 41941 nodes: 12452 columns, checksum 492824524,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (15.0 s)
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Thirty-three edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left child a column to the right | P1 2342, P2 2731, P5 3200, P6 2542 |
| M2 | ★: the rows left out of the sort | P1 1094, P5 2432, P6 1292 |
| M3 | ★: the places sorted by row first | P1 2338, P2 2757, P5 3200, P6 2538 |
| M4 | bfs: a row never sorted | P1 240, P2 646, P6 435 |
| M5 | bfs: the right child a column to the left | P1 2351, P2 2731, P5 1874, P6 2551 |
| M6 | bfs: a row sorted in reverse | P1 450, P6 646 |
| M7 | buckets: a bucket never sorted | P1 378, P2 846, P6 573 |
| M8 | buckets: one bucket too many | P1 3000, P2 3200, P5 745, P6 3200 |
| M9 | buckets: one bucket too many on the left | P1 3000, P2 3200, P5 3200, P6 3200 |
| M10 | merge: the left subtree's columns dropped | P1 2365, P2 2808, P4 2565, P5 3200, P6 2565 |
| M11 | merge: each column in reverse | P1 1625, P5 2453, P6 1824 |
| M12 | merge: every node in twice | P1 3000, P4 3200, P5 3200, P6 3200 |
| M13 | map: a column never sorted | P1 360, P2 846, P6 557 |
| M14 | map: the columns in reverse | P1 2514, P5 2996, P6 2714 |
| M15 | map: the values filed as rows | P1 2950, P3 3199, P4 3144, P5 3200, P6 3150 |

P1 and P6 kill all fifteen, P5 eleven, P2 nine, P4 three and P3 one.
Raising every value keeps every comparison between values, so P3 sees
only M15, which sorts by value where the row belongs and then reports
rows as values. P4 sees only the mutants that lose or repeat a node.
The mirror image keeps the nodes of each column, so P2 is blind to a
mutant that orders a column by a rule the mirror keeps: M2 sorting by
value alone, M6 and M11 sorting in reverse, M14 reversing the columns,
which the mirror's answer reversed again undoes. P5 is blind to the
three columns left unsorted, M4, M7 and M13: each walk meets the old
nodes in the same order with the new root on top, and the new root goes
first in its column whatever the order.

Eighteen other edits were tried and set aside. Five failed exactly the
same checks as a kept one: buckets leaving the rows out of the sort and
map doing the same, as M2; merge never sorting a column, as M7; map
moving the left child a column to the right, as M1; map reversing each
column, as M11. Four were sound but beyond three an arm: ★ never
sorting the places; buckets listing each column bottom to top; merge
dropping the right subtree's columns; map putting the right child two
columns over. Three crashed in both lanes, with an index out of bounds:
bfs putting the left child in its parent's column and bfs keeping only
the left children give fewer columns than the tree has, so P5's check
reaches past the end of the arm's answer for the column right of the
old root; buckets putting the right child in its parent's column takes
its left children further left than the first walk's leftmost column.

Six survived and are equivalent, and they show why rows need care. A
node at depth d in column c took (d + c) / 2 steps to the right and
(d - c) / 2 to the left, so within one column any count that grows
with the depth orders the nodes as the row does, and a tie in it is a
tie in the row. ★ putting a right child two rows down counts depth
plus right steps; buckets putting a left child two rows down, depth
plus left steps; merge not lowering the left subtree's rows counts the
right steps alone, and not lowering the right subtree's the left steps;
map putting a right child in its parent's row counts the left steps.
Merge putting each subtree's root at row 1,000,000 of its column
instead of 0 adds the same 1,000,000 to every row.

## Verification

Every arm prints the same output as `vertical_traversal.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 2.2 s (★) to 6.7 s (merge, which
copies each subtree's columns up to its parent, so the path of 1,000
nodes costs half a million copies), and the differential 15.0 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

The merge arm first sorted its columns with `for col in cols { let mut c
= col; c.sort(); ... }`. `karac check` refused the sort: a `for` over a
collection borrows it, so `col` is a `ref` to an element, and `let mut
c = col` copies the reference rather than the column (core-semantics
§4.6, §5.9). The arm consumes the columns with `cols.into_iter()`.

## Benchmarks

The bench runs the ★ arm in all five languages. The program grows 20
random trees of LeetCode's largest size, 1,000 nodes with values up to
1,000, once. In each of 500 rounds it runs the arm on every tree, each
round starting from a different one, and folds each answer's number of
columns and its middle column's size and first value into a checksum.
Every implementation prints `500 rounds over 20 trees of 1000 nodes:
189000 columns, checksum 693414335`. Each call walks the tree, sorts
its 1,000 places and builds a fresh list of columns. The Rust tree is
LeetCode's `Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's
`shared struct` is; C sorts with `qsort` and Go with `sort.Slice`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.272 to 1.474 s | 1.338 s |
| Rust (`rustc -O`) | 0.921 to 1.071 s | 0.967 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.909 to 1.028 s | 0.927 s |
| Go | 2.291 to 2.596 s | 2.416 s |
| Python | 4.4 s | |
| Kāra (`karac build --mir`) | 1.083 to 1.225 s | 1.152 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 3.8 times
Kāra's; its sort runs in C.

v2 took 1.24 times Rust's median time under overflow checks and 0.86
times C's. Under valgrind's cachegrind v2 ran 6,203 million
instructions and 1,072 million branches, 200 million of them indirect,
with 67.8 million mispredicted; Rust with overflow checks 4,170
million, 665 million with 3.6 million indirect, and 65.7 million; C
6,114 million, 1,416 million with 182 million indirect, and 94.2
million. C's indirect branches are `qsort` calling its comparison
through a pointer, about once per comparison. v2 makes a similar number,
which fits its sort also calling the tuple comparison through a pointer
where Rust's sort compiles the comparison in place (inferred, not
traced).
