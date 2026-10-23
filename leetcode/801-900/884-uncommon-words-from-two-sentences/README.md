# 884. Uncommon Words from Two Sentences

A sentence is a string of single-space separated words where each word
consists only of lowercase letters. A word is uncommon if it appears
exactly once in one of the sentences, and does not appear in the other
sentence. Given two sentences `s1` and `s2`, return a list of all the
uncommon words. You may return the answer in any order.

```
s1 = "this apple is sweet", s2 = "this apple is sour"  ->  ["sweet","sour"]
s1 = "apple apple", s2 = "banana"  ->  ["banana"]
```

**Constraints:** `1 <= s1.length, s2.length <= 200`, `s1` and `s2`
consist of lowercase English letters and spaces, do not have leading or
trailing spaces, and all their words are separated by a single space.

## Approaches

| file | mechanism |
|---|---|
| `uncommon_from_sentences.kara` ★ | one map of counts: a word that appears exactly once in one sentence and not at all in the other appears exactly once in the two together, and the converse holds too, so the words of both are counted in one `Map` and the answer is the words counted once. O(total length) |
| `uncommon_from_sentences_sorted.kara` | sorting the words: the words of both sentences in one list, sorted so that copies of a word sit together; a word alone in its run is uncommon. O(W log W) comparisons for W words |
| `uncommon_from_sentences_sets.kara` | two sets: each word met in turn goes into the set of words seen once the first time, and any later time leaves it for the set of words seen again, where it stays; the words left seen once are the answer. O(total length) |
| `uncommon_from_sentences_ordered.kara` | each sentence counted on its own, in order: a `SortedMap` of counts for each sentence, and a word uncommon when one counts it once and the other not at all, the statement's test, which walking the maps in order gives alphabetically. O(W log W) |
| `uncommon_from_sentences_trie.kara` | a trie of counts: the words of both sentences put into a trie, a node for every prefix, each with room for 26 children and a count of the words ending there; a depth-first walk in letter order collects the words counted once. O(total length * 26) |
| `differential.kara` | the five arms against the statement read literally, six properties |

