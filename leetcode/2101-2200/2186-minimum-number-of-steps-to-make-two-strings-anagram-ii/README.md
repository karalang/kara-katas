# 2186. Minimum Number of Steps to Make Two Strings Anagram II

You are given two strings `s` and `t`. In one step, you can append
**any character** to either `s` or `t`.

Return *the minimum number of steps to make* `s` *and* `t` ***anagrams**
of each other.*

An **anagram** of a string is a string that contains the same
characters with a different (or the same) ordering.

```
s = "leetcode", t = "coats"  ->  7
s = "night",    t = "thing"  ->  0
```

**Constraints:** `1 <= s.length, t.length <= 2 * 10^5`; `s` and `t`
consist of lowercase English letters.

Letters can only be added, so every letter one string has more of than
the other must be appended to the other, and nothing else need be. The
steps are, for each letter, the difference of its counts in the two
strings, summed. O(|s| + |t|).

## Approaches

| file | mechanism |
|---|---|
| `anagram_steps.kara` ★ | each letter counted up in s and down in t, in one `Vec.filled(26, 0)`, and the sizes of the counts summed |
| `anagram_steps_sorted.kara` | both strings' bytes sorted, then walked together like a merge: a letter both have passed in both, the smaller of two that differ a step, and what is left of either at the end steps too; O(n log n) |
| `anagram_steps_map.kara` | the letters of s counted into a `Map[char, i64]` with `entry` and `or_insert`, those of t counted off it, and the sizes summed over its `values`, in whatever order they come |
| `anagram_steps_struct.kara` | a `struct Ledger` of how many more of each letter the left side has, made `empty`; s is `credit`ed and t `debit`ed to it (`mut ref self`), and it says how many letters must be `appended` (`ref self`) |
| `anagram_steps_iter.kara` | each string's letters `fold`ed into a list of 26 counts; the two lists `zip`ped, each pair `map`ped to its difference's size, and `sum`med |
| `anagram_steps_solution.kara` | LeetCode's Rust template: `-> i32`, a `[0i32; 26]` indexed by `(b - b'a') as usize`, `iter().map(\|x\| x.abs()).sum()`, `struct Solution;`, `Solution::`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one letter twice, two different letters, one string's letters inside
the other's, and the same letters in another order), each with its
steps; then the total and a checksum over 2000 random pairs of 1 to 30
letters, from a to c or a to z in turn; then the constraints' largest,
2 * 10^5 letters each: all a against all z, two at random, and one
against itself reversed. `anagram_steps.py` mirrors the ★ arm and its
output is byte-identical.

