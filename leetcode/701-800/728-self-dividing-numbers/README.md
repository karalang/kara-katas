# 728. Self Dividing Numbers

A self-dividing number is divisible by every digit it contains, and so
has no digit 0: 128 is one, since 128 % 1, 128 % 2 and 128 % 8 are all
0. Given two integers `left` and `right`, return all the self-dividing
numbers from `left` to `right`, both included, in order.

```
left = 1, right = 22   ->  [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15, 22]
left = 47, right = 85  ->  [48, 55, 66, 77]
```

**Constraints:** 1 <= `left` <= `right` <= 10^4.

## Approaches

Every arm tests each number of the range on its own; they differ in how
they get at its digits.

| file | mechanism |
|---|---|
| `self_dividing_numbers.kara` ★ | the digits peeled off with % 10 and / 10, stopping at the first 0 or the first digit that does not divide the number; O((right - left) * d) time for d digits |
| `self_dividing_numbers_text.kara` | each number written out in decimal and its digits read back as characters |
| `self_dividing_numbers_mask.kara` | the set of each number's digits as a bit mask, made from n / 10's and the last digit, filled from 1 up to right; a number passes when its mask lacks 0 and every digit in it divides the number; O(right) space |
| `self_dividing_numbers_lcm.kara` | a number is divisible by each of its digits exactly when it is divisible by their least common multiple, made from n / 10's and the last digit, 0 standing for a zero digit; O(right) space |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: the two LeetCode examples; the range
of just 1, and of just 10, which has none; 100 to 130; 9,990 to
10,000, where only 9,999 qualifies; 1,111 to 1,150; the whole of 1 to
10,000, with how many there are, their sum and the largest; and
300 random ranges with how many numbers they hold and a checksum.
`self_dividing_numbers.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which asks of each number whether each digit from 0 to 9 appears in it,
by looking at every power of ten up to the number, and keeps it when
0 does not and every digit that does divides it. 3,000 random ranges of
1 to 200 numbers are checked, all within 1 to 3,000, which keeps the two
arms that fill a table up to right quick enough for the interpreter;
368 hold no self-dividing number.

| | property |
|---|---|
| P1 | the list is the definition's |
| P2 | the list is increasing and inside the range |
| P3 | the range cut in two at a random place gives the two lists one after the other |
| P4 | every number in the range whose digits are all the same is in the list, and no number with a 0 is |

It prints `3000 ranges (368 with none), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each digit tested against what is left of the number | P1 2689 |
| M2 | ★: every other digit skipped | P1 2791, P4 1996 |
| M3 | ★: right left out of the range | P1 131, P3 167, P4 15 |
| M4 | text: the last digit not written | P1 2636, P4 2414 |
| M5 | text: a remainder of 1 taken as dividing | P1 2816 |
| M6 | text: left left out of the range | P1 184, P3 136, P4 35 |
| M7 | mask: each number's digits taken from n / 100 | P1 2791, P4 1996 |
| M8 | mask: a digit 1 rejected instead of a 0 | P1 2772, P4 1992 |
| M9 | mask: the digit 9 never tested | P1 2006 |
| M10 | lcm: the digits multiplied instead | P1 2570, P4 863 |
| M11 | lcm: the number with no digits given 0 | P1 2632, P4 950 |
| M12 | lcm: the number tested as a divisor of the multiple | P1 2631, P4 949 |
| E1 | ★: the digit loop running while rest != 0 | 0 |
| E2 | lcm: a zero multiple left to the formula, which keeps it 0 | 0 |
| E3 | mask: a digit's bit tested as > 0 | 0 |

P1 kills all twelve, and three of them only P1 sees: M1 tests each digit
against what is left of the number, M5 takes a remainder of 1 as
dividing, and M9 never tests the digit 9, and none of them touches a
number whose digits are all the same or lets a 0 through. P2 sees none:
every edit still returns numbers from the range in order, so P2 is there
to show the arms keep to the shape of the answer. P3 sees only M3 and
M6, which drop an end of the range, since a cut range then loses the
number at the cut as well. M2 and M7 are one mistake in two arms, every
other digit lost, and fail the same ranges. E1 runs the ★ arm's digit
loop while what is left is not 0, the same test for positive numbers;
E2 leaves a zero multiple to the formula, which keeps it 0; E3 tests a
digit's bit as > 0.

## Verification

Every arm prints the same output as `self_dividing_numbers.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a4b0967495`, whose last compiler change is `d2fb23c673`. The runtime
archives were built after the last runtime change, `3c8e763161`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking, at a `*` over a vector's `iter()`
(`*n` over the numbers found in the harness, `*c` over a number's
`bytes().iter()` in the text arm), since legacy gives those by value
where v2 gives references. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws
40,000 random ranges within 1 to 10,000, the problem's bounds, and
counts and sums the numbers found in each. The C program collects them
into a fresh array per range, as the others do into a vector, slice or
list. Every implementation prints `40000 random ranges: 4077449 numbers,
sum 16140189255`, the Kāra program under `karac __mir-run` included (in
1.2 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.59 to 0.65 s |
| Rust (`rustc -O`) | 0.44 to 0.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.44 to 0.51 s |
| Go | 0.75 to 0.83 s |
| Python | 17.3 to 17.5 s |
| Kāra (`karac build --mir`) | 0.50 to 0.58 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.3 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is a tenth ahead of C and a third ahead of Go at the
medians of the interleaved runs (0.53 s against 0.59 and 0.78), and a
fifth behind Rust (0.44) and a tenth behind Rust under overflow checks
(0.48). Under valgrind's cachegrind all three run about the same work:
4.9 billion instructions for Kāra and Rust and 5.1 for C, 0.9 to
1.0 billion branches, and 110 to 118 million of them mispredicted, the
digit tests on numbers that pass or fail unpredictably. With the counted
work this even, where the differences in time come from was not traced.
The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
