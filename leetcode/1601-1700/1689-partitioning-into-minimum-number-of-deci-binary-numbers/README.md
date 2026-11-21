# 1689. Partitioning Into Minimum Number Of Deci-Binary Numbers

A decimal number is called **deci-binary** if each of its digits is
either `0` or `1` without any leading zeros. For example, `101` and
`1100` are **deci-binary**, while `112` and `3001` are not.

Given a string `n` that represents a positive decimal integer, return
*the **minimum** number of positive **deci-binary** numbers needed so
that they sum up to* `n`*.*

```
n = "32"                       ->  3
n = "82734"                    ->  8
n = "27346209830709182346"     ->  9
```

**Constraints:** `1 <= n.length <= 10^5`; `n` consists of only digits;
`n` does not contain any leading zeros and represents a positive
integer.

## Approaches

| file | mechanism |
|---|---|
| `deci.kara` ★ | a deci-binary number adds at most 1 to each digit, so a digit d needs d of them, and d suffice (the k-th has a 1 wherever the digit is at least k): the largest digit, one pass over the bytes. O(n) |
| `deci_chars.kara` | each character read by `to_digit(10)`, the largest kept by `max()`. O(n) |
| `deci_peel.kara` | the deci-binary numbers taken off one at a time: each round takes 1 from every digit not yet 0, until all are, and the rounds are counted. O(9n) |
| `deci_solution.kara` | a Rust solution as LeetCode's Rust users write it, the largest byte by `bytes().max()` less `b'0'`, `as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, 1, and
1000; then the answers summed and a checksum for 3000 random numbers of
up to 10 digits, 300 of up to 1000 and 10 of up to `10^5`, each number's
digits up to a random top from 1 to 9. `deci.py` mirrors the ★ arm and
its output is byte-identical.

```
3
8
9
1
1
3000 numbers of up to 10 digits: answers sum to 13016, checksum 436506849
300 numbers of up to 1000 digits: answers sum to 1468, checksum 721277462
10 numbers of up to 100000 digits: answers sum to 41, checksum 840757317
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, by value rather than by digit: for every n below 10000, the
fewest deci-binary numbers that sum to it, carries allowed, from a table
over the value that tries each of the deci-binary numbers below 10000.
It checks 3000 random n from 1 to 9999, each with a digit to write after
it. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the digits sorted, largest first, give the same answer |
| P3 | n written twice gives the same answer |
| P4 | a digit d written after n gives the larger of the answer and d |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 207834101, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the same table by value, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M4, M6 and M8 each give the smallest
digit, or 0 where one is 0, and fail the same checks; so do M9 and M10,
one more than the answer. An edit that keeps a digit of 1 from going down
(`*d > 1` in the peel arm) never ends, and one that skips the first digit
of `chars` fails `unwrap()` on a one-digit n, so neither was used.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last digit, not the largest | P1 2018, P2 2031, P4 1403, P5 2018 |
| M2 | ★: the first digit skipped | P1 664, P2 1753, P3 664, P5 664 |
| M3 | ★: `min` for `max` | P1 3000, P4 2715, P5 3000 |
| M4 | chars: `min()` for `max()` | P1 2991, P4 2681, P5 2991 |
| M5 | chars: only the first two digits | P1 1239, P2 1239, P4 791, P5 1239 |
| M6 | peel: rounds only while no digit is 0 | P1 2991, P4 2681, P5 2991 |
| M7 | peel: a round clears every digit | P1 2997, P4 2404, P5 2997 |
| M8 | solution: the smallest byte | P1 2991, P4 2681, P5 2991 |
| M9 | solution: one more | P1 3000, P4 458, P5 3000 |
| M10 | peel: the rounds start at 1 | P1 3000, P4 458, P5 3000 |

## Benchmarks

The bench draws 100 random numbers of `10^5` digits, LeetCode's longest,
each with digits up to a random top, all of them first, then answers
each 50 times by the ★ arm in all five languages. Every implementation
prints `100 numbers of 100000 digits, 50 rounds: answers sum to 24600,
checksum 456192326`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.045 s |
| C (`clang -O3`) | 0.163 s |
| Go | 0.285 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.429 s |
| Kāra (`karac build`) | 0.431 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.564 s |
| Python | 16 s |

The sequential Kāra build takes 9.53x Rust's time and 0.76x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.412 s and 0.424 s on one
run).

## Verification

All four arms print the same output as `deci.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The chars and peel arms checked clean as first written. The ★ arm keeps
its largest digit in `let mut largest = 0`, which `max` with a byte
types `u8`, and returned it `as i32`; the `lossless_cast` lint saw that
a `u8` widens to `i32` by itself, and `karac fix` dropped the cast.

LeetCode's Rust solution took one `karac fix` of 4 edits:
`struct Solution {}` added, `.iter()` put before `max()` (Kāra's
`bytes()` is a slice, and an adaptor on it wants an explicit `.iter()`),
the widening `as i32` dropped, and the harness's `n.clone()` passed as
`n` (`redundant_clone`).

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
