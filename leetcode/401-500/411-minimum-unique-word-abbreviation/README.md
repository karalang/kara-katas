# 411. Minimum Unique Word Abbreviation

A word is abbreviated by replacing any number of non-adjacent runs of
its letters with their lengths (kata 408). The length of an
abbreviation is its letters plus its numbers: `"a32bc"` has length 4.
Given a target and a dictionary, return an abbreviation of the target
of the least length that abbreviates no word of the dictionary. Any one
of the shortest is accepted.

```
target = "apple", dictionary = ["blade"]                  -> "a4"   (length 2)
target = "apple", dictionary = ["plain","amber","blade"]  -> "1p3"  (length 3)
```

**Constraints:** `m == target.length`, `n == dictionary.length`;
`1 <= m <= 21`; `0 <= n <= 1000`; `1 <= dictionary[i].length <= 100`;
`log2(n) + m <= 21` if `n > 0`; all strings are lowercase letters, and
the target is not in the dictionary.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `min_abbreviation.kara` ★ | masks over the letters: an abbreviation is a mask of kept letters; only dictionary words of the target's length matter, and one shares the abbreviation exactly when it agrees at every kept letter, so take each word's mask of differing letters; a mask is unique when it meets every one. Try every mask and keep the shortest | O(2^m (m + n)) | O(n) |
| `min_abbreviation_search.kara` | depth-first search building the abbreviation left to right, keeping a letter or writing a number for a run, with every branch cut once its length reaches the best found; the masks of differences decide uniqueness at the end | O(2^m n) at worst | O(m) stack |
| `min_abbreviation_levels.kara` | shortest length first: for length 1, 2, ..., list the masks of exactly that length and compare each dictionary word with the target at the kept positions; the first length with a unique mask wins | O(m 2^m n) | O(2^m) |
| `min_abbreviation_strings.kara` | every abbreviation written out as text, as in LeetCode #320 (Generalized Abbreviation), and each checked against every dictionary word with two pointers, as kata 408 does; the shortest unique one wins | O(2^m m n) | O(2^m m) |
| `differential.kara` | the four arms on 1,500 random cases, five properties, one of them a brute force over every abbreviation written out | — | — |

The arms may return different abbreviations of the same least length,
so the harness does not print the answer. For each case it prints the
answer's length and whether it abbreviates the target and no dictionary
word, checked by its own copy of kata 408's two pointers. Every arm
prints the same 10 lines: the two LeetCode examples, seven edge cases
(no dictionary, only words of other lengths, one letter, two words that
force both letters, four words each one letter off, a 20-letter target
with a word that differs only in its last letter, three words that
differ from a run of eight a's in one place each), and for 1,000 random
targets of 1 to 8 letters from a and b, each with up to 10 dictionary
words, how many answers are unique, their total length and a checksum.
`min_abbreviation.py` mirrors the ★ arm and its output is
byte-identical.

The strings arm reads `best_length = target.len()` before
`best = String.from(target)`. In the other order `karac check` refuses
the second use of `target` as a use after a move, though `Str` is
`Copy` (kara `B-2026-10-12-14`); both orders are natural, so the arm
keeps this one.

## Differential

`differential.kara` holds copies of the four arms. Each of 1,500 random
cases makes a target of 1 to 8 letters from a and b or from a to c, and
up to 8 dictionary words of its length. The properties are about an
answer's length and uniqueness, since shortest answers can differ:

| | property |
|---|---|
| P1 | the answer abbreviates the target and no dictionary word |
| P2 | with only words of other lengths, the answer has length 1; and it is never longer than the target |
| P3 | for up to 6 letters, its length is the least over every abbreviation of the target, written out from a mask and checked as text |
| P4 | adding a word one letter longer than the target changes nothing |
| P5 | adding a word of the target's length never shortens the answer |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | masks: every dropped letter counts 1 to the length | P2 1327, P3 650 |
| M2 | masks: longer dictionary words are compared too | P2 895, P4 321 |
| M3 | search: a number stands for one letter only | P2 1327, P3 650 |
| M4 | search: only the first same-length word is checked | P1 637, P3 372 |
| M5 | levels: a leading run costs nothing | P2 1327, P3 113, P5 3 |
| M6 | levels: no abbreviation of length 1 is tried | P2 1327, P3 106 |
| M7 | strings: no number runs to the end of the word | P2 1327, P3 280 |
| M8 | strings: an abbreviation of a prefix of a word matches it | P2 1158, P4 321 |

M1 and M3 differ in mechanism and fail the same checks: either way no
abbreviation is shorter than the target itself, so every answer has the
target's length. M4 is the only mutant P1 sees,
since it alone returns answers that clash with the dictionary; the
others return unique answers that are too long. M2 and M8 both let a longer word clash
with an abbreviation of its first `m` letters, and P4's added word does
so in the same 321 cases. P5 sees only M5, and rarely.

## Verification

All four arms print the same output as `min_abbreviation.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints `30000
checks, 0 failures` under both.

Every arm and the differential run under `karac __mir-llvm-run` since
compiler commit 62f5f6de04 added the `String.as_str` native: every arm
takes a `Str` and the harness passes it string literals and `String`s.
The frozen legacy typechecker refuses every file, which stops
`karac run --interp`, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac
build`: it refuses `dictionary[d]` as an argument to a bare `Str`
parameter as a move out of an index expression, since it predates bare
parameters borrowing. That is not filed.

## Benchmarks

The bench program uses the ★ arm on 30 random targets of 20 letters
from a and b, each with 2 dictionary words of its length, so that
`log2(2) + 20 = 21`, the problem's limit; the work is the 2^20 masks of
each target. It folds the answers' lengths and bytes into a total and a
checksum. Every implementation prints `30 targets of 20 letters, 2
words each: total 106, checksum 809333835`; a 2-target cut of the Kāra
program under `karac __mir-run` prints the same as the C program cut
the same way. Spot timings on a shared 4-core container (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.21 s |
| Rust (`rustc -O`) | 0.50 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.7 s |
| Go | 3.3 s |
| Python | 42 s |

The hot loop is the length of each mask, a shift by a variable amount
per letter. Checked Rust tests each shift for overflow, and Go checks a
shift by a variable for its range, which is likely where their extra
time goes; that is inferred, not profiled. The legacy `karac build`
refuses the Kāra program, as above. The Kāra program prints the same
line under `karac __mir-llvm-run` in 5.1 s, compile included; that JITs
the MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings. The strings arm's order of two lines is chosen around
`B-2026-10-12-14`, as above.
