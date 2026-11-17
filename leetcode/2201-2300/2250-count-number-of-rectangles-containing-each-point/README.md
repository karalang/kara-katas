# 2250. Count Number of Rectangles Containing Each Point

You are given a 2D integer array `rectangles` where `rectangles[i] =
[l_i, h_i]` indicates that the `i`th rectangle has a length of `l_i` and
a height of `h_i`. You are also given a 2D integer array `points` where
`points[j] = [x_j, y_j]` is a point with coordinates `(x_j, y_j)`.

The `i`th rectangle has its **bottom-left corner** at `(0, 0)` and its
**top-right corner** at `(l_i, h_i)`. Return *an integer array `count`
of length `points.length` where `count[j]` is the number of rectangles
that **contain** the `j`th point*. The `i`th rectangle contains the
`j`th point if `0 <= x_j <= l_i` and `0 <= y_j <= h_i`; points on the
**edges** of a rectangle are also contained.

```
rectangles = [[1,2],[2,3],[2,5]], points = [[2,1],[1,4]]  ->  [2,1]
rectangles = [[1,1],[2,2],[3,3]], points = [[1,3],[1,1]]  ->  [1,3]
```

**Constraints:** `1 <= rectangles.length, points.length <= 5 * 10^4`;
`rectangles[i].length == points[j].length == 2`; `1 <= l_i, x_j <=
10^9`; `1 <= h_i, y_j <= 100`; all the `rectangles` are unique, and all
the `points` are unique.

Heights are at most 100 while lengths reach 10^9, so the rectangles are
grouped by height and each group's lengths sorted: a point `(x, y)`
counts, in each group from height `y` to 100, the lengths of at least
`x`, by a binary search. O(r log r + p * 100 log r). The arms do not
rely on the rectangles or points being unique, and the harness repeats
them on purpose.

## Approaches

| file | mechanism |
|---|---|
| `rectangles.kara` ★ | a `Vec.filled(101, ..)` of buckets by height, each bucket's lengths sorted; a point sums `len() - partition_point(\|l\| l < x)` over the buckets from `y` to 100 |
| `rectangles_suffix.kara` | one search per point: for each height from 100 down to 1, the sorted lengths of every rectangle at least that tall, each list the one above with this height's own lengths merged in by a hand-written `merge_sorted`; a point takes one `partition_point` on the list for its `y` |
| `rectangles_sweep.kara` | offline, no search: the rectangles sorted longest first and the points' indices by `sort_by_key(\|i\| -x)`; before each point every rectangle at least as long is added to a `tall` count by height, and the point sums `tall` from `y` to 100; answers go back to the points' own order |
| `rectangles_struct.kara` | a `struct Shelf` of one height's sorted lengths whose `at_least` (`ref self`) is a binary search written out by hand, and a `struct Board` of 101 shelves built by `Board.build`, whose `containing` (`ref self`) sums the shelves from `y` to 100 |
| `rectangles_iter.kara` | iterator chains: the lengths grouped by height with a `fold` over an owned `Vec[Vec[i64]]`, each group sorted in a `map`, and each point the `sum` of a `map` over `y..101` |
| `rectangles_solution.kara` | LeetCode's Rust template: two `Vec<Vec<i32>>` in, `Vec<i32>` out, `vec![vec![]; 101]` by height, `sort_unstable` through `iter_mut`, and each point a closure over `p[1] as usize..=100`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (a point on a corner, points just past one, the largest values,
one rectangle three times), each with its counts; then the total over
2000 cases of 1 to 8 rectangles and 1 to 8 points with values 1 to 10,
with a checksum of the counts; then the constraints' most rectangles,
5 * 10^4 with lengths up to 10^9 and heights up to 100, against 10^4
points. `rectangles.py` mirrors the ★ arm and its output is
byte-identical. The large case keeps 10^4 points rather than 5 * 10^4
so that every arm stays near 5 s under `karac __mir-run`.

`karac fix` carries the template in one round of 36 edits: `Vec<..>` to
`Vec[..]`, `vec![vec![]; 101]` to `Vec.filled(101, Vec.new())`,
`sort_unstable` to `sort`, `&rectangles` and `&g[h]` to `ref`, the `&`
pattern dropped from the closures, `struct Solution;` to `struct
Solution {}`, and `Solution::` to `Solution.`. `p[1] as usize..=100` and
`partition_point` are Kāra as they stand.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every point every rectangle tried, counted when `0 <= x
<= l` and `0 <= y <= h`; no buckets, sorting or searching. It checks 300
random cases of 1 to 8 rectangles and 1 to 8 points with values 1 to
10; then 30 with lengths and `x` up to 5 * 10^8, so that doubled they
stay in bounds, and heights and `y` up to 100; then 30 of one rectangle
of height 100 many times. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | each count is the rectangles holding the point, read literally |
| P2 | the rectangles and the points both reversed: the counts reversed |
| P3 | the first rectangle added again: each count one more where that rectangle holds the point, the same elsewhere |
| P4 | every length and every `x` doubled: the same counts |
| P5 | the point `(1, 1)` added last: every rectangle counted for it, the other counts the same |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 610193125, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading through the
complement: all the rectangles, less those too short, less those too
low, plus those both. On a failure it prints the first ten and then the
count by property.

