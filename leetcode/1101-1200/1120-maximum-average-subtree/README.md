# 1120. Maximum Average Subtree

Given the `root` of a binary tree, return the maximum average value of a
subtree of that tree. Answers within `10^-5` of the actual answer will
be accepted.

A subtree of a tree is any node of that tree plus all its descendants.

The average value of a tree is the sum of its values, divided by the
number of nodes.

```
root = [5,6,1]      ->  6.00000
root = [0,null,1]   ->  1.00000
```

**Constraints:** the number of nodes in the tree is in the range `[1,
10^4]`; `0 <= Node.val <= 10^5`.

The arms are `fn maximum_average_subtree(root: Option[TreeNode]) ->
f64`, where `TreeNode` is a `shared struct` with `mut` fields:
LeetCode's Rust `Option<Rc<RefCell<TreeNode>>>` is Kāra's
`Option[TreeNode]`. Every arm divides a subtree's whole sum by its whole
count, so two arms that find the same subtree give the same `f64`, and
the arms are compared exactly.

## Approaches

| file | mechanism |
|---|---|
| `maximum_average_subtree.kara` ★ | one walk from the root: each call returns its subtree's sum and count, after its children's, and the best average so far is kept through a `mut ref f64`. O(n) |
| `maximum_average_subtree_levels.kara` | the nodes met level by level into a `Vec`, each with its parent's index, then walked back from the last: a node's sum and count are whole when it is reached, and are added to its parent's. O(n) |
| `maximum_average_subtree_stats.kara` | a recursion that changes nothing outside it: each call returns a `Stats` of its subtree's sum, count and best average, `None` for no node. O(n) |
| `maximum_average_subtree_fraction.kara` | the averages compared as fractions, `a / b > c / d` as `a * d > c * b`, through a `mut ref (i64, i64)`, and the best divided out once at the end. O(n) |
| `maximum_average_subtree_stack.kara` | an explicit stack, as Rust writes a walk with no recursion: each node pushed to open it and again to close it, its subtree's sum and count popped from a second stack of results. Written as Rust and carried to Kāra by `karac fix`. O(n) |
| `maximum_average_subtree_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `Rc<RefCell<TreeNode>>`, a nested `fn dfs` returning the sum and count and writing the best through `&mut f64`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines, each answer to five places: the
answers for LeetCode's two examples and six more (one node, all zeros,
a leaf beating its parent, a value far above the rest deep in a full
tree, a chain, a tree whose best is a lone leaf), then over 2000 random
trees of up to 40 nodes, values up to 10, 1000 or 10^5, the answers
summed and a checksum (`2000 random trees: answers total 56550931.129,
checksum 143096677`), and two of LeetCode's largest: 10^4 random nodes,
and a chain of 10^4 falling from 10^5. `maximum_average_subtree.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every node's subtree, its values listed and averaged, and the
largest average kept. Each arm answers a fresh copy of the tree. It
checks 2000 problems in four kinds of 500: up to 12 nodes hung at
random, values up to 1 or up to 10; one to three nodes, values up to
10^5; a chain of up to 20, each node to a random side, values up to
100; and a complete tree of up to 31, values up to 10^5. Every random
choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | by a second reading: some node's subtree, its nodes counted one at a time, has the answer for its average, and the answer is at least every leaf's value and the whole tree's average, and at most the largest value |
| P3 | the tree mirrored gives the same answer |
| P4 | every value raised by a random `k` raises the answer by `k` (to `10^-6`) |
| P5 | every value doubled doubles the answer |
| P6 | the tree hung below a new root of 0 gives the same answer |

