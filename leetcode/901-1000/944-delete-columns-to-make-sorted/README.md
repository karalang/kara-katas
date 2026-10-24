# 944. Delete Columns to Make Sorted

You are given an array of `n` strings `strs`, all of the same length.

The strings can be arranged such that there is one on each line, making
a grid. For example, `strs = ["abc", "bce", "cae"]` can be arranged as:

```
abc
bce
cae
```

You want to **delete** the columns that are **not sorted
lexicographically**. In the above example, columns 0 (`'a'`, `'b'`,
`'c'`) and 2 (`'c'`, `'e'`, `'e'`) are sorted, while column 1 (`'b'`,
`'c'`, `'a'`) is not, so you would delete column 1.

Return *the number of columns that you will delete*.

```
strs = ["cba","daf","ghi"]  ->  1
strs = ["a","b"]            ->  0
strs = ["zyx","wvu","tsr"]  ->  3
```

**Constraints:** `n == strs.length`; `1 <= n <= 100`; `1 <=
strs[i].length <= 1000`; `strs[i]` consists of lowercase English
letters.

## Approaches

| file | mechanism |
|---|---|
| `min_deletion_size.kara` ★ | down each column comparing each row with the next, stopping at the first step down; the columns with one are counted. O(n m) |
| `min_deletion_size_rows.kara` | the grid read a row at a time, as it is stored, each row compared with the one before letter by letter and every column where the letter goes down marked in a `Vec[bool]`; the marked columns are counted. O(n m) time, O(m) space |
| `min_deletion_size_sortcol.kara` | each column copied out of the grid and the copy sorted; the columns the sorting changed are counted. O(m n log n) |
| `min_deletion_size_seen.kara` | down each column counting how many of each letter have been seen, and at each letter looking for any larger one counted already, since a column is sorted when no letter has a larger one anywhere above it. O(26 n m) |
| `min_deletion_size_halves.kara` | the rows from `lo` to `hi` of a column sorted when the top half and the bottom half both are and the last letter of the top half is no larger than the first of the bottom, worked out recursively for each column. O(n m), recursion `log n` deep |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and five
more (one row, one column of equal letters, one column falling, two
columns that each rise and fall, and a grid of `a` and `b` with two of
three columns falling somewhere); for 300 random grids of 1 to 20 rows of 1 to
30 letters from the first 1 to 26 of the alphabet, the rows, the
columns, how many are deleted and a checksum; and four of LeetCode's
largest, 100 rows of 1,000 letters: random letters from all 26, random
`a` and `b`, a grid whose columns are all sorted but where row `r`
holds a `z` at column `10 r`, and a grid whose columns all fall.
`min_deletion_size.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a column is sorted when every letter is no larger than every
letter below it, each pair of rows compared. It checks 3,200 random
grids, each column of random letters sorted with odds from 0 to 4 in 4
chosen for each grid, so that sorted columns are common: 3,000 of up to
5 rows of up to 5 letters from the first 1 to 3 of the alphabet,
against the statement, and 200 of up to 40 rows of up to 150 letters
from the first 1 to 26, against the other properties; 323,020 letters,
and 8,391 columns deleted.

| | property |
|---|---|
| P1 | the statement's count, on the small grids |
| P2 | from 0 to the number of columns, and 0 for a grid of one row |
| P3 | the columns in a random order give the same count, and the grid written beside itself twice the count |
| P4 | the rows in reverse order with the alphabet reversed, `a` for `z`, give the same count |
| P5 | a row of `a`'s put above and a row of `z`'s below give the same count, and so does every row written twice |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 grids of 323020 letters, 8391 deleted, checksum
837781103, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(20 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first two rows never compared | P1 384, P4 395, P5 398, P6 398 |
| M2 | ★: the last two rows never compared | P1 2178, P5 586, P6 2339 |
| M3 | ★: the first column never checked | P1 511, P3 741, P6 602 |
| M4 | rows: the last column never compared | P1 502, P3 746, P6 597 |
| M5 | rows: the unmarked columns counted | P1 2855, P2 586, P6 3054 |
| M6 | rows: a mark taken off by the next step down | P1 230, P6 374 |
| M7 | sortcol: each copy sorted falling | P1 1253, P5 2221, P6 1403 |
| M8 | sortcol: only the last letters compared | P1 310, P4 489, P5 837, P6 443 |
| M9 | sortcol: `z` read as `y` | P4 541 |
| M10 | seen: a letter one larger missed | P1 658, P6 681 |
| M11 | seen: one larger letter above allowed | P1 601, P4 434, P5 650, P6 650 |
| M12 | seen: a `z` above never noticed | P4 676, P6 1 |
| M13 | halves: the bottom half never checked | P1 343, P4 567, P5 606, P6 467 |
| M14 | halves: the seam from the top of each half | P1 98, P4 139, P5 470, P6 112 |
| M15 | halves: two rows taken as sorted | P1 563, P4 194, P5 776, P6 610 |

P6 kills fourteen, P1 thirteen, P4 and P5 eight each, P3 two and P2 one.

P1 misses M9 and M12, which go wrong only on a `z`, and the small grids
use `a` to `c`. P4's reversed alphabet turns their `a`'s into `z`'s, and
it kills M9 alone; M12 also fails P6 once, on a large grid.

M2 stops the walk down one row early, so it never reaches the end of a
column and deletes every column of a grid of two rows or more. That is
the same with the rows reversed and the alphabet too, so P4 misses it;
P5 sees it only on grids of one row, which framing makes three.

P4 misses six more. M3 and M4 skip one column, which reversing the rows
and the alphabet keeps where it was. M5 counts the sorted columns, M6
counts the columns with an odd number of steps down, M7 counts the
columns that do not fall, and M10 misses a step down to the letter just
below; reversing both the rows and the alphabet turns every step down
into a step down between the same two letters reflected, so all four
answer the same.

P5 misses M3 to M6, M9, M10 and M12. A row of `a`'s above and of `z`'s
below adds no step down, and neither does writing a row twice, so a
mistake about which columns or which steps it counts sees nothing new;
and M9 and M12, wrong only about a `z` above another letter, never meet
one in the row of `z`'s, which is below.

P3 kills only M3 and M4, the two that skip one column, which shuffling
the columns moves; every other mistake treats every column alike. P2
kills only M5, which on a grid of one row counts every column, all of
them sorted.

Six other edits were tried and set aside, failing exactly the same
checks as each other in two groups, so none of them was kept: four that
take two equal letters for a step down (★, rows, seen counting an equal
letter above, and halves at the seam); and rows comparing every row
with the first and sortcol comparing only the first letters, which
both delete exactly the columns whose first letter is not the smallest.

## Verification

Every arm prints the same output as `min_deletion_size.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.5 to 2.0 s each and the
differential 20 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The ★, sortcol, seen and halves arms print the same output under the
frozen legacy interpreter, the legacy JIT and both legacy builds, with
and without auto-par. Legacy refuses the rows arm and the differential
at the first `*` on an element of a `Vec`'s `.iter()` ("unary '*'
requires 'ref T', ..."), legacy's older rule, under which the element is
a copy; under v2 it is a reference and the `*` is required. It refuses
the bench program at `min_deletion_size(grids[(r + i) % count])`, a move
out of an index ("cannot move ... out of an index"), which v2's
borrowing parameters make a borrow. Legacy is frozen, so none of this is
filed.

