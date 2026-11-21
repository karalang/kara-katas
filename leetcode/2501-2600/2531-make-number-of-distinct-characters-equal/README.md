# 2531. Make Number of Distinct Characters Equal

You are given two **0-indexed** strings `word1` and `word2`.

A **move** consists of choosing two indices `i` and `j` such that
`0 <= i < word1.length` and `0 <= j < word2.length` and swapping
`word1[i]` with `word2[j]`.

Return `true` *if it is possible to get the number of distinct
characters in* `word1` *and* `word2` *to be equal with **exactly one**
move.* Return `false` *otherwise.*

```
word1 = "ac", word2 = "b"         ->  false
word1 = "abcc", word2 = "aab"     ->  true
word1 = "abcde", word2 = "fghij"  ->  true
```

**Constraints:** `1 <= word1.length, word2.length <= 10^5`; `word1` and
`word2` consist of only lowercase English letters.

A move's effect depends only on which two letters it swaps, not where
they stand, so there are at most `26 * 26` moves to try, each on the
counts of the letters. The approaches differ in how they try one.

## Approaches

| file | mechanism |
|---|---|
| `chars.kara` ★ | an `Array[i64, 26]` of counts for each word; each pair of a letter present in word1 and one present in word2 swapped on the counts, the distinct letters compared, and the counts put back. O(n + 26^3) |
| `chars_delta.kara` | no swap done: for different letters `a` and `b`, word1 loses a distinct letter when `a` was its only copy and gains one when it had no `b`, and word2 the same the other way; equal letters change nothing. O(n + 26^2) |
| `chars_maps.kara` | a `Map` from each word's letters to their counts, its `len` the distinct letters, and only the letters present tried with the delta arm's arithmetic; the answer does not depend on the order the keys come in |
| `chars_rec.kara` | recursion: the 676 pairs walked by a recursion on the pair's number, `p / 26` from word1 and `p % 26` from word2, each tried on the counts as the ★ arm does; at most 677 deep |
| `chars_iter.kara` | iterators: the counts `fold`ed from each word's bytes, and the answer whether `any` present letter of word1 and `any` of word2 give equal counts by the delta arm's arithmetic |
| `chars_solution.kara` | LeetCode's Rust template: two `String`s in, `bool` out; `[i32; 26]` counts and the ★ arm's swap on them; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and five
more, among them two equal one-letter words, every letter against one,
and a pair that one swap cannot balance; then 3000 random pairs of 1 to
8 letters from the first 1 to 6 and 300 of 1 to 2000 letters from all
26, as how many are possible and a checksum. `chars.py` mirrors the ★
arm and its output is byte-identical, and the mirror was checked on
3000 random pairs of 1 to 6 letters from the first 1 to 5 against every
swap of two positions done on the strings, and the two agreed on every
pair.

`check` reported nothing on the five Kāra arms as first written. The
harness, as first written, built its letters with `('a' as u8 + ..) as
char`, and `check` refused the `char` to `u8` cast with the byte
literal `b'a'` as its machine fix.

