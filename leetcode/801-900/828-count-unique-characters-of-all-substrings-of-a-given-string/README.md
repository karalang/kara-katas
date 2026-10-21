# 828. Count Unique Characters of All Substrings of a Given String

Let `countUniqueChars(t)` be the number of characters that appear
exactly once in `t`. Given a string `s`, return the sum of
`countUniqueChars(t)` over every substring `t` of `s`. Substrings that
are equal but sit at different places are counted separately.

```
s = "ABC"       ->  10
s = "ABA"       ->  8
s = "LEETCODE"  ->  92
```

**Constraints:** `1 <= s.length <= 10^5`, `s` holds uppercase English
letters only.

## Approaches

Turn the sum around: rather than count the unique letters of each
substring, count for each position the substrings in which its letter is
unique. The letter at `i` is unique in a substring exactly when the
substring holds `i` and no other copy of that letter, so it starts after
the previous copy and ends before the next one: `(i - prev) * (next -
i)` substrings, with `prev` taken as -1 and `next` as `n` where there is
no copy.

| file | mechanism |
|---|---|
| `unique_letter_string.kara` ★ | one pass keeping the last two positions of each letter, which settles the middle copy's count each time its letter recurs, and a closing pass for the last copy of each letter. O(n) |
| `unique_letter_string_dp.kara` | the total over the substrings ending at each position, carried along: extending them by `s[i]` makes its letter unique in the `i - last` that start after its previous copy and takes it away from the `last - before` that start between its two previous copies. O(n) |
| `unique_letter_string_positions.kara` | the positions of each letter in its own list between the sentinels -1 and `n`, and each copy's count read off its neighbours in the list. O(n) |
| `unique_letter_string_iter.kara` | per letter, a `filter` over the indices `chain`ed between the two sentinels, and the counts a `map` over `windows(3)` of that list, all summed. O(26 n) |
| `differential.kara` | the four arms against the statement read substring by substring, four properties |

Every arm prints the same 13 lines: LeetCode's three examples; six small
strings (one letter; a letter twice and four times; a pair repeated; the
alphabet; and the alphabet backwards with a second `Z` after it); three
strings of LeetCode's greatest length, 100,000 letters at random over
all 26, over two, and over one; and 300 random strings of up to 30
letters over up to six, with a total and a checksum.
`unique_letter_string.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every substring, and in it the letters seen exactly once,
counted as the substring grows to the right. Its 1,600 cases are strings
of up to 20 letters and come in four kinds of 400: over one to three
letters, so that most recur; over up to all 26, so that most do not;
runs of one letter; and a block of up to four letters repeated.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the string reversed gives the same answer |
| P3 | the letters renamed, each moved the same distance round the alphabet, give the same answer |
| P4 | a letter the string does not hold, appended, adds `n + 1` and the unique letters of every suffix |

P4's addition is the substrings that end at the new letter: each holds
that letter once, and a suffix of the string before it.

It prints `1600 cases, 25600 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the closing pass dropped | P1 1600, P2 894, P4 1600 |
| M2 | ★: a copy's substrings start anywhere before it | P1 1219, P2 736 |
| M3 | ★: the closing pass stops before `Z` | P1 6, P2 2, P3 198, P4 6 |
| M4 | dp: the substrings that lose the letter not taken away | P1 1441, P4 1441 |
| M5 | dp: the total the last position's alone | P1 1535, P2 694, P4 1600 |
| M6 | dp: the gain one short | P1 1600, P4 1600 |
| M7 | positions: the sentinel `n` left out | P1 1600, P2 894, P4 1600 |
| M8 | positions: the sentinel 0, not -1 | P1 1600, P2 694, P4 1600 |
| M9 | positions: the positions counted from 1 | P1 873, P2 694, P4 1600 |
| M10 | iter: the two spans added, not multiplied | P1 1549, P4 1539 |
| M11 | iter: the sentinel 0, not -1 | P1 1600, P2 694, P4 1600 |
| M12 | iter: the sentinel `n - 1`, not `n` | P1 1600, P2 694, P4 1600 |

P1 kills all twelve. P3 sees only M3: every arm treats the letters
alike, so renaming them can only expose an edit that does not, and M3
forgets the last copy of `Z` alone, which the random strings rarely hold
and a renaming often makes. P2 sees the edits that treat the two ends of
the string differently, and is blind to M4, M6 and M10, which miscount
the same at both ends. M1 and M7 are the same mistake in two arms, the
last copy of each letter never counted, and fail the same cases. The
first edit tried for M3, the copy before last never moved, failed 1,441
cases under P1 and P4 and none under P2 or P3, the same counts as M4,
most likely the same miscount in another arm (not traced). It showed P3
nothing, so it was replaced by an edit that depends on which letter is
which.

## Verification

Every arm prints the same output as `unique_letter_string.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release build
that runs `check` and `__mir-run` and the debug build that runs
`__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` are both at kara
`90714715b1`, with the runtime archives built from that tree; the
mutation runs used the release build at `c342322052`.

Under `karac __mir-run` the ★, dp and positions arms take about 1 s each
and the iterator arm 23 s, with the same output; the differential takes
13 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for the ★, dp and positions arms. Legacy refuses the iterator arm and
the differential that copies it: its interpreter has no `cloned` on the
literal's iterator, and its compiled backends no handler for the
`collect` after the `chain`. Its checker refuses the bench program,
which passes `strings[round % count]` to a bare parameter and so, under
legacy's rules, moves it out of an index. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 32
strings of 100,000 letters, LeetCode's greatest length, once, the g-th
over the first `1 + g % 26` letters, so that some letters recur every
few places and some hardly at all. Each of 12,800 rounds answers the
next string. Every implementation prints `12800 rounds of 32 strings:
total 251285114000, checksum 335896320`, the Kāra program under `karac
__mir-run` included, in 1,287 s with the interpreter's step limit raised
by `KARAC_MIR_MAX_STEPS`.

The timed Kāra binary was built at kara `10d45bb347`, from the same
runtime archives. Spot timings on a shared 4-core container, eight runs
of each compiled program and 13 of v2's, five of them interleaved, and
three of Python (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.22 to 1.37 s |
| Rust (`rustc -O`) | 2.10 to 2.32 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.02 to 2.53 s |
| Go | 1.54 to 1.98 s |
| Python | 159 to 167 s |
| Kāra (`karac build --mir`) | 1.90 to 2.28 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 2.13 s, against Rust's
2.16 (2.12 under overflow checks), C's 1.25 and Go's 1.73: level with
Rust, and 1.7 times C's time. The loop is one pass over the bytes with
two reads and two writes of a 26-entry table per byte, and every program
mispredicts almost no branch. Under valgrind's cachegrind v2 runs 30.8
billion instructions and 9.0 billion branches, against Rust's 26.9 and
3.8 billion and C's 20.5 and 2.6 billion. C's tables are fixed arrays
and its arithmetic unchecked, where v2 checks each index into its two
tables and each product and sum for overflow; most likely those checks
are the extra branches (not traced). Built for `x86-64-v3`, the target
`karac build` uses, C takes 1.19 to 1.40 s and Rust with overflow checks
2.09 to 2.35 s, against v2's 1.90 to 2.28 s in the same five interleaved
runs. Python takes 165 s, about 130 times C's time. The comparison with
C and Rust waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written. Two spellings in the iterator arm follow
the checker's own suggestions rather than Rust's habits, and neither is
a gap: a `[-1].iter()` yields `ref i64` where the indices are `i64`, so
the literals take `.cloned()`, and `windows(3)` gives a `Vec` of slices,
so its `map` needs `.iter()` first.
