# 1094. Car Pooling

There is a car with `capacity` empty seats. The vehicle only drives east
(it cannot turn around and drive west).

You are given the integer `capacity` and an array `trips` where
`trips[i] = [numPassengers_i, from_i, to_i]` indicates that the `i`th
trip has `numPassengers_i` passengers and the locations to pick them up
and drop them off are `from_i` and `to_i` respectively. The locations
are given as the number of kilometers due east from the car's initial
location.

Return `true` if it is possible to pick up and drop off all passengers
for all the given trips, or `false` otherwise.

```
trips = [[2,1,5],[3,3,7]], capacity = 4  ->  false
trips = [[2,1,5],[3,3,7]], capacity = 5  ->  true
```

**Constraints:** `1 <= trips.length <= 1000`; `trips[i].length == 3`;
`1 <= numPassengers_i <= 100`; `0 <= from_i < to_i <= 1000`;
`1 <= capacity <= 10^5`.

The arms are `fn car_pooling(trips: Vec[Vec[i64]], capacity: i64) ->
bool`. Passengers whose trip ends at a stop get off before anyone gets
on there, which is what makes `[[2,1,5],[3,5,7]]` fit three seats.

## Approaches

| file | mechanism |
|---|---|
| `car_pooling.kara` ★ | a difference array over the stops, `Vec.filled(1001, 0)`: each trip adds its passengers where they get on and takes them off where they get off, and the passengers aboard are those changes summed from stop 0 on. A drop-off and a pickup at one stop meet in one entry. O(n + 1001) |
| `car_pooling_events.kara` | sorted events: each trip is two `(stop, change)` tuples, built with `flat_map` over a two-element list, and `sort()` on the tuples puts a drop-off (a negative change) before a pickup at the same stop; the passengers aboard are a `scan` over the changes, and `all` must fit. O(n log n) |
| `car_pooling_heap.kara` | the trips by pickup stop (`sort_by_key`), and a `PriorityQueue` of the trips aboard keyed by their drop-off stop: before each pickup, `while let Some(..) = aboard.peek()` lets off every trip that ends by then, and the new trip must fit. O(n log n) |
| `car_pooling_map.kara` | a `SortedMap` from each stop where anyone gets on or off to the change there, updated with `change[k] = change.get(k).unwrap_or(0) + n`, and walked in stop order with a running total. Only the stops that occur are stored. O(n log n) |
| `car_pooling_pickups.kara` | the car is fullest just after some pickup, so only pickup stops are checked: iterator chains, `all` over the trips with a `filter` + `sum` inside counting every trip aboard there. O(n^2) |
| `car_pooling_solution.kara` | LeetCode's Rust template (`impl Solution` over `Vec<Vec<i32>>`, `Vec::with_capacity`, `for t in &trips`, `sort_unstable_by` with `a.0.cmp(&b.0).then(a.1.cmp(&b.1))`, `for &(_, d) in events.iter()`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers to LeetCode's two
examples and ten more (a drop-off and a pickup at one stop, three trips
at 11 seats and at 10, one trip one over and exactly full, a trip over
the whole road, trips at the first and last stops, four overlapping
trips at 6 and 5, three trips sharing their stops), then over 2000
random lists of 1 to 12 trips the smallest capacity each fits, found by
binary search over the arm, and how many fit a capacity drawn from 1 to
40 (`smallest capacities sum to 50510, 851 with enough seats, checksum
87392897`), and the same search over 1000 trips, LeetCode's most
(`smallest capacity 19830, true at it, false one below`).
`car_pooling.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the car drives from stop 0 to stop 1000, and at each stop
everyone whose trip ends there gets off and then everyone whose trip
starts there gets on, the trips aboard kept as a list; the most
passengers it ever carries. It checks 2000 problems in four kinds of
500: 1 to 12 trips of 1 to 10 passengers between stops 0 and 20; a
chain of 1 to 10 trips, each getting on where the last got off; 1 to 40
trips of 1 to 100 passengers over stops 0 to 1000; and 1 to 8 trips
nested inside one another or sharing both stops. The capacity is drawn
from 1 to the passengers of all the trips together. Every random choice
is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer at the capacity drawn is whether the fullest the literal car gets fits it |
| P2 | more seats never hurt: refused one seat below the literal fullest, accepted at it and at 10^5 |
| P3 | the trips in another order (reversed and rotated) give the same answer |
| P4 | every stop moved on by the same amount, and the road then driven backwards (stop s read as 1000 - s), gives the same answer |
| P5 | a trip cut in two at a stop inside it, and another trip's passengers split over two trips with the same stops, give the same answer |
| P6 | every trip's passengers doubled with the capacity gives the same answer; one more trip of a passenger more than the capacity never fits |

All 72,000 checks pass on every arm: `2000 problems: checksum
240385939, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, by a difference array, gives the same checksum.

