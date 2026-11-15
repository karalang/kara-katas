# 1160. Find Words That Can Be Formed by Characters

You are given an array of strings `words` and a string `chars`.

A string is good if it can be formed by characters from `chars` (each
character can only be used once for each word in `words`).

Return the sum of lengths of all good strings in `words`.

```
words = ["cat","bt","hat","tree"], chars = "atach"            ->  6
words = ["hello","world","leetcode"], chars = "welldonehoneyr" ->  10
```

**Constraints:** `1 <= words.length <= 1000`; `1 <= words[i].length,
chars.length <= 100`; `words[i]` and `chars` consist of lowercase
English letters.

The arms are `fn count_characters(words: Vec[String], chars: Str) -> i64`.

## Approaches

A word is good exactly when, letter by letter, it needs no more of a
letter than `chars` holds; the order of either string does not matter.

| file | mechanism |
|---|---|
| `count_characters.kara` ★ | counts of each letter in fixed arrays of 26 (`[0; 26]`): `chars` counted once, each word counted until a letter outruns `chars`. O(\|chars\| + total letters) |
| `count_characters_take.kara` | each word takes letters from a clone of `chars`'s counts, over `chars()` and `char` arithmetic, good when `all` of them were there; the good words' lengths summed by `filter`, `map` and `sum` |
| `count_characters_sorted.kara` | `chars` sorted once and each word sorted; a merge walk checks the word's letters are a sub-multiset of `chars`'s. O(\|chars\| log \|chars\| + sum of \|w\| log \|w\|) |
| `count_characters_map.kara` | `chars` and each word tallied into a `Map[char, i64]` with `entry().or_insert`; a word is good when every letter's tally is at most `chars`'s, a missing letter counting 0 |
| `count_characters_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `[i32; 26]` counts indexed by `(b - b'a') as usize`, `as_bytes()`, a labelled `continue 'outer`, the lengths summed as `i32`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, seven properties |

Every arm prints the same 11 lines: LeetCode's examples (6, 10); a word
needing a letter twice that `chars` holds once (`["aa", "a"]`, `"ab"`:
1); a word equal to `chars` beside one longer (`["abc", "cba",
"abcd"]`, `"abc"`: 6); one letter, missing and present (0, 1); a word
repeated, each use counted (`["ab", "ba", "ab"]`, `"ab"`: 6). Then 2000
random problems of 1 to 20 words of 1 to 10 letters and `chars` of 1 to
30, over the first 1 to 6 letters or all 26 (`2000 random problems:
total 57400, checksum 375665263`), and 1000 words with `chars` of 100
letters, the most the constraints allow: words of 1 to 100 letters over
26 letters (1272) and over 3 (38271), and every word `chars` itself
(100000). `count_characters.py` mirrors the ★ arm and its output is
byte-identical; a Python reading that removes each letter of a word
from a list of `chars`'s letters gives the same output.

The Mend loop: the ★, take and sorted arms check clean as written. The
map arm takes one fix, `copied()` to `cloned()` on the `Option` that
`Map.get` returns. The Rust arm takes three rounds (5, 1 and 4 edits):
`Vec<String>` to `Vec[String]`, `for &b in s.as_bytes()` to `for b in
s.bytes()`, `Solution::` to `Solution.`, then `struct Solution {}`,
then `ans` annotated `i32` and the adapter's `as i64` dropped. The
labelled `continue 'outer`, the `[0i32; 26]` arrays and the `as usize`
indices are kept as written. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each letter of a word matched to the first place of `chars`
not yet used. It checks 1600 problems in four kinds of 400: 1 to 8 words
of 1 to 6 letters and `chars` of 1 to 12 over the first 1 to 4 letters;
1 to 20 words of 1 to 10 letters and `chars` of 1 to 30 over the first 2
to 6; 1 to 12 words each drawn from `chars` (each place kept with odds
one in two, shuffled), half of them given one more of a letter they
took, so they fail by one; and 10 to 40 words of 1 to 100 letters over
26 with `chars` of 100, a third of them drawn from `chars` the same way.
The literal reading runs on the first three kinds. Every random choice
the properties make is drawn before any arm answers.

