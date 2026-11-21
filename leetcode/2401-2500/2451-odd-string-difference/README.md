# 2451. Odd String Difference

You are given an array of equal-length strings `words`. Assume that the
length of each string is `n`.

Each string `words[i]` can be converted into a **difference integer
array** `difference[i]` of length `n - 1` where `difference[i][j] =
words[i][j+1] - words[i][j]` where `0 <= j <= n - 2`. Note that the
difference between two letters is the difference between their
**positions** in the alphabet i.e. the position of `'a'` is `0`, `'b'`
is `1`, and `'z'` is `25`.

- For example, for the string `"acb"`, the difference integer array is
  `[2 - 0, 1 - 2] = [2, -1]`.

All the strings in words have the same difference integer array,
**except one**. You should find that string.

Return *the string in* `words` *that has different **difference
integer array**.*

```
words = ["adc","wzy","abc"]         ->  "abc"
words = ["aaa","bob","ccc","ddd"]   ->  "bob"
```

**Constraints:** `3 <= words.length <= 100`; `n == words[i].length`;
`2 <= n <= 20`; `words[i]` consists of lowercase English letters.

Of any three words at least two share the common array, so the first
three settle which array is common, and one pass finds the word that
does not have it. The difference of two letters' places is the
difference of their byte codes, so no alphabet is needed.

## Approaches

| file | mechanism |
|---|---|
| `odd.kara` ★ | each word's difference array from its bytes, the common one read off the first three words, and the first word whose array is not it. O(m n) |
| `odd_naive.kara` | the statement read directly: each word compared with every other step by step, and the word that matches none of them is the answer. O(m^2 n) |
| `odd_map.kara` | a `Map[Vec[i64], i64]` from each difference array to how many words have it, built by `entry` and `or_insert`, then the words walked in order for the one whose array was seen once; the map is only looked up, never walked. O(m n) |
| `odd_column.kara` | column by column: at each step place every word's step compared with the first word's, and at the first place where some differ, the first word when all the others do and otherwise the one that does. O(m n) |
| `odd_iter.kara` | iterators: each word's array by `windows(2)` and `map`, the common one the array that `filter` and `count` find more than once among the first three, and the answer where `position` finds one that differs. O(m n) |
| `odd_solution.kara` | LeetCode's Rust template: a closure over `&String` with its return type written `-> Vec<i32>`, the arrays by `as_bytes().windows(2)`, and the odd word the one whose array differs from both of the next two, counted round the end; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; the odd
word first and last among two-letter words, `a` to `z`; then 100 words
of 20 letters, the constraints' most, with the odd one at places 0, 57
and 99; and 3000 random lists of 3 to 8 words of 2 to 6 letters as a
checksum of where each answer stands. `odd.py` mirrors the ★ arm and
its output is byte-identical, and the mirror was checked on 20000
random lists of up to 7 words whose odd word's array differs in one
step by one.

`check` first reports 8 errors on the template, and `karac fix` carries
it in one call, reporting 15 edits: the angle brackets of
`Vec<String>`, `Vec<i32>` and `Vec<Vec<i32>>` made square in seven, the
closing `>>` one; the closure's parameter type `&String` written `ref String`; `&&`
written `and`; `String::new` written `String.new`; `struct Solution;`
given its braces; and, once the template parses, the closure's `-> Vec[i32]`
moved to a type on the binding, `diff: Fn(ref String) -> Vec[i32]`,
since a Kāra closure does not declare its return type, in two edits;
`as_bytes()` written `bytes()`; and `.into_iter()` put after
`windows(2)`, which gives a vector in Kāra. The closure passed to `map`
by name, `as i32` and the `!=` on vectors stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each word's difference array built as the statement defines
it, each letter's place found by walking the alphabet, and the answer
the word whose array differs from every other word's while the others
all agree with one another. No array is counted or hashed, and none is
chosen from the first three. It checks 300 random lists of 3 to 8 words
of 2 to 6 letters; then 30 of up to 40 words of up to 20 letters; then
30 of 3 to 10 words where the odd word's array differs in one step by
one. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the words in reverse order: the same word |
| P3 | each word moved along the alphabet as far as it stays in it: the word at the same place |
| P4 | the letters of each word reversed: the word at the same place |
| P5 | the answer moved to the front of the list: the same word |
| P6 | each arm agrees with at least three of the other five |

