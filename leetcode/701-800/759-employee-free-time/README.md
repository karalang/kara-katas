# 759. Employee Free Time

Each employee's schedule is a sorted list of working intervals that do
not overlap. Return, sorted, the finite intervals of positive length in
which every employee is free: the gaps after the first interval starts
and before the last one ends.

```
[[1, 2], [5, 6]]  [[1, 3]]  [[4, 10]]            ->  [[3, 4]]
[[1, 3], [6, 7]]  [[2, 4]]  [[2, 5], [9, 12]]    ->  [[5, 6], [7, 9]]
```

**Constraints:** 1 to 50 employees with 1 to 50 intervals each; 0 <=
start < end <= 10^8.

## Approaches

Every arm takes and returns `Interval` structs with `start` and `end`,
as LeetCode's version does.

| file | mechanism |
|---|---|
| `employee_free_time.kara` ★ | pool every interval, sort by start and sweep, keeping the latest end; an interval that starts past it leaves a gap; O(n log n) |
| `employee_free_time_heap.kara` | a `PriorityQueue` holding each employee's next interval, smallest start first, hands the intervals out in order without sorting them; the same sweep; O(n log k) for k employees |
| `employee_free_time_events.kara` | each interval as a start and an end event, sorted with starts first at equal times; the number of people working is counted, and everyone is free from when it falls to zero until the next start |
| `employee_free_time_merge.kara` | the employees' sorted lists merged in pairs, then the results in pairs, into one list of busy intervals, each merge fusing intervals that overlap or touch; the free time is the gaps between them |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: the two LeetCode examples; one
employee with one interval and with three; intervals that touch end to
start; one long interval covering another employee's; employees given
out of order; and one interval covering three; then 300 random schedules
of up to 50 employees with up to 50 intervals each, up to 10^8, with the
number of free intervals, their total length and a checksum.
`employee_free_time.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which looks at each unit of time from t to t + 1 and calls it free when
no interval covers it; the free intervals are the runs of free units
after the first start and before the last end. 1,500 random schedules of
one to four employees with one to four intervals each, within 0 to
36, are checked against it, and 300 large ones like the arms' own
against the other properties.

| | property |
|---|---|
| P1 | the answer is the definition's (the 1,500 small schedules) |
| P2 | it is valid free time: sorted, each interval of positive length and apart from the next, inside the working day, and overlapping no one's working interval |
| P3 | shuffling the employees, and splitting one employee's intervals between two employees, changes nothing |
| P4 | the schedule in a mirror, each time t made m - t, has this answer mirrored |

It prints `1800 schedules (6327 free intervals), 4 arms, 27600 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the intervals sorted by end | P1 167, P2 464, P3 115, P4 670 |
| M2 | ★: a gap of no length kept | P1 537, P2 537 |
| M3 | ★: the latest end replaced by every interval's | P1 297, P2 594, P3 215, P4 667 |
| M4 | heap: each employee's last interval dropped | P1 1271, P2 543, P3 577, P4 1512 |
| M5 | heap: a gap before the first interval | P1 1500, P2 1800, P4 1800 |
| M6 | heap: each employee's first interval queued by its end | P1 734, P2 1032, P3 740, P4 1073 |
| M7 | events: ends before starts at the same moment | P1 537, P2 537 |
| M8 | events: sorted by time alone | P1 340, P2 340, P3 300, P4 501 |
| M9 | events: free time starting one late | P1 1325, P2 1052, P4 1624 |
| M10 | merge: intervals that touch not fused | P1 537, P2 537 |
| M11 | merge: a fused interval's end replaced even by a smaller one | P1 393, P2 690, P3 698, P4 730 |
| M12 | merge: the odd list out dropped | P1 211, P2 368, P3 775 |
| E1 | events: idle tested as since a time above 0 | 0 |
| E2 | ★: the latest end started at the first interval's start | 0 |
| E3 | merge: ties taken from the second list | 0 |

P1 kills all twelve. M2, M7 and M10 each report a free interval of no
length where one interval ends as another starts, and only P1 and P2 see
them: shuffling or mirroring a schedule keeps such a meeting, so the
wrong answers agree. P3 also misses M5 and M9, whose wrong answers do
not depend on the order of the employees, and P4 misses M12, since a
mirrored schedule drops the same odd list. The first edit tried for
M8 set `idle_since` when the last but one person stopped working; it
survived, rightly, since the count must then fall to zero, which sets
`idle_since` again before any start reads it, so it was replaced.
E1 tests `idle_since > 0`, but no interval ends at 0; E2 starts the
latest end at the first interval's start, which that interval raises at
once; E3 takes ties between two lists from the second, but intervals
that start together are fused either way.

## Verification

Every arm prints the same output as `employee_free_time.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a62eacd307`, whose last compiler change is `7d736aae75`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the heap and merge arms: each prints
the same output under `karac run` (the legacy JIT), `karac build` and an
auto-par build, and the merge arm under the legacy interpreter too; the
heap arm ran past the check's 60 s limit under the legacy interpreter of
the debug build. They refuse the ★ and events arms, the differential and
the bench at a `*` over an element of `iter()` (`all.push(*interval);`,
`if *kind == 0`), which legacy gives by value where v2 gives references.
The legacy timings below are of a copy of the bench without that `*`,
which prints the same line. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, on 3,000 random
schedules of 50 employees with 50 intervals each, the most LeetCode
allows, adding up the free time and a checksum. Every implementation
prints `3000 schedules of 50 x 50 intervals: 6338 free intervals,
1861793582 free in all, checksum 941431521`, the Kāra program under
`karac __mir-run` included (in 71 s). C holds the schedule in a fixed
array and sorts with `qsort`; Go sorts with `sort.Slice`.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.68 to 0.76 s |
| Rust (`rustc -O`) | 0.25 to 0.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.27 to 0.33 s |
| Go | 1.36 to 1.52 s |
| Python | 8.6 to 8.9 s |
| Kāra (`karac build --mir`) | 0.38 to 0.43 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
2.4 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.40 s,
against C's 0.71, Rust's 0.30 (0.31 under overflow checks) and Go's
1.41. Under valgrind's cachegrind v2 runs 2.8 billion instructions, Rust
2.4 billion and C 4.2 billion; C makes 138 million indirect branches,
presumably `qsort` calling its comparison function, where Rust and Kāra
inline theirs (inferred, not profiled). The legacy build of the same
program ran 0.24 to 0.26 s, a median of 0.25 s in the interleaved runs,
so v2 takes 1.6 times as long as legacy, inside M2's limit of twice
legacy; new katas' benches are outside M2's frozen set in any case. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new.
