# 2409. Count Days Spent Together

Alice and Bob are traveling to Rome for separate business meetings.

You are given 4 strings `arriveAlice`, `leaveAlice`, `arriveBob`, and
`leaveBob`. Alice will be in the city from the dates `arriveAlice` to
`leaveAlice` (**inclusive**), while Bob will be in the city from the
dates `arriveBob` to `leaveBob` (**inclusive**). Each will be a 5-character
string in the format `"MM-DD"`, corresponding to the month and day of the
date.

Return *the total number of days that Alice and Bob are in Rome
together.*

You can assume that all dates occur in the **same** calendar year, which
is **not** a leap year. Note that the number of days per month can be
represented as: `[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]`.

```
"08-15", "08-18", "08-16", "08-19"   ->  3      (08-16 to 08-18)
"10-01", "10-31", "11-01", "12-31"   ->  0
```

**Constraints:** all dates are valid dates in `"MM-DD"`; Alice's and
Bob's arrival dates are **earlier than or equal to** their leaving dates.

The days together run from the later arrival to the earlier departure,
none if that is backwards. Because both fields are two digits, the
strings themselves sort as the dates do.

## Approaches

| file | mechanism |
|---|---|
| `days.kara` ★ | days of the year: each date's month and day read from its bytes, the days before its month from a table; the overlap `(last - first + 1).max(0)`. O(1) |
| `days_compare.kara` | string comparison: the later arrival and earlier departure picked as strings, and only then turned into days, the month and day by `parse` on slices, the months before summed in a loop; carried by `karac fix` |
| `days_calendar.kara` | a calendar: every day's "MM-DD" built in order, Alice's days marked in a `[false; 365]` by string comparison, then Bob's marked days counted. O(365) |
| `days_split.kara` | `split("-")`, each field parsed, the day of the year by a `while` over the months before; carried by `karac fix` |
| `days_iter.kara` | iterators: the fields by `split` and `map`, the months before by `take` and `sum`, the arrivals' `max` and departures' `min` over two-element arrays; carried by `karac fix` |
| `days_solution.kara` | LeetCode's Rust template: a closure `\|s: &String\| -> i32` reading the fields by `parse` on `s[..2]` and `s[3..]`, the months before by `days[..m - 1].iter().sum::<i32>()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; the whole
year twice; one shared day; Bob leaving the day Alice arrives; Alice the
whole year with Bob each month in turn; then 3000 random pairs of
stays, with a checksum and the total of the answers. `days.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
on 20000 random pairs of stays against walking every date of a non-leap
year with Python's `datetime`.

`days_compare.kara`, `days_split.kara` and `days_iter.kara` were first
written with `.parse()` on a string slice whose target only a later use
names; `check` reports E0236 there, since Kāra's `parse` takes its
target from an expected type, and `karac fix` writes `i64.parse(..)` in
one call each, in 2, 2 and 1 edits.

`check` first reports 8 errors on the template, and `karac fix`
carries it in one call, reporting 13 edits: the closure's `&String`
written `ref String`, and its `-> i32` moved to the binding as `let f:
Fn(ref String) -> i32 =`, since a Kāra closure names no return type;
the `::<i32>` turbofish on `sum` deleted and the month table's first
literal written `31i32`, which the turbofish had typed; the `&` of the
four arguments dropped; `struct Solution;` given its braces; and both
`.parse()` calls written `usize.parse(..)` and `i32.parse(..)`. At
first the closure's `-> i32` and the turbofish were deleted with
nothing put in their place, since the closure's tail is arithmetic
over a `sum` rather than the `sum` itself: the table defaulted to
`i64`, the closure returned `i64`, and the function's `i32` tail `(b -
a + 1).max(0)` was a narrowing `check` reported with no fix
(B-2026-11-21-41, fixed). The template was carried again after the
fix.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every day of the year as a (month, day) pair, each stay's
ends parsed into pairs, a day inside a stay when it lies between them
pair by pair, and the days inside both counted. No day numbers and no
string comparison. It checks 1000 random pairs of stays, a tenth of the
stays one day long. All 1000 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | Alice and Bob swapped: the same answer |
| P3 | Alice with herself: her stay's length; and the answer at most the shorter stay's length |
| P4 | Bob's stay cut after its first day: the two parts' answers sum to the whole's |
| P5 | both stays moved a day later, when both end before 12-31: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the days in both do not depend on whose they are, P3
because the days in both stays are days in each, P4 because the two
parts of Bob's stay share no day, and P5 because moving both stays
moves every shared day with them.

The differential prints `1000 cases: checksum 719096650, 36000 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and intersects the two stays as sets of day numbers. On a
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
| M4 | ★: the tens of the day ignored | P1 448, P3 657, P4 58, P5 163, P6 448 |
| M5 | ★: only the month read | P1 599, P3 895, P4 354, P5 49, P6 599 |
| M6 | ★: a gap counted as days together | P1 390, P3 301, P4 624, P6 390 |
| M7 | compare: the earlier arrival taken | P1 998, P3 678, P4 458, P6 998 |
| M9 | compare: each date's own month counted | P1 294, P3 522, P4 14, P5 38, P6 294 |
| M10 | compare: only the tens of the day read | P1 541, P3 890, P4 261, P5 128, P6 541 |
| M12 | calendar: Alice's last day missed | P1 303, P2 601, P3 1000, P6 303 |
| M13 | calendar: a 29 February in the calendar | P1 66, P3 253, P4 1, P5 3, P6 66 |
| M16 | calendar: 1 January never marked | P3 5 |
| M18 | split: every month 30 days | P1 400, P3 736, P4 12, P5 27, P6 400 |
| M19 | split: a one-day overlap missed | P1 49, P3 84, P4 289, P6 49 |
| M21 | split: the month read as the day | P1 593, P3 891, P4 354, P5 49, P6 593 |
| M22 | iter: each date's own month counted | P1 294, P3 522, P4 15, P5 39, P6 294 |
| M24 | iter: a gap counted as one day | P1 396, P4 626, P6 396 |
| M25 | iter: the day halved | P1 530, P3 870, P4 149, P5 284, P6 530 |
| M29 | solution: each stay one day short | P1 604, P3 1000, P4 289, P6 604 |
| M31 | solution: the later departure taken | P1 997, P3 651, P4 746, P6 997 |

