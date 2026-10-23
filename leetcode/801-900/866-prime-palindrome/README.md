# 866. Prime Palindrome

Given an integer `n`, return the smallest prime palindrome greater than
or equal to `n`. An integer is prime if it has exactly two divisors: 1
and itself; 1 is not a prime number. An integer is a palindrome if it
reads the same from left to right as it reads from right to left. The
test cases are generated so that the answer always exists and is in the
range `[2, 2 * 10^8]`.

```
n = 6   ->  7
n = 8   ->  11
n = 13  ->  101
```

**Constraints:** `1 <= n <= 10^8`.

## Approaches

| file | mechanism |
|---|---|
| `prime_palindrome.kara` ★ | the odd-length palindromes in order: a palindrome with an even number of digits is a multiple of 11 (its digits pair up as d * (10^i + 10^j) with i + j odd, and each such sum is), so 11 is the only prime among them. The root r of d digits gives the palindrome of 2d - 1 digits that starts with r and ends with r reversed, the two sharing r's last digit, so the roots 1, 2, 3, ... give the odd-length palindromes in increasing order; the first at least n that is prime is the answer, with 11 put in its place between 7 and 101. Trial division by the odd numbers up to the square root. About sqrt(answer) roots |
| `prime_palindrome_scan.kara` | every number from n up: a palindrome when its digits reversed give it again, a prime when no 6k - 1 or 6k + 1 up to its square root divides it; at four, six or eight digits the scan jumps to the next power of ten. Up to O(answer - n) numbers |
| `prime_palindrome_build.kara` | the palindromes of each length from n's upward, built from their first halves in increasing order, even lengths included with no use of the multiple-of-11 fact; trial division by the primes up to the square root of 10^L, found for each length by a sieve of Eratosthenes |
| `prime_palindrome_mirror.kara` | from one palindrome to the next: the smallest palindrome at least x is x's first half mirrored, or the first half plus one mirrored when that falls below x, or 10...01 after a half of all nines; each is tested with Miller-Rabin to the bases 2, 3, 5 and 7, exact below 3,215,031,751 |
| `prime_palindrome_digits.kara` | a depth-first search that sets the palindrome's digits a pair at a time from the outside in, each from 0 to 9, so the palindromes of a length come in increasing order; while the digits so far equal n's a smaller digit is passed over, and with more than one digit the outermost is 1, 3, 7 or 9. Trial division by every number up to the square root |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's three examples; ten more
(n = 1, 2, 11 and 12 around the one even-length answer, 102, 9,990 over
the four-digit gap, 1,000,000, the largest seven-digit prime palindrome
9,989,899 and the n just above it, and LeetCode's largest n, 10^8); the
answers for every n from 1 to 2,000, summed and with a checksum; and
the answers for 200 random n of one to eight digits, each length as
likely, of which 102 have more digits than n. `prime_palindrome.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a palindrome when its decimal digits read the same from
either end, a prime when it has exactly two divisors, counted in pairs
(d, x / d) up to the square root. One pass downward from the first prime
palindrome at least 10^6, 1,003,001, gives the statement's answer for
every n up to it: n itself when n is a prime palindrome, and otherwise
the answer for n + 1. It checks 2,300 values of n: every n from 1 to
2,000, 200 random n up to 1,003,001, and 100 random n of one to eight
digits, each length as likely.

| | property |
|---|---|
| P1 | the statement's answer (n up to 1,003,001) |
| P2 | the answer is a palindrome with exactly two divisors |
| P3 | the answer is at least n |
| P4 | one less: the answer for n - 1 is n - 1 when that is a prime palindrome, and otherwise the answer for n |
| P5 | a random m from n to the answer has the same answer |
| P6 | the answer is its own answer |

It prints `2300 values of n, answers sum to 1850138062, 68870 checks over
5 arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 11 missed when n is 11 | P1 1, P4 2, P6 7 |
| M2 | ★: every other root skipped | P1 556, P4 9 |
| M3 | ★: trial division stopped below the square root | P1 1105, P2 1105, P4 1 |
| M4 | scan: two digits skipped as well | P1 8, P4 1 |
| M5 | scan: 6k + 1 never tried | P1 1544, P2 1548, P4 7 |
| M6 | scan: every other pair 6k - 1, 6k + 1 skipped | P1 1131, P2 1133, P4 6 |
| M7 | build: the smallest palindrome of each length skipped | P1 107, P4 2 |
| M8 | build: odd and even lengths swapped | P1 19, P4 12, P5 10, P6 23 |
| M9 | build: a prime's square taken for a prime | P1 1113, P2 1113, P4 6 |
| M10 | mirror: a palindrome x passed over by `next_palindrome(x)` | P1 32, P4 58, P5 65, P6 2300 |
| M11 | mirror: a^d = -1 taken for a witness | P1 824, P4 9 |
| M12 | mirror: two digits skipped as well | P1 8, P4 1 |
| M13 | digits: held to n's digits after passing them | P1 427, P4 25, P5 340 |
| M14 | digits: 3 not allowed as the first digit | P1 202, P4 5 |
| M15 | digits: 2 never tried as a divisor | P1 7, P2 7, P4 9 |

P1 and P4 each kill all fifteen. P2 sees only the mutations that let a
composite through (M3, M5, M6, M9, M15): the others return a real prime
palindrome, just not the smallest. M4 and M12 lose the one even-length
answer, 11, and fail exactly the n from 8 to 11, some of them drawn
again among the random n; M1 loses it only at n = 11. P3 kills none,
since every arm searches upward from n.

Three earlier mutants were replaced. Two made an arm run on without
end rather than answer wrongly: the ★ arm building even-length
palindromes, which are never prime past 11, ran until an integer
overflow, and the mirror arm's first half a digit short until the
interpreter's step limit. The third was the mirror arm's roll-over from
a first half of all nines to 10...01, which turned out unreachable: that
half mirrors to 99...9, never below x. The branch was taken out of the
arm.

## Verification

Every arm prints the same output as `prime_palindrome.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara
`292a4ca2f0`. Under `karac __mir-run` the arms take under 3 s each but
`scan`, 23 s, and the differential 30 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends run the ★, `scan` and `mirror` arms through
`karac run --legacy --interp`, `karac run --legacy`, `karac build` and a
`KARAC_AUTO_PAR=1` build with the same output. They refuse the `build`
and `digits` arms and the differential at a `*` on a `for` element,
saying the value is not a reference, where v2 yields a reference.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 60,000 random
n of one to eight digits, each length as likely, and the sum and a
checksum of their answers. Every implementation prints `60000 random n
of 1 to 8 digits: answers sum to 822191707095, checksum 353698362`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.50 to 0.58 s | 0.53 s |
| Rust (`rustc -O`) | 0.50 to 0.57 s | 0.51 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.56 to 0.60 s | 0.58 s |
| Go | 0.72 to 0.80 s | 0.75 s |
| Python | 28.4 s | |
| Kāra (`karac build --mir`) | 0.72 to 0.84 s | 0.74 s |
| Kāra, frozen legacy (`karac build`) | 0.57 to 0.62 s | 0.59 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 865's does.

v2 takes 1.28 times Rust's median time under overflow checks, 1.4 times
C's, and 1.25 times legacy's. Nearly all of every program's time is the
trial division, one 64-bit `div` per odd divisor. Under valgrind's
cachegrind C runs 7.75 billion instructions, Rust with overflow checks
8.69 billion, legacy 7.94 billion and v2 10.37 billion, and the three
overflow-checked programs take the same 1.84 billion branches. In the
inner loop of `is_prime` v2 runs two instructions more than legacy per
divisor: it keeps the divisor as `d + 2` and rebuilds `d` with a `lea`,
and checks `d += 2` against a bound with a `cmp` where legacy uses the
`add`'s overflow flag. That was read from the disassembly and not
traced further; the comparison with C and Rust waits until after M4.
