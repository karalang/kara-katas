# 2826. Sorting Three Groups

You are given an integer array `nums`. Each element in `nums` is 1, 2
or 3. In each operation, you can remove an element from `nums`. Return
the **minimum** number of operations to make `nums` **non-decreasing**.

```
nums = [2,1,3,2,1]    ->  3
nums = [1,3,2,1,3,3]  ->  2
nums = [2,2,2,2,3,3]  ->  0
```

**Constraints:** `1 <= nums.length <= 100`; `1 <= nums[i] <= 3`.

## Approaches

The fewest removals leave the longest non-decreasing subsequence, and
with only three values it is some 1s, then 2s, then 3s.

| file | mechanism |
|---|---|
| `groups.kara` ★ | a three-entry table of the most numbers kept so far ending at a value at most v; each number adds one to its own entry and carries it up to the higher ones |
| `groups_tails.kara` | patience tails for the longest non-decreasing subsequence: each number replaces the first tail above it, found by `partition_point`, or extends the tails |
| `groups_cuts.kara` | two cuts: with counts of each value in every prefix, in a `Vec` of `Array[i64, 3]`, every pair of cuts i <= j tried, 1s kept before the first, 2s between, 3s after; O(n^2) |
| `groups_fold.kara` | the fewest removals for an array ending in a 1, at most a 2 and at most a 3, a tuple carried through `fold` |
| `groups_solution.kara` | a Rust solution as LeetCode's Rust users write it: `f = [0; 3]` of the fewest removals ending in each group, each number building a fresh `g` from `f[..=j].iter().min()` and the cost of `x`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; one
number; 100 numbers falling 3, 2, 1 in runs of 34, 33 and 33; 100
rising in the same runs; and 5000 random arrays of 1 to 100 numbers
from 1 to 3, as a total and a checksum. `groups.py` mirrors the ★ arm
and its output is byte-identical.

```
3
2
0
0
66
0
5000 arrays: 134734 removals, checksum 167342385
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every set of numbers removed, by a bit mask, kept when
what is left is non-decreasing by `windows(2)`, and the fewest removed.
It draws 2000 random arrays of 1 to 12 numbers from 1 to 3, then 50 of
up to 500, all before any arm answers; the literal reading is asked
only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 numbers, the answer is the literal reading's |
| P2 | every v as 4 - v and the order reversed: the same answer |
| P3 | a 3 put at the end: the same answer |
| P4 | a 1 put at the front: the same answer |
| P5 | the numbers kept are at least the count of the commonest value, and at most all of them |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 892669730, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Not run yet. On the karac release this batch was checked with
(`684b860a5`), the mutation runner stopped on a compiler crash before
any verdict; the table comes with a run on a newer build.

## Benchmarks

The bench draws 200000 arrays of 100 numbers from 1 to 3, LeetCode's
most, all of them first, then answers each 5 times by the ★ arm in all
five languages. Every implementation prints `200000 arrays of 100, 5
rounds: 56420200 removals, checksum 419017036`.

BENCHTAB

## Verification

All five arms print the same output as `groups.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the four own arms checked clean as first written. The cuts
arm wrote its prefix counts as `Vec[[i64; 3]]`, Rust's array type, and
`karac check` reported E0001, naming `Array[T, N]`; `karac fix` made it
`Vec[Array[i64, 3]]`. The differential's literal reading first called
`.all` on `windows(2)`, which returns a `Vec`, and `karac check`
reported E0236; `karac fix` added the `.into_iter()`.

LeetCode's Rust template took 9 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `for &x` and `|&v|` lost their `&`; `Solution::`
took `.`; and the wrapper's `as i64` went. `[0; 3]` stays, a fixed
`Array` in Kāra as in Rust, and so do `x as usize` and the `*` on
`min().unwrap()`.

Before kara 0d28296389 the template stopped at E0200: `f = [0; 3]`'s
literal settled to `i64` where `g[j] = best + if .. { 0 } else { 1 }`
stored an arithmetic result, and the `i32` return then narrowed it;
`karac fix` offered `0i32`. Design.md §8 says an assignment fixes a
literal's type, so the store keeps it open and the return makes it
`i32`; this was B-2026-11-21-201, found writing 2812, and the fix covers
both.
