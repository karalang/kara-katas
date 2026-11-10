# 2081. Sum of k-Mirror Numbers

A k-mirror number is a positive integer without leading zeros that reads
the same both forward and backward in base-10 as well as in base-k.

For example, `9` is a 2-mirror number. The representation of `9` in
base-10 and base-2 are `9` and `1001` respectively, which read the same
both forward and backward. On the contrary, `4` is not a 2-mirror
number. The representation of `4` in base-2 is `100`, which does not
read the same both forward and backward.

Given the base `k` and the number `n`, return the sum of the `n`
smallest k-mirror numbers.

```
k = 2, n = 5   ->  25
k = 3, n = 7   ->  499
k = 7, n = 17  ->  20379000
```

**Constraints:** `2 <= k <= 9`; `1 <= n <= 30`.

The k-mirror numbers are rare: the 30th in base 7 is 64454545446. But
the base-10 palindromes can be listed in increasing order directly, by
length and then by first half, each made by writing its half back onto
itself. There are about `2 · 10^(d/2)` of them below `10^d`, and each
one is tried in base `k` until `n` pass. The approaches differ in how
they list the palindromes and how they test the other base.

## Approaches

| file | mechanism |
|---|---|
| `kmirror.kara` ★ | the decimal palindromes from their halves, the half's digits written back with `p = p * 10 + rest % 10`; the base-`k` digits pushed onto a `Vec` and compared from both ends |
| `kmirror_string.kara` | by text: the half's `to_string()` and its `chars().rev()`, `skip`ping the middle digit at odd lengths, parsed back with `i64.parse`; the base-`k` digits written as a `String` with `char.from_digit`, which must equal its reverse |
| `kmirror_next.kara` | palindrome to palindrome: `next_palindrome(p)` is the first half plus one written back, or `10^len + 1` after all nines; base `k` tested by reversing the number there, `r = r * k + y % k` |
| `kmirror_iter.kara` | an `impl Iterator for Palindromes` of a length and the next half, `filter`ed to the base-`k` palindromes, `take(n)`, `sum()`; the digits tested by `zip` with their own `rev()` and `all` |
| `kmirror_basek.kara` | from the other base: the base-`k` palindromes in increasing order, made the same way in base `k`, kept when the decimal text reads the same reversed |
| `kmirror_solution.kara` | LeetCode's Rust template (`k: i32, n: i32`, `10i64.pow(half - 1)` with a `u32` length, `Self::is_mirror(p, k)` with a `mut x` parameter, `vec![]`, `(0..m / 2).all(..)`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more, each question and its sum; then the sum and a checksum of the
answers for every base and every `n` from 1 to 20; then the answer for
the constraints' largest `n`, 30, in every base. `kmirror.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number from 1 up, kept when its decimal text and its
base-`k` digits each read the same backwards, and the first `n` kept
summed. It checks 300 random questions of a base from 2 to 9 and `n`
from 1 to 12; then 20 whose `n` is below the base, and 20 that reach the
13th to 15th number in a base whose numbers stay small (2, 3, 4, 6, 8,
9; in bases 5 and 7 the 13th is past `10^7`). All 340 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the sum is the statement read literally |
| P2 | the `n`th number, the sum less the sum for `n - 1`, is 1 for the first and grows from each to the next |
| P3 | for `n` below the base and at most 9 the numbers are 1 to `n`, and the sum `n(n + 1) / 2` |
| P4 | the `n`th number reads the same backwards in base 10 and in base `k` |
| P5 | the `n`th number is a multiple of neither 10 nor `k` |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 questions: checksum 344167837, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal sums was checked against a Python reading of the same
questions. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first digit never compared | P1 208, P4 165, P5 46, P6 208 |
| M2 | ★: the middle digit kept at the even lengths | P1 175, P2 51, P3 42, P6 175 |
| M3 | ★: one number more summed | P1 340, P2 48, P3 132, P4 4, P5 4, P6 340 |
| M4 | text: the middle digit dropped at every length | P1 184, P2 28, P6 184 |
| M5 | text: the rest of the length counted on | P1 275, P2 277, P3 126, P4 319, P5 263, P6 275 |
| M6 | text: the base-`k` digits divided in base 10 | P1 208, P4 167, P5 67, P6 208 |
| M7 | next: the palindrome after the nines one too far | P1 79, P4 7, P6 79 |
| M8 | next: every other half skipped | P1 304, P3 106, P6 304 |
| M9 | next: a number kept when its reverse is no smaller | P1 186, P4 153, P6 186 |
| M10 | iter: each digit compared with itself | P1 208, P4 171, P5 47, P6 208 |
| M11 | iter: the stream starting at 2 | P1 340, P2 26, P3 132, P6 340 |
| M12 | iter: two middle digits dropped at odd lengths | P1 169, P2 16, P4 168, P5 37, P6 169 |
| M13 | basek: the halves widened at the even lengths | P1 186, P2 24, P6 186 |
| M14 | basek: only the lengths compared | P1 184, P4 181, P5 36, P6 184 |
| M15 | basek: the `n`th number left out of the sum | P1 340, P2 26, P3 132, P4 26, P5 26, P6 340 |
| M16 | solution: the adapter's base one more | P1 208, P4 202, P5 70, P6 208 |
| M17 | solution: each length's first half skipped | P1 340, P2 51, P3 132, P6 340 |

