# 2017. Grid Game

You are given a 2 by `n` grid of points. Two robots start at `(0, 0)` and
end at `(1, n - 1)`, each moving only right or down. The first robot moves
first and collects every point on its path, setting those cells to 0; then
the second robot moves and collects the points on its own path. The first
robot plays to make the second robot's total as small as possible, and the
second plays to make it as large as possible. Return the second robot's
total when both play their best.

```
grid = [[2,5,4],[1,5,1]]        ->  4
grid = [[3,3,1],[8,5,2]]        ->  4
grid = [[1,3,1,15],[1,3,3,1]]   ->  7
```

**Constraints:** `grid.length == 2`; `1 <= n <= 5 * 10^4`; `1 <= grid[r][c]
<= 10^5`.

The first robot's path is fixed by the column where it goes down. What it
leaves is the top row after that column and the bottom row before it, and
no path of the second robot can take from both, so the second robot takes
the larger of the two.

## Approaches

| file | mechanism |
|---|---|
| `grid.kara` ★ | one pass moves the turning column along, the top row's remainder falling and the bottom row's start growing, and keeps the smallest of the larger shares. O(n) |
| `grid_prefix.kara` | each row's prefix sums, then the shares at each turn read off them, `map` and `min` over the turns. O(n) with O(n) extra |
| `grid_brute.kara` | each turn's two shares summed afresh. O(n^2) |
| `grid_scan.kara` | the top row's sums after each column by `scan` over the row reversed, the bottom row's sums before each column by `scan`, joined by `zip`. O(n) |
| `grid_game.kara` | each turn played out: the first robot's path cleared from a copy of the grid, and the second robot's best path found by walking the columns. O(n^2) |
| `grid_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<Vec<i32>>`, the sums widened by `as i64`, `i64::MAX`, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: the answers for LeetCode's three
examples and four more; then the sum and a checksum of the answers for 3000
grids of 1 to 12 columns of points up to 1 to 20, and for 4 grids of up to
3000 columns of points up to 3 or 100000. `grid.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each column the first robot can turn at, its path cleared,
and then every column the second robot can turn at, its path summed; the
smallest over the first robot's turns of the largest over the second's. It
checks 1500 problems of 1 to 10 columns of points up to 1 to 20. Every
random choice of a problem (the points, a new corner value) is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the grid turned half round, the top row read backwards as the bottom and the bottom backwards as the top, leaves the answer |
| P3 | every point doubled doubles the answer |
| P4 | the top left point changed leaves the answer: the first robot always takes it |
| P5 | the bottom right point changed leaves the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 problems: checksum 899782515, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: both shares summed | P1 1157, P6 1157 |
| M2 | ★: the top total missing the first point | P1 1069, P2 1009, P4 1189, P6 1069 |
| M3 | prefix: the largest share over the turns taken | P1 1335, P6 1335 |
| M4 | prefix: the bottom sums read from the top row | P1 907, P2 1112, P4 1184, P6 907 |
| M5 | prefix: the first turn never tried | P1 81, P2 167, P6 81 |
| M6 | brute: the top share from the turning column | P1 1313, P2 168, P4 168, P6 1313 |
| M7 | brute: the bottom share started at the first top point | P1 1174, P2 1196, P4 1439, P6 1174 |
| M8 | scan: the bottom sums never carried | P1 1421, P2 1185, P5 914, P6 1421 |
| M9 | scan: the bottom sums read one turn late | P1 1168, P6 1168 |
| M10 | scan: the top sums read one turn late | P1 1190, P6 1190 |
| M11 | game: the second robot leaving the top cell behind | P1 1076, P2 958, P6 1076 |
| M12 | game: the whole top row cleared | P1 1355, P6 1355 |
| M13 | Rust: the top share kept whole | P1 1500, P2 1328, P4 1482, P6 1500 |
| M14 | Rust: the bottom share's points counted twice | P1 1172, P2 1111, P6 1172 |
| M15 | Rust: only half of each top point taken off | P1 1481, P2 1164, P3 1034, P4 1435, P6 1481 |

P1 and P6 kill all fifteen, P2 ten, P4 six, and P3 and P5 one each. P2
turns the grid half round, which swaps the top row's share after the turn
with the bottom row's before it, so it sees every edit that treats the two
shares or the two rows unevenly. It misses the edits that are their own
image under the turn: both shares summed (M1), the largest over the turns
(M3), the game played with the top row or a whole share gone (M12), and the
scan arm's two sums read a turn late (M9, M10), which shift both shares
alike. P4 changes the top left point, which only the first robot ever
takes, so it sees the edits that let that point into a share: a top total
missing it or counting it (M2, M6, M13, M15), a bottom share that starts
with it (M7), and bottom sums read from the top row (M4). P5 changes the
bottom right point, which the first robot also always takes, and sees only
the scan arm's bottom sums that never carry, which read the point a turn
early (M8). P3 doubles every point, and every edit but one is linear in
the points; halving each point taken off the top (M15) is not, since an
odd point loses a remainder.

The other fifteen fail as a kept one does. A share that counts the turning
column itself takes eleven of them across five arms: the bottom share (P1
1313, P2 168, P5 162: the ★, prefix, brute, scan, game and Rust arms, seven
edits) or the top share (M6's counts: the ★, prefix, scan and game arms,
four more). The ★ arm taking the smaller share and the game arm clearing
the whole bottom row answer 0 always, as M12 does; the brute arm's top
share stopping a column short fails as M11, and its bottom share read from
the top row as M4. Nine drafts were replaced. The ★ arm never turning at
the last column leaves a grid of one column with no answer, and the
checksum overflows (a crash). Eight more answered 0 always and duplicated
M12: only the top share counted, the scan arm's top sums never reversed and
the smaller of each pair taken, the second robot going down at once, only
from above or read on the top row, and the Rust arm's top total and answer
starting at 0.

## Verification

Every arm prints the same output as `grid.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.44 s (★) to 17 s (game) and the
differential 3.0 s.

The five arms were written in Kāra and checked clean, with no fix; the scan
arm's closures return Kāra's `Some((next_state, item))`.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in two rounds (15 and 3 edits). The first
carries the struct, the `Vec<..>` types, the `&` patterns, the `&Vec`
parameter and the `::` paths, `i64::MAX` among them; the second drops the
`as i64` on each point, since an `i32` widens to `i64` implicitly.

## Benchmarks

The bench builds 200 grids of 2 rows of 50000 points up to 100000 once in
all five languages and runs the ★ arm on each for 10 rounds: 2000 calls,
10^8 points read. Every implementation prints `2000 calls: sum
2456881912290, checksum 122255201`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.338 to 0.373 s | 0.347 s |
| Rust (`rustc -O`) | 0.375 to 0.399 s | 0.384 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.404 to 0.416 s | 0.409 s |
| Kāra (`karac build`) | 0.409 to 0.469 s | 0.416 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.433 to 0.478 s | 0.443 s |
| Go | 0.560 to 0.603 s | 0.579 s |
| Python | 19.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.349 s) is not above its real time (0.416 s).

The sequential Kāra program is 0.92x Rust under overflow checks and 1.18x
C.