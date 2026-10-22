# 859. Buddy Strings

Given two strings `s` and `goal`, return `true` if you can swap two
letters in `s` so that the result is equal to `goal`, and `false`
otherwise. Swapping letters means choosing two different indices `i` and
`j` and exchanging `s[i]` and `s[j]`.

```
s = "ab", goal = "ba"  ->  true
s = "ab", goal = "ab"  ->  false
s = "aa", goal = "aa"  ->  true
```

**Constraints:** `1 <= s.length, goal.length <= 2 * 10^4`; `s` and `goal`
consist of lowercase letters.

## Approaches

| file | mechanism |
|---|---|
| `buddy_strings.kara` ★ | a swap changes exactly the two positions it touches, or nothing when their letters are equal. So the strings must have the same length and either differ at exactly two positions `i` and `j` with `s[i] == goal[j]` and `s[j] == goal[i]`, or be equal with some letter of `s` twice. One pass records the first two differing positions and stops at a third; with none, a flag per letter finds the repeat. O(n) time, O(1) space |
| `buddy_strings_counts.kara` | a swap keeps the letters, so both strings hold the same count of every letter; given that, two differing positions must hold each other's letters. Equal lengths, equal counts, and two differences, or none and a count of two. It reads both strings to the end. O(n) |
| `buddy_strings_swap.kara` | the only swap that can work is the one of the first and the last differing positions: it is made on a copy of `s`, and the copy compared with `goal`. Equal strings look for a repeat with a `Set`. O(n) time and space |
| `buddy_strings_brute.kara` | every pair of positions `i < j` swapped in a copy of `s` and compared with `goal`. O(n^3) |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's three examples; eleven
more (one letter, lengths that differ, two swaps, three differences, a
repeat among equal strings); the count of buddies among all 729 pairs of
strings of three letters over `a`, `b` and `c`, which is 75 (21 equal
strings with a repeated letter and 54 swaps of two different letters);
and 2,000 random pairs of up to 30 letters, `goal` made from `s` by one
of five edits, with the count of buddies and a checksum.
`buddy_strings.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every pair of different indices, in either order, swapped in
a list of the characters of `s`, the list read back as a string and
compared with `goal`. Its 2,500 pairs are all 1,521 pairs of strings of
one to three letters over three letters and 979 random pairs of up to
twelve letters over one to five, `goal` made from `s` as in the arms; 622
of them are buddies.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | symmetric: `goal` and `s` exchanged give the same answer |
| P3 | `s` against itself is a buddy exactly when it has a repeated letter |
| P4 | `s` with two positions holding different letters swapped is a buddy |
| P5 | every letter of both strings moved the same number of places round the alphabet gives the same answer |
| P6 | `s` with one letter added is never a buddy |

P4 is checked on the pairs whose `s` has two different letters.

It prints `2500 pairs, 622 buddies, 57512 checks over 4 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a third difference not refused | P1 36 |
| M2 | ★: equal strings always buddies | P1 110, P3 748 |
| M3 | ★: only one of the two cross checks | P1 60, P2 120 |
| M4 | counts: the letter counts not compared | P1 300 |
| M5 | counts: a repeat read as a count of three | P1 93, P3 965 |
| M6 | counts: equal strings accepted without a repeat | P1 110, P3 748 |
| M7 | swap: the swap made on a copy of `goal` | P1 394, P2 192, P4 1878 |
| M8 | swap: the copy compared short of the last difference | P1 60, P2 120 |
| M9 | swap: the repeat never found | P1 420, P3 1752 |
| M10 | brute: `i` equal to `j` allowed | P1 110, P3 748 |
| M11 | brute: only the first position compared | P1 599, P2 287, P3 253 |
| M12 | brute: `s` compared with `goal` in place of the swap | P1 246, P3 537, P4 1878 |

P1 kills all twelve. M2, M6 and M10 are the same fault, equal strings
accepted whatever their letters, and fail the same cases. M3 and M8 each
check only one of the two exchanged letters, and fail the same 60 pairs
and the same 120 symmetric checks. P5 and P6 kill nothing: none
of the mutants depends on which letters are used, and every arm compares
the lengths first. Three mutants tried first were equivalent and were
replaced: in the counting arm a single difference always leaves the
counts unequal, so accepting one changes nothing, and in the swap arm a
single difference swapped with its neighbour or with itself can never
match `goal`. Two more ended the run with an index out of bounds rather
than a wrong answer, and were replaced as well.

## Verification

Every arm prints the same output as `buddy_strings.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are at kara `79705a2290`. Under `karac __mir-run` the arms take
0.3 to 1.1 s and the differential 1.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run the counting and brute-force arms through
`karac run --interp`, `karac run`, `karac build` and a
`KARAC_AUTO_PAR=1` build with the same output. They refuse the ★ and
swap arms, the differential and the bench program at `*c`, over a
`for` of the bytes of a string, saying the element is a `u8` that is
copied, where v2 yields a reference to each element. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm on the bytes of the strings, in all
five languages: two strings of 20,000 letters, LeetCode's longest, built
once, and 40,000 rounds that each edit `goal` in place (two positions
swapped, one letter changed, or two swaps), ask whether it is a buddy of
`s`, and undo the edit. Every implementation prints `40000 rounds on
20000 letters: 14347 buddies, checksum 748972932`, the Kāra program
under `karac __mir-run` included, in 440 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.34 to 0.47 s |
| Rust (`rustc -O`) | 0.24 to 0.38 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.23 to 0.32 s |
| Go | 0.69 to 1.00 s |
| Python | 24.8 to 26.3 s |
| Kāra (`karac build --mir`) | 0.22 to 0.35 s |

Legacy refuses the bench program (see Verification), so it has no
timing. `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 0.24 s, against Rust's
0.27 (0.25 under overflow checks), C's 0.38 and Go's 0.80: 0.96 times
Rust's time under overflow checks, 0.63 times C's and 0.30 times Go's.
Under valgrind's cachegrind C runs 3.73 billion instructions and 1.02
billion branches, Rust 3.06 billion and 1.02 billion, and v2 2.45
billion and 0.81 billion; none mispredicts more than 0.2 million. Built
for `x86-64-v3`, the target `karac build` uses, C takes 0.23 to 0.29 s
and Rust with overflow checks 0.28 to 0.34 s, against v2's 0.24 to 0.29
s in the same five interleaved runs: built for the same target, C
matches v2. Python takes 25 s, about 66 times C's time. The
comparison with C and Rust waits until after M4.
