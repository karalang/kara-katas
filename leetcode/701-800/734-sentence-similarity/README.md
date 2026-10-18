# 734. Sentence Similarity

A sentence is given as an array of words. Given two sentences,
`sentence1` and `sentence2`, and an array `similarPairs` of pairs of
words, where `similarPairs[i] = [xi, yi]` says that the words `xi` and
`yi` are similar, return whether the two sentences are similar. They are
when they have the same number of words and each word of `sentence1` is
similar to the word in the same place in `sentence2`. A word is always
similar to itself, and similarity is not transitive: when `a` and `b`
are similar and `b` and `c` are, `a` and `c` need not be.

```
sentence1 = ["great", "acting", "skills"]
sentence2 = ["fine", "drama", "talent"]
similarPairs = [["great", "fine"], ["drama", "acting"],
                ["skills", "talent"]]                   ->  true
sentence1 = ["great"], sentence2 = ["great"],
similarPairs = []                                       ->  true
sentence1 = ["great"], sentence2 = ["doubleplus", "good"]
similarPairs = [["great", "doubleplus"]]                ->  false
```

**Constraints:** 1 <= `sentence1.length`, `sentence2.length` <=
1000; 1 <= each word's length <= 20; words are English letters; 0 <=
`similarPairs.length` <= 1000; every pair is two words of 1 to
20 letters, and the pairs are distinct.

## Approaches

Every arm first answers false when the lengths differ, and then tests
the places one by one, stopping at the first that is not similar; they
differ in how they find whether two different words are a pair.

| file | mechanism |
|---|---|
| `sentence_similarity.kara` ★ | a `Set` of the pairs, each put in both ways round; two different words are similar when the set holds them in that order; O(p + n) set operations |
| `sentence_similarity_neighbours.kara` | a `Map` from each word to the `Set` of words it is paired with, filled from both ends of each pair; O(p + n) map and set operations |
| `sentence_similarity_sorted.kara` | each pair written smaller word first and the pairs sorted; two different words, written the same way, are looked for by binary search; O(p log p) to sort and O(log p) a place |
| `sentence_similarity_scan.kara` | no index: for each place where the words differ, the whole list of pairs is searched for one holding the two words either way round; O(n p) time, no extra space |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: the three LeetCode examples; `a` and
`c` with pairs `(a, b)` and `(b, c)`, which are not similar, since
similarity is not transitive; a pair given the other way round; two
words swapped; a word paired with two others, neither of them the word
it faces; 1,000 words, each facing a word it is paired with among
1,000 pairs over 200 words; the same with the last word changed to one
in no pair, with the pairs left out, and with one word short; and
300 random cases with how many are similar and a checksum.
`sentence_similarity.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which for each place tests the two words for equality and then looks
through every pair, either way round. 3,000 random cases are checked,
each of 1 to 6 words out of 6 with 0 to 6 random pairs over the same
6 words; each word of the second sentence is the first's word, a word
from one of the pairs or any word, and one case in ten has a word more
in the second sentence. 846 of the cases are similar.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the two sentences the other way round give the same answer |
| P3 | every pair written the other way round gives the same answer |
| P4 | with the same number of words, the sentences are similar exactly when every place alone, as two one-word sentences, is similar |

It prints `3000 cases (846 similar), 4 arms, 46772 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each pair stored one way round only | P1 102, P2 160, P3 160 |
| M2 | ★: equal words needing a pair | P1 752 |
| M3 | ★: the last place never checked | P1 366, P4 1481 |
| M4 | neighbours: the first word of a pair given itself | P1 102, P2 160, P3 160 |
| M5 | neighbours: a word in no pair let through | P1 622, P2 699 |
| M6 | neighbours: the first place never checked | P1 365, P4 1482 |
| M7 | sorted: the pairs not put smaller word first | P1 115, P3 166 |
| M8 | sorted: the search landing past equal pairs | P1 189 |
| M9 | sorted: the pairs never sorted | P1 111 |
| M10 | scan: a pair matched one way round only | P1 102, P2 160, P3 160 |
| M11 | scan: equal words needing a pair when there are any | P1 387 |
| M12 | scan: a longer second sentence let through | P1 96, P2 96 |
| E1 | ★: the test as not (equal or paired) | 0 |
| E2 | sorted: equal words ordered with < | 0 |
| E3 | scan: the search going on after a match | 0 |

P1 kills all twelve. M1, M4 and M10 are one mistake in three arms, a
pair matched only one way round, and fail the same cases; P2 and P3 see
them too, since turning the sentences or the pairs round then changes
the answer. M3 and M6 skip a place, the last and the first, and P4 sees
them most, since a one-word sentence is then never checked at all.
M7 leaves the sorted arm's pairs in their given order, so a pair is
found only when it was written smaller word first, which P3 sees as
well. M5 and M12 let a mismatch through from one side only, a word of
the first sentence in no pair and a longer second sentence, which
P2 sees by turning the sentences round. M2, M8, M9 and M11 only P1 sees:
they get the answer wrong the same way whichever way round the sentences
or the pairs are written. E1 writes the ★ arm's test as not (equal or
paired); E2 orders a pair with < rather than <=, which differs only for
two equal words, which are never looked up; E3 lets the scan go on after
a match.

## Verification

Every arm prints the same output as `sentence_similarity.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`969445f00a`, whose last compiler change is `b830c8f243`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★, neighbours and sorted arms, and
each prints the same output under the legacy interpreter, `karac run`
and `karac build`, and under `KARAC_AUTO_PAR=1`. They refuse the scan
arm and the differential at type checking, at `p.0 == a`, which compares
a pair's `String` with the `StringSlice` that `as_str()` gives, a
comparison v2 allows. They build the bench program, after an ownership
warning that `s2` is used after a move into the function at line
65 (legacy takes a bare parameter as owned, where v2 borrows it), and it
prints the same line under the legacy `karac build` in 0.76 to 0.86 s
(below). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
1,000 random pairs over 5,000 words and two sentences of 1,000 words,
each place filled with the two words of a random pair in one order or
the other, and in each of 1,000 rounds changes one word of the second
sentence to a random word and checks the sentences, then puts the word
back and checks again; each check builds its set of pairs afresh, as the
function does. The C program's set holds pointers to the words rather
than copies, and so do Go's strings and Python's tuples, where the Kāra
and Rust programs clone the words into the set, as the ★ arm does. Every
implementation prints `1000 rounds of 2 checks of 1000 words with
1000 pairs: 1000 similar`, the Kāra program under `karac __mir-run`
included (in 12 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.18 to 0.22 s |
| Rust (`rustc -O`) | 0.85 to 1.05 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.88 to 1.05 s |
| Go | 0.53 to 0.63 s |
| Python | 0.42 to 0.44 s |
| Kāra (`karac build --mir`) | 0.64 to 0.77 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
6.6 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is 3.4 times C at the medians of the interleaved runs
(0.67 s against 0.20), a sixth behind Go (0.58), and more than a quarter
ahead of Rust (0.92) and Rust under overflow checks (0.98). Python, at
0.42 to 0.44 s, is ahead of all of them but C: its tuples share the
words and each word keeps its hash once computed, while Kāra and Rust
clone 4,000 words into each fresh set and hash every pair in full. Under
valgrind's cachegrind the v2 build runs 8.0 billion instructions against
Rust's 8.9 and C's 1.8, and 1.2 billion branches against 1.1 and
0.4, with 13 to 21 million mispredicted in the three. The legacy build
of the same program runs in 0.76 to 0.86 s over eight runs, so v2 is a
fifth ahead of it. The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
