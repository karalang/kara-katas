# 953. Verifying an Alien Dictionary

In an alien language, surprisingly, they also use English lowercase
letters, but possibly in a different `order`. The `order` of the
alphabet is some permutation of lowercase letters. Given a sequence of
`words` written in the alien language, and the `order` of the alphabet,
return `true` if and only if the given `words` are sorted
lexicographically in this alien language.

```
words = ["hello","leetcode"], order = "hlabcdefgijkmnopqrstuvwxyz"       ->  true
words = ["word","world","row"], order = "worldabcefghijkmnpqstuvxyz"     ->  false
words = ["apple","app"], order = "abcdefghijklmnopqrstuvwxyz"            ->  false
```

**Constraints:** `1 <= words.length <= 100`; `1 <= words[i].length <= 20`;
`order.length == 26`; all characters in `words[i]` and `order` are
English lowercase letters.

## Approaches

| file | mechanism |
|---|---|
| `is_alien_sorted.kara` ★ | a rank per letter: each letter numbered by its place in the order, then each word compared with the next, the first letter where they differ deciding, and a word that runs out first allowed only when it is the earlier one. Sorted neighbours make a sorted list, since the order on words is transitive. O(total letters) |
| `is_alien_sorted_translate.kara` | each word rewritten letter by letter into English, the order's first letter as `a`, its second as `b` and so on, and the rewrites compared as ordinary strings, each with the one before. O(total letters) |
| `is_alien_sorted_keys.kara` | each word turned into the vector of its letters' ranks, and the vectors compared lexicographically, a prefix first, each with the next. O(total letters) |
| `is_alien_sorted_sorted.kara` | a copy of the words sorted by a key of letter ranks and compared with the words as given: a sorted list is its own sort. O(total letters log n) |
| `is_alien_sorted_columns.kara` | column by column, as a dictionary is laid out: within a run of words sharing their first d letters, the words that end at d come first, the letter at d never falls down the run, and each run sharing that letter is checked from d + 1 on, recursively. O(total letters) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's three examples and six
more (one word, a prefix before its extension, a short word after a
longer one whose first letter ranks lower, a word twice, two words
sorted only in their own order, and a word repeated after another); for
300 random cases of 1 to 10 words of 1 to 5 letters, drawn from 1 to 4
letters of a random order, 1,671 words in all, how many are sorted and a
checksum; and six cases of LeetCode's largest size: 100 sorted words of
up to 20 letters, the same with the two middle words swapped, the same
reversed, 100 copies of one word, `q` growing to 20 `q`s and staying
there, and that list backwards. `is_alien_sorted.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, as LeetCode explains lexicographic order: two words padded to
one length with a blank that comes before every letter, compared letter
by letter, the first difference deciding; the list is sorted when every
word is at most every word after it, all pairs tried. It checks 3,200
random cases, each with its own random order and every second one sorted
first: 3,000 of 1 to 6 words of 1 to 4 letters, from 1 to 3 letters of
the order, against the statement, and 200 of up to 100 words of up to 16
letters, from 1 to 26 letters, against the other properties, 21,082
words in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | every letter renamed by one random permutation, in the words and the order alike, gives the same answer |
| P3 | one word written twice in a row gives the same answer |
| P4 | followed by a second case of one to six words in the same order, sorted half the time, the list is sorted exactly when both cases are and the first case's last word is at most the second's first, by the statement's comparison |
| P5 | one random prefix before every word, keeping every word within LeetCode's 20 letters, gives the same answer |
| P6 | each arm agrees with at least two of the other four |

Words of the large cases have at most 16 letters, so P5 always has room
for a prefix.

It prints `3200 cases of 21082 words, 2097 sorted, checksum 879077820,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (8 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Forty-one edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a longer word allowed before its prefix | P1 390, P4 377, P6 394 |
| M2 | ★: the rank comparison reversed | P1 989, P4 223, P6 1085 |
| M3 | ★: letters compared in English | P1 586, P2 452, P4 129, P6 680 |
| M4 | translate: the order itself taken as the translation | P1 587, P2 453, P4 144, P6 680 |
| M5 | translate: equal neighbours refused | P1 597, P3 1459, P4 27, P6 638 |
| M6 | translate: the first pair skipped | P1 238, P3 87, P4 309, P6 239 |
| M7 | keys: every letter ranked 0 | P1 717, P4 204, P6 813 |
| M8 | keys: only the last pair compared | P1 452, P3 141, P4 1617, P6 498 |
| M9 | keys: each key reversed | P1 689, P4 51, P5 748, P6 785 |
| M10 | sorted: the answer inverted | P1 3000, P4 2561, P6 3200 |
| M11 | sorted: only the two lists' lengths compared | P1 1005, P4 1871, P6 1103 |
| M12 | sorted: each key only the first letter | P1 455, P4 439, P5 644, P6 459 |
| M13 | columns: words ending at the column not skipped first | P1 1995, P6 2097 |
| M14 | columns: each run's first word left out of the recursion | P1 239, P3 68, P4 139, P5 696, P6 239 |
| M15 | columns: the last word left out | P1 255, P3 88, P4 281, P6 255 |

P1 and P6 kill all fifteen, P4 fourteen (all but M13), P3 five (M5, M6,
M8, M14, M15), P5 three (M9, M12, M14) and P2 two (M3, M4).

Twenty-six other edits were tried and set aside. Seventeen failed
exactly the same checks as a kept one: four more arms comparing letters
in English (translate leaving the words as they are, keys, sorted and
columns ranking by the letter itself), as M3; four ranking the order
backwards (★, keys and sorted reversing the ranks, columns comparing the
next run the wrong way), as M2; ★ building the inverse permutation, as
M4; ★ dropping the prefix rule, as M1; keys refusing equal neighbours, as
M5; ★ and keys skipping the first pair, as M6; translate never moving to
the next word, as M11; ★ skipping no common prefix and columns never
recursing, which both compare first letters only, as M12; and columns
not splitting runs by letter, as M7. Four were sound but beyond three an
arm: translate comparing each word with the one before the wrong way
round and sorted reversing its copy, which fail the same checks as each
other, keys comparing every word with the first, and keys ranking
letters in pairs. Two crashed with an index out of bounds: columns
allowing a word that ends inside a run, and columns recursing two
columns on.

Three were equivalent. ★ stopping the shared prefix one letter short of
the first word's end: the letter it then compares is equal, which never
refuses. Translate starting the English letters at `b`: the rewrite
still keeps every comparison. Keys numbering the ranks in steps of two:
the same order.

## Verification

Every arm prints the same output as `is_alien_sorted.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `46c2e7477d`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the
arms take 0.2 s each and the differential 8.7 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program builds 200 sets of 100 words once, each with its own
random order: words of 1 to 20 letters drawn from the order's first three
letters, so neighbours share long prefixes, sorted by an insertion sort
in the order, and in every third set the last two words swapped. In each
of 2,000 rounds it runs the ★ arm on every set, each round starting from
a different one, and folds the answers into a checksum. Every
implementation prints `2000 rounds over 200 sets of 100 words: 268000
sorted, checksum 609747253`. Each call builds the 26 ranks and reads the
words in place: `bytes()` in Kāra, `as_bytes()` in Rust, string indexing
in Go and Python, and in C a pointer and length per word.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.52 to 0.60 s | 0.57 s |
| Rust (`rustc -O`) | 0.50 to 0.58 s | 0.52 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.53 to 0.62 s | 0.56 s |
| Go | 0.53 to 0.61 s | 0.56 s |
| Python | 17.7 s | |
| Kāra (`karac build --mir`) | 0.55 to 0.72 s | 0.59 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 31 times
C's.

v2 takes 1.04 times Rust's median time under overflow checks and 1.03
times C's. Under valgrind's cachegrind v2 runs 3.16 billion
instructions and 0.81 billion branches with 44.8 million mispredicted,
Rust with overflow checks 3.02 billion, 0.66 billion and 41.8 million,
and C 2.52 billion, 0.57 billion and 49.0 million.
