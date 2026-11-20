# 1214. Two Sum BSTs

Given the roots of two binary search trees, `root1` and `root2`, return
`true` if and only if there is a node in the first tree and a node in
the second tree whose values sum up to a given integer `target`.

```
root1 = [2,1,4], root2 = [1,0,3], target = 5              ->  true    2 and 3
root1 = [0,-10,10], root2 = [5,1,7,0,2], target = 18      ->  false
```

**Constraints:** the number of nodes in each tree is in `[1, 5000]`;
`-10^9 <= Node.val, target <= 10^9`.

The arms are `fn two_sum_bsts(root1: Option[TreeNode], root2:
Option[TreeNode], target: i32) -> bool`, over a `shared struct TreeNode`
with an `i32` value and two `Option[TreeNode]` children, the handle
LeetCode's `Rc<RefCell<TreeNode>>` becomes. The two Rust arms keep the
method LeetCode gives Rust users, inside `impl Solution`, and a one-line
`two_sum_bsts` calls it.

## Approaches

| file | mechanism |
|---|---|
| `two_sum_bsts.kara` ★ | each tree's values read in order into a `Vec`, rising, then two pointers, one climbing the first list from its least value and one coming down the second from its greatest: a sum too small moves the first on, too large the second. O(n1 + n2) |
| `two_sum_bsts_set.kara` | the first tree's values gathered into a `Set`, then the second tree walked, each node asking whether the set holds `target - value`; the order the trees keep goes unused. O(n1 + n2) expected |
| `two_sum_bsts_search.kara` | every node of the second tree, from a stack, looks for `target - value` down the first tree, turning left or right at each node as a search tree allows. O(n2 h1) |
| `two_sum_bsts_lazy.kara` | the two pointers without the lists: an in-order walk of the first tree and a reverse in-order walk of the second, each a `struct Walk` holding a stack of the nodes still to visit, so only one root-to-leaf path of each tree is held at once. O(n1 + n2) time, O(h1 + h2) space |
| `two_sum_bsts_hashset.kara` | a Rust solution as LeetCode's Rust users write it (two nested `fn`s over `&Option<Rc<RefCell<TreeNode>>>`, one gathering the first tree into a `HashSet<i32>` through `n.borrow()`, the other asking `set.contains(&(target - n.val))` at each node of the second), carried to Kāra by `karac fix` |
| `two_sum_bsts_stacks.kara` | another Rust solution (two stacks of `Rc<RefCell<TreeNode>>`, filled by `while let Some(n) = c1 { c1 = n.borrow().left.clone(); s1.push(n); }`, their tops read through `s1.last().unwrap().borrow().val`, and a step taken by `s1.pop().unwrap().borrow().right.clone()`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 12 lines: LeetCode's two examples; one node in
each tree, with a target their sum (`true`) and one more (`false`); the
range's two ends, -10^9 and 10^9 against a target of 0 (`true`), and
10^9 against 10^9 and -10^9 with a target of 10^9 (`false`); a tree of
five against a tree of three, a target two values reach (`true`) and one
less (`false`); 1000 random small cases, 1 to 8 values from -10 to 10 in
each tree, put in one by one with repeats allowed (`1000 small cases:
304 true, checksum 905804664`); and three at the constraints' top: two
balanced trees of 5000 distinct values up to 10^9 and a sum they hold
(`true`), the same trees against 20 random targets (`19 not found`), and
two chains of 5000 nodes, every node the right child of the one before
in the first (0, 2, up to 9998) and the left child in the second (-1,
-3, down to -9999), against the sum of the first's deepest node and the
second's root (`true`) and against an even target, which an even and an
odd value never reach (`false`). `two_sum_bsts.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, set, search and lazy arms check clean as written.
The hashset arm takes one round of 62 fixes (among them the three `use`
lines dropped, `struct Solution;` to `struct Solution {}`, the nested
`fn collect` and `fn find` moved to the top level,
`Option<Rc<RefCell<TreeNode>>>` to `Option[TreeNode]`, `&mut
HashSet<i32>` to `mut ref Set[i32]` and `&HashSet<i32>` to `Set[i32]`,
`let n = n.borrow();` dropped, `contains(&(target - n.val))` to
`contains(target - n.val)`, and `||` to `or`), and the stacks arm one
round of 36 (among them `Vec<Rc<RefCell<TreeNode>>>` to `Vec[TreeNode]`,
`n.borrow().left.clone()` to `n.left.clone()`,
`s1.last().unwrap().borrow().val` to `s1.last().unwrap().val`, and
`s1.pop().unwrap().borrow().right.clone()` to
`s1.pop().unwrap().right.clone()`). Both outputs match.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every node of the first tree against every node of the
second. 2000 random cases: 1 to 7 values from -8 to 8 in each tree, put
in one by one with repeats allowed, and a target from -16 to 16; 612 of
them answer true.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the trees swapped give the same |
| P3 | the first tree's values and the target each one more give the same |
| P4 | both trees mirrored and negated, with the target negated, give the same |
| P5 | the sum of a node from each tree is found |
| P6 | a node added to the first tree keeps a true answer true |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 456253994,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, every value of the first list against every value of the
second, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: each tree read right to left, falling | P1 554, P2 105, P4 105, P5 1616, P6 8, P7 2770 |
| S2 | ★: the second list's greatest value skipped | P1 152, P2 206, P4 225, P5 598, P7 760 |
| E1 | set: the second tree's right subtrees never asked | P1 237, P2 280, P4 295, P5 658, P7 237 |
| E2 | set: the first tree gathered negated | P1 619, P2 653, P3 630, P5 1187, P7 619 |
| H1 | search: the search turns the wrong way | P1 378, P2 280, P5 1055, P7 378 |
| H2 | search: the second tree's right children never visited | P1 237, P2 280, P4 295, P5 658, P7 237 |
| Z1 | lazy: both walks go down the left side | P1 389, P2 273, P4 329, P5 1120, P7 389 |
| Z2 | lazy: the other walk advanced | P1 557, P2 105, P4 105, P5 1659, P6 12, P7 557 |
| X1 | hashset: the first tree's left subtrees never gathered | P1 221, P2 261, P4 294, P5 569, P7 221 |
| X2 | hashset: the other half taken as target plus the value | P1 598, P2 653, P5 1160, P7 598 |
| K1 | stacks: a step along the first walk goes left | P1 227, P2 280, P4 294, P5 650, P7 227 |
| K2 | stacks: the walks advanced the wrong way round | P1 557, P2 105, P4 105, P5 1659, P6 12, P7 557 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. E1 and H2 are one fault in two arms: only the second tree's
left spine, its root and each left child below it, is ever asked, and
they fail alike. Z2 and K2 are another, the two walks advanced the wrong
way round, so a sum too small makes it smaller still, and fail alike
too; with S1, whose lists both fall, they are the three that P6 catches,
an answer that rests on how the pointers meet rather than on which sums
exist. P3, the first tree's values and the target each one more, catches
only E2, which pairs each value of the second tree with the negation of
one of the first: the difference it finds moves by two where a sum moves
by one with the target. S2 starts the second pointer one short of the
greatest value, so against a tree of one node it never looks at all.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (each tree's values read in order, then two pointers, one climbing
the first list and one coming down the second) on 16 pairs of balanced
search trees of 5000 nodes each, the constraints' most, with distinct
values up to 10^9, built once; then 10 rounds over the pairs, each with
four targets, two of them sums a pair holds, every answer folded into a
checksum. Every program prints `10 rounds over 16 pairs of 5000-node
trees: checksum 432989804`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.108 to 0.153 s | 0.120 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.109 to 0.136 s | 0.117 s |
| Rust (`rustc -O`) | 0.133 to 0.174 s | 0.154 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.135 to 0.170 s | 0.148 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.124 to 0.177 s | 0.148 s |
| C (`clang -O3`) | 0.069 to 0.088 s | 0.073 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.068 to 0.091 s | 0.074 s |
| Go | 0.133 to 0.163 s | 0.147 s |
| Python | 1.481 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 21% ahead of Rust with overflow checks on (0.117 s
against 0.148 s), and the two ranges overlap. Kāra takes about 1.6x C's
time (0.117 s against 0.073 s); Kāra is about 20% ahead of Go (0.117 s
against 0.147 s). Python takes about 13x Kāra's time. No profile was
taken.
