# 1035. Uncrossed Lines

You are given two integer arrays `nums1` and `nums2`. We write the
integers of `nums1` and `nums2` (in the order they are given) on two
separate horizontal lines.

We may draw connecting lines: a straight line connecting two numbers
`nums1[i]` and `nums2[j]` such that `nums1[i] == nums2[j]`, and the
line we draw does not intersect any other connecting (non-horizontal)
line. Note that a connecting line cannot intersect even at the
endpoints (i.e., each number can only belong to one connecting line).

Return the maximum number of connecting lines we can draw in this way.

```
nums1 = [1,4,2],          nums2 = [1,2,4]          ->  2
nums1 = [2,5,1,2,5],      nums2 = [10,5,2,1,5,2]   ->  3
nums1 = [1,3,7,1,7,5],    nums2 = [1,9,2,5,1]      ->  2
```

**Constraints:** `1 <= nums1.length, nums2.length <= 500`;
`1 <= nums1[i], nums2[j] <= 2000`.

## Approaches

| file | mechanism |
|---|---|
| `uncrossed_lines.kara` ★ | a table over both prefixes: lines that do not cross join equal values in the same order in both lists, so the most lines is the longest common subsequence. `best[i][j]` covers the first `i` values of `nums1` and the first `j` of `nums2`: one more than `best[i - 1][j - 1]` when those last values are equal, otherwise the better of dropping either. O(m n) |
| `uncrossed_lines_row.kara` | one row and a diagonal: the same recurrence in one row over `nums2`, with `diagonal` carrying the row above's value at `j - 1` from one step to the next. O(m n) time, O(n) space |
| `uncrossed_lines_memo.kara` | recursion over the suffixes: `lines(i, j)` is 0 when either list is used up, one more than `lines(i + 1, j + 1)` when the first values are equal, otherwise the better of skipping either, kept in a table of -1 for unknown. O(m n) |
| `uncrossed_lines_lis.kara` | matches as an increasing subsequence (Hunt and Szymanski): walk `nums1`, and for each value its places in `nums2` from the last down, so one value joins at most one place; the longest strictly increasing chain of places, kept as patience piles with a binary search, is the answer. O((m + r) log n) for `r` equal pairs |
| `uncrossed_lines_bits.kara` | a bit-parallel row (Allison and Dix, as Crochemore et al. write it): one bit per place of `nums2` in `u64` words, a mask per value, every bit set at the start; for each `x` of `nums1` with mask `M`, `V` becomes `(V + (V & M)) \| (V & ~M)`, the addition carried word to word with `wrapping_add`. The answer is the number of clear bits. O(m n / 64) |
| `differential.kara` | the five arms against the statement read literally, seven properties |