P1 and P6 kill all seventeen, P4 eleven, P2 and P5 nine each, and P3
seven. P4 and P5, which test the `n`th number itself, see an edit that
lets a number through that is no palindrome in one base: a digit never
compared (M1, M10), only lengths compared (M14), the wrong base (M6,
M16), a reverse that need only be no smaller (M9). They do not see an
edit that lists true palindromes in a wrong order or skips some, since
every number it keeps is still a k-mirror number: there P2 and P3 see
the numbers start somewhere other than 1 or fail to grow (M2, M4, M11,
M13, M17), and P3 a sum that is not `n(n + 1) / 2` for small `n` (M8).
P2 sees a sum of one number more or less (M3, M15) at `n = 1`, where
the sum is not 1.

Of the thirty, thirteen were not kept, and one survives. Six fail as a
kept one: the ★ arm's first halves skipped, the next arm's walk from 2
and the basek arm's first half skipped as M11; the text arm's lengths
compared as M10; the Rust arm's first digit never compared as M1 and its
adapter asking one more as M3; the iter arm's one number fewer taken
as M15. Two are killed with checks of their own but were left out
because their arm keeps three: the text arm's search going on past the
`n`th (P1 340, P2 98, P3 132, P4 89, P5 28) and the next arm's half one
digit short (P1 296, P2 225, P3 88). Three ran past the 300 s limit and
are not kept: the ★ arm's digits taken in base 10, and the basek and Rust
arms' middle digit kept at odd lengths, each a search whose `n`th
number lies far beyond the true one. The survivor is not equivalent: the
iter arm's length moved on a half late gives each `10^j + 1` once too
early (101 between 9 and 11, 1001 after 999), and none of those is a
k-mirror number for any base up to the 15th, as far as the differential
asks.

## Verification

Every arm prints the same output as `kmirror.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 14 s to 36 s, but for the string
arm's 120 s, which builds and parses two strings for each of the more
than a million palindromes the last line walks, and the differential
7.0 s (timed while other work shared the machine).

The string arm met two compiler gaps. It wrote each base-`k` digit as
Rust does, `char::from_digit(d, k)`, and the checker said only "no
associated function 'from_digit' on type 'char'", though `to_digit` and
`is_digit` are Rust's. `char.from_digit(num, radix) -> Option[char]` now
exists on every backend. Fixed in kara 0909d4aa26, test
`tests/kata_2081_char_from_digit.rs`. It also parsed with
`(front + &back).parse::<i64>()`, which `karac fix` made
`i64.parse(front + ref back)`, and compared with
`digits == digits.chars().rev().collect::<String>()`, whose turbofish
`karac fix` deletes; what is left cannot be typed, as `==` takes its own
right-hand type, and the checker asks for a typed `let`, which the arm
and the basek arm write (B-2026-10-29-36).

The iter arm met the other: it tested the digits with Rust's
`digits.iter().eq(digits.iter().rev())`, and Kāra's iterators have no
`eq`. Adding one to the library's `Iterator` broke `==` in its other
generic bodies, so it is filed as B-2026-11-10-26, and the arm writes
`zip(..).all(..)`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 5 and 2 edits: Rust's spellings (`Self::` and
`Solution::` to `.`, `mut x: i64` to `x: own i64` with `let mut x = x;`,
`struct Solution;` to `struct Solution {}`); then `vec![]` to
`Vec.new()` and the `i64` suffix of `10i64` dropped. The fixed arm reads
as the template does.

## Benchmarks

The bench asks every base from 2 to 9 for every `n` from 1 to 32, each
search started afresh from 1, with the ★ arm in all five languages: 256
searches through the decimal palindromes, the digits of each in base `k`
gathered in a growable array (a `Vec`, a `Vec`, a slice, a `list`, a
`malloc`'d buffer). Every implementation prints `256 answers: sum
12467237112977, checksum 222543769`.

BENCHTAB
