# 720. Longest Word in Dictionary

Given an array of strings `words` representing an English dictionary,
return the longest word in `words` that can be built one character at a
time by other words in `words`, each step adding one letter to the end
of a previous word. If there is more than one possible answer, return
the longest word with the smallest lexicographical order. If there is no
answer, return the empty string.

```
words = ["w", "wo", "wor", "worl", "world"]                  ->  "world"
words = ["a", "banana", "app", "appl", "ap", "apply", "apple"]  ->  "apple"
```

**Constraints:** 1 <= `words.length` <= 1000; 1 <= `words[i].length` <=
30; lowercase English letters.

## Approaches

A word can be built exactly when every one of its shorter prefixes is in
the dictionary, from its first letter up. Each arm finds those words in
its own way and keeps the longest, and of those the smallest.

| file | mechanism |
|---|---|
| `longest_word_in_dictionary.kara` ★ | the words sorted, so each comes after its own prefixes, and walked once keeping a set of the words that can be built: a word joins when it is one letter long or the word one letter shorter is in the set; the first word of the greatest length is the answer; O(L log n), L the total letters |
| `longest_word_in_dictionary_trie.kara` | a trie of the words with the node where each ends marked, and a depth-first walk from the root that steps only onto marked nodes, children from a to z, a strictly deeper node replacing the best; O(L) |
| `longest_word_in_dictionary_every.kara` | a set of all the words, and every prefix of every word looked up in it, the best kept by comparing as the words come, with no sort; O(L * w), w the longest word |
| `longest_word_in_dictionary_levels.kara` | the words grouped by length and the buildable ones found a length at a time from those one letter shorter, until a length has none; the smallest word of the last length reached is the answer |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 15 lines: the two LeetCode examples; a
one-letter word alone; a word with no first letter in the list, and a
two-letter word without its first letter; three one-letter words; a
two-letter word on the later of two one-letter words; two tied branches
of one tree; two chains where the longer starts later in the alphabet;
two words of the longest length, both listed before their prefix; two
chains of 30 letters, the problem's longest word, one with its 29-letter
link missing; 1,000 words grown from one another from 3 letters and from
26; 1,000 random words of up to 30 letters; and 300 random dictionaries
of up to 40 words with a checksum. `longest_word_in_dictionary.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which has no set, no trie and no sort: a word can be built when each of
its shorter prefixes is found by comparing it with every word in the
list, and of those words it keeps the longest, then the smallest.
3,000 random dictionaries are checked, each of 1 to 12 words from 1 to
3 letters grown from one another, so chains, broken chains and ties are
common; 1,134 of them have no answer.

| | property |
|---|---|
| P1 | the word is the definition's |
| P2 | the words reversed give the same word |
| P3 | every word listed twice gives the same word |
| P4 | the word with one more letter added to the list gives an answer that starts with it |

It prints `3000 dictionaries (1134 with no answer), 4 arms,
48000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

P4 holds because the added word is the only word of its length that can
be built: any other word one letter longer than the answer would have
been buildable already, and longer than the answer. It need not be the
new answer, since a longer word in the list may continue it.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a two-letter word built without its first letter | P1 1029, P4 457 |
| M2 | ★: a later word of the same length taking over | P1 272 |
| M3 | ★: the words reversed instead of sorted | P1 1394, P2 1392, P3 1344, P4 1866 |
| M4 | trie: the walk stepping onto nodes where no word ends | P1 1774, P4 875 |
| M5 | trie: a later node of the same depth taking over | P1 272 |
| M6 | trie: every new node marked as the end of the first word | P1 1774, P4 875 |
| M7 | every: the one-letter prefix never looked up | P1 1029, P4 457 |
| M8 | every: the largest of the longest kept | P1 272 |
| M9 | every: a smaller word winning whatever its length | P1 665, P2 1362 |
| M10 | levels: a two-letter word built without its first letter | P1 265, P4 457 |
| M11 | levels: a length with no word not stopping the climb | P1 575, P4 1062 |
| M12 | levels: the largest of the last length kept | P1 272 |
| E1 | every: the prefixes still looked up after one is missing | 0 |
| E2 | levels: the groups grown while fewer than the length plus one | 0 |
| E3 | trie: no word told apart by its depth instead of its index | 0 |

P1 kills all twelve, and is the only property that sees the four that
keep the largest of the longest words, M2, M5, M8 and M12, with
272 failures each: reversing or doubling the list cannot change which
word wins a tie in an arm that sorts or compares, and after P4's
addition every word long enough to win starts with the added word,
however a tie falls. P2 sees M3, whose walk follows the list reversed
instead of sorted, and M9, where a smaller word wins whatever its
length, so the result depends on which comes last; P3 sees only
M3. P4 sees M3 as well, the edits that let a word in without all its
prefixes, M1, M4, M6, M7 and M10, and M11, which answers with nothing
whenever the list holds a word longer than any that can be built. M1 and
M7 fail the same checks, since both take a word whose prefixes are all
there but its first letter. M10 makes the same edit to the levels arm
and fails less often, because that arm stops at the first length with no
word, so with no one-letter word at all it never reaches length
2. M4 and M6 fail the same checks, since both answer with the longest
word in the list whether or not it can be built. E1 keeps looking up
prefixes after one is missing, which only costs time; E2 grows the
groups while there are fewer than the length plus one, the same test;
E3 tells "no word" by a depth of 0 instead of an index of -1, and only
the root has depth 0.

## Verification

Every arm prints the same output as `longest_word_in_dictionary.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` and the release build that runs `check` and `__mir-run` are both
at kara `a73d3c10ad`, whose last compiler change is `3c8e763161`. The
runtime archives were built after that change.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking: at `*b` over `bytes().iter()` in the
trie arm, the differential's copy of it and the bench program, and at
`*word` over `iter()` in the every and levels arms and the differential,
since legacy gives those by value where v2 gives references; and every
arm at `next_random(mut seed)` in the harness's `random_word`, whose
argument is already a `mut ref`, where legacy wants the marker dropped
and design.md § Call-site `mut` markers now requires it (kara
B-2026-10-14-25). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the trie arm, not the ★ arm, in all five
languages: it is the same algorithm in each, where the ★ arm's sort and
string set would be five different libraries, and C has neither. It
makes 40 dictionaries of 1,000 words from 4 letters once, each word but
the fresh ones grown from an earlier word by one letter, and in each of
300 rounds gives one word of every dictionary a letter more before
asking every dictionary again, summing the lengths of the answers. Every
query builds its own trie, one array of 26 children per node. Every
implementation prints `300 rounds of 40 dictionaries of 1000 words: sum
144292`, the Kāra program under `karac __mir-run` included (in
2.5 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.72 to 0.89 s |
| Rust (`rustc -O`) | 0.90 to 1.00 s, one run at 1.18 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.94 to 1.11 s, one run at 1.67 s |
| Go | 2.01 to 2.14 s |
| Python | 11.2 to 11.6 s |
| Kāra (`karac build --mir`) | 0.85 to 1.05 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.1 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is level with Rust and about a sixth behind C at the
medians of the interleaved runs (0.93 s against 0.96 and 0.79), and
twice as fast as Go. Under valgrind's cachegrind it runs 7.4 billion
instructions against Rust's 7.3 and C's 5.2, and mispredicts 35 million
branches against 33 and 32. Every query allocates one array per trie
node in all five, so the time includes the allocator's; that share was
not measured. The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
