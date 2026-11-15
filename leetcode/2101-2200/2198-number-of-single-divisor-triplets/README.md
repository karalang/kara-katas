# 2198. Number of Single Divisor Triplets

You are given a **0-indexed** array of positive integers `nums`. A
triplet of three **distinct** indices `(i, j, k)` is called a **single
divisor triplet** of `nums` if `nums[i] + nums[j] + nums[k]` is
divisible by **exactly one** of `nums[i]`, `nums[j]`, or `nums[k]`.

Return *the number of **single divisor triplets** of* `nums`*.*

```
nums = [4, 6, 7, 3, 2]  ->  12
nums = [1, 2, 2]        ->  6
nums = [1, 1, 1]        ->  0
```

**Constraints:** `3 <= nums.length <= 10^5`; `1 <= nums[i] <= 100`.

The numbers are at most 100, so the array is tallied by value and every
ordered triple of values is tried, not every triple of indices: when
exactly one of the three values divides their sum, the triple stands for
the tally's product of index triples, each value's count stepped down
once for each time the same value came earlier. A triple of one value
never counts, since each of its three divides 3a. O(n + 100^3).

## Approaches

| file | mechanism |
|---|---|
| `count.kara` ★ | a `[0; 101]` tally, three nested loops over 1 to 100 skipping a value the array lacks, the three divisibility tests spelled out, and the product with the counts stepped down for a value repeated |
| `count_sorted.kara` | each multiset a <= b <= c tried once, its ordered index triples counted by its shape: three distinct values in any of 6 orders, two alike with the third in any of 3 places |
| `count_distinct.kara` | the array tallied into a `SortedMap`, its entries listed as (value, count) pairs, every ordered triple of entries tried, a repeated entry stepping its count down by index, so few values take few steps |
| `count_struct.kara` | a `struct Tally` with `ordered` (`ref self`) giving the index triples for values (a, b, c) in that order, and a `Triple` whose `is_single` says whether exactly one divides the sum |
| `count_iter.kara` | the values held `filter`ed from 1 to 100, every ordered triple reached by nested `flat_map`s, kept by `filter` when one of the three divides the sum (`count` over the three), `map`ped to its index triples and `sum`med |
| `count_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i64` out, a `[i64; 101]` tally indexed `as usize`, loops over `1..=100usize`, the divisors summed from `bool`s cast `as i32`, and the index triples by a `match` on which values are alike; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and three
more (three numbers single in every order, one value with one other, and
every value from 1 to 100 once), each with its answer; then a checksum
of 200 random arrays of 3 to 60 numbers up to 6, 20 and 100 in turn;
then the constraints' longest, 10^5 numbers up to 100 and 10^5 numbers
of two values. `count.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in two rounds of 9 and 2 edits: first
`Vec<i32>` to `Vec[i32]` twice, `for &x in &nums` to `for x in ref
nums`, `|&x|` to `|x|`, `struct Solution;` to `struct Solution {}` and
`Solution::` to `Solution.`; then the two `0i64` to `0`.

The template loops `for a in 1..=100usize`, as Rust writes it, and adds
and divides the counters. Until kara `B-2026-11-15-39` that passed the
check and then stopped both backends with invalid MIR: the loop's
counter took the unsuffixed start's `i64` while the checker had typed it
`usize`. The fixed counter takes the suffixed end's type.

The iter arm's closures each hand on an iterator over the values, so the
arm binds `let held = ref values;` and the closures capture the view. A
closure over the vector itself passes the check but takes the vector by
move on every call of the outer closure, which stops the interpreter and
double-frees in a compiled build; that is kara `B-2026-11-15-32`, found
by kata 2174, and the arm names it.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every ordered triple of distinct indices tried and counted
when exactly one of its three numbers divides their sum; no tally. It
checks 300 random arrays of 3 to 30 numbers up to 6, 20 and 100 in
turn; then 30 of one number repeated; then 30 of two numbers. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | it is a multiple of 6, the orders of three indices, and at most n (n - 1) (n - 2) |
| P3 | the array reversed: the same count |
| P4 | every number multiplied by the largest factor that keeps them all at most 100: the same count |
| P5 | one more number x appended: the count grows by 3 times the ordered pairs of other indices that make a single divisor triplet with x |
| P6 | each arm agrees with at least three of the other five |

P4 holds because multiplying all three numbers by one factor multiplies
their sum by it too, so the same ones divide it. P5's growth is counted
by the literal reading, from the pairs of old indices only.

The differential prints `360 cases: checksum 374939297, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading over
`itertools.permutations` of the indices. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm, five to each of
the sorted, distinct, struct and iter arms and to the template arm, each
run under `karac __mir-llvm-run`, and the kept ones under `karac
__mir-run` too. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: two divisors counted as single | P1 251, P2 163, P5 220, P6 251 |
| M5 | ★: the sum without c above 50 | P1 90, P2 54, P4 191, P5 188, P6 90 |
| M6 | ★: the last number not tallied | P1 285, P3 232, P5 294, P6 285 |
| M7 | sorted: three distinct values in 3 orders | P1 276, P2 135, P5 292, P6 276 |
| M9 | sorted: the pair alike at the top taken from the bottom | P1 220, P2 106, P5 35, P6 220 |
| M10 | sorted: c from a when b is above 50 | P1 43, P4 152, P5 38, P6 43 |
| M12 | distinct: the tally one short for repeats | P1 249, P5 244, P6 249 |
| M13 | distinct: the second step keyed on the value | P1 286, P2 237, P4 172, P5 256, P6 286 |
| M15 | distinct: the hits with c twice | P1 286, P2 192, P5 299, P6 286 |
| M17 | struct: all three dividing taken as single | P1 248, P5 29, P6 248 |
| M18 | struct: the first count stepped down | P1 225, P2 195, P5 37, P6 225 |
| M19 | struct: the held values from 2 | P1 156, P4 138, P5 159, P6 156 |
| M22 | iter: the inner values from the outer one | P1 288, P2 220, P5 296, P6 288 |
| M24 | iter: the sum without a | P1 290, P2 192, P5 300, P6 290 |
| M25 | iter: the third not stepped for the second | P1 290, P2 256, P5 272, P6 290 |
| M27 | solution: the adapter's numbers capped at 99 | P1 15, P4 57, P5 15, P6 15 |
| M28 | solution: a == c paired with b | P1 230, P2 154, P5 182, P6 230 |

