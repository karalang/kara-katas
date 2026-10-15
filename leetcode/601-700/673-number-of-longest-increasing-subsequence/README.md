# 673. Number of Longest Increasing Subsequence

Given an array of integers `nums`, return how many longest strictly
increasing subsequences it has.

```
[1, 3, 5, 4, 7]  ->  2   ([1, 3, 4, 7], [1, 3, 5, 7])
[2, 2, 2, 2, 2]  ->  5   (each [2] is one)
```

**Constraints:** 1 <= `nums.length` <= 2,000; -10^6 <= `nums[i]` <=
10^6; the answer fits in a 32-bit integer.

## Approaches

Every arm is `fn find_number_of_lis(nums: Vec[i64]) -> i64`. Each one
tracks, for a place or a value, a pair: the longest length reached and
how many subsequences reach it. Pairs combine by keeping the longer
length, and adding the counts when the lengths tie.

| file | mechanism |
|---|---|
| `number_of_longest_increasing_subsequence.kara` ★ | the pair for subsequences ending at each place, from every earlier, smaller place; O(n^2) |
| `number_of_longest_increasing_subsequence_fenwick.kara` | the values ranked, and a Fenwick tree over the ranks holding the best pair for each prefix; O(n log n) |
| `number_of_longest_increasing_subsequence_piles.kara` | patience piles, each pile keeping running counts, so a binary search and a subtraction sum the numbers a new one extends; O(n log n) |
| `number_of_longest_increasing_subsequence_memo.kara` | the pair for subsequences starting at each place, by memoized recursion returning a tuple; O(n^2) |
| `differential.kara` | the four arms against every subset of small arrays, five properties |

Every arm prints the same 18 lines: the two LeetCode examples and twelve
corners, among them one number, rising and falling runs, pairs of
repeats, pairs swapped (ten numbers, 32 subsequences, and sixty,
2^30), and 2,000 numbers rising and falling, the problem's longest; a
checksum of 300 random arrays of up to 200 numbers, spread over 5, 50 or
the whole range, with the largest answer among them; and three random
arrays of 1,000 numbers. `number_of_longest_increasing_subsequence.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every subset of the places as a bit mask and counts the
strictly increasing ones of the greatest length. That is affordable up
to 12 numbers, and 70 arrays that small are checked against it. A
further 1,000 random arrays of up to 60 numbers, spread over 3, 10 or
1,000 values so that repeats range from common to rare, are held to the
other four properties.

| | property |
|---|---|
| P1 | the answer is the definition's (small arrays only) |
| P2 | the array reversed and negated has the same answer |
| P3 | the array with every number moved by a constant has the same answer |
| P4 | the array with a new largest number appended has the same answer |
| P5 | the array followed by a copy moved above all of it has the answer squared |

It prints `1070 arrays (70 against the definition), 4 arms,
17400 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal earlier number extended too | P1 33 |
| M2 | ★: a longer length restarts its count at 1 | P1 15, P2 681, P4 385, P5 755 |
| M3 | ★: only the last longest place counted | P1 33, P2 745, P4 656, P5 656 |
| M4 | fenwick: a value ranked above its equals | P1 41, P2 750, P4 650, P5 650 |
| M5 | fenwick: every rank above updated, not the tree's | P1 34, P2 619, P5 583 |
| M6 | piles: an equal number dealt to the next pile | P1 27 |
| M7 | piles: the whole previous pile extended | P1 39, P2 952 |
| M8 | memo: the next place skipped | P1 56, P4 473, P5 241 |
| E1 | ★: places at least the longest length counted | 0 |
| E2 | fenwick: repeated values kept in the ranking | 0 |
| E3 | fenwick: tested by the count below, not the length | 0 |
| E4 | memo: the place itself among those after it | 0 |

P1 kills all eight. Two of them it kills alone: M1 and M6 count
non-decreasing subsequences rather than strictly increasing ones, and
every other property holds for those too, since reversing and negating,
moving, appending a new largest number and appending a copy above all
keep a non-decreasing subsequence non-decreasing. The other six break
the way pairs combine, and P2, P4 or P5 see most of them on hundreds of
arrays. P3 sees none: every arm compares numbers only with each other,
so moving them all changes nothing a mutant could get wrong. The four
survivors cannot change an answer: no place is longer than the longest;
a repeated value's extra ranks are never looked up, since the binary
search finds its first copy; a pair's count is above 0 exactly when its
length is; and a place is never larger than itself.

## Verification

Every arm prints the same output as
`number_of_longest_increasing_subsequence.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak. The differential prints its line
under all three. `karac check` passes all four arms, the differential
and the bench program. All with the compiler at kara `8d40e1a762` for
the debug build and `85dccd703c` for the release build that runs `check`
and `__mir-run`, with runtime archives newer than the last `runtime/src`
change.

The frozen legacy backends print the same output for the ★ arm and the
piles arm under the interpreter, the JIT and `karac build`, with and
without `KARAC_AUTO_PAR=1`; `karac build` warns that `nums` is moved
into `show` and used again, and builds anyway. The memo arm is the same
under the JIT and `karac build`, but the legacy interpreter has printed
only 12 of its 18 lines when the 60 s limit stops it. The Fenwick arm is
right under the legacy interpreter and wrong under the legacy JIT and
`karac build`, which print 1 for every array. The legacy `karac build`
of the differential reports 46 failures of P1, and the legacy
interpreter does not finish it within 60 s. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It counts the longest increasing
subsequences of 150 arrays of 2,000 numbers, the problem's longest, each
number below 32,768 from the same generator in every language, and puts
each answer into a checksum. Every implementation prints `150 arrays of
2000: checksum 638652218`, the Kāra program under `karac __mir-run`
included (in 97 s).

Each implementation is the same double loop, with two arrays allocated
for each input, so this measures the inner loop's comparisons and
branches. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.81 to 0.86 s |
| Rust (`rustc -O`) | 0.82 to 0.85 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.86 to 1.01 s |
| Go | 0.93 to 0.99 s |
| Python | 17.0 to 17.3 s |
| Kāra (`karac build --mir`) | 1.27 to 1.31 s |
| Kāra, legacy (`karac build`) | 0.93 to 0.95 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 3.4 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is about 1.4 times legacy, inside the M2 bar of 1.5, and
about 1.5 times C and Rust on this one inner loop of comparisons and
branches; Go is level with legacy. It has not been profiled. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
