# 1154. Day of the Year

Given a string `date` representing a Gregorian calendar date formatted as
`YYYY-MM-DD`, return the day number of the year.

```
date = "2019-01-09"  ->  9
date = "2019-02-10"  ->  41
```

**Constraints:** `date.length == 10`; `date[4] == date[7] == '-'`, and all
other `date[i]`'s are digits; `date` represents a calendar date between
Jan 1st, 1900 and Dec 31st, 2019.

The arms are `fn day_of_year(date: Str) -> i64`.

## Approaches

The answer is the days of the months before the date's month, plus its
day of the month. A Gregorian year is a leap year, with a February of 29
days, when 4 divides it, unless 100 does, unless 400 does.

| file | mechanism |
|---|---|
| `day_of_year.kara` ★ | a table of the days before each month, plus the day, plus one from March on in a leap year; each field read by `i64.parse` of a slice of `date`. O(1) |
| `day_of_year_split.kara` | `date` split at its dashes, the months' lengths in an array with February set to 29 in a leap year, and those before the date's month added in a loop. O(1) |
| `day_of_year_bytes.kara` | the digits read straight from `date.bytes()`, each month's length from a formula (30 or 31 by the parity of `month + month / 8`, which flips at August; February apart), added in a loop. O(1) |
| `day_of_year_civil.kara` | a difference of day numbers: Howard Hinnant's `days_from_civil` for the date, less that for the first of January of its year, plus one. It counts the year from March, so the leap day falls last and needs no test of its own. O(1) |
| `day_of_year_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `date: String`, the fields parsed by `split('-').map(\|s\| s.parse().unwrap())` into a `Vec<i32>`, and the month lengths before the date summed over a slice with `iter().sum::<i32>()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples; the first
of March in a common and a leap year (60, 61); 1900's first of January,
last of February, first of March and last day (1, 59, 60, 365: 100
divides 1900, so it is no leap year); 2000's last of February, first of
March and last day (60, 61, 366: 400 divides 2000); 2016's leap day
(60); and 2019's last day (365). Then every date the constraints allow,
1900-01-01 to 2019-12-31, in order, each checked against a running
count that starts again at 1 on each first of January, with a checksum
(`43829 dates: 0 wrong, longest year 366 days, checksum 159001186`).
`day_of_year.py` mirrors the ★ arm and its output is byte-identical;
the same 43,829 dates read by Python's `datetime.date.timetuple().tm_yday`
give the same checksum.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, with the calendar as the rhyme and the Gregorian rule give it:
thirty days have September, April, June and November, February 28 or, in
a leap year, 29, and all the rest 31; a year is a leap year when 4
divides it, unless 100 does, unless 400 does. The literal answer is the
place of the date among the year's days, walked one at a time from the
first of January. It checks 4000 dates in four kinds of 1000: any date
the constraints allow; any date of a four-digit year (1 to 9999); a
first, last or second-to-last day of a month in a year that 100 divides,
where the leap rule's exceptions fall; and the first of January, the
last of February, the first of March or the last of December of any
four-digit year. The constraints stop at 2019, where only 1900 and 2000
test the exceptions; every arm reads any four-digit year, and the wider
years are what tell a rule that is right on those two from one that is
right everywhere. Every random choice the properties make is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the date after, by the harness's own month lengths, answers one more, or 1 after a 365 or a 366 |
| P3 | the same date 400 years on (or back, past 9999) answers the same: the calendar repeats every 400 years |
| P4 | within a month, the answer less the day does not change |
| P5 | the last of December answers 305 more than the first of March, in every year |
| P6 | a date in January answers its day, and one in February its day plus 31 |
| P7 | an earlier date of the same year answers less, and a later one more |

All 124,995 checks pass on every arm: `4000 dates: checksum 471572726,
124995 checks over 5 arms: 0 failures`. A Python reading of the same
dates by `datetime` gives the same line.

## Mutation testing

