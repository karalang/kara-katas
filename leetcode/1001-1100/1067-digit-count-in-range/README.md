# 1067. Digit Count in Range

Given a single digit `d` and two integers `low` and `high`, return the
number of times `d` occurs as a digit in all the integers in the
inclusive range `[low, high]`.

```
d = 1, low = 1, high = 13      ->  6    (1, 10, 11, 12, 13: 11 holds two)
d = 3, low = 100, high = 250   ->  35   (103, 113, .., 130 to 139, ..)
```

**Constraints:** `0 <= d <= 9`; `1 <= low <= high <= 2 * 10^8`.

The count over `[low, high]` is the count over `[1, high]` less the
count over `[1, low - 1]`, and the count up to `n` follows from `n`'s
digits alone, so no arm walks the range. A 0 is the one digit that
never leads a number, and every arm has a case for it.

The arms take `d`, `low` and `high` as `i64` and return the count as an
`i64`.

## Approaches

| file | mechanism |
|---|---|
| `digit_count.kara` ★ | place by place: at place `p`, the part of `n` above it, the digit there and the part below. `d` holds that place `p` times in each full turn of the part above, then `p` times, the part below plus one, or not at all for the turn `n` is in, as `n`'s digit there is above, at or below `d`. For `d == 0` the turn whose part above is 0 is left out. O(log n) |
| `digit_count_dp.kara` | digit dynamic programming: the numbers up to `n` written from the top digit down, with the count of `d` so far, whether the digits so far are `n`'s own (so the next is held to `n`'s) and whether a digit other than 0 has come yet. Once free of `n` and begun, the rest depends only on the place and the count, and is remembered (`memo: mut ref Vec[i64]`). O(log^2 n * 10) |
| `digit_count_recursive.kara` | the last digit and the rest: every part from 1 to `n / 10 - 1` comes with all ten last digits, and `n / 10` with those up to `n % 10`, so the parts hold `d` ten times the count up to `n / 10 - 1`, found the same way, and `n % 10 + 1` times `n / 10`'s own; a last digit is `d` once in every ten numbers from `d` (from 10 when `d` is 0). O(log^2 n) |
| `digit_count_blocks.kara` | by length, then in blocks: every shorter number of each length (`d` leads 10^(L-1) of the L-digit ones unless it is 0, and holds each other place in a tenth of them), then the numbers as long as `n` in blocks of 10^k whose last k digits run free, one block for each digit below `n`'s at each place (not 0 at the top). O(log n) |
| `digit_count_string.kara` | the ★ count over `n` written out: at each place, the part before and the part after read back as numbers (`i64.parse(s[0..i])`). O(log^2 n) for the slices and the parsing |
| `digit_count_solution.kara` | LeetCode's Rust template (`struct Solution;`, `i32`, `Self::count`, `Solution::digits_count`): at each place, the turns of the part above that reach `d`, `(a + 9 - d) / 10`, times the place, the part below plus one when the digit there is `d`, and one place less for `d == 0`. Carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's two examples and eight
more, up to `[1, 200000000]`; the sum and a checksum of the answers for
3000 ranges below 12000 and 300 inside `[1, 200000000]`; each digit's
count over `[1, 200000000]` (148888897 zeros, 260000000 ones,
160000001 twos, 160000000 of each other digit); the zeros from 1 to each
power of ten, the ones over each length of number, and each digit of
199999990 alone. `digit_count.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number of the range taken apart digit by digit and the
digits equal to `d` counted. It checks 2000 problems: 1000 ranges inside
`[1, 199]` and 1000 of up to 1000 numbers from below 3000, each with a
random `d`. Every random choice of a problem is drawn before any arm
answers, so a wrong arm cannot change the problems the others see.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the range cut in two at a random point answers the sum of its halves |
| P3 | the ten digits' counts over the range add up to the number of digits written in it |
| P4 | `[10 * low, 10 * high + 9]`, every number of the range with each digit appended, answers ten times the count and one more for each number of the range |
| P5 | the range widened by one number at the top answers the count and that number's own digits equal to `d`, and a single number up to 200000000 answers its own |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 778258758, 84000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python
reading of the same 2000 problems gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm; every kept edit fails the same way under both backends, none
by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the place equal to `n` never visited (`p < n`) | P1 2, P3 25, P4 2, P5 1, P6 2 |
| M2 | ★: `n` itself not counted at a place holding `d` | P1 798, P3 716, P4 798, P5 890, P6 798 |
| M3 | ★: a digit equal to `d` counted as a full turn | P1 610, P3 1962, P5 1496, P6 610 |
| M4 | dp: each number counted with one `d` more | P1 2000, P3 2000, P4 14, P5 4000, P6 2000 |
| M5 | dp: a free digit never 9 | P1 1682, P3 1958, P4 1981, P5 215, P6 1682 |
| M6 | dp: remembered by place alone, not the count so far | P1 1546, P3 1641, P4 1965, P5 143, P6 1546 |
| M7 | recursive: each full part counted nine times | P1 1539, P3 1950, P4 1963, P5 153, P6 1539 |
| M8 | recursive: `n`'s own part one number short | P1 616, P3 792, P4 826, P5 93, P6 616 |
| M9 | recursive: a part's leading digit never counted | P1 301, P3 1967, P4 28, P5 358, P6 301 |
| M10 | blocks: the one-digit numbers left out | P1 91, P3 102, P4 91, P6 91 |
| M11 | blocks: the free digits counted as one place | P1 927, P3 927, P4 1905, P5 45, P6 927 |
| M12 | string: the part after read with the digit itself | P1 542, P3 1958, P4 315, P5 86, P6 542 |
| M13 | string: a digit one above `d` counted as below it | P1 720, P3 921, P5 793, P6 720 |
| M14 | solution: the turns reaching `d` counted one short | P1 856, P3 716, P5 881, P6 856 |
| M15 | solution: the part below added only at the top place | P1 679, P3 1721, P4 1, P5 1736, P6 679 |

P1, P3 and P6 kill all fifteen, P5 fourteen, P4 twelve and P2 none.
Every arm answers `F(high) - F(low - 1)` for its own count `F` up to a
number, so a wrong `F` still splits a range exactly into its halves: P2
sees only an edit to `low` or `high` themselves, and two of those are
among the edits not kept (low left out, 520 failures each). P5 misses
the one-digit numbers left out (M10): that error depends only on how
many digits `n` has, so it cancels between the counts up to two
neighbours. P4 misses three edits to how `n`'s digit at a place compares
with `d` (M3, M13, M14). Appending a digit moves every place up one and
makes the same error ten times larger, as P4's ten times the answer
expects, and both ends of the longer range end in 9, so an error at the
new last place falls on both and cancels.

Two of the thirty edits are not usable. The string arm's `before == 0`
made `before < 0` survives: it is equivalent, since `before` is 0 only
at the top place, whose digit is never 0, so `(before - 1) * p` takes
back the `p` that the digit above `d == 0` adds again. The dp arm held
to `n`'s digits for good (`held` for `held and x == top`) is never free
of `n`, so nothing is remembered: it fails 11084 checks compiled but
runs out the time limit under the interpreter, so it does not fail the
same way under both. Of the other thirteen not kept, four fail as a kept
edit or as each other: a 0 counted in front of the number (★), as a
leading digit of the shorter numbers (blocks) and not taken back at the
top place (solution) all fail 857 checks the same way; `n` itself not
counted in the blocks arm fails as M2; `low` left out (★, and the
solution's crossing to `i32`) and the top place never visited (string,
solution) fail in pairs. The dp arm's leading 0 counted, the recursive
arm's number 0 counted for a last 0 and its last digit `d` counted from
`d + 10`, the blocks arm's 0 allowed to lead and the string arm's number
after `high` counted each fail in a way of their own.

## Verification

Every arm prints the same output as `digit_count.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.2 s to 1.3 s (dp) and
the differential 11.2 s.

