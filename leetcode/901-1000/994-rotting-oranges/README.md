# 994. Rotting Oranges

You are given an `m x n` `grid` where each cell can have one of three
values:

- `0` representing an empty cell,
- `1` representing a fresh orange, or
- `2` representing a rotten orange.

Every minute, any fresh orange that is **4-directionally adjacent** to
a rotten orange becomes rotten.

Return *the minimum number of minutes that must elapse until no cell
has a fresh orange*. If *this is impossible, return* `-1`.

```
grid = [[2,1,1],[1,1,0],[0,1,1]]  ->  4
grid = [[2,1,1],[0,1,1],[1,0,1]]  ->  -1   (the bottom left orange never rots)
grid = [[0,2]]                    ->  0    (no fresh orange at minute 0)
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`1 <= m, n <= 10`; `grid[i][j]` is `0`, `1`, or `2`.

## Approaches

The minute an orange rots is its distance, in steps between oranges,
from the nearest rotten one, and the answer is the largest such
distance. Two arms find the distances by a breadth-first search from
all the rotten oranges at once; three let the minutes settle by
repeated passes or by walking on wherever the rot can arrive sooner.

| file | mechanism |
|---|---|
| `oranges_rotting.kara` ★ | breadth-first from every rotten orange at once: they all go into one `VecDeque` at minute 0, each orange taken off rots its fresh neighbours a minute later and queues them, and the last minute taken off is the answer, unless a fresh orange is left. O(mn) |
| `oranges_rotting_levels.kara` | a frontier a minute at a time: the oranges that rotted last minute form a list, and the next list is their fresh neighbours; a minute that rots nothing while fresh oranges are left means they never rot. O(mn) |
| `oranges_rotting_scan.kara` | the whole grid scanned each minute: a pass rots every fresh orange next to one that had rotted by the minute before, stamping each with the minute it rots so it cannot pass the rot on in the same pass; the first pass that rots nothing ends it. O((mn)²) |
| `oranges_rotting_relax.kara` | minutes relaxed to a fixed point, as Bellman-Ford does: each fresh orange starts at "never" and each rotten one at 0, and passes lower each fresh orange to one more than its lowest neighbour until nothing changes. O((mn)²) |
| `oranges_rotting_dfs.kara` | depth-first stamps: a recursive walk from each rotten orange stamps every orange it reaches with the minute the rot gets there, and walks on only where that minute is earlier than the stamp already there. O((mn)²) at worst |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines. The first ten are LeetCode's three
examples and seven more: an empty cell alone, a fresh orange alone,
and a rotten one alone; two rotten oranges meeting in the middle; a
row with two rotten oranges and fresh ones on both sides of each; a
column rotting downwards; and two fresh oranges walled off from the
rotten one. Then five grids of LeetCode's largest size, 10 by 10: all
fresh but a rotten corner, 18 minutes; all fresh but a rotten cell
near the middle; all fresh, which never rots; a winding path of 55
oranges, rotting from one end in 54 minutes; and a checkerboard, whose
oranges touch only at corners. Then totals over random grids: 300 of
up to 3 by 3 and 3,000 of up to 10 by 10, with a cell empty 2 times in
16 and rotten 1 time in 16. `oranges_rotting.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: minute after minute, every fresh orange next to an
orange that was rotten when the minute began, read from a copy of the
grid, turns rotten; when a minute changes nothing the answer is the
minutes gone by, or -1 if a fresh orange is left. It checks 3,200
random grids: 3,000 of up to 5 by 5, a cell rotten 2 times in 16,
against the statement, and 200 of up to 10 by 10, rotten 1 time in 16
and empty 2 and 5 times in 16 in turn, against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 grids |
| P2 | the grid transposed gives the same answer |
| P3 | the grid turned upside down gives the same answer |
| P4 | one random cell made a rotten orange cannot make the answer later, with -1 counted as the latest |
| P5 | -1 exactly when a fresh orange has no path of oranges to a rotten one, found by a flood fill; otherwise at most the number of fresh oranges, and 0 exactly when there are none |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 grids of 33256 cells: 1412 never rot, 5798 minutes,
checksum 972649387, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` (7.1 s) and `karac __mir-llvm-run`, and the same
under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-eight edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a rotted orange not counted off | P1 1637, P5 1722, P6 1722 |
| M2 | ★: the answer a minute late | P1 1683, P4 19, P5 263, P6 1769 |
| M3 | ★: the rot never spreads upwards | P1 1012, P2 893, P3 944, P5 959, P6 1084 |
| M4 | levels: a minute that rots nothing ends with the minutes so far | P1 1298, P4 1071, P5 1412, P6 1412 |
| M5 | levels: stops with one fresh orange left | P1 1329, P5 364, P6 1408 |
| M6 | levels: fresh oranges start in the frontier | P1 2935, P5 3134, P6 3134 |
| M7 | scan: an orange rotted this pass not stamped | P1 984, P3 1075, P6 1049 |
| M8 | scan: a fresh neighbour passes the rot on | P1 2223, P3 598, P5 974, P6 2361 |
| M9 | scan: the answer a minute late | P1 1702, P5 282, P6 1788 |
| M10 | relax: "never" left as the answer | P1 1298, P5 1412, P6 1412 |
| M11 | relax: rotten oranges start at minute 1 | P1 1637, P5 216, P6 1722 |
| M12 | relax: a single pass | P1 1041, P3 603, P5 1072, P6 1118 |
| M13 | dfs: the rot two minutes going up | P1 510, P2 849, P3 947, P5 59, P6 561 |
| M14 | dfs: empty cells walked through | P1 465, P4 3, P5 256, P6 555 |
| M15 | dfs: the answer a minute early | P1 1702, P4 38, P5 230, P6 1788 |

P1 and P6 kill all fifteen, P5 fourteen, P3 five, P4 four and P2 two.
P5 misses only M7, whose answers come out early but still between 0
and the number of fresh oranges, and -1 just when they should. A
transposed grid trades up for left and down for right, so P2 sees only
the arms that treat one direction differently from the others: M3 and
M13. M7, M8 and M12 depend instead on the order of a pass, top to
bottom and left to right: what a cell sees of its upper and left
neighbours has already changed in the pass, and of its lower and right
ones has not. Transposing swaps up with left and down with right,
which leaves that split as it was; turning the grid upside down does
not, and P3 kills all three. M4 and M10 fail the same 1,298 small
grids, both answering a grid that never finishes rotting with
something other than -1: M4 with the minutes until the rot stopped,
M10 with relax's "never", 1,000,000. P4 ranks -1 as 1,000,000 too, so
it sees M4, whose minutes can grow when a new rotten orange lets the
rot finish, and cannot tell M10's answer from the right one.

Thirteen other edits were tried and set aside. Six failed exactly the
same checks as a kept one: levels not counting a rotted orange off,
scan passing the rot on only from the minute before last, so that
nothing ever rots, and relax not adding one to a neighbour's minute,
which answers 0 wherever the right answer is a positive number, all as
M1; scan not checking for fresh oranges left, as M4; scan never
spreading down, as M3; and scan passing the rot on from oranges rotted
in the same pass, as M7. Four were sound but beyond three an arm: ★
letting one fresh orange through, levels never spreading left, relax
relaxing empty cells too, and scan taking a diagonal neighbour in
place of the right one. Two survived and are equivalent: ★ keeping the
largest minute rather than the last one, which is the same, since
oranges leave the queue in the order they rot; and dfs walking on over
a stamp equal to its own, which walks a path again and stamps it the
same way.

One crashed, the same way in both lanes: dfs walking on only where the
stamp is later restamps two neighbouring oranges back and forth, each
later than the last, until `fatal runtime error: stack overflow`.

## Verification

Every arm prints the same output as `oranges_rotting.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 0.96 s (levels) to 2.6 s
(relax, which passes over the grid until nothing changes), and the
differential 7.1 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
random grids of LeetCode's largest size, 10 by 10, once, each cell
empty 3 times in 32 and rotten 1 time in 32; five of the twenty never
finish rotting. In each of 20,000 rounds it runs the arm on every
grid, each round starting from a different one, and folds every answer
into a checksum. Every implementation prints `20000 rounds over 20
grids of 10 by 10: 100000 never rot, 3320000 minutes, checksum
857381118`. Each call copies the grid, row by row, and runs the search
with a fresh queue; C's queue is an array that grows with `realloc`
and is read from a moving head, as Go's slice is.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.251 to 0.338 s | 0.294 s |
| Rust (`rustc -O`) | 0.362 to 0.454 s | 0.390 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.377 to 0.481 s | 0.406 s |
| Go | 1.806 to 2.248 s | 1.883 s |
| Python | 23.8 s | |
| Kāra (`karac build --mir`) | 0.464 to 0.842 s | 0.532 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 45 times
Kāra's.

v2 took 1.31 times Rust's median time under overflow checks and 1.81
times C's, and its runs spread the widest. Under valgrind's cachegrind
v2 ran 6,300 million instructions and 1,299 million branches with 94.2
million mispredicted, Rust with overflow checks 5,305 million, 1,130
million and 53.5 million, and C 3,343 million, 738 million and 53.8
million. Split by function, the allocator is not the difference: v2
spends 786 million instructions in glibc's `malloc.c` and Rust 930
million. Of v2's misses 90.0 million are in its own compiled code,
against Rust's 48.3 million in its `main`, about 104 more for each of
the 400,000 calls, or one for each cell of the grid; which branch that
is was not traced.
