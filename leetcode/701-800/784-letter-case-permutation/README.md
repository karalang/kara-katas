# 784. Letter Case Permutation

Given a string `s`, every letter of it can be put in lower case or in
upper case on its own, making another string. Return all the strings
that can be made this way, in any order.

```
s = "a1b2"  ->  ["a1b2", "a1B2", "A1b2", "A1B2"]
s = "3z4"   ->  ["3z4", "3Z4"]
```

**Constraints:** `s` has 1 to 12 characters, each a lower or upper case
English letter or a digit.

## Approaches

A string with `L` letters has `2^L` permutations, one for each choice of
case for each letter; the digits stay as they are. Every arm is `fn
letter_case_permutation(s: String) -> Vec[String]`, and each returns the
permutations in its own order, so the harness sorts them before
printing.

| file | mechanism |
|---|---|
| `letter_case_permutation.kara` ★ | backtracking over one buffer of the characters: a letter is set to lower case and the rest permuted, then to upper case and the rest permuted again, and every walk to the end copies the buffer out; O(2^L n) |
| `letter_case_permutation_bitmask.kara` | one bit for each letter: each number from 0 to `2^L - 1` spelled out over the string, bit `j` putting the `j`-th letter in upper case; O(2^L n) |
| `letter_case_permutation_doubling.kara` | every permutation of the string read so far, starting from the empty string: a digit is appended to each, and a letter doubles the list, each prefix taking it once in each case; O(2^L n) |
| `letter_case_permutation_gray.kara` | Gray code order: from every letter in lower case, step `k` flips the case of the letter that the lowest 1 bit of `k` names, so each permutation comes from the one before by a single change; O(2^L n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: LeetCode's two examples; digits only;
one letter; letters in mixed case; a letter in both cases with a digit;
twelve letters, LeetCode's most, with how many strings, the first and
last, and a checksum; then 300 random strings of 1 to 12 letters and
digits, with how many permutations they make and a checksum.
`letter_case_permutation.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every way of putting each character in lower or upper case, the digits
included, with the repeats removed by a `SortedSet`. Its 1,000 random
strings are a quarter of any letters and digits (1 to 12 characters), a
quarter letters only (1 to 10), a quarter digits only, and a quarter
digits with a letter in about one place in four.

| | property |
|---|---|
| P1 | the strings, sorted, are the definition's |
| P2 | there are `2^L` strings for `L` letters, no two the same |
| P3 | every string is `s` but for the case of its letters, and `s` itself is among them |
| P4 | `s` with the case of every letter swapped gives the same strings |

It prints `1000 strings (107683 permutations), 4 arms, 16000 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: digits tried in both cases too | P1 641, P2 641 |
| M2 | ★: upper case tried twice | P1 697, P2 697, P3 580 |
| M3 | ★: the last character never permuted | P1 524, P2 524, P4 524 |
| M4 | bitmask: every character counted as a letter | P1 641, P2 641 |
| M5 | bitmask: the first bit for every letter | P1 575, P2 575, P3 474 |
| M6 | bitmask: the count stopping one short | P1 1000, P2 1000, P3 420 |
| M7 | doubling: digits doubled too | P1 641, P2 641 |
| M8 | doubling: the upper copy keeping the input's case | P1 580, P2 580, P4 697 |
| M9 | doubling: digits dropped | P1 641, P3 641 |
| M10 | gray: a letter only ever raised | P1 575, P2 575, P3 402 |
| M11 | gray: the walk stopping one step early | P1 697, P2 697, P3 114 |
| M12 | gray: the letter chosen by the count of 1 bits | P1 575, P2 575, P3 290 |

P1 kills all twelve. P2 kills all but M9: dropping the digits leaves the
right number of strings, all different, and only P3 sees that they are
not `s` up to case. P4 sees just M3 and M8, the two mutants whose answer
depends on the case the input was written in: M3 never permutes the last
character, which keeps its case from the input, and M8 gives the upper
case copy the input's case. Every other mutant makes the same wrong
strings from either case. M1, M4 and M7 fail the same checks, all making
a digit in both cases, which gives repeats in every string with a digit.

## Verification

Every arm prints the same output as `letter_case_permutation.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the doubling arm, which prints the
same output under the legacy interpreter (`karac run --interp`), the
legacy JIT (`karac run`), `karac build` and an auto-par build. They
refuse the other three arms, the differential and the bench program at
the type check: in `for c in buf.iter()` they take the items for `char`
rather than references, so `*c` is an error. Copies of the ★ and bitmask
arms with those `*`s removed print the same output under all four; the
gray arm's copy fails in all four, since legacy has no
`is_ascii_lowercase` on a `char`. The legacy builds warn that a borrowed
`s` is used after a move, since legacy predates borrowed parameters. The
bench timing below is of a copy with its `*` removed. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 strings of 12
characters, LeetCode's limit, are made once, each with 6 to 11 letters
in random places and digits for the rest. Each of 20,000 rounds permutes
the next string and folds the first and last byte of every permutation
into a checksum. Every implementation prints `20000 rounds of
12-character strings: 10480704 permutations, checksum 520063910`, the
Kāra program under `karac __mir-run` included (in 292 s).

The rounds make 10.5 million strings of 12 characters, each its own
allocation, so the bench measures the recursion, building short strings
and the allocator. Kāra and Rust build each string by pushing `char`s
one by one, Go converts the byte buffer with `string(buf)`, C copies it
into a `malloc`ed buffer with `memcpy`, and Python joins a list. Spot
timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.37 to 0.46 s |
| Rust (`rustc -O`) | 0.65 to 0.75 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.75 to 0.89 s |
| Go | 0.49 to 0.58 s |
| Python | 5.15 to 5.70 s |
| Kāra (`karac build --mir`) | 1.07 to 1.27 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 8.6 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.16 s,
against C's 0.39, Rust's 0.69 (0.81 under overflow checks) and Go's
0.52. Under valgrind's cachegrind v2 runs 13.8 billion instructions and
2.46 billion branches, against C's 3.53 billion and 0.49 billion and
Rust's 8.68 billion and 1.25 billion; it mispredicts 121 million
branches, 26 million of them indirect, to C's 12 million and Rust's 29
million. Where v2's extra instructions lie is not profiled. The legacy
build of the copy ran 0.90 to 0.97 s, a median of 0.91 s in the
interleaved runs, so v2 takes 1.27 times legacy. The comparison with C
and Rust waits until after M4.

## Compiler findings

Nothing new.
