# 500. Keyboard Row

Given an array of strings `words`, return the words that can be typed
using letters of the alphabet on only one row of an American keyboard.

The rows are `"qwertyuiop"`, `"asdfghjkl"` and `"zxcvbnm"`. Case does
not matter: `"Dad"` can be typed on the middle row.

```
words = ["Hello","Alaska","Dad","Peace"]  ->  ["Alaska","Dad"]
words = ["omk"]                           ->  []
words = ["adsdf","sfd"]                   ->  ["adsdf","sfd"]
```

**Constraints:** `1 <= words.length <= 20`; `1 <= words[i].length <= 100`;
`words[i]` consists of English letters (both lowercase and uppercase).

## Approaches

Every arm is `fn find_words(words: Vec[String]) -> Vec[String]` and
keeps the words in the order given.

| file | mechanism |
|---|---|
| `keyboard_row.kara` ★ | a table of 26 row numbers, one per letter; a word stays when every lowercase letter's row is the first letter's row, and the walk stops at the first letter on another row |
| `keyboard_row_sets.kara` | a `Set[char]` for each row; a word stays when one of the sets holds all its lowercase letters |
| `keyboard_row_masks.kara` | each row and each word as a 26-bit mask of its letters; a word stays when some row's mask covers it (`m & ~row == 0`) |
| `keyboard_row_filter.kara` | one `filter` over the words: `any` row whose text holds, for `all` the word's lowercase letters, `any` equal letter; then `map(clone)` and `collect` |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 8 lines: the three LeetCode examples, one
letter each, whole rows, mixed case, `["abc","Keyboard","Row"]`, and for
300 random lists of 1 to 20 words of 1 to 12 letters (each word from one
row, 2 in 3, or the whole alphabet, a letter upper case with odds 1 in
4) the count of words kept, their letters and a checksum of them.
`keyboard_row.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases, each two lists of 1 to 10 words of 1 to 8 letters:
each word from one row (2 in 3) or the whole alphabet, a letter upper
case with odds 1 in 4, and now and then one more letter from anywhere,
so that many words miss their row by one letter.

| | property |
|---|---|
| P1 | the words are the reference's, which compares every letter of each word with every letter of each row |
| P2 | the words kept are words given, in their order |
| P3 | swapping the case of every letter keeps the same words, case swapped |
| P4 | reversing every word keeps the same words, reversed |
| P5 | the two lists together keep what each keeps alone, one after the other |

## Mutation testing

Nine edits to `differential.kara`, each run under `karac __mir-run`.
All eight non-equivalent ones are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `l` is left off the middle row, so its table entry stays 0, the top row | P1 536 |
| M2 | ★: a letter on a lower row than the first letter passes (`r < first` for `r != first`) | P1 903, P4 1014 |
| M3 | sets: a word stays when no letter is in the row, not every letter | P1 1052 |
| M4 | sets: the letters are not lowercased | P1 1248, P3 1059 |
| M5 | masks: a word stays when its mask has no bit inside the row (`m & row == 0`) | P1 1052 |
| M6 | masks: a letter flips its bit instead of setting it (`^` for `\|`) | P1 114 |
| M7 | filter: every row must hold the word (`all` rows for `any`) | P1 1388 |
| M8 | filter: one letter on the row is enough (`any` letter for `all`) | P1 1287 |
| E1 | sets: no `break` after a word is kept | 0 |

E1 is equivalent: no letter is on two rows, so a word that one set
holds no other set holds, and the loop over the rows could keep it at
most once with or without the `break`.

M2 is the one that depends on the order of the letters: a word whose
first letter is on the bottom row and whose others are on the rows above
passes forwards and fails reversed, so P4 sees it. M4 drops every word
with an upper-case letter, since no set holds one, and swapping the
case turns the lower-case words it keeps into upper-case ones it drops,
so P3 sees it. M3 and M5 are the same
wrong rule written two ways, "no letter of the word in this row", and
fail the same 1,052 cases. M6 only goes wrong on a word with a letter
an even number of times, whose bit then cancels out (`"qaqa"` has the
empty mask and passes every row), which the short random words make
rare: 114 cases. Each of M1, M3 and M5 to M8 is a rule that depends only
on which letters a word has, never their order or case, so P2 to P5 hold
under it and only P1 sees it. P2 kills none of the eight: no mutation
reorders the output.

## Verification

All four arms print the same output as `keyboard_row.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
`karac check` passes on every file, the bench program included. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on all four arms: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output, and the differential prints `30000 checks, 0
failures` under `karac run --interp`. Legacy `karac build` warns on the
masks arm that `word` is "moved here, used again here", where
`mask(word)` lends the word before `word.clone()`; the output is right
all the same. It does not build the differential: "`Iterator.rev()` is
not yet supported under `karac build`/`karac run` (codegen) for this
chain shape", on P4's `w.chars().rev().collect()`. Nor does it build the
bench program (see Benchmarks). Legacy is frozen, so these are noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 20,000 lists of 20 words
(the problem's most) of 1 to 100 letters (the problem's most) once, each
word from one row (2 in 3) or the whole alphabet, a letter upper case
with odds 1 in 4. Then it solves each list once, folding each kept
word's length and first letter into a checksum. Every implementation
prints `20000 lists of 20 words: 268941 words kept, 13476095 letters,
checksum 17452164`, the Kāra program under `karac __mir-run` included
(in 68 s, at kara `d9a7136c58`).