All 72,000 checks pass on every arm: `2000 problems: checksum 608512155,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems, averaging every node's subtree with `fractions.Fraction`,
gives the same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left subtree counted twice | P1 449, P2 349, P3 537, P4 173 |
| M2 | ★: a leaf never the best | P1 1279, P2 1279, P4 233, P6 226 |
| M3 | ★: a node's own value left out of what it hands up | P1 575, P2 460, P4 276 |
| M4 | levels: every node's parent taken as the root | P1 733, P2 733, P6 293 |
| M5 | levels: walked from the root down, the sums not yet whole | P1 955, P2 955 |
| M6 | levels: the whole tree never a candidate | P1 475, P2 475, P4 233, P6 475 |
| M7 | stats: the right child's best replaces the left's | P1 574, P2 550, P3 797 |
| M8 | stats: a child's sum halved | P1 575, P2 473, P4 363, P5 154 |
| M9 | stats: a child counted as one node | P1 1322, P2 1322, P4 1392, P6 739 |
| M10 | fraction: the cross-multiplication crossed wrong | P1 1488, P2 1256, P6 1984 |
| M11 | fraction: a half added to any best of two or more nodes | P1 604, P2 604, P3 2, P5 604 |
| M12 | stack: a node with only a right child never a candidate | P1 269, P2 144, P3 569, P6 68 |
| M13 | stack: an empty result pushed as each node opens | P1 113, P2 113, P3 153 |
| M14 | solution: the larger subtree counted, not both | P1 648, P2 648, P4 851 |
| M15 | solution: the answer starts at one | P1 55, P2 55, P4 55, P5 55 |

P1 and P2 catch all fifteen, P4 eight, P6 six, P3 five and P5 three.
P2 sometimes fails on fewer problems than P1: it asks only that the
answer be some subtree's average and beat every leaf and the whole tree,
so a wrong answer that happens to be another subtree's average above all
of those passes it. P4 is the strongest self-comparison: raising every
value by `k` raises a subtree's average by `k` whatever its size, so an
edit that weighs subtrees by something other than their count of nodes
fails it. P6 sees the edits that lose or misjudge a subtree depending on
where it sits, since a new root above the tree moves every node down. P3
sees the edits that treat left and right apart, and P5 the three whose
error does not double with the values: halving a child's sum loses odd
halves, adding a half adds the same half, and starting at one does not
scale. P3 to P6 together catch fourteen of the fifteen; M5 they cannot,
since walking from the root down hands up partial sums the same way in
every form of the tree. M15 failed on only 4 problems at first, those
whose best average is below one, which the inputs almost never held;
half the trees of the first kind now take values of only 0 and 1.

Of the fifteen not kept, four fail as a kept edit: the levels arm
counting a child as one node and the stack arm handing a subtree up as
one node as M9, the fraction arm never taking a leaf as M2, and the
fraction arm starting at one as M15. Two more fail alike in two arms:
the left subtree walked for the right (★ and stats), and the right
children never met (levels and solution). The stack arm never walking
the right children stops: a node pops a result its right child never
pushed, and `unwrap()` on `None` panics. The other six fail in ways of
their own but were not needed: the ★ arm losing the right subtree's sum,
the stats arm taking only leaves, the fraction arm not counting the
right subtree's nodes, the stack arm counting the left subtree one node
too many, and the solution arm taking half of any value and taking a
left child's count from the sum.

## Verification

Every arm prints the same output as `maximum_average_subtree.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found one gap, now fixed. The ★, levels, stats and fraction
arms were written as Kāra, the stack and solution arms as Rust writes
them. `karac fix` carried the stack arm to a clean check in one round
(`Option<TreeNode>` to `Option[TreeNode]`, `Vec<..>` to `Vec[..]`,
`Vec::new()` to `Vec.new()`) and the solution arm in six:
`Rc<RefCell<TreeNode>>` to `TreeNode` and the `use` lines dropped,
`&Option<..>` and `&mut f64` to `ref Option[..]` and `mut ref f64`, each
`dfs(&n.left, ans)` to `dfs(n.left, mut ans)`, the nested `fn dfs` moved
out of the `impl`, `struct Solution {}` declared and `Solution::` to
`Solution.`, and `ref Option[TreeNode]` to `Option[TreeNode]`, a
parameter borrowing by default. The gap: the solution's `let n =
n.borrow();`, which reads the node through its `RefCell`, became `let n
= n;` when the `RefCell` went, a binding that only renames; the fix now
drops the statement (B-2026-11-11-40). The solution arm keeps one leftover of the
`use` lines it lost, a blank line after its header comment. In the ★ and
fraction arms, `karac fix` took out a habit from Rust, `n.val as i64`
added to an `i64` sum, since an `i32` widens to `i64` by itself; in the
differential it took out two more such casts and a `sum::[i64]()`
turbofish.

## Benchmarks

The bench builds 16 random trees of 10^4 nodes once, LeetCode's
largest, values up to 10^5, each node hung at a random free place below
the ones before it. Each of 200 rounds changes one node's value in every
tree and solves it with the ★ arm: 3200 walks of 10^4 nodes. Every
implementation prints `200 rounds over 16 trees of 10^4 nodes: answers
total 319910490.000, checksum 370189636`. Rust's nodes are LeetCode's
own `Rc<RefCell<TreeNode>>`, Go's are on its collected heap, Python's
are objects with `__slots__`, and C `malloc`s each node.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `3402c1954a`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Go | 0.514 to 0.549 s | 0.529 s |
| C (`clang -O3`) | 0.616 to 0.667 s | 0.631 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.628 to 0.689 s | 0.640 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.717 to 0.819 s | 0.736 s |
| Kāra (`karac build`) | 0.706 to 0.862 s | 0.737 s |
| Rust (`rustc -O`) | 0.933 to 0.999 s | 0.968 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.949 to 1.044 s | 0.982 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.932 to 1.047 s | 0.992 s |
| Python | 10.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 1.4x Go's time and 1.2x C's, and is about 1.3x
faster than Rust, whose nodes are reached through `Rc<RefCell<..>>` with
a borrow flag checked on every read. Kāra's nodes are reference counted
and C frees each one, where Go's are left to its collector; the gap to
Go and C was not traced further. Python takes about 14x Kāra's time.
