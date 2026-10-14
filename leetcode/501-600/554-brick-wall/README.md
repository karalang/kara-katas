# 554. Brick Wall

There is a rectangular brick wall in front of you with `n` rows of
bricks. The `i`th row has some number of bricks each of the same height
(i.e., one unit) but they can be of different widths. The total width of
each row is the same. Draw a vertical line from the top to the bottom
and cross the least bricks. If your line goes through the edge between
two bricks, this will not be considered as crossing a brick. You cannot
draw a line just along one of the two vertical edges of the wall, in
which case the line will obviously cross no bricks. Given the 2D array
`wall` that contains the information about the wall, return the minimum
number of crossed bricks after drawing such a vertical line.

```
wall = [[1,2,2,1],[3,1,2],[1,3,2],[2,4],[3,1,2],[1,3,1,1]]  ->  2
wall = [[1],[1],[1]]                                        ->  3
```

**Constraints:** `n == wall.length`, `1 <= n <= 10^4`, `1 <=
wall[i].length <= 10^4`, `1 <= sum(wall[i].length) <= 2 *
10^4`, `sum(wall[i])` is the same for each row `i`, and `1 <= wall[i][j]
<= 2^31 - 1`.

## Approaches

Every arm is `fn least_bricks(wall: Vec[Vec[i64]]) -> i64`. A line
crosses every row except those with an edge where it is drawn, and a
row's edges are its running sums with the last (the wall's right side)
left out. So the answer is the number of rows less the most rows that
share one edge position.

| file | mechanism |
|---|---|
| `brick_wall.kara` ★ | a `Map` from position to the number of rows with an edge there, the largest count kept as it goes; O(bricks) |
| `brick_wall_sorted.kara` | every edge in one `Vec`, sorted, and the longest run of one position; O(bricks log bricks) |
| `brick_wall_merge.kara` | the rows' edges, each row already in order, merged by a `PriorityQueue` holding every row's next edge, smallest first; equal positions come off together; O(bricks log rows) |
| `brick_wall_search.kara` | every distinct edge position, from a `Set`, tried as the line: a `binary_search` in each row's running sums says whether the row is crossed there; O(positions * rows * log bricks) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: the two examples, five small walls
at the edges (one brick, aligned rows, bricks 2^31 - 1 wide), a checksum
over 300 random walls, and two at the problem's most: just under
20,000 bricks in rows 300 wide, and 10,000 rows of one brick.
`brick_wall.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: a line at every whole position strictly
inside the wall, each row walked brick by brick to see whether the line
passes through a brick or along an edge, and the fewest crossed. Each
arm is held to the properties below on 1,000 random walls: 1 to 8 rows
1 to 12 wide with bricks 1 to 4 wide, or 1 to 5 rows 1 to 600 wide with
bricks 1 to 150 wide, in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is between 0 and the number of rows |
| P3 | the rows in the other order give the same answer |
| P4 | every row read right to left gives the same answer |
| P5 | one more row of a single brick gives one more |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the wall's right side counted as an edge | P1 582, P5 1000 |
| M2 | ★: every edge stored as a count of one | P1 328 |
| M3 | sorted: a run continued by any larger position | P1 891, P2 838 |
| M4 | sorted: the edges reversed, not sorted | P1 538, P3 42, P4 42 |
| M5 | merge: the wall's right side pushed as an edge | P1 490 |
| M6 | merge: the next edge set to a brick's width, not added | P1 498, P2 264, P3 95, P4 283 |
| M7 | search: a row counted as crossed where it has an edge | P1 770, P5 944 |
| M8 | search: each row's first edge left out | P1 336, P4 166 |
| E1 | ★: the most taken on a tie as well | 0 |
| E2 | sorted: the run started at one | 0 |
| E3 | merge: no check that a run has started | 0 |
| E4 | search: `contains` in place of the binary search | 0 |

M1 and M5 make the same mistake in two arms and are seen differently. In
M1 every row has an edge at the right side, so the answer is always
0 and one more row of one brick still gives 0, which P5 sees on every
case. In M5 a row of one brick pushes no first edge and so none after
it; the extra row is still crossed, so P5 holds and only P1 sees it.
M2 is wrong only when three or more rows share an edge, since a stored
count of one still makes the next a two. P3 and P4 see the mutants whose
answer depends on the order the bricks come in: M4's runs, M6's
positions and M8's missing first edge, which reading the row backwards
turns into a missing last one. E3 is safe because every edge is at least
1 and the run starts from position 0, E2 because the run is set to one
at the first edge anyway, and E1 and E4 because they give the same
counts.

## Verification

Every arm prints the same output as `brick_wall.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends: every arm prints the same output under
`karac run` and `karac build`, and under `KARAC_AUTO_PAR=1 karac build`.
Under `karac run --interp` the ★, sorted and merge arms do too, but the
search arm prints wrong answers, 0 for the first example where the
answer is 2: `sums.binary_search(x)` with `x` taken from a `Set`'s
`iter()` reports every position as found, in every row, in the legacy
tree-walker. The differential stops at type checking under all three on
`*w` over a `Vec[i64]`'s `iter()` ("unary '*' requires 'ref T' ... found
'i64'"). Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 20 random walls once, each
1,000,000 wide with bricks 1 to 10,000 wide, row after row until it has
just under 20,000 bricks (the problem's most); then 50 times over every
wall is answered, a fresh `Map` each time. Every implementation prints
`20 walls, 382016 bricks, 50 rounds each: total 92700, checksum
471262060`, the Kāra program under `karac __mir-run` included (30.4 s).

Each implementation counts with its own hash map, made fresh for each
wall: `HashMap` in Rust, a `map` in Go and a `dict` in Python; C has
none, so its mirror makes an open-addressing table of position and count
that doubles as it fills. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.99 to 1.06 s |
| Rust (`rustc -O`) | 1.22 to 1.29 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.13 to 1.28 s |
| Go | 1.34 to 1.37 s |
| Python | 2.70 to 2.78 s |
| Kāra (`karac build --mir`) | 1.08 to 1.16 s |

The legacy `karac build` refuses this program: it moves `walls[(round *
7 + g) % count]` out of the index (E_INDEX_MOVE_NON_COPY) where
v2 borrows it. So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`af2123abc5`. Under `karac __mir-llvm-run` the program prints the same
line in 13.3 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark. The Kāra row is level
with C's hand-written table and a little ahead of Rust's `HashMap`,
whose default hasher is SipHash as Kāra's `Map`'s is. Python is close
behind for once, because its `dict` is written in C and does all the
work here.

## Compiler findings

None new. Nothing was filed from this kata; the legacy failures above
are not filed because legacy is frozen.
