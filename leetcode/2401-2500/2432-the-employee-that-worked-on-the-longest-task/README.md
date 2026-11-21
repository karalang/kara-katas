# 2432. The Employee That Worked on the Longest Task

There are `n` employees, each with a unique id from `0` to `n - 1`.

You are given a 2D integer array `logs` where `logs[i] = [id_i,
leaveTime_i]` where:

- `id_i` is the id of the employee that worked on the `i`th task, and
- `leaveTime_i` is the time at which the employee finished the `i`th
  task. All the values `leaveTime_i` are **unique**.

Note that the `i`th task starts the moment right after the `(i - 1)`th
task ends, and the `0`th task starts at time `0`.

Return *the id of the employee that worked the task with the longest
time.* If there is a tie between two or more employees, return *the
**smallest** id among them*.

```
n = 10, logs = [[0,3],[2,5],[0,9],[1,15]]  ->  1
n = 26, logs = [[1,1],[3,7],[2,12],[7,17]] ->  3
n = 2,  logs = [[0,10],[1,20]]             ->  0
```

**Constraints:** `2 <= n <= 500`; `1 <= logs.length <= 500`;
`logs[i].length == 2`; `0 <= id_i <= n - 1`; `1 <= leaveTime_i <= 500`;
`id_i != id_{i+1}`; `leaveTime_i` are sorted in a strictly increasing
order.

Each task runs from the leave time before it to its own, so one pass
with the last leave time in hand measures every task, and the answer is
the least id among the longest. Only the tie needs care: a longer task
replaces the best, and an equal one only when its id is smaller.

## Approaches

| file | mechanism |
|---|---|
| `longest.kara` ★ | one pass over the logs, the last leave time carried as the next task's start, the best replaced by a longer task or by an equal one of a smaller id. O(m) |
| `longest_naive.kara` | the statement read directly: every employee in order of id, the longest of their tasks found by scanning every log, and the best replaced only by a strictly longer one, so the least id keeps a tie. O(n m) |
| `longest_sort.kara` | every task as a tuple of its length negated and its id, `sort`ed, so the first tuple is the longest with the least id. O(m log m) |
| `longest_map.kara` | a `SortedMap[i64, i64]` from each length to the least id that worked one that long, the answer in its `last` entry. O(m log m) |
| `longest_iter.kara` | iterators: the starts as `once(0)` `chain`ed before the leave times, `zip`ped with the logs, each mapped to its length and its id negated, and the largest by `max`. O(m) |
| `longest_solution.kara` | LeetCode's Rust template: `logs` a `Vec<Vec<i32>>`, the first log taken as the best before a loop from 1, and each length compared with `\|\|` and `&&`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples; one log;
every task one unit long, so the least id of all wins; the longest task
last; a tie between a high id first and a low id last; the constraints'
largest, 500 logs of one unit each by ids falling from 499, then one of
them made two units; 250 random logs over 500 employees; and 3000 random
cases of 2 to 10 employees and 1 to 12 logs, full of ties, as a checksum
and the total. `longest.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on every list of 1 to 5 logs
over 2 to 4 employees with leave times from 1 to 8, 33756 of them,
against the least id among the longest tasks found by `max` and `min`.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 6 edits: the three brackets of
`Vec<Vec<i32>>`; `||` written `or` and `&&` written `and`; and `struct
Solution;` given its braces. The loop over `1..logs.len()` and the
indexing `logs[i - 1][1]` stand as Kāra.

Writing the iter arm, `std.iter.once(0)` drew `E0100`, Kāra's library
having no `std.iter` path, and `karac fix` wrote it `once(0)`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every task's length found from the log before it, each task
tested against every other for one that lasted longer, and the least id
among the tasks that none outlasts. No best is carried through the
logs. It checks 300 random cases of 2 to 10 employees and 1 to 12 logs,
leave times rising by 1 to 1 up to 1 to 4, full of ties; then 30 of up
to 500 employees and 500 logs, leave times up to 500; then 30 of up to
50 employees and 50 logs, every task one unit long. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every leave time doubled: the same answer |
| P3 | a last task longer than any, by a new employee `n`, with `n + 1` employees: `n` |
| P4 | the answer worked a task as long as any |
| P5 | every id raised by one, with `n + 1` employees: the answer plus one |
| P6 | each arm agrees with at least three of the other five |

P2 holds because doubling every leave time doubles every length and
keeps their order. P3 holds because the new task outlasts every other.
P5 holds because raising every id keeps their order, so the tie goes the
same way. P2 and P3 take the leave times past 500, outside the
constraints; every arm holds for any rising leave times.

The differential prints `360 cases: checksum 321054251, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and takes the least id among the longest tasks. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the start never moved | P1 243, P4 72, P6 243 |
| M3 | ★: a tie never replaces | P1 195, P6 195 |
| M6 | ★: the first task never tried | P1 236, P3 284, P4 89, P6 236 |
| M9 | naive: each start the log two before | P1 117, P3 70, P4 37, P6 117 |
| M10 | naive: an employee's last task, not their longest | P1 43, P4 12, P6 43 |
| M11 | naive: the first task started at 1 | P1 41, P2 18, P4 18, P5 16, P6 41 |
| M12 | sort: the shortest first | P1 164, P3 360, P4 141, P6 164 |
| M14 | sort: the length answered for the id | P1 323, P2 360, P3 317, P4 191, P5 360, P6 323 |
| M15 | sort: never sorted | P1 248, P3 360, P4 84, P6 248 |
| M17 | map: the last id kept for a length | P1 197, P6 197 |
| M18 | map: the largest id kept for a length | P1 277, P6 277 |
| M21 | map: the start moved before the length | P1 91, P3 360, P4 91, P6 91 |
| M23 | iter: the shortest task | P1 325, P3 360, P4 131, P6 325 |
| M24 | iter: the id never negated | P1 344, P3 360, P4 344, P5 360, P6 344 |
| M25 | iter: the starts one log behind | P1 117, P3 80, P4 44, P6 117 |
| M27 | solution: the first task one unit short | P1 26, P2 3, P4 3, P6 26 |
| M29 | solution: the last log never tried | P1 47, P3 360, P4 16, P6 47 |


