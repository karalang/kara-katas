# 1335. Minimum Difficulty of a Job Schedule

You want to schedule a list of jobs in `d` days. Jobs are dependent
(i.e. to work on the `i`-th job, you have to finish all the jobs `j`
where `0 <= j < i`). You have to finish at least one task every day. The
difficulty of a job schedule is the sum of difficulties of each day of
the `d` days. The difficulty of a day is the maximum difficulty of a job
done on that day. You are given an integer array `jobDifficulty` and an
integer `d`. Return the minimum difficulty of a job schedule. If you
cannot find a schedule for the jobs return `-1`.

```
jobDifficulty = [6,5,4,3,2,1], d = 2  ->  7
jobDifficulty = [9,9,9], d = 4        ->  -1
jobDifficulty = [1,1,1], d = 3        ->  3
```

**Constraints:** `1 <= jobDifficulty.length <= 300`, `0 <=
jobDifficulty[i] <= 1000`, `1 <= d <= 10`.

The arms are `fn min_difficulty(job_difficulty: Vec[i32], d: i32) ->
i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_difficulty.kara` ★ | the least difficulty of the first i jobs in so many days, one day at a time; a day ending after job i starts at each earlier place j, walked back so the day's hardest job is kept as it grows. O(d n^2) |
| `min_difficulty_stack.kara` | the same days, each in one pass with a stack of the jobs harder than every later one so far, each carrying the least cost of the days before a day it heads; a job pops the easier ones, takes over their costs, and can extend the day of the harder job below it. O(d n) |
| `min_difficulty_memo.kara` | top-down: the least difficulty of the jobs from `start` on in `days` days, each day ending at every place that leaves a job for each day after it, remembered in a `Map` keyed by (start, days). O(d n^2) |
| `min_difficulty_scan.kara` | the ★ arm's cells each found by an iterator: the places a day can start walked back with `rev`, the hardest job so far carried by `scan`, the least total taken by `min`. O(d n^2) |
| `min_difficulty_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `vec![vec![i32::MAX; n + 1]; d + 1]` table indexed by `usize`, inclusive ranges `k..=n`, and the running hardest job and each cell kept with `.max(..)` and `.min(..)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples, one job,
and two jobs of difficulty 0 in one day (`7 -1 3 7 0`); 300 jobs, the
constraints' most, in 10 days and in 1, and 300 jobs rising by 3 in 10
days (`300 jobs: 3625 998, rising 1005`); and 300 random schedules of 1
to 300 jobs, most of them short, with difficulties up to 5 or 1000 and 1
to 10 days (`300 random schedules: 78 impossible, checksum 804834236`).
`min_difficulty.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run` and
`karac __mir-llvm-run`.

The Mend loop: the ★ and stack arms check clean. The memo arm draws a
warning for `d as i64`, a cast an `i32` does not need on its way to an
`i64`, and `karac fix` drops it. The scan arm was first written with
Rust's `scan`, whose closure writes its state in place (`*hardest =
max(*hardest, ..)` and `Some(best[j] + *hardest)`); `check` refused it,
saying Kāra's `scan` closure takes its state by value and returns
`Some((next_state, item))`, and `karac fix` rewrote the closure that way
(`let hardest = max(hardest, ..)` and `Some((hardest, best[j] +
hardest))`). The Rust arm takes one round of 12 fixes by `karac fix`'s
count, from 6 errors: `struct Solution;` to `struct Solution {}`, each
`Vec<..>` to `Vec[..]`, `usize` to `i64`, `vec![vec![x; n + 1]; d + 1]`
to `Vec.filled(d + 1, Vec.filled(n + 1, x))`, `i32::MAX` to `i32.MAX`,
`let mut mx = 0;` annotated `i32`, and `Solution::` to `Solution.`. Its
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to cut the jobs, in order, into d days of at least
one job each, chosen as d - 1 of the n - 1 places between two jobs; each
day's hardest job summed and the least sum kept, or -1 when there are
fewer jobs than days. 2000 schedules of 1 to 8 jobs in 1 to 9 days, in
four kinds, 500 each: difficulties from 0 to 2; from 0 to 1000; every
job alike; and rising or falling by 0 to 5 from a start up to 50. Every
schedule and amount is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the jobs in the other order: the same answer |
| P3 | every difficulty raised by one amount up to 1000: the answer raised by that amount for each day, or still -1 |
| P4 | one day: the hardest job |
| P5 | every difficulty doubled: twice the answer, or still -1 |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 schedules: checksum
644298842, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`. Python, trying every
cut, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a day's first job left out of its hardest | P1 816, P2 300, P3 794, P4 570, P6 3264 |
| M2 | ★: as many days as jobs refused | P1 206, P4 251, P6 824 |
| M3 | stack: a popped job's cost forgotten | P1 596, P2 502, P3 24, P4 1405, P5 444, P6 596 |
| M4 | stack: a harder earlier job's day never extended | P1 262, P2 414, P3 29, P4 799, P5 155, P6 262 |
| M5 | memo: the last day short of the last job | P1 698, P2 531, P3 794, P4 532, P6 698 |
| M6 | memo: the last two days taken as one | P1 610, P2 315, P3 769, P6 610 |
| M7 | scan: the hardest job started at 1 | P1 206, P3 206, P4 49, P5 205, P6 206 |
| M8 | scan: the places a day can start walked forwards | P1 451, P2 541, P4 766, P6 451 |
| M9 | solution: a day's first job taken as its hardest | P1 407, P2 412, P4 766, P6 407 |
| M10 | solution: a day's last job taken as its hardest | P1 427, P2 412, P4 799, P6 427 |

P1 and P6 kill all ten, P4 nine, P2 eight, P3 six and P5 three. One day
(P4) needs only the largest job, so it catches every edit that reads a
day's jobs wrongly; it misses only the two days taken as one (M6), which
never touches a single day. Reading the jobs backwards (P2) catches every
edit that treats a day's two ends differently, and misses only the days
refused when they match the jobs (M2) and the hardest started at 1 (M7),
neither of which cares about order. Raising every job (P3) catches the
edits whose error does not grow with the difficulties: a job left out
(M1, M5), days merged (M6), costs dropped by the stack (M3, M4), and the
1 that a raise past 1 hides (M7). Doubling (P5) catches only M3, M4 and
M7; the rest are wrong in proportion and double their own wrong answer.

## Benchmarks

The bench builds 20 schedules of 300 jobs, the constraints' most, with
difficulties up to 1000, once; then makes 30 passes, each setting one
job of every schedule and the number of days, 6 to 10, from the
checksum so far, so no answer carries over, answering every schedule
with the ★ arm and folding the answer plus the pass into the checksum.
Every language reads the jobs in place. Every implementation prints `30
passes over 20 schedules of 300 jobs: checksum 827702553`.

BENCHTAB
