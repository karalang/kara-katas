# 1755. Closest Subsequence Sum

You are given an integer array `nums` and an integer `goal`.

You want to choose a subsequence of `nums` such that the sum of its
elements is the closest possible to `goal`. That is, if the sum of the
subsequence's elements is `sum`, then you want to **minimize the
absolute difference** `abs(sum - goal)`.

Return *the **minimum** possible value of* `abs(sum - goal)`.

Note that a subsequence of an array is an array formed by removing some
elements **(possibly all or none)** of the original array.

```
nums = [5, -7, 3, 5], goal = 6      ->  0    the whole array
nums = [7, -9, 15, -2], goal = -5   ->  1    [7, -9, -2] sums to -4
nums = [1, 2, 3], goal = -7         ->  7    the empty subsequence
```

**Constraints:** `1 <= nums.length <= 40`; `-10^7 <= nums[i] <= 10^7`;
`-10^9 <= goal <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `closest.kara` ★ | meet in the middle with binary search: every subset sum of each half of at most 20 values is listed, each a sum without its lowest member plus that member, read off with `trailing_zeros`; the right half's are sorted, and for each left sum `partition_point` finds the right sums at and below the rest of the goal. O(2^(n/2) n) |
| `closest_pointers.kara` | each half's subset sums from a recursion that leaves out or takes each value, both lists sorted; one pointer walks the left sums up and the other the right sums down, a pair below the goal moving the first and one above moving the second. O(2^(n/2) n) |
| `closest_set.kara` | each half's subset sums built by doubling a list; the right half's go into a `SortedSet`, and `range_inclusive` above and `range` below the rest of the goal give the nearest right sums. O(2^(n/2) n) |
| `closest_solution.kara` | a Rust solution as LeetCode's Rust users write it, a nested `fn sums` doubling a list for each half, the right sorted with `sort_unstable` and searched with `partition_point`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, then one
value, the empty subsequence's 0 as the closest, and the farthest goal;
then the sum of the answers and a checksum for 3000 random problems of
up to 6 values within 5, 300 of up to 20 values within 10^7, and 10 of
up to 40 values, LeetCode's limits. `closest.py` mirrors the ★ arm and
its output is byte-identical.

```
0
1
7
5
20
990000000
3000 problems of up to 6 values within 5: differences add to 19896, checksum 281193621
300 problems of up to 20 values within 10000000: differences add to 8396390019, checksum 233573882
10 problems of up to 40 values within 10000000: differences add to 4985697008, checksum 308858985
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every subsequence, as a bit mask, the empty one included,
summed in `i64`, and the smallest distance from the goal. It checks 3000
random problems of 1 to 10 values from -10 to 10 and a goal from -40 to
40, each with a random value to append. Every case is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values reversed give the same answer |
| P3 | the values and the goal negated give the same answer |
| P4 | one more value never raises the answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 224952709, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, every mask summed, gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M4, the pointers arm moving
the left pointer on an exact hit as well, is equivalent, since an exact
hit has already made the answer 0, and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each sum built from the member at the mask's bit count, not its lowest | P1 1372, P2 1598, P4 283, P5 1372 |
| M2 | ★: only the right sums at or above the rest tried | P1 1032, P3 2092, P5 1032 |
| M3 | ★: the sum of the whole half never listed | P1 733, P2 245, P5 733 |
| M4 | pointers: a pair below the goal moves the right pointer down | P1 1431, P2 1471, P3 2569, P4 546, P5 1431 |
| M5 | pointers: every sum that takes the value dropped again | P1 2574, P5 2574 |
| M6 | pointers: the left sums not sorted | P1 892, P2 1195, P3 1677, P4 223, P5 892 |
| M7 | set: the doubled list keeps only the sums with the new value | P1 2692, P4 1467, P5 2692 |
| M8 | set: the smallest right sum below the rest taken, not the largest | P1 967, P2 783, P3 1972, P4 328, P5 967 |
| M9 | solution: the largest right sum never taken as the one at or above | P1 83, P2 82, P3 182, P4 6, P5 83 |
| M10 | solution: the right half split one value early, its first value counted twice | P1 372, P2 564, P4 259, P5 372 |

## Benchmarks

The bench draws 8 random problems of 40 values within 10^7, LeetCode's
limits, and goals within 10^8, all of them first, then answers each once
by the ★ arm in all five languages: two lists of 2^20 subset sums, one
sorted, and 2^20 binary searches each. C sorts with `qsort` and Go with
`slices.Sort`. Every implementation prints `8 problems of 40 values:
differences add to 7224012, checksum 262794676`. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| Kāra (`karac build`) | 0.598 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.602 s |
| Rust (`rustc -O`) | 0.627 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.660 s |
| Go | 1.322 s |
| C (`clang -O3`) | 1.390 s |
| Python | 8.1 s |

The sequential Kāra build is level with Rust and 9% faster than Rust with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.589 s and
0.597 s on one run).

## Verification

All four arms print the same output as `closest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★, pointers and set arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 22 edits. The nested
`fn sums` moved above the `impl`, since Kāra has no nested items and it
captures nothing; `struct Solution {}` was added; `Vec<i32>` became
`Vec[i32]` and `&[i32]` became `Slice[i32]`; `vec![0]` became `[0i32]`;
the `&` came off the `for &x in v` and `|&r|` patterns and off the
`&nums[..n / 2]` arguments; `for &l in &left` became `for l in ref left`;
`sort_unstable` became `sort`; and `i32::MAX` and
`Solution::min_abs_difference` took `.` paths. `partition_point`, the
`min` and `abs` methods and the doubling loop carried over as written.

The differential and the bench checked clean as generated.
