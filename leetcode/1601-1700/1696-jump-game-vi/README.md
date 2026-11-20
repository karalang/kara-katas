# 1696. Jump Game VI

You are given a **0-indexed** integer array `nums` and an integer `k`.

You are initially standing at index `0`. In one move, you can jump at
most `k` steps forward without going outside the boundaries of the
array. That is, you can jump from index `i` to any index in the range
`[i + 1, min(n - 1, i + k)]` **inclusive**.

You want to reach the last index of the array (index `n - 1`). Your
**score** is the **sum** of all `nums[j]` for each index `j` you visited
in the array.

Return *the **maximum score** you can get*.

```
nums = [1,-1,-2,4,-7,3], k = 2              ->  7
nums = [10,-5,-2,4,0,3], k = 3              ->  17
nums = [1,-5,-20,4,-1,3,-6,-3], k = 2       ->  0
```

**Constraints:** `1 <= nums.length, k <= 10^5`;
`-10^4 <= nums[i] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `jump.kara` ★ | best[i] is nums[i] plus the best of the k scores before it; a `VecDeque` holds the indexes in reach whose scores fall from front to back, one that left the reach going off the front and a new score popping those at the back no better than it, so the front is the best. O(n) |
| `jump_heap.kara` | each score into a max-first `PriorityQueue` with its index; the top taken once any that left the reach is popped. O(n log n) |
| `jump_table.kara` | the largest of the k scores before each index read afresh, `best[from..i].iter().max()`. O(n * k) |
| `jump_solution.kara` | a Rust solution as LeetCode's Rust users write it, `k as usize`, `vec![0; n]` and a `VecDeque<usize>` trimmed by `while let Some(&front) = dq.front()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, one value,
and steps of one; then the answers summed and a checksum for 3000 random
arrays of up to 12 values within 5, 300 of up to 1000 values within
`10^4` and 10 of up to `10^5` values within `10^4`, each with a random k
up to its length (and up to 100 for the last, so the table arm finishes).
`jump.py` mirrors the ★ arm and its output is byte-identical.

```
7
17
0
5
0
3000 arrays of up to 12 values within 5, k up to 12: answers sum to 15112, checksum 451342483
300 arrays of up to 1000 values within 10000, k up to 1000: answers sum to 243111136, checksum 615183458
10 arrays of up to 100000 values within 10000, k up to 100: answers sum to 358922528, checksum 236764185
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way from index 0 to the last, each jump 1 to k forward
and never past the end, scored by the values stood on, by recursion; the
best score wins. It checks 3000 random arrays of 1 to 10 values from -5
to 5, each with a k from 1 to its length. Every case is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a k of at least n - 1 gives the first value, the last, and every positive one between |
| P3 | k + 1 never gives less |
| P4 | the array reversed gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 795193245, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the same recursion over every path, gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1 and M8 reach one index too far and
fail the same 537 checks; only P1 sees them, as a longer reach is a
larger k, which P2 and P3 allow. M5, M7 and M9 each jump from the worst
score in reach and fail the same checks. Three first drafts reached one
index short and stopped on k = 1 with nothing in reach (the deque
emptied, a slice `max()` of nothing); they were replaced. A first M10
deleted `dp[0] = nums[0]`, the only store that types `dp`'s elements
`i32`, and `karac check` refused the narrowing at the return; it was
replaced too.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one index more kept in reach | P1 537, P5 537 |
| M2 | ★: the jump taken from the back of the deque | P1 1724, P2 2050, P5 1724 |
| M3 | ★: the deque's last index never popped for a better score | P1 1412, P2 2029, P3 631, P4 143, P5 1412 |
| M4 | heap: each value pushed for its score | P1 2113, P2 2006, P4 2086, P5 2113 |
| M5 | heap: smallest first | P1 1957, P2 2379, P3 537, P5 1957 |
| M6 | table: twice the reach | P1 564, P5 564 |
| M7 | table: `min()` for `max()` | P1 1957, P2 2379, P3 537, P5 1957 |
| M8 | solution: one index more kept in reach | P1 537, P5 537 |
| M9 | solution: the scores kept rising, not falling | P1 1957, P2 2379, P3 537, P5 1957 |
| M10 | solution: the jump taken from the back of the deque | P1 1724, P2 2050, P5 1724 |

## Benchmarks

The bench draws 50 random arrays of `10^5` values within `10^4`,
LeetCode's largest, each with a random k up to `10^5`, all of them
first, then answers each 20 times by the ★ arm in all five languages:
`VecDeque` in Kāra and Rust, `collections.deque` in Python, and in C and
Go, which have no deque, an array with a head and a tail (an index only
goes on at the back, so n slots hold them all). Every implementation
prints `50 arrays of 100000 values, 20 rounds: answers sum to
164191437780, checksum 12038672`. The C build also runs clean under
gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.835 s |
| Rust (`rustc -O`) | 0.863 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.873 s |
| Go | 0.883 s |
| Kāra (`karac build`) | 0.890 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.907 s |
| Python | 17 s |

The sequential Kāra build is 1.05x Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.835 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.881 s and 0.902 s on one
run).

## Verification

All four arms print the same output as `jump.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, heap and table arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 14 edits: the
`use std::collections::VecDeque;` line replaced by `struct Solution {}`
(`VecDeque` is in Kāra's prelude), `Vec<i32>` and `VecDeque<usize>`
written with brackets and `usize` as `i64`, `k as usize` written
`k as i64`, `vec![0; n]` written `Vec.filled(n, 0)`, `VecDeque::new`
written `VecDeque.new`, and each `while let Some(&front) = dq.front()`
written `while let Some(front) = dq.front().cloned()`. The
`dp[*dq.front().unwrap()]` that reads the best index carried over as
written.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
