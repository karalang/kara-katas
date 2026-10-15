# 683. K Empty Slots

`n` bulbs stand in a row, numbered 1 to `n`, all off. On day `i +
1` exactly one bulb comes on, bulb `bulbs[i]`, so `bulbs` is an order of
1 to `n`. Given `k`, return the first day on which two bulbs that are on
have exactly `k` bulbs between them, all of them off; return -1 if there
is no such day.

```
bulbs = [1, 3, 2], k = 1  ->  2    (day 2: 1 and 3 on, 2 off)
bulbs = [1, 2, 3], k = 1  ->  -1
```

**Constraints:** 1 <= `n` <= 2 * 10^4; `bulbs` is an order of 1 to `n`;
0 <= `k` <= 2 * 10^4.

## Approaches

Every arm is `fn k_empty_slots(bulbs: Vec[i64], k: i64) -> i64`.

| file | mechanism |
|---|---|
| `k_empty_slots.kara` ★ | turn the input around into the day each position comes on, and slide a window of k + 2 positions whose inside must all come on later than both ends; a bulb inside that comes on sooner than an end makes the window jump to start at it |
| `k_empty_slots_sorted.kara` | turn the bulbs on day by day, keeping the positions that are on in a `SortedSet`, and stop when a new bulb's nearest neighbour on either side is k + 1 away |
| `k_empty_slots_fenwick.kara` | the same day-by-day walk, with a Fenwick tree counting the bulbs on in each prefix: a pair k + 1 apart is both on with nothing on between when the counts say so |
| `k_empty_slots_deque.kara` | the days by position again, with the earliest day inside each window kept as a sliding minimum in a `VecDeque` |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 13 lines: the two LeetCode examples; nine
corners, among them one bulb, `k` = 0, a pair that closes on the last
day and an order with no day; every order of 1 to 7 bulbs for every `k`
from 0 to n - 1, 40,319 in all, counting those with a day and with a
checksum; and 200 random orders of up to 1,000 bulbs, with a checksum.
`k_empty_slots.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: turn the bulbs on
one day at a time, and after each day look at every bulb that is on for
one k + 1 to its right that is on too, with every bulb between them off.
1,500 random orders are checked: two thirds of up to 12 bulbs, which go
against the definition, and a third of up to 300; half with any `k` and
half with `k` from 0 to 2.

| | property |
|---|---|
| P1 | the answer is the definition's (up to 12 bulbs) |
| P2 | numbering the bulbs from the other end gives the same answer |
| P3 | the days after the answer, put in any other order, change nothing |
| P4 | two bulbs k + 1 apart that come on first make the answer day 2 |

It prints `1500 orders (853 with a day), 4 arms, 18704 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the window jumps only past a bulb sooner than both ends | P1 222, P2 333, P3 7 |
| M2 | ★: a window's day taken as its earlier end | P1 568, P3 325, P4 1278 |
| M3 | sorted: a lower neighbour k + 1 or closer counts | P1 405, P2 777 |
| M4 | sorted: the upper neighbour never looked at | P1 250, P2 799 |
| M5 | fenwick: the bulbs between not counted | P1 265 |
| M6 | fenwick: no pair ending at the last bulb | P1 71, P2 149 |
| M7 | deque: the sliding maximum, not the minimum | P1 100, P2 133, P3 24 |
| M8 | deque: the last window never looked at | P1 158, P2 219, P4 308 |
| E1 | ★: a tie with the best day taken again | 0 |
| E2 | sorted: the lower neighbour searched from position 0 | 0 |
| E3 | fenwick: a tree one longer | 0 |
| E4 | deque: an inside day equal to an end's counted | 0 |

P1 kills all eight. P2 sees six, every mutant that treats the two ends
of the row differently, M5 and M2 aside: M5 ignores the bulbs between a
pair on both sides alike, and M2, which takes a window's earlier end, is
symmetric too. P3 sees M1, M2 and M7, which can answer with a day the
tail of the order then changes. P4 sees M2, which answers day 1 for a
pair that is not complete until day 2, and M8, which never looks at the
last window, where a pair from P4 sometimes sits. M5 is seen by
P1 alone: a pair k + 1 apart with a bulb on between them is never built
by P2 to P4. The four survivors change no answer: two windows never end
on the same day, since only one bulb comes on each day; position 0 holds
no bulb; a longer Fenwick tree only counts positions no bulb reaches;
and no inside day can equal an end's day.

## Verification

Every arm prints the same output as `k_empty_slots.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`042e204d6c` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends print the same output for the ★ arm under the
interpreter, the JIT and `karac build`, with and without
`KARAC_AUTO_PAR=1`, and for the Fenwick arm under the JIT and `karac
build`; the legacy interpreter had printed 11 of the Fenwick arm's
13 lines when the 60 s limit stopped it. They refuse the sorted arm and
the differential at type checking, at `*below` and `*x`, since legacy
gives these items by value where v2 gives references. They accept the
deque arm, then the interpreter fails with "method 'front' not found on
type 'Vec'" and codegen with "Vec/String method 'back' is not yet
supported". Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random orders of
20,000 bulbs, LeetCode's largest, once, then answers every order in each
of 30 rounds with a `k` from 0 to 49 that changes with the round,
putting each answer into a checksum. Every implementation prints
`3000 answers: 0 without a day, checksum 305324849`, the Kāra program
under `karac __mir-run` included (in 41 s).

Each implementation is the same window over a freshly allocated array of
days. Spot timings on a shared 4-core container, six runs each, three of
them interleaved (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.45 to 0.49 s |
| Rust (`rustc -O`) | 0.50 to 0.59 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.51 to 0.59 s |
| Go | 0.65 to 0.68 s |
| Python | 11.8 to 12.5 s |
| Kāra (`karac build --mir`) | 0.54 to 0.59 s |
| Kāra, legacy (`karac build`, a copy) | 0.50 to 0.53 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking: `k_empty_slots(orders[c], k)` moves an element
out of `orders` under legacy, where a bare parameter is owned, but
v2 borrows it. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata whose parameter
is `ref Vec[i64]` builds under legacy, and its row is above. Under
`karac __mir-llvm-run` the program prints the same line in 2.6 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with legacy, Rust and C here, and Go a little
behind. Every compiled row does the same work: building the orders and
then, for each answer, filling a 20,000-element array and walking it
once. The comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The sorted arm
writes `on.range(x + 1, n + 1).iter().next()`, where the spec's
`SortedSet.range` returns an iterator and `.next()` alone would do: on
v2 `range` returns an eager `Vec`, and `.next()` on it is refused. That
is B-2026-10-06-67, open, whose title was corrected from this kata (it
said `range` did not exist at all). Drop the `.iter()` once it is fixed.
The same eager `Vec` makes the arm's `on.range(1, x).last()` copy every
smaller bulb each day, so the harness keeps its random orders to
1,000 bulbs.
