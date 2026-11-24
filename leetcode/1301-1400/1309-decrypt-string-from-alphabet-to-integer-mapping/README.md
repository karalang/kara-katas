# 1309. Decrypt String from Alphabet to Integer Mapping

You are given a string `s` formed by digits and `'#'`. We want to map `s`
to English lowercase characters as follows:

- Characters (`'a'` to `'i'`) are represented by (`'1'` to `'9'`)
  respectively.
- Characters (`'j'` to `'z'`) are represented by (`'10#'` to `'26#'`)
  respectively.

Return the string formed after mapping. The test cases are generated so
that a unique mapping will always exist.

```
s = "10#11#12"  ->  "jkab"
s = "1326#"     ->  "acz"
```

**Constraints:** `1 <= s.length <= 1000`, `s` consists of digits and the
`'#'` letter, and `s` will be a valid string such that mapping is always
possible.

The arms are `fn freq_alphabets(s: String) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `freq_alphabets.kara` ★ | the code read from the right, where a `#` says the two digits before it are one letter from j to z and a digit alone is a letter from a to i; the letters, met last first, turned round at the end. O(n) |
| `freq_alphabets_replace.kara` | every `26#` in the code replaced by z, then every `25#` by y, and so on down to `10#`, and only then every digit left by its letter from a to i, with `String.replace`; the two-digit codes must go first, so that their digits are not read alone. O(26 n) |
| `freq_alphabets_split.kara` | the code cut at every `#` with `split`; in each piece before a cut the last two digits are one letter from j to z and the digits before them a letter each from a to i, and the piece after the last cut is all single letters. O(n) |
| `freq_alphabets_solution.kara` | a Rust solution as LeetCode's Rust users write it (the code walked from the left over `s.as_bytes()`, looking two places ahead for a `#`, each letter pushed onto a `String::new()` as `(b'a' + n - 1) as char`), carried to Kāra by `karac fix` |
| `freq_alphabets_rev.kara` | a second Rust solution as LeetCode's Rust users write it (an iterator over `s.bytes().rev()` stepped by `while let Some(c) = it.next()`, a `#` pulling the two digits before it with `it.next().unwrap()`, the bytes collected back to front, reversed and made a `String` with `String::from_utf8`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, every letter
once in order, one letter alone at each end of the alphabet, and a run of
1s ending in `10#` (`jkab acz abcdefghijklmnopqrstuvwxyz a z aaaj`); then
3000 random texts of 1 to 300 letters, from the first 2, 10 or all 26
letters, written in the code and read back (`3000 random texts: 3000 read
back, checksum 608184691`). `freq_alphabets.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★ arm's first draft cast its digits to `i64`, and
`karac check` warned that the casts were unnecessary; that draft was
rewritten for another reason, since it took `b'0'` from a `#` before
testing for one, which underflows a `u8`, and the rewrite checked clean,
as the replacing and splitting arms did as first written. The first Rust
arm takes one round of 5 fixes by `karac fix`'s count, from 4 errors:
`struct Solution;` to `struct Solution {}`, `as_bytes()` to `bytes()`,
`String::new()` to `String.new()`, `&&` to `and`, and `::` to `.`. The
second takes one round of 5 fixes from 4 errors: `struct Solution;`, the
iterator's `s.bytes().rev()` to `s.bytes().iter().rev()`, since Kāra's
`bytes()` gives a `Slice[u8]`, `Vec::new()` to `Vec.new()`,
`String::from_utf8` to `String.from_utf8`, and `::` to `.`. Both outputs
match on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: from each place, every letter whose code starts there tried in
turn, and the first that leaves a rest that can itself be read taken.
2000 codes of texts of 1 to 12 letters in four kinds, 500 each: from a,
b, c, j, k, l and t, whose codes begin alike; from any letter; from a to
i only, so with no `#`; and from j to z only. Every code, and the code
joined to it for P3, is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the answer written in the code again: the code itself |
| P3 | two codes joined: the two answers joined |
| P4 | the answer's length: one letter for each digit, less two for each `#` |
| P5 | as many letters from j to z as there are `#`s |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 codes: checksum 235525445,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Eleven edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. One is left out: the backward Rust
arm reading the tens digit before a `#` as its own letter fails every
property exactly as often as the replacing arm putting the single digits
first (M3) does, on every code with a `#`. The ten kept, two to
each arm, are each killed, fail the same way under both backends and not
by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the two digits before a `#` read the wrong way round | P1 1424, P2 1424, P4 909, P5 866, P6 5696 |
| M2 | ★: the letters never turned round | P1 1810, P2 1810, P3 1999, P6 7240 |
| M3 | replacing: the single digits replaced first | P1 1452, P2 1452, P4 1452, P5 1452, P6 1452 |
| M4 | replacing: `26#` never replaced | P1 276, P2 276, P4 276, P5 276, P6 276 |
| M5 | splitting: the last piece dropped | P1 874, P2 874, P3 658, P4 874, P6 874 |
| M6 | splitting: a piece's letter from j read from its first two digits | P1 735, P2 735, P3 644, P4 381, P6 735 |
| M7 | solution: a `#` in the last place missed | P1 1126, P2 1126, P3 1126, P4 1126, P5 1126, P6 1126 |
| M8 | solution: a `#` stepped onto as a digit | P1 1452, P2 1452, P4 1452, P6 1452 |
| M9 | backwards: a letter from a to i one too far on | P1 1366, P2 1366, P5 334, P6 1366 |
| M10 | backwards: a letter from j one too far on | P1 1452, P2 1452, P6 1452 |

P1, P2 and P6 kill all ten, P4 seven, P5 five and P3 four. The code is
one to one, so an answer that writes back to the code is the right one,
and P2 fails exactly where P1 does. The length (P4) is a byte count, so
it fails the edits that drop or add letters (M3, M4, M5, M6, M7, M8) and
the digits read the wrong way round (M1), whose letters past z are not
one byte; it passes the letters left back to front (M2) and the letters
one too far on (M9, M10). The count of letters from j (P5) fails the
edits that move a letter across from i to j or the other way, or change
how many there are: M1, whose `10#` reads as a, M3 and M4, which spell a
two-digit letter as single ones, M7, and M9, whose i becomes j. Joining
two codes (P3) fails only the edits that depend on where a code ends: the
letters left back to front (M2), the last piece dropped (M5), a piece's
letter read from its first digits (M6), which the join lengthens, and a
`#` in the last place missed (M7).

## Benchmarks

The bench builds the codes of 200 texts of 300 letters, up to 900 digits
and `#`s each, within the constraints' 1000, once from its own
generator; then makes 500 passes, each setting one letter of one text
from the checksum so far and writing that text's code afresh, then
reading every code back with the ★ arm and folding one letter of each
answer, at a place also chosen from the checksum, its length and the pass
into the checksum. Each answer is a fresh string: a `Vec[char]` collected
into a `String` in Kāra and Rust, a byte slice in Go, a list joined in
Python, and a `malloc` in C. Every implementation prints `500 passes
over 200 codes: checksum 906723694`.

BENCHTAB
