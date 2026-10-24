# 963. Minimum Area Rectangle II

You are given an array of points in the **X-Y** plane `points` where
`points[i] = [xi, yi]`. Return *the minimum area of any rectangle
formed from these points, with sides **not necessarily parallel** to
the X and Y axes*. If there is not any such rectangle, return `0`.
Answers within `10^-5` of the actual answer will be accepted.

```
points = [[1,2],[2,1],[1,0],[0,1]]                          ->  2.00000
points = [[0,1],[2,1],[1,1],[1,0],[2,0]]                    ->  1.00000
points = [[0,3],[1,2],[3,1],[1,3],[2,1]]                    ->  0
points = [[3,1],[1,1],[0,1],[2,1],[3,3],[3,2],[0,2],[2,3]]  ->  2.00000
```

**Constraints:** `1 <= points.length <= 50`; `points[i].length == 2`;
`0 <= xi, yi <= 4 * 10^4`; all the given points are **unique**.

Every arm finds the area exactly, as an integer: a rectangle's area is
the cross product of the two sides from one corner, and the corners
have integer coordinates. It is returned as an `f64` and printed with
five decimals.

## Approaches

| file | mechanism |
|---|---|
| `min_area_free_rect.kara` ★ | diagonals by centre: four points make a rectangle exactly when they split into two pairs, its diagonals, that share their midpoint and their length. Every pair goes into a `Map` keyed by the sum of its ends and its squared length, and any two pairs under one key are a rectangle. O(n^2) pairs, then the pairs within each key |
| `min_area_free_rect_corners.kara` | right-angled corners: every point a with two others b and c, perpendicular when the dot product of ab and ac is 0, and the fourth corner b + c - a looked up in a `Set` of the points. O(n^3) |
| `min_area_free_rect_sides.kara` | Pythagoras: a right angle at a when the squared lengths satisfy ab^2 + ac^2 = bc^2, and the fourth corner found by binary search in the points sorted by x * 1000000 + y. O(n^3 log n) |
| `min_area_free_rect_sorted.kara` | the same diagonals as ★ without a map: every pair as a tuple of its ends' sum, its squared length and its two points, sorted, so the pairs under one key sit in a run. O(n^2 log n) |
| `min_area_free_rect_quads.kara` | every four points, and each of the three ways to split them into two pairs tested as diagonals. O(n^4) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's four examples and seven
more (one point, a unit square, a square on its corner, a tilted
rectangle with sides of different lengths, the largest square, four
points on a line, and two unit squares side by side); for 300 random
cases of 1 to 10 points from 0 to 4, 1,652 points in all, the total of
the areas and a checksum; and four cases of LeetCode's largest size, 50
points: random from 0 to 40000, a 10 by 5 grid 4000 apart, 50 points
on one circle of radius 1105 (25 and the 25 opposite them, so every two
diameters are the diagonals of a rectangle), and a 7 by 7 grid tilted
by the 3-4-5 triangle with a stray point. `min_area_free_rect.py`
mirrors the ★ arm and its output is byte-identical.

