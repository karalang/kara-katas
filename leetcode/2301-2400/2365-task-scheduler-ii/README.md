# 2365. Task Scheduler II

You are given a **0-indexed** array of positive integers `tasks`,
representing tasks that need to be completed **in order**, where
`tasks[i]` represents the **type** of the `i`th task.

You are also given a positive integer `space`, which represents the
**minimum** number of days that must pass **after** the completion of a
task before another task of the **same** type can be performed.

Each day, until all tasks have been completed, you must either:

- Complete the next task from `tasks`, or
- Take a break.

Return *the **minimum** number of days needed to complete all tasks*.

```
tasks = [1,2,1,2,3,1], space = 3  ->  9
tasks = [5,8,8,5], space = 2      ->  6
```

**Constraints:** `1 <= tasks.length <= 10^5`; `1 <= tasks[i] <= 10^9`;
`1 <= space <= tasks.length`.

Doing the next task as early as it may be done is never worse, so the
day of each task is the day after the last one, or the day after its
type last ran plus `space`, whichever is later. `10^5` tasks of one type
with a space of `10^5` take `10^10` days, past `i32`, which is why
LeetCode's answer is an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `tasks.kara` ★ | the day moved on by one for each task, and to the day after the type's last run plus `space` when that is later; a `Map` keeps each type's last day. O(n) |
| `tasks_allowed.kara` | the earliest day each type may run again, kept in a `SortedMap`: a task runs on the day after the last or its type's earliest day, whichever is later. O(n log n) |
| `tasks_prev.kara` | no map: the places sorted by (type, place), so that each place's previous one of its type stands just before it, and then the days filled in order from those previous places. O(n log n) |
| `tasks_compress.kara` | the types compressed: the distinct types sorted, each task's type found among them by `binary_search`, and the last days kept in a plain vector. O(n log n) |
| `tasks_iter.kara` | iterators: the tasks folded into (day, last day of each type), each task moving the day on |
| `tasks_solution.kara` | LeetCode's Rust template: a `HashMap` of last days read by `if let Some(&d) = last.get(&t)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one task;
`10^5` tasks of one type with a space of `10^5`; `10^5` tasks of two
types in turn with a space of 1 and of 2; `10^5` distinct tasks; then
2000 random lists of 1 to 40 tasks of 1 to 6 types with a space of 0 to
8, with a checksum and the days of breaks in all. A space of 0, and one
larger than the list, are outside the constraints but kept here and in
the differential: the rule reads the same for them, and 0 is the case
where a type never waits. `tasks.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
against playing the days one by one on 3000 random lists.

The iter arm was first written as Rust writes it, `let (day, mut last)
= state;`. `check` refuses the `mut` inside the pattern, and `karac fix`
wrote `let mut (day, last) = state;` in 2 edits.

`check` first reports 10 errors on the template, and `karac fix`
carries it in one call, reporting 15 edits: the
`use std::collections::HashMap` line deleted; `HashMap` renamed `Map`
and its `::new` written with a dot; `struct Solution;` given its braces;
`Vec<..>` and `HashMap<..>` their brackets; `for &t in &tasks` written
`for t in ref tasks`; `if let Some(&d) = last.get(&t)` written
`if let Some(d) = last.get(t).cloned()`; and `Solution::` written with
a dot.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the days played one at a time, and on each the next task
done if its type last ran more than `space` days before, or a break
taken. No jumps. It checks 300 random lists of 1 to 40 tasks of 1 to 6
types with a space of 0 to 8; then 30 of up to 2000 tasks of up to 50
types with a space of up to 50; then 30 of up to 300 tasks of types up
to `10^9` with a space of up to 300. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | from `n` to `1 + (n - 1) (space + 1)` |
| P3 | every type `t` written `10^9 - t`: the same answer |
| P4 | a task of a type not in the list appended: one more |
| P5 | the last task repeated: `space + 1` more days |
| P6 | each arm agrees with at least three of the other five |

P3 holds because the rule only asks whether two tasks share a type, and
P4 because a new type never waits, so its task runs the day after the
last. P5 holds because the last task ran on the last day, so another of
its type waits until `space + 1` days after it. P5 was first the space
one larger: no fewer days, which holds too but failed none of the 31
edits first run against it.

The differential prints `360 cases: checksum 341528872, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and plays the days one by one. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only a task run the day before waits | P1 232, P6 232 |
| M2 | ★: the wait added to the day, not to the last run | P1 265, P6 265 |
| M6 | ★: the day counted from one | P1 360, P2 80, P6 360 |
| M7 | allowed: the earliest day without the one | P1 307, P5 328, P6 307 |
| M10 | allowed: the earliest day set before the day moves on | P1 328, P2 328, P4 328, P6 328 |
| M11 | allowed: the space doubled | P1 309, P2 104, P5 328, P6 309 |
| M12 | prev: the previous place the first of the type | P1 281, P5 293, P6 281 |
| M15 | prev: the last task of the type taken as the previous | P1 300, P5 320, P6 300 |
| M16 | prev: the largest day returned of the first n - 1 | P1 352, P2 55, P4 178, P5 216, P6 352 |
| M18 | compress: a type that has run taken as new when it ran on day 1 | P1 150, P5 8, P6 150 |
| M19 | compress: the wait taken from the type before | P1 255, P3 253, P4 231, P5 194, P6 255 |
| M20 | compress: the last day set before the wait | P1 340, P2 218, P5 360, P6 340 |
| M22 | iter: a new type started a day late | P1 360, P2 80, P4 360, P6 360 |
| M23 | iter: the day stored under the next type | P1 303, P3 212, P5 328, P6 303 |
| M24 | iter: the day not moved on | P1 360, P2 75, P4 360, P6 360 |
| M29 | solution: the day moved on after the wait | P1 339, P2 74, P5 360, P6 339 |
| M30 | solution: the wait from the last run alone | P1 267, P2 87, P6 267 |

