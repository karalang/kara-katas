# 740. Delete and Earn

Given an integer array `nums`, earn as many points as possible by
repeating this move: pick any `nums[i]`, delete it and earn `nums[i]`
points, then delete every element equal to `nums[i] - 1` and every
element equal to `nums[i] + 1`. Return the most points that can be
earned.

```
nums = [3, 4, 2]           ->  6   (take 4, deleting 3; then 2)
nums = [2, 2, 3, 3, 3, 4]  ->  9   (take the 3s, deleting 2s and 4)
```

**Constraints:** 1 <= `nums.length` <= 2 * 10^4; 1 <= `nums[i]` <= 10^4.

## Approaches

Taking one copy of a value deletes its neighbours, after which nothing
stops the other copies being taken too, so a game is a choice of values,
every copy of each taken, no two of them adjacent. That is the house
robber problem over the values, each worth its value times its count;
the arms differ in how they lay the values out.

| file | mechanism |
|---|---|
| `delete_and_earn.kara` ★ | total the points each value is worth in a table as long as the largest value, then walk it keeping the best total with the last value taken and with it left; O(n + m) for the largest value m |
| `delete_and_earn_sorted.kara` | sort the numbers and walk them a value at a time; a value one more than the last can only follow the last left, any other can follow either; O(n log n) and no table as large as the values |
| `delete_and_earn_totals.kara` | total each value's copies in a `SortedMap` and run the same choice over its entries, looking two entries back for a value whose neighbour is present and one back otherwise |
| `delete_and_earn_runs.kara` | split the values present into runs of consecutive ones, which never interfere, solve each run on its own by the take-or-leave walk, and add up the runs |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: the two LeetCode examples; one
number; four copies of one value; 1 to 10; small and large values
alternating; a list with runs and gaps; the first fifteen digits of π;
20,000 random numbers up to 10,000; every number from 1 to 10,000 once;
20,000 random numbers up to 50; and 300 random lists of 1 to 12 numbers
up to at most 10, with the points in all and a checksum.
`delete_and_earn.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which plays the game itself: from counts by value, it tries every
distinct number present as the next move, taking one copy and deleting
every copy of its two neighbours, and keeps the best total over all
orders of moves. 3,000 random lists are checked, each of 1 to 7 numbers
from 1 to r for a random r from 1 to 9, so that repeats and neighbours
are common; the best games earn 27,235 points in all.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the numbers in reverse order give the same answer |
| P3 | every number made one larger raises the answer by at least 0 and at most the count of numbers, since the same choice of values is still open and each copy is worth one more |
| P4 | a second list of 1 to 4 numbers from 12 to 14, apart from the first by a gap of two at least, played together with it earns the sum of the two answers |

It prints `3000 cases (27235 points in all), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one copy of each value counted | P1 1915 |
| M2 | ★: a value taken after its neighbour | P1 1729 |
| M3 | ★: the largest value never reached | P1 2692, P4 2692 |
| M4 | sorted: neighbours never recognised | P1 1729 |
| M5 | sorted: one copy of each value counted | P1 1915 |
| M6 | sorted: a gap treated as neighbours | P1 889, P4 1596 |
| M7 | totals: one copy of each value counted | P1 1915 |
| M8 | totals: a neighbour's best taken as if apart | P1 1729 |
| M9 | totals: neighbours looked for two apart | P1 1929 |
| M10 | runs: a value taken after its neighbour | P1 1729 |
| M11 | runs: a run starting at the largest value missed | P1 1593, P4 1593 |
| M12 | runs: the first value of each run left out | P1 2337 |
| E1 | ★: a table one value longer | 0 |
| E2 | sorted: the walk starting from a last value of -1 | 0 |
| E3 | runs: the walk going one value past the largest | 0 |

P1 kills all twelve. Several are one mistake in more than one arm and
fail the same checks: M1, M5 and M7 count one copy of each value and
fail the same 1915; M2, M4, M8 and M10 let a value be taken after its
neighbour and fail the same 1729. P4 sees the edits whose answer depends
on where the values sit: M3 misses the largest value and M11 misses it
when it starts a run, and in the joined list that value is one from the
second list, and M6 treats a gap as neighbours, which the gap of two
between the lists exposes. P2 and P3 see none: every arm totals or sorts
the numbers first, so their order never matters, and none of the edits
moves an answer outside P3's bounds. E1 makes the table of totals one
value longer, with a zero the walk never reaches; E2 starts the sorted
walk from a last value of -1 instead of -10, and the first value, at
least 1, is no neighbour of either; E3 lets the run walk step one value
past the largest, where the table holds a zero.

## Verification

Every arm prints the same output as `delete_and_earn.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`3df39964e7`, whose last compiler change is `56339e6224`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse the ★, totals and runs arms, the
differential and the bench program at type checking, at a `*` over a
vector's `iter()` (`*x` over the numbers), since legacy gives those by
value where v2 gives references. They accept the sorted arm, which
prints the right output under the legacy interpreter, `karac run`,
`karac build` and an auto-par build. Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
20,000 random numbers from 1 to 10,000 once, and in each of 5,000 rounds
changes 20 random numbers to a random value and finds the most points
again. Each call builds its table of 10,000 or so totals afresh as a
growable array, as the ★ arm does. Every implementation prints
`5000 rounds of 20000 numbers: 288505069373 points in all`, the Kāra
program under `karac __mir-run` included (in 3.8 min).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.20 to 0.22 s |
| Rust (`rustc -O`) | 0.16 to 0.20 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.16 to 0.20 s |
| Go | 0.69 to 0.72 s |
| Python | 8.7 to 9.1 s |
| Kāra (`karac build --mir`) | 0.23 to 0.30 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.9 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is about a third behind C at the medians of the
interleaved runs (0.27 s against 0.20) and three fifths behind Rust,
with or without overflow checks (0.17), and well ahead of Go
(0.71). Under valgrind's cachegrind it runs 3.5 billion instructions
against C's 1.9 and Rust's 1.8, and 778 million branches against 164 and
428, almost none of them mispredicted in any of the three. Where the
extra instructions and branches go was not traced. The comparison with C
and Rust waits until after M4.

## Compiler findings

None new.
