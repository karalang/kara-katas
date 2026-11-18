# 2291. Maximum Profit From Trading Stocks

You are given two **0-indexed** integer arrays of the same length
`present` and `future` where `present[i]` is the current price of the
`i`th stock and `future[i]` is the price of the `i`th stock a year in
the future. You may buy each stock at most **once**. You are also given
an integer `budget` representing the amount of money you currently
have.

Return *the maximum amount of profit you can make*.

```
present = [5,4,6,2,3], future = [8,5,4,3,5], budget = 10   ->  6
present = [2,2,5], future = [3,4,10], budget = 6           ->  5
present = [3,3,12], future = [0,3,15], budget = 10         ->  0
```

In the first, buying the 0th, 3rd and 4th stocks costs 10 and returns
`3 + 1 + 2 = 6`.

**Constraints:** `n == present.length == future.length`;
`1 <= n <= 1000`; `0 <= present[i], future[i] <= 100`;
`0 <= budget <= 1000`.

A 0/1 knapsack: a stock's weight is its price now and its value the
profit it makes, and a stock that makes none is never worth buying. One
row of the most profit for every budget from 0 up, run downwards for
each stock so that the stock is taken at most once. O(n * budget).

## Approaches

| file | mechanism |
|---|---|
| `profit.kara` ★ | `Vec.filled(budget + 1, 0)`, each stock that gains taken in by running `(cost..budget + 1).rev()` |
| `profit_naive.kara` | every set of stocks by recursion, each stock bought or not, a stock that does not fit skipped. O(2^n) |
| `profit_memo.kara` | the same recursion with its answers kept in a `Map[(i64, i64), i64]` keyed by the stock and the budget left, passed down as `mut ref` |
| `profit_struct.kara` | `struct Stock` with its `gain`; `struct Table` fills the full two-dimensional knapsack, a row per stock considered, each row cloned from the last and improved |
| `profit_iter.kara` | `zip` the prices, `filter` the stocks that gain, and `fold` the row through them, each stock `map`ping every budget to a new row and `collect`ing it |
| `profit_solution.kara` | LeetCode's Rust template: `Vec<i32>` twice and `i32` in, `i32` out; `vec![0; budget + 1]` over `usize` indexes, every stock taken in, a losing one never improving a cell; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; a budget
of 0; stocks that cost nothing; every stock at a loss or even; one
stock costing the whole budget against two cheap ones; then 2000 random
markets of 1 to 10 stocks, prices 0 to 100, budgets 0 to 400, with a
checksum and the profit in all. The harness keeps to 10 stocks so the
naive arm's 2^n sets stay cheap; the differential goes to 12.
`profit.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 12 edits:
`struct Solution;` to `struct Solution {}`; the brackets of the two
`Vec<i32>`, four edits; the `&` of `(&p, &f)` dropped twice;
`vec![0; budget + 1]` to `Vec.filled(budget + 1, 0i32)`, the `0` given
the `i32` that Rust inferred for it; the two `as usize` casts to `as
i64`, since Kāra indexes with `i64`; and in the adapter the `as i64` on
the template's `i32` answer dropped. The struct arm's `let last =
self.rows[..]`, which would move a `Vec` out of an index, was turned to
`ref self.rows[..]`: 1 edit.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of stocks, counted out as the bits of a number
from 0 to 2^n - 1; of those whose prices now come to at most the
budget, the most that the prices to come exceed the prices now. It
checks 300 random markets of 1 to 12 stocks with a budget of up to all
the prices now; then 30 where every stock but the first loses or breaks
even; then 30 whose budget is exactly the price of a random set of the
stocks. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `0 <= answer <=` the gains of all the stocks that gain, summed |
| P3 | a budget of every price now summed: just that sum of the gains |
| P4 | the stocks in the opposite order: the same answer |
| P5 | a stock that costs nothing and gains 7 added: 7 more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 622721447, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading by
`itertools.combinations`. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the budgets run upwards | P1 263, P2 256, P3 301, P6 263 |
| M3 | ★: the budget one short | P1 5, P3 32, P6 5 |
| M4 | ★: the gain the future price | P1 314, P2 284, P3 360, P6 314 |
| M7 | naive: a stock too dear bought anyway | P1 27, P6 27 |
| M9 | naive: the profit the price now | P1 313, P2 116, P3 359, P5 360, P6 313 |
| M10 | naive: a stock's own profit only | P1 220, P3 255, P5 285, P6 220 |
| M12 | memo: the memo read by the stock alone | P1 33, P4 20, P6 33 |
| M13 | memo: the memo stored by the stock alone | P1 1, P4 8, P6 1 |
| M15 | memo: a stock affordable only below the budget left | P1 5, P3 32, P5 4, P6 5 |
| M18 | struct: each row from the first | P1 271, P3 294, P4 214, P5 139, P6 271 |
| M20 | struct: the answer from the first column | P1 285, P3 321, P6 285 |
| M21 | struct: the stocks from the second | P1 133, P3 180, P4 203, P6 133 |
| M23 | iter: the price never taken off | P1 285, P2 259, P3 321, P6 285 |
| M24 | iter: the futures out of step | P1 297, P2 100, P3 330, P4 296, P5 358, P6 297 |
| M25 | iter: the gain counted twice | P1 285, P2 276, P3 321, P5 360, P6 285 |
| M28 | solution: the price as the gain | P1 313, P2 195, P3 360, P5 360, P6 313 |
| M29 | solution: the price from the future list | P1 285, P3 321, P5 360, P6 285 |

P1 and P6 kill all seventeen, P3 fourteen, P5 eight, P2 seven and P4
five. P3, a budget that buys every stock, needs no choosing at all, so
it catches every edit that miscounts a profit or a price, but none
that only chooses badly. P4, the stocks reversed, fails only where an
arm treats a stock by its place: the memo keyed by the stock alone,
the rows all built from the first, the first stock left out, and the
futures paired with the wrong stocks. Two edits fail on a single case
or a handful: the memo stored by the stock alone (M13) is read back
only when the budget left is 0, and then gives the answer stored for
some other budget, which happened in one case, and the naive arm's stock too dear bought anyway (M7)
only where a stock costs at most 5 more than the budget left and gains.

Of the thirty-one, fourteen were not kept. One crashes under both
backends: the naive arm's next stock skipped on a buy (M11) recursed
without end on its own guard and overflowed the stack. One passes
every check: the iter arm's losing stocks kept (M22) lets a stock that
loses into the fold, where `max` with the old cell never takes it, so
it is the same function. Twelve fail as a kept one does or in a way of
their own that their arm does not need: the budget never spent in the
★ and naive arms and the template's price free (M2, M8, M31) all fail
only P1 and P6 on 65 cases; the ★ arm's last stock left out and the
memo arm's end one stock early (M5, M16) fail together; the ★ arm's
stock costing one less (M6) on 8 cases; the memo arm's price paid
twice (M14) as the struct arm's answer from the first column (M20);
the struct arm's gain backwards (M17) as the naive arm's profit the
price now (M9); the struct arm's row improved in place and the
template's upwards (M19, M27) as the ★ arm's budgets run upwards (M1);
the iter arm's answer at half the budget (M26) on its own; and the
template's exact budget out of reach (M30) as the memo arm's affordable
only below the budget (M15).

## Verification

Every arm prints the same output as `profit.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.5 to 1.5 s, except the
template, whose `i32` arithmetic is checked and cast at every cell:
2.2 s. The differential takes 10 s there and 0.6 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 100 markets of 500 stocks once, prices 0 to 100, then
answers each with a budget of 1000, with the ★ arm in all five
languages. Every implementation prints `100 markets of 500 stocks,
budget 1000: checksum 986040156`.

BENCHTAB
