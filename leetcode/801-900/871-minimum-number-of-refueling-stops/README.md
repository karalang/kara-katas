# 871. Minimum Number of Refueling Stops

A car travels from a starting position to a destination which is
`target` miles east of the starting position. There are gas stations
along the way, given as an array `stations` where `stations[i] =
[position_i, fuel_i]`: the i-th station is `position_i` miles east of the
start and has `fuel_i` liters of gas. The car starts with an infinite
tank that holds `startFuel` liters and uses one liter per mile. When it
reaches a station it may stop and refuel, transferring all the gas from
the station into the car. Return the minimum number of refueling stops
needed to reach the destination, or `-1` if it cannot be reached. A car
that reaches a station, or the destination, with 0 fuel left has still
reached it.

```
target = 1,   startFuel = 1,  stations = []                                  ->  0
target = 100, startFuel = 1,  stations = [[10,100]]                          -> -1
target = 100, startFuel = 10, stations = [[10,60],[20,30],[30,30],[60,40]]   ->  2
```

**Constraints:** `1 <= target, startFuel <= 10^9`, `0 <= stations.length
<= 500`, `1 <= position_i < position_i+1 < target`, `1 <= fuel_i < 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `min_refuel_stops.kara` ★ | a heap of the stations passed: drive as far as the fuel goes, pushing the fuel of every station passed into a max-first `PriorityQueue`; when the target is out of reach, the car must have stopped at one more of them, and the best to have stopped at is the one with the most fuel, which the heap gives. -1 when the heap runs dry first. O(n log n) |
| `min_refuel_stops_reach.kara` | the farthest reach for each number of stops: `reach[t]` is the farthest the car gets with t stops among the stations seen so far. A station at p with fuel f turns every t whose reach gets to p into t + 1 stops reaching `reach[t] + f`, t taken from high to low so the station is used once. The answer is the smallest t whose reach gets to the target. O(n^2) |
| `min_refuel_stops_table.kara` | a table over stations and stops: `best[i][k]` is the farthest the car gets with k stops among the first i stations, or -1. Station i is passed by, keeping `best[i][k]`, or is a stop, adding its fuel to `best[i][k - 1]` when that gets to it. O(n^2) time and space |
| `min_refuel_stops_scan.kara` | the richest station in reach, found by a scan: the heap's greedy one stop at a time, scanning every unused station for the one in reach with the most fuel. O(n^2) |
| `min_refuel_stops_sorted.kara` | a sorted list of the stations passed: the heap's greedy with the fuel kept in an ascending `Vec`, each new station inserted where a binary search puts it and the stop taken with `pop`. O(n^2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples and nine
more (no stations, with the start fuel exactly enough and one short; a
station reached with 0 fuel left, and one mile out of reach; nine
stops in a row; a rich station just past what two stops reach; and
LeetCode's extremes, a target of 10^9 with a station at 1 and at 2);
the stops of 3,000 random trips with a target up to 100 and up to 8
stations, 1,952 in all with 855 trips unreachable; and 40 trips with
500 stations, LeetCode's largest, targets up to 10^9, 2,306 stops with 5
unreachable and a checksum. `min_refuel_stops.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of stations to stop at, the car driven station by
station and the trip failing when the fuel goes below 0 before a
station or the target, the fewest stops of the sets that get there. It
checks 1,700 trips: 1,500 with a target up to 60 and up to 9 stations
against the statement, and 200 with targets up to 10^6 and up to 60
stations against the other properties. The ★ arm's answers make 1,339
stops, with 563 trips unreachable.

| | property |
|---|---|
| P1 | the statement's answer (up to nine stations) |
| P2 | more start fuel never needs more stops (-1 counting as more than any number) |
| P3 | one more station, at a position not taken, never needs more stops |
| P4 | a shorter trip, the stations at or past its end dropped, never needs more stops |
| P5 | the answer is 0 exactly when the start fuel reaches the target, and -1 exactly when stopping at every station still falls short |
| P6 | every distance and every amount of fuel tripled gives the same answer |

It prints `1700 cases, stops sum to 1339, 563 unreachable, 50000 checks
over 5 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a station exactly in reach left out | P1 73, P5 57 |
| M2 | ★: the station with the least fuel taken | P1 389, P2 12, P3 59 |
| M3 | ★: a stop not counted | P1 707, P5 735 |
| M4 | reach: stops counted from low to high, so a station can be used twice | P1 11, P5 6 |
| M5 | reach: a station exactly in reach left out | P1 73, P5 57 |
| M6 | reach: the target reached only when passed | P1 101, P4 8, P5 81 |
| M7 | table: a station never passed by | P1 1004, P3 850, P5 338 |
| M8 | table: a first stop never possible | P1 707, P5 735 |
| M9 | table: one unit of start fuel lost | P1 172, P5 138 |
| M10 | scan: the station with the least fuel taken | P1 389, P2 12, P3 59 |
| M11 | scan: a station used again | P1 101, P5 146 |
| M12 | scan: a station exactly in reach left out | P1 73, P5 57 |
| M13 | sorted: the order reversed, so the least fuel is taken | P1 389, P2 12, P3 59 |
| M14 | sorted: every station put first | P1 218, P3 31 |
| M15 | sorted: every other station skipped | P1 157, P3 21, P5 119 |

P1 kills all fifteen. The same fault in different arms fails the same
trips: M1, M5 and M12 (a station exactly in reach), M2, M10 and M13 (the
least fuel taken), and M3 and M8, which both lose exactly one stop's
worth. P6 kills none: every mutation here is wrong at every scale, so an
arm compared with itself on tripled numbers agrees with itself.

## Verification

Every arm prints the same output as `min_refuel_stops.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara
`e903d5b111`. Under `karac __mir-run` the arms take up to 10 s each and
the differential 3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends refuse all five arms, the differential and
the bench program at a `*` on a `for` element, saying the value is not a
reference, where v2 yields a reference. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 100 lists of
500 stations at random positions (repeats dropped) on targets from
5 x 10^8 to 10^9, each list driven 400 times with start fuel from 1 to
about half the target, counting stops, unreachable trips and a
checksum. The heap is a max-first `PriorityQueue` in Kāra, a
`BinaryHeap` in Rust, `container/heap` in Go, `heapq` in Python and an
array heap in C. Every implementation prints `40000 trips over 100 lists
of 500 stations: stops sum to 1258194, 171 unreachable, checksum
582052808`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.24 to 0.25 s | 0.24 s |
| Rust (`rustc -O`) | 0.20 to 0.21 s | 0.20 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.22 to 0.26 s | 0.23 s |
| Go | 1.34 to 1.43 s | 1.39 s |
| Python | 4.7 s | |
| Kāra (`karac build --mir`) | 0.28 to 0.32 s | 0.28 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 870's does. Legacy refuses the bench program
(above), so it has no lane here.

v2 takes 1.2 times Rust's median time under overflow checks and 1.2
times C's. Go's `container/heap` passes every value through an
`interface{}`, and values this large are most likely boxed on the heap
at each push (inferred from the timings, not traced), which would
explain its 1.4 s. Under valgrind's cachegrind C runs 0.95 billion
instructions, Rust with overflow checks 0.99 billion and v2 1.65
billion; under callgrind both v2 and Rust keep the trip loop and the
heap inlined into `main` (95% of v2's instructions, 91% of Rust's), so the
difference is in the heap's own code. The comparison with C and Rust
waits until after M4.
