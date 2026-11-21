# 2437. Number of Valid Clock Times

You are given a string of length `5` called `time`, representing the
current time on a digital clock in the format `"hh:mm"`. The
**earliest** possible time is `"00:00"` and the **latest** possible time
is `"23:59"`.

In the string `time`, the digits represented by the `?` symbol are
**unknown**, and must be **replaced** with a digit from `0` to `9`.

Return *an integer* `answer`*, the number of valid clock times that can
be created by replacing every* `?` *with a digit from* `0` *to* `9`.

```
time = "?5:00"  ->  2      ("05:00", "15:00")
time = "0?:0?"  ->  100
time = "??:??"  ->  1440
```

**Constraints:** `time` is a valid string of length `5` in the format
`"hh:mm"`; `"00" <= hh <= "23"`; `"00" <= mm <= "59"`; some of the
digits might be replaced with `'?'` and need to be replaced with digits
from `0` to `9`.

The hour and the minute are chosen apart: no hour rules out a minute.
So the answer is the hours from 0 to 23 that fit the first two
characters times the minutes from 0 to 59 that fit the last two, at
most 84 checks; the arms differ in how literally they walk the day and
how much of the count they work out by hand.

## Approaches

| file | mechanism |
|---|---|
| `clock.kara` ★ | the hours that fit the first two characters times the minutes that fit the last two, a value fitting when each digit equals its character or meets a `?`, by a helper over a `Slice[u8]`. O(24 + 60) |
| `clock_naive.kara` | the statement read directly: every minute of the day written out by `f"{h:02}:{m:02}"` and compared with the pattern at every shown character. O(1440 * 5) |
| `clock_cases.kara` | by cases: the hour's choices from a `match` on which of its two characters are hidden, 24, 3 or 2, 10 or 4, or 1, and the minute's 6 and 10 multiplied. O(1) |
| `clock_digits.kara` | digit by digit: every digit a `?` may stand for, nested four deep, and the tuple counted when its hour is below 24 and its minute below 60. O(10^4) |
| `clock_iter.kara` | iterators: the hours and the minutes each by `filter` over their range, a value fitting by `zip` and `all` over its two digits and the pattern's two characters, and the counts by `count` multiplied. O(24 + 60) |
| `clock_solution.kara` | LeetCode's Rust template: the pattern as a `Vec<char>`, every minute of the day by `format!("{:02}:{:02}", h, m)`, and its characters `zip`ped with the pattern's under `all(\|(a, &b)\| b == '?' \|\| a == b)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples; no `?`
at all; each hour digit hidden on its own, the tens over 0 to 2 and the
units as the tens is 2 or not; each minute digit hidden on its own; and
3000 random valid times, each digit hidden half the time, as a checksum
and the total. `clock.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on every valid time with
every set of its digits hidden, 2926 patterns, against every minute of
the day compared with the pattern.

`check` first reports 5 errors on the template, and `karac fix` carries
it in one call, reporting 7 edits: the brackets of `Vec<char>`;
`format!("{:02}:{:02}", h, m)` written as the f-string `f"{h:02}:{m:02}"`,
the arguments moved into their places; the `&` of the pattern `&b`
dropped, since a Kāra pattern matches through a reference; `||` written
`or`; `struct Solution;` given its braces; and the harness wrapper's
`as i64` on the template's `i32` answer dropped, the widening being
implicit. `chars()`, `zip`, `all` and the `char` literals `'?'` stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to put a digit in each `?`, each filled string read
back as an hour and a minute, and counted when the hour is below 24 and
the minute below 60. No time of day is listed and no part is counted
apart. It checks 360 random valid times, each digit hidden half the
time, all drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | one more digit hidden: an answer no smaller |
| P3 | between 1, for the time the case was made from, and 1440 |
| P4 | the hour's count with the minute hidden, over 60, times the minute's with the hour hidden, over 24: the answer |
| P5 | the time the case was made from, nothing hidden: 1 |
| P6 | each arm agrees with at least three of the other five |

