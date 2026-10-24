# 980. Unique Paths III

You are given an `m x n` integer array `grid` where `grid[i][j]` could
be:

- `1` representing the starting square. There is exactly one starting
  square.
- `2` representing the ending square. There is exactly one ending
  square.
- `0` representing empty squares we can walk over.
- `-1` representing obstacles that we cannot walk over.

Return the number of 4-directional walks from the starting square to
the ending square, that walk over every non-obstacle square exactly
once.

```
grid = [[1,0,0,0],[0,0,0,0],[0,0,2,-1]]  ->  2
grid = [[1,0,0,0],[0,0,0,0],[0,0,0,2]]   ->  4
grid = [[0,1],[2,0]]                     ->  0
```

**Constraints:** `1 <= m, n <= 20`; `1 <= m * n <= 20`;
`-1 <= grid[i][j] <= 2`; there is exactly one starting cell and one
ending cell.

## Approaches

| file | mechanism |
|---|---|
| `unique_paths_iii.kara` ★ | backtracking on the grid: a walk steps to a free neighbour, marks it, recurses with one square fewer to cover and unmarks it on the way back; reaching the end with nothing left to cover counts one path. O(3^k) for k free squares |
| `unique_paths_iii_stack.kara` | the same walk without recursion: the path is a stack of squares, each with the next direction it will try, and a square that has tried all four is popped and unmarked |
| `unique_paths_iii_bits.kara` | a bitmask over numbered squares: the free squares are numbered and each given the list of its free neighbours, so the walk never looks at the grid; the squares covered are the bits of one integer |
| `unique_paths_iii_memo.kara` | memoised over (covered set, place): the ways to finish depend only on where the walk stands and which squares it has covered, so each pair is counted once and kept in a `Map`. At most 2^k * k states, far fewer reachable |
| `unique_paths_iii_layers.kara` | counting forward a step at a time: a `Map` from (covered set, place) to the number of walks that got there, advanced from the start one step at a time; after k - 1 steps the walks on the end with every square covered are the answer |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines. The first ten are LeetCode's three
examples and seven more: start and end side by side (1); an obstacle
between them (0); [2, 0, 1] (1); a 2 x 2 grid from corner to opposite
corner, which the checkerboard rules out (0); a 3 x 3 ring around an
obstacle from corner to opposite corner, which must leave one side
uncovered (0); the open 3 x 3 grid from corner to opposite corner (2);
and from its middle to a corner (2). Then totals and checksums over
random grids with about one square in five an obstacle: 300 of up to
9 squares (59 paths) and 3,000 of up to 16 (199). The last five are
LeetCode's largest, open grids of 20 squares: 4 x 5 from corner to
opposite corner (20), to the corner below (23), and from (1, 2) to a
corner (14); 2 x 10 from one corner to the far corner on the same side
(1); and 1 x 20 from end to end (1). `unique_paths_iii.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every ordering of the free squares between the start and
the end is tried, and the ones whose every step is to a neighbour are
counted. That is (k - 2)! orderings, so the statement's grids are
small: it checks 3,200 grids, 3,000 of up to 9 squares against the
statement and 200 of up to LeetCode's 20 against the other properties.
About one square in five is an obstacle in the small grids and one in
eight in the large ones, every third grid has none, and every other
grid has its start and end drawn again, up to 20 times, until the
checkerboard allows a path. 770 of the 3,200 grids have one.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 grids |
| P2 | the grid transposed, or turned left to right, has as many paths |
| P3 | the start and the end swapped has as many paths, each read backwards |
| P4 | no path when the checkerboard forbids one: with an even count of free squares a path ends on the other colour from where it starts, with an odd count it starts and ends on the colour with one square more |
| P5 | a border of obstacles all round changes nothing |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 grids of 21790 squares: 822 paths in 770 grids,
checksum 157705646, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (28.9 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-nine edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: reaching the end early counted | P1 1958, P4 658, P6 2113 |
| M2 | ★: a square never unmarked | P1 104, P2 161, P3 65, P6 120 |
| M3 | ★: never a step to the left | P1 307, P2 405, P3 202, P6 329 |
| M4 | stack: a square never unmarked | P1 182, P2 165, P3 41, P6 200 |
| M5 | stack: never a step up | P1 627, P2 539, P3 443, P6 654 |
| M6 | stack: the start and the end not counted as free | P1 1186, P4 33, P6 1235 |
| M7 | bits: the start not marked as covered | P1 879, P3 228, P4 151, P6 921 |
| M8 | bits: no neighbour above | P1 408, P2 303, P3 443, P6 431 |
| M9 | bits: square 0 left out of the full set | P1 877, P2 77, P4 143, P6 913 |
| M10 | memo: the place left out of the key | P1 180, P2 164, P3 129, P6 199 |
| M11 | memo: one too many remembered | P2 4, P3 10, P4 3, P6 10 |
| M12 | memo: no neighbour to the right | P1 294, P2 418, P3 202, P6 315 |
| M13 | layers: one step short | P1 740, P6 770 |
| M14 | layers: each way in counted once | P3 3, P6 5 |
| M15 | layers: one path counted when none arrives | P1 2260, P4 831, P6 2430 |

P6 kills all fifteen, P1 thirteen (all but M11 and M14), P3 ten, P2
nine, P4 six (M1, M6, M7, M9, M11, M15) and P5 none. M11 and M14 are
wrong only when two partial walks reach the same covered set and place,
which a grid of up to 9 squares with obstacles rarely allows, so the
statement never sees them; only the large grids show them, where the
wrong count of a grid differs from that of its transpose or its swap. No
arm treats the grid's edge differently from an obstacle, so P5 finds
nothing. M13 stands for a family: one step short, the place never moved
and the start not marked all leave layers with no walk on the end, so
each answers 0 and fails P1 on the 740 small grids that have a path and
P6 on all 770.

Fourteen other edits were tried and set aside. Seven failed exactly
the same checks as a kept one: stack, bits and memo counting a walk
that reaches the end early, as M1; memo not marking the start, as M7;
layers never moving the place or not marking the start, as M13; and
layers with no neighbour to the left, as M3. Four were sound but
beyond three an arm: ★ not counting the end among the squares to
cover and starting with one square fewer, which fail the same checks
as each other; bits marking the square it leaves rather than the one
it enters; memo numbering the end one square early. Two are
equivalent: stack carrying on past the end and layers letting walks
carry on past it, since the end is then marked and no later step can
return to it, so a walk that passed it never counts.

One survived and is not equivalent: memo keying its map by
`seen * 16 + at` instead of `seen * 32 + at`, so that a place of 16 or
more collides with a different covered set. It needs 17 free squares
and two reachable states whose keys collide. Run separately on every
start and end of the open 4 x 5, 5 x 4, 2 x 10 and 3 x 6 grids, it
answers wrongly for 8 of the 1,520 pairs; none of the differential's
200 large grids is one of them.

## Verification

Every arm prints the same output as `unique_paths_iii.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.33 s (bits) to 0.54 s (stack), and the differential
28.9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages over every start and
end of an open 4 x 5 grid, LeetCode's largest: 380 searches a round,
each a full backtracking walk over 20 squares, in 20 rounds. Every
implementation prints `20 rounds over 380 starts and ends of a 4 x 5
grid: 40240 paths, checksum 848569101`. Each search copies the grid
and walks it by recursion, marking and unmarking squares in place: C
on a fixed 4 x 5 array, the others on a vector of rows.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.305 to 0.347 s | 0.328 s |
| Rust (`rustc -O`) | 0.484 to 0.584 s | 0.511 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.472 to 0.505 s | 0.484 s |
| Go | 0.370 to 0.415 s | 0.389 s |
| Python | 16.0 s | |
| Kāra (`karac build --mir`) | 0.481 to 0.566 s | 0.517 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 31 times
Kāra's.

v2 took 1.07 times Rust's median time under overflow checks and 1.58
times C's. Under valgrind's cachegrind v2 ran 4,773 million
instructions and 745 million branches with 67.7 million mispredicted,
Rust with overflow checks 4,867 million, 726 million and 67.6 million,
and C 2,754 million, 415 million and 68.8 million. All three
mispredict alike, on which neighbour is free; v2 and Rust run about
1.75 times C's instructions, where both index a vector of rows with
bounds checks and C a fixed array without them, which is the likely
part of the difference (inferred, not traced).
