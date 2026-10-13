# 518. Coin Change II

You are given an integer array `coins` representing coins of different
denominations and an integer `amount` representing a total amount of
money.

Return the number of combinations that make up that amount. If that
amount of money cannot be made up by any combination of the coins,
return `0`.

You may assume that you have an infinite number of each kind of coin.
The answer is guaranteed to fit into a signed 32-bit integer.

```
amount = 5,  coins = [1,2,5]  ->  4    (5, 2+2+1, 2+1+1+1, 1+1+1+1+1)
amount = 3,  coins = [2]      ->  0
amount = 10, coins = [10]     ->  1
```

**Constraints:** `1 <= coins.length <= 300`; `1 <= coins[i] <= 5000`;
all the values of `coins` are unique; `0 <= amount <= 5000`.

## Approaches

Every arm is `fn change(amount: i64, coins: Vec[i64]) -> i64`.

| file | mechanism |
|---|---|
| `change.kara` ★ | one row of counts by amount, the coins on the outer loop and the amounts walked upwards, so each combination is counted once in coin order and a coin can be reused. O(n * amount) time, O(amount) space |
| `change_table.kara` | the full table `ways[i][a]` over the first i coins: the ways without coin i - 1 plus the ways that use it at least once, read from the same row. O(n * amount) time and space |
| `change_memo.kara` | top-down on (coin index, amount left): skip the coin, or use it once more and stay on it, each answer kept in a `Map[(i64, i64), i64]` that goes down the recursion as `mut ref`. O(n * amount) states |
| `change_copies.kara` | for each coin, every number of copies it could add: a fresh row whose entry at a sums the old row at a, a - coin, a - 2 coin and so on. O(n * amount^2 / smallest coin) |
| `differential.kara` | the four arms on 1,500 random amounts, five properties |

Every arm prints the same 8 lines: the three LeetCode examples, the
amount 0, an amount only even coins cannot reach, 500 from eight coins
(6295434 ways), 5,000 from four coins, and for 300 random amounts from
0 to 300 with 1 to 8 different coins from 1 to 60 the count that
cannot be made and a checksum. `change.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random amounts from 0 to 40 with 1 to 5 different coins from 2
to 15.

| | property |
|---|---|
| P1 | the count is the reference's: every way written out by a depth-first search that never picks a coin earlier in the list than the last one picked |
| P2 | the coins in the other order count the same |
| P3 | every coin and the amount times d (2 to 4) count the same, and the amount times d plus 1 to d - 1 cannot be made |
| P4 | a coin larger than the amount changes nothing |
| P5 | with a 1 added, the count is the sum of the counts for every amount from 0 to this one, since the ones make up whatever the other coins leave |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the amounts walked downwards (`.rev()`), so each coin is used at most once | P1 774, P5 1426 |
| M2 | ★: the amount equal to the coin skipped | P1 883, P5 1458 |
| M3 | table: a coin's reuse read from the row without it | P1 774, P5 1426 |
| M4 | table: the last row never told that 0 can be made | P1 281, P2 289, P4 239, P5 1216 |
| M5 | memo: using coin i moves on to the next coin | P1 774, P5 1426 |
| M6 | memo: the last coin never tried | P1 710, P2 597, P4 710, P5 1383 |
| M7 | copies: every coin used at least once | P1 821, P4 251, P5 251 |
| M8 | copies: a coin may not make up the whole amount (`<` for `<=`) | P1 925 |
| E1 | ★: the row one longer | 0 |
| E2 | table: the amounts start at 0 | 0 |
| E3 | memo: never looked up (the key is never stored) | 0 |
| E4 | copies: the coins taken in reverse | 0 |

E1 adds a cell nothing reads. E2 recomputes the amount 0 as 1 again,
since no coin is 0. E3 makes the recursion forget what it worked out,
which only costs time at these sizes. E4 holds because the count does
not depend on the order the coins are taken in.

M1, M3 and M5 are three spellings of the same wrong answer, each coin
at most once, and fail exactly the same cases. P2, P3 and P4 cannot
see any of them: a coin used at most once is still unmoved by the
order of the coins, by scaling and by a coin too large to use. P5
sees them nearly every time, since adding a 1 that can be used only
once breaks the sum. M8 drops the term where the coin makes up all of
what is left, which is a consistent rule too: only the reference sees
it. M6 and M4 lose the last coin, which P2 sees by moving another coin
to the end, and P4 by putting a coin there that should change nothing.

## Verification

Every arm prints the same output as `change.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `30000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program.

On the frozen legacy backends the table arm agrees: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output. The ★, memo and copies arms, the differential
and the bench program are refused by all of them at type checking:
legacy types the items of a `Vec`'s `iter()` and the value a `Map`'s
`get` returns by value, so it refuses `*c`, `*coin` and `*v`, "unary
'*' requires 'ref T' ... found 'i64'". Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 3,000 random sets of 100
different coins from 500 to 5,000, each with an amount from 4,000 to
5,000 (the problem's most), and solves each once. Coins of at least
500 keep every count inside an `i64` (at most ten coins fit in an
amount); the problem promises answers inside 32 bits, and small coins
can push the counts on these amounts past 64. Every implementation
prints `3000 sets of 100 coins: checksum 336655348`, the Kāra program
under `karac __mir-run` included (in 130 s).

Every mirror allocates a fresh row for every call, as the ★ arm's
`vec![0; amount + 1]`. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.16 to 0.17 s |
| Rust (`rustc -O`) | 0.90 to 0.98 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.89 to 0.91 s |
| Go | 0.43 to 0.45 s |
| Python | 22.4 to 25.2 s |
| Kāra (`karac build --mir`) | 0.53 to 0.60 s |

The legacy `karac build` refuses this program at the same `*c` (see
Verification). So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`0736eef763`. Under `karac __mir-llvm-run` the program prints the same
line in 3.6 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
