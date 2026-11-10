# 2063. Vowels of All Substrings

Given a string `word`, return the sum of the number of vowels (`'a'`,
`'e'`, `'i'`, `'o'`, and `'u'`) in every substring of `word`.

A substring is a contiguous (non-empty) sequence of characters within a
string.

**Note:** Due to the large constraints, the answer may not fit in a signed
32-bit integer. Please be careful during the calculations.

```
word = "aba"   ->  6    ("a" 1, "ab" 1, "aba" 2, "b" 0, "ba" 1, "a" 1)
word = "abc"   ->  3
word = "ltcd"  ->  0
```

**Constraints:** `1 <= word.length <= 10^5`; `word` consists of
lowercase English letters.

There are about `n² / 2` substrings, too many to visit, but a letter at
place `i` lies in exactly `(i + 1) · (n - i)` of them: it is counted that
many times, and the answer is the sum over the vowels, O(n). It is at
most `n (n + 1) (n + 2) / 6`, about `1.7 · 10^14` for `n = 10^5`, so it
needs 64 bits. The approaches differ in how they arrive at that sum.

## Approaches

| file | mechanism |
|---|---|
| `vowels.kara` ★ | each vowel's count of substrings, `(i + 1) · (n - i)`, summed over `chars().enumerate()`; a vowel test `"aeiou".contains(c.to_string())`. O(n) |
| `vowels_ending.kara` | by where substrings end: the vowels in all substrings ending at `i` are those ending at `i - 1`, each grown by a letter, plus `i + 1` if letter `i` is a vowel; a running count over `bytes()`, summed. O(n) |
| `vowels_prefix.kara` | from prefix counts: `before[k]` vowels in the first `k` letters, built by `scan` with Kāra's state-returning closure, and the sum over all `i < j` of `before[j] - before[i]` folded to `Σ (k - (n - k)) · before[k]`. O(n) |
| `vowels_halves.kara` | divide and conquer over a `Slice[char]`: the substrings of each half, plus those crossing the middle, where a vowel in the left half lies in `(i - l + 1) · (r - m)` of them and one in the right in `(m - l) · (r - j)`. O(n log n) |
| `vowels_each.kara` | one vowel at a time: the places of each of the five found with `match_indices`, mapped to their counts and summed, and the five sums summed, all in one iterator chain. O(5 n) |
| `vowels_solution.kara` | LeetCode's Rust template (`word.chars().enumerate()`, a `filter` on `"aeiou".contains(*c)`, `i as i64` from a `usize`, `.sum()`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and five
more, each word and its answer; then a checksum of the answers for 500
random words of 1 to 300 letters, each a vowel with a chance of 0 to 100
in 100 and else one of `bcdxyz`; then the answers for the largest words
the constraints allow, 100000 vowels and 100000 letters of which about
40 in 100 are vowels. `vowels.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every substring taken out whole and its vowels counted one by
one, O(n³). It checks 300 random words of 1 to 40 letters, drawn as the
harness draws them, then 20 of vowels only, 20 with none and 20 of 41 to
120 letters. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the word reversed has the same answer |
| P3 | a consonant added at the end adds `i + 1` for each vowel at `i` |
| P4 | every vowel made `a` and every consonant `z` leave the answer |
| P5 | a consonant made a vowel raises the answer, and no answer passes `n (n + 1) (n + 2) / 6` |
| P6 | each arm agrees with at least three of the other five |

P3 holds because the substrings the new letter adds are the word's `n +
1` suffixes with it on the end, and a vowel at `i` is in `i + 1` of them.

The differential prints `360 words: checksum 354744556, 12960 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of the
literal answers was checked against a Python reading of the same words.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, four to six to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones and the
survivor under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed, fails
the same way under both backends and not by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each vowel's ends one short | P1 312, P2 250, P5 27, P6 312 |
| M2 | ★: `u` not a vowel | P1 248, P3 248, P4 248, P6 248 |
| M3 | ★: the first letter skipped | P1 196, P2 120, P3 196, P5 27, P6 196 |
| M4 | ending: a vowel adding one substring fewer | P1 312, P2 250, P3 312, P5 27, P6 312 |
| M5 | ending: the running count cleared at a consonant | P1 254, P2 253, P3 312, P6 254 |
| M6 | ending: only a vowel's end adding up | P1 254, P2 250, P3 312, P6 254 |
| M7 | prefix: each prefix taken away one time too few | P1 312, P2 250, P3 312, P5 76, P6 312 |
| M8 | prefix: the count started afresh at each letter | P1 309, P2 250, P3 312, P5 145, P6 309 |
| M9 | prefix: the whole word's prefix left out | P1 312, P3 312, P5 51, P6 312 |
| M10 | halves: a left vowel's crossing starts one short | P1 309, P2 250, P3 312, P6 309 |
| M11 | halves: a right vowel's crossing ends one short | P1 303, P2 250, P6 303 |
| M12 | halves: a lone consonant counted | P1 306, P3 360, P5 3, P6 306 |
| M13 | each: each place's ends one too many | P1 312, P2 250, P5 75, P6 312 |
| M14 | each: `a` counted twice | P1 238, P3 238, P4 310, P5 80, P6 238 |
| M15 | each: only each vowel's first place | P1 253, P2 240, P3 253, P4 291, P5 180, P6 253 |
| M16 | solution: the adapter's word in capitals | P1 312, P3 312, P5 306, P6 312 |
| M17 | solution: the consonants counted | P1 353, P3 357, P5 306, P6 353 |

