# 2068. Check Whether Two Strings are Almost Equivalent

Two strings `word1` and `word2` are considered almost equivalent if the
differences between the frequencies of each letter from `'a'` to `'z'`
between `word1` and `word2` is at most `3`.

Given two strings `word1` and `word2`, each of length `n`, return `true`
if `word1` and `word2` are almost equivalent, or `false` otherwise.

The frequency of a letter `x` is the number of times it occurs in the
string.

```
word1 = "aaaa", word2 = "bccb"            ->  false  (4 a's against none)
word1 = "abcdeef", word2 = "abaaacc"      ->  true
word1 = "cccddabba", word2 = "babababab"  ->  true
```

**Constraints:** `n == word1.length == word2.length`; `1 <= n <= 100`;
`word1` and `word2` consist only of lowercase English letters.

One pass over each word, counting the first's letters up and the
second's down, leaves each letter's difference; the words are almost
equivalent when none is past 3 either way. O(n + 26). The approaches
differ in where they keep the differences, and two keep none at all.

## Approaches

| file | mechanism |
|---|---|
| `almost.kara` ★ | one `Array[i64, 26]` of differences over the two words' `bytes()`, checked with `all(\|d\| d.abs() <= 3)`. O(n + 26) |
| `almost_map.kara` | the differences in a `Map[char, i64]` over `chars()`, only the letters the words hold ever keys, checked with `values().all(..)` |
| `almost_sorted.kara` | both words' letters sorted, then walked together a run at a time: the smaller letter still ahead in either word, its run measured in each by a helper, the two lengths compared. O(n log n) |
| `almost_each.kara` | one letter of the alphabet at a time, each word's count of it taken with `filter` and `count`, all inside one `all` over the alphabet's `chars()` that stops at the first letter too far apart. O(26 n) |
| `almost_fold.kara` | the words are as long as each other, so a `zip` of their bytes folded into a `Vec` of differences, each pair moving one letter up and one down; the largest difference either way by `map` and `max` |
| `almost_solution.kara` | LeetCode's Rust template (a `[0i32; 26]` of counts, `c as u8 - b'a'` to a `usize` index over `chars()`, `cnt.iter().all(\|&x\| x.abs() <= 3)`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and five
more, each pair and its answer; then how many of 1000 random pairs are
almost equivalent and a checksum of their answers in order, each pair 1
to 100 letters from the first 1 to 26 of the alphabet, the second word
either drawn afresh or the first with 0 to 24 letters changed.
`almost.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each of the 26 letters, its count in each word found by a
walk over that word, and the words almost equivalent when no two counts
are more than 3 apart. It checks 300 random pairs of 1 to 40 letters
from 1 to 6 kinds, drawn as the harness draws them; then 20 from all 26
letters, and 20 whose second word has exactly 3 or 4 more of one letter
than the first, the edge the statement turns on. All 340 are drawn
before any arm answers; 259 are almost equivalent.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the words swapped have the same answer |
| P3 | the letters renamed in a cycle (`a` to `b`, ..., `z` to `a`) leave the answer |
| P4 | the same letter added to both words, and the first word reversed, leave the answer |
| P5 | a word is almost equivalent to itself, and not to itself with four of one letter added against four of another |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 pairs: 259 almost equivalent, checksum
600503722, 12240 checks over 6 arms: 0 failures` under every lane in
Verification; the count and checksum of the literal answers were checked
against a Python reading of the same pairs. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, four to six to each of its arms, each
run under `karac __mir-llvm-run`, and the kept ones and the survivor
under `karac __mir-run` too. Seventeen are kept, three to each Kāra arm
and two to the Rust-template arm. Each kept one is killed, fails the
same way under both backends and not by a crash, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: three apart refused | P1 64, P6 64 |
| M2 | ★: a `z` in the first word not counted | P2 1, P3 2 |
| M3 | ★: the second word's first letter skipped | P1 15, P2 24, P6 15 |
| M4 | map: three short refused | P1 53, P2 38, P6 53 |
| M5 | map: a letter only in the second word not counted down | P1 4, P2 4, P6 4 |
| M6 | map: an `a` in the first word counted twice | P1 153, P2 74, P3 156, P5 200, P6 153 |
| M7 | sorted: four apart allowed | P1 41, P5 340, P6 41 |
| M8 | sorted: the second word left unsorted | P1 144, P2 22, P4 1, P5 213, P6 144 |
| M9 | sorted: the walk stopped when one word is done | P1 2, P3 1, P4 1, P6 2 |
| M10 | each: `z` never looked at | P1 1, P3 2, P6 1 |
| M11 | each: the second count taken from the first word | P1 81, P5 340, P6 81 |
| M12 | each: the first count of every letter up to it | P1 241, P4 6, P5 322, P6 241 |
| M13 | fold: only the first word's surplus checked | P1 29, P2 44, P6 29 |
| M14 | fold: the words paired one letter apart | P1 19, P2 39, P4 28, P5 15, P6 19 |
| M15 | fold: the first pair left out | P1 14, P4 21, P6 14 |
| M16 | solution: the second word counted up too | P1 232, P5 319, P6 232 |
| M17 | solution: the adapter's second word with every `a` a `b` | P1 167, P2 35, P3 167, P4 1, P5 200, P6 167 |

P1 and P6 kill sixteen each, P2 nine, P5 eight, P4 six and P3
five. M2 is the one P1 misses: a `z` comes up in few of the pairs, and
never where it decides the answer, but P2 sees the answer change when
the words swap and P3 when renaming moves `y` onto `z`. P5's second half
sees an arm that allows four apart or never counts the second word
down (M7, M11, M16); P2 an edit that treats the two words differently;
P3 an edit that tells one letter from another (M2, M6, M9, M10, M17),
which no correct arm does; P4, which reverses the first word, the fold
arm's edits that pair letters by place (M14, M15).

Of the thirty, thirteen were not kept. One survives, and it is
equivalent: the sorted arm taking a letter both words are at from the
first word, which is the same letter. Ten fail as a kept one: the each
and fold arms' three apart refused as M1; the ★, map and sorted arms'
first word's surplus only as M13; the ★ arm's second word counted up as
M16; the Rust arm's four apart allowed as M7; the each arm's one letter
close enough, the fold arm's second letters taken from the first word,
and the Rust adapter's second word the first, as M11. Two are killed
with checks of their own but were left out because their arm keeps
three: the map arm's first letter skipped (P1 13, P2 24, P4 21) and its
second word counting down only the letters the first has (P1 6, P2 7).

## Verification

Every arm prints the same output as `almost.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 0.4 s to 0.7 s, except the each
arm at 3.5 s, which walks both words once for every letter of the
alphabet, and the differential 5.9 s (timed while other work shared the
machine).

No arm met a compiler gap. The Rust arm was written as LeetCode's Rust
template. `karac fix` carries it in two rounds of 3 and 2 edits: the `&`
of `|&x|` dropped, `struct Solution;` to `struct Solution {}` and
`Solution::` to `Solution.`; then `c as u8` to `c as u32 as u8`, since a
`char` does not narrow to 8 bits in one cast. The `as usize` indices are
kept: nothing mixes them with `i64`. The fixed arm reads as the template
does.

## Benchmarks

The bench answers every pair of 1500 words with the ★ arm in all five
languages, 1124250 pairs: each word 100 letters, a common word of `a`,
`b` and `c` with up to 30 letters changed, so close to half the pairs
are almost equivalent. Every implementation prints `1124250 pairs:
525731 almost equivalent, checksum 949457206`.

BENCHTAB
