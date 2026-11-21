# 2490. Circular Sentence

A **sentence** is a list of words that are separated by a **single**
space with no leading or trailing spaces.

- For example, `"Hello World"`, `"HELLO"`, `"hello world hello world"`
  are all sentences.

Words consist of **only** uppercase and lowercase English letters.
Uppercase and lowercase English letters are considered different.

A sentence is **circular** if:

- The last character of each word in the sentence is equal to the first
  character of its next word.
- The last character of the last word is equal to the first character
  of the first word.

Given a string `sentence`, return `true` *if it is circular*.
Otherwise, return `false`.

```
sentence = "leetcode exercises sound delightful"  ->  true
sentence = "eetcode"                              ->  true
sentence = "Leetcode is cool"                     ->  false
```

**Constraints:** `1 <= sentence.length <= 500`; `sentence` consist of
only lowercase and uppercase English letters and spaces; the words in
`sentence` are separated by a single space; there are no leading or
trailing spaces.

Words are split by single spaces, so the last letter of a word and the
first of the next stand on either side of a space, and the wrap from the
last word to the first is the sentence's last letter against its first.
The approaches differ in whether they look at the spaces, the words, or
the letters one at a time.

## Approaches

| file | mechanism |
|---|---|
| `circular.kara` ★ | by the spaces: one pass over the bytes, every space asked for the same letter on both sides, and the first byte compared with the last. O(n) |
| `circular_words.kara` | by words: `split(" ")`, and each word's last letter compared with the first of the word after it, `% m` wrapping the last to the first. O(n) |
| `circular_walk.kara` | by a walk over the letters with no indexing: the letter before a space carried along and compared with the letter after it, and the first letter kept for the end. O(n) |
| `circular_ends.kara` | by two strings: the first letter of every word and the last letter of every word; circular when the firsts, turned round by one with `substring`, spell the lasts. O(n) |
| `circular_iter.kara` | iterators: the words `zip`ped with themselves `cycle().skip(1)`, and `all` pairs asked whether `chars().last()` is the next `chars().next()`. O(n) |
| `circular_solution.kara` | LeetCode's Rust template: a `String` in, `bool` out; `as_bytes()`, every `windows(3)` with a space in the middle asked for equal ends, and the first byte against the last; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's three examples and eight
more, among them one letter, two different letters, the same letter
in another case, and a wrap that fails though every space holds; then
3000 random sentences of 1 to 10 words of 1 to 5 letters from `aAb` and
3000 from all 52 letters, each word begun by the last letter of the one
before half the time, as a count and a checksum of the circular ones;
then the constraints' longest, 500 characters, as one word, as 250
words of one letter, and those with the last changed. `circular.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 20000 random sentences of 1 to 6 words of 1 to 4 letters
from `aAb` against the statement read literally. The two agreed on
every sentence.

`check` first reports 3 errors on the template: `struct Solution;`,
`&&` and `||`. `karac fix` carries it in one call, reporting 5 edits:
`struct Solution {}`; `and` and `or`; `as_bytes()` becomes `bytes()`;
and `windows(3)`, a list of slices in Kāra, gets `.into_iter()` before
`all`. The byte literal `b' '` and the slice indexing stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the words cut out letter by letter, no `split`, and every
word's last letter compared with the next word's first, the last word's
with the first's. It checks 300 random sentences of 1 to 8 words of 1
to 4 letters from `aAb`, then 20 of one word, and 40 of 20 to 60 words
of 1 to 5 letters from all 52; each word is begun by the last letter of
the one before three times in four, and the last word ended by the
first letter of the first half the time, so that 125 of the 360 are
circular. The longest is 266 characters. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the sentence read backwards: the same answer |
| P3 | the first word moved to the end: the same answer |
| P4 | the sentence twice, joined by a space: the same answer |
| P5 | a word of the first word's last letter twice put after it: the same answer |
| P6 | each arm agrees with at least three of the other five |

The four are the pairs of letters seen another way. Read backwards,
every word is reversed and so is their order, so each pair of letters
across a space is the same pair turned round, and the wrap too. Moving
the first word to the end or doubling the sentence keeps the same set of
pairs across spaces and wraps, only met in another order or twice. The
word put in for P5 matches the first word's last letter on its left,
and offers that same letter to the second word on its right, so the
one pair it breaks is the one it copies.

The differential prints `360 cases, 125 circular: checksum 783350069,
12960 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python
reading that builds the same cases and adds up the same sums. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the ends never compared | P1 54, P3 60, P4 54, P6 54 |
| M3 | ★: the first place never checked | P1 10, P2 11, P3 16, P4 10, P5 10, P6 10 |
| M6 | ★: case ignored at a space | P1 32, P3 23, P6 32 |
| M8 | words: first letters compared | P1 92, P2 29, P5 2, P6 92 |
| M9 | words: last letters compared | P1 105, P2 29, P6 105 |
| M11 | words: the first word skipped | P1 40, P2 38, P3 46, P4 40, P5 23, P6 40 |
| M13 | walk: an equal letter taken as the break | P1 95, P3 16, P4 42, P5 6, P6 95 |
| M15 | walk: the check made after an a | P1 96, P2 8, P3 24, P4 2, P5 2, P6 96 |
| M16 | walk: a space never carried as the last | P1 125, P3 118, P6 125 |
| M18 | ends: the firsts turned the other way | P1 62, P5 6, P6 62 |
| M19 | ends: each word ended at its second letter | P1 93, P2 41, P5 1, P6 93 |
| M21 | ends: only the first pair compared | P1 147, P2 88, P3 100, P5 71, P6 147 |
| M22 | iter: each word against itself | P1 69, P6 69 |
| M23 | iter: any pair enough | P1 215, P5 3, P6 215 |
| M25 | iter: each word against the one two on | P1 68, P5 1, P6 68 |
| M28 | solution: every window asked for a space | P1 103, P4 22, P6 103 |
| M31 | solution: the first compared with the middle | P1 96, P2 42, P3 49, P4 67, P5 43, P6 96 |

