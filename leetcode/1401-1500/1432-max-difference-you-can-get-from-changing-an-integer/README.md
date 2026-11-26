# 1432. Max Difference You Can Get From Changing an Integer

You are given an integer `num`. You will apply the following steps to
`num` two separate times: pick a digit `x` (`0 <= x <= 9`), pick another
digit `y` (`0 <= y <= 9`), where `y` can be equal to `x`, and replace
all the occurrences of `x` in the decimal representation of `num` by
`y`. Let `a` and `b` be the two results from applying the operation to
`num` independently. Return the max difference between `a` and `b`. Note
that neither `a` nor `b` may have any leading zeros, and they must not
be 0.

```
num = 555    ->  888    a = 999 (x = 5, y = 9), b = 111 (x = 5, y = 1)
num = 9      ->  8      a = 9, b = 1
```

**Constraints:** `1 <= num <= 10^8`.

Each arm is `fn max_diff(num: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_diff.kara` ★ | the largest from the first digit that is not a 9 made a 9 everywhere, and the smallest from the first digit made a 1, or, when it is a 1 already, the first later digit that is neither a 0 nor a 1 made a 0, each change made by `String.replace` and read back by `i32.parse`. O(d) for d digits |
| `max_diff_digits.kara` | the same choices made on the digits as numbers, split off by `% 10`, and each change put back together digit by digit. O(d) |
| `max_diff_table.kara` | each choice as a table from every digit to what it becomes, an `Array[i32, 10]` with only the chosen digit changed, and the number read through it by `fold` over its bytes. O(d) |
| `max_diff_brute.kara` | every x and y, 100 changes, each made on the text through `chars().map(..).collect()`, those that lead with a 0 set aside, and the largest less the smallest of the rest. O(100 d) |
| `max_diff_solution.kara` | a Rust solution as LeetCode's Rust users write it (`num.to_string()`, the choices by `s.replace(c, "9")` on a `char`, the results read back by `parse::<i32>().unwrap()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples and six more
(`888 8 820000 80000 8700 8 800000000 888`); the constraints' most, 10^8
and two numbers below it, and every number from 1 to 10^5 summed (`10^8:
800000000 88888888 82000000, 1 to 10^5: 7446604367`); and 2000 random
numbers of 1 to 8 digits, each drawn from 0 to 2, 0 to 9, or 1 and 9
(`2000 random numbers: 24357542020 in all, checksum 349586703`).
`max_diff.py` mirrors the ★ arm, and its output is byte-identical. Every
arm gives the same output under `karac __mir-run`, `karac run`, `karac
build` and `karac __mir-llvm-run`.

The Mend loop: the digits and brute arms check clean as first written.
The ★ arm handed `String.replace` a `char` three times, which `karac
check` refuses, saying `replace` takes a `Str` pattern and to write the
`char` as `c.to_string()`, and `karac fix` writes it, 3 fixes. The table
arm indexed its tables by `(b - b'0') as i64`, which checks with a
warning that a `u8` widens to `i64` without the cast, and `karac fix`
drops the casts, 4 fixes. The Rust solution takes one round of 15 fixes
by `karac fix`'s count: `struct Solution;` to `struct Solution {}`, its
three `char` patterns to `.to_string()`, `&&` to `and`, `parse::<i32>()`
to `i32.parse(..)`, and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every x and y, each change made on the digits, a change that
leads with a 0 or makes 0 set aside, and every allowed change then taken
as a and every one as b. LeetCode's examples, ten edge cases (one, ten,
the constraints' most and the eight nines below it, ones alone, a 1 with
a 0 after it, a 9 first, a 1 first, a 9 then a 0, and a 1 then a 9), and
1991 random numbers of 1 to 8 digits, drawn as the harness draws them,
each with a place for P3.

The differential first wrote its widenings out, `digits_of(num as i64)`
and `Some((num as i64) * ten + num as i64)`, which check with a warning
that an `i32` widens to `i64` without the cast, and `karac fix` drops
them, 5 fixes.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at least 0, and at most d nines less a 1 and d - 1 zeros |
| P3 | at least what making every copy of one of its digits a 9 moves the number by |
| P4 | the number written twice, while it fits, gives the answer times 10^d + 1 |
| P5 | the first digit written d times gives 8 written d times |
| P6 | the ★ arm's answer |

All 55,085 checks pass on every arm: `2003 cases: checksum 995318555,
55085 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by `str.replace`
over every x and y, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the first digit made a 2 for the smallest, not a 1 | P1 1092, P5 1092, P6 4368 |
| M2 | ★: a later 1 made a 0 for the smallest, so the number can lead with a 0 | P1 338, P2 338, P4 143, P5 792, P6 1352 |
| M3 | digits: a later 1 made a 0 for the smallest | P1 338, P2 338, P4 143, P5 792, P6 338 |
| M4 | digits: the first digit that is not an 8 made a 9, not the first that is not a 9 | P1 371, P5 68, P6 371 |
| M5 | table: the first digit that is not an 8 made a 9 | P1 371, P5 68, P6 371 |
| M6 | table: a later 1 made a 0 for the smallest | P1 338, P2 338, P4 143, P5 792, P6 338 |
| M7 | brute: a change that leads with one 0 allowed | P1 1228, P2 1228, P4 237, P5 237, P6 1228 |
| M8 | brute: no digit ever made a 0 | P1 636, P6 636 |
| M9 | solution: the first digit that is not an 8 made a 9 | P1 371, P5 68, P6 371 |
| M10 | solution: the first digit made a 0 for the smallest, not a 1 | P1 1092, P2 1092, P5 1092, P6 1092 |

## Benchmarks

The bench runs the ★ arm on 3 * 10^6 numbers of 1 to 10^8, each drawn
from two draws, folding the answers to a checksum. Each implementation
makes the number's text and its two changes as fresh strings, as the ★
arm makes a `String` of each; the C bench writes each into its own
`malloc`ed buffer. Every implementation prints `3 * 10^6 numbers:
checksum 459344675`.

BENCHTAB

Measured by hand, Kāra takes 0.37 s against Rust's 0.24 to 0.25 s (0.24
s with overflow checks on), C's 0.36 s and Go's 0.67 to 0.68 s; Python
takes 3.7 s.