P1, P3 and P6 kill sixteen each, P4 fifteen, P5 nine, and P2 one. P2
swaps Alice and Bob, so it catches only a mutant that treats them
apart: the calendar arm's Alice's last day missed (M12). The calendar
arm's 1 January never marked (M16) fails only P3, which sets a stay
against itself, so one starting on 1 January comes out a day short;
the random pairs of P1 rarely both hold that day.

Of the thirty-one, fourteen were not kept, each failing the same checks
as a kept one or, for three, left over: the ★ arm's each stay one day
short (M2) as the template's (M29); the earlier arrival taken in the ★,
iter and template arms (M3, M23, M28) as the compare arm's (M7); the
compare arm's one-day overlap missed (M8) as the split arm's (M19); the
later departure taken (M11, M26) as the template's (M31); each date's
own month counted in the split arm and template (M17, M27) as the iter
arm's (M22); the split arm's day ignored (M20) as the ★ arm's only the
month read (M5); and the template's only the units of the day read
(M30) as the ★ arm's tens of the day ignored (M4). The ★ arm's March
given a day more (M1) and the calendar arm's a day in either stay
counted (M14) and months written unpadded (M15) fail apart from every
kept one, and were left out because those arms keep three already.

## Verification

Every arm prints the same output as `days.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.36 to 0.73 s, except the
calendar arm at 5.4 s. The differential takes 15 s there, 4.1 s under
`karac __mir-llvm-asan` and 1.1 s under `karac run`.

## Benchmarks

The bench builds every day's "MM-DD" and `10^5` random pairs of stays
as indexes into them, once from the harness's generator, then makes 100
passes, answering every pair and folding each answer plus the pass into
the checksum, with the ★ arm in all five languages. Every implementation
prints `100 passes over 10^5 pairs of stays: checksum 902129352`. Kāra
builds the table of days before each month as a local array in every
call, as the ★ arm writes it, and reads each date through `bytes()`; C,
Rust and Go read a constant table and index the string's bytes in
place, and Python a module-level list.

BENCHTAB