Every mirror lower-cases each word into a fresh string, as the ★ arm's
`to_lowercase()` does, and copies each kept word into a fresh growable
output, as its `out.push(word.clone())` does: Rust `to_lowercase()` and
`clone()` onto `Vec::new()`, Go `strings.ToLower` and `append` (a Go
string is immutable, so its copy is the reference), Python `lower()`
and `append`, and C a `malloc`'d lower-case buffer, a `malloc`'d copy
and an output array it doubles with `realloc`. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.13 to 0.15 s |
| Rust (`rustc -O`) | 0.31 to 0.38 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.28 to 0.33 s |
| Go | 0.50 to 0.54 s |
| Python | 11.9 to 12.8 s |
| Kāra (`karac build --mir`) | 0.47 to 0.68 s |

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `find_words(all[k])`, which v2 reads as a borrow.
So `bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`22c7db1833`. Under `karac __mir-llvm-run` the program prints the same line in
4.3 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

kara B-2026-10-13-16 (diagnostics, open): `karac fix` turns `!x` into
`not x` whatever `x` is. The masks arm was first written Rust-style,
`m & !row == 0`; one `karac fix` gave `m & not row == 0`, a type error
("unary 'not' requires 'bool', found 'i64'; the bitwise complement of
an integer is `~`"), and a second gave `m & ~ row == 0`. The arm reads
`m & ~row == 0`.

P4 builds each reversed word as `let back: String =
w.chars().rev().collect();` and then pushes it, where
`reversed.push(w.chars().rev().collect())` is the natural form. That
form runs right on `karac __mir-run` and passes `karac check` with
`KARAC_CHECK_LIBRARY=1`, but default `karac check` refuses it:
"expected 'String', found 'Vec[char]'". That is kara B-2026-10-12-33,
filed from kata 459, so this is a second data point for it.

`String.contains` takes a `Str`, so the filter arm asks whether a row
holds a letter with `row.chars().any(|r| r == ch)`, not
`row.contains(ch)`. That is the documented signature, not a bug.

When the arms were written (kara `d9a7136c58`), `karac check` refused
`char.is_ascii_uppercase()`, kara B-2026-10-13-12 (filed from kata 482),
and P3 used `is_uppercase()`. kara `68f0f9d257` fixed that before this
kata landed, and P3 now uses `is_ascii_uppercase()`.
