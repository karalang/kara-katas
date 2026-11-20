# 1239. Maximum Length of a Concatenated String with Unique Characters

You are given an array of strings `arr`. A string `s` is formed by the
**concatenation** of a **subsequence** of `arr` that has **unique
characters**.

Return *the **maximum** possible length* of `s`.

A **subsequence** is an array that can be derived from another array by
deleting some or no elements without changing the order of the
remaining elements.

```
arr = ["un","iq","ue"]                  ->  4    ("uniq" or "ique")
arr = ["cha","r","act","ers"]           ->  6    ("chaers" or "acters")
arr = ["abcdefghijklmnopqrstuvwxyz"]    ->  26
```

**Constraints:** `1 <= arr.length <= 16`; `1 <= arr[i].length <= 26`;
`arr[i]` contains only lowercase English letters.

The arms are `fn max_length(arr: Vec[String]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `maximum_length_of_a_concatenated_string_with_unique_characters.kara` ★ | backtracking over bitmasks: each word with no repeated letter becomes a 26-bit mask (`mask_of` gives `None` for one that repeats a letter, and `filter_map` drops it), and a search over the words in order either skips a word or takes it when its mask is disjoint from the letters taken so far. The answer is the most bits ever set (`count_ones`). O(2^n) |
| `maximum_length_of_a_concatenated_string_with_unique_characters_grow.kara` | every reachable letter set, grown a word at a time: the sets so far, and each of them joined with the word's mask when the two share no letter. O(n 2^n) at worst |
| `maximum_length_of_a_concatenated_string_with_unique_characters_subsets.kara` | every subset of the words, by the bits of a counter: a subset counts when its words' total length equals the number of letters in the union of their letter sets, since only then is no letter used twice, within a word or across two. O(n 2^n) |
| `maximum_length_of_a_concatenated_string_with_unique_characters_concat.kara` | backtracking on the strings themselves: from each prefix of the concatenation, every later word appended, a branch stopped as soon as the string repeats a letter (a `SortedSet` of its chars is shorter than it). O(2^n) strings |
| `maximum_length_of_a_concatenated_string_with_unique_characters_masks.kara` | a Rust solution as LeetCode's Rust users write it (a `vec![0u32]` of letter masks grown over `arr.iter()`, each word's mask from `s.bytes()` with `1 << (b - b'a')`, the best by `count_ones() as i32`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's three examples (`4`, `6`,
`26`) and two words that each repeat a letter (`0`); a checksum of the
answers for 1000 random lists of 1 to 16 words of 1 to 6 letters, drawn
from the first 8 to 26 letters of the alphabet so that words share and
repeat letters (`346046117`); and three lists at the constraints' top, 16
words of one letter each, 16 random words of up to 4 letters, and 16
copies of the alphabet (`16, 17, 26`).
`maximum_length_of_a_concatenated_string_with_unique_characters.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the four Kāra arms check clean as written. The masks arm
takes one round of 7 fixes (`Vec<String>` to `Vec[String]`, `vec![0u32]`
to `[0u32]`, `!ok` to `not ok`, `struct Solution;` to `struct Solution
{}`, and the two literals typed: `let mut best: i32 = 0` for the `i32`
it is compared with, and `let bit: u32` for the `u32` mask it is or-ed
into) and checks clean.

## Gaps

A common Rust solution, a `fn dfs` nested in the method that checks the
string so far with `let set: std::collections::HashSet<char> =
s.chars().collect();`, is held out of the kata. `karac fix` carries the
rest in one round of 11 fixes (it hoists the nested `fn`, writes
`&Vec<String>` as `ref Vec[String]` and `String::new()` as
`String.new()`), then stops at the annotation with `error[E0002]:
Expected `=`, found `::`` and no fix. A `::` path in any type position
stops the parse the same way, though the bare `HashSet<char>` in a type,
and the qualified path in an expression, are both fixed (B-2026-11-19-34).

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subsequence of the words, concatenated in order, kept
when no character appears twice in it, compared character by character;
the longest. 2000 cases, a third with 1 to 6 words, a third with 7 to
10 and a third with 11 to 16, of 1 to 6 letters from the first 8 to 26
letters of the alphabet.

| | property |
|---|---|
| P1 | the statement read literally (up to 10 words) |
| P2 | from 0 to the letters there are, in the words and in the alphabet |
| P3 | the words listed backwards give the same answer |
| P4 | every letter renamed (`a` for `z`, `b` for `y`, ..) gives the same answer |
| P5 | a word with a repeated letter added gives the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 328802296,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, with every
case read literally, up to 16 words, gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a word taken though it shares a letter | P1 821, P6 5728 |
| S2 | ★: a word cut short at its first repeated letter | P1 720, P5 1496, P6 4560 |
| G1 | grow: a word with a repeated letter kept | P1 738, P5 1491, P6 1143 |
| G2 | grow: a set joined with a word sharing some, not all, of its letters | P1 821, P6 1432 |
| U1 | subsets: one letter used twice allowed | P1 1110, P2 69, P5 409, P6 1766 |
| U2 | subsets: the subset of every word left out | P1 119, P5 119, P6 119 |
| C1 | concat: the word right after the last one taken skipped | P1 894, P3 916, P6 1336 |
| C2 | concat: a string with a repeated letter counted one short | P1 1072, P2 275, P3 1436, P5 283, P6 1717 |
| R1 | masks: a word with a repeated letter kept, cut at it | P1 720, P5 1496, P6 1140 |
| R2 | masks: the empty set never joined | P1 1281, P6 1947 |

All ten are caught, each by P1, the statement read literally, though P1
reads only the two thirds of cases with up to 10 words, so its counts
are the smaller. Four of the ten answer a word with a repeated letter
wrongly: the ★ arm cutting such a word short at the repeat (S2), the grow
arm keeping it (G1), and the masks arm keeping it cut at the repeat (R1)
give an answer that changes when `"qq"` is added, which P5 catches, and
the subsets arm that lets one letter be used twice (U1) does too. P2, the
answer between 0 and the letters there are, catches only the mutations
that can count past them: a letter used twice (U1) and a string with a
repeated letter counted one short instead of not at all (C2). P3, the
words listed backwards, catches the two that depend on the order the
words come in, the concat arm skipping the word right after the last one
taken (C1) and counting a repeated string (C2). P4, every letter renamed,
catches none, as expected: each mutation is blind to which letters are
which. The subsets arm that leaves out the subset of every word (U2)
fails only the 119 cases whose answer takes every word.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (backtracking over 26-bit masks) on 20000 lists of 16 random words
of 1 or 2 letters, built once; prints the total of the answers and a
checksum of them. Every program prints `20000 lists of 16 words: total
296692, checksum 829187823`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.868 to 1.064 s | 0.938 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.870 to 1.055 s | 0.923 s |
| Rust (`rustc -O`) | 0.853 to 0.977 s | 0.918 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.851 to 0.963 s | 0.907 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.832 to 1.139 s | 0.861 s |
| C (`clang -O3`) | 0.970 to 1.164 s | 1.052 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.821 to 1.039 s | 0.850 s |
| Go | 1.000 to 1.157 s | 1.044 s |
| Python | 57.37 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.907 s
against 0.923 s), and the two ranges overlap. Kāra is about 12% ahead of
C (0.923 s against 1.052 s); Kāra is about 12% ahead of Go (0.923 s
against 1.044 s). Python takes about 62x Kāra's time. No profile was
taken.
