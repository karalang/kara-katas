# 2506. Count Pairs Of Similar Strings

You are given a **0-indexed** string array `words`.

Two strings are **similar** if they consist of the same characters.

- For example, `"abca"` and `"cba"` are similar since both consist of
  characters `'a'`, `'b'`, and `'c'`.
- However, `"abacba"` and `"bcfd"` are not similar since they do not
  consist of the same characters.

Return *the number of pairs* `(i, j)` *such that* `0 <= i < j <=
word.length - 1` *and the two strings* `words[i]` *and* `words[j]` *are
similar*.

```
words = ["aba","aabb","abcd","bac","aabc"]  ->  2
words = ["aabb","ab","ba"]                  ->  3
words = ["nba","cba","dba"]                 ->  0
```

**Constraints:** `1 <= words.length <= 100`; `1 <= words[i].length <=
100`; `words[i]` consist of only lowercase English letters.

Two words are similar exactly when their sets of letters are equal, and
a set of lowercase letters fits in a 26-bit mask. The approaches differ
in how a word's set is held and how equal sets are counted.

## Approaches

| file | mechanism |
|---|---|
| `similar.kara` ★ | every word's letters as a 26-bit mask; each word pairs with every earlier word of its mask, whose number a `Map` keeps. O(total length) |
| `similar_sets.kara` | every word's letters `collect`ed into a `Set[char]`, and every pair of words compared by their sets. O(n^2 26 + total length) |
| `similar_keys.kara` | every word's distinct letters sorted into a `String` key; the keys sorted, and each run of `r` equal keys worth `r (r - 1) / 2` pairs |
| `similar_rec.kara` | recursions: a word's mask built letter by letter from its end, and the pairs from place `i` on, the later words sharing `i`'s mask plus the pairs from `i + 1`. At most 100 deep |
| `similar_iter.kara` | iterators: every word's mask `fold`ed from its `chars`, then for each place the later places of the same mask `filter`ed and `count`ed, and the counts `sum`med |
| `similar_solution.kara` | LeetCode's Rust template: `Vec<String>` in, `i32` out; every word's `bytes()` folded into a mask, and a `HashMap<i32, i32>` entry per mask read and then bumped through one `entry(..).or_insert(0)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and five
more; then 2000 random lists of 1 to 30 words of 1 to 8 letters, from
3 letters and from 26, each as a count of the lists with no pair and a
checksum; then the constraints' largest, 100 words: each of 100 letters
running through the alphabet from a different start; 100 random words
of 100 letters; and 100 random words of 1 to 4 letters from 3.
`similar.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked on 5000 random lists of 1 to 12 words against a
comparison of every pair's sets of letters, and the two agreed on every
list.

The harness builds a letter as `(b'a' + k as u8) as char`. Written
`('a' as i64 + k) as char`, `check` refuses it with E_INT_AS_CHAR, since
not every integer is a `char`, and points at `char.try_from`; written
`('a' as u8 + k as u8) as char`, it refuses `'a' as u8` and points at
the byte literal `b'a'`, which is what the harness uses.

`check` first reports 5 errors on the template: the `use
std::collections::HashMap;` line, `struct Solution;`, `Vec<String>` and
`HashMap<i32, i32>` in angle brackets, and `HashMap::new`. `karac fix`
carries it in one call, reporting 12 edits: the `use` line goes, since
`Map` is in the prelude, and `HashMap` becomes `Map`; `struct Solution
{}`; the brackets and the `.` path; `let mut ans = 0` given `: i32`,
which its `0` would otherwise not be beside the `i32` return; and the
wrapper's `words.clone()` and lossless `as i64` dropped. The mask built
from `b - b'a'`, a `u8` shift amount, and the `let e = cnt.entry(mask)
.or_insert(0); ans += *e; *e += 1;` that reads and bumps through one
reference stand as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of places `i < j`, similar when every letter of
each word is found in the other by a scan. No set or mask is built. It
checks 300 random lists of 1 to 10 words of 1 to 5 letters, from 2 or
4 letters; then 20 of one word of up to 8 letters from 26; and 40 of 20
words from 3 letters. All 360 are drawn before any arm answers, and 113
of them have no pair.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | from 0 to `n (n - 1) / 2` |
| P3 | the words in the other order: the same answer |
| P4 | every letter written as its mirror in the alphabet, `a` as `z` and `z` as `a`: the same answer |
| P5 | the list followed by a copy of itself: `4 x + n` |
| P6 | each arm agrees with at least three of the other five |

