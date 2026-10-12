# 441. Arranging Coins

You have `n` coins and build a staircase with them: the first row has
1 coin, the second 2, the i-th i. The last row may be incomplete.
Return the number of complete rows.

```
n = 5  ->  2     (1 + 2 = 3 coins in two rows, 2 left for a third of 3)
n = 8  ->  3     (1 + 2 + 3 = 6, 2 left)
```

**Constraints:** `1 <= n <= 2^31 - 1`.

## Approaches

k complete rows take T(k) = k (k + 1) / 2 coins, so the answer is the
largest k with T(k) <= n. The arms find that k in different ways.

| file | mechanism |
|---|---|
| `arrange_coins.kara` ★ | the closed form k = (sqrt(8n + 1) - 1) / 2, with the square root taken in integers by Newton's method and rounded down, so the division rounds to exactly that k. O(log n) |
| `arrange_coins_binary.kara` | binary search for the largest k in `[0, n]` with T(k) <= n. O(log n) |
| `arrange_coins_rows.kara` | the plain reference: lay row after row while enough coins are left for the next. O(sqrt n), about 65,000 rows at the problem's largest n |
| `arrange_coins_float.kara` | the closed form with an `f64` square root, then corrected: step k up while T(k + 1) <= n and down while T(k) > n, both tests exact in integers. O(1) |
| `differential.kara` | the four arms on 1,500 random n, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, six edge
cases (one coin, three coins, the largest n, the largest triangular
number below it, T(65535) = 2147450880, and one less, and a billion),
and for 300 random n the total of the answers and a checksum.
`arrange_coins.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random n of at most 1 to 10 digits; a draw is below 2^30.

| | property |
|---|---|
| P1 | the answer r has T(r) <= n < T(r + 1) |
| P2 | T(m) coins make m rows and T(m) - 1 make m - 1, for a random m up to 46,340 |
| P3 | one more coin adds a row exactly when n + 1 is T(r + 1) |
| P4 | the coins that complete row r + 1 make r + 1 rows, and one fewer leave r |
| P5 | more coins never make fewer rows, nor more rows than coins added |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. Seven are killed; M8 is an equivalent mutant.

| # | mutation | failures by property |
|---|---|---|
| M1 | sqrt: the square root of 8n instead of 8n + 1 | P1 93, P2 1500, P3 142, P4 1500 |
| M2 | sqrt: Newton's method stops a step early | P1 188, P2 1250, P3 55, P4 1121 |
| M3 | binary: rows that use every coin do not count | P1 93, P2 1500, P3 142, P4 1500 |
| M4 | binary: the search starts at n / 2 | P1 37, P3 51, P4 51 |
| M5 | rows: a row is laid when exactly enough coins are left for it | P1 49, P2 1500, P3 80, P4 1500 |
| M6 | rows: the count starts at one row | P1 49, P2 1500, P3 80, P4 1500 |
| M7 | float: the downward correction also steps off an exact fit | P1 93, P2 1500, P3 142, P4 1500 |
| M8 | float: the upward correction takes one coin too many | none |

Most of these mutants go wrong only on a triangular n or one coin
short of it, which is why P2 and P4, built on exactly those numbers,
fail in most or all cases while random n (P1) rarely lands on one. M4
is the exception: n / 2 is too small a bound only for n of 1 and 3, so
only the checks that reach those two numbers find it. M8 steps up once
too often when n + 1 is triangular, and the downward correction then
steps back: with the downward loop also disabled, the same edit fails
3,129 checks. So the downward loop repairs any overshoot of the upward
one, and the float arm can only be broken where the downward loop
decides to stop. P5 kills nothing: every mutant here is wrong by a
consistent shift, which never makes the count fall or jump. P5 is kept
anyway: it is the only property that compares answers for two
unrelated n.

## Verification

All four arms print the same output as `arrange_coins.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`, and the differential prints
`0 failures` under `karac run --interp` and `karac build`.

## Benchmarks

The bench program uses the ★ arm on 3,000,000 random n up to 2^31 - 1,
each drawn from three random numbers. Every implementation prints
`3000000 random n: total 131069461887, checksum 116776277`, the Kāra
program under `karac __mir-run` included (in 22 s). Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.32 to 0.33 s |
| Rust (`rustc -O`) | 0.31 to 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.33 to 0.35 s |
| Go | 0.40 to 0.43 s |
| Kāra (frozen legacy `karac build`) | 0.32 to 0.34 s |
| Python | 8.1 to 8.6 s |

Each query is mostly the integer square root's chain of divisions
(read from the code, not profiled), which costs about the same in
every compiled language, so the times sit together; the legacy build
checks integer overflow and matches Rust with overflow checks on. The Kāra program prints the same line under
`karac __mir-llvm-run` in 1.3 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings.
