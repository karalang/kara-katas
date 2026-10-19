# 782. Transform to Chessboard

`board` is an `n` by `n` grid of 0s and 1s. A move swaps any two rows or
any two columns. Return the fewest moves that turn the board into a
chessboard, one where no two cells side by side hold the same value, or
-1 when no number of moves can.

```
board = [[0,1,1,0],[0,1,1,0],[1,0,0,1],[1,0,0,1]]  ->  2
board = [[0,1],[1,0]]                              ->  0
board = [[1,0],[1,0]]                              ->  -1
```

**Constraints:** `n` is from 2 to 30.

## Approaches

Swaps keep two things about the board: every row stays the same row of
values with its cells reordered alike, and a rectangle's four corners
hold an even number of 1s exactly when they did before. A chessboard has
just two kinds of row, each the other flipped, as many of each as `n`
allows, and its rows half 1s. So a board can be made one exactly when
it has the same, and then the rows and the columns can be put in order
apart: each is a line of two kinds to be made alternate, and every swap
fixes at most two places.

| file | mechanism |
|---|---|
| `transform_to_chessboard.kara` ★ | every rectangle with the top left corner even, the first row and column as near half 1s as `n` allows, then the places where the first column and the first row disagree with `0101...` counted, halved, and for an even `n` the nearer of the two patterns taken; O(n²) |
| `transform_to_chessboard_masks.kara` | each row read as a bit mask, exactly two kinds allowed, each the other flipped, then the line of row kinds and the first row's bits each matched against both alternate lines with the same counts; O(n²) |
| `transform_to_chessboard_swapping.kara` | every row compared with the first row and its flip, then the swaps made: for each alternate line with the right counts, one finger on the next misplaced 0 and another on the next misplaced 1, swapped and counted, the fewer kept; O(n²) |
| `transform_to_chessboard_cycles.kara` | every row compared as above, then the permutation that puts each line in place built, a row already where it belongs staying and the misplaced ones of each kind paired, and its swaps counted as its length less its cycles; O(n²) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: LeetCode's three examples; one cell,
which LeetCode does not ask about; four other small boards, solvable and
not, among them one whose rows are of two right kinds in the wrong
numbers; a 30 by 30 chessboard, LeetCode's largest, with its rows and
columns shuffled, and the same with one cell flipped; a shuffled 29 by
29; then 300 random boards of 1 to 12 a side, a third shuffled
chessboards, a third those with one cell flipped and a third with every
row the first or its flip, with how many are solvable, in how many moves
all told, and a checksum. `transform_to_chessboard.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
breadth first search over every board reached by swapping two rows or
two columns, the boards coded as bits, until a chessboard turns up, or
-1 when none is reached. Its 1,600 random boards are 1,300 of 1 to 4 a
side and 60 of 5, where that search is cheap enough, then 240 of 6 to
30. A quarter are chessboards with their rows and columns shuffled, a
quarter those with one cell flipped, a quarter a random first row with
every other row it or its flip, so that only the counts can be wrong,
and a quarter random cells.

| | property |
|---|---|
| P1 | the answer is the definition's (boards up to 5 a side) |
| P2 | the board transposed gives the same answer |
| P3 | every cell flipped gives the same answer: the flip of a chessboard is a chessboard |
| P4 | after a swap of two rows and one of two columns the board is solvable exactly when it was, in at most two moves more or fewer |

It prints `1600 boards (716 solvable), 4 arms, 24640 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the corner rule not checked | P1 203, P4 117 |
| M2 | ★: the first row's count not checked | P1 70, P2 168 |
| M3 | ★: the wrong pattern taken for an odd n | P1 141, P2 97 |
| M4 | masks: a row's flip taken with its first bit kept | P1 389, P2 94, P4 60 |
| M5 | masks: the counts not checked | P1 348 |
| M6 | masks: the farther pattern kept | P1 152 |
| M7 | swapping: the counts not checked | P1 348 |
| M8 | swapping: the 0s looked for where 0s belong | P1 70, P2 77, P3 123 |
| M9 | swapping: the columns lined up by the rows' kinds | P1 186, P2 325 |
| M10 | cycles: a row one cell off taken for the flip | P1 169, P2 227, P4 129 |
| M11 | cycles: the larger count kept | P1 152 |
| M12 | cycles: a misplaced 1 sent to itself | P1 119, P2 77, P3 197, P4 8 |

