# 1844. Replace All Digits with Characters

You are given a 0-indexed string `s` that has lowercase English letters
in its even indices and digits in its odd indices. You must perform an
operation `shift(c, x)`, where `c` is a character and `x` is a digit,
that returns the `x`th character after `c`. For example, `shift('a', 5)
= 'f'` and `shift('x', 0) = 'x'`. For every odd index `i`, you want to
replace the digit `s[i]` with the result of the `shift(s[i-1], s[i])`
operation. Return `s` after replacing all digits. It is guaranteed that
`shift(s[i-1], s[i])` will never exceed `'z'`.

```
s = "a1c1e1"     ->  "abcdef"
s = "a1b2c3d4e"  ->  "abbdcfdhe"
```

**Constraints:** `1 <= s.length <= 100`, `s` consists only of lowercase
English letters and digits, `shift(s[i-1], s[i]) <= 'z'` for all odd
indices `i`.

The arms are `fn replace_digits(s: String) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `replace_digits.kara` ★ | the string's bytes walked, each letter written as it is and each digit as the letter before it shifted on by the digit. O(n) |
| `replace_digits_chars.kara` | the string's chars in a `Vec`, each digit replaced in place by the letter before it moved on by its value, `to_digit`, through `char.try_from` of the code point, and the chars collected back into a string. O(n) |
| `replace_digits_map.kara` | the string's bytes mapped by place: an even place keeps its letter, an odd one reads the letter before it and adds its digit, and the bytes made a string again by `String.from_utf8`. O(n) |
| `replace_digits_pairs.kara` | the bytes cut into pairs of a letter and a digit by `chunks(2)`, each pair written as its letter and the letter shifted, and a last letter with no digit written alone. O(n) |
| `replace_digits_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s.into_bytes()`, each odd place set in place over a `step_by(2)`, and `String::from_utf8`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; five edges,
one letter, a shift of 0, a shift to `z`, the largest shift, and a last
letter with no digit (`q mm qz aj zzyzxzw`); the constraints' most, 100
places drawn at random and 100 places of `a9`; and 3000 random cases of
1 to 20 places, each output folded to one number (`3000 random cases:
checksum 995961287`). Each case puts a letter at every even place and at
every odd place a digit that keeps the shift at or before `z`.
`replace_digits.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, map and pairs arms and the harness check clean as
first written. The chars arm was first written with Rust's
`char.from_u32(..).unwrap()`; check refused it with E0236, naming
`char.try_from(n)`, which takes a `u32` code point and returns a
`Result`, and `.ok()` for the `Option` Rust's `from_u32` returns. `karac
fix` wrote `char.try_from(..).ok().unwrap()`, 1 fix, and the arm unwraps
the `Result` itself, `char.try_from(..).unwrap()`. The Rust solution
takes 13 fixes by `karac fix`'s count, and its diff is: `struct Solution
{}` added above the `impl`; `s.into_bytes()` to `s.bytes().to_vec()`, as
`s` is borrowed; `String::from_utf8` to `String.from_utf8`; and
`Solution::` to `Solution.` at the harness's 10 calls.
`(1..b.len()).step_by(2)` and `b[i] = b[i - 1] + (b[i] - b'0')` are Kāra
as they stand. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: `shift(c, x)`, the `x`th character after `c`, found by
counting `x` places on from `c` in the alphabet, and each digit at an
odd place replaced by `shift` of the letter before it. It runs 2000
random cases of 1 to 20 places, drawn as the harness draws them. Each
arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | as long as `s`, its letters where they were, and every place a lowercase letter |
| P3 | `s` cut between two pairs gives the two outputs joined |
| P4 | every digit a 0 writes each letter twice, a last one with no digit once |
| P5 | a string of whole pairs, its pairs reversed, gives its output's pairs reversed |
| P6 | the ★ arm's answer |

The differential was first written with `.collect()` of the doubled
letters, each a `String`, into a `String`; check refused it, as `String`
implements `FromIterator[char]` and not `FromIterator[String]`, and
named collecting the pieces into a `Vec[String]` and joining them, which
the differential does. All 60,000 checks pass on every arm: `2000 cases:
checksum 534759878, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.
Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. The chars
arm's first edit was first to step three places on; it read a letter as
a digit and stopped on `unwrap()` of `None`, a crash, and it now shifts
each letter one place too far. The map arm's second edit was first to
swap the places that keep their letter and those that shift; it read
before the first byte, an index out of bounds, and it now drops a last
letter with no digit.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each shift one short | P1 1899, P2 29, P4 1899, P6 7596 |
| M2 | ★: a letter kept at every third place, a shift at the rest | P1 1781, P2 1781, P3 1285, P4 1705, P5 932, P6 7124 |
| M3 | chars: each shift one too far | P1 1899, P2 847, P4 1899, P6 1899 |
| M4 | chars: the digit's own code point shifted, not the letter's | P1 1899, P2 1899, P4 1899, P6 1899 |
| M5 | map: each digit replaced by the letter before it, unshifted | P1 1859, P6 1859 |
| M6 | map: a last letter with no digit dropped | P1 964, P2 964, P4 964, P6 964 |
| M7 | pairs: the string cut into threes | P1 1797, P2 1797, P3 1285, P4 1797, P5 928, P6 1797 |
| M8 | pairs: no pair's digit written | P1 1899, P2 1899, P4 1899, P5 1029, P6 1899 |
| M9 | solution: every other digit left as it is | P1 1705, P2 1705, P3 910, P4 1705, P5 521, P6 1705 |
| M10 | solution: each shift halved | P1 1859, P6 1859 |

## Benchmarks

The bench builds 40 strings of 100 places once and makes 500000 calls of
the ★ arm, each call's string drawn from the checksum so far, and folds
in one byte of each output, at a place drawn the same way. Each call
builds its own output string. It checks clean as first written. Every
implementation prints `500000 calls: checksum 666402138`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.08 s against Rust's 0.12 s (0.11 s with
overflow checks on), C's 0.03 s and Go's 0.25 s; Python takes 3.8 s.
