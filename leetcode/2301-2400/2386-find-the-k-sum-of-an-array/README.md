# 2386. Find the K-Sum of an Array

You are given an integer array `nums` and a **positive** integer `k`.
You can choose any **subsequence** of the array and sum all of its
elements together.

We define the **K-Sum** of the array as the `k`th **largest**
subsequence sum that can be obtained (**not** necessarily distinct).

Return *the K-Sum of the array*.

A **subsequence** is an array that can be derived from another array by
deleting some or no elements without changing the order of the
remaining elements.

**Note** that the empty subsequence is considered to have a sum of `0`.

```
nums = [2,4,-2], k = 5           ->  2
nums = [1,-2,3,4,-10,12], k = 16 ->  10
```

**Constraints:** `n == nums.length`; `1 <= n <= 10^5`;
`-10^9 <= nums[i] <= 10^9`; `1 <= k <= min(2000, 2^n)`.

The largest sum takes every positive value. Any other sum is the largest
less some set of the values' sizes: a positive left out, or a negative
put in, costs its size. So the `k`th largest is the largest less the
`k`th smallest sum of a set of the sizes, the empty set first, and only
the smallest `k` of those are ever needed.

## Approaches

| file | mechanism |
|---|---|
| `ksum.kara` ★ | a heap: from the smallest size, a `PriorityQueue` of (sum, last place) hands each sum on to two, the next size added or swapped in for the last; the (k-1)-th popped is the loss. O(n log n + k log k) |
| `ksum_merge.kara` | merged lists: the `k` smallest sums kept sorted, each size merging them with themselves plus it, cut at `k`, until a size no smaller than the `k`th. O(n log n + n k) |
| `ksum_search.kara` | binary search: the least bound with at least `k` sets summing within it, the sets counted by a walk over the sorted sizes that stops at a size too big and at `k`. O(n log n + k log(sum)) |
| `ksum_set.kara` | the ★ arm's walk with a `SortedSet` popped from its first in place of the heap, each entry carrying a serial number, since two sets can share a sum and a last place |
| `ksum_iter.kara` | iterators: the largest sum by `filter` and `sum`, the sizes by `map`; a `fold` over the sizes keeps the `k` smallest sums, each size's sums `chain`ed on, sorted and cut at `k` |
| `ksum_solution.kara` | LeetCode's Rust template: a `BinaryHeap` of `Reverse((i64, usize))`, the sizes by `sort_unstable`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one value
each way, for both its sums; all four sums of two values; then `10^5`
random values from `-10^9` to `10^9` for `k = 2000`, and `10^5` 0s for
`k = 2000`; then 3000 random arrays of 1 to 12 values for a random `k`
up to `2^n`, with a checksum and the sum of the answers. `ksum.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 3000 random arrays of up to 10 values against every
subsequence's sum, sorted.

The iter arm's `best.iter().chain(best.iter().map(|s| s + a))` was
refused, as Rust refuses it, for chaining `ref i64` items onto `i64`
ones; `check` names the cure and `karac fix` writes
`best.iter().cloned().chain(..)`.

`check` first reports 13 errors on the template, and `karac fix` carries
it in one round, reporting 26 edits: the two `use` lines deleted,
`struct Solution;` given its braces, `Vec<..>` its brackets,
`Vec::with_capacity` and `Solution::` written with a dot, `for &x in
&nums` written `for x in ref nums`, the `as i64` of `total += x as i64`
dropped as a cast that widens anyway, `sort_unstable` written `sort`,
`BinaryHeap::new()` written `PriorityQueue.new()` and every `Reverse(..)`
taken off, since Kāra's queue pops its smallest first, the `0usize` and
`0i64` suffixes dropped, and the `&` of the wrapper's `|&v|` dropped.
The `(x as i64).abs()` and the `as i32` casts stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the sum of every one of the `2^n` subsequences, sorted from
the largest, and the `k`th taken. No sizes and no heap. It checks 300
random arrays of 1 to 12 values from `-top` to `top`, `top` one of 2,
10, 1000 and `10^9`, which the literal reading answers; then 30 of up to
2000 values from `-10^9` to `10^9`; then 30 of up to 2000 values from -2
to 2, where sums tie by the thousand. Each asks for a random `k` up to
`2^n` and 2000, the long ones up to 500, and all 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | up to 12 values, the answer is the literal reading's |
| P2 | at most the largest sum and at least the smallest, and the largest exactly when `k` is 1 |
| P3 | the values reversed: the same answer |
| P4 | every value negated: the answer less the sum of all the values |
| P5 | `k` one more, while there are that many: the answer or smaller |
| P6 | each arm agrees with at least three of the other five |

P4 holds because a subsequence and the rest of the array sum to the
whole, so the `k`th largest sum of the negated values is the negated
`k`th smallest, which is the whole less the `k`th largest.

The differential prints `360 cases: checksum 595254387, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and sums every subsequence. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the negatives counted in the largest | P1 282, P2 175, P4 349, P6 342 |
| M2 | ★: the sizes not sorted | P1 152, P3 227, P5 75, P6 211 |
| M3 | ★: the swap taking out the smallest size | P1 215, P6 245 |
| M7 | merge: the stop at twice the size | P1 49, P5 2, P6 79 |
| M8 | merge: each size added twice | P1 271, P2 144, P5 91, P6 301 |
| M9 | merge: the empty set left out | P1 223, P2 51, P6 253 |
| M12 | search: the empty set not counted | P1 273, P2 26, P6 333 |
| M13 | search: a size that fits exactly left out | P1 247, P6 307 |
| M14 | search: the bound searched from 1 | P1 29, P2 27, P6 59 |
| M18 | set: the swap leaving the sum as it was | P1 227, P6 257 |
| M19 | set: the queue popped from its last | P1 229, P5 136, P6 276 |
| M21 | set: each positive counted as one | P1 218, P2 85, P4 338, P6 277 |
| M22 | iter: the largest summing the sizes | P1 282, P2 215, P4 349, P6 342 |
| M24 | iter: the largest sums kept | P1 261, P5 149, P6 291 |
| M26 | iter: each size added twice | P1 271, P2 133, P6 301 |
| M28 | solution: one sum too few popped | P1 156, P6 186 |
| M31 | solution: the swap dropping the next size | P1 236, P2 112, P5 142, P6 266 |

