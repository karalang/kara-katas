# 1305. All Elements in Two Binary Search Trees

Given two binary search trees `root1` and `root2`, return a list
containing all the integers from both trees sorted in ascending order.

```
root1 = [2,1,4], root2 = [1,0,3]  ->  [0,1,1,2,3,4]
root1 = [1,null,8], root2 = [8,1] ->  [1,1,8,8]
```

**Constraints:** the number of nodes in each tree is in `[0, 5000]`, and
`-10^5 <= Node.val <= 10^5`.

The arms are `fn get_all_elements(root1: Option[TreeNode], root2:
Option[TreeNode]) -> Vec[i32]`, over `shared struct TreeNode { mut val:
i32, mut left: Option[TreeNode], mut right: Option[TreeNode] }`.

## Approaches

| file | mechanism |
|---|---|
| `get_all_elements.kara` ★ | each tree read in order into its own `Vec`, already sorted, then the two merged, the smaller front taken each step. O(m + n) |
| `get_all_elements_sort.kara` | the search order set aside: every value of both trees gathered by a pre-order walk from a `Vec` used as a stack, then the lot sorted. O((m + n) log(m + n)) |
| `get_all_elements_heap.kara` | every value of both trees into a smallest-first `PriorityQueue` by a recursive walk, then popped off in order. O((m + n) log(m + n)) |
| `get_all_elements_morris.kara` | each tree read in order with no stack and no recursion, by threading each node's in-order predecessor back to it for the climb up and cutting the thread on the way past; the two sorted lists then merged, the rest of whichever is left added with `extend`. A tree holds no repeated value, so a predecessor's right child is the thread exactly when its value is the node's own. O(m + n) |
| `get_all_elements_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn dfs(node: &Option<Rc<RefCell<TreeNode>>>, v: &mut Vec<i32>)` nested in the method reading both trees in order into one `Vec`, then `v.sort_unstable()`), carried to Kāra by `karac fix` |
| `get_all_elements_stacks.kara` | a second Rust solution as LeetCode's Rust users write it (two in-order walks stepped side by side, each a `Vec<Rc<RefCell<TreeNode>>>` stack fed down the left spine by `while let Some(n) = c1 { c1 = n.borrow().left.clone(); .. }`, the smaller top taken by a `match (s1.last(), s2.last())`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, one tree
empty and both empty (`-` is the empty list), and a chain of 5000 values
put in rising beside one of 5000 put in falling, one all right children
and the other all left, the answer's length and checksum
(`0,1,1,2,3,4 1,1,8,8 1,5,7 - 10000:27484355`); then 2000 random pairs of
0 to 300 draws each from -10 to 10, -1000 to 1000 or `-10^5` to `10^5`, a
repeat left out of its tree (`2000 random pairs: elements total 407587,
checksum 116673005`). `get_all_elements.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`. The Morris arm makes
each tree a cycle for a while, and under `karac __mir-llvm-asan` it, and
the second Rust arm, run clean.

