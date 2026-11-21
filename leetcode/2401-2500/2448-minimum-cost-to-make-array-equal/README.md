# 2448. Minimum Cost to Make Array Equal

You are given two **0-indexed** arrays `nums` and `cost` consisting each
of `n` **positive** integers.

You can do the following operation **any** number of times:

- Increase or decrease **any** element of the array `nums` by `1`.

The cost of doing one operation on the `i`th element is `cost[i]`.

Return *the **minimum** total cost such that all the elements of the
array* `nums` *become **equal***.

```
nums = [1,3,5,2], cost = [2,3,1,14]      ->  8
nums = [2,2,2,2,2], cost = [4,2,8,1,3]   ->  0
```

**Constraints:** `n == nums.length == cost.length`; `1 <= n <= 10^5`;
`1 <= nums[i], cost[i] <= 10^6`; the answer is at most `2^63 - 1`.

Making every value `x` costs `sum cost[i] |nums[i] - x|`. Moving `x` up
by one adds the cost of every value at or below it and takes off the
cost of every value above, so the total falls while more cost lies
above `x` than at or below it and rises after: it is convex, and its
least is at a weighted median, a value where the cost on either side is
at most half the whole. The answers to the cases below reach about
`5 * 10^14`, well inside an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `cost.kara` ★ | the weighted median: the pairs of value and cost sorted, the first value whose running cost reaches half the total taken, and every value moved there. O(n log n) |
| `cost_naive.kara` | the statement read directly: every value of `nums` tried as the target, since the total is linear between values, and each target's cost summed over every value. O(n^2) |
| `cost_ternary.kara` | a ternary search over the integers from the least value to the largest, the total being convex: of two inner points the outer side of the dearer one dropped, until three or fewer remain to try. O(n log V) |
| `cost_prefix.kara` | an order of the indices by `sort_by_key`, and prefix sums of the costs and of each cost times its value, so each value's total as a target is four lookups. O(n log n) |
| `cost_iter.kara` | iterators: the pairs by `zip` and sorted, the running cost by `scan`, the median by `find`, and the cost to move every value there by `map` and `sum`. O(n log n) |
| `cost_solution.kara` | LeetCode's Rust template: the pairs widened to `(i64, i64)` through `\|(&a, &b)\|`, sorted by `sort_unstable`, and the median found by `for &(x, c) in &v`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; one value;
two values of equal cost; one heavy cost among light ones; then `2000`
values and costs from 1 to `10^6`; `2000` values from 1 to 10 with
costs to `10^6`, full of ties; `2000` values to `10^6`, every cost
`10^6`; and 3000 random cases of 1 to 8 values from 1 to 10, costs to
10, as a checksum and the total. The largest cases hold `2000` values,
not the constraints' `10^5`, because the naive arm tries every value
against every other. `cost.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 20000 random cases of up
to 8 values against every integer target from the least value to the
largest.

`check` first reports 10 errors on the template, and `karac fix`
carries it in one call, reporting 16 edits: each of the six angle
brackets of the three `Vec<..>` made square; the `&` dropped from the
five patterns `&a`, `&b`, `&(_, c)`, `&(x, c)` and `&(x, c)`, since a
Kāra pattern already matches through a reference; the loop's `&v`
written `ref v`; `struct Solution;` given its braces; and, once the
template parses, `sort_unstable` written `sort`, the library having
only the stable sort, and the `i64` suffix dropped from the two `0i64`,
`i64` being a literal's default. The casts `a as i64` and `b as i64`,
`.abs()` and the `sum()` into the declared `i64` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every integer from the least value to the largest tried as
the one all values are made equal to, each value's cost of `cost[i]`
for every step to it summed one step at a time, and the least total
kept. No median is found and nothing is sorted. It checks 300 random
cases of 1 to 10 values from 1 to 60, costs from 1 to 20; then 30 of up
to 50 values from 1 to 300, costs to `10^5`; then 30 of up to 200
values from 1 to 5, costs to `10^5`, full of ties. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the pairs in reverse order: the same answer |
| P3 | every value raised by one number from 1 to 1000: the same answer |
| P4 | every cost multiplied by one number from 2 to 9: the answer times it |
| P5 | every value `x` mirrored to `10^6 + 1 - x`: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the total does not depend on the order of the pairs.
P3 and P5 hold because raising every value, or mirroring them, keeps
every distance between a value and the matching target. P4 holds
because every target's total is multiplied by the same number.

The differential prints `360 cases: checksum 729966444, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every integer target. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the median a quarter of the way | P1 284, P5 317, P6 284 |
| M4 | ★: the target one below the median | P1 360, P5 316, P6 360 |
| M5 | ★: the costs left out of the sum | P1 325, P4 326, P5 5, P6 325 |
| M7 | naive: only the first target | P1 247, P2 317, P6 247 |
| M9 | naive: the distance not made absolute | P1 318, P2 316, P5 326, P6 318 |
| M10 | naive: the first value never moved | P1 310, P2 299, P6 310 |
| M12 | ternary: the dearer side kept | P1 298, P6 298 |
| M13 | ternary: the top point never tried | P1 28, P5 46, P6 28 |
| M14 | ternary: the search ending at the least value | P1 308, P5 326, P6 308 |
| M17 | prefix: the order never sorted | P1 305, P2 319, P5 326, P6 305 |
| M18 | prefix: the value's own cost counted above too | P1 360, P2 5, P3 359, P5 360, P6 360 |
| M19 | prefix: the moments without the costs | P1 360, P2 48, P3 350, P4 360, P5 357, P6 360 |
| M23 | iter: the median where the whole cost is reached | P1 297, P5 326, P6 297 |
| M24 | iter: the pairs never sorted | P1 217, P2 11, P6 217 |
| M25 | iter: each distance times the value | P1 324, P3 326, P4 326, P5 326, P6 324 |
| M28 | solution: the total of the values | P1 334, P3 303, P4 273, P5 360, P6 334 |
| M29 | solution: the median one above | P1 352, P5 309, P6 352 |


