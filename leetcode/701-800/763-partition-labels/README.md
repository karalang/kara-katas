# 763. Partition Labels

Split a string `s` of lowercase letters into as many parts as possible
so that each letter appears in at most one part, and return the sizes of
the parts, in order. The parts joined in order must be `s`.

```
"ababcbacadefegdehijhklij"  ->  [9, 7, 8]
"eccbbbbdec"                ->  [10]
```

**Constraints:** 1 <= `s.length` <= 500; `s` is lowercase English
letters.

## Approaches

| file | mechanism |
|---|---|
| `partition_labels.kara` ★ | record each letter's last appearance; walk the string, stretching the current part's end to the last appearance of each letter met, and close the part when the walk reaches its end; O(n) |
| `partition_labels_intervals.kara` | each letter's span, first appearance to last, from two `Map`s; sort the spans and merge those that overlap, each merged span a part |
| `partition_labels_counts.kara` | count each letter, then walk, using up the counts and tracking how many letters seen are not used up; a part ends wherever that falls to zero |
| `partition_labels_masks.kara` | the letters of every prefix and every suffix as 26-bit masks; a part ends after i wherever the prefix's and the following suffix's masks share no bit |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: the two LeetCode examples; one
letter; three different letters; a letter at both ends; three pairs;
spans that chain into one long part with one letter left over; the
alphabet backwards with `z` again at the end; then 300 random strings of
up to 500 letters whose letters drift through the alphabet, so that most
fall into several parts, with the number of parts and a checksum of
their sizes. `partition_labels.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which ends a part after position i wherever no letter appears both up to
i and after it, comparing the letters pair by pair. 1,500 random strings
of up to 40 letters are checked against it, and 300 of up to 500 against
the other properties.

| | property |
|---|---|
| P1 | the answer is the definition's (the 1,500 short strings) |
| P2 | it is a partition: positive sizes adding up to the length, with no letter in two parts |
| P3 | the string reversed has the sizes reversed |
| P4 | renaming the letters one to one, by a random permutation of the alphabet, changes nothing |

It prints `1800 strings (23953 parts), 4 arms, 27600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error; the count of parts is the ★
arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each letter's first appearance taken for its last | P1 959, P2 1246, P3 1246 |
| M2 | ★: the part's end replaced, not stretched | P1 513, P2 726, P3 726 |
| M3 | ★: each size one short | P1 1500, P2 1800 |
| M4 | intervals: spans that only touch merged | P1 1468 |
| M5 | intervals: spans sorted by their ends | P1 469, P2 636, P3 423 |
| M6 | intervals: the merged end replaced, not stretched | P1 469, P2 594, P3 423 |
| M7 | counting: a letter closed one appearance early | P1 1500, P2 1800, P3 973 |
| M8 | counting: a part ended with one letter still open | P1 959, P2 1246 |
| M9 | counting: every letter counted twice | P1 1500, P2 1800 |
| M10 | masks: the suffix taken from i, not after it | P1 1500, P2 1800 |
| M11 | masks: suffix letters toggled, not added | P1 453, P2 730, P3 724 |
| M12 | masks: each prefix holding only its last letter | P1 513, P2 726, P3 726 |
| E1 | ★: last appearances started at -1 | 0 |
| E2 | intervals: the first end started at 0 | 0 |
| E3 | masks: one spare suffix slot | 0 |

P1 kills all twelve, and P4 none: every arm treats all letters alike, so
renaming them cannot change what any edit does. M4 merges spans that
only touch, which still gives a partition, just with fewer parts than it
could have, so only P1 sees it; reversing the string keeps such a merge
where it was, so P3 misses it too. M3, M9 and M10 break the sizes the
same way on every string and P3 cannot see them either, since the
reversed string is broken alike. E1 starts the last appearances at
-1 instead of 0, but a letter that never appears is never looked up;
E2 starts the first merged span's end at 0, but the first span starts at
0 and stretches it at once; E3 gives the suffix masks a slot that is
never read.

## Verification

Every arm prints the same output as `partition_labels.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a62eacd307`, whose last compiler change is `7d736aae75`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse every arm, the differential and the
bench at a `*` over an element of `iter()`, which legacy gives by value
where v2 gives references: the harness's `*size` in every arm, and
`(*at, last[*letter])` in the interval arm itself. The legacy timings
below are of a copy of the bench that writes `size` for `*size`, which
prints the same line. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, on
100,000 random strings of 500 letters, the most LeetCode allows, built
as the arms' random strings are, adding up the number of parts and a
checksum of their sizes. Every implementation prints `100000 strings of
500 letters: 730100 parts, checksum 371918971`, the Kāra program under
`karac __mir-run` included (in 142 s). Building the strings is part of
the timed work in every language.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.15 to 0.18 s |
| Rust (`rustc -O`) | 0.26 to 0.32 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.24 to 0.30 s |
| Go | 0.47 to 0.55 s |
| Python | 26.6 to 27.3 s |
| Kāra (`karac build --mir`) | 0.56 to 0.67 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
4.1 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.65 s,
against C's 0.15, Rust's 0.27 (0.26 under overflow checks) and Go's
0.52. Under valgrind's cachegrind v2 runs 7.2 billion instructions, Rust
3.4 billion and C 1.7 billion; C writes each letter into a fixed array,
where the others append one-letter slices to a growing string, and the
Kāra program then copies it into a `Vec[char]`; that these account for
the gap is inferred, not profiled. The legacy build of the copy ran
0.38 to 0.45 s, a median of 0.39 s in the interleaved runs, so v2 takes
1.7 times as long as legacy, inside M2's limit of twice legacy; new
katas' benches are outside M2's frozen set in any case. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new.
