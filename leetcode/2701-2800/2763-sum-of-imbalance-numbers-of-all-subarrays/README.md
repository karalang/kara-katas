# 2763. Sum of Imbalance Numbers of All Subarrays

The **imbalance number** of a **0-indexed** integer array `arr` of
length `n` is defined as the number of indices in `sarr = sorted(arr)`
such that:

- `0 <= i < n - 1`, and
- `sarr[i + 1] - sarr[i] > 1`

Here, `sorted(arr)` is the function that returns the sorted version of
`arr`.

Given a **0-indexed** integer array `nums`, return *the **sum of
imbalance numbers** of all its **subarrays***.

A **subarray** is a contiguous **non-empty** sequence of elements within
an array.

```
nums = [2, 3, 1, 4]     ->  3
nums = [1, 3, 3, 3, 5]  ->  8
```

**Constraints:** `1 <= nums.length <= 1000`, `1 <= nums[i] <=
nums.length`.

## Approaches

A subarray's distinct values fall into runs of consecutive numbers, and
its imbalance is the gaps between runs: the runs less 1.

| file | mechanism |
|---|---|
| `imbalance.kara` ★ | each run counted once, at the leftmost occurrence of its top value x with no x + 1 in the subarray: index i is that for (i - left) (right - i) subarrays, left the last x or x + 1 before it and right the first x + 1 after it, each from one pass keeping the last place of every value. O(n) |
| `imbalance_set.kara` | from each start the numbers go into a `SortedSet`; a new number between neighbours p and s, found by `range` with `next_back` and `next`, takes away the gap p to s and adds the gaps p to x and x to s. O(n^2 log n) |
| `imbalance_bits.kara` | from each start the values seen are bits in a `Vec[u64]`, and after each number the runs are counted afresh: each word ANDed with the complement of itself shifted down, the next word's low bit carried in, and `count_ones`. O(n^3 / 64) |
| `imbalance_sorted.kara` | from each start the distinct numbers in a sorted `Vec`, each new one placed by `partition_point` and `insert`, and its neighbours, read by `get` and matched as a pair of `Option`s, saying which gaps it closes and opens. O(n^3) in the worst case, the inserts' shifting |
| `imbalance_solution.kara` | a Rust solution as LeetCode's Rust users write it, from each start a `vec![false; n + 2]` of the values seen, indexed `as usize`, and a count that a new value raises by 1 and lowers for each neighbour already seen, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one number;
1000 equal numbers and 1000 rising by 1, LeetCode's most, with no gap
anywhere; 1000 falling by 2 from 1000, twice over; 2000 random arrays of
1 to 20 numbers up to their length; and 5 of 1000, the last two with the
sum of the answers and a checksum. `imbalance.py` mirrors the ★ arm and
its output is byte-identical.

```
3
8
0
0
0
145708000
2000 small arrays: imbalances sum to 316143, checksum 269733779
5 arrays of 1000: imbalances sum to 417480693, checksum 526328975
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray copied out and sorted by `sort`, its imbalance
the indices of the sorted copy whose next number is more than 1 above,
and the imbalances summed; no counting of runs. It draws 2000 random
arrays of 1 to 14 numbers up to their length, then 40 of up to 300, all
before any arm answers; the literal reading is asked only of the first
2000.

| | property |
|---|---|
| P1 | up to 14 numbers, the answer is the literal reading's |
| P2 | the numbers reversed: the same answer |
| P3 | every number x made n + 1 - x: the same answer |
| P4 | every number made 1: 0 |
| P5 | from 0 to (n + 1) n (n - 1) / 6; and the last number put again at the end: no less |
| P6 | each arm agrees with at least three of the other four |

P5 first left the first number off and asked for no more, which keeps a
value of n in an array of n - 1: the ★ arm's tables are sized by the
length, as the constraints allow, and it stopped at an index out of
bounds. Putting the last number again keeps every value within the
length.

The differential prints `2040 cases: checksum 894434150, 61200 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same sorting gives the same checksum.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M7 first inserted an equal number again, which
changes no gap; it is replaced by an edit that opens no gap above a new
greatest number.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal number before not stopping the left end | P1 1656, P3 1485, P4 1891, P6 1696 |
| M2 | ★: the right end stopped at the next x, not x + 1 | P1 1700, P2 1634, P3 1687, P4 1891, P5 762, P6 1740 |
| M3 | set: a gap of 2 between the neighbours not closed | P1 800, P2 1001, P6 840 |
| M4 | set: the neighbour just above skipped | P1 1334, P2 1441, P3 1448, P6 1374 |
| M5 | bits: no bit carried in from the next word | P3 26, P6 21 |
| M6 | bits: the runs counted, not the runs less 1 | P1 2000, P4 2040, P5 709, P6 2040 |
| M7 | sorted: a new greatest number opening no gap | P1 1451, P2 1504, P3 1537, P5 93, P6 1491 |
| M8 | sorted: a new least number opening no gap | P1 1446, P2 1500, P3 1537, P5 102, P6 1486 |
| M9 | solution: the neighbour below never asked | P1 1513, P2 1650, P3 1697, P6 1553 |
| M10 | solution: the first number of each start never marked seen | P1 1688, P2 1544, P3 1569, P6 1728 |

## Benchmarks

The bench draws 20000 arrays of 1000 numbers up to 1000, LeetCode's
most, all of them first, then answers each 5 times by the ★ arm in all
five languages. Every implementation prints `20000 arrays of 1000, 5
rounds: imbalances sum to 8388184503130, checksum 643923927`.

BENCHTAB

## Verification

All five arms print the same output as `imbalance.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ and set arms checked clean as first written. The bits arm wrote
Rust's `!` for the complement of a word, and `karac fix` made it `~`.
The sorted arm first recounted the gaps after each insert by
`sorted.windows(2).filter(..)`, and `karac check` refused it, `windows`
giving a `Vec` of slices; `karac fix` added `.into_iter()`, but the
`Vec` of slices built afresh for every subarray took 24 s under `karac
run`, so the arm now changes the count by the new number's neighbours.
It then compared `sorted.get(at) != Some(x)`, an `Option[ref i64]`
against an `Option[i64]`; `karac check` refused it and `karac fix`
wrote `.cloned()`.

LeetCode's Rust template took 10 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `Vec<i32>` and `Vec<i64>` became
`Vec[i32]` and `Vec[i64]`; `vec![false; n + 2]` became `Vec.filled(n +
2, false)`; `!seen[x]` became `not seen[x]`; the `&x` pattern dropped
its `&`; and `Solution::` became `Solution.`, with the wrapper's `as
i64` dropped. The `as usize` casts stayed, a `usize` index being
accepted as it is.
