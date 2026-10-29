# 1017. Convert to Base -2

Given an integer `n`, return a binary string representing it in base
`-2`. The string has no leading zeros unless it is `"0"`.

```
n = 2  ->  "110"   ((-2)^2 + (-2)^1 = 4 - 2)
n = 3  ->  "111"   (4 - 2 + 1)
n = 4  ->  "100"
```

**Constraints:** `0 <= n <= 10^9`.

## Approaches

Place `i` of a base -2 numeral is worth `(-2)^i`: 1, -2, 4, -8, 16, ...
The even places add and the odd ones take away, and with digits 0 and 1
every integer has exactly one form. The arms differ in where they get
the digits from.

| file | mechanism |
|---|---|
| `negabase.kara` ★ | division by -2: the last digit is `n`'s parity; take it off and divide by -2 to get the number the other digits spell, until nothing is left. O(log n) |
| `negabase_mask.kara` | the odd-bit mask: with `M` set at every odd bit, the digits of `n` are the binary digits of `(n + M) ^ M`, one line. O(1) arithmetic and O(log n) to print |
| `negabase_digits.kara` | carrying signed digits: start from `n`'s binary digits with each odd one made -1 (an odd place's `2^i` is `-(-2)^i`), then carry from the bottom, each digit keeping its parity and handing `(d - r) / -2` up. O(log n) |
| `negabase_greedy.kara` | place values from the top: knowing the range the lower places can reach, set each place exactly when what is left lies outside it. O(log n) |
| `negabase_powers.kara` | adding powers of two: `2^k` is `1` or `11` followed by `k` zeros, and a base -2 adder (a column of 2 or 3 carries -1, a column of -1 carries 1) sums them over `n`'s bits. O(log^2 n) |
| `differential.kara` | the five arms against the value of what they print, six properties |