P2 and P5 hold because the order of the words does not change which
array is common. P3 holds because moving a word along the alphabet
keeps every difference. P4 holds because reversing a word reverses and
negates its array, so two words' arrays are equal after it exactly when
they were before.

The differential prints `360 cases: checksum 95266295, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and compares every pair of arrays. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the common array from the first two | P1 74, P2 126, P6 74 |
| M4 | ★: each step the sum of its letters | P1 288, P2 348, P3 44, P6 288 |
| M6 | ★: the third word for the first | P1 63, P2 138, P6 63 |
| M8 | naive: only the first step compared | P1 40, P2 48, P4 68, P6 40 |
| M9 | naive: the last word never tried | P1 61, P2 124, P6 61 |
| M10 | naive: steps compared by their size | P1 9, P2 11, P6 9 |
| M13 | map: the first step left out of each key | P1 65, P2 78, P4 28, P6 65 |
| M14 | map: the key the letters themselves | P1 287, P2 353, P3 104, P4 13, P6 287 |
| M16 | map: a count of two taken as odd | P1 30, P2 48, P6 30 |
| M17 | column: the first word odd when one differs | P1 297, P2 350, P6 297 |
| M19 | column: only the second word compared | P1 286, P2 337, P5 137, P6 286 |
| M20 | column: each step the letter alone | P1 295, P2 344, P3 12, P4 3, P6 295 |
| M23 | iter: an array seen once enough | P1 63, P2 124, P5 360, P6 63 |
| M25 | iter: the word after the odd one | P1 360, P2 343, P3 28, P5 201, P6 360 |
| M26 | iter: the first common array found | P1 360, P2 344, P6 360 |
| M27 | solution: only the next word compared | P1 297, P2 349, P3 26, P5 194, P6 297 |
| M28 | solution: either neighbour enough | P1 297, P2 350, P3 16, P5 143, P6 297 |


P1, P2 and P6 kill all seventeen, P3 six, P5 five and P4 four.

Fourteen are not kept. Nine fail exactly as a kept one: the ★ arm's
first word taken as common (M2) as the iter arm's array seen once
enough (M23), both taking the first word's array as the common one;
the ★ arm's first step left out and the column arm's first step place
skipped (M3, M18) as the map arm's first step left out of each key
(M13); the ★ arm's common word returned and the map arm's commonest
array taken (M5, M15) as the iter arm's first common array found
(M26), each answering a word that has the common array; the naive arm's
word matched with itself, the map arm's every count one and the column
arm's first word returned for the one that differs (M7, M12, M21) as
the column arm's first word odd when one differs (M17), each answering
the first word in nearly every case; and the template's next word
returned (M31) as the iter arm's word after the odd one (M25). Two fail
apart from every kept one and alike, and neither is kept because those
arms keep their share already: the naive arm's word matched only
against later ones and the template's second neighbour not wrapped
(M11, M29), each answering the word before the odd one when the odd
one is last. The template's each step the sum of its letters (M30)
also fails apart and is left out.

Two end in a panic, not a wrong answer, under both
backends: the iter arm's common array from the first two and its
windows of three (M22, M24). The first finds no array twice when the
first two words differ, and the second gives every two-letter word the
same empty array, so no word differs; either way an `unwrap` meets
`None`.

## Verification

Every arm prints the same output as `odd.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.6 to 1.5 s, and the
differential 3.3 s; under `karac __mir-llvm-asan` the differential
takes 1.0 s and under `karac run` 0.8 s.

## Benchmarks

The bench builds 2000 lists of 100 words of 20 letters, the
constraints' largest, once from its own generator: each list's steps
from -1 to 1, and one word whose last step is one more. It then makes
110 passes; pass `p` swaps each list's first word with its word at
place `p + c`, so the odd word moves and the scan stops in a new place,
then answers every list and folds the answer's letters plus the pass
into the checksum. The bench uses the ★ arm, the common array from the
first three words, in all five languages. Every implementation prints
`110 passes over 2000 lists of 100 words: checksum 219505160`. Each
difference array is a fresh growable list (`Vec`, `Vec`, a slice by
`append`, a Python list), and in C a fresh `malloc`ed array, compared
by `memcmp`.

BENCHTAB
