# 2530. Maximal Score After Applying K Operations

You are given a **0-indexed** integer array `nums` and an integer `k`.
You have a **starting score** of `0`.

In one **operation**:

1. choose an index `i` such that `0 <= i < nums.length`,
2. increase your **score** by `nums[i]`, and
3. replace `nums[i]` with `ceil(nums[i] / 3)`.

Return *the maximum possible **score** you can attain after applying
**exactly*** `k` *operations*.

The ceiling function `ceil(val)` is the least integer greater than or
equal to `val`.

```
nums = [10, 10, 10, 10, 10], k = 5  ->  50
nums = [1, 10, 3, 3, 3], k = 3      ->  17
```

**Constraints:** `1 <= nums.length, k <= 10^5`; `1 <= nums[i] <= 10^9`.

Taking the largest number each time is best: a number's later values
are never larger than it, so any other choice can be exchanged for it
without lowering the score. The approaches differ in how they keep the
largest at hand. The score reaches about `1.5 * 10^14`, an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `score.kara` ★ | a max-first `PriorityQueue`: `k` times the largest popped, added, and its third rounded up, `(top + 2) / 3`, pushed back. O((n + k) log n) |
| `score_counts.kara` | a `SortedMap` from each value to how many numbers hold it: each step takes the largest key, one of its copies, and adds a copy of its third. Equal numbers are one entry |
| `score_queues.kara` | no heap: the numbers sorted largest first, and a `VecDeque` of the thirds made so far, which come out largest first too, since each number taken is no larger than the one before; each step takes the larger front. O(n log n + k) |
| `score_rec.kara` | recursion: one operation, then a recursion for the other `k - 1`, the queue passed down; up to `10^5` deep |
| `score_iter.kara` | iterators: the queue `collect`ed from the numbers, and the score a `map` over `0..k` that pops and pushes, `sum`med |
| `score_solution.kara` | LeetCode's Rust template: `Vec<i32>` and an `i32` in, `i64` out; a `BinaryHeap` from `into_iter().collect()` and an `i64` score; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and six
more, among them a single 1 with `k = 10^5`, a single `10^9` with
`k = 25`, and ties; then 2000 random lists of 1 to 20 numbers to 30
with `k` up to 30 and 200 of 1 to 1000 to `10^9` with `k` up to 2000,
as the sum of the answers and a checksum; then the constraints'
largest, `10^5` numbers to `10^9` and `k = 10^5`. `score.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
on 3000 random lists of 1 to 8 numbers to 50 with `k` up to 15 against
the operations applied one by one to the first largest number, and the
two agreed on every list.

`check` reported errors on four of the five Kāra arms as first written.
The ★, rec and iter arms used Rust's `BinaryHeap`, which pops the
largest first; Kāra's is `PriorityQueue`, which pops the smallest first
unless built with `max_first`, and `check` said so. `karac fix` wrote
`PriorityQueue.max_first()` for `BinaryHeap.new()` and
`PriorityQueue.max_first_from(..)` around the two `collect`s, and the
types to match: 2 edits on the ★ arm, 3 on the rec arm, 2 on the iter
arm. The counts arm bound `let (top, many) = counts.last().unwrap();`
and then removed `top` from the map. The two bindings are references
into the map, which a plain `let` keeps (core-semantics.md §1.1), so the
removal was refused as a write while `top` held a borrow of it. That is
the rule. With the annotation the rule offers, `let (top, many): (i64,
i64) = ..`, the two read as `i64`s (§5.10), and `check` accepted the
types but still refused the removal: the tuple pattern bound the
references even so, where `let pair: (i64, i64) = ..` did not
(B-2026-11-23-69). The annotated form is now accepted, and is the one the arm
uses. The queues arm checked clean.

`check` first reports 6 errors on the template: the line `use
std::collections::BinaryHeap;`, the unit struct `struct Solution;`,
Rust's `Vec<i32>` and `BinaryHeap<i32>`, the path call
`Solution::max_kelements`, and the `&x` closure pattern. `karac fix`
carries it in one call, reporting 12 edits: besides those, the heap
made a max-first `PriorityQueue` from the collected numbers, the
parameter the `into_iter` consumes marked `own`, and the casts an `i32`
widens through by itself dropped. LeetCode's own `div_ceil` is
unstable on `i32` in Rust, so the template rounds up with `(top + 2) /
3`, as the Kāra arms do.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: `k` times the list is walked for its first largest number,
which is added to the score and replaced by its third rounded up, the
ceiling taken by whether 3 divides it. It checks 300 random lists of 1
to 10 numbers from 1 to 30 with `k` from 1 to 20, and 60 of 1 to 10
from 1 to `10^9` with `k` from 1 to 40. All 360 are drawn before any
arm answers, and in 107 of them the next operation would add only 1.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least `k` and at most `k` times the largest number |
| P3 | the list reversed: the same answer |
| P4 | `k` one more: the answer grows by at least 1 and by at most the largest number |
| P5 | a 1 appended: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 107 with a next step of 1: checksum
725097608, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against
a Python reading that builds the same lists and applies the operations
one by one. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the third rounded down | P1 273, P2 6, P4 98, P5 86, P6 273 |
| M3 | ★: each step scored one short | P1 360, P2 8, P4 107, P6 360 |
| M6 | ★: the first number counted twice | P1 283, P3 280, P6 283 |
| M8 | counts: a key kept at a count of 0 | P1 339, P6 339 |
| M9 | counts: a third counted once however many | P1 173, P6 173 |
| M10 | counts: repeated numbers counted once | P1 89, P6 89 |
| M13 | queues: each third put at the front | P1 254, P6 254 |
| M14 | queues: the sorted number against the smallest third | P1 120, P5 65, P6 120 |
| M15 | queues: the list left in its order | P1 240, P3 245, P5 32, P6 240 |
| M19 | rec: the base case worth 1 | P1 360, P2 21, P6 360 |
| M20 | rec: the smallest number taken first | P1 328, P5 286, P6 328 |
| M21 | rec: the third one too many | P1 291, P2 1, P4 1, P6 291 |
| M23 | iter: an odd number scored one short | P1 333, P2 6, P4 107, P6 333 |
| M24 | iter: the number halved | P1 306, P6 306 |
| M26 | iter: one operation too many | P1 360, P2 44, P6 360 |
| M28 | solution: the number quartered | P1 290, P2 6, P4 89, P5 80, P6 290 |
| M29 | solution: the score the last number only | P1 342, P2 204, P4 360, P6 342 |

P1 and P6 kill all seventeen, P2 eight, P4 six, P5 five and P3 two:
the ★ arm's first number counted twice (M6) and the queues arm's
list left in its order (M15) are the two that only a reordering finds.

Fourteen are not kept. Five fail exactly as a kept one does: the ★,
counts and iter arms' smallest number taken first (M2, M7, M25) as the
rec arm's (M20), the queues arm's thirds taken from the back (M16) as its
thirds put at the front (M13), and the rec arm's number put back whole
(M18) as the counts arm's key kept at a count of 0 (M8). The other nine
are killed but give a fourth to an arm that has its three: one operation
fewer in the ★, rec, iter and template arms (M4, M17, M22, M27) and the template's `k` read one
short (M31), which all fail as `P1 360, P2 19, P6 360`; the ★ arm's third
rounded from a remainder of 2 only (M5); the counts arm's third rounded
up from a multiple of 3 (M11); the queues arm's sorted list ascending
(M12); and the template's odd number put back one more (M30).

## Verification

Every arm prints the same output as `score.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 to 28.4 s and the differential 1.3 s; under `karac __mir-llvm-asan` the arms take 0.5 to 1.5 s and the differential 0.6 s; and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds `10^5` random numbers from 1 to `10^9` once from its
own generator, then makes 170 passes. Each pass asks for the score with
`k = 5 * 10^4 + check % (5 * 10^4 + 1)`, and folds it, reduced, plus
the pass into the checksum. The bench uses the ★ arm in all five
languages: the Rust mirror uses `BinaryHeap`, the C mirror an array
heap of its own, and the Go mirror `container/heap`, whose calls go
through an interface and box each value. Every implementation prints
`170 passes over 100000 numbers: checksum 495290402`.

BENCHTAB
