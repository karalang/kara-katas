# 1404. Number of Steps to Reduce a Number in Binary Representation to One

Given the binary representation of an integer as a string `s`, return
the number of steps to reduce it to `1` under the following rules:

If the current number is even, you have to divide it by `2`.

If the current number is odd, you have to add `1` to it.

It is guaranteed that you can always reach one for all test cases.

```
s = "1101"  ->  6    13 -> 14 -> 7 -> 8 -> 4 -> 2 -> 1
s = "10"    ->  1
s = "1"     ->  0
```

**Constraints:** `1 <= s.length <= 500`, `s` consists of characters
`'0'` or `'1'`, `s[0] == '1'`.

Each arm is `fn num_steps(s: String) -> i32`. A number of up to 500
digits does not fit any integer type, so every arm works on the digits.

## Approaches

| file | mechanism |
|---|---|
| `num_steps.kara` ★ | the digits collected into a `Vec[char]` and walked from the last up to the second, with a carry left by the additions so far: a digit that is 1 with its carry is odd, so it takes an addition and a halving and leaves a carry, and anything else is halved at once; a carry left at the end is one more halving. O(n) |
| `num_steps_simulate.kara` | the number itself, its digits last first in a `Vec[u8]` from `s.bytes()`, halved by removing the last digit and one added by carrying through its trailing 1s, step by step. O(n^2) |
| `num_steps_count.kara` | counted outright: the 0s after the last 1, found by `rfind`, are each one halving, and before them a number ending in 1, unless it is 1, takes as many halvings as it has digits, one more for the digit its first addition carries out, and one addition for each 0 inside it, so n + 1 + those 0s. O(n) |
| `num_steps_recursive.kara` | the rules as a recursion on the text: a number ending in 0 is one step more than itself without that 0, sliced off, and one ending in 1 is one step more than the number after it, built by a recursive `plus_one` over `strip_suffix`. O(n^2) |
| `num_steps_solution.kara` | a Rust solution as LeetCode's Rust users write it (the same walk with a carry over `s.as_bytes()`, each digit as `(bytes[i] - b'0') as i32`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and three
more (`6 1 0 5 3 6`); the constraints' most, 500 digits all 1, 1 and
then 0s, and drawn (`500 digits: 501 499 742`); and 2000 random numbers
of 1 to 100 digits (`2000 random numbers: 148957 steps in all, checksum
195308283`). `num_steps.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ arm checks clean as first written. A string's
search methods take a `Str` pattern (library/strings.md), so the count
arm's `s.rfind('1')` and the recursive arm's `strip_suffix('1')` and
`ends_with('0')` are refused, check names the string literal, and `karac
fix` writes `"1"` and `"0"`, 1 and 2 fixes. `s.bytes()` is a
`Slice[u8]`, whose adaptors are reached through `.iter()`, so the
simulate arm's `s.bytes().rev()` is refused, and `karac fix` writes
`s.bytes().iter().rev()`, 1 fix. The Rust solution takes one round of 10
fixes by `karac fix`'s count: `struct Solution;` to `struct Solution
{}`, `s.as_bytes()` to `s.bytes()`, the cast in `(bytes[i] - b'0') as
i32` dropped since a `u8` widens by itself, which leaves `steps` and
`carry` at `i64` beside the `i32` returned, so `let mut steps: i32` and
`let mut carry: i32`, and `Solution::` to `Solution.`. Its output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the number read into an `i64`, halved while even and one
added while odd, until it is 1, on up to 62 digits. LeetCode's examples
and the edges (1, 2, 3, 15, 8, 11, and at 62 and 500 digits all 1s, a
power of two, 10 repeated, a power of two plus one), and 1988 random
numbers, 1 to 62 digits two times in three and else 63 to 500.

The examples are a `for` over an array of string literals, each pushed
as a `String`. `cases.push(String.from(s))` there is refused as a move
out of a borrowed place, E0516, though the same loop over a parameter's
collection, or over `.iter()`, copies the item; that is B-2026-11-26-5.
The differential pushes `s.clone()`, which the error suggests, `s` being
a `String` already.

| | property |
|---|---|
| P1 | the statement read literally, on up to 62 digits |
| P2 | every halving drops a digit, so at least n - 1 steps, and an addition is never needed twice in a row, so at most 2n - 1 |
| P3 | the number doubled, a 0 after it, takes one more step |
| P4 | a number ending in 1, other than 1, takes the same steps with a 1 or a 0 after it: 2x + 1 goes to 2x + 2 and then x + 1, and 2x to x and then x + 1 |
| P5 | a number ending in 1, other than 1, takes one step more than the number after it |
| P6 | the ★ arm's answer |

All 46,415 checks pass on every arm (P1 and P3 to P5 apply to some cases
only): `2003 cases: checksum 235656328, 46415 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, doing the steps on its own integers,
gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an odd digit counted as one step, not an addition and a halving | P1 1292, P5 973, P6 7828 |
| M2 | ★: the carry left at the end not counted | P1 1292, P5 27, P6 7828 |
| M3 | simulate: a halving dropping the first digit instead of the last | P1 1266, P3 970, P4 970, P6 1930 |
| M4 | simulate: an addition leaving the 0 its carry reaches a 0 | P1 1206, P5 450, P6 1870 |
| M5 | count: n + the 0s, the halving of the digit the first addition carries out left out | P1 1292, P5 27, P6 1957 |
| M6 | count: the 0s counted over the whole number, the trailing ones too | P1 637, P3 1952, P4 970, P5 946, P6 984 |
| M7 | recursive: one added to 1 giving 1, so a run of 1s loses the digit it carries out | P1 1292, P5 27, P6 1957 |
| M8 | recursive: an addition counted as two steps | P1 1292, P2 934, P5 973, P6 1957 |
| M9 | solution: an odd digit leaving no carry | P1 1199, P4 970, P5 720, P6 1844 |
| M10 | solution: the walk taking in the leading digit too | P1 1337, P2 64, P5 27, P6 2003 |

A first M4, the digit an addition carries out pushed as 0 rather than 1,
survived: the number then has one 0 more, and halving it down to one
digit takes as many steps, so it was an equivalent mutant and was
replaced.

## Benchmarks

The bench draws a pool of 10^5 random digits and runs the ★ arm on
200000 numbers of 500 digits, a 1 and then 499 digits of the pool, each
start drawn from the checksum so far. Every implementation prints
`200000 numbers of 500 digits: checksum 955002830`. Rust is about three
times as fast as Kāra with overflow checks off and level with it with
them on (`rustc -O -C overflow-checks=on`), measured by hand at 0.215 s,
0.695 s and Kāra's 0.669 s.

BENCHTAB
