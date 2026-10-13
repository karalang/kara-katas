# 504. Base 7

Given an integer `num`, return a string of its base 7 representation.

```
num = 100  ->  "202"
num = -7   ->  "-10"
```

**Constraints:** `-10^7 <= num <= 10^7`.

## Approaches

Every arm is `fn convert_to_base7(num: i64) -> String`.

| file | mechanism |
|---|---|
| `convert_to_base7.kara` ★ | divide by 7 until nothing is left, keeping each remainder in a `Vec[i64]`; the remainders are the digits, last first, so read them back with `digits.iter().rev()` and `out.push_str(f"{d}")` after a `-` for a negative number |
| `convert_to_base7_recursive.kara` | a negative number is `"-" + convert_to_base7(-num)`, a number below 7 is `f"{num}"`, and any other is `convert_to_base7(num / 7) + f"{num % 7}"` |
| `convert_to_base7_decimal.kara` | build an integer whose decimal digits are the base 7 digits, the k-th remainder worth 10^k, and print it with the input's sign; 10^7 has 9 base 7 digits, so it stays below 10^9 |
| `convert_to_base7_powers.kara` | find the largest power of 7 not above the number, then from it down to 1 push the digit `n / power`, read from a `Vec[char]` of the seven glyphs, and go on with `n % power` |
| `differential.kara` | the four arms on 1,500 random numbers, five properties |

Every arm prints the same 11 lines: the two LeetCode examples, 0, 6,
7, 48, 49, -1, the extremes 10^7 and -10^7, and for 300 random numbers
(from -100 to 100, or from the whole range, in turn) the count of
digits, how many are negative, and a checksum of the strings, each
read back as a decimal number with `i64.parse`, which the base 7 digits
name uniquely. `convert_to_base7.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random numbers, from -400 to 400, from -10^5 to 10^5, or from
the whole range -10^7 to 10^7, in turn.

| | property |
|---|---|
| P1 | the string is the reference's, which at each power of 7, highest first, tries the digits 6 down to 0 for the largest that fits |
| P2 | the string is canonical base 7, an optional `-` and then digits 0 to 6 with no leading zero and no `-0`, and reads back as the number |
| P3 | seven times the number is the same digits and a `0` |
| P4 | the negated number gains or loses the `-`, nothing else |
| P5 | for a number not below 0, the next number's string is this one counted up a digit, carry included |

P5 applies only to the numbers not below 0, so the run makes 26,036
checks rather than 30,000. It prints `1500 cases, 4 arms, 26036
checks, 0 failures` under `karac __mir-run`.

## Mutation testing

Ten edits to `differential.kara`, two to each arm and two equivalent
ones, each run under `karac __mir-run`. All eight non-equivalent ones
are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the digits are not reversed (`digits.iter()`) | P1 1417, P2 1417, P3 1498, P5 505 |
| M2 | ★: the leading digit is dropped (`while n > 6`) | P1 1498, P2 1498, P5 12 |
| M3 | recursive: 7 is one digit (`num <= 7`) | P1 128, P2 128, P5 6 |
| M4 | recursive: the sign is dropped | P1 991, P2 991, P4 1498 |
| M5 | decimal: the places go up by 7, not 10 | P1 1490, P2 1490, P3 1498, P5 203 |
| M6 | decimal: the sign is dropped | P1 991, P2 991, P4 1498 |
| M7 | powers: the last digit is dropped (`while power > 1`) | P1 1500, P2 1500, P3 1297, P4 2, P5 433 |
| M8 | powers: zero gets a sign (`num <= 0`) | P1 2, P2 2, P3 2, P4 2, P5 2 |
| E1 | decimal: the loop runs `while n != 0` | 0 |
| E2 | powers: the power grows `while power <= n / 7` | 0 |

E1 is equivalent because `n` starts at `num.abs()` and only shrinks by
whole division, so it is never below 0. E2 is equivalent because for
whole numbers `power * 7 <= n` holds exactly when `power <= n / 7`
does; it is the form that cannot overflow.

M4 and M6 are the same wrong answer, the sign dropped, written into
two arms, and fail the same cases: every negative number, and P4 in
every case. M5 computes the number itself in decimal, so the sign is
right and P4 cannot see it. M2 and M7 drop a digit from opposite ends.
M2's dropped digit is the leading one, which seven times the number
shares, so P3 passes; M7's is the last one, which seven times the
number turns into the `0` P3 expects, so it fails where the dropped
digit was not 0. M3 goes wrong only where some leading part of the
number is exactly 7, which then prints as `7`. M8 goes wrong only on
0, which comes up twice in the 1,500 cases, and every property sees
both.

## Verification

All four arms print the same output as `convert_to_base7.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `26036 checks, 0 failures` on both and runs clean under the
third. `karac check` passes on every file, the bench program included.

The frozen legacy backends agree on all four arms: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output, and the differential prints `26036 checks, 0
failures` under `karac run --interp` and legacy `karac build`. Legacy
`karac build` warns on the differential that `got` is "moved here, used
again here", where P2 passes `got` to `read_base7`, which v2 reads as
a borrow, and its failure message reads `got` again; the output is
right all the same. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It converts 5,000,001 numbers across
the whole range, -10^7 to 10^7 in steps of 4, reads each string back as
a decimal number, and folds those into a checksum. Every
implementation prints `5000001 numbers: 44137209 characters, checksum
462451096`, the Kāra program under `karac __mir-run` included (in
137 s).

Every mirror keeps the digits in a growable array and formats each
digit into the answer, as the ★ arm's `f"{d}"` formats each into a
fresh `String`: Rust `format!` and `push_str`, Go `strconv.FormatInt`
and `+=`, Python an f-string and `+=`, and C `snprintf` into a small
buffer copied into a `malloc`'d answer. Each reads the string back
with its library parser (`parse`, `strconv.ParseInt`, `int`,
`strtoll`). Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.97 to 2.03 s |
| Rust (`rustc -O`) | 2.38 to 2.73 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.21 to 2.34 s |
| Go | 2.09 to 2.23 s |
| Python | 8.3 to 8.7 s |
| Kāra (legacy `karac build`) | 1.53 to 1.64 s |
| Kāra (`karac build --mir`) | 3.44 to 3.62 s |

Legacy `karac build` builds this program, so `bench.sh` is the
`scripts/new-bench.sh` output unchanged and times the legacy build; the
`--mir` row is timed by hand at kara `486f47f97d`. The v2 build is the
slower of the two, and the f-strings are most of the difference (kara
B-2026-10-13-20, below). Under `karac __mir-llvm-run` the program
prints the same line in 27 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

kara B-2026-10-13-20 (perf, open): an f-string with one integer hole
costs three allocations on the v2 compiled backend. `f"{d}"` lowers to
three runtime calls that format into a thread-local stack of buffers:
the integer is rendered into a temporary `String`, appended to the
buffer, and the buffer is copied into the result. 44 million
`f"{i % 7}"` take 2.7 s on `karac build --mir` against 0.3 s on legacy
`karac build`, about 9 times as long, and close to Rust's `format!`
(1.9 to 2.6 s). There is no integer-to-`char` cast in Kāra (`as` from
an integer to `char` is rejected), so formatting is the natural way to
turn a digit into text, and the ★ arm does it once per digit.
