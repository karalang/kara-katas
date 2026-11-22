# 2809. Minimum Time to Make Array Sum At Most x

You are given two **0-indexed** integer arrays `nums1` and `nums2` of
equal length. Every second, for all indices `0 <= i < nums1.length`,
value of `nums1[i]` is incremented by `nums2[i]`. **After** this is
done, you can do the following operation:

- Choose an index `0 <= i < nums1.length` and make `nums1[i] = 0`.

You are also given an integer `x`.

Return *the **minimum** time in which you can make the sum of all
elements of* `nums1` *to be **less than or equal** to* `x`, *or* `-1`
*if this is not possible.*

```
nums1 = [1, 2, 3], nums2 = [1, 2, 3], x = 4   ->  3
nums1 = [1, 2, 3], nums2 = [3, 3, 3], x = 4   ->  -1
```

**Constraints:** `1 <= nums1.length <= 10^3`; `1 <= nums1[i] <= 10^3`;
`0 <= nums2[i] <= 10^3`; `nums1.length == nums2.length`; `0 <= x <=
10^6`.

## Approaches

After t seconds the sum is sum1 + t * sum2, less what the t resets
saved; resetting index i at the j-th second saves nums1[i] + j *
nums2[i], so no index is worth resetting twice, and among the indices
chosen the larger nums2 go later. Over the pairs sorted by nums2, a
knapsack finds the most j resets can save for every j, and the answer
is the least t whose sum is at most x, or -1. The harness and the
differential use 0 in nums1 too, which the arms all allow.

| file | mechanism |
|---|---|
| `time.kara` ★ | the `(nums2, nums1)` pairs zipped and sorted, `best[j]` updated from the top over each pair so that it is taken once, then a scan for t |
| `time_table.kara` | the whole table `saved[i][j]` over the first i pairs, the order an index `Vec` sorted by `sort_by_key`, and t by `find` over `0..=n` with `unwrap_or(-1)` |
| `time_memo.kara` | top down: `most(i, j)` by memoized recursion, a pair left or reset j-th, too few pairs unreachable |
| `time_rows.kara` | forward rows: the pairs sorted by nums2 alone with `sort_by` and a `cmp`, a fresh row made from the last for each pair, unreachable counts kept apart |
| `time_solution.kara` | a Rust solution as LeetCode's Rust users write it, `zip` of `cloned()` iterators, `sort_unstable_by_key`, a `vec![0i64; n + 1]` knapsack and casts to `i64`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; nothing to
do; 1000 pairs, LeetCode's most, nums1 at its largest with nums2 all
1, and counting up with nums2 0 and x 0; 3000 random cases of 1 to 6
pairs up to 10 with x up to 40; and 30 of up to 1000 pairs up to 1000
with x up to 10^6, the last two with the sum of the times and a
checksum. `time.py` mirrors the ★ arm and its output is byte-identical.

```
3
-1
0
894
1000
3000 small cases: times sum to -2, checksum 172977781
30 large cases: times sum to -5, checksum 50502356
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every sequence of choices for 0, 1, 2 and more seconds,
played out on a copy of nums1, each second adding nums2 and then zeroing
the index chosen, until one ends with a sum at most x; no sorting and no
knapsack. It stops at n + 1 seconds, since a reset after the n-th is
never needed. It draws 2000 random cases of 1 to 4 pairs up to 10 with x
up to 40, then 50 of up to 300 pairs up to 1000 with x up to 10^6, all
before any arm answers; the literal reading is asked only of the first
2000. The large cases stop at 300 pairs so that the interpreter lane,
where the memo arm's table is filled for each of six questions per
case, runs in under half a minute; the harness covers 1000.

| | property |
|---|---|
| P1 | up to 4 pairs, the time is the literal reading's |
| P2 | -1 or from 0 to n |
| P3 | x 1000 more: a time, and no later one, when there was a time |
| P4 | the pairs given in reverse: the same time |
| P5 | x the sum of nums1: 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 128771177, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pairs left in their given order | P1 92, P4 99, P6 92 |
| M2 | ★: the knapsack run upward, a pair taken more than once | P1 265, P6 266 |
| M3 | table: the j-th reset saving nums2 once, not j times | P1 170, P6 170 |
| M4 | table: the order sorted by nums1 | P1 109, P4 16, P6 109 |
| M5 | memo: the value stored the leave alone | P1 48, P6 48 |
| M6 | memo: the j-th reset saving nums2 only j - 1 times | P1 265, P6 265 |
| M7 | rows: the pairs sorted by nums2 from the largest | P1 145, P6 145 |
| M8 | rows: the j-th reset saving nums2 j + 1 times | P1 459, P6 459 |
| M9 | solution: the scan stopping one short of n | P1 175, P6 175 |
| M10 | solution: the time's growth left out of the sum | P1 486, P6 490 |

## Benchmarks

The bench draws 20 cases of 1000 pairs, LeetCode's most, nums1 up to
1000 and nums2 up to 2, with x from 3 * 10^5 to 5 * 10^5 so that most
answers fall inside n, all of them first, then answers each 20 times by
the ★ arm in all five languages; C sorts its pairs with `qsort` on
(nums2, nums1), the order the tuples sort in elsewhere. Every
implementation prints `20 cases of 1000 pairs, 20 rounds: times sum to
203480, checksum 313211135`.

BENCHTAB

## Verification

All five arms print the same output as `time.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the harness checked clean as first written.

LeetCode's Rust template took 31 `karac fix` edits, the wrapper
included: `Vec<..>` took `[..]`; `vec![0i64; n + 1]` became
`Vec.filled(n + 1, 0)`; `sort_unstable_by_key` became `sort_by_key`;
the `&(a, b)`, `&(_, b)`, `&a`, `&b` and `&v` patterns lost their `&`;
the casts `as i64` on `i32` and on `usize` values went, `usize` being
`i64` here and an `i32` widening to `i64` by itself in mixed arithmetic
(design.md §5); `struct Solution {}` was added; and `Solution::` became
`Solution.`, the wrapper's `as i64` dropped. The narrowing casts `as
i32` stay.
