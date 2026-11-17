# 2233. Maximum Product After K Increments

You are given an array of non-negative integers `nums` and an integer
`k`. In one operation, you may choose **any** element from `nums` and
**increment** it by `1`.

Return *the **maximum** **product** of* `nums` *after **at most*** `k`
*operations.* Since the answer may be very large, return it **modulo**
`10^9 + 7`. Note that you should maximize the product before taking the
modulo.

```
nums = [0, 4],        k = 5  ->  20     (5 * 4)
nums = [6, 3, 3, 2],  k = 2  ->  216    (6 * 4 * 3 * 3)
```

**Constraints:** `1 <= nums.length, k <= 10^5`; `0 <= nums[i] <= 10^6`.

Each increment goes to the smallest number: raising `x` by one
multiplies the product by `(x + 1) / x`, which is largest for the
smallest `x`, and an increment never lowers the product, so all `k` are
used. A min-first `PriorityQueue` hands them out, and the product is
taken modulo `10^9 + 7` as the queue empties. O((n + k) log n).

## Approaches

| file | mechanism |
|---|---|
| `product.kara` ★ | a min-first `PriorityQueue`, its smallest popped and pushed back one higher `k` times, then emptied with `while let Some(x) = queue.pop()` into the product |
| `product_sorted.kara` | the numbers sorted, the smallest `i` filled up level by level to the next number's value while the increments last, the rest spread evenly over those `i`, `k / i` each and one more for `k % i` of them |
| `product_buckets.kara` | a count per value in a `Vec.filled` of `largest + k + 2`, walked up from 0 moving as many numbers up one value as the increments allow, the product each value to its count by a fast `power` |
| `product_struct.kara` | a `struct Increments` holding the queue, with `raise_smallest` and `product` (`mut ref self`) |
| `product_iter.kara` | the level the smallest numbers reach found by a binary search, the largest `m` whose cost (a closure `cost`, the `sum` of `(m - x).max(0)`) is at most `k`; every number raised to it with `map`, the spare increments lifting that many numbers at the level by one more inside a `fold` that takes the product |
| `product_solution.kara` | LeetCode's Rust template: a `BinaryHeap<Reverse<i64>>` `collect`ed from `nums.into_iter().map(\|x\| Reverse(x as i64))`, each increment `let Reverse(x) = heap.pop().unwrap()` and `heap.push(Reverse(x + 1))`, the product a `fold` over `heap.into_iter()` with the pattern `\|acc, Reverse(x)\|`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and five
more (one zero and one increment, two zeros and one increment, enough
increments to level everything, a product past the modulus, and all
numbers equal), each with its answer; then a checksum of 3000 random
cases of 1 to 20 numbers of up to 10, 1000 and 10^6 in turn with `k`
from 1 to 100; then the constraints' largest, 10^5 numbers of up to
10^6 with `k = 10^5`, and 10^5 numbers of up to 10, where the
increments level them. `product.py` mirrors the ★ arm and its output
is byte-identical.