`check` first reports 5 errors on the template: the unit struct
`struct Solution;`, the `||`, the two `&&c` closure patterns, and the
path call `Solution::is_it_possible`. `karac fix` carries it in one
call, reporting 5 edits: `struct Solution {}`, `or`, both `&&`
dropped, and `Solution.`. The template's `[0i32; 26]`, its `as usize`
indices and the `String` parameters, which the wrapper fills with
`to_string()`, are accepted as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every index `i` of word1 and `j` of word2 the two letters
are swapped in copies of the words, each copy's distinct letters
counted, and the answer is whether any swap makes the counts equal. It
checks 300 random pairs of 1 to 8 letters from the first 1 to 4, and 60
of 1 to 8 from all 26. All 360 are drawn before any arm answers, and
247 of them are possible.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | true only when the distinct counts differ by at most 2, and true when they are equal and a letter is shared |
| P3 | the words swapped: the same answer |
| P4 | every letter moved on one (`z` to `a`): the same answer |
| P5 | a letter neither word holds appended to both: a true answer stays true |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 247 possible: checksum 154703718,
12960 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python
reading that builds the same words and tries every swap of two
positions. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: word2 not given the letter | P1 126, P2 42, P3 188, P5 4, P6 126 |
| M3 | ★: a letter of word2 needed in word1 too | P1 35, P3 61, P6 35 |
| M6 | ★: the counts compared as totals | P1 211, P2 136, P6 211 |
| M7 | delta: a pair of equal letters always enough | P1 76, P2 17, P6 76 |
| M8 | delta: word1 never gaining | P1 43, P3 83, P6 43 |
| M9 | delta: word2 losing on two copies | P1 28, P3 37, P6 28 |
| M12 | maps: equal letters compared off by one | P1 94, P2 81, P3 30, P6 94 |
| M13 | maps: word1 losing on any count | P1 45, P3 65, P6 45 |
| M14 | maps: word2 gaining when it has the letter | P1 77, P3 52, P6 77 |
| M18 | rec: the pairs from 26 | P1 95, P2 71, P3 42, P4 95, P6 95 |
| M19 | rec: the walk stopped at the first present pair | P1 63, P2 7, P4 2, P5 5, P6 63 |
| M20 | rec: word1 not given the letter | P1 99, P2 35, P3 193, P5 16, P6 99 |
| M23 | iter: word1 never losing | P1 69, P3 95, P6 69 |
| M24 | iter: equal letters never enough | P1 81, P2 81, P6 81 |
| M26 | iter: the distinct counts with zeros | P1 247, P2 158, P6 247 |
| M28 | solution: the first letter alone | P1 69, P2 15, P3 63, P4 180, P6 69 |
| M30 | solution: the counts of two letters | P1 111, P2 39, P3 154, P5 52, P6 111 |

P1 and P6 kill all seventeen, P3 twelve, P2 eleven, P5 four, and P4
three.

Two of the first thirty-one edits survived, both to the rec arm, and
were replaced. The pair read the other way, `a = p % 26` and
`b = p / 26`, walks the same 676 pairs in another order and is
equivalent. The last pair not tried leaves out `z` for `z`, which
decides a case only when both words hold `z` and no other swap works,
and no case of the 360 is one. They became the rec arm's word1
compared with itself and word2 not losing the letter (M17, M21). The
first version of P5, each word reversed, killed none of the kept
edits, since no arm reads the letters' order; it was replaced by the
letter neither word holds, which any swap that worked leaves working.

Fourteen are not kept, and none survives. One fails exactly as a kept
one: the maps arm's letters counted once each (M15) as its word1 losing
on any count (M13), each a copy count of 1 for every letter. The maps
arm's first pair alone tried (M16) fails differently under the two
backends: which pair comes first is the map's iteration order, a
different permutation in each process. The other twelve fail in nine
ways of their own, in arms that already hold their kept edits: the ★
arm's counts not put back and the template's swap left in place (M2,
M31); the ★ arm's distinct counts off by one allowed (M4); its first
25 letters of word2 only (M5), killed by P4 alone, once `y` moves on to
`z`; the delta arm's gain read from the wrong word and the iter arm's
word2 gaining from word2 (M10, M22); the delta arm's letters missing
from word1 tried (M11); the rec arm's word1 compared with itself and
the template's word2 read as word1 (M17, M29); the rec arm's word2 not
losing the letter (M21); the iter arm's every letter of word2 tried
(M25); and the template's swap one way only (M27).

## Verification

Every arm prints the same output as `chars.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.0 to 6.6 s and the differential 2.4 s; under `karac __mir-llvm-asan` the arms take 0.6 to 1.7 s and the differential 0.9 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 1000 random pairs of words once from its own
generator, each word of 1 to 1000 letters from its own first 1 to 26,
then makes 24 passes. Each pass asks every pair, starting at an offset
the checksum so far picks, and folds each answer plus the pass into the
checksum. The bench reads each pair as `let (word1, word2) = ref
pairs[..]`: written without the `ref`, `check` refused moving the two
`String`s out of the list and offered it as the fix. The bench uses the
★ arm in all five languages. Every implementation prints `24 passes
over 1000 pairs of words: checksum 544204298`.

BENCHTAB
