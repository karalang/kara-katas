# 1704. Determine if String Halves Are Alike

You are given a string `s` of even length. Split this string into two
halves of equal lengths, and let `a` be the first half and `b` be the
second half.

Two strings are **alike** if they have the same number of vowels (`'a'`,
`'e'`, `'i'`, `'o'`, `'u'`, `'A'`, `'E'`, `'I'`, `'O'`, `'U'`). Notice
that `s` contains uppercase and lowercase letters.

Return `true` *if* `a` *and* `b` *are **alike***. Otherwise, return
`false`.

```
s = "book"      ->  true
s = "textbook"  ->  false
```

**Constraints:** `2 <= s.length <= 1000`; `s.length` is even; `s`
consists of **uppercase and lowercase** letters.

## Approaches

| file | mechanism |
|---|---|
| `halves.kara` ★ | one pass over the bytes, a `match` naming the ten vowels: one in the first half counts up and one in the second down, and the halves are alike when the count comes back to 0. O(n) |
| `halves_count.kara` | `split_at` cuts the string in two, and each half's vowels are counted by `chars().filter(..).count()`, a vowel being a char that `"aeiouAEIOU"` contains. O(n) |
| `halves_table.kara` | an `Array[bool, 128]` marks the vowels' bytes; one index walks the first half and the same index plus the half the second, the difference kept. O(n) |
| `halves_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `count` closure over a `&str`, `&s[..n / 2]` and `&s[n / 2..]`, and `"aeiouAEIOU".contains(c)`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, capitals
(true), no vowel at all (true) and two vowels (true); then the strings
alike and a checksum for 3000 random strings of an even 2 to 12 letters,
300 of up to 100 and 3000 of up to 1000, LeetCode's longest, each letter
a vowel with a chance of its string's own and otherwise a consonant,
either case. `halves.py` mirrors the ★ arm and its output is
byte-identical.

```
true
false
true
true
true
3000 strings of up to 12 letters: 1567 alike, checksum 152609975
300 strings of up to 100 letters: 105 alike, checksum 438924033
3000 strings of up to 1000 letters: 695 alike, checksum 478330873
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the string's letters split at the half, every letter compared
with each of the ten vowels the statement lists and a match counted to
its half; alike when the two counts are equal. It checks 3000 random
strings of an even 2 to 12 letters, drawn from the same seed as the
arms' first batch and so the very same strings: its checksum is that
batch's. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the two halves swapped give the same answer |
| P3 | the string reversed gives the same answer |
| P4 | the string in capitals gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 152609975, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M2 and M4 both move the middle letter
into the first half and fail the same checks. A vowel left out (M1, M5)
or a letter added (M10) is seen by P4 too, since the capitals change
which of the letters counts.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `U` left out of the vowels | P1 476, P4 453, P5 476 |
| M2 | ★: the middle letter counted in the first half | P1 894, P2 398, P3 380, P5 894 |
| M3 | ★: alike when the first half has at least as many | P1 735, P2 1433, P3 1433, P5 735 |
| M4 | count: the cut one letter late | P1 894, P2 398, P3 380, P5 894 |
| M5 | count: the capital vowels left out | P1 1095, P4 1528, P5 1095 |
| M6 | table: the second half read one letter early | P1 634, P3 690, P5 634 |
| M7 | table: the first pair of letters skipped | P1 584, P3 690, P5 584 |
| M8 | table: the second half counted up too | P1 957, P5 957 |
| M9 | solution: the second half starting one letter late | P1 1109, P2 847, P3 856, P5 1109 |
| M10 | solution: a lower-case `y` counted as a vowel | P1 130, P4 130, P5 130 |

## Benchmarks

The bench draws 1000 random strings of 1000 letters, LeetCode's longest,
all of them first, then answers each 400 times by the ★ arm in all five
languages. Every implementation prints `1000 strings of 1000 letters,
400 rounds: 84000 alike, checksum 288061636`. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 1.067 s |
| Rust (`rustc -O`) | 1.094 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.139 s |
| Kāra (`karac build`) | 1.180 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.212 s |
| Go | 3.691 s |
| Python | 16 s |

The sequential Kāra build is level with Rust and 6% faster than Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 1.067 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.183 s and 1.186 s on one
run).

## Verification

All four arms print the same output as `halves.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and table arms checked clean as first written.

The count arm's first draft asked `"aeiouAEIOU".contains(c)` of a
`char`, as Rust allows. Kāra's `contains` takes a `Str` pattern only
(docs/library/strings.md); `karac check` said so and named
`c.to_string()`, and `karac fix` wrote it.

LeetCode's Rust template took one `karac fix` of 6 edits:
`struct Solution {}` added, the closure's `&str` parameter written
`Str`, `|&c|` written `|c|`, `contains(c)` written
`contains(c.to_string())` as in the count arm, and the two `&` before
`s[..n / 2]` and `s[n / 2..]` dropped.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
