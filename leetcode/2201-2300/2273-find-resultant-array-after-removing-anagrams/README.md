# 2273. Find Resultant Array After Removing Anagrams

You are given a **0-indexed** string array `words`, where `words[i]`
consists of lowercase English letters.

In one operation, select any index `i` such that `0 < i < words.length`
and `words[i - 1]` and `words[i]` are **anagrams**, and **delete**
`words[i]` from `words`. Keep performing this operation as long as you
can select an index that satisfies the conditions.

Return `words` *after performing all operations*. It can be shown that
selecting the indices for each operation in **any** arbitrary order
will lead to the same result.

An **Anagram** is a word or phrase formed by rearranging the letters of
a different word or phrase using all the original letters exactly
once. For example, `"dacb"` is an anagram of `"abdc"`.

```
words = ["abba","baba","bbaa","cd","cd"]  ->  ["abba","cd"]
words = ["a","b","c","d","e"]             ->  ["a","b","c","d","e"]
```

**Constraints:** `1 <= words.length <= 100`; `1 <= words[i].length <=
10`; `words[i]` consists of lowercase English letters.

Being anagrams is an equivalence, so a run of adjacent anagrams
collapses to its first word whatever the order of the deletions: a word
stays exactly when it is not an anagram of the word before it. Each
word's sorted letters, or its 26 letter counts, are a key to compare
with the previous word's. O(m w log w) for m words of w letters, or
O(m w) by counts.

## Approaches

| file | mechanism |
|---|---|
| `anagrams.kara` ★ | each word's sorted letters as a `String` key, the word kept when its key differs from the previous word's |
| `anagrams_counts.kara` | each word's letter counts in an `Array[i64, 26]`, compared with the previous word's; no sort |
| `anagrams_stack.kara` | the deletions as stated, on a stack: a word is pushed unless it is an anagram of the top, by sorted bytes |
| `anagrams_struct.kara` | `struct Filter` of the words kept and the last word's counts; `offer` (`mut ref self`) keeps a word whose counts differ and always remembers them |
| `anagrams_iter.kara` | in chains: the keys by `map`, then `enumerate`, a `filter` keeping the first word and each whose key differs from the one before, and `collect` |
| `anagrams_solution.kara` | LeetCode's Rust template: `Vec<String>` in and out; a closure `key` sorts a word's bytes by `sort_unstable`, and `for w in words` pushes a word whose key differs from the last one kept; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one word; every word an anagram of the first, `[abc]`; anagrams
apart but not adjacent, all kept; a word of another length between a
word and its anagram, all kept; a run broken and resumed,
`[xy, z, xy]`), each with what is left; then 3000 random lists of 1 to
30 words of up to 1, 3 or 10 letters from the first 2, 3 or 26, each
word after the first half the time the one before it shuffled, with the
number kept and a checksum; then three of the constraints' largest, 100
words of 10 letters: random (51 kept), two anagrams alternating (1),
and two families in pairs (50). `anagrams.py` mirrors the ★ arm and its
output is byte-identical.

