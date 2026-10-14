# 630. Course Schedule III

There are `n` online courses, each given as `[duration, lastDay]`: the
course takes `duration` days without a break and must be finished by day
`lastDay`. Starting on day 1, and taking one course at a time, return
the most courses that can be taken.

```
courses = [[100,200],[200,1300],[1000,1250],[2000,3200]]  ->  3
courses = [[1,2]]                                         ->  1
courses = [[3,2],[4,3]]                                   ->  0
```

**Constraints:** 1 to 10,000 courses; each `duration` and `lastDay` from
1 to 10,000.

## Approaches

Every arm is `fn schedule_course(courses: Vec[Vec[i64]]) -> i64` and
takes the courses in order of last day: a set of courses can all be
finished exactly when taking them by last day finishes each one in time.

| file | mechanism |
|---|---|
| `schedule_course.kara` ★ | each course added in turn and, when the total runs past its last day, the longest course taken so far dropped, from a largest-first `PriorityQueue` of the durations taken; O(n log n) |
| `schedule_course_swap.kara` | a course that fits added, and one that does not swapped for the longest course taken, found by scanning a `Vec`, when that one is longer; O(n^2) |
| `schedule_course_mintime.kara` | for each count, the least total time of that many courses that all fit, extended by each course in turn; the answer is the largest count reached; O(n^2) |
| `schedule_course_multiset.kara` | the ★ arm's greedy with the durations taken in a `SortedMap` from duration to how many, the longest being its largest key; O(n log n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: the three LeetCode examples; six
more (a long early course dropped for two later ones, three equal
courses of which one fits and of which two fit, a mix of seven that
keeps three, the largest single course, and one longer than its own last
day); a total and checksum over 300 random cases of 1 to 30 courses
lasting 1 to 100 days with last days up to 1,000; and the answers for
2,000 courses with the problem's largest durations and last days and for
2,000 one-day courses due by day 1,000 at the latest.
`schedule_course.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the most courses in any subset that can all be finished, checking every
subset by taking its courses by last day. Each of 1,000 random cases has
2 to 9 courses lasting 1 to 6 days with last days from 1 to 15, so that
most do not all fit, and a second set of 15 to 40 courses lasting 1 to
4 days with last days up to 30, too many subsets to list, for which the
definition is a table over total time: taking the courses by last day,
the most courses whose durations add up to exactly each total, every one
finished by its last day.

| | property |
|---|---|
| P1 | the count is the definition's, for both sets |
| P2 | the courses in reverse order give the same count |
| P3 | a course longer than its own last day changes nothing |
| P4 | every duration and last day doubled changes nothing |
| P5 | without the first course, the count is the same or one less |

It prints `1000 cases (3433 courses taken), 4 arms, 20000 checks,
0 failures`, counting the small sets' courses, under `karac __mir-run`
and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the courses taken by duration, not last day | P1 982, P2 142 |
| M2 | ★: a course ending on its last day counted as late | P1 682 |
| M3 | swap: the scan for the longest skipping the second course | P1 96, P2 18, P5 3 |
| M4 | swap: a course ending on its last day counted as late | P1 682 |
| M5 | mintime: a course allowed to end a day late | P1 587, P4 226 |
| M6 | mintime: a course added without its duration | P1 1000, P3 1000 |
| M7 | multiset: a dropped duration left in the map when it was taken twice | P1 136 |
| M8 | multiset: the new course's duration taken off instead of the longest | P1 749, P2 49, P5 13 |
| E1 | ★: the lateness test written the other way round | 0 |
| E2 | swap: a taken course as long as the new one swapped for it | 0 |
| E3 | mintime: an equal total stored again | 0 |
| E4 | multiset: the last copy recognised as fewer than two | 0 |

P1 kills all eight, and M7 only through the second, larger set: it
leaves a phantom copy of a dropped duration in the map, which goes wrong
only after two drops of the same longest duration and a later overflow.
An earlier version of this differential with the small sets alone did
not reach that, and M7 survived it. M2 and M4 are the same edit in two
arms and fail the same counts. P2 sees the mutants whose answer depends
on the order of courses with the same last day or on the order they were
given in: M1's sort by duration, M3's scan, and M8's wrong total.
P3 sees only M6, which adds a course without its duration, so even an
impossible course fits. P4 sees only M5: a day of slack no longer scales
when every day is doubled. P5 sees M3 and M8, whose counts drop by more
than one when a course is removed. The four survivors cannot change an
answer: `time > last` and `last < time` are the same test; swapping a
course for one as long changes neither the count nor the total; storing
an equal total again stores the same value; and a count is 1 exactly
when it is fewer than two.

## Verification

Every arm prints the same output as `schedule_course.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `ead49e635f` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends refuse every file at type checking. They
still hold the old rule that an argument which is already a `mut ref`,
as `seed` is inside `random_courses`, drops its call-site `mut` marker;
they take a bare parameter by value, so the bench's
`schedule_course(all[...])` is "cannot move out of an index expression";
and they type the items of a `Vec`'s `iter()` by value, so the
differential's `*b` is an error. Legacy is frozen, so these are noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 inputs of 10,000 courses,
the problem's most, each lasting 1 to a random longest from 10 to
1,000 days with a last day from 1 to 10,000, once; then 200 times
answers one of them, picked by the round, adding up the answers and
putting each into a checksum. Every implementation prints `20 inputs,
200 rounds: total 162630, checksum 858755461`, the Kāra program under
`karac __mir-run` included (in 65 s).

Each implementation copies the courses, sorts the copy by last day and
keeps a max-heap of the durations taken. Kāra and Rust clone a `Vec` of
10,000 two-element `Vec`s, so each round allocates 10,001 vectors; Go
copies the outer slice and Python builds a sorted list, both sharing the
inner lists; C copies a flat array of pairs. Rust uses `BinaryHeap`, Go
`container/heap`, Python `heapq` and C a hand-written binary heap. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine), each including making the
inputs:

| | time |
|---|---|
| C (`clang -O3`) | 0.37 to 0.41 s |
| Rust (`rustc -O`) | 0.25 to 0.29 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.26 to 0.27 s |
| Go | 0.69 to 0.80 s |
| Python | 1.14 to 1.16 s |
| Kāra (`karac build --mir`) | 0.51 to 0.54 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses it as above;
that edit is by hand, on top of the `scripts/new-bench.sh` output. A
copy outside the kata that takes `courses` as `ref Vec[Vec[i64]]` builds
under legacy and takes 0.56 to 0.62 s, so the v2 build is a little ahead
of legacy. Under `karac __mir-llvm-run` the program prints the same line
in 2.8 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

The Kāra build is about twice the Rust build. Two copies of the bench
outside the kata split it, two runs each: answering only up to the sort,
so cloning and sorting, takes 0.37 to 0.38 s in Kāra and 0.22 to 0.27 s
in Rust, and the heap loop is the rest, about 0.15 s in Kāra against a
few hundredths in Rust. Neither part is profiled further. Go, the
slowest compiled row, is not profiled.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
