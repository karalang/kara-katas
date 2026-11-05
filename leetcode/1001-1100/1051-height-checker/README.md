# 1051. Height Checker

A school is trying to take an annual photo of all the students. The
students are asked to stand in a single file line in **non-decreasing
order** by height. Let this ordering be represented by the integer array
`expected` where `expected[i]` is the expected height of the `i`th student
in line.

You are given an integer array `heights` representing the **current order**
that the students are standing in. Each `heights[i]` is the height of the
`i`th student in line (**0-indexed**).

Return the **number of indices** where `heights[i] != expected[i]`.

```
heights = [1,1,4,2,1,3]   ->  3
heights = [5,1,2,3,4]     ->  5
heights = [1,2,3,4,5]     ->  0
```

**Constraints:** `1 <= heights.length <= 100`; `1 <= heights[i] <= 100`.

## Approaches

The expected line is the heights sorted, so the answer is the number of
places where the line and its sorted copy differ.

| file | mechanism |
|---|---|
| `height_checker.kara` ★ | a sorted copy, compared place by place. O(n log n) |
| `height_checker_counts.kara` | counting sort over the heights 1 to 100, its walk compared with the line as it goes, with no copy. O(n + H) |
| `height_checker_iter.kara` | the ★ check as `heights.iter().zip(expected.iter()).filter(\|(a, b)\| a != b).count()` |
| `height_checker_heap.kara` | a `PriorityQueue` of the heights handing out the expected line shortest first. O(n log n) |
| `height_checker_insertion.kara` | the expected line built by insertion sort, then the count. O(n^2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for LeetCode's three
examples and seven more (`[2, 1, 2, 1, 2]`, where only the first and fourth
students are out of place, and `[5, 4, 3, 2, 1]`, where the middle one does, among them); the
total and a checksum of the answers for 3000 random lines of 1 to 8
students of 1 to 4 and for 1000 lines of 1 to 100 students of 1 to 100;
and two lines of 100, tallest first (100) and in order with the ends
swapped (2). `height_checker.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, with no sorting: place `i` of the expected line holds height `h`
exactly when fewer than `i + 1` students are shorter than `h` and at least
`i + 1` are no taller, so a student is out of place when their own height
fails that test at their own place. The copy of the counting arm counts
heights up to 201, for the heights P4 doubles. It checks 3000 random
lines: 2000 of 1 to 8 students of 1 to 3, where heights repeat, and 1000
of 1 to 40 students of 1 to 100.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is between 0 and the number of students, and never 1 |
| P3 | the line in order gives 0, and the line reversed gives the number of places where the line differs from its heights tallest first |
| P4 | every height one taller, or twice as tall, changes nothing |
| P5 | a student taller than all added at the back, or one shorter than all at the front, changes nothing |
| P6 | each arm agrees with at least two of the other four |

P2 holds because one student out of place leaves a place they should be
in taken by someone else, who is out of place too. P3's reversed line,
read from the back, is the line against its heights falling. P4 and P5
hold because the expected line depends only on the order of the heights,
and a new tallest at the back or shortest at the front is where it
belongs.

The differential prints `3000 lists: checksum 299438263, 90000 checks over
5 arms: 0 failures` under `karac __mir-run` (5.9 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error, and the same
line under `karac run` and from a `karac build` binary. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three to
each arm. All fifteen are killed, each fails the same way under both
backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: never sorted | P1 2351, P3 2349, P6 2351 |
| M2 | ★: sorted tallest first | P1 1968, P3 2605, P5 2793, P6 1968 |
| M3 | ★: the places that agree counted | P1 2736, P2 974, P3 3000, P5 3000, P6 2736 |
| M4 | counts: one empty height skipped at most | P1 1302, P2 228, P3 1704, P4 1380, P5 3000, P6 1302 |
| M5 | counts: the walk never advances | P1 1837, P2 346, P3 2605, P5 3000, P6 1837 |
| M6 | counts: the student's own height taken off, not the walk's | P1 1972, P2 453, P3 1963, P6 1972 |
| M7 | iter: the copy one place ahead | P1 2071, P2 408, P3 2605, P5 3000, P6 2071 |
| M8 | iter: only students shorter than their place counted | P1 2351, P2 740, P3 2349, P6 2351 |
| M9 | iter: sorted by height mod 50 | P1 667, P3 919, P4 696, P5 2339, P6 667 |
| M10 | heap: the first student left out | P1 1857, P2 471, P3 3000, P5 3000, P6 1857 |
| M11 | heap: at most one counted | P1 2351, P2 2351, P3 2349, P6 2351 |
| M12 | heap: a 0 added | P1 2314, P2 628, P3 3000, P5 3000, P6 2314 |
| M13 | insertion: one step left at most | P1 1314, P3 1326, P6 1314 |
| M14 | insertion: never to the front | P1 1414, P3 1405, P5 1414, P6 1414 |
| M15 | insertion: each student put at the front | P1 1587, P3 2401, P5 2249, P6 1587 |

P1, P3 and P6 kill all fifteen, P5 ten, P2 nine and P4 two. M1 and M13
are seen only by those three: a line left as it is, or half sorted,
still gives a count in range that a taller or longer line does not move,
but a sorted line is not 0 against it, or its reverse is not. P4 sees only
the edits that read the heights' values rather than their order: the
counting walk that skips one empty height (M4), whose gaps double with the
heights, and the sort by height mod 50 (M9). P2 sees a count of 1 (M11),
and the edits that count more places than are out of order. P5 misses the
edits whose error does not change when the line grows at its ends.

Fifteen other edits were set aside. Eight fail exactly as a kept one does:
the iter arm never sorted as M1; the heap counting the places that agree
as M3; and six that read one of the two lines backwards or sort tallest
first as M2 (iter reading the line or the copy backwards, the heap
tallest first or walked from the back, insertion sorting tallest first or
comparing from the back), since each pairs every student with the place
the reversed order gives. Five fail in ways of their own: the ★ arm never
comparing the first or the last place, or comparing each student with the
next place; the counting arm counting only taller students; and insertion
comparing the line one place behind. Two crash: the counting walk starting
at 1, which never takes off the 0 P5 puts in front, and each height
counted once, which runs out of counts; both run the walk past the end,
and both backends stop with the same "index out of bounds".

## Verification

Every arm prints the same output as `height_checker.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file. The runs used a release build of kara `6c8a806480`.
Under `karac __mir-run` the arms take 0.2 s (★) to 0.8 s (heap).

The ★, counting, heap and differential files passed `karac check` as
first written; `karac fix` turned the insertion arm's `&&` into `and`.
The iter arm, written the way Rust writes it, stopped short before kara
`6c8a806480`: `expected.sort_unstable()` was "no method 'sort_unstable'" with
no fix. The library has only the stable sorts, and a stable sort is also a
valid unstable one, so that refusal now says so, `karac fix` drops the
`_unstable`, and the same holds for `sort_unstable_by` and
`sort_unstable_by_key`.

## Benchmarks

The bench builds 2000 lines of 100 students of 1 to 100 once in all five
languages, then runs the ★ arm on every line fifty times, adding up the
answers and folding each into a checksum. Every implementation prints
`2000 lines of 100 students, 50 rounds: total 9800850, checksum
216388696`. With 100 heights for 100 students nearly every student is out
of place, so the count is dominated by the copy and the sort.

Each implementation copies the line into a fresh array, sorts it with its
library's sort and compares. Kāra's `sort` on integers compiles to ipnsort,
the algorithm of Rust's `sort_unstable`, since among equal integers a
stable sort cannot be told from an unstable one, so the Rust mirror calls
`sort_unstable`. Go uses `slices.Sort` (pdqsort), Python `sorted`, and C
`qsort`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `6c8a806480` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.083 to 0.110 s | 0.088 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.085 to 0.101 s | 0.089 s |
| Kāra (`karac build`) | 0.087 to 0.110 s | 0.091 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.089 to 0.102 s | 0.094 s |
| Go | 0.356 to 0.393 s | 0.373 s |
| C (`clang -O3`) | 0.443 to 0.487 s | 0.469 s |
| Python | 0.97 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.087 s) matches its real time.

Kāra took 0.95 times Rust's median time under overflow checks, and 0.19
times C's. Kāra and Rust run the same ipnsort with the comparison inlined;
C's `qsort` calls its comparator through a pointer for every comparison,
and that is most of its time. Go's `slices.Sort` is pdqsort, inlined too,
but four times slower here than ipnsort on 100 small integers.
