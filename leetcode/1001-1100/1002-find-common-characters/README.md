# 1002. Find Common Characters

Given a string array `words`, return *an array of all characters that
show up in all strings within the* `words` *(including duplicates)*.
You may return the answer in **any order**.

```
words = ["bella","label","roller"]  ->  ["e","l","l"]
words = ["cool","lock","cook"]      ->  ["c","o"]
```

**Constraints:** `1 <= words.length <= 100`;
`1 <= words[i].length <= 100`; `words[i]` consists of lowercase English
letters.

## Approaches

A letter shows up in every word, duplicates included, as many times as
the word that holds it least, so the answer is each letter that many
times. Three arms count; two match letters themselves, in sorted words
or by striking them out.

| file | mechanism |
|---|---|
| `common_chars.kara` ★ | the least count of each letter: one count of 26 per word and a running least over the words, then each letter that many times, in alphabetical order. O(total length + 26 words) |
| `common_chars_sorted.kara` | sorted words merged: each word's letters sorted, and the answer so far merged with each next word by two places walking up the two lists, a letter kept when both hold it. O(total length × log length) |
| `common_chars_remove.kara` | letters struck out: the answer so far starts as the first word's letters, and against each next word each is looked for among the word's letters not yet struck out; found, it stays and the match is struck out, and not found, it goes. O(words × length²) |
| `common_chars_letters.kara` | letter by letter: for each letter of the alphabet, how many times each word holds it, counted by a filter over the word, and the least of those over the words. O(26 × total length) |
| `common_chars_maps.kara` | maps of counts: the first word counted in a `Map`, each next word in a `Map` of its own, and the answer's map cut down to the letters both hold, each at the smaller count; the answer comes out in the map's own order. O(total length) |
| `differential.kara` | the five arms against the statement read literally, six properties |

