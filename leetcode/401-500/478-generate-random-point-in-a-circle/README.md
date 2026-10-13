# 478. Generate Random Point in a Circle

Given the radius and the position of the center of a circle, implement
the function `randPoint` which generates a uniform random point inside
the circle.

Implement the `Solution` class:

- `Solution(double radius, double x_center, double y_center)`
  initializes the object with the radius of the circle `radius` and the
  position of the center `(x_center, y_center)`.
- `randPoint()` returns a random point inside the circle. A point on
  the circumference of the circle is considered to be in the circle.
  The answer is returned as an array `[x, y]`.

```
Solution(1.0, 0.0, 0.0); randPoint(); randPoint(); randPoint()
    ->  e.g. [-0.02493, -0.38077], [0.82314, 0.38945], [0.36572, 0.17248]
```

**Constraints:** `0 < radius <= 10^8`; `-10^7 <= x_center, y_center <=
10^7`; at most `3 * 10^4` calls are made to `randPoint`.

## Approaches

Every arm is a `Solution` with `fn new(radius: f64, x_center: f64,
y_center: f64, seed: i64) -> Solution` and `fn rand_point(mut ref self)
-> (f64, f64)`. The problem allows the language's own random numbers;
the arms draw from a seeded generator of their own (`Uniform`, a linear
congruential generator giving 30 random bits as a float in `[0, 1)`),
so that every run, and the Python mirror, draws the same values.

| file | mechanism | draws per point |
|---|---|---|
| `random_point.kara` ★ | a point uniform in the square around the circle, kept if it lands inside, else drawn again | 2 × 4/π ≈ 2.55 |
| `random_point_polar.kara` | the distance from the centre is `R × sqrt(u)`, the inverse of its distribution (within `d` of the centre with chance `(d/R)²`), and the angle is uniform | 2 |
| `random_point_larger.kara` | the distance is `R` times the larger of two uniform draws, which is at most `d` with chance `d²` as it should be; no square root | 3 |
| `random_point_folded.kara` | the distance is `R` times the sum of two uniform draws, folded back (`s` becomes `2 - s`) when it passes 1: the triangle the sum has for its density, folded in half, is the density `2d` the distance needs | 3 |
| `differential.kara` | each arm held to five properties |

The arms draw differently, so the same seed gives each of them
different points, and the harness prints only what every correct arm
must make true. Every arm prints the same 6 lines: for five circles
(the LeetCode example; radius 10 at `(5, -7.5)`; radius 0.01 at
`(-73839, 9500000)`, where the centre is a billion times the radius;
radius `10^8` at `(10^7, -10^7)`, the largest of both; radius 0.5 at
`(0.25, 0.25)`) and 100,000 points each, whether every point is in the
circle, and whether, in units of the radius, the four quadrants, eight
equal sectors, ten rings of equal area, and the 80 cells of rings by
sectors each got their share within 4 standard deviations (5 for the
80 cells), and whether the mean point is within 4 standard deviations
of the centre; and whether one seed twice draws the same 1,000 points,
and another seed other ones. All of them read `true`.
`random_point.py` mirrors the ★ arm and draws the same points.

Its output differs from the Kāra arms' in four lines, all for the same
reason: Kāra prints the whole-number floats `1.0`, `0.0`, `10.0`,
`5.0`, `-73839.0`, `9500000.0`, `100000000.0`, `10000000.0` and
`-10000000.0` as `1`, `0`, `10` and so on, where the v1 spec
(`docs/library/core-types.md` § Printing in the kara repo) says a float
always prints with a `.` or an exponent, as Python does. That is
B-2026-10-13-9, below. Everything else is byte-identical, every
`true` included.

## Differential

`differential.kara` holds copies of the four arms. Each is held to the
properties below on its own: 1,500 random circles (radius from 10^-6 to
10^8, centre within 10^7 of the origin) with 10 points each for P1 to
P3, and ten seeded runs of 20,000 points in the unit disk for P4 and P5.

