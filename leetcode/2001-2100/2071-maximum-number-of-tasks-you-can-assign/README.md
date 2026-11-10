# 2071. Maximum Number of Tasks You Can Assign

You have `n` tasks and `m` workers. Each task has a strength requirement
stored in a 0-indexed integer array `tasks`, with the `i`-th task
requiring `tasks[i]` strength to complete. The strength of each worker is
stored in a 0-indexed integer array `workers`, with the `j`-th worker
having `workers[j]` strength. Each worker can only be assigned to a
single task and must have a strength greater than or equal to the task's
strength requirement (i.e., `workers[j] >= tasks[i]`).

Additionally, you have `pills` magical pills that will increase a
worker's strength by `strength`. You can decide which workers receive
the magical pills, however, you may only give each worker at most one
magical pill.

Given the 0-indexed integer arrays `tasks` and `workers` and the integers
`pills` and `strength`, return the maximum number of tasks that can be
completed.

```
tasks = [3,2,1], workers = [0,3,3], pills = 1, strength = 1                ->  3
tasks = [5,4], workers = [0,0,0], pills = 1, strength = 5                  ->  1
tasks = [10,15,30], workers = [0,10,10,10,10], pills = 3, strength = 10    ->  2
```

**Constraints:** `n == tasks.length`; `m == workers.length`;
`1 <= n, m <= 5 · 10^4`; `0 <= pills <= m`;
`0 <= tasks[i], workers[j], strength <= 10^9`.

If `k` tasks can be done, the `k` easiest can, by the `k` strongest
workers, and `k - 1` can too; so the most is found by a binary search
over `k`, each `k` tested greedily. The test that is linear goes through
the workers weakest first: every task a pill would bring in reach waits
in order, and a worker does the easiest waiting task if able, and
otherwise takes a pill and the hardest waiting task, since a pill-taker
is the only kind of worker who could need it. The approaches differ in
the test and in how they search.

## Approaches

| file | mechanism |
|---|---|
| `tasks.kara` ★ | the binary search, each `k` tested workers weakest first with the waiting tasks in a `VecDeque`, a `match` on `front()` with a guard. O((n + m) log(n + m)) |
| `tasks_multiset.kara` | the test from the tasks' side, hardest first: the workers a multiset, a `SortedMap` from strength to count; a task to the strongest if able, else with a pill to the weakest a pill makes able, found by `ceiling` |
| `tasks_free.kara` | the same tasks'-side test with no tree: the workers a sorted `Vec`, a worker given a task struck off with a next-free link followed with path halving, the weakest a pill makes able from `partition_point` |
| `tasks_partition.kara` | the search left to `partition_point` over the counts laid out as a `Vec`; the ★ test with a plain `Vec` as the deque, a `head` index for its front and `pop` for its back |
| `tasks_pool.kara` | the workers as a value: a `struct Pool` over a `SortedSet` of (strength, place) pairs with methods to give a task to the strongest or to the weakest of at least some strength, the second by `range_inclusive(..).next()` |
| `tasks_solution.kara` | LeetCode's Rust template (`use std::collections::VecDeque`, `mut` parameters, a `check` closure `\|k: usize\| -> bool` that captures the sorted lists, `*dq.front().unwrap()`, `let (mut lo, mut hi)`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's four examples and four
more, each problem's sizes, pills and answer; then the sum of the
answers and a checksum for 300 random problems of 1 to 40 tasks and 1 to
40 workers, strengths up to 20 or `10^9`, pills up to the workers and a
pill's strength up to the largest; then the answer for the constraints'
largest, 50000 tasks and 50000 workers with 1000 pills of `10^7`.
`tasks.py` mirrors the ★ arm and its output is byte-identical; it also
agrees with an exhaustive search over 3000 random problems of up to six
tasks and six workers.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way of giving tasks to workers tried by a search, each
task left undone or given to a worker not yet used who is able, with a
pill if one is left and the worker needs it, and the most tasks done
kept. It checks 300 random problems of 1 to 6 tasks and 1 to 6 workers,
strengths up to 20, pills up to the workers and a pill's strength up to
20; then 20 whose every worker is weaker than every task, so only pills
help, and 20 with pills of strength 0. All 340 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the tasks and the workers in reverse order leave the answer |
| P3 | one more pill, or a pill one stronger, never lowers the answer |
| P4 | every strength doubled, a pill's too, leaves the answer |
| P5 | the answer is at most the tasks and at most the workers, at least the answer with no pills, and at most that and the pills |
| P6 | each arm agrees with at least three of the other five |

The upper bound in P5 holds because a matching grows by at most one for
each edge a pill adds.

