# 1360. Number of Days Between Two Dates

Write a program to count the number of days between two dates.

The two dates are given as strings, their format is `YYYY-MM-DD` as
shown in the examples.

```
date1 = "2019-06-29", date2 = "2019-06-30"  ->  1
date1 = "2020-01-15", date2 = "2019-12-31"  ->  15
```

**Constraints:** the given dates are valid dates between the years
`1971` and `2100`.

Each arm is `fn days_between_dates(date1: Str, date2: Str) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `days_between_dates.kara` ★ | each date as its count of days from 1971-01-01: the years before it and the months before it in its year added up, a leap year being one divisible by 4 but not by 100, or by 400; the answer is the two counts' distance. O(Y) for Y years |
| `days_between_dates_civil.kara` | each date's day number in closed form (Howard Hinnant's `days_from_civil`): the year taken to begin in March, so the leap day falls last, a 400-year era of 146097 days, and the day of the year from March (153 m' + 2) / 5 + d - 1. O(1) |
| `days_between_dates_walk.kara` | from the earlier date to the later one day at a time, the day rolled over at the end of its month and the month at the end of the year, the steps counted. O(D) for D days apart |
| `days_between_dates_table.kara` | the days before each year from 1971 and before each month of a common and of a leap year summed once into tables; a date's day number is then three lookups. O(Y) to build, O(1) for each date |
| `days_between_dates_solution.kara` | a Rust solution as LeetCode's Rust users write it (`fn days(date: &str) -> i32` nested in the method, `date.split('-').map(\|x\| x.parse().unwrap())`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, a date
against itself, the range's two ends, across the leap day of 2000 and
across the end of February 2100, which has none (`1 15 0 47481 2 1`);
and 2000 random pairs of dates folded into a checksum (`2000 random
pairs: 30848991 days in all, checksum 951826772`).
`days_between_dates.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the civil and table arms check clean. The ★ arm was
first written `date[0..4].parse_int()`; `karac check` answers that a
string has no `parse_int` and is parsed by the type it becomes,
`i64.parse(s)` (E0236), and the arm was rewritten to that by hand. The
walk arm's `let (mut at, end) = ..` becomes `let mut (at, end) = ..`
by `karac fix`. The Rust solution takes 13 fixes: the nested `fn days`
is lifted to the top level, `split('-')` becomes `split("-")`,
`x.parse()` becomes `i32.parse(x)`, `&str` becomes `Str`, `Vec<i32>`
becomes `Vec[i32]`, `&&` and `||` become `and` and `or`, the two `&`
arguments lose their sigil, and `struct Solution;` becomes `struct
Solution {}`. Every arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every day from 1971-01-01 to 2100-12-31 listed in
order, each the day after the last, and two dates' days apart the
distance of their places in the list. It checks LeetCode's examples,
the range's ends, the leap days of 1972, 2000 and 2096, the end of
February 2100, every year's last day against the next year's first,
and 2000 random triples of dates.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the dates swapped, the same days; a date and itself, none |
| P3 | through a third date, the days add up or one takes the other away |
| P4 | a date and the day after it, 1 |
| P5 | the same day a year later, 366 when a 29 February falls between them and 365 when none does |
| P6 | the ★ arm's days |

All 74,685 checks pass on every arm: `2136 cases: checksum 152079472,
74685 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python's `datetime`, on the same
dates, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every fourth year a leap year | P1 28, P4 1, P5 16, P6 112 |
| M2 | ★: a leap year's day added in January too | P1 742, P4 36, P5 945, P6 2968 |
| M3 | civil: February left in its own year | P1 297, P4 11, P5 94, P6 297 |
| M4 | civil: the months' lengths rounded up | P1 718, P4 146, P6 718 |
| M5 | walk: September given 31 days | P1 1983, P4 9, P5 2121, P6 1983 |
| M6 | walk: every February given 29 days | P1 1971, P4 1, P5 1600, P6 1971 |
| M7 | table: the leap day put at the end of March | P1 77, P4 4, P5 77, P6 77 |
| M8 | table: the leap and common rows swapped | P1 1198, P4 136, P5 851, P6 1198 |
| M9 | solution: the rule for 400 forgotten | P1 705, P5 23, P6 705 |
| M10 | solution: each month at the next one's length | P1 1093, P4 47, P6 1093 |

P1 and P6 kill all ten, P4 nine and P5 eight; P2 and P3 kill none. Every
arm but the walk numbers each date and takes the two numbers' distance,
and any such answer is the same both ways round and adds up through a
third date however wrong the numbering, while the walk's slips add the
same days whichever date it starts from; those two properties stand for
an arm that would measure its two dates differently. The day after (P4)
catches the edits that misplace a month's end or a leap day, at the
date where it does: 2100's 28 February alone for every fourth year a
leap year (M1), and the walk's 29 February in a common year (M6). It
misses the rule for 400 (M9), whose one wrong step, 29 February 2000 to
1 March, no case starts from. A year later (P5) misses the two edits
that move a day within every year alike: the months rounded up (M4) and
each month at the next one's length (M10).

## Benchmarks

The bench writes 1000 random dates once, then asks 3 * 10^5 questions,
each pair of dates drawn from the checksum so far, so no answer carries
over, answered by the ★ arm and folded into the checksum. Every
implementation prints `300000 questions: checksum 926321032`. The work
is reading three numbers out of each date and adding up the years
before it, about 65 of them on average, the same in every language.

BENCHTAB