P1 and P6 kill all seventeen, P3 fourteen, P5 twelve, P2 eleven and P4
three. 312 of the 360 words hold a vowel, so `P1 312` is an arm wrong
on every one of them. P2 sees an edit that weighs a vowel's starts and
ends unevenly (M1, M4, M13); P3, which grows the word by a letter, one
that miscounts the substrings a new end adds; P4 an edit that tells one
vowel from another (M2, M14, M15), which no correct arm does; P5 an
answer that does not rise when a vowel is added, or passes the most any
word of its length can hold.

Of the thirty-one, fourteen were not kept. One survives, and it is
equivalent: the Rust arm's adapter handing it the word reversed, which
has the same answer (P2). Eight fail as a kept one: the ★ and Rust arms'
starts one short as M4, and their length one short as M1; the ending,
halves and each arms' `u` not a vowel as M2; the ending arm's first
letter skipped as M3. Five are killed with checks of their own but were
left out because their arm keeps three: the prefix arm's every letter a
vowel (P1 306, P3 360, P5 306) and count started at one (P1 360, P3 360,
P5 54); the halves arm's lone vowel counted twice (P1 312, P5 54) and a
left half's first letter never crossing (P1 302, P2 223, P3 291); and
the each arm's places ending anywhere (P1 303, P2 250, P5 214).

## Verification

Every arm prints the same output as `vowels.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 1.2 s to 3.4 s (the halves arm
the slowest) and the differential 10.7 s, timed while other work shared
the machine.

No arm met a compiler gap. The prefix arm was written first with Rust's
`scan`, whose closure writes its state in place (`*seen += 1; Some(*seen)`);
Kāra's `scan` closure takes the state by value and returns the next state
with the item, and the checker refused the Rust form saying exactly that.
The arm returns `Some((seen, seen))`. The ★ arm's vowel test is written in
the form the char-pattern fix gives (kata 2062), and costs it the
allocation Benchmarks shows.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds of 2, 4 and 1 edits: `struct Solution;` to `struct
Solution {}` and `Solution::` to `Solution.`; then the `*` of `*c`
dropped (a char is copied) and three `as i64` casts from a length and
places that are already `i64`; then `c.to_string()` for the char
pattern. The fixed arm reads as the template does.

## Benchmarks

The bench cuts 200 windows of 100000 letters from one text of 140000,
each letter a vowel with a chance of 40 in 100, and answers each with
the ★ arm in all five languages, the window copied out first. Every
implementation prints `200 windows: checksum 12096485`.

The ★ arm's vowel test, `"aeiou".contains(c.to_string())`, allocates a
`String` for every letter; with a `match` on the letter the Kāra build
is about 5.8 times faster (B-2026-11-10-25).

BENCHTAB
