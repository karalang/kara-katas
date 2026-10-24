# 960. Delete Columns to Make Sorted III

You are given an array of `n` strings `strs`, all of the same length. We
may choose any deletion indices, and we delete all the characters in
those indices for each string. Suppose we chose a set of deletion
indices `answer` such that after deletions, the final array has **every
string (row) in lexicographic order**, that is
`strs[0][0] <= strs[0][1] <= ... <= strs[0][strs[0].length - 1]`, and so
on for every row. Return *the minimum possible value of*
`answer.length`.

```
strs = ["babca","bbazb"]      ->  3
strs = ["edcba"]              ->  4
strs = ["ghi","def","abc"]    ->  0
```

**Constraints:** `n == strs.length`; `1 <= n <= 100`;
`1 <= strs[i].length <= 100`; `strs[i]` consists of lowercase English
letters.

## Approaches

| file | mechanism |
|---|---|
| `min_deletion_size.kara` ★ | the longest chain of columns: column k may come before a later column j when every string's letter in k is at most its letter in j, and the longest chain ending at j is one more than the longest ending at any earlier column that may come before it. The columns off the longest chain are deleted. O(m^2 n) for n strings of length m |
| `min_deletion_size_matrix.kara` | the strings turned into columns first, then a table of which column may come before which, and the longest chain a longest path through the table. O(m^2 n) time, O(m^2) space |
| `min_deletion_size_memo.kara` | memoised chains from the left: the longest chain starting at column j is j and then the longest starting at any later column it may come before, each column's answer kept in a `Map`. O(m^2 n) time, O(m) stack |
| `min_deletion_size_deletes.kara` | deletions counted directly: with column j the last kept so far, the fewest deletions are the j columns before it, or the deletions up to an earlier kept column k that may come before it and the j - k - 1 between them; the answer adds the columns after the last one kept. O(m^2 n) |
| `min_deletion_size_lists.kara` | each column with the list of later columns it may come before, built in one pass over the pairs; the chains are then measured from the right, each one more than the longest chain starting in its list. O(m^2 n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines: LeetCode's three examples and seven
more (one letter, two letters falling, two strings falling in turn, two
equal strings, three strings that cross, a high first column, and a low
last column); for 300 random cases of 1 to 8 strings of 1 to 10 letters
from a to d, 1,404 strings in all, the total of the columns deleted and
a checksum; and six cases of LeetCode's largest size, 100 strings of
100 letters: random over 26 letters and over a and b, a single random
string, 100 copies of one string, the strings with their letters
sorted, and one string climbing from a to y and back twice.
`min_deletion_size.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of columns tried, and the largest that leaves each
string's kept letters non-decreasing kept. It checks 3,200 random cases:
3,000 of up to 6 strings of up to 8 letters from a to d against the
statement, and 200 of up to 20 strings of up to 30 letters from 2 to 26
letters against the other properties; 12,789 strings in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | the strings in another order give the same answer |
| P3 | each string backwards, each letter turned round the alphabet (a for z, b for y), gives the same answer |
| P4 | a column of a's in front and a column of z's at the end give the same answer |
| P5 | every column twice, side by side, deletes twice as many |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 12789 strings: 10369 columns deleted, checksum
389664059, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(30 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-seven edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: equal letters refused | P1 1388, P4 1331, P5 3200, P6 1421 |
| M2 | ★: each chain starting at no columns | P1 3000, P5 3200, P6 3200 |
| M3 | ★: only the first string checked | P1 1738, P2 1000, P6 1920 |
| M4 | matrix: the columns read backwards | P1 1351, P4 3200, P6 1395 |
| M5 | matrix: the table empty to start | P1 1759, P4 3200, P5 3200, P6 1816 |
| M6 | matrix: the first string skipped | P1 1077, P2 617, P6 1112 |
| M7 | memo: each answer stored under the next column | P1 483, P3 702, P4 303, P5 1143, P6 512 |
| M8 | memo: the next column never followed | P1 893, P4 1659, P5 2776, P6 912 |
| M9 | memo: only the chains from the first column | P1 672, P3 899, P4 714, P6 714 |
| M10 | deletes: no deletions before the first kept column | P1 2451, P6 2642 |
| M11 | deletes: the last string skipped | P1 1048, P2 588, P6 1082 |
| M12 | deletes: the deletions before k forgotten | P1 1323, P3 1235, P4 2113, P5 2113, P6 1377 |
| M13 | lists: any one string enough | P1 2050, P6 2237 |
| M14 | lists: the first column never measured | P1 1046, P3 756, P4 2142, P5 1058, P6 1058 |
| M15 | lists: every successor adding one | P1 1025, P3 900, P4 3200, P5 1816, P6 1057 |

P1 and P6 kill all fifteen, P4 nine (M1, M4, M5, M7 to M9, M12, M14,
M15), P5 eight (M1, M2, M5, M7, M8, M12, M14, M15), P3 five (M7, M9,
M12, M14, M15) and P2 three (M3, M6, M11).

Twenty-two other edits were tried and set aside. Thirteen failed exactly
the same checks as a kept one: matrix, memo, deletes and lists refusing
equal letters, as M1; memo counting a chain of one as none, deletes
counting the tail one too wide and lists starting each chain at none, as
M2; memo asking the order backwards, as M4; deletes counting the gap one
too wide and letting no column come before another, as M5; deletes
starting the answer at 0, as M10; lists never taking the next column as
a successor, as M8; and lists taking the chain from the first column
alone, as M9. Seven were sound but beyond three an arm: ★ taking the
last chain rather than the longest, letting a column come before
itself, and extending the wrong chain; matrix reading its table
transposed; memo making a remembered answer one too long; and deletes
always keeping the last column and never putting the first column
before another.

Two were equivalent. ★ checking every string even after one has
refused the pair: the answer is the same, only found later. And matrix
comparing each column with itself: the table's diagonal is never read,
since a column is only ever compared with earlier ones.

## Verification

Every arm prints the same output as `min_deletion_size.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `cb8ffcccec`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` matrix
takes 0.55 s, ★ 2.7 s, deletes 3.5 s, memo 4.7 s and lists 5.4 s, and
the differential 30 s; most of the difference is reading a letter as
`strs[i].bytes()[k]` in the inner loop, where matrix reads its columns.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 50 cases of 100 strings of 100 letters once,
from the first 2 to 26 letters in turn, each string sorted and then
disturbed by 0 to 9 swaps of neighbouring letters, so that many pairs of
columns are compared down most of the strings. In each of 40 rounds it
runs the ★ arm on every case, each round starting from a different one,
and folds the answers into a checksum. Every implementation prints `40
rounds over 50 cases of 100 strings of 100 letters: 48960 columns
deleted, checksum 762110918`. Each call allocates its chain lengths (a
`Vec` in Kāra and Rust, a slice in Go, a list in Python) except in C,
which keeps them in an array on the stack.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.32 to 0.39 s | 0.34 s |
| Rust (`rustc -O`) | 0.70 to 0.84 s | 0.80 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.70 to 0.88 s | 0.81 s |
| Go | 1.11 to 1.26 s | 1.17 s |
| Python | 44.4 s | |
| Kāra (`karac build --mir`) | 0.91 to 1.07 s | 0.98 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 132 times
C's.

v2 takes 1.21 times Rust's median time under overflow checks and 2.9
times C's. Under valgrind's cachegrind v2 runs 16.04 billion
instructions and 4.98 billion branches with 10.3 million mispredicted,
Rust with overflow checks 12.04 billion, 3.98 billion and 10.5 million,
and C 4.72 billion, 1.53 billion and 15.3 million. Rust and v2 check
each letter's index against its string's length in the inner loop,
which C does not.
