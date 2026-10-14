# 616. Add Bold Tag in String

Given a string `s` and a list of words, wrap every part of `s` that some
word occurs over in `<b>` and `</b>`. Occurrences that overlap or touch
share one pair of tags.

```
s = "abcxyz123", words = ["abc", "123"]  ->  "<b>abc</b>xyz<b>123</b>"
s = "aaabbb",    words = ["aa", "b"]     ->  "<b>aaabbb</b>"
```

**Constraints:** `s` of 1 to 1,000 characters; 0 to 100 words, all
different, of 1 to 1,000 characters each; letters and digits only.

## Approaches

Every arm is `fn add_bold_tag(s: Str, words: Vec[String]) -> String`.

| file | mechanism |
|---|---|
| `add_bold_tag.kara` ★ | mark every character an occurrence covers, trying each word at each position with `starts_with`, then write `s` out with a `<b>` where a marked run starts and a `</b>` where it ends; O(n * total length of the words) |
| `add_bold_tag_merge.kara` | every occurrence as an interval, found by comparing slices, the intervals sorted and each merged into the one before when it overlaps or touches it, then `s` copied out between and inside the merged intervals; O(n * total length + m log m) for m occurrences |
| `add_bold_tag_reach.kara` | one walk keeping the farthest position any occurrence started so far reaches, a character bold when that reach is past it, then `s` copied out a run at a time, each bold run whole in an f-string; O(n * total length) |
| `add_bold_tag_trie.kara` | the words in a trie of `Map[char, i64]` nodes, walked from each position as far as the characters allow, marking up to the longest word that ends on the way, then `s` written a character at a time; O(n * the longest word) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 13 lines: the two LeetCode examples; nine more
(no words, a word longer than the string, occurrences that touch, that
overlap and that cover everything, a word that never occurs, one
occurrence inside another, a single character, and letters with digits);
a total length, count of bold runs and checksum over 300 random strings
of 1 to 30 characters with up to five words each; and the same for a
string of 1,000 characters with 100 words of 5 to 14 characters, half of
them cut from the string. `add_bold_tag.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition: a
character is bold when an occurrence of some word covers it, every
occurrence found by comparing the word with `s` a character at a time at
every start, and then a `<b>` goes before every bold character whose
left neighbour is not bold and a `</b>` after every one whose right
neighbour is not. Each of 1,000 random cases is a string of 1 to
12 characters from a and b or from a to c, with 0 to 5 different words
of 1 to 4 characters from the same letters.

| | property |
|---|---|
| P1 | the string is the definition's |
| P2 | with its tags taken out, it is `s` |
| P3 | the tags alternate, opening first and closing last, with no `<b></b>` and no `</b><b>` |
| P4 | the words in reverse order, with a word added that cannot occur, give the same string |
| P5 | with `s` itself added as a word, the answer is all of `s` in one pair of tags |

It prints `1000 cases (600 with bold), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each occurrence's last character left unmarked | P1 600, P5 1000 |
| M2 | ★: a `<b>` before every bold character | P1 499, P3 499, P5 926 |
| M3 | merge: touching intervals kept apart | P1 302, P3 302 |
| M4 | merge: an interval inside the last one cuts it short | P1 39, P5 357 |
| M5 | reach: a character bold when the reach only gets to it | P1 871 |
| M6 | reach: the reach set by the last word found, not the farthest | P1 67, P4 70, P5 373 |
| M7 | trie: every node on the way taken as a word's end | P1 555 |
| M8 | trie: a run reaching the end left open | P1 327, P3 327, P5 1000 |
| E1 | ★: the last position tested as `i + 1 == n` | 0 |
| E2 | merge: the intervals sorted by start alone | 0 |
| E3 | reach: the reach also set when it stays the same | 0 |
| E4 | trie: the longest kept only when it grows | 0 |

P5 kills the mutants that go wrong on a long occurrence that covers
everything. M1 leaves the last character of `s` outside the tags, and
M8 never closes a run that reaches the end of `s`, so both fail it on
every case; M4 and M6 fail it whenever a shorter occurrence inside `s`
comes after the whole one in their order and cuts the run short. P3 sees
the mutants that write the tags wrong: M2's extra openings, M3's
`</b><b>` between touching runs, and M8's missing close, each on exactly
the cases where P1 sees them. M6's answer depends on the order the words
are tried, which P4 reverses. M5 and M7 only bold the wrong characters,
with well-formed tags and the whole string still bold under P5, so only
the definition sees them. P2 kills nothing: no mutant changes the
characters between the tags.

## Verification

Every arm prints the same output as `add_bold_tag.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. All at kara
`ea2a2da2be`.

The frozen legacy backends run the ★, reach and trie arms right under
`karac run --interp` only; `karac run` and `karac build` stop in codegen
at the arm's `s.len()` ("no handler for method 'len' on variable 's'"),
which has no lowering for a `Str` parameter. They refuse the merge arm
and the differential at type checking: legacy types the items of a
`Vec`'s `iter()` by value, so the `*span` that copies one is an error.
Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 cases, each a string of
1,000 characters from a to d with 100 words of 5 to 14 characters, half
cut from the string and half made at random, once; then 1,000 times
writes one of them out, picked by the round, adding up the lengths and
putting every character into a checksum. Every implementation prints
`20 cases, 1000 rounds: 1249900 characters, checksum 56784368`, the Kāra
program under `karac __mir-run` included (in 240 s).

Each implementation marks the characters in an array of flags, tests
each word at each position as the ★ arm's `s[i..n].starts_with(word)`
does, and appends to one growing string: Rust with `starts_with` on a
`str` slice and a `String`, Go with `strings.HasPrefix` and a
`strings.Builder`, C with `strncmp` and a buffer that doubles, the
words' lengths taken once a call, and Python with `startswith(word, i)`
and a list of parts joined at the end. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.47 to 0.49 s |
| Rust (`rustc -O`) | 0.33 to 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.30 to 0.32 s |
| Go | 0.44 to 0.57 s |
| Python | 7.1 to 7.6 s |
| Kāra (`karac build --mir`) | 2.44 to 2.57 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses it at the
`texts[c]` it passes by value ("cannot move out of an index
expression"); that edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
10.6 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

The Kāra row is about seven times Rust's. In callgrind profiles at
50 rounds the v2 program runs 777 million instructions to Rust's
187 million, against 6.7 and 3.2 million at 0 rounds. Both spend
110 million in glibc's `memcmp`. The v2 program spends the rest in
`main` (187 million), the runtime's `karac_mir_str_test` (170 million)
and `karac_mir_str_view` (152 million), and an unnamed function in the
runtime's code (152 million), across the 5 million word tests; Rust's
tests are inlined into its `main`. That the slice and the `starts_with`
are the two named calls is read from their names; it is not measured by
changing the program. Heap use is no part of the gap: 550 allocations at
50 rounds to Rust's 500.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
