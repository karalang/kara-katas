# 408. Valid Word Abbreviation

A string can be abbreviated by replacing any number of non-adjacent,
non-empty runs of its letters with their lengths, written without
leading zeros. Given a word and an abbreviation, return whether the
abbreviation is one of the word's.

```
word = "internationalization", abbr = "i12iz4n"  -> true
word = "apple",                abbr = "a2e"      -> false
```

**Constraints:** `1 <= word.length <= 20`, of lowercase letters;
`1 <= abbr.length <= 10`, of lowercase letters and digits; every number
in `abbr` fits in a 32-bit integer.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `valid_word_abbreviation.kara` ★ | two pointers: walk the word and the abbreviation together; a letter must equal the word's next letter, a number skips that many letters, a number that starts with 0 is invalid, and both must end together | O(n + m) | O(1) |
| `valid_word_abbreviation_expand.kara` | expand the abbreviation into a `Vec[Option[u8]]`, a wildcard for each letter a number stands for, then compare it with the word letter by letter | O(n + m) | O(n) |
| `valid_word_abbreviation_recursive.kara` | recursion on what is left of each: both used up, or a matching letter and the rest, or a number and the rest after skipping that many letters | O(n + m) | O(m) stack |
| `valid_word_abbreviation_tokens.kara` | a tokenizer and a parser: read the abbreviation into an `enum Token { Letter(u8), Skip(i64) }`, refusing a leading zero, then walk the tokens over the word | O(n + m) | O(m) |
| `differential.kara` | the four arms on 3,000 random cases whose answers are known by construction, five properties | — | — |

Every arm prints the same 17 lines: the two LeetCode examples, fourteen
edge cases (the whole word as one number, a leading zero, a lone 0, a
number longer than the word, abbreviations that run past the word's end,
a number of two digits, a number of 55 letters), and for 3,000 random
words of 1 to 20 letters from a to c, each abbreviated at random and
three in four then broken by changing, inserting or deleting one
character, how many are valid and a checksum. `valid_word_abbreviation.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 3,000 random
cases makes a word of 1 to 20 letters from a to c and an abbreviation of
it, and derives the others from that abbreviation:

| | property |
|---|---|
| P1 | an abbreviation built by replacing runs of the word with their lengths, never two numbers in a row, is valid |
| P2 | the word itself, and its length written out, are valid |
| P3 | the abbreviation with a 0 written before one number, or a lone 0 added if it has none, is invalid |
| P4 | the abbreviation with one number made 1 larger or 1 smaller (never 0) is invalid; with no number, a 1 is appended |
| P5 | the abbreviation with one of its letters changed to another is invalid |

It prints `3000 cases, 4 arms, 60000 checks, 0 failures` under
`karac run --interp`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac run --interp`
(the tokens arm stops `karac __mir-run`; see below). All eight are
killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | pointers: a number may start with 0 | P3 2841 |
| M2 | pointers: the abbreviation may stop short of the word's end | P4 402 |
| M3 | expand: a number may not reach the end of the word | P1 1485, P2 3000 |
| M4 | expand: a letter is never compared | P5 2722 |
| M5 | recursive: a number skips one letter fewer | P1 2841, P2 3000, P4 724 |
| M6 | recursive: a number's digits are added, not read as a number | P1 575, P2 1626 |
| M7 | tokens: a skip moves one letter fewer | P1 2841, P2 3000, P4 883 |
| M8 | tokens: a number may start with 0 | P3 3000 |

Each property is the only one to see some mutant: P3 alone sees the
leading zeros (M1, M8), P4 alone a stop short of the end (M2), P5 alone
a letter never compared (M4). M1 is seen on fewer cases than M8: where
the abbreviation has no number, P3 appends a lone 0 after its last
letter, which the pointers arm never reads because it stops once the
word is used up, while the tokens arm reads it as a skip of 0. M6 is seen only
where a number has two digits. A first M3, an expansion shorter than the
word accepted, made the expand arm read past the end of its expansion,
and was replaced.

## Verification

All four arms print the same output as `valid_word_abbreviation.py`
under `karac run --interp`, `karac __mir-run` (the v2 MIR interpreter)
and `karac __mir-llvm-run`, and `karac check` passes on every file. The
differential prints `60000 checks, 0 failures` under all three. The four
arms and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

Until kara e44d71929c the tokens arm, and with it the differential,
stopped before running on the MIR backends: its `Token.Skip` variant
was refused as `'Skip' is already defined in this scope`, because the
MIR pipeline put the iterator library's `struct Skip` in the program's
own top-level scope (kara `B-2026-10-12-17`). The arm was written as it
should be and did not change.

`karac __mir-llvm-run` needs compiler commit 62f5f6de04, which added
the `String.as_str` native: every arm takes a `Str` and is passed a
string literal or a `String`. The frozen legacy
codegen has no `bytes()` on a `Str` parameter, which stops LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build` on every arm. That is
not filed.

## Benchmarks

The bench program uses the ★ arm on 20,000 random words of 20 letters
(the problem's limit) from a and b, each abbreviated once as in the
harness. Each of 1,000 rounds checks word `i` against abbreviation
`(i + round) mod 20000`, so every round asks different questions and no
compiler can hoist one out of the loop; round 0 is all valid and the
others about one in seven. It folds the count of valid pairs per round
into a total and a checksum. Every implementation prints `20000 words,
1000 rounds: 2759493 valid, checksum 376654456`, and so does the Kāra
program under `karac __mir-run`. Spot timings on a shared 4-core
container (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.74 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.74 s |
| Rust (`rustc -O`) | 0.75 s |
| Go | 0.77 s |
| Python | 12 s |

The legacy `karac build` refuses `words[i]` as an argument to a bare
parameter, since it predates bare parameters borrowing; not filed. The
Kāra program prints the same line under `karac __mir-llvm-run` in
2.3 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

- **A user type named like an iterator adaptor was refused on the MIR
  pipeline** (kara `B-2026-10-12-17`, filed with this kata, fixed by
  e44d71929c): the tokens arm's `enum Token { Letter(u8), Skip(i64) }`
  passed `karac check` and ran under `karac run --interp`, and
  `karac __mir-run` refused it as `'Skip' is already defined in this
  scope`, pointing into the library's `iter.kara`. The fix renamed the
  library's adaptor structs; `Peekable` keeps its name and still clashes
  (kara `B-2026-10-12-21`).
