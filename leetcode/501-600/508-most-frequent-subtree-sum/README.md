# 508. Most Frequent Subtree Sum

Given the `root` of a binary tree, return the most frequent subtree
sum. If there is a tie, return all the values with the highest
frequency in any order.

The subtree sum of a node is defined as the sum of all the node values
formed by the subtree rooted at that node (including the node itself).

```
root = [5,2,-3]  ->  [2,-3,4]
root = [5,2,-5]  ->  [2]
```

**Constraints:** the number of nodes in the tree is in the range
`[1, 10^4]`; `-10^5 <= Node.val <= 10^5`.

## Approaches

Every arm is `fn find_frequent_tree_sum(root: Option[TreeNode]) ->
Vec[i64]` over a `shared struct TreeNode`, and returns the sums in any
order, as the problem allows.

| file | mechanism |
|---|---|
| `find_frequent_tree_sum.kara` ★ | one post-order walk: a node's sum is its value plus its two subtrees' sums, counted in a `Map[i64, i64]` with `*counts.entry(sum).or_insert(0) += 1` on the way back up; then the largest count, and every sum that has it, by two `for (s, c) in counts.iter()` loops. O(n) |
| `find_frequent_tree_sum_sorted.kara` | the same walk pushes every sum onto a `Vec`, which is sorted; then the runs of equal sums, a run longer than the best so far starting the answer over and one as long joining it. No table. O(n log n) |
| `find_frequent_tree_sum_levels.kara` | no recursion: the nodes breadth first in a `Vec`, each with its parent's index, then a walk from the back, which meets every node after all its descendants and adds its finished sum into its parent's. The sums are counted in a `SortedMap`, and two iterator chains (`map` and `max`, then `filter` and `map`) give the answer. O(n log n) |
| `find_frequent_tree_sum_stack.kara` | no recursion: post-order on a stack of `(Option[TreeNode], bool)`, each finished subtree pushing its sum onto a second stack and an empty child 0. Counts go in a `Map` by `match counts.get(sum)` and `insert`, and the answer is kept as they grow. O(n) |
| `differential.kara` | the four arms on 1,500 random trees, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, one
node, a tree of seven whose sums all differ, a tree of zeros, a chain,
the extremes, a tree whose sums cancel, and for 300 random trees (1 to
40 nodes, the values from -2 to 2, from -50 to 50, or from -10^5 to
10^5 in turn) the count of nodes, of most frequent sums and a checksum
of those, sorted. The trees are given in LeetCode's level order, built
by the harness. `find_frequent_tree_sum.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random trees of 1 to 30 nodes, the values from -2 to 2, from -50
to 50, or from -10^5 to 10^5 in turn, each new node hung at the end of
a random walk down from the root. The answers are sorted before they
are compared.

| | property |
|---|---|
| P1 | the sums are the reference's, which adds up the subtree of every node by its own walk and counts each sum by scanning the list |
| P2 | the mirror image of the tree has the same sums |
| P3 | every value negated negates the sums |
| P4 | every value times 3 triples the sums |
| P5 | two copies of the tree under a new root of 10^9 have the same sums: every sum turns up twice as often, and the root's own sum is far from all of them |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right subtree is left out of a sum | P1 1374, P2 1382, P3 1374, P4 1374, P5 1449 |
| M2 | ★: the sums seen once are the answer (`*c == 1`) | P1 708, P2 708, P3 708, P4 708, P5 1500 |
| M3 | sorted: a longer run does not start the answer over | P1 664, P2 664, P3 636, P4 664, P5 664 |
| M4 | sorted: the sums are not sorted | P1 539, P2 532, P3 539, P4 539, P5 1434 |
| M5 | levels: a child hands up its own value, not its sum | P1 1124, P2 1124, P3 1124, P4 1124, P5 1124 |
| M6 | levels: the root is not counted (`while i > 0`) | P1 884, P2 884, P3 884, P4 884 |
| M7 | stack: an empty child counts 1 | P1 1488, P2 1488, P3 1495, P4 1499, P5 1488 |
| M8 | stack: the right child is walked twice and the left never | P1 1329, P2 1337, P3 1329, P4 1329, P5 1329 |
| E1 | sorted: a run grows while a sum equals the one before it, not the run's first | 0 |
| E2 | levels: the root's parent is -2, not -1 | 0 |
| E3 | stack: a sum seen the first time counts 0, not 1 | 0 |
| E4 | ★: the best count is taken with `>=` | 0 |

E1 is equivalent because inside a run every sum equals the first. E2
is equivalent because the walk asks only whether a parent index is
below 0. E3 is equivalent because counting every sum one lower keeps
their order, and a first sum still joins the empty answer (0 is the
starting best, so it is equal rather than greater). E4 is equivalent
because the largest count is the same however ties are taken.

M2 is right only where every sum is seen once, and P5 sees it in
every case: in two copies of a tree every sum is seen at least twice
except the new root's, so M2 answers with that one. M6 loses only the
root's sum, which matters when it is among the answer, and so P5,
whose root's sum never is, cannot see it. M3 keeps the shorter runs
that come before the longest one in sorted order; negating the values
reverses that order, so P3 fails on a different set of cases, here a
smaller one. M4 counts only the
runs of equal sums that happen to sit next to each other in post-order,
and fails P5 nearly always, where the second copy of every sum comes
a whole tree later. M1, M5, M7 and M8 give wrong sums, and every
property sees them.

## Verification

All four arms print the same output as `find_frequent_tree_sum.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints `30000 checks, 0 failures` on both and
runs clean under the third. `karac check` passes on every file, the
bench program included.

On the frozen legacy backends only the sorted arm runs, and only under
`karac run --interp`, which prints the same output. LLJIT and legacy
`karac build` fail on it at codegen ("Module verification failed: Call
parameter type does not match function signature!", at the harness's
calls to `show`, whose first parameter is a `Str` given a string
literal, as on kata 501). Legacy refuses the other three arms, the
differential and the bench program at type checking, all with "unary
'*' requires 'ref T' ... found 'i64'": it types a `Map`'s or
`SortedMap`'s `iter()` items and `get` result by value, so the `*c`
and `*s` in the ★, levels and stack arms are refused, and with them
the differential's `*s` over `want.iter()`. Legacy is frozen, so these
are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random trees of 10,000
nodes (the problem's most), the values from -2 to 2, from -50 to 50,
or from -10^5 to 10^5 in turn, each tree a random root over its list
of values with the values before it on the left and those after it on
the right, once. Then it solves each 30 times, adding up the count and
the total of the sums returned, which does not depend on their order.
Every implementation prints `100 trees of 10000 nodes, 30 times each:
6720 most frequent sums, adding up to -418998330`, the Kāra program
under `karac __mir-run` included (in 111 s).

Every mirror counts into a fresh hash table for every call, as the ★
arm counts into `Map.new()`, and returns a fresh array: Rust a std
`HashMap` (SipHash, as Kāra's `Map`) over `Rc<RefCell<TreeNode>>`, the
closest match to a `shared struct`, Go a `map`, Python a `dict`, and C
an open-addressing table it writes itself, grown by doubling. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.81 to 1.86 s |
| Rust (`rustc -O`) | 2.45 to 2.55 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.45 to 2.71 s |
| Go | 1.84 to 1.91 s |
| Python | 8.8 to 9.7 s |
| Kāra (`karac build --mir`) | 2.11 to 2.24 s |

The legacy `karac build` refuses this program at type checking (see
Verification). So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`10fdedabfc`. Under `karac __mir-llvm-run` the program prints the same
line in 12.1 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