P1 kills all twelve, and M5, M6, M7 and M11 only P1. M5 and M7 skip the
count check, so a board whose rows are of the right two kinds in the
wrong numbers gets a number of moves rather than -1; M6 and M11 keep the
farther of the two alternate lines rather than the nearer. Each is
wrong the same way on the board transposed, flipped or moved by a swap,
and the farther line is still within one move of where it was after a
swap, so only the definition sees them. P3 sees only M8 and M12, which
treat 0s and 1s differently. The count of solvable boards differs under
M1 and M2 because the large boards take their expected answer from the ★
arm. No first choice survived.

## Verification

Every arm prints the same output as `transform_to_chessboard.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
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

The frozen legacy backends accept all four arms, and each prints the
same output under the legacy interpreter (`karac run --interp`), the
legacy JIT (`karac run`) and `karac build`, each build with a warning
that a borrowed parameter is used after a move, since legacy predates
borrowed parameters. An auto-par build (`KARAC_AUTO_PAR=1`) prints the
same for three arms, but the cycles arm's answers 0 for every board that
passes its row check, where the right answer is a number of moves or,
when the counts are wrong, -1 (`[[1, 0], [1, 0]] -> 0`, `300 random
boards: 205 solvable in 0 moves`); auto-par is opt-in and frozen since
the v2 redesign. Legacy refuses the differential at its type check,
taking the items of `row.iter()` and `level.iter()` for `i64` rather
than references, as katas 778 to 781 note, and the bench at
`moves_to_chessboard(boards[g])`, as a move out of an index; the bench
timing below is of a copy whose parameter is `ref Vec[Vec[i64]]`. Legacy
is frozen, so all this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 boards of 30
by 30, LeetCode's largest, are built once: each a chessboard with its
rows and columns shuffled, a quarter then with one random cell flipped,
and a quarter with a random first row and every other row it or its
flip, so that only the counts can be wrong. Each of 2,000,000 rounds
answers the next board. Every implementation prints `2000000 rounds of
30 x 30 boards: 1000000 solvable, checksum 421080430`, the Kāra program
under `karac __mir-run` included (in 842 s, with
`KARAC_MIR_MAX_STEPS=400000000000`: it passes the interpreter's default
limit of 40 billion steps).

Each round checks every cell of a 30 by 30 board against three others
for the corner rule, unless a flipped cell stops it early, then walks
the first row and column once. Spot timings on a shared 4-core
container, eight runs of each compiled program, five of them
interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.55 to 0.84 s |
| Rust (`rustc -O`) | 1.36 to 2.04 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.42 to 1.69 s |
| Go | 2.08 to 3.02 s |
| Python | 155.7 to 156.5 s |
| Kāra (`karac build --mir`) | 1.45 to 1.86 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 14.1 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.71 s,
against C's 0.74, Rust's 1.56 (1.48 under overflow checks) and Go's
2.58. Under valgrind's cachegrind v2 runs 22.8 billion instructions and
6.90 billion branches, Rust 21.6 billion and 6.73 billion, and C 8.75
billion and 1.63 billion. C indexes its rows unchecked, while Rust and
v2 check every index of the `Vec` of `Vec`s, which is likely much of
the difference; that is not profiled. The legacy build of the copy ran
1.64 to 1.83 s, a median of 1.68 s in the interleaved runs, so v2 takes
1.02 times legacy. The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new.
