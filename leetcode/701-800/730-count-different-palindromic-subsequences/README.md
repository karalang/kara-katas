# 730. Count Different Palindromic Subsequences

Given a string `s`, return the number of different non-empty palindromic
subsequences of `s`, modulo 10^9 + 7. A subsequence is what is left
after deleting any number of characters, none included, and it is
palindromic when it reads the same reversed. Two subsequences are
different when they differ as strings, wherever in `s` they were taken
from.

```
s = "bccb"   ->  6     (b, c, bb, cc, bcb, bccb)
s = "abcdabcdabcdabcdabcdabcdabcdabcddcbadcbadcbadcbadcbadcbadcbadcba"
             ->  104860361   (3104860382 modulo 10^9 + 7)
```

**Constraints:** 1 <= `s.length` <= 1000; each `s[i]` is `a`, `b`, `c`
or `d`.

## Approaches

All four arms count over intervals of the string, in one of two ways: by
the interval's two end letters, or by the outer letter of the
palindrome, whose first and last copies in the interval stand for every
pair of it, so that nothing is counted twice.

| file | mechanism |
|---|---|
| `count_different_palindromic_subsequences.kara` ★ | count[i][j] by the end letters: when they differ, the two shorter intervals less their overlap; when they match, the inside doubled and corrected by the copies of that letter strictly inside, found from tables of the next and previous copy; O(n^2) time and space |
| `count_different_palindromic_subsequences_letters.kara` | one table per end letter, the palindromes of each interval that begin and end with it, in one flat vector; an interval whose ends are both c holds c, cc, and c ... c around every palindrome inside; O(4 n^2) time and space |
| `count_different_palindromic_subsequences_outer.kara` | by outer letter, top down: c, then cc and c ... c around the inside's count when c appears twice, with the inside counts memoized; O(4 n^2) time, O(n^2) space, recursion depth up to n / 2 |
| `count_different_palindromic_subsequences_lengths.kara` | the outer-letter count bottom up by interval length, the first and last copies from tables of next and previous copies; O(4 n^2) time, O(n^2) space |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 14 lines: the two LeetCode examples; seven
short strings, among them a single letter, four a's, the four letters
once each and palindromes of three to seven letters; 1,000 random
letters, the problem's longest; 1,000 random a's and b's; 1,000 a's,
which hold exactly the 1,000 palindromes of a's; abcd 250 times; and
300 random strings of up to 30 letters with a checksum.
`count_different_palindromic_subsequences.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which takes every subsequence, one for each subset of places, and keeps
those that read the same both ways in a set. 3,000 random strings are
checked, each of 1 to 10 letters drawn from the first 1 to 4 of a to d,
so repeated letters are common; the most palindromes any of them holds
is 46.

| | property |
|---|---|
| P1 | the count is the definition's |
| P2 | the string reversed gives the same count |
| P3 | the letters renamed, a to d and b to c, give the same count |
| P4 | with no d in the string, a d at both ends gives twice the count plus two: each palindrome alone and wrapped in d ... d, and d and dd |

It prints `3000 strings (most 46 palindromes), 4 arms, 45848 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: with no copy inside, only one of c and cc added | P1 1956, P4 2462 |
| M2 | ★: the palindromes wrapped twice never taken away | P1 1043 |
| M3 | ★: with different end letters, the inside counted twice | P1 1552 |
| M4 | letters: only one of c and cc added | P1 2492, P4 2462 |
| M5 | letters: a last letter that is not c dropping the first as well | P1 1910, P2 1029, P4 2412 |
| M6 | letters: palindromes of d never wrapped | P1 322, P3 1881 |
| M7 | outer: a letter alone never counted | P1 3000, P4 2462 |
| M8 | outer: the inside taken from the first copy itself | P1 2492, P2 994, P4 2462 |
| M9 | outer: the last copy looked for before j | P1 2331, P2 1203, P4 2462 |
| M10 | lengths: cc never counted | P1 2492, P4 2462 |
| M11 | lengths: the interval's first letter never an outer copy | P1 3000, P2 894, P4 2183 |
| M12 | lengths: the inside taken with its outer pair | P1 2080, P4 1355 |
| E1 | ★: a non-empty inside tested as i + 2 <= j | 0 |
| E2 | lengths: the count reduced as (total + m) % m | 0 |
| E3 | letters: the rest tested as i < j | 0 |

P1 kills all twelve, and M2 and M3 only P1 sees: both give the same
count for a string, for it reversed and for it with its letters renamed,
and keep the rule for a string wrapped in a new letter, so they are
wrong only against the definition itself. P2 sees M5, M8, M9 and
M11, which treat an interval's two ends differently, so that reversing
the string changes the count. P3 sees only M6, which never wraps
palindromes of d: renaming the letters moves that mistake onto other
strings. P4 misses M2, M3 and M6, and is checked only on strings with no
d, which is why the line counts fewer than 48,000 checks. M4 and M10 are
one mistake in two arms, cc never counted, and fail as many strings
under every property. E1 tests a non-empty inside as i + 2 <= j,
E2 reduces the count as (total + m) % m, which a count already reduced
and not negative leaves as it was, and E3 tests the rest of the interval
as i < j.

## Verification

Every arm prints the same output as
`count_different_palindromic_subsequences.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer) with no error; the differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. The debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the release
build that runs `check` and `__mir-run` are both at kara `969445f00a`,
whose last compiler change is `b830c8f243`. The runtime archives were
built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms, which print the same
output under the legacy `karac build`, sequential and with
`KARAC_AUTO_PAR=1`, and under its JIT; the legacy interpreter did not
finish any of them within the check's 60 s limit, with four strings of
1,000 letters to count. They refuse the differential at type checking,
at `*c` over a vector's `iter()`, since legacy gives those by value
where v2 gives references. They accept the bench program, which prints
the same line under the legacy `karac build` in 0.53 to 0.62 s over
three runs (below). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
200 random strings of 1,000 letters from a to d, the problem's largest,
each just before it is counted, and sums the counts modulo 10^9 + 7. The
C program's table is an array of row pointers, as Rust's is a vector of
vectors. Every implementation prints `200 strings of 1000 letters: sum
87822787`, the Kāra program under `karac __mir-run` included (in
2.2 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.88 to 1.12 s |
| Rust (`rustc -O`) | 1.04 to 1.24 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.10 to 1.14 s |
| Go | 1.40 to 1.51 s |
| Python | 19.5 to 20.0 s |
| Kāra (`karac build --mir`) | 0.77 to 0.88 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
3.9 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is ahead of all four at the medians of the interleaved
runs: 0.80 s against C's 0.98, Rust's 1.11, Rust's under overflow checks
1.13 and Go's 1.44. Under valgrind's cachegrind it nonetheless runs
9.6 billion instructions against C's 4.9 and Rust's 5.5, and 3.3 billion
branches against 2.0 and 0.8, with 31 million of them mispredicted in
all three. Why the program that does the most counted work takes the
least time was not traced; the table is a million numbers, 8 MB, so the
time is likely in memory rather than in instructions. The legacy build
of the same program is faster still, 0.53 to 0.62 s, about two thirds of
v2's time; that is within M2's limit of twice legacy, and new katas'
benches are outside M2's frozen set, so it is noted, not filed. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new.
