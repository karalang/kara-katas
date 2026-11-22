# 2781. Length of the Longest Valid Substring

You are given a string `word` and an array of strings `forbidden`.

A string is called **valid** if none of its substrings are present in
`forbidden`.

Return *the length of the **longest valid substring** of the string*
`word`.

A **substring** is a contiguous sequence of characters in a string,
possibly empty.

```
word = "cbaaaabc", forbidden = ["aaa", "cb"]       ->  4
word = "leetcode", forbidden = ["de", "le", "e"]   ->  4
```

**Constraints:** `1 <= word.length <= 10^5`, `word` consists only of
lowercase English letters, `1 <= forbidden.length <= 10^5`, `1 <=
forbidden[i].length <= 10`, `forbidden[i]` consists only of lowercase
English letters.

## Approaches

A valid window ending at j starts after the last start of a forbidden
word inside it, and a forbidden word has at most 10 letters, so only
the 10 substrings ending at j can move the start.

| file | mechanism |
|---|---|
| `valid.kara` ★ | the forbidden words in a `Set[String]`; for each end j the substrings ending there of up to 10 letters asked of the set from the shortest, borrowed from the word, and the window's start moved past the first found. O(n * L^2), L = 10 |
| `valid_trie.kara` | the forbidden words written backwards into a trie, each node 26 slots of a `Vec[i64]`, and from each end j the trie walked back over the word's bytes while the window allows. O(n * L) |
| `valid_ends.kara` | from the starts: the earliest end of a forbidden word starting at each i, its lengths asked of a `Set[String]`, and from the right the first forbidden end at or after i, the least of its own and the next start's; the longest valid substring from i stops just before it. O(n * L^2) |
| `valid_codes.kara` | no strings hashed: a word of up to 10 letters read as a number in base 27, its letters the digits 1 to 26 from the last, so different words are different numbers below `27^10`; the forbidden ones in a `Set[i64]`, and each substring's number built a letter at a time going back. O(n * L) |
| `valid_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashSet<String>` from `forbidden.into_iter().collect()` and the starts from j down to `i.max(j.saturating_sub(9))` asked by `contains(&word[k..=j])`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one letter
forbidden and one not; `10^5` a's, LeetCode's longest word, against
"aa" and against "b"; 3000 random words of 1 to 30 letters from a, b
and c against 1 to 10 forbidden of 1 to 4; and 3 of `10^5` letters from
a to e against `10^5` forbidden of 8 to 10, LeetCode's most, the last
two with the sum of the lengths and a checksum. `valid.py` mirrors the
★ arm and its output is byte-identical.

```
4
4
0
1
1
100000
3000 small cases: lengths sum to 13873, checksum 979764822
3 cases of 10^5: lengths sum to 269, checksum 95102
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring of the word, kept when no forbidden word is
found in it by `contains`, and the longest kept; no window and no set.
It draws 2000 random cases, words of 1 to 12 letters from a, b and c
against 1 to 6 forbidden of 1 to 3, or every fourth one from a and b
against 1 to 3 forbidden of 6 to 10; then 50 of up to 2000 letters from
2 to 4 against up to 200 forbidden of 1 to 10, all before any arm
answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 letters, the answer is the literal reading's |
| P2 | the word and every forbidden word reversed: the same answer |
| P3 | a forbidden "z", a letter no word holds: the same answer |
| P4 | a "z" put after the word: the same answer or one more |
| P5 | from 0 to n; n just when no forbidden word is in the word, and 0 just when every letter of it is forbidden alone |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 834940149, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same substrings gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1, M6 and M9 each change only words of 10
letters, which the random cases rarely hold: each is killed by one case
of 2050.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: substrings of up to 9 letters asked | P1 1, P5 1, P6 1 |
| M2 | ★: the start moved onto a forbidden word, not past it | P1 962, P2 481, P5 278, P6 1012 |
| M3 | trie: the words written in forwards | P1 249, P5 104, P6 251 |
| M4 | trie: the start moved one letter too far | P1 448, P2 574, P5 71, P6 454 |
| M5 | ends: only the nearest start's end kept | P1 23, P2 49, P6 32 |
| M6 | ends: forbidden words of 10 letters never asked | P1 1, P5 1, P6 1 |
| M7 | codes: the substrings' letters read as 0 to 25 | P1 1091, P5 607, P6 1141 |
| M8 | codes: the substrings read in base 26 | P1 391, P2 163, P5 232, P6 402 |
| M9 | solution: starts no further back than j - 8 | P1 1, P5 1, P6 1 |
| M10 | solution: each window counted one letter short | P1 1843, P5 1075, P6 1861 |

## Benchmarks

The bench draws 10 words of `10^5` letters from a to e, each against
`10^5` forbidden words of 8 to 10 letters, LeetCode's most, all of them
first, then answers each 5 times by the ★ arm in all five languages,
every answer building its own set of copies: Kāra's `Set[String]`,
Rust's `HashSet<String>`, a Go map, a Python set, and in C an
open-addressing table of copied strings, FNV-1a hashed and probed
linearly. Each lookup is a slice of the word, copied by none of them.
Every implementation prints `10 words of 10^5, 5 rounds: lengths sum to
4955, checksum 995981152`.

BENCHTAB

## Verification

All five arms print the same output as `valid.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Two of the own arms took `karac fix` edits as first written, each the
same two: Rust's `w.bytes().rev()`, refused since `bytes()` gives a
`Slice` and its adaptors are reached by `.iter()`, became
`w.bytes().iter().rev()`; and a `u8` cast `as i64` where it widens by
itself lost its cast, in the trie's index and the codes' sums. The
codes arm's closure also declared `-> i64`, Rust syntax, and the fix
removed it.

LeetCode's Rust template took 13 `karac fix` edits, the wrapper
included: `use std::collections::HashSet` became `struct Solution {}`;
the `Vec<String>`s became `Vec[String]`; `HashSet<String>` became
`Set[String]`; `forbidden.into_iter()` became
`forbidden.clone().into_iter()`, the parameter being borrowed;
`contains(&word[k..=j])` dropped its `&`; and `Solution::` became
`Solution.`, with the wrapper's `as i64` dropped. `j.saturating_sub(9)`
and the `ans as i32` stayed.
