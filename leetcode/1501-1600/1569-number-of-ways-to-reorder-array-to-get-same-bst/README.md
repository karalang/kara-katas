# 1569. Number of Ways to Reorder Array to Get Same BST

Given an array `nums` that represents a permutation of integers from `1`
to `n`, we construct a binary search tree by inserting the elements of
`nums` in order into an initially empty BST. Find the number of different
ways to reorder `nums` so that the constructed BST is identical to that
formed from the original array `nums`. Return the number of ways, other
than the original, modulo `10^9 + 7`.

```
nums = [2,1,3]       ->  1
nums = [3,4,5,1,2]   ->  5
nums = [1,2,3]       ->  0
```

**Constraints:** `1 <= nums.length <= 1000`; `nums` is a permutation of
`1` to `nums.length`.

## Approaches

An order gives the same tree exactly when it starts with the root, and
the values on each side, read in that order, give the same subtree: the
two sides may interleave in any way.

| file | mechanism |
|---|---|
| `ways.kara` ★ | the ways to interleave the two sides, a binomial from Pascal's triangle, times each side's own count, by recursion on the values `filter`ed to each side. O(n^2) |
| `ways_tree.kara` | the tree built in an arena of `Node`s by walking down from the root, each subtree's size summed child into parent in reverse insertion order, and the count the product over the nodes of their binomials, from factorials and their inverses by Fermat. O(n h) for a tree of height h |
| `ways_hook.kara` | the hook length formula for trees: the orders with every node before its subtree number n! over the product of the subtree sizes. The tree is never built: a value's parent is whichever of its neighbours among the values before it, in a `SortedMap` from value to position, came later. O(n log n) |
| `ways_solution.kara` | LeetCode's Rust template (`num_of_ways(nums: Vec<i32>) -> i32`, the ★ arm with its recursion a function nested in the method and a block-level `const MOD`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples, then
`[1]`, two small trees, a chain under a root, a full tree of 20 values,
and 1000 values that make two chains under 500 (the binomial 999 choose
499); then the count with no other order and a checksum for 3000 random
permutations of up to 8 values, 300 of up to 100 and 30 of up to 1000.
`ways.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every order of the values, each put into a tree by insertion
and written as each value's parent, the orders other than `nums` with
the same parents counted. It checks 3000 permutations of 1 to n for n
from 1 to 6, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is below `10^9 + 7`, and 0 with at most two values |
| P3 | every value `x` turned into `n + 1 - x` leaves the answer |
| P4 | the root, then the smaller values, then the larger, each in their order, leaves the answer |
| P5 | every value moved up by one and `1` put first leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 71159558, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M1 ended the ★ recursion at one value rather than two, which
is the same count (two values have one order), and the first M5 summed
the tree arm's sizes parent first, which stopped on an index out of
bounds rather than a property; both were replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: up to three values taken to have one order | P1 492, P6 492 |
| M2 | ★: the binomial taken from the row below | P1 1792, P3 1725, P6 1792 |
| M3 | ★: Pascal's rule adding 1 for the entry above | P1 1299, P3 1725, P6 1299 |
| M4 | tree: the binomial's second factorial dropped | P1 1255, P3 1731, P5 2490, P6 1255 |
| M5 | tree: a node's own value counted among those below it | P1 2149, P2 253, P3 2257, P6 2149 |
| M6 | tree: insertion walks the wrong way | P1 1523, P3 1824, P4 370, P5 1036, P6 1523 |
| M7 | hook: the parent the earlier neighbour | P1 1417, P5 1785, P6 1417 |
| M8 | hook: n! taken as (n - 1)! / 1 | P1 2490, P2 489, P5 3000, P6 2490 |
| M9 | template: the larger side skips one more value | P1 239, P3 480, P4 87, P5 1169, P6 239 |
| M10 | template: the original order counted | P1 3000, P2 999, P6 3000 |

## Benchmarks

The bench builds 20 permutations of 1 to 1000 once and makes 15 passes,
each swapping two values of every permutation and asking it by the ★
arm, in all five languages. Every call builds its own triangle of
1001 by 1001 and a list of values for each side at every node. Every
implementation prints `15 passes over 20 permutations of 1000 values:
ways sum 769017594, checksum 437224495`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.285 s |
| Rust (`rustc -O`) | 0.435 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.467 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.493 s |
| Kāra (`karac build`) | 0.495 s |
| Go | 1.198 s |
| Python | 22.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.46 s and 0.47 s on one run).

Kāra is 1.06x Rust under overflow checks by median. Not traced. The
triangle is half a million additions and remainders a call, which every
language but C fills row by row through a vector of vectors; C's rows
come from `calloc`, which hands back pages already zeroed.

## Verification

All four arms print the same output as `ways.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★ and tree arms were written in Kāra and checked as written. The
hook arm was first written with Rust's one-ended ranges,
`seen.range(..x).next_back()` and `seen.range(x + 1..).next()`;
`karac fix` rewrote them to `range(i64.MIN, x)` and
`range_inclusive(x + 1, i64.MAX)` in one round.

The Rust template took six rounds of `karac fix`, 9 changed lines, then
the nested function moved out, then 1 added, then 3, 1 and 1 changed:

1. the `Vec<..>` types to `Vec[..]`, `&[i32]` to `Slice[i32]`,
   `&Vec<..>` to `ref`, the `&left`, `&right`, `&nums` and `&comb`
   arguments bare, `|&&x|` and `|&x|` to `|x|`, and `Solution::` to
   `Solution.`;
2. the `fn dfs` nested in the method moved out to the top level, ahead of
   the `impl`;
3. `struct Solution {}` added;
4. `dfs`'s `ref` on `comb` dropped as redundant, the `0i64` suffix
   dropped as the default, and the wrapper's `as i64` dropped (an `i32`
   widens);
5. the inner `vec![..]` to `Vec.filled`;
6. the outer one.

The block-level `const MOD` and the `1_000_000_007` literals were taken
as written. It checks and agrees with no hand edit.
