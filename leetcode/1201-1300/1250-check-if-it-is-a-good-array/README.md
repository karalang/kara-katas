# 1250. Check If It Is a Good Array

Given an array `nums` of positive integers, your task is to select some
subset of `nums`, multiply each element by an integer and add all these
numbers. The array is said to be *good* if you can obtain a sum of `1`
from the array by any possible subset and multiplicand.

Return `true` if the array is good, otherwise return `false`.

```
nums = [12, 5, 7, 23]  ->  true    (5 * 3 + 7 * (-2) = 1)
nums = [29, 6, 10]     ->  true    (29 * 1 + 6 * (-3) + 10 * (-1) = 1)
nums = [3, 6]          ->  false
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`.

The arms are `fn is_good_array(nums: Vec[i64]) -> bool`, the array
borrowed.

## Approaches

| file | mechanism |
|---|---|
| `is_good_array.kara` ★ | Euclid's algorithm in a `while` loop, folded over the array from 0, returning as soon as the divisor is 1: a sum of whole multiples can be 1 exactly when the greatest common divisor is 1 (Bézout) |
| `is_good_array_fold.kara` | a fold: `nums.iter().fold(0, \|g, x\| gcd(g, x)) == 1` with a recursive `gcd`, no early stop |
| `is_good_array_binary.kara` | Stein's binary algorithm: the shared twos taken out with `trailing_zeros` and shifts, then the smaller odd value taken from the larger, no division |
| `is_good_array_primes.kara` | by primes: the first value factored by trial division, and the array good when every one of its primes fails to divide some value, with `all` and `any` |
| `is_good_array_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn gcd` nested in the method, `fold` with `\|acc, &x\|`, `Vec<i32>`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples; the count
of good arrays and a checksum of the answers for 1500 random arrays of 1
to 2000 values, a third up to 10^9, a third short and up to 30, a third
sharing a factor from 2 to 9 with, half the time, one value of no shared
factor put in (`1025 good, checksum 581626674`); and two arrays at the
constraints' top, 100000 values all 223092870 (the product of the primes
to 23) but a last 29, and 100000 multiples of 223092870.
`is_good_array.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac run` and `karac build`, and
under the AddressSanitizer build.

The Mend loop: the four Kāra arms checked clean as first written. The
solution arm takes one round of fixes: four diagnostics, all
machine-applicable, 6 edits by `karac fix`'s count (`struct Solution;` to
`struct Solution {}`, `Vec<i32>` to `Vec[i32]`, the `fn gcd` nested in
the method moved above the `impl`, since Kāra has no nested items and a
nested `fn` captures nothing, and the `|acc, &x|` pattern to
`|acc, x|`). It then checks clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every sum of whole multiples of the values, built by adding or
taking away one value at a time from 0 with each partial sum kept between
minus and plus the largest value, and the array good when 1 is among
them. 2000 cases of 1 to 6 values up to 60, half of them sharing a factor
from 2 to 5.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array rotated by one gives the same answer |
| P3 | the first value raised by the last gives the same answer |
| P4 | every value doubled is not good |
| P5 | the product of the first and last values added gives the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 388350579,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, with
`math.gcd`, gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the walk stopped once the divisor is 2 or less | P1 232, P4 720, P6 928 |
| S2 | ★: the first value left out | P1 156, P2 113, P5 3, P6 624 |
| F1 | fold: the fold started from 1 | P1 1280, P4 2000, P6 1280 |
| F2 | fold: the recursion stopped when the second value is 1 | P1 720, P6 720 |
| B1 | binary: the shared twos not put back | P1 449, P4 1166, P5 33, P6 449 |
| B2 | binary: a first value of 0 giving 0 | P1 720, P6 720 |
| P1 | primes: trial division stopping below the square root | P1 64, P2 117, P3 98, P4 8, P6 64 |
| P2 | primes: `any` prime in place of `all` | P1 703, P2 328, P3 245, P4 1202, P6 703 |
| L1 | solution: a divisor of 2 taken as good | P1 232, P4 720, P6 232 |
| L2 | solution: the last value left out | P1 154, P2 106, P3 105, P5 154, P6 154 |

All ten are caught, every one by P1, the statement read literally, and
by P6, which fails on the other four arms too when the ★ arm is the one
mutated (S1, S2). P4, every value doubled, catches the six that answer
good too readily: a divisor of 2 taken as 1 (S1, L1), the fold from 1
(F1, good every time), the twos dropped (B1), a square of a prime
counted as a prime (P1), and one prime of the first value enough (P2).
P2 and P3, the array rotated and its first value changed, catch the four
whose answer hangs on where a value sits: the first or last left out
(S2, L2) and the primes arm, which factors the first value (P1, P2). F2
and B2 answer "not good" every time, which every property but P1 and P6
allows.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (Euclid's algorithm folded over the array, stopping once the divisor
reaches 1) on 50 random arrays of 100000 values built once, every value
sharing a factor from 2 to 1000 and, in half of them, one value of no
shared factor put in at a random place; each asked 20 times, every
answer folded into a checksum. Every program prints `20 rounds of 50
arrays of 100000 values: checksum 174170013`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.543 to 0.583 s | 0.553 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.548 to 0.579 s | 0.557 s |
| Rust (`rustc -O`) | 0.538 to 0.559 s | 0.550 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.542 to 0.585 s | 0.557 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.544 to 0.587 s | 0.555 s |
| C (`clang -O3`) | 0.545 to 0.571 s | 0.558 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.546 to 0.572 s | 0.552 s |
| Go | 0.782 to 0.816 s | 0.795 s |
| Python | 12.27 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.557 s
against 0.557 s), and the two ranges overlap. C runs level with Kāra
(0.558 s against 0.557 s); Kāra is about 30% ahead of Go (0.557 s
against 0.795 s). Python takes about 22x Kāra's time. No profile was
taken.