`karac fix` carries the template in two rounds of 2 and 1 edits:
`struct Solution;` to `struct Solution {}` and `Solution::` to `.`;
then the adapter's widening `as i64` dropped, as the `i32` widens to
the `i64` it returns. Kāra takes the rest as it is: the `[0i32; 26]`
array, the `b'a'` byte literal, and the `as usize` index, which mixes
with no `i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the two strings sorted and compared, and at the first place
they differ, or where one runs out, the smaller letter appended to the
string that lacks it, one step at a time, until the two sort the same.
No counts. It checks 300 random pairs of 1 to 8 letters, from a to c or
a to e in turn; then 30 of a string against itself reversed; then 30
with t a single letter over and over. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the steps are the statement read literally |
| P2 | s and t swapped: the same steps |
| P3 | the same word of 1 to 4 letters appended to both: the same steps |
| P4 | every letter 21 later in the alphabet, a to e made v to z: the same steps |
| P5 | the steps at least the lengths' difference and at most their sum, and of the same parity as the sum |
| P6 | each arm agrees with at least three of the other five |

The literal reading is the fewest steps since the smaller letter at the
first difference is one the other string has fewer of, so every letter
it appends is one that must be appended. P2 holds since the question
reads s and t alike. P3 holds since a word added to both adds the same
to each letter's two counts. P4 holds since renaming the letters keeps
their counts. P5 holds since the two strings end the same length, so
the shorter one takes at least the difference, and the steps plus both
lengths are twice that length.

The differential prints `360 pairs: checksum 921607380, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
pairs. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, five to each Kāra arm and six to
the template, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: t counted up too | P1 318, P3 360, P6 318 |
| M3 | ★: the sum halved | P1 326, P5 240, P6 326 |
| M5 | ★: z left out | P4 103 |
| M6 | sorted: t never sorted | P1 177, P2 182, P3 282, P6 177 |
| M7 | sorted: what is left of t dropped | P1 120, P2 271, P3 36, P5 102, P6 120 |
| M8 | sorted: s's smaller letter two steps | P1 182, P2 268, P3 40, P5 123, P6 182 |
| M11 | map: t's letters inserted at 1 | P1 186, P2 226, P3 111, P5 150, P6 186 |
| M12 | map: t's new letters never inserted | P1 186, P2 248, P3 111, P5 144, P6 186 |
| M13 | map: the letters counted, not their sizes | P1 291, P3 83, P5 213, P6 291 |
| M16 | struct: a debt never counted | P1 258, P2 283, P5 205, P6 258 |
| M17 | struct: a debit of 2 | P1 348, P2 299, P3 326, P5 251, P6 348 |
| M20 | struct: a credit to the next letter | P1 259, P2 222, P3 272, P6 259 |
| M22 | iter: the difference with its sign | P1 258, P2 283, P5 146, P6 258 |
| M23 | iter: the first letter left out | P1 240, P4 240, P5 186, P6 240 |
| M24 | iter: s's counts shifted one | P1 298, P2 262, P3 293, P4 253, P5 176, P6 298 |
| M27 | solution: the adapter's t its s | P1 326, P5 283, P6 326 |
| M30 | solution: the adapter's t with an a more | P1 360, P2 240, P4 124, P5 360, P6 360 |

P1 and P6 kill sixteen, P5 thirteen, P2 eleven, P3 ten and P4 four.
Only P4 sees z left out (M5), since the differential's own strings use
a to e, and P4 moves them to v to z; it also sees the edits that treat
a apart, which the move leaves with none: the first letter left out
(M23), the counts shifted one (M24), and the adapter's a more (M30). P5
misses an edit whose count stays a possible one: t counted up, every
letter of both (M1), t never sorted (M6), and a credit to the next
letter (M20), besides z. P2 swaps s and t, and misses an edit that
reads them alike: M1, the halving (M3), the letters counted (M13), the
first letter left out (M23), t its s (M27), and z. P3 adds a word to
both, and misses an edit that reads only each letter's difference,
which the word leaves as it is: M3, M5, a debt never counted (M16), the
signed difference (M22), M23, M27 and M30.

Of the thirty-one, fourteen were not kept, none of them equivalent. One
crashes: the template's t read from `b'b'` (M26) takes 1 from an a's
`u8` 0. One is refused by the type checker: the template's t one
letter shorter (M28), whose `t[1..]` is a `Str` where a `String` is
taken. Three fail as a kept one does: the ★ arm's only s's surplus
summed, as M16; the struct arm's t credited, as M1; and the template's
first count left out, as M23. Nine were left out to keep three to an
arm: the ★ arm's each differing letter counted once (M4), the sorted
arm's mismatch moving both (M9) and match counted a step (M10), the map
arm's surplus squared (M14) and largest surplus only (M15), the struct
arm's s debited too (M19), the iter arm's s counted twice (M21) and
larger count (M25), and the template's t's letters one place on (M29).

## Verification

Every arm prints the same output as `anagram_steps.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the struct, ★, template and sorted arms take
1.1 s to 1.7 s, and the iter and map arms 2.4 s and 2.5 s. The
differential takes 0.7 s.

## Benchmarks

The bench builds one row of 10^6 random letters once; then solves 200
pairs of windows of 2 * 10^5 letters, the constraints' longest, each at
a random start, so that no solve repeats one before, with the ★ arm in
all five languages. C works over pointers and lengths, Rust and Go over
slices of the row; Kāra and Python copy each window into a string of
its own, as the ★ arm takes a `String`. Every implementation prints
`200 solves: checksum 452412235`.

BENCHTAB
