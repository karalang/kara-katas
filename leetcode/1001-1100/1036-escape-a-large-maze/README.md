# 1036. Escape a Large Maze

There is a 1 million by 1 million grid on an XY-plane, and the
coordinates of each grid square are `(x, y)`.

We start at the `source = [sx, sy]` square and want to reach the
`target = [tx, ty]` square. There is also an array of `blocked`
squares, where each `blocked[i] = [xi, yi]` represents a blocked square
with coordinates `(xi, yi)`.

Each move, we can walk one square north, east, south, or west if the
square is not in the array of `blocked` squares. We are also not
allowed to walk outside of the grid.

Return `true` if and only if it is possible to reach the `target`
square from the `source` square through a sequence of valid moves.

```
blocked = [[0,1],[1,0]], source = [0,0], target = [0,2]            ->  false
blocked = [],            source = [0,0], target = [999999,999999]  ->  true
```

**Constraints:** `0 <= blocked.length <= 200`; `blocked[i].length == 2`;
`0 <= xi, yi < 10^6`; `source.length == target.length == 2`;
`0 <= sx, sy, tx, ty < 10^6`; `source != target`; it is guaranteed that
`source` and `target` are not blocked.

The Kāra arms take `blocked` as a `Vec[(i64, i64)]` and each point as
an `(i64, i64)`.

## Approaches

Every arm rests on one bound: `n` blocked squares fence off the most
room when they cut a corner on a diagonal, which shuts in
`n * (n - 1) / 2` squares. A search from the source that reaches the
target, or more squares than that, cannot be fenced in, and the source
and the target can meet exactly when neither is fenced in. Each arm
takes the side of the grid as a parameter of an inner function, so the
differential can run it on small grids.

| file | mechanism |
|---|---|
| `escape_maze.kara` ★ | breadth-first, bounded: a `VecDeque` and a `Set[(i64, i64)]` of the squares seen, from the source and then from the target, each stopping at the other end or past the bound. O(n^2) squares per search |
| `escape_maze_dfs.kara` | depth-first, by recursion: the same bounded search, walked by a recursive function that returns as soon as it reaches the other end or passes the bound |
| `escape_maze_stack.kara` | a stack over numbered squares: depth first with a `Vec` as the stack, every square numbered `x * side + y`, so the blocked and seen sets hold plain integers |
| `escape_maze_rows.kara` | a looser bound, squares by row: `n * n` squares, a bound that needs no argument about corners, with the blocked and seen squares kept as a `Map` from each row to the `Set` of its columns |
| `escape_maze_both.kara` | two searches at once: breadth first from both ends, one square from each in turn. A square one search reaches that the other has seen joins them; a search that runs dry within the bound means false; once both pass the bound, true |
| `differential.kara` | the five arms against the statement read literally on small grids, six properties |

Every arm prints the same 15 lines: the answers for eleven mazes,
LeetCode's two examples among them, with walls of 200 squares across a
corner and diamonds of 200 around a square, from inside, from outside,
and with both ends inside; and for four groups of random mazes (10 to
200 blocks within 6 to 10^6 squares of a corner), the number that
escape and a checksum. `escape_maze.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms' inner functions and
the statement read literally on a small grid: from the source, move one
square north, east, south or west at a time, never onto a blocked
square and never off the grid, and answer whether the target is among
the squares that can be reached, found by visiting every one of them.
It checks 718 cases: 600 random mazes on grids of side 2 to 7 with up
to 12 blocked squares, all searched in full; 60 on the 10^6 grid with
up to 30 blocked squares within 8 of a corner; and 58 walls of 2 to 30
blocks across a corner of the 10^6 grid, which shut in exactly as many
squares as the bound allows, from a square inside to one outside
(false) or to another inside (true). 595 of the 718 have a path. Each case is also asked with the source and the target the
other way round, with the grid mirrored, with it turned on its
diagonal, and with one blocked square taken away. The small grids test
the bound where the grid's edges are close on every side, which the
10^6 grid never has.

| | property |
|---|---|
| P1 | the statement read literally, on grids of side at most 7, or the answer a corner wall forces |
| P2 | a path one way is a path back |
| P3 | mirroring the grid mirrors every path |
| P4 | turning the grid on its diagonal turns every path |
| P5 | taking a blocked square away never closes a path |
| P6 | each arm agrees with at least two of the other four |

The differential prints `718 cases (600 searched in full, 595 with a
path): checksum 754029025, 21240 checks over 5 arms: 0 failures` under
`karac __mir-run` (6.8 s), `karac __mir-llvm-run` and `karac
__mir-llvm-asan` with no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`. Fifteen are kept, three to each arm. All
fifteen are killed, each fails the same checks under both backends,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first column out of bounds | P1 100, P4 108, P6 102 |
| M2 | ★: only the source asked | P1 4, P2 41, P6 6 |
| M3 | ★: a fenced search that moved at all called free | P1 54, P6 58 |
| M4 | dfs: only the first open neighbour walked | P1 166, P3 74, P4 101, P5 13, P6 183 |
| M5 | dfs: one column past the edge | P1 30, P4 33, P6 31 |
| M6 | dfs: blocked squares walked through | P1 119, P6 123 |
| M7 | stack: never steps into row 0 | P1 76, P3 97, P4 112, P6 76 |
| M8 | stack: a step south lands one east too | P1 64, P3 56, P4 87, P6 70 |
| M9 | stack: east past the edge wraps to the next row | P1 18, P3 4, P4 19, P6 19 |
| M10 | rows: the bound `n`, not `n * n` | P1 27, P6 27 |
| M11 | rows: a row with any mark holds every column | P1 422, P4 23, P6 473 |
| M12 | rows: a second mark in a row dropped | P1 83, P4 29, P5 6, P6 87 |
| M13 | both: the source's search free at the bound itself | P1 31, P2 31, P6 31 |
| M14 | both: one search free is enough | P1 31, P6 31 |
| M15 | both: the last row out of bounds | P1 27, P3 66, P4 55, P6 28 |

