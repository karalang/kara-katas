# 2396. Strictly Palindromic Number

An integer `n` is **strictly palindromic** if, for **every** base `b`
between `2` and `n - 2` (**inclusive**), the string representation of
the integer `n` in base `b` is **palindromic**.

Given an integer `n`, return `true` *if* `n` *is **strictly
palindromic** and* `false` *otherwise*.

A string is **palindromic** if it reads the same forward and backward.

```
n = 9  ->  false    (9 is 1001 in base 2, a palindrome, but 100 in base 3)
n = 4  ->  false    (4 is 100 in base 2)
```

**Constraints:** `4 <= n <= 10^5`.

In base `n - 2`, `n` is written `12` for every `n` from 5 up, and `4` in
base 2 is `100`, so the answer is always `false`. Five arms still try
every base, and every arm exposes its test of one base, so the
differential can tell them apart.

## Approaches

| file | mechanism |
|---|---|
| `palindromic.kara` ★ | every base tried, each base's digits taken off the bottom into a `Vec` and checked from both ends. O(n log n) |
| `palindromic_reverse.kara` | every base tried, the number's digits reversed arithmetically; a palindrome is its own reversal. O(n log n) |
| `palindromic_peel.kara` | every base tried, the highest and lowest digit compared and both taken off, recursively, the length carried so that zeros inside are not lost. O(n log n) |
| `palindromic_proof.kara` | one base, by the proof above: only base `n - 2`, its digits pushed into a `VecDeque` and taken off both ends. O(log n) |
| `palindromic_iter.kara` | iterators: each base's digits by `map` over the powers that fit, checked by `all` against the same digits from the other end; every base by `all`. O(n log n) |
| `palindromic_solution.kara` | LeetCode's Rust template: every base by `(2..=n - 2).all`, each base's digits compared with their reversal by `digits.iter().eq(digits.iter().rev())`, the test a private method called as `Self::`; carried by `karac fix` |
| `differential.kara` | the six arms, each its test of one base and its answer, against the statement read literally, six properties |

Every arm prints the same 64 lines: LeetCode's two examples; every `n`
from 4 to 60 and 1000, 65535, 99999 and `10^5`, each with how many of
its bases 2 to `n - 2` read it as a palindrome and its answer; then 3000
numbers in random bases from 2 to 31, a third drawn below 2000, a third
built as palindromes and a third built so with one digit then changed,
with a checksum of the verdicts and the count of palindromes.
`palindromic.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked against writing every `n` below 3000 out in every
base from 2 to 59, and every answer below 2000.

`palindromic_iter.kara` was first written with `vec![1]`; `karac fix`
rewrote it as the list literal `[1]`, in one call of 1 edit.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 3 edits: `struct Solution;` given its braces;
`Vec::new` written with a dot; and `Self::is_palindrome` written
`Solution.is_palindrome`. `(2..=n - 2)`, `digits.iter().eq(..)` and the
private method stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the number written out in base `b`, its highest digit first
from the largest power that fits, and that list compared with a reversed
copy. It checks 360 numbers in random bases from 2 to 31: a third drawn
below 2000, a third built as palindromes, and a third built so with one
digit then changed; and with each, an `n` from 4 to 363 for the whole
question. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the one base's verdict is the literal reading's |
| P2 | the number written twice over, its digits then its digits again: a palindrome exactly when it is (where that fits in 32 bits) |
| P3 | the number with a 0 written after it: never a palindrome (where that fits in 32 bits) |
| P4 | the `n` from 4 to 363: strictly palindromic exactly when the literal reading finds every base from 2 to `n - 2` a palindrome |
| P5 | a number not ending in 0, its digits reversed: a palindrome exactly when it is |
| P6 | each arm agrees with at least three of the other five on the base |

P2 holds because a list followed by itself reads the same backwards
exactly when the list does, P3 because a number ends in 0 but never
starts with one, and P5 because reversing a palindrome's digits gives
it back. The 32-bit limit is the template's `i32`; P2 is checked on 275
of the 360 cases, P3 on 354 and P5 on 343.

The differential prints `360 cases: checksum 750451593, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and writes each number out. On a failure it prints the
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
| M4 | ★: each digit compared with the one before its partner | P1 136, P3 68, P4 4, P5 17, P6 136 |
| M5 | ★: every digit compared with the last | P1 93, P6 93 |
| M6 | ★: a palindrome base taken as the failure | P4 23 |
| M7 | reverse: a reversal at least the number enough | P1 119, P4 1, P5 172, P6 119 |
| M8 | reverse: each digit read one place up | P1 174, P3 167, P6 174 |
| M11 | reverse: every other digit skipped | P1 120, P2 51, P6 120 |
| M12 | peel: two digits taken as a palindrome | P1 59, P2 41, P3 51, P4 3, P6 59 |
| M14 | peel: the top power lowered one place, not two | P1 58, P2 66, P5 4, P6 58 |
| M15 | peel: a power equal to n over b not counted | P1 6, P2 6, P3 12, P5 6, P6 6 |
| M17 | proof: the middle pair never compared | P1 59, P2 41, P3 51, P4 359, P6 59 |
| M19 | proof: both ends taken from the front | P1 96, P2 5, P3 27, P5 6, P6 96 |
| M20 | proof: the highest digit dropped | P1 138, P2 5, P3 64, P4 360, P5 19, P6 138 |
| M22 | iter: any equal pair enough | P1 117, P2 126, P3 37, P6 117 |
| M23 | iter: each digit compared with the one before its partner | P1 137, P3 167, P4 3, P5 17, P6 137 |
| M25 | iter: a power equal to n over b not counted | P1 6, P2 6, P3 13, P4 1, P5 6, P6 6 |
| M30 | solution: a last digit 1 dropped | P1 25, P3 17, P4 1, P5 9, P6 25 |
| M31 | solution: each base read one larger | P1 122, P2 60, P3 28, P5 9, P6 122 |