P1 and P6 kill all seventeen, P4 fourteen, P3 ten, and P2 and P5
three.

Fourteen are not kept. Ten fail exactly as a kept one. Four take a tie
by the larger id, as the map arm's largest id kept for a length (M18):
the ★, naive and iter arms' and the template's (M1, M7, M22, M28). Two
take a tie by the later log, as the map arm's last id kept (M17): the ★
arm's tie always replaces and the iter arm's later log (M4, M26). The ★
arm's leave time taken as the length and the sort arm's start never
moved (M5, M16) fail as the ★ arm's start never moved (M2), the same
reading. The sort arm's last pair answered (M13) fails as the iter
arm's shortest task (M23); the map arm's shortest answered (M19) as the
sort arm's shortest first (M12); and the map arm's first id kept for a
length (M20) as the ★ arm's tie never replaces (M3), both keeping the
first log of a tie. Three fail apart from every kept one and were left
out because those arms keep their share already: the naive arm's last
employee never tried (M8), and the template's first task never the best
and length from the log after (M30, M31).

Five of the first run were replaced. The map arm's each length one
short is equivalent, since it keeps every comparison between lengths;
its first length never kept and the iter arm's first log never zipped
ended in `unwrap()` on `None` on a single log, a crash; and the iter
arm's every start 0, written `once(0).cycle()`, is refused by `check`
with `E0236`, since `cycle` takes a `Clone` iterator and `IterOnce` is
not one, as the library's `cycle` section says. They became the map
arm's first id kept for a length and start moved before the length
(M20, M21) and the iter arm's id never negated and tie taken by the
later log (M24, M26). The sort arm's id negated too, a seventh copy of
the larger id on a tie, became the length answered for the id (M14), so
that the ★, sort, map and iter arms had a signature of their own each.

## Verification

Every arm prints the same output as `longest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.5 s, and the
differential 2.8 s; under `karac __mir-llvm-asan` the differential
takes 0.9 s and under `karac run` 0.5 s.

## Benchmarks

The bench builds 2000 cases once from its own generator, each 500
employees and 500 logs, the constraints' largest, no two logs in a row
by one employee and the leave times rising by 1 to 3. It then makes 50
passes; each moves every case's last leave time on by one, so the last
task grows and no answer can be carried from one pass to the next, then
answers every case, folding the answer plus the pass into the checksum.
The bench uses the ★ arm, the one pass, in all five languages. Every
implementation prints `50 passes over 2000 cases of 500 logs: checksum
359514848`. Each case is a list of rows in every language, and in C an
array of row pointers.

BENCHTAB
