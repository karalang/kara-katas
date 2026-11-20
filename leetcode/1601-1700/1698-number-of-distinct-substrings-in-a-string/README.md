# 1698. Number of Distinct Substrings in a String

Given a string `s`, return *the number of **distinct** substrings of*
`s`.

A **substring** of a string is obtained by deleting any number of
characters (possibly zero) from the front of the string and any number
(possibly zero) from the back of the string.

```
s = "aabbaba"   ->  21
s = "abcdefg"   ->  28
```

**Constraints:** `1 <= s.length <= 500`; `s` consists of lowercase
English letters.

**Follow up:** Can you solve this problem in `O(n)` time complexity?

## Approaches

| file | mechanism |
|---|---|
| `distinct.kara` ★ | a substring is a prefix of a suffix, so each suffix walked into a trie makes one new node per substring not met before; the trie is a `Vec` of 26 children per node. O(n^2) time and nodes |
| `distinct_set.kara` | each of the n(n + 1) / 2 substrings copied into a `Set[String]`, whose size is the answer. O(n^3) |
| `distinct_lcp.kara` | the suffixes sorted as `Str` slices: each shares with the one before it exactly the prefixes already counted, so the answer is n(n + 1) / 2 less the longest common prefix of each neighbouring pair. O(n^2 log n) |
| `distinct_automaton.kara` | a suffix automaton, a `struct State` of length, link and 26 transitions, built a letter at a time with clones for split states; the answer is the sum of len[v] - len[link[v]] over the states. The follow-up's O(n), times 26 |
| `differential.kara` | the four arms against the statement read literally, five properties |

LeetCode offers no Rust template for this problem, so there is no
Rust-template arm.

Every arm prints the same 8 lines: LeetCode's two examples, one letter,
one letter four times, and a pair twice; then the answers summed and a
checksum for 3000 random strings of up to 12 letters from up to 4, 300
of up to 100 from up to 4 and 10 of up to 500 from up to 26.
`distinct.py` mirrors the ★ arm and its output is byte-identical.

```
21
28
1
4
7
3000 strings of up to 12 letters from up to 4: answers sum to 57861, checksum 775236908
300 strings of up to 100 letters from up to 4: answers sum to 381605, checksum 181385849
10 strings of up to 500 letters from up to 26: answers sum to 421048, checksum 712688979
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every substring, from every start to every end, is counted
unless the same letters were met at an earlier start and end, compared
letter by letter. It checks 3000 random strings of 1 to 10 letters from
the first 1 to 4 of the alphabet. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed gives the same answer |
| P3 | the letters renamed, a to c, b to a, c to d and d to b, give the same answer |
| P4 | a letter not in the string put at the end adds the string's length plus one |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 840315874, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the size of a `set` of every slice, gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1, M3 and M4 each leave out the
whole string, or its first letter's suffixes, and fail the same checks;
M2 and M5 fail the same checks too. Only M7, which compares letters by
order, depends on which letters they are, so it alone fails P3.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each suffix walked from its second letter | P1 3000, P2 906, P4 3000, P5 3000 |
| M2 | ★: a new node linked to the one before it | P1 1915, P2 906, P4 3000, P5 1915 |
| M3 | ★: the first suffix left out | P1 3000, P2 906, P4 3000, P5 3000 |
| M4 | set: no substring reaches the end | P1 3000, P2 906, P4 3000, P5 3000 |
| M5 | set: each substring one letter short | P1 1915, P2 906, P4 3000, P5 1915 |
| M6 | lcp: one less taken off for each pair | P1 2703, P4 3000, P5 2703 |
| M7 | lcp: a common prefix grown while a letter is not above the other | P1 1915, P2 965, P3 922, P4 2979, P5 1915 |
| M8 | automaton: a state never split | P1 1316, P2 1239, P5 1316 |
| M9 | automaton: the split state's link left as it was | P1 1316, P2 1036, P5 1316 |
| M10 | automaton: each state's whole length counted | P1 2508, P2 1029, P5 2508 |

## Benchmarks

The bench draws 100 random strings of 500 letters, LeetCode's longest,
each from the first 2 to 26 letters of the alphabet, all of them first,
then answers each 3 times by the ★ arm in all five languages: a `Vec` of
26-child `Vec`s in Kāra and Rust, lists in Python, slices in Go, and in
C one growable array of 26-child rows. Every implementation prints `100
strings of 500 letters, 3 rounds: answers sum to 37245591, checksum
630392278`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.447 s |
| Kāra (`karac build`) | 1.370 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.432 s |
| Rust (`rustc -O`) | 3.675 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.757 s |
| Go | 5.044 s |
| Python | 21 s |

The sequential Kāra build is 61% faster than Rust and 62% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md). C is the fastest here at 0.447 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.312 s and 1.337 s on one
run).

## Verification

All four arms print the same output as `distinct.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

All four arms, the differential and the bench checked clean as first
written. `arm_name` in the differential indexes a list of string
literals for a `Str`, as #1662's does (B-2026-11-19-131).
