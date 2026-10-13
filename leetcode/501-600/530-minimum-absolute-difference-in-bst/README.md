# 530. Minimum Absolute Difference in BST

Given the `root` of a Binary Search Tree (BST), return the minimum
absolute difference between the values of any two different nodes in
the tree.

```
root = [4, 2, 6, 1, 3]               ->  1
root = [1, 0, 48, null, null, 12, 49]  ->  1
```

**Constraints:** the number of nodes in the tree is in the range `[2,
10^4]`; `0 <= Node.val <= 10^5`.

## Approaches

Every arm is `fn get_minimum_difference(root: Option[TreeNode]) ->
i64` over a `shared struct TreeNode` (as in kata 501). The trees are
built by inserting values in order, a smaller value going left and a
larger one right, and an equal one either way by a coin flip, so a
tree may hold a value twice; the answer is then 0.

| file | mechanism |
|---|---|
| `get_minimum_difference.kara` ★ | in-order recursively; values come out ascending, so only neighbours in that order need comparing |
| `get_minimum_difference_stack.kara` | the same walk with an explicit stack |
| `get_minimum_difference_morris.kara` | Morris traversal: the walk threads each left subtree's rightmost node back to its parent and cuts the thread on the way back, O(1) extra space |
| `get_minimum_difference_sorted.kara` | every value gathered in any order, sorted, and neighbours compared; ignores the search order, so it works for any binary tree |
| `differential.kara` | the four arms against every pair of values, five properties |

Every arm prints the same 9 lines: both examples (inserted as `4, 2,
6, 1, 3` and `1, 0, 48, 12, 49`, which build the trees shown), two
nodes at the ends of the range, a repeated value, a rising and a
falling chain, and a closest pair on either side of the root; then for
300 random trees of 2 to 60 values from 0 to 9, 0 to 999, or 0 to
100,000 in turn how many have a repeat and a checksum over the
answers; and last the largest case, 10,000 values 10 apart except one
moved to 3 short of the next, inserted in a random order.
`get_minimum_difference.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the smallest difference over every pair of values. Each arm is held to
the properties below on 1,000 random trees of 2 to 30 values from 0 to
9, 0 to 999, or 0 to 100,000 in turn, rebuilt from the same values and
seed for every arm.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the tree is the same, in shape and values, after the call |
| P3 | one more copy of a value already there makes the answer 0 |
| P4 | every value `v` made `100,000 - v`, which turns the tree left to right, gives the same answer |
| P5 | the answer is between 0 and 100,000 |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`. P2 reads the tree in pre-order with a budget of one more
node than it holds, so a Morris thread left behind shows as a cycle cut
short instead of a walk that never ends.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers or the tree, and four that do not, each run under `karac
__mir-run`. All eight that change something are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right subtree walked in place of the left | P1 974, P3 964, P4 987, P5 974 |
| M2 | ★: only the first value kept as the one met last | P1 709, P3 720, P4 819 |
| M3 | stack: a node's right child never taken | P1 751, P3 782, P4 887, P5 108 |
| M4 | stack: the value met last kept one too high | P1 1000, P3 1000, P5 344 |
| M5 | morris: a thread never cut on the way back | P2 972 |
| M6 | morris: `is_some` for `is_none`, so no thread is ever made | P1 752, P3 793, P4 893, P5 108 |
| M7 | sorted: repeated values dropped after the sort | P1 344, P3 1000, P5 1 |
| M8 | sorted: the first gap skipped | P1 101, P3 80, P4 155, P5 33 |
| E1 | ★: `min` taken the other way round | 0 |
| E2 | stack: the best starts at 100,001, past any answer | 0 |
| E3 | morris: the difference taken as an absolute value | 0 |
| E4 | sorted: each gap taken backwards, as an absolute value | 0 |

M5 is the one P2 is for: the answers stay right and only the tree is
left changed. It fails 972 of 1,000 cases rather than all of them
because the rest have no left child anywhere, so no thread is made.
Before P2 had its budget, M5 ended the run with a stack overflow in
the property's own walk. M3 and M6 fail nearly the same checks: both
leave the walk with the left spine and lose everything to the right
of it. M7's one P5 failure is a tree of a single repeated value, which
the dedup leaves as one value and no gap. E2 holds because the
largest possible difference is 100,000, and E3 because an in-order
walk never meets a smaller value after a larger one.

## Verification

Every arm prints the same output as `get_minimum_difference.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints `20000 checks, 0 failures` on the first
two and runs clean under the third. `karac check` passes on every arm,
the differential and the bench program. All of this is at kara
`21ffa33dff`.

On the frozen legacy backends, `karac run --interp` runs the ★, stack
and sorted arms with the same output. The Morris arm stops at
`ref_eq`, which neither the legacy interpreter nor its codegen has
("method 'ref_eq' not found on type 'TreeNode'"). LLJIT and legacy
`karac build` fail every arm at codegen: the harness's call
`show("example 1", vec![...], mut seed)` fails LLVM's module
verification ("Call parameter type does not match function
signature"). The differential is refused at type checking: legacy
types the items of a `Vec`'s `iter()` by value, so it refuses `*v`.
The bench program builds and runs right on legacy. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random search trees of
10,000 different values (the problem's most) once, drawn from 0 to
10,000, 0 to 20,000, and so on up to 0 to 100,000, then finds the
answer for each tree 50 times. With that many values the closest pair
is almost always 1 apart, and here every answer is: every
implementation prints `100 trees of 10000 values, 50 times each:
total 5000, checksum 414687699`, the Kāra program under `karac
__mir-run` included (in 166 s). The work is the walk, which visits every
node whatever the answer.

Rust's tree is `Rc<RefCell<TreeNode>>`, the closest match to a `shared
struct`; C mallocs each node and Go leaves them to the collector. Spot
timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.17 to 1.28 s |
| Rust (`rustc -O`) | 3.23 to 3.32 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.82 to 3.07 s |
| Go | 1.21 to 1.40 s |
| Python | 18.8 to 19.5 s |
| Kāra (legacy `karac build`) | 2.73 to 2.86 s |
| Kāra (`karac build --mir`) | 2.90 to 3.12 s |

Legacy `karac build` builds this program, so `bench.sh` is the
`scripts/new-bench.sh` output unchanged and times the legacy build;
the `--mir` row is timed by hand. Both are timed at kara `21ffa33dff`.
Under `karac __mir-llvm-run` the program prints the same line in
4.7 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
written.
