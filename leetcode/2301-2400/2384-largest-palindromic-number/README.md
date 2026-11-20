# 2384. Largest Palindromic Number

You are given a string `num` consisting of digits only.

Return *the **largest palindromic** integer (in the form of a string)
that can be formed using digits taken from* `num`. It should not contain
**leading zeroes**.

**Notes:**

- You do **not** need to use all the digits of `num`, but you must use
  **at least** one digit.
- The digits can be reordered.

```
num = "444947137"  ->  "7449447"
num = "00009"      ->  "9"
```

**Constraints:** `1 <= num.length <= 10^5`; `num` consists of digits.

A longer palindrome is a larger number, so every pair of equal digits
goes in, the larger digits outside; one digit left over can stand in the
middle, the largest such. The one catch is 0: pairs of 0s may only go in
once a larger digit has led, and a string of nothing but 0s answers
`"0"`.

## Approaches

| file | mechanism |
|---|---|
| `palindrome.kara` ★ | the digits counted; the left half takes each digit's pairs from 9 down, but no 0s while it is empty; the middle the largest digit left over; the right half the left reversed. O(n) |
| `palindrome_sort.kara` | the digits sorted from 9 down and walked: two equal side by side a pair for the half, unless 0s with the half empty; the first digit left unpaired the middle. O(n log n) |
| `palindrome_strip.kara` | built whole, every pair from 9 down to 0 in the half, then the 0s that lead stripped from both ends at once. O(n) |
| `palindrome_each.kara` | a pair at a time: the half grows by the largest digit with a pair left, scanning from 9 each time, a 0 only once the half has a digit. O(n * 10) |
| `palindrome_iter.kara` | iterators: the counts by `fold`, the half `flat_map`ped from 9 down with each digit `repeat`ed for its pairs, the middle by `filter` and `take`, the three `chain`ed |
| `palindrome_solution.kara` | LeetCode's Rust template: the counts in a `[0usize; 10]`, the halves and the middle as `String`s, and the answer by `format!`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one, two
and three 0s; ten different digits, and four 0s with two 1s; then
`10^5` random digits and `10^5` 0s with one 5, the first by length and
checksum; then 3000 random strings of 1 to 30 digits below 1 to 10, a 0
with a chance of 0 to 9 in 10, with a checksum and the total length.
`palindrome.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked on 1500 random strings of up to 7 digits against
every arrangement of every choice of their digits.

`check` first reports 7 errors on the template, and `karac fix` carries
it in one call, reporting 8 edits: `struct Solution;` given its braces;
`String::new` and `Solution::` written with a dot; `&&` written `and`;
`format!("{}{}{}", left, mid, right)` written as the f-string
`f"{left}{mid}{right}"`; and the wrapper's `num.clone()` passed as
`num`. The `[0usize; 10]` counts, the `as usize` index, `(b'0' + d as
u8) as char` and `chars().rev().collect()` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every palindrome of up to as many digits as the string, with
no 0 leading but 0 itself, built from each possible left half, kept when
the string holds its digits, and the largest kept. No counting from 9
down. It checks 300 random strings of 1 to 6 digits, which the literal
reading answers; then 30 of up to 300; then 30 of up to 300 nearly all
0s. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 6 digits, the answer is the literal reading's |
| P2 | a palindrome, with no 0 leading unless it is 0, its digits drawn from the string's |
| P3 | the string reversed: the same answer |
| P4 | two 9s added: the answer with a 9 at each end, when it has more than one digit |
| P5 | the answer as the string: the same answer |
| P6 | each arm agrees with at least three of the other five |

P4 holds because a 9 at each end is the largest pair, and an answer of
more than one digit already holds every pair, 0s too; a one-digit
answer may have left pairs of 0s out that two 9s let in. P5 holds
because the answer is already the largest arrangement of its own
digits.

The differential prints `360 cases: checksum 984145245, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and every palindrome of up to their length. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: a pair taken for an odd digit left over | P1 183, P2 232, P5 232, P6 232 |
| M4 | ★: no middle | P1 183, P2 37, P6 232 |
| M6 | ★: 1s kept from leading too | P1 16, P2 1, P6 24 |
| M7 | sort: the digits from 0 up | P1 168, P4 109, P6 222 |
| M10 | sort: a pair skipping the digit after it | P1 44, P4 104, P5 85, P6 95 |
| M11 | sort: the first digit left out | P1 105, P2 18, P3 121, P4 87, P5 217, P6 137 |
| M12 | strip: only the leading 0s stripped | P1 73, P2 76, P4 76, P5 76, P6 76 |
| M13 | strip: the middle a digit with an even count | P1 301, P2 360, P5 360, P6 360 |
| M14 | strip: the right half one short | P1 131, P2 104, P4 102, P5 107, P6 185 |
| M18 | each: a single digit taken as a pair | P1 183, P2 232, P6 232 |
| M20 | each: a middle 0 dropped | P1 8, P6 11 |
| M21 | each: a pair taking one digit | P1 45, P2 96, P4 109, P5 96, P6 96 |
| M22 | iter: the lead test turned round | P1 180, P2 162, P4 162, P6 239 |
| M23 | iter: a single digit enough to lead | P1 73, P2 76, P6 76 |
| M25 | iter: two middles | P1 124, P2 164, P4 45, P6 164 |
| M27 | solution: 0 whenever no middle | P1 15, P2 5, P6 20 |
| M30 | solution: the pairs from 0 up | P1 58, P2 5, P6 109 |

P1 and P6 kill all seventeen, P2 fourteen, P4 eight, P5 seven and P3
one. Every arm counts or sorts its digits, so none can see their order,
and P3, the string reversed, fails only an edit that drops a digit by
its place: the sort arm's first digit left out (M11). P4, two 9s added,
fails the edits that misplace the outer pairs, as the digits from 0 up
(M7), the right half one short (M14) or the lead test turned round
(M22). P5, the answer fed back, fails the edits whose answer is not the
best arrangement of its own digits, or not a palindrome at all, as a
pair taken for an odd digit left over (M3) or only the leading 0s
stripped (M12).

Of the thirty-one, fourteen were not kept. 0s allowed to lead in the ★,
sort and each arms (M1, M8, M17) fail alike; so do the right half not
reversed in the ★, iter and template arms (M5, M26, M28), the middle the
smallest left over in the ★ and iter arms (M2, M24), and the sort arm's
middle the last left over and the each arm's smallest left over (M9,
M19). The template's 0 never the middle (M29) fails as the each arm's
middle 0 dropped (M20). The strip arm's last digit not counted and pairs
from 0 up (M15, M16) and the template's middle before the left half
(M31) each fail apart from every kept one, and were left out to keep
three to an arm and two to the template. Two edits were replaced. The
sort arm's `"0"` answer never given survived: its walk never leaves the
answer empty, as a pair of 0s it may not take leaves its first 0
unpaired, and so the middle; it became the first digit left out (M11).
The strip arm's `"0"` answer only for nothing at all let a string of
three 0s strip two from each end of three, and the slice it then took
ran backwards and crashed; it became the last digit not counted
(M15).

## Verification

Every arm prints the same output as `palindrome.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.0 to 1.4 s, and the
differential 2.9 s there and 0.70 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 100 strings of `10^4` digits once from the harness's
generator, string `s`'s digits below `1 + s % 10` and each a 0 with a
chance of `s % 7` in 10, then makes 200 passes, folding each answer's
length and middle digit plus the pass into the checksum, with the ★ arm
in all five languages. Every implementation prints `200 passes over 100
strings of 10^4 digits: checksum 726119070`. Every implementation
allocates its half and its answer afresh in each call.

BENCHTAB
