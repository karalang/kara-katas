# 418. Sentence Screen Fitting

Given a screen of `rows x cols` characters and a sentence as a list of
words, return how many times the sentence fits on the screen. The words
go in order, repeating the sentence, and a word may not be split across
two rows. Two neighbouring words on one row are separated by one space.

```
sentence = ["hello","world"], rows = 2, cols = 8          -> 1
sentence = ["a","bcd","e"], rows = 3, cols = 6            -> 2
sentence = ["i","had","apple","pie"], rows = 4, cols = 5  -> 1
```

**Constraints:** `1 <= sentence.length <= 100`;
`1 <= sentence[i].length <= 10`, lowercase letters;
`1 <= rows, cols <= 2 * 10^4`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `sentence_screen.kara` ★ | one pointer into the text: join the words with a space after each, so the screen shows this text repeated. Each row moves the pointer `cols` ahead; on a space it skips the space, otherwise it backs up to the start of the word the row would split. The answer is the whole texts passed | O(rows · longest word) | O(text) |
| `sentence_screen_rows.kara` | the screen typed row by row: place words while the next one fits, counting a sentence at each last word | O(rows · cols) | O(1) |
| `sentence_screen_table.kara` | what a row holds depends only on its first word, so fill one row from each word once, recording the next row's first word and the sentences completed; then each row is a lookup | O(n · cols + rows) | O(n) |
| `sentence_screen_cycle.kara` | the table arm's first words repeat with a period of at most `n`: record where each first word was seen, then add whole periods at once and walk the rows left over | O(n · cols + n) | O(n) |
| `differential.kara` | the four arms on 2,000 random sentences and screens, five properties, one of them a greedy wrap of the sentence's copies written out | — | — |

`n` is the number of words. A word longer than a row can never be
placed, so the answer is then 0: the ★ arm's pointer backs up to the
same place on every row, and the other arms check for it first.

Every arm prints the same 11 lines: the three LeetCode examples, seven
edge cases (one word that fits exactly, one word one letter too long,
a 1 x 1 screen, two one-letter words on rows of 2 and of 3, LeetCode's
`10000 x 9001` screen, three one-letter words on `8 x 7`), and for
1,000 random sentences of 1 to 8 words of 1 to 6 letters on screens of
1 to 40 rows and 1 to 20 columns, so that some words do not fit, the
total of the answers and a checksum. `sentence_screen.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 2,000
random cases makes a sentence of 1 to 6 words of 1 to 5 letters and a
screen of 1 to 30 rows and 1 to 25 columns:

| | property |
|---|---|
| P1 | the answer is the number of words that fit on the first `rows` lines when enough copies of the sentence are written out and wrapped greedily, divided by `n` |
| P2 | one more row, or one more column, never lowers the answer |
| P3 | the sentence written twice gives half the answer, rounded down |
| P4 | `n` words of one length `L` on rows of exactly `m(L + 1) - 1` columns fit `m` words a row, so the answer is `rows · m / n` |
| P5 | a word longer than a row makes the answer 0, and rows exactly one sentence long fit one sentence each |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | pointer: a row ending at a space does not skip it | P1 393, P4 1850, P5 2000 |
| M2 | pointer: backing up stops at the space, not after it | P1 790, P2 200 |
| M3 | rows: a word may run one column past the row | P1 547 |
| M4 | rows: the space after each word takes no column | P1 1283, P4 592, P5 453 |
| M5 | table: each row counts the sentences of the row after it | P1 477, P3 394, P4 596 |
| M6 | table: each row starts one word after the last | P1 498, P3 487, P4 154 |
| M7 | cycle: the rows left after the whole periods are skipped | P1 289, P2 34, P3 268, P4 277 |
| M8 | cycle: a period's gain is taken as one sentence | P1 851, P2 248, P3 837, P4 833 |

M1 fails every P5 case: rows exactly one sentence long always end at
the text's space, which M1 then carries into the next row. M3 is seen
only by P1: P4's and P5's rows are filled exactly, so the extra column
fits no further word there, and an arm that always allows one more
column still never answers less for a taller or wider screen. M2 leaves the pointer on the space before the
split word, which costs a column on the next row. P5 cannot see the
table and cycle mutants, since rows exactly one sentence long make every
row start at the first word whatever the table says.

## Verification

All four arms print the same output as `sentence_screen.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp`, and `karac check` passes on every file. The
differential prints `40000 checks, 0 failures` on every backend:
`karac __mir-run`, `karac __mir-llvm-run`, `karac run --interp`, LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

The arms' harness runs under `karac __mir-llvm-run` since compiler
commit 62f5f6de04 added the `String.as_str` native: `show(text: Str)`
is passed a string literal. It still stops on the other three, as the
frozen legacy codegen has no `split_whitespace()` on that `Str` parameter,
which stops LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build`.
That is not filed. The differential and the bench program pass no
`Str`, and both run on every backend.

## Benchmarks

The bench program calls the ★ arm 10,000 times, each on a sentence of 1
to 100 words (the problem's limit) drawn from a pool of 200 random
words of 1 to 10 letters, on a screen of up to 20,000 rows and 10 to
20,000 columns. Each call joins its own text, as the ★ arm does; the C
mirror copies each word and builds the text in a fresh buffer the same
way, while the Go mirror's sentence shares the pool's strings. It folds
the answers into a total and a checksum. Every implementation prints
`10000 calls: total 6375987449, checksum 31545929`; a 20-call cut of
the Kāra program under `karac __mir-run` prints the same as the C
program cut the same way. Spot timings on a shared 4-core container,
three runs each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.84 to 0.89 s |
| Rust (`rustc -O`) | 0.86 to 0.88 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.87 to 0.91 s |
| Kāra (legacy `karac build`) | 0.87 to 0.90 s |
| Go | 1.39 to 1.41 s |
| Python | 22 s |

The Kāra program also prints the same line under
`karac __mir-llvm-run` in 2.3 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark. The
`karac build` time is the frozen legacy backend.

## Compiler findings

No new findings. The harness writes each sentence as one string and
splits it with `split_whitespace()`: a `vec!` of string literals passed
as `Vec[Str]` is refused, which is kara `B-2026-10-12-13`.
