# 930. Binary Subarrays With Sum

Given a binary array `nums` and an integer `goal`, return the number of
non-empty subarrays with a sum `goal`.

A subarray is a contiguous part of the array.

```
nums = [1,0,1,0,1], goal = 2  ->  4   ([1,0,1], [1,0,1,0], [0,1,0,1], [1,0,1])
nums = [0,0,0,0,0], goal = 0  ->  15
```

**Constraints:** `1 <= nums.length <= 3 * 10^4`; `nums[i]` is either
`0` or `1`; `0 <= goal <= nums.length`.

## Approaches

| file | mechanism |
|---|---|
| `num_subarrays_with_sum.kara` ★ | one pass with the running prefix sum and, in a `Vec` of `n + 1` slots indexed by value, how many earlier prefixes had each sum; each step adds the count of prefixes equal to the running sum less `goal`. O(n), O(n) space |
| `num_subarrays_with_sum_window.kara` | a sliding window counting the subarrays whose sum is at most `goal`, run twice: exactly `goal` is at most `goal` less at most `goal - 1`. O(n), O(1) space |
| `num_subarrays_with_sum_ones.kara` | the positions of the 1s with a sentinel at each end: `goal` consecutive 1s add the product of the gaps before the first and after the last, and with `goal` 0 each run of `z` zeros adds `z * (z + 1) / 2`. O(n) |
| `num_subarrays_with_sum_three.kara` | one window per end, shrunk past surplus 1s and leading 0s, never past its end, counting the 0s passed since the last 1 dropped; with the sum at `goal`, that count plus one subarrays end there. O(n), O(1) space |
| `num_subarrays_with_sum_map.kara` | the prefix-sum count run from the right over suffix sums, kept in a `Map[i64, i64]`. O(n) expected |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more (a single element either way, `goal` 0 over all 1s, a goal above
the 1s, all 1s, `goal` 0 between 1s, 0s at both ends, and every 1
needed); for 300 random arrays of 1 to 2,000 elements, leaning from 0 to
1, with a goal up to one past the number of 1s, the answers' sum and a
checksum; and three of LeetCode's largest, 30,000 elements: all 0s with
`goal` 0 (450,015,000), all 1s with `goal` 15,000, and alternating with
`goal` 7,500. `num_subarrays_with_sum.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every non-empty subarray, its elements added one by one,
counted when the sum is `goal`. It checks 3,200 random arrays, each
leaning from 0 to 1 by a random amount, with a goal from 0 to one past
the number of 1s: 3,000 of 1 to 12 elements against the statement, and
200 of 1 to 2,000 against the other properties; 191,523 elements in
all.

| | property |
|---|---|
| P1 | the statement's answer, on the small arrays |
| P2 | between 0 and `n(n + 1)/2`, and positive exactly when some subarray can sum to `goal` |
| P3 | the same answer for the array reversed |
| P4 | a 0 at the end adds one subarray for each suffix, the empty one included, that sums to `goal` |
| P5 | the array followed by a second random array of 1 to 50 elements counts both arrays' answers plus the subarrays crossing the join, counted from the suffix sums of the first and the prefix sums of the second |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays, 191523 elements, answers summing to 2244338,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (6 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty prefix never counted | P1 1952, P2 365, P3 1027, P4 773, P5 1805, P6 2148 |
| M2 | ★: each prefix counted before it is looked up | P1 780, P2 387, P4 786, P6 786 |
| M3 | ★: no lookup when the running sum is exactly `goal` | P1 1952, P2 834, P3 972, P4 773, P5 2303, P6 2148 |
| M4 | window: each window one start short | P1 780, P2 417, P4 786, P6 786 |
| M5 | window: at most `goal` less at most `goal - 2` | P1 2129, P2 766, P4 2414, P5 1736, P6 2323 |
| M6 | window: the first element never ending a window | P1 1678, P2 434, P3 768, P4 832, P5 2349, P6 1771 |
| M7 | ones: a run of `z` zeros holding `z` subarrays | P1 465, P4 502, P5 229, P6 470 |
| M8 | ones: the last window of 1s left out | P1 1457, P2 500, P3 671, P4 1648, P5 1707, P6 1648 |
| M9 | ones: the gap after a window one short | P1 1457, P2 647, P3 1017, P5 1981, P6 1648 |
| M10 | three: the 0s passed kept after a 1 is dropped | P1 731, P3 783, P4 1023, P5 2408, P6 919 |
| M11 | three: the window itself not counted | P1 2123, P2 826, P3 1017, P4 2434, P5 1858, P6 2320 |
| M12 | three: leading 0s never passed | P1 1302, P3 1017, P4 1102, P5 1796, P6 1494 |
| M13 | map: the empty suffix never counted | P1 1954, P2 363, P3 1027, P4 786, P5 1948, P6 2150 |
| M14 | map: `goal` less the sum looked up | P1 1936, P2 615, P3 1384, P5 2682, P6 2130 |
| M15 | map: each suffix sum noted once, not counted | P1 1281, P3 1017, P4 2150, P5 1837, P6 1471 |

P1 and P6 kill all fifteen, P4 and P5 thirteen each, and P2 and P3
eleven each. M2 and M4 are off by exactly `n` when `goal` is 0 (M2
pairs each prefix with itself, counting an empty subarray at every end,
and M4 loses one start at every end), and both are right otherwise: P5
splits that `n` exactly between the two arrays, and the reversed array
is off by the same `n`, so P3 and P5 miss both, while P2 sees them where
the error crosses a bound. P3 also misses M5 and M7, whose mistakes are
as symmetric. P2 misses the four whose wrong counts stay within bounds
and positive exactly when a subarray is possible (M7, M10, M12 and M15).
P4 misses M9 and M14, whose wrong answers happen to grow by exactly the
suffix count when a 0 is added.

Seven other edits were tried and set aside. One stopped at runtime on an
index out of bounds (window keeping its windows below `goal`, which for
`goal` 0 never stops shrinking). Five failed exactly the same checks as
a kept mutant: ★ noting each prefix sum once, as M12; ones putting its
first sentinel at 0 and map never adding the first element, as M1; and
three shrinking past its end and map noting each suffix before looking
it up, as M2. One was sound but beyond three an arm (ones adding the
gaps rather than multiplying them).

## Verification

Every arm prints the same output as `num_subarrays_with_sum.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.5 to 1.2 s each and the
differential 6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The window, ones, three and map arms print the same output under the
frozen legacy interpreter, the legacy JIT and both legacy builds, with
and without auto-par; the builds of the window arm also warn that
`nums` is moved and then used again, which v2's borrowing parameters
make untrue. Legacy refuses the ★ arm, the differential and the bench
program at the first `*` on an element of a `Vec[i64]`'s `.iter()`
("unary '*' requires 'ref T', ... found 'i64'"), legacy's older rule;
under v2 the element is a reference and the `*` is required. Legacy is
frozen, so none of this is filed.

## Benchmarks

The bench program builds 100 arrays of 30,000 elements once, LeetCode's
largest, each leaning from 0 to 1 by a random amount and given a goal
from 0 to its number of 1s, and in each of 100 rounds runs the ★ arm on
every array, each round starting from a different one. Every
implementation prints `100 rounds over 100 arrays of 30000: answers
summing to 1262893900, checksum 800895525`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.30 to 0.38 s | 0.35 s |
| Rust (`rustc -O`) | 0.36 to 0.44 s | 0.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.48 to 0.57 s | 0.52 s |
| Go | 0.54 to 0.62 s | 0.58 s |
| Python | 22.7 s | |
| Kāra (`karac build --mir`) | 0.54 to 0.69 s | 0.59 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 66 times C's.

v2 takes 1.13 times Rust's median time under overflow checks and 1.70
times C's. The loop has no branch worth predicting: under valgrind's
cachegrind all three mispredict fewer than 40,000. v2 runs 9.06 billion
instructions and 4.74 billion branches, Rust with overflow checks 7.57
billion and 4.45 billion, and C 4.68 billion and 2.85 billion, so the
gap follows the instruction count; that the difference is overflow and
bounds checks on `seen[sum - goal]` and `seen[sum]` is inferred, not
profiled.