## Benchmarks

The bench program builds 20 grids of 100 rows of 1,000 letters once,
LeetCode's largest, each column of random letters sorted and then, in
half the columns, two random rows swapped, so that a walk down a column
goes some way before it finds a step down or reaches the end; in each of
150 rounds it runs the ★ arm on every grid, each round starting from a
different one, and folds the counts into a checksum. Every
implementation prints `150 rounds over 20 grids of 100 rows of 1000
letters: 1429800 deleted, checksum 47097499`. Kāra copies each row's
bytes into a `Vec[u8]` on every call, as the ★ arm does; the others read
the strings in place. Building the grids sorts 20,000 columns, which C
does with `qsort` and the others with their own sorts.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.20 to 0.30 s | 0.23 s |
| Rust (`rustc -O`) | 0.24 to 0.28 s | 0.25 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.21 to 0.26 s | 0.23 s |
| Go | 0.46 to 0.49 s | 0.48 s |
| Python | 14.3 s | |
| Kāra (`karac build --mir`) | 0.25 to 0.30 s | 0.26 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 64 times C's.

v2 takes 1.15 times Rust's median time under overflow checks and 1.16
times C's. Under valgrind's cachegrind v2 runs 3.26 billion
instructions and 1.07 billion branches with 4.8 million mispredicted,
Rust with overflow checks 3.10 billion, 0.84 billion and 5.1 million,
and C 1.72 billion, 0.41 billion and 14.0 million. C's 24 million
indirect branches, against under a million in the others, are `qsort`
calling its comparison function, and its extra mispredictions are
likely in the same sort; that C's fewer instructions in the walk itself
are the bounds checks it does not make, and v2's extra branches over
Rust its copy of every row on each call, is inferred, not profiled.
