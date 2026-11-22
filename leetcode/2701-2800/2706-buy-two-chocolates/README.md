# 2706. Buy Two Chocolates

You are given an integer array `prices` representing the prices of
various chocolates in a store. You are also given a single integer
`money`, which represents your initial amount of money.

You must buy **exactly** two chocolates in such a way that you still
have some **non-negative** leftover money. You would like to minimize
the sum of the prices of the two chocolates you buy.

Return *the amount of money you will have leftover after buying the two
chocolates*. If there is no way for you to buy two chocolates without
ending up in debt, return `money`. Note that the leftover must be
non-negative.

```
prices = [1,2,2], money = 3  ->  0
prices = [3,2,3], money = 3  ->  3
```

**Constraints:** `2 <= prices.length <= 50`, `1 <= prices[i] <= 100`,
`1 <= money <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `chocolates.kara` ★ | only the two cheapest chocolates matter: if the money covers them, what is left is the most that can be; if not, no pair is affordable and the money stays whole. One pass keeps the cheapest and the next cheapest, starting above the dearest price, 100. O(n) |
| `chocolates_sorted.kara` | a sorted copy of the prices puts the two cheapest first. O(n log n) |
| `chocolates_pairs.kara` | every pair of two different chocolates priced, and the most money any affordable pair leaves kept, starting from the money itself for when none is. O(n^2) |
| `chocolates_iter.kara` | the cheapest price by `min`, then the cheapest of the rest by `enumerate`, a `filter` skipping the first index that held it, and `min` again. O(n) |
| `chocolates_solution.kara` | a Rust solution as LeetCode's Rust users write it, `sort_unstable` on a `mut` parameter and an `if` on the sum, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; the two
cheapest exactly the money; two of the dearest against all the money;
49 of the dearest and one of the cheapest; 50 prices falling from 50;
then the money left summed and a checksum for 5000 random cases of 2 to
50 prices up to 100 and money up to 100, and 5000 of 2 to 5 prices up
to 10 and money up to 20. `chocolates.py` mirrors the ★ arm and its
output is byte-identical.

```
0
3
0
100
100
97
5000 cases: money left sums to 197656, checksum 739476039
5000 cases of 2 to 5 prices up to 10: money left sums to 30146, checksum 723393076
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of chocolates, as a mask over the prices, that
holds exactly two and leaves the money non-negative, and the most money
any leaves, or all of it when there is none. It checks 1000 random cases
of 2 to 10 prices up to 12 and money up to 25, then 500 of 2 to 50
prices up to 100 and money up to 100. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | up to 10 prices, the answer is the literal reading's |
| P2 | the answer is the money, or between 0 and the money less 2 |
| P3 | the prices rotated: the same answer |
| P4 | where two are bought, 1 to 10 more money: that much more left |
| P5 | a price of 100 added: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1500 cases: checksum 616091587, 45000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases over every pair gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M2 and M4 are one fault in two arms, an exact
spend refused, and so are M3 and M5, the cheapest bought twice; each
pair fails the same cases.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cheapest replaced without passing down | P1 211, P3 331, P6 347 |
| M2 | ★: an exact spend refused | P1 46, P6 58 |
| M3 | sorted: the cheapest bought twice | P1 625, P6 1001 |
| M4 | sorted: nothing left counted as unaffordable | P1 46, P6 58 |
| M5 | pairs: a chocolate paired with itself | P1 625, P6 1001 |
| M6 | pairs: the least money left kept | P1 639, P4 797, P6 1005 |
| M7 | iter: the dearest taken as the first | P1 713, P5 557, P6 1115 |
| M8 | iter: an unaffordable pair leaves nothing | P1 228, P2 29, P4 325, P6 325 |
| M9 | solution: the prices never sorted | P1 638, P3 567, P6 1037 |
| M10 | solution: the last two prices after sorting | P1 720, P5 293, P6 1122 |

## Benchmarks

The bench draws `10^5` lists of 50 prices up to 100 with money up to
100, LeetCode's largest, all of them first, then answers each 10 times
by the ★ arm in all five languages. Every implementation prints `100000
lists of 50 prices, 10 rounds: money left sums to 44248480, checksum
481244905`.

BENCHTAB

## Verification

All five arms print the same output as `chocolates.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four arms of our own checked clean as first written.

LeetCode's Rust template took one `karac fix` of 7 edits: `struct
Solution {}` added, `Vec<i32>` respelled `Vec[i32]`, and the `mut
prices` parameter, which Kāra does not have, became `prices: own
Vec[i32]` with a `let mut prices = prices;` rebinding, since sorting in
place needs the vector owned. `sort_unstable` became `sort`. The
wrapper's `as i64` on the `i32` answer was dropped, since it widens by
itself.