Every file went through `karac fix`. In every file it cast the `pow`
exponents (`10.pow((l - 1) as u32)`). The Rust arm reaches its
last fix in two rounds: the syntax (`struct Solution {}`, `Self::count`
to `Solution.count`, `Solution::digits_count` to
`Solution.digits_count`), then the three `10.pow(k)` exponents to
`k as u32`. The kata found two gaps in `karac fix`, fixed in kara
`d9a6a4fd5a` with `tests/kata_1067_check_gaps.rs`:

- **`Self::f(..)` was mangled.** The parser's Rust-path recovery knew
  `Type::f`, not `Self::f`: `karac check` reported a missing semicolon
  after `Self`, and `karac fix` applied it, writing `Self;::count(..)`.
  Now `Self::` inside an impl is reported as Rust's path with the fix
  `Solution.`, the type the impl names; outside an impl the error names
  the type to write and offers no fix.
- **`pow`'s exponent cast had no fix.** `pow expects an exponent of type
  u32, got i64 (cast with as u32)` said what to write but left it by
  hand. It is now machine-applicable, with parentheses when the exponent
  is not a single term (`(k - 1) as u32`).

One error is left by hand. `let mut res = 0; let mut p = 1;` in the
Rust arm become `i64`, since an operand of `res += .. * p` does not fix
a literal's type, so `count`'s `res` return draws an `i64` to `i32`
narrowing error with no fix. The arm writes `let mut res: i32 = 0; let
mut p: i32 = 1;`. By the ruling on kara `B-2026-11-07-57`, a
compound assignment's operand does not fix a literal's type, so the
error stands; what is missing is its fix, the annotation, which is kara
`B-2026-11-08-20`.

## Benchmarks

The bench builds a million queries once, in all five languages, each a
random digit and a range inside `[1, 200000000]`, then answers each with
the ★ arm's count: two counts up to a number, each nine places at most.
Every implementation prints `1000000 calls: answers sum 56949830724239,
checksum 152955095`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with kara `d9a6a4fd5a`
on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.176 to 0.191 s | 0.179 s |
| C (`clang -O3`) | 0.170 to 0.196 s | 0.181 s |
| Kāra (`karac build`) | 0.179 to 0.193 s | 0.183 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.180 to 0.202 s | 0.185 s |
| Rust (`rustc -O`) | 0.181 to 0.201 s | 0.187 s |
| Go | 0.344 to 0.533 s | 0.389 s |
| Python | 4.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.169 s) is below its real time.

Kāra, C and both Rust builds run within the noise of each other. The
work is division: each place divides `n` by `p * 10` and by `p`, which
no compiler can turn into a multiplication because `p` changes. Under
callgrind Kāra runs 812 million instructions, checked Rust 781 million,
plain Rust 761 million and C 660 million, and the difference does not
show in the time, which the divisions set. All four come from LLVM,
which on x86-64 tests whether both operands of a 64-bit division fit in
32 bits and then uses the much cheaper 32-bit `div`; every number here
is below 2^31, so every division takes that path. Go divides with a
64-bit `idiv` every time, after a test for a divisor of -1, which is the
likely cause of its 2.1x (inferred from the code, not measured with
counters).
