# 729. My Calendar I

Implement a calendar that takes a booking only when it does not double
book. A booking is a half-open interval [start, end), start < end, and a
double booking happens when two bookings share some time. `MyCalendar()`
makes an empty calendar, and `book(start, end)` adds the booking and
returns true if it overlaps none already in the calendar, and otherwise
leaves the calendar as it was and returns false.

```
book(10, 20) -> true
book(15, 25) -> false   (15 to 20 is taken)
book(20, 30) -> true    (it starts as the first ends)
```

**Constraints:** 0 <= `start` < `end` <= 10^9; at most 1000 calls to
`book`.

## Approaches

Two bookings [s1, e1) and [s2, e2) overlap exactly when s1 < e2 and s2 <
e1. The bookings a calendar holds never overlap, so sorted by start they
are sorted by end too, and a new booking need only be checked against
its neighbours in that order.

| file | mechanism |
|---|---|
| `my_calendar_i.kara` ★ | every accepted booking in a list, each checked against the new one in turn; O(n) per booking |
| `my_calendar_i_sorted.kara` | the starts and ends in two sorted lists; a binary search finds where the new booking would go, and it fits if the booking before ends by its start and the one after starts no earlier than its end; O(log n) to check, O(n) to insert |
| `my_calendar_i_ordered.kara` | a `SortedMap` from start to end, whose `floor` and `ceiling` give the bookings either side of the new start; O(log n) per booking |
| `my_calendar_i_tree.kara` | an unbalanced search tree of `shared struct` nodes, walked left when the booking ends by a node's start and right when it starts at or after its end, refused otherwise, and hung as a new leaf where the walk falls off; O(depth) per booking |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: the LeetCode example; four more
short runs, with bookings that touch, a booking of the whole range and
repeats; 1,000 random bookings of up to 10^6 over 0 to 10^9, the
problem's most calls; 1,000 bookings end to end, rising and falling;
1,000 bookings nested around one point, of which only the first fits;
and 300 random runs of up to 20 bookings with how many were accepted and
a checksum. `my_calendar_i.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition, a
row of 1,200 minutes in which a booking is accepted when every minute it
covers is free, and then takes them. 3,000 random runs are checked, each
of 1 to 20 bookings of 1 to 15 minutes starting from 0 to 99, so
clashes, touching ends and free slots are all common; 14,221 bookings
are refused.

| | property |
|---|---|
| P1 | the answers are the definition's |
| P2 | the accepted bookings never overlap, and each refused one overlaps one accepted before it |
| P3 | every booking 1,000 later gives the same answers |
| P4 | the accepted bookings alone, last first, are all accepted |

It prints `3000 runs (14221 bookings refused), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: bookings that only touch taken as clashing | P1 560, P2 560, P4 570 |
| M2 | ★: each booking kept as empty | P1 2212, P2 2212, P4 2104 |
| M3 | ★: a clash seen only when the new start falls inside | P1 2234, P2 2234, P4 2154 |
| M4 | sorted: a booking ending at the new start taken as clashing | P1 560, P2 560, P4 570 |
| M5 | sorted: the next booking compared with the new start, not its end | P1 2234, P2 2234, P4 2152 |
| M6 | sorted: each end added at the back, not beside its start | P1 1999, P2 1999, P4 1937 |
| M7 | ordered: a one-minute overlap with the booking before let through | P1 573, P2 573, P4 573 |
| M8 | ordered: only a booking's first minute recorded | P1 2100, P2 2100, P4 2100 |
| M9 | ordered: a one-minute overlap with the booking after let through | P1 603, P2 603, P4 603 |
| M10 | tree: a booking ending at a node's start not sent left | P1 594, P2 594, P4 539 |
| M11 | tree: the walk left looking in the right subtree | P1 1958, P2 1958, P4 1543 |
| M12 | tree: the first booking never stored | P1 2521, P2 2521 |
| E1 | ★: the overlap test's two halves swapped | 0 |
| E2 | ordered: the booking after found from start + 1 | 0 |
| E3 | sorted: the midpoint as lo + (hi - lo) / 2 | 0 |

P1 and P2 kill all twelve, P4 all but M12, and P3 none. M12 never stores
the first booking, so the tree stays empty and every booking is
accepted; P4 only asks that bookings already accepted are accepted
again, which an arm that accepts everything does. No edit makes an arm
depend on where the bookings fall, so P3 sees none; it is there to show
that none of them does. M1 and M4 are one mistake in two arms, bookings
that only touch taken as clashing, and fail as many runs under every
property; M3 and M5 both let a booking through when only its end
overlaps, and fail 2,234 runs each under P1. E1 swaps the two halves of
the ★ arm's overlap test, E2 looks for the booking after from start +
1, since a booking at start itself is already found before it, and
E3 writes the sorted arm's midpoint as lo + (hi - lo) / 2.

## Verification

Every arm prints the same output as `my_calendar_i.py` under `karac
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
type checking, at a `*` over a vector's `iter()` (`*r` over the answers
in the harness), since legacy gives those by value where v2 gives
references. They accept the bench program, which prints the same line
under the legacy `karac build` in 0.88 to 0.97 s over three runs. Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
20 lists of 1,000 random bookings of up to 10^6 once, and in each of
80 rounds books every list into a fresh calendar, every booking moved
later by the round number, counting the bookings accepted. Every
implementation prints `80 rounds of 20 lists of 1000 bookings:
1054880 accepted`, the Kāra program under `karac __mir-run` included (in
8.6 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.75 to 0.88 s |
| Rust (`rustc -O`) | 0.75 to 0.85 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.66 to 0.79 s |
| Go | 1.00 to 1.10 s |
| Python | 9.9 s |
| Kāra (`karac build --mir`) | 0.90 to 1.00 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
4.2 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is about a tenth behind C and a sixth behind Rust at the
medians of the interleaved runs (0.94 s against 0.86 and 0.81), ahead of
Go (1.08), and a third behind Rust under overflow checks (0.69), which
here runs faster than plain Rust; why was not traced. The legacy build
of the same program is level with it. Under valgrind's cachegrind it
runs 5.2 billion instructions against 2.8 for both C and Rust, and
1.4 billion branches against 1.2, with 136 million of them mispredicted
in all three, the overlap test on random bookings. Those mispredictions
likely dominate all three times, which would be why nearly twice the
instructions cost only a tenth more; that was not traced. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new.
