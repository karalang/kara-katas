# 2786. Visit Array Positions to Maximize Score

You are given a **0-indexed** integer array `nums` and a positive
integer `x`.

You are **initially** at position `0` in the array and you can visit
other positions according to the following rules:

- If you are currently in position `i`, then you can move to **any**
  position `j` such that `i < j`.
- For each position `i` that you visit, you get a score of `nums[i]`.
- If you move from a position `i` to a position `j` and the
  **parities** of `nums[i]` and `nums[j]` differ, then you lose a score
  of `x`.

Return *the **maximum** total score you can get*.

**Note** that initially you have `nums[0]` points.

```
nums = [2, 3, 6, 1, 9, 2], x = 5  ->  13
nums = [2, 4, 6, 8], x = 3        ->  20
```

**Constraints:** `2 <= nums.length <= 10^5`, `1 <= nums[i], x <= 10^6`.

## Approaches

The best walk ending on a number depends only on the best walks before
it that end on each parity.

| file | mechanism |
|---|---|
| `score.kara` ★ | the best score of a walk ending on an even number and on an odd one, a two-slot array indexed by `v % 2`; each number extends the better of its own parity's walk and the other's less x. O(n) |
| `score_suffix.kara` | from the end: the best walk starting at i is its number and the best walk on, from a later number of its parity or of the other less x, or nothing more; the best later walk of each parity kept as an `Option[i64]`, and the answer the walk from 0. O(n) |
| `score_fold.kara` | the ★ arm's two walks as one `fold` over the numbers after the first, its state the tuple (best ending even, best ending odd). O(n) |
| `score_table.kara` | the whole table: a `struct Row` per position with the best walk ending at or before it on each parity, `None` where there is none yet, each row made from the one before. O(n) |
| `score_solution.kara` | a Rust solution as LeetCode's Rust users write it, `dp = [i64::MIN / 2; 2]` indexed by `(v & 1) as usize`, each number after the first by `&nums[1..]` taking `dp[p].max(dp[p ^ 1] - x) + v as i64`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; an even
start before odd numbers worth less and more than x; `10^5` numbers of
`10^6`, LeetCode's most, alternating parity, with x = 1 and `x = 10^6`;
3000 random arrays of 2 to 12 numbers from 1 to 10 with x from 1 to 10;
and 20 of `10^5` numbers up to `10^6` with x up to `10^6`, the last two
with the sum of the scores and a checksum. `score.py` mirrors the ★ arm
and its output is byte-identical.

```
13
20
7
25
99999850001
50000000000
3000 small arrays: scores sum to 86982, checksum 120462794
20 arrays of 10^5: scores sum to 735078078992, checksum 129164944
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every walk from position 0 to later positions, each a subset
of the rest taken by the bits of a mask, scored as the sum of its
numbers less x for each step between parities, and the best kept; no
running best. It draws 2000 random arrays of 2 to 12 numbers from 1 to
10 with x from 1 to 10, then 50 of up to 2000 numbers up to `10^6` with
x up to `10^6`, all before any arm answers; the literal reading is asked
only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 numbers, the score is the literal reading's |
| P2 | x one more: no more, and no less than the score less n - 1 |
| P3 | a number put after: no less, and no more than the score plus it |
| P4 | `x = 10^6`, LeetCode's most, where the numbers sum to less: the sum of the numbers of the first one's parity |
| P5 | from the first number to the sum of all, and the sum when they are all of one parity |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 240440735, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same masks gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a change of parity never charged x | P1 1818, P4 1818, P6 1868 |
| M2 | ★: the first number taken as both parities | P1 936, P4 978, P6 962 |
| M3 | suffix: x charged for a walk on in the same parity | P1 1871, P4 1811, P5 182, P6 1921 |
| M4 | suffix: x charged twice for a change | P1 1212, P2 34, P6 1262 |
| M5 | fold: an odd number never reached from an even one | P1 791, P6 841 |
| M6 | fold: the first number counted twice | P1 2000, P4 2000, P5 686, P6 2050 |
| M7 | table: a change of parity from nothing of its own never charged | P1 1483, P4 1226, P6 1527 |
| M8 | table: an even row forgetting the odd walks | P1 509, P3 111, P4 917, P5 35, P6 559 |
| M9 | solution: x added for a change, not taken off | P1 1818, P2 1868, P3 2050, P4 1818, P5 1868, P6 1868 |
| M10 | solution: only walks ending on the first number's parity answered | P1 840, P3 462, P6 869 |

## Benchmarks

The bench draws 20 arrays of `10^5` numbers up to `10^6` with x up to
`10^6`, LeetCode's most, all of them first, then answers each 100 times
by the ★ arm in all five languages. Every implementation prints `20
arrays of 10^5, 100 rounds: scores sum to 76872711836000, checksum
843363694`.

BENCHTAB

## Verification

All five arms print the same output as `score.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the own arms checked clean as first written. The table arm
began its rows as Rust makes a `Vec` from an array, `[first].to_vec()`,
with `Row` a plain struct; `karac check` refused it, the copy cloning
each element, and said to add `#[derive(Copy, Clone)]` to `Row`, which
`karac fix` did. A list literal is already the `Vec`, so the edit
wanted was to drop `.to_vec()`, and `[first]` is what the arm reads.
That was kara `B-2026-11-20-148`, fixed at `0d28296389`: the refusal now
says the literal is the list, and the fix drops the copy.

The differential's P4 first set x to `10^12`, past LeetCode's most; the
solution arm narrows x to `i32` as LeetCode's signature does, so it
answered for a different x, and P4 failed there alone. The property now
keeps to `x = 10^6`, where the numbers sum to less.

LeetCode's Rust template took 12 `karac fix` edits, the wrapper
included: `struct Solution {}` added; the `Vec<..>`s became `Vec[..]`;
`i64::MIN` became `i64.MIN`; the `as i64` widenings of `nums[0]` and `v`
were dropped, an `i32` widening by itself; `for &v in &nums[1..]`
became `for v in nums[1..]`; the wrapper's `|&v|` dropped its `&`; and
`Solution::` became `Solution.`. The `as usize` indices stayed.
