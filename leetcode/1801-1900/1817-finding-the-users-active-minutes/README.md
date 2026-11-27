# 1817. Finding the Users Active Minutes

You are given the logs of users' actions on LeetCode and an integer `k`.
The logs are a 2D integer array `logs` where each `logs[i] = [IDi,
timei]` says that the user with `IDi` performed an action at the minute
`timei`. Several users can act at once, and one user can act more than
once in a minute. A user's active minutes (UAM) is the number of
distinct minutes in which the user performed an action; a minute counts
once however many actions fall in it. Return a 1-indexed array `answer`
of size `k` where `answer[j]` is the number of users whose UAM equals
`j`.

```
logs = [[0,5],[1,2],[0,2],[0,5],[1,3]],  k = 5  ->  [0,2,0,0,0]
logs = [[1,1],[2,2],[2,3]],              k = 4  ->  [1,1,0,0]
```

**Constraints:** `1 <= logs.length <= 10^4`, `0 <= IDi <= 10^9`, `1 <=
timei <= 10^5`, and `k` is in the range `[the largest UAM of any user,
10^5]`.

The arms are `fn finding_users_active_minutes(logs: Vec[Vec[i64]], k:
i64) -> Vec[i64]`.

## Approaches

| file | mechanism |
|---|---|
| `finding_users_active_minutes.kara` ★ | each user's distinct minutes gathered in a `Set` under the user's id in a `Map`, and the answer's entry for `j` counts the users with `j` distinct minutes. O(n) expected |
| `finding_users_active_minutes_sorted.kara` | no hashing: the logs sorted as (user, minute) pairs, so a user's logs stand together in minute order, and a user's distinct minutes are the changes of minute within its run. O(n log n) |
| `finding_users_active_minutes_pairs.kara` | the distinct (user, minute) pairs kept in one `Set`, then each user's count of them tallied in a `Map`, so no user holds a set of its own. O(n) expected |
| `finding_users_active_minutes_ordered.kara` | the ★ arm's grouping in ordered containers: a `SortedMap` from each user to a `SortedSet` of its minutes, walked in id order. O(n log n) |
| `finding_users_active_minutes_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<i32, HashSet<i32>>` filled by `entry(..).or_default()`, then tallied over `values()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; four edges,
one log, one user many times in one minute, ids and minutes at their
largest, and a `k` past every user's minutes (`[1] [1, 0] [1, 1, 0] [1,
1, 0, 0, 0, 0]`); the constraints' most, 10^4 logs of one user over 10^4
minutes and 10^4 users with a minute each (`the most: 1 1 [10000, 0,
0]`); and 3000 random cases of 1 to 40 logs over 1 to 6 users and 1 to 9
minutes (`3000 random cases: checksum 984610470`).
`finding_users_active_minutes.py` mirrors the ★ arm, and its output is
byte-identical. The ★ and pairs arms walk a `Map`, whose order is random
per process, but each only adds into the answer, so the answer does not
depend on it. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, sorted, pairs and ordered arms and the harness
check clean as first written. The Rust solution takes 27 fixes by `karac
fix`'s count, and its diff is: `use std::collections::{HashMap,
HashSet};` deleted and `struct Solution {}` added; `Vec<Vec<i32>>` and
`Vec<i32>` to `Vec[Vec[i32]]` and `Vec[i32]`; `HashMap<i32,
HashSet<i32>>` and `HashMap::new()` to `Map[i32, Set[i32]]` and
`Map.new()`; `.or_default()` to `.or_insert(Set.new())`; `vec![0; k as
usize]` to `Vec.filled(k, 0)`; `Solution::` to `Solution.` at the
harness's 9 calls; and the harness's `x as i64` on each `i32` of the
answer taken off, an `i32` widening to `i64` without a cast. The
solution takes `Vec[Vec[i32]]` logs and an `i32` `k`, so its harness
builds them so. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each user, in the order first seen, its logs are looked
over one by one, a minute is counted when no earlier log of that user
has it, and the user's count is tallied. It runs 2000 random cases of 1
to 30 logs over 1 to 6 users and 1 to 9 minutes, with ids and minutes
near their largest in a quarter of them, each with a `k` from the
minutes to two past them. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | every user is counted once: the answer adds up to the users |
| P3 | the logs in reverse order give the same answer |
| P4 | every log twice gives the same answer |
| P5 | the users' minutes add up to the distinct (user, minute) pairs |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 304465363, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: minutes merged in twos | P1 1342, P5 1342, P6 5368 |
| M2 | ★: each entry set to one, not counted | P1 1240, P2 1240, P5 1240, P6 4960 |
| M3 | sorted: a minute counted only after a gap | P1 1508, P5 1508, P6 1508 |
| M4 | sorted: each user's run cut after two logs | P1 1689, P2 1689, P4 1863, P5 1438, P6 1689 |
| M5 | pairs: only each minute's parity kept | P1 1338, P5 1338, P6 1338 |
| M6 | pairs: every user given one minute | P1 1635, P5 1635, P6 1635 |
| M7 | ordered: the user's id kept for its minute | P1 1635, P5 1635, P6 1635 |
| M8 | ordered: a user's set started afresh at every log | P1 1635, P5 1635, P6 1635 |
| M9 | solution: every user counted at one minute | P1 1635, P5 1635, P6 1635 |
| M10 | solution: the first log skipped | P1 869, P2 245, P3 718, P4 869, P5 869, P6 869 |

## Benchmarks

The bench builds one list of 10^4 logs over 1000 users and 100 minutes
once and makes 5000 calls of the ★ arm on runs of its first 5000 to 9999
logs, each run's length drawn from the checksum so far, with `k = 100`.
The C mirror has no map of sets: it keeps one open-addressing hash table
of (user, minute) pairs, for the distinct pairs, and one of users, for
their counts, which is the pairs arm's mechanism. It checks clean as
first written. Every implementation prints `5000 calls: checksum
181488070`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 4.1 s against Rust's 3.9 s (4.0 s with overflow checks on),
C's 0.40 s and Go's 4.2 s; Python takes 5.1 s.