The differential prints `340 problems: checksum 963155379, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
problems. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, four to six to each of its arms, each
run under `karac __mir-llvm-run`, and the kept ones and the survivors
under `karac __mir-run` too. Seventeen are kept, three to each Kāra arm
and two to the Rust-template arm. Each kept one is killed, fails the
same way under both backends and not by a crash, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the easiest waiting task taken even with a pill | P1 9, P6 9 |
| M2 | ★: the weakest workers chosen | P1 86, P5 31, P6 86 |
| M3 | ★: tasks let in only when a worker can do them unaided | P1 94, P6 94 |
| M4 | multiset: the weakest worker, not the strongest, tried first | P1 50, P6 50 |
| M5 | multiset: a pill given to the strongest | P1 37, P6 37 |
| M6 | multiset: the tasks easiest first | P1 67, P6 67 |
| M7 | free: a worker struck off still found | P1 14, P6 14 |
| M8 | free: the strongest's cursor never moved past the taken | P1 36, P6 36 |
| M9 | free: no pill counted | P1 12, P5 8, P6 12 |
| M10 | partition: the front waiting task taken from the back too | P1 32, P3 6, P5 1, P6 32 |
| M11 | partition: the counts from 0 | P1 340, P5 250, P6 340 |
| M12 | partition: an empty deque not refused | P1 43, P3 3, P5 1, P6 43 |
| M13 | pool: a pill's strength counted twice | P1 20, P6 20 |
| M14 | pool: the strongest able to do a task one short | P1 13, P6 13 |
| M15 | pool: a pill's need one less | P1 6, P4 6, P6 6 |
| M16 | solution: the adapter's pills one fewer | P1 41, P6 41 |
| M17 | solution: the adapter's workers all one weaker | P1 18, P6 18 |

P1 and P6 kill all seventeen, P5 five, P3 two and P4 one; P2 none. Every
arm sorts the tasks and the workers before anything else, so no edit
here could make one depend on their order, and doubling every strength
changes only an edit off by a fixed step, as M15's `- 1` is. P5's bounds
see an answer below the one with no pills, or above it by more than the
pills: the weakest workers chosen (M2), a pill never spent (M9), a count
off by one (M11). P3 sees the partition arm's broken deque (M10, M12),
whose answer can fall when a pill is added. So most kept edits are told
apart by how often they are wrong, not where, and the literal reading
is what they are measured against.

Of the thirty, thirteen were not kept. Two survive, and both are
equivalent: the ★ arm's middle taken as `(lo + hi) / 2 + 1`, which lies
in `(lo, hi]` as the search needs, and the free arm's halving done in
the other order, which still leads only upward to a free worker. One
crashes and is not kept: the pool arm's equal strengths merged leaves
the set short of workers, and `max().unwrap()` meets an empty set. Five
fail as a kept one: the pool arm's pill-taker the strongest above the
need and the Rust arm's pill taking the easiest task as M1; the ★ arm's
worker who can do the easiest task taking a pill anyway as M14; the
multiset and partition arms' pill never used up as M9. Four fail in two
pairs and none of them is kept: the partition arm's counts one short and
the Rust arm's search one short (P1 250), and the free arm's pill-taker
looked for one place too high and the multiset arm's pill-taker with
exactly the need refused (P1 2). One is killed with checks of its own
but was left out because its arm keeps three: the multiset arm's
worker's count never taken down (P1 38).

## Verification

Every arm prints the same output as `tasks.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 1.8 s to 3.0 s, except the
multiset and pool arms at 9.6 s and 10.4 s, whose every test builds a
tree of the workers, and the differential 1.2 s (timed while other work
shared the machine).

No arm met a compiler gap that stopped it. The pool arm's
`self.workers.pop_last();` drew a `must_use` warning for the discarded
`Option`, with the help `let _ = ..` but no fix `karac fix` could apply,
while the same discard on a `VecDeque`'s `pop_front` or a `Vec`'s `pop`
drew none: design.md § `#[must_use]` exempts the container methods whose
`Option` reports a displaced value, and its list named neither
`SortedSet` nor `SortedMap`'s `pop_first` and `pop_last`. They are now on
it, in the compiler and in design.md, and the arm writes the discard as
a statement.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 24 and 1 edits: Rust's spellings (the `VecDeque`
import deleted, `Vec<..>` and `VecDeque<..>` to brackets, `mut tasks:`
to `tasks: own` with a `let mut` in the body, the closure's `-> bool`
dropped, `let (mut lo, mut hi)` to `let mut (lo, hi)`, `&&` to `and`,
`::` paths to `.`, `struct Solution;` to `struct Solution {}`, the `&`
of `|&t|` dropped); then the closure's `k: usize` to `i64`, Kāra's type
for counts and places, which the `n.min(m)` it is compared with already
is. The fixed arm reads as the template does.

## Benchmarks

The bench answers 12 problems of the constraints' largest size with the
★ arm in all five languages: 50000 tasks and 50000 workers, strengths up
to `10^9`, 0 to 11000 pills of strength `10^7`. C and Go keep the deque
as an array the size of the tasks with a head and a tail; Rust uses its
`VecDeque`. Every implementation prints `12 problems: sum 599448,
checksum 805443067`.

BENCHTAB
