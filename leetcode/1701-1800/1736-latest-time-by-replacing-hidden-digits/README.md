# 1736. Latest Time by Replacing Hidden Digits

You are given a string `time` in the form of `hh:mm`, where some of the
digits in the string are hidden (represented by `?`).

The valid times are those inclusively between `00:00` and `23:59`.

Return *the latest valid time you can get from* `time` *by replacing the
hidden digits*.

```
time = "2?:?0"      ->  "23:50"
time = "0?:3?"      ->  "09:39"
time = "1?:22"      ->  "19:22"
```

**Constraints:** `time` is in the format `hh:mm`; it is guaranteed that
you can produce a valid time from the given string.

## Approaches

| file | mechanism |
|---|---|
| `time.kara` ★ | each hidden digit the largest its neighbours allow: the hour's first is 2 unless the second is shown above 3, when it is 1; the hour's second is 3 after a 2 and 9 otherwise; the minute's are 5 and 9. The time's `char`s are collected into a `Vec`, replaced in place and collected back. O(1) |
| `time_search.kara` | the 1440 times from 23:59 down to 00:00 written out as `hh:mm` in turn, the first whose every shown digit agrees with the pattern the answer. O(1440) |
| `time_split.kara` | the hour and the minute do not constrain each other, so the answer is the largest hour from 0 to 23 that fits the first two characters and the largest minute from 0 to 59 that fits the last two, each found by `(0..24).rev().find(..)`. O(84) |
| `time_solution.kara` | a Rust solution as LeetCode's Rust users write it, the time's bytes by `into_bytes()`, each `b'?'` replaced, and `String::from_utf8(t).unwrap()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 10 lines: LeetCode's three examples, every
digit hidden, none, the hour's second digit hidden after a 2, and the
hour's first hidden before a 4; then the latest times summed in minutes
and a checksum for 3000 random valid times with each digit hidden with
a chance of 1 in 2, 3000 with 1 in 4, and 3000 with every digit hidden.
`time.py` mirrors the ★ arm and its output is byte-identical.

```
23:50
09:39
19:22
23:59
13:07
23:59
14:59
3000 times with 1 digit in 2 hidden: latest times sum to 3195019 minutes, checksum 557808087
3000 times with 1 digit in 4 hidden: latest times sum to 2690773 minutes, checksum 922482654
3000 times with 1 digit in 1 hidden: latest times sum to 4317000 minutes, checksum 69827146
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way to put a digit from 0 to 9 in each hidden place,
kept when it is a valid time from 00:00 to 23:59, and the latest of
them. It checks 3000 random valid times with each digit hidden with a
chance of 1 in 2. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is a valid time that keeps every shown digit |
| P3 | one more digit hidden never gives an earlier time |
| P4 | the answer with the same digits hidden gives the answer again |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 378786575, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the latest valid one of every
`itertools.product` of digits for the hidden places, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M6 and M7 leave the split arm with an
hour or a minute that no number fits, and its `find(..).unwrap()` panics
on the first such problem, which ends the run with exit 101 and no
count; the other eight fail checks. M3 and M9 both put a digit above 5
in a hidden tens of minutes and fail the very same checks. M1 fails only
the 83 problems whose hour is `?3`.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a hidden first hour digit 2 only before a shown 0 to 2 | P1 83, P3 5, P5 83 |
| M2 | ★: a hidden second hour digit 4 after a 2 | P1 878, P2 878, P5 878 |
| M3 | ★: a hidden tens of minutes 9 | P1 1538, P2 1538, P5 1538 |
| M4 | search: the times tried earliest first | P1 2814, P3 1190, P5 2814 |
| M5 | search: every time taken to fit, shown digits ignored | P1 3000, P2 3000, P4 3000, P5 3000 |
| M6 | split: only the hours 0 to 19 tried | panics: `unwrap()` on `None` |
| M7 | split: both digits compared with the tens digit | panics: `unwrap()` on `None` |
| M8 | solution: a hidden first hour digit always 2 | P1 376, P3 22, P5 376 |
| M9 | solution: a hidden tens of minutes 6 | P1 1538, P2 1538, P5 1538 |
| M10 | solution: a hidden last digit left hidden when the tens of minutes is 5 | P1 903, P2 903, P5 903 |

## Benchmarks

The bench draws `10^6` random valid times with each digit hidden with a
chance of 1 in 2, all of them first, then answers each 10 times by the
★ arm in all five languages; each answer is a fresh string. Every
implementation prints `1000000 times, 10 rounds: hour digits sum to
47587650, checksum 692968022`. Kāra and Rust collect the time's `char`s
into a vector and back, Go converts to and from a slice of runes, and C
copies the six bytes into a `malloc`'d buffer. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ad6400d909` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.225 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.545 s |
| Kāra (`karac build`) | 0.553 s |
| Rust (`rustc -O`) | 0.775 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.779 s |
| Go | 0.807 s |
| Python | 6.9 s |

The sequential Kāra build is 30% faster than Rust and 30% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md). C is the fastest here at 0.225 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.513 s and 0.542 s on one
run).

## Verification

All four arms print the same output as `time.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `ad6400d909`.

## Writing it

The ★, search and split arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 4 edits:
`struct Solution {}` added, `time.into_bytes()` written
`time.bytes().to_vec()`, `||` written `or`, and `String::from_utf8`
written `String.from_utf8`. The `b'?'` byte literals carried over as
written.

The bench first took the answer's bytes with Rust's `as_bytes()`;
`karac check` named `.bytes()`, and one `karac fix` of 2 edits wrote it
and dropped an `as i64` the byte took by itself.

The differential's literal reading first put each digit in place with
`('0' as i64 + rest % 10) as char`, which `karac check` refuses, as Rust
does, since not every integer is a `char`; it writes
`char.from_digit((rest % 10) as u32, 10).unwrap()`, and the differential
then checked clean. `arm_name` in it indexes a list of string literals
for a `Str`, as #1662's does (B-2026-11-19-131).
