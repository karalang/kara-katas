# 1694. Reformat Phone Number

You are given a phone number as a string `number`. `number` consists of
digits, spaces `' '`, and/or dashes `'-'`.

You would like to reformat the phone number in a certain manner. Firstly,
**remove** all spaces and dashes. Then, **group** the digits from left to
right into blocks of length 3 **until** there are 4 or fewer digits. The
final digits are then grouped as follows:

- 2 digits: A single block of length 2.
- 3 digits: A single block of length 3.
- 4 digits: Two blocks of length 2 each.

The blocks are then joined by dashes. Notice that the reformatting
process should **never** produce any blocks of length 1 and produce **at
most** two blocks of length 2.

Return *the phone number after formatting.*

```
number = "1-23-45 6"     ->  "123-456"
number = "123 4-567"     ->  "123-45-67"
number = "123 4-5678"    ->  "123-456-78"
```

**Constraints:** `2 <= number.length <= 100`; `number` consists of
digits and the characters `'-'` and `' '`; there are at least **two**
digits in `number`.

## Approaches

| file | mechanism |
|---|---|
| `phone.kara` ★ | the digits collected into a `String` by `filter(is_ascii_digit)`; blocks of three cut as `Str` slices of it while more than four are left, then two of two or one of the rest, joined by `join("-")`. O(n) |
| `phone_sizes.kara` | the block sizes from the count d alone: all threes when d % 3 is 0, a last two when it is 2, and two last twos when it is 1; then the digit bytes cut by them. O(n) |
| `phone_recursive.kara` | the digits kept by a loop, then `blocks` by recursion: up to three are one block, four are two of two, and more are three, a dash and the rest, matched on the length with a range pattern. O(n^2) for the copies |
| `phone_solution.kara` | a Rust solution as LeetCode's Rust users write it, the digits as a `Vec<char>` and each block pushed by `res.extend(&digits[i..i + 3])`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 10 lines: LeetCode's three examples, two
digits, four, five, and seven among spaces and dashes; then the dashes in
the answers and a checksum of their bytes for 3000 random numbers of up
to 12 characters, 300 of up to 100 and 10 of up to `10^5`, each with at
least two digits. `phone.py` mirrors the ★ arm and its output is
byte-identical.

```
123-456
123-45-67
123-456-78
12
12-34
123-45
123-45-67
3000 numbers of up to 12 characters: 4183 dashes, checksum 553500610
300 numbers of up to 100 characters: 4016 dashes, checksum 8760743
10 numbers of up to 100000 characters: 132247 dashes, checksum 801915659
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, by its rules rather than its steps: the spaces and dashes
removed, every cut of the digits into blocks of 2 and 3 is listed, and
the one cut with at most two blocks of 2 and no block of 3 after one of
2 is the answer (the check asserts that exactly one is). It checks 3000
random numbers of 2 to 14 characters, at least two of them digits. Every
case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer's digits are the number's, in order |
| P3 | every block is 2 or 3 long, at most two are 2, and none of 3 follows one of 2 |
| P4 | the digits alone, each followed by a space, give the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 616177113, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the same rules over `itertools.product`, gives
the same checksum. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M2, M4, M6 and M7 each break only a
number whose digit count leaves 1 over three, and fail the same 909
problems; M9 and M10 break the 1907 that do not end in a block of 3.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: blocks of three cut only while more than five are left | P1 844, P3 844, P5 844 |
| M2 | ★: the second of two last blocks of two dropped | P1 909, P2 909, P5 909 |
| M3 | ★: only spaces removed, dashes kept | P1 1117, P3 1117, P4 1117, P5 1117 |
| M4 | sizes: a last three and one for two twos | P1 909, P3 909, P5 909 |
| M5 | sizes: no dash after the first block | P1 2449, P3 2449, P5 2449 |
| M6 | recursive: four digits left as one block | P1 909, P3 909, P5 909 |
| M7 | recursive: four digits cut three and one | P1 909, P3 909, P5 909 |
| M8 | recursive: only spaces removed, dashes kept | P1 1117, P3 1117, P4 1117, P5 1117 |
| M9 | solution: the last four's rule applied to three | P1 1907, P3 1907, P5 1907 |
| M10 | solution: blocks of three cut while more than two are left | P1 1907, P3 1907, P5 1907 |

## Benchmarks

The bench draws 100000 random numbers of 100 characters, LeetCode's
longest, the first two digits, all of them first, then answers each 40
times by the ★ arm in all five languages; the sink folds each answer's
length and its middle and last bytes. Every implementation prints
`100000 numbers of 100 characters, 40 rounds: 443453600 characters out,
checksum 702642917`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.757 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.163 s |
| Rust (`rustc -O`) | 2.215 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 3.378 s |
| Kāra (`karac build`) | 3.382 s |
| Go | 5.054 s |
| Python | 26 s |

The sequential Kāra build takes 1.53x Rust's time and 1.56x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.757 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (3.493 s and 3.556 s on one
run).

## Verification

All four arms print the same output as `phone.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★, sizes and recursive arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 8 edits:
`struct Solution {}` added, `Vec<char>` written `Vec[char]`,
`String::new` written `String.new`, and the `&` dropped from each
`res.extend(&digits[..])`. That left four calls extending a `String` by
a `Slice[char]`, which is not `IntoIterator` in Kāra; `karac check`
refused each one (E0200, the bound `I: IntoIterator` not satisfied) with
no fix. Since kara `93fd9b2078` (B-2026-11-20-39) the refusal says to read the slice
through `.iter()`, which lends the `char`s a `String`'s `extend` takes,
and `karac fix` wrote `res.extend(digits[i..i + 3].iter())` at each.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
