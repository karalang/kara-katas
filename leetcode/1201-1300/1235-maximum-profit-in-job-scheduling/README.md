# 1235. Maximum Profit in Job Scheduling

We have `n` jobs, where every job is scheduled to be done from
`startTime[i]` to `endTime[i]`, obtaining a profit of `profit[i]`.

You're given the `startTime`, `endTime` and `profit` arrays, return the
maximum profit you can take such that there are no two jobs in the
subset with overlapping time range.

If you choose a job that ends at time `X` you will be able to start
another job that starts at time `X`.

```
startTime = [1, 2, 3, 3], endTime = [3, 4, 5, 6], profit = [50, 10, 40, 70]  ->  120
startTime = [1, 2, 3, 4, 6], endTime = [3, 5, 10, 6, 9], profit = [20, 20, 100, 70, 60]  ->  150
startTime = [1, 1, 1], endTime = [2, 3, 4], profit = [5, 6, 4]  ->  6
```

**Constraints:** `1 <= startTime.length == endTime.length ==
profit.length <= 5 * 10^4`; `1 <= startTime[i] < endTime[i] <= 10^9`;
`1 <= profit[i] <= 10^4`.

The arms are `fn job_scheduling(start_time: Vec[i64], end_time:
Vec[i64], profit: Vec[i64]) -> i64`. The three Rust arms keep the method
LeetCode gives Rust users, on `i32`, inside `impl Solution`, and a
four-line `job_scheduling` calls it.

## Approaches

