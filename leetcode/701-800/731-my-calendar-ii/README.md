# 731. My Calendar II

Implement a calendar that takes a booking only when it does not triple
book. A booking is a half-open interval [start, end), start < end, and a
triple booking happens when three bookings share some time.
`MyCalendarTwo()` makes an empty calendar, and `book(start, end)` adds
the booking and returns true if no time it covers is already held by two
bookings, and otherwise leaves the calendar as it was and returns false.

```
book(10, 20) -> true
book(50, 60) -> true
book(10, 40) -> true    (10 to 20 is held twice)
book(5, 15)  -> false   (10 to 15 would be held three times)
book(5, 10)  -> true
book(25, 55) -> true    (25 to 40 and 50 to 55 held twice)
```

**Constraints:** 0 <= `start` < `end` <= 10^9; at most 1000 calls to
`book`.

## Approaches

A booking makes a triple booking exactly when it meets time that two
bookings already share, and three bookings share time when the latest of
their starts is before the earliest of their ends.

| file | mechanism |
|---|---|
| `my_calendar_ii.kara` ★ | two lists, every accepted booking and every stretch two of them share; a booking that meets a shared stretch is refused, and otherwise its overlap with each accepted booking becomes a new shared stretch; O(n) per booking in the lists' lengths |
| `my_calendar_ii_counts.kara` | a `SortedMap` counting, at each boundary, the bookings starting there less those ending there; the booking is added and the counts summed up to its end, and it is taken out again if any stretch reaches three, which can only be inside it; boundaries that come to 0 are removed; O(n) per booking |
| `my_calendar_ii_segtree.kara` | a segment tree over [0, 10^9] of `shared struct` nodes made only where a booking reaches, each holding the bookings that cover all of it and the most over any point in it; a booking is refused when the most over its stretch is two; O(log 10^9) per booking |
| `my_calendar_ii_pieces.kara` | the booked time as a sorted list of disjoint pieces held once or twice; a booking that meets a piece held twice is refused, and otherwise the list is rebuilt, the parts of pieces it meets held twice and the gaps it fills once; O(n) per booking |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: the LeetCode example; four more
short runs, with one stretch booked three times, bookings that touch, a
booking of the whole range and repeats; 1,000 random bookings of up to
10^6 over 0 to 10^9, the problem's most calls; 1,000 bookings each
overlapping the next two, rising and falling, of which a third are
refused; 1,000 bookings nested around one point, of which only the first
two fit; and 300 random runs of up to 20 bookings with how many were
accepted and a checksum. `my_calendar_ii.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition, a
row of 1,200 minutes, each with how many bookings hold it, in which a
booking is accepted when no minute it covers is held twice, and then
holds its minutes once more. 3,000 random runs are checked, each of 1 to
20 bookings of 1 to 15 minutes starting from 0 to 79, so triple
bookings, double ones and free time are all common; 7,160 bookings are
refused.

| | property |
|---|---|
| P1 | the answers are the definition's |
| P2 | no accepted booking shares time with two accepted before it, and each refused one does |
| P3 | every booking 1,000 later gives the same answers |
| P4 | the accepted bookings alone, last first, are all accepted |

It prints `3000 runs (7160 bookings refused), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a booking touching a double booking refused | P1 417, P2 417, P4 333 |
| M2 | ★: a double booking recorded to the new booking's end | P1 717, P2 717, P4 684 |
| M3 | ★: a double booking met only if it holds the start | P1 1711, P2 1711, P4 1346 |
| M4 | counts: refused at two bookings | P1 2583, P2 2583 |
| M5 | counts: a refused booking's end left in | P1 1082, P2 1082, P4 1082 |
| M6 | counts: only the start's minute summed | P1 1711, P2 1711, P4 1485 |
| M7 | segtree: the bookings over a whole node left out of a query | P1 1395, P2 1395, P3 1240, P4 1098 |
| M8 | segtree: a covered node's most never raised | P1 1730, P2 1730, P3 1020, P4 1233 |
| M9 | segtree: a node's most without its own bookings | P1 502, P2 502, P3 610, P4 248 |
| M10 | pieces: refused at any piece | P1 2583, P2 2583 |
| M11 | pieces: gaps between pieces never filled | P1 153, P2 153, P4 153 |
| M12 | pieces: a piece's part before the booking made two | P1 733, P2 733, P4 511 |
| E1 | ★: the later start found the other way round | 0 |
| E2 | counts: a boundary that comes to 0 never removed | 0 |
| E3 | segtree: the middle as (lo + hi) / 2 | 0 |

P1 and P2 kill all twelve, P4 all but M4 and M10, and P3 only the three
segtree edits. M4 and M10 refuse a booking that meets one other, the
rule of My Calendar I, so the bookings they accept never overlap at all,
and P4 only asks that accepted bookings are accepted again. Moving every
booking 1,000 later moves it across the segment tree's fixed halving
points, so the segtree's mistakes, M7 to M9, land on different bookings
and P3 sees them; the other arms have nothing fixed on the clock to get
wrong. M4 and M10 are one mistake in two arms and fail as many runs
under every property; M3 and M6 both look only at the new booking's
start, and fail 1,711 runs each under P1. E1 finds the later of two
starts the other way round, E2 keeps boundaries that come to 0, which
add nothing to the running sum, and E3 halves the segtree's stretches at
(lo + hi) / 2, which moves the splits but not the answers.

## Verification

Every arm prints the same output as `my_calendar_ii.py` under `karac
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
vector's `iter()` (`*r` over the answers in the harness, `*p` over the
pieces) and on the value `SortedMap.get` finds (`*v` in the counts arm),
since legacy gives those by value where v2 gives references. They accept
the bench program, which prints the same line under the legacy `karac
build` in 1.06 to 1.19 s over three runs (below). Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
20 lists of 1,000 random bookings of up to 3 * 10^6 once, long enough
that many overlap, and in each of 80 rounds books every list into a
fresh calendar, every booking moved later by the round number, counting
the bookings accepted. Every implementation prints `80 rounds of
20 lists of 1000 bookings: 1087840 accepted`, the Kāra program under
`karac __mir-run` included (in 10.9 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.02 to 1.10 s |
| Rust (`rustc -O`) | 0.92 to 0.97 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.94 to 1.05 s |
| Go | 1.19 to 1.27 s |
| Python | 12.4 to 12.8 s |
| Kāra (`karac build --mir`) | 1.01 to 1.36 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
5.0 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is about a fifth behind C and 1.4 times Rust at the
medians of the interleaved runs (1.30 s against 1.08 and 0.95), a
quarter behind Rust under overflow checks (1.03) and level with Go
(1.26). Under valgrind's cachegrind it runs 7.9 billion instructions
against C's 4.1 and Rust's 5.0, and 2.3 billion branches against 1.5 for
both, with 181 million of them mispredicted in all three, the overlap
tests on random bookings. The legacy build of the same program runs in
1.06 to 1.19 s, a little ahead of v2 and well within M2's limit of twice
legacy; new katas' benches are outside M2's frozen set in any case.
Where the extra instructions go was not traced. The comparison with C
and Rust waits until after M4.

## Compiler findings

None new.
