# 1109. Corporate Flight Bookings

There are `n` flights that are labeled from `1` to `n`.

You are given an array of flight bookings `bookings`, where `bookings[i]
= [first_i, last_i, seats_i]` represents a booking for flights `first_i`
through `last_i` (inclusive) with `seats_i` seats reserved for each
flight in the range.

Return an array `answer` of length `n`, where `answer[i]` is the total
number of seats reserved for flight `i`.

```
bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5   ->  [10,55,45,25,25]
bookings = [[1,2,10],[2,2,15]], n = 2            ->  [10,25]
```

**Constraints:** `1 <= n <= 2 * 10^4`; `1 <= bookings.length <= 2 *
10^4`; `bookings[i].length == 3`; `1 <= first_i <= last_i <= n`; `1 <=
seats_i <= 10^4`.

The arms are `fn corp_flight_bookings(bookings: Vec[Vec[i64]], n: i64)
-> Vec[i64]`. A flight holds at most `2 * 10^4 * 10^4 = 2 * 10^8` seats,
so the Rust solution's `i32` is wide enough.

## Approaches

| file | mechanism |
|---|---|
| `corp_flight_bookings.kara` ★ | a difference array: each booking adds its seats where its range starts and takes them away just past where it ends, and a running total over the flights gives every flight's seats. O(n + m) |
| `corp_flight_bookings_fenwick.kara` | a Fenwick tree over the same changes, a `struct` with methods on `mut ref self`: a booking is two point updates, and each flight's seats are the prefix sum up to it, the index stepping by its lowest set bit with `wrapping_neg`. O((n + m) log n) |
| `corp_flight_bookings_sweep.kara` | a sweep over events: each booking opens at its first flight and closes after its last, the events kept in a `SortedMap` through `entry(..).or_insert(0)`, and the flights walked in order with a `peekable` iterator over the events carrying the open seats. O(m log m + n) |
| `corp_flight_bookings_segment.kara` | a segment tree over the flights, by recursion over a `mut ref Vec[i64]`: a booking adds its seats to the O(log n) nodes that cover its range exactly, and one walk down the tree hands each leaf the sum along its path. O((n + m) log n) |
| `corp_flight_bookings_scan.kara` | iterator chains: the bookings folded into a difference array, then the running total taken with `scan` over a slice of it, as Rust writes a prefix sum |
| `corp_flight_bookings_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `Vec<Vec<i32>>`, a difference array in the answer itself, closed only when `last < n`, then summed in place), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's two
examples and six more (one flight, one booking of every flight, the
last flight and the first, three equal bookings, 10^4 seats with a
flight left empty, four overlapping), then over 2000 random problems of
up to 30 flights and 30 bookings the seats summed and a checksum
(`2000 random problems: 9675829 seats, checksum 204410551`), and two
of LeetCode's largest: 2 * 10^4 random bookings over 2 * 10^4 flights,
and 2 * 10^4 bookings of every flight. `corp_flight_bookings.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each flight, the seats of every booking whose range
holds it. It checks 2000 problems in four kinds of 500: up to 12
flights and 12 bookings at random; one to three flights with up to 10^4
seats; bookings of one flight each over up to 20; and bookings nested
inside one another over up to 30, the first of every flight. Every
random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | by a second reading, the changes: the answer has `n` entries, from one flight to the next it moves by the seats of the bookings that start at the second less those that end at the first, and it holds every booking's seats once for each flight the booking covers |
| P3 | the bookings in another order, reversed and rotated, give the same answer |
| P4 | each booking of two or more flights cut in two at a random flight, and the second part's seats shared between two bookings, give the same answer |
| P5 | the flights numbered from the other end, every booking `[a, b, s]` as `[n + 1 - b, n + 1 - a, s]`, give the answer reversed |
| P6 | every booking twice gives twice the seats, and one more booking of every flight adds its seats to each |

