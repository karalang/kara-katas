# 1465. Maximum Area of a Piece of Cake After Horizontal and Vertical Cuts

You are given a rectangular cake of size `h x w` and two arrays of
integers `horizontalCuts` and `verticalCuts` where `horizontalCuts[i]`
is the distance from the top of the rectangular cake to the `i`th
horizontal cut and similarly, `verticalCuts[j]` is the distance from the
left of the rectangular cake to the `j`th vertical cut. Return the
maximum area of a piece of cake after you cut at each horizontal and
vertical position provided in the arrays `horizontalCuts` and
`verticalCuts`. Since the answer can be a large number, return this
modulo `10^9 + 7`.

```
h = 5, w = 4, horizontalCuts = [1,2,4], verticalCuts = [1,3]   ->  4
h = 5, w = 4, horizontalCuts = [3,1], verticalCuts = [1]       ->  6
h = 5, w = 4, horizontalCuts = [3], verticalCuts = [3]         ->  9
```

**Constraints:** `2 <= h, w <= 10^9`, `1 <= horizontalCuts.length <=
min(h - 1, 10^5)`, `1 <= verticalCuts.length <= min(w - 1, 10^5)`, `1 <=
horizontalCuts[i] < h`, `1 <= verticalCuts[i] < w`, and the cuts of each
array are distinct.

The arms are `fn max_area(h: i32, w: i32, horizontal_cuts: Vec[i32],
vertical_cuts: Vec[i32]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_area.kara` ★ | every piece is a gap one way by a gap the other, so the largest is the widest gap each way multiplied: each way's cuts cloned and sorted, the widest gap found in one walk with the edges at 0 and the size counted, and the two multiplied in `i64` and taken modulo 10^9 + 7. O(n log n) |
| `max_area_windows.kara` | the edges pushed onto a clone of each way's cuts, sorted, and the widest neighbouring pair found by `windows(2).into_iter().map(..).max()`. O(n log n) |
| `max_area_sorted_set.kara` | each way's cuts collected into a `SortedSet[i32]` with the far edge inserted, and walked in order from the near edge. O(n log n) |
| `max_area_buckets.kara` | each way's widest gap found without sorting: m points from 0 to the size leave a gap at least size / (m - 1) wide, so with buckets that wide no gap inside one is the widest; a closure puts each point into its bucket's smallest and largest, and the widest gap runs from one filled bucket's largest to the next one's smallest. O(n) |
| `max_area_solution.kara` | a Rust solution as LeetCode's Rust users write it (both cut lists taken as `mut` parameters and sorted in place by `sort_unstable`, the far edge read through `last().unwrap()`, the gaps by `windows(2)`, the product taken in `i64` under a `const MOD`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and three
more, the largest cake cut once each way near an edge, a cake of 2 by 2
cut in its middle, and a cake of 100001 by 100001 cut each way at every
place but one (`4 6 9 64 1 4`); the constraints' most, 100000 cuts each
way on a cake of 10^9 by 10^9 (`100000 cuts: 257969961`); and 2000
random cakes of 2 to 10^9 each way with 1 to 50 cuts each way (`2000
random cakes: checksum 83398770`). `max_area.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★ arm, written with `best as i64` for the widest
gap's return, takes one fix by `karac fix`: the cast dropped, since
`i32` widens to `i64` implicitly. The windows arm, written with Rust's
`points.windows(2).map(..)`, takes one: `.into_iter()` after
`windows(2)`, which makes a `Vec` of views. The sorted-set arm takes
two: `best` and `last` declared `i32`, since the literal `0` keeps its
default `i64`, which would narrow into the `i32` return. As first
written it then multiplied the two widest gaps into `let area: i64`,
which traps with `integer overflow` on the largest cake: each operation
runs in its own operands' type, so the product of two `i32` is computed
and checked in `i32` before it widens (design.md § Mixed-width
operands). One factor is widened by hand, `widest(..) as i64 *
widest(..)`. The buckets arm takes four: three casts dropped, the
redundant `cuts.len() as i64` and a lossless `c as i64`, and the two `as
usize` on the bucket count and index, since lengths and indices are
`i64`. The Rust solution takes one round of 13 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, each `mut horizontal_cuts: Vec<i32>` parameter to
`horizontal_cuts: own Vec[i32]` with `let mut horizontal_cuts =
horizontal_cuts;` at the body's start, `sort_unstable` to `sort`, and
`Solution::max_area` to `Solution.max_area`; the parameters' `own`
carries to the harness's `max_area` that calls the method. Every arm's
output then matches on its first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the cake cut into every piece, each piece's area in `i64`,
and the largest of them modulo 10^9 + 7, while there are at most 2000
cuts. LeetCode's examples, four edge cases (the largest cake cut once
each way near an edge, a cake of 2 by 2, a cake of 1000 by 7 cut at
every place, and one of 100001 by 100001 cut at every place but one),
the constraints' most, and 1995 random cakes, half of 2 to 30 each way
with 1 to 12 cuts each way, half of 2 to 10^9 with 1 to 50.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 2000 cuts |
| P2 | the cake turned, its two sides and their cuts swapped, gives the same answer |
| P3 | the cuts shuffled give the same answer |
| P4 | every cut measured from the other edge gives the same answer |
| P5 | the cake and every cut doubled, while that fits, gives four times the answer, modulo 10^9 + 7 |
| P6 | the ★ arm's answer |

All 56,560 checks pass on every arm: `2003 cases: checksum 610309703,
56560 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, zipping each
way's sorted points with its edges, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the cuts never sorted | P1 1933, P3 1855, P4 1967, P6 7736 |
| M2 | ★: the gap to the far edge never counted | P1 501, P4 824, P6 2004 |
| M3 | windows: the near edge never added | P1 380, P4 824, P6 380 |
| M4 | windows: the narrowest gap taken | P1 1985, P6 1987 |
| M5 | sorted set: every gap measured from the near edge | P1 2001, P6 2003 |
| M6 | sorted set: the far edge never added | P1 501, P4 824, P6 501 |
| M7 | buckets: the last filled bucket never moved on | P1 1995, P4 1493, P5 296, P6 1997 |
| M8 | buckets: each gap measured to a bucket's largest point, not its smallest | P1 878, P4 1243, P5 178, P6 879 |
| M9 | solution: the vertical cuts never sorted | P1 1702, P2 1910, P3 1546, P4 1829, P6 1703 |
| M10 | solution: each vertical gap one short | P1 1320, P2 1675, P5 723, P6 1322 |

## Benchmarks

The bench draws 100 cakes with 5000 cuts each way from 1 to 5 x 10^8,
once; then makes 20 passes, each answering every cake with the ★ arm at
a height and a width of 10^9 less a number chosen from the checksum so
far, so no answer carries over, and folding the answer into the
checksum. Each implementation copies each way's cuts and sorts them with
its library's sort: Rust's `sort`, C's `qsort` with a comparison
function, Go's `slices.Sort` and Python's `sorted`. Every implementation
prints `20 passes over 100 cakes of 5000 cuts each way: checksum
288462385`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.40 s against Rust's 0.37 s (0.52 s with overflow checks
on), C's 2.0 s and Go's 1.6 s; Python takes 5.0 s.
