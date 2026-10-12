# 436. Find Right Interval

You are given an array of intervals, where `intervals[i] = [start_i,
end_i]` and each `start_i` is unique. The right interval for an
interval `i` is an interval `j` such that `start_j >= end_i` and
`start_j` is minimized. Note that `i` may equal `j`.

Return an array of right interval indices for each interval `i`. If no
right interval exists for interval `i`, put `-1` at index `i`.

```
intervals = [[1,2]]               ->  [-1]
intervals = [[3,4],[2,3],[1,2]]   ->  [-1,0,1]
intervals = [[1,4],[2,3],[3,4]]   ->  [-1,2,-1]
```

**Constraints:** `1 <= intervals.length <= 2 * 10^4`;
`-10^6 <= start_i <= end_i <= 10^6`; the start of each interval is
unique.

## Approaches

Every arm takes the intervals as `Vec[(i64, i64)]`, borrowed, and
returns a new `Vec[i64]`.

| file | mechanism |
|---|---|
| `right_interval.kara` ★ | sort the indices by start once, then for each interval binary search that order for the first start not below its end. O(n log n) |
| `right_interval_sorted_map.kara` | a `SortedMap` from start to index (the starts are distinct), and for each interval the map's `ceiling` of its end. O(n log n) |
| `right_interval_sweep.kara` | sort the indices once by start and once by end, then walk the ends in ascending order with a pointer into the starts that only moves forward. O(n log n) for the sorts, O(n) for the sweep |
| `right_interval_scan.kara` | for each interval, look at every interval and keep the smallest start at or after its end. O(n^2): the plain reference |
| `differential.kara` | the four arms on 1,500 random sets, five properties |

Every arm prints the same 9 lines: the three LeetCode examples, five
edge cases (a point interval that is its own right interval, both ends
of the range, one long interval over short ones, intervals nested so
none has a right interval, and a chain touching end to start), and for
300 random sets of up to 40 intervals with distinct starts, how many
right intervals there are and a checksum of every answer.
`right_interval.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random sets of 0 to 40 intervals with distinct starts in
[-100, 100), each 0 to 3, 15 or 40 long.

| | property |
|---|---|
| P1 | the answer is the reference's, which reads a table of starts by coordinate upwards from each end |
| P2 | the answer meets the problem's definition: each `j` starts at or after its interval's end, no start lies between, and `-1` only when no start is at or after the end |
| P3 | shuffling the intervals moves the arm's answers with them, and shifting every interval towards an end of the range leaves them alone |
| P4 | one more interval, at a start not yet used, changes one of the arm's answers only to point at it |
| P5 | k intervals touching end to start point each to the next, k point intervals each to itself, k nested ones nowhere, and no intervals give no answers |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | binary search: a start equal to the end does not count | P1 1196, P2 1196, P5 1500 |
| M2 | binary search: the last start in order is the fallback | P1 1339, P2 1339, P5 1500 |
| M3 | sorted map: the ceiling of the end plus one | P1 1196, P2 1196, P5 1500 |
| M4 | sorted map: keyed by end instead of start | P1 1460, P2 1460, P3 522, P5 1500 |
| M5 | sweep: the ends walked in order of start | P1 828, P2 828, P4 424 |
| M6 | sweep: the pointer also passes a start equal to the end | P1 1196, P2 1196, P5 1500 |
| M7 | scan: keeps the largest start, not the smallest | P1 1392, P2 1392, P5 1427 |
| M8 | scan: an interval is never its own right interval | P1 954, P2 954, P5 1500 |

P1 and P2 kill all eight. P3 and P4 compare an arm with itself, so they
only see a mutant whose answer depends on the order of the intervals or
on intervals it should not look at. Keyed by end (M4), two intervals
with the same end overwrite each other in the map in whichever order
they arrive, which P3's shuffle exposes. Walked in order of start (M5),
the sweep's pointer misses starts it already passed, so one more
interval moves answers that should not move, and P4 sees it. M5 is
also the one P5 misses: in its chain and points the ends come in the
same order as the starts, and in its nested set no interval has an
answer. M1, M3 and M6 are the same mistake
in three arms, a start equal to the end not counting, and fail alike.

## Verification

All four arms print the same output as `right_interval.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and all four frozen legacy backends: `karac run --interp`, LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`. `karac check` passes
on every file. The differential prints `30000 checks, 0 failures`
under `karac __mir-run`, `karac __mir-llvm-run` and
`karac run --interp`. The four arms and the differential also run
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

The legacy code generator does not compile the differential: it
refuses `[4, 16, 41][next_random(seed) % 3]`, an index into an array
literal ("Index operator applied to non-array type"), as in kata 435.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. Each of 100 rounds builds 20,000
intervals (the problem's limit) with distinct starts, one in each step
of 100 across [-1000000, 1000000), each up to 32,767 long, shuffles
them, and finds every right interval, folding the answers into a
checksum. Every implementation prints `100 rounds of 20000 intervals:
1983686 right intervals, checksum 137610209`; a 3-round cut of the
Kāra program under `karac __mir-run` prints the same as the C program
cut the same way.

The time is the index sort and the 20,000 binary searches. Kāra's
`sort_by_key` and Rust's are stable sorts, as is Python's; C uses
`qsort` and Go `slices.SortFunc`, which are not, and with distinct
starts give the same order. Spot timings on a shared 4-core container,
three runs each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.35 to 0.37 s |
| Rust (`rustc -O`) | 0.37 to 0.39 s |
| Kāra (legacy `karac build`) | 0.57 to 0.59 s |
| C (`clang -O3`) | 0.58 to 0.61 s |
| Go | 0.67 to 0.71 s |
| Python | 6.9 to 7.1 s |

The two Rust builds are within noise of each other. The Kāra program
prints the same line under `karac __mir-llvm-run` in 2.7 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

## Compiler findings

No new findings. The sorted-map arm reads `ceiling`'s value as `*j`,
as the library types it as a reference. Until kara 1309ed92e0,
`karac check` and `karac __mir-run` both refused `*j`, typing the items
of `floor` and `ceiling` as values (kara `B-2026-10-12-9`, as in kata
391, now closed), and the arm read `j`.
