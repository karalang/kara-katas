# 906. Super Palindromes

Let's say a positive integer is a **super-palindrome** if it is a
palindrome, and it is also the square of a palindrome.

Given two positive integers `left` and `right` represented as strings,
return the number of super-palindromes integers in the inclusive range
`[left, right]`.

```
left = "4", right = "1000"  ->  4    (4, 9, 121 and 484; 676 is a palindrome but 26 is not)
left = "1", right = "2"     ->  1
```

**Constraints:** `1 <= left.length, right.length <= 18`; `left` and
`right` consist of only digits, cannot have leading zeros, and
represent integers in the range `[1, 10^18 - 1]`; `left` is less than
or equal to `right`.

## Approaches

A super-palindrome below 10^18 is the square of a palindrome below 10^9,
so every arm builds the palindromic roots rather than looking at the
numbers in the range.

| file | mechanism |
|---|---|
| `superpalindromes_in_range.kara` ★ | each number `half` below 10^5 gives two roots, its digits followed by their reverse with and without the last digit; for each length the roots grow with `half`, so stop once a square passes `right`, and keep a square in range that reads the same backwards as a string. O(right^(1/4)) roots |
| `superpalindromes_in_range_numeric.kara` | the same roots and test without strings: digits peeled off with `% 10` and appended, a square reversed the same way. O(right^(1/4)) roots |
| `superpalindromes_in_range_digits.kara` | a palindrome's square reads the same backwards exactly when squaring carries nothing, so no root digit is above 2 except in the root 3: halves counted in base 3, mirrored, squared and tested, and 3 on its own |
| `superpalindromes_in_range_squares.kara` | squaring carries nothing exactly when the middle column, the sum of the squares of the root's digits, is at most 9: roots filled from both ends inward never letting that sum pass 9, each finished root counted when its square is in range, with no palindrome test at all |
| `superpalindromes_in_range_recursive.kara` | every palindromic root, filled from both ends inward with any digits, for each length whose smallest root's square is within `right`; each square tested like the ★ arm's |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and eight
more (`1`–`1`, `9`–`9`, `10`–`120`, `121`–`121`, `122`–`483`,
`1`–`10000`, `40804`–`44944` and `1000000`–`999999999`); for 60 random
ranges with ends below 10^1 to 10^12, the sum and a checksum of the
counts; and three of LeetCode's largest: everything below 10^18 (70),
the 17-digit numbers (22) and the 18-digit numbers (none, since an
18-digit square needs a root of at least 316,227,767 and every root
with no digit above 2 is smaller). `superpalindromes_in_range.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every number in the range tried, and counted when it reads
the same backwards and some number that also does squares to it. It
checks 3,200 random ranges: 3,000 of up to 300 numbers below 20,000
against the statement, two thirds of them around the square of a
palindrome below 142, and 200 anywhere below 10^8 against the other
properties; the ★ arm finds 2,518 super-palindromes in them in all.

| | property |
|---|---|
| P1 | the statement's count, on the small ranges |
| P2 | the range cut in two at a random place: the two parts' counts sum to the whole |
| P3 | the count from 1 to `right` less the count from 1 to `left - 1` |
| P4 | the square of a random palindrome made from a half below 100 (below 15 on the small ranges), as a range of one number, counts 1 exactly when it reads the same backwards |
| P5 | a range wider by up to 999 at each end counts at least as many |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every range. It prints `3200 ranges, 2518
super-palindromes found, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every palindrome square counted | P1 1489, P4 2135, P6 1685 |
| M2 | ★: odd-length roots built with the last digit doubled | P1 1224, P4 1065, P6 1239 |
| M3 | ★: a root whose square is exactly `right` never tried | P1 437, P2 161, P3 36, P4 1065, P6 437 |
| M4 | numeric: the last digit never mirrored | P1 1230, P4 1065, P6 1245 |
| M5 | numeric: `left` itself left out | P1 543, P2 21, P3 16, P4 1065, P6 543 |
| M6 | numeric: odd-length roots mirrored two digits short | P1 893, P4 753, P6 908 |
| M7 | digits: the root 3 forgotten | P1 550, P4 98, P6 550 |
| M8 | digits: a 0 put between the half's digits | P1 482, P4 513, P6 497 |
| M9 | digits: the last digit never mirrored | P1 853, P4 508, P6 867 |
| M10 | squares: digit squares summing to 10 allowed | P4 93, P6 16 |
| M11 | squares: the middle digit counted twice | P1 702, P4 191, P6 702 |
| M12 | squares: `left` ignored | P1 2473, P2 3171, P3 2673, P4 3084, P6 2673 |
| M13 | recursive: no digit 2 | P1 798, P4 416, P6 812 |
| M14 | recursive: no 0 inside a root | P1 164, P4 201, P6 178 |
| M15 | recursive: each length's smallest root taken as 1 more than it is | P1 164, P3 168, P4 200, P6 164 |

