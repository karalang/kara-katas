# 789. Escape The Ghosts

You start at `[0, 0]` on an endless grid and want to reach `target`.
`ghosts[i]` is where ghost `i` starts. Each turn you and every ghost at
the same time move one square up, down, left or right, or stay put. You
escape if you reach the target before any ghost reaches you; meeting a
ghost anywhere, the target included, at the same moment is not an
escape. Return whether you can escape whatever the ghosts do.

```
ghosts = [[1, 0], [0, 3]], target = [0, 1]  ->  true
ghosts = [[1, 0]],         target = [2, 0]  ->  false
ghosts = [[2, 0]],         target = [1, 0]  ->  false
```

**Constraints:** there are 1 to 100 ghosts, more than one may start on
the same square, and every coordinate is from -10,000 to 10,000.

## Approaches

A ghost that can reach the target no later than you can wait there, so
you cannot escape it. A ghost that needs longer cannot catch you on a
shortest way either: catching you at a point after `t` moves would put
it within `t` plus the rest of your way of the target, which is no more
than your own distance. So you escape exactly when every ghost's
Manhattan distance to the target is more than yours.

| file | mechanism |
|---|---|
| `escape_ghosts.kara` ★ | every ghost's distance to the target against yours, stopping at the first that is no farther; O(g) |
| `escape_ghosts_all.kara` | the same test as one `all` over `ghosts.iter()` with a closure; O(g) |
| `escape_ghosts_sorted.kara` | the ghosts' distances collected with `map` and `collect`, sorted, and the least compared with yours; O(g log g) |
| `escape_ghosts_walk.kara` | your walk to the target along x and then y, one step a move, asking at each point whether some ghost could be there by then; O(g d) for a distance `d` to the target |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: LeetCode's three examples; two
ghosts, one nearer the target than you; the target where you stand,
three times: with a ghost on it, with one two moves away, and with five
ghosts on two squares one move away; two boards at the edge of the
constraints; and 300 random boards with up to 10 ghosts within 20 of
you, with how many escapes and a checksum. `escape_ghosts.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
for boards within 6 of you: the fewest moves from the target to every
square of a box around the board, found by breadth-first search, and an
escape when every ghost needs more moves to the target than you. Its
1,600 random boards are 1,200 small ones of up to 6 ghosts, a quarter
random, a quarter with one ghost exactly as far from the target as you,
a quarter with every ghost one move farther, and a quarter with ghosts
sharing squares; then 360 within 200 of you with up to 100 ghosts and 40
within 10,000 with up to 3, where only the properties are checked.

| | property |
|---|---|
| P1 | the answer is the definition's, on the small boards |
| P2 | the board turned a quarter about you, with the ghosts in reverse order, gives the same answer |
| P3 | one ghost fewer never takes away an escape |
| P4 | a ghost added on the target means no escape |

It prints `1600 boards (577 escapes), 4 arms, 23144 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a ghost as far as you let through | P1 208, P4 6 |
| M2 | ★: your distance along x alone | P1 381, P2 336 |
| M3 | ★: the ghosts' distance to you, not to the target | P1 472 |
| M4 | all: any ghost farther, not every one | P1 472, P3 88, P4 1411 |
| M5 | all: a ghost as far as you let through | P1 208, P4 6 |
| M6 | all: the y difference without its sign dropped | P1 363, P2 231 |
| M7 | sorted: the farthest ghost, not the nearest | P1 472, P3 88, P4 1411 |
| M8 | sorted: the last ghost's distance, not the least | P1 313, P2 503, P3 234 |
| M9 | sorted: one move of slack | P1 208, P4 6 |
| M10 | walk: the moves counted from 1 | P1 345 |
| M11 | walk: a ghost caught only when strictly nearer | P1 208, P4 6 |
| M12 | walk: the start never checked | P1 1, P4 6 |

P1 kills all twelve. M1, M5, M9 and M11 each let a ghost exactly as far
from the target as you through, and fail the same checks; P4 sees them
only on the six boards whose target is where you stand, since a ghost on
the target is then as far from it as you, 0. M12 also matters only
there, as on any other board a ghost on your start is caught at the
target, and it fails 7 checks. M2 and M3 change the ★ arm's answer for
the large boards too, which is taken as the expected answer there, so
their escape counts differ.

## Verification

Every arm prints the same output as `escape_ghosts.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms and the differential
unchanged. Each prints the same output under the legacy interpreter
(`karac run --interp`), the legacy JIT (`karac run`), `karac build` and
an auto-par build, each build with a warning that a borrowed `ghosts` is
used after a move, since legacy predates borrowed parameters. Legacy
refuses the bench program's `escape_ghosts(boards[r % 64], target)` as a
move out of an index; a copy with the parameter written `ref
Vec[Vec[i64]]` builds, and the bench timing below is of it. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 boards of 100
ghosts, LeetCode's most, anywhere within 10,000 of you, are made once.
Each of 10,000,000 rounds asks the next board whether you can escape to
a random target within 1,000 of you, and about half the rounds are
escapes, which look at all 100 ghosts. Every implementation prints
`10000000 rounds of 100-ghost boards: 5014832 escapes, checksum
57857667`, the Kāra program under `karac __mir-run` included (in 29
minutes, run with `KARAC_MIR_MAX_STEPS` raised above its default of 40
billion steps).

The bench measures a loop of absolute differences and a comparison over
the ghosts. The ghosts are a `Vec[Vec[i64]]` in Kāra, as LeetCode gives
them, so each ghost is a separate allocation of two numbers, and each
target is a new `Vec` of two; C's ghosts are an array of pairs, Rust's a
`Vec<[i64; 2]>` and Go's a `[][2]int64`, all laid out flat, with the
target a pair on the stack, and Python's are lists. Spot timings on a
shared 4-core container, eight runs of each compiled program, five of
them interleaved, and three of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.94 to 1.30 s |
| Rust (`rustc -O`) | 0.74 to 1.43 s |
| Rust (`rustc -O -C overflow-checks=on`) | 5.25 to 7.39 s |
| Go | 1.09 to 2.21 s |
| Python | 89.94 to 105.90 s |
| Kāra (`karac build --mir`) | 1.66 to 2.00 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 10.7 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.93 s,
against C's 0.94, Rust's 0.77 and Go's 1.53. Rust with overflow checks
takes 5.49 s, seven times plain Rust; why is not profiled. Under
valgrind's cachegrind v2 runs 22.5 billion instructions and 4.98 billion
branches, against C's 12.5 billion and 1.42 billion and Rust's 12.6
billion and 1.44 billion; all three mispredict about 10 million. The
legacy build of the copy ran 1.65 to 1.82 s, a median of 1.78 s in the
interleaved runs, so v2 takes 1.08 times legacy. The comparison with C
and Rust waits until after M4.

## Compiler findings

Nothing new.
