# 829. Consecutive Numbers Sum

Given an integer `n`, return the number of ways to write `n` as the sum
of consecutive positive integers.

```
n = 5   ->  2     (5 = 2 + 3)
n = 9   ->  3     (9 = 4 + 5 = 2 + 3 + 4)
n = 15  ->  4     (15 = 8 + 7 = 4 + 5 + 6 = 1 + 2 + 3 + 4 + 5)
```

**Constraints:** `1 <= n <= 10^9`.

## Approaches

A run of `k` numbers from `a` sums to `k * a + k * (k - 1) / 2`. So `n`
has a run of length `k` exactly when `n - k * (k - 1) / 2` is a positive
multiple of `k`, and the run is unique for that `k`. The shortest such
sum, `1 + 2 + ... + k`, must not pass `n`, so `k` stays below about the
square root of `2n`.

| file | mechanism |
|---|---|
| `consecutive_numbers_sum.kara` ★ | each length `k` while `1 + 2 + ... + k` fits in `n`, counted when what is left after the triangle is a multiple of `k`. O(sqrt n) |
| `consecutive_numbers_sum_odd.kara` | the odd divisors of `n`, which match the runs one for one: the number of divisors of `n` with its factors of 2 taken out, from its prime factors by trial division. O(sqrt n) |
| `consecutive_numbers_sum_pairs.kara` | the ways to split `2n` into `k * m` with `k < m` and `k + m` odd, since a run of `k` from `a` has `2n = k * (2a + k - 1)`. O(sqrt n) |
| `consecutive_numbers_sum_iter.kara` | the lengths `take_while` the triangle fits, `filter`ed by the remainder and `count`ed, over the open range `1..` |
| `differential.kara` | the four arms against the statement read start by start, four properties |

Every arm prints the same 15 lines: LeetCode's three examples; ten
single numbers (1 to 4; 1,024 and 2^29, which have one run each; 945,
which has 16; 10^9, the largest; 999,999,937, the largest prime below
it; and 918,918,000, which has 256); every `n` from 1 to 3,000, and 100
random numbers up to 10^9, each with a total and a checksum.
`consecutive_numbers_sum.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: from each start `a` from 1 to `n`, add `a`, `a + 1`, ...
until the sum reaches `n`, and count the starts where it lands on `n`.
Its 1,600 cases are numbers up to 600 and come in four kinds of 400: any
number; a power of two times an odd number below 16; a power of one odd
prime from 3 to 13; and a product of the primes 2, 3, 5 and 7.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | `2n` gives the same answer |
| P3 | `n` times an odd prime that does not divide it gives twice the answer |
| P4 | `n` times a number `m` up to about 50 with no factor in common gives the answer times `m`'s |

P2 to P4 follow from the odd-divisor count: doubling adds no odd
divisor, and the count is multiplicative.

It prints `1600 cases, 25600 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run that is exactly `1 + 2 + ... + k` left out | P1 291, P2 330, P3 541, P4 524 |
| M2 | ★: the triangle not halved | P1 1348, P2 1477, P3 922, P4 1472 |
| M3 | ★: the run of length 1 left out | P1 1600, P3 1600, P4 1595 |
| M4 | odd: the factors of 2 kept | P1 402, P2 479, P3 87, P4 352 |
| M5 | odd: the prime left over not counted | P1 1019, P3 332, P4 890 |
| M6 | odd: the exponents added, not multiplied | P1 111, P3 665, P4 625 |
| M7 | pairs: the parity test dropped | P1 741, P2 1477, P3 100, P4 162 |
| M8 | pairs: `k` tried only up to the square root of `n` | P1 802, P2 760, P3 1176, P4 1256 |
| M9 | pairs: `n` split, not `2n` | P1 831, P2 831, P4 1176 |
| M10 | iter: only runs of odd length | P1 1150, P2 292, P3 851, P4 1325 |
| M11 | iter: lengths bounded by the square root of `n` | P1 510, P2 473, P3 1181, P4 1048 |
| M12 | iter: the remainder tested against the next length | P1 1374, P2 1260, P3 1510, P4 1345 |