| | property |
|---|---|
| P1 | the total is the literal one (the first three kinds) |
| P2 | the words reordered give the same total |
| P3 | the letters of every word and of `chars` renamed by one permutation of the 26 give the same total |
| P4 | `chars` shuffled gives the same total |
| P5 | the words split in two at a random place: the two parts' totals add to the whole |
| P6 | a random letter added to `chars` never lowers the total |
| P7 | `chars` itself added as one more word adds its length |
| P8 | a letter `chars` lacks, appended to one word, takes away exactly that word's own total |

All 60,835 checks pass on every arm: `1600 problems: checksum
226223028, 60835 checks over 5 arms: 0 failures`, in 29 s under `karac
__mir-run`. A Python reading of the same draws, with the mirror against
the letter-removal reading, gives the same checksum.

## Mutation testing

Nineteen edits to the differential, three to five to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run` with
`KARAC_HASH_SEED=1`, each failing the same way under both. Seventeen
are caught and two are equivalent: the ★ arm's count walking on past
the letter that outruns `chars` (C5) only spends time, since that word
is already marked bad; and the map arm's tallies each started at 1 (M2)
raise a word's count and `chars`'s alike, while a letter `chars` lacks
still meets 0.

| # | mutation | failures by property |
|---|---|---|
| C1 | ★: a letter used as often as `chars` holds it refused | P1 766, P7 1600 |
| C2 | ★: `chars` holds each letter once | P1 870, P7 1440 |
| C3 | ★: good words counted, not their letters | P1 975, P7 1531 |
| C4 | ★: a word's counts carried into the next | P1 900, P2 978, P5 666, P6 3, P7 1582, P8 570 |
| T1 | take: the last of a letter refused | P1 766, P7 1600 |
| T2 | take: one letter in hand is enough | P1 786, P8 1340 |
| T3 | take: `chars` counted twice | P1 613 |
| S1 | sorted: the walk skips the letter it wants | P1 1062, P7 1600 |
| S2 | sorted: a letter of `chars` used again | P1 657 |
| S3 | sorted: the word not sorted | P1 812, P3 344, P7 1371 |
| S4 | sorted: `chars` not sorted | P1 845, P3 342, P4 336, P7 1371 |
| M1 | map: a letter `chars` lacks counted once | P1 156, P8 892 |
| M3 | map: a letter used as often as `chars` holds it refused | P1 766, P7 1600 |
| X1 | solution: one letter too many allowed | P1 713, P8 1086 |
| X2 | solution: the inner loop continued, the word still counted | P1 792, P8 1367 |
| X3 | solution: a word's counts carried into the next | P1 900, P2 978, P5 666, P6 3, P7 1582, P8 570 |
| X4 | solution: each good word one short | P1 1062, P7 1600 |

P1 catches all seventeen, P7 eleven, P8 six, P3 two, P2, P5 and P6 two
each (the carried counts), and P4 one. The edits that allow too much
(T3, S2) are seen only by P1: a word given extra letters stays
consistent with every reordering, renaming, split and addition, and
`chars` as a word still fits. Those two, and the third kind's words that
fail by one letter, are why the literal reading runs on the drawn kinds.

## Benchmarks

`bench/` times the ★ arm against the same fixed-array counts in C, Rust,
Go and Python. 12 problems of 1000 words, the most the constraints
allow, are built once, each with `chars` of 100 letters, in three kinds
in turn: words of 1 to 100 letters over 26 (most fail within a few
letters), words of 1 to 30 letters over 4 with `chars` over 4, and words
drawn from `chars` with every other one given one letter too many. Each
of 1500 passes answers all 12. Every program prints `1500 passes over
12 problems of 1000 words: checksum 427478559`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `77ed9881fc`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.379 to 0.413 s | 0.389 s |
| C (`clang -O3`) | 0.425 to 0.517 s | 0.433 s |
| Rust (`rustc -O`) | 0.453 to 0.532 s | 0.465 s |
| Go | 0.481 to 0.538 s | 0.519 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.573 to 0.660 s | 0.597 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.577 to 0.700 s | 0.612 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.630 to 0.759 s | 0.657 s |
| Kāra (`karac build`) | 0.635 to 0.733 s | 0.666 s |
| Python | 27.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, byte
for byte, so the two Kāra rows are one program timed twice. Kāra takes
about 1.07x overflow-checked Rust's time, the equal-safety comparison.
The checks cost this loop: overflow-checked Rust is 1.3x unchecked
Rust, and C and Go, which check neither the counts nor (C) the indices,
take about 0.6x to 0.8x Kāra's time. Python takes about 42x.
