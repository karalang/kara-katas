# 773. Sliding Puzzle

A 2 by 3 board holds the tiles 1 to 5 and an empty cell, 0. A move swaps
the 0 with a tile next to it, up, down, left or right. Return the fewest
moves that bring the board to `[[1,2,3],[4,5,0]]`, or -1 if no sequence
of moves does.

```
[[1,2,3],[4,0,5]]  ->  1
[[1,2,3],[5,4,0]]  ->  -1
[[4,1,2],[5,0,3]]  ->  5
```

**Constraints:** the board is 2 by 3 and holds each of 0 to 5 once.

## Approaches

A board is one of 6! = 720 orders of its cells, and a move an edge
between two of them, so all four arms search that graph; they differ in
how they name a board and in the order they search.

| file | mechanism |
|---|---|
| `sliding_puzzle.kara` ★ | breadth-first search from the board over six-digit strings, with a `Set[String]` of boards seen and a `VecDeque` |
| `sliding_puzzle_ranked.kara` | breadth-first search over the boards' Lehmer codes, 0 to 719, with a table of 720 distances; a code is turned back into cells to move the 0 |
| `sliding_puzzle_meet.kara` | bidirectional breadth-first search, from the board and from the solved board, over the integers the six digits spell, a whole level at a time from the smaller side |
| `sliding_puzzle_astar.kara` | A* over the same integers, a `PriorityQueue` ordered by moves made plus the tiles' total Manhattan distance from home |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 7 lines: LeetCode's three examples; the solved
board; a board 14 moves away; `[[0,1,2],[3,4,5]]`, 15 away; then all
720 boards in dictionary order, with how many can be solved, their total
moves, the most any needs and a checksum. Exactly half, 360, can be
solved, the hardest in 21 moves. `sliding_puzzle.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
one breadth-first search outward from the solved board, over the boards
as lists of cells, gives every board's distance, and a board it never
reaches cannot be solved. It runs every arm on all 720 boards, and on
every fourth board also a neighbour of it and a board a random number of
random moves, from 1 to 30, from the solved one.

| | property |
|---|---|
| P1 | the answer is the definition's distance, or -1 |
| P2 | the answer is -1 exactly when the tiles, read row by row with the 0 left out, are in an odd order |
| P3 | a board one move away has an answer one more or one less, or both are -1 |
| P4 | a board k moves from solved has an answer of at most k, and even exactly when k is |

It prints `720 boards (4544 moves), 4 arms, 7200 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error; the total is the ★ arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the end of the top row joined to the start of the bottom | P1 262 |
| M2 | ★: the 0 in the bottom middle never moving up | P1 177, P3 2, P4 5 |
| M3 | ★: each move counted twice | P1 359, P3 96, P4 105 |
| M4 | ranked: the code counting larger cells, not smaller | P1 512, P2 360, P3 180, P4 107 |
| M5 | ranked: every new board one move from the start | P1 357, P3 95, P4 69 |
| M6 | ranked: the goal one move short of solved | P1 360, P4 180 |
| M7 | meet: the frontiers swapped without their maps | P1 714, P2 360, P3 179, P4 70 |
| M8 | meet: the move across the meeting not counted | P1 359, P3 1, P4 162 |
| M9 | meet: the 0 in the bottom middle never moving right | P1 85, P3 9 |
| M10 | A*: the heuristic doubled, so it can overestimate | P1 47, P3 4 |
| M11 | A*: the board with the largest estimate taken first | P1 357, P3 23, P4 139 |
| M12 | A*: the 0 in the top middle never moving down | P1 208, P3 6, P4 6 |

P1 kills all twelve. P2 sees only M4 and M7, which confuse boards
wholesale; every other edit leaves the solvable boards solvable and the
rest not. M1 adds a move between cells 2 and 3, the end of the top row
and the start of the bottom, which keeps everything the other properties
check: the two cells have different colours on the board's checkerboard,
so moves still alternate colours and the solvable half stays the same,
and only P1 sees the shorter answers. M6 and M8 move answers by one,
which P4 sees through its parity, while P3, comparing two answers moved
alike, mostly cannot; M3 doubles them, which both see. The edits that
make a move one-way or search in the wrong order, M2, M9, M10, M11 and
M12, lengthen some answers, which P3 and P4 see only when the rule they
check breaks. Eight first choices were replaced. Six did nothing: taking
a level's longest meeting in the bidirectional arm, which the
alternating colours make the same as its shortest; and in the A* arm
taking the goal when first reached rather than first popped, counting
the 0 in the estimate, as a tile or at home in cell 5, taking tile t's
home as cell t, and never improving a board once queued, all of which
leave A* with Manhattan distance on this graph still finding the fewest
moves first. Two others stopped: never improving a board but re-queueing
it at more moves ran past the ten-minute limit, and reading the cells
from the right failed at an index.

## Verification

Every arm prints the same output as `sliding_puzzle.py` under `karac
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

The frozen legacy backends refuse all four arms, the differential and
the bench at `*x` on the element of a `for` over a `Vec[i64]`, which
legacy gives by value; they also refuse the bench at
`sliding_puzzle(boards[round % 720])`, as a move out of an index. The
timing below is of a copy whose parameter is `ref Vec[Vec[i64]]` and
whose two `*` are dropped. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. The 720 boards
are built once, in dictionary order; each of 20,000 rounds solves the
next of them and folds the answer into a checksum. Every implementation
prints `20000 boards: 10000 solvable, checksum 91450481`, the Kāra
program under `karac __mir-run` included (in 74 s). Kāra's `Set` and
Rust's `HashSet` both hash strings with SipHash-1-3; Go uses its own map
hash and Python its own string hash; C keeps each board in seven bytes,
in an open-addressing table with FNV-1a, and its queue in a fixed array,
so it allocates nothing per board.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.17 to 0.23 s |
| Rust (`rustc -O`) | 1.33 to 1.73 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.25 to 1.60 s |
| Go | 1.21 to 1.31 s |
| Python | 4.79 to 5.05 s |
| Kāra (`karac build --mir`) | 1.98 to 2.50 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
11.8 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 2.05 s,
against C's 0.18, Rust's 1.35 (1.32 under overflow checks) and Go's
1.25, and Python takes about 4.9 s. Under valgrind's cachegrind v2 runs
17.9 billion instructions, Rust 13.4 billion and C 0.76 billion: Kāra,
Rust, Go and Python make a new string and a hash-set entry for every
board they reach, up to 360 a search, while C copies seven bytes. The
legacy build of the copy ran 1.83 to 2.19 s in six runs, a median of
1.91 s in the interleaved ones, so v2 takes 1.07 times legacy, inside
M2's limit of twice legacy; new katas' benches are outside M2's frozen
set in any case. The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new.