`karac fix` carries the template in one round, reporting 24 edits: the
generics' `<` and `>` to `[` and `]`, the closure's `&String` to `ref
String`, `w.bytes().collect()` to `w.bytes().iter().collect()`,
`sort_unstable` to `sort`, `Vec::new()` to `Vec.new()`, `||` to `or`,
`key(&w)` to `key(w)`, `struct Solution;` to `struct Solution {}`,
`Solution::` to `Solution.`, and in the adapter `&Vec<String>` to a
bare `Vec[String]` and the `.clone()` dropped. Since a parameter
borrows by default, `for w in words` yields each word borrowed, and
`ans.push(w)` becomes `ans.push(w.clone())`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: while some word is an anagram of the word before it, the
first such word is removed and the scan starts again, two words being
anagrams when each of the 26 letters occurs in them equally often. No
key and no single pass. It checks 300 random lists of 1 to 8 words of
up to 1, 3 or 5 letters from the first 2, 3 or 26, each word after the
first half the time the one before it shuffled; then 30 of shuffles of
`kayak`; then 30 of shuffles of `stop` and `lemon` alternating. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the words left are the literal reading's |
| P2 | every word reversed: the words left, reversed |
| P3 | the letters relabelled, the alphabet turned by seven: the words left, relabelled |
| P4 | the first word kept, the words left in their order among the words, and no two adjacent ones anagrams |
| P5 | the list twice over: the words left twice, less the second copy's first word when the last word is an anagram of the first |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 549275221, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
deletes the first `Counter`-equal neighbour until none is left. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: never sorted | P1 115, P4 115, P5 50, P6 115 |
| M3 | ★: only anagrams kept | P1 308, P4 222, P5 360, P6 308 |
| M6 | ★: the key kept for the word | P1 202, P2 230, P3 105, P4 198, P6 202 |
| M8 | counts: presence for count | P1 40, P5 17, P6 40 |
| M10 | counts: the second word always kept | P1 177, P4 177, P5 218, P6 177 |
| M11 | counts: letters 13 apart counted as one | P1 1, P6 1 |
| M13 | stack: only one word sorted | P1 115, P2 93, P3 17, P4 115, P5 69, P6 115 |
| M14 | stack: nothing pushed | P1 360, P4 360, P6 360 |
| M15 | stack: anagrams by length | P1 133, P5 97, P6 133 |
| M17 | struct: the last counts never moved | P1 268, P4 268, P5 147, P6 268 |
| M20 | struct: the word kept at the front | P1 230, P4 230, P5 14, P6 230 |
| M21 | struct: the first word never offered | P1 248, P4 248, P5 212, P6 248 |
| M22 | iter: every word against the first | P1 185, P4 169, P5 213, P6 185 |
| M23 | iter: the keys cut to their first letter | P1 77, P3 12, P5 56, P6 77 |
| M26 | iter: the first word skipped | P1 360, P4 360, P5 238, P6 360 |
| M29 | solution: each word kept twice | P1 360, P4 360, P5 147, P6 360 |
| M30 | solution: the words taken backwards | P1 266, P4 266, P6 266 |

P1 and P6 kill all seventeen, P4 thirteen, P5 thirteen, P3 three, and
P2 two. P4 checks the shape of an answer without the literal reading,
and catches every edit that loses the first word, reorders or repeats
words, or leaves two anagrams side by side. P5 catches the edits whose
decision for a word depends on more than the word before it. P2 sees
only the edits that read a word's letters in order, the key kept for
the word and one word sorted; P3 sees those and the keys cut to their
first letter, since relabelling moves which letter sorts first. Letters
13 apart counted as one fails a single case: it needs neighbouring
words that differ only by such a pair of letters, which only the lists
from all 26 letters can hold.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. All fourteen fail as a kept one does: the ★ arm's
one word sorted (M2) as the stack arm's (M13); the ★ arm's last key
never moved (M4) as the struct arm's last counts (M17); the ★ arm's and
the struct arm's presence for count (M5, M19) as the counts arm's (M8);
the ★ arm's, the counts arm's and the template's every word against the
first (M7, M16, M27) as the iter arm's (M22); the counts arm's first
word skipped (M9) as the iter arm's (M26); the counts arm's and the
template's never sorted or counted (M12, M28) as the ★ arm's never
sorted (M1); the struct arm's and the template's second word always
kept (M18, M31) as the counts arm's (M10); the iter arm's only anagrams
kept (M24) as the ★ arm's (M3); and the iter arm's key kept for the
word (M25) as the ★ arm's (M6).

One edit of the first draft was replaced because it failed as another
did: the iter arm's keys never sorted, as the ★ arm's M1. It is now
M23.

## Verification

Every arm prints the same output as `anagrams.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the stack arm takes 0.8 s, the struct arm and
the ★ arm 1.1 s, the template 1.3 s, the counts and iter arms 1.4 s,
and the differential 1.7 s.

## Benchmarks

The bench answers 20000 lists of the constraints' largest, 100 words of
10 letters from the first 4, each word after the first half the time
the one before it shuffled, with the ★ arm in all five languages. Every
implementation prints `20000 lists of 100: checksum 950988518`. Each
builds its words from the same generator; C sorts each word's letters
with `qsort`, Go with `sort.Slice`.

BENCHTAB
