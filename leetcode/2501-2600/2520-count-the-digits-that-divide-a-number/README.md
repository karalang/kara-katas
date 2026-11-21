# 2520. Count the Digits That Divide a Number

Given an integer `num`, return *the number of digits in `num` that
divide `num`*.

An integer `val` divides `nums` if `nums % val == 0`.

```
num = 7     ->  1
num = 121   ->  2
num = 1248  ->  4
```

**Constraints:** `1 <= num <= 10^9`; `num` does not contain `0` as one
of its digits.

A digit that appears more than once is counted each time it appears,
so `121` answers 2: the two ones divide it and the two does not. With
no digit 0 every remainder is defined. The approaches differ in how the
digits are reached.

## Approaches

| file | mechanism |
|---|---|
| `digits.kara` ★ | the digits peeled off the low end by `% 10` and `/ 10`, each counted when it divides the number. O(log num) |
| `digits_text.kara` | the number written out with `to_string`, its `chars` each turned back into a digit by `to_digit(10)` |
| `digits_tally.kara` | a tally of how often each digit 1 to 9 appears, then the digits that divide the number adding their tallies |
| `digits_rec.kara` | recursion over the rest of the number: the last digit's 1 or 0 plus the answer for the rest divided by 10. At most 10 deep |
| `digits_iter.kara` | iterators: the rests a `successors` chain dividing by 10, `map`ped to their last digits, `filter`ed and `count`ed |
| `digits_solution.kara` | LeetCode's Rust template: `i32` in, `i32` out; the bytes of `num.to_string()` less `b'0'` `filter`ed and `count`ed; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples and six
more; then 2000 random numbers of 1 to 4 digits and 2000 of 1 to 9,
none with a digit 0, as the sum and a checksum; then every number from
1 to `2 10^5` with no digit 0: how many there are, how many every digit
divides, and the sum of the answers. `digits.py` mirrors the ★ arm and
its output is byte-identical, and the mirror was checked against a
count over the decimal text on every number from 1 to `2 10^5` with no
digit 0, and the two agreed on every one.

`check` first reports 3 errors on the template: `struct Solution;`, the
`&b` pattern of the closure, and the path call `Solution::count_digits`.
`karac fix` carries it in one call, reporting 6 edits: `struct Solution
{}`; the `&` pattern dropped; `Solution.count_digits`; `.iter()`
inserted after `bytes()`, since an iterator adaptor needs an explicit
iterator; the `as i32` on `b - b'0'` dropped, a `u8` widening to `i32`
without one; and the wrapper's lossless `as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the number's decimal text, each of its bytes turned into a
digit, and the positions whose digit divides the number counted. It
checks 180 random numbers of 1 to 4 digits and 150 of 5 to 9; then 30
of one digit repeated 1 to 9 times. Every number keeps the constraints.
All 360 are drawn before any arm answers, and 97 of them are divided by
every digit.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | from 0 to the number of digits, and 1 for a one-digit number |
| P3 | a number of up to 4 digits written twice: the answer at least twice its own |
| P4 | at least the number of digits that are 1, together with those that equal a last digit of 2 or 5 |
| P5 | the last digit written as many times as the number has digits: the answer that many |
| P6 | each arm agrees with at least three of the other five |

P3 holds because the number written twice is the number times
`10^len + 1`, so every digit that divides the number divides it too;
it is checked only up to 4 digits, where the doubled number keeps the
constraints. P4 holds because 1 divides everything, and a last digit
of 2 or 5 makes the number even or a multiple of 5. P5 holds because a
digit divides any number made only of itself.

The differential prints `360 cases, 97 divided by every digit:
checksum 292463672, 12960 checks over 6 arms: 0 failures` under every
lane in Verification; the checksum of the literal answers was checked
against a Python reading that builds the same cases and counts over the
decimal text. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the number divided by the rest | P1 191, P3 42, P4 51, P5 267, P6 191 |
| M4 | ★: the rest divided by the digit | P1 221, P3 55, P6 221 |
| M5 | ★: two digits peeled at once | P1 181, P3 74, P4 74, P5 307, P6 181 |
| M8 | text: each digit one more | P1 280, P2 53, P4 121, P5 334, P6 280 |
| M9 | text: the digit divided by the number | P1 256, P3 53, P4 189, P5 307, P6 256 |
| M11 | text: the number tested by its last digit | P1 212, P4 66, P6 212 |
| M12 | tally: the digit 9 left out | P1 17, P2 5, P5 47, P6 17 |
| M13 | tally: a digit counted once however often | P1 122, P3 155, P4 51, P5 307, P6 122 |
| M14 | tally: the tally divided instead | P1 268, P3 117, P4 16, P5 169, P6 268 |
| M17 | rec: the leading digit left out | P1 167, P2 53, P4 52, P5 360, P6 167 |
| M18 | rec: the recursion from the number | P1 127, P3 36, P4 8, P6 127 |
| M20 | rec: a dividing digit counted 2 | P1 309, P2 144, P5 360, P6 309 |
| M22 | iter: the last step dropped | P1 114, P3 53, P4 35, P5 307, P6 114 |
| M24 | iter: the remainder kept for the digit | P1 221, P3 26, P4 127, P5 142, P6 221 |
| M25 | iter: the filter turned over | P1 324, P2 53, P3 9, P4 46, P5 360, P6 324 |
| M28 | solution: the digit 1 not counted | P1 147, P2 7, P4 98, P5 38, P6 147 |
| M31 | solution: the number cut to its last 4 digits | P1 116, P3 67, P4 48, P5 166, P6 116 |

P1 and P6 kill all seventeen, P4 and P5 fourteen each, P3 eleven, and
P2 six.

Two of the first thirty-one edits were replaced. The tally arm's every
digit 1 to 9 tested survived: a digit the number lacks has a tally of
0, so adding it changes nothing, and the edit is equivalent. The
template's digit off by one (`b - b'1'`) crashed on division by zero at
the first digit 1. They became the tally arm's tally begun one digit in
(M16) and the template's digit 1 not counted (M28).

Fourteen are not kept, and none survives. Eight fail exactly as a kept
one. The ★ arm's leading digit left out, the text arm's first character
skipped, the tally arm's leading digit not tallied and the template's
first byte skipped (M2, M7, M15, M27) fail as the rec arm's leading
digit left out (M17); the ★ arm's and the template's not-dividing
digits counted (M6, M30) as the iter arm's filter turned over (M25);
the text arm's dividing digit counted twice (M10) as the rec arm's
(M20); and the iter arm's digit tested against the number (M26) as the
text arm's digit divided by the number (M9). The other six fail in two
ways of their own, each shared by three: the ★ arm's count begun at 1,
the rec arm's end counted as 1 and the template's one more than the
count (M3, M19, M29) add 1 to every answer, and the tally arm's tally
begun one digit in, the rec arm's rest begun one digit in and the iter
arm's first value skipped (M16, M21, M23) drop the last digit; each
arm already holds its kept edits.

## Verification

Every arm prints the same output as `digits.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.0 to 3.0 s and the differential 0.4 s; under `karac __mir-llvm-asan` the arms take 0.6 to 1.1 s and the differential 0.5 s; and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds 100000 random numbers of 1 to 9 digits from 1 to 9
once from its own generator, then makes 150 passes. Each pass asks
every number, starting at the index `check % 100000` and wrapping,
folding each answer plus the pass into the checksum. The bench uses the
★ arm in all five languages. Every implementation prints `150 passes
over 100000 numbers: checksum 882744588`.

BENCHTAB
