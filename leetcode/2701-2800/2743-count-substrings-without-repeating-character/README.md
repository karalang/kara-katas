# 2743. Count Substrings Without Repeating Character

You are given a string `s` consisting only of lowercase English letters.
We call a substring **special** if it contains no character which has
occurred at least twice (in other words, it does not contain a repeating
character). Your task is to count the number of **special** substrings.
For example, in the string `"pop"`, the substring `"po"` is a special
substring, however, `"pop"` is not special (since `'p'` has occurred
twice).

Return *the number of **special** substrings.*

A **substring** is a contiguous sequence of characters within a string.
For example, `"abc"` is a substring of `"abcd"`, but `"acd"` is not.

```
s = "abcd"  ->  10
s = "ooo"   ->  3
s = "abab"  ->  7
```

**Constraints:** `1 <= s.length <= 10^5`, `s[i]` consists of lowercase
English letters.

## Approaches

Every substring of a special substring is special, so the special
substrings ending at i are exactly those starting no earlier than the
longest one's start, and that start never moves back as i grows.

| file | mechanism |
|---|---|
| `substrings.kara` ★ | a window over the bytes with each letter's last place in an `Array[i64, 26]`: the window's start moves past the last time the new letter was seen, and each i adds the window's length. O(n) |
| `substrings_counts.kara` | two pointers over a `Vec[char]` with a count of each letter in the window, the left end moved on one letter at a time while the new letter is in it twice. O(n) |
| `substrings_set.kara` | the window's letters kept in a `Set[char]`, a letter already there pushing the left end on until it is not; each end adds the set's size. O(n) |
| `substrings_runs.kara` | no window: from each start, letters taken until one comes twice, those seen kept as a bit mask; a special substring holds at most 26 letters, so each start looks at most 27 ahead. O(26 n) |
| `substrings_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashMap<char, usize>` of last places, `chars().enumerate()` and `if let Some(&j) = last.get(&c)`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one letter;
a word that repeats; the alphabet, every substring special; 2000 random
words of 1 to 30 letters from the first 1 to 26 of the alphabet; and 20
of `10^5` letters, LeetCode's longest, each batch with the sum of its
answers and a checksum. `substrings.py` mirrors the ★ arm and its output
is byte-identical.

```
10
3
1
7
351
2000 small words: counts sum to 106929, checksum 302554578
20 words of 100000 letters: counts sum to 8089729, checksum 713735501
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring, from every start to every end, looked at
letter by letter against every other letter in it, and counted when no
two are the same; no window. It draws 1000 random words of 1 to 20
letters from the first 1 to 26 of the alphabet, then 200 of up to 2000
letters, all before any arm answers; the literal reading is asked only
of the first 1000.

| | property |
|---|---|
| P1 | up to 20 letters, the answer is the literal reading's |
| P2 | the word reversed: the same answer |
| P3 | every letter moved on 7 places round the alphabet: the same answer |
| P4 | at least the word's length, at most 26 for each of its letters |
| P5 | another word put after it: at least the two answers added |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1200 cases: checksum 764036077, 36000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, a `set` of each substring's letters, gives
the same checksum. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M2 and M6 fail the same checks, both counting
each window one short; M4 and M5 do, both keeping the letter that left
in the window; and M7 and M10 do, both taking one letter too many.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the window's start moved back as well as on | P1 670, P2 833, P6 864 |
| M2 | ★: each end adds the window less one | P1 1000, P4 287, P6 1200 |
| M3 | counts: a letter twice allowed in the window | P1 779, P6 979 |
| M4 | counts: the leaving letter's count taken from the new one | P1 672, P2 833, P6 866 |
| M5 | set: the window's left letter left in the set | P1 672, P2 833, P6 866 |
| M6 | set: counted before the new letter goes in | P1 1000, P4 287, P6 1200 |
| M7 | runs: one letter more than the run taken | P1 779, P2 752, P6 979 |
| M8 | runs: two letters to a bit | P1 693, P3 920, P6 887 |
| M9 | solution: a letter last seen before the window still moves it | P1 473, P2 559, P6 665 |
| M10 | solution: the window's left end on the repeat itself | P1 779, P2 752, P6 979 |

## Benchmarks

The bench draws 20 words of `10^5` letters, LeetCode's longest, each
from the first 5 to 26 of the alphabet, all of them first, then answers
each 300 times by the ★ arm in all five languages. Every implementation
prints `20 words of 100000 letters, 300 rounds: counts sum to
2646441300, checksum 587890317`.

BENCHTAB

## Verification

All five arms print the same output as `substrings.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The set arm checked clean as first written. The ★ and runs arms wrote
Rust's `s.as_bytes()`; `karac check` says a string's bytes are
`.bytes()`, and `karac fix` made it so. The counts arm cast a letter's
place to `i64` for an index, `(c as u32 - 'a' as u32) as i64`; `karac
check` warns that a `u32` widens to `i64` by itself there, and `karac
fix` dropped the cast.

LeetCode's Rust template took one `karac fix` of 14 edits, the wrapper
included: the `use std::collections::HashMap` became `struct Solution
{}`, `HashMap<char, usize>` and `HashMap::new()` became `Map[char, i64]`
and `Map.new()`, `let mut ans = 0` gained `: i32`, `if let Some(&j) =
last.get(&c)` became `if let Some(j) = last.get(c).cloned()`, and
`Solution::` became `Solution.` with the `as i64` dropped.
