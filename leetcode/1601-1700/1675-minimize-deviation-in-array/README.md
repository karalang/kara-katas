# 1675. Minimize Deviation in Array

You are given an array `nums` of `n` positive integers.

You can perform two types of operations on any element of the array any
number of times:

- If the element is **even**, **divide** it by `2`.
  - For example, if the array is `[1,2,3,4]`, then you can do this
    operation on the last element, and the array will be `[1,2,3,2]`.
- If the element is **odd**, **multiply** it by `2`.
  - For example, if the array is `[1,2,3,4]`, then you can do this
    operation on the first element, and the array will be `[2,2,3,4]`.

The **deviation** of the array is the **maximum difference** between any
two elements in the array.

Return *the **minimum deviation** the array can have after performing
some number of operations.*

```
nums = [1,2,3,4]      ->  1
nums = [4,1,5,20,3]   ->  3
nums = [2,10,8]       ->  3
```

**Constraints:** `n == nums.length`; `2 <= n <= 5 * 10^4`;
`1 <= nums[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `deviation.kara` ★ | every value at the largest it can reach (odd values doubled) in a `PriorityQueue.max_first()`, the smallest kept beside it; the largest is popped, the deviation measured, and while it is even it goes back halved. Once the largest is odd it can only rise, and the loop stops. O(n log n log m) |
| `deviation_sorted.kara` | the same values, each with its index so equal ones stay apart, in a `SortedSet`: the deviation is its `max()` less its `min()`, and an even largest is taken out and put back halved. O(n log n log m) |
| `deviation_window.kara` | every value each one can reach, tagged with its index, sorted; a window slides over them, and the narrowest that holds a value from every index is the answer. O(n log m log(n log m)) |
| `deviation_solution.kara` | a Rust solution as LeetCode's Rust users write it, the ★ arm's queue a `std::collections::BinaryHeap` drained by `while let Some(max_val) = heap.pop()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, two odd
values (1), a value that halves down to another's double (0), and the
largest values (1); then the deviations summed and a checksum for 3000
random arrays of up to 8 values up to 64, 300 of up to 1000 values up to
`10^9` and 10 of up to `5 * 10^4` values up to `10^9`. `deviation.py`
mirrors the ★ arm and its output is byte-identical.

```
1
3
3
1
0
1
3000 arrays of up to 8 values up to 64: deviations sum to 84475, checksum 77189207
300 arrays of up to 1000 values up to 1000000000: deviations sum to 296239964452, checksum 9150859
10 arrays of up to 50000 values up to 1000000000: deviations sum to 9996474530, checksum 102972444
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each value's reachable set is found by applying the two
operations until nothing new comes, and every choice of one reachable
value per position is tried; the least largest-less-smallest wins. It
checks 3000 random arrays of 2 to 5 values from 1 to between 1 and 48.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | each odd value doubled, the largest it can reach, gives the same answer |
| P4 | every value times 3 gives 3 times the answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 289043559, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the least over `itertools.product` of the
reachable sets, gives the same checksum. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first drafts were replaced. A
first M5 tagged every halved value with index 0, so that two equal
values could merge in the set; that changes the answer too rarely for
3000 small arrays to show, and it passed every check. A first M1 started
every value as it was (`let start = x;`), which makes the queue a
`PriorityQueue[ref i32]` of the loop's elements; that program is valid,
but `karac check` refused it (E0516, the loop variable "written while
borrowed") and the build could not lower the queue's sift of a
reference element. The first was fixed in kara `93fd9b2078` (B-2026-11-20-35); the
second is B-2026-11-20-40. M1 now starts odd values undoubled and even values
doubled, which keeps the queue's values `i32`.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: odd values start undoubled, even ones doubled | P1 1908, P3 1227, P5 1908 |
| M2 | ★: the smallest not lowered by a halved value | P1 1035, P5 1035 |
| M3 | ★: the loop stops at a top that is 2 mod 4 | P1 2718, P5 2718 |
| M4 | sorted: odd values not doubled | P1 1087, P3 1087, P5 1087 |
| M5 | sorted: the deviation read down to the second smallest | P1 2301, P5 2301 |
| M6 | window: an odd value's double not reachable | P1 1087, P3 1087, P5 1087 |
| M7 | window: the window shrunk once per value, not while it covers | P1 2479, P5 2479 |
| M8 | window: the halving stops one short | P1 2718, P5 2718 |
| M9 | solution: the smallest not lowered by a halved value | P1 1035, P5 1035 |
| M10 | solution: the smallest never taken from the start values | P1 3000, P4 3000, P5 3000 |

## Benchmarks

The bench draws 50 arrays of `5 * 10^4` values up to `10^9`, LeetCode's
largest, all of them first, then answers each 10 times by the ★ arm in
all five languages: `PriorityQueue.max_first()` in Kāra, `BinaryHeap` in
Rust, `heapq` on negated values in Python, `container/heap` in Go, and a
binary max-heap written for the bench in C. Every implementation prints
`50 arrays of 50000 values, 10 rounds: deviations sum to 499971988460,
checksum 54907629`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.549 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.592 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.596 s |
| Kāra (`karac build`) | 0.614 s |
| C (`clang -O3`) | 0.667 s |
| Go | 1.908 s |
| Python | 6.2 s |

The sequential Kāra build is 1.09x Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.583 s and 0.590 s on one
run).

## Verification

All four arms print the same output as `deviation.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ and window arms checked clean as first written.

The sorted arm's first draft read the set's ends with `last()` and
`first()`, Rust's `BTreeSet` names; `karac check` named Kāra's, `max()`
and `min()`, and `karac fix` wrote them.

LeetCode's Rust template took one `karac fix` of 10 edits: the
`use std::collections::BinaryHeap;` line replaced by `struct Solution {}`,
`Vec<i32>` written `Vec[i32]`, `BinaryHeap::new()` written
`PriorityQueue.max_first()` (Rust's heap pops the largest first, and so
does that one; `PriorityQueue.new()` would pop the smallest), each
`i32::MAX` written `i32.MAX`, and `for &num in &nums` written
`for num in ref nums`.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does (B-2026-11-19-131).
