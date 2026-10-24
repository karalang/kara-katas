# 972. Equal Rational Numbers

Given two strings `s` and `t`, each of which represents a non-negative
rational number, return `true` if and only if they represent the same
number. The strings may use parentheses to denote the repeating part of
the rational number.

A rational number can be represented using up to three parts:
`<IntegerPart>`, `<NonRepeatingPart>`, and a `<RepeatingPart>`. The
number will be represented in one of the following three ways:

- `<IntegerPart>`, for example `12`, `0` and `123`;
- `<IntegerPart><.><NonRepeatingPart>`, for example `0.5`, `1.`, `2.12`
  and `123.0001`;
- `<IntegerPart><.><NonRepeatingPart><(><RepeatingPart><)>`, for example
  `0.1(6)`, `1.(9)` and `123.00(1212)`.

The repeating portion of a decimal expansion is conventionally denoted
within a pair of round brackets. For example, 1/6 = 0.16666666... =
`0.1(6)` = `0.1666(6)` = `0.166(66)`.

```
s = "0.(52)",    t = "0.5(25)"    ->  true
s = "0.1666(6)", t = "0.166(66)"  ->  true
s = "0.9(9)",    t = "1."         ->  true
```

**Constraints:** each part consists only of digits; the
`<IntegerPart>` does not have leading zeros (except for the zero
itself); `1 <= <IntegerPart>.length <= 4`;
`0 <= <NonRepeatingPart>.length <= 4`;
`1 <= <RepeatingPart>.length <= 4`.

## Approaches

