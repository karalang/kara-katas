# 2108. Find First Palindromic String in the Array

Given an array of strings `words`, return the first palindromic string
in the array. If there is no such string, return an empty string `""`.

A string is palindromic if it reads the same forward and backward.

```
words = ["abc","car","ada","racecar","cool"]   ->  "ada"
words = ["notapalindrome","racecar"]           ->  "racecar"
words = ["def","ghi"]                          ->  ""
```

**Constraints:** `1 <= words.length <= 100`; `1 <= words[i].length <=
100`; `words[i]` consists only of lowercase English letters.

The words are tried in order, so the answer is the first word that
passes; the work is the palindrome check, which can stop at the first
pair of letters, from the two ends inward, that differ.

## Approaches

| file | mechanism |
|---|---|
| `palindrome.kara` ★ | each word's `bytes()` read from both ends towards the middle with two indices in a `while`, the first word whose ends agree all the way in returned with `clone()`. O(total letters) |
| `palindrome_reverse.kara` | each word reversed into a new `String` with `chars().rev().collect()` and compared with the word itself |
| `palindrome_iter.kara` | one chain: `find` over the words, a word a palindrome when its letters `zip` with themselves reversed and `all` pairs agree, then `cloned()` and `unwrap_or(String.new())` |
| `palindrome_recursive.kara` | a recursive check over the word's letters in a `Vec[char]`: the outer two agree and the letters between them read the same both ways, down to one letter or none; the words walked by index in a `while` |
| `palindrome_struct.kara` | a `struct Word` of the text and its letters, its `is_palindrome` comparing the first half with its mirror through `(0..n / 2).all(..)`; the words mapped to `Word`s lazily, filtered, and the first taken with `next()` and matched |
| `palindrome_solution.kara` | LeetCode's Rust template (`Vec<String>`, `into_iter().find` with `collect::<String>()` compared with `*w`, `unwrap_or_default()`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more (one word of one letter; an even palindrome after an odd near-miss;
a palindrome only at the end; the same palindrome twice), each with its
answer; then, over 3000 random lists of 1 to 20 words of 1 to 6 letters
from the first 2 to 5 letters, how many have a palindrome, the letters
in the answers, and a checksum of them; then the constraints' largest,
100 words of 100 letters, only the last a palindrome, and then none.
`palindrome.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the words in order, each letter compared with the one as far
from the other end, all of them rather than half. It checks 300 random
lists of 1 to 8 words of 1 to 5 letters from the first 1 to 3 letters;
then 30 of 1 to 100 words of up to 100 letters from two; then 30 of
palindromes with one letter of each changed three times in four. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is empty or one of the words, and reads the same reversed |
| P3 | a one-letter word appended: the same answer, or that word when there was none |
| P4 | every word reversed: the same answer |
| P5 | every letter renamed, `a` to `z`, `b` to `y` and so on: the answer renamed |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 961426951, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-three edits to the differential, five or six to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the far end stepping two | P1 49, P2 21, P4 30, P6 49 |
| M3 | ★: the last palindrome taken | P1 205, P3 334, P6 205 |
| M26 | ★: the near end stepping two | P1 51, P2 26, P4 30, P6 51 |
| M6 | reverse: the word compared with itself | P1 124, P2 124, P4 124, P6 124 |
| M8 | reverse: the reverse a letter short | P1 334, P3 360, P6 334 |
| M27 | reverse: the first word for none | P1 26, P2 26, P3 26, P4 26, P6 26 |
| M10 | iter: one agreeing pair enough | P1 88, P2 88, P4 88, P6 88 |
| M11 | iter: the reverse shifted one | P1 112, P2 74, P4 100, P6 112 |
| M28 | iter: one-letter words refused | P1 158, P3 126, P6 158 |
| M14 | recursive: the innermost pair skipped | P1 53, P2 53, P4 53, P6 53 |
| M15 | recursive: the far end held | P1 52, P6 52 |
| M17 | recursive: the first letter left out | P1 118, P2 82, P4 100, P6 118 |
| M18 | struct: the outer pair never compared | P1 74, P2 74, P4 74, P6 74 |
| M20 | struct: the first word that is not one | P1 360, P2 192, P3 168, P4 192, P6 360 |
| M30 | struct: a `z` for none | P1 26, P2 26, P3 26, P5 26, P6 26 |
| M25 | solution: the first word skipped | P1 166, P6 166 |
| M31 | solution: even palindromes refused | P1 106, P6 106 |

P1 and P6 kill all seventeen, P2 eleven, P4 ten, P3 six and P5 one. P2
and P4 see the edits that call a word a palindrome when it is not: a
pair skipped (M2, M14, M18, M26), the wrong pair compared (M11, M17), one
agreeing pair taken for all (M10), the word compared with itself (M6),
or the test turned round (M20); such a word does not read the same
reversed, and reversing every word makes a different word pass. P2 also
sees a wrong answer for none (M27, M30), which is not one of the words,
and P4 the first word for none (M27), which reversing the words changes.
P3 sees the edits whose answer depends on what follows the first
palindrome or on there being none: the last palindrome taken (M3), every
palindrome refused (M8), one-letter words refused (M28), the inverted
test (M20), and the wrong answer for none (M27, M30). P5 sees only a
fixed text for none (M30), which renaming the words does not rename; the
first word for none (M27) is renamed with them.

Of the thirty-three, sixteen were not kept, and one survives, equivalent
to the arm it edits: the struct arm comparing one pair past the middle
(M21). For an odd length that pair is the middle letter with itself, and
for an even one it is the middle pair again, read from the other side.
Of the other fifteen, all killed, fourteen fail as a kept one: the ★
arm's middle pair never compared as M14, its last letter never compared
as M11, and its first pair never compared as M18; the reverse arm's first
word that is not one as M20, and its first word skipped as M25; the iter
arm's last palindrome as M3, and its `a` for none as M30; the recursive
arm's one agreeing pair enough as M6, and its first word skipped as M25;
the struct arm's letter against its mirror's neighbour and its last
letter left out as M11; and the Rust arm's first word that is not one as
M20, its last palindrome as M3, and its `none` for none as M30. One is
killed with checks of its own but was left out because its arm keeps its
share: the Rust adapter dropping the last word (P1 48, P3 74, P6 48).

## Verification

Every arm prints the same output as `palindrome.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.45 s to 0.66 s, and the
differential 2.4 s; compiled it takes 0.6 s.

