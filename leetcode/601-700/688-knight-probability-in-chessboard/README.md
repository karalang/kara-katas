# 688. Knight Probability in Chessboard

A knight stands on square (`row`, `column`) of an `n` x `n` chessboard,
rows and columns numbered from 0, and tries to make exactly `k` moves.
Each move is one of its eight moves chosen uniformly at random, even one
that leaves the board; once off the board it stops. Return the
probability that it is still on the board when it stops.

```
n = 3, k = 2, row = 0, column = 0  ->  0.06250
n = 1, k = 0, row = 0, column = 0  ->  1.00000
```

**Constraints:** 1 <= `n` <= 25; 0 <= `k` <= 100; 0 <= `row`, `column`
<= `n` - 1.

## Approaches

Every arm is `fn knight_probability(n: i64, k: i64, row: i64, column:
i64) -> f64`. The arms add up in different orders, so their answers can
differ in the last bits; they print to five places, and the differential
compares to within 10^-12.

| file | mechanism |
|---|---|
| `knight_probability.kara` ★ | the chance of standing on each square, forward from the start: each move sends an eighth of every square's chance to each of its targets, and what is sent off the board is lost; the answer is what is left after k moves; O(k x n^2) |
| `knight_probability_back.kara` | the chance of staying on for s more moves from every square at once, backward: 1 for s = 0, then an eighth of the sum over the targets on the board; the start's entry for s = k; O(k x n^2) |
| `knight_probability_memo.kara` | the same recurrence by recursion from the start, keeping each (moves left, square) answer, so only squares the knight can reach are worked out |
| `knight_probability_count.kara` | the walks that stay on, counted forward as f64, since they reach 8^100, and divided by 8^k, a power of two, at the end |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 15 lines: the two LeetCode examples; nine
corners: a board too small for any move, a 2 x 2 board, the 3 x 3 centre
that no move leaves from, no moves at all, a square all eight moves stay
on, 30 moves from the corner of 8 x 8, and 100 moves on 25 x 25 from its
centre, a corner and an edge; from a corner of 3 x 3, where every square
but the centre has exactly two moves on the board, the chance times 4^k,
which is 1 for every k, down to a chance of 1 / 4^100; every start on
every board of 1 to 8 squares a side for 0 to 6 moves, 1,428 queries,
with how many are certain to fall off and to stay, and their sum; every
start on 12 x 12 for 20 moves, with the lowest, highest and sum; and
200 random queries up to 25 x 25 and 50 moves, summed. Chances print to
five places. `knight_probability.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: read each of the 8^k
move sequences as the k digits of a number in base 8, walk it from the
start, and take the share of sequences that never leave the board.
900 random queries are checked, two thirds on boards of 1 to 8 squares a
side with 0 to 4 moves and a third of 1 to 12 with 0 to 10; the
600 small ones go against the definition.

| | property |
|---|---|
| P1 | the answer is the definition's (up to 8 x 8 and 4 moves) |
| P2 | the start moved by one of the board's other seven symmetries answers the same |
| P3 | k + 1 moves answer the average, over the eight first moves, of k moves from where each lands, 0 off the board |
| P4 | a move more never raises the answer, and a board one square larger each way, the start where it was, never lowers it |

It prints `900 queries (600 against the definition), 4 arms,
13200 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last column taken as off the board | P1 277, P2 350, P3 249 |
| M2 | ★: one jump, (2, -1), made (2, 1) again | P1 239, P2 433, P3 365 |
| M3 | back: one move too few | P1 370, P3 134 |
| M4 | back: the top row taken as off the board | P1 278, P2 350, P3 256 |
| M5 | memo: an answer kept per square, not per square and moves left | P1 89, P2 153, P3 340, P4 185 |
| M6 | memo: the sum kept, not the average | P1 175, P2 198, P3 473, P4 444 |
| M7 | count: divided by 8^(k + 1) | P1 475 |
| M8 | count: a square with a single walk never moves on | P1 349, P3 113 |
| E1 | ★: squares with no chance spread too | 0 |
| E2 | back: the start read transposed | 0 |
| E3 | memo: an answer of 0 worked out again | 0 |
| E4 | count: times 1 / 8^k, not divided by 8^k | 0 |

P1 kills all eight. P2 sees the five that break the board's symmetry:
M1, M2 and M4 by their moves or edges, M5 and M6 because what they
return depends on the order the memo fills in. M3, M7 and M8 change
every square alike. P3 sees all but M7, but M3 and M8 only at k =
0: M3 answers the right chance for one move fewer, and M8 answers 0 for
any k of 1 or more, since the start square holds a single walk and never
moves on, and both of those satisfy P3 from k = 1 on. M7 is seen by
P1 alone: it divides every answer by 8, and P2, P3 and P4 only compare
answers with each other, which a common scale keeps. P4 sees M5 and
M6 only. Every other mutant is still a walk with fixed moves on a fixed
board, only with the wrong moves, board, length or scale, and any such
walk loses chance with a move more and keeps it on a larger board;
M5 and M6 are not walks at all. The four survivors change no answer. A
square with no chance spreads none; transposing is a symmetry of both
the board and the knight's moves; working out a 0 again gives 0 again;
and 8^k is a power of two, so multiplying by its reciprocal, which is
exact, rounds as dividing does.

## Verification

Every arm prints the same output as `knight_probability.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`f8fe87fbe5` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy JIT and `karac build` print the same output for the
back and memo arms, and so does the `KARAC_AUTO_PAR=1` build. The legacy
interpreter printed the first eight lines of each and was stopped at the
60-second limit, at 100 moves on 25 x 25. The legacy backends refuse the
★ and count arms, the differential and the bench program at type
checking, at `*p` or `*w`, since legacy gives the items of
`board.iter()` by value where v2 gives references. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It draws 60 queries once, boards of
15 to 25 squares a side and 50 to 100 moves from a random start, then
answers every query in each of 50 rounds, adding the answers up. Every
implementation prints `3000 queries answered, sum 90.959461`, the Kāra
program under `karac __mir-run` included (in 219 s).

Each implementation is the same forward pass over a flat board of
doubles, with a freshly allocated board for each move. Spot timings on a
shared 4-core container, six runs each, three of them interleaved (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.18 to 0.22 s |
| Rust (`rustc -O`) | 0.29 to 0.58 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.70 to 0.87 s |
| Go | 0.85 to 0.94 s |
| Python | 48.3 to 51.9 s |
| Kāra (`karac build --mir`) | 0.97 to 1.24 s |
| Kāra, legacy (`karac build`, a copy) | 0.73 to 0.87 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program at type checking, as above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata that reads `total
+= p;` for `total += *p;` builds under legacy, and its row is above.
Under `karac __mir-llvm-run` the program prints the same line in 4.5 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is about a quarter behind legacy here, a little behind
Go and Rust with overflow checks, and about five times C; why was not
looked into. The gap to legacy is under the M2 bar of 1.5x, so it is
noted, not filed. The comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