P2 holds because every time that fits a pattern still fits it with one
more digit hidden. P3 holds because the case is made by hiding digits of
a real time, which fits, and the day has 1440 minutes. P4 holds because
the hour and the minute are chosen apart, so the count with the minute
hidden is the hour's choices times 60, and likewise for the minute.

The differential prints `360 cases: checksum 767202159, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and fills every `?`. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: minutes to 59 | P1 127, P3 2, P4 358, P5 5, P6 127 |
| M3 | ★: the units digit never checked | P1 270, P5 360, P6 270 |
| M4 | ★: the hours and minutes added | P1 360, P4 360, P5 360, P6 360 |
| M7 | naive: each ? compared as itself | P1 345, P2 15, P3 345, P4 15, P6 345 |
| M10 | naive: one agreeing character enough | P1 274, P2 184, P3 29, P4 331, P5 360, P6 274 |
| M11 | naive: the last character never compared | P1 175, P5 360, P6 175 |
| M13 | cases: d? split at 1 | P1 47, P6 47 |
| M14 | cases: ?? as 23 | P1 82, P4 360, P6 82 |
| M15 | cases: the minute tens as 5 | P1 194, P4 360, P6 194 |
| M17 | digits: a ? standing for 1 to 9 | P1 345, P4 360, P6 345 |
| M18 | digits: hours up to 24 | P1 104, P3 29, P4 106, P6 104 |
| M19 | digits: the minute digits swapped | P1 199, P3 69, P5 159, P6 199 |
| M22 | iter: hours to 20 | P1 172, P3 31, P4 329, P5 65, P6 172 |
| M23 | iter: any digit enough | P1 331, P5 360, P6 331 |
| M24 | iter: the minute read from the hour | P1 264, P4 278, P6 264 |
| M27 | solution: minutes to 50 | P1 219, P3 25, P4 335, P5 53, P6 219 |
| M29 | solution: the hour and minute swapped | P1 281, P3 87, P4 175, P5 217, P6 281 |


P1 and P6 kill all seventeen, P4 twelve, P5 ten, P3 eight and P2 two.

Fourteen are not kept. Three fail exactly as a kept one: the ★ arm's
hours to 25 (M1) as the digits arm's hours up to 24 (M18), both letting
in the hour 24; the iter arm's `?` never matching (M26) as the naive
arm's each `?` compared as itself (M7), both matching only patterns with
nothing hidden; and the template's one character enough (M30) as the
iter arm's any digit enough (M23). Nine fail apart from every kept one
and were left out because those arms keep their share already: the ★
arm's hour read from the minute and `?` matching only 0 (M5, M6); the
naive arm's hours to 23 (M8); the cases arm's `?d` split at 3 and `2?`
as 3 (M12, M16); the digits arm's minute never checked and second hour
digit from the first (M20, M21); the iter arm's digits reversed (M25);
and the template's hours from 1 (M31).

One ends in an index out of bounds, not a wrong answer, under both
backends: the naive arm's time written without padding (M9) writes the
minute as `{m}0`, three characters for a minute of 10 or more, so the
written time is longer than the pattern it is compared with.

One survives, and is equivalent: the template's colon a wildcard only
(M28) lets a pattern's `:` match anything, but every pattern has its
`:` where every written time has one, so the extra case never decides.

## Verification

Every arm prints the same output as `clock.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 to 2.8 s, but for the naive
arm and the template, which write out every minute of the day for each
pattern: they take 70 s and 48 s there, 11 s and 9 s under `karac
__mir-llvm-asan`, and 0.9 s each under `karac run`. The differential
takes 77 s under `karac __mir-run`, 13 s under `karac __mir-llvm-asan`
and 1.2 s under `karac run`.

## Benchmarks

The bench builds every valid time with every set of its digits hidden,
1440 times by 16 masks, 23040 patterns, once. It then makes 120
passes; pass `p` answers every pattern in an order the pass shifts,
folding the answer plus the pass into the checksum. The bench uses the
★ arm, the hours times the minutes, in all five languages. Every
implementation prints `120 passes over 23040 patterns: checksum
12478189`. The patterns are strings in every language, in C
`malloc`ed and NUL-terminated.

BENCHTAB
