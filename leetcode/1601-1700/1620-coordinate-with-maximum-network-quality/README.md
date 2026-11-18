# 1620. Coordinate With Maximum Network Quality

You are given an array of network towers `towers`, where
`towers[i] = [xi, yi, qi]` denotes the `ith` network tower with location
`(xi, yi)` and quality factor `qi`. All the coordinates are **integral
coordinates** on the X-Y plane, and the distance between the two
coordinates is the **Euclidean distance**.

You are also given an integer `radius` where a tower is **reachable** if
the distance is **less than or equal to** `radius`. Outside that
distance, the signal becomes garbled, and the tower is **not reachable**.

The signal quality of the `ith` tower at a coordinate `(x, y)` is
calculated with the formula `⌊qi / (1 + d)⌋`, where `d` is the distance
between the tower and the coordinate. The **network quality** at a
coordinate is the sum of the signal qualities from all the
**reachable** towers.

Return *the array* `[cx, cy]` *representing the **integral** coordinate*
`(cx, cy)` *where the **network quality** is maximum. If there are
multiple coordinates with the same **network quality**, return the
lexicographically minimum **non-negative** coordinate.*

**Note:** A coordinate `(x1, y1)` is lexicographically smaller than
`(x2, y2)` if either `x1 < x2`, or `x1 == x2` and `y1 < y2`. `⌊val⌋` is
the greatest integer less than or equal to `val` (the floor function).

```
towers = [[1,2,5],[2,1,7],[3,1,9]],  radius = 2  ->  [2,1]
towers = [[23,11,21]],               radius = 9  ->  [23,11]
towers = [[1,2,13],[2,1,7],[0,1,9]], radius = 2  ->  [1,2]
```

**Constraints:** `1 <= towers.length <= 50`; `towers[i].length == 3`;
`0 <= xi, yi, qi <= 50`; `1 <= radius <= 50`.

## Approaches

| file | mechanism |
|---|---|
| `network.kara` ★ | every point of the 51 x 51 square, x then y, its quality summed over the towers in reach with `f64` distances; a strictly larger sum replaces the best, so the first best is the least. O(51^2 t) |
| `network_exact.kara` | no square roots: a tower is in reach when `d2 <= radius^2`, and its signal `floor(q / (1 + sqrt(d2)))` is the largest `k <= q` with `k^2 * d2 <= (q - k)^2`, counted down from `q`. O(51^2 t q) |
| `network_scatter.kara` | turned round: each tower adds its signal to a 51 x 51 grid over its bounding square only, then one pass keeps the first largest. O(t r^2 + 51^2) |
| `network_solution.kara` | LeetCode's Rust template (`for x in 0..=50`, `for t in &towers`, `vec![x, y]`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and two
more (towers too weak to reach past their own point, and towers of
strength 0, whose answer is the origin), then the cases answered at the
origin and a checksum of every answer for 3000 random cases of up to 4
towers in an 8 x 8 corner, 300 of up to 20 anywhere, and 30 of up to 50.
`network.py` mirrors the ★ arm and its output is byte-identical.