| file | mechanism |
|---|---|
| `is_rational_equal.kara` ★ | both as fractions in lowest terms: with w the integer and non-repeating digits read as one number, n the number of non-repeating digits and r the repeating digits as a number of k digits, the string is w / 10^n + r / (10^n (10^k - 1)), since a block of k digits repeated forever is that block over k nines. Two fractions in lowest terms are equal exactly when their numerators and denominators are, and 0.(9) = 1 needs no special case |
| `is_rational_equal_common.kara` | no reducing: both fractions are brought to the least common multiple of their denominators, which stays below 10^11, and compared by numerator |
| `is_rational_equal_expand.kara` | long expansions a last digit apart at most: each number written out as 4 integer digits and 24 decimals and cut there. Equal numbers cut this way differ by at most one in the last place (0.999... against 1.000...), and different ones by at least 10^-16, which is 10^8 in the last place, so the numbers are equal exactly when the two 28-digit expansions differ by 0 or 1 |
| `is_rational_equal_canonical.kara` | one way to write each number, with no arithmetic on values: the repeating block, "0" when there is none, is cut to its shortest period and started as early as it can be; a block of 9 becomes one more in the last place before it and a block of 0, whose trailing zeros roll in the same way. Two strings are equal exactly when these forms are |
| `is_rational_equal_longdiv.kara` | the fraction divided out again: each fraction is expanded by long division, noting the remainder before each digit, until a remainder comes back. Long division never ends in repeating nines and finds the shortest block at its earliest start, so the integer part, the digits before the block and the block are the same exactly when the numbers are |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples and nine
more (a bare integer against a trailing zero, zero against a block of
zeros, 9998.(9) against 9999, a block of nines after a non-repeating
digit, a block of three started one place later, two blocks that are
rotations of each other and differ, a block against the same digit not
repeated, a block of 9 against one of 99, and a block of zeros against
padding); and for 300 and then 3,000 random pairs, how many are equal
(100 and 1,000) and a checksum of the answers. A third of the pairs are
one number written two ways, by one to three rewrites that keep every
part within LeetCode's lengths (a digit of the block moved out in
front, the block doubled or halved, a zero or a block of 0 added or
taken away, the last digit lowered by one before a block of 9); a third
are such a pair with one digit of the second string changed; and a third
are two random numbers. `is_rational_equal.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each number's digits, its integer part padded to four digits
and 40 decimals, compared place by place; the two are the same number
when every place agrees, or when at the first place they differ one has
a digit d followed only by nines and the other d + 1 followed only by
zeros. A block starts within 8 places and repeats within 4, so 44
places show everything. It checks 3,200 pairs made as above: 3,000 of
random lengths against the statement, and 200 of LeetCode's longest
strings, four digits in every part, against the other properties; 1,068
of them are equal.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 pairs |
| P2 | each string equals itself, and the order of the two does not matter |
| P3 | each string equals another way of writing it, and the rewritten strings compare as the originals do |
| P4 | adding one to both integer parts (or taking one away, when one of them is 9999) keeps the answer, and adding one to just one of them makes a different number |
| P5 | both numbers times ten, the first decimal moved into the integer part, compare as they did, when both integer parts are below 1,000 |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 pairs: 1068 equal, checksum 327466101, 95000 checks over
5 arms: 0 failures` under `karac __mir-run` (7.5 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the fractions never reduced | P1 384, P3 1870, P5 25, P6 385 |
| M2 | ★: the repeating block over a power of ten | P1 177, P3 995, P5 19, P6 177 |
| M3 | ★: the integer digits counted as decimals | P1 189, P3 1102, P4 2, P5 29, P6 189 |
| M4 | common: every power of ten one too high | P1 233, P3 1315, P5 18, P6 234 |
| M5 | common: the integer part not shifted | P1 186, P3 1082, P4 4, P5 29, P6 186 |
| M6 | common: zeros skipped | P1 20, P3 48, P4 2, P5 6, P6 20 |
| M7 | expand: a last-place difference not allowed | P1 68, P3 304, P6 68 |
| M8 | expand: only 8 decimals | P1 1, P5 1, P6 3 |
| M9 | expand: the block's first digit repeated | P1 207, P3 521, P5 33, P6 227 |
| M10 | canonical: the block never shortened | P1 80, P3 590, P6 81 |
| M11 | canonical: the block never started earlier | P1 190, P3 1103, P5 29, P6 190 |
| M12 | canonical: a 9 bumped past the digits | P1 3, P3 10, P4 4, P5 6, P6 3 |
| M13 | longdiv: every digit 0 | P1 427, P5 106, P6 472 |
| M14 | longdiv: the closing parenthesis read as a digit | P1 336, P3 1716, P5 20, P6 337 |
| M15 | longdiv: a terminating number over ten times its power of ten | P1 155, P3 671, P6 155 |

P1 and P6 kill all fifteen, P3 thirteen (all but M8 and M13), P5 twelve
(all but M7, M10 and M15), P4 four (M3, M5, M6, M12) and P2 none. Every
arm compares two values, forms or expansions made the same way from
each string, so none of these edits can make an arm call a string
different from itself or care which string comes first; P2 guards
against an arm that treats its two arguments differently. M8 sees only
12 places, so it calls two numbers equal when they agree that far,
which the random pairs rarely do. M13 turns every number into its
integer part and the shape of its remainders, which two ways of writing
one number share, so P3 cannot see it.

Ten other edits were tried and set aside. Four failed exactly the same
checks as a kept one: common reading k nines as 10^k + 1, as M4; expand
subtracting without a borrow and subtracting the larger from the
smaller, and canonical reading only a block of 99 as nines, as M7. Two
were sound but beyond three an arm: ★ making the repeating denominator
one too big and comparing only the numerators. Two were equivalent:
canonical keeping trailing zeros after adding one in the last place,
since every 9 before a block of 9 has already rolled into the block, so
the digit that is raised is never a 9 and no zeros appear; and longdiv
starting the block a digit late, which moves one digit from every block
to the end of what comes before it, the same for every number, so equal
numbers still match and different ones still differ. One crashed and was
not counted: common crossing the scale factors overflows. One never
finished under `karac __mir-run`: longdiv reading k nines as a 1
followed by k nines makes denominators such as 19 and 1999, whose long
divisions repeat only after up to hundreds of digits, each looked up in
the list of remainders; `karac __mir-llvm-run` finished it (failing P1,
P3, P5 and P6) and `karac __mir-run` did not within 200 s.

## Verification

Every arm prints the same output as `is_rational_equal.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.30 s (★) to 0.50 s (expand), and the differential 7.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

`canonical` was first written with `let (mut int, mut non, mut rep) =`,
Rust's way of making a tuple's bindings mutable; `karac` refused it with
a diagnostic saying that Kāra writes `let mut (int, non, rep) =`, which
makes every binding mutable, and the arm uses that.

## Benchmarks

The bench program makes 1,000 random pairs once, as the arms' harness
does. In each of 1,000 rounds it runs the ★ arm on every pair, each
round starting from a different one, and folds every answer into a
checksum. Every implementation prints `1000 rounds over 1000 pairs:
334000 equal, checksum 413542311`. Kāra, Rust, Go and C read the
strings in place and allocate nothing in the timed loop.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.098 to 0.143 s | 0.105 s |
| Rust (`rustc -O`) | 0.119 to 0.155 s | 0.122 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.158 to 0.180 s | 0.164 s |
| Go | 0.152 to 0.174 s | 0.169 s |
| Python | 3.5 s | |
| Kāra (`karac build --mir`) | 0.162 to 0.187 s | 0.176 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 33 times
C's.

v2 took 1.07 times Rust's median time under overflow checks and 1.68
times C's. Under valgrind's cachegrind v2 ran 738 million instructions
and 177 million branches with 16.5 million mispredicted, Rust with
overflow checks 724 million, 204 million and 17.2 million, and C 538
million, 108 million and 9.3 million. Which character comes next in a
string, and how many steps Euclid's algorithm takes, change from pair
to pair, and C mispredicts about half as often as the other two; where
those mispredictions come from was not measured.