`karac fix` carries the template in one round of 21 edits:
`use std::cmp::Reverse` to `import std.cmp.Reverse`, the
`use std::collections::BinaryHeap` deleted, `Vec<i32>` to `Vec[i32]`,
the `BinaryHeap<Reverse<i64>>` built by `collect` to a
`PriorityQueue[Reverse[i64]]` built by `PriorityQueue.max_first_from`
(Rust's heap is max-first, so with `Reverse` it pops the smallest, as
here), every `Reverse(x)` constructor and pattern, the closure's
included, to `Reverse { value: x }`, and `struct Solution;` to `struct
Solution {}`. Kāra's `Reverse` is a struct with one field, `value`.
Since a bare parameter borrows, `nums.into_iter()` became
`nums.clone().into_iter()`. The fix also dropped the `i64` suffixes of
`1_000_000_007i64` and the fold's `1i64`, which `x` types anyway, and
the adapter's `as i64` on an `i32` result, a lossless cast.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way of sharing the `k` increments among the numbers
tried, recursively, each product taken, and the largest; no heap and no
levelling. The cases are small enough that no product reaches
`10^9 + 7`, so the remainder is the product itself. It checks 300
random cases of 1 to 4 numbers of up to 6 with `k` from 1 to 6; then 30
of 5 numbers of up to 10 with `k` from 1 to 8; then 30 of zeros only
with `k` from 1 to 5, where too few increments leave a zero. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the largest product, read literally |
| P2 | the answer is at least the product with all `k` increments given to one smallest number, and below `10^9 + 7` |
| P3 | the numbers reversed: the same answer |
| P4 | one increment more: no smaller answer |
| P5 | a 1 appended to the numbers: no smaller answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 924758571, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that tries
every assignment of each increment to a number (`itertools.product`)
and takes the largest product. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-three edits to the differential, six to the ★ arm, five to
each of the sorted, buckets and iter arms and the template, and seven
to the struct arm, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the smallest raised by two | P1 349, P6 349 |
| M3 | ★: a max-first queue, the largest raised | P1 262, P2 222, P5 13, P6 262 |
| M5 | ★: zeros multiplied in as 1 | P1 11, P6 11 |
| M6 | sorted: each level charged one increment, not one per number | P1 45, P5 5, P6 45 |
| M7 | sorted: one remainder increment too many | P1 354, P6 354 |
| M8 | sorted: never sorted | P1 76, P2 7, P3 92, P6 76 |
| M10 | buckets: the power's odd steps skipped | P1 341, P2 315, P4 94, P5 96, P6 341 |
| M11 | buckets: only one number moved up per bucket, the count still charged | P1 142, P2 135, P4 61, P5 137, P6 142 |
| M12 | buckets: one number taken per bucket | P1 165, P6 165 |
| M15 | struct: the smallest pushed back unraised | P1 349, P2 319, P6 349 |
| M18 | struct: a sum, not a product | P1 356, P2 214, P6 356 |
| M32 | struct: a zero raised by two | P1 116, P6 116 |
| M20 | iter: the level at most one above the smallest | P1 201, P2 187, P6 201 |
| M22 | iter: every number at the level lifted, spare or not | P1 360, P5 11, P6 360 |
| M23 | iter: numbers above the level counted at a negative cost | P1 153, P6 153 |
| M28 | solution: one increment fewer | P1 349, P2 267, P6 349 |
| M29 | solution: each number multiplied in one higher | P1 360, P6 360 |

P1 and P6 kill all seventeen, P2 eight, P5 five, P4 two and P3 one.
P2's floor, all `k` given to one smallest number, is a real answer of
the problem, so it catches the edits that waste increments or lose
them (M15, M28) or give them to the largest (M3), but not those that
hand out too many. P3 catches only the sorted arm left unsorted (M8),
the one arm whose answer depends on the order of its input. P4 and P5
catch the edits whose error grows with `k` or with the length, the
buckets arm's broken power and moves (M10, M11), and the levelling
edits that leave a number behind (M3, M6, M22).

Of the thirty-three, sixteen were not kept. One survives and is
equivalent: the iter arm's search taking the level only when its cost
is below `k` (M21), since when the cost is exactly `k` the search stops
one level lower and the spare increments are exactly enough to lift
every number at that level to the next. Three crash: the buckets arm's
counts sized to the largest number only (M14, index out of bounds), and
the ★ and struct arms leaving the first number out of the queue (M31,
M16), which empties the queue under a one-number case and unwraps a
`None`. None differs between the backends. Eight fail as a kept one
does: one increment fewer in the ★ and struct arms and the template's
`k` passed one less (M1, M17, M30) as the template's own (M28); the ★
arm's product from 0 (M4) as the struct arm's unraised push (M15); the
buckets arm's zeros skipped (M13) as the ★ arm's zeros as 1 (M5); the
struct arm's and the template's largest raised (M19, M27) as the ★
arm's (M3); and the template's raise by two (M26) as the ★ arm's (M2).
Four fail their own way and are left out for the count of three: the
sorted arm's level from 0 (M9), the iter arm's numbers below the level
kept one under it and its spare increments dropped (M24, M25), and the
struct arm's zeros held as 1 (M33).

## Verification

Every arm prints the same output as `product.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the sorted arm takes 0.7 s, the iter arm 3.8 s,
the ★, struct and template arms about 10 s, and the differential 0.5 s.
The buckets arm takes 127 s: it fills and walks a count for every value
up to the largest number, and a thousand of the random cases have
numbers up to 10^6, so it runs over 10^9 bucket steps; compiled it takes
1.4 s.

## Benchmarks

The bench draws 20000 numbers of up to 10^6 once, then makes 150 passes,
one number drawn again before each, each pass the ★ arm with
`k = 50000`. Rust uses `BinaryHeap<Reverse<i64>>`, Python `heapq`, and
C and Go a binary min-heap written out in an array. Every
implementation prints `150 passes over 20000 numbers, k = 50000:
checksum 546170942`.

BENCHTAB