The Mend loop: the ★, sorting and heap arms checked clean as first
written. The Morris arm wrote Rust's `let (mut i, mut j) = (0, 0)`, and
`karac fix` made it `let mut (i, j) = (0, 0)` (3 fixes from 2 errors).
The first Rust arm takes one round of 41 fixes by `karac fix`'s count,
from 19 errors: the two `use` lines deleted, since a `shared struct` is
Kāra's `Rc<RefCell<..>>`, `struct Solution;` to `struct Solution {}`,
`Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, `Vec<..>` to
`Vec[..]`, the nested `fn dfs` moved to the top level, its `&Option<..>`
parameter made bare and its `&mut Vec<i32>` made `mut ref Vec[i32]`, `let
n = n.borrow();` dropped, the calls' `&n.left` to `n.left` and `&mut v`
to `mut v`, `Vec::new()` to `Vec.new()`, `v.sort_unstable()` to
`v.sort()`, Kāra's one sort of a `Vec`, and `::` to `.`. The second takes
one round of 30 fixes from 8 errors: the same `use` lines, `struct` and
type rewrites, `vec![]` to `Vec.new()`, `n.borrow().left.clone()` to
`n.left.clone()` and `a.borrow().val` to `a.val`, `&&` to `and`, and `::`
to `.`. Both outputs match on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every value of both trees, then the smallest of those left
taken again and again until none are left. 2000 pairs of trees of 0 to
12 draws each, a repeat left out of its tree, in four kinds, 500 each:
values from -3 to 3, so that the two trees share most of them; from -20
to 20; one tree empty; and the values put in sorted, rising or falling,
so that the trees are chains. Every tree and extra value is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the trees swapped: the same answer |
| P3 | both trees mirrored and every value negated, which keeps them search trees: the answer negated and reversed |
| P4 | one more value put into a copy of the first tree: the answer with it in its place, unless the first tree has it |
| P5 | the second tree shifted above every value of the first: the first tree's answer alone, then the second's alone, shifted |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 pairs: checksum 101622377,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Thirteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. One is left out: the Morris arm
never cutting its threads leaves each tree a cycle, and the run dies of
a stack overflow, a crash rather than a failed check. The twelve kept, two
to each arm, are each killed, fail the same way under both backends and
not by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the merge stopped when either list runs out | P1 1952, P2 267, P3 1281, P4 2000, P5 1282, P6 9760 |
| M2 | ★: each node read before its left subtree | P1 1648, P2 306, P3 1877, P4 1793, P6 8240 |
| M3 | sorting: no left child gathered | P1 1648, P3 1876, P4 1793, P6 1648 |
| M4 | sorting: a value in both trees kept once | P1 855, P4 973, P6 855 |
| M5 | heap: the largest popped first | P1 1893, P4 1951, P5 1282, P6 1893 |
| M6 | heap: the second tree never put in | P1 1627, P2 1942, P4 1627, P6 1627 |
| M7 | Morris: a node with no left child left out | P1 1952, P3 1827, P4 2000, P6 1952 |
| M8 | Morris: the second list's tail never added | P1 1107, P2 1718, P3 1050, P4 1003, P6 1107 |
| M9 | solution: the sort left out | P1 1226, P2 1272, P3 1272, P4 1521, P6 1226 |
| M10 | solution: the first tree read twice | P1 1942, P2 1942, P4 1992, P6 1942 |
| M11 | stacks: the larger top taken | P1 1274, P2 254, P3 731, P4 1614, P5 1282, P6 1274 |
| M12 | stacks: no right child of the first tree followed | P1 1178, P2 1643, P3 1468, P4 1445, P6 1178 |

P1, P4 and P6 kill all twelve, P2 and P3 eight each, and P5 three.
Swapping the trees (P2) passes the edits that treat both trees alike
(M3, M4, M5, M7) and fails the ones that treat the first and second
differently (M6, M8, M10, M12) or whose merge goes wrong in a way that
depends on which list is which (M1, M2, M9, M11). Mirroring and negating
(P3) turns a left child into a right one and the order round, so it
fails the edits tied to one direction of the walk (M2, M3, M7, M12) or of
the merge (M1, M8, M9, M11), and passes dropping repeats (M4), sorting
largest first (M5) and the edits that read one tree in place of the
other (M6, M10). With the second tree shifted above the first (P5), a
merge takes all of the first list and then all of the second, so the
answer is the two single-tree answers joined whatever an edit does to
each list; only the edits that order values from the two ranges wrongly
fail it: the merge stopping as the first list runs out (M1), the largest
first (M5), and the larger top taken (M11).

## Benchmarks

The bench builds 20 pairs of search trees of 4900 values each, drawn
from `-10^5` to `10^5` and put in in the order drawn, a repeat left out,
once from its own generator; then makes 100 passes, each putting one
value from the checksum so far into the first tree of every pair, so no
answer carries over and no tree passes the constraints' 5000, answering
it with the ★ arm and folding one value of the answer, at a place also
chosen from the checksum, its length and the pass into the checksum. The
nodes are `shared struct`s in Kāra and LeetCode's own
`Rc<RefCell<TreeNode>>` in Rust; each list is a `Vec` in Kāra and Rust, a
slice in Go, a list in Python, and an array grown by doubling with
`realloc` in C. Every implementation prints `100 passes over 20 pairs of
trees: checksum 777965476`.

BENCHTAB
