# 916. Word Subsets

You are given two string arrays `words1` and `words2`.

A string `b` is a subset of string `a` if every letter in `b` occurs in
`a` including multiplicity. For example, `"wrr"` is a subset of
`"warrior"` but is not a subset of `"world"`.

A string `a` from `words1` is universal if for every string `b` in
`words2`, `b` is a subset of `a`.

Return an array of all the universal strings in `words1`. You may return
the answer in any order.

```
words1 = ["amazon","apple","facebook","google","leetcode"], words2 = ["e","o"]
  ->  ["facebook","google","leetcode"]
words1 = ["amazon","apple","facebook","google","leetcode"], words2 = ["l","e"]
  ->  ["apple","google","leetcode"]
words1 = ["amazon","apple","facebook","google","leetcode"], words2 = ["e","oo"]
  ->  ["facebook","google"]
```

**Constraints:** `1 <= words1.length, words2.length <= 10^4`,
`1 <= words1[i].length, words2[i].length <= 10`, `words1[i]` and
`words2[i]` consist only of lowercase English letters, and all the
strings of `words1` are unique.

Every arm here returns the universal words in `words1`'s order, so the
answers compare as lists.

## Approaches

A word of `words1` is universal when, for each letter, it holds at least
as many as any one word of `words2` does: the need for a letter is the
largest count of it over `words2`.