P1 and P6 kill all seventeen, P5 thirteen, P2 seven, and P3 and P4
four each.

Fourteen are not kept. Two fail exactly as a kept one: the ★ arm's and
the template's pairs never sorted (M1, M31) as the iter arm's (M24).
Ten fail apart from every kept one and were left out because those arms
keep their share already: the ★ arm's and the template's running cost
a count (M2, M27), which fail alike, each taking the median by the
number of values rather than by their cost; the ★ arm's last pair never
reached (M6); the naive arm's largest total kept (M8) and the
template's every distance doubled (M30), which fail alike and which P1
and P6 alone catch, since either is consistent under every
transformation; the naive arm's each target one above its value (M11);
the ternary arm's costs left out of each total and near side dropped
(M15, M16); and the prefix arm's last value never a target and best
judged by the cost below (M20, M21).

Two end in a panic, not a wrong answer, under both backends: the iter
arm's running cost restarted at each pair and running cost of the pairs
before (M22, M26). Each can leave no pair whose running cost reaches
half the total, so `find` gives `None` and the `unwrap` after it stops
the program.

## Verification

Every arm prints the same output as `cost.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 0.6 s, but for the naive
arm, which tries every value against every other: on the cases of
`2000` values that is `1.2 * 10^7` terms, and it takes 5.6 s there,
1.0 s under `karac __mir-llvm-asan` and 0.3 s under `karac run`. The
differential takes 6.1 s under `karac __mir-run`, 1.8 s under `karac
__mir-llvm-asan` and 0.9 s under `karac run`.

## Benchmarks

The bench builds `10^5` values and costs from 1 to `10^6`, the
constraints' largest, once from its own generator. It then makes 200
passes; pass `p` draws 1000 new costs up to `10^6` from place `1000 p`
on, so the median moves and no answer can be carried from one pass to
the next, then answers and folds the answer plus the pass into the
checksum. The bench uses the ★ arm, the weighted median of the sorted
pairs, in all five languages. Every implementation prints `200 passes
over 10^5 values: checksum 816675463`. Each language sorts the pairs
with its library's sort: `sort` on a vector of tuples in Kāra and Rust,
`qsort` with a comparison function in C, `sort.Slice` in Go, and
`sorted` in Python, each comparing the value and then the cost.

BENCHTAB