Every arm prints the same 19 lines: the forms of seventeen values of `n`,
LeetCode's three examples among them, up to `10^9`; and for every `n`
up to 20,000 and for 2,000 random `n` up to `10^9`, the digits and ones
in all, the longest form and a checksum of the forms in order.
`negabase.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and checks 7,456
values of `n`: every one up to 1,365 (the largest value of eleven
digits), the largest value of each odd length and the one after it,
every power of two up to `2^29` and the number below it, and 6,000
random values up to `10^9`.

| | property |
|---|---|
| P1 | the form spells `n`: its digits, weighted by powers of -2, add up to `n` |
| P2 | the form holds only 0s and 1s with no leading zero, and is `"0"` exactly for 0 |
| P3 | for `n` up to 1,365, the form is the one string of at most eleven digits that spells `n`, from a table of all of them (which also checks that no value has two) |
| P4 | a positive `n` has the shortest odd length whose largest value, `(4^k - 1) / 3`, reaches it |
| P5 | `4n` and `4n + 1` have `n`'s form with `00` and `01` added |
| P6 | each arm agrees with at least two of the other four |

The differential prints `7456 values: checksum 960773825, 193375 checks
over 5 arms: 0 failures` under `karac __mir-run` (16 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

P1 compares an `Option[i64]` with `Some(*n)`, where `n` comes from
`ns.iter()`. The natural `Some(n)` is refused: a comparison does not
read the `ref` inside a constructor operand as its value, though a
`let` with a type, an argument and a `vec!` element all do. That is
filed in kara as `B-2026-10-29-35`; `*n` is the explicit read the
language allows.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the digits left last first | P1 7358, P2 3795, P3 1321, P5 7454, P6 7358 |
| M2 | ★: 0 as the empty string | P1 2, P2 2, P3 2, P6 2 |
| M3 | ★: every digit inverted | P1 7454, P2 7454, P3 1397, P5 7454, P6 7454 |
| M4 | mask: the even bits set instead | P1 7454, P3 1397, P4 7454, P5 7454, P6 7454 |
| M5 | mask: or for xor | P1 7456, P2 2, P3 1399, P4 7454, P5 7454, P6 7456 |
| M6 | mask: bit 1 missing | P1 3718, P3 697, P4 28, P5 3718, P6 3718 |
| M7 | digits: the odd bits not negated | P1 7360, P3 1321, P4 6212, P6 7360 |
| M8 | digits: the parity as a signed remainder, `d % 2` | P1 7360, P2 4612, P3 1321, P4 6212, P6 7360 |
| M9 | digits: no room made for the top carry | index out of bounds panic, exit 101 |
| M10 | greedy: only the top of the range tested | P1 7360, P3 1321, P5 7360, P6 7360 |
| M11 | greedy: the low end summing every place | P1 7373, P3 1325, P4 3305, P5 7454, P6 7373 |
| M12 | greedy: too few places | P1 3311, P3 473, P4 3311, P5 3311, P6 3311 |
| M13 | powers: a column of 2 carrying 1 | P1 6792, P3 892, P4 2889, P6 6792 |
| M14 | powers: a column of -1 carrying nothing | P1 6792, P3 892, P4 2372, P6 6792 |
| M15 | powers: a column of 2 kept as a digit | P1 6792, P2 1179, P3 892, P4 1600, P6 6792 |

P1, P3 and P6 kill the fourteen that finish, P4 ten, P5 eight and P2
six; M9 is killed by its bounds check. The checks draw no random number
that depends on an answer, so every mutant sees the same values and
their counts can be compared.

Fifteen other edits were tried and set aside. Four change no answer
here: a mask of 32 bits, which is right for every `n` below about
`5.7 * 10^9`, past the largest the differential asks (`4n` for `n` up to
`10^9`); greedy computing one place more than it needs, whose leading
zero it never prints; digits keeping a top zero on a result of two
digits, and powers keeping top zeros on sums of up to three, neither of
which the differential meets. One never ends: digits carrying with the wrong sign, whose
digits grow without bound until `karac __mir-llvm-run` panics `out of
memory` and the system kills `karac __mir-run`. Eight failed exactly
the same checks as a kept one: ★ taking the digit as a signed remainder
(as M8); ★ dividing by 2, ★ dividing before taking the digit off and
greedy using places of base 2 (as M7); powers
printing its digits lowest first (as M1); and digits negating the even
bits, powers putting the extra 1 on even powers and powers putting each
power one place high (as M4). The other two were killed too, beyond
three per arm: the mask subtracted, which overflows `i64`, and greedy dropping
zeros after the first 1.

## Verification

Every arm prints the same output as `negabase.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error; the differential prints its line under all three. `karac
check --output=json` reports no diagnostic for the five arms, the
differential and the bench program, so `karac fix` had nothing to do.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. The release build is kara `56c60bdf7c`, with
runtime archives rebuilt at `ce706dd131`, the last commit before it to
change the runtime.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

Under `karac __mir-run` the arms take 1.2 s (mask) to 5.1 s (powers).

## Benchmarks

The bench runs the ★ arm in all five languages for every `n` from 0 to
3,000,000, folding each form into a digit count and a checksum: about 65
million digits, each a division by -2 and a character pushed, and a
string built and reversed for every `n`. Every implementation prints
`n = 0..3000000: 65271739 digits, checksum 407000584`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.422 to 0.470 s | 0.440 s |
| Rust (`rustc -O`) | 0.687 to 0.755 s | 0.716 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.657 to 0.768 s | 0.683 s |
| Go | 0.717 to 0.913 s | 0.820 s |
| Python | 12.7 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.694 to 0.772 s | 0.728 s |
| Kāra (`karac build`) | 0.704 to 0.870 s | 0.734 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time equals its real time) and runs as fast as the sequential
one.

v2 took 1.07 times Rust's median time under overflow checks and 1.66
times C's. Rust and Kāra build a growing string and then a reversed
copy of it for every `n`, where C writes into a stack buffer and makes
one allocation of the right size; we did not measure how much of the
gap that is.
