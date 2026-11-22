# 2747. Count Zero Request Servers

You are given an integer `n` denoting the total number of servers and a
**2D** **0-indexed** integer array `logs`, where `logs[i] = [server_id,
time]` denotes that the server with id `server_id` received a request at
time `time`.

You are also given an integer `x` and a **0-indexed** integer array
`queries`.

Return *a **0-indexed** integer array* `arr` *of length*
`queries.length` *where* `arr[i]` *represents the number of servers
that **did not receive** any requests during the time interval*
`[queries[i] - x, queries[i]]`.

Note that the time intervals are inclusive.

```
n = 3, logs = [[1, 3], [2, 6], [1, 5]], x = 5, queries = [10, 11]          ->  [1, 2]
n = 3, logs = [[2, 4], [2, 1], [1, 2], [3, 1]], x = 2, queries = [3, 4]    ->  [0, 1]
```

**Constraints:** `1 <= n <= 10^5`, `1 <= logs.length <= 10^5`, `1 <=
queries.length <= 10^5`, `logs[i].length == 2`, `1 <= logs[i][0] <= n`,
`1 <= logs[i][1] <= 10^6`, `1 <= x <= 10^5`, `x < queries[i] <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `servers.kara` ★ | offline: the logs sorted by time as `(time, server)` tuples and the queries taken in time order through a sorted index; a window of logs `[q - x, q]` slides forward with a count of requests for each server and of the servers with any, and each answer is n less that. O(L log L + Q log Q + n) |
| `servers_scan.kara` | each query looks at every log: the servers of those in the window `filter`ed and `collect`ed into a `Set`, and the answer is n less its `len()`. O(Q L) |
| `servers_bisect.kara` | each server's request times sorted in a `Vec[Vec[i64]]`; a query asks every server whether its first time at or after `q - x`, by `partition_point`, is at most q. O(L log L + Q n log L) |
| `servers_intervals.kara` | a request at t keeps its server busy for the queries in `[t, t + x]`: each server's stretches merged into a `Vec` of `struct Busy`, each marking the sorted queries it covers with +1 and -1 in a difference array, and a running sum giving each query's busy servers. O(L log L + Q log Q) |
| `servers_solution.kara` | a Rust solution as LeetCode's Rust users write it, `mut logs` sorted in place by `sort_unstable_by_key`, the queries as `(q, i)` pairs and a `let (mut l, mut r, mut active)` window, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; a request
exactly at each end of the window and one just outside; 1000 random
cases of 1 to 10 servers, 1 to 20 logs and 1 to 20 queries with times
up to 30; and 3 cases of 1000 servers, 3000 logs and 3000 queries with
times up to `10^6`, the last two with the sum of the answers and a
checksum. `servers.py` mirrors the ★ arm and its output is
byte-identical.

```
[1, 2]
[0, 1]
[2, 3, 3, 4]
1000 small cases: answers sum to 39128, checksum 835114926
3 cases of 3000 logs: answers sum to 5948059, checksum 130512530
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each query, every server from 1 to n asked in turn
whether any log of its own falls in `[q - x, q]`, ends included, in
plain loops, with no sorting and no window. It draws 1000 random cases
of 1 to 10 servers, 1 to 20 logs and queries, times up to 30, then 50 of
up to 300 servers and 1000 logs and queries, times up to `10^6`, all
before any arm answers; the literal reading is asked only of the first
1000.

| | property |
|---|---|
| P1 | up to 10 servers, the answers are the literal reading's |
| P2 | the logs listed in reverse order: the same answers |
| P3 | the queries listed in reverse order: the answers reversed |
| P4 | every time, of logs and queries, 1000 later: the same answers |
| P5 | each answer from 0 to n; and a server n + 1 with no logs: each answer one more |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1050 cases: checksum 716814638, 31500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same loops gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M5 fail the same checks, both leaving
out a request at the query's own time; so do M2 and M3, both one at
`q - x`.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a request at q itself left out | P1 671, P6 678 |
| M2 | ★: a request at q - x let go | P1 667, P6 671 |
| M3 | scan: a request at q - x left out | P1 667, P6 671 |
| M4 | scan: the busy servers counted, not the idle | P1 989, P5 1050, P6 1039 |
| M5 | bisect: a request at q itself taken as outside | P1 671, P6 678 |
| M6 | bisect: each server's times left unsorted | P1 739, P2 869, P6 788 |
| M7 | intervals: stretches that only touch kept apart | P1 135, P5 38, P6 135 |
| M8 | intervals: one server's stretch merged into another's | P1 783, P5 524, P6 833 |
| M9 | solution: the logs never sorted | P1 871, P2 902, P6 921 |
| M10 | solution: a server that goes quiet still counted busy | P1 861, P5 416, P6 911 |

## Benchmarks

The bench draws 10 cases of `10^5` servers, `10^5` logs and `10^5`
queries, LeetCode's most, with times up to `10^6`, all of them first,
then answers each 3 times by the ★ arm in all five languages. C sorts
with `qsort`, Go with `slices.SortFunc` and `slices.SortStableFunc`,
Rust and Kāra with `sort` and `sort_by_key`, and Python with `sorted`;
the order of equal queries does not change any answer. Every
implementation prints `10 cases of 100000 logs and queries, 3 rounds:
answers sum to 282948644892, checksum 186936813`.

BENCHTAB

## Verification

All five arms print the same output as `servers.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The scan arm checked clean as first written. The ★ arm wrote Rust's
`let (mut start, mut end) = (0, 0)`, which `karac fix` made `let mut
(start, end) = (0, 0)`. The bisect arm read a server's times as `let t
= times[server]`, and `karac fix` borrowed it, `ref times[server]`. The
intervals arm first named its struct `Span`, which shadows the prelude
type of that name; `karac check` warned, and it became `Busy`.

LeetCode's Rust template took 44 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `mut logs: Vec<Vec<i32>>` became
`logs: own Vec[Vec[i32]]` with a `let mut logs = logs;`;
`sort_unstable_by_key` and `sort_unstable` became `sort_by_key` and
`sort`; `usize` became `i64`; the `vec![..]`s became `Vec.filled(..)`,
with `0i32` written where the element type came from the return type;
`let (mut l, mut r, mut active)` became `let mut (l, r, active)`; the
`&q` and `&v` patterns dropped their `&`; `&&` became `and`; and
`Solution::` became `Solution.`.