P1, P5 and P6 kill all seventeen, P2 eleven, P4 five and P3 one. P2
misses the six edits whose counts stay multiples of 6 within the bound:
the last number not tallied, c from a, the tally one short, all three
dividing taken as single, the held values from 2 and the numbers capped
at 99 (M6, M10, M12, M17, M19, M27). P4 scales every number, so it kills
the five that treat a value by its size (M5, M10, M13, M19, M27). P3
reverses the array, which a tally cannot see, and kills only the edit
that drops the last number (M6).

Of the thirty-one, fourteen were not kept. Eleven are killed and fail as
a kept one does or are left out for the count of three: the ★ arm's
second count not stepped down and the distinct arm's third not stepped
for the first (M1, M16) as M25; the ★ arm's values to 99 (M4) as M27;
the distinct arm's third entry from the second (M14) as M22; the iter
arm's two divisors kept, which keeps three too (M23), as M17; the
template's two divisors taken (M29) as M3; and five that fail their own
way, the sorted arm's divisor counted once per value (M11), the struct
arm's c taken as the first value and a value tallied twice (M20, M21),
and the template's first pair alike counted unordered and one value
never counted (M30, M31).

Three survive, and each is equivalent. The ★ arm's third count stepped
down once at most (M2) differs only when all three values are alike,
which is never single. The sorted arm's pair alike at the bottom counted
unordered (M8) changes a branch no single triple reaches: for a = b < c,
a divides 2a + c exactly when c is a multiple of a, and c divides it
only when c = 2a, a multiple of a; so either both a's divide or c alone
cannot. The iter arm's values taken in from the next one (M26) adds
values the array lacks, whose count of 0 zeroes every product they
enter.

## Verification

Every arm prints the same output as `count.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.8 s to 13 s, the iter arm 49 s,
as it makes a tuple for each of the 10^6 ordered triples of values on
each of the long arrays, and the differential 136 s.

## Benchmarks

The bench builds 20 arrays of 10^5 numbers once, each drawn up to its
own top from 81 to 100, then counts each of them 10 times over with the
★ arm in all five languages. Every implementation prints `10 passes over
20 arrays: checksum 354678406`.

BENCHTAB
