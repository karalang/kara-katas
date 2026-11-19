# 1657. Determine if Two Strings Are Close

Two strings are considered **close** if you can attain one from the
other using the following operations:

- Operation 1: Swap any two **existing** characters.
  - For example, `abcde -> aecdb`
- Operation 2: Transform **every** occurrence of one **existing**
  character into another **existing** character, and do the same with
  the other character.
  - For example, `aacabb -> bbcbaa` (all `a`'s turn into `b`'s, and all
    `b`'s turn into `a`'s)

You can use the operations on either string as many times as necessary.

Given two strings, `word1` and `word2`, return `true` *if* `word1` *and*
`word2` *are **close**, and* `false` *otherwise.*

```
word1 = "abc",    word2 = "bca"     ->  true
word1 = "a",      word2 = "aa"      ->  false
word1 = "cabbba", word2 = "abbccc"  ->  true
```

**Constraints:** `1 <= word1.length, word2.length <= 10^5`; `word1` and
`word2` contain only lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `close.kara` ★ | swapping positions keeps every count and swapping letters swaps two counts, so the words are close exactly when they use the same letters and have the same counts, sorted. O(n + 26 log 26) |
| `close_maps.kara` | each word's counts in a `Map`; close when the key sets match and so do the `SortedMap`s of how many letters have each count. O(n) |
| `close_buckets.kara` | the letters used as a 26-bit mask and the counts tallied in buckets by size, so nothing is sorted. O(n) |
| `close_solution.kara` | LeetCode's Rust template: two `[i32; 26]` counts, the letters compared with `zip`, both sorted and compared. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, lengths
that differ (`false`), a letter only one side has (`false`), and the
same counts on swapped letters (`true`); then how many pairs are close
and a checksum for 3000 random pairs of up to 8 letters from 3, 1000 of
up to 1000 from 26 and 20 of up to `10^5` from 26, half of the second
words made close by construction. `close.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every word the two operations reach from the first, searched
breadth first, swapping any two positions or any two letters the word
holds. It checks 3000 random pairs of words of 1 to 6 letters from the
first 1 to 3 of the alphabet, half of the second words shuffled from the
first with two of its letters swapped throughout. Every pair is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the words swapped give the same answer |
| P3 | the first word reversed gives the same answer |
| P4 | both words relabelled by one shift of the alphabet give the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 446693666, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first tries were replaced. The ★
arm checking only that no letter of the first word is missing from the
second survived and is equivalent: equal sorted counts mean the same
number of letters used, so a letter missing one way means another
missing the other way. The bucket arm marking a count present rather
than counting it survived too: telling `{1, 1, 3, 5, 5}` from
`{1, 3, 3, 3, 5}` takes 15 letters, past the differential's 6.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the letters used never compared | P1 247, P5 247 |
| M2 | ★: the first word's counts left unsorted | P1 1343, P5 1343 |
| M3 | ★: each of the second word's counts held at 1 | P1 1180, P2 252, P5 1180 |
| M4 | maps: only the number of letters used compared | P1 247, P5 247 |
| M5 | maps: a count present marked, not counted | P1 1, P5 1 |
| M6 | buckets: the letter a never tallied | P1 208, P4 208, P5 208 |
| M7 | buckets: letters paired in the mask | P1 148, P4 190, P5 148 |
| M8 | buckets: the counts never compared | P1 26, P5 26 |
| M9 | template: the letters must differ everywhere, not anywhere | P1 247, P5 247 |
| M10 | template: the second word's counts left unsorted | P1 1343, P5 1343 |

## Benchmarks

The bench draws 400 random pairs of words of `10^5` letters, LeetCode's
longest, each pair from the first 1 to 26 of the alphabet, half of the
second words the first reversed with two letters swapped throughout, all
of them first, then answers each by the ★ arm in all five languages.
Every implementation prints `400 pairs of 100000 letters: 218 close,
checksum 308289320`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `close.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

## Writing it

The ★, maps and buckets arms checked clean as first written.

LeetCode's Rust template takes one `karac fix` of 3 edits:
`struct Solution;` to `struct Solution {}` and Rust's `sort_unstable()`
to `sort()` on each count array. Its `[0i32; 26]` counts,
`(b - b'a') as usize` indices and the `zip` closure's `*a == 0` all
check as written. The arm then checks and agrees with no hand edit.
