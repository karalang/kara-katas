# 737. Sentence Similarity II

A sentence is given as an array of words. Given two sentences,
`sentence1` and `sentence2`, and an array `similarPairs` of pairs of
words, where `similarPairs[i] = [xi, yi]` says that `xi` and `yi` are
similar, return whether the two sentences are similar: they have the
same number of words, and each word of `sentence1` is similar to the
word in the same place in `sentence2`. A word is always similar to
itself, and unlike kata 734 similarity is transitive: when `a` and `b`
are similar and `b` and `c` are, so are `a` and `c`.

```
sentence1 = ["great", "acting", "skills"]
sentence2 = ["fine", "drama", "talent"]
similarPairs = [["great", "good"], ["fine", "good"],
                ["drama", "acting"], ["skills", "talent"]]   ->  true
sentence1 = ["I", "love", "leetcode"]
sentence2 = ["I", "love", "onepiece"]
similarPairs = [["manga", "onepiece"], ["platform", "anime"],
                ["leetcode", "platform"], ["anime", "manga"]] ->  true
similarPairs = [["manga", "hunterXhunter"], ["platform", "anime"],
                ["leetcode", "platform"], ["anime", "manga"]] ->  false
```

**Constraints:** 1 <= `sentence1.length`, `sentence2.length` <=
1000; 1 <= each word's length <= 20; words are English letters; 0 <=
`similarPairs.length` <= 2000; every pair is two words of 1 to
20 English letters.

## Approaches

Similar words are the words joined by a chain of pairs, the connected
components of the graph whose edges are the pairs. Every arm first
answers false when the lengths differ and passes a place whose two words
are equal; they differ in how they decide that two different words share
a component.

| file | mechanism |
|---|---|
| `sentence_similarity_ii.kara` ★ | number every word in a pair with a `Map`, join the two words of each pair in a union-find with union by size and path compression, and compare roots; O((p + n) α(p)) after numbering |
| `sentence_similarity_ii_components.kara` | build the graph as a `Map` from each word to its neighbours and label each component once by a breadth-first search from every word not yet labelled; two words are similar when their labels match |
| `sentence_similarity_ii_search.kara` | build the same graph and, at every place where the words differ, search it depth first from one word for the other with a `Set` of the words seen; nothing is kept from one place to the next, O(n (p + w)) for w words |
| `sentence_similarity_ii_relax.kara` | number the words, label each with its own number, and sweep the pairs again and again, lowering both words of a pair to the smaller label, until a sweep changes nothing; each word then carries the smallest number in its component |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 15 lines: the three LeetCode examples; `a` and
`c` with pairs `(a, b)` and `(b, c)`, now similar, and with `(a, b)` and
`(c, d)`, not; a word facing itself with no pairs; sentences of
different lengths; two words swapped, joined through a third; the two
ends of a chain of 1,000 words given in a shuffled order, and the same
chain with one pair left out; 1,000 words each joined to the word facing
it by a walk of up to 5 steps along 2,000 random pairs over 3,000 words,
and the same with the last word changed to one in no pair, with the
pairs left out, and with one word short; and 300 random cases with how
many are similar and a checksum. `sentence_similarity_ii.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which numbers every word that appears, marks each word similar to itself
and the two words of each pair similar both ways round, closes that
table under transitivity with Floyd and Warshall's triple loop, and
looks each place up in it. 3,000 random cases are checked, each of 1 to
6 words out of 8 with 0 to 8 random pairs over the same 8 words; each
word of the second sentence is the first's word, a word from one of the
pairs or any word, and one case in ten has a word more in the second
sentence. 979 of the cases are similar.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the two sentences the other way round give the same answer |
| P3 | every pair written the other way round, and the pairs in the reverse order, give the same answer |
| P4 | with the same number of words, the sentences are similar exactly when every place alone, as two one-word sentences, is similar |

It prints `3000 cases (979 similar), 4 arms, 46748 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the word joined, not its root | P1 29, P3 44 |
| M2 | ★: the second word's root never found | P1 186, P3 137 |
| M3 | ★: equal words needing to be in a pair | P1 502 |
| M4 | components: each pair followed one way only | P1 240, P3 147 |
| M5 | components: every component given the same label | P1 353 |
| M6 | components: only a start's own neighbours labelled | P1 273, P3 89 |
| M7 | search: only words one pair away found | P1 250 |
| M8 | search: equal words needing to be in a pair | P1 502 |
| M9 | search: the first place never checked | P1 343, P4 1365 |
| M10 | relax: a single sweep | P1 133, P3 134 |
| M11 | relax: every word starting with the same label | P1 353 |
| M12 | relax: a change counted only at a pair's first word | P1 326, P3 76 |
| E1 | relax: labels raised to the larger, not lowered | 0 |
| E2 | search: the start not marked seen | 0 |
| E3 | search: only the first word required in the graph | 0 |