`karac fix` carries the template in two rounds of 9 and 2 edits:
Rust's spellings (`Vec<..>` to brackets, `struct Solution;` to `struct
Solution {}`, the adapter's `&Vec` to `ref` and `Solution::` to `.`, and
`w.chars().rev().collect::<String>() == *w` to
`String.from_iter(w.chars().rev()) == *w`); then `words.clone()` before
`into_iter()`, which takes the vector the method only borrows, and the
adapter's `ref` parameter to a bare one.

The turbofish needed two compiler fixes. Every other
turbofish's fix deletes it, or moves its type onto the `let` the call is
bound to; here the call is an operand of `==`, which takes its own
right-hand type, so deleting the list left `collect()` with nothing to
fix what it builds, and the template stopped at "cannot infer type
parameter". A turbofished `collect` compared with `==` or `!=` now
becomes the receiver of the collection's `from_iter`, the function
`collect` calls (kara PALSHA). And `String.from_iter`, which the
checker typed, did not resolve to the library's `impl
FromIterator[char] for String` in the MIR builder; it does since kara
B-2026-11-10-43, which landed the same fix first.
`tests/kata_2108_collect_turbofish_compare.rs` pins both.

Writing the differential met a third: `letters.iter().copied()`, Rust's
spelling, drew "no method 'copied'" with nothing to apply, where
`Option`'s `.copied()` already had a fix to `.cloned()`. An iterator's
gets the same fix now (kara COPIEDSHA).

## Benchmarks

The bench builds 200 lists of 100 words of 100 letters once, each word a
palindrome with one letter of its inner half changed in all but one word
in 200, so most checks walk to that letter; it then searches each list
50 times, with the ★ arm in all five languages: the bytes read from both
ends. Every implementation prints `10000 searches: 3600 found, 360000
letters, checksum 2246540`.

BENCHTAB
