# 2764. Is Array a Preorder of Some Binary Tree

*A premium problem.*

Given a **0-indexed** integer **2D array** `nodes`, your task is to
determine if the given array represents the **preorder** traversal of
some **binary** tree.

For each index `i`, `nodes[i] = [id, parentId]`, where `id` is the id of
the node at the index `i` and `parentId` is the id of its parent in the
tree (if the node has no parent, then `parentId == -1`).

Return `true` *if the given array* ***represents*** *the preorder
traversal of some tree, and* `false` *otherwise.*

**Note:** the **preorder** traversal of a tree is a recursive way to
traverse a tree in which we first visit the current node, then we do
the preorder traversal for the left child, and finally, we do it for
the right child.

```
nodes = [[0, -1], [1, 0], [2, 0], [3, 2], [4, 2]]  ->  true
nodes = [[0, -1], [1, 0], [2, 0], [3, 1], [4, 1]]  ->  false
```

**Constraints:** `1 <= nodes.length <= 10^5`, `nodes[i].length == 2`,
`0 <= nodes[i][0] <= 10^5`, `-1 <= nodes[i][1] <= 10^5`, the input is
generated such that `nodes` make a binary tree.

## Approaches

A node of a binary tree has at most two children, and either may be the
left, so the list is a preorder of some binary tree just when it is a
depth-first order of the tree it describes: each node's parent is the
node just before it or an ancestor of that node.

| file | mechanism |
|---|---|
| `preorder.kara` ★ | a stack of the nodes whose subtrees are still open: each node closes every subtree above its parent, by `while let Some(top) = stack.last()`, and fails when its parent is not open at all. O(n) |
| `preorder_recursive.kara` | the list walked as written: a node takes its place, then as long as the next node names it as parent, that node's subtree is read by a recursive call sharing one position through `mut ref`; a preorder when the first node is the root and the walk reads every node. O(n), recursing as deep as the tree |
| `preorder_intervals.kara` | each subtree must fill the places from its root's on, as many as it has nodes: the sizes summed from the leaves up, a node queued in a `VecDeque` once its children are done, places and parents in `Map`s by id, and every node's stretch checked against its parent's by `all`. O(n) |
| `preorder_ancestors.kara` | no stack: from the node before, the parent pointers, a `Map` built by `collect` from `(id, parent)` pairs, climbed until the new node's parent turns up, or past the root. A node climbed past is closed and never climbed again. O(n) |
| `preorder_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `Vec<i32>` stack popped by `while let Some(&top) = stack.last()` until the parent is on top, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one node; a
chain of `10^5`, LeetCode's most, and the same with its second and third
nodes swapped; a node whose parent's subtree has already closed; 3000
random trees of 1 to 12 nodes; and 10 of `10^5`, the last two with the
count of preorders and a checksum. Each random tree's ids are spread over
0 to `10^5`, it is listed in a random preorder, and half the time two
places are swapped. `preorder.py` mirrors the ★ arm and its output is
byte-identical.

```
true
false
true
true
false
false
3000 small trees: 1883 preorders, checksum 355201519
10 trees of 100000: 2 preorders, checksum 38
```

The chain recurses `10^5` deep in the recursive arm, under the MIR
interpreter as well as compiled.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the tree the pairs describe, each node's two children taken
in both orders, left or right, every combination's preorder built by the
recursive definition, and the list a preorder when one of them is the
list itself; no stack. It draws 2000 random trees of 1 to 12 nodes, then
100 of up to 2000, as the arms' harness draws them, all before any arm
answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 nodes, the answer is the literal reading's |
| P2 | every id x made `10^5 - x`: the same answer |
| P3 | a new node put at the end, a child of the node before it: the same answer |
| P4 | from 2 nodes on, the root moved to the end: false |
| P5 | the nodes relisted in a preorder of their own tree: true |
| P6 | each arm agrees with at least three of the other four |

P4 first moved the first node to the end, which, in a list whose swap
had moved the root off the front, can bring the root to the front and
make a preorder; 355 checks failed on that, and P4 now moves the root.

The differential prints `2100 cases: checksum 207434393, 63000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same orders of children gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M2 and M6 fail the same checks in the same
numbers, as do M3 and M10, and M4 and M7: each pair breaks the answer
the same way, from different arms.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the stack never popped | P1 497, P6 545 |
| M2 | ★: the bottom of the stack read for its top | P1 905, P3 168, P5 1687, P6 957 |
| M3 | recursive: only a node's first child read | P1 880, P5 1642, P6 932 |
| M4 | recursive: a node's parent taken for itself | P1 1073, P3 176, P5 1924, P6 1125 |
| M5 | intervals: only the parent before the child asked | P1 78, P6 79 |
| M6 | intervals: each child counted as one node | P1 905, P3 168, P5 1687, P6 957 |
| M7 | ancestors: the node before never taken as the parent | P1 1073, P3 176, P5 1924, P6 1125 |
| M8 | ancestors: a list not starting at the root let through | P1 132, P4 1374, P6 132 |
| M9 | solution: the root refused too | P1 1249, P5 2100, P6 1301 |
| M10 | solution: the whole stack cleared on a mismatch | P1 880, P5 1642, P6 932 |

## Benchmarks

The bench draws 20 random trees of `10^5` nodes, LeetCode's most, as the
harness draws them, all of them first, then answers each 100 times by
the ★ arm in all five languages: the stack is a `Vec` in Kāra and Rust,
a list in Python, a slice in Go and an array with a top index in C.
Every implementation prints `20 trees of 100000, 100 rounds: 800
preorders, checksum 746968672`.

BENCHTAB

## Verification

All five arms print the same output as `preorder.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The harness first
took its pairs as `list: Array[(i64, i64)]`, with no length; `karac
check` took that for a type of its own and refused the list literal
passed to it as a `Vec`, naming neither the length nor `Slice`. That was
kara `B-2026-11-20-143`, fixed at `0d28296389`: `Array[T]` now says it
takes a length, and `karac fix` makes it `Slice[T]`.

The harness first drew every random number below 32768, as each draw is
a 15-bit value; past that many nodes no new parent could be drawn, every
earlier node filled, and the Python mirror ran on with no end. The large
draws now join two.

LeetCode's Rust template took 15 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `Vec<Vec<i32>>`, `Vec<i32>` and
`Vec<Vec<i64>>` became `Vec[Vec[i32]]`, `Vec[i32]` and `Vec[Vec[i64]]`;
`Vec::new()` became `Vec.new()`; `while let Some(&top) = stack.last()`
became `while let Some(top) = stack.last().cloned()`; `&&` became `and`;
the `&v` pattern dropped its `&`; and `Solution::` became `Solution.`.
