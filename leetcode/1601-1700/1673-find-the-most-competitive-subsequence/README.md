# 1673. Find the Most Competitive Subsequence

Given an integer array `nums` and a positive integer `k`, return *the
most **competitive** subsequence of* `nums` *of size* `k`.

An array's subsequence is a resulting sequence obtained by erasing some
(possibly zero) elements from the array.

We define that a subsequence `a` is more **competitive** than a
subsequence `b` (of the same length) if in the first position where `a`
and `b` differ, subsequence `a` has a number **less** than the
corresponding number in `b`. For example, `[1,3,4]` is more competitive
than `[1,3,5]` because the first position they differ is at the final
number, and `4` is less than `5`.

```
nums = [3,5,2,6], k = 2              ->  [2,6]
nums = [2,4,3,3,5,4,9,6], k = 4      ->  [2,3,3,4]
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^9`;
`1 <= k <= nums.length`.

## Approaches

| file | mechanism |
|---|---|
| `competitive.kara` ★ | a rising stack: each value pops the larger values on top while enough values remain after it to still fill k, then goes on if the stack is not full. Each value is pushed and popped at most once: O(n) |
| `competitive_scan.kara` | the j-th value is the smallest in the window that still leaves k - j - 1 values after it, the first one on a tie, and the next window starts after it. O(n * k) at worst |
| `competitive_heap.kara` | the same windows, their values in a min-`PriorityQueue` of (value, index): each step adds the value its window gains and takes the smallest at or after the window's start, dropping any left behind. O(n log n) |
| `competitive_solution.kara` | a Rust solution as LeetCode's Rust users write it, the ★ arm's stack with `k as usize`, `Vec::with_capacity(k)` and `while let Some(&top) = stack.last()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's two examples, all of an
array, one value, and k = 3 of a rising and of a falling array; then the
values chosen and a checksum of every answer for 3000 random arrays of up
to 12 values below 5, 300 of up to 1000 below `10^9`, and 10 of up to
`10^5` below 10, each with a random k. `competitive.py` mirrors the ★ arm
and its output is byte-identical.

```
[2, 6]
[2, 3, 3, 4]
[5, 1, 4]
[1]
[1, 2, 3]
[3, 2, 1]
3000 arrays of up to 12 values below 5: 11503 chosen, checksum 118178720
300 arrays of up to 1000 values below 1000000000: 77256 chosen, checksum 467090788
10 arrays of up to 100000 values below 10: 93375 chosen, checksum 538371057
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every choice of k indexes in order, from all `2^n` sets, is
read as a subsequence, and they are compared as sequences, `<` on two
`Vec`s; the smallest wins. It checks 3000 random arrays of 1 to 10 values
from 0 to between 1 and 5, each with a random k. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer holds k values and is a subsequence of `nums` |
| P3 | a value above all the others put in front changes nothing |
| P4 | a value below all the others put in front, with k + 1, gives that value and then the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 835479923, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the smallest of `itertools.combinations`,
gives the same checksum. On a failure it prints the first ten and then
the count by property. A first P3 put the large value at the end and was
false (more room behind can let an earlier, smaller value in:
`[2,1,3,2,0]`, k = 3, gives `[1,2,0]`, and with a 9 behind it `[1,0,9]`);
every arm failed it the same way, and it was replaced.

## Mutation testing

Ten edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M7 stops on both before any property is
checked: with the first value never taken, the heap runs dry and
`unwrap()` meets `None`. M1 and M5 make the same mistake in two arms (one
value too little room) and fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a pop only when one more value than needed remains | P1 877, P3 917, P5 877 |
| M2 | ★: the stack let grow to k + 1 | P1 1206, P2 1206, P5 1206 |
| M3 | ★: a smaller value empties the whole stack | P1 725, P2 562, P4 1320, P5 725 |
| M4 | scan: the last smallest taken on a tie | P1 422, P5 422 |
| M5 | scan: each window one value short | P1 877, P3 917, P5 877 |
| M6 | scan: the next window starts at the value taken | P1 1167, P2 1167, P4 3000, P5 1167 |
| M7 | heap: the value at the window's start skipped | `called unwrap() on None` |
| M8 | heap: one value never pushed | P1 499, P4 992, P5 499 |
| M9 | solution: a pop with one value too few left | P1 897, P2 897, P5 897 |
| M10 | solution: smaller values popped, not larger | P1 1588, P3 3000, P4 2083, P5 1588 |

## Benchmarks

The bench draws 50 arrays of `10^5` values up to `10^9`, LeetCode's
largest, each with a random k, all of them first, then answers each 20
times by the ★ arm in all five languages; the sink folds each answer's
length and its first and last values. Every implementation prints `50
arrays of 100000 values, 20 rounds: 49535260 chosen, checksum
109480773`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.615 s |
| Rust (`rustc -O`) | 0.644 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.651 s |
| Kāra (`karac build`) | 0.688 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.690 s |
| Go | 0.856 s |
| Python | 13 s |

The sequential Kāra build takes 1.07x Rust's time and 1.06x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.615 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.712 s and 0.736 s on one
run).

## Verification

All four arms print the same output as `competitive.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm checked clean as first written. The scan arm wrote the window's
end `n - (k as i64 - j - 1)`; `k` is an `i32` that widens by itself, and
`karac fix` dropped the cast.

The heap arm's first draft built its queue `PriorityQueue.min()`, a
direction guessed into the constructor's name; Kāra's `PriorityQueue.new()`
pops the smallest first and `max_first()` the largest (the opposite of
Rust's `BinaryHeap`). The refusal named no constructor until kara
`93fd9b2078` (B-2026-11-20-34); since then it says which one is meant, and `karac fix`
wrote `PriorityQueue.new()`.

LeetCode's Rust template took one `karac fix` of 13 edits:
`struct Solution {}` added, `Vec<i32>` written `Vec[i32]`, `k as usize`
written `k as i64`, `Vec::with_capacity` written `Vec.with_capacity`,
`for (i, &x)` written `for (i, x)`, `while let Some(&top) =
stack.last()` written `while let Some(top) = stack.last().cloned()`, and
`&&` written `and`.

The differential's literal first matched `best` by value inside the loop,
which moves it out, and `karac check` refused the later `best.unwrap()`
(E0500); `karac fix` bound it `Some(ref b)`. Its P4 array was first
`vec![-1]`, deprecated, and `karac fix` wrote the list literal `[-1]`.
`arm_name` indexes a list of string literals for a `Str`, as #1662's
differential does (B-2026-11-19-131).
