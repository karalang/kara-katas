# 2416. Sum of Prefix Scores of Strings

You are given an array `words` of size `n` consisting of **non-empty**
strings.

We define the **score** of a string `term` as the **number** of strings
`words[i]` such that `term` is a **prefix** of `words[i]`.

- For example, if `words = ["a", "ab", "abc", "cab"]`, then the score of
  `"ab"` is `2`, since `"ab"` is a prefix of both `"ab"` and `"abc"`.

Return *an array* `answer` *of size* `n` *where* `answer[i]` *is the
**sum** of scores of every **non-empty** prefix of* `words[i]`.

**Note** that a string is considered as a prefix of itself.

```
words = ["abc","ab","bc","b"]  ->  [5,4,3,2]
words = ["abcd"]               ->  [4]
```

**Constraints:** `1 <= words.length <= 1000`; `1 <= words[i].length <= 1000`;
`words[i]` consists of lowercase English letters.

Each word passing through a trie node adds one to the score of every
word whose path reaches that node, so a word's answer is the sum of the
counts along its own path.

## Approaches

| file | mechanism |
|---|---|
| `score.kara` ★ | a trie in flat arrays: node `k`'s child by letter `c` at `next[26 k + c]`, 0 for none, and `count[k]` the words through it; every word inserted, then the counts along each word's path summed. O(total length, times 26 for the table) |
| `score_hash.kara` | prefix hashes: each prefix named by a pair of polynomial hashes under two primes, a `Map[(i64, i64), i64]` counting every word's prefixes, and a word's own prefixes read back. O(total length) |
| `score_sort.kara` | sorting: the words sorted, the prefix two neighbours share computed, and from each word a running least of those walked out both ways, since the prefix two sorted words share is the least between them. O(n log n compares + n^2) |
| `score_trie.kara` | a `Trie` struct: a `Vec` of `Node`s, each an `Array[i64, 26]` of child indexes and a count, with `insert` and `score` methods. O(total length) |
| `score_iter.kara` | iterators: for each pair of words, the letters by `zip`, kept by `take_while` they agree, `count`ed, and the counts summed. O(n^2 times the shared prefix) |
| `score_solution.kara` | LeetCode's Rust template: a `#[derive(Default)]` trie of `Option<Box<Trie>>` children, built by `get_or_insert_with` through a `&mut` cursor and walked by `as_ref().unwrap()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; one letter;
one word three times; a chain of prefixes; words with no first letter
in common; the constraints' largest, 1000 words of up to 1000 letters
from 2 letters and from all 26, each as a digest and the total of the
scores; then 2000 random lists of up to 10 words of up to 8 letters from
the first 1 to 4, as a checksum and the total. `score.py` mirrors the ★
arm and its output is byte-identical, and the mirror was checked on
20000 random lists of up to 8 words of up to 6 letters against every
prefix of every word tested against every word.

`check` first reports 11 errors on the template, and `karac fix` carries
it in one call, reporting 19 edits: `Option<..>` and both `Vec<..>`
given brackets and `[T; 26]` written `Array[T, 26]`; `Box<Trie>` and
`Box::new(..)` dropped, leaving each child an `Option[Trie]`; the `::` of both `Trie::default` calls
written `.`; `&words`, `&root` and `&mut root` written as
`ref` and `mut ref` borrows; the score counter annotated `i32`, the type
the template's `-> Vec<i32>` gives it; and `struct Solution;` given its
braces. The `get_or_insert_with` cursor and `as_ref().unwrap()` stand as
Kāra.

`check` then refused the template's derive:
`E_DERIVE_DEFAULT_MISSING_FIELD_DEFAULT` on `children`, an
`Array[Option[Trie], 26]`, though Rust gives `[T; N]` a `Default` of
`N` copies of `T`'s whenever `T` has one, and `Option[T]`'s is `None`
(B-2026-11-21-37, fixed). The derive now gives an array field `N`
copies of its element's default, under the same rule as every other
field.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each word, each of its non-empty prefixes, and every word
checked for starting with it. No trie, no hashing, no sort. The trie
arm's `Trie` and `Node` are renamed `ArmTrie` and `ArmNode` there, since
the template's `Trie` is in the same file. It checks 300 random lists of
1 to 8 words of 1 to 5 letters from the first 1 to 3, then 30 of up to
60 words of up to 20 letters from the first 2, then 30 of up to 60
words of up to 20 letters from all 26. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answers are the literal reading's |
| P2 | each answer is at least its word's length and at most the number of words times it |
| P3 | the words in reverse order: the answers reversed |
| P4 | every letter renamed to the next, `z` to `a`: the same answers |
| P5 | the list given twice: every answer doubled, for both copies |
| P6 | each arm agrees with at least three of the other five |

P2 holds because each of a word's prefixes is a prefix of the word
itself, and of at most every word. P3 holds because a score does not
depend on the order of the list, P4 because renaming the letters
one-to-one keeps every prefix relation, and P5 because each copy of a
word doubles the count of every prefix it has.

