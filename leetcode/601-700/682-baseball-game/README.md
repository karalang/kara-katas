# 682. Baseball Game

Keep score for a game with odd rules, given its operations in order: an
integer records a new score; `"+"` records the sum of the previous two
scores; `"D"` records double the previous score; `"C"` cancels the
previous score, removing it from the record. Return the sum of the
scores on the record at the end.

```
["5", "2", "C", "D", "+"]               ->  30    (5, 10, 15)
["5", "-2", "4", "C", "D", "9", "+", "+"]  ->  27
["1", "C"]                              ->  0
```

**Constraints:** 1 <= `operations.length` <= 1000; each is `"C"`, `"D"`,
`"+"` or an integer from -3 * 10^4 to 3 * 10^4; `"+"` always has two
scores before it and `"C"` and `"D"` one; every score and the answer fit
in 32 bits.

## Approaches

Every arm is `fn cal_points(operations: Vec[String]) -> i64`.

| file | mechanism |
|---|---|
| `baseball_game.kara` ★ | a stack of the scores on the record: push, push a sum or a double, or pop; the answer is the sum of what is left |
| `baseball_game_running.kara` | the same stack with its sum kept up to date, adding each score pushed and taking away each one cancelled, in a `match` on the operation |
| `baseball_game_typed.kara` | the strings read first into an `enum` of operations, then played on a buffer as long as the list with a count of the scores in use |
| `baseball_game_recursive.kara` | the record after k operations built from the record after k - 1 of them, by recursion |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: the three LeetCode examples; seven
corners, among them a chain of `D`, a chain of `+` growing like
Fibonacci, every score cancelled, and the largest scores LeetCode
allows; every list of 1 to 7 operations over `1`, `-2`, `+`, `D` and `C`
that can be played, 23,408 of them, with a checksum of their answers;
and 300 random lists of up to 1,000 operations, with a checksum.
`baseball_game.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms, as a scorekeeper
would play it on paper: every score is written down and never erased,
`C` crosses out the last score not yet crossed out, `+` and `D` read the
last one or two of those, and the answer is the sum of the scores not
crossed out. 600 random lists of 1 to 60 operations that can all be
played are checked against it, half with numbers from -9 to 9 and half
from -30,000 to 30,000.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | a number and then `C` at the end change nothing |
| P3 | a number x and then `D` at the end add 3x |
| P4 | a list that can be played on its own, played after this one, adds its own answer |
| P5 | every number negated negates the answer |

It prints `600 lists, 4 arms, 12000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `+` doubles the top score | P1 474 |
| M2 | ★: `C` cancels the oldest score | P1 511, P2 586, P4 374 |
| M3 | running: `C` leaves the total as it was | P1 530, P2 589 |
| M4 | running: `D` doubles the first score | P1 487, P3 585, P4 342 |
| M5 | typed: `+` read as `D` | P1 474 |
| M6 | typed: `C` does nothing | P1 532, P2 589 |
| M7 | recursive: the last operation left out | P1 584, P2 584, P3 595, P4 584 |
| M8 | recursive: `+` takes the difference | P1 481 |
| E1 | ★: `D` as a sum of the top with itself | 0 |
| E2 | running: `C` reads the top, then pops it | 0 |
| E3 | typed: a buffer one longer than the list | 0 |
| E4 | recursive: the base case at k <= 0 | 0 |

P1 kills all eight. P2 sees the four that get `C` wrong, M2, M3, M6, and
M7, which drops the `C` at the end of the list; P3 sees M4, which
doubles the wrong score, and M7; P4 sees M2, M4 and M7, which reach into
the list played first; P5 sees none, since every mutant is still linear
in the numbers. M1, M5 and M8 get `+` wrong, which only P1 sees: none of
P2 to P5 ends a list with `+` or compares against a sum. M1 and M5 fail
exactly the same checks, since both turn `+` into twice the last score.
The four survivors change no answer: a score added to itself is its
double; reading the top and then popping it takes away the same score;
the buffer never fills, as the typed arm's comment says, so one more
slot is never used; and `k` never falls below 0.

## Verification

Every arm prints the same output as `baseball_game.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`cba3787150` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives newer than the last
`runtime/src` change.

The frozen legacy backends refuse the ★ and typed arms and the
differential at type checking, at `*x` over a `Vec`'s `iter()`, whose
items legacy gives by value where v2 gives references. They print the
same output for the running and recursive arms under `karac build`, with
and without `KARAC_AUTO_PAR=1`. The legacy JIT overflows its stack on
both, and the legacy interpreter prints the same output for the running
arm but had printed 11 of the 12 lines of the recursive arm when the
60 s limit stopped it. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 200 lists of
5,000 operations that can all be played once, about seven in ten of them
numbers, then scores every list in each of 30 rounds, in an order that
changes each round, putting each answer into a checksum. Every
implementation prints `6000 games scored, checksum 343835318`, the Kāra
program under `karac __mir-run` included (in 134 s).

Each implementation is the same stack, reading each number with its
language's own parser (`strtoll` in C, `str::parse` in Rust,
`strconv.ParseInt` in Go, `int` in Python). Spot timings on a shared
4-core container, six runs each, three of them interleaved (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.98 to 1.11 s |
| Rust (`rustc -O`) | 0.60 to 0.66 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.63 to 0.72 s |
| Go | 1.05 to 1.19 s |
| Python | 4.3 to 4.4 s |
| Kāra (`karac build --mir`) | 1.54 to 1.76 s |
| Kāra, legacy (`karac build`, a copy) | 1.20 to 1.37 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking, at the same `*x`. That edit is by hand, on top
of the `scripts/new-bench.sh` output. A copy outside the kata with
`total += x` and a `ref Vec[String]` parameter builds under legacy, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 11.2 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is about 1.3x legacy and 2.5x Rust here, and the parse
is most of it. Under callgrind, one round of scoring, a million
operations of which some 700,000 are numbers, costs about 410M
instructions, and the parse and what it calls, the copy into a new
`String`, its `malloc` and `free`, the trim and the `i128` parse, come
to about 380 instructions a number, some two thirds of the round:
B-2026-10-13-34, open. Building the lists takes 0.08 s of the run. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The bench meets
B-2026-10-13-34 (open, filed from kata 539): `i64.parse` on the
v2 compiled backend copies the text into a new heap `String`, trims it
and parses an `i128` on every call.