| file | mechanism |
|---|---|
| `word_subsets.kara` ★ | each word counted into an `Array[i64, 26]`; `words2` folded into the 26 largest counts once, then each word of `words1` kept when its counts reach all 26. O(total length + 26 (\|words1\| + \|words2\|)) |
| `word_subsets_sorted.kara` | each word of `words2` sorted and merged into one sorted word that holds each letter as often as the most any of them does (a union with multiplicity); a word is universal when that merged word is a subsequence of its own letters sorted, decided by two pointers. O(total length log 10) |
| `word_subsets_map.kara` | counts kept in a `Map[u8, i64]`; the need holds only the letters some word of `words2` uses, and a word is universal when its own map reaches each of them. O(total length) expected |
| `word_subsets_decrement.kara` | the need folded from a running count of each word's letters, then spent: a copy of the need loses one for each letter of the word, a counter of letters still owed drops while a letter is owed, and the word is universal when nothing is left owing. O(total length + 26 (\|words1\| + \|words2\|)) |
| `word_subsets_letters.kara` | letter by letter rather than word by word: every word of `words1` starts as a candidate, and for each letter the need asks for, only the candidates holding it often enough are kept. O(26 \|words1\| 10) at worst |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the seven examples (LeetCode's first
with `["e","o"]`, `["l","e"]`, `["e","oo"]` and `["lo","eo"]`, then
`["a","a"]` and `["aa"]` against short words, and a letter nobody holds);
for 400 random cases of up to 300 distinct words of up to 10 letters
from 3, 6 or 26 letters against up to 5 words of up to 4 letters, the
universal words kept (12,011) and a checksum; and two of LeetCode's
largest, 10^4 words against 10^4 single letters (none universal) and
10^4 words of 4 letters against 10^4 of 2 (670 universal).
`word_subsets.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: `b` is a subset of `a` when each letter of `b` can take its
own unused equal letter of `a`, found greedily, and a word of `words1`
is universal when every word of `words2` is a subset of it. It checks
3,200 random cases: 3,000 of up to 6 distinct words of up to 5 letters
from 3 against up to 3 words of up to 3 letters, against the statement;
and 200 of up to 200 words of up to 10 letters from 3, 6 or 26 against
up to 5 of up to 4, against the other properties; 37,491 words in all,
6,932 of them universal.

| | property |
|---|---|
| P1 | the statement's universal words, on the small cases |
| P2 | the same answer, renamed, with the alphabet permuted at random in both lists |
| P3 | the same answer with `words2` reversed, each of its words' letters shuffled, and a front part of one of its words added |
| P4 | the answer is `words1` with some words left out, in order, and is universal for itself |
| P5 | one more random word in `words2` keeps only some of the answer |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases, 37491 words, 6932 universal, 95000 checks over 5
arms: 0 failures` under `karac __mir-run` (21 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the counts of `words2` added up, not the largest taken | P1 595, P3 988, P6 683 |
| M2 | ★: a word one letter short let through | P1 2443, P6 2641 |
| M3 | ★: z never checked | P2 136, P6 3 |
| M4 | sorted: a later letter matching a needed one | P1 1340, P2 1376, P6 1517 |
| M5 | sorted: the letters never sorted | P1 799, P2 179, P3 339, P6 920 |
| M6 | sorted: only the last word of `words2` needed | P1 936, P3 1376, P5 1058, P6 1064 |
| M7 | map: repeated letters counted once | P1 989, P6 1090 |
| M8 | map: a missing letter taken as present once | P1 1540, P6 1714 |
| M9 | map: a letter's first count kept, not its largest | P1 227, P3 453, P6 271 |
| M10 | decrement: a letter not owed counted as paid | P1 2219, P5 923, P6 2408 |
| M11 | decrement: a letter's need from the last word using it | P1 223, P3 469, P5 258, P6 268 |
| M12 | decrement: one letter left owing forgiven | P1 2086, P6 2243 |
| M13 | letters: a word holding exactly the needed count dropped | P1 1440, P6 1579 |
| M14 | letters: the first word of `words1` never a candidate | P1 763, P4 1347, P6 802 |
| M15 | letters: a never filtered | P1 1054, P2 1160, P6 1138 |

P6 kills all fifteen and P1 fourteen; P3 five, P2 four, P5 three and P4
one. M3 is the one P1 misses: the small cases use only a, b and c, so z
never appears, and only P2's permutation, which moves some letter onto
z, finds it; P6 sees it just 3 times, in the large cases over 26
letters. P4 is weak by design: an answer that is wrong for `words1` is
usually still universal for itself, so it only catches an arm that
drops a word it should keep whatever the input, as M14 does.

Three mutants were replaced, all in the M14 slot, because each failed
exactly the same checks as an earlier mutant and so told nothing new:
the need taken from the last word of `words2` only (as M6), a letter
needed once never filtered on (as M8, which also lets a single missing
letter through), and z never checked (as M3).

## Verification

Every arm prints the same output as `word_subsets.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 2.2 to 4.1 s each
and the differential 21 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The decrement arm prints the same output under the frozen legacy
interpreter, the legacy JIT and both legacy builds, with and without
auto-par; the builds also warn that `words1` is moved and then used
again, which v2's borrowing parameters make untrue. Legacy refuses the
other four arms, the differential and the bench program at the first
`*` on an element of a `Vec`'s `.iter()` ("unary '*' requires 'ref T',
... found 'String'"), legacy's older rule; under v2 the element is a
reference and the `*` is required. Legacy is frozen, so none of this is
filed.

## Benchmarks

The bench program uses the ★ arm on 50,000 words of 10 letters from a to
h, built once. Each round draws three words of 1 to 3 letters from a to
h as `words2`, finds the universal words and folds their letters into a
checksum; 200 rounds. Every implementation prints `200 rounds over
50000 words: 1676304 universal, checksum 9099770`. Kāra and Rust return
copies of the universal words and C `strdup`s them, as the problem
returns new strings; Go appends the same immutable string, which costs
nothing to share.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.36 to 0.42 s | 0.39 s |
| Rust (`rustc -O`) | 0.40 to 0.52 s | 0.44 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.41 to 0.53 s | 0.44 s |
| Go | 0.61 to 0.78 s | 0.68 s |
| Python | 16.8 s | |
| Kāra (`karac build --mir`) | 0.37 to 0.44 s | 0.40 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification).

v2 takes 0.91 times Rust's median time under overflow checks and 1.03
times C's. Under valgrind's cachegrind v2 runs 3.15 billion instructions
and 0.68 billion branches, against 3.74 billion and 0.87 billion for
Rust with overflow checks and 2.68 billion and 0.40 billion for C. Go
takes 1.7 times C's time; why was not profiled.

The ★ arm counts into an `Array[i64, 26]`, as C, Rust and Go count into
a fixed array on the stack. A first version counted into
`Vec.filled(26, 0)`, a heap allocation for every word: built the same
way it took 0.66 to 0.76 s, and cachegrind counted 7.50 billion
instructions, twice Rust's. The `Array` version gives the same output
under every lane, and its three mutants fail exactly the same checks as
under the `Vec` version. Under `karac __mir-run` the `Array` arm is the
slower of the two, 4.0 s against 2.2 s.
