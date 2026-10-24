# 939. Minimum Area Rectangle

You are given an array of points in the **X-Y** plane `points` where
`points[i] = [xi, yi]`.

Return the minimum area of a rectangle formed from these points, with
sides parallel to the X and Y axes. If there is not any such rectangle,
return `0`.

```
points = [[1,1],[1,3],[3,1],[3,3],[2,2]]              ->  4
points = [[1,1],[1,3],[3,1],[3,3],[4,1],[4,3]]        ->  2
```

**Constraints:** `1 <= points.length <= 500`; `points[i].length == 2`;
`0 <= xi, yi <= 4 * 10^4`; all the given points are **unique**.

## Approaches

| file | mechanism |
|---|---|
| `min_area_rect.kara` ★ | every point in a `Set`; any two points that differ in both x and y can be opposite corners, and are when the other two corners are in the set; every pair tried and the least area kept. O(n²) |
| `min_area_rect_columns.kara` | the columns swept from left to right: each two points in a column are a vertical side, and if an earlier column had the same two heights, the latest such column and this one are the sides of the narrowest rectangle with those heights so far; a `Map` keeps, for each pair of heights, the last column that had it. O(n²) |
| `min_area_rect_edges.kara` | every vertical side listed as its two heights and its column and the list sorted, so that sides with the same heights lie next to each other in order of column, and each two neighbours are the sides of the narrowest rectangle between them. O(n² log n) |
| `min_area_rect_sorted.kara` | the points sorted by x and then y, and for each pair with the first to the left of the second and at another height, the other two corners looked up by a binary search written by hand. O(n² log n) |
| `min_area_rect_rows.kara` | the points grouped into rows, each row's x in order; for each two rows, both lists walked together to find the x they share, each two shared x next to each other being the sides of the narrowest rectangle between those rows there. O(r n) for `r` rows |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and six
more (one point, three corners of a square, points on one line, four
points in a diamond, which make no rectangle with sides along the axes,
a rectangle across the whole plane, the largest area there can be, and
a small rectangle inside a larger one); for 300 random sets of 1 to 60
points on grids of 2 to 10 cells a side, the cells 1 to 1,000 apart, the
points, how many sets have a rectangle, the areas and a checksum; and
five of LeetCode's largest, 500 points: a whole grid of 25 by 20, a 100
by 100 grid with cells 400 apart, points anywhere, the same 250 heights
at x = 0 and at x = 40,000, and points on a diagonal.
`min_area_rect.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every four of the points, kept when they are the corners of a
rectangle with sides along the axes, which four distinct points are
exactly when they hold two values of x and two of y. It checks 3,200
random sets of distinct points on grids, so that rectangles are common:
3,000 of up to 8 points on grids of 2 to 4 cells a side, 1 to 3 apart,
against the statement, and 200 of up to 100 points on grids of 2 to 30
cells a side, 1 to 600 apart, against the other properties; 22,071
points, and 1,440 of the sets have a rectangle.

| | property |
|---|---|
| P1 | the statement's least area, on the small sets |
| P2 | 0 exactly when no four points make a rectangle, and otherwise the area of one that some four make |
| P3 | the points moved by a random amount with every x doubled give twice the area |
| P4 | the points with x and y swapped and x mirrored, `[40000 - y, x]`, in reverse order, give the same area |
| P5 | one more point, its x from one point and its y from another where that is new, never gives a larger area, and the corners of a square of side 1 put in somewhere give 1 |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 sets of 22071 points, 1440 with a rectangle, checksum
250802624, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(11 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only one of the other two corners looked up | P1 716, P2 802, P6 802 |
| M2 | ★: the first rectangle kept | P1 245, P4 469, P5 1215, P6 369 |
| M3 | ★: the largest area kept | P1 589, P5 1317, P6 734 |
| M4 | columns: each height one too many | P1 1280, P2 1278, P4 319, P5 3200, P6 1440 |
| M5 | columns: keyed by the lower height only | P1 252, P2 274, P4 558, P5 62, P6 368 |
| M6 | columns: the points never sorted | P1 1224, P2 1364, P4 373, P5 3186, P6 1383 |
| M7 | edges: the first two sides never compared | P1 518, P2 467, P4 318, P5 841, P6 527 |
| M8 | edges: the sides never sorted | P1 948, P2 1066, P4 951, P5 661, P6 1106 |
| M9 | edges: each width from the first side | P1 190, P2 265, P4 444, P5 2144, P6 304 |
| M10 | sorted: any place the search ends counted as found | P1 1212, P2 1317, P4 397, P6 1317 |
| M11 | sorted: the search stepping two past the middle | P1 818, P2 659, P4 721, P5 3075, P6 894 |
| M12 | sorted: each point the corner of one rectangle at most | P1 21, P4 61, P5 1, P6 40 |
| M13 | rows: the lowest row never the first of two | P1 826, P2 808, P4 726, P5 87, P6 848 |
| M14 | rows: the wrong list stepped on | P1 135, P2 149, P4 311, P6 200 |
| M15 | rows: a shared x of 0 before the first | P1 953, P2 1055, P3 1055, P4 1264, P6 1055 |

P1 and P6 kill all fifteen, P4 thirteen, P2 twelve, P5 eleven and P3
one.

P2 misses M2, M3 and M12, which give the area of a rectangle that is
there, only not the least: the first one found, the largest, and the
least among those each point finds first. P2 asks only that the area
be one some four points make.

P3 kills only M15. Every other mistake still builds its answer from
differences of coordinates, a width times a height, even a wrong width
(M9 measures from the first side's column) or a height one too many
(M4, whose width doubles with the rest), so moving the points and
doubling every x doubles its answer as well. M15 measures its first
width from x = 0, which the move changes.

P4 misses M1 and M3. M3 keeps the largest area, which turning the
points does not change. M1 counts a rectangle when the corner with the
first point's x and the second point's y is there; turning the points
and reversing their order makes it look up the image of the same
corner, so it counts the same shapes, three corners or four.

P5 misses M1, M10, M14 and M15. M1 and M10 take shapes with corners
missing for rectangles, and another point only gives them more to choose
from, the square of side 1 among them; why M14 and M15 also never grow
with another point was not worked out.

Fourteen other edits were tried and set aside. Ten failed exactly the
same checks as each other, in four groups, so none of them was kept: ★
and sorted each making every width one too many; columns keeping the
first column with two heights and rows measuring each width from the
first shared x; edges pairing a point with itself as a side, and sorted
letting its search pass an equal key, signing its height, and taking two
points in one column as corners; and edges and rows measuring each
height up from 0. Three were sound but beyond three an arm (★ never
pairing two points next to each other in the list, columns measuring
each width from x = 0, and sorted reading the first height modulo
40,000). One was equivalent: sorted never finding the last point, the
top of the rightmost column, which as the top right corner of a
rectangle is never looked up, since that rectangle is found from its
other diagonal.

## Verification

Every arm prints the same output as `min_area_rect.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.4 to 2.5 s each and the
differential 11 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Legacy refuses all five arms and the bench program at a call with an
indexed `Vec` as its argument, `min_area_rect(examples[i])` and
`min_area_rect(sets[(r + i) % count])`, a move out of an index ("cannot
move ... out of an index"), which v2's borrowing parameters make a
borrow. It refuses the differential where `arm` passes its `ref`
parameter on to an arm ("expected 'Vec[Vec[i64]]', found 'ref
Vec[Vec[i64]]'"), for the same reason. Legacy is frozen, so none of this
is filed.

## Benchmarks

The bench program builds 20 sets of 500 points once, LeetCode's most,
each at random cells of a 40 by 40 grid with its cells 1 to 100 apart;
in each of 10 rounds it runs the ★ arm on every set, each round starting
from a different one, and folds the areas into a checksum. Every
implementation prints `10 rounds over 20 sets of 500 points: areas
adding to 758000, checksum 618319844`. Kāra's `Set` and Rust's
`HashSet` hash with SipHash, Go uses its built-in map, Python its set,
and C a table of 1,024 slots with linear probing and a multiplicative
hash.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.42 to 0.49 s | 0.44 s |
| Rust (`rustc -O`) | 0.49 to 0.58 s | 0.52 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.53 to 0.58 s | 0.55 s |
| Go | 0.49 to 0.53 s | 0.51 s |
| Python | 3.43 s | |
| Kāra (`karac build --mir`) | 0.72 to 0.79 s | 0.75 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 8 times C's: its set is written in
C, and most pairs end at the first lookup.

v2 takes 1.38 times Rust's median time under overflow checks and 1.71
times C's. Under valgrind's cachegrind v2 runs 5.46 billion instructions
and 0.49 billion branches with 28.7 million mispredicted, Rust with
overflow checks 3.65 billion, 0.24 billion and 17.1 million, and C 0.82
billion, 0.18 billion and 33.5 million. C's hash is one multiplication
where v2's and Rust's are SipHash, which would explain most of the
instructions both run beyond it, while C still mispredicts most, on
its probing loop. v2 runs twice Rust's branches, 9.8 million of them
indirect against Rust's 62,000; that these are the set's hashing called
through a function pointer rather than inlined is inferred, not
profiled.
