# 2517. Maximum Tastiness of Candy Basket

You are given an array of positive integers `price` where `price[i]`
denotes the price of the `i`th candy and a positive integer `k`.

The store sells baskets of `k` **distinct** candies. The **tastiness**
of a candy basket is the smallest absolute difference of the **prices**
of any two candies in the basket.

Return *the **maximum** tastiness of a candy basket.*

```
price = [13,5,1,8,21,2], k = 3  ->  8
price = [1,3,1], k = 2          ->  2
price = [7,7,7,7], k = 2        ->  0
```

**Constraints:** `2 <= k <= price.length <= 10^5`; `1 <= price[i] <=
10^9`.

With the prices sorted, a basket of `k` whose closest two differ by at
least `d` exists exactly when the greedy pick, the cheapest and then
each next price at least `d` above the last picked, reaches `k`: any
basket can be moved onto the greedy's picks one candy at a time. That
gets only harder as `d` grows, so the greatest such `d` is searched for.
The approaches differ in how the search and the greedy pick are run.

## Approaches

| file | mechanism |
|---|---|
| `tastiness.kara` ★ | the greatest `d` bisected in `[0, (greatest - least) / (k - 1)]`, each test a greedy scan of the sorted prices. O(n log n + n log M) |
| `tastiness_jumps.kara` | the same bisection, but the greedy jumps straight to the next price at least `d` above the last by a `partition_point`, so a test costs O(k log n) |
| `tastiness_bits.kara` | the answer built a bit at a time from `2^29` down, each bit kept when the basket still fits, the greedy run from the dearest price down |
| `tastiness_rec.kara` | recursion: the bisection a function of its range, into the upper half when the middle fits and the lower half when it does not. About 30 deep |
| `tastiness_iter.kara` | iterators: the greedy a `fold` over the sorted prices carrying the count and the last picked, and the answer a `fold` over the bits from `2^29` down |
| `tastiness_solution.kara` | LeetCode's Rust template: `Vec<i32>` and `i32` in, `i32` out; `mut price` sorted in place, a bisection over `i32` with the greedy pick as a closure over the prices; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's three examples and five
more; then 2000 random lists of 2 to 10 prices to 20, and 2000 of 2 to
1000 prices to `10^9`, each with `k` from 2 to the length, as the sum of
the answers and a checksum; then the constraints' largest, `10^5`
prices: random to `10^9` with `k` 2, 1000 and `10^5`; and 1 to `10^5`
with `k` 50000 and 50001. `tastiness.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked on 3000 random
lists of 2 to 9 prices to 30 with every `k` against the best of every
basket's least difference, and the two agreed on every list.

`check` first reports 7 errors on the template: `struct Solution;`, the
`mut price` parameter, `Vec<i32>` in angle brackets, the closure's `->
bool`, the `&p` pattern, and the `mut lo` and `mut hi` inside `let (mut
lo, mut hi)`. `karac fix` carries it in one call, reporting 13 edits:
`struct Solution {}`; the parameter becomes `price: own Vec[i32]` with
`let mut price = price;` as the body's first line, since the body sorts
the vector it was given; the brackets; the `-> bool` dropped, a
closure's type being inferred; the `&` dropped; `let mut (lo, hi) =
(0i32, ...)`, the `0` given `i32` beside the `i32` spread;
`sort_unstable` becomes `sort`; and the wrapper's lossless `as i64`
dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every basket of `k` distinct candies, chosen by a recursion
that takes or skips each candy in turn, its tastiness the smallest
difference of any two in it found by comparing every pair; the answer
is the greatest tastiness. No sort and no bisection. It checks 300
random lists of 2 to 8 prices to 30 with `k` from 2 to the length; then
20 of 8 prices from 1 to 3, and 40 of 8 prices to `10^6`, `k` 4. All
360 are drawn before any arm answers, and 35 of them have a tastiness of
0.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | from 0 to `(greatest - least) / (k - 1)` |
| P3 | the prices in the reverse order: the same answer |
| P4 | every price doubled: twice the answer |
| P5 | one more candy, while `k` is below `n`: at most the answer |
| P6 | each arm agrees with at least three of the other five |

P2's bound holds because the `k - 1` gaps between a basket's sorted
prices add up to at most the whole spread.

The differential prints `360 cases, 35 with a tastiness of 0: checksum
747988492, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and takes the best of every
basket. On a failure it prints the first ten and then the count by
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
| M1 | ★: the sort left out | P1 276, P3 172, P4 5, P6 276 |
| M2 | ★: a pick at d - 1 | P1 202, P4 239, P6 202 |
| M5 | ★: a fitting mid one past | P1 185, P2 60, P4 241, P5 1, P6 185 |
| M8 | jumps: one jump fewer | P1 189, P4 93, P6 189 |
| M9 | jumps: each jump from the cheapest | P1 202, P4 118, P6 202 |
| M11 | jumps: the sort left out | P1 278, P3 160, P4 2, P6 278 |
| M13 | bits: the dearest not counted | P1 313, P6 313 |
| M14 | bits: the cheapest never looked at | P1 260, P6 260 |
| M16 | bits: a pick at d + 1 | P1 325, P4 325, P6 325 |
| M17 | rec: fits at k - 1 | P1 230, P2 170, P6 230 |
| M20 | rec: the last picked kept at the first | P1 209, P2 184, P6 209 |
| M21 | rec: the top half the spread | P1 114, P4 64, P6 114 |
| M22 | iter: bit 0 never tried | P1 192, P4 192, P6 192 |
| M23 | iter: two skipped | P1 139, P6 139 |
| M24 | iter: a pick at d - 1 | P1 360, P2 158, P4 360, P6 360 |
| M27 | solution: the sort left out | P1 275, P3 173, P6 275 |
| M29 | solution: a fitting mid one past | P1 181, P2 63, P4 233, P6 181 |

