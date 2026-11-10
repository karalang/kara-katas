# 2100. Find Good Days to Rob the Bank

You and a gang of thieves are planning on robbing a bank. You are given
a 0-indexed integer array `security`, where `security[i]` is the number
of guards on duty on the `i`th day. The days are numbered starting from
0. You are also given an integer `time`.

The `i`th day is a good day to rob the bank if:

- there are at least `time` days before and after the `i`th day,
- the number of guards at the bank for the `time` days before `i` are
  non-increasing, and
- the number of guards at the bank for the `time` days after `i` are
  non-decreasing.

More formally, day `i` is a good day if and only if `security[i - time]
>= security[i - time + 1] >= ... >= security[i] <= ... <= security[i +
time - 1] <= security[i + time]`.

Return a list of all days (0-indexed) that are good days to rob the
bank. The order that the days are returned in does not matter.

```
security = [5,3,3,3,5,6,2], time = 2   ->  [2,3]
security = [1,1,1,1,1], time = 0       ->  [0,1,2,3,4]
security = [1,2,3,4,5,6], time = 2     ->  []
```

**Constraints:** `1 <= security.length <= 10^5`; `0 <= security[i],
time <= 10^5`.

A day is good when the run of days that never rise ending at it and the
run of days that never fall starting at it are both at least `time`
long. Every arm returns the good days in increasing order, so all six
give the same list. They differ in how they measure the two runs.

## Approaches

| file | mechanism |
|---|---|
| `good_days.kara` ★ | two `Vec.filled` counts: the run before each day left to right, the run after it right to left over `(0..n - 1).rev()`; the days whose both reach `time` picked with `filter` over the range. O(n) |
| `good_days_prefix.kara` | prefix sums of the rises and of the falls in one pass; a day is good when the rises in the `time` days up to it and the falls in the `time` days after it are both zero, each one subtraction, over `time..n - time`. O(n) |
| `good_days_scan.kara` | the runs from iterator chains: `windows(2)` as pairs, `scan` keeping the running count, `once(0).chain(..)` for the first day, the same over the pairs reversed and turned round; the good days from `zip`, `enumerate` and `filter_map`. O(n) |
| `good_days_struct.kara` | a `struct Streaks` holding, for each day, the day of the last rise (or 0) and the day before the next fall (or the last day), with `before`, `after` and `good` methods. O(n) |
| `good_days_segments.kara` | the maximal stretches that never rise and that never fall, each found with nested `while` loops; inside a stretch the days with `time` quiet days behind (or ahead) are marked, and a day marked twice is good. O(n) |
| `good_days_solution.kara` | LeetCode's Rust template (`security: Vec<i32>`, `time: i32`): the run before each day in a `vec!`, then one walk back keeping the run after in a single counter, pushing the good days and reversing them at the end; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's three examples and four
more, each schedule with its answer; then how many good days 3000
random schedules of 1 to 30 days (of 0 to 3 guards, so that level days
are common, or of 0 to 10^5) have, each with a time of 0 to 5, and a
checksum of them; then the constraints' largest, 10^5 days of valleys
2000 days wide asked for five times, and 10^5 level days asked for
49999 and for 10^5. `good_days.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each day checked on its own, the `time` steps before it
never rising and the `time` steps after it never falling. It checks 300
random schedules of 1 to 12 days of 0 to 3 guards; then 20 valleys and
hills of 1 to 15 days, each side climbing 0 to 2 guards a day from a
random lowest (or highest) day; then 20 schedules of 1 to 12 days of 0
to 10^5 guards; each with a time of 0 to 4. All 340 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer goes up, and every day it names is good |
| P3 | the schedule reversed: the answer mirrored |
| P4 | one more day asked for (`time + 1`): an answer inside this one |
| P5 | each guard count replaced by its rank among the counts: the same answer |
| P6 | each arm agrees with at least three of the other five |

The transformed schedules stay within the constraints: a rank is at
most 14, and `time + 1` at most 5. The differential prints `340
schedules: checksum 606161085, 12240 checks over 6 arms: 0 failures`
under every lane in Verification; the checksum of the literal answers
was checked against a Python reading of the same schedules. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-eight edits to the differential, five or six to each arm and
then six more aimed at P4 and P5, which none of the first thirty-two
saw, each run under `karac __mir-llvm-run` and `karac __mir-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends
and not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: exactly `time` quiet days wanted before | P1 93, P3 101, P4 53, P6 93 |
| M2 | ★: the last day's run after never started | P1 34, P3 41, P6 34 |
| M3 | ★: the runs never reset | P1 47, P2 47, P3 75, P6 47 |
| M4 | prefix: a rise of one guard not counted | P1 35, P2 35, P3 54, P5 5, P6 35 |
| M5 | prefix: a fall counted as a rise | P1 69, P2 36, P3 60, P6 69 |
| M6 | prefix: the last day left out | P1 98, P3 97, P6 98 |
| M7 | scan: a rise of one guard let through | P1 77, P2 77, P5 12, P6 77 |
| M8 | scan: the run after never turned round | P1 72, P2 61, P3 71, P6 72 |
| M9 | scan: the first day given a run of one | P1 52, P2 52, P6 52 |
| M10 | struct: the fall's own day kept in the run | P1 53, P2 53, P3 74, P6 53 |
| M11 | struct: the run after never ending | P1 49, P2 49, P3 74, P6 49 |
| M12 | struct: only the run before asked | P1 121, P2 121, P3 154, P6 121 |
| M13 | segments: a time over 3 read as none | P1 74, P2 74, P4 76, P6 74 |
| M14 | segments: the days before a stretch's quiet ones marked | P1 118, P2 118, P3 154, P6 118 |
| M15 | segments: the stretch's last day left unmarked | P1 120, P3 101, P6 120 |
| M16 | solution: the adapter's guards halved | P1 51, P2 51, P5 22, P6 51 |
| M17 | solution: the answer never turned round | P1 96, P2 96, P6 96 |

