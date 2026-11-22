# 2748. Number of Beautiful Pairs

You are given a **0-indexed** integer array `nums`. A pair of indices
`i`, `j` where `0 <= i < j < nums.length` is called beautiful if the
**first digit** of `nums[i]` and the **last digit** of `nums[j]` are
**coprime**.

Return *the total number of beautiful pairs in* `nums`.

Two integers `x` and `y` are **coprime** if there is no integer greater
than 1 that divides both of them. In other words, `x` and `y` are
coprime if `gcd(x, y) == 1`, where `gcd(x, y)` is the **greatest common
divisor** of `x` and `y`.

```
nums = [2, 5, 1, 4]  ->  5
nums = [11, 21, 12]  ->  2
```

**Constraints:** `2 <= nums.length <= 100`, `1 <= nums[i] <= 9999`,
`nums[i] % 10 != 0`.

## Approaches

| file | mechanism |
|---|---|
| `beautiful.kara` ★ | only the earlier number's first digit and the later one's last digit matter: the first digits seen so far counted in an `Array` of 10, and each number adds the counts of the digits coprime to its last digit by a recursive `gcd`. O(9 n) |
| `beautiful_brute.kara` | every pair i < j, the first digit found by dividing down and Euclid's algorithm in a `while` loop. O(n^2) |
| `beautiful_digits.kara` | each number written out by `to_string()`, its digits read as `char`s by `to_digit(10)`, and every pair tested against a 10 by 10 `Array` of `bool`s built once with `all`. O(n^2) |
| `beautiful_suffix.kara` | from the right, by `iter().rev()`: the last digits of the numbers after i counted in a `Vec`, and each number adds those coprime to its first digit through `filter`, `map` and `sum`. O(9 n) |
| `beautiful_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `fn gcd` nested in the method and each first digit read off `to_string().chars().next()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; 100 ones,
every pair beautiful; 100 of 22, none; LeetCode's largest and smallest
numbers together; and 5000 random lists of 2 to 100 numbers from 1 to
9999, none a multiple of 10, with the sum of the answers and a checksum.
`beautiful.py` mirrors the ★ arm and its output is byte-identical.

```
5
2
4950
0
5
5000 lists: pairs sum to 6071578, checksum 52061106
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair i < j, the first digit the first character of
`nums[i]` written out and the last digit the last character of
`nums[j]`, coprime when no digit from 2 to 9 divides both. It draws 2000
random lists of 2 to 30 numbers from 1 to 9999, none a multiple of 10,
then 300 of up to 100, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every number's digits reversed, and the list reversed: the same answer |
| P3 | the tens digit of every number of 3 digits or more moved on 3: the same answer |
| P4 | a 1 put at the end, and one put at the front: each n more |
| P5 | at most n (n - 1) / 2, and every last digit made 1: exactly that |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2300 cases: checksum 972836535, 69000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases with `math.gcd` gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M10 first turned Euclid's step into a division,
which from gcd(1, 1) calls itself with the same pair forever and
overflowed the stack under both backends, so it was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a first digit of 1 never counted | P1 1841, P2 2089, P4 2300, P5 1844, P6 1841 |
| M2 | ★: the tens digit taken for the last | P1 2129, P2 2173, P3 2176, P4 2300, P5 2224, P6 2129 |
| M3 | brute: the last two digits taken for the last | P1 1954, P2 2040, P3 1863, P5 2026, P6 1954 |
| M4 | brute: Euclid's a never moved on | P1 2262, P2 2089, P4 2300, P5 2292, P6 2262 |
| M5 | digits: 2 never taken as a shared factor | P1 2080, P6 2080 |
| M6 | digits: the later number's first digit read for its last | P1 2087, P2 2161, P5 2219, P6 2087 |
| M7 | suffix: the numbers walked from the left | P1 2135, P6 2135 |
| M8 | suffix: each last digit counted at most once | P1 2030, P2 1991, P4 2178, P5 2230, P6 2030 |
| M9 | solution: the earlier number's last digit read for its first | P1 2104, P2 2161, P6 2104 |
| M10 | solution: each number paired with itself too | P1 2295, P4 2300, P5 2300, P6 2295 |

## Benchmarks

The bench draws 20000 lists of 100 numbers from 1 to 9999, none a
multiple of 10, LeetCode's most, all of them first, then answers each
10 times by the ★ arm in all five languages, each with the same
recursive `gcd`. Every implementation prints `20000 lists of 100
numbers, 10 rounds: pairs sum to 709858620, checksum 253642654`.

BENCHTAB

## Verification

All five arms print the same output as `beautiful.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, digits and suffix arms checked clean as first written. The brute
arm wrote Rust's `let (mut a, mut b) = ..`, which `karac fix` made `let
mut (a, b) = ..`.

LeetCode's Rust template took 10 `karac fix` edits, the wrapper
included: `struct Solution {}` added; the `fn gcd` nested in the method
moved out to the top level beside it, unchanged; `Vec<i32>` and
`Vec<i64>` became `Vec[i32]` and `Vec[i64]`; the `&x` pattern dropped
its `&`; and `Solution::` became `Solution.`, with the wrapper's `as
i64` dropped.

The differential first read a reversed number back with a guessed
`text.parse_int()`; `karac check` named `i64.parse(text)`, which gives a
`Result`.