P1 and P6 kill all seventeen, P4 eleven, P2 five, P3 three, the three
sorts left out, and P5 one, the ★ arm's fitting mid one past.

One of the first thirty-one edits was replaced for crashing: with the
rec arm's sort left out, the spread from the first price to the last
can be below 0, the bisection's range then never closes, and the
recursion runs out of stack on both backends. It became the count from
2 (M18).

Fourteen are not kept, and none survives. Ten fail exactly as a kept
one: the ★ arm's count from 0, the iter arm's fits past `k` and the
template's `cnt` from 0 (M3, M25, M28) as the bits arm's dearest not
counted (M13), each needing one candy more; the jumps arm's jump past
an equal price and the rec and template arms' pick at `d + 1` (M7, M19,
M31) as the bits arm's (M16); the jumps arm's end reached as a fit (M10)
as its each jump from the cheapest (M9); the bits arm's bit 0 never
tried (M12) as the iter arm's (M22); the rec arm's count from 2 (M18) as
its fits at `k - 1` (M17), the same test; and the template's top half
the spread (M30) as the rec arm's (M21). The bits arm's bit kept when it
fails and the iter arm's bits kept the other way (M15, M26) fail as
each other. Two fail in ways of their own, but their arm already holds
its kept edits: the ★ arm's top over `k` and last picked never moved
(M4, M6).

## Verification

Every arm prints the same output as `tastiness.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 7.2 to 123.8 s, the jumps arm's `partition_point` closures the slowest, and the differential 1.7 s; under `karac __mir-llvm-asan` the arms take 2.2 to 14.6 s and the differential 0.7 s; and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds 20 random lists of `10^5` prices to `10^9` once from
its own generator, then makes 3 passes. Each pass asks every list with
`k` from 2 to 1001, `check % 1000 + 2`, folding each answer plus the
pass into the checksum. The bench uses the ★ arm in all five languages.
Every implementation prints `3 passes over 20 lists of 10^5 prices:
checksum 517805988`.

BENCHTAB