Thirty-one edits to the differential, six or seven to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run` with
`KARAC_HASH_SEED=1`, each failing the same way under both. All
thirty-one are caught, two of them by an out-of-bounds index (the tens
of the month dropped, and month and day swapped in the split arm).
Twenty-three are kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the leap day added in February too | P1 100, P2 65, P6 100 |
| M2 | ★: a year 400 divides not a leap year | P1 221, P2 10 |
| M3 | ★: `or` read as `and` in the leap rule | P1 736, P2 55 |
| M4 | ★: one day too many before August | P1 246, P2 73 |
| M5 | ★: the tens of the day dropped | P1 2610, P2 1208, P4 2610, P5 4000, P6 583, P7 153 |
| M6 | ★: the tens of the month dropped | index out of bounds |
| M7 | ★: every second year a leap year | P1 518, P2 69 |
| M8 | split: March given the leap day | P1 736, P2 132, P5 969 |
| M9 | split: January never added | P1 3471, P2 328, P6 470, P7 32 |
| M10 | split: counted from 0 | P1 4000, P2 292, P6 999 |
| M11 | split: June given 31 days | P1 1767, P2 101, P5 4000 |
| M12 | bytes: the 30/31 parity flips at September | P1 1263, P2 257, P5 4000 |
| M13 | bytes: the date's own month added | P1 4000, P2 887, P6 999, P7 5 |
| M14 | bytes: the thousands of the year dropped | P1 216, P2 11, P3 153 |
| M15 | bytes: the units of the day dropped | P1 4000, P2 3721, P4 3119, P5 4000, P6 999, P7 73 |
| M16 | bytes: March's length taken as February's | P1 3001, P2 531, P5 4000, P7 1 |
| M17 | civil: February counted in the year before | P1 470, P2 305, P6 470, P7 641 |
| M18 | civil: every fourth year a leap year | P1 858, P2 37, P7 1 |
| M19 | civil: the month table rounded the wrong way | P1 768, P2 171, P5 4000 |
| M20 | civil: the month read as the day | P1 3642, P2 4000, P4 3119, P5 4000, P6 695, P7 332 |
| M21 | solution: every second century year a leap year | P1 211, P2 8 |
| M22 | solution: every fourth year a leap year | P1 637, P2 22 |
| M23 | solution: February always 29 days | P1 2265, P2 214 |

P1 and P2 catch all twenty-nine edits that do not crash, P6 eleven, P5
and P7 ten, P4 four and P3 one. An edit to the leap rule is seen only by
P1 and P2: it is applied the same way to every date, so the answers stay
consistent with each other, and only the literal walk and the harness's
own month lengths hold the rule independently. P3, the 400-year cycle,
catches only the bytes arm reading three digits of the year (M14), the
one edit that does not keep the cycle. M14 changes no answer between
1900 and 2019, since 1900 and 900, and 2000 and 0, fall alike under the
rule; it is caught on the four-digit years alone (1000 is no leap year;
0 would be). The civil arm's era one day short fails exactly as M2: the
day numbers of a date and of its first of January cancel unless an era
boundary falls between them, which happens only after February in a
year 400 divides.

Of the eight caught and not kept, each fails exactly as a kept one: the
bytes arm refusing every year 100 divides and the civil arm's short era,
as M2; the split arm's `or` read as `and`, as M3; the split arm with
month and day swapped, as M6; the solution arm giving March the leap
day, as M8; the civil arm counting from 0, as M10; the solution arm
adding the date's own month, as M13; and the solution arm reading the
month as the day, as M20.

## Verification

Every arm prints the same output as `day_of_year.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file, and `karac fix` has nothing to apply.

The ★, split, bytes and civil arms were written as Kāra. `karac fix`
dropped the bytes arm's `as i64` on a byte difference added to an `i64`.
`karac fix` carried the solution arm in three rounds: `Vec<i32>` to
`Vec[i32]`, `&&` and `||` to `and` and `or`, the turbofish of
`sum::<i32>()` removed, the adapter's `&str` to `Str`,
`Solution::day_of_year` to `Solution.day_of_year` and its `as i64`
dropped; then `struct Solution {}` declared; then `split('-')` to
`split("-")`, `s.parse()` to `i32.parse(s)`, and the first literal of
`days` given the suffix `i32`.

The kata found two gaps, both in the solution arm's last round, each an
error left with no edit:

- `s.parse()` in the `map` closure took `map`'s own result parameter as
  its target, so the `Vec[i32]` that `collect` fills never reached it,
  and the error said only to name the type. The parse now follows the
  closure's result to the `Vec[i32]`, and the error offers `i32.parse(s)`,
  as it does when a later `let` names the type (B-2026-11-14-44,
  fixed).
- `days[..(m - 1) as usize].iter().sum() + d`, returned as an `i32`, was
  refused for narrowing an `i64` with only "write an explicit `as i32`",
  though `days.iter().sum() + d` names `days`, whose literals took the
  default `i64`, and offers the suffix `31i32`. A range of `days` now
  reads its elements as `days` does, and gets the same fix (B-2026-11-14-45,
  fixed).

## Benchmarks

`bench/` times the ★ arm against the same table in C, Rust, Go and
Python. Every date the constraints allow, 1900-01-01 to 2019-12-31, is
built once as a string; each of 1000 passes answers all 43,829 in turn,
adding the answers to a total and a checksum. Every program prints `1000
passes over 43829 dates: total 8026014000, checksum 356432303`. Each
reads the three fields as decimal numbers that refuse a non-digit: Rust
with `str::parse`, Go with `strconv.ParseInt`, Python with `int`, and C
with a digit loop that aborts on anything else.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `dba1dbedaf`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.212 to 0.341 s | 0.229 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.217 to 0.407 s | 0.229 s |
| Rust (`rustc -O`) | 0.216 to 0.441 s | 0.240 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.236 to 0.327 s | 0.250 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.239 to 0.334 s | 0.259 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.602 to 0.743 s | 0.631 s |
| Kāra (`karac build`) | 0.598 to 0.804 s | 0.634 s |
| Go | 1.252 to 1.448 s | 1.308 s |
| Python | 14.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` runs on one core too (user
time 0.651 s against 0.634 s), at the same speed. Kāra takes 2.4x
overflow-checked Rust's time, about 2.8x C's, and half Go's; Python takes
about 23x.

The gap is `i64.parse`. Counted with callgrind over 20 passes, setup
subtracted, the ★ arm spends 318 instructions a call and overflow-checked
Rust 125; the same Kāra reading the fields with a digit loop over
`date.bytes()`, as the bytes arm does, spends 110. So each of the three
parses costs about 70 instructions more than the loop. About 21 of them
are a walk over the slice's characters testing for Unicode whitespace,
the trim `parse` does at both ends; the rest go to the slice's checks
and to the `Option` and `Result` the answer passes through
(B-2026-11-14-43, open).