P1 kills all twelve, and each property kills most. P2 is blind to the
edits that leave the count of odd divisors alone under doubling: M3
loses the run of length 1 from `n` and `2n` alike, and M5 and M6 never
look at the factors of 2. M6 fails P1 on only 111 cases: with one odd
prime found by the trial division, `1 + e` and `e + 1` agree, so it
needs two; P3 and P4, which multiply in further primes, catch it about
six times as often. The obvious edit to the pairs arm's bound, `k * k <=
2n` for `k * k < 2n`, was not used, since it changes nothing: at `k * k
= 2n` the two factors are equal, their sum even, and the pair never
counted.

## Verification

Every arm prints the same output as `consecutive_numbers_sum.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release build
that runs `check`, `__mir-run` and the mutation runs is at kara
`51fae64395`; the debug build that runs `__mir-llvm-run`,
`__mir-llvm-asan` and `build --mir` is at `90714715b1`, four commits
earlier, none of them in the runtime; the runtime archives match both.

Under `karac __mir-run` the ★, odd-divisor and factor-pair arms take 0.2
to 1.2 s and the iterator arm 10.5 s, with the same output; the
differential takes 1.3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy JIT (`karac run`), `karac build` and an auto-par build
print the same output for the other three arms, and the legacy
interpreter (`karac run --interp`) as well. Every legacy backend refuses
the iterator arm and the differential, finding no method `take_while` on
`RangeFrom`. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
numbers between 5 * 10^8 and 10^9, LeetCode's largest, once, and each of
16,000 rounds answers the next one, about 39,000 lengths tried each.
Every implementation prints `16000 rounds of 64 numbers: total 221000,
checksum 875202234`, the Kāra program under `karac __mir-run` included,
in 221 s with the interpreter's step limit raised by
`KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, eight runs of each compiled
program and 13 of v2's, five of them interleaved, and three of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.40 to 1.91 s |
| Rust (`rustc -O`) | 1.41 to 1.67 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.43 to 1.79 s |
| Go | 2.23 to 2.65 s |
| Python | 79.8 to 81.0 s |
| Kāra, legacy (`karac build`) | 1.42 to 1.68 s |
| Kāra (`karac build --mir`) | 1.35 to 1.83 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.59 s, against Rust's
1.44 (1.61 under overflow checks), C's 1.49, legacy's 1.55 and Go's
2.27: level with C, Rust and legacy. Each length tried costs a 64-bit
division for the remainder, and under valgrind's cachegrind the
instruction counts differ more than the times do: v2 runs 20.4 billion
instructions and 4.3 billion branches, Rust 21.0 and 2.5 billion, and C
14.8 and 1.2 billion. Most likely the division's latency sets the pace
of every compiled program alike (not traced). Built for `x86-64-v3`, the
target `karac build` uses, C takes 1.38 to 1.64 s and Rust with overflow
checks 1.38 to 1.64 s, against v2's 1.35 to 1.79 s in the same five
interleaved runs. Python takes 80 s, about 54 times C's time. The
comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-21-46: an open range took no iterator adaptor. `(1..).take(3)`
and `(1..).take_while(..)` were refused as having no such method on
`RangeFrom`, while `(1..).into_iter()` and `(1..).iter()` were refused
as already being an iterator, so no spelling of the iterator arm's
natural form was accepted. design.md § Ranges says `lo..` is iterable
and ended by `take` or the like. It is fixed in kara `2b42975210`, and
the arm is back to `(1..)` (rechecked at kara `13fdc32828`); until then
it used `1..=n`, which `take_while` stops long before its end.

Two neighbours, found while probing that one, hold nothing in this kata.
B-2026-10-21-47, `for i in 1.. { .. }` not parsing, is fixed in kara
`510c9cf71d`: the loop parses now and stops where its parenthesised form
did, at B-2026-10-21-48, the MIR builder refusing a `for` over an open
range as a loop over a collection. That one is fixed in kara
`3cd584acce`: both forms, left by a `break`, pass `karac check` and run
under `karac __mir-run` and `karac __mir-llvm-run` (rechecked at kara
`cd64cc58b3`).