LeetCode takes the words in any order, and two of the arms give them in
the order of a hash map or set, which differs from run to run, so every
answer is sorted before it is printed or compared. Every arm prints the
same 10 lines: LeetCode's two examples and six more (`a` and `b`; `a`
and `a`; `a a a` and `b`; the same three words in either order; two
sentences sharing some words; and two of 199 characters, 100 words each,
with one word between them said once); the uncommon words of 3,000 pairs
of up to 20 characters, 10,722 in all; and of 1,000 pairs of up to 200
characters, LeetCode's most, with words of up to 4 of 5 letters, with a
checksum of the words in order. `uncommon_from_sentences.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every word of `s1` tried, counted in `s1` and in `s2` and kept
when the counts are one and none, then every word of `s2` the same way.
It checks 3,400 cases: 3,000 pairs of up to 20 characters with words of
one or two of 3 letters, against the statement; and 400 of LeetCode's
sizes, up to 200 characters with words of up to 4 of 5 letters, against
the other properties. The ★ arm finds 29,164 uncommon words in all.

| | property |
|---|---|
| P1 | the statement's words, on pairs of up to 20 characters |
| P2 | no word twice, each one said once in the two sentences together, and no more words than they hold |
| P3 | the sentences swapped, and their words each in another order, give the same words |
| P4 | a word of `s1` said once more in `s2` leaves the answer if it was in it, and nothing else changes |
| P5 | the two sentences joined into one, beside a sentence of one new word, give the same words and the new one |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3400 cases, 29164
uncommon words in all, 100000 checks over 5 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a word counted twice taken too | P1 2153, P2 2545, P4 1707, P6 2545 |
| M2 | ★: the first sentence counted in place of the second | P1 2941, P5 3400, P6 3341 |
| M3 | ★: one-letter words left out | P1 2058, P6 2181 |
| M4 | sorted: the words left unsorted | P1 2155, P2 2551, P3 2074, P4 3331, P6 2551 |
| M5 | sorted: the last word never checked | P1 2168, P5 3400, P6 2523 |
| M6 | sorted: a run of copies stepped over two at a time | P1 1141, P2 1507, P4 1181, P6 1507 |
| M7 | sets: a word met a third time taken as new | P1 1141, P2 1507, P4 1181, P6 1507 |
| M8 | sets: a word met again kept among the words seen once | P1 2512, P2 2908, P4 3400, P6 2908 |
| M9 | sets: the words seen again returned | P1 3000, P2 2908, P4 3400, P5 3400, P6 3400 |
| M10 | ordered: a word in both sentences kept | P1 1673, P2 2037, P3 1280, P4 2500, P5 2037, P6 2037 |
| M11 | ordered: the first sentence walked in place of the second | P1 2509, P3 3341, P5 3400, P6 2908 |
| M12 | ordered: every word counted once | P1 1752, P2 2140, P5 2324, P6 2140 |
| M13 | trie: the last word of each sentence never counted | P1 2672, P2 1491, P3 2658, P4 2869, P5 3400, P6 3044 |
| M14 | trie: every word collected | P1 2512, P2 2908, P4 3400, P6 2908 |
| M15 | trie: a new node made for every letter | P1 2849, P2 2635, P3 2858, P4 3400, P6 3249 |

P1 and P6 kill all fifteen. M6 and M7 fail the same cases: stepping over
a run two copies at a time and letting a third sighting start over both
take a word said an odd number of times, three or more. M8 and M14 fail
the same cases too, as both return every word of the sentences once.
M3 is the closest to surviving: only the statement and the arms' vote
see it, since a one-letter word left out changes nothing the other
properties compare. None of the fifteen tried was equivalent or crashed,
and none was replaced.

## Verification

Every arm prints the same output as `uncommon_from_sentences.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `89d76e3ff2` and the runtime
archives at `e903d5b111`, with no runtime change between them. Under
`karac __mir-run` the arms take 1.4 to 1.6 s each, but for the trie arm
at 2.4 s, and the differential 18 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends run only the sorted arm, and only under the
interpreter, where its output is the same. Everything else is refused or
fails: `*n` on a map entry (the ★ and ordered arms, the differential and
the bench program) and a word passed to `Set.contains` (the sets arm)
are type errors there; its JIT and builds have no `split` method; and
its interpreter has no `String.pop`, which the trie arm uses. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 1,000 sentences
of up to 200 characters, words of 1 to 4 of the letters a to e, drawn
once; then each sentence paired with the 200 after it in turn, 200,000
pairs, and the uncommon words of each folded into a checksum that does
not depend on their order, as the hash maps give them in different
orders. The map is Kāra's `Map`, Rust's `HashMap`, Go's built-in map and
Python's `dict`; each copies the word into its map, but Go and Python,
whose strings share their bytes, at no cost. C has no map, so its program
writes a table out, open addressing over 512 slots keyed by FNV-1a, and
copies each new word into it and each uncommon word out, as the Kāra
program does. Every implementation prints `1000 sentences, each paired
with 200 others: 9167319 uncommon words, checksum 545478462`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.91 to 1.03 s | 0.96 s |
| Rust (`rustc -O`) | 2.85 to 3.16 s | 2.92 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.75 to 3.12 s | 3.01 s |
| Go | 2.04 to 2.29 s | 2.18 s |
| Python | 5.4 s | |
| Kāra (`karac build --mir`) | 3.18 to 3.34 s | 3.29 s |

The frozen legacy backend refuses the bench program (`*n` on a map
entry), so it has no row. `bench.sh` builds the Kāra program with
`karac build --mir`, the v2 compiled backend, as kata 883's does.

v2 takes 1.09 times Rust's median time under overflow checks, 1.51
times Go's and 3.43 times C's. Under valgrind's cachegrind C runs 6.60
billion instructions, Rust with overflow checks 24.97 billion and v2
31.14 billion. Rust and v2 both hash with SipHash, Kāra's `Map` with
SipHash-1-3 under a key drawn per process, and allocate a `String` for
every word counted, where C hashes with FNV-1a, which most likely
accounts for much of C's lead (inferred from the code, not profiled).
Python is closer to the compiled programs here than in most katas, as
nearly all its work is in `str.split` and `dict`, which are written in
C. The comparison with C and Rust waits until after M4.
