# 2719. Count of Integers

You are given two numeric strings `num1` and `num2` and two integers
`max_sum` and `min_sum`. We denote an integer `x` to be *good* if:

- `num1 <= x <= num2`
- `min_sum <= digit_sum(x) <= max_sum`.

Return *the number of good integers*. Since the answer may be large,
return it **modulo** `10^9 + 7`.

Note that `digit_sum(x)` denotes the sum of the digits of `x`.

```
num1 = "1", num2 = "12", min_sum = 1, max_sum = 8  ->  11
num1 = "1", num2 = "5",  min_sum = 1, max_sum = 5  ->  5
```

**Constraints:** `1 <= num1 <= num2 <= 10^22`, `1 <= min_sum <= max_sum <= 400`.

## Approaches

| file | mechanism |
|---|---|
| `integers.kara` ★ | the good numbers up to a bound, by a digit-by-digit recursion: every digit up to the bound's while the prefix is the bound's, up to 9 once it is below, the sum carried down and cut off past `max_sum`; a free place's count depends only on the place and the sum, so it is remembered in a `Vec[Vec[i64]]`. The answer is the count up to num2, less that up to num1, plus num1 itself when it is good. O(digits · max_sum · 10) |
| `integers_table.kara` | `ways[k][s]`, the strings of k free digits that sum to s, filled once bottom up; then a walk along the bound, where each digit below the bound's at a place leaves the rest free and adds their ways to each allowed sum; the bound itself counted at the end. Same order |
| `integers_both.kara` | one walk tight against both bounds at once, num1 padded with leading zeros to num2's length, so nothing is subtracted; a `struct Walk` holds the bounds and a `Map[(i64, i64, bool, bool), i64]` memo over place, sum and the two tight flags. Same order |
| `integers_sweep.kara` | bottom up over the places, the prefixes below the bound counted by digit sum in one row, moved forward by every digit at each place, while the one prefix equal to the bound splits into those below it and the one that stays. Same order |
| `integers_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `const MOD` and a `fn dfs` nested in a `fn calc` nested in the method, a `vec![vec![-1i64; 401]; n]` memo passed `&mut`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; 1 to
`10^22`, LeetCode's widest range, with every sum allowed and with only
400; one number alone; the 22 nines; 1 to the 22 nines with sum 99; then
2000 random ranges up to `10^4` with sums up to 40, and 300 of up to 22
digits with sums up to 200, each with the sum of their answers and a
checksum. `integers.py` mirrors the ★ arm and its output is
byte-identical.

```
11
5
490000
0
1
1
407219807
2000 ranges up to 10^4: counts sum to 1368813, checksum 946076198
300 ranges up to 22 digits: counts mod p sum to 77678379133, checksum 39024645
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every integer from num1 to num2 in turn, its digits summed,
and the good ones counted, with no digit recursion. It draws 1000 random
ranges of up to 3 digits with sums up to 30, then 20 of up to 22 digits
with sums up to 200, all before any arm answers; the literal reading is
asked only of the first 1000.

| | property |
|---|---|
| P1 | up to 3 digits, the answer is the literal reading's |
| P2 | the range cut after a number m inside it: the two parts' answers add up to the answer, mod `10^9 + 7` |
| P3 | the sums cut after a k between min_sum and max_sum: the two parts' answers add up to the answer |
| P4 | every sum from 1 to 400 allowed: num2 - num1 + 1, mod `10^9 + 7` |
| P5 | the range num1 to num1: 1 when num1's digit sum is allowed, else 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1020 cases: checksum 983124686, 30600 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by counting every integer gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a free place's count remembered while tight too | P1 442, P2 158, P4 575, P6 461 |
| M2 | ★: tightness passed on by the digit alone | P1 576, P2 209, P4 654, P6 595 |
| M3 | table: the free places' ways summed to 8, not 9 | P1 880, P2 79, P4 976, P6 899 |
| M4 | table: the bound itself never counted | P1 380, P2 105, P6 388 |
| M5 | both: num1's floor kept after the walk leaves it | P1 785, P2 814, P4 968, P6 804 |
| M6 | both: num1 padded at the end, not the front | P1 808, P2 657, P4 917, P6 827 |
| M7 | sweep: the equal prefix splits on digits up to its own | P1 906, P2 96, P4 917, P6 925 |
| M8 | sweep: prefixes below the bound end at sums under min_sum | P1 892, P2 372, P3 970, P6 912 |
| M9 | solution: a walk cut off at the largest sum itself | P1 329, P2 8, P3 688, P6 342 |
| M10 | solution: num1 never added back | P1 423, P2 608, P4 1020, P5 430, P6 430 |

## Benchmarks

The bench draws 300 ranges of two 22-digit numbers, num1 below `5 ·
10^21` and num2 above, with sums from 1 to 400, all of them first, then
answers each 10 times by the ★ arm's remembered recursion in all five
languages. Every implementation prints `300 ranges of 22 digits, 10
rounds: counts mod p sum to 648097066560, checksum 713358322`.

BENCHTAB

## Verification

All five arms print the same output as `integers.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The both-bounds arm took one `karac fix`: the `as i64` on the byte
difference pushed onto `low` dropped, since a `u8` widens by itself. The
fix leaves the parentheses that held the cast, `low.push((b - b'0'))`,
and they are kept as the fix wrote them.

LeetCode's Rust template took one `karac fix` of 40 edits, the wrapper
included. The nested `fn calc` and `fn dfs` and the `const MOD` were
hoisted out of the method to the top level, since Kāra has no nested
items; `&str` became `Str`, `Vec<usize>` became `Vec[i64]` and the
`usize` index parameter `i64`; `vec![vec![-1i64; 401]; n]` became
`Vec.filled(n, Vec.filled(401, -1))`; `&d` and `&mut memo` became `d`
and `mut memo` at the calls, `&Vec<usize>` and `&mut Vec<Vec<i64>>`
became `ref Vec[i64]` and `mut ref Vec[Vec[i64]]`; the four `sum as
usize` indices dropped their cast; `.bytes().map` became
`.bytes().iter().map`; `!` and `&&` became `not` and `and`; and
`Solution::` became `Solution.`, with the wrapper's `as i64` dropped.
