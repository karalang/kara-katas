# 2280. Minimum Lines to Represent a Line Chart

You are given a 2D integer array `stockPrices` where `stockPrices[i] =
[dayi, pricei]` indicates the price of the stock on day `dayi` is
`pricei`. A **line chart** is created from the array by plotting the
points on an XY plane with the X-axis representing the day and the
Y-axis representing the price and connecting adjacent points.

Return *the **minimum number of lines** needed to represent the line
chart*.

```
stockPrices = [[1,7],[2,6],[3,5],[4,4],[5,4],[6,3],[7,2],[8,1]]  ->  3
stockPrices = [[3,4],[1,2],[7,8],[2,3]]                          ->  1
```

**Constraints:** `1 <= stockPrices.length <= 10^5`;
`stockPrices[i].length == 2`; `1 <= dayi, pricei <= 10^9`; all `dayi`
are **distinct**.

With the points in day order, the chart is one segment per pair of
neighbours, and a new line starts wherever it turns. Three neighbours
`a`, `b`, `c` lie on one line exactly when the cross product of `b - a`
and `c - b` is zero. Each difference is below 10^9, so the products fit
in an `i64` and no slope is ever divided: two slopes can differ by less
than 10^-17, which a `f64` cannot tell apart. O(n log n) for the sort.

## Approaches

| file | mechanism |
|---|---|
| `chart.kara` ★ | the points sorted by `sort_by_key` on the day; one line for the first segment and one more at each neighbouring three whose cross product is not zero |
| `chart_gcd.kara` | each segment's step `(dx, dy)` reduced by the gcd of `dx` and `\|dy\|`; the day always moves forward, so equal slopes reduce to equal steps, and a line starts at each step unlike the one before |
| `chart_map.kara` | the prices into a `SortedMap` keyed by day, walked in order with the last two points kept, a turn found by the cross product |
| `chart_struct.kara` | `struct Pen` of where it last stopped, the step it is drawing and the lines drawn; `draw` (`mut ref self`) moves it on and lifts it for a new line when the step turns |
| `chart_iter.kara` | one chain: the sorted points' `windows(3)`, the turns among them by `filter` on the cross product, and `count` plus one |
| `chart_solution.kara` | LeetCode's Rust template: `mut stock_prices: Vec<Vec<i32>>` in, `i32` out; `sort_unstable_by_key` on the day, then `for w in stock_prices.windows(3)` with each difference widened `as i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one point, 0; two points, 1; a turn, 2; a zigzag, 4; three points
whose two slopes differ by less than 10^-17, 2), each with its count;
then 2000 random charts of 1 to 40 points walked in straight pieces of
1 to 5 steps, each step up to 2, 30 or 10^6, then shuffled, with a
checksum; then three of the constraints' largest, 10^5 points: walked
in pieces (33402), all on one line (1), and a zigzag (99999).
`chart.py` mirrors the ★ arm and its output is byte-identical.

The ★ arm first read the three neighbours as `let (a, b, c) =
(points[i - 2], points[i - 1], points[i])`. `karac check` refuses it as
Rust would, a move out of a collection element (E0515), and `karac fix`
borrows each in place with `ref`. The iter arm first chained `filter`
straight onto `windows(3)`, which in Kāra returns a `Vec[Slice[T]]`, not
an iterator; `karac check` names the `.into_iter()` it needs and `karac
fix` inserts it. The template's `for w in stock_prices.windows(3)` needs
neither.

