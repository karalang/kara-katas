# 869. Reordered Power of 2

You are given an integer `n`. We reorder the digits in any order
(including the original order) such that the leading digit is not zero.
Return `true` if and only if we can do this so that the resulting number
is a power of two.

```
n = 1   ->  true
n = 10  ->  false
```

**Constraints:** `1 <= n <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `reordered_power_of_2.kara` ★ | digit counts: a reordering keeps exactly n's digits, so n can be reordered into a power of two when some power has the same count of each digit, and a power of two never starts with 0. n's counts are compared with those of 2^0 to 2^29 (2^30 has ten digits, and the one ten-digit n allowed, 10^9, has other digits). O(30 * digits) |
| `reordered_power_of_2_sorted.kara` | sorted digit strings: two numbers are reorderings of each other exactly when their sorted digits spell the same string; n's is compared with those of 2^0 to 2^30 |
| `reordered_power_of_2_trie.kara` | arranging the digits most significant first, each position taking an unused digit, and extending a prefix only when some power of two with as many digits as n starts with it (the prefixes kept in a `Set`); success when every digit is placed. No leading 0 is ever placed, since no power starts with one |
| `reordered_power_of_2_primes.kara` | a product of primes: digit d stands for the d-th prime, a number for the product of its digits' primes, at most 29^10; by unique factorisation two numbers have the same product exactly when they have the same digits |
| `reordered_power_of_2_packed.kara` | packed counts in a set: each digit's count fills four bits at 4 * d of one integer, the packed counts of 2^0 to 2^30 go into a `Set`, and n is true when its own packed counts are in it |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 21 lines: LeetCode's two examples; sixteen
more (orders of the digits of 16, 64, 128, 512 and 1024, and 24, which
is none; 2^29 and 102,356,789, its digits in increasing order with the
1 in front; and 10^9 and 10^9 - 1, LeetCode's largest);
how many n from 1 to 100,000 are true, 376, with a checksum; how many of
20,000 random n up to 10^9 are true, 7; and 600 shuffled powers of two,
20 orders of each of 2^0 to 2^29, all true. `reordered_power_of_2.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every order of n's digits with a nonzero digit first, built
one digit at a time, each tested for a power of two by halving while
even. It checks 11,130 values of n: every n from 1 to 10,000, 100 random
n of up to seven digits and the powers of two below 10^7 against the
statement, and the powers up to 10^9 and 1,000 random n up to 10^9
against the other properties; 137 of them are true.

| | property |
|---|---|
| P1 | the statement's answer (n up to seven digits) |
| P2 | a random order of n's digits, no 0 first, gives the same answer |
| P3 | the digits from largest to smallest give the same answer |
| P4 | a multiple of 3 is never true: no power of two is one, and the digit sum keeps n's remainder by 3 |
| P5 | a random power of two from 2^0 to 2^29, its digits in a random order, is true |
| P6 | the smallest order with no 0 first gives the same answer |

It prints `11130 values of n, 137 true, 291690 checks over 5 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 2^29 left out | P5 381 |
| M2 | ★: zeros not counted | P1 115 |
| M3 | ★: only the even powers | P1 70, P5 5569 |
| M4 | sorted: 2^0 left out | P1 2, P5 332 |
| M5 | sorted: the digits never sorted | P1 92, P2 38, P3 34, P5 8806, P6 71 |
| M6 | sorted: only the lengths compared | P1 9994, P4 3694 |
| M7 | trie: prefixes of longer powers kept too | P1 393, P4 123 |
| M8 | trie: the whole powers left out of the prefixes | P1 130, P5 11130 |
| M9 | trie: a digit not given back after a dead end | P1 37, P5 3400 |
| M10 | primes: 0 given the factor 1 | P1 115 |
| M11 | primes: the powers stopped below 10^8 | P5 1117 |
| M12 | primes: the primes summed, not multiplied | P1 2184, P4 675 |
| M13 | packed: one bit per digit, so counts carry | P1 376, P4 94 |
| M14 | packed: the leading digit not counted | P1 321, P2 340, P3 338, P4 102, P5 6058, P6 340 |
| M15 | packed: n's last digit dropped | P1 392, P2 322, P3 282, P4 84, P5 10507, P6 357 |

No one property kills all fifteen: P1 kills thirteen, and P5 the other
two, M1 and M11, which lose only powers above 10^7, past the statement's
reach here. M2 and M10 are one fault, a 0 that counts for nothing, and
fail the same 115 values of n. P2, P3 and P6 compare an arm with itself
on a reordering, so they see only the mutations whose answer depends on
the order of the digits (M5, M14, M15).

## Verification

Every arm prints the same output as `reordered_power_of_2.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara
`292a4ca2f0`. Under `karac __mir-run` the arms take 4 to 17 s each and
the differential 24 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends refuse all five arms and the differential at
a `*` on a `for` element, saying the value is not a reference, where v2
yields a reference. Legacy `karac build` builds the bench program, whose
binary prints the same line as every other. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: every n from
1 to 1,000,000, counting the true ones, with a checksum. The digit
counts are a `Vec` in Kāra and Rust and a slice in Go, made for every
number, as the arm writes it; C keeps them in arrays on the stack. Every
implementation prints `n from 1 to 1000000: 1036 true, checksum
134332211`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.39 to 0.45 s | 0.41 s |
| Rust (`rustc -O`) | 0.85 to 0.95 s | 0.89 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.85 to 0.95 s | 0.91 s |
| Go | 0.24 to 0.30 s | 0.25 s |
| Python | 12.7 s | |
| Kāra (`karac build --mir`) | 0.62 to 0.75 s | 0.66 s |
| Kāra, frozen legacy (`karac build`) | 0.66 to 0.80 s | 0.71 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 868's does.

v2 takes 0.73 times Rust's median time under overflow checks, 0.93
times legacy's, 1.6 times C's and 2.6 times Go's. Every call of
`digit_counts` makes a new ten-entry vector, 31 million of them: Kāra
and Rust put them on the heap, and Go's compiler, seeing that the slice
does not outlive the call, most likely keeps it on the stack as C does
(inferred from the timings, not traced). Under valgrind's cachegrind C
runs 2.79 billion instructions, Rust with overflow checks 12.70 billion,
legacy 12.12 billion and v2 11.74 billion. The comparison with C and
Rust waits until after M4.