P1 and P2 both lean on the literal car's fullest load; P3 to P6 compare
the arm only with itself. P4 holds backwards because the order at a
stop turns round with the road: a trip that ended there now starts
there, and a drop-off still comes first.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a full car refused | P1 99, P2 2000 |
| M2 | ★: passengers off a stop early | P1 55, P2 313, P5 4, P6 85 |
| M3 | ★: only one stop's change counted | P1 539, P2 1621, P4 89, P6 40 |
| M4 | events: never sorted | P1 633, P2 1365, P5 23 |
| M5 | events: one fit is enough (`any` for `all`) | P1 1213, P2 1990, P6 2000 |
| M6 | heap: trips by drop-off stop | P1 71, P2 574, P3 8, P4 62, P5 22 |
| M7 | heap: nobody ever gets off | P1 689, P2 1365, P5 96 |
| M8 | heap: the latest drop-off first | P1 332, P2 818, P5 51 |
| M9 | map: a drop-off overwrites its stop | P1 21, P2 204, P3 69, P4 96, P5 39, P6 3 |
| M10 | map: a pickup overwrites its stop | P1 478, P2 1230, P3 328, P4 369, P5 190, P6 10 |
| M11 | map: one passenger over allowed | P1 97, P2 1990, P6 97 |
| M12 | pickups: a trip not aboard at its pickup | P1 604, P2 1990, P4 39, P5 80, P6 897 |
| M13 | pickups: drop-off stops checked | P1 464, P2 1532, P4 92, P5 301, P6 738 |
| M14 | pickups: the first trip's pickup not checked | P1 158, P2 310, P3 60, P4 17, P5 139 |
| M15 | solution: pickups before drop-offs at a stop | P1 108, P2 667, P5 105 |

P1 and P2 catch all fifteen, P5 eleven, P6 eight, P4 seven and P3 four.
The properties that compare an arm only with itself, P3 to P6, catch
fourteen of the fifteen between them; they miss only a full car refused
(M1), which moves every answer the same way. P3 is the weakest because most arms do not depend on the
trips' order at all: it sees the heap's sort key (M6), the two `SortedMap`
overwrites, where which trip writes last matters (M9, M10), and the
pickups arm skipping its first trip (M14). M2 is the hardest for the
properties: getting off a stop early only matters where the stop before
a drop-off is the fullest, and P5 sees it 4 times in 2000, P6 85.

Of the fifteen not kept, eleven fail exactly as a kept edit: M1 is also
the pickups arm and the solution arm refusing a full car; M2 is also
the ★ and solution arms putting passengers on a stop late; M4 is also
the events arm checking each change and not the total and the heap arm
keying a trip by its pickup (each sees one trip at a time); M5 is also
the solution arm sorting by the change alone and counting the changes
the wrong way; M15 is also the events arm dropping off after the
pickups, the heap arm not freeing a drop-off at the pickup stop, and
the pickups arm keeping a trip aboard at its drop-off. The other four
fail in ways of their own but were not needed: the ★ arm adding a
passenger at every stop, the map arm at every pickup, and the events
and map arms counting a drop-off as a pickup.

## Verification

Every arm prints the same output as `car_pooling.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing
on any file, and `karac fix` has nothing to apply.

The kata found no compiler gap. `karac fix` carried every Rust spelling
tried across, each in one or two rounds:

- The events arm first wrote `flat_map(|t| [(t[1], t[0]), (t[2],
  -t[0])])`, a list where Rust takes any `IntoIterator`; Kāra's
  `flat_map` wants an iterator, and the fix adds `.into_iter()`.
- LeetCode's template reaches a clean check in three rounds: the syntax
  (`Vec<..>` to `Vec[..]`, `Vec::with_capacity` to `.`, `for t in
  &trips` to `for t in ref trips`, `cmp(&b.0)` to `cmp(b.0)`, and the
  `&(_, d)` pattern to `(_, d)`), then `struct Solution {}`, then
  `sort_unstable_by` to `sort_by`.
- A heap arm written as Rust writes it, `BinaryHeap::new()` holding
  `Reverse((off, n))` with `use std::collections::BinaryHeap` and `use
  std::cmp::Reverse`, became a smallest-first `PriorityQueue` of plain
  tuples in four rounds, and gives the same answers.
- `sort_by_key(|(s, d)| (*s, *d))` drops the `*`s, since the key
  closure binds copies of a tuple of `i64`s.

## Benchmarks

The bench builds 64 lists of 1000 trips once, LeetCode's most, each of
up to 100 passengers over stops 0 to 1000. Each of 100 rounds changes
one trip's passengers in every list and finds the smallest capacity the
list fits by binary search over 1 to 10^5 with the ★ arm, 17 calls, so
108,800 calls in all, each filling a fresh table of 1001 stops. Every
implementation prints `100 rounds over 64 lists of 1000 trips: smallest
capacities sum to 124037680, checksum 56779892`. C `calloc`s and frees
the table per call; Kāra's `Vec.filled`, Rust's `vec!`, Go's `make` and
Python's list do the same.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `9a544f7990`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.156 to 0.193 s | 0.165 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.148 to 0.204 s | 0.176 s |
| Kāra (`karac build`) | 0.230 to 0.295 s | 0.241 s |
| Rust (`rustc -O`) | 0.235 to 0.265 s | 0.246 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.238 to 0.355 s | 0.251 s |
| Go | 0.241 to 0.305 s | 0.253 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.239 to 0.365 s | 0.264 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.247 to 0.320 s | 0.265 s |
| Python | 15.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra, Rust and Go sit within the spread of one another, about
1.5x C's time; C reads its trips from one static array, where the
others follow a pointer to each trip's row. Python takes about 62x
Kāra's time.
