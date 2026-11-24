# 1324. Print Words Vertically

Given a string `s`, return all the words vertically in the same order in
which they appear in `s`. Words are returned as a list of strings,
complete with spaces when necessary (trailing spaces are not allowed).
Each word is put on only one column and each column holds only one word.

```
s = "HOW ARE YOU"         ->  ["HAY","ORO","WEU"]
s = "TO BE OR NOT TO BE"  ->  ["TBONTB","OEROOE","   T"]
s = "CONTEST IS COMING"   ->  ["CIC","OSO","N M","T I","E N","S G","T"]
```

**Constraints:** `1 <= s.length <= 200`, `s` contains only upper case
English letters, and there is exactly one space between two words, with
none at either end.

The arms are `fn print_vertically(s: String) -> Vec[String]`.

## Approaches

| file | mechanism |
|---|---|
| `print_vertically.kara` ★ | the words split apart, and row i made of each word's i-th letter in turn, a space for a word too short to have one, with the spaces left at the row's end cut off by `trim_end`. O(words × longest word) |
| `print_vertically_pad.kara` | every word padded with spaces to the longest word's length, so the words form a grid of `char`s; the grid read down its columns gives the rows, and each row's spaces at the end are popped off. O(words × longest word) |
| `print_vertically_bytes.kara` | one pass over the sentence's bytes, counting which word and which letter of it each byte is: letter i of word j goes on the end of row i, which is first padded with spaces out to column j. A row is only padded to reach a letter, so no row ends in a space and nothing is trimmed. O(length of s + the rows' lengths) |
| `print_vertically_solution.kara` | a Rust solution as LeetCode's Rust users write it (the words from `split_whitespace`, each row made of every word's `chars().nth(i).unwrap_or(' ')`, then `trim_end`), carried to Kāra by `karac fix` |
| `print_vertically_lastword.kara` | a second Rust solution as LeetCode's Rust users write it (the words as `as_bytes().to_vec()`, and each row built only out to the last word long enough to reach it, so there is nothing to trim), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, one letter,
the row count for one word of 200 letters, the constraints' longest, and
100 one-letter words, the most there can be (`[HAY,ORO,WEU]
[TBONTB,OEROOE,   T] [CIC,OSO,N M,T I,E N,S G,T] [A] 200 [BBB…BC]`);
then 600 random sentences of up to 200 letters and spaces, with words of
1 to 3 letters, of 1 to 10, of 1 to 40, or a single word, over 2 or 26
letters (`600 random sentences: rows total 16841, checksum 789617559`).
`print_vertically.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the three Kāra arms checked clean as first written. The
first Rust arm takes one round of 12 fixes by `karac fix`'s count, from 9
errors: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `Vec<&str>` to `Vec[Str]`, `::` to `.`, and `for w in &words`
to `for w in ref words`; `split_whitespace`, `chars().nth(i)` and
`unwrap_or` are kept as written. The second takes one round of 14 fixes
from 6 errors: the same rewrites, `vec![]` to `Vec.new()`, the `char`
pattern of `split(' ')` to the text `" "`, and `as_bytes()` to `bytes()`.
Both outputs match on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a grid of spaces as tall as the longest word and as wide as the
words are many, each word written down its own column, and each row's
spaces at the end cut off. 2000 sentences of 1 to 8 words, in four kinds,
500 each: words of 1 to 3 letters over 2; words of 1 to 6 letters over 26;
short words with one of 4 to 12 letters among them; and a single word.
Every sentence and extra word is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the words in the reverse order: each row, padded out to the number of words, read backwards |
| P3 | a word put on the end: each of its letters on the end of its row, and new rows below if it is the longest |
| P4 | every word said twice where it stands: every place of every row, padded out, twice |
| P5 | the first word taken away, when there are two or more: each row's first place gone, and empty rows at the bottom dropped |
| P6 | the ★ arm's answer |

All 56,510 checks pass on every arm: `2000 sentences: checksum 638085684,
56510 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum and check count.

## Mutation testing

Twelve edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Two are left out: in the lastword
arm, a word as long as the row's number taken to reach it leaves a space
at the row's end, and fails on its own arm exactly the checks the ★ arm's
untrimmed rows fail on every arm (M1); and a word reaching a row only if
it goes on past it fails exactly the checks of the bytes arm's words
begun a row down (M6). The ten kept, two to each arm, are each killed,
fail the same way under both backends and not by a crash, and no two fail
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the spaces at a row's end never trimmed | P1 858, P2 831, P3 915, P4 858, P5 682, P6 3432 |
| M2 | ★: one row too few | P1 2000, P3 1085, P5 255, P6 8000 |
| M3 | pad: at most one space popped off a row's end | P1 504, P2 513, P3 476, P4 858, P5 366, P6 504 |
| M4 | pad: the last word left out of every row | P1 2000, P2 1302, P3 2000, P4 2000, P5 401, P6 2000 |
| M5 | bytes: a row padded out one column short | P1 1084, P2 1263, P3 1444, P4 1084, P5 498, P6 1084 |
| M6 | bytes: each word after the first begun a row down | P1 1302, P2 1302, P3 2000, P4 2000, P5 1302, P6 1302 |
| M7 | solution: nothing put where a word has no letter | P1 1084, P2 1263, P3 1444, P5 831, P6 1084 |
| M8 | solution: as many rows as the first word has letters | P1 831, P2 1005, P3 1196, P5 842, P6 831 |
| M9 | lastword: the words counted from the second, so the last to reach a row is found a place early | P1 1302, P2 1302, P3 2000, P4 2000, P5 1109, P6 1302 |
| M10 | lastword: each row built out to the first word that reaches it | P1 1104, P2 1104, P3 1302, P4 1302, P5 1104, P6 1104 |

P1, P3, P5 and P6 kill all ten, P2 nine and P4 seven. Putting a word on
the end (P3) makes the new word the last column, so every edit that gets
a row's end wrong, or the last word, or the rows' number, shows there.
Reversing the words (P2) misses only the row too few (M2), which is lost
whichever way round the words stand. Saying every word twice (P4) misses
the three edits whose mistake is made the same way twice over: the row
too few (M2), the missing spaces left out twice as often (M7), and the
rows counted from a first word that is still first (M8).

## Benchmarks

The bench builds 100 sentences of 200 letters and spaces, the
constraints' longest, once, in turn from words of 1 to 3 letters, of 1
to 10, of 1 to 40 and of 1 to 200; then makes 1000 passes, each setting
one letter of every sentence from the checksum so far, so no answer
carries over, answering it with the ★ arm and folding the rows' letters,
their number and the pass into the checksum. Each call takes fresh words
and rows in every language, a `malloc` for each in C. Every
implementation prints `1000 passes over 100 sentences of 200: checksum
248418253`.

BENCHTAB
