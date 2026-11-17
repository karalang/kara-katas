# 2217. Find Palindrome With Fixed Length

Given an integer array `queries` and a **positive** integer
`intLength`, return *an array* `answer` *where* `answer[i]` *is either
the* `queries[i]th` *smallest **positive palindrome** of length*
`intLength` *or* `-1` *if no such palindrome exists*.

A **palindrome** is a number that reads the same backwards and
forwards. Palindromes cannot have leading zeros.

```
queries = [1, 2, 3, 4, 5, 90], intLength = 3  ->  [101, 111, 121, 131, 141, 999]
queries = [2, 4, 6], intLength = 4             ->  [1111, 1331, 1551]
```

**Constraints:** `1 <= queries.length <= 5 * 10^4`;
`1 <= queries[i] <= 10^9`; `1 <= intLength <= 15`.

A palindrome is fixed by its first half, `(intLength + 1) / 2` digits,
and the halves in order are the numbers from `10^(half - 1)`: the q-th
is `10^(half - 1) + q - 1`, and past `10^half` there is none. The half
is mirrored onto itself, the middle digit of an odd length used once.
O(k * intLength).

## Approaches

| file | mechanism |
|---|---|
| `palindrome.kara` ★ | the q-th half by arithmetic, then mirrored by arithmetic: its digits taken off the end with `% 10` and appended, from the half less its last digit for an odd length |
| `palindrome_string.kara` | the half written out with `to_string`, its characters reversed after it with the middle one skipped for an odd length, and the whole read back with `i64.parse` |
| `palindrome_digits.kara` | q - 1 counted out in the half's own digits, the first from 1 to 9 and the rest from 0 to 9, into a `Vec` of the whole length set at each place and its mirror; a first digit past 9 means there is none |
| `palindrome_struct.kara` | a `struct Palindromes` of one length with the smallest half, `count` (`ref self`) and `nth` (`ref self`) returning `Option[i64]`, `None` past the last, read with `unwrap_or(-1)` |
| `palindrome_iter.kara` | the smallest half by `fold`, the half's digits by `chars`, followed by them reversed (`chain`, `rev`, `skip`) and `fold`ed into a number; every query by `map` |
| `palindrome_solution.kara` | LeetCode's Rust template: a `Vec<i32>` and an `i32` in, `Vec<i64>` out, the smallest half by `10_i64.pow(half - 1)` with `half` a `u32`, and each answer by `format!` and `parse::<i64>()`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(length 1 to its end and past it, length 2, the last palindrome of
length 15 and the one after, and a query of 10^9), each with its
answers; then a checksum of 3000 random cases of 1 to 20 queries of
length 1 to 15, each up to twice the palindromes of that length and at
most 10^9; then the constraints' largest, 5 * 10^4 queries of length 15
up to 10^9 and 5 * 10^4 of length 14 counting up from 1. A query past
32767 is drawn from two draws, since one stops there. `palindrome.py`
mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 20 edits: `Vec<..>` to
`Vec[..]` five times, `10_i64.pow` to `10.pow`, the `|&q|` to `|q|`
twice, `skip((int_length % 2) as usize)` to `skip((int_length % 2))`,
`format!("{}{}", s, rev).parse::<i64>()` to `i64.parse(f"{s}{rev}")`,
`struct Solution;` to `struct Solution {}` and `Solution::` to
`Solution.`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number of the length tried in order, each written out
and checked against its reverse, the palindromes listed, and each query
the one at its place or -1 past the end; no halves. It checks 300
random cases of 1 to 8 queries of length 1 to 4, each up to twice the
palindromes of that length; then 30 of length 5; then 30 asking for the
last palindrome of length 1 to 4 and the one after. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | one answer for each query, each -1 or a palindrome of the length |
| P3 | the queries reversed: the answers reversed |
| P4 | each query asked again one higher: -1 or a larger palindrome, and -1 again after a -1 |
| P5 | the partner length (one more for an odd length, one less for an even one) shares the halves: -1 where it is -1, else the same palindrome with its middle digit written once more or once less |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 740423724, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that lists
the palindromes by string reversal. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm, five to each of
the other Kāra arms and to the template arm, each run under `karac
__mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the half taken as `int_length / 2` digits | P1 122, P2 20, P5 185, P6 122 |
| M3 | ★: the half one past the last let through (`>` for `>=`) | P1 64, P2 64, P5 24, P6 64 |
| M6 | ★: 0 for no palindrome, not -1 | P1 324, P2 253, P4 328, P6 324 |
| M9 | string: the half written out again unreversed | P1 164, P2 164, P5 109, P6 164 |
| M10 | string: the smallest half one digit short | P1 188, P2 37, P5 36, P6 188 |
| M11 | string: the q-th half one low | P1 332, P2 15, P5 3, P6 332 |
| M12 | digits: the first digit counted from 0, not 1 | P1 335, P2 53, P5 39, P6 335 |
| M13 | digits: a first digit of 9 taken as past the last | P1 102, P6 102 |
| M14 | digits: the digits never mirrored | P1 256, P2 256, P5 194, P6 256 |
| M17 | struct: the last palindrome taken as past the end | P1 67, P6 67 |
| M18 | struct: `count` ten times the smallest half, not nine | P1 95, P2 95, P5 44, P6 95 |
| M20 | struct: the odd and even lengths swapped | P1 329, P2 329, P5 329, P6 329 |
| M22 | iter: the middle digit never skipped | P1 195, P2 195, P5 329, P6 195 |
| M23 | iter: the smallest half ten times too large | P1 360, P2 360, P5 206, P6 360 |
| M25 | iter: each digit read one low | P1 329, P2 86, P5 70, P6 329 |
| M28 | solution: one digit of the reversed half kept | P1 93, P2 93, P5 185, P6 93 |
| M31 | solution: the reversed half written first | P1 165, P2 126, P4 18, P5 165, P6 165 |

P1 and P6 kill all seventeen, P2 fifteen, P5 fourteen, P4 two, and P3
none. P2 misses only the edits that still answer with palindromes of
the length, just the wrong ones or -1 too early (M13, M17). P5 kills the
edits that build the mirror wrongly or size the half wrongly, since the
partner length shares the half and shows the difference. P4 needs an
answer that falls as its query rises: 0 for none, below the palindrome
before it (M6), and the reversed half first, where the half 20 gives
220 after the half 19 gave 9119 (M31). P3 kills none of the thirty-one: every arm answers each
query on its own, so reversing the queries cannot tell a wrong arm
from a right one; it stays as a check that no arm carries state across
queries.

Of the thirty-one, fourteen were not kept. One crashes under both
backends, as it should: the template's half as `int_length / 2` makes
the half of length 1 zero, and `half - 1` on a `u32` overflows (M27).
The other thirteen are killed, and none differs between the backends.
Eight fail as a kept one does: the ★ arm's odd and even lengths swapped
and the string arm's skip of `1 - int_length % 2` (M4, M7) as the
struct arm's swap (M20); the ★ arm's mirror from the whole half (M5) as
the iter arm's middle digit never skipped (M22); the struct arm's
smallest half by `length / 2` (M19) as the ★ arm's (M1); the struct
arm's `unwrap_or(0)` (M21) as the ★ arm's 0 for none (M6); the iter arm's
and the template's `>` for `>=` (M24, M30) as the ★ arm's (M3); and the
iter arm's chain unreversed (M26) as the string arm's (M9). Four fail
alike and none of them is kept: the ★ arm's, the digits arm's and the
template's q-th half one high, and the string arm's every half taken as
too long, which answers -1 throughout (M2, M16, M29, M8). One fails its
own way and is left out for the count of three: the digits arm's half
filled from its first digit, not its last (M15).

## Verification

Every arm prints the same output as `palindrome.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.5 s to 2.0 s, and the
differential 13 s, most of it the literal reading's walk over every
number of length 5.

## Benchmarks

The bench draws 30 lists of 5 * 10^4 queries once, for each length from
1 to 15 in turn and up to twice the palindromes of that length, then
punches each list 10 times, one query drawn again each time, and
answers it after each punch with the ★ arm in all five languages. Every
implementation prints `30 lists of 5 * 10^4 queries, 10 punches:
checksum 804899206`.

BENCHTAB