P5 holds because each copy holds the `x` pairs, and across the copies
every word pairs with its own copy and with both copies of each word
similar to it: `n + 2 x` more.

The differential prints `360 cases, 113 with no pair: checksum
877093155, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and compares every pair's
sets. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a new mask worth 1 | P1 360, P2 91, P5 360, P6 360 |
| M4 | ★: the mask never cleared | P1 255, P3 197, P5 204, P6 255 |
| M5 | ★: the first letter only | P1 251, P6 251 |
| M8 | sets: only neighbours compared | P1 225, P5 316, P6 225 |
| M9 | sets: sets of the first two letters | P1 198, P6 198 |
| M10 | sets: sets of one size taken as similar | P1 219, P6 219 |
| M12 | keys: the letters unsorted | P1 217, P6 217 |
| M13 | keys: repeated letters kept | P1 233, P6 233 |
| M14 | keys: the keys unsorted | P1 198, P5 296, P6 198 |
| M17 | rec: the last letter left out | P1 200, P6 200 |
| M18 | rec: letters added | P1 226, P4 161, P6 226 |
| M20 | rec: the recursion two along | P1 195, P3 161, P5 313, P6 195 |
| M24 | iter: differing masks counted | P1 308, P5 360, P6 308 |
| M25 | iter: letters xored | P1 223, P6 223 |
| M26 | iter: the first place skipped | P1 187, P3 134, P5 360, P6 187 |
| M28 | solution: a mask begun at 1 | P1 199, P4 199, P6 199 |
| M30 | solution: the bump never made | P1 247, P5 360, P6 247 |

P1 and P6 kill all seventeen, P5 eight, P3 three, P4 two, and P2 one.

Fourteen are not kept, and none survives. Three fail exactly as a kept
one: the ★ arm's letters counted, not marked, and the template's
letters added (M1, M29) as the rec arm's letters added (M18), each
telling `aab` from `ab`; and the iter arm's fold begun at 1 (M22) as the
template's mask begun at 1 (M28), each giving every word an `a`. Nine
fail as one another, in three sets: the ★ arm's count never grown and
the rec arm's later places counted once (M3, M21), each word pairing
with at most one other of its mask; the ★ and template arms' count
read after the bump, the sets arm's word paired with itself, the rec
arm's mask matched with itself and the iter arm's place matched with
itself (M6, M27, M7, M19, M23), every word also paired with itself; and
the sets arm's and the template's pairs counted from 1 (M11, M31). Two
fail in ways of their own, but their arm already holds its kept edits:
the keys arm's run worth `r^2 / 2` and last run dropped (M15, M16).

## Verification

Every arm prints the same output as `similar.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.0 to 3.0 s and the differential 1.6 s; under `karac __mir-llvm-asan` the arms take 0.5 to 0.9 s and the differential 0.8 s; and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds 1000 lists of 100 words once from its own generator,
each word 1 to 100 letters from the first 3 to 6 of the alphabet, then
makes 24 passes. Each pass, for every list, copies the word at place
`(check / 100 + p) % 100` over the one at `check % 100`, asks, and puts
the word back, folding the answer plus the pass into the checksum. The
bench uses the ★ arm in all five languages, each counting the masks in
a fresh hash table on every ask: Kāra's `Map`, Rust's `HashMap`, Go's
map, Python's `dict`, and in C an open-addressed table of 256 slots.
Every implementation prints `24 passes over 1000 lists of 100 words:
checksum 740837717`.

BENCHTAB
