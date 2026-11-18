# 2303. Calculate Amount Paid in Taxes

You are given a **0-indexed** 2D integer array `brackets` where
`brackets[i] = [upper_i, percent_i]` means that the `i`th tax bracket
has an upper bound of `upper_i` and is taxed at a rate of `percent_i`.
The brackets are **sorted** by upper bound (i.e. `upper_{i-1} <
upper_i` for `0 < i < brackets.length`).

Tax is calculated as follows:

- The first `upper_0` dollars earned are taxed at a rate of
  `percent_0`.
- The next `upper_1 - upper_0` dollars earned are taxed at a rate of
  `percent_1`.
- The next `upper_2 - upper_1` dollars earned are taxed at a rate of
  `percent_2`.
- And so on.

You are given an integer `income` representing the amount of money you
earned. Return *the amount of money that you have to pay in taxes.*
Answers within `10^-5` of the actual answer will be accepted.

```
brackets = [[3,50],[7,10],[12,25]], income = 10  ->  2.65000
brackets = [[1,0],[4,25],[5,50]], income = 2     ->  0.25000
brackets = [[2,50]], income = 0                  ->  0.00000
```

**Constraints:** `1 <= brackets.length <= 100`; `1 <= upper_i <= 1000`;
`0 <= percent_i <= 100`; `0 <= income <= 1000`; `upper_i` is sorted in
ascending order and all `upper_i` are unique; the upper bound of the
last tax bracket is at least `income`.

Each bracket taxes the part of the income between the upper bound
before it (0 for the first) and its own, capped at the income, and the
walk can stop at the first bracket that starts at or above the income.
Every part is a whole number of dollars and every percent a whole
number, so the tax is a whole number of hundredths of a dollar, at most
`1000 * 100`: summed as an integer and divided once, it is exact up to
the one rounding of that division. O(brackets).

## Approaches

| file | mechanism |
|---|---|
| `tax.kara` ★ | the brackets walked in order with the bound below each: the part `upper.min(income) - below` times the percent added in hundredths, a `break` once the bound below reaches the income, and one division by 100 at the end |
| `tax_naive.kara` | dollar by dollar: each dollar from the first to the last taxed at the percent of the first bracket whose upper bound reaches it. O(income * brackets) |
| `tax_float.kara` | in `f64` throughout, as the answer is: the income still untaxed is `left`, each bracket takes `left.min(upper - below)` of it at `percent / 100.0`, and the walk stops when `left` is 0 |
| `tax_iter.kara` | each bracket's lower bound is the upper bound before it, so the brackets `zip`ped with `[0].into_iter().chain(..)` of their own upper bounds give each band, `map`ped to its hundredths, `.max(0)` for a band above the income, and `sum`med |
| `tax_struct.kara` | a `struct Band { low, high, percent }` built from the brackets, `Band.hundredths(income)` the tax on the income inside it, nothing for an income at or below its low end |
| `tax_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` brackets read as `b[0]` and `b[1]`, `taxed as f64 * percent as f64 / 100.0` summed in `f64`, a `break` at the first bracket with nothing to tax; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples, each to
five places; an income on a bracket's upper bound; a bracket of 100
percent between two others; the largest income all taxed in full; then
2000 random cases of 1 to 10 brackets rising to at most 1000, percents
from 0 to 100 and an income up to the last upper bound, with a
checksum of the tax in cents and the cents in all. `tax.py` mirrors the
★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 4 edits:
`struct Solution;` to `struct Solution {}`, and the three brackets of
`Vec<Vec<i32>>`, `<`, `<` and `>>`, to `Vec[Vec[i32]]`. The rest of the
template is Kāra as it stands: the `as f64` widenings, `income.min(upper)`
on `i32`, and the tuple `let (upper, percent) = (b[0], b[1])`.

