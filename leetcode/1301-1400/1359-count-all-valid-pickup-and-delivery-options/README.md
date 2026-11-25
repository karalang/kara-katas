# 1359. Count All Valid Pickup and Delivery Options

Given `n` orders, each order consists of a pickup and a delivery
service.

Count all valid pickup/delivery possible sequences such that
delivery(i) is always after of pickup(i).

Since the answer may be too large, return it modulo `10^9 + 7`.

```
n = 1  ->  1     (P1, D1)
n = 2  ->  6     (P1,P2,D1,D2), (P1,P2,D2,D1), (P1,D1,P2,D2), (P2,P1,D1,D2), (P2,P1,D2,D1), (P2,D2,P1,D1)
n = 3  ->  90
```

**Constraints:** `1 <= n <= 500`.

Each arm is `fn count_orders(n: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `count_orders.kara` ★ | the orders added one at a time. With i - 1 orders placed, their 2i - 2 events leave 2i - 1 gaps; the i-th pickup and delivery go into them in (2i - 1) + (2i - 2) + .. + 1 = i (2i - 1) ways with the pickup first, so the count is the product of i (2i - 1), modulo 10^9 + 7. O(n) |
| `count_orders_dp.kara` | the events put in order one at a time, counting by how many orders wait to be picked up and how many are on the way: from p waiting and d on the way, any of the p can be picked up, or any of the d delivered. O(n^2) |
| `count_orders_factorial.kara` | of the (2n)! orders of the 2n events, each pair comes pickup first in exactly half, and the pairs are independent, so the count is (2n)! / 2^n; the division is a multiplication by the inverse of 2^n, 2^n raised to p - 2 by Fermat's little theorem. O(n + log p) |
| `count_orders_gaps.kara` | the ★ arm's gaps counted one by one: the i-th pickup goes into one of the 2i - 1 gaps, and its delivery into any place after it. O(n^2) |
| `count_orders_solution.kara` | a Rust solution as LeetCode's Rust users write it (`const MOD: i64 = 1_000_000_007;` and `for i in 1..=n as i64 { ans = ans * i % MOD * (2 * i - 1) % MOD; }`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, 4, 10 and
500, the constraints' largest (`1 6 90 2520 850728840 764678010`); and
every n from 1 to 500 folded into a checksum (`n from 1 to 500:
checksum 916208766`). `count_orders.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, dp and gaps arms check clean. The factorial arm
was written `power(power(2, n as i64), MOD - 2)` with `power` taking
`i64`s; `karac check` warns that the cast is unnecessary, an `i32`
widening to `i64` implicitly (W0310, `lossless_cast`), and `karac fix`
drops it. The Rust solution takes one fix: `struct Solution;` becomes
`struct Solution {}`. `1_000_000_007`, with its digit separators, and
`1..=n as i64` stand as Rust wrote them. Every arm matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the 2n events put in order one at a time, any waiting pickup
or the delivery of any order on the way next, every choice followed and
counted when all are placed, with a memo on which orders are waiting,
on the way and delivered. That reading is exact but takes 3^n states,
so it answers n up to 8; the other properties cover every n from 1 to
500, the constraints' whole range.

| | property |
|---|---|
| P1 | the statement read literally, for n up to 8 |
| P2 | one order more: the count times (n + 1)(2n + 1), the new pair's places among the 2n + 1 gaps |
| P3 | each pair in order in half of the (2n)! orders: the count times 2^n is (2n)! |
| P4 | a residue modulo p, and not 0, since p is a prime above 2n |
| P5 | the orders' own order times the ways to pair the 2n places, n! (2n - 1)!! |
| P6 | the ★ arm's count |

All 12,535 checks pass on every arm: `500 values of n: checksum
853110611, 12535 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`. Python, counting
every permutation of the events for n up to 5 and the product of
i (2i - 1) above, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last order left out | P1 7, P2 499, P3 499, P5 499, P6 1996 |
| M2 | ★: the last product left unreduced | P1 1, P2 493, P3 490, P4 389, P5 491, P6 1964 |
| M3 | dp: the finished state counted twice | P1 8, P3 500, P5 500, P6 500 |
| M4 | dp: the modulus written 10^8 + 7 | P1 2, P2 494, P3 494, P5 494, P6 494 |
| M5 | factorial: 2^n's inverse one power short | P1 8, P2 499, P3 500, P5 500, P6 500 |
| M6 | factorial: 2^n taken as 4^(n / 2) | P1 4, P2 499, P3 250, P5 250, P6 250 |
| M7 | gaps: the pickup never in the first gap | P1 8, P3 500, P4 500, P5 500, P6 500 |
| M8 | gaps: the modulus written 10^6 + 7 | P1 3, P2 495, P3 495, P5 495, P6 495 |
| M9 | solution: the product reduced modulo p - 1 | P1 1, P2 493, P3 493, P5 493, P6 493 |
| M10 | solution: the modulus written 10^5 + 7 | P1 4, P2 496, P3 496, P5 496, P6 496 |

P1, P3, P5 and P6 kill all ten, P2 eight and P4 two. The edits that go
wrong only past some n are told apart by where they start: a modulus a
few digits short leaves every count below it alone, so 10^5 + 7 first
fails at n = 5, 10^6 + 7 at 6 and 10^8 + 7 at 7, and p - 1 and the
unreduced product only once the counts pass p, at n = 8; 4^(n / 2) is
wrong for odd n alone. One order more (P2) misses the two edits that
keep each count's ratio to the next: the finished state counted twice
doubles every count (M3), and the first gap skipped makes every count
0 (M7). A residue and not 0 (P4) catches that 0, and the unreduced
product, which no longer fits below p.

## Benchmarks

The bench asks 3 * 10^5 questions, each n from 1 to 500 drawn from the
checksum so far, so no answer carries over, answered by the ★ arm's
product and folded into the checksum. Every implementation prints
`300000 questions: checksum 77786248`. The work is two 64-bit
remainders for each order, the same in every language.

BENCHTAB
