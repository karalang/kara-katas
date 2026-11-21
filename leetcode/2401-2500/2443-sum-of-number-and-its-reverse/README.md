# 2443. Sum of Number and Its Reverse

Given a **non-negative** integer `num`, return `true` *if* `num` *can be
expressed as the sum of any **non-negative** integer and its reverse, or*
`false` *otherwise.*

```
num = 443  ->  true    (172 + 271)
num = 63   ->  false
num = 181  ->  true    (140 + 041)
```

**Constraints:** `0 <= num <= 10^5`.

The reverse of a number may have leading zeros, which drop away, so 140
reversed is 41. Any `k` that works is at most `num`, and `num` is at most
`10^5`, so trying every `k` from 0 to `num` and reversing each is a few
hundred thousand digit steps at most.

## Approaches

| file | mechanism |
|---|---|
| `sum.kara` ★ | every `k` from 0 to `num`, its digits reversed by `% 10` and `/ 10`, the first with `k + reverse(k) = num` answering true. O(num log num) |
| `sum_half.kara` | half the range: `k` or its reversal is at least `num / 2`, and when the reversal is the larger `k` has no trailing zero, so the reversal works too; only `k` from `num` down to `num / 2` are tried. O(num log num) |
| `sum_table.kara` | a table of every sum: each reversal built from that of `k / 10` by putting `k % 10` in front at the place `k / 10` reaches, and `k + reverse(k)` marked in a table of flags; the answer is the flag at `num`. O(num) |
| `sum_text.kara` | the reversal as text: each `k` written by an f-string, its bytes reversed and read back by `i64.parse`. O(num log num) |
| `sum_iter.kara` | iterators: `any` over `0..=num`, each reversal a `fold` over the digits by `successors`. O(num log num) |
| `sum_solution.kara` | LeetCode's Rust template: `(0..=num).any(..)` with each reversal by `k.to_string().chars().rev().collect::<String>().parse::<i32>()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; 0, 1 and
10; `10^5`, the constraints' largest; then every `num` from 0 to 1000,
as the count that hold and a checksum of them; 30 random `num` from 0 to
`10^5` as a checksum of the verdicts; and 30 sums of a random `k` up to
`5 * 10^4` and its reversal, each with the sum plus one, as the count
that hold. `sum.py` mirrors the ★ arm and its output is byte-identical,
and the mirror was checked on every `num` from 0 to 3000 and 300 random
ones up to `10^5` against the set of every `k + reverse(k)` for `k` up
to `10^5`, the reversal by Python's text.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 5 edits: `collect::<String>()` written
`String.from_iter(..)` and `parse::<i32>()` written `i32.parse(..)`,
since Kāra has no call-site type arguments and names the type before
the call; and `struct Solution;` given its braces. `(0..=num)`, `any`,
`to_string`, `chars`, `rev` and `unwrap` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every split of `num` into `a + b` tried, `a`'s decimal digits
listed from the top, reversed, stripped of the zeros that then lead, and
compared digit by digit with `b`'s list; a split that matches answers
true. No reversal is formed as a number. It checks 300 random `num` from
0 to 2000; then 30 from 0 to 5000; then 30 sums `k + reverse(k)` for a
random `k` up to 3000. All 360 are drawn before any arm answers. The
numbers stay small because the iter arm and the template take a
closure call for every `k` under `karac __mir-run`.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `k + reverse(k)` for a random `k` from 0 to `num`: true |
| P3 | twice the palindrome made from `num`'s leading half: true |
| P4 | 11 times `m`, `m` from 0 to 18: true |
| P5 | `101 s + 20 b`, `s` from 1 to 18 and `b` from 0 to 9: true |
| P6 | each arm agrees with at least three of the other five |

P2 holds by its making. P3 holds because a palindrome is its own
reversal. P4 holds because a two-digit `ab` and its reversal add to
`11 (a + b)`, and 0 is `0 + 0`; P5 because a three-digit `abc` and its
reversal add to `101 (a + c) + 20 b`, with `a` at least 1.

