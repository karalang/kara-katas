# 2249. Count Lattice Points Inside a Circle

Given a 2D integer array `circles` where `circles[i] = [x_i, y_i, r_i]`
represents the center `(x_i, y_i)` and radius `r_i` of the `i`th circle
drawn on a grid, return *the **number of lattice points** that are
present inside **at least one** circle*.

**Note:** a **lattice point** is a point with integer coordinates, and
points that lie **on the circumference of a circle** are also
considered to be inside it.

```
circles = [[2,2,1]]          ->  5
circles = [[2,2,2],[3,4,1]]  ->  16
```

**Constraints:** `1 <= circles.length <= 200`; `circles[i].length ==
3`; `1 <= x_i, y_i <= 100`; `1 <= r_i <= min(x_i, y_i)`.

A point `(px, py)` is in a circle exactly when `(px - x)^2 + (py - y)^2
<= r^2`, all in integers, so the border counts with no rounding. Every
circle lies in the square from `(0, 0)` to `(200, 200)`, so the points
of the box bounding all the circles can simply be tried.
O(box * circles).

## Approaches

| file | mechanism |
|---|---|
| `lattice.kara` ★ | the box bounding all the circles, from `min` and `max` of their edges; every point of it tried against the circles until one holds it |
| `lattice_set.kara` | each circle's own points, from its square of side `2r + 1`, put in a `Set[(i64, i64)]`, which keeps each point once however many circles hold it |
| `lattice_rows.kara` | row by row: on row `py` a circle holds the run of `x` from `x - w` to `x + w`, `w` the integer square root of `r^2 - (py - y)^2`; each row's runs sorted and merged; no point tested on its own |
| `lattice_struct.kara` | a `#[derive(Copy, Clone)] struct Circle` with `contains` (`ref self`), and a `struct Board` of 201 * 201 marks and their count: `cover` (`mut ref self`) marks a circle's points, counting the new ones, and `marked` (`ref self`) |
| `lattice_iter.kara` | iterator chains: the bounding box by `map`, `min` and `max`, its points by `flat_map`, kept by `filter` when `any` circle holds them, and `count`ed |
| `lattice_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in, `i32` out, the points from `(0, 0)` to the largest `x + r` and `y + r` by `0..=max_x` and `0..=max_y`, each counted when `circles.iter().any(..)` holds it; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and four
more (the smallest circle, one circle twice, one inside another, and
the largest beside the smallest), each with its answer; then the total
over 2000 cases of 1 to 6 circles with centres from 1 to 12, with a
checksum of the answers; then the constraints' largest, 200 circles
anywhere, and 200 copies of the largest circle. `lattice.py` mirrors
the ★ arm and its output is byte-identical.

The ★ arm first tried every point from `(0, 0)` to `(200, 200)` for
every case, as the bound in the statement allows; under `karac
__mir-run` that took 106 s, nearly all of it on the 2000 small cases, so
it tries only the box the circles span.

`karac fix` carries the template in one round of 13 edits: `Vec<..>` to
`Vec[..]`, `struct Solution;` to `struct Solution {}`, `Solution::` to
`Solution.`, the `&` pattern dropped from the adapter's closure, and its
`as i64` removed as lossless. `0..=max_x` is Kāra as it stands.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every lattice point from `(0, 0)` to `(30, 30)` tried, and
counted when its distance from some centre, a square root in floating
point, is at most that circle's radius; no integer squares. It checks
300 random cases of 1 to 5 circles with centres from 1 to 8; then 30 of
one circle many times; then 30 of rings about `(8, 8)`. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the count, read literally |
| P2 | the circles in reverse order: the same answer |
| P3 | every circle's `x` and `y` swapped: the same answer |
| P4 | every circle moved by `(3, 5)`: the same answer |
| P5 | a circle added: at least the old count, and at most the old count plus the new circle's own |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 816486840, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
gathers each circle's points column by column with `math.isqrt` into
one set of tuples. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the box one short on the right | P1 360, P3 46, P5 86, P6 360 |
| M4 | ★: the box's bottom from the highest circle | P1 250, P3 219, P5 44, P6 250 |
| M5 | ★: `dy` measured from the centre's `x` | P1 301, P3 198, P4 313, P5 120, P6 301 |
| M8 | set: the square one short on the right | P1 360, P3 98, P6 360 |
| M9 | set: a point kept by its `x` twice | P1 360, P3 173, P6 360 |
| M11 | set: only the first circle | P1 249, P2 186, P6 249 |
| M12 | rows: the root one too large | P1 360, P3 232, P4 193, P6 360 |
| M13 | rows: the runs not sorted | P1 193, P2 222, P3 198, P6 193 |
| M16 | rows: the room `r^2 - abs(dy)` | P1 292, P3 232, P4 259, P6 292 |
| M19 | struct: the mark set at the diagonal | P1 299, P2 123, P3 119, P4 257, P6 299 |
| M20 | struct: every circle's `y` read as its `x` | P1 190, P3 196, P6 190 |
| M21 | struct: the square from the centre rightwards only | P1 360, P3 154, P6 360 |
| M23 | iter: inside every circle | P1 260, P5 146, P6 260 |
| M25 | iter: the box's top from the lowest circle | P1 257, P3 217, P5 87, P6 257 |
| M26 | iter: `dy` squared as `dx` times `dy` | P1 360, P3 190, P4 274, P5 94, P6 360 |
| M28 | solution: the top read from `x` | P1 131, P3 269, P4 258, P5 98, P6 131 |
| M29 | solution: the scan begun at `x = 1` | P1 193, P3 180, P4 193, P6 193 |

P1 and P6 kill all seventeen, P3 fifteen, P4 and P5 seven each, and P2
three. P3 swaps `x` and `y`, which hands every edit that treats the two
axes differently a different count; it misses only the edits that are
symmetric in them (M11, M23). P4 moves every circle away from the
axes, and catches the edits whose error depends on where the circle is,
such as `dy` read from `x` or a scan begun at 1. P2 reverses the
circles, and catches only the edits that read them in order: the first
circle only (M11), unsorted runs (M13) and marks that collide (M19).

Of the thirty-one, fourteen were not kept, and none survives, crashes
or differs between the backends. One fails as a kept one does: the iter
arm's box one short on the right (M24) as the ★ arm's (M2). Six fail
alike in a group of their own, wrong on every case: the border left out
in the ★, set, struct, iter and template arms, and the set arm's radii
one less (M1, M7, M17, M22, M27, M10). Four more fail alike: the ★ arm's
point counted for every circle, the rows arm's start not clipped and
end never advanced, and the struct arm's point counted again (M3, M14,
M15, M18), all counting an overlap twice. Two are a pair: the radius
doubled, not squared, in the ★ arm and the template (M6, M31). One fails
its own way and is left out for the count of two: the template's top
row dropped (M30).

## Verification

Every arm prints the same output as `lattice.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the rows arm takes 1.3 s, the ★ arm 1.9 s, the
iter arm and the template 4.6 s, the struct and set arms 5.0 s, and the
differential 5.8 s.

## Benchmarks

The bench answers 100 cases of 200 circles with the ★ arm in all five
languages, centres from 1 to 100 and radii up to the nearer axis, so the
box spans most of the 201 * 201 square. Every implementation prints
`100 cases of 200 circles: checksum 665083456`.

BENCHTAB