P1 and P6 kill all seventeen, P5 eleven, P3 nine, P2 eight, and P4
seven.

Fourteen are not kept, and none survives. Ten fail exactly as a kept
one: the words and iter arms' no wrap to the first word and the walk
and template arms' ends never compared (M7, M26, M12, M27) as the ★
arm's ends never compared (M1), since the wrap from the last word to
the first is the same pair as the sentence's last letter and its first;
the ★ arm's equal letters taken as the break (M4) as the walk arm's
(M13); the words arm's each word against the one before and the iter
arm's first against last (M10, M24) as the ends arm's firsts turned the
other way (M18), each comparing the pairs the wrong way round; the ends
arm's firsts never turned (M17) as the iter arm's each word against
itself (M22); and the ends arm's lasts taken as the firsts (M20) as the
words arm's last letters compared (M9). The ★ arm's letter before
compared with the space, the walk arm's space itself carried and the
template's letter before compared with the space (M5, M14, M29) fail as
one another, each answering false at every space, and their arms
already hold their kept edits. The ★ arm's last space never checked
(M2) and the template's space looked for first in the window (M30) fail
in ways of their own; the ★ arm's is seen by P1 on one case only, so
its place went to M1.

## Verification

Every arm prints the same output as `circular.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.9 to 1.3 s and the differential 1.0 s; under `karac __mir-llvm-asan` the arms take 0.5 to 0.6 s and the differential 0.7 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 200 circular sentences of about 500 letters, within
the constraints, once from its own generator, then makes 2300 passes;
each changes one letter of every sentence, the place and the new letter
chosen by the checksum so far, asks, and changes it back, so most
answers walk the whole sentence and a change at a word's end breaks it.
The answer, as 1 or 2, plus the pass is folded into the checksum. The
bench uses the ★ arm in all five languages, each sentence kept as a list
of letters and joined into a fresh string for every answer; C copies it
into one buffer. Every implementation prints `2300 passes over 200
sentences: 307740 circular, checksum 106768641`.

BENCHTAB
