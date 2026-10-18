# 739. Daily Temperatures

Given an array of integers `temperatures`, the daily temperatures,
return an array `answer` where `answer[i]` is the number of days after
day `i` to wait for a warmer temperature. If no future day is warmer,
`answer[i]` is 0.

```
[73, 74, 75, 71, 69, 72, 76, 73]  ->  [1, 1, 4, 2, 1, 1, 0, 0]
[30, 40, 50, 60]                  ->  [1, 1, 1, 0]
[30, 60, 90]                      ->  [1, 1, 0]
```

**Constraints:** 1 <= `temperatures.length` <= 10^5; 30 <=
`temperatures[i]` <= 100.

## Approaches

A day's answer is the first later day strictly warmer than it. Looking
ahead from every day is O(n^2); each arm keeps just enough of the days
already seen to find that day at once, one walking from the first day
and three from the last.

| file | mechanism |
|---|---|
| `daily_temperatures.kara` ★ | walk from the first day keeping a stack of the days still waiting, whose temperatures never rise from the bottom up; a day pops and answers every waiting day colder than it, then waits itself; each day is pushed and popped once, O(n) |
| `daily_temperatures_jump.kara` | walk from the last day with no structure but the answer: from the next day, while it is no warmer, jump to the day that answers it, since nothing between the two is warmer; a day with no answer ends the search |
| `daily_temperatures_nearest.kara` | walk from the last day keeping, for each temperature from 30 to 100, the nearest later day that had it; a day's answer is the nearest of those over every warmer temperature, O(71 n) |
| `daily_temperatures_backstack.kara` | walk from the last day keeping a stack of later days, each warmer than every day above it; a day drops the days on top that are no warmer, which it hides from everything before it, and the top that is left is its answer |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: the three LeetCode examples; one
day; four equal days; eight days cooling from 100 to 30; eight days with
equal neighbours and a long wait; 30 and 100 in turn; 100,000 random
days with how many have no warmer day and a checksum of the answers, and
the same for 99,999 days cooling slowly from 99 to 30 before a day of
100, and for 100,000 days rising from 30 to 100 again and again; and
300 random runs of 1 to 12 days over 1 to 6 temperatures with the days
waited in all and a checksum. `daily_temperatures.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which looks at the days after each day in turn for the first warmer one.
3,000 random cases are checked, each of 1 to 40 days with temperatures
from 30 to 30 + r for a random r from 0 to 35, so that many cases have
few temperatures and runs of equal days; they hold 61,450 days, of which
14,908 have no warmer day.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | every temperature doubled less 30, which keeps their order and stays within 30 to 100, gives the same answer |
| P3 | with a day of 100 added at the end, warmer than every other, each day that had no warmer day waits for it, and the rest wait as before |
| P4 | on the first half of the days alone, a day keeps its answer when its warmer day is in that half, and has none otherwise |

It prints `3000 cases (61450 days, 14908 with no warmer day), 4 arms,
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
| M1 | ★: an equal day taken as warmer | P1 2441 |
| M2 | ★: one waiting day answered a day at most | P1 2563, P3 2890 |
| M3 | ★: the bottom day answered, not the top | P1 2688, P3 2890, P4 1871 |
| M4 | jump: an equal day taken as warmer | P1 2441 |
| M5 | jump: the search starting a day late | P1 2786, P3 3000 |
| M6 | jump: a jump going one day past the answer | P1 2515, P3 2699 |
| M7 | nearest: an equal temperature counted as warmer | P1 2441 |
| M8 | nearest: the farthest day kept at each temperature | P1 2317, P4 2064 |
| M9 | nearest: 100 never looked at | P2 29, P3 3000 |
| M10 | backstack: equal days kept on the stack | P1 2441 |
| M11 | backstack: a day pushed only onto an empty stack | P1 2445, P3 2786, P4 1681 |
| M12 | backstack: the bottom day taken, not the top | P1 2445, P3 2786, P4 1681 |
| E1 | jump: a day with no answer stepped past, not ending the search | 0 |
| E2 | nearest: a table one temperature longer | 0 |
| E3 | backstack: the top tested again for being warmer | 0 |

P1 kills eleven of the twelve. M9 never looks at 100, which no case
reaches, since the cases' temperatures run from 30 to 65; P3's added day
is 100, so under M9 no day ever waits for it, and P2 sees the 29 cases
whose doubled temperatures reach 100. M1, M4, M7 and M10 are one mistake
in four arms, an equal day taken as warmer, and fail the same
2441 checks, all under P1, because the wrong answer keeps every property
the right one has. M11 and M12 fail the same 6912: a stack that takes a
day only when it is empty holds only its bottom day, so both answer from
the bottom. P3 sees the edits that lose a waiting day or answer from the
wrong one (M2, M3, M5, M6, M11, M12), since the added day then fails to
answer the days that should be left waiting for it, and P4 sees those
whose wrong answers point into the second half
(M3, M8, M11, M12). E1 steps past a day with no answer rather than
ending the search there, but every day after it is no warmer than it, so
the walk finds nothing either; E2 makes the table of nearest days one
temperature longer, and the extra entry is never read; E3 tests the top
of the stack again for being warmer, which it always is once the days no
warmer are dropped.

## Verification

Every arm prints the same output as `daily_temperatures.py` under `karac
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

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at a `*` over a vector's `iter()`
(`*a` over the answers in the harness and the bench, `*w` and `*x` in
the differential), since legacy gives those by value where v2 gives
references. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
100,000 random days from 30 to 100 once, and in each of 300 rounds
changes 100 random days to a random temperature, finds every day's wait
again and adds them up. Each call builds its answer and its stack afresh
as growable arrays, as the ★ arm does. Every implementation prints
`300 rounds of 100000 days: 145697447 days waited in all`, the Kāra
program under `karac __mir-run` included (in 91 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.31 to 0.34 s |
| Rust (`rustc -O`) | 0.33 to 0.40 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.34 to 0.40 s |
| Go | 1.08 to 1.28 s |
| Python | 4.2 to 4.6 s |
| Kāra (`karac build --mir`) | 0.39 to 0.45 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 2.8 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is about a third behind C at the medians of the
interleaved runs (0.42 s against 0.32), a seventh behind Rust (0.37) and
a fifth behind Rust under overflow checks (0.35), and well ahead of Go
(1.16). Under valgrind's cachegrind it runs 1.8 billion instructions
against C's 1.0 and Rust's 1.2, and 478 million branches against 241 and
307, though with 34 million mispredicted against 27 and 28 it loses less
to them than the counts suggest. Where the extra instructions and
branches go was not traced. The comparison with C and Rust waits until
after M4.

## Compiler findings

None new.
