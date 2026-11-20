# 1281. Subtract the Product and Sum of Digits of an Integer

Given an integer number `n`, return the difference between the product of
its digits and the sum of its digits.

```
n = 234   ->  15      product 2 * 3 * 4 = 24, sum 2 + 3 + 4 = 9
n = 4421  ->  21      product 4 * 4 * 2 * 1 = 32, sum 4 + 4 + 2 + 1 = 11
```

**Constraints:** `1 <= n <= 10^5`.

The arms are `fn subtract_product_and_sum(n: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `subtract_product_and_sum.kara` ★ | by remainders: the digits taken from the lowest by `% 10` and `/ 10`, each multiplied into the product and added to the sum. O(log n) |
| `subtract_product_and_sum_text.kara` | by text: the number written out by `to_string`, each character read back by `to_digit`, and the digits' `product` and `sum` taken by the iterator methods |
| `subtract_product_and_sum_recursive.kara` | by recursion: a number's (product, sum) is its last digit folded into the pair for the number without it, a single digit being its own pair |
| `subtract_product_and_sum_fold.kara` | by a fold over bytes: the number formatted by `f"{n}"`, and its `bytes()` folded into one (product, sum) pair, each byte less `'0'` |
| `subtract_product_and_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut n: i32`, a `while n > 0` loop, `let (mut p, mut s) = (1, 0)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, then 1, 99999
and 100000 (`15 21 0 59004 -1`); and every `n` the constraints allow, 1 to
10^5 (`1 to 100000: total 186471944, 68 zero, checksum 302912786`).
`subtract_product_and_sum.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the four arms written in Kāra checked clean as first
written. The solution arm takes one round of 10 fixes by `karac fix`'s
count: Rust's `mut n` parameter became a plain `n: i32` with `let mut n =
n;` at the top of the body, `let (mut p, mut s) = (1, 0)` became `let mut
(p, s) = (1i32, 0i32)` with the `i32` Rust inferred from the return,
`struct Solution;` and `::` took Kāra's spelling, and the wrapper's `as
i64` on the `i32` answer was dropped as a widening Kāra does by itself.
No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the number's decimal digits, each found as how many times its
power of ten fits in what is left, from the largest power down, with no
division; then their product and their sum. 2000 random numbers, a third
up to 999 and the rest up to 10^5.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a 0 written after the number: minus the digit sum |
| P3 | the digits reversed, when the number does not end in 0: the same answer |
| P4 | a 1 written after the number: one less |
| P5 | a 2 written before the number: the product doubled and the sum 2 more |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 numbers: checksum 927210932,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the leading digit never read (`while rest > 9`) | P1 1998, P2 2000, P3 1468, P5 1989, P6 7992 |
| S2 | ★: a 0 digit skipped in the product | P1 556, P2 2000, P5 556, P6 2224 |
| X1 | text: the first digit left out of the sum | P1 2000, P2 2000, P3 1572, P5 2000, P6 2000 |
| X2 | text: a 9 read as 0 | P1 618, P2 621, P5 621, P6 618 |
| R1 | recursive: a two-digit number taken as one digit | P1 1984, P2 2000, P3 1621, P4 14, P5 1994, P6 1984 |
| R2 | recursive: the sum takes the tens digit | P1 1779, P2 2000, P3 1572, P4 1797, P5 1801, P6 1779 |
| F1 | fold: the digits added into the product | P1 1996, P2 2000, P4 2000, P5 1996, P6 1996 |
| F2 | fold: the sum starts at 1 | P1 2000, P2 2000, P5 2000, P6 2000 |
| O1 | solution: the product starts at 0 | P1 1444, P5 1444, P6 1444 |
| O2 | solution: every other digit skipped (`n /= 100`) | P1 1973, P2 1994, P3 323, P4 1880, P5 1994, P6 1973 |

All ten are caught, every one by P1, the statement read literally, and by
P5, the 2 written in front. P2, the 0 written after, catches all but O1:
a product that starts at 0 already answers minus the digit sum, which is
exactly what P2 expects. P3, the digits reversed, catches only the edits
that treat one position differently from the rest (S1, X1, the recursive
pair, O2); an edit that mistreats a digit by its value (S2, X2) or every
digit alike (F1, F2, O1) answers a reversed number the same wrong way.
P4, a 1 written after, multiplies the product by 1 and adds 1 to the sum,
so it sees only edits that change with the number's length or last digit
(R1, R2, O2) or that add digits into the product (F1). S2's skipped 0
hides from P1 on numbers with no 0 digit, which is why it fails 556 of
2000. The first version of F1 overflowed in the byte-to-digit subtraction,
which Kāra's overflow check stops with a runtime error under both
backends, and was replaced by this one.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the digits by remainders) on every n from 1 to 10^5, 2000 rounds,
every answer folded into a checksum. Every program prints `2000 rounds
of 1 to 100000: checksum 284995552`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.576 to 1.652 s | 1.595 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.583 to 1.732 s | 1.624 s |
| Rust (`rustc -O`) | 1.305 to 1.379 s | 1.336 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.561 to 1.752 s | 1.591 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.539 to 1.755 s | 1.597 s |
| C (`clang -O3`) | 1.282 to 1.520 s | 1.333 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.296 to 1.479 s | 1.331 s |
| Go | 1.564 to 1.714 s | 1.663 s |
| Python | 106.55 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (1.591 s
against 1.624 s), and the two ranges overlap. C is about 18% ahead of
Kāra (1.333 s against 1.624 s); Go runs level with Kāra (1.663 s against
1.624 s). Python takes about 66x Kāra's time. No profile was taken.