| file | mechanism |
|---|---|
| `maximum_profit_in_job_scheduling.kara` ★ | dynamic programming over the jobs sorted by end time (`sort_by_key` on their indices): the best from the first `k + 1` jobs either skips job `k` or takes it on top of the best from the jobs that end by its start, counted by `partition_point` on the sorted ends. O(n log n) |
| `maximum_profit_in_job_scheduling_starts.kara` | the jobs as a `struct Job` sorted by start time, and the best from job `k` onward computed from the back: skip it, or take it and continue from the first job that starts at or after its end, found by `partition_point`. O(n log n) |
| `maximum_profit_in_job_scheduling_heap.kara` | the jobs in order of start time, every chain a job could extend held in a `PriorityQueue[(i64, i64)]` of (end, profit), smallest end first; before a job starts, the chains that have ended are popped into the best finished profit, and the job starts a chain on top of it. O(n log n) |
| `maximum_profit_in_job_scheduling_table.kara` | the jobs in order of end time and a `SortedMap[i64, i64]` from end time to the best profit by then, kept rising: a job's best is its profit on top of the table's `floor` at its start, and it enters the table only when it beats the best so far. O(n log n) |
| `maximum_profit_in_job_scheduling_sorted.kara` | a Rust solution as LeetCode's Rust users write it (the jobs zipped into `(end, start, profit)` tuples by `into_iter().zip(..)`, sorted by `sort_unstable()`, the jobs that end by each start counted by `partition_point` with a `\|&(e, _, _)\|` closure), carried to Kāra by `karac fix` |
| `maximum_profit_in_job_scheduling_btree.kara` | another Rust solution (the indices sorted by `sort_by_key(\|&i\| end_time[i])`, a `BTreeMap<i32, i32>` from end time to the best profit by then, read at each start by `range(..=start).next_back()`), carried to Kāra by `karac fix` |
| `maximum_profit_in_job_scheduling_search.kara` | a third Rust solution (the jobs as `[i32; 3]` arrays sorted by `sort_by(\|a, b\| a[1].cmp(&b[1]))`, a rising list of `(end, best)` pairs searched by `binary_search_by`, an `Err(i)` meaning the pair before `i`), carried to Kāra by `karac fix` |
| `differential.kara` | the seven arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's three examples and one job
(`4`), a checksum of the answers for 1000 random sets of 1 to 30 jobs
with times up to 50, so that jobs share start and end times
(`926850687`), and three answers at the constraints' top, 5 * 10^4 jobs:
spread over 10^9 (`33421573`), all from 1 to 10^9, so that only one can
be taken (`10000`), and back to back, so that all can (`250025000`).
`maximum_profit_in_job_scheduling.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the heap and table arms check clean as written. The ★ and
starts arms were first written with Rust's `vec![0; n + 1]`, which the
fix makes `Vec.filled(n + 1, 0)`. The sorted arm takes one round of 17
fixes (among them `Vec<(i32, i32, i32)>` to `Vec[(i32, i32, i32)]`, the
three parameters that `into_iter()` consumes to `own Vec[i32]`,
`sort_unstable()` to `sort()`, `vec![0; n + 1]` to `Vec.filled(n + 1,
0i32)`, `|&(e, _, _)|` to `|(e, _, _)|`), the btree arm one round of 21
(among them `BTreeMap<i32, i32>` to `SortedMap[i32, i32]`, `Vec<usize>`
to `Vec[i64]`, `for &i in &idx` to `for i in ref idx`,
`dp.range(..=start_time[i])` to `dp.range_inclusive(i32.MIN,
start_time[i])`), and the search arm one round of 19 (among them
`Vec<[i32; 3]>` to `Vec[Array[i32, 3]]`, `a[1].cmp(&b[1])` to
`a[1].cmp(b[1])`, `vec![(0, 0)]` to `[(0, 0)]`, and the `match` over
`binary_search_by` to one `partition_point` search for the end of the
run of equal end times, the pair before it), and all three
check clean.

## Gaps

One.

- B-2026-11-19-32, fixed in kara at a402330c7a: the fix for a Rust
  `binary_search_by` (and `binary_search`, `binary_search_by_key`) took
  `Ok`'s index as the first element equal to the one sought. Rust's
  documentation lets it return any of them, but its implementation
  returns the last, and this search arm depends on that: its list holds
  repeated end times, each with a higher profit than the one before, and
  only the last is the best. Carried with the first, the arm answered
  wrongly for 278 of the differential's 2000 cases and gave the checksum
  `747145701` for the 1000 random sets, where the Rust solution, built
  by rustc, gives `926850687`; the shortest case was `startTime = [8, 2,
  5, 2, 7, 4]`, `endTime = [11, 3, 8, 6, 8, 7]`. The fix now takes the
  last, as rustc's Rust does, and the arm is its output.

## Differential

`differential.kara` holds copies of the seven arms and the statement
read literally: every subset of the jobs, kept when no two of its jobs
overlap (each starts before the other ends), the most profit of those,
for up to 12 jobs. 2000 cases, a third with 1 to 12 jobs, a third with
13 to 100 and a third with 101 to 1000, half of them with every start
within `n + 5`, so that jobs share start and end times.

| | property |
|---|---|
| P1 | the statement read literally (up to 12 jobs) |
| P2 | from the best single job to all the jobs' profit |
| P3 | the jobs listed backwards give the same answer |
| P4 | every time moved 1000 later gives the same answer |
| P5 | every profit doubled doubles the answer |
| P6 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 189625650,
84000 checks over 7 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, with every
subset tried for up to 12 jobs, gives the same checksum and the same
answers.

## Mutation testing

Thirteen edits to the differential, two or three to each arm but the
search arm, each run under `karac __mir-run` and `karac run`.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a job may start before the last one ends | P1 264, P6 6024 |
| S2 | ★: jobs ending at a start kept apart | P1 218, P6 5544 |
| S3 | ★: a job never skipped | P1 404, P2 109, P3 867, P6 10410 |
| T1 | starts: sorted by end, searched by start | P1 108, P3 746, P6 1381 |
| T2 | starts: the next job one later | P1 522, P3 791, P6 1789 |
| H1 | heap: a chain ending at a start left open | P1 218, P6 924 |
| H2 | heap: the open chains never drained | P1 667, P2 171, P6 2000 |
| M1 | table: every job entered | P1 296, P3 874, P6 1619 |
| M2 | table: read at the start's next time | P1 218, P6 924 |
| R1 | sorted: sorted by start in the tuple | P1 580, P6 1913 |
| R2 | sorted: the job's own profit dropped | P1 667, P2 2000, P6 2000 |
| B1 | btree: the best never raised | P1 667, P2 2000, P6 2000 |
| B2 | btree: the table read just before the start | P1 218, P6 924 |

All thirteen are caught, and P1, the statement read literally, catches
every one. A mutation of the ★ arm fails P6 on the six other arms. Four
of them are the same mistake, a job that starts the moment another ends
counted as overlapping it, made four ways: the ★ arm's search for `<`
rather than `<=` (S2), a chain popped only once it has ended before the
start (H1), the table read one time unit early (M2) and the btree's
range made exclusive (B2). All four fail exactly the same 218 cases, and
S2's P6 count is H1's 924 over six arms. R2 and B1 answer 0 for every
set, so P2, the answer between the best single job and the sum of all
of them, fails all 2000; P2 also catches the ★ arm that never skips a
job (S3), which can end below the best single job, and the heap whose
open chains are never drained (H2), which loses every chain still open
at the end. P3, the jobs listed backwards, catches the arms whose answer
depends on the order the jobs arrive in: S3, the starts arm sorted by
the wrong time (T1) or continuing one job too late (T2), and the table
that enters every job (M1), whose `floor` then finds a later, smaller
best. P4 and P5, every time shifted and every profit doubled, catch
none: no mutation here depends on a time's or a profit's size.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, dynamic programming over the jobs sorted by end time, the jobs that
end by each start counted by `partition_point`. O(n log n). Every
program prints `20 sets of 50000 jobs, 10 passes: checksum 663218007`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.742 to 0.871 s | 0.804 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.734 to 0.867 s | 0.766 s |
| Rust (`rustc -O`) | 0.752 to 0.896 s | 0.775 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.737 to 0.927 s | 0.806 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.743 to 0.886 s | 0.802 s |
| C (`clang -O3`) | 2.476 to 2.727 s | 2.555 s |
| C (`clang -O3 -march=x86-64-v3`) | 2.397 to 2.490 s | 2.452 s |
| Go | 4.499 to 4.906 s | 4.693 s |
| Python | 9.201 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 5% ahead of Rust with overflow checks on (0.766 s
against 0.806 s), and the two ranges overlap. C takes about 3.3x Kāra's
time; Go takes about 6.1x Kāra's time. Python takes about 12x Kāra's
time. No profile was taken.
