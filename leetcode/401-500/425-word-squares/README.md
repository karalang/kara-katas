# 425. Word Squares

Given an array of unique strings `words`, return all the word squares
you can build from `words`. The same word from `words` can be used
multiple times. You can return the answer in any order.

A sequence of strings forms a valid word square if the k-th row and
the k-th column read the same string, for `0 <= k < max(numRows,
numColumns)`.

```
words = ["area","lead","wall","lady","ball"]
  -> [["ball","area","lead","lady"], ["wall","area","lead","lady"]]
words = ["abat","baba","atan","atal"]
  -> [["baba","abat","baba","atal"], ["baba","abat","baba","atan"]]
```

**Constraints:** `1 <= words.length <= 1000`;
`1 <= words[i].length <= 4`; every `words[i]` has the same length and
holds lowercase English letters; all `words[i]` are unique.

## Approaches

| file | mechanism |
|---|---|
| `word_squares.kara` ★ | a map of prefixes: build each square a row at a time. Row `r` must start with the letters already in column `r`, which the rows above fix. Every word is indexed under each of its prefixes, so a row's candidates are one lookup away |
| `word_squares_trie.kara` | a trie whose every node lists the words below it; walk it along column `r`'s letters to the node holding the candidates |
| `word_squares_scan.kara` | the same search with no index: try every word for every row and keep it when its first `r` letters match column `r` |
| `word_squares_sorted.kara` | the words sorted: the words with a prefix are one run, found by binary search for its first word and walked while the prefix holds |
| `differential.kara` | the four arms on 1,500 random word lists, five properties, one of them every sequence of words tried |

All four do the same backtracking search, so their running time is the
number of partial squares the search visits, which no formula bounds
usefully; the arms differ in how a row's candidates are found.

Every arm prints the same 11 lines: the two LeetCode examples, eight
edge cases (one letter, one two-letter word with no square, a pair that
squares both ways, a word that squares with itself, a 3 by 3 square,
three rotations of one word that square in three orders, a pair that
squares one way, and three words whose two squares share one), and for 300 random lists of 3 to 30
distinct words of 2 to 4 letters from a, b and c, the number of
squares and a checksum. The squares are printed as sorted
`row/row/row` lines, since any order is allowed. `word_squares.py`
mirrors the ★ arm and its output is byte-identical.

The ★ arm's index first held each word under every prefix from the
empty one to the whole word. Picking mutants showed that the whole
word is never looked up: row `r` looks up a prefix of `r` letters, and
`r` is less than the length. The index now stops one short.

## Differential

`differential.kara` holds copies of the four arms. Each of 1,500 random
cases is a list of 2 to 8 distinct words of 1 to 3 letters from a, b
and c. Each arm's squares are compared as sorted lines:

| | property |
|---|---|
| P1 | the squares are those of trying every sequence of words and keeping the ones that read the same down as across |
| P2 | every square's rows are given words and read the same down as across, and no square appears twice |
| P3 | renaming the letters (a to b, b to c, c to a) renames the squares and finds no others |
| P4 | the list reversed gives the same squares; one more word keeps every square |
| P5 | all four words of two letters over a and b give 8 squares (the symmetric 2 by 2 grids), all eight of three letters give 64, and the one word `ccc` gives 1 |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | prefix: the column is read from each row's first letter | P1 946, P2 892, P3 946 |
| M2 | prefix: a square is complete one row early | P1 1472, P2 484, P3 1472, P5 1500 |
| M3 | trie: the root lists no words | P1 1387, P3 1387, P5 1500 |
| M4 | trie: each word is listed at the root again instead of below | P1 1387, P2 484, P3 1387, P5 1500 |
| M5 | scan: the last letter of the column is not compared | P1 994, P2 994, P3 994, P5 1500 |
| M6 | scan: the row is compared with the diagonal | P1 1003, P2 1003, P3 1003 |
| M7 | sorted: the binary search runs the wrong way | P1 1387, P3 1387, P5 1500 |
| M8 | sorted: the run is not checked for the prefix | P1 961, P2 961, P3 954, P5 1500 |

No mutant fails P4: reversing the list, or adding a word, changes no
arm's way of finding candidates, so a mutant is wrong the same way on
both lists. M3 and M7 fail the same checks, since both find no
candidates at all; P2 misses them because an empty answer is well
formed. P5 misses M1 and M6 because it checks only counts: when every
word of a length is present, any rule that fixes one more letter per
row leaves the same number of choices, so those mutants find a wrong
set of squares of the right size.

## Verification

All four arms print the same output as `word_squares.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp`, and `karac check` passes on every file. The
differential prints `30000 checks, 0 failures` on all six backends:
those three, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build`.

The arms do not run on the last three: the frozen legacy codegen has
no `split_whitespace()` on a `Str` parameter, which the harness's
`show(text: Str)` uses, as in katas 418, 419 and 422. Legacy is frozen,
so this is noted, not filed. The arms' own code builds there, as the
differential and the bench program show.

## Benchmarks

The bench program uses the ★ arm on 1,000 distinct words of 4 letters
(the problem's limits) from the first 16 letters, about 60,000 squares
per search. Each of 20 rounds replaces one word with a new one and
searches again, and the program folds the squares' count and two
letters of each square into a checksum. Every implementation prints
`20 rounds on 1000 words: 1199807 squares, checksum 616762056`; a
2-round cut of the Kāra program under `karac __mir-run` prints the
same as the C program cut the same way. The C mirror's map is a table
indexed by the prefix read as a base-27 number, where the others use a
hash map keyed by the prefix string; each implementation copies every
square's rows out, as the Kāra program clones them. Spot timings on a
shared 4-core container, three runs each (`bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.26 to 0.29 s |
| Go | 0.65 to 0.82 s |
| Kāra (legacy `karac build`) | 0.77 to 0.92 s |
| Rust (`rustc -O`) | 0.91 to 1.05 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.00 to 1.12 s |
| Python | 4.9 s |

The C mirror's array index is likely most of its lead (not measured
separately). The Kāra program also prints the same line under
`karac __mir-llvm-run` in 7.0 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark. The
`karac build` time is the frozen legacy backend.

## Compiler findings

No new findings. The ★ arm first wrote the index with `Map.get_mut`,
which `docs/library/collections.md` documents but `karac check`
refuses (B-2026-10-12-3, open); `Map.entry(..).or_insert(..)`, the
form the same document uses for grouping, is what the arm uses now.