P1 and P6 kill all seventeen, P2 thirteen, P3 twelve, P4 two and P5
three. P2 misses the edits that only leave good days out (M2, M6, M15)
or ask for more than the statement (M1): every day they name is still
good. P3 misses the edits that change both directions alike (M7, M9, M13,
M16, M17): the reversed schedule's answer is wrong in the mirrored
way, so the mirror still matches. P4 sees only an answer that
is not monotone in `time`, so only the edits that treat one time unlike
the next (M1 and M13). P5 sees only the edits that look at the size of
a step rather than its direction: a rise of one guard ignored (M4, M7)
and the halving that merges neighbouring counts (M16), all on the wide
schedules, where ranking shrinks every step to one.

Of the thirty-eight, twenty-one were not kept. Twelve fail the same way
as each other and were left out together: a level day breaking the run
before (★ by `<`, struct, segments, and the Rust arm, P1 42, P3 31, P6
42); the run after counting days that never rise (★, prefix's falls
looked for before the day, scan's steps backwards not swapped, and the
Rust arm, P1 67, P2 33, P3 60, P6 67); one day more wanted before (★
and struct, P1 123, P3 101, P6 123); either run enough (★) and a day
marked once enough (segments) (P1 154, P2 154, P6 154). Seven are
killed with checks of their own but were left out because their arm
keeps its share: prefix's level day counted as a fall, scan's level
step breaking the run and its run never reset, segments' next stretch
starting on the last one's end, and the Rust arm's adapter asking one
day more, run after never reset, and guards read backwards. One crashes
and is not kept: the prefix arm's window one day short, which at time 0
reads one past the end. One survives because it is equivalent: the
struct arm's run after one longer on day 0, which is good only when
`time` is 0 and then good either way.

## Verification

Every arm prints the same output as `good_days.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 1.4 s to 2.8 s, except the scan
arm at 13.2 s, whose closures run once per day through `scan`, `zip`
and `filter_map`; the differential takes 0.8 s (timed while other work
shared the machine).

No arm met a compiler gap.

`karac fix` carries the template in two rounds of 18 and 2 edits:
Rust's spellings (`Vec<i32>` to brackets, `&&` to `and`, `Solution::`
to `.`, `struct Solution;` to `struct Solution {}`, the closures' `&x`
patterns dropped, the adapter's `&Vec` to `ref Vec`); then `vec![0; n]`
to `Vec.filled(n, 0)`, and the adapter's `ref` parameter to a bare one,
which borrows already.

## Benchmarks

The bench asks 100 schedules of 10^5 days, the constraints' largest,
each a walk that moves by -1, 0 or +1 guards a day between 0 and 10^5,
each for a random time of 0 to 7, with the ★ arm in all five languages:
the run before each day counted left to right, the run after right to
left, and the good days collected. Every implementation prints `100
answers: 2306129 good days, checksum 771485866`.

BENCHTAB
