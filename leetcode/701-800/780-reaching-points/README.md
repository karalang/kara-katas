# 780. Reaching Points

A move takes a point `(x, y)` to `(x, x + y)` or to `(x + y, y)`. Given
a start `(sx, sy)` and an end `(tx, ty)`, return whether some sequence
of moves turns the start into the end.

```
sx = 1, sy = 1, tx = 3, ty = 5  ->  true    (1,1) (1,2) (3,2) (3,5)
sx = 1, sy = 1, tx = 2, ty = 2  ->  false
sx = 1, sy = 1, tx = 1, ty = 1  ->  true
```

**Constraints:** all four numbers are from 1 to 1,000,000,000.

## Approaches

A move makes one coordinate larger by the other, so run backwards from
the end there is at most one move to undo: the larger coordinate came
from adding the smaller one. The way back is Euclid's algorithm with
every subtraction kept, and walking it one move at a time can take a
billion steps, so every arm undoes a run of moves on the same coordinate
at once.

| file | mechanism |
|---|---|
| `reaching_points.kara` ★ | the larger coordinate taken modulo the smaller while both are above the start's, then the start reached exactly when one coordinate matches and the other is the start's plus a whole number of the matching one; O(log max(tx, ty)) |
| `reaching_points_recursive.kara` | the last move undone and the question asked again, a whole run of moves at a time, stopping a run at the start's value when the other coordinate already matches; O(log max(tx, ty)) |
| `reaching_points_doubling.kara` | as the ★ arm without a division: each run undone by subtracting the smaller coordinate in doubling multiples, as long division does in binary; O(log² max(tx, ty)) |
| `reaching_points_segments.kara` | the whole way back listed first, as runs in which one coordinate holds still while the other falls by it from a top to a bottom, then the start looked for in them; O(log max(tx, ty)) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: LeetCode's three examples; ends of
1,000,000,000, LeetCode's limit, reached from (1, 1) along one run and
along two; an end below the start, and one whose way back passes below
it; a start reached along a long run, and the same
end one less; an end near 1,000,000,000 walked from (35, 13), and the
same one less; then 400 random pairs, half of them an end walked from
the start and half random, with how many are reachable and a checksum.
`reaching_points.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every point reached from the start by the moves, found by depth first
search over the points no larger than the end. Its 2,000 random pairs
are 1,600 with a start of 1 to 10 in each coordinate and 400 with a
start up to 1,000 and an end after up to 40 moves. A quarter of the ends
are reached by moves, a quarter are such an end with one coordinate
moved by one, a quarter are walked from a start next to this one, and a
quarter are random. The definition answers the small pairs whose end is
at most 80 in each coordinate, 1,390 of them; on the rest the ★ arm's
answer stands in for it, and P2 to P4 still apply.

| | property |
|---|---|
| P1 | the answer is the definition's (small pairs) |
| P2 | both points with their coordinates swapped give the same answer |
| P3 | moves compose: the end reaches a point a few random moves on from it, and so does the start when it reaches the end |
| P4 | all four coordinates multiplied by the same number, from 2 to 1,000, give the same answer, since the moves are linear |

It prints `2000 pairs (570 reachable), 4 arms, 29560 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last run's remainder not checked | P1 59, P2 245, P3 5 |
| M2 | ★: the remainders taken down to the start and past it | P1 389, P3 2000 |
| M3 | ★: the last x run checked against the start's x | P1 142, P2 419, P3 889 |
| M4 | recursive: no stop at the start's x | P1 97, P2 246, P3 468 |
| M5 | recursive: an end below the start in one coordinate let through | P1 43 |
| M6 | recursive: one move too many undone on y | P1 175, P2 100, P3 1083 |
| M7 | doubling: the single last subtraction left out | P1 293, P3 1698 |
| M8 | doubling: the run stopping at the smaller coordinate | P1 173, P2 100, P3 1091 |
| M9 | doubling: the steps tripled | P1 175, P3 1064, P4 37 |
| M10 | segments: the bottom of each run left out | P1 40, P3 25 |
| M11 | segments: the step within a run not checked | P1 132 |
| M12 | segments: the start's coordinates swapped | P1 348, P3 1975 |

P1 kills all twelve, and M5 and M11 only P1. M5 errs only on an end
below the start in one coordinate, which only the random ends give, and
M11 only where the start lies within a run but off its step; on the
pairs the other properties build, the mutants' two answers are wrong
alike. P4 sees only M9, the one mutant that is not linear: halving a
tripled step rounds down, and the rounding does not scale, while every
other mutant goes wrong on the scaled pair exactly when it does on the
pair itself. P2 sees the mutants that treat the two coordinates
differently, M1, M3, M4, M6 and M8 each breaking one of the two
branches. The count of reachable pairs differs under M1 to M3 because
the large pairs take their expected answer from the ★ arm. No first
choice survived.

## Verification

Every arm prints the same output as `reaching_points.py` under `karac
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

The frozen legacy backends accept the ★, recursive and doubling arms.
Under the legacy JIT (`karac run`), `karac build` and an auto-par build
each prints the same output. The legacy interpreter (`karac run
--interp`) prints `400 random pairs: 206 reachable, checksum 678604701`
as the last line, a different set of pairs: in `walk(mut seed, sx, sy,
next_random(mut seed) % 30)` it passes the first argument as `seed` was
before the fourth advanced it, the behaviour katas 771, 775 and 777
note. With that argument computed into a name first, it prints the same
output. Legacy refuses the segments arm and the differential at its type
check: in `for run in runs_back(tx, ty).iter()` it takes the items for
`Run` rather than references, so `*run` is an error, as kata 778 notes
for a `Vec[i64]`. Legacy is frozen, so all this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 1,024 queries
are built once: each start is 1 to 1,000 in each coordinate, and each
end is walked from a start by random moves until a coordinate passes
500,000,000. Half the ends are walked from their own start, a quarter
have their y lowered by one after, and a quarter are walked from the
start with its x one higher. Each of 15,000 rounds answers all of them.
Every implementation prints `15000 rounds of 1024 queries: 7680000
reachable, checksum 324725756`, the Kāra program under `karac __mir-run`
included (in 56 s).

Each query walks Euclid's algorithm back from an end near
500,000,000, about seventeen 64-bit divisions in a chain, each waiting on
the one before, so the bench measures the divider's latency more than
anything the compilers do around it. Spot timings on a shared 4-core
container, eight runs of each compiled program, five of them
interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.24 to 1.43 s |
| Rust (`rustc -O`) | 1.27 to 1.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.32 to 1.45 s |
| Go | 1.33 to 1.39 s |
| Python | 14.1 to 15.3 s |
| Kāra (`karac build --mir`) | 1.31 to 1.37 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as every kata's does since the v2 redesign; that edit
is by hand, on top of the `scripts/new-bench.sh` output. Under `karac
__mir-llvm-run` the program prints the same line in 4.3 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.36 s,
against C's 1.30, Rust's 1.36 (1.35 under overflow checks) and Go's
1.35. Under valgrind's cachegrind v2 runs 5.16 billion instructions,
C 5.87 billion and Rust 6.47 billion, and all three mispredict about 33
million branches. The legacy build of the same program ran 1.40 to
1.53 s, a median of 1.48 s in the interleaved runs, so v2 takes 0.92
times legacy. The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new.