| | property |
|---|---|
| P1 | every point is in the circle |
| P2 | the same seed with the centre moved by `(dx, dy)` gives the same points moved by `(dx, dy)` |
| P3 | the same seed with the radius k times as large (k from 2 to 9), centred on the origin, gives the points k times as far out |
| P4 | ten rings of equal area each get their share of the points, within 5 standard deviations |
| P5 | so do 16 cells: eight sectors by angle, each cut where half its area is |

P1 to P3 allow `10^-9 × radius + 10^-15 × (|x| + |y|)` for rounding: a
few units in the last place of the centre's coordinates, which is what
a point there can be known to. P4 and P5 use 5 standard deviations
because they check 1,040 counts in all.

It prints `1500 circles and 10 runs, 4 arms, 19040 checks, 0 failures`
under `karac __mir-run`, in 10 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a dart anywhere in the square is kept | P1 1387, P4 100, P5 160 |
| M2 | ★: y is drawn from `[0, 1)`, not `[-1, 1)` | P5 160 |
| M3 | polar: the distance is `R × u`, no square root | P4 90, P5 160 |
| M4 | polar: the angle covers half a turn | P5 160 |
| M5 | larger: the smaller of the two draws | P4 90, P5 160 |
| M6 | larger: the angle reuses the first draw | P5 142 |
| M7 | folded: the sum is halved, not folded | P4 90, P5 125 |
| M8 | folded: y is measured from the centre's x | P1 1360, P2 1500 |

Under M1 about one point in five lands in a corner outside the circle,
so a circle's 10 points all land inside anyway about one time in eleven
(113 of the 1,500 circles here). M2 and M4 cover half the disk evenly,
so the rings still get their shares and only the sectors see it. M6 is
the subtle one: the distance and the angle are each right on their own,
but a large angle comes with a large distance, so only the 16 cells,
which look at both at once, catch it. M8 is invisible wherever the
centre's x and y are equal, which P3's origin-centred circles always
are; no mutant here handles the radius wrongly, so P3 kills none of
them.

## Verification

All four arms print the same output under `karac __mir-run` (the v2
MIR interpreter) and `karac __mir-llvm-run`, and `karac check` passes
on every file, the bench program included. The differential prints
`19040 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The Python mirror
matches apart from the float printing of B-2026-10-13-9.

The frozen legacy backends agree too: `karac run --interp`, LLJIT,
legacy `karac build` and a `KARAC_AUTO_PAR=1` build all print the same
output on every arm (whole floats without `.0` included), and the
differential prints `0 failures` on the legacy interpreter and a legacy
build.

## Benchmarks

The bench program uses the ★ arm: 20,000,000 points from the circle
of radius 10,000 centred at `(20000, 30000)`, so that every coordinate
is positive and truncating it to an integer means the same in every
language. Every implementation prints `20000000 points: 9998473 right
of the centre, checksum 787840211`, the Kāra program under
`karac __mir-run` included (in 154 s). The checksum folds in each
coordinate times 1,000, truncated; it matches across all five
languages because every mirror does the same float operations in the
same order on the same 30-bit draws.

Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.56 to 0.61 s |
| Rust (`rustc -O`) | 0.26 to 0.30 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.39 to 0.47 s |
| Go | 0.54 to 0.60 s |
| Python | 36.3 to 37.4 s |
| Kāra (`karac build`) | 0.75 to 0.79 s |
| Kāra (`karac build --mir`) | 0.72 to 0.75 s |

C is twice as slow as Rust here, which was not looked into. The legacy
`karac build` builds and runs this program correctly, so `bench.sh` is
the `scripts/new-bench.sh` output unchanged and times that build. The
`--mir` row is the v2 compiled backend, timed for comparison. Both Kāra
rows are timed at kara `b0b1557b39`. Under `karac __mir-llvm-run` the
program prints the same line in 2.7 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-9** (open): a whole-number `f64` prints without
  `.0` on every backend (`println(1.0)` prints `1`), and no float ever
  prints in exponent form (`1e16` prints `10000000000000000`), where
  `docs/library/core-types.md` § Printing says `1.0` and `1e+16`. The
  MIR interpreter, the MIR compiled backend and the frozen legacy
  interpreter all agree, so no run/build comparison sees it; the
  Python mirror does, in the four circle lines.
