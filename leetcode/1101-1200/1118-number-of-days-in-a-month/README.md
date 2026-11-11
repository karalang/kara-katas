# 1118. Number of Days in a Month

Given a year `year` and a month `month`, return the number of days of
that month.

```
year = 1992, month = 7  ->  31
year = 2000, month = 2  ->  29
year = 1900, month = 2  ->  28
```

**Constraints:** `1583 <= year <= 2100`; `1 <= month <= 12`.

The arms are `fn number_of_days(year: i32, month: i32) -> i32`. 1583 is
the first full year of the Gregorian calendar, so a year is a leap year
when 4 divides it and 100 does not, or when 400 does.

## Approaches

| file | mechanism |
|---|---|
| `number_of_days.kara` ★ | a `match` on the month: February 29 days in a leap year and 28 otherwise, April, June, September and November 30, every other month 31. O(1) |
| `number_of_days_table.kara` | a `const` table of the twelve months' days in a common year, read at the month, with one more day for February in a leap year. O(1) |
| `number_of_days_civil.kara` | the days between the first of the month and the first of the next, each counted from 1 March of year 0 as Howard Hinnant's `days_from_civil` counts them: the year taken to start in March, so February's leap day falls last, and a month's start `(153 * m + 2) / 5` days in. O(1) |
| `number_of_days_bits.kara` | the twelve lengths packed two bits a month into one number, each month's days less 28, read with a shift and a mask; February's bits are 0, and a leap year adds one. O(1) |
| `number_of_days_scan.kara` | the days of the year before each month, as a running total of the months' lengths taken with `scan` after a `0` chained in front, and the month's days the gap between its start and the next one's, written as Rust writes it. O(1), a table of 13 a call |
| `number_of_days_solution.kara` | a Rust solution as LeetCode's Rust users write it: `impl Solution` with a `match` on the month and the leap test inline, carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples, the twelve
months of 2023, 2024, 2100, 1583 and 1600, and over every month from
1583 to 2100 the days summed, the leap years counted and a checksum
(`1583 to 2100: 189196 days, 126 leap years, checksum 912221462`).
`number_of_days.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a month runs from its first day to the day before the next
month's first, so it has 28 days and as many more as the weekday moves
on from one first to the next, each weekday by Zeller's congruence. It
checks every month of every year LeetCode allows, 6216 problems, each
with a second year drawn at random from the same span for P4.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | by a second reading, the year: the month 28 to 31 days, 30 only in April, June, September and November, and the twelve months making 366 days in a leap year and 365 in any other |
| P3 | 400 years on, the month is as long |
| P4 | a month other than February is as long in any year |
| P5 | March to December mirror about the turn of July and August: month `m` is as long as month `15 - m` |
| P6 | 28 years on, with no century year from now to then that 400 does not divide, the month is as long |

All 206,100 checks pass on every arm: `6216 problems: checksum
912221462, 206100 checks over 6 arms: 0 failures`. Python's
`calendar.monthrange` over the same months gives the same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Twenty-three are kept, no two failing
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every fourth year a leap year | P1 4, P2 48 |
| M2 | ★: no century year a leap year | P1 2, P2 24, P6 3 |
| M3 | ★: November given 31 days | P1 518, P2 6216, P5 1036 |
| M4 | ★: August given 30 days and September 31 | P1 1036, P2 1036, P5 2072 |
| M5 | ★: the next year's leap day | P1 252, P2 3024, P6 4 |
| M6 | table: each month read from the next one's slot | P1 5180, P2 4270, P5 2072 |
| M7 | table: a leap year adds a day to every month | P1 1386, P2 1512, P4 2090 |
| M8 | table: 200 in place of 400 | P1 1, P2 12 |
| M9 | table: every eighth year a leap year | P1 62, P2 744, P6 98 |
| M10 | civil: January and February counted in their own year | P1 1036, P2 3556, P4 197, P5 1036, P6 4 |
| M11 | civil: no century day dropped | P1 6, P2 72, P6 3 |
| M12 | civil: the month-start formula rounded the other way | P1 2072, P2 2072, P5 4144 |
| M13 | civil: December measured to the same year's January | P1 518, P2 6216, P4 195, P5 1036 |
| M14 | civil: the year of the era one on | P1 248, P2 2976, P6 10 |
| M15 | bits: February's pair 1, not 0 | P1 518, P2 6216 |
| M16 | bits: the mask keeps one bit | P1 5698, P2 6216 |
| M17 | bits: each month read from the previous one's pair | P1 5698, P2 6216, P5 2072 |
| M18 | scan: each month a day long | P1 6216, P2 6216 |
| M19 | scan: each month's start handed out, not its end | P1 5698, P2 6216, P4 198, P5 2072 |
| M20 | solution: August falling to February's arm | P1 518, P2 6216, P4 176, P5 1036 |
| M21 | solution: September falling to February's arm | P1 518, P2 6216, P4 194, P5 1036 |
| M22 | solution: 300 in place of 400 | P1 4, P2 48, P3 4, P6 3 |
| M23 | solution: 10 in place of 100 | P1 20, P2 240, P6 33 |

P1 and P2 catch all twenty-three, P5 ten, P6 eight, P4 six and P3 one.
The problems are every input LeetCode allows, so a small count is all
the inputs on which an edit differs: taking 200 for 400 (M8) changes
only February 1800. P2 asks for each month of the year at once, so it
fails on twelve problems where P1 fails on one. P5 sees the edits that
break the pattern of long and short months from March on, P4 the ones
that make a month other than February depend on its year, and P6 the
leap rules that go wrong within 28 years, as for 1900 and 2100. P3 is
the weakest: the edits to the leap rule keep a 400-year cycle, so only
taking 300 for 400 (M22) fails it.

Of the seven not kept, all fail as a kept edit: the bits arm taking
every fourth year as M1, the scan arm taking no century year as M2, the
scan arm giving December a day too many as M3, the table, bits and scan
arms swapping two months' lengths as M4, and the solution arm swapping
leap and common Februaries as M15. Three edits written first were
dropped as not edits at all: a stray bit below January's pair, which no
month's shift reaches; every date in the civil arm one era on, and every
running total in the scan arm a day ahead, both of which cancel in the
difference.

## Verification

Every arm prints the same output as `number_of_days.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file, and `karac fix` has nothing to apply.

