# 824. Goat Latin

Given a sentence of words separated by single spaces, each word made of
English letters, return its Goat Latin. A word that begins with a vowel
(`a`, `e`, `i`, `o` or `u`, in either case) gets `"ma"` appended; a word
that begins with a consonant has its first letter moved to the end and
then gets `"ma"`. Each word then gets one `'a'` for its place in the
sentence: one for the first word, two for the second, and so on.

```
"I speak Goat Latin"  ->  "Imaa peaksmaaa oatGmaaaa atinLmaaaaa"
"The quick brown fox jumped over the lazy dog"
    ->  "heTmaa uickqmaaa rownbmaaaa oxfmaaaaa umpedjmaaaaaa overmaaaaaaa
         hetmaaaaaaaa azylmaaaaaaaaa ogdmaaaaaaaaaa"
```

**Constraints:** `1 <= sentence.length <= 150`, the sentence holds only
English letters and spaces, has no leading or trailing space, and its
words are separated by single spaces.

## Approaches

Each word is rewritten on its own, and the only thing a word needs from
the ones before it is how many there were. A sentence of w words gains
`2w + w(w + 1)/2` characters, so every arm is O(n + w^2) for n
characters, the size of its own answer.

| file | mechanism |
|---|---|
| `goat_latin.kara` ★ | `split(" ")` into words, each written into one growing `String`, with the run of `'a'`s kept in a second `String` that grows by one letter per word |
| `goat_latin_scan.kara` | one pass over the `chars()` with no split: a space closes a word, and a first consonant is held in an `Option[char]` and written when its word closes, followed by `"ma"` and the `'a'`s counted out |
| `goat_latin_join.kara` | each word rewritten into its own `String`, a vowel found by `starts_with` on the word's `to_lowercase()`, and the words `join`ed with single spaces at the end |
| `goat_latin_iter.kara` | `split`, `enumerate` and `map` rewriting each word with `f"..."` strings, the `'a'`s a `collect` of a range, and the words collected and `join`ed |
| `differential.kara` | the four arms against the statement read letter by letter, four properties |

Every arm prints the same 10 lines: LeetCode's two examples; six small
cases (one vowel; one consonant; two capitals; a sentence of words of
every kind; three words of repeated letters; and five capital vowels);
LeetCode's largest, 150 characters at most, as 75 one-letter words of
149 characters, which grow to 3,149; and 300 random sentences of up to
12 words of up to 8 letters drawn from vowels and consonants of both
cases, with the total length of the answers and a checksum of their
bytes. `goat_latin.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the sentence collected into characters, a word the run of
characters up to the next space, a vowel one of ten listed letters, and
the `'a'`s counted out from the word's place. Its 1,600 sentences have
up to 15 words and come in four kinds of 400: words of up to 9 letters
of either case; of vowels only; of consonants only; and of one or two
letters, so that most words are their first letter alone.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the answer has one space fewer than it has words, as the sentence does |
| P3 | the answer is `2w + w(w + 1)/2` characters longer than the sentence, for w words |
| P4 | the answer to the sentence with more words appended begins with this answer and a space |

It prints `1600 cases, 25600 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: uppercase vowels taken as consonants | P1 609 |
| M2 | ★: no `'a'`s after `"ma"` | P1 1600, P3 1600 |
| M3 | ★: a consonant dropped, not moved | P1 1192, P3 1192 |
| M4 | scan: the count of `'a'`s not grown for the last word | P1 1600, P3 1600, P4 1600 |
| M5 | scan: a held consonant lost | P1 1192, P3 1192 |
| M6 | scan: `'u'` taken as a consonant | P1 273 |
| M7 | join: uppercase vowels taken as consonants | P1 609 |
| M8 | join: one `'a'` short | P1 1600, P3 1600 |
| M9 | join: words joined with no space | P1 1495, P2 1495, P3 1495, P4 1600 |
| M10 | iter: one `'a'` short | P1 1600, P3 1600 |
| M11 | iter: the first letter kept as well as moved | P1 1192, P3 1192 |
| M12 | iter: `"ma"` written as `"m"` | P1 1600, P3 1600 |

