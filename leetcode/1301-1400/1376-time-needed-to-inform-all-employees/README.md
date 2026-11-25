# 1376. Time Needed to Inform All Employees

A company has `n` employees with a unique ID for each employee from `0`
to `n - 1`. The head of the company is the one with `headID`.

Each employee has one direct manager given in the `manager` array where
`manager[i]` is the direct manager of the `i`-th employee,
`manager[headID] = -1`. Also, it is guaranteed that the subordination
relationships have a tree structure.

The head of the company wants to inform all the company employees of an
urgent piece of news. He will inform his direct subordinates, and they
will inform their subordinates, and so on until all employees know about
the urgent news.

The `i`-th employee needs `informTime[i]` minutes to inform all of his
direct subordinates (i.e., After `informTime[i]` minutes, all his direct
subordinates can start spreading the news).

Return the number of minutes needed to inform all the employees about
the urgent news.

```
n = 1, headID = 0, manager = [-1], informTime = [0]                          ->  0
n = 6, headID = 2, manager = [2,2,-1,2,2,2], informTime = [0,0,1,0,0,0]      ->  1
```

**Constraints:** `1 <= n <= 10^5`, `0 <= headID < n`, `manager.length ==
n`, `0 <= manager[i] < n`, `manager[headID] == -1`, `informTime.length
== n`, `0 <= informTime[i] <= 1000`, `informTime[i] == 0` if employee
`i` has no subordinates, and it is guaranteed that all the employees can
be informed.

Each arm is `fn num_of_minutes(n: i32, head_id: i32, manager: Vec[i32],
inform_time: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `num_of_minutes.kara` ★ | each manager's reports gathered in a list, then a breadth-first walk down from the head, each employee hearing the news when its manager heard it plus the manager's inform time; the answer is the latest. O(n) |
| `num_of_minutes_dfs.kara` | the same lists, and a recursive walk down: a manager's time is its own inform time plus the longest of its reports' times. O(n), recursion as deep as the chain of command |
| `num_of_minutes_climb.kara` | no lists: each employee's time found by climbing to the first one whose time is known, then filling in every employee on the climb on the way back down. Each is filled once. O(n) |
| `num_of_minutes_leaves.kara` | from the bottom up: each manager's reports counted, the employees with none started from, each one's time passed up to its manager, who keeps the longest and passes it on, with its own inform time added, once its last report has. The head is the last. O(n) |
| `num_of_minutes_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![vec![]; n]` of reports, and a recursive `fn dfs` nested in the method, taking `&Vec<Vec<usize>>` and `&Vec<i32>`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, and 10^5
employees, the constraints' most, in a chain from 0 down, in a chain
from n - 1 down, all reporting to one head, and as a binary heap (`0 1
99999000 50049999 1000 9849`); and 2000 random companies of 1 to 300
employees, labelled in a random order, each employee reporting to any
employee taken before it, to one of the last three, so the chain runs
deep, to one of the first three, so it runs wide, or to one of the last
half, 500 of each (`2000 random companies: 3196675 minutes in all,
checksum 184952685`). `num_of_minutes.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`; the
recursive arms reach 10^5 deep on the chains.

The Mend loop: each of the four Kāra arms took one round of `karac fix`,
one or two fixes from one error, and then matched on the first run. In
three, a running maximum started at `0` kept the default `i64` and was
returned as the `i32`; the fix declares it `: i32`, and the ★ arm's
`Vec.filled(n, 0)` of times becomes `Vec.filled(n, 0i32)`. In the
bottom-up arm, `(0..n).filter(..).collect()` into a `Vec[i64]` over an
`i32` `n` was refused, `collect` does not convert its items, and the fix
adds `.map(|x| x as i64)`. The Rust solution takes one round of 33 fixes
from 16 errors: `struct Solution;` to `struct Solution {}`, each
`Vec<..>` to `Vec[..]`, each `&T` parameter to `ref T`, the `&` dropped
from the patterns `(i, &m)` and `&v` and from the call's arguments, `n
as usize` to `n as i64`, `m as usize` and `head_id as usize` to `m` and
`head_id`, `u: usize` to `u: i64`, `vec![vec![]; n]` to `Vec.filled(n,
Vec.new())`, `for &v in &children[u]` to `for v in ref children[u]`,
`Solution::` to `Solution.`, and the nested `fn dfs` moved out of the
method to the top level, which Kāra has instead of nested items, and
which it can do since a nested `fn` captures nothing. Its output matches
on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: an employee hears the news once every manager above it, from
the head down, has spent its inform time, so its time is the sum of
those inform times, found by climbing from it to the head; the answer is
the latest. LeetCode's two examples and 2000 companies of 1 to 12
employees, drawn as above, 500 of each kind, a manager taking 1 to 9
minutes, each with a time from 1 to 9 for P4. Every company is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | every inform time doubled: twice as long |
| P3 | employee i renamed n - 1 - i: the same time |
| P4 | a new head above the old one, taking t minutes: t longer |
| P5 | at least the head's own inform time, at most every inform time added, and 0 exactly when the head is alone |
| P6 | the ★ arm's time |

All 60,060 checks pass on every arm: `2002 cases: checksum 740066849,
60060 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, climbing from
each employee the same way, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a report's time from its own inform time, not its manager's | P1 1840, P4 1792, P5 507, P6 7360 |
| M2 | ★: a report's time its manager's inform time alone, not added to when the manager heard | P1 1589, P4 1840, P6 6356 |
| M3 | dfs: the reports' times added, not the longest kept | P1 681, P6 681 |
| M4 | dfs: the longer of the reports' time and the manager's own, not the two added | P1 1589, P4 1840, P6 1589 |
| M5 | climb: every time taken as known, 0, from the start | P1 1840, P4 2002, P5 1840, P6 1840 |
| M6 | climb: employee 0 left out of the latest | P1 259, P3 501, P4 162, P5 80, P6 259 |
| M7 | leaves: a manager keeps the last report's time, not the longest | P1 822, P3 1088, P6 822 |
| M8 | leaves: the head's own inform time left out | P1 1840, P4 1792, P5 507, P6 1840 |
| M9 | solution: the reports of employee 0 never listed | P1 520, P3 892, P6 520 |
| M10 | solution: the walk started at employee 0, not the head | P1 1484, P3 1508, P4 2002, P5 1039, P6 1484 |

