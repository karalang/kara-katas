# 1271. Hexspeak

A decimal number can be converted to its Hexspeak representation by
first converting it to an uppercase hexadecimal string, then replacing all
occurrences of the digit `'0'` with the letter `'O'`, and the digit `'1'`
with the letter `'I'`. Such a representation is valid if and only if it
consists only of the letters in the set `{'A', 'B', 'C', 'D', 'E', 'F',
'I', 'O'}`.

Given a string `num` representing a decimal integer `n`, return the
Hexspeak representation of `n` if it is valid, otherwise return
`"ERROR"`.

```
num = "257"  ->  "IOI"
num = "3"    ->  "ERROR"
```

**Constraints:** `1 <= num.length <= 12`; `num` does not contain leading
zeros; `num` represents an integer in the range `[1, 10^12]`.

The arms are `fn to_hexspeak(num: Str) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `hexspeak.kara` ★ | by digits: the number parsed by `i64.parse`, its hexadecimal digits taken from the lowest by `% 16`, 0 spelled `O`, 1 `I` and 10 to 15 `A` to `F`, any of 2 to 9 an error, and the letters reversed. O(log n) |
| `hexspeak_format.kara` | by formatting: the number printed by `{n:X}`, its `0` and `1` replaced by `O` and `I`, and the result checked to hold nothing but the eight letters |
| `hexspeak_table.kara` | by a table: the sixteen spellings in an `Array[Option[char], 16]`, the digits taken from the highest by shifting, and the first `None` an error by `?` in a helper returning an `Option` |
| `hexspeak_recursive.kara` | by recursion: a number's spelling is its sixteenths' spelling and its last digit's letter, named by a `match`, with an error carried up by `?` on a `Result` |
| `hexspeak_collect.kara` | by collecting options: the number printed by `{n:x}`, each character mapped to its letter or `None`, and the `Option`s collected into an `Option[String]`, which is `None` as soon as one is |
| `hexspeak_solution.kara` | a Rust solution as LeetCode's Rust users write it (`num.parse::<u64>()`, `format!("{:X}", n)`, a `match` with `'A'..='F'`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, then 1, 10^12
and 747,823,223,228 (`IOI ERROR I ERROR AEIDBCDIBC`); and 3000 random
numbers, a third anything up to 10^12, a third spelled in the eight
letters' digits and a third in them and one other (`3000 random numbers:
1535 valid, checksum 81273315`). `hexspeak.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, table, recursive and collect arms checked clean as
first written, and `karac fix`'s style pass removed the `.to_string()` on
each arm's `"ERROR"`, which a `String` result takes as it is. The format
arm's `"ABCDEFIO".contains(c)` with a `char` got E0200, "'contains' takes
a `Str` pattern, found 'char': write it as `c.to_string()`", and `karac
fix` made that edit. The solution arm takes one round of 8 fixes:
`num.parse::<u64>()` to `u64.parse(num)`, `format!("{:X}", n)` to
`f"{n:X}"`, `String::new` to `String.new`, `&str` to `Str`, `struct
Solution;` to `struct Solution {}`, `::` to `.`, and `"ERROR".to_string()`
to `"ERROR"`. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the number written in upper case hexadecimal digit by digit
from a table of the sixteen, every `0` then replaced by `O` and every `1`
by `I`, and the result valid only if each character is one of the eight.
2000 random numbers drawn as the harness draws them.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | an answer is `ERROR` or holds nothing but the eight letters |
| P3 | a spelling read back as hexadecimal is the number |
| P4 | the number times 16 is the same spelling and an `O`, or both are errors |
| P5 | the number times 16 plus a digit from 2 to 9 is an error |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 numbers: checksum 52904991,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a digit 10 an error | P1 467, P6 2335 |
| S2 | ★: the letters not reversed | P1 866, P3 866, P4 1041, P6 4330 |
| F1 | format: `1` not replaced by `I` | P1 495, P6 495 |
| F2 | format: a `2` let through | P1 42, P2 42, P3 42, P5 148, P6 42 |
| T1 | table: a zero inside the number skipped | P1 360, P3 360, P4 1041, P6 360 |
| T2 | table: 9 spelled `I` | P1 42, P3 42, P5 122, P6 42 |
| R1 | recursive: a 1 an error | P1 495, P6 495 |
| R2 | recursive: the last letter put first | P1 866, P3 866, P4 1041, P6 866 |
| C1 | collect: `a` to `f` left in lower case | P1 1011, P2 1011, P3 1011, P6 1011 |
| C2 | collect: 0 spelled `I` | P1 360, P3 360, P4 1041, P6 360 |
| O1 | solution: an `F` an error | P1 479, P6 479 |
| O2 | solution: a `1` dropped | P1 495, P2 27, P3 495, P6 495 |

All twelve are caught, every one by P1, the statement read literally. The
four that turn a valid spelling into an error (S1, F1, R1, O1) are seen by
P1 alone: an `ERROR` passes every property that checks a spelling's form,
and the times-16 property errs on both sides alike. P4, times 16, catches
the edits that put the letters in the wrong order or misplace a zero, and
P5, a bad last digit, the two that let a 2 or a 9 through. O2 fails P2 on
the 27 numbers made only of 1s, whose answer it leaves empty.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the decimal text parsed, its hexadecimal digits spelled from the
lowest, 0 as O, 1 as I, 10 to 15 as A to F, any other an error) on
100,000 numbers up to 10^12 drawn once, half spelled in the eight
letters, 150 rounds; every answer folded into a checksum. Every program
prints `150 rounds of 100000 numbers: checksum 107703778`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.077 to 1.190 s | 1.103 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.082 to 1.220 s | 1.137 s |
| Rust (`rustc -O`) | 1.271 to 1.383 s | 1.317 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.294 to 1.480 s | 1.368 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.293 to 1.498 s | 1.343 s |
| C (`clang -O3`) | 0.881 to 1.004 s | 0.928 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.881 to 1.077 s | 0.917 s |
| Go | 1.407 to 1.669 s | 1.446 s |
| Python | 25.12 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 17% ahead of Rust with overflow checks on (1.137 s
against 1.368 s). C is about 18% ahead of Kāra (0.928 s against 1.137
s); Kāra is about 21% ahead of Go (1.137 s against 1.446 s). Python
takes about 22x Kāra's time. No profile was taken.
