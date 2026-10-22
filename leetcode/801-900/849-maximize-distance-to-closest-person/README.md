# 849. Maximize Distance to Closest Person

You are given a row of seats, `seats[i] = 1` for a seat someone sits in
and `0` for an empty one, with at least one of each. Alex wants to sit
in an empty seat where the distance to the closest person is as large as
possible. Return that distance.

```
seats = [1,0,0,0,1,0,1]  ->  2   (seat 2)
seats = [1,0,0,0]        ->  3   (the last seat)
seats = [0,1]            ->  1
```

**Constraints:** `2 <= seats.length <= 2 * 10^4`, `seats[i]` is 0 or 1,
at least one seat is empty and at least one is taken.

## Approaches

| file | mechanism |
|---|---|
| `max_dist_to_closest.kara` ★ | one pass, remembering the last person: each person ends a stretch of empty seats; before the first person the best seat is the far end, as far away as the stretch is long; between two people it is the middle, half the gap away, rounded down; after the last person it is the other end. O(n) time, O(1) space |
| `max_dist_to_closest_sides.kara` | the nearest person on each side: `left[i]`, how far the nearest person at or before seat `i` is, from a pass left to right, and `right[i]` from a pass right to left, a side with nobody counting as infinitely far; an empty seat's closest person is the nearer. O(n) time and space |
| `max_dist_to_closest_runs.kara` | runs of empty seats: the row cut into runs between people, each marked with whether it touches an end; a run of `k` seats at an end gives `k`, one between two people `(k + 1) / 2`. O(n) time |
| `max_dist_to_closest_next.kara` | each seat against the next person ahead: `prev` is the last person passed and `next` the first at or after the seat, moved on only when the walk passes it, so it moves forward only. O(n) time |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 18 lines: LeetCode's three examples; nine more
(an empty seat at the front and at the back of two, gaps of one, two and
four seats, the best seat at each end, a full row with both ends empty,
one empty seat among people, and a long front run beaten by nothing);
five rows of LeetCode's most seats, 2 * 10^4: one person at the front,
one in the middle, people at both ends, every other seat taken, and
about one seat in 500 taken; and 600 random rows of up to 31 seats, with
the sum of their answers and a checksum. `max_dist_to_closest.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for every empty seat, the distance to its closest person is
the least `|i - j|` over the taken seats `j`, and the answer is the
largest of those. Its 1,600 cases of 2 to 24 seats come in four kinds of
400: few people, many people, one or two people anywhere, the ends
included, and half and half; each has at least one person and one empty
seat. Their answers sum to 5,612.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the row reversed gives the same answer |
| P3 | a person sitting in one more empty seat never makes the answer larger |
| P4 | an empty seat added in front changes nothing if the first seat is taken, and otherwise gives the larger of the answer and the empty seats in front plus one |
| P5 | the answer lies between 1 and `n - 1` |

It prints `1600 cases, distances sum to 5612, 32000 checks over 4 arms:
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the front stretch halved like a gap | P1 403, P2 791, P4 608, P5 51 |
| M2 | ★: a gap's middle counted one short | P1 276, P4 69, P5 69 |
| M3 | ★: the back stretch one short | P1 388, P2 791, P4 47, P5 47 |
| M4 | sides: the person on the right counted a seat further | P1 890, P2 886, P4 855, P5 60 |
| M5 | sides: a person not resetting the left distance | P1 993, P2 1044, P3 171 |
| M6 | sides: the right pass skipping the last seat | P1 173, P2 310, P4 60, P5 60 |
| M7 | runs: a run at the back taken for a gap | P1 341, P2 693 |
| M8 | runs: a gap's seat rounded down | P1 276, P4 69, P5 69 |
| M9 | runs: the last run left out | P1 388, P2 791, P3 54, P4 91, P5 91 |
| M10 | next: nobody ahead counted as next to the seat | P1 388, P2 791, P3 54, P4 91, P5 91 |
| M11 | next: the person behind counted a seat further | P1 872, P2 886, P5 60 |
| M12 | next: the answer capped at half the row | P1 228, P4 248 |

P1 kills all twelve. M2 and M8 are the same mistake, a gap of an odd
number of seats rounded the wrong way, in two arms, and fail the same
cases; so are M9 and M10, which both lose the run after the last person.
P2 sees every edit that treats the two ends of the row, or the two sides
of a seat, differently, which is all of them but the rounding (M2, M8)
and the cap (M12). P4 sees the edits that get the front run wrong (M1,
M4, M12) and many of the rest, since the added seat makes the front run
the answer more often; P5 those that push an answer out of range in a
small row, down to 0 or past `n - 1`. P3 sees the edits whose answer can
rise when a seat is filled: M5, whose left distances run on through
people, and M9 and M10, where filling the seat after the last person can
bring back a run they lose.

## Verification

Every arm prints the same output as `max_dist_to_closest.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `7fb33738c5`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 0.2 to 0.4 s
and the differential 0.6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run all four arms right: `karac run
--interp`, `karac run`, `karac build` and a `KARAC_AUTO_PAR=1` build all
print the same output, and `karac run --interp` and `karac build` print
the differential's `0 failures`. Legacy refuses the bench program as
moving a row out of an index, which v2's borrowing parameters do not do.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64 rows
once, each of LeetCode's most seats, 2 * 10^4: row `g` takes a seat with
probability 1 in `2 << (g % 8)`, from one in two to one in 256, and has
at least one person and one empty seat. Each of 20,000 rounds asks the
next row. Every implementation prints `20000 rounds of 64 rows:
distances sum to 3649292, checksum 784805880`, the Kāra program under
`karac __mir-run` included, in 67 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.89 to 1.03 s |
| Rust (`rustc -O`) | 0.84 to 0.97 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.80 to 0.91 s |
| Go | 0.91 to 1.16 s |
| Python | 15.0 to 15.6 s |
| Kāra (`karac build --mir`) | 0.77 to 0.85 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 0.83 s, against Rust's
0.89 (0.87 under overflow checks), C's 0.94 and Go's 0.99: 0.95 times
Rust's time under overflow checks, 0.88 times C's and 0.84 times Go's.
Under valgrind's cachegrind v2 runs the fewest instructions, 2.81
billion against C's 4.61 billion and Rust's 4.22 billion, and the fewest
branches, 657 million against 850 and 858 million, but all three
mispredict 53 million, about one for every person in the random rows;
most likely those mispredicts are where the time goes, which would leave
the instruction counts little to add (not traced). Built for
`x86-64-v3`, the target `karac build` uses, C takes 0.73 to 0.84 s and
Rust with overflow checks 0.74 to 0.86 s, against v2's 0.77 to 0.87 s in
the same five interleaved runs. Python takes 15.1 s, about 16 times C's
time. The comparison with C and Rust waits until after M4.
