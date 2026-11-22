# 2792. Count Nodes That Are Great Enough

You are given a `root` to a binary tree and an integer `k`. A node of
this tree is called **great enough** if the following conditions hold:

1. Its subtree has **at least** `k` nodes.
2. Its value is **greater** than the value of **at least** `k` nodes in
   its subtree.

Return *the number of nodes in this tree that are great enough.*

The node `u` is in the **subtree** of the node `v`, if `u == v` or `v`
is an ancestor of `u`.

```
root = [7, 6, 5, 4, 3, 2, 1], k = 2  ->  3
root = [1, 2, 3], k = 1              ->  0
root = [3, 2, 2], k = 2              ->  1
```

**Constraints:** the number of nodes in the tree is in the range `[1,
10^4]`, `1 <= Node.val <= 10^4`, `1 <= k <= 10`.

## Approaches

A node is great enough when at least k values of its subtree are below
its own, that is when the k-th least value of its subtree is below it;
so each node needs only the k least values of its subtree, and those
are among its own and its children's k least.

The arms take the tree as its values and each node's left and right
child, `-1` for none, the root node 0; the solution arm's adapter builds
LeetCode's nodes from them.

| file | mechanism |
|---|---|
| `great.kara` ★ | the nodes ordered parents first by a stack, then walked back so children come first; each node's own value and its children's k least lists joined, sorted and cut to k, and the node counted when the list is full and its last below the node's value. O(n k log k) |
| `great_heap.kara` | by recursion and heaps: each call returns a `PriorityQueue` of the subtree's k least values with the greatest on top, by their negatives, filled from the children's heaps and cut back to k; the count carried in a `mut ref`. O(n k log k) |
| `great_tour.kara` | by a preorder tour and a Fenwick tree: each subtree one run of places, and a node's count of values below its own the count over its run, read offline as the Fenwick tree's count at the run's end less the count before its start. O(n log V) |
| `great_merge.kara` | by recursion and merging: each call returns its subtree's k least values, the two children's lists merged by two fingers and the node's value merged in, no sorting, the count returned beside them. O(n k) |
| `great_solution.kara` | a Rust solution as LeetCode's Rust users write it, `Option<Rc<RefCell<TreeNode>>>` in, a nested `dfs` returning each subtree's k least values as a sorted `Vec<i32>`, the count kept in a `&mut i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; a path of
`10^4` nodes, LeetCode's most, going left, its values falling, so that
every node with k below it is great enough, and the same rising, so
that none is; 3000 random trees of 1 to 12 nodes with values from 1 to 5
and k from 1 to 4; and 20 of `10^4` nodes with values up to `10^4` and
k up to 10, the last two with the sum of the counts and a checksum.
`great.py` mirrors the ★ arm and its output is byte-identical.

```
3
0
1
9990
0
3000 small trees: great enough sum to 3623, checksum 550440331
20 trees of 10^4: great enough sum to 38482, checksum 50961849
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for every node, its subtree gathered by a stack, and the node
counted when the subtree holds at least k nodes and the node's value is
greater than the values of at least k of them; no least values kept. It
draws 2000 random trees of 1 to 10 nodes with values from 1 to 5 and k
from 1 to 4, then 50 of up to 2000 nodes with values up to `10^4` and k
up to 10, all before any arm answers; the literal reading is asked only
of the first 2000.

| | property |
|---|---|
| P1 | up to 10 nodes, the count is the literal reading's |
| P2 | every value 1000 more: the same count |
| P3 | the tree mirrored, each left child swapped with the right: the same count |
| P4 | k one more: no more |
| P5 | from 0 to n - k, the k least values being in no count, and 0 when every value is 1 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 446285225, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, each subtree gathered by recursion, gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value equal to the node's counted below it | P1 1396, P5 1759, P6 1446 |
| M2 | ★: the k least cut to k - 1 | P1 999, P6 1049 |
| M3 | heap: the heap cut back to k + 1 | P1 999, P6 1049 |
| M4 | heap: the node's own value pushed without its sign turned | P1 1681, P5 1759, P6 1731 |
| M5 | tour: the count before a run left out | P1 1145, P3 746, P6 1195 |
| M6 | tour: the count below a node read up to its own value | P1 1498, P3 358, P5 1759, P6 1548 |
| M7 | merge: the merge keeping k + 1 | P1 999, P6 1049 |
| M8 | merge: the left list's head taken whatever the right's | P1 556, P3 616, P4 250, P6 604 |
| M9 | solution: only the least value asked to be below | P1 550, P6 597 |
| M10 | solution: the lists cut to one value | P1 509, P6 556 |

## Benchmarks

The bench draws 20 random trees of `10^4` nodes, LeetCode's most, with
values up to `10^4` and k = 10, all of them first, then answers each 20
times by the ★ arm in all five languages. Every implementation prints
`20 trees of 10^4, 20 rounds: great enough sum to 358380, checksum
657620860`.

BENCHTAB

## Verification

All five arms print the same output as `great.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the own arms checked clean as first written. The merge arm
began its fingers as `let (mut i, mut j) = (0, 0)`, which `karac check`
refused, `mut` going before the whole pattern, and `karac fix` made it
`let mut (i, j)`.

LeetCode's Rust template took 44 `karac fix` edits, the adapter
included: the `use std::cell::RefCell` and `use std::rc::Rc` lines went;
`Option<Rc<RefCell<TreeNode>>>` became `Option[TreeNode]`, LeetCode's
node a `shared struct`; the nested `fn dfs` moved out to the top level,
taking `node: Option[TreeNode]`, `k: i64` for `k: usize` and `ans: mut
ref i32` for `&mut i32`; `n.borrow()` went, the fields read straight
from the node; `vec![]` became `Vec.new()`, `&&` became `and`, the
`&n.left` and `&mut ans` arguments became `n.left` and `mut ans`, and
`k as usize` became `k`; the adapter's `Vec<..>`s became `Vec[..]`, its
`|&v|` dropped the `&`, and its `as i64` on the answer, an `i32`
widening by itself, was dropped; and `Solution::` became `Solution.`.