The quads arm reads its four points through borrows,
`let a = ref points[p];`. Written `let a = points[p];` it fails
`karac check` with `E_INDEX_MOVE_NON_COPY`, whose message offers the
borrow first, but `karac fix` applies `.clone()`, a copy of each point
on every one of the O(n^4) calls. That is kara `B-2026-10-24-18`,
filed from another program the same day.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every four points in each of their three cyclic orders, a
rectangle when all four corners are right angles. It checks 3,200
random cases: 3,000 of 1 to 8 points in grids from 0 to at most 5
against the statement, and 200 of 4 to 24 points from 0 to 20000 with
up to three tilted rectangles planted among them (sides (a, b) and
m(-b, a) for small a, b and m) against the other properties; 16,490
points in all. The large cases stop at 24 points so that the O(n^4)
arm keeps the run near half a minute; the arms' own programs cover 50.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | every point moved by the same random offset gives the same area |
| P3 | every point turned a quarter round gives the same area |
| P4 | every coordinate doubled gives four times the area |
| P5 | the points in another order give the same area |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 16490 points: the areas sum to 4852, checksum
10455280, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(27 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-one edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: pairs grouped without their length | P1 608, P5 40, P6 608 |
| M2 | ★: pairs grouped without their x sum | P1 825, P3 1050, P5 585, P6 825 |
| M3 | ★: a pair paired with itself | P1 679, P6 822 |
| M4 | corners: no right angle asked for | P1 615, P5 203, P6 615 |
| M5 | corners: the fourth corner one coordinate off | P1 1247, P3 768, P5 453, P6 1344 |
| M6 | corners: a corner taken as its own neighbour | P1 224, P5 323, P6 355 |
| M7 | sides: a squared length missing a square | P1 207, P3 350, P4 316, P5 176, P6 282 |
| M8 | sides: the fourth corner packed too tightly to look up | P1 301, P2 435, P3 435, P6 444 |
| M9 | sides: the fourth corner never checked | P1 1469, P3 209, P6 1469 |
| M10 | sorted: runs without the length | P1 600, P3 41, P6 600 |
| M11 | sorted: runs without the y sum | P1 250, P3 424, P5 191, P6 252 |
| M12 | sorted: the pairs not sorted | P1 632, P5 140, P6 763 |
| M13 | quads: one split never tried | P1 195, P5 382, P6 338 |
| M14 | quads: no length asked for | P1 596, P6 596 |
| M15 | quads: midpoints compared by x alone | P1 456, P3 598, P5 105, P6 456 |

P1 and P6 kill all fifteen, P5 ten (M1, M2, M4 to M7, M11 to M13, M15),
P3 eight (M2, M5, M7 to M11, M15), and P2 and P4 one each (M8 and M7).
Most wrong answers here are not symmetric under moving, doubling or
reordering, so the statement and the other arms do most of the
killing; M8's packing aliases only once the points move, and M7's
broken length is the only one that does not scale.

Sixteen other edits were tried and set aside. Four failed exactly the
same checks as a kept one, all as M3, by finding a rectangle of area 0
and keeping it: sides taking the hypotenuse from a and searching one
past its target, and sorted pairing a pair with itself and taking the
corner from the second pair. One crashed rather than fail a check:
sorted reading each run one pair too long runs off the end of the pairs.
Eight were sound but beyond three an arm: ★ keeping the largest area
and measuring the length one coordinate off; corners skipping
neighbours next to each other in the list and adding the cross
product's terms; sides putting the fourth corner at b + c + a and not
sorting the points; and quads never pairing the second point with the
next and counting a failed split as area 0.

Three were equivalent. ★ measuring the sides from the other end of the
first diagonal: every corner of a rectangle gives the same area. Sides
never searching the last point: when the target is above every other
key the search still stops on the last place and compares it. And
sorted taking its second side to the opposite corner: the cross product
of a side and a diagonal is twice the triangle they span, which is the
rectangle's area again.

## Verification

Every arm prints the same output as `min_area_free_rect.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `cb8ffcccec`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` ★
and sorted take 0.35 s each, corners 0.59 s, sides 0.95 s and quads
4.4 s, and the differential 30 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 50 cases of 50 points once, LeetCode's largest
count, packed into grids from 8 by 8 to 17 by 17, so that many pairs
share a centre and a length and the groups are large. In each of 40
rounds it runs the ★ arm on every case, each round starting from a
different one, and before each call moves one random point to a random
spot in its grid when that spot is free, so no two calls see the same
points. Every implementation prints `40 rounds over 50 cases of 50
points: the areas sum to 2983.00000, checksum 401791732`. Kāra, Rust,
Go and Python build a hash map of growable lists on every call (Kāra's
and Rust's hash with SipHash); C uses an open-addressing table of 4096
slots on the stack, each holding a key and the head of a linked list of
its pairs, and allocates nothing.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.053 to 0.072 s | 0.058 s |
| Rust (`rustc -O`) | 0.28 to 0.41 s | 0.34 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.30 to 0.40 s | 0.32 s |
| Go | 0.40 to 0.45 s | 0.43 s |
| Python | 1.24 s | |
| Kāra (`karac build --mir`) | 0.33 to 0.48 s | 0.35 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 21 times
C's and 3.6 times Kāra's: the work is mostly hashing and small
allocations, which Python's dict does in C.

v2 takes 1.09 times Rust's median time under overflow checks and 5.9
times C's. Under valgrind's cachegrind v2 runs 4.21 billion
instructions and 0.54 billion branches with 7.3 million mispredicted,
Rust with overflow checks 2.77 billion, 0.28 billion and 6.7 million,
and C 0.22 billion, 59 million and 4.0 million. The gap to C is most
likely the map: a hash of three integers with a few multiplications
against SipHash, and a table on the stack against a growable list per
key.