The differential prints `360 cases: checksum 63406731, 12960 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers was checked against a Python reading that builds the
same cases and looks each up in the set of every `k + reverse(k)`. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the digits summed | P1 277, P2 48, P3 23, P4 167, P5 35, P6 277 |
| M4 | ★: one more than num matched | P1 61, P2 252, P3 296, P4 339, P5 197, P6 61 |
| M6 | ★: each k added to itself | P1 188, P2 172, P4 183, P5 193, P6 188 |
| M7 | half: the middle never tried | P1 4, P2 9, P3 19, P4 20, P5 21, P6 4 |
| M10 | half: each digit doubled | P1 98, P2 331, P3 297, P4 324, P5 350, P6 98 |
| M11 | half: the search stopped at two thirds | P1 13, P2 27, P3 54, P4 88, P5 116, P6 13 |
| M12 | table: the new digit put second | P1 236, P2 26, P3 24, P5 46, P6 236 |
| M14 | table: num itself never marked | P1 65, P2 360, P3 360, P4 360, P5 360, P6 65 |
| M15 | table: one digit placed at 1 | P1 106, P2 297, P3 326, P4 167, P5 320, P6 106 |
| M18 | text: each reversal a tenth | P1 112, P2 307, P3 297, P4 271, P5 326, P6 112 |
| M19 | text: the reversal alone enough | P1 85, P6 85 |
| M21 | text: odd k skipped | P1 2, P2 7, P3 17, P4 8, P5 21, P6 2 |
| M22 | iter: num itself never tried | P1 1, P2 2, P3 1, P4 12, P6 1 |
| M25 | iter: every k needed | P1 64, P2 358, P3 359, P4 348, P5 360, P6 64 |
| M26 | iter: the reversal started at 1 | P1 81, P2 355, P3 359, P4 348, P5 357, P6 81 |
| M30 | solution: only the lower half tried | P1 4, P2 8, P4 21, P5 19, P6 4 |
| M31 | solution: only the last two digits reversed | P1 97, P2 238, P3 271, P5 294, P6 97 |


P1 and P6 kill all seventeen, P2 sixteen, P5 fifteen, and P3 and P4
fourteen each.

Fourteen are not kept. Ten fail exactly as a kept one: the ★ arm's
`num` itself never tried, the half arm's top never tried and the
template's 0 never tried (M1, M8, M27) as the iter arm's `num` itself
never tried (M22), each missing only `num = 0`, whose one way is
`0 + 0`; the table arm's place never grown (M13) as its new digit put
second (M12), both multiplying the new digit by 10 whatever the length;
the text arm's and the template's never reversed (M17, M28) as the ★
arm's each `k` added to itself (M6); the text arm's next `k` written and
the template's one more than `num` matched (M20, M29) as the ★ arm's one
more than `num` matched (M4); the iter arm's last two digits kept
together (M23) as the text arm's each reversal a tenth (M18), both
dropping the reversal's last digit; and the iter arm's digits summed
(M24) as the ★ arm's (M2). Four fail apart from every kept one and were
left out because those arms keep their share already: the ★ arm's every
other digit skipped and only the lower half tried (M3, M5), the half
arm's `k` ending in 0 never counted (M9), and the table arm's odd `num`
read at the even below (M16).

## Verification

Every arm prints the same output as `sum.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, half and table arms take 2.3 to 5.0 s,
the text arm 23 s, and the iter arm and the template, which make a
closure call for every `k`, 34 s and 35 s; under `karac
__mir-llvm-asan` the arms take 0.9 to 8.4 s, and under `karac run` 0.3
to 0.7 s. The differential takes 29 s under `karac __mir-run`, 7.3 s
under `karac __mir-llvm-asan` and 0.8 s under `karac run`.

## Benchmarks

The bench draws 400 values of `num` from `9 * 10^4` to `10^5`, the top
of the constraints, from its own generator, answers each and folds the
number, its verdict and its place into the checksum. The bench uses the
★ arm, every `k` tried with an arithmetic reversal, in all five
languages. Every implementation prints `400 nums near 10^5: checksum
886846723`.

BENCHTAB