P1 and P6 kill all fifteen, P4 nine, P3 five, and P2 and P5 two each.
P2 sees only the edits that treat the two ends differently: ★ asking
only from the source (M2), and the two searches' bound applied
differently (M13). P3 mirrors the x axis, so it misses the edits that
go wrong the same way on both sides of it, and P4 the ones that go
wrong the same way across the diagonal. P5 sees only the edits whose
answer can turn false when a block goes: a walk that takes only the
first open neighbour (M4), and a row's second mark dropped (M12). The
checks draw random numbers for every case whatever the answers, so
every mutant sees the same cases and their counts can be compared.

The corner walls were added after a first run of these mutants on the
660 random mazes alone. That run left M10 alive: random blocks almost
never shut in more than `n` squares, so a bound of `n` gave every
right answer there. All 27 of its failures now are
walls, and the bound edits (M3, M13, M14 and the alike group below) fail far more
often with them.

Fifteen other edits were tried and set aside. Three change no answer
and are equivalent: the recursive walk not counting its start square
(it is seen again on the way back, and the bound still holds), the
rows arm counting every square twice (`n * n / 2` is still at least
`n * (n - 1) / 2`), and the two searches putting new squares at the
front of the queue (a bounded search finds the same squares in any
order). The other twelve were killed too, beyond three per arm. Three
fail exactly alike, `P1 41, P6 41`: ★'s bound one square short, the
recursive walk free at the bound itself, and the two searches' bound
halved. Two fail alike, `P1 168, P6 170`: ★ not stopping at the target
and the two searches never meeting. Seven fail on their own: ★ and the
rows arm allowing a diagonal step, the recursive walk never stepping
west, the stack arm numbering the blocked squares turned, numbering
the goal from its row twice, and reading a square's row and column the
wrong way round, and the rows arm taking either end free as enough.

## Verification

Every arm prints the same output as `escape_maze.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. The differential prints its line under all three. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reported nothing on any file.
The release build is kara `6697158faf`, with runtime archives rebuilt at
that commit. Under `karac __mir-run` the arms take 4.3 s (stack) to 35
s (rows, whose bound is twice as loose and whose sets are nested). No
gap turned up.

## Benchmarks

The bench builds 30 mazes of 200 blocks (LeetCode's most) once in all
five languages: ten diamonds around a random square searched from
inside, ten searched from outside to the far corner, and ten walls
across the corner at (0, 0) searched from outside to a random square.
Then it answers all thirty four times with the ★ arm, counting the
escapes and folding the answers into a checksum. Kāra's sets are
`Set[(i64, i64)]` and Rust's `HashSet<(i64, i64)>`, both SipHash-1-3;
Go's are maps keyed by `[2]int64`; Python's are sets of tuples; C has
no set, so its squares are integers `x * side + y` in an open-addressing
table with a multiplicative hash. Every implementation prints `30 mazes
of 200 blocks, 4 rounds: 80 escapes, checksum 511860669`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.278 to 0.324 s | 0.285 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.685 to 0.756 s | 0.714 s |
| Rust (`rustc -O`) | 0.683 to 0.864 s | 0.724 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.929 to 1.198 s | 0.976 s |
| Kāra (`karac build`) | 0.953 to 1.019 s | 0.978 s |
| Go | 1.138 to 1.258 s | 1.202 s |
| Python | 4.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(0.96 s real, 0.96 s user) and runs as fast as the sequential one.

Kāra took 1.37 times Rust's median time under overflow checks, with the
same hash on both sides. C's lead is mostly its cheaper hash and flat
table, so it measures a different set, not a faster language (inferred
from the sources, not profiled).