The square's distances are irrational except where `d2` is a perfect
square, so `floor` on an `f64` quotient is exact for every `q <= 50`:
the exact arm agrees with the three `f64` arms on every case.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every integral point of the square with its network quality,
sorted by quality descending, then x, then y, and the first taken. It
checks 100 cases of 1 to 6 towers in a square of side 1 to 51, radius 1
to 12. Three cases in four are built to sit on an edge, since random
towers almost never decide an answer there: two towers exactly `radius`
apart whose points tie only when each reaches the other, two just out of
each other's reach at offset `(radius, 1)` whose points would tie if
each did, and one tower on the square's last column. Every random choice
is drawn before any arm answers. The interpreter takes about 20 s for
the 100.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the towers listed backwards leave the answer |
| P3 | one more tower of strength 0 leaves the answer |
| P4 | no tower's own point has a better quality than the answer |
| P5 | every tower written twice leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `100 problems: checksum 449783100, 2400 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. On wholly random towers, M5, M6 and M7
were not: a point just past the radius, the last column, or the edge of
a tower's reach almost never decides the answer. The built cases kill
each of them in about one case in four.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a later point of equal quality replaces the best | P1 27, P2 27, P3 27, P5 27, P6 27 |
| M2 | ★: a tower exactly `radius` away out of reach | P1 26, P2 26, P3 26, P4 1, P5 26, P6 26 |
| M3 | ★: the signal rounded, not floored | P1 37, P2 37, P3 37, P4 10, P5 37, P6 37 |
| M4 | exact: `k * d2` compared, not `k^2 * d2` | P1 8, P2 8, P3 8, P4 2, P5 8, P6 8 |
| M5 | exact: `radius^2 + 1` in reach | P1 26, P2 26, P3 26, P4 26, P5 26, P6 26 |
| M6 | exact: the last column left out | P1 26, P2 26, P3 26, P4 26, P5 26, P6 26 |
| M7 | scatter: each tower's last column of reach left out | P1 27, P2 27, P3 27, P4 27, P5 27, P6 27 |
| M8 | scatter: a later point of equal quality replaces the best | P1 27, P2 27, P3 27, P5 27, P6 27 |
| M9 | template: the y distance measured from x | P1 100, P2 100, P3 100, P4 100, P5 100, P6 100 |
| M10 | template: the best quality kept one too high | P1 24, P2 24, P3 24, P4 24, P6 24 |

## Benchmarks

The bench makes 1000 random cases of 50 towers anywhere in the square
with a radius of 1 to 50, all of it first. Then each one's best
coordinate by the ★ arm, 2601 points against 50 towers, in all five
languages. Every implementation prints `1000 cases of 50 towers:
coordinates sum to 49285, checksum 712054062`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9691a6290e` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.461 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.498 s |
| Go | 0.499 s |
| Kāra (`karac build`) | 0.509 s |
| Rust (`rustc -O`) | 0.660 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.696 s |
| Python | 19 s |

Kāra is level with C and Go and ahead of both Rust builds. The work is
a square root and a division per point and tower, the same in every
language, and Rust reads `towers` as a `Vec<Vec<i32>>` with a bounds
check per field, as Kāra does; why Rust is a third slower here was not
looked into.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (0.389 s and 0.394 s on one run).

## Verification

All four arms print the same output as `network.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`9691a6290e`, and again at `eb32a1ff0` after the ★ arm was restored to
its natural form.

## Writing it

The ★ arm was first written with `for x in 0..=50` and `best = [x, y]`
returned as a `Vec[i32]`. Kāra does not let an operator fix a literal's
type (design.md §8), so `t[0] - x` beside an `i32` leaves the range's
literals at the default `i64`, and `best.to_vec()` was refused as a
`Vec[i64]`, at first with no machine fix (B-2026-11-18-52). Since kara
c52d43047e, `karac fix` carries it in three edits: `[0, 0]` to
`[0i32, 0]`, then both ranges to `0i32..=50`, and the arm is what it
left. The exact arm's `best` is annotated `Vec[i32]`; the scatter arm
works in `i64` and narrows the answer once.

LeetCode's Rust template met the same rule: `ans = vec![x, y]` into a
`Vec<i32>` with `x` from `0..=50`, refused as an `i64` element with only
"write an explicit 'as i32'" offered. Kara 9691a6290e makes `karac fix`
suffix the range's first literal, `0i32..=50`, when a binding a range of
literals feeds is narrowed (B-2026-11-18-51). The template then takes one
`karac fix` of 14 edits: `struct Solution;` to `struct Solution {}`, the
`<..>` types to `[..]`, `vec![0, 0]` to `[0i32, 0]`, both ranges to
`0i32..=50`, `for t in &towers` to `for t in ref towers`, `vec![x, y]` to
`[x, y]`, `Solution::` to `Solution.`, and the harness's redundant
`as i64`, which every arm's harness lost the same way. It then checks and agrees with
no hand edit.
