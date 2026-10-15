# 648. Replace Words

Given a dictionary of roots and a sentence of words separated by single
spaces, replace every word that starts with a root by that root, the
shortest one when several start it, and return the sentence.

```
dictionary = ["cat","bat","rat"]
sentence   = "the cattle was rattled by the battery"
          ->  "the cat was rat by the bat"

dictionary = ["a","b","c"]
sentence   = "aadsfasf absbs bbab cadsfafs"
          ->  "a a b c"
```

**Constraints:** 1 to 1,000 roots of 1 to 100 lowercase letters; a
sentence of 1 to 10^6 characters, lowercase words separated by single
spaces with none at either end.

## Approaches

Every arm is `fn replace_words(dictionary: Vec[String], sentence:
String) -> String`. Each splits the sentence on spaces and joins the
answers with them.

| file | mechanism |
|---|---|
| `replace_words.kara` ★ | a trie of the roots, 26 children to a node, the end of each root marked; each word walks it from its first letter and stops at the first marked node; O(total letters) |
| `replace_words_prefixes.kara` | the roots in a `Set[String]`; each word tries its prefixes from one letter up to the longest root's length and stops at the first in the set |
| `replace_words_shortest.kara` | the roots sorted shortest first; each word takes the first one it starts with |
| `replace_words_every.kara` | each word against every root, keeping the shortest that starts it |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: the two LeetCode examples; six more
(a root that is a whole word; a root longer than the word it would
start; roots inside roots, the shortest winning; no word with a root; a
root given twice; and one word), each with its answer; a count and a
checksum of the characters of the answers to 300 random cases of 1 to
10 roots of 1 to 4 letters and 1 to 10 words of 1 to 8, all from the
first 3 letters of the alphabet; and two cases of 1,000 roots of 3 to
6 letters and 20,000 words, from the first 4 letters, where most words
have a root, and from all 26, where few do. `replace_words.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
for each word, its prefixes from one letter up, each compared letter by
letter with every root, the first that matches replacing the word. Each
of 1,000 cases has 1 to 6 roots of 1 to 3 letters and 1 to 6 words of
1 to 6 letters, all from the first 2 or 3 letters of the alphabet, so
roots often start one another and repeat.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer has one word for each word of the sentence, each a prefix of its word |
| P3 | the roots in reverse give the same answer |
| P4 | each word of the sentence replaced on its own gives the same word |
| P5 | replacing the answer again changes nothing |

It prints `1000 cases (3492 words), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk not stopped at the first root | P1 690 |
| M2 | ★: the newest node marked, not the root's own | P1 196, P3 290 |
| M3 | prefixes: the longest root's length never tried | P1 191 |
| M4 | prefixes: the search not stopped at the first root | P1 215 |
| M5 | shortest: the roots sorted longest first | P1 215 |
| M6 | shortest: the word tested as a prefix of the root | P1 797, P2 288, P3 48 |
| M7 | every: the last root that starts the word kept | P1 106, P3 192 |
| M8 | every: roots measured against the word, not the best so far | P1 94, P3 161, P5 94 |
| E1 | ★: the root node's mark trusted | 0 |
| E2 | prefixes: prefixes longer than every root tried too | 0 |
| E3 | shortest: the roots in alphabetical order | 0 |
| E4 | every: a root tested against the best so far, not the word | 0 |

P1 kills all eight. M4 and M5 fail in exactly the same 215 cases because
both keep the longest root that starts a word rather than the shortest.
M1 fails far more often: walking past the first root, it replaces a word
only when the walk happens to stop on another root's end. P3 sees the
four mutants whose answer depends on the order of the roots: M2 marks
whichever node was made last, M6 breaks ties by that order, and M7 and
M8 keep the last root that passes their test. P2 sees only M6, the one
mutant that can answer a root longer than its word, and P5 only
M8, whose second pass can find a shorter root than its first. P4 sees
nothing, and cannot: every arm answers each word on its own, so a word
alone gets the same answer, right or wrong. The four survivors cannot
change an answer: no root is empty, so the trie's first node is never
marked; a prefix longer than every root is not a root; the roots that
start one word all start one another, so the alphabetically first of
them is the shortest; and a root shorter than the best so far starts the
word exactly when it starts that best, itself a prefix of the word.

## Verification

Every arm prints the same output as `replace_words.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` (the release build is from `4497546898`, whose compiler
source is the same), with runtime archives newer than the last
`runtime/src` change.

The frozen legacy backends refuse every arm and the differential at type
checking: the harness hands `seed`, already a `mut ref` parameter, on
with the `mut` marker design.md asks for, which legacy rejects, and it
and the ★ arm read `*b` from `bytes().iter()`, which legacy types by
value. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 inputs once, each
1,000 roots of 3 to 6 letters and a sentence of 20,000 words of 1 to
10 letters, all from the first 3 to 8 letters of the alphabet, the count
picked for each input; then 100 rounds each answer one input, picked by
the round, counting the characters of the answers and putting each into
a checksum. Every implementation prints `20 inputs, 100 rounds:
8807835 characters, checksum 881012212`, the Kāra program under `karac
__mir-run` included (in 33 s).

Each implementation builds the same trie with 26 children to a node and
walks each word. Kāra, Rust and Go split the sentence into words,
collect the answers and join them, Rust and Kāra copying each word into
a new string, Go slicing the sentence; Python does the same with its own
strings. C scans the sentence in place and writes the answer into one
buffer, copying no word on its own. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine), each including making the inputs:

| | time |
|---|---|
| C (`clang -O3`) | 0.11 s in all three runs |
| Rust (`rustc -O`) | 0.23 to 0.27 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.24 s in all three runs |
| Go | 0.25 to 0.27 s |
| Python | 2.45 to 2.47 s |
| Kāra (`karac build --mir`) | 0.36 to 0.45 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: it reads `*b` from `bytes().iter()`, `random_word` hands on
`seed` with the `mut` marker, and its parameters are still owned, so
handing `dictionaries[i]` to `replace_words` moves an element out of a
`Vec`. That edit is by hand, on top of the `scripts/new-bench.sh`
output. A copy outside the kata that reads `b`, drops that marker and
makes both parameters `ref` builds under legacy and takes 0.37 to
0.38 s. Under `karac __mir-llvm-run` the program prints the same line in
2.3 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is level with legacy, two of its three runs within
0.01 s of it, and behind Rust and Go, which do the same splitting,
copying and joining; C, which copies no word on its own, is fastest. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
