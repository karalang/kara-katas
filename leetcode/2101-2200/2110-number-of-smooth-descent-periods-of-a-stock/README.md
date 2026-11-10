# 2110. Number of Smooth Descent Periods of a Stock

You are given an integer array `prices` representing the daily price
history of a stock, where `prices[i]` is the stock price on the `i`th
day.

A smooth descent period of a stock consists of one or more contiguous
days such that the price on each day is lower than the price on the
preceding day by exactly 1. The first day of the period is exempted
from this rule.

Return the number of smooth descent periods.

```
prices = [3,2,1,4]   ->  7
prices = [8,6,7,7]   ->  4
prices = [1]         ->  1
```

**Constraints:** `1 <= prices.length <= 10^5`; `1 <= prices[i] <=
10^5`.

A period ending on a day is that day alone, or a period ending the day
before extended by it, which is possible exactly when the price fell by
one. So the periods ending on each day number the length of the descent
run up to it, and the answer is their sum. At the constraints' largest,
one descent of 10^5 days, it is 5000050000, past `i32`, which is why
LeetCode's signature returns `i64`.

## Approaches

| file | mechanism |
|---|---|
| `descent.kara` ★ | the run length up to each day in a `for` over the places, reset to 1 at a break, added to the total. O(n) |
| `descent_runs.kara` | whole runs: each maximal descent found with two indices in nested `while`s, adding `len * (len + 1) / 2` |
| `descent_scan.kara` | one chain: `windows(2).iter()`, `scan` carrying the run length to each later day as `Some((next, next))`, and `sum`, plus the first day |
| `descent_table.kara` | `ending[i]`, the periods ending on day `i`, in a `Vec.filled(n, 1)`, each one more than the day before's after a fall of one, summed with `iter().sum()` |
| `descent_struct.kara` | a `struct Streak` of the last price, the run and the total, its `see` method (`mut ref self`) extending or restarting the run, started by `Streak.new(prices[0])` |
| `descent_solution.kara` | LeetCode's Rust template (`Vec<i32>` to `i64`): `chunk_by(\|a, b\| a - b == 1)` into maximal descents, each adding `len * (len + 1) / 2` through `map` and `sum`, carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (one long descent, a rise, a repeated price splitting a descent),
each with its answer; then the total for 3000 random arrays of 1 to 40
prices from 1 to 5, and a checksum of the answers; then the constraints'
largest, 10^5 prices: one descent from 10^5 to 1, and a saw of descents
of 1000 each. `descent.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every first and last day, each step between them checked to
fall by exactly one. It checks 300 random arrays of 1 to 10 prices from
1 to 4; then 30 of up to 120 prices from 1 to 3; then 30 of up to 120
that fall by one at each step and jump up otherwise, 15 with odds of
four in five for a fall and 15 with odds of 59 in 60, so that runs of
more than 50 days occur. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least `n` and at most `n * (n + 1) / 2` |
| P3 | every price raised by 7: the same answer |
| P4 | the prices reversed, each `p` made `200000 - p`: the same answer |
| P5 | a price 5 above the last appended: the answer plus one |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 arrays: checksum 644876944, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
arrays. On a failure it prints the first ten and then the count by
property.

The last 15 arrays were added after the first run of the mutations: the
runs arm's descents split at 50 days survived, since with odds of four
in five for a fall no array held a run that long.

## Mutation testing

Thirty-five edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a day after a break not counted | P1 312, P2 278, P4 94, P5 360, P6 312 |
| M3 | ★: the first day not counted | P1 360, P2 150, P6 360 |
| M5 | ★: a flat or rising step taken for a descent | P1 302, P5 360, P6 302 |
| M7 | runs: every run at least two days | P1 337, P2 37, P4 39, P5 360, P6 337 |
| M8 | runs: the day after each run skipped | P1 312, P2 259, P4 109, P5 212, P6 312 |
| M31 | runs: descents split at 50 days | P1 5, P6 5 |
| M12 | scan: the run starting from nothing | P1 72, P4 94, P6 72 |
| M32 | scan: a step of one up extending the run | P1 202, P6 202 |
| M33 | scan: runs capped at 20 days | P1 13, P6 13 |
| M16 | table: a run's day counted as the one before | P1 210, P6 210 |
| M34 | table: runs capped at 10 days | P1 22, P6 22 |
| M35 | table: the last day's step never checked | P1 75, P4 94, P5 75, P6 75 |
| M21 | struct: the first price kept as the last | P1 200, P4 154, P6 200 |
| M24 | struct: the second price never seen | P1 297, P2 138, P4 144, P5 37, P6 297 |
| M25 | struct: a break keeping the run | P1 177, P4 179, P5 210, P6 177 |
| M27 | solution: each run one short | P1 360, P2 314, P5 360, P6 360 |
| M28 | solution: the prices halved | P1 217, P3 198, P4 198, P6 217 |

P1 and P6 kill all seventeen, P4 nine, P5 eight, P2 six and P3 one. P4
sees the edits that treat the two ends of the array differently: a
first or last step skipped (M12, M35), the first price kept (M21), the
second dropped (M24), and the edits whose error depends on where a run
starts (M2, M7, M8, M25, M28). P5 sees the edits that count a lone last
day wrongly or let a rise extend a run (M2, M5, M7, M8, M25, M27, M35),
and the struct arm's dropped second price (M24). P2 sees the edits that
fall below one period a day (M2, M3, M8, M24, M27) or above one per
pair of days (M7). P3 sees only the Rust adapter's halved prices (M28):
no other edit reads a price's value, only the difference of two, which
raising them all keeps. The caps and the split (M31, M33, M34) only show
on runs longer than they allow, which P1 alone counts.

Of the thirty-five, eighteen were not kept. Every one is killed and none
survives. Four fail alike as rises counted for falls, P1 231, P6 231:
the ★ arm's, the runs arm's, the table arm's and the Rust arm's. Five
fail as M16, P1 210, P6 210: four give the answer `n`, as M16 does (the
★ and struct arms' day counted once, the runs arm's run's days counted
once, the scan arm's later days counted once), and the scan arm's any
fall taken for a step of one fails with the same counts. The first day not counted in the scan,
table and struct arms fails as M3, the scan arm's day after a break as
M2, and the table arm's second day's step never checked as M12. The
runs arm's single days not counted and the table arm's no day alone
counted fail alike, P1 360, P2 329, P5 360, P6 360. Two are killed with
checks of their own but were left out because their arm keeps its
share: the Rust arm's runs squared (P1 210, P2 14, P6 210) and its first
price dropped (P1 360, P2 169, P4 94, P6 360).

## Verification

Every arm prints the same output as `descent.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.7 s to 1.6 s, and the
differential 1.4 s; compiled it takes 0.4 s.

`karac fix` carries the template in three rounds of 8, 1 and 2 edits:
Rust's spellings (`Vec<..>` to brackets, `struct Solution;` to `struct
Solution {}`, the adapter's `&Vec` to `ref`, its `|&p|` to `|p|` and
`Solution::` to `.`); then `.iter()` after `chunk_by(..)`, which in Kāra
gives a `Vec` of the runs rather than an iterator; then `run.len() as
i64` to `run.len()`, already an `i64`, and the adapter's `ref` parameter
to a bare one. The scan arm met the same `.iter()` fix after
`windows(2)`.

## Benchmarks

The bench builds 20 arrays of 10^5 prices once, each falling by one
with odds of three in four and jumping up by 0 to 19 otherwise; it then
counts each 10 times, raising one price by one before each count so no
count repeats the one before, with the ★ arm in all five languages: the
run up to each day. Every implementation prints `200 counts: 80017237
periods, checksum 750850884`.

BENCHTAB
