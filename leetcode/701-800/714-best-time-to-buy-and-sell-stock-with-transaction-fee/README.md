# 714. Best Time to Buy and Sell Stock with Transaction Fee

You are given an array `prices` where `prices[i]` is the price of a
given stock on the ith day, and an integer `fee` representing a
transaction fee. Find the maximum profit you can achieve. You may
complete as many transactions as you like, but you need to pay the
transaction fee for each transaction. You may not hold more than one
share at a time (you must sell the stock before you buy again), and the
fee is charged once for each purchase and sale.

```
prices = [1, 3, 2, 8, 4, 9],  fee = 2  ->  8   (buy 1, sell 8; buy 4, sell 9)
prices = [1, 3, 7, 5, 10, 3], fee = 3  ->  6
```

**Constraints:** 1 <= `prices.length` <= 5 * 10^4; 1 <= `prices[i]` <
5 * 10^4; 0 <= `fee` < 5 * 10^4.

## Approaches

After any day the trader either holds nothing or holds one share, and
the best money in each of those two states depends only on the best
money in both the day before. Every arm is that recurrence, run
forwards, backwards or folded into one running price.

| file | mechanism |
|---|---|
| `best_time_to_buy_and_sell_stock_with_transaction_fee.kara` ★ | two running values, `cash` holding nothing and `hold` holding a share: cash takes yesterday's hold sold today less the fee if that is more, hold takes today's cash spent on a share if that is more; O(n) time, O(1) space |
| `best_time_to_buy_and_sell_stock_with_transaction_fee_table.kara` | the same two values kept for every day in a table, each row computed only from the one before; O(n) space |
| `best_time_to_buy_and_sell_stock_with_transaction_fee_greedy.kara` | one running buy price with the fee included: a lower price plus fee replaces it, a higher price is sold for the difference and becomes the buy price with no new fee, so a sale made too early is extended for free if the price keeps rising |
| `best_time_to_buy_and_sell_stock_with_transaction_fee_suffix.kara` | the two states from the last day backwards: the most to be made from day i on holding nothing, which can wait or buy, and holding a share, which can wait or sell and pay the fee |
| `differential.kara` | the four arms against the definition, four properties |

The ★ arm updates hold from the cash it has just updated, which would
buy back on the day of a sale; that never helps, since it only pays the
fee, so it never wins and the order is safe.

