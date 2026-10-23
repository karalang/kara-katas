# 878. Nth Magical Number

A positive integer is magical if it is divisible by either `a` or `b`.
Given the three integers `n`, `a`, and `b`, return the `n`-th magical
number. Since the answer may be very large, return it modulo `10^9 + 7`.

```
n = 1, a = 2, b = 3  ->  2
n = 4, a = 2, b = 3  ->  6
```

**Constraints:** `1 <= n <= 10^9`, `2 <= a, b <= 4 * 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `nth_magical_number.kara` ★ | binary search on the answer: the magical numbers up to x are the multiples of a and of b less those of lcm(a, b), `x / a + x / b - x / lcm`, a count that only rises with x, so the n-th is the smallest x whose count reaches n, searched for below n * min(a, b). O(log(n min(a, b))) |
| `nth_magical_number_merge.kara` | whole periods, then a merge: the magical numbers repeat with period lcm(a, b), each period holding `lcm / a + lcm / b - 1` of them, so n = q * per + r is q periods on from the r-th of the first period, found by merging the multiples of a and of b in order. O(a + b) |
| `nth_magical_number_period.kara` | whole periods, then a binary search for the r-th within one period, where no number below the lcm is a multiple of both. O(log lcm) |
| `nth_magical_number_listed.kara` | one period listed: the multiples of a and of b up to the lcm, sorted, with the lcm once; the n-th is (n - 1) / per periods on from entry (n - 1) % per. O((a + b) log(a + b)) |
| `nth_magical_number_gallop.kara` | galloping up, then binary search: from the smaller of a and b the bound doubles until the count reaches n, and a binary search between half the bound and the bound finds the answer |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more (`n = 5, a = 2, b = 4`, where every multiple of 4 is one of 2;
`n = 3, a = 6, b = 4`; a = b = 4 x 10^4, LeetCode's largest, with n = 1
and n = 10^9; n = 10^9 with a = 2, b = 3 and with a = 39,999, b =
40,000; n = 999,999,999 with a = b = 2; and `n = 123456789, a = 210, b
= 330`, which share the factor 30); the answers of 3,000 cases with n up
to 100 and a, b up to 20, 835,965 in all; and 200 cases of LeetCode's
sizes, a fifth of them with b a multiple of a, with a checksum.
`nth_magical_number.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the positive integers 1, 2, 3, ... in turn, each divisible by
a or by b counted, until the n-th. It checks 1,800 cases: 1,500 with n up
to 200 and a, b from 2 to 30 against the statement, and 300 of
LeetCode's sizes, half of them with n up to 2 x 10^4 so that the answer
stays below the modulus, against the other properties. The ★ arm's
answers sum to 77,443,195,429.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | an answer below the modulus is divisible by a or b, with n magical numbers up to it and n - 1 below it |
| P3 | a and b swapped give the same answer |
| P4 | a and b both multiplied by c, 2 to 4, multiply an answer below the modulus by c |
| P5 | with b a multiple of a, the answer is n * a |
| P6 | n larger by one period's count, `lcm / a + lcm / b - 1`, makes the answer larger by the lcm, modulo 10^9 + 7 |

It prints `1800 cases, answers sum to 77443195429, 50805 checks over 5
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the count asked to pass n | P1 1252, P2 1401, P6 8 |
| M2 | ★: common multiples counted twice | P1 1343, P2 1427, P5 1743, P6 1663 |
| M3 | ★: the search capped one below n * min(a, b) | P1 248, P2 254, P4 254, P5 1758, P6 8 |
| M4 | merge: the lcm counted twice in a period | P1 1343, P2 1427, P5 1743, P6 1663 |
| M5 | merge: the larger multiple taken first | P1 1165, P2 1313, P3 1603, P4 5 |
| M6 | merge: whole periods counted from n - 1 | P1 194, P2 194, P5 1093 |
| M7 | period: the count asked to pass r | P1 1306, P2 1461, P4 136, P5 665 |
| M8 | period: the lcm taken as a * b | P1 594, P2 632, P4 1320, P5 1743, P6 453 |
| M9 | period: a whole number of periods taken one period too far | P1 194, P2 194, P5 1093 |
| M10 | listed: the period left unsorted | P1 1275, P2 1423, P3 1746, P4 1 |
| M11 | listed: the lcm listed twice | P1 1343, P2 1427, P5 1743, P6 1663 |
| M12 | listed: the entry one on taken | P1 1446, P2 1601, P5 1153 |
| M13 | gallop: the search starting one too high | P1 6, P2 6, P4 6, P6 7 |
| M14 | gallop: common multiples taken as multiples of a * b | P1 594, P2 632, P4 1320, P5 1743, P6 453 |
| M15 | gallop: doubling past a bound that already reaches n | P1 51, P2 51, P4 51, P5 56, P6 75 |

P1 kills all fifteen. M2, M4 and M11 are one fault in three arms, the
lcm counted twice, and fail the same cases; so are M8 and M14, the lcm
taken as a * b. M6 and M9 fail the same cases, those where n is a
whole number of periods, the one answering a period short and the other
a period too far. Three mutants tried first were replaced. In the merge
arm, a common multiple stepped past for a only (the third branch, where
the next multiples of a and b are equal) was equivalent: the first
common multiple is the lcm, the last number of the period, and the merge
stops before it, at r < per, so the branch never runs and the arm could
drop it. A period one number short in the period arm, and the lcm left
out of the listed arm's period, made a period of a = b hold no numbers
and divided by zero; M9 and M10 replace them.

## Verification

Every arm prints the same output as `nth_magical_number.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `89d76e3ff2` and the runtime
archives at `e903d5b111`, with no runtime change between them. Under
`karac __mir-run` the arms take under 2 s each and the differential 6
s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends (its interpreter and JIT, and `karac build
--legacy` with and without auto-par) print the same output for the ★,
merge, period and gallop arms, and their JIT and builds for the listed
arm too. The legacy interpreter stops on the listed arm asking for an
allocation of 204,794,880,128 bytes, and every legacy lane stops on the
differential out of memory (the interpreter asking for 56,588,874,112
bytes), where v2 runs both, under the sanitizer as well. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 1,000,000 cases
of LeetCode's sizes, n up to 10^9 and a, b from 2 to 4 x 10^4, drawn
from the same generator in each language as they are solved, summing
the answers and a checksum. Each case takes up to about 45 steps of the binary
search, each with three divisions. Every implementation prints
`1000000 cases: answers sum to 499881535048781, checksum 471998361`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.65 to 0.69 s | 0.66 s |
| Rust (`rustc -O`) | 0.66 to 0.70 s | 0.68 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.66 to 0.70 s | 0.68 s |
| Go | 0.69 to 0.72 s | 0.70 s |
| Python | 12.1 s | |
| Kāra (`karac build --mir`) | 0.67 to 0.72 s | 0.69 s |
| Kāra legacy (`karac build --legacy`) | 0.67 to 0.68 s | 0.67 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 877's does.

v2 takes 1.01 times Rust's median time under overflow checks, 1.05
times C's and 1.03 times legacy's. Under valgrind's cachegrind C runs
1.63 billion instructions, Rust with overflow checks 1.93 billion,
legacy 1.77 billion and v2 2.20 billion, so v2's extra checks cost
instructions but not time: the 64-bit divisions, each waiting on the
search's last step, most likely set the time in every language
(inferred from the timings, not traced). The comparison with C and Rust
waits until after M4.