`karac fix` carries the template in one round, reporting 15 edits: `mut
stock_prices: Vec<Vec<i32>>` to `stock_prices: own Vec[Vec[i32]]` with
`let mut stock_prices = stock_prices;` as the body's first line,
`sort_unstable_by_key` to `sort_by_key`, `struct Solution;` to `struct
Solution {}`, and in the adapter `&Vec<Vec<i64>>` to a bare
`Vec[Vec[i64]]`, `|&x|` to `|x|`, `Solution::` to `Solution.` and the
`as i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the chart drawn from each point to the one with the next
day, found by a scan with no sort, each segment's line written `a x + b
y = c` in lowest terms, and a new line counted wherever a segment's line
is not the last one's. No cross products of neighbours. It checks 300
random charts of 1 to 12 points, walked in straight pieces with steps
up to 1, 3 or 10, or scattered over 30 days and 4 prices; then 30 on
one line; then 30 zigzags. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the points given in reverse order: the same count |
| P3 | every price turned upside down, `p` made `10^4 - p`, and every day tripled and moved 10^8 up: the same count |
| P4 | 0 for one point; otherwise from 1 to one fewer than the points, and 1 exactly when every point lies on one line |
| P5 | the last segment carried on to one more point: the same count; a second point after one: 1 |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 713171892, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that sorts
the points and counts the runs of equal slopes as `Fraction`s. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: one point drawn as a line | P1 26, P4 26, P6 26 |
| M3 | ★: the cross product's terms crossed | P1 180, P3 122, P4 41, P5 238, P6 180 |
| M4 | ★: the turn test inverted | P1 280, P4 132, P5 334, P6 280 |
| M8 | gcd: a fall the same as a rise | P1 66, P4 35, P6 66 |
| M10 | gcd: the slope a truncated quotient | P1 110, P3 182, P4 27, P6 110 |
| M11 | gcd: the last step never kept | P1 234, P4 63, P5 334, P6 234 |
| M12 | map: the first line never counted | P1 334, P4 151, P5 26, P6 334 |
| M14 | map: the chart keyed by price | P1 194, P2 49, P4 62, P5 147, P6 194 |
| M15 | map: the step measured from two back | P1 202, P4 53, P5 277, P6 202 |
| M17 | struct: the step never kept | P1 240, P4 240, P6 240 |
| M18 | struct: the pen never moved | P1 147, P5 235, P6 147 |
| M19 | struct: a turn only where the price changes way | P1 153, P3 86, P4 42, P6 153 |
| M23 | iter: the second step from the first point | P1 204, P4 53, P5 277, P6 204 |
| M25 | iter: four points to a window | P1 152, P4 24, P5 152, P6 152 |
| M26 | iter: sorted by price | P1 169, P2 42, P3 42, P5 125, P6 169 |
| M30 | solution: never sorted | P1 178, P5 204, P6 178 |
| M31 | solution: a turn only upward | P1 205, P3 165, P4 41, P6 205 |

P1 and P6 kill all seventeen, P4 fourteen, P5 eleven, P3 five, and P2
two. P4 misses the three edits that still read some order of the points
and count its turns: never sorted, sorted by price, and the pen never
moved, each between 1 and one fewer than the points and 1 for a straight
chart, which is straight in any order. P5 catches an edit whose count
moves when the chart runs on along its last line, though that adds no
turn. P3 catches the edits that read the values and not only their
differences' ratio: terms crossed between days and prices, a slope
truncated, a turn by which way the price goes, a sort by price, and a
turn only upward, each changed by turning the prices over or stretching
the days. P2 catches only the two edits that lean on the order the
points arrive in: a map keyed by price, where a repeated price keeps
the later day, and a stable sort by price, which keeps that order among
equal prices.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Seven fail as a kept one does: the ★ and iter
arms' never sorted (M1, M24) as the template's (M30); the ★ arm's
sorted by price (M6) as the iter arm's (M26); the struct arm's first
point drawn again and the template's one point drawn as a line (M20,
M27) as the ★ arm's (M2); and the iter arm's turns without the first
line and the template's count from 0 (M22, M28) as the map arm's first
line never counted (M12). Seven fail in ways of their own and are left
out because their arms keep enough: the ★ arm's first three never
compared and the map arm's first turn never tested (M5, M16), alike;
the gcd arm's never reduced and its first segment free (M7, M9); the
map arm's point two back never moved (M13); the struct arm's first
price taken as 0 (M21); and the template's each step against itself
(M29).

## Verification

Every arm prints the same output as `chart.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the differential takes 0.6 s, the ★ arm 2.1 s,
the gcd and struct arms 2.4 s, the iter arm 3.4 s, the template 5.3 s,
and the map arm 9.1 s, the 3 * 10^5 inserts of the long cases into the
`SortedMap` taking most of it; compiled, the map arm takes 0.4 s like
the others.

## Benchmarks

The bench answers 20 charts of the constraints' largest, 10^5 points
walked in straight pieces of 1 to 5 steps, each up to 1000 days on and
1000 up or down, then shuffled, with the ★ arm in all five languages.
Every implementation prints `20 charts of 10^5: checksum 285635687`.
Each sorts a fresh copy of the points per call: C an array of `struct`
pairs by `qsort`, Go a slice of slices by `sort.Slice`, and Kāra, Rust
and Python a list of two-element lists.

BENCHTAB
