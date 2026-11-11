# 2085. Count Common Words With One Occurrence

Given two string arrays `words1` and `words2`, return the number of
strings that appear exactly once in each of the two arrays.

```
words1 = ["leetcode","is","amazing","as","is"], words2 = ["amazing","leetcode","is"]  ->  2
words1 = ["b","bb","bbb"], words2 = ["a","aa","aaa"]                                 ->  0
words1 = ["a","ab"], words2 = ["a","a","a","ab"]                                     ->  1
```

**Constraints:** `1 <= words1.length, words2.length <= 1000`; `1 <=
words1[i].length, words2[j].length <= 30`; the words are lowercase
English letters.

A word counts when it is in each list once, so each list's words are
counted, and the words the first list holds once are looked up in the
second's counts: O(n + m) with a hash map. The approaches differ in how
they keep the counts.

## Approaches

| file | mechanism |
|---|---|
| `common.kara` ★ | each list counted into a `Map[String, i64]` with `*entry(..).or_insert(0) += 1`, and the first map's words of count 1 kept by `filter` when the second's `get` is `Some(1)`. O(n + m) |
| `common_pairs.kara` | one `Map[String, (i64, i64)]` of each word's counts in the two lists, and the values equal to `(1, 1)` counted |
| `common_sorted.kara` | both lists sorted, so equal words sit together, and walked with two cursors; where both hold the same word, its runs are measured, and it counts when each is one word long. O(n log n + m log m) |
| `common_sets.kara` | each list's words met once and met again in two `Set`s, its once-words their `difference`, and the answer the `intersection` of the two lists' once-words |
| `common_scan.kara` | no map: each word of the first list looked for in both with `filter(..).count()`. O(n · (n + m)) |
| `common_solution.kara` | LeetCode's Rust template (`use std::collections::HashMap`, `HashMap<&str, i32>`, `for w in &words1`, `filter(\|(w, &c)\| .. && c2.get(*w) == Some(&1))`, `count() as i32`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more, each pair of lists and its count; then the sum and a checksum of
the counts for 300 random pairs of 1 to 100 words of 1 to 3 letters
from the first 2, 3 or 5 of the alphabet; then the count for the
constraints' largest, 1000 words a side of up to 30 letters, drawn from
1500. `common.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every word of either list, once each, counted when a walk of
each list finds it there exactly once. It checks 300 random pairs of
lists of 1 to 12 words of 1 or 2 letters from the first 2, 3 or 5 of the
alphabet; then 20 pairs of one list of words all different, the second
its reverse, and 20 pairs whose lists share no letter. All 340 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the lists swapped give the same count |
| P3 | each list reversed gives the same count |
| P4 | the first list written twice over counts 0 |
| P5 | a new word added to both lists counts one more, and added to the first alone, the same |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 pairs: checksum 598145414, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal counts was checked against a Python reading of the same
pairs. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-five edits to the differential, five to seven to each of its
arms, each run under `karac __mir-llvm-run` and `karac __mir-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends and
not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each count started at 1 | P1 188, P5 340, P6 188 |
| M2 | ★: each list's first word not counted | P1 140, P3 102, P4 59, P6 140 |
| M3 | ★: the second list's word allowed anything but twice | P1 276, P2 264, P5 340, P6 276 |
| M4 | pairs: a first-list word counted in both | P1 288, P2 257, P5 340, P6 288 |
| M5 | pairs: the second loop over the first list | P1 288, P2 259, P5 340, P6 288 |
| M6 | pairs: the second count need only be one or more | P1 99, P2 132, P6 99 |
| M7 | sorted: every run measured as one | P1 189, P4 276, P6 189 |
| M8 | sorted: the first list not sorted | P1 117, P2 143, P3 133, P4 135, P6 117 |
| M9 | sorted: the runs need only be as long as each other | P1 38, P4 71, P6 38 |
| M10 | sets: the once-words united | P1 316, P4 332, P5 340, P6 316 |
| M11 | sets: the once-words the words met again | P1 208, P4 142, P5 340, P6 208 |
| M12 | sets: the second list's once-words not in the first's | P1 285, P2 259, P4 332, P5 340, P6 285 |
| M13 | scan: the first list's word need only be there | P1 101, P2 145, P4 231, P6 101 |
| M14 | scan: a word missing from the second list counted | P1 263, P2 257, P5 340, P6 263 |
| M15 | scan: the first list's first word passed over | P1 71, P2 75, P3 69, P6 71 |
| M16 | solution: the adapter's answer at most one | P1 78, P5 188, P6 78 |
| M17 | solution: the second list's first word not counted | P1 98, P2 107, P3 93, P6 98 |

