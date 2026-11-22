# 2835. Minimum Operations to Form Subsequence With Target Sum

You are given a **0-indexed** array `nums` consisting of
**non-negative** powers of `2`, and an integer `target`.

In one operation, you must apply the following changes to the array:

- Choose any element of the array `nums[i]` such that `nums[i] > 1`.
- Remove `nums[i]` from the array.
- Add **two** occurrences of `nums[i] / 2` to the **end** of `nums`.

Return the ***minimum number of operations** you need to perform so
that* `nums` *contains a **subsequence** whose elements sum to*
`target`. If it is impossible to obtain such a subsequence, return
`-1`.

A **subsequence** is an array that can be derived from another array by
deleting some or no elements without changing the order of the
remaining elements.

```
nums = [1,2,8], target = 7     ->  1
nums = [1,32,1,2], target = 12  ->  2
nums = [1,32,1], target = 35    ->  -1
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i] <= 2^30`;
`nums` consists only of non-negative powers of two; `1 <= target <
2^31`.

## Approaches

| file | mechanism |
|---|---|
| `ops.kara` ★ | counts by size through `trailing_zeros()`, low bit to high: a bit the target needs takes a power of its own size when there is one, else the nearest larger power is split down to it, one operation a level, leaving one of each size between; what is left at each size pairs up into the next |
| `ops_heap.kara` | largest first, from a `PriorityQueue.max_first()`: a power no larger than what is left of the target is taken, one the rest can do without is thrown away, any other is split in two |
| `ops_buckets.kara` | the largest-first rule over buckets by size, high to low, with no queue: a whole bucket's powers are taken, thrown away or split at once |
| `ops_carry.kara` | by recursion over the bits: each call settles one bit with the counts it owns (`own Vec[i64]`), sizes found by doubling rather than `trailing_zeros()`, and carries the unused ones up as pairs to the next call |
| `ops_solution.kara` | a Rust solution as LeetCode's Rust users write it: an `i64` sum checked first, a `[0i64; 32]` count by `trailing_zeros() as usize`, and the low-to-high walk with a `while` over the larger counts, the answer as `i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's three examples; a target
met as it stands; one 2^30 split down to 1; 1000 ones and 1000 of
2^30, LeetCode's most, against 2^31 - 1; then 3000 random arrays of 1
to 8 powers up to 2^5 with targets up to 64, and 300 of up to 1000
powers up to 2^30 with targets below 2^31, as a count out of reach and
a checksum. `ops.py` mirrors the ★ arm and its output is
byte-identical.

```
1 2 -1
0 30
-1 30
3000 short arrays: 1140 out of reach, checksum 202348041
300 long arrays: 5 out of reach, checksum 533131438
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: a breadth-first search over the arrays the operations
can make, each kept as a count of every size and seen once, from no
operation up, until one holds a subsequence summing to the target,
found by a subset-sum bitset. It draws 2000 random arrays of 1 to 5
powers up to 2^3 with targets up to 24, then 50 of up to 1000 powers
up to 2^29 with targets below 2^30, so that P3's doubling stays in
`i32` for the Rust solution; all are drawn before any arm answers, and
the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 5 powers of at most 8, the answer is the literal reading's |
| P2 | the powers reversed: the same answer |
| P3 | every power and the target doubled: the same answer |
| P4 | the target's own bits added as powers: no operation |
| P5 | -1 exactly when the powers sum to less than the target |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 150740583, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Nine are killed, each the same
way under both backends. M6 survives and is equivalent: after the powers
that fit are taken and the ones the rest can spare are thrown away, at
most one is left in a bucket, since what is left is below that power, so
a split counted once is a split counted per power.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the split counted as one operation | P1 123, P6 124 |
| M2 | ★: no pairs carried up | killed under both: runtime error: index out of bounds |
| M3 | heap: a power the rest can do without split anyway | P1 207, P4 557, P6 208 |
| M4 | heap: a split power left one half short | killed under both: runtime error: called unwrap() on None |
| M5 | buckets: none thrown away | killed under both: runtime error: index out of bounds |
| M6 | buckets: a split counted for the bucket, not each power | survives: equivalent (above) |
| M7 | carry: the split counted one short | P1 376, P6 378 |
| M8 | carry: the carry made by threes | killed under both: runtime error: index out of bounds |
| M9 | solution: a power filed one size up | P1 662, P4 1475, P6 689 |
| M10 | solution: the operations never counted | P1 376, P6 378 |

## Benchmarks

The bench draws 2000 arrays of 1000 powers, LeetCode's most, from 2^16
to 2^30, so that a target below 2^31 has low bits to split for (with
powers from 2^0 every size is present and no array needs an
operation), all of them first, then answers each 200 times by the ★
arm in all five languages. Every implementation prints `2000 arrays of
1000, 200 rounds: operations total 6005600, checksum 640596123`.

BENCHTAB

## Verification

All five arms print the same output as `ops.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 14 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `|&x|`, `for &x in &nums` and `|&v|` lost their `&`,
the loop becoming `for x in ref nums`; `target as i64` lost its cast,
an `i32` widening; `[0i64; 32]` lost its suffix, `i64` being the
default (the `redundant_suffix` lint); `let mut ans = 0` took `: i32`,
which the `ans += (j - i) as i32` and the `i32` return want;
`Solution::` took `.`, and the wrapper's `as i64` went. The index
`cnt[x.trailing_zeros() as usize]` was accepted as written, `usize`
being a Kāra type.
