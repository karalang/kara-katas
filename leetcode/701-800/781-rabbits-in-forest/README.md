# 781. Rabbits in Forest

Some rabbits in a forest were asked how many other rabbits have the
same colour as them, and `answers[i]` is rabbit `i`'s answer. Return
the least number of rabbits the forest can hold.

```
answers = [1, 1, 2]     ->  5
answers = [10, 10, 10]  ->  11
```

**Constraints:** 1 to 1,000 answers, each from 0 to 999.

## Approaches

A rabbit that answers `v` has `v` others of its colour, so its colour
has `v + 1` rabbits in all. Rabbits with different answers have
different colours, and up to `v + 1` rabbits answering `v` can share
one. So `c` rabbits answering `v` need at least `ceil(c / (v + 1))`
colours, each of `v + 1` rabbits, and that many are enough.

| file | mechanism |
|---|---|
| `rabbits_in_forest.kara` ★ | the answers counted in a `Map`, and `ceil(c / (v + 1))` colours of `v + 1` rabbits added for each; O(n) |
| `rabbits_in_forest_sorted.kara` | the answers sorted and walked: a rabbit opens a new colour of `v + 1` unless the colour opened last is for the same answer and has room; O(n log n) |
| `rabbits_in_forest_greedy.kara` | one pass keeping, in a `Map`, how many more rabbits each answer's latest colour can take, a rabbit taking a place or opening a colour; O(n) |
| `rabbits_in_forest_table.kara` | the answers counted in a table of 1,000 slots, the ceiling found as a quotient and whether it leaves a remainder; O(n + 1,000) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: LeetCode's two examples; one
rabbit; three answering 0; three other small forests mixing two answers;
1,000 random answers below 1,000, LeetCode's limits; 1,000 answers of
999 and 1,000 of 0; then 300 random forests of 1 to 50 answers below
up to 10, with the sum of their sizes and a checksum.
`rabbits_in_forest.py` mirrors the ★ arm and its output is
byte-identical.

The ★ and greedy arms walk a `Map`, whose order is random from one run
to the next, but each only adds up what it finds there, so no output
depends on the order.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every way of sharing the rabbits out among colours, a colour holding
only rabbits with its answer `v` and at most `v + 1` of them and adding
`v + 1` to the forest, searched in full for the least forest. Its 1,500
random forests are 1,200 of 1 to 7 answers below up to 4, where that
search is cheap, and 300 of up to 1,000 answers drawn from a few values
or from 950, which leaves room below LeetCode's limit of 1,000 for P3's
second forest.

| | property |
|---|---|
| P1 | the answer is the definition's (small forests) |
| P2 | the answers in another order give the same forest |
| P3 | a second forest of up to 30 answers, all above every answer of the first, adds its own size |
| P4 | `v + 1` more rabbits answering `v`, for an answer `v` already given, add one colour of `v + 1` |

It prints `1500 forests (25801686 rabbits), 4 arms, 22800 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the colours rounded down | P1 669 |
| M2 | ★: a colour for every rabbit | P1 528, P4 826 |
| M3 | ★: only whether an answer occurs counted | P1 744, P4 1500 |
| M4 | sorted: a colour opened with one place too many | P1 724, P4 762 |
| M5 | sorted: the room carried over to another answer | P1 183, P3 760 |
| M6 | sorted: the answers not sorted | P1 265, P2 457 |
| M7 | greedy: a colour opened with one place too few | P1 396, P4 420 |
| M8 | greedy: a place taken when none is left | P1 1158, P4 501 |
| M9 | greedy: a place taken not used up | P1 198, P4 826 |
| M10 | table: a remainder of one rabbit ignored | P1 601 |
| M11 | table: the answer 0 left out | P1 984, P4 674 |
| M12 | table: a colour counted as v rabbits | P1 1200, P4 1500 |

P1 kills all twelve, and M1 and M10 only P1. Both get the rounding of
`c / (v + 1)` wrong, and the other properties keep a count's remainder
as it was: another order and another forest beside it leave every count
alone, and `v + 1` more rabbits answering `v` leave its remainder the
same. P2 sees only M6, the one mutant whose answer depends on the order
of the answers, and P3 only M5, the one that lets a colour's room carry
over from one answer to another. The count of rabbits differs under M1
to M3 because the large forests take their expected answer from the ★
arm. No first choice survived.

## Verification

Every arm prints the same output as `rabbits_in_forest.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`4f079681eb`, whose last compiler change is `ecb1a0322e`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the sorted arm, and it prints the
same output under the legacy interpreter (`karac run --interp`), the
legacy JIT (`karac run`), `karac build` and an auto-par build. Legacy
refuses the other three arms, the differential and the bench program at
its type check: it takes the items of `answers.iter()`, the pairs of
`count.iter()` and the value in `room.get(v)`'s `Some` for `i64` rather
than references, so `*a`, `*v`, `*c` and `*r` are errors, as katas 778
and 780 note for other loops. The bench timing below is of a copy with
those four `*`s taken out and its parameter `ref Vec[i64]`. Legacy is
frozen, so all this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 forests of
1,000 answers, LeetCode's most, are drawn once: a third answer below 10,
a third below 100 and a third below 1,000. Each of 50,000 rounds counts
the next forest. Every implementation prints `50000 rounds of 1000
answers: 5276259024 rabbits, checksum 278403140`, the Kāra program under
`karac __mir-run` included (in 119 s).

Each round is 1,000 updates of a map from answer to count and a walk
over it, so the bench measures the maps more than anything else. Rust's
`HashMap` and Kāra's `Map` both hash with SipHash-1-3 under a random
key, and Go's map has its own keyed hash; C has no map, so its mirror
counts in a hand-written open-addressing table with a multiplicative
hash and linear probing, which is far cheaper than any keyed hash and
makes C's time a floor rather than a match. Spot timings on a shared
4-core container, eight runs of each compiled program, five of them
interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`, hand-written table) | 0.31 to 0.38 s |
| Rust (`rustc -O`) | 1.02 to 1.14 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.99 to 1.19 s |
| Go | 1.35 to 1.83 s |
| Python | 4.21 to 4.35 s |
| Kāra (`karac build --mir`) | 1.59 to 1.76 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 17.4 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.69 s,
against Rust's 1.09 (1.07 under overflow checks), Go's 1.43 and C's
0.33. Under valgrind's cachegrind v2 runs 16.7 billion instructions to
Rust's 9.0 billion, and makes 139 million indirect branches, about
three for each map update, where Rust makes 1.8 million; that is not
profiled further. The legacy build of the copy ran 1.81 to 2.30 s in
five runs interleaved with v2's, a median of 1.82 s against v2's 1.66 s
in the same runs, so v2 takes 0.91 times legacy. The comparison with C
and Rust waits until after M4.

## Compiler findings

Nothing new.