P1 and P6 kill all ten, P4 seven, P5 five, P3 four and P2 none. A new
head above the old one (P4) catches the edits that price a manager
wrong, whose answers do not grow by the new head's minutes: a report's
own inform time added for its manager's (M1), the head's left out (M8),
the time not carried down (M2, M4), every time taken as known (M5) and
the walk started away from the head (M10); and, in the companies of one
employee, the latest taken without employee 0 (M6), there the old head
and now the one heard last. Renaming (P3) catches the edits that look at
an employee's number, employee 0 left out (M6, M9) or the walk started
there (M10), and the one that keeps the last report's time (M7), since
renaming changes the order in which a manager's reports come. The bounds
(P5) catch the edits that can fall below the head's own inform time (M1,
M8) or give 0 to a company of more than one (M5, M6, M10). Doubling (P2)
catches nothing: every arm here only adds inform times and compares the
sums, so every edit's answer doubles with the true one. The weakest edit
is adding the reports' times (M3): it errs only where a manager has two
reports or more that are managers themselves, which 681 of the 2002
small companies hold.

## Benchmarks

The bench builds 10 companies of 10^5 employees, the constraints' most,
once: labelled in a random order, each employee after the first
reporting to any taken before it, a manager taking 1 to 1000 minutes.
Then 200 rounds, each giving one employee of one company, both drawn
from the checksum so far, a new inform time if it is a manager, and
timing that company with the ★ arm. Every implementation prints `200
rounds over 10 companies of 100000 employees: checksum 51959329`. The
work is the reports' lists built and one walk over 10^5 employees a
round. The Rust function takes `&[i32]`, as the Kāra one borrows its
`Vec`s; C has no growable list, so its reports are counted first and
laid out one manager after another.

BENCHTAB