P1 kills all twelve. The same mistake in two arms fails on the same
number of cases: uppercase vowels in M1 and M7 (609), and a consonant
lost or doubled in M3, M5 and M11 (1,192, every sentence with a word
that begins with a consonant). An edit that moves a letter without
changing the count, M1, M6 and M7, is seen by P1 alone. P2 sees only M9,
and fails on the 1,495 sentences with more than one word. P4 sees M4,
whose last word is one `'a'` short but stops being last once more words
follow, and M9, whose appended words carry no space.

## Verification

Every arm prints the same output as `goat_latin.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release build
that runs `check` and `__mir-run` and the debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` are both at kara
`36a43d8e50`, with the runtime archives built from that tree.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backend runs none of the four arms. Its interpreter
has no `as_str` on a `String`, which every harness calls; its compiled
backend has no `as_str` either (★ arm), no dispatch for `split` on a
`Str` parameter (join arm) and panics in `control_flow_for.rs` on the
`for` over the parameter's `chars()` (scan arm); and its checker wants
an `.iter()` between `split` and `enumerate` (iterator arm and the
differential). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
sentences once, each of words of 1 to 9 random letters of either case
added while the sentence stays within 150 characters, LeetCode's
largest. Each of 2,000,000 rounds answers the next sentence afresh and
reads one byte of the answer. Every implementation prints `2000000
rounds of 64 sentences: total 1040281250, checksum 353256567`, the Kāra
program under `karac __mir-run` included, in 516 s with the
interpreter's step limit raised by `KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, 13 runs of C, Go and Rust
with overflow checks, 5 of plain Rust and 18 of v2, ten of them in two
interleaved sets, and three of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.11 to 1.37 s |
| Rust (`rustc -O`) | 2.02 to 2.12 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.01 to 2.29 s |
| Go | 3.49 to 3.80 s |
| Python | 12.9 to 13.3 s |
| Kāra (`karac build --mir`) | 5.05 to 5.96 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the second interleaved set v2 takes 5.33 s, against
C's 1.24, Rust's 2.08 (2.17 under overflow checks) and Go's 3.52: 4.3
times C's time and 2.5 times Rust's under overflow checks. Under
valgrind's cachegrind v2 runs 57.1 billion instructions, against Rust's
19.1 billion and C's 12.2 billion. Callgrind on a copy with 100,000
rounds puts about 43% of v2's instructions in `is_vowel`: the ★ arm
writes `"aeiouAEIOU".contains(c.to_string().as_str())`, since a string
search takes a `Str` pattern (kara B-2026-10-20-22), so every word
builds a one-letter `String` through the formatter and searches for it.
The search (`karac_mir_str_find`) takes 23.7% counting what it calls,
and the formatter's `karac_mir_fmt_end_string`, `karac_mir_fmt_char` and
`karac_mir_fmt_begin` 11.5%, 6.1% and 2.1%; each is called once per
word, 2.48 million times in the copy, so `split` is not among the
search's callers. C calls `strchr` on the byte and Rust's `contains`
takes the `char`. The scan arm's `match` on the letter avoids it. The
rest of the gap is not traced. Built for `x86-64-v3`, the target `karac
build` uses, C takes 1.27 to 1.35 s and Rust with overflow checks 2.17
to 2.39 s, against v2's 5.24 to 5.79 s in the same five interleaved
runs. Python takes 13 s, about 10 times C's time. The comparison with C
and Rust waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written, and in the first spelling tried.

The bench's largest cost on v2 is the one-letter `String` each word
builds to test for a vowel (Benchmarks). That follows from string
searches taking a `Str` pattern, a ruling rather than a defect
(B-2026-10-20-22, fixed), so it is noted, not filed.
