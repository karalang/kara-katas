# 1037. Valid Boomerang

Given an array `points` where `points[i] = [xi, yi]` represents a point
on the X-Y plane, return `true` if these points are a boomerang.

A boomerang is a set of three points that are all distinct and not in a
straight line.

```
points = [[1,1],[2,3],[3,2]]  ->  true
points = [[1,1],[2,2],[3,3]]  ->  false
```

**Constraints:** `points.length == 3`; `points[i].length == 2`;
`0 <= xi, yi <= 100`.

The Kāra arms take `points` as a `Vec[(i64, i64)]`.

## Approaches

| file | mechanism |
|---|---|
| `boomerang.kara` ★ | the cross product: `(b - a) × (c - a)` is twice the triangle's signed area, zero exactly when the points are on one line or two of them are equal. O(1) |
| `boomerang_slopes.kara` | slopes as reduced fractions: two equal points answer false; otherwise the slopes from a to b and from a to c, each `dy / dx` in lowest terms with `dx` made non-negative, are equal exactly on a line. O(log of the coordinates) |
| `boomerang_shoelace.kara` | the shoelace formula: `x1 (y2 - y3) + x2 (y3 - y1) + x3 (y1 - y2)`, summed over the points in turn with a loop, and its absolute value compared with zero. O(1) |
| `boomerang_heron.kara` | Heron's formula in integers: with `p`, `q`, `r` the squared side lengths, `16 * area^2 = 2 (pq + qr + rp) - (p^2 + q^2 + r^2)`, zero exactly for a flat triangle. O(1) |
| `boomerang_step.kara` | a whole number of steps: the smallest lattice step from a towards b is `(b - a) / gcd`, and c is on the line exactly when `c - a` is a whole number of those steps, the same number along x and along y. O(log of the coordinates) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: the answers for ten triples,
LeetCode's two examples among them, with repeated points, a vertical
line, and near misses across the whole 0 to 100 square; then, for every
ordered triple on a 3 by 3 grid (729) and on a 5 by 5 grid (15625), and
for 3000 random triples, the number of boomerangs and a checksum.
`boomerang.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally for points from 0 to 6: three points are a boomerang
when they are all distinct and no straight line holds all three. A line
through two lattice points of that square is `u x + v y = w` for some
`u` and `v` from -6 to 6, not both zero, so the literal arm tries all
168 of them and asks whether one gives the three points the same `w`.
It checks 7096 cases: every ordered triple of a 4 by 4 grid, repeats
allowed (4096); 2000 random triples from 0 to 6; and 1000 from 0 to
100, a third of the random ones with the third point at the midpoint of
the first two when there is a lattice midpoint. 6096 are inside the
literal arm's square and 4944 are boomerangs.

| | property |
|---|---|
| P1 | the statement read literally, on points from 0 to 6 |
| P2 | the answer is the same in all six orders of the points |
| P3 | moving every point by the same random amount (-100 to 100) |
| P4 | turning the plane a quarter, and mirroring it on its diagonal |
| P5 | scaling every point by the same factor from 2 to 9 |
| P6 | replacing the third point with one of the first two is never a boomerang |
| P7 | each arm agrees with at least two of the other four |

The differential prints `7096 cases (6096 searched in full, 4944
boomerangs): checksum 853256506, 243360 checks over 5 arms: 0 failures`
under `karac __mir-run` (19 s), `karac __mir-llvm-run` and `karac
__mir-llvm-asan` with no error, and the same line under `karac run` and
from a `karac build` binary.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three
to each arm. All fifteen are killed, each fails the same checks under
both backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cross product's two terms added | P1 916, P2 1625, P6 2313, P7 1242 |
| M2 | ★: one coordinate of a mixed up (`cx - ay`) | P1 1391, P2 3466, P3 709, P4 1546, P6 4757, P7 1715 |
| M3 | ★: the two products compared off by one | P1 2220, P2 825, P4 825, P5 401, P6 7096, P7 2553 |
| M4 | slopes: a vertical slope not normalised | P1 40, P2 168, P4 75, P7 40 |
| M5 | slopes: slopes not reduced | P1 432, P2 412, P7 519 |
| M6 | slopes: only `dx` negated | P1 155, P2 676, P4 237, P7 155 |
| M7 | shoelace: the last term dropped | P1 1490, P2 2647, P3 698, P4 1621, P6 4748, P7 1818 |
| M8 | shoelace: a sum where a difference belongs | P1 1626, P3 197, P6 6324, P7 1959 |
| M9 | shoelace: an area of one half called a line | P1 825, P5 825, P7 825 |
| M10 | heron: the factor 2 dropped | P1 1792, P6 6803, P7 2125 |
| M11 | heron: one side counted twice | P1 1018, P2 2557, P6 3481, P7 1105 |
| M12 | heron: one side's `y` part not squared | P1 1669, P2 470, P4 998, P5 273, P6 5795, P7 1997 |
| M13 | step: a fractional number of steps allowed | P1 147, P2 627, P4 292, P5 151, P7 151 |
| M14 | step: a vertical step puts every point on the line | P1 717, P2 2172, P4 1437, P7 723 |
| M15 | step: every vertical step a boomerang | P1 166, P4 312, P7 168 |

P1 and P7 kill all fifteen, P2 eleven, P4 nine, P6 eight, P5 four and
P3 three. P3 sees only the edits that stop being a function of the
differences between the points: a coordinate mixed in (M2), a term
dropped (M7), and a difference turned into a sum (M8). P5 sees four:
the two fixed offsets that scaling moves past (M3's off by one, and
M9's area of one half, which is two at the smallest scale), the
unsquared part that no longer grows as a square (M12), and the
fractional steps that scaling makes whole (M13). P6 misses every
slopes and step edit, since both arms answer a repeated point before
they reach the edited code.

Fifteen other edits were tried and set aside. Six change no answer and
are equivalent: the slopes arm taking its second slope from b instead
of a (two slopes through a shared point are equal exactly when the
three are on a line), and keeping a negative gcd (both parts are
divided by it, and two multiples of one slope get the same sign); the
heron arm calling a value of 1 a line (a lattice triangle's
`16 * area^2` is 0 or at least 4), and measuring sides as `dx^2 - dy^2`
(the expression becomes minus four times the cross product squared,
zero in the same places); and the step arm not catching an equal first
and last point (`c - a` is zero steps, so it is on the line), and
taking the offset from b (`c - b` is a whole number of steps exactly
when `c - a` is). The other nine were killed too, beyond three per arm.
Three fail exactly alike, `P1 4277, P7 4944`, by never seeing a
boomerang: ★ reading the third point as the second, and the shoelace
arm reading the previous point as the next or `y` for `x`. Two fail
alike, `P1 2151, P2 4944, P4 4944, P7 2478`: ★ and the shoelace arm
counting only one winding. Three fail on their own: ★ reading the
first point transposed, the heron arm dropping one product, and the
step arm's gcd taken one off. The slopes arm missing an equal first
and last point stops with `division by zero` under both backends.

## Verification

Every arm prints the same output as `boomerang.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reported
nothing on any arm or the differential. The release build is kara
`6697158faf`, with runtime archives rebuilt at that commit. Under
`karac __mir-run` the arms take 0.21 to 0.24 s.