P1 and P6 kill all seventeen, P5 ten, P2 nine, P4 five and P3 two. P3,
every type turned around, fails only the edits that read a type for
more than whether it is equal to another: the wait taken from the type
before in the sorted list, and the day stored under the next type. P4,
a task of a new type appended, fails the edits that let a new type wait
or that never move the day on.

The edits first run were four others: the wait one day short in the ★,
iter and template arms, and the iter arm's last day left as the first.
The wait one day short fails alike in every arm, as the allowed arm's
earliest day without the one (M7) and the template's space halved
(M31), and the last day left as the first as the prev arm's previous
place the first of its type (M12). They were replaced by the ★ arm's
only a task run the day before waits (M1), the iter arm's new type
started a day late (M22) and day stored under the next type (M23), and
the template's first task's day never stored (M27).

Of the thirty-one, fourteen were not kept. The last day kept from the
first run fails alike in the ★, allowed and template arms (M3, M8, M28)
as the prev arm's (M12); the day not moved on before the wait and the
wait one day long in the ★ arm (M4, M5) as the template's day moved on
after the wait (M29); the day taken as the earliest only and the wait
from the type alone (M9, M25) as the template's wait from the last run
alone (M30); the wait counted from the previous place in the prev arm
(M14) and the template's space halved (M31) as the allowed arm's
earliest day without the one (M7); the iter arm's space counted twice
(M26) as the allowed arm's space doubled (M11); and the template's
first task's day never stored (M27) as the compress arm's type that ran
on day 1 taken as new (M18). The prev arm's places sorted by type only
(M13) is no slip, since the sort is stable and keeps each type's places
in order, nor is the compress arm's types left with their duplicates
(M17), since `binary_search` finds one place for each value. The types
left unsorted (M21) stop on an `unwrap` of `None` when `binary_search`
misses a type.

## Verification

Every arm prints the same output as `tasks.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.5 to 2.5 s but the allowed
arm, 15.2 s. On the line of `10^5` distinct tasks the types fall from
`10^9`, so its `SortedMap` takes every key at the front, and the
interpreter's sorted table shifts every later entry on each such insert,
as in kata 2364's direct arm. Under `karac __mir-llvm-run` it takes
0.33 s (B-2026-11-21-50). The differential takes 25 s under `karac __mir-run` and
0.89 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 lists of `10^5` tasks once from the harness's
generator, list `a` holding tasks of `4^(a / 2 + 1)` types (at most
`10^5`) up to `10^9` with a space of `3^a`, then makes 20 passes, pass
`p` folding each answer plus `p` into the checksum, with the ★ arm in
all five languages. Every implementation prints `20 passes over 10
lists of 10^5 tasks: checksum 56801713`. Rust uses `HashMap` and Go its
`map`, both seeded hash maps as Kāra's `Map` is, and Python its dict. C
has no hash map in its standard library, so it carries one of open
addressing with linear probing over `2^18` slots, the key mixed by
splitmix64's finalizer: the same algorithm over a different table, which
the comparison should be read with. Every implementation builds its map
afresh in each call.

BENCHTAB