P1 and P6 kill all seventeen, P2 ten, P5 nine, P4 eight, and P3 four.
P2 sees every edit that treats the two lists differently: a count of one
asked of the first and less of the second (M3, M6, M13, M14), the
first's words written into the second's counts (M4, M5, M12), one list
left unsorted (M8) or its first word dropped (M15, M17). P4, whose
first list holds every word twice, sees an edit that lets a repeated
word through (M2, M7, M8, M10, M11, M13), asks only that the runs match
(M9), or answers from the second list's once-words (M12). P5 sees an
edit that miscounts a word met once in each list or in one: a count
started at 1 (M1), a word the second list lacks let in (M3, M14), the
first list's words in both counts (M4, M5), the once-words united or
replaced (M10, M11, M12), the answer capped (M16). P3 sees only the
edits that depend on the order of a list: a first word skipped (M2,
M15, M17) and a list left unsorted (M8).

Of the thirty-five, eighteen were not kept, and two survive. Thirteen
fail as a kept one: the ★ arm's second count asked only to be there,
the sorted arm's second run not checked, the pairs arm's second count
stopping at one and the Rust arm's second count asked only to be there
as M6; the pairs arm's first-list pair started at `(0, 1)` as M4; the
sets arm's first list met with itself, the scan arm's second count taken
in the first, the ★ arm's second list counted from the first and the
Rust adapter's second list the first as M5; the sorted arm's equal word
taken as smaller and the Rust arm's words counted twice as M1; the sets
arm's repeated words kept as M7; the sets arm's first word passed over
as M2. Three are killed with checks of their own but were left out
because their arm keeps three: the ★ arm's first count not looked at
(P1 101, P2 132, P4 231), with the same failures as the Rust arm's first
count asked to be one or more, and the scan arm's other words counted
(P1 181, P2 19, P5 318). Both survivors are equivalent: the sorted arm's
cursor into the second list left in place on a match moves on through
the next comparison, as the word is now smaller than the first list's,
and the Rust arm's second count asked to equal the first is asked to be
1, since the first must be.

## Verification

Every arm prints the same output as `common.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.5 s to 0.7 s, but for the scan
arm's 4.1 s, which walks both lists for each word of the first, and the
differential 1.2 s (timed while other work shared the machine).

The Rust arm was written as LeetCode's Rust template. `karac fix` carried
`Some(&1)` to `Some(ref 1)`, which the checker then refused
(E_REF_OPERAND_UNSUPPORTED): a literal has no place to borrow. The edit
now drops the `&` before a scalar literal, and Kāra compares the value
as it is. Fixed in kara 81aca4606b, test `tests/kata_2085_ref_literal.rs`.
With it `karac fix` carries the arm in three rounds of 24, 4 and 1
edits: Rust's spellings (`Vec<String>` and `HashMap<&str, i32>` to
brackets, `&str` to `Str`, `HashMap::new` and `Solution::` to `.`, the
`use` dropped, `&words1` to `ref words1`, the `&` of `|(w, &c)|` and of
`Some(&1)` dropped, `&&` to `and`, `struct Solution;` to `struct
Solution {}`); then `HashMap` to `Map`; then the adapter's `as i64`,
which the `i32` widens to anyway. The fixed arm reads as the template
does.

## Benchmarks

The bench builds 2500 pairs of lists of 1000 words, the constraints'
limit, each word of 1 to 4 letters from 2 to 26 letters of the alphabet,
so from nearly every word repeated to nearly none, and answers each pair
with the ★ arm in all five languages, both lists counted into a hash
map (a `Map`, a `HashMap`, a Go `map`, a `dict`, an open-addressed table
over FNV-1a in C) and the first walked: five million words counted.
Every implementation prints `2500 pairs: sum 116489, checksum
725951900`.

BENCHTAB
