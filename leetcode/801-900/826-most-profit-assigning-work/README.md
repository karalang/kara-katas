# 826. Most Profit Assigning Work

There are `n` jobs, job `i` of difficulty `difficulty[i]` paying
`profit[i]`, and `m` workers, worker `j` able to do any job of
difficulty at most `worker[j]`. Each worker does at most one job, and a
job can be done by any number of workers. Return the most total profit.

```
difficulty = [2,4,6,8,10], profit = [10,20,30,40,50], worker = [4,5,6,7]  ->  100
difficulty = [85,47,57],   profit = [24,66,99],       worker = [40,25,25] ->  0
```

**Constraints:** `1 <= n, m <= 10^4`, `1 <= difficulty[i], profit[i],
worker[j] <= 10^5`.

## Approaches

Workers do not compete, so each takes the best profit among the jobs no
harder than their ability, and the answer is the sum. A harder job can
pay less, so the best is a running maximum over the jobs in order of
difficulty, not the last job reached.

| file | mechanism |
|---|---|
| `max_profit_assignment.kara` ★ | the jobs paired and sorted, the workers sorted, and one pointer walking the jobs as the abilities grow, keeping the best profit passed. O(n log n + m log m) |
| `max_profit_assignment_table.kara` | a table of the best profit at each difficulty up to the largest value, turned by a running maximum into the best at that difficulty or below, read once per worker. No sorting. O(n + m + D) for D the largest value |
| `max_profit_assignment_search.kara` | the jobs ordered by `sort_by_key` on difficulty with their profits carried forward as the best so far, and a binary search per worker, who are not sorted. O((n + m) log n) |
| `max_profit_assignment_iter.kara` | the jobs `zip`ped and sorted, a `scan` turning their profits into the best so far, and a `fold` over the sorted abilities that walks that ladder |
| `differential.kara` | the four arms against the statement read worker by worker, four properties |

Every arm prints the same 10 lines: LeetCode's two examples; five small
cases (a worker exactly able for the one job, and one short of it;
profit falling with difficulty; two jobs of the same difficulty and a
worker far above every job; and three jobs of one difficulty with
workers below, at and above it); two cases of LeetCode's largest size,
10,000 random jobs and workers, and the same with profit falling as
difficulty rises; and 300 random cases of up to 12 jobs and 12 workers,
with a total and a checksum. `max_profit_assignment.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each worker looks at every job and takes the best profit
among those no harder than their ability, or nothing. Its 1,600 cases
have up to 15 jobs and 15 workers and come in four kinds of 400:
difficulties up to 40 and abilities up to 45; difficulties of 1 to 4
only, so that many jobs share one; profit falling as difficulty rises;
and abilities mostly below the jobs.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the jobs and the workers in reverse order give the same answer |
| P3 | a job one harder than the ablest worker, paying more than any other, changes nothing |
| P4 | a worker able for every job adds the best profit of all |

It prints `1600 cases, 25600 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a job as hard as the ability refused | P1 504, P4 107 |
| M2 | ★: the last job passed taken, not the best | P1 1096, P4 1220 |
| M3 | ★: the workers not sorted | P1 687, P2 442, P4 334 |
| M4 | table: the running maximum left out | P1 1495, P4 1480 |
| M5 | table: a later job at a difficulty replaces an earlier one | P1 294, P2 459, P4 262 |
| M6 | table: the table sized by the jobs only | index out of bounds |
| M7 | search: the last job no harder found one too far | P1 404, P3 1600 |
| M8 | search: the profits not carried forward | P1 1170, P2 553, P4 1294 |
| M9 | search: the jobs not sorted | P1 701, P2 892, P3 1009 |
| M10 | iter: the ladder the profits, not the best so far | P1 1096, P4 1220 |
| M11 | iter: a worker who passes no new job earns nothing | P1 1291, P4 1043 |
| M12 | iter: the jobs not sorted | P1 975, P2 927, P3 542 |

P1 kills eleven, and M6 dies of an index out of bounds the first time a
worker is abler than every job is hard. M2 and M10 are the same mistake,
the profit of the last job reached instead of the best, and give the
same answer on every case. M7 fails P3 on every case: reading one past
its range, the ablest worker reaches the added job, which pays more than
any other. The first edit tried for M11, walking the ladder from its
start for each worker, survived every case and was replaced: the ladder
only rises, so the walk ends on the same entry and only costs time. P2
sees the edits that make an arm depend on the order of its input (M3,
M5, M8, M9, M12).

## Verification

Every arm prints the same output as `max_profit_assignment.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release build
that runs `check` and `__mir-run` and the debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` are both at kara
`909d2c7a1f`, with the runtime archives built from that tree.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for the ★, table and binary-search arms. The legacy interpreter also
runs the iterator arm and the differential, while its compiled backends
refuse both, with no handler for the `collect` after `zip`; its checker
refuses the bench program, which passes `difficulties[g]` to a bare
parameter and so, under legacy's rules, moves it out of an index. Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
cases of 10,000 jobs and 10,000 workers, values from 1 to 100,000,
LeetCode's largest, once. Each of 2,000 rounds answers the next case
afresh: the jobs paired and sorted, the workers copied and sorted, and
the sweep. Every implementation prints `2000 rounds of 64 cases: total
654757766486, checksum 639871891`, the Kāra program under `karac
__mir-run` included, in 72 s with the interpreter's step limit raised by
`KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, eight runs of each compiled
program and 13 of v2's, five of them interleaved, and three of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 5.66 to 6.05 s |
| Rust (`rustc -O`) | 1.47 to 1.74 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.50 to 1.80 s |
| Go | 6.67 to 7.17 s |
| Python | 15.3 to 16.2 s |
| Kāra (`karac build --mir`) | 2.76 to 3.12 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 2.83 s, against Rust's
1.61 (1.73 under overflow checks), C's 5.91 and Go's 6.70: 1.6 times
Rust's time under overflow checks, and half of C's. The two sorts are
most of the work, and the languages sort differently: C calls the
library's `qsort`, which reaches its comparison through a function
pointer for every pair it compares, and Go's `sort.Slice` calls a
closure, where Rust's `sort` and Kāra's are compiled for the element
type. Under valgrind's cachegrind v2 runs 15.5 billion instructions,
against Rust's 11.6 billion and C's 21.4 billion. Most likely the
indirect comparison is what puts C and Go behind (not traced). Built for
`x86-64-v3`, the target `karac build` uses, C takes 5.60 to 5.90 s and
Rust with overflow checks 1.54 to 1.69 s, against v2's 2.77 to 2.98 s in
the same five interleaved runs. Python, whose `sorted` is native code,
takes 16 s, about 2.6 times C's time. The comparison with C and Rust
waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written, and in the first spelling tried.
