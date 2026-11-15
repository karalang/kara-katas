# 2129. Capitalize the Title

You are given a string `title` consisting of one or more words separated
by a single space, where each word consists of English letters.
Capitalize the string by changing the capitalization of each word such
that:

- If the length of the word is `1` or `2` letters, change all letters to
  lowercase.
- Otherwise, change the first letter to uppercase and the remaining
  letters to lowercase.

Return the capitalized `title`.

```
title = "capiTalIze tHe titLe"       ->  "Capitalize The Title"
title = "First leTTeR of EACH Word"  ->  "First Letter of Each Word"
title = "i lOve leetcode"            ->  "i Love Leetcode"
```

**Constraints:** `1 <= title.length <= 100`; `title` consists of words
separated by a single space without any leading or trailing spaces; each
word consists of uppercase and lowercase English letters and is
non-empty.

Each word is lowered whole, and one of three letters or more has its
first letter raised. One pass, O(n).

## Approaches

| file | mechanism |
|---|---|
| `title.kara` ★ | `split(" ")`, each word `to_lowercase()`, a long one rebuilt as `f"{lower[..1].to_uppercase()}{lower[1..]}"`, collected into a `Vec[String]` and joined |
| `title_bytes.kara` | one pass over `bytes()`, each word's start remembered; at the space or the end that closes it, its bytes pushed lowered by arithmetic, the first raised, through `char.try_from(..)` |
| `title_chars.kara` | the chars read into a `Vec[char]` word, lowered with `to_ascii_lowercase`, `chain`ed with a final space so the last word is handed on too |
| `title_struct.kara` | a `struct Word { text }` whose `capitalized` (`ref self`) matches on the length with a range pattern `0..=2`; the words gathered with `fold` |
| `title_words.kara` | `split_whitespace` into lowered words, each long one rewritten in place through `iter_mut` as `*w = f"..."` |
| `title_solution.kara` | LeetCode's Rust template: each word lowered, a long one rebuilt from `cs.next()` raised and `cs.as_str()`, carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (one letter, two, three, and words of every length up to five),
each with its answer; then the capitals and a checksum over 3000 random
titles of 1 to 8 words of 1 to 6 letters, each letter a capital with
chance a half; then the constraints' longest, 50 words of one letter, 33
of two and 25 of three. `title.py` mirrors the ★ arm and its output is
byte-identical.