P4 and P6 kill all fifteen and P1 kills fourteen; P3 kills four and P2
three; P5 kills none. M10 is the one P1 misses: the smallest root whose
digits' squares sum to 10 is 1221, whose square 1,490,841 is far above
the small ranges, and P4's random squares reach it. P5 can only see a
count that falls as its range grows, and every mutant still counts the
members of some fixed set that lie in the range (M12's set test just
ignores `left`), so each count still grows with it. P2 and P3 see only
the mutants whose counts depend on where the range ends rather than on
which numbers are in it: M3 and M5 drop a number at an end, M12 ignores
`left`, and M15 (P3 only) skips a whole length of roots for some values
of `right`.

One mutant was replaced. The first M8 read each half's digits as
remainders mod 2 while still dividing by 3, which made some halves 0,
so a root was 0 and the differential stopped with a division by zero
in `right / root`.

## Verification

Every arm prints the same output as `superpalindromes_in_range.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.2 to 15.5 s
each (the ★ arm, which formats and reverses two strings for each of
about 200,000 roots on the two widest ranges, 15.5 s; the recursive arm
5.1 s; the others about a second or less) and the differential 29 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy lanes split. The numeric and digits arms print the
same output under the legacy interpreter, the legacy JIT and both legacy
builds, with and without auto-par. The ★ arm prints it under the legacy
interpreter, but the legacy JIT and both legacy builds stop at codegen
on the `chars().rev()` that reverses a string: `Iterator.rev()` is not
yet supported there "for this chain shape". The bench program stops
there too. Every legacy lane refuses the squares and recursive arms and the
differential: `*d` on an element of `.iter()` is rejected, because
legacy's iterator gives the value itself. Legacy is frozen, so none of
this is filed.

## Benchmarks

The bench program uses the ★ arm on 40 random ranges below 10^18, given
as strings, each wide enough that every root up to its end is built: on
the order of 200,000 roots a range, each formatted, reversed, parsed
and its square formatted and reversed again. Each query folds its count
into a checksum. Every implementation builds its strings the same way
(C with `snprintf` and `strtoll`, Go with `strconv`). Every
implementation prints `40 ranges below 10^18: counts summing to 72,
checksum 416592972`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.50 to 0.62 s | 0.52 s |
| Rust (`rustc -O`) | 0.54 to 0.73 s | 0.61 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.53 to 0.73 s | 0.58 s |
| Go | 0.41 to 0.53 s | 0.47 s |
| Python | 1.33 s | |
| Kāra (`karac build --mir`) | 0.64 to 0.85 s | 0.69 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build the bench
program (above), so it has no row.

Python is only about 2.5 times slower than C here, because almost all
of the work is converting numbers to and from text, which Python does
in C. Go is the fastest. v2 takes 1.18 times Rust's median time under
overflow checks and 1.30 times C's. Under valgrind's cachegrind C runs
7.69 billion instructions and 0.99 billion branches, Rust with overflow
checks 8.42 billion and 1.33 billion, and v2 9.71 billion and 1.54
billion; C mispredicts 25 million times, Rust 54 million and v2 36
million. So v2 runs 15% more instructions than Rust with overflow
checks; where they go was not profiled. The comparison with C and Rust
waits until after M4.
