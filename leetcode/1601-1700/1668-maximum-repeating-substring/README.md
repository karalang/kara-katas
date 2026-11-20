# 1668. Maximum Repeating Substring

For a string `sequence`, a string `word` is **`k`-repeating** if `word`
concatenated `k` times is a substring of `sequence`. The `word`'s
**maximum `k`-repeating value** is the highest value `k` where `word` is
`k`-repeating in `sequence`. If `word` is not a substring of `sequence`,
`word`'s maximum `k`-repeating value is `0`.

Given strings `sequence` and `word`, return *the **maximum `k`-repeating
value** of `word` in `sequence`*.

```
sequence = "ababc", word = "ab"  ->  2
sequence = "ababc", word = "ba"  ->  1
sequence = "ababc", word = "ac"  ->  0
```

**Constraints:** `1 <= sequence.length <= 100`;
`1 <= word.length <= 100`; `sequence` and `word` contain only lowercase
English letters.

## Approaches

| file | mechanism |
|---|---|
| `maximum.kara` ★ | the word k + 1 times over is in the sequence only if it is k times over, so the copies are added one at a time while `contains` still finds them. At most n / m + 1 searches |
| `maximum_runs.kara` | `runs[end]`, the copies ending at `end` back to back: one more than at `end - m` when the m letters before `end` are the word. O(n * m) time, O(n) space |
| `maximum_scan.kara` | from every start, step over copies for as long as the rest `starts_with` the word. O(n * n) |
| `maximum_solution.kara` | LeetCode's Rust template, `word.repeat(k + 1)` searched for until it is missing, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

The arms take the two strings as `Str` views; the solution arm keeps
LeetCode's `String` parameters behind a `Str` wrapper.

Every arm prints the same 9 lines: LeetCode's three examples, a sequence
whose longest run does not start at the first copy (`"aaaba"` in
`"aaabaaaabaaabaaaabaaaabaaaabaaaaba"`, 5, where a search that restarts
after the first copy found misses it), a word longer than the sequence,
and a sequence that is the word; then the answers summed and a checksum
for 3000 random problems of up to 12 letters, 3000 of up to 100 and 300
of up to 100 with words of up to 100. A random sequence is built of
whole copies of the word and single letters, half and half, from an
alphabet of 1 to 3 letters. `maximum.py` mirrors the ★ arm and its
output is byte-identical.

```
2
1
0
5
0
1
3000 problems of up to 12 letters: answers sum to 8300, checksum 580698953
3000 problems of up to 100 letters: answers sum to 28116, checksum 177384665
300 problems of up to 100 letters: answers sum to 589, checksum 615571521
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every piece of the sequence whose length is a multiple of the
word's is cut into word-long parts, and a piece whose parts all equal the
word is the word k times over; the answer is the largest k, or 0. It
checks 3000 random problems, words of 1 to 3 letters and sequences of up
to 16. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the word repeated answer times is in the sequence |
| P3 | the word repeated answer + 1 times is not |
| P4 | the word added to the end of the sequence answers the same or one more |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 481450788, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the count starts at 1 | P1 3000, P2 3000, P5 3000 |
| M2 | ★: `if` for `while`, one copy at most | P1 2173, P3 2173, P5 2173 |
| M3 | ★: the search starts from two copies | P1 2864, P3 2864, P5 2864 |
| M4 | runs: every copy a run of one | P1 2173, P3 2173, P5 2173 |
| M5 | runs: a copy ending at the last letter missed | P1 1381, P3 1381, P5 1381 |
| M6 | runs: the last run kept, not the longest | P1 471, P3 471, P4 234, P5 471 |
| M7 | scan: one letter stepped, not one copy | P1 1420, P2 891, P3 529, P4 946, P5 1420 |
| M8 | scan: only the first start tried | P1 1031, P3 1031, P5 1031 |
| M9 | scan: the last start's count kept | P1 2773, P3 2773, P5 2773 |
| M10 | solution: the count stepped by 2 | P1 1571, P2 1571, P4 1010, P5 1571 |

## Benchmarks

The bench draws 400000 problems, words of 1 to 6 letters and sequences
of about 100 (LeetCode's longest) built the same way, all of them first,
then answers each by the ★ arm in all five languages, each with its own
library's substring search: Kāra's `Str.contains`, Rust's
`str::contains`, Go's `strings.Contains`, Python's `in` and C's `strstr`.
Every implementation prints `400000 problems of about 100 letters:
answers sum to 7102853, checksum 94524761`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.513 s |
| Kāra (`karac build`) | 0.761 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.779 s |
| Go | 0.852 s |
| Rust (`rustc -O`) | 1.387 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.422 s |
| Python | 12 s |

The sequential Kāra build is 44% faster than Rust and 45% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md). C is the fastest here at 0.513 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.779 s and 0.809 s on one
run).

## Verification

All four arms print the same output as `maximum.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm checked clean as first written: its count is returned as the
`i32` the signature names, and that use fixes the literal's type. The
runs and scan arms kept their best count with `max(best, ..)` and
`best.max(k)`, and a call or a method does not fix a literal's type
(design.md § Literals), so `best` stayed an `i64` and returning it as
`i32` was refused (E0200). `karac fix` declared `best: i32`, and in the
scan arm `k: i32` as well.

LeetCode's Rust template took one `karac fix`: `struct Solution {}`
added, the `&` on `contains(&word.repeat(..))` dropped, `k` declared
`i32`, and `k as usize + 1` written `k + 1`.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
