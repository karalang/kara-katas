# 909. Snakes and Ladders

You are given an `n x n` integer matrix `board` where the cells are
labeled from `1` to `n²` in a
[Boustrophedon style](https://en.wikipedia.org/wiki/Boustrophedon)
starting from the bottom left of the board (i.e. `board[n - 1][0]`) and
alternating direction each row.

You start on square `1` of the board. In each move, starting from
square `curr`, do the following:

- Choose a destination square `next` with a label in the range
  `[curr + 1, min(curr + 6, n²)]`. This choice simulates the result of a
  standard 6-sided die roll: i.e., there are always at most 6
  destinations, regardless of the size of the board.
- If `next` has a snake or ladder, you **must** move to the destination
  of that snake or ladder. Otherwise, you move to `next`.
- The game ends when you reach the square `n²`.

A board square on row `r` and column `c` has a snake or ladder if
`board[r][c] != -1`. The destination of that snake or ladder is
`board[r][c]`. Squares `1` and `n²` are not the starting points of any
snake or ladder.

Note that you only take a snake or ladder at most once per dice roll. If
the destination to a snake or ladder is the start of another snake or
ladder, you do **not** follow the subsequent snake or ladder.

Return the least number of dice rolls required to reach the square
`n²`. If it is not possible to reach the square, return `-1`.

```
board = [[-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1],
         [-1,35,-1,-1,13,-1],
         [-1,-1,-1,-1,-1,-1],
         [-1,15,-1,-1,-1,-1]]   ->  4   (1 -> 2, ladder to 15; 15 -> 17, snake to 13;
                                         13 -> 14, ladder to 35; 35 -> 36)
board = [[-1,-1],[-1,3]]        ->  1
```

**Constraints:** `n == board.length == board[i].length`, `2 <= n <= 20`,
`board[i][j]` is either `-1` or in the range `[1, n²]`, and the squares
labeled `1` and `n²` are not the starting points of any snake or ladder.

## Approaches

| file | mechanism |
|---|---|
| `snakes_and_ladders.kara` ★ | a breadth-first search over the squares: every roll is one move, so the first time a search from square 1 reaches `n²` is the answer; each rolled square is read off the board, its row counted from the bottom and its column from the left or the right as the rows alternate, and a snake or ladder there moves the player on, once. O(n²) |
| `snakes_and_ladders_flat.kara` | the board flattened first: the rows walked from the bottom in alternating directions, writing each square's destination into one array, then the same search with no coordinates. O(n²) |
| `snakes_and_ladders_rounds.kara` | relaxing every square in rounds: a best-known number of moves for every square, swept again and again, each square known in `d` moves offering `d + 1` to where each of its rolls lands, until a sweep changes nothing. O(n⁴) |
| `snakes_and_ladders_layers.kara` | the reachable squares, one move at a time: the set of squares first reached after `d` moves kept as a row of flags, the next set made from it, until a set holds `n²` or comes out empty. O(n⁴) at worst |
| `snakes_and_ladders_recursive.kara` | a depth-first search that lowers the moves it has found: square `s` reached in `d` moves is explored again only when `d` beats the best known for it. |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and five
more (the empty 2 x 2 and 3 x 3 boards, a 3 x 3 board whose squares 2
to 7 are all snakes to square 1, a 4 x 4 board whose ladder from 2 lands
on another ladder that is not taken, and a ladder from 2 to the end);
for 300 random boards of side 2 to 20, with snakes and ladders on every
square, on 1 in 4 or on 1 in 30, or snakes alone on 1 in 2, the number
out of reach, the sum and a checksum of the answers; and three of
LeetCode's largest, 20 x 20: empty, and random with snakes and ladders
on 1 in 4 and on 1 in 20. `snakes_and_ladders.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the labels written onto the board as the statement says,
starting at `board[n - 1][0]` and turning at the end of each row, and
then every game played, each move choosing a square 1 to 6 ahead and
taking the snake or ladder on it once. A game never ends a move on a
square it has already ended one on, and is stopped once it is as long
as the shortest found, since neither can lead to a shorter game. It
checks 3,200 random boards: 3,000 of side 2 to 4 against the statement
and 200 of side 5 to 12 against the other properties; 44,344 squares in
all. The boards have snakes and ladders on every square, on 1 in 3 or
on 1 in 12, snakes alone on every square, or snakes 5 squares down on 7
squares in 8, which make the player crawl: 94 of the boards leave the
end out of reach and the longest answer is 84 moves.

| | property |
|---|---|
| P1 | the statement's fewest moves, on the small boards |
| P2 | `-1` or 1 to `n² - 1` moves, and `ceil((n² - 1) / 6)` for the empty board of the same side |
| P3 | the same answer with a jump from a square to itself added on random empty squares |
| P4 | no worse with a ladder to `n²` added on a random empty square |
| P5 | with only the ladders kept, the end reached in at most the empty board's moves; with only the snakes, in at least as many or never |
| P6 | each arm agrees with at least two of the other four |

P5 holds because with ladders alone every roll of 6 (or the exact roll
onto `n²`) moves the player at least as far as on the empty board, and
with snakes alone no move goes further. P2 to P6 are checked on every
board. It prints `3200 boards, 44344 squares, 94 with the end out of
reach, at most 84 moves, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a snake or ladder's end followed on, once more | P1 373, P6 434 |
| M2 | ★: every row read left to right | P1 855, P3 273, P5 108, P6 929 |
| M3 | ★: rolls of 1 to 5 | P1 448, P2 200, P5 60, P6 541 |
| M4 | flat: rows counted from the top | P1 1066, P3 458, P5 794, P6 1215 |
| M5 | flat: no roll of 1 | P1 87, P6 107 |
| M6 | flat: the last square reached only by a ladder | P1 2323, P2 3200, P5 2539, P6 2452 |
| M7 | rounds: a single sweep | P6 1 |
| M8 | rounds: snakes ignored | P1 287, P6 341 |
| M9 | rounds: square 1 counted as one move | P1 2931, P2 3200, P5 2420, P6 3106 |
| M10 | layers: the bottom row read right to left | P1 1442, P3 422, P5 174, P6 1554 |
| M11 | layers: the rolled square kept, not where it leads | P1 1095, P4 1597, P5 699, P6 1279 |
| M12 | layers: ladders ignored | P1 644, P6 784 |
| M13 | recursive: each move counted twice | P1 2931, P2 3200, P5 2757, P6 3106 |
| M14 | recursive: a way just one move shorter never explored | P1 1208, P2 200, P4 180, P5 466, P6 1336 |
| M15 | recursive: games longer than half the squares cut off | P1 35, P6 51 |

P6 kills all fifteen and P1 fourteen; P5 kills nine, P2 five, P3 three
and P4 two. M7 is the weakest kill. Its one sweep goes up the squares in
order, so it finds every shortest game that only moves forward and
misses only a game that takes a snake down on the way to a ladder; that
mattered on one large board in 3,200 and on none of the small ones, so
only P6 sees it. P3 sees only the mutants that put a square in the wrong
cell (M2, M4, M10): a jump to itself written in a cell the mutant
assigns to another square becomes a real snake or ladder there. P4 sees
the two that can make a board worse with a ladder added: M11 keeps the
rolled square, so the new ladder is never taken, and M14 misses the
shorter games it opens. M15 was killed only once the crawling boards
were added: on the first run, with random boards alone, no answer was
above half the squares, so cutting such games off changed nothing.

Two mutants were replaced. The first M5 marked the rolled square as
seen rather than where it leads, and the differential ran out of
memory and stopped with exit 101: a destination never marked seen is
queued again each time a roll reaches it, and a snake back down makes
that a cycle, so the queue grows without bound. The
first M14 read every row from the other end, which is the same function
as M10 (reading the bottom row right to left swaps the direction of
every row), and both gave the same failures.
## Verification

Every arm prints the same output as `snakes_and_ladders.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.4 to 7.5 s
each (the depth-first search the longest) and the differential 16 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every arm and the differential also print the same output under the
frozen legacy interpreter, the legacy JIT and both legacy builds, with
and without auto-par. The legacy builds of the depth-first arm and of
the differential warn that `goes` (and, in the differential, `board`)
is moved into one call and used again, under legacy's older rule that a
bare parameter takes ownership; the programs run correctly all the
same. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on one 20 x 20 board, LeetCode's
largest, built empty. Each round picks a square from 2 to 399, gives it
no snake or ladder (with chance 1 in 2) or one to a random square,
solves the board and folds the answer into a checksum; 100,000 rounds.
Every implementation prints `100000 rounds on a 20 x 20 board: 139 with
the end out of reach, the rest summing to 394178, checksum 153767498`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.23 to 0.39 s | 0.27 s |
| Rust (`rustc -O`) | 0.33 to 0.54 s | 0.36 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.35 to 0.52 s | 0.36 s |
| Go | 0.73 to 0.84 s | 0.75 s |
| Python | 25.0 s | |
| Kāra (`karac build --mir`) | 0.31 to 0.40 s | 0.37 s |
| Kāra (legacy `karac build`) | 0.29 to 0.44 s | 0.33 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does.

v2 takes 1.02 times Rust's median time under overflow checks and 1.39
times C's. Under valgrind's cachegrind v2 runs 4.40 billion instructions
and 1.19 billion branches, legacy 4.30 billion and 1.19 billion, Rust
with overflow checks 4.68 billion and 1.35 billion, and C 2.97 billion
and 0.61 billion; C also mispredicts 52 million branches against about
75 million for the other three. C reads the board and the move counts
with no bounds checks, which is a likely part of its lead in branches,
but the generated code was not compared.
