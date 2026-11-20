# 1723. Find Minimum Time to Finish All Jobs

You are given an integer array `jobs`, where `jobs[i]` is the amount of
time it takes to complete the `ith` job.

There are `k` workers that you can assign jobs to. Each job should be
assigned to **exactly** one worker. The **working time** of a worker is
the sum of the time it takes to complete all jobs assigned to them. Your
goal is to devise an optimal assignment such that the **maximum working
time** of any worker is **minimized**.

Return *the **minimum** possible **maximum working time** of any
assignment.*

```
jobs = [3,2,3], k = 3          ->  3
jobs = [1,2,4,7,8], k = 2      ->  11    (1 + 2 + 8 and 4 + 7)
```

**Constraints:** `1 <= k <= jobs.length <= 12`; `1 <= jobs[i] <= 10^7`.

## Approaches

| file | mechanism |
|---|---|
| `jobs.kara` ★ | backtracking: each job, the longest first, tried on every worker, a branch cut once a worker's load plus the job reaches the best finish found; workers with nothing yet are alike, so a job goes to the first idle one only. O(k^n) at worst |
| `jobs_binary.kara` | a binary search on the finish between the longest job and the sum, each limit tried by the same backtracking, which stops at the first assignment that fits. O(log(sum) k^n) at worst |
| `jobs_dp.kara` | dynamic programming over subsets: `sum[mask]` from the mask without its lowest job, then for each worker more the best of a mask is the least, over each part of it given to the new worker, of that part's sum and the old best of the rest. O(k 3^n) |
| `jobs_solution.kara` | a Rust solution as LeetCode's Rust users write it, `sort_unstable_by` descending, a `vec![0; k as usize]` of loads, and a `HashSet` per level so equal loads are tried once, through `Self::backtrack(&jobs, 0, &mut workers, &mut ans)`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, one job,
twelve jobs of `10^7` for twelve workers and for one; then the answers
summed and a checksum for 3000 random problems of 1 to 6 jobs up to 10,
300 of 1 to 10 jobs up to `10^7`, and 20 of 12 jobs up to `10^7`, each
with 1 to as many workers as jobs. `jobs.py` mirrors the ★ arm and its
output is byte-identical.

```
3
11
5
10000000
120000000
3000 problems of 1 to 6 jobs up to 10: answers sum to 33905, checksum 477319134
300 problems of 1 to 10 jobs up to 10000000: answers sum to 3559028189, checksum 423182767
20 problems of 12 to 12 jobs up to 10000000: answers sum to 319750603, checksum 525859007
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every assignment of each job to one of the k workers, counted
as the digits of a number in base k, each worker's time the sum of its
jobs, and the least of the longest. It checks 3000 random problems of 1
to 6 jobs of 1 to 6 each, and 1 to as many workers as jobs. Every case
is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the jobs in reverse order give the same answer |
| P3 | every job doubled doubles the answer |
| P4 | a job as long as the answer added, with one worker more, gives the same answer |
| P5 | each arm agrees with at least two of the other three |

P4 holds because the new worker can take the new job alone, and no
assignment finishes before its longest job. The differential prints
`3000 problems: checksum 922781982, 60000 checks over 4 arms: 0
failures` under every lane in Verification, and a Python reading of the
statement, the least of the longest over `itertools.product(range(k),
repeat=n)`, gives the same checksum. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Three first drafts were replaced. The
dp arm's parts stepped by `sub - 1` without `& mask` was equivalent: a
part that holds a job outside the mask stands for an assignment of more
jobs, which never finishes sooner, so the least is unchanged. Two
solution mutants, its level loop missing the last worker and its seen
test turned round, left some answer at `i32.MAX`, and P3's doubling
overflowed and stopped the run. M3 and M5 both answer the sum of all the
jobs, M3 because the loads only grow and M5 because no limit below the
sum ever reports a fit, and they fail the very same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an idle worker ends the loop before the job is tried on it | P1 3000, P3 3000, P4 3000, P5 3000 |
| M2 | ★: a finish taken as the least load, not the largest | P1 1756, P4 1244, P5 1756 |
| M3 | ★: a job never taken back off its worker | P1 1756, P4 3000, P5 1756 |
| M4 | binary: a load must stay below the limit, not reach it | P1 1756, P3 1756, P4 3000, P5 1756 |
| M5 | binary: an assignment that fits not passed back up | P1 1756, P4 3000, P5 1756 |
| M6 | dp: a mask's time from the mask shifted down, not from the mask without its lowest job | P1 2308, P2 2162, P4 2950, P5 2308 |
| M7 | dp: one worker fewer | P1 1280, P4 1244, P5 1280 |
| M8 | dp: the lowest job taken as the count of jobs less one | P1 1216, P2 1511, P4 575, P5 1216 |
| M9 | solution: a worker too full for the job ends the level | P1 836, P4 1329, P5 836 |
| M10 | solution: a finish taken as the first worker's load | P1 241, P5 241 |

## Benchmarks

The bench draws 100 random problems of 12 jobs up to `10^7`, LeetCode's
largest, each with 2 to 12 workers, all of them first, then answers each
5 times by the ★ arm in all five languages. Every implementation prints
`100 problems of 12 jobs, 5 rounds: answers sum to 6384905550, checksum
345235525`. The work is the backtracking's recursion, a few compares and
adds a call; how much of the tree the cut leaves depends on the problem,
the same in every language since each tries the workers in the same
order. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.972 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.998 s |
| Go | 1.195 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.282 s |
| Kāra (`karac build`) | 1.317 s |
| C (`clang -O3`) | 1.371 s |
| Python | 43 s |

The sequential Kāra build takes 1.32x Rust's time and 1.28x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.593 s and 1.596 s on one
run).

## Verification

All four arms print the same output as `jobs.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, binary and dp arms checked clean as first written. In the ★ arm
`*best = loads.iter().max().unwrap();` takes the largest load as an
`i32` with no `*`, and `Vec.filled(k, 0)` takes the `i32` worker count
as its length.

LeetCode's Rust template took one `karac fix` of 28 edits:
`struct Solution {}` added, `use std::collections::HashSet;` deleted,
`Vec<i32>` written `Vec[i32]`, `&[i32]` written `Slice[i32]`, `&mut`
parameters written `mut ref`, `usize` written `i64`, `Self::backtrack`
written `Solution.backtrack` with `&jobs` and `&mut` arguments written
`jobs` and `mut`, `sort_unstable_by` written `sort_by`,
`vec![0; k as usize]` written `Vec.filled(k, 0)`, `i32::MAX` written
`i32.MAX`, `HashSet::new()` written `Set.new()`, and `!` written `not`.
`let mut jobs = jobs;` moves the parameter, so the fix declared it
`own Vec[i32]`, and the same on the harness's bridge, which hands its
`jobs` on.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
