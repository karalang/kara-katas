# 2369. Check if There is a Valid Partition For The Array

You are given a **0-indexed** integer array `nums`. You have to
partition the array into one or more **contiguous** subarrays.

We call a partition of the array **valid** if each of the obtained
subarrays satisfies **one** of the following conditions:

1. The subarray consists of **exactly** `2` equal elements. For
   example, the subarray `[2,2]` is good.
2. The subarray consists of **exactly** `3` equal elements. For
   example, the subarray `[4,4,4]` is good.
3. The subarray consists of **exactly** `3` consecutive increasing
   elements, that is, the difference between adjacent elements is `1`.
   For example, the subarray `[3,4,5]` is good, but the subarray
   `[1,3,5]` is not.

Return `true` *if the array has **at least** one valid partition*.
Otherwise, return `false`.

```
nums = [4,4,4,5,6]  ->  true
nums = [1,1,1,2]    ->  false
```

**Constraints:** `2 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^6`.

The first `i` values split when the last block before `i`, of two or
three values, is valid and the values before that block split too, so
whether each prefix splits follows from the two and three before it.

## Approaches

| file | mechanism |
|---|---|
| `partition.kara` ★ | `good[i]` for each prefix, from `good[i - 2]` and a pair or `good[i - 3]` and a valid three. O(n) |
| `partition_rolling.kara` | the same recurrence kept in three flags, rolled on by one at each value. O(n), no table |
| `partition_memo.kara` | top down: the values from place `i` split when a valid block starts there and the values after it split, by recursion with a memo; up to `5 * 10^4` deep on the long lines |
| `partition_push.kara` | forward: from each place the values before split, the valid blocks starting there mark the places they reach, and the answer is whether the end is marked. O(n) |
| `partition_iter.kara` | iterators: the values folded into the last two values and the three flags |
| `partition_solution.kara` | LeetCode's Rust template: a table over `1..=n` of `usize` places, each block guarded by `i >= 2` or `i >= 3`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; two values;
`10^5` equal values; 99999 and `10^5` values rising by one; 99999
values in rising threes from `10^6` down; then 3000 arrays of 2 to 30
values built from random blocks, each two or three equal values or
three rising, a third of them with one value then raised by one, with a
checksum and how many are valid. `partition.py` mirrors the ★ arm and
its output is byte-identical, and the mirror was checked on 3000 random
arrays of 2 to 12 values from 1 to 4 against trying every way to cut
them.

`check` first reports 9 errors on the template, and `karac fix`
carries it in one call, reporting 11 edits: `struct Solution;` given its
braces, `Vec<i32>` its brackets, `vec![false; n + 1]` written
`Vec.filled(n + 1, false)`, each `&&` written `and` and the `||`
written `or`, and `Solution::` written with a dot. The `1..=n` range,
the `let (a, b, c) = (..)` binding and the `usize` length stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way of cutting the array into contiguous pieces, one
cut mask of `n - 1` bits at a time, and the array valid when some way
leaves every piece a valid block. No recurrence. It checks 300 arrays of
2 to 16 values built from random blocks, a third of them with one value
then raised by one; then 30 of up to 2000 values built the same way;
then 30 of up to 16 values built from blocks some of which are three
falling values or three rising by two, which look valid and are not.
All 360 are drawn before any arm answers, and the literal reading
answers the 330 of them with at most 16 values.

| | property |
|---|---|
| P1 | up to 16 values, the answer is the literal reading's |
| P2 | an array built from valid blocks and left unchanged: valid |
| P3 | every value `x` written `10^6 + 1 - x`, in reverse order: the same answer |
| P4 | a pair of `10^6` put in front: the same answer |
| P5 | the array written twice: valid when it is |
| P6 | each arm agrees with at least three of the other five |

P3 holds because reversing a block of three rising values and turning
each value around leaves it rising, and equal values stay equal. P4
holds because the pair can only stand as its own block: no value of a
case reaches `10^6`, so no block of three can take it. P5 holds because
two valid partitions laid end to end make one.

