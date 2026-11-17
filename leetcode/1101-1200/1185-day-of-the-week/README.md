# 1185. Day of the Week

Given a date as three integers `day`, `month` and `year`, return its day of
the week, one of `"Sunday"`, `"Monday"`, `"Tuesday"`, `"Wednesday"`,
`"Thursday"`, `"Friday"`, `"Saturday"`.

```
day = 31, month = 8, year = 2019  ->  "Saturday"
day = 18, month = 7, year = 1999  ->  "Sunday"
day = 15, month = 8, year = 1993  ->  "Sunday"
```

**Constraints:** the date is a valid date between 1971 and 2100.

The arms are `fn day_of_the_week(day: i64, month: i64, year: i64) ->
String`. The two Rust arms keep the method LeetCode gives Rust users, over
`i32`, inside `impl Solution`, and a one-line `day_of_the_week` calls it.

## Approaches

1 January 1971 was a Friday, so counting the days from it names any later
date; a formula over the Gregorian calendar names it directly.

| file | mechanism |
|---|---|
| `day_of_the_week.kara` ★ | the days from 1 January 1971 counted (whole years, whole months of the date's year with its leap day, then the day), and that many days on from Friday. O(year - 1971) |
| `day_of_the_week_zeller.kara` | Zeller's congruence: January and February counted as months 13 and 14 of the year before, so the leap day falls at the end of the year, then one formula in the day, the month, the year within its century and the century. O(1) |
| `day_of_the_week_sakamoto.kara` | Sakamoto's method: a table of each month's offset, the year taken one back before March, the leap days counted as `y / 4 - y / 100 + y / 400`. O(1) |
| `day_of_the_week_solution.kara` | a Rust solution as LeetCode's Rust users write it (the days counted from 1971 with an `is_leap` closure, the months walked over `0..(month - 1) as usize`, the name indexed with `as usize`), carried to Kāra by `karac fix` |
| `day_of_the_week_chain.kara` | another Rust solution, one expression (`(1971..year).map(..).sum::<i32>()` for the years, the month table's `iter().take(..).sum::<i32>()`, a leap day and the day, the name indexed out of an array literal), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; the range's
first and last days (`first day: Friday`, `last day: Friday`); 29 February
2000, a leap day in a century year divisible by 400 (`Tuesday`); 1 March
2100, after the 28 February of a century year that is not a leap year
(`Monday`); 29 February 1972, the range's first leap day (`Tuesday`); and
3000 random dates (`3000 random dates: checksum 380580623`).
`day_of_the_week.py` mirrors the ★ arm and its output is byte-identical;
it also checks every answer, and every one of the 47,482 days from 1971 to
2100, against Python's own calendar (`datetime.date.weekday`). Every arm
gives the same output under `karac run` and `karac build`.

The Mend loop: the ★, Zeller and Sakamoto arms take no fixes. The solution
arm takes one round of 5 (`struct Solution;` to `struct Solution {}`, `&&`
to `and` twice, `||` to `or`, `Solution::` to `Solution.`) and its output
matches. The chain arm takes 9 in its first round, the same, its two
`as usize` casts to `as i64` and its two `sum::<i32>()` turbofishes
removed, and was then refused with no fix (the
gap below); with the fix, one more round of 2 writes `366i32` and `31i32`
and its output matches.

## Gap

**A sum over literals got no reason and no fix.** With its turbofishes
removed, the chain arm reads `let days: i32 = (1971..year).map(|y| if
leap(y) { 366 } else { 365 }).sum() + [31, 28, ..].iter().take(month as
i64 - 1).sum() + if month > 2 and leap(year) { 1 } else { 0 } + day`. It
was refused with "implicit coercion from 'i64' to 'i32' would narrow or
change sign" and the advice to write `as i32`. The refusal is right: the
closure's literals and the month table's meet the `i32` `day` only through
`+`, so they keep the `i64` default (design.md §8 Literals). But nothing
said so, and the turbofish fix's own advice, to annotate the binding, was
already followed. Now a `sum` or `product` over a closure's literal result
or over an array of literals names them, "the `sum` is an 'i64' because
the literals its closure returns took the default (design.md §8 Literals);
write `366i32`, which types the closure's other literals too", and `karac
fix` writes it, then `31i32` for the table. kara B-2026-11-17-99.

The differential's first draft took 8 fixes in one round: `[Str; 7]` to
`Array[Str, 7]`, `let (mut d, mut m, mut y)` to `let mut (d, m, y)`, and
`!` to `not`.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the calendar turned a day at a time from 1 January 1971, a
Friday, until it shows the date, naming each day after the one before. 300
random dates from 1971 to 2100; the first ten are 29 February of a leap
year and the next ten the last day of a month.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the answer names a day of the week |
| P3 | seven days later is the same day, and the next day the next name |
| P4 | the first of the next month is the rest of this month on |
| P5 | a year later is 365 days on, or 366 past a 29 February |
| P6 | the ★ arm's answer |

All 9,690 checks pass on every arm: `300 dates: checksum 206171619, 9690
checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac run` and
`karac build`.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All ten
are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: February's leap day counted in February | P1 13, P4 19, P5 9, P6 52 |
| A2 | ★: the count starts a year early | P1 300, P6 1200 |
| Z1 | Zeller: `13 * m / 5` for `13 * (m + 1) / 5` | P1 300, P4 166, P6 300 |
| Z2 | Zeller: only January moved to the year before | P1 38, P4 66, P5 9, P6 38 |
| S1 | Sakamoto: the year never taken back | P1 66, P4 38, P5 24, P6 66 |
| S2 | Sakamoto: December's offset one too many | P1 27, P4 17, P6 27 |
| X1 | solution: the leap day added after March | P1 5, P4 18, P5 13, P6 5 |
| X2 | solution: the week started a day late | P1 300, P6 300 |
| R1 | chain: the date's own month counted whole | P1 262, P4 247, P6 262 |
| R2 | chain: the leap day counted from February | P1 13, P4 19, P5 9, P6 13 |

A mutation of the ★ arm fails P6 on every arm. A2 and X2 move every date
by the same number of days, so only P1 and P6 see them. P4 and P5 catch
the faults that put a month or a leap day in the wrong place. A1 and R2
are the same fault in two arms and fail the same checks. P2 and P3 catch
none: every fault here moves a whole month or more at once.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 10000 random dates from 1971 to 2100, built once, then 100 rounds
naming every one, each name's length and first letter folded into a
checksum. Every program prints `100 rounds of 10000 dates: checksum
900479054`. Each returns a fresh string, as Kāra's and Rust's `String` do:
C with `strdup` and `free`, Go with `strings.Clone`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `2a5724c2d4`
and kata 1186's two fixes, on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.147 to 0.161 s | 0.151 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.146 to 0.219 s | 0.153 s |
| Rust (`rustc -O`) | 0.115 to 0.136 s | 0.118 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.124 to 0.156 s | 0.129 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.126 to 0.181 s | 0.129 s |
| C (`clang -O3`) | 0.129 to 0.180 s | 0.132 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.138 to 0.181 s | 0.140 s |
| Go | 0.137 to 0.175 s | 0.141 s |
| Python | 6.90 to 6.99 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 4% of wall time for both Kāra
rows, so both ran on one core. Kāra takes about 1.19x the time of
overflow-checked Rust, the equal-safety comparison, 1.16x C's and 1.09x
Go's; Python takes about 45x Kāra's. The work is the year loop, 65 years
a date on average, each a leap-year test, and one small string a date;
where Kāra's time over Rust's goes was not profiled.
