# 2892. Minimizing Array After Replacing Pairs With Their Product

Given an integer array `nums` and an integer `k`, you can perform the
following operation on the array any number of times:

- Select two **adjacent** elements of the array like `x` and `y`, such
  that `x * y <= k`, and replace both of them with a **single element**
  with value `x * y` (e.g. in one operation the array `[1, 2, 2, 3]`
  with `k = 5` can become `[1, 4, 3]` or `[2, 2, 3]`, but can't become
  `[1, 2, 6]`).

Return *the **minimum** possible length of* `nums` *after any number of
operations*.

```
nums = [2,3,3,7,3,5], k = 20  ->  3
nums = [3,3,3,3],     k = 6   ->  4
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^9`;
`1 <= k <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `product.kara` ★ | a 0 swallows everything, each neighbour in turn, so an array holding one leaves 1. Otherwise every value is at least 1, so a run can be merged into one exactly when its product is at most k, and greedily, left to right, each value joins the run before it while the product stays within k, and starts a new run when it would not |
| `product_window.kara` | dynamic programming over where the last run starts: the fewest runs for the first i values is one more than for the first j, the earliest start whose run up to i has product at most k, since the fewest runs never falls as the prefix grows. That start only moves right, so a sliding window keeps the run's product, dividing values out as it leaves them |
| `product_fold.kara` | the ★ arm's greedy pass as one `fold` over (runs, product), started at k + 1 so that the first value joins nothing; the 0 found by `any` |
| `product_stack.kara` | the merges done as the statement does them, on a stack of what is left: each value pushed, then the two on top replaced by their product while it is at most k. A 0 needs no case of its own: it merges with what is under it, and the 0 left merges with everything after |
| `product_solution.kara` | a Rust solution as LeetCode's Rust users write it: `nums.contains(&0)` first, then the greedy pass over `&nums[1..]` in `i64`, `k` shadowed as one, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The greedy was checked first against an exhaustive search in Python
over 3000 random arrays of up to 7 values with 0s, before any arm was
written.

Every arm prints the same 4 lines: LeetCode's two examples; 10^5 values,
LeetCode's most: all 1 with k 1, all 10^9 with k 10^9, and all 2 with k
2^30; then 3000 random arrays of 1 to 8 values from 1 to 6, k 1 to 40,
one in fifteen with a 0, and 100 of 1000 to 10^5 values, half 1 and the
rest up to 1000, k up to 10^9, one in ten with a 0, as a total of the
answers and a checksum. `product.py` mirrors the ★ arm and its output is
byte-identical.

```
3 4
1 100000 3334
3000 short arrays: lengths total 7611, checksum 51518594
100 long arrays: lengths total 805976, checksum 363146076
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every neighbouring pair whose product is at most k
tried as the next replacement, a search over the arrays that can be
left, each seen once, kept in a `Map[String, i64]` by its values written
out, to the shortest. It draws 2000 random arrays of 1 to 7 values from
0 to 6, one in five allowed 0s, k 1 to 40, then 50 of up to 3000 values,
half 1 and the rest up to 1000, k up to 10^9, one in ten with a 0, all
before any arm answers; the literal reading is asked only of the first
2000.

| | property |
|---|---|
| P1 | up to 7 values, the answer is the literal reading's |
| P2 | the array reversed: the same answer |
| P3 | the array twice over: from the answer to twice it |
| P4 | k doubled: no more than the answer |
| P5 | from 1 to n; 1 when a 0 is held, n when no neighbours' product is at most k |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, lengths total 18005: checksum
839187466, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python search over the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, three to the ★ arm, two each to the
window, the fold and the stack, and one to the solution, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run's product kept below k, not at most k | P1 92, P6 92 |
| M2 | ★: a new run's product started at 1 | P1 547, P2 60, P5 128, P6 592 |
| M3 | ★: no 0 looked for | P1 34, P2 72, P5 38, P6 38 |
| M4 | window: a run of product k shrunk too | P1 92, P6 92 |
| M5 | window: the run taken as the last value alone | P1 1271, P6 1316 |
| M6 | fold: the first value able to join nothing only above k | P1 81, P2 44, P3 19, P5 77, P6 81 |
| M7 | fold: a new run starting from the old product | P1 1271, P6 1316 |
| M8 | stack: a merge keeping only the top | P1 835, P2 318, P5 28, P6 880 |
| M9 | stack: one merge per value pushed | P1 34, P2 72, P5 38, P6 38 |
| M10 | solution: values summed, not multiplied | P1 642, P2 209, P5 93, P6 687 |

## Benchmarks

The bench draws 50 arrays of 10^5 values, LeetCode's most, half of them
1 and the rest up to 1000, k up to 10^9, one in ten with a 0 near its
end, all first, then answers each 20 times by the ★ arm in all five
languages. Every implementation prints `50 arrays of 100000, 20 rounds:
lengths total 15910800, checksum 276828660`.

BENCHTAB

## Verification

All five arms print the same output as `product.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written, `nums.contains(0)` on
a borrowed `Vec[i64]` and a `fold` whose closure returns a tuple from an
`if` among them.

LeetCode's Rust template took 11 `karac fix` edits over two runs, the
wrapper included: `struct Solution {}` came for the `impl`; `Vec<..>`
became `Vec[..]` in both signatures; `nums.contains(&0)` lost its `&`;
`for &x in &nums[1..]` became `for x in nums[1..]`; the wrapper's `|&x|`
lost its `&`, its `as i64` on the `i32` result went, and `Solution::`
took `.`. The shadowing `let k = k as i64;` and `let x = x as i64;` were
accepted as written.
