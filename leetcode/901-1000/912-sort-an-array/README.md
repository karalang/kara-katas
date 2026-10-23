# 912. Sort an Array

Given an array of integers `nums`, sort the array in ascending order and
return it.

You must solve the problem **without using any built-in** functions in
`O(nlog(n))` time complexity and with the smallest space complexity
possible.

```
nums = [5,2,3,1]       ->  [1,2,3,5]
nums = [5,1,1,2,0,0]   ->  [0,0,1,1,2,5]
```

**Constraints:** `1 <= nums.length <= 5 * 10^4` and
`-5 * 10^4 <= nums[i] <= 5 * 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `sort_array.kara` ★ | heap sort: a max-heap built in place from the last parent down, then the root, the largest value left, swapped to the end of the shrinking heap and the new root sifted down. O(n log n) time and O(1) space beyond the array, the least the statement asks for |
| `sort_array_merge.kara` | bottom-up merge sort: runs of width 1, 2, 4, ... merged from the array into a buffer and back, the left head taken on a tie. O(n log n) time, O(n) space |
| `sort_array_quick.kara` | quicksort with a three-way partition around the median of the first, middle and last values, so equal values cost nothing more; the smaller side by recursion and the larger by looping, keeping the stack O(log n) deep. O(n log n) expected |
| `sort_array_counting.kara` | counting sort over the values' own range: a counter for each value from the smallest to the largest, then each value written as many times as counted. O(n + range) time and space, the range at most 10^5 + 1 |
| `sort_array_radix.kara` | radix sort base 256: every value shifted up by 5 * 10^4, then sorted stably by its lowest byte, its next and so on while any value has a byte left, and shifted back. O(n) a pass, three passes |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and seven
more (`[1]`, the two extremes, small negatives, a rising and a falling
run, five equal values, and values around the byte boundaries 255, 256
and 65,535 once shifted); for 300 random arrays of up to 2,000 numbers
in ranges of 10, 1,000 or the whole span, a checksum of the sorted
values; and three of LeetCode's largest, 50,000 numbers random, falling
and nearly all equal. `sort_array.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: ascending order defined place by place, place `i` holding the
value with fewer than `i + 1` values below it and at least `i + 1` at or
below it. It checks 3,200 random arrays: 3,000 of up to 10 numbers in
ranges of 3, 100 or 10,000 against the statement, and 200 of up to 500
numbers in ranges of 3, 100 or the whole span against the other
properties, each range placed anywhere from -5 * 10^4 to 5 * 10^4;
65,797 numbers in all.

| | property |
|---|---|
| P1 | the statement's ascending order, on the small arrays |
| P2 | as long as the input, and never falling |
| P3 | the same values: the same count, sum, sum of squares and sum of cubes (modulo 10^9 + 7) |
| P4 | the same answer for the input reversed |
| P5 | the input negated sorts to the answer negated and reversed |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every array. It prints `3200 arrays, 65797
numbers, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the smaller child sifted up | P1 2238, P2 2438, P4 2266, P5 2523, P6 2438 |
| M2 | ★: the last parent never sifted when building | P1 793, P2 810, P4 1407, P5 1422, P6 810 |
| M3 | ★: the last two values never swapped | P1 2078, P2 2164, P5 2093, P6 2164 |
| M4 | merge: the larger head taken first | P1 2655, P2 2855, P6 2855 |
| M5 | merge: runs tripled, not doubled | P1 2188, P2 2388, P4 2504, P5 2566, P6 2388 |
| M6 | merge: each left run cut one short | P1 2100, P2 2300, P4 2669, P5 2811, P6 2300 |
| M7 | quick: the smaller side's last value left unsorted | P1 215, P2 346, P4 423, P5 554, P6 346 |
| M8 | quick: a value skipped after the smaller side | P1 622, P2 762, P4 1044, P5 1243, P6 762 |
| M9 | quick: a value swapped in from the right never examined | P1 1449, P2 1641, P4 1896, P5 1920, P6 1641 |
| M10 | counting: repeats counted once | P1 962, P2 1133, P3 1133, P6 1133 |
| M11 | counting: the largest value left out | P1 3000, P2 3200, P3 3200, P5 2855, P6 3200 |
| M12 | counting: at most two copies of a value written | P1 591, P2 720, P3 720, P6 720 |
| M13 | radix: the top byte never sorted | P1 1079, P2 1169, P4 139, P5 1167, P6 1169 |
| M14 | radix: each pass scattering from the end, not stable | P1 2063, P2 2262, P5 2796, P6 2262 |
| M15 | radix: negative values not shifted up | P1 2406, P2 2606, P4 2808, P5 2606, P6 2606 |

P1, P2 and P6 kill all fifteen; P5 kills twelve, P4 nine and P3 three.
Every mutant except the counting arm's only moves values around, so it
keeps the values themselves and P3 cannot see it; the three counting
mutants lose or drop copies, which P3 sees and P2 sees too, through the
length. Dropping repeats (M10, M12) is the same for a value and its
negation, so P5 misses those two.

The first run of the counting mutants M10 to M12 stopped with an index
out of bounds in the differential itself: P5 walked the negated answer
up to the input's length, so an answer of another length ran off its
end. P5 now walks the answer's own length, and every mutant was run
again on the corrected differential; the counts above are from that
run.

One mutant was replaced. The first M4 capped each merge's right end at
`n - 1`, which hung: once the left end reached `n - 1` the right end
equalled it, and the pass never advanced.

## Verification

Every arm prints the same output as `sort_array.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 1.6 to 3.8 s
each (the quicksort the longest) and the differential 9.7 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every arm and the differential also print the same output under the
frozen legacy interpreter, the legacy JIT and both legacy builds, with
and without auto-par. The legacy builds warn that `nums` is moved into
one call and used again, under legacy's older rule that a bare
parameter takes ownership; the programs run correctly all the same.
Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on 500,000 numbers from -5 * 10^4 to
5 * 10^4, built once. Each round heap-sorts a copy, folds every 997th
sorted value into a checksum and changes one number; 6 rounds. Every
implementation prints `6 rounds over 500000 numbers: checksum
306730727`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.39 to 0.46 s | 0.41 s |
| Rust (`rustc -O`) | 0.40 to 0.46 s | 0.42 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.39 to 0.44 s | 0.43 s |
| Go | 0.46 to 0.56 s | 0.49 s |
| Python | 14.5 s | |
| Kāra (`karac build --mir`) | 0.48 to 0.54 s | 0.52 s |
| Kāra (legacy `karac build`) | 0.41 to 0.47 s | 0.45 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does.

v2 takes 1.22 times Rust's median time under overflow checks, 1.28 times
C's and 1.15 times legacy's. Under valgrind's cachegrind v2 runs 2.15
billion instructions and 542 million branches, about twice legacy's
1.09 billion and 265 million, against 0.96 billion and 213 million for
C and 1.07 billion and 269 million for Rust with overflow checks. All
four mispredict about 30 million branches, the sift's choice between
two children, and the time stays much closer than the instruction
counts, which fits a sort waiting on those mispredictions and on memory
more than on instructions. Where v2's extra instructions go was not
profiled.