Every arm prints the same 19 lines: the answers for eight pairs,
LeetCode's three examples among them; for seven groups of random pairs
(300 of up to 8 values from 1 to 3 down to 6 of up to 500 from 1 to
2,000), the sum of the answers and a checksum; and four answers on 500
values each. `uncrossed_lines.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a set of lines joins some values of `nums1` to some of
`nums2`, each value in at most one line, and lines do not cross exactly
when the k-th chosen value of `nums1` is joined to the k-th chosen of
`nums2`. So it tries every choice of values from each list, joined in
that order, and keeps the largest whose lines all join equal values.
It checks 862 cases: every pair of lists of 1 to 3 values from 1 and 2
(196), then 600 random pairs of 1 to 6 values up to 2, 3 or 6, 60 of up
to 100 values up to 3, 50 or 2,000, and 6 of up to 500. The 796 pairs of
at most 6 values each are searched in full. Each case is also asked
with the lists the other way round, with both reversed, with every
value `v` renamed `2001 - v`, and with one random value added at the end
of both.

| | property |
|---|---|
| P1 | the statement read literally, on lists of at most 6 values |
| P2 | which list is first does not matter |
| P3 | reversing both lists does not change the answer |
| P4 | renaming the values one-to-one does not change the answer |
| P5 | the answer is at most the shorter list's length, and 0 exactly when the lists share no value |
| P6 | an equal value added at the end of both adds one line |
| P7 | each arm agrees with at least two of the other four |

The differential prints `862 cases (796 searched in full): checksum
382253775, 29840 checks over 5 arms: 0 failures` under `karac
__mir-run` (15 s), `karac __mir-llvm-run` and `karac __mir-llvm-asan`
with no error.

## Mutation testing

Thirty-one edits to the differential, each run under `karac __mir-run`
and `karac __mir-llvm-run`. Fifteen are kept, three to each arm. All
fifteen are killed, each fails the same checks under both backends,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: never drops a value of `nums2` | P1 275, P2 422, P3 322, P5 168, P7 328 |
| M2 | ★: the last value of `nums2` never matched | P1 688, P5 743, P6 862, P7 743 |
| M3 | ★: a match where `i == j` ignored | P1 153, P3 204, P5 49, P6 175, P7 159 |
| M4 | row: the diagonal starts at one | P1 413, P2 377, P3 278, P5 207, P7 425 |
| M5 | row: the first value of `nums2` never matched | P1 292, P2 383, P3 239, P5 132, P7 300 |
| M6 | row: the answer read one place short | P1 311, P2 384, P3 239, P5 129, P6 541, P7 321 |
| M7 | memo: a known answer read as at most 1 | P1 14, P2 47, P3 47, P6 63, P7 52 |
| M8 | memo: never skips a value of `nums2` | P1 296, P2 412, P3 322, P5 177, P6 692, P7 349 |
| M9 | memo: the last value of `nums1` never matched | P1 321, P2 384, P3 250, P5 147, P6 527, P7 333 |
| M10 | lis: the last pile never searched | P1 342, P6 743, P7 387 |
| M11 | lis: a pile top never lowered | P1 243, P2 165, P3 165, P6 1, P7 284 |
| M12 | lis: only the first place of each value kept | P1 211, P2 86, P3 73, P6 3, P7 243 |
| M13 | bits: the carry dropped between words | P2 27, P3 14, P5 8, P6 1, P7 20 |
| M14 | bits: places packed 63 to a word | P2 14, P3 11, P6 29, P7 10 |
| M15 | bits: the carry out of adding the carry lost | P2 1 |

P7 kills fourteen, P1, P2 and P3 twelve each, P6 eleven, P5 nine, and
P4 none. Every arm compares values only for equality, and the bits
arm's masks are keyed by value, so a one-to-one renaming changes
nothing an edit here touches (read from the code). P1 misses the three
bits edits: they go wrong only where `nums2` runs past one 64-bit word,
and no list it searches has more than 6 values. M15 is the weakest kept
edit. Adding the carry carries out only when a word is all ones before
it, and of the 4,310 checks P2 makes, one case does that: the bits arm
asked with the lists the other way round. The checks draw random
numbers for every case whatever the answers, so every mutant sees the
same cases and their counts can be compared.

Sixteen other edits were tried and set aside. Two change no answer and
are equivalent: ★ adding and taking away the cell above in a match,
and the bits arm counting its last word in full (the bits past the end
of `nums2` are set at the start and never cleared). One never ends:
memo searching a known 0 again is exponential, and both backends ran
past 120 s. The other thirteen were killed too, beyond three per arm.
Three fail exactly as M2 or M1 do: memo knowing every answer as 0 and
the bits arm never clearing the matched bits as M2, and the row arm
never dropping a value of `nums2` as M1. Four fail alike each other
(`P1 251, P2 447, P5 104, P6 2, P7 282`): ★ and the row arm adding a
match to the row above, memo using a matched value of `nums2` again,
and lis allowing a non-decreasing chain. Two pairs fail alike: the row
arm's diagonal carrying the new value and lis taking places from the
first up, and ★ and lis capping the answer below `nums1`'s length. Two
fail on their own: memo also storing each answer at the swapped place,
and the bits arm adding the whole mask.

## Verification

Every arm prints the same output as `uncrossed_lines.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. The differential prints its line under all three. `karac run` and
a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reported one thing: the lis
arm's `None => places.insert(nums2[j], vec![j]),` beside `Some(list) =>
list.push(j),` is E0212 "match arms have incompatible types: '()' and
'Option[Vec[i64]]'", since `insert` returns the value it replaced. It
came with no edit, and I wrote the arm as a block. Rust refuses the
same line the same way. Every file then checks clean. The release build
is kara `6697158faf`, with runtime archives rebuilt at that commit.
Under `karac __mir-run` the arms take 0.39 s (bits) to 5.3 s (memo). No
gap turned up.

## Benchmarks

The bench builds 40 random pairs of 500 values from 1 to 10 (LeetCode's
largest lists) once in all five languages, then answers every pair 20
times with the ★ arm, folding the answers into a sum and a checksum.
Every call allocates its table: 501 rows of `Vec`s in Kāra and Rust, of
slices in Go, of lists in Python, and one `calloc`'d block in C. Every
implementation prints `40 pairs of 500 values, 20 rounds: sum 184980,
checksum 344923516`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.275 to 0.314 s | 0.294 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.623 to 0.695 s | 0.634 s |
| Kāra (`karac build`) | 0.624 to 0.732 s | 0.677 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.840 to 0.895 s | 0.850 s |
| Rust (`rustc -O`) | 0.840 to 0.902 s | 0.862 s |
| Go | 0.941 to 1.102 s | 1.053 s |
| Python | 24.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(0.64 s real, 0.64 s user) and runs about as fast as the sequential
one.

Kāra took 0.75 times Rust's median time under overflow checks and 2.16
times C's. C indexes one block with no bounds checks, where Kāra and
Rust index a row and then a column and check both (inferred from the
sources, not profiled).
