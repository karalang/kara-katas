# 1080. Insufficient Nodes in Root to Leaf Paths

Given the `root` of a binary tree and an integer `limit`, delete all
insufficient nodes in the tree simultaneously, and return the root of the
resulting binary tree.

A node is insufficient if every root-to-leaf path intersecting this node
has a sum strictly less than `limit`.

A leaf is a node with no children.

```
root = [1,2,3,4,-99,-99,7,8,9,-99,-99,12,13,-99,14], limit = 1  ->  [1,2,3,4,null,null,7,8,9,null,14]
root = [5,4,8,11,null,17,4,7,1,null,null,5,3], limit = 22       ->  [5,4,8,11,null,17,4,7,null,null,null,5]
root = [1,2,-3,-5,null,4,null], limit = -1                      ->  [1,null,-3,4]
```

**Constraints:** the number of nodes is in `[1, 5000]`;
`-10^5 <= Node.val <= 10^5`; `-10^9 <= limit <= 10^9`.

A node goes when no path through it reaches the limit, so what is left is
exactly the nodes on paths that do. A node that loses both children is
not a leaf of the old tree, and goes with them: its paths all ran through
a child that went.

The arms take LeetCode's tree, a `shared struct TreeNode` with an `i32`
value, as an `Option[TreeNode]`, and the limit as an `i64`, and return
the root of what is left. The trees are read and written in LeetCode's
level-order text.

## Approaches

| file | mechanism |
|---|---|
| `sufficient_subset.kara` ★ | one walk down that passes on what the rest of a path still has to make up: a leaf stays when its value covers it; any other node prunes both children against that less its own value, and stays only if a child does. O(n) time, O(h) stack |
| `sufficient_subset_best.kara` | the best path, bottom up: each call returns the largest sum of a path from its node down to a leaf, and a child goes when the sum down to it plus the child's best is short of the limit. O(n) time, O(h) stack |
| `sufficient_subset_stack.kara` | the ★ walk on an explicit `Vec[Visit]` stack: each node is met twice, first to push its children with what is left for them, then, after both, to decide; going is a cut in the parent's side, kept on the stack with the node. O(n) time, O(h) stack |
| `sufficient_subset_rebuild.kara` | the ★ rule into a new tree: every node that stays is a fresh copy whose children are the rebuilt children, so the tree passed in keeps every node. O(n) |
| `sufficient_subset_marks.kara` | the paths marked from their leaves: the nodes numbered level by level with their parents and the sums down to them; every leaf whose sum reaches the limit marks itself and the nodes above it, stopping at one already marked; then each node drops the children that are not marked. O(n), no recursion |
| `sufficient_subset_solution.kara` | LeetCode's Rust template (`struct Solution;`, `Option<Rc<RefCell<TreeNode>>>`, a `dfs` nested in the method that takes `borrow_mut()` of each node and `take`s its children, `Solution::`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and seven
more; how many of 300 random trees of 1 to 300 nodes, valued -10 to 10,
keep their root at a limit near the sum of one of their paths, with a
checksum over what is left (`291 keep their root, checksum 536429515`);
and a chain of 5000 nodes valued 1, kept whole at a limit of 5000 and
gone at 5001. `sufficient_subset.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the tree as arrays, every root-to-leaf path listed, and a node
kept when some path through it sums to the limit at least (no arm's
walk is reused). It checks 2000 problems, 1000 trees of 1 to 12 nodes
valued -3 to 3 and 1000 of 1 to 28 nodes valued -10 to 10, each at a
limit equal to one of its path sums, one either side of it, or anywhere
in the range the tree can make. Every random choice is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every root-to-leaf path left sums to the limit at least |
| P3 | what is left, pruned again at the same limit, stays as it is |
| P4 | at a higher limit (by 1 to 5), what is left answers the same as the tree |
| P5 | a limit at the least path sum keeps the whole tree, and one past the greatest keeps nothing |
| P6 | the root's value and the limit moved together (by -10 to 10) leave the same nodes, the root moved |

All 72,000 checks pass on every arm: `2000 problems: checksum 374153236,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems, pruning each node by the greatest path sum through it, gives
the same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All thirty are caught, each the
same way under both backends. Fifteen are kept, no two failing the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a leaf exactly at the limit dropped (`>`) | P1 646, P5 2000 |
| M2 | ★: the left side never takes the node's value off | P1 833, P2 410, P5 1240, P6 487 |
| M3 | ★: a node with only a right child judged as a leaf | P1 537, P2 263, P3 253, P4 192, P5 537 |
| M4 | best: a left side exactly at the limit cut (`<=`) | P1 464, P2 144, P3 144, P4 48, P5 1307 |
| M5 | best: the smaller side taken as the best (`min`) | P1 849 |
| M6 | best: the root never dropped | P1 412, P2 357, P5 2000 |
| M7 | stack: the children never take the value off | P1 1013, P2 493, P5 1294, P6 696 |
| M8 | stack: a node with no left child goes | P1 1235, P5 1520 |
| M9 | rebuild: the sides swapped | P1 1495, P3 1495, P4 980, P5 1861 |
| M10 | rebuild: every leaf kept | P1 1261, P2 1261, P5 2000 |
| M11 | marks: the root never marked (`j > 0`) | P1 1588, P5 2000 |
| M12 | marks: the wrong side cut | P1 849, P2 820, P3 820, P4 502 |
| M13 | marks: a node with only a right child counted a leaf | P1 208, P4 27, P5 344 |
| M14 | solution: a node kept when what is left to reach is not positive | P1 392, P5 649 |
| M15 | solution: a negative value taken as positive (`b.val.abs()`) | P1 923, P2 923, P5 1563, P6 201 |

