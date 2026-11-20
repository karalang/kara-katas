# 2389. Longest Subsequence With Limited Sum

You are given an integer array `nums` of length `n`, and an integer
array `queries` of length `m`.

Return *an array* `answer` *of length* `m` *where* `answer[i]` *is the
**maximum** size of a **subsequence** that you can take from* `nums`
*such that the **sum** of its elements is less than or equal to*
`queries[i]`.

A **subsequence** is an array that can be derived from another array by
deleting some or no elements without changing the order of the
remaining elements.

```
nums = [4,5,2,1], queries = [3,10,21]  ->  [2,3,4]
nums = [2,3,4,5], queries = [1]        ->  [0]
```

**Constraints:** `n == nums.length`; `m == queries.length`;
`1 <= n, m <= 1000`; `1 <= nums[i], queries[i] <= 10^6`.

Order does not matter to a sum, and the smallest values make the
longest subsequence for any limit: swapping a chosen value for a
smaller one never breaks the limit. So the answer is how many of the
sorted values' running sums are within it.

## Approaches

| file | mechanism |
|---|---|
| `limited.kara` ★ | the values sorted into prefix sums; each query's answer how many are within it, by binary search. O((n + m) log n) |
| `limited_greedy.kara` | query by query, the sorted values taken from the smallest while they still fit. O(n log n + n m) |
| `limited_offline.kara` | offline, two pointers: the queries' places sorted by their limits, one running sum walked forward as the limits grow. O(n log n + m log m) |
| `limited_drop.kara` | dropping the largest: each query starts from every value in a `PriorityQueue` that pops the largest first, and drops until the rest fit. O(m n log n) |
| `limited_iter.kara` | iterators: the running sums by `scan`, each query's count by `take_while` and `count`, `map`ped over the queries |
| `limited_solution.kara` | LeetCode's Rust template: `mut nums` sorted and summed in place, each query by `partition_point`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; a query of
0, one of everything and one past it; four equal values, each limit
around a multiple; then 1000 values up to `10^6` with 1000 queries up
to `10^9`, as a checksum; then 3000 random arrays of 1 to 30 values up
to 1 to 100, with 1 to 10 queries up to the sum and a little more, with
a checksum and the total length. `limited.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked on 3000 random
arrays of up to 10 values against every subsequence.

`check` first reports 16 errors on the template, and `karac fix` carries
it in one call, reporting 25 edits: `struct Solution;` given its
braces; `Vec<..>` its brackets; the parameter `mut nums: Vec<i32>`
written as Kāra writes an owned parameter it will change, `nums: own
Vec[i32]` with `let mut nums = nums;` at the top; the `&` of every
`|&q|`, `|&p|` and `|&v|` dropped; and `Solution::` written with a
dot. `partition_point`, the `as i32` and `as i64` casts and the sums in
place stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each query, every one of the `2^n` subsequences summed,
and the longest within the limit kept. No sorting. It checks 300 random
arrays of 1 to 12 values up to 1 to 20, which the literal reading
answers; then 30 of up to 500 values up to `10^6`; then 30 of up to 500
values from 1 to 3, where the values tie. Each has 1 to 20 queries up
to its sum and a little more, and all 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | up to 12 values, the answers are the literal reading's |
| P2 | each answer `a`: the `a` smallest values fit the limit, and one more does not |
| P3 | the values reversed: the same answers |
| P4 | the queries reversed: the answers reversed |
| P5 | every value and every limit doubled: the same answers |
| P6 | each arm agrees with at least three of the other five |

P2 is the greedy argument as a check on each answer, worked out from a
sorted copy in the harness. P3 holds because a sum does not see order,
P4 because each query is answered alone, and P5 because doubling both
sides of every comparison changes none of them.

The differential prints `360 cases: checksum 580718218, 12960 checks
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
| M1 | ★: the values unsorted | P1 219, P2 278, P3 291, P6 278 |
| M4 | ★: the search one short at the top | P1 215, P2 219, P6 219 |
| M5 | ★: the prefix sums from the second value | P1 292, P2 351, P6 351 |
| M7 | greedy: a value equal to the room refused | P1 206, P2 236, P6 236 |
| M10 | greedy: the count from one | P1 301, P2 360, P6 360 |
| M11 | greedy: the room one larger | P1 215, P2 244, P5 244, P6 244 |
| M12 | offline: the queries in their own order | P1 268, P2 322, P4 311, P6 322 |
| M14 | offline: the used sum never added | P1 264, P2 323, P6 323 |
| M16 | offline: the queries from the largest | P1 282, P2 337, P6 337 |
| M19 | drop: a dropped value counted twice | P1 258, P2 317, P6 317 |
| M20 | drop: the queue built only once | P1 271, P2 326, P4 319, P6 326 |
| M21 | drop: the answer the dropped count | P1 300, P2 359, P6 359 |
| M23 | iter: each limit read as twice itself | P1 282, P2 341, P6 341 |
| M25 | iter: the answers in the queries' reverse order | P1 277, P2 332, P6 332 |
| M26 | iter: the first sum skipped | P1 299, P2 358, P6 358 |
| M28 | solution: the sums from the third value | P1 216, P2 249, P6 249 |
| M30 | solution: each sum the first value plus its own | P1 242, P2 301, P6 301 |

P1, P2 and P6 kill all seventeen, P4 two, P3 one and P5 one. P3, the
values reversed, fails only the values unsorted (M1): every other edit
leaves the sort in place. P4, the queries reversed, fails the two edits
that carry something from one query to the next, the queries taken in
their own order by the offline arm (M12) and the queue built only once
by the drop arm (M20). P5, everything doubled, fails only the room one
larger (M11), a slack of one that doubling does not double.

Of the thirty-one, fourteen were not kept, and twelve of them fail
exactly as a kept one. The values unsorted in the greedy, offline, iter
and template arms (M9, M15, M24, M27) fail as the ★ arm's (M1); a sum
equal to the limit refused in the ★, offline and template arms (M2,
M13, M29) as the greedy arm's value equal to the room refused (M7);
each prefix sum its own value in the ★ arm, the room never used up in
the greedy arm and the scan never carrying in the iter arm (M3, M8,
M22) as the offline arm's used sum never added (M14); and the drop
arm's total one short and the template's limit one larger (M18, M31) as
the greedy arm's room one larger (M11). The ★ arm's values from the
largest and the drop arm's smallest dropped first (M6, M17) fail alike,
and apart from every kept one; neither arm had room for it. Two
edits first made to the iter arm, a sum equal to the limit refused and
the running sums from 1, also failed as M7 did, and were replaced by
the two kept there (M23, M25).

## Verification

Every arm prints the same output as `limited.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 1.3 s, but the drop arm
7.6 s: it builds a `PriorityQueue` of every value for each query. The
differential takes 11.3 s there and 0.63 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 100 arrays of 1000 values up to `10^6`, each with 1000
queries up to `10^9`, once from the harness's generator, then makes 200
passes, answering every array's queries and folding each answer plus
the pass into the checksum, with the ★ arm in all five languages. Every
implementation prints `200 passes over 100 arrays of 1000 values and
1000 queries: checksum 438786587`. Every implementation sorts a fresh
copy of the values and allocates its answers in each call; C's sort is
the library's `qsort`, which calls its comparison through a pointer.

BENCHTAB
