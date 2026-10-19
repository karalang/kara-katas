# 790. Domino and Tromino Tiling

Count the ways to tile a 2 × `n` board with 2 × 1 dominoes and L-shaped
trominoes of three squares, each piece turned any way. Two tilings
differ when some two squares that share an edge are covered by one piece
in one tiling and by two in the other. Return the count modulo
1,000,000,007.

```
n = 3  ->  5
n = 1  ->  1
```

**Constraints:** `n` is from 1 to 1,000.

## Approaches

| file | mechanism |
|---|---|
| `num_tilings.kara` ★ | two tables: the tilings of the first `i` columns, and of the first `i` columns with one more square of column `i + 1` covered, a ragged end, as many for the top square as for the bottom; a full board ends with a vertical domino, two horizontal dominoes, or a tromino finishing a ragged end of either side, and a ragged end grows by a horizontal domino on its open side or starts with a tromino on a full board; O(n) |
| `num_tilings_recurrence.kara` | the ragged ends taken out of the ★ arm's two counts leave `f(n) = 2 f(n - 1) + f(n - 3)`, three numbers carried along; O(n) |
| `num_tilings_matrix.kara` | the same recurrence as a 3 × 3 matrix moving `(f(i), f(i - 1), f(i - 2))` one step on, raised to the power `n - 2` by repeated squaring; O(log n) |
| `num_tilings_profile.kara` | column by column, counting the ways to reach each of the four ways a column can already be partly covered by pieces from the one before, each column filled from the top by search over the pieces that cover its first open square and perhaps reach into the next; O(n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: LeetCode's two examples; `n` = 2, 4,
5 and 10; 27, the largest `n` whose count is below the modulus, and 28;
100, 999 and 1,000; and 300 random `n` up to 1,000, with the sum of the
answers modulo 1,000,000,007 and a checksum. `num_tilings.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition. On
boards up to 10 columns the definition counts every tiling one by one,
covering the first open square, column by column, with each of the six
piece shapes that has it as its first square and fits. On longer boards
it counts tilings as sequences of blocks, stretches with clean cuts at
both ends and none inside: one vertical domino, two horizontal dominoes,
or, for three columns or more, a chain of trominoes and horizontal
dominoes in one of two mirror forms. Its 600 boards are 300 up to 10
columns, 240 of 11 to 30, and 60 of 31 to 1,000, the last 1,000 itself.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | `f(n) = 2 f(n - 1) + f(n - 3)` from `n` = 4 |
| P3 | up to 30 columns, `f(n) = f(n - 1) + f(n - 2) + 2 (f(0) + ... + f(n - 3))`, by the last block |
| P4 | up to 30 columns, cut after a random column `m`: either the cut is clean, `f(m) f(n - m)` ways, or one block crosses it with `i` of its columns on the left and `j` on the right, `f(m - i) b(i + j) f(n - m - j)` ways, where `b` is the number of blocks of a length |

It prints `600 boards (answers sum to 85377158), 4 arms, 8616 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one tromino form, not two | P1 535, P2 508, P3 475, P4 475 |
| M2 | ★: a ragged end never grown by a domino | P1 508, P2 508, P3 448, P4 448 |
| M3 | ★: no ragged end of one column | P1 535, P3 475, P4 475 |
| M4 | recurrence: f(n - 2) for f(n - 3) | P1 508, P2 508, P3 448, P4 448 |
| M5 | recurrence: started from f(0) = 0 | P1 535, P3 475, P4 470 |
| M6 | recurrence: one step too few | P1 535, P2 39, P3 475, P4 475 |
| M7 | matrix: the step taking f(i - 1) for f(i - 2) | P1 508, P2 508, P3 448, P4 448 |
| M8 | matrix: the result multiplied on even bits | P1 535, P2 475, P3 475, P4 475 |
| M9 | matrix: f(0) left out of the last product | P1 535, P3 475, P4 472 |
| M10 | profile: no horizontal dominoes | P1 566, P2 508, P3 506, P4 506 |
| M11 | profile: no tromino over both squares of the next column | P1 535, P2 508, P3 475, P4 475 |
| M12 | profile: a vertical domino over an already covered square | P1 566, P2 508, P3 506, P4 506 |

P1 kills all twelve. The first M12 took the tromino with both squares of
this column and the top square of the next for the one with the bottom
square, so that one form was counted twice and its mirror image not at
all; by that mirror symmetry the counts are the same, so it could not be
killed and was replaced by this one. M3, M5 and M9 each give the
recurrence other starting values, M5 and M9 taking `f(0)` as 0, and any
starting values satisfy P2, so P2 misses them. M6 answers `f(n - 1)`
from `n` = 3 on, which also satisfies the recurrence except at `n` = 5,
where P2 fails on the 39 boards with 5 columns.

## Verification

Every arm prints the same output as `num_tilings.py` under `karac
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

The frozen legacy backends accept all four arms and the bench program
unchanged, and refuse the differential at the type check: in `for (dr,
dc) in shape.iter()` they take the items for `i64` rather than
references, so `*dr` is an error. All four arms, and a copy of the
differential with those `*`s removed, print the same output under the
legacy interpreter (`karac run --interp`), the legacy JIT (`karac run`),
`karac build` and an auto-par build; the builds of the matrix arm and
the differential warn that a borrowed `step` is used after a move in
`multiply(step, step)`, since legacy predates borrowed parameters. The
legacy bench timing below is of the bench program as it is. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. Each of 300,000
rounds counts the tilings of a 2 × `n` board for a random `n` from 1 to
1,000, LeetCode's most, so about 150 million table entries are filled.
Every implementation prints `300000 rounds of n up to 1000: answers sum
to 783627304, checksum 281905067`, the Kāra program under `karac
__mir-run` included (in 204 s).

The bench measures two tables grown one entry at a time, with a
remainder per entry. Kāra, Rust and Go grow them by pushing, as the ★
arm does, Python by appending, and C allocates both at their full size
up front. Spot timings on a shared 4-core container, eight runs of each
compiled program, five of them interleaved, and two of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.79 to 1.21 s |
| Rust (`rustc -O`) | 1.18 to 1.70 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.22 to 1.89 s |
| Go | 3.68 to 7.11 s |
| Python | 33.88 to 37.47 s |
| Kāra (`karac build --mir`) | 1.08 to 1.30 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as for the other katas since the redesign; the legacy
`karac build` also builds this one unchanged. Under `karac
__mir-llvm-run` the program prints the same line in 5.8 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.22 s,
against C's 0.82, Rust's 1.28 (1.39 under overflow checks) and Go's
3.75. Under valgrind's cachegrind v2 runs 8.75 billion instructions and
1.35 billion branches, against C's 4.29 billion and 0.16 billion and
Rust's 9.06 billion and 0.92 billion. Where Go's time goes is not
profiled. The legacy build ran 1.15 to 1.60 s, a median of 1.18 s in the
interleaved runs, so v2 takes 1.03 times legacy. The comparison with C
and Rust waits until after M4.

## Compiler findings

Nothing new.