P1 and P6 kill all seventeen, P2 nine, P5 six, P4 three and P3 one.
P3, the values reversed, fails only the ★ arm's sizes not sorted (M2):
every other edit leaves the sort in place, so no other arm sees the
input's order. P4, every value negated, fails the edits that misjudge
the largest sum by the values' signs: the negatives counted in it (M1),
the sizes summed for it (M22) and each positive counted as one (M21).
P5, `k` one more, fails the edits whose answers for neighbouring `k`
come out of order, as the sizes not sorted (M2), the stop at twice the
size (M7), a size added twice (M8), the queue popped from its last
(M19), the largest sums kept (M24) and the swap dropping the next size
(M31).

Of the thirty-one, fourteen were not kept. The template's sizes left
unsorted fails exactly as the ★ arm's (M27, M2), its total counting
negatives as the ★ arm's negatives counted in the largest (M29, M1),
and its size its value as the ★ arm's negative value its own size
(M30, M6); the merge and iter arms' stop as soon as `k` are kept fail
alike (M10, M25). The iter arm's sizes not sorted (M23) is equivalent:
the sort only lets the fold stop early, and every size is still merged
into the `k` smallest sums. The set arm's serial never advanced (M17)
makes equal sums one entry, and the queue runs dry and the arm panics,
which is a crash. The ★ arm's first sum popped kept and next size added
twice (M4, M5), the merge arm's sizes from the largest (M11), the search
arm's size after its last skipped and room never used up (M15, M16) and
the set arm's queue started from nothing (M20) each fail apart from
every kept one, and were left out to keep three to an arm and two to
the template.

## Verification

Every arm prints the same output as `ksum.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 3.1 to 8.3 s, but the ★ arm 18.9 s
and the template 17.8 s: both push and pop a `PriorityQueue` of tuples,
which the interpreter runs slowest, for `k = 2000` over the `10^5`
values. The differential takes 32.2 s there and 0.75 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values from `-10^9` to `10^9` once
from the harness's generator, then makes 60 passes, pass `p` asking
array `a` for `k = 2000 - (7p + a) % 100` and folding each answer plus
the pass into the checksum, with the ★ arm in all five languages. Every
implementation prints `60 passes over 10 arrays of 10^5 values:
checksum 988388582`. The time goes mostly to sorting the sizes, afresh
in each call; C's sort is the library's `qsort`, which calls its
comparison through a pointer, and Go's `sort.Slice` through a closure.

BENCHTAB
