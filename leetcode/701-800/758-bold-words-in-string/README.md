# 758. Bold Words in String

Given a list of keywords and a string `s`, wrap every part of `s` that
some keyword occurs over in `<b>` and `</b>`, with as few tags as
possible: occurrences that overlap or touch share one pair.

```
words = ["ab", "bc"], s = "aabcd"  ->  "a<b>abc</b>d"
words = ["ab", "cb"], s = "aabcd"  ->  "a<b>ab</b>cd"
```

**Constraints:** `s` of 1 to 500 letters; 0 to 50 words of 1 to
10 letters each; lowercase letters only.

This is kata 616, Add Bold Tag in String, under smaller limits. So that
the same problem tries different parts of the compiler, three of the
arms here use mechanisms 616's arms do not; the reach arm is close to
616's, but looks each slice up in a `Set` where 616 tries each word.

## Approaches

| file | mechanism |
|---|---|
| `bold_words.kara` ★ | for each word, every occurrence by `find` on the rest of `s`, searching again from one past each, marking what it covers; then `s` written out with a tag where a marked run starts and ends; O(words x length of s x longest word) |
| `bold_words_automaton.kara` | an Aho-Corasick automaton: a trie with failure links and completed transitions, each node knowing the longest word ending there; one pass marks, at each character, the longest word ending on it; O(length of s + 26 x total length of the words) |
| `bold_words_hashing.kara` | for each length a word has, a rolling polynomial hash slid over `s`; a window whose hash is a word's is checked against a `Set` of the words before it is marked; O(distinct lengths x length of s) |
| `bold_words_reach.kara` | a `Set` of the words looked up at every position for every length up to the longest word, keeping how far the bold text reaches and writing the tags as the walk enters and leaves it, with no array of marks; O(length of s x longest word) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the two LeetCode examples; no words;
a word that is all of `s`; occurrences that touch; occurrences that
overlap; a word that never occurs; one word occurring twice apart; a
word longer than `s`; and nested occurrences; then 300 random strings of
up to 500 letters from two to six letters with up to 50 words, some of
them with a letter `s` lacks, with the number of bold runs, the tag
characters and a checksum of the answers. `bold_words.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which makes a character bold when some word, at some start at or before
it, matches `s` letter by letter and covers it, and tags the runs.
2,000 random strings are checked, of 1 to 40 letters from two to four,
with up to eight words of one to five letters, so that occurrences
overlap, touch and nest.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the tags taken out leave `s`, and they alternate, with no empty pair and none closing where the next opens |
| P3 | renaming the letters by a random permutation renames the answer's text and bolds the same characters |
| P4 | one more random word never takes a character out of bold |

It prints `2000 strings (4880 bold runs), 4 arms, 32000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each search resumed past the whole occurrence | P1 154 |
| M2 | ★: an occurrence's last character not marked | P1 1525 |
| M3 | ★: no search from the last character | P1 156 |
| M4 | automaton: no word found through a failure link | P1 615, P4 161 |
| M5 | automaton: every failure link to the root | P1 931, P4 273 |
| M6 | automaton: a word's first character not marked | P1 1525 |
| M7 | hashing: the wrong character taken out of the window | P1 1439 |
| M8 | hashing: the leaving character's power one too high | P1 1474 |
| M9 | hashing: a word as long as s skipped | P1 20 |
| M10 | reach: the reach allowed to shrink | P1 176, P4 32 |
| M11 | reach: the longest words never tried | P1 459 |
| M12 | reach: the bold run closed one character late | P1 1272 |
| E1 | ★: one more search, from the end | 0 |
| E2 | automaton: a word as long as the one recorded also recorded | 0 |
| E3 | hashing: every window checked against the words, hash or not | 0 |

P1 kills all twelve. P2 and P3 kill none: every edit still writes
well-formed tags around some set of characters, merging runs that touch,
and treats every letter alike. P4 sees M4, M5 and M10, for which an
added word can cost a character its bold; in the reach arm of M10, for
one, an added word's match ending short of the reach pulls it back.
M9 is seen least, 20 times, since it matters only when a word is as long
as `s` and is all of it. E1 searches once more, from the end of `s`,
where no word, being at least one letter, can occur; E2 records a word
at a trie node that already has one as long, which changes nothing;
E3 drops the hash filter, but each window is then looked up among the
words themselves, which the filter only saves time on.

## Verification

Every arm prints the same output as `bold_words.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a62eacd307`, whose last compiler change is `7d736aae75`. This paragraph
said the runtime archives were built after the last runtime change,
`b09cd37112`; in fact they predated a later one, `176f59738b`, which
changed only the order in which the runtime's merge sort makes its
merges, so it could not change any result here. Every arm and the
differential were checked again at kara `8a2af7d554`, whose last
compiler change is `60d9973e03`, with the archives rebuilt after
`176f59738b`: each prints the same under `karac __mir-llvm-run` and
`karac __mir-llvm-asan` with no error, and the bench program built by
`karac build --mir` prints the same line. The timings below are from the
earlier build.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★, automaton and reach arms and
the bench: each arm prints the same output under the legacy interpreter,
`karac run`, `karac build` and an auto-par build. They refuse the
hashing arm and the differential at a `*` over a set's `iter()` (`let
size = *size;`), which legacy gives by value where v2 gives references.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, on 20,000 random
strings of 500 letters from a to d, each with 50 random words of 1 to
10 letters from a to e, adding up the lengths of the answers and a
checksum. Every implementation prints `20000 strings of 500 letters:
18558585 characters out, checksum 665052978`, the Kāra program under
`karac __mir-run` included (in 72 s). Each finds occurrences with its
library's substring search: C's `strstr`, Rust's and Kāra's `find`, Go's
`strings.Index` and Python's `str.find`.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.39 to 0.43 s |
| Rust (`rustc -O`) | 1.99 to 2.29 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.91 to 2.13 s |
| Go | 0.67 to 0.96 s |
| Python | 10.4 to 10.5 s |
| Kāra (`karac build --mir`) | 2.19 to 2.44 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
7.4 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 2.26 s,
against C's 0.40, Rust's 2.08 (2.04 under overflow checks) and Go's
0.73. Under valgrind's cachegrind v2 runs 13.7 billion instructions,
Rust 10.8 billion and C 2.4 billion; C's `strstr` and Go's
`strings.Index` are presumably faster searches for such short words than
the `find` Rust and Kāra use (inferred, not profiled). The legacy build
of the same program ran 2.20 to 2.31 s, a median of 2.24 s in the
interleaved runs, so v2 is level with legacy, inside M2's limit of twice
legacy; new katas' benches are outside M2's frozen set in any case. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new.
