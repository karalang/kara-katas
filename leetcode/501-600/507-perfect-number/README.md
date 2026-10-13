# 507. Perfect Number

A perfect number is a positive integer that is equal to the sum of its
positive divisors, excluding the number itself. A divisor of an integer
`x` is an integer that can divide `x` evenly.

Given an integer `n`, return `true` if `n` is a perfect number,
otherwise return `false`.

```
num = 28  ->  true    (28 = 1 + 2 + 4 + 7 + 14)
num = 7   ->  false
```

**Constraints:** `1 <= num <= 10^8`.

## Approaches

Every arm is `fn check_perfect_number(num: i64) -> bool`.

| file | mechanism |
|---|---|
| `check_perfect_number.kara` ★ | the divisors in pairs: every `i` from 2 while `i * i <= num` that divides `num` brings its partner `num / i`, a square root counted once, and the sum starts at 1; 1 itself is not perfect. O(sqrt n) |
| `check_perfect_number_sigma.kara` | the sum of all divisors from the prime factors: sigma(n) is the product over the prime powers p^k of 1 + p + ... + p^k, built by trial division, and n is perfect when sigma(n) is 2n. O(sqrt n) |
| `check_perfect_number_euclid.kara` | Euclid-Euler: the even perfect numbers are 2^(p-1) (2^p - 1) with 2^p - 1 prime, and no odd one exists below 10^1500, so walk p up while that number is at most `num` and test the Mersenne factor for primality |
| `check_perfect_number_iter.kara` | the ★ arm's pairs as one chain: `(1..=root).filter(...).map(...).sum()`, 1 and a square root counted alone |
| `differential.kara` | the four arms on 1,500 numbers, five properties |

Every arm prints the same 13 lines: the two LeetCode examples, 1, 2,
6, 12, 496, 8128, 33550336, the number after it and 10^8; every
perfect number from 1 to 10,000; and for 300 numbers (in turn a random
one up to 10^8, one of the five perfect numbers in range, one of those
plus or minus 1, and twice one of those) the count found perfect and a
checksum that folds in each answer with `answer as i64`.
`check_perfect_number.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 numbers: in turn a random one from 1 to 20,000, one from 1 to
10^8, a perfect number, one within 5 of a perfect number (1 among
them), and twice a perfect number.

| | property |
|---|---|
| P1 | the answer is the reference's, which adds up every proper divisor of a number up to 20,000, and above that looks it up among the five perfect numbers below 10^8 |
| P2 | a perfect number is even |
| P3 | a number and the next are never both perfect |
| P4 | a perfect number is 2^k (2^(k+1) - 1) |
| P5 | the smallest prime not below the number is not perfect |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a divisor is added twice, not with its partner (`sum += i`) | P1 329 |
| M2 | ★: 1 is not set apart (`num == 0`) | P1 7, P2 7, P4 7 |
| M3 | sigma: the last prime factor is dropped | P1 329 |
| M4 | sigma: a term is 1 + p^k, not 1 + p + ... + p^k | P1 275 |
| M5 | euclid: the walk starts at p = 3 | P1 54 |
| M6 | euclid: a candidate equal to `num` is passed over (`>=`) | P1 329 |
| M7 | iter: 1 is counted with its partner `num` | P1 329 |
| M8 | iter: 1 is not set apart | P1 7, P2 7, P4 7 |
| E1 | euclid: the walk starts at p = 1 | 0 |
| E2 | iter: the search for the root starts at 0 | 0 |
| E3 | ★: a square root is counted twice (`if true`) | 0 |
| E4 | sigma: the trial stops while `p * p < rest` | 0 |

E1 is equivalent because p = 1 gives the candidate 1 with the
Mersenne factor 1, which is not prime, so 1 still gets `false` and
every other number walks on to p = 2. E2 is equivalent because the
search raises the root to 1 for any `num` of at least 1.

E3 and E4 compute a wrong divisor sum but never a wrong answer within
the problem's range, which an exhaustive search shows. E3 adds a square
root a second time, so it can only change the answer for a square `n =
k^2` whose proper divisors add up to `n - k`: of the 9,999 squares from
4 to 10^8 none does. E4 leaves a final factor `q^2` whole, giving the
term `1 + q^2` for `1 + q + q^2`, which happens only for `n = m q^2`
with every prime factor of `m` below `q`: of the 212,491 such numbers
up to 10^8 none changes answer either way. Both searches were C
programs over every case, outside this repository.

M1, M3, M6 and M7 turn every perfect number into `false` and fail the
same 329 cases, the ones holding a perfect number. M4 fails 275 of
them: 6 is 2 * 3, whose terms have no square in them, so it stays
perfect. M5 loses only 6. M2 and M8 call 1 perfect, which P2 sees
since 1 is odd and P4 since it is not 2^k (2^(k+1) - 1); 1 comes up in
7 of the 1,500 cases. Every mutation that keeps the answer `false` for
numbers that are not perfect leaves P2 to P5 passing, so P1 does most
of the work; P3 and P5 kill none of these eight.

## Verification

All four arms print the same output as `check_perfect_number.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `30000 checks, 0 failures` on both and runs clean under the
third. `karac check` passes on every file, the bench program included.

The frozen legacy backends agree on all four arms: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output, and the differential prints `30000 checks, 0
failures` under `karac run --interp` and legacy `karac build`.

## Benchmarks

The bench program uses the ★ arm. It builds 100,000 numbers from 1 to
10^8 (the problem's most), one in ten of them one of the five perfect
numbers in range, once. Then it checks each once. Every implementation
prints `100000 numbers: 10000 perfect, checksum 197514648`, the Kāra
program under `karac __mir-run` included (in 91 s).

Every mirror is the same loop over `i` while `i * i <= num`. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.22 to 1.33 s |
| Rust (`rustc -O`) | 1.28 to 1.41 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.26 to 1.37 s |
| Go | 2.00 to 2.15 s |
| Python | 29.7 to 30.2 s |
| Kāra (legacy `karac build`) | 1.21 to 1.32 s |
| Kāra (`karac build --mir`) | 1.23 to 1.29 s |

The loop is almost all integer division, so C, Rust and both Kāra
builds land close together. Legacy `karac build` builds this program, so
`bench.sh` is the `scripts/new-bench.sh` output unchanged and times
the legacy build; the `--mir` row is timed by hand at kara
`486f47f97d`. Under `karac __mir-llvm-run` the program prints the
same line in 3.4 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