One gap turned up writing the bench with a Rust habit:
`println!("{} triples, ..", count, ..)`. `karac fix` deletes only the
`!`, which leaves `println("{} triples, ..", count, ..)`, an E0202
"takes 0 or 1 argument(s)" with no fix, where `format!` gets the
f-string rewrite. Filed as kara `B-2026-11-01-8`, with the case it
makes worse: `println!("{n}")` becomes `println("{n}")`, which compiles
and prints the literal `{n}`. The bench's f-string was written by hand.

## Benchmarks

The bench builds 1,000,000 triples once in all five languages, each
its own three-element vector: a third of them three points a step
apart on one line, the rest three random points in the 0 to 100
square. Then it answers all of them 100 times with the ★ arm, counting
the boomerangs and folding each answer into a checksum, a chain of
multiplications modulo `10^9 + 7` that keeps the loop sequential in
every language. C allocates each triple separately too, as the vectors
of vectors do. Every implementation prints `1000000 triples, 100
rounds: 66599500 boomerangs, checksum 596080488`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.644 to 0.706 s | 0.677 s |
| C (`clang -O3`) | 0.694 to 0.730 s | 0.708 s |
| Rust (`rustc -O`) | 0.722 to 0.810 s | 0.756 s |
| Kāra (`karac build`) | 0.733 to 0.920 s | 0.840 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.752 to 1.059 s | 0.872 s |
| Go | 0.834 to 0.937 s | 0.882 s |
| Python | 30.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(0.997 s real, 0.932 s user on one run) and its median is within the
spread of the sequential one.

Kāra took 1.29 times Rust's median time under overflow checks. The
three compiled languages land within 12% of each other because the
modular checksum chain, the same in every language, is most of the
work; the cross product itself is four subtractions and two
multiplications (inferred from the sources, not profiled).
