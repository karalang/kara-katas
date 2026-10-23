# 893. Groups of Special-Equivalent Strings

You are given an array of strings of the same length `words`.

In one move, you can swap any two even indexed characters or any two
odd indexed characters of a string `words[i]`.

Two strings `words[i]` and `words[j]` are special-equivalent if after
any number of moves, `words[i] == words[j]`.

- For example, `words[i] = "zzxy"` and `words[j] = "xyzz"` are
  special-equivalent because we may make the moves `"zzxy" -> "xzzy" ->
  "xyzz"`.

A group of special-equivalent strings from `words` is a non-empty subset
of words such that every pair of strings in the group are
special-equivalent, and the group is the largest size possible (i.e.,
there is not a string `words[i]` not in the group such that `words[i]`
is special-equivalent to every string in the group).

Return the number of groups of special-equivalent strings from `words`.

```
words = ["abcd","cdab","cbad","xyzz","zzxy","zzyx"]  ->  3
words = ["abc","acb","bac","bca","cab","cba"]  ->  3
```

**Constraints:** `1 <= words.length <= 1000`, `1 <= words[i].length <=
20`, `words[i]` consists of lowercase English letters, and all the
strings are of the same length.

## Approaches

Swaps among the even positions can put their letters in any order, and
likewise the odd ones, but no letter ever crosses from one set to the
other; so two words are special-equivalent exactly when they hold the
same letters at even positions and the same at odd positions. The arms
differ in how they compare that.