The kata found three gaps, all fixed. The ★, table, civil and bits arms
were written as Kāra, the scan and solution arms as Rust writes them.
`karac fix` carried the table's `[i32; 12]` to `Array[i32, 12]` in two
rounds and the solution in three (`&&` and `||` to `and` and `or`,
`struct Solution {}` declared, `Solution::` to `Solution.`). In the
harness each arm shares, it gave the loop's year list an `i32` suffix
and took out two `as i64` casts. The
gaps were all in the scan arm's integer literals. The month lengths
`[31, if leap { 29 } else { 28 }, ..]` were typed `i64` at once because
of the `if` among them (B-2026-11-11-38); `[0].into_iter().chain(..)`
collected into a `Vec[i32]` was refused with no fix
(B-2026-11-11-41); and the `scan`'s state `0` settled to `i64` before
the `collect` that would fix it (B-2026-11-11-61). The arm is as first
written.

## Benchmarks

The bench draws 10^6 months once from LeetCode's years, 1583 to 2100,
and asks for them again in each of 40 rounds with the ★ arm, each call's
year moved by the last answer so no call can start before the one before
it ends: 4 * 10^7 calls.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `628eb9974d`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.188 to 0.224 s | 0.219 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.189 to 0.275 s | 0.220 s |
| Rust (`rustc -O`) | 0.190 to 0.229 s | 0.224 s |
| Kāra (`karac build`) | 0.201 to 0.250 s | 0.230 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.201 to 0.284 s | 0.233 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.200 to 0.270 s | 0.233 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.202 to 0.278 s | 0.234 s |
| Go | 0.283 to 0.342 s | 0.323 s |
| Python | 5.710 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` parallelizes nothing here
(its user time equals its wall time). Kāra, C and Rust are within 7% of
each other, the spread of their runs, with Kāra's overflow checks on as
in the checked Rust rows. Go takes about 1.4x their time. Python takes
about 24x Kāra's time.