The template and the bytes arm met three gaps, all fixed in karac with
a test named for this kata (karac 5ffe421e9a,
`tests/kata_2129_rust_char_spellings.rs`). The template rebuilds a word
the way Rust's answers usually do, `f.to_uppercase().collect::<String>()
+ cs.as_str()`. A char's `to_uppercase()` is a `char` in Kāra, the
one-scalar mapping, so `.collect()` had no method and no fix; `karac fix`
now writes `f.to_string().to_uppercase()`, the full mapping Rust
collects. The iterator `chars()` returns had no `as_str`; it now has
Rust's, the text not yet read. And the bytes arm, written
`char.from_u32(b as u32).unwrap()`, was refused with the name of
`char.try_from` but no fix; `karac fix` now writes
`char.try_from(b as u32).ok()`, the same `Option`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each letter looked up in the alphabet in both cases, its word
found by scanning left and right to a space, and the letter written as a
capital when it starts a word of three letters or more and in small
otherwise. It checks 300 random titles of 1 to 5 words of 1 to 5
letters; then 30 of words of 1 to 3 letters only, where the rule turns;
then 30 of one word of 1 to 8. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the words in reverse order: the answer's words reversed |
| P3 | every letter's case swapped: the same answer |
| P4 | the title written twice with a space between: the answer twice |
| P5 | the answer capitalized again: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 titles: checksum 764251545, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
titles. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-four edits to the differential, four to nine to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the rest of a word left as it was | P1 290, P3 303, P6 290 |
| M4 | ★: the first letter kept twice | P1 303, P5 303, P6 303 |
| M5 | ★: a three-letter word left small | P1 169, P6 169 |
| M7 | bytes: a Z never lowered | P1 64, P3 116, P5 26, P6 64 |
| M8 | bytes: each word starting at its space | P1 273, P2 268, P4 360, P5 273, P6 273 |
| M9 | bytes: the last word never closed | P1 360, P2 273, P4 360, P6 360 |
| M10 | chars: the letters never lowered | P1 338, P3 360, P6 338 |
| M12 | chars: the word never cleared | P1 273, P2 273, P4 360, P5 273, P6 273 |
| M13 | chars: a space only after more than one letter | P1 59, P2 105, P4 70, P5 42, P6 59 |
| M14 | struct: a two-letter word raised | P1 165, P6 165 |
| M15 | struct: a long word raised whole | P1 303, P6 303 |
| M16 | struct: the words folded in reverse | P1 273, P5 273, P6 273 |
| M26 | words: the first word never raised | P1 217, P2 221, P4 217, P6 217 |
| M27 | words: the last word never raised | P1 218, P2 221, P4 218, P6 218 |
| M28 | words: the words joined with nothing | P1 273, P2 273, P4 360, P5 246, P6 273 |
| M23 | solution: the adapter adding a space at the end | P1 360, P2 360, P4 360, P5 360, P6 360 |
| M32 | solution: a short word kept as it was | P1 182, P3 254, P6 182 |

P1 and P6 kill all seventeen, P2, P4 and P5 eight each, and P3 four.
Most of the edits that miscase a word fail P1 alone: a word of the
wrong length raised (M5, M14) or a long word raised whole (M15) answers
the same however the title is turned, since a word's answer depends on
nothing outside it. P2 and P4 see the edits that treat one word unlike
the others, by its place (M26, M27) or at its edges, where a word is
opened, closed or spaced (M8, M9, M12, M13, M28, M23). P3 sees the edits
that leave some letter's case as it came: the rest of a word (M1), a
short word (M32), every letter (M10), or only a Z (M7), which no other
property but P5 sees, since a Z swapped to a z is right. P5 sees an
answer that is not yet a title: a letter kept twice (M4), words run
together or reversed (M16, M28), a trailing space (M23).

Of the thirty-four, seventeen were not kept. Three are equivalent: the
struct arm raising each word before lowering it, the adapter lowering
the title, and the template reading `as_str()` before the first `next()`.
None survives, and none fails by a crash. Twelve fail as a kept one
does: a long word raised whole or its first letter never raised or
lowered in the ★, template and words arms as M15; a two-letter word
raised in the ★, chars and words arms as M14; a long word cut to its
first letter in the template and its second letter dropped in the words
arm as M4; a three-letter word left small in the bytes arm and the
template as M5; the words never lowered in the words arm as M10; and a
short word kept as it was in the ★ arm as M32. Two are killed with
checks of their own but were left out because their arms keep their
share: the template collecting all but the first word and the chars arm
dropping the last (P1 360, P2 273, P4 360, P5 273, P6 360).

## Verification

Every arm prints the same output as `title.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 s to 0.45 s and the
differential 0.78 s.

`karac fix` carries the template in two rounds of 7 and 3 edits: Rust's
spellings (the turbofish on `collect` into a `Vec<String>` moved to
`Vec[String].from_iter(..)`, the one on `collect::<String>()` dropped,
`String::new()` to `String.new()`, `struct Solution;` to `struct
Solution {}`, the adapter's `&str` to `Str` and `Solution::` to
`Solution.`); then the char separator `' '` of `split` to `" "`,
`f.to_uppercase().collect()` to `f.to_string().to_uppercase()`, and
`cs.as_str()` given `.to_string()`, since `+` appends an owned
`String`. The bytes arm's `char.from_u32(b as u32)` is carried in one
edit to `char.try_from(b as u32).ok()`.

## Benchmarks

The bench builds 1000 titles of words of 1 to 6 letters, up to 100
letters and spaces, once as bytes, then capitalizes every title 200
times, one letter's case swapped before each so that no title repeats
one before, the title made a string from its bytes each time, with the
★ arm in all five languages; C, which has no split, lowers each word
into one buffer. Every implementation prints `200000 titles: 2913800
capitals, checksum 780942859`.

BENCHTAB