Every arm prints the same 16 lines: the two LeetCode examples; one day;
falling and rising prices, the rising ones at fees of 0, 3 and 4; a
zigzag at fees of 0, 3 and 4, the last of which takes a swing's whole
gain; a mixed list; a 50,000-day random walk, the problem's most, at
fees of 0, 50 and 49,999; 50,000 random prices with a fee of 1,000; and
500 random price lists with a checksum.
`best_time_to_buy_and_sell_stock_with_transaction_fee.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which uses no states at all: it tries every set of an even number of
days, reads them in order as buy, sell, buy, sell, and totals each sale
less its purchase and the fee; the answer is the best total, or 0 for no
trade. 3,000 lists are checked, each 1 to 11 days of prices from 1 up to
1 to 20, with a fee from 0 to 5.

| | property |
|---|---|
| P1 | the profit is the definition's |
| P2 | every price raised by the same amount, from 1 to 1,000, gives the same profit |
| P3 | every price and the fee doubled doubles the profit |
| P4 | a fee one higher loses nothing to gain, and at most one for each of the at most n / 2 trades |

It prints `3000 price lists (1814 with a profit), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run`. All eleven are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no fee charged on a sale | P1 1930 |
| M2 | ★: the first day's share held for nothing | P1 2276, P2 2722 |
| M3 | ★: the worse purchase kept | P1 1586, P4 13 |
| M4 | table: a sale made from the day with no share | P1 2276, P2 2722, P4 1529 |
| M5 | table: a purchase made while already holding | P1 1473 |
| M6 | table: the last day read holding a share | P1 3000, P2 3000 |
| M7 | greedy: a fee charged again when a trade runs on | P1 476, P4 66 |
| M8 | greedy: a cheaper start sought without the fee | P1 308, P4 34 |
| M9 | suffix: no fee charged on a sale | P1 1930 |
| M10 | suffix: a purchase leading to the free state | P1 1814 |
| M11 | suffix: the answer read holding a share | P1 2516, P2 2998, P4 241 |
| E1 | greedy: a sale at the running price taken too | 0 |
| E2 | ★: a tie taken as a sale | 0 |
| E3 | suffix: a tie taken as a purchase | 0 |

P1 kills all eleven, and is the only property that sees four of them.
M1 and M9 charge no fee, and M5 and M10 never trade more than once or
never at all; all four are still a consistent rule for some other
problem, so lifting the prices, doubling them, or raising the fee does
what those properties expect. P2 sees the mutants that end up counting a
share's price as money, M2, M4, M6 and M11, since lifting the prices
lifts that too. P4 catches the ones whose answer can rise with the fee
or fall by more than a trade's worth, M3, M4, M7, M8 and M11. P3 kills
nothing: every mutant still builds its answer from sums and differences
of prices and the fee and comparisons between them, so doubling every
input doubles its answer as well. It is kept because a mistake that adds
a constant would fail it, and none of these does. E1 also sells at a
price equal to the running buy price, earning nothing and leaving the
buy price where it was; E2 and E3 break ties the other way, which gives
the same number.

## Verification

Every arm prints the same output as
`best_time_to_buy_and_sell_stock_with_transaction_fee.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`4ac59f62cb`, whose last compiler change is `500dff0834`. No
`runtime/src` change has landed since the runtime archives were built.

The sanitizer lane cannot see a leak (kara B-2026-10-18-31), so the leak
check copied each arm's and the differential's lane executable as it was
linked and ran it with the preloaded shim from kata 708, which refuses
the lane's hand-made stack so that LeakSanitizer sees `main` (kata
708 showed it reporting a leak the lane misses): all five print their
output and report no leak.

The frozen legacy backends run all four arms and print the same output
under `karac run --interp`, `karac run`, `karac build` and a
`KARAC_AUTO_PAR=1` build, with an ownership warning at the harness's
second `max_profit(walk, ...)` that `walk` was moved by the first; under
v2 a bare parameter borrows, so nothing moves and v2 rightly says
nothing. They build and run the bench program too. They refuse the
differential at type checking, at `*p` over `iter()`, since legacy gives
those items by value where v2 gives references. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes ten
random walks of 100,000 days once, starting at 50,000 with daily steps
of up to 10 up to 100, and trades each in 300 rounds at a fee of 3 times
the round, so no round repeats another's work, summing the profits.
Every implementation prints `300 rounds of 10 walks of 100000 days: sum
656473922`, the Kāra program under `karac __mir-run` included (in 72 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.69 to 0.74 s |
| Rust (`rustc -O`) | 0.64 to 0.74 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.64 to 0.75 s |
| Go | 0.63 to 0.76 s |
| Python | 18.2 to 19.6 s |
| Kāra (`karac build --mir`) | 0.65 to 0.75 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds it as well (above).
That edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.1 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So all five compiled programs are level, and the legacy build too, at
0.61 to 0.75 s. Each day is a chain: today's cash needs yesterday's hold
and today's hold needs today's cash, so the loop runs at the speed of
that chain, not of its instruction count. Under valgrind's cachegrind C
and Rust run 3.62 billion instructions and 151 million branches each,
few enough that their two comparisons must be conditional moves; the
v2 build runs 4.83 billion and 906 million, about three branches a day,
so it keeps them as branches. On these walks those branches are
predicted almost perfectly, 15 thousand misses in all, so they cost
nothing here; on prices that swing unpredictably they would. That is
inferred from the counts, not traced. The comparison with C and Rust
waits until after M4.

## Compiler findings

None new.
