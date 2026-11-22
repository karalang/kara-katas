# 2744. Find Maximum Number of String Pairs

You are given a **0-indexed** array `words` consisting of **distinct**
strings.

The string `words[i]` can be paired with the string `words[j]` if:

- The string `words[i]` is equal to the reversed string of `words[j]`.
- `0 <= i < j < words.length`.

Return *the **maximum** number of pairs that can be formed from the
array* `words`*.*

Note that each string can belong in **at most one** pair.

```
words = ["cd", "ac", "dc", "ca", "zz"]  ->  2
words = ["ab", "ba", "cc"]              ->  1
words = ["aa", "ab"]                    ->  0
```

**Constraints:** `1 <= words.length <= 50`, `words[i].length == 2`,
`words` consists of distinct strings, `words[i]` contains only lowercase
English letters.

## Approaches

The words are distinct, so a word's reverse is at most one other word,
and a palindrome's is itself: pairs never compete for a word, and the
most pairs is simply how many words have their reverse later on.

| file | mechanism |
|---|---|
| `pairs.kara` ★ | the words seen kept in a `Set[String]`; each word whose reverse, built by `chars().rev()`, was seen already makes a pair. O(n) |
| `pairs_brute.kara` | every two words, i before j, their bytes compared crosswise. O(n^2) |
| `pairs_grid.kara` | a 26 by 26 `Array` of the words seen, first letter by second; a word makes a pair when its letters crossed over were seen. O(n) |
| `pairs_sort.kara` | each word turned into the lesser of itself and its reverse, so that a word and its reverse share a key; sorted, a pair is two equal keys side by side, counted over `windows(2)`. O(n log n) |
| `pairs_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashSet` filled from `for w in words`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's three examples; one word;
25 words with their 25 reverses, LeetCode's most; and 5000 random lists
of 1 to 50 distinct words from the first 1 to 26 letters, never more
words than the letters allow, with the sum of the answers and a
checksum. `pairs.py` mirrors the ★ arm and its output is byte-identical.

```
2
1
0
0
25
5000 lists: pairs sum to 11319, checksum 262585228
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way of pairing the words, each word at most once,
searched in full for the most pairs where one word is the other
reversed; nothing assumed about pairs not competing. It draws 1000
random lists of 1 to 10 distinct words from the first 1 to 26 letters,
then 500 of up to 50, all before any arm answers; the literal reading is
asked only of the first 1000.

| | property |
|---|---|
| P1 | up to 10 words, the answer is the literal reading's |
| P2 | the list in reverse order: the same answer |
| P3 | every word reversed: the same answer |
| P4 | every letter moved on 5 places round the alphabet: the same answer |
| P5 | at most half the words; and the reverse of an unpaired word that is no palindrome added: one pair more |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1500 cases: checksum 11834910, 45000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same search gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1, M6 and M10 fail the same checks, all three
pairing a palindrome such as "aa" with itself; so do M2 and M5, both
finding no pair at all, since the words are distinct.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a word counted against itself | P1 422, P5 158, P6 801 |
| M2 | ★: the word itself looked for, not its reverse | P1 153, P5 1385, P6 452 |
| M3 | brute: one letter compared, not both | P1 515, P2 919, P3 919, P5 722, P6 937 |
| M4 | brute: neighbours never compared | P1 60, P5 115, P6 129 |
| M5 | grid: the word looked for, not crossed | P1 153, P5 1385, P6 452 |
| M6 | grid: a word marked before it is looked for | P1 422, P5 158, P6 801 |
| M7 | sort: neighbours paired on their first letter alone | P1 577, P4 106, P5 326, P6 1010 |
| M8 | sort: the keys left unsorted | P1 107, P5 1270, P6 390 |
| M9 | solution: each word counted once its reverse comes, twice | P1 153, P5 1408, P6 452 |
| M10 | solution: a word kept before its reverse is looked for | P1 422, P5 158, P6 801 |

## Benchmarks

The bench draws 20000 lists of 50 distinct words, LeetCode's most, from
the first 8 letters so that many of them pair, all of them first, then
answers each 10 times by the ★ arm in all five languages: a hash set of
the words seen, which C keeps as a small open-addressing table of
`malloc`ed strings, Go as a `map[string]bool` and Python as a `set`.
Every implementation prints `20000 lists of 50 words, 10 rounds: pairs
sum to 3389340, checksum 738533973`.

BENCHTAB

## Verification

All five arms print the same output as `pairs.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The harness first built its fixed lists as Rust does, `["cd", "ac",
..].map(|w| w.to_string()).to_vec()`. `karac check` says an iterator
adaptor needs `.into_iter()` on a literal, and `karac fix` wrote it;
`.to_vec()` was then refused on the iterator with no fix. That gap was
kara `B-2026-11-20-141`, fixed at `0d28296389`: `karac fix` now writes
`collect()`.

The ★ and sort arms checked clean as first written. The brute arm wrote
Rust's `words[i].as_bytes()`, which `karac fix` made `.bytes()`; the
grid arm wrote `w.bytes().map(..)`, and `karac fix` put the `.iter()`
hop in that a `Slice` needs.

LeetCode's Rust template took 11 `karac fix` edits, the wrapper
included, the harness's apart: the `use std::collections::HashSet`
became `struct Solution {}`, `Vec<String>` became `Vec[String]`,
`HashSet::new()` became `Set.new()`, `contains(&r)` dropped its `&`,
`seen.insert(w)` became `seen.insert(w.clone())`, since `for w in words`
over a borrowed parameter reads each word in place, and `Solution::`
became `Solution.` with the wrapper's `words.clone()` and `as i64`
dropped.
