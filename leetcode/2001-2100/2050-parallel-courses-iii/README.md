# 2050. Parallel Courses III

You are given an integer `n`, which indicates that there are `n` courses
labelled from `1` to `n`. You are also given a 2D integer array
`relations` where `relations[j] = [prevCourse, nextCourse]` denotes that
course `prevCourse` has to be completed before course `nextCourse`, and a
0-indexed integer array `time` where `time[i]` denotes how many months it
takes to complete the `(i + 1)`th course.

You must find the minimum number of months needed to complete all the
courses, following these rules: you may start taking a course at any time
if its prerequisites are met, and any number of courses can be taken at
the same time. Return the minimum number of months. The graph is a
directed acyclic graph.

```
n = 3, relations = [[1,3],[2,3]], time = [3,2,5]                      ->  8
n = 5, relations = [[1,5],[2,5],[3,5],[3,4],[4,5]], time = [1,2,3,4,5]  ->  12
```

**Constraints:** `1 <= n <= 5 * 10^4`; `0 <= relations.length <=
min(n * (n - 1) / 2, 5 * 10^4)`; `1 <= prevCourse, nextCourse <= n`,
`prevCourse != nextCourse`; all the pairs are unique; `time.length == n`;
`1 <= time[i] <= 10^4`; the graph has no cycle.

With as many courses at once as wanted, each course starts the month its
last prerequisite finishes. So each course's finish is its own time after
the latest of its prerequisites' finishes, and the answer is the latest
finish: the heaviest path through the graph, counting each course's time.

## Approaches

| file | mechanism |
|---|---|
| `courses.kara` ★ | Kahn's topological order: each course waits for as many prerequisites as it has, a `VecDeque` starts with those that have none, and a course taken from it hands its finish on to each course it unlocks as the latest start so far |
| `courses_memo.kara` | a memoized recursion over the prerequisites: a course's finish is its own time after the latest of its prerequisites', each worked out once and kept in a `Vec[Option[i64]]`; 50000 calls deep on a chain |
| `courses_stack.kara` | the same recursion with an explicit stack: a course is pushed, then its unfinished prerequisites (collected with a `filter`); back on top with all of them finished, it finishes itself |
| `courses_heap.kara` | the term simulated: a `PriorityQueue` holds each course being taken by the month it finishes, smallest first; when one finishes, a course it unlocks that waits for nothing more starts that month |
| `courses_rounds.kara` | relaxation in rounds, as Bellman-Ford finds a longest path: every course starts finished at its own time, and each round walks the relations, pushing a finish later where a prerequisite ends after it starts, until a round changes nothing |
| `courses_solution.kara` | LeetCode's Rust template, Kahn's order (`use std::collections::VecDeque`, `let n = n as usize`, `vec![vec![]; n]` and `vec![0; n]`, relations as `Vec<Vec<i32>>` read `r[0] as usize - 1`, `for &v in &graph[u]`, `*dist.iter().max().unwrap()`), carried by `karac fix` in three rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more,
each graph and its answer; then the sum and a checksum of the answers for
2000 random graphs of 2 to 30 courses and up to 60 relations; then for
three graphs of 50000 courses with times up to 10^4, the constraints'
limits: a chain through every course in reverse order, a random graph of
50000 relations, and every other course required by course 1. Each random
graph takes its relations from a random order of the courses, so it has no
cycle, and no relation twice. `courses.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the months simulated one at a time, every course not yet
started starting the first month all of its prerequisites are done, until
every course is. It checks 500 random graphs of 2 to 30 courses and up to
60 relations, drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least the longest course and at most all of them one after another |
| P3 | the courses relabelled at random, their times and relations with them, have the same answer |
| P4 | the relations listed in reverse order have the same answer |
| P5 | a new course of 7 months that requires every other course makes the answer 7 months later |
| P6 | each arm agrees with at least three of the other five |

The differential prints `500 graphs: checksum 304286841, 18000 checks over
6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-six edits to the differential, six to each of its arms, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and no
two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the answer the last course finished, not the latest | P1 66, P2 12, P3 30, P4 32, P5 66, P6 66 |
| M2 | ★: a course queued at its first prerequisite | P1 221, P3 112, P4 173, P5 84, P6 221 |
| M3 | ★: only the first course without prerequisites queued | P1 351, P2 242, P3 287, P5 355, P6 351 |
| M4 | memo: the prerequisites' finishes added, not the latest | P1 435, P2 327, P5 500, P6 435 |
| M5 | memo: only the last course's finish taken | P1 444, P2 201, P3 430, P5 444, P6 444 |
| M6 | memo: the own time counted twice | P1 500, P2 237, P5 500, P6 500 |
| M7 | stack: a course finished without its own time | P1 491, P2 274, P5 500, P6 491 |
| M8 | stack: the earliest prerequisite waited for | P1 422, P5 500, P6 422 |
| M9 | stack: a course finished before its prerequisites | P1 356, P3 318, P4 196, P6 356 |
| M10 | heap: the latest finish taken first (`max_first`) | P1 359, P2 153, P3 32, P6 359 |
| M11 | heap: a course unlocked starting at month 0 | P1 491, P2 342, P3 22, P5 500, P6 491 |
| M12 | heap: a course unlocked by its first prerequisite | P1 374, P5 442, P6 374 |
| M13 | rounds: only one round | P1 393, P4 412, P6 393 |
| M14 | rounds: a course pushed back by its prerequisite's time, not its own | P1 468, P2 72, P5 477, P6 468 |
| M15 | rounds: a course's finish pulled earlier (`<`) | P1 491, P5 500, P6 491 |
| M16 | solution: a course queued at its first prerequisite | P1 177, P3 80, P4 138, P5 122, P6 177 |
| M17 | solution: the course numbers read as 0-based | P1 346, P3 351, P5 242, P6 346 |

