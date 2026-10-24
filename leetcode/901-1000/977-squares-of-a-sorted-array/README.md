# 977. Squares of a Sorted Array

Given an integer array `nums` sorted in non-decreasing order, return an
array of the squares of each number sorted in non-decreasing order.

```
nums = [-4,-1,0,3,10]  ->  [0,1,9,16,100]
nums = [-7,-3,2,3,11]  ->  [4,9,9,49,121]
```

**Constraints:** `1 <= nums.length <= 10^4`; `-10^4 <= nums[i] <= 10^4`;
`nums` is sorted in non-decreasing order.

## Approaches

| file | mechanism |
|---|---|
| `sorted_squares.kara` ★ | two pointers from the ends: the largest square belongs to whichever end has the larger absolute value, so two indices start at the ends and the result is filled from the back, each step taking the larger square and moving that index inward. O(n) |
| `sorted_squares_sort.kara` | square, then sort: the order of the input is ignored, every number squared and the squares sorted. O(n log n) |
| `sorted_squares_merge.kara` | merge from the middle: a binary search finds the first number that is not negative; the squares of the negatives read leftwards from there are sorted, and so are those of the rest read rightwards, so the two runs are merged outwards, smallest first. O(n) |
| `sorted_squares_counting.kara` | counting by absolute value: a table up to the largest absolute value counts each one, and the squares are written out walking the table upwards, each as many times as counted. O(n + 10^4) |
| `sorted_squares_heap.kara` | a heap of squares: every square goes into a smallest-first `PriorityQueue`, which is then emptied into the result. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines. The first ten are LeetCode's two
examples and eight more, each printed with its squares: a lone zero; a
lone negative; all negatives; all positives; equal values on both
sides of zero; LeetCode's extremes, -10^4 and 10^4, beside -1 and 1;
-2 to 2; and [-10, 1, 2, 3, 4], whose largest square comes from the
left end. The last three are totals and checksums of every square over
random sorted arrays: 300 of up to 12 numbers in [-5, 5], 3,000 of up
to 60 in [-1,000, 1,000], and 4 of 10^4 over LeetCode's whole range.
`sorted_squares.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each number squared and inserted after every square already
placed that is no larger. It checks 3,200 arrays: 3,000 of 1 to 30
numbers in [-2, 2], [-5, 5], [-100, 100] or [-10^4, 10^4], so that
many repeat and zero falls anywhere, every fifth of them moved 3 up or
down, against the statement, and 200 of 300 numbers over LeetCode's
whole range against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 arrays |
| P2 | every number negated and the order reversed, which keeps the array sorted, gives the same squares |
| P3 | as many squares as numbers, in non-decreasing order, summing to the sum of the squares, from the smallest absolute value's square to the largest's |
| P4 | a number at least as large in absolute value as every other, put at the end or, negated, at the front, adds its square at the end |
| P5 | a number of smallest absolute value taken out takes out the first square, when another number is left |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays of 107327 numbers: squares total 2206256924071,
checksum 2555058, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (16.2 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last number left never placed | P1 1907, P3 2101, P5 2369, P6 2101 |
| M2 | ★: the wrong index moved after taking the left end | P1 2664, P2 2234, P3 2864, P4 1566, P6 2864 |
| M3 | ★: the right square taken with the left number | P1 2740, P2 3078, P3 2940, P4 1625, P5 2090, P6 2940 |
| M4 | sort: the sign kept | P1 2751, P2 3178, P3 2951, P4 1575, P5 2864, P6 2951 |
| M5 | sort: never sorted | P1 2664, P2 3068, P3 2864, P4 1575, P5 2864, P6 2864 |
| M6 | sort: sorted largest first | P1 2891, P3 3091, P4 3200, P5 3091, P6 3091 |
| M7 | merge: the sign ignored in the comparison | P1 2578, P2 2855, P3 2778, P4 1523, P5 1890, P6 2778 |
| M8 | merge: the negative nearest zero skipped | P1 2751, P2 2240, P3 2951, P4 141, P5 477, P6 2951 |
| M9 | merge: stopped when one side runs out | P1 3000, P2 1017, P3 3200, P4 3194, P5 27, P6 3200 |
| M10 | counting: each absolute value once | P1 1840, P3 2039, P4 30, P5 1064, P6 2039 |
| M11 | counting: the largest absolute value never written | P1 3000, P3 3200, P4 3200, P6 3200 |
| M12 | counting: zeros never written | P1 1093, P3 1099, P5 1092, P6 1099 |
| M13 | heap: the numbers, not their squares | P1 2977, P2 3178, P3 3177, P4 3200, P5 2864, P6 3177 |
| M14 | heap: the last square left in the heap | P1 3000, P3 3200, P4 3170, P6 3200 |
| M15 | heap: every second square thrown away | P1 2900, P3 3100, P4 1519, P5 2989, P6 3100 |

P1, P3 and P6 kill all fifteen, P4 thirteen (all but M1 and M12), P5
twelve (all but M2, M11 and M14) and P2 eight (M2, M3, M4, M5, M7, M8,
M9, M13). P2 sees only edits that treat the two signs differently; an
edit that loses or repeats squares, or orders them backwards, does the
same to the mirrored array. The answer is fixed by its input as a
multiset, so nearly every wrong edit is wrong on most arrays, and P3's
sum and end points alone catch all fifteen.

Ten other edits were tried and set aside. Two failed exactly the same
checks as a kept one: the heap popping largest first, as M6, and the
heap keeping the sign, as M4. Seven were sound but beyond three an arm:
★ placing the smaller square at the back and never reading the last
number; sort taking absolute values for squares and dropping repeated
squares; merge taking the larger square first; counting one copy too
few of each value and each number twice. One is equivalent: the
binary search in merge splitting before the first number of at least 1
instead of at least 0 puts the zeros with the negatives, whose run read
leftwards starts 0, 1, 4 and is still sorted.

## Verification

Every arm prints the same output as `sorted_squares.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.36 s (★) to 2.3 s (heap), and the differential 16.2 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program makes 20
sorted arrays of 10,000 random numbers in [-10^4, 10^4] once. In each
of 500 rounds it runs the arm on every array, each round starting from
a different one, and folds the first and last squares into a total and
one square, at a place that moves with the round, into a checksum.
Every implementation prints `500 rounds over 20 arrays of 10000
numbers: squares total 999920018000, checksum 446991547`. Kāra, Rust,
Go and Python allocate a fresh result on each call; C writes into one
static buffer, as kata 976's bench does for its copy.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.464 to 0.530 s | 0.494 s |
| Rust (`rustc -O`) | 0.518 to 0.643 s | 0.550 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.549 to 0.683 s | 0.618 s |
| Go | 0.689 to 0.804 s | 0.718 s |
| Python | 15.4 s | |
| Kāra (`karac build --mir`) | 0.670 to 0.718 s | 0.675 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 23 times
Kāra's.

v2 took 1.09 times Rust's median time under overflow checks and 1.37
times C's. Under valgrind's cachegrind v2 ran 3,735 million
instructions and 1,703 million branches with 44.0 million
mispredicted, Rust with overflow checks 2,904 million, 1,605 million
and 43.9 million, and C 1,678 million, 116 million and 1.5 million.
C's 116 million branches are about one for each of the 100 million
elements written, the loop's own test, which suggests clang turned the
choice between the two squares into conditional moves (the assembly was
not read); C also has no bounds checks, which v2 and Rust keep. v2
and Rust mispredict the same 44 million times, and v2 runs 29% more
instructions than Rust for 6% more branches; where the extra
instructions go was not measured.
