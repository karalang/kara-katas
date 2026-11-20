# 1671. Minimum Number of Removals to Make Mountain Array

You may recall that an array `arr` is a **mountain array** if and only
if:

- `arr.length >= 3`
- There exists some index `i` (**0-indexed**) with `0 < i < arr.length - 1`
  such that:
  - `arr[0] < arr[1] < ... < arr[i - 1] < arr[i]`
  - `arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`

Given an integer array `nums`, return *the **minimum** number of elements
to remove to make `nums` a **mountain array***.

```
nums = [1,3,1]               ->  0
nums = [2,1,1,5,6,2,3,1]     ->  3
```

**Constraints:** `3 <= nums.length <= 1000`; `1 <= nums[i] <= 10^9`; it
is guaranteed that you can make a mountain array out of `nums`.

## Approaches

| file | mechanism |
|---|---|
| `mountain.kara` ★ | `up[i]`, the longest strictly rising run of kept values ending at i, and `down[i]`, the longest strictly falling one starting there, each from the values before (after) it; a value with both longer than 1 can be the peak of a mountain of `up[i] + down[i] - 1`. O(n^2) |
| `mountain_patience.kara` | the same two tables by patience sorting: a value replaces the first tail not below it, found by `partition_point`, and the run it ends is that index + 1 long; one pass forward, one over the reversed array. O(n log n) |
| `mountain_peaks.kara` | every value tried as the peak: the longest rise among the values before it that are below it, and the longest fall among those after, each found afresh by a patience pass over an `impl Iterator`. O(n^2 log n) |
| `mountain_solution.kara` | LeetCode's Rust template, the ★ arm's tables written `vec![1; n]` with `max` as a method, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's two examples, a mountain
already (0), one whose sides hold every value twice (5), a peak behind
two larger values (2), and a peak next to the end (0); then the removals
summed and a checksum for 3000 random arrays of up to 12 values up to 5,
300 of up to 1000 values up to `10^9` and 30 of up to 1000 values up to
10. A random array has one value inside raised above all the others, so
a mountain can always be made of it. `mountain.py` mirrors the ★ arm and
its output is byte-identical.

```
0
3
0
5
2
0
3000 arrays of up to 12 values up to 5: 9052 removals, checksum 425514723
300 arrays of up to 1000 values up to 1000000000: 127569 removals, checksum 760706399
30 arrays of up to 1000 values up to 10: 16141 removals, checksum 614776176
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every set of kept values, in order, from all `2^n`, is tried
as a mountain (at least 3, strictly up to a peak that is neither end,
then strictly down), and the fewest removed wins. It checks 3000 random
arrays of 3 to 10 values from 1 to between 2 and 6, each drawn again
until a mountain can be made of it. Unlike the arms' batches, no value is
raised above the rest, so the best peak need not be the largest value.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer leaves at least 3 values |
| P3 | the array reversed gives the same answer |
| P4 | every value raised by 1000 gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 484099455, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, by `itertools.combinations`, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first draft of the differential
raised one value above all the others, as the arms' batches do; there
the largest value is always the best peak, and M2, which lets a run that
only rises (or only falls) count as a mountain, passed every check. The
draw was changed to keep any array a mountain can be made of, and M2 now
fails 9 of 3000; M10 fails 3 for the same reason, it takes the rising
side alone.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the rise not strict (`<=`) | P1 1655, P3 1464, P5 1655 |
| M2 | ★: a peak with a rise or a fall, not both | P1 9, P5 9 |
| M3 | ★: the peak counted twice short (`- 2`) | P1 3000, P2 1729, P5 3000 |
| M4 | patience: a tail equal to the value kept (`<=`), the rise not strict | P1 2043, P5 2043 |
| M5 | patience: each run one short | P1 3000, P2 2683, P5 3000 |
| M6 | patience: the falls left in reversed order | P1 1204, P2 586, P5 1204 |
| M7 | peaks: the left side takes values equal to the peak | P1 919, P3 69, P5 919 |
| M8 | peaks: the right side read forward, a rise | P1 729, P3 1020, P5 729 |
| M9 | solution: a fall extended by a rise's length | P1 1180, P2 131, P3 1431, P5 1180 |
| M10 | solution: a peak with a rise alone | P1 3, P3 9, P5 3 |

## Benchmarks

The bench draws 300 arrays of 1000 values up to `10^9`, LeetCode's
largest, one raised above the rest, all of them first, then answers each
by the ★ arm in all five languages. Every implementation prints `300
arrays of 1000 values: 274952 removals, checksum 36504183`. The C build
also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.350 s |
| Rust (`rustc -O`) | 0.380 s |
| Go | 0.473 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.490 s |
| Kāra (`karac build`) | 0.492 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.522 s |
| Python | 12 s |

The sequential Kāra build takes 1.29x Rust's time and 0.94x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.350 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.474 s and 0.478 s on one
run).

## Verification

All four arms print the same output as `mountain.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and patience arms checked clean as first written.

The peaks arm's first draft took `values: impl Iterator[Item = i32]` and
looped over it, and passed `nums[..i].iter().filter(..)`. Two errors:
a bare parameter borrows, and a borrowed iterator cannot be advanced
(E0232), so `karac fix` took it `own impl Iterator[..]`; and a slice's
`iter()` yields `ref i32`, not the `i32` the bound names, so the fix
added `.cloned()` after each `filter`.

LeetCode's Rust template took one `karac fix` of 6 edits:
`struct Solution {}` added, `Vec<i32>` written `Vec[i32]`, each
`vec![1; n]` written `Vec.filled(n, 1)`, and `&&` written `and`.

The bench first passed `nums.clone()`; the `redundant_clone` lint saw
that the parameter only borrows it, and `karac fix` passed `nums`.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