P1 catches all fifteen, P5 thirteen, P2 eight, P4 five, P3 four and P6
three. P5 misses two edits that still get both ends right: M5's
smallest bests are path sums too, so at the least sum nothing is cut and
past the greatest the root goes, and M12 cuts the wrong side only when a
side goes, which at either end none does. M5 is the one only
P1 sees: taking each child's smaller best cuts too much, but every path
it leaves still reaches the limit, pruning again finds nothing, and the
answer moves with the root. P6 sees only an edit that gets wrong what a
node passes down, since moving the root and the limit together cancels
everywhere else.

Of the fifteen not kept, four fail exactly as a kept edit: the stack
arm's leaf at the limit and the marks arm's path at the limit as M1, the
marks arm's leaf judged by its own value as M7, and the rebuild arm's
node with no left side dropped as M8. Eleven fail in a way of their own
but were not needed: in the ★ arm, a node losing either child dropped
and the right side adding the value; in the best arm, the sum above
counted twice and the right side never adding the node; in the stack
arm, always the left child cut and the left child marked as a right one;
in the rebuild arm, the left side copied to the right and asked for one
less; in the solution arm, a leaf one short kept, the right side keeping
the whole limit and the left side never pruned.

## Verification

Every arm prints the same output as `sufficient_subset.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 2.7 s to 3.2 s and the
differential 29.9 s.

The kata found one false positive in the checker, fixed in kara
`52b677beea` with `tests/kata_1080_private_impl_pub_fn.rs`:

- **A `pub fn` of a private type was refused for naming private types.**
  After `karac fix` carries the Rust template's
  `Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, the check
  stopped at E0221, "private type 'TreeNode' leaks through method
  parameter 'root' of 'sufficient_subset'". `Solution` is not `pub`
  either, so nothing outside the program can name it or reach the
  method; Rust accepts the same shape. An inherent impl of a type that
  is not `pub` is no longer walked for leaks; a `pub` type's `pub fn` is
  still checked. Kara B-2026-11-09-24.

Every file went through `karac fix`. The Rust arm reaches a clean check
in three rounds and gives the text the arm holds: the syntax (`struct
Solution {}`, `<>` to `[]`, `&&` to `and`, `Solution.`); then
`Rc[RefCell[TreeNode]]` to the `shared struct`'s own `TreeNode`, with
`n.borrow_mut()` dropped to `n` and the first `use` gone; then the
nested `fn dfs` moved out of the method and the second `use` gone. In
the differential it dropped four `.to_string()`s on string literals
where a `String` is wanted.

## Benchmarks

The bench draws 200 random tree shapes of 1000 nodes once, valued -100
to 100, each node hung below the root by a random walk down to the first
empty place, and kept as arrays. Every one of 100 rounds builds each tree
afresh from its shape, since pruning cuts it apart, prunes it with the ★
arm at a limit from -200 to 200 that changes with the round and the
tree, and counts what is left. Every implementation prints `100 rounds
over 200 trees of 1000 nodes: 11305926 nodes kept, checksum 629549208`.
The Rust mirror is LeetCode's `Option<Rc<RefCell<TreeNode>>>`, counted
by reference as Kāra's `shared struct` is; the C mirror `malloc`s each
node and frees it when it is cut, or after the count.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `2a1ba88113`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`,
the matched-ISA rows `bench.sh` records:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.818 to 0.873 s | 0.839 s |
| C (`clang -O3`) | 0.802 to 0.963 s | 0.849 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.064 to 1.225 s | 1.110 s |
| Kāra (`karac build`) | 1.057 to 1.189 s | 1.117 s |
| Go | 1.083 to 1.228 s | 1.119 s |
| Rust (`rustc -O`) | 1.079 to 1.256 s | 1.128 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.078 to 1.248 s | 1.161 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.125 to 1.330 s | 1.171 s |
| Python | 9.73 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.11 s) is its real time.

The work is 20 million nodes allocated, walked twice and freed. Kāra,
Rust and Go are level, within 2% of one another, and Kāra is 4% ahead
of Rust with overflow checks at the same ISA. C, which keeps no count
on each node, takes 24% less. Python runs the same walk at 8.8x Kāra.
