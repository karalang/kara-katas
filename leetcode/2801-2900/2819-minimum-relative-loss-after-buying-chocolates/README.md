# 2819. Minimum Relative Loss After Buying Chocolates

You are given an integer array `prices`, which shows the chocolate
prices and a 2D integer array `queries`, where `queries[i] = [ki, mi]`.

Alice and Bob went to buy some chocolates, and Alice suggested a way to
pay for them, and Bob agreed.

The terms for each query are as follows:

- If the price of a chocolate is **less than or equal to** `ki`, Bob
  pays for it.
- Otherwise, Bob pays `ki` of it, and Alice pays the **rest** of it.

Bob wants to select **exactly** `mi` chocolates such that his
**relative loss** is **minimized**, more formally, if, in total, Alice
has paid `ai` and Bob has paid `bi`, Bob wants to minimize `bi - ai`.

Return *an integer array* `ans` *where* `ans[i]` *is Bob's **minimum
relative loss** possible for* `queries[i]`.

```
prices = [1,9,22,10,19],     queries = [[18,4],[5,2]]                 ->  [34,-21]
prices = [1,5,4,3,7,11,9],   queries = [[5,4],[5,7],[7,3],[4,5]]      ->  [4,16,7,1]
prices = [5,6,7],            queries = [[10,1],[5,3],[3,3]]           ->  [5,12,0]
```

**Constraints:** `1 <= prices.length == n <= 10^5`; `1 <= prices[i]
<= 10^9`; `1 <= queries.length <= 10^5`; `queries[i].length == 2`; `1
<= ki <= 10^9`; `1 <= mi <= n`.

## Approaches

A chocolate at price p adds p to Bob's loss when p <= k and k - (p - k)
= 2k - p past it: the loss rises with the price up to k and falls after
it, so over the sorted prices the m least losses are some l cheapest
and the m - l dearest.

| file | mechanism |
|---|---|
| `loss.kara` ★ | the prices sorted with prefix sums, and per query a binary search for l: the first cheap price whose sum with the dear price it would displace reaches 2k; the loss read off the prefix sums, O(log n) a query |
| `loss_ends.kara` | the prices sorted, and per query m steps from both ends, each taking the cheapest or the dearest left by the smaller loss; O(m) a query |
| `loss_splits.kara` | the prices sorted with prefix sums in a `Shop` struct whose method sums a range's losses either side of the first price above k, found by `partition_point`; per query every l from 0 to m tried, the least kept by `min()`; O(m) a query |
| `loss_each.kara` | per query each chocolate's loss, the losses sorted and the first m summed by a slice's `iter().sum()`: the choice is free, so the m least are the answer; O(n log n) a query |
| `loss_solution.kara` | a Rust solution as LeetCode's Rust users write it: the `i32` prices sorted, `i64` prefix sums, and per query a binary search over `usize` bounds `(mut l, mut r)`, the answers pushed into a `Vec::with_capacity`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; one
chocolate at k and past it; 2000 prices rising by 1000 with 200 queries
of m = 1000 and k stepping by 10000, as a checksum; 3000 random shops
of 1 to 10 prices up to 30 with 3 queries each, and 50 of up to 1000
prices up to 10^9 with 50 queries each, as checksums. `loss.py`
mirrors the ★ arm and its output is byte-identical.

```
[34, -21]
[4, 16, 7, 1]
[5, 12, 0]
[7, -1]
909058238
3000 small shops: checksum 967080752
50 large shops: checksum 620975189
```

Losses go below 0, so every checksum folds with `((h * 31 + a) % M +
M) % M`: Kāra's `%`, like Rust's, C's and Go's, takes the dividend's
sign, and Python's the divisor's, and the second `% M` makes them
agree.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every choice of exactly m chocolates by a bit mask, Bob
paying `min(p, k)` of each and Alice `max(p - k, 0)`, and the least of
Bob's total less Alice's. It draws 2000 random shops of 1 to 10 prices
up to 30 with 3 queries, then 50 of up to 600 prices up to 10^9 with 20
queries, all before any arm answers; the literal reading is asked only
of the first 2000.

| | property |
|---|---|
| P1 | up to 10 prices, every answer is the literal reading's |
| P2 | m = n: the losses of every chocolate summed |
| P3 | the prices reversed: the same answers |
| P4 | the queries reversed: the answers reversed |
| P5 | for 2 <= m < n, the answer at m + 1 less the answer at m is at least the answer at m less the answer at m - 1: the losses come in rising order |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 770362167, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, by `itertools.combinations`, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pair's sum held against k, not 2k | P1 1753, P2 1830, P5 531, P6 1803 |
| M2 | ★: the dear ones charged k, not 2k | P1 1849, P2 1962, P5 511, P6 1899 |
| M3 | ends: the dearest's loss read as its price | P1 1523, P5 1115, P6 1573 |
| M4 | ends: a dear chocolate's loss as k - p | P1 1888, P2 1938, P6 1938 |
| M5 | splits: every chocolate from the cheap end never tried | P1 1126, P6 1176 |
| M6 | splits: a range past the cut measured from the cut | P1 1888, P2 1938, P5 1115, P6 1938 |
| M7 | each: the m greatest losses summed | P1 1764, P5 1463, P6 1814 |
| M8 | each: Alice's share left out | P1 1827, P2 1938, P6 1877 |
| M9 | solution: the dear end summed over all m | P1 1866, P2 1960, P5 464, P6 1916 |
| M10 | solution: the prices never sorted | P1 1627, P2 1470, P3 1826, P5 1039, P6 1677 |

## Benchmarks

The bench draws 10 shops of 10^5 prices up to 10^9, LeetCode's most,
each with 10^5 queries, all of them first, then answers each shop's
queries 3 times by the ★ arm in all five languages. C sorts by `qsort`,
Go by `slices.Sort`. Every implementation prints `10 shops of 100000, 3
rounds: 1316112 losses below 0, checksum 76303591`.

BENCHTAB

## Verification

All five arms print the same output as `loss.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the four own arms checked clean as first written. The splits
arm started its prefix sums as `vec![0]`, and `karac check` reported
W0245, `vec![..]` deprecated for the list literal; `karac fix` made it
`[0]`. The differential first read `let value = got[arm];` out of a
`Vec[Vec[i64]]`, and `karac check` refused it as
E_INDEX_MOVE_NON_COPY, a move out of an index; the binding is only
read, and `karac fix` made it `ref got[arm]`.

LeetCode's Rust template took 36 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `prices`
became `own Vec[i32]`, since the body rebinds it as `let mut` and sorts
it; `Vec<..>` became `Vec[..]` and `vec![0i64; n + 1]` `Vec.filled(n +
1, 0)`; `Vec::with_capacity` became `Vec.with_capacity`; `as usize`
became `as i64`, and the `as i64` casts on the `i32` prices went, the
values widening implicitly; `let (mut l, mut r) = (0usize, m)` became
`let mut (l, r) = (0, m)`; `|&p|` and `|&v|` lost their `&`; and
`Solution::` took `.`.