The last 30 cases first repeated a rectangle of any height. Under that
draw three mutations survived, each leaving out height 100 (M4, M11,
M29): a random height is 100 once in a hundred, and the wide cases
rarely put a point under it. The repeated rectangle is now always of
height 100, and all three are killed.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed and
fails the same way under both backends and not by a crash. The
thirty-one fall into only thirteen ways of failing, all thirteen among
the kept ones; no two kept ones in the same arm fail the same checks,
and three pairs across arms do (M5 and M18, M9 and M26, M4 and M29).

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the buckets not sorted | P1 61, P2 84, P3 19, P6 61 |
| M4 | ★: height 100 left out | P1 25, P3 25, P5 30, P6 25 |
| M5 | ★: the lengths short of `x` counted | P1 335, P3 302, P5 360, P6 335 |
| M7 | suffix: the merge stopped when the list above runs out | P1 314, P3 225, P5 360, P6 314 |
| M8 | suffix: a height's own lengths not sorted | P1 62, P2 84, P3 34, P6 62 |
| M9 | suffix: only the point's own height | P1 297, P3 196, P5 349, P6 297 |
| M12 | sweep: rectangles taken shortest first | P1 217, P3 105, P6 217 |
| M13 | sweep: points taken shortest first | P1 243, P3 144, P5 117, P6 243 |
| M14 | sweep: a rectangle exactly as long not added | P1 178, P3 73, P5 93, P6 178 |
| M18 | struct: the lengths short of `x` counted | P1 335, P3 302, P5 360, P6 335 |
| M20 | struct: only shelves above `y` | P1 171, P3 73, P5 111, P6 171 |
| M21 | struct: `x` and `y` swapped at the call | P1 281, P3 190, P4 267, P6 281 |
| M22 | iter: the heights from 1 to `y` | P1 336, P3 288, P5 349, P6 336 |
| M25 | iter: each group holding heights | P1 278, P3 176, P4 238, P6 278 |
| M26 | iter: only the point's own height | P1 297, P3 196, P5 349, P6 297 |
| M29 | solution: height 100 left out | P1 25, P3 25, P5 30, P6 25 |
| M31 | solution: every count one higher on the way out | P1 360, P5 360, P6 360 |

P1 and P6 kill all seventeen, P3 sixteen, P5 twelve, and P2 and P4 two
each. P3 misses only M31, whose extra one is in both of the counts
P3 compares. P5's point `(1, 1)` is held by
every rectangle, so it catches each edit that drops some heights or
lengths. P4 doubles lengths and `x` but not heights, so it catches only
the edits that mix the two up: bucketing heights instead of lengths
(M25) and `x` and `y` swapped (M21). P2 reverses both lists, and catches
only the unsorted buckets, whose search then depends on the order the
lengths arrived in (M3, M8).

Of the thirty-one, fourteen were not kept, and none survives, crashes
or differs between the backends. Each fails as a kept one does: a
length equal to `x` not counted in the ★, struct, iter and template
arms (M1, M17, M24, M27) as the sweep's (M14); heights above `y` only,
or the list one height up, in the ★, suffix, sweep and template arms
(M2, M10, M15, M28) as the struct arm's (M20); the struct and iter arms
unsorted (M19, M23) as the ★ arm (M3); the ★ arm's and the template's
buckets holding heights (M6, M30) as the iter arm's (M25); the sweep's
rectangle counted twice (M16) as the suffix's stopped merge (M7); and
the suffix's height 100 dropped (M11) as the ★ arm's (M4).

## Verification

Every arm prints the same output as `rectangles.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the sweep arm takes 0.7 s, the struct arm 2.7
s, the suffix arm 3.2 s, the ★ arm 4.2 s, the template 5.0 s, the iter
arm 5.3 s, and the differential 5.2 s.

## Benchmarks

The bench answers 4 cases of 5 * 10^4 rectangles and 5 * 10^4 points
with the ★ arm in all five languages, lengths and `x` from 1 to 10^9 and
heights and `y` from 1 to 100. Every implementation prints `4 cases of
5 * 10^4 rectangles and points: checksum 667364762`.

BENCHTAB
