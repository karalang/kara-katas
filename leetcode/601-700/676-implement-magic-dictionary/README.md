# 676. Implement Magic Dictionary

Design a dictionary that is built from a list of distinct words, and
answers whether a search word can be turned into one of them by changing
exactly one letter.

```
buildDict(["hello", "leetcode"])
search("hello")     -> false   (in the dictionary, but none changed)
search("hhllo")     -> true    (change the second h to e)
search("hell")      -> false
search("leetcoded") -> false
```

**Constraints:** at most 100 words of 1 to 100 lowercase letters, all
distinct; search words of 1 to 100 lowercase letters; at most
100 searches.

## Approaches

Every arm is a `struct MagicDictionary` with `new()`, `build_dict(mut
ref self, dictionary: Vec[String])` and `search(ref self, search_word:
String) -> bool`.

| file | mechanism |
|---|---|
| `magic_dictionary.kara` ★ | the words as given; a search compares every word of its length a byte at a time and wants exactly one difference; O(total length) a search |
| `magic_dictionary_patterns.kara` | a `Map` counting each word's patterns with one place replaced by `*`, and a `Set` of the words, since a word in the dictionary matches its own patterns and so needs a count of two; O(length^2) a search |
| `magic_dictionary_trie.kara` | a trie walked down the search word, free to step down one other branch once; O(26 * length^2) a search at worst |
| `magic_dictionary_candidates.kara` | the words sorted; every word one letter away from the search word made and looked up by binary search; O(25 * length * (length + log n)) a search |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 7 lines: the LeetCode example; four small
dictionaries: one word of one letter, two words that are each other's
neighbours, two words searched for themselves and their neighbours, and
three words, one far from the rest; a word of 100 letters, the problem's
longest, searched with each end changed, unchanged and lengthened; and a
checksum of 6,000 searches of 300 random dictionaries, with how many
were found. The first six are printed as LeetCode prints the calls'
results. `magic_dictionary.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
some other dictionary word becomes the search word when one of its
places takes the search word's letter there, which compares strings
whole rather than counting differences. 500 random dictionaries of up to
30 words, of 1 to 6 letters over an alphabet of 2 to 4, are each
searched 20 times, every search held to the definition.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | a dictionary word with one letter changed is found |
| P3 | a word longer than every dictionary word is not |
| P4 | adding words to the dictionary never turns a found word into a missing one |
| P5 | reversing every word, in the dictionary and searched for, leaves each answer |

It prints `500 dictionaries, 10000 searches (6537 found), 4 arms,
124000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search word itself counted as a match | P1 520 |
| M2 | ★: only places where the word's letter is larger counted | P1 3458, P2 298 |
| M3 | patterns: a word in the dictionary needs one pattern match | P1 520 |
| M4 | patterns: every pattern counted once | P1 3987, P2 19, P4 764 |
| M5 | trie: a word reached without the change spent | P1 520 |
| M6 | trie: any number of changes allowed | P1 2244 |
| M7 | candidates: any place the search lands counted as found | P1 3327, P3 491, P5 44 |
| M8 | candidates: only the search word's own letter tried | P1 3070, P2 481 |
| E1 | ★: a word equal to the search word skipped | 0 |
| E2 | patterns: the wildcard written as `#` | 0 |
| E3 | trie: the change tested against the letter again | 0 |
| E4 | candidates: the midpoint taken as lo + (hi - lo) / 2 | 0 |

P1 kills all eight. M1, M3 and M5 make the same mistake three ways,
letting a search word that is in the dictionary match itself, and each
fails the same 520 searches, which only P1 sees: every other property
holds for a dictionary that also finds its own words. M2 and M8 miss
real neighbours, so P2 sees them as well; M4 forgets that patterns can
be shared, so adding words can lose a match and P4 sees it; M7 reports
any word that sorts inside the dictionary as found, so P3 sees it. The
four survivors cannot change an answer: a word equal to the search word
has no differences, so skipping it changes nothing; any character that
is not a letter serves as the wildcard; the trie's other branches
already differ from the letter; and the two midpoints are equal for
numbers this small.

## Verification

Every arm prints the same output as `magic_dictionary.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `85dccd703c` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends print the same output for every arm under the
interpreter, the JIT and `karac build`, with and without
`KARAC_AUTO_PAR=1`, and run the differential to the same line under the
interpreter, the JIT and `karac build`; `karac build` warns that
`dictionary` is moved and used again in the differential, and builds
anyway.

## Benchmarks

The bench program uses the ★ arm. It builds 1,000 dictionaries of
100 words, the problem's most, each of 50 letters over `a` and `b` from
the same generator in every language, and searches each 100 times, the
problem's most: every other search a dictionary word with one letter
changed, the rest a random word, which is never found. Each answer goes
into a checksum. Every implementation prints `1000 dictionaries of
100 words, 100000 searches, 50000 found: checksum 593838326`, the Kāra
program under `karac __mir-run` included (in 296 s).

Each implementation is the same comparison of bytes, counting every
difference, so this measures that inner loop. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.26 to 0.33 s |
| Rust (`rustc -O`) | 0.12 to 0.18 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.10 to 2.16 s |
| Go | 0.34 to 0.41 s |
| Python | 20.7 to 21.0 s |
| Kāra (`karac build --mir`) | 2.16 to 2.21 s |
| Kāra, legacy (`karac build`) | 2.35 to 2.48 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 5.3 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy and with Rust under
`overflow-checks=on`, and about eight times C and fifteen times plain
Rust. The unchecked loops count the differences without a branch that
can fail, which leaves them free to be vectorized; the checked count of
differences costs that, which is the equal-safety tie BENCHMARKS.md
describes. That is inferred from the checked Rust row, not profiled. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
