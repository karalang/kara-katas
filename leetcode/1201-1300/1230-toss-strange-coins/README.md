# 1230. Toss Strange Coins

You have some coins. The `i`-th coin has a probability `prob[i]` of facing
heads when tossed.

Return the probability that the number of coins facing heads equals
`target` if you toss every coin exactly once.

```
prob = [0.4], target = 1                      ->  0.40000
prob = [0.5,0.5,0.5,0.5,0.5], target = 0      ->  0.03125
```

**Constraints:** `1 <= prob.length <= 1000`; `0 <= prob[i] <= 1`; `0 <=
target <= prob.length`; answers will be accepted as correct if they are
within `10^-5` of the correct answer.

The arms are `fn probability_of_heads(prob: Vec[f64], target: i64) ->
f64`. The two Rust arms keep the method LeetCode gives Rust users, with
an `i32` target, inside `impl Solution`, and a one-line
`probability_of_heads` calls it. Every harness prints five decimals.

## Approaches

| file | mechanism |
|---|---|
| `toss_strange_coins.kara` ★ | one row of the table: `ways[j]` is the chance that the coins so far show `j` heads; each coin moves every count up by one with its chance of heads and leaves it with its chance of tails, the row updated from the top count down so that each count still reads the old row below it. Counts above the target are never needed. O(n · target) |
| `toss_strange_coins_table.kara` | the whole table: `dp[i][j]` from the row before, tails over `dp[i − 1][j]` and heads over `dp[i − 1][j − 1]`. O(n · target) time and space |
| `toss_strange_coins_memo.kara` | top-down: the chance that the coins from `i` on show `need` more heads, from the next coin's two answers, each kept in a `Map[(i64, i64), f64]`; a need larger than the coins left is 0 at once. Recurses n deep |
| `toss_strange_coins_product.kara` | as a product of polynomials: coin `p` is `(1 − p) + p x`, and the coefficient of `x^target` in the product of all of them is the answer; the product taken by halves over `Slice[f64]`s |
| `toss_strange_coins_row.kara` | a Rust solution as LeetCode's Rust users write it (one row `vec![0.0; target + 1]` over a `usize` target, `for &p in prob.iter()`, the counts updated by `(1..=target).rev()`), carried to Kāra by `karac fix` |
| `toss_strange_coins_grid.kara` | another Rust solution (the whole table, `vec![vec![0f64; t + 1]; n + 1]`, each row filled only up to `t.min(i)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's two examples, three coins
that are sure (`1.00000` for two heads, `0.00000` for one), the total of
the answers for 500 random sets of 1 to 60 coins, a twentieth of them
sure heads and a twentieth sure tails, and how many answers are 0
(`31.080066`, `52`), and three answers at the constraints' top, 1000
coins: chances that climb from 0 to 1 and start again, targets 500 and
480 (`0.02231`, `0.02364`), and 1000 fair coins, target 500 (`0.02523`).
`toss_strange_coins.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, table, memo and product arms check clean as
written. The row arm takes one round of 6 fixes (among them `Vec<f64>`
to `Vec[f64]`, `target as usize` to `target as i64`, `vec![0.0; target +
1]` to `Vec.filled(target + 1, 0.0)`, `for &p in` to `for p in`) and
checks clean. The grid arm writes Rust's `0f64`, which in Kāra is an
integer with a float suffix (design.md §3), and before B-2026-11-19-27 `karac
fix` corrupted it (see below); it now takes one round of 8 fixes, `0f64`
to `0.0f64` among them, and checks clean.

## Gaps

One.

- B-2026-11-19-27, fixed in kara at d1ab453bcb: `0f64` was lexed as the integer `0`
  and the identifier `f64`, and the parser's recovery asked for a `;`
  after each operand of `vec![vec![0f64; t + 1]; n + 1]`, fixes `karac
  fix` applied: it wrote `vec![vec![0f64; t + 1;]; n + 1;]`, and every
  round made it worse. The literal is now one error, "a literal with
  neither a point nor an exponent is an integer (design.md §3), so write
  `0.0f64`", whose fix writes the float, and the parse goes on as that
  float.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every outcome of the tosses, as the bits of a number, its
chance the product of each coin's heads or tails, summed over the
outcomes with `target` heads, for up to 12 coins. 1500 cases, a third
with 1 to 12 coins, a third with 13 to 40 and a third with 41 to 200, a
twentieth of the coins sure heads and a twentieth sure tails. Answers
are compared within `10^-9`.

| | property |
|---|---|
| P1 | the statement read literally (up to 12 coins) |
| P2 | from 0 to 1 |
| P3 | the chances of every target sum to 1 (up to 40 coins) |
| P4 | the coins in reverse give the same answer |
| P5 | heads and tails swapped give the chance of the other count |
| P6 | the ★ arm's answer |

All 54,000 checks pass on every arm: `1500 cases: total 114.632580,
54000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, with exact
fractions, gives the same total.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the counts updated bottom up | P1 314, P3 950, P4 574, P5 800, P6 4895 |
| S2 | ★: no heads never updated | P1 381, P3 997, P5 1499, P6 5955 |
| T1 | table: heads read from the same count | P1 377, P3 997, P5 150, P6 1016 |
| T2 | table: the last coin left out | P1 431, P4 966, P5 1108, P6 1029 |
| M1 | memo: a need of exactly the coins left refused | P1 451, P3 1000, P6 1094 |
| M2 | memo: every answer stored under a need of 0 | HANGS |
| P1 | product: a coin's heads and tails swapped | P1 451, P6 1129 |
| P2 | product: each term overwrites the one before | P1 298, P3 947, P4 333, P5 333, P6 933 |
| R1 | row: no heads never updated | P1 381, P3 997, P5 1499, P6 1191 |
| R2 | row: heads and tails swapped | P1 394, P3 996, P4 926, P5 1146, P6 1077 |
| G1 | grid: each row filled one count short | P1 451, P3 1000, P6 1094 |
| G2 | grid: the empty table half sure | P1 451, P3 1000, P6 1084 |

All twelve are caught. Eleven fail P1, the statement read literally, and
P6; M2, the memo that stores every answer under a need of 0, never finds
a stored answer again, so its search is exponential and the run is
stopped at its 25-minute limit under both modes. Two mistakes are made
twice, in different arms, and fail the same cases: the chance of no
heads never multiplied by a coin's tails (S2 in the ★ arm, R1 in the row
arm), 381 cases of P1 and 1499 of P5, and an answer that loses a coin's
last count (M1 in the memo, G1 in the grid), 451 of P1 and all 1000 of
P3. P3, the chances of every target summing to 1, catches nine; it
misses the table arm leaving out the last coin (T2) and the product
arm's coin with heads and tails swapped (P1), whose chances still sum to
1, and P1 is caught only by the statement and the ★ arm. P5, heads and
tails swapped giving the other count's chance, catches the seven that
treat heads and tails unevenly, and P4, the coins in reverse, the four
whose answer depends on the order of the coins. P2, every answer between
0 and 1, catches none: no mutation here leaves that range.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, one row of the table updated from the top count down, over 200
random sets of 1000 coins with random targets, drawn once and each
solved once, the answers summed. Every program prints `200 sets of 1000
coins: total 0.250520`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.134 to 0.245 s | 0.145 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.131 to 0.174 s | 0.151 s |
| Rust (`rustc -O`) | 0.133 to 0.219 s | 0.155 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.134 to 0.199 s | 0.144 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.168 to 0.232 s | 0.180 s |
| C (`clang -O3`) | 0.068 to 0.090 s | 0.072 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.051 to 0.068 s | 0.054 s |
| Go | 0.125 to 0.201 s | 0.139 s |
| Python | 7.669 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.144 s
against 0.151 s), and the two ranges overlap. Kāra takes about 2.1x C's
time (0.151 s against 0.072 s); Go is about 8% ahead of Kāra (0.139 s
against 0.151 s). Python takes about 51x Kāra's time. No profile was
taken.