P1 kills all twelve. M3 and M8 are one mistake in two arms, equal words
that must be in a pair, and fail the same 502 cases; M5 and M11 both
make every word in a pair similar to every other, and fail the same
353. P3 sees the edits whose answer depends on the order or the
direction the pairs come in: M1 joins a word rather than its root,
M2 never finds the second word's root, M4 follows each pair one way
only, M6 labels only a start's own neighbours, M10 makes a single sweep
and M12 counts a change only at a pair's first word, and each of them
joins more or fewer words when the pairs are turned round and reversed.
P4 sees only M9, which skips the first place, never checked in a
one-word sentence. P2 sees none: every edit treats the two sentences
alike. E1 raises both words of a pair to the larger label, which leaves
every word with the largest number in its component instead of the
smallest, as good a label; E2 leaves the start of a search unmarked, so
that it can be pushed once more but no more; E3 drops the test that the
second word is in the graph, since a search cannot reach a word that is
not.

## Verification

Every arm prints the same output as `sentence_similarity_ii.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`3df39964e7`, whose last compiler change is `56339e6224`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse the ★, components and relax arms, the
differential and the bench program at type checking: at a `*` on the
value a `Map`'s `get` finds, which legacy gives by value where v2 gives
a reference, and in the components arm at `Map.get_mut`, which legacy
does not have. They accept the search arm, which prints the right output
under the legacy interpreter but aborts under the legacy `karac run` and
`karac build` with glibc's `malloc_consolidate(): unaligned fastbin
chunk detected`, a corrupted heap. Legacy is frozen, so this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
2,000 random pairs over 3,000 words and two sentences of 1,000 words
once, each word of the second reached from the first's by a walk of up
to 5 steps along the pairs, and in each of 1,000 rounds changes one word
of the second sentence to a random word and checks the sentences, then
puts the word back and checks again; each check numbers the words and
builds its union-find afresh, as the function does. The C program's
table of word numbers holds pointers to the words rather than copies,
and so do Go's and Python's maps, where the Kāra and Rust programs copy
each word into theirs, as the ★ arm does. Every implementation prints
`1000 rounds of 2 checks of 1000 words with 2000 pairs: 1196 similar`,
the Kāra program under `karac __mir-run` included (in 35 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.62 to 0.77 s |
| Rust (`rustc -O`) | 0.80 to 0.89 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.79 to 1.02 s |
| Go | 0.70 to 0.81 s |
| Python | 2.4 to 2.5 s |
| Kāra (`karac build --mir`) | 0.67 to 0.89 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 7.4 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is a sixth behind C at the medians of the interleaved
runs (0.79 s against 0.67), level with Go (0.78), and a tenth ahead of
Rust (0.87) and Rust under overflow checks (0.89). Under valgrind's
cachegrind it runs 9.4 billion instructions against Rust's 7.4 and C's
3.2, and 1.6 billion branches against 0.88 and 0.83, with 32 to
39 million mispredicted in the three. Where the v2 build's extra
instructions go, and why it is still ahead of Rust in time, was not
traced. The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
