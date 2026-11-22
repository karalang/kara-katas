# 2895. Minimum Processing Time

You have a certain number of processors, each having 4 cores. The
number of tasks to be executed is four times the number of processors.
Each task must be assigned to a unique core, and each core can only be
used once.

You are given an array `processorTime` representing the time each
processor becomes available and an array `tasks` representing how long
each task takes to complete. Return the *minimum* time needed to
complete all tasks.

```
processorTime = [8,10],  tasks = [2,2,3,1,8,7,4,5]  ->  16
processorTime = [10,20], tasks = [2,3,1,2,5,8,4,3]  ->  23
```

**Constraints:** `1 <= n == processorTime.length <= 25000`;
`1 <= tasks.length <= 10^5`; `0 <= processorTime[i] <= 10^9`;
`1 <= tasks[i] <= 10^9`; `tasks.length == 4 * n`.

## Approaches

| file | mechanism |
|---|---|
| `processing.kara` ★ | the processor free first takes the four longest tasks, the next the next four, and so on: an exchange argument shows no other assignment finishes sooner. Each processor then finishes with its longest task, the first of its four |
| `processing_queue.kara` | core by core: every core of every processor goes into a `PriorityQueue` by the time it is free, and the tasks, longest first, each go to the core free soonest |
| `processing_search.kara` | binary search on the finishing time T: T is reachable when, the processor free last taking the four shortest tasks left and so on back, every task fits before T. Reachable is monotone in T, so the least reachable T is found by halving |
| `processing_chunks.kara` | the ★ arm's pairing as an iterator chain: the processors from free last, zipped with the tasks in fours from the shortest, by `chunks(4)`, each processor's finish its time plus the last of its four |
| `processing_solution.kara` | a Rust solution as LeetCode's Rust users write it: both arguments rebound `mut`, the processors sorted up and the tasks down by `sort_unstable_by(\|a, b\| b.cmp(a))`, then `tasks[i * 4]` added to each processor's time, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 25000
processors, LeetCode's most, all free at 0 with tasks 1 to 10^5, and all
at 10^9 with tasks of 10^9; then 3000 random cases of 1 to 3
processors, times and tasks 1 to 20, and 100 of 250 to 25000
processors, times and tasks up to 10^9, as a total of the answers and a
checksum. `processing.py` mirrors the ★ arm and its output is
byte-identical. The largest answer, 2 * 10^9, still fits the template's
`i32`.

```
16 23
100000 2000000000
3000 small cases: times total 80169, checksum 206460030
100 large cases: times total 100021842374, checksum 178741822
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every way to hand each task to a core, four to a
processor, searched, and the earliest time all are done kept. It draws
2000 random cases of 1 or 2 processors, times 0 to 9 and tasks 1 to 9,
then 50 of up to 750 processors, times and tasks up to 10^9, all before
any arm answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 2 processors, the answer is the literal reading's |
| P2 | every time and every task one more: two more |
| P3 | both lists reversed: the same answer |
| P4 | from the latest processor plus the shortest task, and the first plus the longest, to the latest plus the longest |
| P5 | a processor free at 0 with four tasks of 1 added: no later |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, times total 50819543781: checksum
336602632, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python search over the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a processor finishing with the shortest of its four | P1 1987, P4 1875, P6 2037 |
| M2 | ★: the tasks left shortest first | P1 1729, P4 1425, P6 1779 |
| M3 | queue: five cores to a processor | P1 219, P4 7, P6 247 |
| M4 | queue: the shortest task handed out first | P1 890, P6 940 |
| M5 | search: a processor's four checked by their shortest | P1 1987, P4 1875, P6 2037 |
| M6 | search: a reachable middle taken away from the range | P1 414, P2 349, P4 275, P6 438 |
| M7 | chunks: each four's shortest taken | P1 1987, P4 1875, P6 2037 |
| M8 | chunks: the processors zipped from free first | P1 890, P6 940 |
| M9 | solution: the tasks sorted up, not down | P1 1729, P4 1425, P6 1779 |
| M10 | solution: each processor's second longest taken | P1 1423, P4 1249, P6 1473 |

## Benchmarks

The bench draws 20 cases of 25000 processors and 10^5 tasks, LeetCode's
most, times and tasks up to 10^9, all first, then answers each 20 times
by the ★ arm in all five languages, each sorting fresh copies, C by
`qsort`. Every implementation prints `20 cases of 25000, 20 rounds:
times total 400013834120, checksum 154783990`.

BENCHTAB

## Verification

All five arms print the same output as `processing.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written, `PriorityQueue.new()`
popping the smallest first, and `shortest.chunks(4).iter()` zipped with
a reversed iterator, among them.

LeetCode's Rust template took 20 `karac fix` edits over two runs, the
wrapper included: `struct Solution {}` came for the `impl`; `Vec<..>`
became `Vec[..]`; the two `mut` parameters became `own` parameters
rebound `let mut` in the body, Kāra having no `mut` on a parameter;
`sort_unstable()` became `sort()` and `sort_unstable_by(..)` became
`sort_by(..)`; `let mut ans = 0;` was annotated `: i32`, so that the
`i32` sums it keeps the larger of stay `i32`; `for (i, &p)` lost its
`&`, the wrapper's two `|&x|` theirs, its `as i64` on the result went and
`Solution::` took `.`. `|a, b| b.cmp(a)` was accepted as written.