| file | mechanism |
|---|---|
| `num_special_equiv_groups.kara` ★ | a count of letters at even and at odd positions: the 52 counts written as a string key into a `Set`, and the groups are the keys. O(total letters) |
| `num_special_equiv_groups_sorted.kara` | the even and odd letters, each sorted: the sorted even letters and then the sorted odd ones are the key. O(total letters * log length) |
| `num_special_equiv_groups_unionfind.kara` | union-find over every pair: every two words compared by their 52 counts, the equivalent ones joined, and the roots left counted. O(n^2 + total letters) |
| `num_special_equiv_groups_leaders.kara` | one word to lead each group: the first word of each group kept as its sorted even and odd letters, and each word joining the first leader that matches or starting a group. O(n * groups * length) |
| `num_special_equiv_groups_keys.kara` | the keys sorted and the changes counted: each word's 52 counts as a vector, the vectors sorted, and the groups counted where a vector differs from the one before. O(n log n * 52) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples and four more
(a repeated one-letter word, two letters swapped across parities, two
pairs of equivalent words, and three 20-letter words: the alphabet to
`t`, the same with its first 19 letters reversed, which keeps every
letter's parity, and the whole word reversed, which flips it), and for 100 random cases of LeetCode's sizes, up to 1,000
words of up to 20 letters from 2 to 26 letters, half of them an earlier
word moved within its group, the number of groups, 19,162 among 48,608
words, with a checksum. `num_special_equiv_groups.py` mirrors the ★ arm
and its output is byte-identical.

Moving a word within its group needs its letters in something that can
be swapped, and `word.bytes()` is a read-only `Slice[u8]`, so the
harness copies it with `word.bytes().to_vec()`. Writing it, `to_vec()`
on a `Vec` receiver turned out to be refused by the typechecker
although the library reference says a `Vec` finds every `Slice` method;
that is filed as kara `B-2026-10-23-5` and does not affect this kata,
which only calls it on a `Slice`.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every word one move reaches, two even positions or two odd
positions swapped, and every word any number of moves reaches, by a
breadth-first search; each word not yet placed starts a group and takes
with it every later word it reaches. It checks 3,200 random cases: 3,000
of up to 8 words of up to 5 letters from 2 or 3 letters against the
statement, and 200 of up to 100 words of up to 20 letters from 2 to 26
against the other properties, half of the words an earlier word moved
within its group. The ★ arm finds 11,445 groups among 23,492 words.

| | property |
|---|---|
| P1 | the statement's groups, on the small cases |
| P2 | between 1 and n groups, and the same for the words reversed and for every word given twice |
| P3 | each word moved within its group by random swaps leaves the count unchanged |
| P4 | every letter renamed by one random permutation of the alphabet leaves the count unchanged |
| P5 | the words cut in two at a random place: the two parts' groups add up to at least the whole's, and neither part has more |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 23492 words,
11445 groups in all, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every letter counted with the even ones | P1 541, P6 582 |
| M2 | ★: each count capped at one | P1 80, P6 109 |
| M3 | ★: the position moved on by two, every letter counted as even | P1 541, P6 582 |
| M4 | sorted: the even letters never sorted | P1 717, P3 601, P6 894 |
| M5 | sorted: the odd letters left out of the key | P1 869, P6 934 |
| M6 | sorted: the last letter left out | P1 1285, P3 639, P6 1472 |
| M7 | unionfind: words joined when only their even letters agree | P1 869, P6 934 |
| M8 | unionfind: each word compared only with the next | P1 1264, P2 2299, P6 1450 |
| M9 | unionfind: every word counted as a root | P1 2403, P2 3200, P6 2596 |
| M10 | leaders: a word compared only with the last leader | P1 1264, P2 2299, P6 1450 |
| M11 | leaders: the odd letters never compared | P1 869, P6 934 |
| M12 | leaders: the letters never sorted | P1 863, P3 617, P6 1040 |
| M13 | keys: the keys never sorted | P1 1264, P2 2299, P6 1450 |
| M14 | keys: the first key not counted | P1 3000, P2 901, P5 373, P6 3200 |
| M15 | keys: neighbouring keys compared on their count of `a` alone | P1 1235, P4 1752, P6 1426 |

P1 and P6 kill all fifteen. The mutants fall into a few faults shared
across arms, which fail the same cases: ignoring the parity (M1, M3),
ignoring the odd letters (M5, M7, M11), and joining only words that sit
next to each other (M8, M10, M13), which P2 catches because reversing
or doubling the list changes which words sit together. P3 kills the
mutants that compare unsorted letters (M4, M12) or drop a position
(M6), as moving a word within its group then changes its key, and P4
the one that looks only at the letter `a` (M15).

Two mutants were replaced because they never change an answer. The
first M2 never counted the letter `a`; but all the words have the same
length, so the counts of the other letters fix how many `a`s sit at
even and at odd positions. The first M6 dropped the separator between
the even and odd letters in the sorted arm's key, which the shared
length also makes unambiguous.

## Verification

Every arm prints the same output as `num_special_equiv_groups.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 2.6 to 15.6 s
each (the union-find arm, which compares every pair, is the slow one)
and the differential 37 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every frozen legacy lane, the interpreter, the JIT and `karac build
--legacy` with and without auto-par, refuses all five arms, the
differential and the bench program: `*c` on an element of `.iter()` is
rejected, because legacy's iterator gives the value itself. Legacy is
frozen, so this is not filed.

## Benchmarks

The bench program uses the union-find arm, the same algorithm in all
five languages with no set, map or library sort: 300 random lists of
1,000 words of 20 letters, LeetCode's largest, half of each list an
earlier word moved within its group. Kāra's and Rust's counts are
vectors compared with `==`, Go's are arrays of 52 compared with `==`,
and C compares its arrays in a loop. Every implementation prints `300
lists of 1000 words of 20 letters: 149987 groups, checksum 274535237`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.77 to 0.92 s | 0.82 s |
| Rust (`rustc -O`) | 0.61 to 0.82 s | 0.69 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.64 to 0.73 s | 0.70 s |
| Go | 0.62 to 0.70 s | 0.65 s |
| Python | 12.3 s | |
| Kāra (`karac build --mir`) | 1.31 to 1.45 s | 1.36 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 892's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 1.95 times Rust's median time under overflow checks and 1.66
times C's. Almost all of the time is the comparison of two words'
counts. Under valgrind's cachegrind C runs 1.96 billion instructions
and mispredicts 22% of its branches, Rust with overflow checks 5.88
billion and 1.7%, and v2 5.16 billion and 9.1%. Rust's `==` on two
`Vec<i64>` calls `bcmp`, which compares many bytes at once without a
branch for each element (154 million indirect branches); C's loop and
v2's stop at the first difference, so their branches follow the data.
The IR that v2 writes out (`KARAC_MIR_LL`) compares the vectors element
by element, with a bounds check on each side for every element; whether
those survive LLVM's optimization was not checked. The comparison with
C and Rust waits until after M4.
