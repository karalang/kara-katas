# 1342. Number of Steps to Reduce a Number to Zero

Given an integer `num`, return the number of steps to reduce it to zero.
In one step, if the current number is even, you have to divide it by 2,
otherwise, you have to subtract 1 from it.

```
num = 14   ->  6
num = 8    ->  4
num = 123  ->  12
```

**Constraints:** `0 <= num <= 10^6`.

The arms are `fn number_of_steps(num: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `number_of_steps.kara` ★ | the statement as a loop: halve an even number, take one from an odd one, count the steps. O(log num) |
| `number_of_steps_bits.kara` | every 1 bit costs a subtraction and every place below the top bit a halving, so the steps are `count_ones()` plus 31 less `leading_zeros()`; zero takes none. O(1) |
| `number_of_steps_recursive.kara` | a `match` on the number and its low bit: zero takes none, an even number is one step from its half, an odd one one step from the number below. O(log num), as deep |
| `number_of_steps_shift.kara` | the bits read from the bottom with `&` and `>>=`, a 1 bit costing two steps and a 0 bit one, and the top bit's halving taken back at the end. O(log num) |
| `number_of_steps_solution.kara` | a Rust solution as LeetCode's Rust users write it (the parameter taken as `mut num: i32`, a `while num != 0` loop with `num /= 2` or `num -= 1`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, zero, one,
10^6, the constraints' largest, and 2^19 - 1, the most steps below 10^6
(`6 4 12 0 1 26 37`); and every number from 0 to 10^6 (`0 to 10^6:
27836444 steps, checksum 487224127`). `number_of_steps.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean. The Rust solution takes
one round of 4 fixes by `karac fix`'s count, from 3 errors: `struct
Solution;` to `struct Solution {}`, `Solution::` to `Solution.`, and the
`mut num: i32` parameter to `num: i32` with `let mut num = num;` as the
body's first line, since a parameter's mode is written in its type and a
scalar is copied in anyway. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every number on the way written down, each the one before
halved if even and less one if not, until zero, and the steps counted as
the numbers after the first. 4000 numbers: every one from 0 to 1999,
then 2000 drawn from 0 to 10^6, all drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | twice the number, when it is not zero: one step more |
| P3 | twice the number and one more, when it is not zero: two steps more |
| P4 | an odd number: one step more than the even number below it |
| P5 | the top bit moved one place up, when there is one: one step more |
| P6 | the ★ arm's answer |

All 109,830 checks pass on every arm: `4000 numbers: checksum 545440561,
109830 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, counting the 1 bits and the
bit length, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an odd number halved too | P1 3987, P3 3999, P4 1968, P6 15948 |
| M2 | ★: an even number quartered | P1 3998, P2 3159, P3 3159, P5 2020, P6 15992 |
| M3 | bits: the 0 bits counted for the 1 bits | P1 3993, P3 3999, P4 1969, P6 3993 |
| M4 | bits: zero not singled out | P1 1, P4 1, P6 1 |
| M5 | recursive: an odd number taken to its half in two steps at once | P1 3999, P4 1, P6 3999 |
| M6 | recursive: zero taken as one step | P1 4000, P6 4000 |
| M7 | shift: a 1 bit costing one step | P1 3999, P3 3999, P4 1969, P6 3999 |
| M8 | shift: a 0 bit costing nothing | P1 3989, P2 3999, P4 1968, P5 3999, P6 3989 |
| M9 | solution: a number halved only when four divides it | P1 3977, P2 1968, P3 1968, P6 3977 |
| M10 | solution: only the subtractions counted | P1 3998, P2 3999, P3 3999, P5 3999, P6 3998 |

P1 and P6 kill all ten, P3 six, P4 six, P2 four and P5 three. Each of
P2 to P5 adds one kind of step and checks its price: a 0 bit at the
bottom (P2) and a place at the top (P5) cost one halving, so they catch
the edits that miscount halvings (M2, M8, M10, and M9 for P2); a 1 bit at
the bottom (P3) costs a subtraction and a halving, so it catches the
edits that miscount either (M1, M2, M3, M7, M9, M10); and the
subtraction alone (P4) catches the edits that miscount it (M1, M3, M7,
M8). An edit off by the same amount everywhere passes all four: zero
taken as one step (M6) adds one to every answer and is caught only by
the statement, and the odd number taken straight to its half (M5) is
right except that every chain now ends at 1 for two steps, one too
many, which P4 sees only at 1 itself. M4 is the weakest: without its
guard the bit count gives -1 for zero alone.

## Benchmarks

The bench answers every number from 0 to 10^6, the constraints' range,
5 times with the ★ arm's loop; each number is offset by the checksum so
far, so no answer can be computed ahead, and the answer plus the pass is
folded into the checksum. Every implementation prints `5 passes over
10^6 + 1 numbers: checksum 804313521`.

BENCHTAB
