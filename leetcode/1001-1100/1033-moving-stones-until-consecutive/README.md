# 1033. Moving Stones Until Consecutive

There are three stones in different positions on the X-axis. You are
given three integers `a`, `b`, and `c`, the positions of the stones.

In one move, you pick up a stone at an endpoint (i.e., either the
lowest or highest position stone), and move it to an unoccupied
position between those endpoints. Formally, let's say the stones are
currently at positions `x`, `y`, and `z` with `x < y < z`. You pick up
the stone at either position `x` or position `z`, and move that stone
to an integer position `k`, with `x < k < z` and `k != y`.

The game ends when you cannot make any more moves (i.e., the stones
are in three consecutive positions).

Return an integer array `answer` of length 2 where `answer[0]` is the
minimum number of moves you can play, and `answer[1]` is the maximum
number of moves you can play.

```
a = 1, b = 2, c = 5  ->  [1,2]
a = 4, b = 3, c = 2  ->  [0,0]
a = 3, b = 5, c = 1  ->  [1,2]
```

**Constraints:** `1 <= a, b, c <= 100`; `a`, `b`, and `c` have
different values.

## Approaches

| file | mechanism |
|---|---|
| `moving_stones.kara` ★ | by the gaps: sort to `x < y < z`. Every move fills at least one free place between the end stones, and stepping an end stone one place in fills exactly one, so the most is `z - x - 2`. The fewest is 0 when the stones touch, 1 when either gap holds at most one free place (fill it, or bring the far stone beside the pair), and 2 otherwise (bring each end stone beside the middle one). O(1) |
| `moving_stones_memo.kara` | recursion over the gaps: only the free places `g1` below the middle stone and `g2` above it matter. A move of the low stone leaves `(j, g2)` for any `j` below `g1`, or jumps the middle stone and leaves `(j, g2 - 1 - j)`; the high stone mirrors both. The fewest and most moves to `(0, 0)` are kept in a `Map` keyed by the gaps. O(g^3) |
| `moving_stones_table.kara` | a table over the gaps: the same moves, filled bottom-up in order of `g1 + g2`, which every move lowers. O(g^3) |
| `moving_stones_bfs.kara` | breadth-first, then step by step: a breadth-first search over sorted positions for the fewest, then the most by stepping in from whichever end has free places beside it and counting. O(g^2) positions |
| `moving_stones_window.kara` | a board and a window: lay the places from the low stone to the high one on a `Vec[bool]`. The most is the free places on it; the fewest is three less the most stones any three consecutive places hold. O(z - x) |
| `moving_stones_steps.kara` | trying the moves: 0 if the stones touch, 1 if some single move of an end stone makes them touch, else 2; the most by playing it out one place at a time. O(z - x) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 16 lines: the answers for eight triples,
LeetCode's three examples among them; for every order of three places
from 1 to 6 (120) and from 1 to 20 (6,840), and for 50 random triples
from 1 to 100, the two sums of the answers and a checksum; and five
answers on the widest spans. `moving_stones.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: from the sorted positions, every move the statement allows
(the stone at `x` or at `z` to any `k` with `x < k < z`, `k != y`),
searched for the fewest and the most moves to three consecutive places,
each position's answer kept in one `Map` across all cases since it does
not depend on how the position was reached. It checks 642 cases: every
order of three places from 1 to 8 (336), 300 random triples from 1 to
25, and 6 from 1 to 100. The 637 with the end stones at most 24 apart
are searched in full. Each case is also asked with the stones named in
another order, moved along by a random amount from 1 to 50, and with
the line read the other way.

| | property |
|---|---|
| P1 | the statement read literally, on spans of at most 25 places |
| P2 | which stone is named first does not matter |
| P3 | moving every stone along by the same amount does not change the answer |
| P4 | the line read the other way does not change the answer |
| P5 | the fewest is 0, 1 or 2, and 0 exactly when the stones touch; it is at most the most, and the most is at most the free places between the end stones |
| P6 | each arm agrees with at least two of the other five |

The differential prints `642 cases (637 searched in full): checksum
648615824, 23082 checks over 6 arms: 0 failures` under `karac
__mir-run` (13 s), `karac __mir-llvm-run` and `karac __mir-llvm-asan`
with no error.

## Mutation testing

Thirty-two edits to the differential, each run under `karac __mir-run`
and `karac __mir-llvm-run`. Eighteen are kept, three to each arm. All
eighteen are killed, each fails the same checks under both backends,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a gap of one free place not filled in one move | P1 169, P6 169 |
| M2 | ★: both gaps small needed for one move | P1 324, P6 325 |
| M3 | ★: the stones reversed, not sorted | P1 540, P2 612, P4 642, P5 419, P6 544 |
| M4 | memo: the high stone's jump into the low gap leaves one free place too many | P1 565, P4 549, P5 570, P6 570 |
| M5 | memo: a move costs nothing for the fewest | P1 597, P5 602, P6 602 |
| M6 | memo: the high gap counted with its stone | P1 637, P4 143, P5 642, P6 642 |
| M7 | table: the pairs with the high gap empty never filled | P1 299, P4 248, P5 118, P6 303 |
| M8 | table: the high stone never jumps into the low gap, for the fewest | P1 70, P4 143, P6 70 |
| M9 | table: pairs with one free place never filled | P1 597, P5 66, P6 602 |
| M10 | bfs: the search stops one place early | P1 131, P5 66, P6 131 |
| M11 | bfs: the place beside the low stone never a target | P1 104, P4 209, P5 34, P6 104 |
| M12 | bfs: a stack, not a queue | P1 492, P4 257, P5 326, P6 497 |
| M13 | window: a window of two places | P1 209, P5 40, P6 209 |
| M14 | window: the window from the low stone never tried | P1 207, P4 325, P5 40, P6 208 |
| M15 | window: the stones counted as free places | P1 551, P5 182, P6 556 |
| M16 | steps: only the low stone tried for one move | P1 167, P4 325, P6 168 |
| M17 | steps: places past the middle stone never tried | P1 202, P4 391, P5 32, P6 203 |
| M18 | steps: stones that touch counted one move away | P1 40, P5 40, P6 40 |

P1 and P6 kill all eighteen, P5 fourteen, P4 ten, and P2 one. P3
kills none: every arm works from the distances between the stones or
counts from the low stone up, so, read from the code, an edit goes as
wrong on the stones moved along as on the stones where they are. P2 sees only the edit that
reverses the stones instead of sorting them (M3). P4 sees the edits that treat
the low end and the high end differently, such as the high stone never
jumping into the low gap (M8) or only the low stone tried (M16). P5
misses the edits that only pick the wrong one of 1 and 2 for the
fewest (M1, M2, M8, M16). The checks draw random numbers for every case
whatever the answers, so every mutant sees the same cases and their
counts can be compared.

Fourteen other edits were tried and set aside. Three change no answer
and are equivalent: the table never letting the low stone jump into the
high gap when counting the most (stepping in already reaches the
most), the table's most starting at 1 (a pair with free places always
has a move), and the steps arm stopping its search at the first single
move that works. Two crash under both backends: memo's high stone
leaving its gap as it was recurses into the same pair until the stack
overflows (exit 134), and the window arm taking its low end from two
of the three stones indexes off the board (exit 101). The other nine
were killed too, beyond three per arm. Three fail exactly as kept ones
do: bfs moving only the low stone as M16, and the steps arm stopping
one step early or calling stones one place apart touching as M9. Two
fail alike each other, ★ and the window arm counting one move too many
(`P1 637, P5 642, P6 642`). The other four fail on their own: ★ calling
stones one place apart touching, memo capping the most at three, bfs
stepping in from the stones as given, and the steps arm counting the
low stone's steps twice.

## Verification

Every arm prints the same output as `moving_stones.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. The differential prints its line under all three. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reported one thing: the bfs
arm's `let (mut x, y, mut z) = start;` is E0001 twice, "`mut x` inside
a pattern is Rust syntax -- in Kāra `mut` goes before the whole
pattern, `let mut <pattern> = ..`". Both came with machine-applicable
edits. I wrote `let mut (x, y, z) = start;` by hand, and `karac fix` on
the original makes the same change. Every file then checks clean. The
release build is kara `6697158faf`, with runtime archives rebuilt at
that commit. Under `karac __mir-run` the arms take 0.15 s (★) to 32 s
(memo, which searches every pair of gaps afresh for each triple). No
gap turned up.

## Benchmarks

The bench builds 1,000,000 random triples of distinct places from 1 to
100 (LeetCode's range) once in all five languages, then answers every
triple 40 times with the ★ arm, folding both answers into a sum and a
checksum. Every call sorts the three stones and returns two answers:
two short `Vec`s per call in Kāra and Rust, two slices in Go, two lists
in Python, and in C two arrays on the stack, sorted with `qsort`. Every
implementation prints `1000000 triples, 40 rounds: sum 2013426600,
checksum 384171582`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 1.062 to 1.291 s | 1.130 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.115 to 1.251 s | 1.144 s |
| Kāra (`karac build`) | 1.353 to 1.469 s | 1.405 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.327 to 1.504 s | 1.433 s |
| C (`clang -O3`) | 1.760 to 1.948 s | 1.866 s |
| Go | 5.922 to 6.656 s | 6.197 s |
| Python | 19.6 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(1.36 s real, 1.36 s user) and runs as fast as the sequential one.

Kāra took 1.25 times Rust's median time under overflow checks. Both
allocate and free the same two small vectors on every call. C is slower
than both, likely because `qsort` calls its comparison through a
function pointer even for three elements (inferred from the source,
not profiled), so C here is not the floor.
