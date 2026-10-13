# 472. Concatenated Words

Given an array of strings `words` (without duplicates), return all the
concatenated words in the given list of `words`.

A concatenated word is defined as a string that is comprised entirely
of at least two shorter words (not necessarily distinct) in the given
array.

```
words = ["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"]
    ->  ["catsdogcats","dogcatsdog","ratcatdogcat"]
words = ["cat","dog","catdog"]  ->  ["catdog"]
```

**Constraints:** `1 <= words.length <= 10^4`; `1 <= words[i].length <=
30`; `words[i]` consists of only lowercase English letters; all the
strings of `words` are unique; `1 <= sum(words[i].length) <= 10^5`.

## Approaches

Every arm is `fn find_all_concatenated_words_in_a_dict(words:
Vec[String]) -> Vec[String]`, and borrows the list. The answer may come
in any order, so the harness sorts it.

| file | mechanism |
|---|---|
| `concatenated_words.kara` ★ | the words from shortest to longest, each broken (word break: which prefixes are made of set words) against a set of the words before it, then added to it; the word itself is never in the set when tested, so a break has at least two pieces. O(total length × longest word) set lookups |
| `concatenated_words_trie.kara` | every word in a trie; from each position, walk the trie along the word and go on from every word that ends, remembering the positions from which the rest cannot be finished; a single piece reaching the end counts only when it did not start at 0 |
| `concatenated_words_count.kara` | every word in one set, the word itself included, and for each prefix the most set words it can be cut into; the word is concatenated when that is at least 2 |
| `concatenated_words_suffix.kara` | some proper prefix is a word and the rest is made of words; whether a string is made of words does not depend on which word it came from, so the answers are kept in one map keyed by the string and shared by all the words |
| `differential.kara` | the four arms on 1,500 random lists, five properties |

Every arm prints the same 8 lines: the two LeetCode examples, `a` to
`aaaa` (a word used more than once), a list where `ab`, `ba`, `aba` and
`abab` all are and `c` is not, one word, `xyz` (two ways, `xy`+`z` and
`x`+`yz`), `abcd` (with `abc` there but no `d`), and for 300 random
lists over 1, 2 or 3 letters (2 to 12 short words, then up to 30 tries
at two to four of the words so far put together, a quarter of them
with one more letter, each kept when new and at most 30 letters) the
number of words, how many are concatenated, and a checksum of the
sorted answers. `concatenated_words.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random lists built as in the harness, with 2 to 8 short words and
up to 15 tries at joined ones. Each arm's answer is sorted.

| | property |
|---|---|
| P1 | among the words of up to 8 letters, the arm finds exactly those that some set of cuts splits into list words, every one of the 2^(n-1) - 1 sets tried |
| P2 | the same words in another order give the same answer |
| P3 | two of the words put together, added when that is a new word of at most 30 letters, add exactly that word to the answer |
| P4 | every word reversed reverses the answer |
| P5 | one concatenated word taken out of the list takes exactly that word out of the answer |

P3 and P5 hold because a piece that is itself concatenated can always
be replaced by its own pieces: adding `a + b` cannot make another word
concatenated that `a` and `b` did not already, and taking a
concatenated word out cannot make another word lose its split.

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, in 17 s, and a count for each property when
anything fails. Each reversed word is bound with its type before it is
pushed, because `karac check` refuses
`v.push(w.chars().rev().collect())` (B-2026-10-12-33). The MIR backends
refused it too when the kata was written (B-2026-10-12-34) and run it
since kara `b9967ff0e0`.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the words are taken longest first | P1 1363, P3 1138 |
| M2 | ★: a piece of one letter is never used | P1 1095, P3 164 |
| M3 | trie: a word that reaches its end in one piece counts | P1 1500 |
| M4 | trie: the search goes on only from the first word that ends | P1 304, P3 373, P4 544 |
| M5 | count: one piece is enough | P1 1500 |
| M6 | count: the first cut found is kept, not the most pieces | P1 1363, P3 1138 |
| M7 | suffix: the rest must be cut again, never be a single word | P1 1363, P3 1138 |
| M8 | suffix: a rest of one letter is never tried | P1 402, P3 13, P4 472, P5 133 |

M1, M6 and M7 find nothing at all (M6 always keeps the whole word, one
piece, which is found first), and fail the same cases: every one with a
concatenated short word, and every P3 that adds one. M3 and M5 find
every word. M4 and M8 are the partial ones: M4 misses a word whose split
needs a longer piece where a shorter word also starts, M8 one whose
split needs a last piece of one letter. P1 looks only at words of up to
8 letters, so P3 and P4, which take all of them, see M4 more often. P2
sees none, since no mutant depends on the input order.

## Verification

All four arms print the same output as `concatenated_words.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

Nothing here runs on the frozen legacy backends. `karac run --interp`
has no `String.as_str`, and LLJIT stops on `as_str` in its code
generator. Legacy `karac build` reads a bare parameter as owned, so it
rejects passing the same word or list to two calls (`value 'word' moved
here, used again here`); on the suffix arm and the differential its
type checker rejects `*known` on what `Map.get` returns. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10000 words once: 1000 of
2 to 5 letters over `a` to `d`, then words joined from 2 or 3 earlier
ones, a quarter of them with an `e` appended so they do not split, none
longer than 30 letters. It then runs the search 10 times. Every
implementation prints `10 rounds on 10000 words: 78220 concatenated,
hash sum 727421579`, the Kāra program under `karac __mir-run` included
(in 13 s).

The legacy `karac build` rejects the bench program (it reads the bare
parameter `word` as owned and moves it, where v2 borrows it), so
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output.

Every mirror sorts by length, keeps the earlier words in a hash set
(the standard one; in C an open-addressing table of its own), and tests
each cut by looking the substring up in it. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.24 to 0.27 s |
| Rust (`rustc -O`) | 0.36 to 0.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.35 to 0.38 s |
| Go | 0.34 to 0.36 s |
| Python | 1.66 to 1.87 s |
| Kāra (`karac build --mir`) | 0.64 to 0.68 s |

The `--mir` row is timed at kara `a9bce361cd`. Under
`karac __mir-llvm-run` the program prints the same line in 5.9 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-3** (MIR, fixed in kara `0e8113c3ec`): a `Slice[T]`'s
  `iter()` drove a `for` loop on the MIR backends but no adaptor or
  terminal. `word.bytes().iter().collect()`, `.count()`, `.position(..)`
  and `v[0..3].iter().map(..).sum()` stopped with "an iterator value is
  not lowered yet", and a closure written with the spec's `*b` was
  refused before that ("found 'u8'"), while `karac check` accepted every
  form. `karac check` itself recommends `word.bytes().iter().collect()`
  when given `word.bytes().collect()`, which is how the trie arm met it.
  The row was measured on a build from before the fix and filed after
  the fix had already reached `main`; every form runs on both MIR
  backends now. The arm keeps `word.bytes().to_vec()`, which the spec
  also lists for `Slice[T]`.
- B-2026-10-12-33 (open) and B-2026-10-12-34 (fixed in kara
  `b9967ff0e0`), see Differential.
