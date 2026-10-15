# 681. Next Closest Time

Given a time `"HH:MM"`, return the next closest time that can be formed
by reusing its digits, each as many times as needed. The given time is
always valid; the answer is the next one going forward, wrapping past
midnight, and is the given time itself when no other works.

```
"19:34"  ->  "19:39"
"23:59"  ->  "22:22"    (the next day)
```

**Constraints:** `time` is `"HH:MM"`, 00 <= HH <= 23, 00 <= MM <= 59.

## Approaches

Every arm is `fn next_closest_time(time: String) -> String`.

| file | mechanism |
|---|---|
| `next_closest_time.kara` ★ | step forward a minute at a time, wrapping at midnight, until every digit of the clock is one of the given digits; at most 1,440 steps |
| `next_closest_time_combos.kara` | all 4^4 = 256 ways to fill the four places from the given digits; of the real times among them, the one the fewest minutes ahead, the given time counting as a whole day |
| `next_closest_time_greedy.kara` | as with the next number from a set of digits: from the last place leftward, raise the first place that can take a larger given digit and still be a time, and set the places after it to the smallest digit; when none can rise, every place takes the smallest digit |
| `next_closest_time_sorted.kara` | every time made of the given digits, in minutes, sorted without repeats, and a binary search for the first one after the given time, wrapping to the first |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 15 lines: the two LeetCode examples; ten
corners, among them a time that is its own answer (`"11:11"`), answers
that wrap to the next day, and a rise in the hour that resets the
minutes (`"20:48"` to `"22:00"`); then, over all 1,440 times of day, how
many answer themselves and how many answer on the next day, the minutes
ahead in all and the farthest answer short of a whole day, and a
checksum. `next_closest_time.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition works on text, apart from the arms' arithmetic: it walks
the day that follows the given time, writing each minute as `"HH:MM"`,
and stops at the first whose characters all appear in the given time. It
is checked on all 1,440 times of day. P3 does not trust the walk: it
draws 20 random fillings of the four places from the given digits for
each time and checks that no real time among them is nearer ahead.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is a real time, and all its digits are the given time's |
| P3 | no time made of the given digits is fewer minutes ahead |
| P4 | a time is its own answer exactly when its four digits are the same |

It prints `1440 times, 4 arms, 66927 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a 0 always allowed | P1 305, P2 305 |
| M2 | ★: only the hour's digits allowed | P1 996, P2 487, P3 1199 |
| M3 | combos: minutes up to 69 taken as times | P1 83, P2 83 |
| M4 | combos: the given time counted as no minutes ahead | P1 1437, P3 11792, P4 1437 |
| M5 | greedy: any second hour digit up to 9 | P1 28, P2 28 |
| M6 | greedy: the places after the raised one left as they were | P1 684, P2 8, P3 658 |
| M7 | sorted: the first time at or after the given one | P1 1437, P3 11886, P4 1437 |
| M8 | sorted: a minute's first digit up to 6 | P1 83, P2 83 |
| E1 | ★: the digit test stops at the first digit not allowed | 0 |
| E2 | combos: the best so far starts beyond a whole day | 0 |
| E3 | greedy: a tie in the next digit taken again | 0 |
| E4 | sorted: repeated times kept | 0 |

P1 kills all eight. P2 sees every mutant but the two that answer the
given time itself, M4 and M7, since that answer is a real time made of
the given digits; P3 and P4 are what see those two, and P4 sees nothing
else. P3 sees M2, M4, M6 and M7, the mutants that return a real time
from the given digits but too far ahead. M1, M3, M5 and M8 return a time
with a digit not given or a time that is not real, which P2 sees and
P3 cannot, since its random fillings never include those answers. The
four survivors change no answer. Stopping the digit test at the first
digit not allowed only skips the rest of a test already failed. In the
combos arm, the given time is always among the fillings and counts as a
whole day ahead, so starting the best at a whole day or one minute more
ends the same. In the greedy arm, a tie is the same digit taken again.
And a repeated time in the sorted list does not move the binary search's
answer.

## Verification

Every arm prints the same output as `next_closest_time.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`cba3787150` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives newer than the last
`runtime/src` change.

The frozen legacy backends print the same output for the ★, combos and
greedy arms under the interpreter, the JIT and `karac build`, with and
without `KARAC_AUTO_PAR=1`. They refuse the sorted arm at type checking,
at `*c` in its `filter` and `map`, since legacy gives the items of a
byte slice's `iter()` by value where v2 gives references, and refuse the
differential for the same reason and an element moved out of a
`Vec[String]` by indexing. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It writes every time of day once, then
answers all 1,440 of them in each of 300 rounds, in an order that
changes each round, 432,000 answers, counting those that fall on the
next day and putting each into a checksum. Every implementation prints
`432000 times: 21000 answers on the next day, checksum 962562307`, the
Kāra program under `karac __mir-run` included (in 72 s).

Each implementation is the same minute-by-minute walk, returning a new
string for each answer. Spot timings on a shared 4-core container, six
runs each, three of them interleaved (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.28 to 0.31 s |
| Rust (`rustc -O`) | 0.21 to 0.24 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.22 to 0.23 s |
| Go | 0.34 to 0.40 s |
| Python | 10.5 to 11.1 s |
| Kāra (`karac build --mir`) | 0.22 to 0.29 s |
| Kāra, legacy (`karac build`, a copy) | 0.21 to 0.23 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking: `next_closest_time(times[at])` moves an
element out of `times` under legacy, where a bare parameter is owned,
but v2 borrows it. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata whose parameter
is `ref String` builds under legacy, and its row is above. Under `karac
__mir-llvm-run` the program prints the same line in 2.8 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build is level with legacy and Rust here, with Go a little
slower. C is slower too, probably because it formats each answer with
`snprintf`, which is general and slow, where the others format two
digits at a time; that is inferred, not profiled. The comparison with C
and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
