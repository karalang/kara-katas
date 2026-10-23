# 890. Find and Replace Pattern

Given a list of strings `words` and a string `pattern`, return a list of
`words[i]` that match `pattern`. You may return the answer in any order.

A word matches the pattern if there exists a permutation of letters `p`
so that after replacing every letter `x` in the pattern with `p(x)`, we
get the desired word. Recall that a permutation of letters is a
bijection from letters to letters: every letter maps to another letter,
and no two letters map to the same letter.

```
words = ["abc","deq","mee","aqq","dkd","ccc"], pattern = "abb"  ->  ["mee","aqq"]
words = ["a","b","c"], pattern = "a"  ->  ["a","b","c"]
```

**Constraints:** `1 <= pattern.length <= 20`, `1 <= words.length <= 50`,
`words[i].length == pattern.length`, and `pattern` and `words[i]` are
lowercase English letters.

## Approaches

LeetCode accepts the matching words in any order; every arm keeps them
in the order they are given, so that all five print the same list.

| file | mechanism |
|---|---|
| `find_and_replace_pattern.kara` ★ | two maps per word: walk the pattern and the word together, keeping the letter each pattern letter has become and the pattern letter each word letter came from; a clash with either rules the word out. O(total letters) |
| `find_and_replace_pattern_shape.kara` | the shape of each word: each letter replaced by the position where it first appears, so `mee` and `abb` are both 0, 1, 1; a one-to-one renaming keeps the shape and nothing else does, so a word matches exactly when its shape is the pattern's. O(total letters * 26) |
| `find_and_replace_pattern_onemap.kara` | one map and a count: each pattern letter mapped to the word letter beside it, ruling the word out on a clash, which makes the renaming a function; it is one-to-one exactly when the map has as many different values as keys, which a set of the values counts. O(total letters) |
| `find_and_replace_pattern_table.kara` | the ★ arm's two maps as arrays of 26 entries indexed by letter, -1 for a letter not yet seen. O(total letters) |
| `find_and_replace_pattern_pairs.kara` | every pair of positions: a one-to-one renaming exists exactly when every two positions hold the same letter in the word if and only if they do in the pattern. O(total letters * pattern length) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples and four more
(a two-letter pattern, both ways round and with a repeat; a repeated
letter as the pattern; a pattern of two letters alternating; and a
20-letter pattern of distinct letters, with a word that repeats one),
and for 3,000 random cases of LeetCode's sizes, up to 50 words of up to
20 letters drawn from 2 to 26 letters, half of the words the pattern
renamed (half of those by a map that sends two letters to one), how many
words match, 42,301, with a checksum of the words kept.
`find_and_replace_pattern.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a search over the permutations, sending each letter of the
pattern, in order of first appearance, to each letter not yet taken from
the alphabet the case is drawn from, and keeping a word when some
assignment rewrites the pattern into it. It checks 3,200 random cases:
3,000 of up to 8 words of up to 6 letters, from 2 to 4 letters, against
the statement, and 200 of LeetCode's sizes against the other
properties; half the words are the pattern renamed, half of those by a
map that merges two letters. The ★ arm keeps 8,081 words in all.

| | property |
|---|---|
| P1 | the words the statement keeps, on the small cases |
| P2 | the words kept are some of the words, in their order, and the pattern itself, added at the end, is kept |
| P3 | a word matches the pattern exactly when the pattern, as the only word, matches the word taken as the pattern |
| P4 | the pattern's letters renamed one-to-one keep the same words, and the words' letters renamed one-to-one keep the same words renamed |
| P5 | the words reversed keep the same words reversed, and each word given twice is kept twice |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 8081 words
kept in all, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the map back from the word never checked | P1 1545, P3 2064, P6 1717 |
| M2 | ★: the map from the pattern never checked | P1 453, P3 2064, P6 494 |
| M3 | ★: the last letter never compared | P1 1007, P6 1070 |
| M4 | shape: every letter taken as first seen at 0 | P1 2255, P6 2438 |
| M5 | shape: the first letter's position recorded anew each time it is seen | P1 974, P6 1040 |
| M6 | shape: only the lengths compared | P1 2255, P6 2438 |
| M7 | onemap: fewer values than keys allowed | P1 1545, P3 2064, P6 1717 |
| M8 | onemap: each pattern letter mapped to itself | P1 1286, P3 534, P4 955, P6 1416 |
| M9 | onemap: the pattern's letters counted instead of the values | P1 1545, P3 2064, P6 1717 |
| M10 | table: a new pattern letter allowed to take a word letter already taken | P1 1599, P6 1752 |
| M11 | table: each pattern letter recorded as going to itself | P1 1207, P4 827, P6 1337 |
| M12 | table: each word letter recorded as coming from itself | P1 1207, P4 827, P6 1337 |
| M13 | pairs: neighbouring positions never compared | P1 823, P6 883 |
| M14 | pairs: only a repeat in the pattern checked | P1 1545, P3 2064, P6 1717 |
| M15 | pairs: the first position never compared | P1 974, P6 1040 |

P1 and P6 kill all fifteen. A one-sided check (M1, M7, M9, M14) keeps a
word that merges two pattern letters, or one that splits a pattern
letter (M2), and P3 catches both, since the pattern does not match such
a word back. P2 and P5 kill none: every fault here decides each word on
its own, so it still keeps a subset of the words in their order and
treats a reversed or doubled list the same way. P4 kills only the
mutants that tie the answer to the letters themselves (M8, M11, M12).

One mutant was replaced because it is equivalent. The first M11 dropped
the `from` table from the clash test, leaving `to[a] != b`; but the two
tables are always written together, so `to[a] == b` already implies
`from[b] == a`, and the fault never changes an answer.

## Verification

Every arm prints the same output as `find_and_replace_pattern.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 3.3 to 6.1 s
each and the differential 15 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy interpreter prints the same output for all five arms.
Its JIT and `karac build --legacy`, with and without auto-par, panic
while compiling every arm (`src/codegen/method_call.rs:3350`, an
integer found where a struct was expected), after a warning that `word`
is moved and used again. Every legacy lane refuses the differential and
the bench program: `words[i]` passed to a function is a move out of an
index (`E_INDEX_MOVE_NON_COPY`). Legacy is frozen, so these are not
filed.

## Benchmarks

The bench program uses the table arm, the same algorithm in all five
languages: 6,000 random words of 10 letters from `a` to `c`, each taken
in turn as the pattern for all 6,000, with the two tables fixed arrays
of 26. Every implementation copies each word it keeps (Go shares the
immutable string) and prints `6000 patterns over 6000 words of 10
letters: 9660 matches, checksum 505073226`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.41 to 0.49 s | 0.45 s |
| Rust (`rustc -O`) | 0.49 to 0.62 s | 0.52 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.50 to 0.63 s | 0.52 s |
| Go | 1.29 to 1.53 s | 1.41 s |
| Python | 18.7 s | |
| Kāra (`karac build --mir`) | 0.53 to 0.59 s | 0.57 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 889's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 1.10 times Rust's median time under overflow checks and 1.27
times C's. Under valgrind's cachegrind C runs 2.08 billion
instructions, Rust with overflow checks 3.92 billion and v2 3.57
billion; C's branches mispredict at 10.1%, Rust's and v2's at 5.5% and
5.3%, which most likely eats part of the lead C's instruction count gives
it (inferred from the counts, not profiled). The comparison with C and
Rust waits until after M4.
