# 1134. Armstrong Number

Given an integer `n`, return `true` if and only if it is an Armstrong
number. The `k`-digit number `n` is an Armstrong number if and only if
the `k`th power of each digit sums to `n`.

```
n = 153  ->  true     (153 = 1^3 + 5^3 + 3^3)
n = 123  ->  false    (123 != 1^3 + 2^3 + 3^3 = 36)
```

**Constraints:** `1 <= n <= 10^8`.

The arms are `fn is_armstrong(n: i64) -> bool`.

## Approaches

Each arm finds `k`, the number of digits, before it can raise any digit
to the `k`th power, so each reads the digits twice or keeps them.

| file | mechanism |
|---|---|
| `is_armstrong.kara` ★ | the digits counted by dividing by 10, then each digit's `k`th power built by repeated multiplication and summed. O(k^2) for `k` digits |
| `is_armstrong_text.kara` | through `n.to_string()`: `k` is its length, and each character's `to_digit(10)` is raised with `pow`. O(k log k) |
| `is_armstrong_recur.kara` | recursively: the digit count, each power and the power sum are three recursions on `n / 10` and `k - 1`. O(k^2) |
| `is_armstrong_count.kara` | how often each digit 0 to 9 occurs, kept in `[0; 10]`, then each digit present raised once and multiplied by its count. O(k + 10k) |
| `is_armstrong_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `n: i32`, `s.len() as u32`, `c.to_digit(10).unwrap() as i32` raised with `.pow(k)` and summed with `.sum::<i32>()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the answers for LeetCode's two
examples and ten more (one digit, the first two digits, three digits,
four, a neighbour, `10^8`, and the largest two up to `10^8`), every
Armstrong number from 1 to 20000, then all 27 up to `10^8` accepted and
none of their other neighbours (`27 of the 27 up to 10^8 accepted, 0 of
their other neighbours`), and over 2000 random numbers from 1 to `10^8`
how many are accepted and a checksum (`2000 random numbers to 10^8: 0
accepted, checksum 491060536`). `is_armstrong.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: `n` written out with `f"{n}"` has `k` characters, and the
`k`th powers of their digits, built by multiplication, sum to `n`. It
checks 2000 problems in five kinds of 400: from 1 to `10^8`; from 1 to
`10^4`; one of the 27 Armstrong numbers up to `10^8`; one of them moved
by 1 to 9 either way; and one of them with its digits in a drawn order.
Every random choice, each problem's own drawn order of its digits for
P3 among them, is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | `n`'s digits reversed have the same power sum, so when they make another number, the two are not both accepted |
| P3 | the same for a drawn order of `n`'s digits, with no leading 0 |
| P4 | `n`'s last digit, when not 0, is accepted: one digit to the first power is itself |
| P5 | `10^k`, one digit more than `n`, sums to 1 and is rejected |
| P6 | the `k` nines, `10^k - 1`, are accepted only when `k` is 1 |

All 60,000 checks pass on every arm: `2000 problems: checksum
615472013, 60000 checks over 5 arms: 0 failures`. A Python reading of
the same problems, `sum(int(c) ** len(s) for c in s) == n`, gives the
same checksum.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a power sum at most `n` accepted | P1 714, P2 435, P3 546, P5 2000 |
| M2 | ★: the last digit left out of the sum | P1 608, P4 1810, P6 362 |
| M3 | ★: each power one less | P1 648, P4 1810, P6 362 |
| M4 | text: one digit too few counted | P1 611, P4 1594, P6 362 |
| M5 | text: a power sum at least `n` accepted | P1 641, P2 513, P3 543, P6 1638 |
| M6 | text: each digit times `k`, not to the `k`th power | P1 284 |
| M7 | recur: every other digit skipped | P1 266 |
| M8 | recur: the first digit left out | P1 645, P4 1810, P6 362 |
| M9 | recur: a two-digit number counted as one digit | P1 283 |
| M10 | count: each digit counted once however often | P1 151 |
| M11 | count: the digit 9 left out | P1 135, P4 147, P6 362 |
| M12 | count: one-digit numbers rejected | P1 362, P4 1810, P6 362 |
| M13 | solution: every number ending in 0 accepted | P1 153, P3 49, P5 2000 |
| M14 | solution: `n` read below `10^5` | P1 131, P5 873 |
| M15 | solution: 153 rejected | P1 16 |

P1 catches all fifteen, P6 seven, P4 six, P3 and P5 three each, and P2
two. P4 and P6 ask about one-digit numbers, which every Armstrong
reading must accept, so they see every edit that breaks those: a power
one short or one less, a digit left out, a digit count off by one. P2,
P3 and P5 see the edits that accept too much: a power sum compared with
`<=` or `>=` (M1, M5), every number ending in 0 (M13), and `n` read
below `10^5`, which reads `10^k` as 0 (M14). Five are seen by P1 alone,
and they are the kind the properties cannot see: each gets some numbers
of two digits or more wrong and keeps the one-digit ones right (M6, M7, M9, M10, M15). The properties never name an Armstrong
number above 9; P1 does, because three kinds of problem draw from the
27 and their near misses.

Of the fifteen not kept, fourteen fail exactly as a kept one: a power one
short in the ★, recur and solution arms, the digit count started at 1 in
the ★ arm, every digit squared in the text arm, and one digit too few
counted in the recur arm, as M4; the first digit left out in the ★ and
text arms, the sum started at 1 in the text arm, and a digit seen once
left out in the count arm, as M8; the last digit left out in the
solution arm as M2; a power sum at least `n` in the recur arm as M5;
each digit's power taken once in the count arm as M10; and each digit
raised to its own count as M9. The other, the digit count capped at 7 in
the solution arm, fails on 52 problems, P1 alone.

## Verification

Every arm prints the same output as `is_armstrong.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found no gap. The ★, text, recur and count arms were written as
Kāra and checked clean as written. `karac fix` carried the solution arm
in two rounds: `.sum::<i32>()` to `.sum()` with the binding declared
`let sum: i32`, and `Solution::is_armstrong` to `Solution.is_armstrong`;
then `struct Solution {}` declared. The differential's own list of the
27 was first written `const KNOWN: [i64; 27]`, Rust's array type, and
`karac fix` made it `Array[i64, 27]`.

## Benchmarks

The bench asks the ★ arm about every number from 1 to 15000000, and
counts, sums and folds into a checksum the ones accepted. Every
implementation prints `1 to 15000000: 24 Armstrong numbers, summing to
26489730, checksum 547816724`. Nothing is allocated: each call is two
passes of division by 10 and, for each digit, `k` multiplications.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `73ec8b248f`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.327 to 0.500 s | 0.385 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.343 to 0.451 s | 0.399 s |
| C (`clang -O3`) | 0.382 to 0.461 s | 0.416 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.397 to 0.514 s | 0.454 s |
| Kāra (`karac build`) | 0.414 to 0.520 s | 0.480 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.409 to 0.576 s | 0.481 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.416 to 0.566 s | 0.499 s |
| Go | 0.517 to 0.674 s | 0.570 s |
| Python | 27.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(the checksum folds the accepted numbers in order) and gives the same
binary, byte for byte, so its two rows differ by noise alone. Kāra takes
about 1.20x C's time at `-O3` and 1.04x at `-march=x86-64-v3`, and about
1.10x Rust's under overflow checks (1.25x at x86-64-v3); like Rust under
overflow checks, it checks each of the power's multiplications and each
sum. Go takes about 1.14x Kāra's time. Python takes about 55x Kāra's
time.