P1 and P6 kill all seventeen, P5 fourteen, P2 and P3 nine each and P4
five. P5 adds a course after every other, which an honest arm finishes
exactly 7 months after the rest; an arm that loses the latest finish
somewhere loses it there too, or finishes the new course early. P4 sees
the arms whose answer depends on the order the relations come in: one
round of relaxation (M13) settles a chain only when its relations come in
order, and the edits that let a course go before its last prerequisite
(M2, M9, M16) or keep the last finish rather than the latest (M1) depend
on which prerequisite comes last. P3 sees those too, and the edits that
pick a course by its number (M3, M5, M17) or a heap ordered by the wrong
end (M10, M11). P2 catches answers below the longest course or above all
of them in a row.

Of the thirty-six, five were not kept, all survivors and all equivalent.
Four reverse the relations, in the ★ arm, the memoized arm's prerequisite
lists, the rounds arm and the Rust arm's adapter: the heaviest path through
a graph is the heaviest path through its reverse, each course's time
counted once either way, so the answer cannot change. The fifth never
keeps the memoized arm's finishes, which only makes it recompute them.

The rest fail as a kept one does. A course finished at its start, without
its own time (★), and the earliest prerequisite waited for (memo) fail as
M15; a course started at its last prerequisite's finish (★) and the latest
overwritten by the last prerequisite (Rust) fail the same way as each
other; the prerequisites summed (stack) fails as M4, the answer the last
course's finish (stack) as M5, a course unlocked one month early (heap) as
M15; a course's first term 0 months long (heap), every course starting at
0 (rounds) and a course without prerequisites finished at 0 (Rust) fail
the same way as each other, as do only course 1's prerequisites walked
(stack) and the answer the first course's finish (rounds, Rust). The
answer the earliest finish (heap) fails on checks of its own.

## Verification

Every arm prints the same output as `courses.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
The memoized arm runs 50000 calls deep on the chain under every lane.
Under `karac __mir-run` the arms take 1.8 s (rounds) to 5.6 s (heap),
and the differential 5.0 s; on kara 3dcd076373.

The five Kāra arms met no compiler gap. One `while let Some(&v) =
stack.last()` was written in Rust's spelling, and `karac fix` turned it
into `Some(v) = stack.last().cloned()`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds of 10, 3 and 5 edits to a clean check: the `use` line
dropped, `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `vec![..; n]` to `Vec.filled(n, ..)`, `VecDeque::new()` to
`VecDeque.new()`, the `usize` casts to `i64`, `&v` in the `for` pattern
dropped and `&graph[u]` to `ref graph[u]`, and the fill `0` to `0i32`.
That last fix is new. `dist` is filled with `0`, which took the default
`i64` because nothing before the return fixed it, and the template
returns `*dist.iter().max().unwrap()` from a function that returns `i32`.
The fill's suffix was offered only where the value read was `dist[i]`;
the return was refused as a narrowing coercion with no fix. Kata 2050 added
the case to the compiler (kara 3dcd076373,
`tests/kata_2050_element_chain_suffix.rs`):
a chain that only walks a collection and picks one of its elements reads
an element as `dist[i]` does. The adapter hands the harness's `i64`s to the
template `as i32`, each relation as a two-element `Vec[i32]`, and widens
the `i32` answer back.

## Benchmarks

The bench draws 40 graphs of 50000 courses, each course but the first in
a random order requiring one of the `reach` courses before it, `reach`
running from 1 (a single chain) to 39001, with times up to 10^4, and
answers each with the ★ arm in all five languages: two million courses
scheduled. Drawing the graphs is part of the work timed. The C mirror
keeps each course's dependents in a growable array and its queue in a
ring as large as the courses. Every implementation prints `40 graphs: sum
241256921, checksum 776437722`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `3dcd076373` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.148 to 0.204 s | 0.162 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.172 to 0.194 s | 0.178 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.174 to 0.191 s | 0.182 s |
| Rust (`rustc -O`) | 0.173 to 0.235 s | 0.183 s |
| Kāra (`karac build`) | 0.177 to 0.203 s | 0.183 s |
| Go | 0.301 to 0.340 s | 0.321 s |
| Python | 3.9 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.175 s) is not above its real time (0.183 s).

The sequential Kāra program is 1.02x Rust under overflow checks and 1.12x
C.
