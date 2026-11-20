# 1261. Find Elements in a Contaminated Binary Tree

Given a binary tree with the following rules:

1. `root.val == 0`
2. For any `treeNode`:
   1. If `treeNode.val` has a value `x` and `treeNode.left != null`, then
      `treeNode.left.val == 2 * x + 1`
   2. If `treeNode.val` has a value `x` and `treeNode.right != null`, then
      `treeNode.right.val == 2 * x + 2`

Now the binary tree is contaminated, which means all `treeNode.val` have
been changed to `-1`.

Implement the `FindElements` class:

- `FindElements(TreeNode* root)` Initializes the object with a
  contaminated binary tree and recovers it.
- `bool find(int target)` Returns `true` if the `target` value exists in
  the recovered binary tree.

```
["FindElements","find","find"], [[[-1,null,-1]],[1],[2]]                          ->  [null,false,true]
["FindElements","find","find","find"], [[[-1,-1,-1,-1,-1]],[1],[3],[5]]           ->  [null,true,true,false]
["FindElements","find","find","find","find"], [[[-1,null,-1,-1,null,-1]],[2],[3],[4],[5]]  ->  [null,true,false,false,true]
```

**Constraints:** `TreeNode.val == -1`; the height of the tree is at most
`20`; the total number of nodes is between `1` and `10^4`; total calls of
`find()` is between `1` and `10^4`; `0 <= target <= 10^6`.

The arms are `struct FindElements` with `fn new(root: Option[TreeNode]) ->
FindElements` and `fn find(self, target: i64) -> bool`, over `shared
struct TreeNode { mut val: i64, mut left: Option[TreeNode], mut right:
Option[TreeNode] }`, LeetCode's `Rc<RefCell<TreeNode>>`.

## Approaches

The values the rules give are the places of a heap: the root 0 and the
children of `x` at `2x + 1` and `2x + 2`. So a target is in the tree when
the tree has a node at the target's heap place, and that place's path
from the root is the binary digits of `target + 1` after its leading 1.

| file | mechanism |
|---|---|
| `find_elements.kara` ★ | by a set: the tree recovered from the root down by recursion, every value kept in a `Set`, and `find` one lookup |
| `find_elements_walk.kara` | by walking: the tree recovered and kept, and `find` steps down by the digits of `target + 1`, a 0 to the left and a 1 to the right, `leading_zeros` finding where they start |
| `find_elements_bfs.kara` | level by level: nodes taken from a `VecDeque`, each setting its children's values from its own, and the values kept in a `SortedSet` |
| `find_elements_bitmap.kara` | by a bitmap: an explicit stack of `(node, value)` pairs, every value marking its place in a `Vec[bool]` that `resize` grows as values reach past its end |
| `find_elements_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Rc<RefCell<TreeNode>>`, `HashSet<i32>`, a nested `fn dfs`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's three examples; 300 random
trees of 1 to 300 nodes at most 20 levels deep, asked 100 targets each,
half of them places in the tree and half from 0 to 10^6 (`30000 targets:
15004 found, checksum 442445002`); and the constraints' top, a full heap
of 10^4 nodes asked every target from 0 to 10^4, and a path of 20 levels
zigzagging down asked every target up to 10^6. `find_elements.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the ★, BFS and bitmap arms checked clean as first written.
The walk arm was written with `label.leading_zeros() as i64`, which is
already an `i64`: a warning, and `karac fix` drops the cast. The solution
arm takes one round of fixes, 36 by `karac fix`'s count: the `use` lines
of `Rc`, `RefCell` and `HashSet` removed, `Option<Rc<RefCell<TreeNode>>>`
to `Option[TreeNode]`, `HashSet<i32>` to `Set[i32]`, the nested `fn dfs`
hoisted out of `new`, `n.borrow_mut()` dropped, `&self`, `&n.left` and
`&target` to bare borrows, `&mut HashSet<i32>` to `mut ref Set[i32]` and
its argument to `mut seen`, and `HashSet::new()` to `Set.new()`. All five
check clean. The arm keeps LeetCode's `i32` target, so the harness hands
targets over `as i32`: an `i64` is not narrowed to an `i32` without one.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a target is in the tree when the tree has a node at its heap
place. 2000 random trees of 1 to 40 nodes, grown one free child at a time
from the root, each asked 30 targets from 0 to two past the deepest
place.

| | property |
|---|---|
| P1 | the statement read literally: found where the tree has a node at the target's heap place |
| P2 | recovered a second time, the same answers |
| P3 | the tree mirrored left to right, the mirrored targets found alike |
| P4 | every node holding its place's value once recovered |
| P5 | a found target's parent found too |
| P6 | the ★ arm's answers |

All 60,000 checks pass on every arm: `2000 trees: checksum 96437170,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the
same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the right child given `2x + 1` | P1 1741, P3 1578, P4 1923, P6 6964 |
| S2 | ★: the root recovered as 1 | P1 1867, P3 1913, P4 2000, P5 648, P6 7468 |
| W1 | walk: a 0 digit steps right and a 1 left | P1 1733, P6 1733 |
| W2 | walk: the path read from `target`, not `target + 1` | P1 1733, P6 1733 |
| B1 | level by level: the left child never queued | P1 1655, P3 1164, P4 1832, P6 1655 |
| B2 | level by level: the left child given `2x` | P1 1741, P3 1803, P4 1913, P5 1144, P6 1741 |
| M1 | bitmap: the last marked place out of bounds for `find` | P1 636, P3 351, P6 636 |
| M2 | bitmap: the left child given `2x + 2` | P1 1710, P3 1578, P4 1913, P6 1710 |
| L1 | solution: the left child given `2x` | P1 1741, P3 1803, P4 1913, P5 1144, P6 1741 |
| L2 | solution: the node's value never written back | P4 2000 |

Nine of the ten are caught by P1, the statement read literally. L2 is
the one it cannot see: the solution still puts each node's right value in
its set and answers every `find` correctly, and only leaves the tree
contaminated, which P4 alone checks; the statement asks `new` to recover
the tree, so it is a real fault. The two walk mutants fail identically,
and only P1 and P6 see them: each answers `true` for 0 and `false` for
every other target, which a mirrored tree answers the same way, and with
no `true` past the root no parent is ever asked. P2, recovering a tree a
second time, catches nothing: every arm sets each value afresh, so a
second recovery is the first again.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the tree recovered from the root down, every value kept in a hash
set) on 20 random contaminated trees of 10000 nodes, at most 20 levels
deep, built once; 120 rounds, each tree recovered again and asked 10000
targets, half of them nodes' places; the targets found counted and
folded into a checksum. Every program prints `120 rounds of 20 trees of
10000 nodes: 12086400 found, checksum 639445200`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.668 to 2.178 s | 1.860 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.533 to 1.960 s | 1.814 s |
| Rust (`rustc -O`) | 1.824 to 2.362 s | 2.073 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.844 to 2.342 s | 2.114 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.791 to 2.266 s | 2.028 s |
| C (`clang -O3`) | 1.181 to 1.322 s | 1.255 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.175 to 1.282 s | 1.220 s |
| Go | 2.145 to 2.598 s | 2.297 s |
| Python | 10.68 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 14% ahead of Rust with overflow checks on (1.814 s
against 2.114 s), and the two ranges overlap. C is about 31% ahead of
Kāra (1.255 s against 1.814 s); Kāra is about 21% ahead of Go (1.814 s
against 2.297 s). Python takes about 6x Kāra's time. No profile was
taken.
