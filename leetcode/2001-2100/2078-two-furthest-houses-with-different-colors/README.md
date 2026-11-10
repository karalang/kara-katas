# 2078. Two Furthest Houses With Different Colors

There are `n` houses evenly lined up on the street, and each house is
beautifully painted. You are given a 0-indexed integer array `colors` of
length `n`, where `colors[i]` represents the color of the `i`-th house.

Return the maximum distance between two houses with different colors.

The distance between the `i`-th and `j`-th houses is `abs(i - j)`, where
`abs(x)` is the absolute value of `x`.

```
colors = [1,1,1,6,1,1,1]  ->  3
colors = [1,8,3,8,3]      ->  4
colors = [0,1]            ->  1
```

**Constraints:** `n == colors.length`; `2 <= n <= 100`; `0 <= colors[i]
<= 100`; test data are generated such that at least two houses have
different colors.

The furthest pair of differing houses has the first house or the last
in it: if it had neither, the first house or the last differs from one
of the pair and makes a longer pair. So the answer is the furthest house
from the first that differs from it, or the furthest from the last,
each found by a scan in from its end: O(n). The approaches differ in how
far they lean on that and how they search.

## Approaches

| file | mechanism |
|---|---|
| `houses.kara` ★ | two `while` scans, one in from the last house to the first unlike the first house, one in from the first to the first unlike the last; the greater distance. O(n) |
| `houses_pairs.kara` | every pair `i < j`, the greatest `j - i` of a pair that differs. O(n²) |
| `houses_find.kara` | the iterator searches: `rposition` for the last house unlike the first, `position` for the first unlike the last, each `unwrap()`ped. O(n) |
| `houses_width.kara` | widest first: each distance `d` from `n - 1` down, and the first at which some `windows(d + 1)` of the street has ends that differ, by `any`. O(n²) at worst |
| `houses_spans.kara` | by color: each color's first and last house in a `SortedMap` of a `struct Reach`, updated through `get_mut`, and the widest span from one color's first house to another's last. O(n + k²) |
| `houses_solution.kara` | LeetCode's Rust template (`Vec<i32>`, two `for` loops with `.rev()` and `break`, `std::cmp::max`, `ans as i32`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more, each street and its answer; then the sum and a checksum of the
answers for 3000 random streets of 2 to 100 houses of 2, 3 or 100
colors, a quarter of them one color but for one house; then the answer
for 100 houses of one color but the middle two. `houses.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of houses looked at, and the greatest distance of
a pair of different colors kept. It checks 300 random streets of 2 to 12
houses of 2, 3 or 100 colors, drawn again when every house is one color;
then 20 of one color but for one house, and 20 of two colors in two
runs. All 340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the street reversed gives the same answer |
| P3 | the colors renamed, `c` to `100 - c`, give the same answer |
| P4 | a house of a new color added at either end gives the length of the street |
| P5 | the street cut short by a house at either end, if two of its houses still differ, answers no more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 streets: checksum 535715428, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
streets. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-four edits to the differential, five to seven to each of its
arms, each run under `karac __mir-llvm-run` and `karac __mir-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends and
not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the scan from the first house | P1 27, P2 58, P5 22, P6 27 |
| M2 | ★: only the scan from the last house | P1 31, P2 58, P5 26, P6 31 |
| M3 | ★: the far house's distance one more | P1 313, P2 58, P4 340, P5 22, P6 313 |
| M4 | pairs: each house against the next alone | P1 309, P4 340, P6 309 |
| M5 | pairs: the last house never paired | P1 279, P2 126, P4 340, P6 279 |
| M6 | pairs: the first house never paired | P1 283, P2 126, P4 340, P6 283 |
| M7 | find: the far house found from the front | P1 22, P2 41, P5 20, P6 22 |
| M8 | find: the near house found from the back | P1 19, P2 41, P5 19, P6 19 |
| M9 | find: the near search for the last house's own color | P1 88, P6 88 |
| M10 | width: the street's full width never tried | P1 252, P4 340, P6 252 |
| M11 | width: a window's second house against its last | P1 129, P2 126, P4 88, P6 129 |
| M12 | width: every window made to differ | P1 64, P5 50, P6 64 |
| M13 | spans: the later color's first house | P1 174, P2 177, P4 194, P5 32, P6 174 |
| M14 | spans: a color's later houses moving its first | P1 221, P4 221, P5 43, P6 221 |
| M15 | spans: only the pairs in color order | P1 147, P2 311, P3 311, P4 340, P6 147 |
| M16 | solution: the adapter's colors halved | P1 122, P3 202, P6 122 |
| M17 | solution: the two loops' distances added | P1 340, P4 340, P5 48, P6 340 |

P1 and P6 kill all seventeen, P2 and P4 ten each, P5 nine and P3 two.
P2, which reverses the street, sees an edit that trusts one end over
the other: one scan alone (M1, M2), a search from the wrong end (M7,
M8), the first or last house left out (M5, M6). P4, which adds a house
of a new color at an end, sees an edit that cannot reach the full
length: pairs too close (M4), the full width never tried (M10), or an
off-by-one (M3). P5, which cuts the street short, sees an answer that
rises when a house is taken away, which a scan that finds a nearer house
than the furthest gives (M1, M2, M7, M8, M12). P3 sees an edit that
leans on the colors' order or values: pairs taken in color order (M15),
two colors merged by the adapter (M16).

Of the thirty-four, seventeen were not kept. Four survive, and all are
equivalent. The ★ arm's far scan comparing with the last house, its
near scan comparing with the first, and the Rust arm's second loop
comparing with the first house each change only a street whose ends
differ, and there the other scan finds the whole street at once, `n -
1`, which is the answer; the Rust arm's adapter reversing the street
leaves the answer, as P2 says. Seven fail as a kept one: the ★ arm's
near house's distance one short, the find arm's near house's place
taken as its distance and the Rust arm's second loop's distance one
short as M1; the find arm's far house measured from the end as M2; the
Rust arm's first loop never breaking as M7; the width arm's narrowest
first as M4; the Rust adapter's first house dropped as M6. Five fail
alike, wrong on every street, and none is kept (P1 340, P4 340): the
pairs arm's pairs of one color and distance one more, the spans arm's
each color against itself and first house one on, the width arm's width
one short. One crashes and is not kept: the width arm's windows one
house too narrow for their `w[d]`.

## Verification

Every arm prints the same output as `houses.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.5 s to 3.1 s, the spans arm the
slowest, and the differential 0.7 s (timed while other work shared the
machine).

No arm met a compiler gap. The width arm was written with
`colors[..].windows(d + 1).any(..)`; `windows` gives a `Vec` of slices,
and the checker refused `any` on it with the edit to `.iter().any(..)`,
which `karac fix` applied. The spans arm's struct was first named
`Span`, and the checker warned that it shadows the prelude's `Span`; it
is named `Reach`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 4 and 1 edits: `Vec<i32>` to brackets,
`std::cmp::max` to `max`, `struct Solution;` to `struct Solution {}`,
`Solution::` to `.`; then the adapter's `as i64`, redundant as the
template's `i32` widens to it. The fixed arm reads as the template does,
`ans as i32` and all.

## Benchmarks

The bench keeps 20000 streets of 100 houses, all of color 0 but for two
houses, and runs 1000 rounds with the ★ arm in all five languages: each
round recolors one house of every street and answers every street that
still has two colors, 19999997 answers in all. Every implementation
prints `19999997 answers: sum 1966325874, checksum 105928072`.

BENCHTAB