P1 and P6 kill sixteen of the seventeen, P3 twelve, P2 and P5 ten each,
and P4 nine. The one they miss is the ★ arm's palindrome base taken as
the failure (M6), which leaves the test of one base alone and changes
only the answer to the whole question: it answers yes for every `n`
with no palindromic base, and P4 alone finds it, 23 times. P4 also
catches the proof arm's edits to its one base (M17, M20) almost every
time, since that arm's answer is that one base's verdict, and six
other edits one to four times each (M4, M7, M12, M23, M25, M30).

Of the thirty-one, fourteen were not kept. The ★ arm's middle pair
never compared (M1) and the peel arm's length one short (M16) fail as
two digits taken as a palindrome (M12) does; the iter arm's digits never
reduced and the template's remainders kept whole (M24, M29) as the
reverse arm's every other digit skipped (M11). The ★ arm's smaller
first digit allowed and the peel arm's higher last digit allowed (M2,
M13) fail alike, as do the proof arm's first unequal pair answering yes
and the template's digits compared with themselves (M21, M28), base 2
never tried in the ★ and reverse arms (M3, M10), and base `n - 2` never
tried in the reverse, iter and template arms (M9, M26, M27); each of
those fails apart from every kept one, and they were left out to keep
three to an arm and two to the template. The last two groups change
only the answer for `n = 4` or 5, where one base is all there is to
try. The proof arm's base `n - 3` (M18) is base 1 for `n = 4`, whose
digits never end: memory ran out, and both backends stopped with an
error. A crash is not kept.

## Verification

Every arm prints the same output as `palindromic.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.36 to 4.2 s, the iter arm the
slowest. The differential takes 0.70 s there and 0.44 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench tests every base from 2 to `n - 2` of every `n` from 4 to
`10^4`, folding each `n`'s count of palindromes and its answer into the
checksum, with the ★ arm in all five languages. Every implementation
prints `every base of every n from 4 to 10000: checksum 403183015, 52247
palindromes`. Every implementation allocates a fresh list of digits for
each base: Kāra, Rust, Go and Python grow it from empty, C from room
for 8.

BENCHTAB