The differential prints `360 cases: checksum 598702930, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests every prefix against every word. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the last letter not scored | P1 360, P2 287, P6 360 |
| M4 | ★: the first letter of each word skipped | P1 357, P2 175, P6 357 |
| M6 | ★: a and b sharing a child | P1 350, P2 308, P4 350, P6 350 |
| M9 | hash: each word counted once per letter of its own | P1 346, P2 317, P6 346 |
| M10 | hash: the whole word only counted | P1 291, P6 291 |
| M11 | hash: a word never counting itself | P1 360, P2 257, P5 360, P6 360 |
| M14 | sort: the earlier words never read | P1 299, P3 134, P4 14, P5 360, P6 299 |
| M15 | sort: the running least never lowered | P1 173, P4 20, P5 224, P6 173 |
| M16 | sort: a word not counting itself | P1 360, P2 360, P3 134, P4 14, P5 360, P6 360 |
| M17 | trie: a new node never counted | P1 360, P2 273, P3 167, P5 347, P6 360 |
| M19 | trie: every word inserted twice | P1 360, P2 236, P6 360 |
| M20 | trie: the last word never inserted | P1 359, P2 137, P3 293, P5 351, P6 359 |
| M22 | iter: a word never paired with itself | P1 360, P2 272, P6 360 |
| M24 | iter: every letter counted, matching or not | P1 224, P6 224 |
| M25 | iter: the letters that differ counted | P1 189, P6 189 |
| M27 | solution: the counts kept on the parent | P1 360, P2 190, P6 360 |
| M28 | solution: the score only the deepest count | P1 346, P2 342, P6 346 |

P1 and P6 kill all seventeen, P2 twelve, P5 six, and P3 and P4 four
each. P2's bounds hold for a score that is wrong but still at least
its word's length, as in the hash arm's whole word only counted (M10)
and the iter arm's letters that differ counted (M25). P3, P4 and P5
compare an arm's answers with its own on the reversed, renamed or
doubled list, which a mutant wrong in the same way on every list
passes; the sort arm's mutants fail them, since its errors depend on
where each word falls in the order.

Of the thirty-one, fourteen were not kept. One fails the same checks as
a kept one: the template's every count doubled (M30) as the trie arm's
every word inserted twice (M19). Three end in a panic, not a wrong
answer, under both backends: the hash arm's one hash only and letters
summed, not placed (M7, M8) count the prefixes under one key and look
them up under another, so the lookup finds none, and the template's
score from the root down one short (M29) walks down from the root by the
word's letters from the second on, so it reaches for a child that is
not there and unwraps nothing. Ten fail apart from every kept one and were left
out because those arms keep their share already: the ★ arm's node
counted only when made (M1), root counted for every word (M2) and
count capped at 2 (M5); the sort arm's words never sorted (M12) and
sorted by length (M13); the trie arm's root scored too (M18) and score
only the deepest count (M21); the iter arm's letters compared one apart
(M23) and prefix counted one long (M26), which fails as M2 does; and
the template's score reduced by the word count (M31).

## Verification

Every arm prints the same output as `score.py` under `karac __mir-run`
(the v2 MIR interpreter), but for the iter arm, below; under `karac
__mir-llvm-run`; and under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer) with no error. `karac run` and a `karac build` binary
print the same output for every arm and the differential. `karac check
--output=json` reports nothing on any of them, and `karac fix --dry-run`
has nothing to apply.

Under `karac __mir-run` the arms take 2.0 to 25 s, the template's
`Option[Trie]` nodes the slowest, but for the iter arm, which never
finishes there: its pairs of `bytes()` walks inside `map` closures keep
every snapshot of a word's bytes until the program returns to `main`,
and the interpreter grows by about 1 GB a second until it is killed
(B-2026-11-21-51). Under `karac __mir-llvm-run` and the other lanes it
prints the expected output. The differential takes 14 s under `karac
__mir-run`, 2.8 s under `karac __mir-llvm-asan` and 0.6 s under `karac
run`.

## Benchmarks

The bench builds 10 lists of 2000 words of 1 to 50 letters once from its
own generator, list `i` from the first `2 + 2 i` letters, so the small
alphabets share long prefixes and the large ones branch early. It then
makes 20 passes, scoring every list and folding every score plus the
pass into the checksum. The bench uses the ★ arm, the trie in flat
arrays, in all five languages. Every implementation prints `20 passes
over 10 lists of 2000 words: checksum 216047661`. Each builds its table
afresh for every list and grows it one node at a time: Kāra's `Vec`,
Rust's `Vec` and C's `realloc` by doubling, Go's `append` by about 1.25
times once a slice is large, so Go copies the table several times more
often (on this container the profile puts 44% of its time in
`memmove`), and Python's list by its own over-allocation. The words are
bytes in every language.

BENCHTAB
