# 438. Find All Anagrams in a String

Given two strings `s` and `p`, return an array of all the start indices
of `p`'s anagrams in `s`. You may return the answer in any order. An
anagram is a word formed by rearranging all the letters of another.

```
s = "cbaebabacd", p = "abc"   ->  [0,6]
s = "abab", p = "ab"          ->  [0,1,2]
```

**Constraints:** `1 <= s.length, p.length <= 3 * 10^4`; `s` and `p`
consist of lowercase English letters.

## Approaches

Every arm takes `s` and `p` as `Str` and returns the starts in
ascending order, so the arms agree line for line.

| file | mechanism |
|---|---|
| `find_anagrams.kara` ★ | a sliding window over the bytes with one table of 26 differences between p's counts and the window's, and a count of the letters that differ. Each step changes two entries and updates that count in O(1). O(n + m) |
| `find_anagrams_compare.kara` | the same window with two count tables, compared in full (`Vec` equality) at every step. O(26 n) |
| `find_anagrams_sorted.kara` | two strings are anagrams when their letters sorted are equal: sort p's bytes once and every window's bytes, and compare. O(n m log m): the plain reference |
| `find_anagrams_map.kara` | the window and p as `Map`s from letter to count, an emptied letter removed, compared entry by entry at each step. Works for any bytes, not only `a` to `z`. O(n m) at worst |
| `differential.kara` | the four arms on 1,500 random pairs, five properties |

Every arm prints the same 10 lines: the two LeetCode examples, seven
edge cases (one letter found, a p longer than s, overlapping runs of
one letter, p the whole of s reversed, every window an anagram, no
letter of p in s, and an anagram only at the end), and for 300 random
pairs over a 1, 2, 3 or 26 letter alphabet the number of starts found
and a checksum of them. `find_anagrams.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random pairs over a 1, 2, 3 or 26 letter alphabet: `s` of 0 to
60 letters and `p` of 1 to 7, half the time a shuffled window of `s`
so that most cases have an answer.

| | property |
|---|---|
| P1 | the starts are the reference's, which counts each of the 26 letters in every window and in p |
| P2 | renaming the letters of both strings by one random permutation of the alphabet gives the same starts |
| P3 | reversing both strings mirrors the starts, i to n - m - i |
| P4 | appending p reversed to s keeps every start found in s and adds one at n |
| P5 | a run of k copies of one letter holds a run of j at every one of its k - j + 1 starts, a run shorter than p holds it nowhere, and the empty string holds nothing |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | one table: a letter leaving never closes a difference | P1 1170, P3 1153, P4 1481, P5 1329 |
| M2 | one table: the first window is never reported | P1 557, P3 581, P4 19, P5 1500 |
| M3 | two tables: the entering letter is the window's old last | P1 810, P3 799, P4 759 |
| M4 | two tables: the first window counts each letter twice | P1 1201, P3 1201, P4 1500, P5 1500 |
| M5 | sorted: p's letters reversed instead of sorted | P1 521, P2 118, P3 515, P4 738 |
| M6 | sorted: the last window is never tried | P1 581, P3 557, P4 1500, P5 1500 |
| M7 | maps: an emptied letter stays in the window's map | P1 432, P3 412, P4 655 |
| M8 | maps: the comparison checks letters, not counts | P1 450, P3 450 |

P2 renames the letters of both strings alike, and every mutant but M5
treats all letters alike, so only M5, whose reversed key depends on
the order of the letters, fails it. P5's runs use one letter, which
none of M3, M5, M7 or M8 can get wrong: one letter has no order, no
other letter to enter, never empties mid-run, and has only one count.
P4 misses M8 for the same reason P5 does: appending p reversed adds a
window with exactly p's counts, which M8's letters-only test also
accepts.

## Verification

All four arms print the same output as `find_anagrams.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends:

- The window, two-table and sorted arms match under
  `karac run --interp`. LLJIT, `karac build` and
  `KARAC_AUTO_PAR=1 karac build` refuse them, the bench program
  included: the legacy code generator has no `bytes()` on a `Str`
  parameter, as in kata 430.
- The map arm and the differential do not typecheck there: the legacy
  checker types `Map.iter()` items as values and refuses `*letter`.

Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds one random text of
1,000,000 letters from `a` to `d` once, so that short patterns have
many anagrams in it, then searches it for 40 random patterns of 1 to
12 letters from the same four, folding every start into a checksum.
Every implementation prints `40 patterns in a text of 1000000: 1919557
anagrams, checksum 612665160`; a 2-pattern cut of the Kāra program
under `karac __mir-run` prints the same as the C program cut the same
way.

C writes the starts into one array allocated up front; the others push
onto a growing vector. Spot timings on a shared 4-core container, three
runs each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.11 s |
| Rust (`rustc -O`) | 0.13 to 0.14 s |
| Go | 0.25 to 0.29 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.54 to 0.57 s |
| Python | 9.5 to 10.0 s |

The overflow checks cost Rust four times its unchecked time here: the
loop body is a handful of counter updates, each now checked, which is
the equal-safety comparison BENCHMARKS.md describes. The frozen legacy
`karac build` cannot build the program (see Verification), so there is
no legacy time. The Kāra program prints the same line under
`karac __mir-llvm-run` in 1.6 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark.

## Compiler findings

One new finding, filed as kara B-2026-10-12-22.

- **B-2026-10-12-22.** The map arm compares the two maps entry by entry
  and first wrote `if b.get(*letter) != Some(*count)`, comparing the
  `Option[ref i64]` that `get` returns with an `Option[i64]`.
  `karac check` accepts that; `karac __mir-run` refuses it ("cannot
  compare 'Option[ref i64]' and 'Option[i64]'"), and `karac check`
  refuses the same comparison on `Vec.get`. `Option`'s equality needs
  both sides of one type, so check is the side in the wrong. The arm
  writes `Some(count)`, with `count` the `ref i64` item, which compares
  `Option[ref i64]` with itself and is accepted everywhere.

Not filed: the map arm first compared the maps with `==`, and
`karac check` says `Map[u8, i64]` does not implement `PartialEq`. The
library gives equality to the sequences (`Vec`, `Array`, `Slice`,
`VecDeque`) and not to `Map` or `Set`, so that is the specified
behaviour, and the arm compares entries itself.
