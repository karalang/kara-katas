# 732. My Calendar III

A k-booking happens when k bookings share some time. A booking is a
half-open interval [start, end), start < end. `MyCalendarThree()` makes
an empty calendar, and `book(start, end)` adds the booking and returns
the largest k for which the calendar now holds a k-booking.

```
book(10, 20) -> 1
book(50, 60) -> 1
book(10, 40) -> 2    (10 to 20)
book(5, 15)  -> 3    (10 to 15)
book(5, 10)  -> 3
book(25, 55) -> 3
```

**Constraints:** 0 <= `start` < `end` <= 10^9; at most 400 calls to
`book`.

## Approaches

The most bookings at once is found by sweeping the boundaries in order,
a start adding a booking and an end taking one away, ends first where
the two meet, since a booking is over at its end. The arms differ in
what they keep between bookings.

| file | mechanism |
|---|---|
| `my_calendar_iii.kara` ★ | every start and every end in two sorted lists, each new one put in its place by binary search, and the two lists walked together as the sweep; O(n) per booking |
| `my_calendar_iii_sweep.kara` | a `SortedMap` counting, at each boundary, the bookings starting there less those ending there, summed in order; O(n) per booking |
| `my_calendar_iii_segtree.kara` | a segment tree over [0, 10^9] of `shared struct` nodes made only where a booking reaches, each holding the bookings that cover all of it and the most over any point in it; each booking is added to its stretch, and the root's most is the answer; O(log 10^9) per booking |
| `my_calendar_iii_pieces.kara` | the booked time as a sorted list of disjoint pieces, each with how many bookings hold it, rebuilt for each booking with the parts of pieces it meets held once more and the gaps it fills held once; the deepest piece so far is the answer; O(n) per booking |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: the LeetCode example; four more
short runs, with one stretch booked three times, bookings that touch, a
booking of the whole range and repeats; 1,000 random bookings of up to
10^6 over 0 to 10^9, more than the problem's 400 calls; 1,000 bookings
each overlapping the next two, rising and falling; 1,000 bookings nested
around one point, all of which share it; and 300 random runs of up to
20 bookings with the largest answer and a checksum. `my_calendar_iii.py`
mirrors the sweep arm, the classic solution, and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition, a
row of 1,200 minutes, each with how many bookings hold it, in which
every booking holds its minutes once more and the answer is the most any
minute is held. 3,000 random runs are checked, each of 1 to 20 bookings
of 1 to 15 minutes starting from 0 to 79, so most answers are from 1 to
5; the last answers of the runs sum to 9,610.

| | property |
|---|---|
| P1 | the answers are the definition's |
| P2 | after each booking, the answer is the most bookings so far that hold the start of one of them |
| P3 | every booking 1,000 later gives the same answers |
| P4 | the bookings in reverse give the same last answer |

It prints `3000 runs (last answers summing to 9610), 4 arms,
48000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a booking ending where another starts counted with it | P1 979, P2 979 |
| M2 | ★: an end put last instead of in its place | P1 2661, P2 2661, P4 2530 |
| M3 | ★: an end never taking a booking away | P1 2813, P2 2813 |
| M4 | sweep: a booking's end put a minute late | P1 979, P2 979 |
| M5 | sweep: a boundary's earlier count forgotten | P1 1871, P2 1871, P4 1327 |
| M6 | sweep: the first boundary left out of the sweep | P1 3000, P2 3000 |
| M7 | segtree: a covered node's most never raised | P1 3000, P2 3000, P3 1366, P4 1372 |
| M8 | segtree: a node's most without its own bookings | P1 1811, P2 1811, P3 1511, P4 1148 |
| M9 | segtree: a node's most taken from its left child alone | P1 2993, P2 2993, P3 395 |
| M10 | pieces: a piece's part before the booking put back at one | P1 11, P2 11, P4 18 |
| M11 | pieces: a piece's part after the booking put back at one | P1 16, P2 16, P4 28 |
| M12 | pieces: the answer only this booking's deepest piece | P1 2300, P2 2300, P4 1630 |
| E1 | ★: a new start or end put before its equals | 0 |
| E2 | sweep: the most raised only at a start | 0 |
| E3 | pieces: the last gap tested as at != end | 0 |

P1 and P2 kill all twelve, P4 seven of them, and P3 only the three
segtree edits. P4 misses M1, M3, M4, M6 and M9, whose wrong answers
depend only on which bookings there are and not on their order, so the
last answer comes out the same in reverse. Moving every booking
1,000 later moves it across the segment tree's fixed halving points, so
the segtree's mistakes, M7 to M9, land on different bookings and P3 sees
them. M1 and M4 are one mistake in two arms, bookings that only touch
counted together, and fail as many runs under every property. M10 and
M11 fail few runs, 11 and 16 under P1, and more under P4, 18 and 28: a
piece's part outside the booking put back too shallow shows only when
later bookings make that part the deepest. E1 puts a new start or end
before its equals rather than after, which leaves the sorted list the
same, E2 raises the sweep's most only at a start, the only place the
running sum rises, and E3 tests the last gap as at != end, since at
never passes end.

## Verification

Every arm prints the same output as `my_calendar_iii.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`969445f00a`, whose last compiler change is `b830c8f243`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms and the differential at
type checking, at a `*` that v2 needs and legacy does not: over a
vector's `iter()` (`*k` over the answers in the harness, `*p` over the
pieces) and on the value `SortedMap.get` finds (`*v` in the sweep arm),
since legacy gives those by value where v2 gives references. They accept
the bench program, which prints the same line under the legacy `karac
build` in 1.11 to 1.17 s over three runs (below). Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, which keeps to
arrays and binary search where C and Go have no ordered map. It makes
20 lists of 1,000 random bookings of up to 10^6 once, and in each of
40 rounds books every list into a fresh calendar, every booking moved
later by the round number, summing every answer. Every implementation
prints `40 rounds of 20 lists of 1000 bookings: answers sum
3103040`, the Kāra program under `karac __mir-run` included (in
3.6 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.92 to 0.99 s |
| Rust (`rustc -O`) | 0.69 to 0.86 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.45 to 1.73 s |
| Go | 1.17 to 1.27 s |
| Python | 33.4 to 33.8 s |
| Kāra (`karac build --mir`) | 1.24 to 1.44 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
4.7 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is 1.4 times C and 1.8 times Rust at the medians of the
interleaved runs (1.30 s against 0.94 and 0.74), level with Go
(1.24), and ahead of Rust under overflow checks (1.55), which checks
each step of the sweep's count. Under valgrind's cachegrind it runs
14.7 billion instructions against C's 6.9 and Rust's 8.5, and
4.1 billion branches against 1.7 and 2.5, with 172 to 227 million
mispredicted in the three, most likely the sweep's choice between the
next start and the next end. The legacy build of the same program runs
in 1.11 to 1.17 s, a sixth ahead of v2 and well within M2's limit of
twice legacy; new katas' benches are outside M2's frozen set in any
case. Where the extra instructions go was not traced. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new.
