# 2831. Find the Longest Equal Subarray

You are given a **0-indexed** integer array `nums` and an integer `k`.

A subarray is called **equal** if all of its elements are equal. Note
that the empty subarray is an **equal** subarray.

Return *the length of the **longest** possible equal subarray after
deleting **at most** `k` elements from* `nums`.

A **subarray** is a contiguous, possibly empty sequence of elements
within an array.

```
nums = [1,3,2,3,1,3], k = 3  ->  3
nums = [1,1,2,2,1,1], k = 2  ->  4
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <=
nums.length`; `0 <= k <= nums.length`.

## Approaches

| file | mechanism |
|---|---|
| `equal.kara` ★ | the places of each value listed in order in a `Vec` of lists, and two pointers over each list: places l..=r of one value become a run by deleting the (pos[r] - pos[l]) - (r - l) numbers between them, so l catches up while that exceeds k |
| `equal_window.kara` | one window over the array with a count per value and the most of any value seen: the window grows while its length minus that most is within k and slides when it is not, so the most never comes down and is the answer |
| `equal_search.kara` | for each value, gap[j] = pos[j] - j, the other numbers before its j-th place, in a `Map` of lists through `entry().or_insert()`; the gaps rise, so for each r the first l within k is found by `partition_point` |
| `equal_each.kara` | from every start i, the run of nums[i] grown rightward, each other number spending one of k deletions until they run out; O(n^2), for the harness's lengths |
| `equal_solution.kara` | a Rust solution as LeetCode's Rust users write it: each value's places in a `HashMap<i32, Vec<usize>>` by `entry().or_default()`, and the same two pointers over `values()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one
number; k = 0, the longest run; k large enough to delete everything
else; 2000 numbers alternating 1 and 2 with k = 999; then 3000 random
arrays of 1 to 12 numbers from 1 to 3 with k up to the count, and 50
of up to 3000 numbers from 1 to 20 with k up to 100, as checksums.
`equal.py` mirrors the ★ arm and its output is byte-identical.

```
3
4
1
4
4
1000
3000 short arrays: checksum 36454989
50 long arrays: checksum 476630632
```

The random values are drawn below `min(n, 3)` (or `min(n, 20)`) plus
one. The harness as first written drew them from 1 to 3 for every
length, which breaks the constraint `nums[i] <= nums.length` for one
or two numbers, and the arms that index by value stopped with an
index out of bounds; that was the harness's error, not theirs.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every subarray and every value in it, kept when the
other numbers in it are at most k, and the most of that value's count.
It draws 2000 random arrays of 1 to 12 numbers from 1 to 3 with k up
to the count, then 50 of up to 2000 numbers from 1 to 20 with k up to
100, all before any arm answers; the literal reading is asked only of
the first 2000.

| | property |
|---|---|
| P1 | up to 12 numbers, the answer is the literal reading's |
| P2 | the numbers reversed: the same answer |
| P3 | k one larger: no shorter |
| P4 | k = n: the count of the commonest value |
| P5 | every v as m + 1 - v, m the largest: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 127989233, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed under both
backends, nine the same way. M10's counts differ between the two because
the mutated arm keeps the best of whichever value's places come last in
a walk over its `Map`, whose order is per process; the counts below are
`__mir-llvm-run`'s.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the gap measured without the kept ones | P1 835, P6 868 |
| M2 | ★: the window counted one short | P1 2000, P4 2050, P6 2050 |
| M3 | window: the window shrunk only past k + 1 | P1 218, P6 223 |
| M4 | window: the left count never given back | P1 336, P6 383 |
| M5 | search: a gap equal to k left out | P1 590, P6 596 |
| M6 | search: the gap taken from the raw index | P1 835, P6 868 |
| M7 | each: the deletions allowed one past k | P1 218, P6 223 |
| M8 | each: the best kept only at the end of a run | P1 814, P2 751, P4 967, P6 815 |
| M9 | solution: the left end moved too soon | killed under both: runtime error: index out of bounds |
| M10 | solution: the best overwritten, not kept | P1 820, P2 956, P4 765, P6 869 (`__mir-run`: P1 1000, P2 884, P4 1063, P6 1048) |

## Benchmarks

The bench draws 20 arrays of 10^5 numbers from 1 to 1000 with k up to
1000, all of them first, then answers each 20 times by the ★ arm in
all five languages. C lays the places out by a count of each value and
a prefix sum into one array, where the others push onto a list per
value; the two pointers are the same. Every implementation prints `20
arrays of 100000, 20 rounds: lengths total 2720, checksum 522062222`.

BENCHTAB

## Verification

All five arms print the same output as `equal.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 19 `karac fix` edits in one run, the
wrapper included: `use std::collections::HashMap` went and `struct
Solution {}` came for the `impl`; `Vec<..>` became `Vec[..]`,
`HashMap<..>` `Map[..]` and `usize` `i64`; `HashMap::new()` became
`Map.new()` and `entry(x).or_default()` became
`entry(x).or_insert(Vec.new())`; `for (i, &x)` and `|&v|` lost their
`&`; `k as usize` became `k as i64`; `Solution::` took `.`, and the
wrapper's `as i64` went.