The iter arm was first written `[0].iter().chain(brackets.iter().map(..))`,
as in Rust: `[0].iter()` yields `ref i64` and the `map` yields `i64`, so
`chain` refuses them. `karac check` says so, names the bound
`J.Item = ref i64` against `Item = i64`, and points to `.cloned()`.
`karac fix` carries it in one call, reporting 3 edits: the `.cloned()`,
and then, since a temporary `[0]` would be dropped while the lazy
iterator still borrows it, the array hoisted into `let lows_src = [0];`
and the chain begun from `lows_src.iter()`. The result prints the same
7 lines. The arm keeps `[0].into_iter()`, which yields the `i64` directly
and is how a Rust user writes it once the item type is seen.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the income not yet taxed is taken bracket by bracket, the
first `upper_0` dollars, then the next `upper_1 - upper_0`, and so on,
each part taxed at its bracket's percent, in whole hundredths. Each
arm's answer is compared in hundredths, rounded. It checks 300 random
cases of 1 to 10 brackets; then 30 whose income is one of their own
upper bounds, so the walk ends exactly on a bracket's edge; then 30 of
100 brackets, the most the constraints allow, of 1 to 10 dollars each,
the last stretched to 1000. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the tax is from 0 to the income |
| P3 | every percent 100: the tax is the income |
| P4 | the widest bracket split in two at its middle, the same percent in both halves: the same answer |
| P5 | one dollar more of income, where the brackets reach it: the tax grows by that dollar's percent, in hundredths |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 708478934, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and takes each bracket's part with `min` and
`max`. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a bracket skipped when it begins at the income's last dollar | P1 15, P3 15, P4 1, P5 43, P6 15 |
| M5 | ★: the first dollar not taxed | P1 357, P3 360, P6 357 |
| M6 | ★: the first bracket left out | P1 358, P3 32, P4 101, P5 86, P6 358 |
| M7 | naive: a dollar on a bracket's upper bound taxed at the next bracket | P1 271, P5 6, P6 271 |
| M9 | naive: every dollar at the first bracket's percent | P1 264, P5 264, P6 264 |
| M10 | naive: each dollar taxed at the smaller of its bracket's bound and percent | P1 137, P3 238, P4 57, P5 20, P6 137 |
| M12 | float: each bracket as wide as its upper bound | P1 201, P4 68, P5 186, P6 201 |
| M13 | float: the untaxed income never reduced | P1 320, P2 148, P3 321, P4 142, P5 295, P6 320 |
| M14 | float: the percent read as a tenth of one | P1 359, P2 316, P3 360, P5 347, P6 359 |
| M17 | iter: a band above the income taxed negative | P1 247, P2 162, P3 247, P4 172, P5 247, P6 247 |
| M18 | iter: each band paired with its own upper bound as its low end | P1 359, P3 360, P5 347, P6 359 |
| M21 | iter: each band's part capped at one dollar | P1 358, P3 359, P4 180, P5 318, P6 358 |
| M23 | struct: the band's upper bound not a cap | P1 264, P2 172, P3 264, P4 180, P5 265, P6 264 |
| M24 | struct: every band starting at 0 | P1 327, P2 290, P3 328, P4 354, P5 247, P6 327 |
| M26 | struct: the last band left out | P1 101, P3 102, P4 62, P5 103, P6 101 |
| M30 | solution: the income not a cap | P1 350, P2 184, P3 351, P5 347, P6 350 |
| M31 | solution: the upper bound and percent swapped | P1 357, P2 52, P3 356, P4 134, P5 348, P6 357 |

P1 and P6 kill all seventeen, P5 sixteen, P3 fourteen, P4 eleven and
P2 seven. P3, every percent 100, turns any error in how many dollars
are taxed into a wrong answer, and misses only the edits that tax the
right dollars at the wrong percent: the naive arm's dollar on a bound
taxed at the next bracket, and every dollar at the first bracket's
percent, and the float arm's brackets as wide as their upper bounds,
which with every percent 100 still stops at the income. P5, one dollar
more, misses only the ★ arm's first dollar not taxed, which loses the
same dollar at either income. P4, a bracket split, fails only where an
edit leans on how many brackets there are or where they start. P2 fails
where an edit can tax more than the income or less than nothing.

Of the thirty-one, fourteen were not kept. Three are equivalent and
killed by nothing: the float arm's stop tested as `left <= upper -
below` after `below` has moved to `upper` (M15), which is `left <= 0`;
the struct arm's band taxed when the income is at its low end (M22),
which taxes 0 dollars there; and the template's stop only when the part
is below 0 (M27), which adds 0 for an empty bracket and stops at the
next. The bound below never moved on in the ★ (M3) and template (M28)
arms fails as the struct arm's every band starting at 0 (M24), and the
float arm's (M16) as its own brackets as wide as their upper bounds
(M12); the ★ arm's hundredths read as tenths (M4) and the template's
percent as a tenth (M29) as the float arm's (M14); the iter arm's
income not a cap (M19) as the template's (M30); the struct arm's low
and high swapped (M25) as the iter arm's bands paired with their own
tops (M18). The ★ arm's every bracket taxed whole (M2), the naive
arm's last dollar not taxed (M8) and dollar zero taxed too (M11), and
the iter arm's lows shifted by one band (M20) fail apart from every
kept one, and were left out to keep three to an arm.

## Verification

Every arm prints the same output as `tax.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.4 s, the naive one,
which walks every dollar, the slowest. The differential takes 1.1 s
there and 0.4 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 20 lists of 100 brackets once, the upper bound of
bracket `i` being `10 (i + 1)` less 0 to 4 and the last 1000, each
percent from 0 to 100; then makes 100 passes, each taxing every income
from 0 to 1000 under every list with the ★ arm in all five languages,
and folds each tax, in cents, rounded, into a checksum. Every
implementation prints `100 passes over 20 lists of 100 brackets and
1001 incomes: checksum 541525082`. Each keeps the brackets as pairs of
64-bit integers: tuples in a `Vec`, `int64_t[2]` rows of a static
array, `[2]int64` in a slice, and tuples in a list. The C build links
`-lm` for `round`.

BENCHTAB
