# 593. Valid Square

Given the coordinates of four points in 2D space `p1`, `p2`, `p3` and
`p4`, return `true` if the four points construct a square. The
coordinate of a point `pi` is represented as `[xi, yi]`. The input is
not given in any order. A valid square has four equal sides with
positive length and four equal angles (90-degree angles).

```
p1 = [0,0], p2 = [1,1], p3 = [1,0], p4 = [0,1]   ->  true
p1 = [0,0], p2 = [1,1], p3 = [1,0], p4 = [0,12]  ->  false
p1 = [1,0], p2 = [-1,0], p3 = [0,1], p4 = [0,-1] ->  true
```

**Constraints:** `p1.length == p2.length == p3.length == p4.length ==
2`; `-10^4 <= xi, yi <= 10^4`.

## Approaches

Every arm is `fn valid_square(p1: Vec[i64], p2: Vec[i64], p3: Vec[i64],
p4: Vec[i64]) -> bool`. The parameters are bare, so the points are
borrowed, and every arm works in squared lengths, so in integers
throughout.

| file | mechanism |
|---|---|
| `valid_square.kara` ★ | the six squared distances between the points, sorted: the four smallest equal and not 0 (the sides), the two largest equal and twice a side (the diagonals); O(1) |
| `valid_square_set.kara` | the six squared distances in a `Set[i64]`: a square exactly when there are two of them and neither is 0; O(1) |
| `valid_square_orders.kara` | the three ways four points can be joined into a closed path (up to where it starts and which way it goes), each tested for four sides of one length, not 0, each at right angles to the next by a dot product; O(1) |
| `valid_square_turn.kara` | a quarter turn about the points' centre must carry each point onto one of the four, and none may be the centre; the points are scaled by 4 so that the centre is a lattice point; O(1) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 13 lines: the three examples above, nine cases
at the edges (a turned square, the largest square the constraints allow,
a rectangle, a rhombus, a kite, one point four times, two points twice
each, three corners of a square with one of them twice, and three points
in a line with one off it), and a count and checksum over 1,000 random
cases. `valid_square.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which builds the square instead of measuring it: some two of the points,
A and B, are a side, and the other two are the corners that side makes,
B + v and A + v with v the step from A to B turned a quarter. Every
ordered pair is tried, so the square may lie on either side of AB. Each
of 1,000 random cases is a square of random size and turn, the same with
one coordinate moved by 1, four points from -2 to 2, or a parallelogram
on two random sides from -3 to 3 (now and then a rectangle, a rhombus or
a square), in a random order; 246 are squares.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the points in two other orders give the same answer |
| P3 | every point moved by the same amount, up to 10,000 each way, gives the same answer |
| P4 | the plane turned a quarter, or mirrored in the x axis, gives the same answer |
| P5 | the plane scaled by 3 gives the same answer |

It prints `1000 cases (246 squares), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the distances not sorted | P1 246 |
| M2 | ★: sorted largest first | P1 246 |
| M3 | set: three distances allowed | P1 83 |
| M4 | set: only the three distances from `p1` | P1 196, P2 413 |
| M5 | orders: the third path not tried | P1 87, P2 149 |
| M6 | orders: the right angles not tested | P1 38 |
| M7 | turn: a half turn in place of a quarter | P1 251 |
| M8 | turn: a point level with the centre on either axis refused | P1 13 |
| E1 | ★: the diagonals compared with twice the fourth side | 0 |
| E2 | set: at most two distances | 0 |
| E3 | orders: three sides and angles tested, not four | 0 |
| E4 | turn: the quarter turn the other way | 0 |

M1 and M2 call nothing a square, so they fail on exactly the
246 squares. Unsorted, the list compares the distance from `p2` to
`p4` with both `p3`'s to `p4` and twice `p1`'s to `p2`, and no square
meets both; largest first, the two diagonals come before the sides, so
the first four are never equal. The other properties never see either:
"not a square" is the same answer for the moved, turned and scaled
points too. That holds of M3, M6, M7 and M8 as well, each of which
answers by the shape alone: M3 takes any four points with three
distances between them, a rectangle among them; M6 takes rhombi; and
M7 every parallelogram, flat ones included, the shapes a half turn
carries onto themselves; M8 refuses the 13 squares with a corner
directly beside, above or below the centre, and a quarter turn, a
mirror, a move or a scale keeps that so. Only M4 and M5 depend on which
point is which, and P2, the points reordered, sees them more often than
the definition does. P3, P4 and P5 kill nothing here; they are there for
an arm that mixes up the coordinates or overflows, and none of these
does.

E1 is safe because the four smallest are already equal; E2 because four
points of a plane cannot all be the same distance apart; E3 because
three equal sides, each at right angles to the next and the third at
right angles to the closing fourth, can only be a square's: the third
side has to run back along the first, and the fourth then matches the
second; and E4 because a set that a quarter turn carries onto itself is
carried onto itself by three, which is the quarter turn the other way.

## Verification

Every arm prints the same output as `valid_square.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. `karac check`
and `karac __mir-run` at kara `cc6d42d1b4`, the compiled MIR backend at
`555c29b44e`.

The frozen legacy backends refuse every arm, the differential and the
bench program under `karac run --interp`, `karac run` and `karac build`,
at type checking: each passes `p[0]` from a `Vec[Vec[i64]]` to a
borrowing parameter, which legacy reads as a move out of an index
(E_INDEX_MOVE_NON_COPY). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 1,000 random cases once, as
the harness makes them, a third squares, a third squares with one
coordinate moved and a third four points from -3 to 3, and then
20,000 times over tests every one. Every implementation prints
`1000 cases, 20000 rounds: 6540000 squares, checksum 484980180`, the
Kāra program under `karac __mir-run` included (122 s).

Each implementation holds the cases as lists of points and builds the
six distances afresh on every call: a `Vec` sorted with `sort` in Rust,
as the Kāra arm's is; a slice sorted with `slices.Sort` in Go; an array
on the stack sorted by insertion in C; a list `sorted` in Python. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.21 to 0.32 s |
| Rust (`rustc -O`) | 0.52 to 0.73 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.56 to 0.63 s |
| Go | 0.67 to 0.75 s |
| Python | 24.7 to 25.0 s |
| Kāra (`karac build --mir`) | 0.94 to 1.04 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`555c29b44e`. Under `karac __mir-llvm-run` the program prints the same
line in 8.8 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about 1.6 times Rust's. In callgrind profiles of both at
1,000 rounds the Kāra program runs 579 million instructions to Rust's
343 million. `malloc` and `free` cost both about the same, 130 to
140 million, for the six distances' `Vec`. The difference is mostly the
sort: Rust inlines its sort of six numbers into the loop, where the
compiled backend calls `karac_mir_sort_int` in the runtime, 111 million
instructions here, and allocates through `karac_mir_vec_alloc` and
`karac_realloc_or_panic`, 43 million more. That this is where the gap
comes from is read from the profiles; it is not measured by changing the
program.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
