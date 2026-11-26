# 1408. String Matching in an Array

Given an array of string `words`, return all strings in `words` that are
a substring of another word. You can return the answer in any order.

```
words = ["mass", "as", "hero", "superhero"]  ->  ["as", "hero"]
words = ["leetcode", "et", "code"]           ->  ["et", "code"]
words = ["blue", "green", "bu"]              ->  []
```

**Constraints:** `1 <= words.length <= 100`, `1 <= words[i].length <=
30`, `words[i]` contains only lowercase English letters, all the strings
of `words` are unique.

Each arm is `fn string_matching(words: Vec[String]) -> Vec[String]`. Any
order is allowed, so every answer is sorted before it is printed or
compared.

## Approaches

| file | mechanism |
|---|---|
| `string_matching.kara` ★ | every word some other word `contains`, as one `filter(..).cloned().collect()` with `any` inside. O(n^2 L^2) |
| `string_matching_sorted.kara` | the words sorted by length with `sort_by_key`, since only a longer word can hold a word, and each tried against those after it. O(n^2 L^2) |
| `string_matching_joined.kara` | all the words joined into one text with a space between: a word is in itself once, so it is inside another word exactly when `matches(w).count()` finds it at least twice. O(n^2 L^2) |
| `string_matching_trie.kara` | a trie of every suffix of every word, in a `Vec` of nodes with a `Map[char, i64]` of children each, every node counting the words it lies in, once each however many suffixes pass; a word is inside another when its own node counts two. O(n L^2) |
| `string_matching_solution.kara` | a Rust solution as LeetCode's Rust users write it (two `enumerate()` loops, `i != j && other.contains(w.as_str())`, a `break` on the first), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and three
more (`[as,hero] [code,et] [] [] [a,aa,aaa] [ab,ba]`); the constraints'
most, 100 words of up to 30 letters from 2 letters and from 26, how many
are found (`100 words: 39 8`); and 2000 random sets of 1 to 20 words of
up to 6 letters from 3 (`2000 random sets: 8250 found, checksum
739459728`). `string_matching.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, sorted, joined and trie arms check clean as first
written. The Rust solution takes one round of 11 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `Vec<String>` to
`Vec[String]`, `Vec::new` to `Vec.new`, `&&` to `and`, and `Solution::`
to `Solution.`. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each word looked for at every place in every other word,
letter by letter. LeetCode's examples, four edge cases (one word, a
chain each inside the next, words inside each other both ways round,
three rotations) and the constraints' most from 2 letters and from 26,
and 1994 random sets, 1 to 12 words of up to 5 letters from 2 or 3, or
13 to 40 words of up to 8 letters from 3. Each case is also given one
more word, drawn of up to 6 letters from 3.

The differential's `check_case` first took that extra word as a bare
`extra: String` and pushed it; a bare parameter borrows
(core-semantics.md §4.1), so check refuses the push, and `karac fix`
writes `extra: own String` and, since the word is printed after it is
pushed, `more.push(extra.clone())`, 2 fixes.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | each one of the words, none twice |
| P3 | the order the words come in does not matter: the list reversed gives the same |
| P4 | beside one word that holds them all, all of them joined with a `z` none has, every word is found and that one is not |
| P5 | one more word never loses a word found |
| P6 | the ★ arm's answer |

All 58,930 checks pass on every arm (P5 applies when the extra word is
new): `2003 cases: checksum 559115801, 58930 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, by its `in`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a word found inside itself, the `other != w` dropped | P1 2003, P4 2003, P6 8012 |
| M2 | ★: `any` written `all`, so a word must be inside every word | P1 1775, P4 2003, P6 7100 |
| M3 | sorted: each word tried only from two places after it | P1 293, P3 351, P4 2003, P6 293 |
| M4 | sorted: the sort left out, so a longer word before a shorter one is never tried | P1 1284, P3 1696, P6 1284 |
| M5 | joined: the words joined with nothing between, so a word can be found across two | P1 1310, P3 1311, P6 1310 |
| M6 | joined: a word found once counted as inside another | P1 2003, P4 2003, P6 2003 |
| M7 | trie: only each word's whole, not its suffixes, put in the trie | P1 1377, P4 1877, P6 1377 |
| M8 | trie: a word taken only when three words hold it | P1 1401, P4 2003, P6 1401 |
| M9 | solution: each word tried only against the words after it | P1 1284, P3 1696, P6 1284 |
| M10 | solution: the `break` left out, so a word in two others is pushed twice | P1 1617, P2 1617, P4 1775, P6 1617 |

A first M7, the trie counting a word every time one of its suffixes
passes a node rather than once, survived: a node is a substring of the
word whose suffix reaches it, and a word cannot be inside itself at a
later place, so its own node is reached twice only from a word that
holds it, and the mutant was equivalent and was replaced.

## Benchmarks

The bench draws a pool of 10^4 words of 1 to 12 letters from 3 and runs
the ★ arm on 2000 windows of 100 words in a row, each kept once, each
window's start drawn from the checksum so far, folding how many are
found and their letters. Every implementation prints `2000 windows of
100 words: checksum 187539351`.

BENCHTAB

Kāra is level with Rust here, measured by hand at 0.18 s against Rust's
0.17 s, with overflow checks on or off.
