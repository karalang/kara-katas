# 940. Distinct Subsequences II

Given a string `s`, return the number of **distinct non-empty
subsequences** of `s`. Since the answer may be very large, return it
**modulo** `10^9 + 7`.

A **subsequence** of a string is a new string that is formed from the
original string by deleting some (can be none) of the characters
without disturbing the relative positions of the remaining characters.
(i.e., `"ace"` is a subsequence of `"abcde"` while `"aec"` is not.)

```
s = "abc"  ->  7     ("a", "b", "c", "ab", "ac", "bc", "abc")
s = "aba"  ->  6     ("a", "b", "ab", "aa", "ba", "aba")
s = "aaa"  ->  3     ("a", "aa", "aaa")
```

**Constraints:** `1 <= s.length <= 2000`; `s` consists of lowercase
English letters.

## Approaches

| file | mechanism |
|---|---|
| `distinct_subseq_ii.kara` ★ | the distinct subsequences of each prefix counted, the empty one included: a new letter doubles them, each one with or without the letter, and the ones counted twice are those that already ended in it, which are the prefix before its last place with the letter put after, so the count from just before that place is taken away; the empty one dropped at the end. O(n) |
| `distinct_subseq_ii_ends.kara` | for each letter, how many distinct subsequences end with it: when a letter comes, those ending with it become every subsequence so far with the letter after, and the letter alone, one more than the sum of all 26, replacing the old count, all of which are among the new; the answer is the sum. O(26 n) |
| `distinct_subseq_ii_suffix.kara` | the subsequence automaton: every distinct subsequence is found exactly once taking each letter as early as possible, so a table gives, for each place and letter, where that letter next comes, and from the right the subsequences starting at or after a place are, for each letter that comes again, that letter alone or followed by one starting just after it. O(26 n) time and space |
| `distinct_subseq_ii_memo.kara` | the same count from each place worked out recursively, each letter taken at its first place from there, each place's answer kept in a table so it is worked out once. O(n²), recursion `n` deep |
| `distinct_subseq_ii_lengths.kara` | for each length and letter, how many distinct subsequences of that length end with that letter, with each length's total: a new letter makes those of length `L` ending with it every subsequence of length `L - 1` with the letter after, done from the longest length down so each uses the totals from before the letter; the answer adds up every length. O(n²) time, O(26 n) space |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples and five
more (one letter, two different letters, `abab`, a word whose first and
last letters are the same, and the alphabet, 2^26 - 1); for 300 random
words of 1 to 100 letters from the first 1 to 26 of the alphabet, the
letters, the counts and a checksum; and five of LeetCode's longest,
2,000 letters: all `a`, `ab` over and over, the alphabet over and over,
random letters, and random letters from `a`, `b` and `c`.
`distinct_subseq_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice of letters to keep, the letters kept read in
order, and the different strings counted in a `Set`, leaving out the
empty one. It checks 3,200 random words: 3,000 of up to 10 letters from
the first 1 to 4 of the alphabet, against the statement, and 200 of up
to 200 letters from the first 1 to 26, against the other properties;
36,041 letters in all.

| | property |
|---|---|
| P1 | the statement's count, on the small words |
| P2 | below the modulus, and for up to 29 letters from `n`, since there is one of each length at least, to `2^n - 1` |
| P3 | the word reversed gives the same count |
| P4 | the letters renamed by a random shuffle of the alphabet give the same count; and the word followed by a word of up to 6 letters it does not use gives `(a + 1)(b + 1) - 1`, each part's choices, empty ones included, multiplied |
| P5 | one more letter, `c`, gives twice the count, plus 1 if `c` is new, or otherwise less the count of the word up to just before its last `c`, from the arm's own answers |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 words of 36041 letters, checksum 199280408, 95000 checks
over 5 arms: 0 failures` under `karac __mir-run` (20 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each letter doubling and adding one | P1 3000, P2 1658, P3 1544, P4 3195, P5 3200, P6 3200 |
| M2 | ★: a repeat of the first letter not taken away | P1 2274, P3 1531, P4 336, P5 296, P6 2467 |
| M3 | ★: the empty prefix counted twice | P1 3000, P2 1312, P4 3200, P6 3200 |
| M4 | ends: `z` left out of the answer | P3 5, P4 317, P5 4, P6 5 |
| M5 | ends: `z` left out of each sum | P3 5, P4 297, P5 4, P6 5 |
| M6 | ends: `z` counted with `a` | P4 444, P6 5 |
| M7 | suffix: only the letter at each place known | P1 1848, P4 3195, P5 1584, P6 2036 |
| M8 | suffix: each place one past its letter | P1 3000, P2 1841, P3 1410, P4 2628, P5 2766, P6 3200 |
| M9 | suffix: a letter not ahead taken as last | P1 3000, P2 2776, P3 1531, P4 3195, P5 1766, P6 3200 |
| M10 | memo: the letter at the place itself skipped | P1 3000, P2 1839, P3 1410, P4 3156, P5 2701, P6 3200 |
| M11 | memo: each answer stored one too many | P1 1848, P2 375, P3 1531, P4 3180, P5 1766, P6 2036 |
| M12 | memo: the last letter taken even when seen | P1 2289, P3 1531, P4 2469, P5 1768, P6 2474 |
| M13 | lengths: the longest never updated | P1 3000, P2 1378, P3 1531, P4 3195, P5 296, P6 3200 |
| M14 | lengths: the longest left out of the answer | P1 3000, P2 1154, P4 3195, P5 739, P6 3200 |
| M15 | lengths: the letters' rows overlapping | P1 545, P3 711, P4 2717, P5 383, P6 718 |

P4 and P6 kill all fifteen, P5 thirteen, P1 twelve, P3 eleven and P2
eight.

P1 misses M4, M5 and M6, the three that go wrong only on a word holding
`z`, which the small words, from `a` to `d`, never do. P4 sees them
most, since its shuffle often renames a letter to `z`; P6 sees them only
on the few large words with a `z` in them.

P5 misses M3 and M6. M3 starts the count at 2, which doubles every count
from then on, the empty one included, and doubled counts follow the
same rule for one more letter; P4 sees it, since a doubled product is
not the product of two doubled counts. M6 counts `z` with `a`, and P5's
extra letter is a `z` only for a large word from all 26 letters, and
then only one time in 26.

P3 misses M3 and M6, again, and M7 and M14. M7 knows only the letter at
each place, not where each letter comes next, and so answers the length
of the word; M14 leaves out the one subsequence of full length. Both
are the same for the word reversed, as are M3's doubled counts and M6's
`z` counted with `a`.

P2 misses M2, M7, M12 and M15, whose counts stay in range for short
words, as well as the three `z` mistakes.

Twenty-seven other edits were tried and set aside. Twenty-two failed
exactly the same checks as each other, in seven groups, so none of them
was kept: four that count every choice of letters, 2^n - 1 (★ taking
nothing away for a repeat, ends adding to its count instead of
replacing it, memo taking every letter whether seen or not, and lengths
never taking the old count off); three that take away too much (★ the
count at the last place itself, ends leaving the letter's own count out
of its sum, and suffix following each letter with the subsequences from
its own place); six that answer 0 (ends, suffix and memo not counting
the letter alone, memo starting every place as worked out at 0, lengths
counting each length from the same length, and lengths never updating
length 1); three that answer one more (★ keeping the empty one, lengths
counting it, and ends starting its answer at 1); two that count the
empty one twice in a different way from M3 (ends counting the letter
alone twice and lengths starting with two empty ones); ★ keeping the
last place one short and memo not marking the letter at its own place
seen; and suffix never finding the last letter next and memo never
taking the last letter. Three were sound but beyond three an arm (suffix
never finding `z` next, memo storing each answer modulo 1,000, and
lengths making each count one too many). One was equivalent: ★ leaving
the difference below 0 before reducing it, which keeps every count
congruent and in range below the modulus and above its negative, so the
last step still lands on the right answer. One crashed: memo starting
from the second place, on the empty word P4 can form.

## Verification

Every arm prints the same output as `distinct_subseq_ii.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.2 to 5.8 s each and the
differential 20 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

All five arms print the same output under the frozen legacy
interpreter, the legacy JIT and both legacy builds, with and without
auto-par. Legacy refuses the differential at the first `*` on an element
of a `Vec[u8]`'s `.iter()` ("unary '*' requires 'ref T', ..."), legacy's
older rule, under which the element is a copy; under v2 it is a
reference and the `*` is required. It refuses the bench program at
`distinct_subseq_ii(words[(r + i) % count])`, a move out of an index
("cannot move ... out of an index"), which v2's borrowing parameters
make a borrow. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 100 words of 2,000 letters once, LeetCode's
longest, each of random letters from the first 1 to 26 of the alphabet;
in each of 200 rounds it runs the ★ arm on every word, each round
starting from a different one, and folds the counts into a checksum.
Every implementation prints `200 rounds over 100 words of 2000 letters:
counts adding to 9145663998600, checksum 134459497`. Kāra copies each
word's bytes into a `Vec[u8]` on every call, as the ★ arm does; the
others read the word in place.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.37 to 0.39 s | 0.38 s |
| Rust (`rustc -O`) | 0.43 to 0.47 s | 0.46 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.43 to 0.47 s | 0.45 s |
| Go | 0.50 to 0.54 s | 0.51 s |
| Python | 8.67 s | |
| Kāra (`karac build --mir`) | 0.42 to 0.47 s | 0.45 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 23 times C's.

v2 takes 0.99 times Rust's median time under overflow checks and 1.17
times C's. Under valgrind's cachegrind v2 runs 2.20 billion instructions
and 0.37 billion branches with 0.91 million mispredicted, Rust with
overflow checks 2.27 billion, 0.37 billion and 0.67 million, and C 1.37
billion and 0.08 billion branches with 0.28 million mispredicted. v2
and Rust run almost the same code; that C's fewer branches are the
bounds and overflow checks it does not make, on `count` and `last`, is
inferred, not profiled.
