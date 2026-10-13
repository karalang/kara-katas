# 513. Find Bottom Left Tree Value

Given the `root` of a binary tree, return the leftmost value in the
last row of the tree.

```
root = [2,1,3]                       ->  1
root = [1,2,3,4,null,5,6,null,null,7]  ->  7
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 10^4]`; `-2^31 <= Node.val <= 2^31 - 1`.

## Approaches

Every arm is `fn find_bottom_left_value(root: TreeNode) -> i64` over a
`shared struct TreeNode`; the tree has at least one node, so the root
is not an `Option`.

| file | mechanism |
|---|---|
| `find_bottom_left_value.kara` ★ | breadth-first with a `VecDeque`, one level at a time (`for _ in 0..queue.len()`): the front of the queue at the start of each level is its leftmost node, and the last level's is the answer. O(n) |
| `find_bottom_left_value_reversed.kara` | breadth-first in one queue with no levels, the right child pushed before the left, so every level is visited right to left and the deepest last: the very last node out of the queue is the answer. O(n) |
| `find_bottom_left_value_depth.kara` | a preorder walk, left before right, carrying the depth: the first node met deeper than any before is the leftmost of its level, kept in a small struct passed down as `mut ref`. O(n) time, O(height) stack |
| `find_bottom_left_value_stack.kara` | the same preorder on an explicit stack of `(TreeNode, i64)`, the right child pushed before the left, the best kept as a `(depth, value)` tuple. O(n) |
| `differential.kara` | the four arms on 1,500 random trees, five properties |

Every arm prints the same 8 lines: the two LeetCode examples, one node,
a lone right child, a bottom row under the right subtree, a zigzag,
the extremes -2^31 and 2^31 - 1, and for 300 random trees (1 to 60
nodes, the values from -2 to 2, from -1,000 to 1,000, or from the
whole range in turn) the count of nodes and a checksum of the answers.
The trees are given in LeetCode's level order, built by the harness.
`find_bottom_left_value.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random trees of 1 to 30 nodes, the values from -2 to 2, from -50
to 50, or from -10^6 to 10^6 in turn, each new node hung at the end of
a random walk down from the root.

| | property |
|---|---|
| P1 | the value is the reference's, the first in preorder of the values at the greatest depth |
| P2 | the mirror image of the tree gives the bottom row's rightmost value |
| P3 | every value plus 7 gives the value plus 7 |
| P4 | the tree as the right child of a new root, beside a leaf on the left, keeps its value, or gives the leaf's when the tree is a single node and the leaf joins its row |
| P5 | two copies of the tree side by side under a new root give the same value |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each level's last node, not its first (`queue.back()`) | P1 667, P2 667, P3 667, P4 723, P5 667 |
| M2 | ★: the walk stops at a level of one node (`while queue.len() > 1`) | P1 1340, P2 1344, P3 1340, P4 1404, P5 1398 |
| M3 | reversed: the left child goes in twice and the right never | P1 1116, P2 1123, P3 1116, P4 1444, P5 1116 |
| M4 | reversed: a stack, not a queue (`pop_back`) | P1 1137, P2 1146, P3 1137, P4 1193, P5 1137 |
| M5 | depth: the last node at a new depth, not the first (`>=`) | P1 667, P2 667, P3 667, P4 723, P5 667 |
| M6 | depth: the right subtree walked twice and the left never | P1 1275, P2 1285, P3 1275, P4 1331, P5 1275 |
| M7 | stack: the last node at a new depth (`>=`) | P1 667, P2 667, P3 667, P4 723, P5 667 |
| M8 | stack: the depth kept is one too deep | P1 712, P2 709, P3 712, P4 689, P5 683 |
| E1 | ★: the level's width read into a local before the loop | 0 |
| E2 | reversed: the answer starts at 0, not the root's value | 0 |
| E3 | depth: the deepest so far starts at -5, not -1 | 0 |
| E4 | ★: the answer starts at 0, not the root's value | 0 |

E1 is equivalent because a range's bounds are read once, when the
loop starts, so `0..queue.len()` already counts only the level's own
nodes while children are pushed. E2 and E4 are equivalent because the
root is queued before the loop, so the starting value is always
written over before it is read; E3 because any start below 0 lets the
root, at depth 0, replace it.

M1, M5 and M7 are the same wrong answer, the bottom row's rightmost
value, written into three arms, and fail the same 667 cases, the
trees whose bottom row holds two different values. P4 sees them in 56
more: when the tree is a single node, the leaf joins the root in the
new bottom row and the rightmost of the two is the tree's root. M2
reads the root, a level of one node, and stops there, so it answers
with the root's value; M3 and M6 walk one side of every node and miss
the other. M8 keeps the depth one too deep, so a node exactly one
level below the best so far no longer replaces it.

## Verification

All four arms print the same output as `find_bottom_left_value.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints `30000 checks, 0 failures` on both and
runs clean under the third. `karac check` passes on every file, the
bench program included.

On the frozen legacy backends, `karac run --interp` prints the same
output for the reversed, depth and stack arms, and panics on the ★ arm
at `queue.front().unwrap().val` ("internal error: entered unreachable
code: field access ... receiver was Value::Unit"). LLJIT and legacy
`karac build` fail on every arm at codegen: on the ★ arm at
`VecDeque.front` ("Vec/String method 'front' is not yet supported in
codegen"), and on the other three at the harness's calls to `show`,
whose first parameter is a `Str` given a string literal ("Module
verification failed: Call parameter type does not match function
signature!", as on katas 501, 508 and 510). Both refuse the
differential at type checking, on the `*d` and `*v` over the
reference's `all.iter()`, whose items legacy types by value ("unary
'*' requires 'ref T' ... found 'i64'"). Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random trees of 10,000
nodes (the problem's most), the values from the whole range, each tree
a random root over its list of values with those before it on the
left and those after it on the right, once. Then it solves each 50
times. Every implementation prints `100 trees of 10000 nodes, 50 times
each: checksum 287747657`, the Kāra program under `karac __mir-run`
included (in 144 s).

Every mirror uses a fresh queue for every call, as the ★ arm uses
`VecDeque.new()`: Rust a `VecDeque` of `Rc<RefCell<TreeNode>>`, the
closest match to a `shared struct`, Go a slice read from the front,
Python a `deque`, and C a ring buffer it writes itself, grown by
doubling. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.82 to 0.88 s |
| Rust (`rustc -O`) | 1.30 to 1.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.32 to 1.46 s |
| Go | 1.49 to 1.52 s |
| Python | 7.6 to 8.1 s |
| Kāra (`karac build --mir`) | 1.94 to 2.08 s |

The legacy `karac build` refuses this program: its codegen has no
`VecDeque.front` ("Vec/String method 'front' is not yet supported in
codegen"). So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`10fdedabfc`. Under `karac __mir-llvm-run` the program prints the same
line in 7.0 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