The differential prints `360 cases: checksum 309124458, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every cut mask. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a falling three taken as a block | P1 6, P6 6 |
| M2 | ★: three equal values never a block | P1 155, P2 174, P6 175 |
| M5 | ★: any rising three taken as a block | P1 26, P6 30 |
| M7 | rolling: the flags rolled by two | P1 206, P2 224, P3 3, P6 226 |
| M9 | rolling: a pair asking about the place one back | P1 143, P2 162, P3 11, P4 72, P6 163 |
| M10 | rolling: a rising three taken by its ends alone | P1 11, P6 12 |
| M12 | memo: every place stored as splitting | P1 6, P3 14, P6 14 |
| M13 | memo: a block of three never ending the array | P1 151, P2 164, P3 106, P6 165 |
| M15 | memo: the third value equal to the second | P1 168, P2 185, P3 6, P6 188 |
| M17 | push: every place a start | P1 76, P3 53, P6 86 |
| M18 | push: a pair moving on one place | P1 138, P2 155, P3 11, P4 79, P6 158 |
| M19 | push: the last two places never a start | P1 54, P2 56, P3 97, P6 57 |
| M22 | iter: three with only two of them equal | P1 42, P4 1, P6 46 |
| M23 | iter: the last two values rolled in the wrong order | P1 215, P2 233, P6 235 |
| M26 | iter: a rising three needing only one step | P1 51, P6 61 |
| M28 | solution: a single value taken as splitting | P1 164, P2 166, P3 101, P4 77, P5 9, P6 178 |
| M29 | solution: a block of three not asking about the values before it | P1 59, P3 63, P6 69 |

P1 and P6 kill all seventeen, P3 ten, P2 nine, P4 four and P5 one.
P5, the array written twice, kills only the template's single value
taken as splitting (M28); every other edit still leaves a rule under
which two valid arrays laid end to end make a valid one.

The last 30 cases were first up to 300 values from 1 to 3 at random,
and then up to 16 of them. The ★ arm's falling three taken as a block
(M1) failed no check under either, since a random array is seldom
valid, and seldom by a falling three alone, so they became arrays built
from blocks of which some look valid and are not, and it fails P1 there.
The iter arm's three with only two of them equal (M22) stands where a
prefix of one value taken as splitting first stood: that flag is read
only beside values that cannot match the start, so the edit changed
nothing.

Of the thirty-one, fourteen were not kept. A block of three asking
about the place two back (M4) fails as the rolling arm's flags rolled
by two and block of three asking the pair's flag (M7, M11); the empty
prefix not splitting (M8), the iter arm's last two values in the wrong
order and pair and block both needed (M23, M25), and the template's
last place never filled (M27) answer false on every case, and fail
alike; a pair asking about the place one back fails alike in the
rolling, iter and template arms (M9, M24, M31); the last value allowed
left over (M6) as the memo's one value left at the end (M14); and the
memo's stored answer read inverted (M16) as every place stored as
splitting (M12). A pair not asking about the values before it (M3), the
push arm's third value one below the second and answer read one place
short (M20, M21), and the template's third value two above the second
(M30) fail apart from every kept one, and were left out to keep three
to an arm and two to the template.

## Verification

Every arm prints the same output as `partition.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.7 to 1.7 s, and the differential
9.4 s there and 0.85 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays once from the harness's generator, array `a`
holding about `10^5` values in random blocks with values up to
`4^(a + 1)`, and the odd ones with one value near the end then raised by
one, which leaves them invalid; then makes 20 passes, pass `p` folding
`a + 1` for a valid array and 0 for an invalid one, plus `p`, into the
checksum, with the ★ arm in all five languages. Every implementation
prints `20 passes over 10 arrays of about 10^5 values: checksum
112252226`. Every implementation builds its table of `n + 1` flags
afresh in each call.

BENCHTAB
