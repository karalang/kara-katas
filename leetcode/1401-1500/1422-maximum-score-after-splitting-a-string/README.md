# 1422. Maximum Score After Splitting a String

Given a string `s` of zeros and ones, return the maximum score after
splitting the string into two non-empty substrings (i.e. left substring
and right substring). The score after splitting a string is the number
of zeros in the left substring plus the number of ones in the right
substring.

```
s = "011101"    ->  5    "0" and "11101" score 1 + 4
s = "00111"     ->  5    "00" and "111" score 2 + 3
s = "1111"      ->  3    "1" and "111" score 0 + 3
```

**Constraints:** `2 <= s.length <= 500`, the string `s` consists of
characters `'0'` and `'1'` only.

Each arm is `fn max_score(s: String) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_score.kara` ★ | a split scores the ones in all of `s`, plus the zeros less the ones to its left: the ones counted once, and the most that difference reaches over the splits, in one pass over the bytes. O(n) |
| `max_score_splits.kara` | every split in turn, its zeros on the left and its ones on the right counted afresh over the two slices. O(n²) |
| `max_score_prefix.kara` | the zeros in every prefix and the ones in every suffix, each counted once into a table, and the best split read off the two by `map` and `max`. O(n) time and space |
| `max_score_fold.kara` | the split moved right one digit at a time in a `fold` over `chars().skip(1).take(..)`, carrying the score so far and the best as a tuple: a 0 crossing to the left scores one more, a 1 one less. O(n) |
| `max_score_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s.as_bytes()`, the ones by `filter(\|&&b\| b == b'1').count() as i32`, the zeros counted up and the ones down as the split moves), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and five
more (`5 5 3 1 2 0 1 3`); the constraints' most, 500 zeros, 500 ones and
500 drawn digits (`500 digits: 499 499 262`); and 2000 random strings of
2 to 60 digits, a 1 from 0 to 10 times in 10 (`2000 random strings:
48914 in all, checksum 218054053`). `max_score.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, splits, prefix and fold arms check clean as first
written. The Rust solution takes one round of 10 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `s.as_bytes()` to
`s.bytes()`, the closure's `|&&b|` to `|b|`, `zeros` and `best` declared
`: i32`, and `Solution::` to `Solution.`; its `count() as i32` is taken
as written. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: `s` cut after each digit but the last into a left and a right
string, each built up a character at a time, and the zeros of the one
and the ones of the other counted, the most kept. LeetCode's examples,
nine edge cases (every string of two digits, one kind only, the best
split first or last), the constraints' most four ways (500 zeros, 500
ones, 250 ones then 250 zeros, and drawn), and 1987 random strings, 2 to
60 digits two times in three and up to 500 otherwise, a 1 from 0 to 10
times in 10. Each case also draws a digit to flip for P5.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a score from 0 to the length |
| P3 | turned round with every digit flipped, the zeros on the left become the ones on the right, and the score stays |
| P4 | at least what the first split and the last score |
| P5 | one digit flipped moves every split's score by one, so the best by at most one |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 cases: checksum 272391231,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. The differential checks
clean as first written. Python, by slicing and `str.count` at every
split, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a one not counted against the lead | P1 1765, P3 1387, P6 7060 |
| M2 | ★: the split after the last digit allowed | P1 579, P3 1164, P6 2316 |
| M3 | splits: the split before the first digit allowed | P1 595, P3 1164, P6 595 |
| M4 | splits: the right part missing its first digit | P1 1424, P3 1164, P4 807, P6 1424 |
| M5 | prefix: the zeros counted as the right part's ones | P1 1885, P3 1970, P4 1200, P6 1885 |
| M6 | prefix: the ones counted from one place too early | P1 595, P3 1164, P6 595 |
| M7 | fold: a leading zero not counted | P1 964, P3 1387, P4 664, P6 964 |
| M8 | fold: the split after the last digit allowed | P1 579, P3 1164, P6 579 |
| M9 | solution: the first digit never counted | P1 1509, P3 1611, P4 676, P6 1509 |
| M10 | solution: every score one too low | P1 2000, P4 1383, P6 2000 |

## Benchmarks

The bench draws a pool of 10^6 digits, a 1 one time in 2, and runs the ★
arm, taking its window as a `Str`, on 10^6 windows of 500 of them, each
window's start drawn. Each implementation copies the window's bytes out
as the ★ arm collects them. Every implementation prints `10^6 windows of
500 digits: checksum 158102440`.

BENCHTAB

Measured by hand, Kāra takes 0.46 to 0.49 s against Rust's 0.90 to 0.96
s (0.63 to 0.74 s with overflow checks on), C's 0.74 s and Go's 0.89 to
0.91 s; Python takes 31 s.
