# 2898. Maximum Linear Stock Score

Given a **1-indexed** integer array `prices`, where `prices[i]` is the
price of a particular stock on the `i`th day, your task is to select
some of the elements of `prices` such that your selection is
**linear**.

A selection `indexes`, where `indexes` is a 1-indexed integer array of
length `k` which is a subsequence of the array `[1, 2, ..., n]`, is
**linear** if:

- For every `1 < j <= k`,
  `prices[indexes[j]] - prices[indexes[j - 1]] == indexes[j] - indexes[j - 1]`.

The **score** of a selection `indexes` is equal to the sum
`prices[indexes[1]] + prices[indexes[2]] + ... + prices[indexes[k]]`.

Return *the **maximum** score that a linear selection can have*.

**Note** that the selection of one element is always considered linear.

```
prices = [1, 5, 3, 7, 8]  ->  20
prices = [5, 6, 7, 8, 9]  ->  35
```

**Constraints:** `1 <= prices.length <= 10^5`;
`1 <= prices[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `stock.kara` ★ | two chosen days are linear when the price rises by exactly the days between them, so `prices[i] - i` is the same for every day of a linear selection, and any set of days sharing it is one. Every price is positive, so the best takes a whole group: the prices summed under `prices[i] - i` in a `Map`, through `entry`, and the largest sum |
| `stock_index.kara` | the ★ arm's groups through `get` and index assignment rather than `entry`, and the best kept by a walk over the map |
| `stock_sorted.kara` | no map: each day as `(prices[i] - i, prices[i])`, the pairs sorted so each group lies in one run, and every run summed as it passes |
| `stock_chain.kara` | as a chain, day by day: the best linear selection ending on a day is its price plus the best ending on the last day before it with the same key, kept in a `SortedMap` |
| `stock_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `HashMap<i32, i64>` filled through `*map.entry(p - i as i32).or_insert(0) += p as i64`, then `*map.values().max().unwrap()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The grouping was checked first against every selection of 3000 random
arrays of up to 9 prices in Python, before any arm was written.

Every arm prints the same 4 lines: LeetCode's two examples; 10^5
prices, LeetCode's most, all 10^9, rising by one from 10^9 - 10^5 + 1,
and falling by one from 10^9; then 3000 random arrays of 1 to 8 prices
from 1 to 10, and 100 of 1000 to 10^5 prices, every other one a few
steps off a rise by one and the rest up to 10^9, as a total and a
checksum. `stock.py` mirrors the ★ arm and its output is
byte-identical.

```
20 35
1000000000 99995000050000 1000000000
3000 small arrays: scores total 30801, checksum 886287513
100 large arrays: scores total 109431354572, checksum 279097005
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every nonempty set of days tried as a bit mask, kept
when each chosen day's price rises from the one before by exactly the
days between them, and the largest sum kept. It draws 2000 random
arrays of 1 to 8 prices from 1 to 10, then 50 of up to 3000 prices,
every other one a few steps off a rise by one and the rest up to 10^9,
all before any arm answers; the literal reading is asked only of the
first 2000.

| | property |
|---|---|
| P1 | up to 8 prices, the answer is the literal reading's |
| P2 | from the largest price to the sum of all of them |
| P3 | a day added after the last at one more: from the answer to the answer plus that price |
| P4 | the first day cut: from the answer less that day's price to the answer |
| P5 | the array written again after itself, each price raised by n: from twice the answer to twice the answer plus n * n |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, scores total 25904154620: checksum
442219035, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python search over the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, three to the sorted arm, two each to
the ★ arm, the index arm and the chain, and one to the solution, each
run under `karac __mir-run` and `karac __mir-llvm-run`. All ten are
killed, each the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the key taken as price plus day | P1 975, P5 1554, P6 1000 |
| M2 | ★: the smallest group taken | P1 1686, P2 1688, P4 271, P6 1736 |
| M3 | index: a group's price replaced, not added | P1 705, P5 1909, P6 730 |
| M4 | index: the walk keeping the smaller | P1 2000, P2 2050, P6 2050 |
| M5 | sorted: a run never reset | P1 1714, P6 1764 |
| M6 | sorted: the pairs left unsorted | P1 406, P5 1469, P6 431 |
| M7 | sorted: the runs split by price | P1 984, P3 177, P4 82, P5 1857, P6 1009 |
| M8 | chain: a chain never extended | P1 705, P5 1909, P6 730 |
| M9 | chain: the key taken as price plus day | P1 975, P5 1554, P6 1000 |
| M10 | solution: the days counted, not their prices | P1 1971, P2 2015, P6 2021 |

## Benchmarks

The bench draws 20 arrays of 10^5 prices, LeetCode's most, half up to
10^9, every key its own group, and half a few steps off a rise by one,
50 groups, all first, then answers each 20 times by the ★ arm in all
five languages. Kāra's `Map` and Rust's `HashMap` both hash with
SipHash; Go's built-in map and Python's dict use their own; C has no
map, and probes a splitmix64 open-addressing table. Every implementation
prints `20 arrays of 100000, 20 rounds: scores total 751479136240,
checksum 614959035`.

BENCHTAB

## Verification

All five arms print the same output as `stock.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as written: `*sums.entry(..).or_insert(0)
+= p` and `sums.values().max().unwrap()` as a Rust author writes them.

LeetCode's Rust template took one `karac fix` run, the wrapper
included, and the diff shows these: `use std::collections::HashMap;` went, Kāra's `Map`
being in the prelude, and `struct Solution {}` came for the `impl`;
`Vec<..>` and `HashMap<..>` became `Vec[..]` and `Map[..]`, and
`HashMap::new()` `Map.new()`; `(i, &p)` and `|&x|` lost their `&`;
`Solution::` took `.`. The `*map.values().max().unwrap()` stayed as
written, and so did `p - i as i32` and `p as i64`.