All 72,000 checks pass on every arm: `2000 problems: checksum
965788160, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, adding every booking to every flight it covers,
gives the same checksum.

P1 sums every booking at every flight and P2 judges the answer by its
changes; P3 to P6 compare the arm only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the seats taken away at the last flight, not past it | P1 2000, P2 2000, P4 1216, P5 1216, P6 2000 |
| M2 | ★: the first booking never read | P1 2000, P2 2000, P3 1382, P4 1056, P6 2000 |
| M3 | ★: only half the seats taken away | P1 1485, P2 1485, P4 1216, P5 1608 |
| M4 | fenwick: an update walks every node above | P1 1434, P2 1434, P5 1455, P6 1495 |
| M5 | fenwick: a prefix adds every node below | P1 1680, P2 1680, P5 1724, P6 1732 |
| M6 | sweep: a second booking from the same flight lost | P1 1414, P2 1414, P3 1171, P4 1216, P5 1336, P6 2000 |
| M7 | sweep: the open seats replaced by each change | P1 1578, P2 1578, P4 805, P5 1608, P6 1608 |
| M8 | segment: a range ending at a node's first flight left out | P1 1687, P2 1687, P4 1150, P5 879, P6 268 |
| M9 | segment: the seats above a node forgotten | P1 1185, P2 1185, P4 1108, P5 791, P6 1732 |
| M10 | segment: an update split one flight right | stops: integer overflow |
| M11 | scan: the totals started one flight late | P1 2000, P2 2000, P5 1732, P6 2000 |
| M12 | scan: a booking to the last flight closed before it | P1 1615, P2 1615, P5 1556, P6 2000 |
| M13 | solution: the first flight never carried | P1 1399, P2 1399, P5 1556, P6 1732 |
| M14 | solution: each flight copies the one before | P1 1607, P2 1607, P5 1109 |
| M15 | solution: a booking's start overwrites | P1 1413, P2 1413, P3 1185, P4 1151, P5 1338, P6 2000 |

Of the fourteen that run to the end, P1 and P2 catch all fourteen, P5
thirteen, P6 twelve, P4 eight and P3 three. P1 and P2 fail on the same
problems every time: an answer of `n` entries whose every change from
one flight to the next is the bookings' is the literal one, since the
first flight starts from nothing. P5 is the strongest self-comparison:
mirrored, a booking's start becomes its end, so an edit that treats the
two ends apart fails it; it misses only M2, which loses the first
booking however the flights are numbered. P3 sees only the three edits
that depend on the order of the bookings: losing the first (M2),
keeping the first of two from one flight (M6), and letting a later
start overwrite an earlier (M15). P4 sees the edits that go wrong at a
range's ends, which cutting a booking in two adds. P6 misses M3 and
M14, the two that stay linear: halving every closing, or copying the
first flight's seats to every flight, scales with the bookings doubled
and moves with a booking of every flight. P3 to P6 together catch all
fourteen. M10 stops: split one flight right, a node's halves can be
itself and an empty one, and the recursion doubles the node number past
`i64`.

Of the fifteen not kept, nine fail as a kept edit: the seats added one
flight late in the ★ arm and taken away at the last flight in the
fenwick and sweep arms as M1, each flight given the total before its
own change in the ★ and scan arms, read one short in the fenwick arm
and an event applied one flight late in the sweep arm as M11, and one
seat left after each booking in the solution arm as M3. The other six
fail in ways of their own but were not needed: the fenwick arm reading
a negative node as zero, the sweep arm never answering the last flight,
the segment arm overwriting a node's seats and giving the right half
half the seats, the scan arm one seat too many at each start and its
total started at one, and the solution arm never closing a booking that
ends at the second-last flight.

## Verification

Every arm prints the same output as `corp_flight_bookings.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found no compiler gap. The ★ arm was written as Kāra, and the
other five as Rust writes them; `karac fix` carried every Rust spelling
to a clean check, in three to five rounds each: `Vec<..>` to `Vec[..]`,
`vec![0; n]` to `Vec.filled(n, 0)`, `Vec::with_capacity(..)` and
`Fenwick::new(..)` to `Vec.with_capacity(..)` and `Fenwick.new(..)`,
`&mut self` and `&self` to `mut ref self` and `self`, `mut i: usize` to
`i: own i64` with a `let mut i = i;`, `&mut Vec<i64>` to `mut ref
Vec[i64]` and `&Vec<i64>` to `Vec[i64]`, every `usize` and `as usize`
dropped, `for b in &bookings` to `for b in ref bookings`, `||` and `&&`
to `or` and `and`, `use std::collections::BTreeMap` dropped and
`BTreeMap` to `SortedMap`, `Some((&at, &change))` to `Some((at,
change))`, the scan closure's `*running += d; Some(*running)` to `let
running = running + d; Some((running, running))`, the fold's `|mut
change, b|` to a `let mut change = change;`, and in the Rust solution
`struct Solution {}` declared and `Solution::` to `Solution.`. One hand
edit: the sweep arm's `next.next();`, whose discarded `Option` draws a
warning that deliberately has no machine fix, written `let _ =
next.next();`. Two leftovers read oddly but are what `karac fix`
leaves: the fenwick and segment arms' `let n = n;`, once `let n = n as
usize;`.

## Benchmarks

The bench builds 16 problems once, each of 2 * 10^4 flights and 2 *
10^4 random bookings of up to 10^4 seats, LeetCode's largest. Each of
200 rounds replaces one booking in every problem and solves it with the
★ arm: 3200 calls, each allocating its change array and its answer.
Every implementation prints `200 rounds over 16 problems of 20000
flights: busiest total 151022533405, checksum 175022010`. Each booking
is its own heap array of three in every language: C `malloc`s each.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.343 to 0.370 s | 0.357 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.343 to 0.399 s | 0.362 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.380 to 0.463 s | 0.394 s |
| C (`clang -O3`) | 0.425 to 0.538 s | 0.450 s |
| Go | 0.451 to 0.521 s | 0.506 s |
| Rust (`rustc -O`) | 0.506 to 0.588 s | 0.532 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.533 to 0.605 s | 0.546 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.525 to 0.591 s | 0.553 s |
| Python | 15.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is the fastest by wall time. C and Rust free each call's
arrays and pay for the pages again on the next call, 0.15 to 0.2 s of
system time each, where Kāra's allocator keeps them: by user time C
takes 0.301 s, Rust 0.363 s and Kāra 0.349 s. Go spends 0.734 s of user
time over 0.506 s of wall time, its collector running beside the
program. Python takes about 43x Kāra's time.