The answer may come in any order, and the maps arm's does come in the
map's, which differs from run to run, so the harness and the checks
sort every answer before printing or comparing it. Every arm prints the
same 16 lines. The first ten are LeetCode's two examples and eight
more: one word of one letter; two words with nothing in common; a
letter repeated, as often as the word that holds it least; three
anagrams; the alphabet forwards and backwards; five words of which the
last shares nothing; `mississippi`, `missouri` and `simple`, which
share each of three letters once though `mississippi` holds two of
them four times; and four words that share `e` three times and `l`
once. Then three lists of LeetCode's largest size, 100 words of 100
letters: all `a`; all `a` but the last word, all `b`; and each word
running through the alphabet from a different letter, so each holds
every letter three or four times and they share 78. Then totals over
random lists, each word's letters drawn from the first few letters of
the alphabet, a random number of them for each list: 300 lists of up
to 3 words of up to 5 letters from up to 3, 3,000 of up to 10 words of
up to 20 letters from up to 6, and 300 of up to 100 words of up to 100
letters from up to 26. `common_chars.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: a letter shows up in all strings, duplicates included,
when every word holds it, and its `k`-th time in the first word is in
the answer when every word holds it at least `k` times, each count made
by walking the word. It checks 3,200 random lists, made as the arms'
random lists are: 3,000 of up to 6 words of up to 8 letters from up to
4 against the statement, and 200 of up to 100 words of up to 100
letters from up to 8 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 lists |
| P2 | the words in another order give the same answer |
| P3 | each word's letters in another order give the same answer |
| P4 | a word added that holds the answer, and then the last word's letters up to 100 in all, gives the same answer |
| P5 | the alphabet relabelled by a random permutation relabels the answer |
| P6 | each arm agrees with at least two of the other four |

P4 holds because the answer is in every word already, so a word that
holds it all lowers no letter's least count, and a letter missing from
the answer stays missing from it.

It prints `3200 lists of 20796 words: 6862 common letters, checksum
923940044, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (258.6 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`. Twenty-five came first. Three of the ★ arm's
ran past the interpreter's first limit of 300 seconds, and two letters
edits failed checks a kept one fails, so five more followed, three for
★ and two for letters; at a limit of 900 seconds two of the three
finished, which left ★ its three without the five. Fifteen are kept,
three to each arm, all fifteen are killed, and each fails the same
checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every count starts at 0 | P1 2456, P6 2574 |
| M2 | ★: z never lowered | P1 3000, P5 3076, P6 3200 |
| M3 | ★: the first word skipped | P1 1390, P2 1002, P6 1406 |
| M4 | sorted: a match moves on in one list only | P1 1189, P2 1239, P6 1300 |
| M5 | sorted: the smaller letter skipped on the wrong side | P1 1020, P4 376, P5 711, P6 1092 |
| M6 | sorted: the second word skipped | P1 908, P2 990, P6 923 |
| M7 | remove: the word's last letter taken as a match | P1 1459, P2 1104, P3 808, P6 1624 |
| M8 | remove: a match at the front of the word not kept | P1 1844, P2 259, P3 451, P4 1013, P6 1960 |
| M9 | remove: the front letter struck out, not the match | P1 536, P2 511, P3 613, P6 601 |
| M10 | letters: no z | P5 149 |
| M11 | letters: the most kept, not the least | P1 2491, P4 3031, P6 2689 |
| M12 | letters: the other letters counted | P1 3000, P6 3200 |
| M13 | maps: the larger count kept | P1 1855, P4 2547, P6 1971 |
| M14 | maps: the next word's count kept | P1 1187, P2 1200, P4 2574, P6 1298 |
| M15 | maps: the answer is the last word's counts | P1 2041, P2 1842, P4 3200, P6 2237 |

P1 and P6 kill fourteen, P2 eight, P4 six, P3 three and P5 three. The
checks draw no random number that depends on an answer, so every
mutant sees the same lists and their counts can be compared: 2,456 of
the 3,000 small lists, and 2,574 of all 3,200, share at least one
letter, and M1, whose answer is always empty, fails exactly those.

The random words take their letters from the first few of the
alphabet, never as far as `z`, so M10, which never asks about `z`, is
right on every list as drawn; only P5's relabelling can turn a letter
into `z`, and then M10 misses it, 149 times. M2 leaves `z` at its
starting count of 1,000, so every answer has 1,000 `z`s, and the
relabelled list's answer has them again where it should have the
letter `z` became, unless that was `z` itself; 3,076 of the 3,200
relabellings move it. P5 also sees M5, whose merge skips the wrong
side and so depends on which letters come first in the alphabet.
Shuffling the letters inside each word, P3, sees only the remove arm's
three, which depend on where in a word a letter sits; the other arms
count or sort the letters, which forgets that. Reordering the words,
P2, sees the edits that treat one word unlike the others: the first
(M3), the second (M6) or the last (M15), the next word's count kept
(M14), a match kept for every copy in the answer so far (M4), and the
remove arm's three. P4 adds a word that holds the answer, which leaves
a right answer as it is; it sees the edits whose answer some word does
not hold, so the new word cuts it down, and M15, whose answer becomes
the new word's own. M12 counts each word's other letters, which
relabelling, reordering and shuffling all leave alone, and fails only
P1 and P6.

Fifteen other edits were tried and set aside. Five failed exactly the
same checks as a kept one: remove not striking a match out, as M4, and
skipping the second word, as M6; and letters putting each letter in
once less, maps counting a letter twice the first time it is met and ★
counting every letter twice, which are wrong exactly when the answer
is not empty, as M1. Seven were sound but beyond three an arm: ★
putting each letter in once, keeping at most 3 of a letter and leaving
`a` out; sorted not sorting the words, and never reaching the next
word's last letter; and letters reading the alphabet from `b`, and
keeping at most 2 of a letter. Two survived and are equivalent:
letters asking the first word again, whose count it starts from, which
changes no least; and maps keeping a letter the next word lacks, at a
count of 0, which puts nothing in the answer and stays 0 at every
later word. One timed out in the interpreter only: ★ keeping the most,
not the least, leaves every count at its starting 1,000, so every
answer holds 26,000 letters. `karac __mir-llvm-run` killed it, failing
P1 3000 and P6 3200, but `karac __mir-run` had not finished after 900
seconds, so its two lanes could not be compared. None crashed.

## Verification

Every arm prints the same output as `common_chars.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `af85e1ac8d`, after the
pattern rule of B-2026-10-24-36, which made the harness drop a `*` on
the numbers it reads out of a tuple, and the runtime archives were
rebuilt at the same commit. The mutants' `karac __mir-run` lane ran on
the build before, at `395f71ae05`, whose checks of the differential
are the same; their `karac __mir-llvm-run` lane was run again on the
new build and gave the same verdicts. Under `karac __mir-run` the arms
take 3.5 s (sorted) to 75.9 s (letters, which calls a filter closure
for every letter of every word 26 times), and the differential
258.6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
lists of LeetCode's largest size, 100 words of 100 letters, once, list
`t` taking its letters at random from the first `2 + t % 10` of the
alphabet. In each of 1,000 rounds it runs the arm on every list, each
round starting from a different one, and folds every letter of every
answer into a checksum. Every implementation prints `1000 rounds over
20 lists of 100 words of 100 letters: 955000 common letters, checksum
614647965`. Each call counts 10,000 letters and returns its answer as
LeetCode's list of one-letter strings, one allocation a letter: a
`Vec[String]` in Kāra, a `Vec<String>` in Rust, a `[]string` in Go, a
list of `str` in Python, and in C an array of `malloc`'d strings that
the caller frees.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `af85e1ac8d`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.192 to 0.279 s | 0.217 s |
| Rust (`rustc -O`) | 0.345 to 0.635 s | 0.471 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.404 to 0.641 s | 0.488 s |
| Go | 0.366 to 0.491 s | 0.420 s |
| Python | 21.6 s | |
| Kāra (`karac build --mir`) | 0.480 to 0.851 s | 0.585 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 37 times
Kāra's.

v2 took 1.20 times Rust's median time under overflow checks and 2.70
times C's. Under valgrind's cachegrind v2 ran 6,374 million
instructions and 1,761 million branches with 6.6 million mispredicted,
Rust with overflow checks 5,292 million, 1,289 million and 5.4
million, and C 1,785 million, 239 million and 2.5 million. Over the
200 million letters the calls count that is about 32 instructions and
9 branches a letter for v2, 26 and 6 for Rust, and 9 and 1 for C. v2
and Rust walk each word as characters, decoding UTF-8, and check the
bounds of the count they add to, where C reads bytes and checks
nothing (inferred); where v2's extra instructions over Rust's go was
not traced.
