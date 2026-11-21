# 2255. Count Prefixes of a Given String

You are given a string array `words` and a string `s`, where
`words[i]` and `s` comprise only of **lowercase English letters**.

Return *the **number of strings** in* `words` *that are a **prefix** of*
`s`.

A **prefix** of a string is a substring that occurs at the beginning of
the string. A **substring** is a contiguous sequence of characters
within a string.

```
words = ["a","b","c","ab","bc","abc"], s = "abc"  ->  3
words = ["a","a"], s = "aa"                        ->  2
```

**Constraints:** `1 <= words.length <= 1000`; `1 <= words[i].length,
s.length <= 10`; `words[i]` and `s` consist of lowercase English letters
only.

Each word is tested on its own: it is a prefix when it is no longer than
`s` and matches `s` letter for letter from the start. A word that
appears twice counts twice, and `s` itself is a prefix of itself.
O(words * |s|).

## Approaches

| file | mechanism |
|---|---|
| `prefixes.kara` ★ | `words.iter().filter(\|w\| s.starts_with(w)).count()` |
| `prefixes_bytes.kara` | no library test: each word's `bytes()` against `s`'s, a word longer than `s` skipped, the rest compared in a `while` loop that stops at the first difference |
| `prefixes_set.kara` | `s`'s own prefixes, all `\|s\|` of them, cut once into a `Set[String]` with `s[0..k]`, and each word looked up in it |
| `prefixes_struct.kara` | a `struct Text` of `s`'s characters whose `begins_with` (`ref self`) walks a word's characters `zip`ped with its own, failing on the first that differs, and counts them to see the word did not run past the text |
| `prefixes_iter.kara` | iterator chains: a word kept by `filter` when it is no longer than `s` and `all` of its characters `zip`ped with `s`'s match, then `count`ed |
| `prefixes_solution.kara` | LeetCode's Rust template: `Vec<String>` and `String` in, `i32` out, `words.iter().filter(\|w\| s.starts_with(w.as_str())).count() as i32`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (a word longer than `s`, a word that is `s`, one prefix three
times, and words that match `s` but for a last letter), each with its
count; then the total over 2000 cases of 1 to 8 words of 1 to 4 letters
and an `s` of 1 to 6, from two letters, with a checksum of the counts;
then 200 cases of the constraints' most words, 1000 of up to 10 letters
from one to five letters, and an `s` of up to 10. `prefixes.py` mirrors
the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 6 edits: `Vec<..>` to
`Vec[..]`, `struct Solution;` to `struct Solution {}`, and, in the
adapter, the `.clone()`s the borrowed parameters do not need and an
`as i64` that widens by itself. `w.as_str()` is Kāra as it stands.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every word, every beginning of `s` cut by
`substring(0, k)` for `k` from 0 to `|s|`, and the word counted when one
of them equals it; no `starts_with`, and no byte or character walk. It
checks 300 random cases of 1 to 8 words of 1 to 4 letters and an `s` of
1 to 6, from two letters; then 30 with words and `s` of up to 10
letters from five; then 30 whose words are beginnings of `s`, half of
them with their last letter drawn again. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the count is the words that are beginnings of `s`, read literally |
| P2 | the words in reverse order: the same count |
| P3 | `s` itself added as a word: the count one more |
| P4 | every word and `s` with `e` put in front: the same count |
| P5 | `s` with one more letter added as a word: the same count |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 109631665, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
compares each word with `s` cut to the word's length. On a failure it
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
| M3 | ★: the word anywhere in `s` | P1 141, P4 139, P6 141 |
| M4 | ★: the words that are not prefixes | P1 334, P3 360, P5 360, P6 334 |
| M6 | ★: the first word skipped | P1 78, P2 96, P6 78 |
| M7 | bytes: a word as long as `s` skipped | P1 55, P3 360, P6 55 |
| M8 | bytes: the last byte not compared | P1 206, P6 206 |
| M9 | bytes: any first byte alike enough | P1 162, P4 258, P6 162 |
| M13 | set: one-letter prefixes left out | P1 136, P3 60, P4 136, P6 136 |
| M14 | set: the suffixes, not the prefixes | P1 143, P4 140, P6 143 |
| M16 | set: only the prefixes up to half of `s` and one | P1 33, P3 258, P4 26, P6 33 |
| M17 | struct: a matching character taken as a difference | P1 235, P3 360, P4 200, P6 235 |
| M19 | struct: the length never counted | P1 190, P3 360, P6 190 |
| M20 | struct: the text read from its second character | P1 174, P3 360, P4 144, P6 174 |
| M23 | iter: no length check | P1 64, P5 360, P6 64 |
| M24 | iter: any character alike enough | P1 223, P4 200, P6 223 |
| M25 | iter: `s` read backwards | P1 131, P3 223, P4 179, P6 131 |
| M30 | solution: the last word skipped | P1 86, P2 96, P3 274, P5 86, P6 86 |
| M31 | solution: only the first letter tested | P1 246, P4 295, P5 360, P6 246 |

P1 and P6 kill all seventeen, P4 ten, P3 nine, P5 four, and P2 two.
P4 puts `e` in front of every word and `s`, so an edit that reads a
different place in `s` than in the word, or tests only the first
letter, now sees an `e` where it saw something else. P3 adds `s` itself,
which every edit that refuses a word as long as `s`, or misreads `s`'s
own letters, does not count. P5 adds a word one letter longer than `s`,
caught by the edits that drop the length check or count the words that
fail, and by the template's skip of the last word, which the added word
moves. P2 reverses the words, and catches only the edits that skip
a word by its place (M6, M30). M8 is caught by no property but the
literal and agreement: a word that matches `s` but for its last letter
is the only case it miscounts, and none of the transformations makes
one.

Of the thirty-one, fourteen were not kept, and none survives, crashes
or differs between the backends. Each fails as a kept one does or as
another left out: `s` itself refused in the ★, set and iter arms (M5,
M12, M22) as the bytes arm's (M7); the word at the end of `s` in the ★
arm and the template (M2, M28) as the set arm's suffixes (M14); the set
arm's words not in the set (M15) as the ★ arm's (M4); the template's
one-letter words dropped (M29) as the set arm's (M13); the struct arm's
one match enough (M18) as the iter arm's missing length check (M23);
the struct arm's text reversed (M21) as the iter arm's (M25); the
bytes and iter arms' first letter not compared (M10, M26), and `s` a
prefix of the word in the ★ arm and the template (M1, M27), as each
other; and the bytes arm's matched bytes counted for the word (M11),
which alone fails its own way and is left out because the bytes arm
keeps three.

## Verification

Every arm prints the same output as `prefixes.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the set arm takes 1.7 s, the ★ arm and the
template 1.8 s, the bytes arm 2.0 s, the iter arm 2.3 s, the struct arm
2.6 s, and the differential 0.4 s; most of each arm's time is making
the 200 * 1000 words.

## Benchmarks

The bench answers 500 cases of 1000 words of up to 10 letters, from one
to five letters, and an `s` of up to 10, with the ★ arm in all five
languages. Making the words is most of the work, as it is in the
harness, so every language makes them the same way: each word's letters
pushed one at a time into a byte buffer of its own, which then becomes
the string (`String.from_utf8` in Kāra and Rust, `bytearray.decode` in
Python, `string(b)` in Go), and in C the buffer itself, one allocation
per word. Every implementation prints `500 cases of 1000 words:
checksum 965480548`.

BENCHTAB
