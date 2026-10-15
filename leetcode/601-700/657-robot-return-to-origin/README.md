# 657. Robot Return to Origin

A robot starts at (0, 0) and makes a string of moves, each `U`, `D`, `L`
or `R`, one step up, down, left or right. Return whether it ends back at
(0, 0).

```
moves = "UD"  ->  true
moves = "LL"  ->  false
```

**Constraints:** 1 to 20,000 moves, each `U`, `D`, `L` or `R`.

## Approaches

Every arm is `fn judge_circle(moves: String) -> bool`.

| file | mechanism |
|---|---|
| `robot_return_to_origin.kara` ★ | the position, one step per move over `moves.chars()`, and whether it ends at (0, 0); one pass |
| `robot_return_to_origin_counts.kara` | four `chars().filter(...).count()`s: as many ups as downs and lefts as rights; four passes |
| `robot_return_to_origin_table.kara` | a `Map[char, i64]` tally filled through `entry(...).or_insert(0)`, a missing move counting 0; one pass |
| `robot_return_to_origin_split.kara` | the displacement of a run as the sum of its halves', down to single moves, over a `Vec[char]`; O(log n) deep |
| `differential.kara` | the four arms against a definition without coordinates, five properties |

Every arm prints the same 11 lines: the two LeetCode examples; five more
strings (one move; each move once; a square; back along one axis but not
the other; and a long way round), each with its answer; how many of
300 random strings of 1 to 60 moves, half of them opposite pairs
shuffled, come back, with a checksum; and three strings of the problem's
longest, 20,000 moves: opposite pairs shuffled, the same with one move
changed, and moves at random. `robot_return_to_origin.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which uses no coordinates: strike out the first move and the first of
its opposites after it, again and again; the robot is back exactly when
every move is struck out. Each of 1,000 random strings has 0 to
40 moves. Half are opposite pairs dropped in at random places, a quarter
of those with one move then changed, and half are moves at random.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | a rotation of the moves gives the same answer |
| P3 | the moves reversed give the same answer |
| P4 | the moves followed by their undoing, reversed and each turned around, come back |
| P5 | the moves made twice give the same answer |

It prints `1000 strings (20364 moves, 426 back), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a move down counted as up | P1 382, P4 948 |
| M2 | ★: back when the two coordinates are equal | P1 70 |
| M3 | counts: ups and lefts against downs and rights together | P1 70 |
| M4 | counts: the rights counted as ups | P1 351, P4 838 |
| M5 | table: a move only marked as made | P1 485 |
| M6 | table: a move never made counted once | P1 37, P5 37 |
| M7 | split: the move at the middle skipped | P1 392, P2 115, P3 76, P4 857, P5 83 |
| M8 | split: the second half's ups and downs subtracted | P1 300, P2 120, P3 71, P4 607, P5 361 |
| E1 | ★: back when the squared distance is 0 | 0 |
| E2 | counts: the rights taken as what is left over | 0 |
| E3 | table: every move tallied twice | 0 |
| E4 | split: each run split after its first move | 0 |

P1 kills all eight, and M2, M3 and M5 only P1 sees: each still answers
by counts alone, the same for any order of the same moves and the same
for a string made twice, and right on every string undone. P2 and P3 see
only the split mutants, M7 and M8, the only ones whose answer depends on
where a move falls. P4 sees the four that miscount a move,
M1, M4, M7 and M8. P5 sees M7 and M8 as well, and M6, which counts a
move never made as made once: made twice, the moves that were made count
double while the missing one still counts one. The four survivors cannot
change an answer: the squared distance is 0 only at (0, 0); with only
four kinds of move, the rights are what is left over; doubling every
count keeps the counts that are equal equal; and the split is right
wherever it falls.

## Verification

Every arm prints the same output as `robot_return_to_origin.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `abbdbaf131` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends refuse every arm at type checking: the
harness reads `*c` from `steps.iter()` over a `Vec[char]`, which legacy
types by value. The differential builds its strings another way, and
legacy's interpreter and `karac build` both print its line, with an
ownership warning that `count_table` takes `tally` owned. Legacy is
frozen, so the refusal is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes eight strings of
1,000,000 moves once, the even ones opposite pairs shuffled and the odd
ones moves at random; then 100 rounds each ask whether one, picked by
the round, brings the robot back, and put the answer into a checksum.
Every implementation prints `8 strings of 1000000, 100 rounds: 50 back,
checksum 934549421`, the Kāra program under `karac __mir-run` included
(in 158 s).

Each implementation is the same walk over the characters; C's over
bytes, which for these letters are the characters. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine), each including making the strings:

| | time |
|---|---|
| C (`clang -O3`) | 0.80 to 0.85 s |
| Rust (`rustc -O`) | 0.82 to 0.84 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.91 to 0.98 s |
| Go | 0.94 to 0.96 s |
| Python | 8.4 to 8.7 s |
| Kāra (`karac build --mir`) | 1.08 to 1.16 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: it reads `*c` from `steps.iter()` over a `Vec[char]`, which
legacy types by value, and its parameters are still owned rather than
borrowed, so handing `strings[pick]` to `judge_circle` moves an element
out of a `Vec`. That edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata with `c` for `*c`
and a `ref String` parameter builds under legacy and takes 0.90 to
0.97 s. Under `karac __mir-llvm-run` the program prints the same line in
3.7 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build takes about a fifth longer than legacy, inside the
M2 bar, and about 1.35 times Rust's. The comparison with C and Rust
waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
