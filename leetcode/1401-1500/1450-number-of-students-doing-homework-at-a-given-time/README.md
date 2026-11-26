# 1450. Number of Students Doing Homework at a Given Time

Given two integer arrays `startTime` and `endTime` and given an integer
`queryTime`. The `ith` student started doing their homework at the time
`startTime[i]` and finished it at time `endTime[i]`. Return the number
of students doing their homework at time `queryTime`. More formally,
return the number of students where `queryTime` lays in the interval
`[startTime[i], endTime[i]]` inclusive.

```
startTime = [1,2,3], endTime = [3,2,7], queryTime = 4  ->  1
startTime = [4], endTime = [4], queryTime = 4          ->  1
```

**Constraints:** `startTime.length == endTime.length`, `1 <=
startTime.length <= 100`, `1 <= startTime[i] <= endTime[i] <= 1000`, `1
<= queryTime <= 1000`.

Each arm is `fn busy_student(start_time: Vec[i32], end_time: Vec[i32],
query_time: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `busy_student.kara` ★ | each student's start and end side by side through `zip`, kept by a `filter` when the query falls between them, and counted. O(n) |
| `busy_student_loop.kara` | every student by place, counted when busy at the query. O(n) |
| `busy_student_sweep.kara` | a sweep over the times: one more student busy from each start, one fewer after each end, the running count read at the query as the sum of `change[..=query_time]`. O(n + 1000) |
| `busy_student_sorted.kara` | the starts and the ends each sorted: those started by the query, less those already ended before it, each found by `partition_point`. O(n log n) |
| `busy_student_solution.kara` | a Rust solution as LeetCode's Rust users write it (the two times zipped, `filter(\|(&s, &e)\| ..)` with `&&`, and `count() as i32`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples and four
more, a query just after the one student, one student over every time,
and a query at a start and at an end (`1 1 0 1 2 2`); the constraints'
most, 100 students over every time asked at 1000, and 100 drawn students
asked at every time from 1 to 1000 (`100 students: 100, and 33384 over
every time`); and 2000 random cases of 1 to 100 students, times from 1
to 1 to 1000 (`2000 random cases: 34673 students, checksum 552407855`).
`busy_student.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean as first written. The Rust
solution takes one round of 9 fixes by `karac fix`'s count: `struct
Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`, the `&`
patterns `|(&s, &e)|` to `|(s, e)|`, `&&` to `and`, and `Solution::` to
`Solution.`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every time each student is doing homework, from the start to
the end, collected, and the students with the query among them, while
every end is at most 100. LeetCode's examples, the four edge cases
above, the constraints' most five ways (100 students over every time
asked at 1000 and at 1, and 100 drawn students asked at 1, 500 and
1000), and 1992 random cases drawn as the harness draws them, a third of
them with times from 1 to 1 to 100, for the literal reading.

The three drawn queries are walked as `for q in [1, 500, 1000]` and
pushed with the `i32` times, which `karac check` refuses, the array's
literals having taken the default `i64`, and `karac fix` writes `[1i32,
500, 1000]`, 1 fix.

| | property |
|---|---|
| P1 | the statement read literally, while every end is at most 100 |
| P2 | the students in the other order give the same count |
| P3 | a student more, from the query to the query, gives one more |
| P4 | a student more, ending just before the query, changes nothing |
| P5 | the count a time before, with those starting at the query and less those who ended the time before |
| P6 | the ★ arm's answer |

All 53,450 checks pass on every arm: `2003 cases: checksum 267659979,
53450 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by `bisect` over
the sorted starts and ends, gives the same checksum.

The fixed cases are a typed list of tuples written as Rust writes them,
`[([1, 2, 3].to_vec(), [3, 2, 7].to_vec(), 4), ..].to_vec()` into a
`Vec[(Vec[i32], Vec[i32], i32)]`. Check refused each tuple, its
`.to_vec()` list taking the default `i64` where the slot names `i32`:
the slot's type reached a `[..].to_vec()` at a `let` of its own but not
one inside a tuple. That was B-2026-11-26-78, fixed at a648c7a471.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a student starting at the query not counted | P1 378, P3 2003, P5 659, P6 2072 |
| M2 | ★: a student ending at the query not counted | P1 410, P3 2003, P5 644, P6 2184 |
| M3 | loop: a student counted when started by the query or not yet ended | P1 751, P4 1957, P5 723, P6 1976 |
| M4 | loop: the first student never looked at | P1 291, P2 782, P5 55, P6 683 |
| M5 | sweep: each student taken off at their end, not after it | P1 410, P3 2003, P5 644, P6 546 |
| M6 | sweep: the starts at the query left out of the count | P1 514, P3 2003, P4 1957, P5 942, P6 762 |
| M7 | sorted: the starts at the query not counted as started | P1 378, P3 2003, P5 659, P6 518 |
| M8 | sorted: the ends never sorted before the search | P1 582, P2 1278, P3 624, P4 1824, P5 488, P6 1561 |
| M9 | solution: a student counted when started by the query or not yet ended | P1 751, P4 1957, P5 723, P6 1976 |
| M10 | solution: each start paired with the next student's end | P1 437, P2 1145, P3 653, P5 236, P6 1227 |

## Benchmarks

The bench draws 3000 classes of 100 students, the constraints' most,
each from a start to an end drawn from 1 to 1000, and asks each class at
every time from 1 to 1000 with the ★ arm, folding the counts to a
checksum. C's loop counts by place; the others zip and filter, as the ★
arm does, or loop, in Go. Every implementation prints `3000 classes
asked 1000 times: checksum 198665608`.

BENCHTAB

Measured by hand, Kāra takes 0.20 to 0.26 s against Rust's 0.12 s (0.39
to 0.48 s with overflow checks on), C's 0.05 s and Go's 0.29 to 0.40 s;
Python takes 20 s.
