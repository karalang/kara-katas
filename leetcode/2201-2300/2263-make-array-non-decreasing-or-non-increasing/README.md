# 2263. Make Array Non-decreasing or Non-increasing

You are given a **0-indexed** integer array `nums`. In one operation,
you can choose an index `i` such that `0 <= i < nums.length` and set
`nums[i]` to `nums[i] + 1` or `nums[i] - 1`.

Return *the **minimum** number of operations to make* `nums`
***non-decreasing** or **non-increasing**.*

```
nums = [3,2,4,5,0]  ->  4
nums = [2,2,3,4]    ->  0
nums = [0]          ->  0
```

**Constraints:** `1 <= nums.length <= 1000`; `0 <= nums[i] <= 1000`.

The cost of a target array is the sum of the distances to it, so this
is L1 isotonic regression, once rising and once falling. Some best
target uses only values that are already in the array, which gives an
O(n * distinct) dynamic program over those values. The slope trick does
it in O(n log n): a max-heap holds the values the target is pinned to,
and a value below the largest of them pays the difference and pulls
that one down to it.

## Approaches

| file | mechanism |
|---|---|
| `convert.kara` ★ | the slope trick on a `PriorityQueue.max_first()`: each value pushed, and when the top is larger, the difference paid, the top popped and the value pushed again; the same over the reversed array, the smaller cost |
| `convert_dp.kara` | costs per candidate value, the sorted distinct values: after each element `up[j]` is its distance to the j-th plus the least `up` at or below it, a running minimum; `down` the same from the top |
| `convert_sorted.kara` | the slope trick without a heap: the pinned values in a sorted `Vec`, each inserted at the place a binary search finds, the last taken off by `pop` |
| `convert_struct.kara` | `struct Slope` of the heap and the cost; `feed` (`mut ref self`) takes one value; one `Slope` is fed the values and the other their negations, a falling array negated being a rising one |
| `convert_iter.kara` | the dp arm in chains: a `fold` over the array whose state is the costs per candidate, each step a `scan` along the candidates carrying the running minimum as Kāra's `Some((next_state, item))`; run over the candidates rising and falling |
| `convert_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; a closure `cost` runs the slope trick on a `BinaryHeap` and is called on the array and a reversed copy; carried by `karac fix` but for one annotation |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (already non-increasing, 0; one out of place, 1; a zig-zag of 0
and 1000, 2000; a valley, 12), each with its cost; then 2000 arrays of
1 to 30 values from 0 to 3, 10, 100 or 1000, with a checksum; then
three of the constraints' longest, 1000 values: random from 0 to 1000
(253572), a zig-zag of 0 and 1000 (499000), and 1000 down to 1 with
every tenth raised to 1000 (50300). `convert.py` mirrors the ★ arm and
its output is byte-identical.

`karac fix` carries the template in one round, reporting 15 edits: the `use
std::collections::BinaryHeap;` line deleted, `Vec<i32>` to `Vec[i32]`
twice, `&Vec` to `ref Vec`, the closure's `-> i32` deleted,
`BinaryHeap::new()` to `PriorityQueue.max_first()`, the patterns
`&x` and `Some(&t)` to `x` and `Some(t)` with `.cloned()` on the
`peek()`, the `&` dropped from both calls of `cost`, and `struct
Solution;` to `struct Solution {}`.

One error is left with no fix. Rust infers `ans` as an `i32` from
`ans += t - x`, which the deleted `-> i32` also said. In Kāra a
literal keeps the default `i64` unless its binding is declared
(design.md §8 Literals), so the closure returns an `i64`, and the
error lands on `cost(nums).min(cost(r))`, the template's `i32` tail,
as a bare narrowing with no word of `ans`. The same `ans` in a
function's own tail gets the explanation and the fix `ans: i32`
(B-2026-11-18-80). The arm writes `let mut ans: i32 = 0;`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every non-decreasing and every non-increasing target array
whose values lie from 0 to the largest value, built a position at a
time, the cost of each the sum of its distances, the least kept. No
heap, no candidate values from the array. It checks 300 random arrays
of 1 to 7 values from 0 to 1, 2, 3 or 5; then 30 already sorted, half
rising and half falling; then 30 of one value with one position
changed. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the cost is the literal reading's |
| P2 | the array reversed: the same cost |
| P3 | every value `v` made `10 - v`: the same cost |
| P4 | 1000 added to every value: the same cost |
| P5 | no more than the cost of making every value the median, and 0 exactly when the array is already sorted one way or the other |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 each swap the two directions, so an arm that gets one
direction wrong fails both.

The differential prints `360 cases: checksum 620966659, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that tries
every array in `product(range(max + 1), repeat = n)` that is sorted one
way or the other. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the top never popped | P1 59, P3 106, P5 24, P6 59 |
| M3 | ★: only the non-decreasing cost | P1 113, P2 220, P3 220, P5 59, P6 113 |
| M5 | ★: the larger of the two directions | P1 220, P5 110, P6 220 |
| M7 | dp: the running minimum not taken | P1 107, P2 220, P3 220, P5 51, P6 107 |
| M8 | dp: the falling table read rising | P1 178, P2 75, P3 98, P5 122, P6 178 |
| M9 | dp: the distance squared | P1 25, P2 41, P3 41, P6 25 |
| M12 | sorted: the value put at the front | P1 135, P3 142, P5 94, P6 135 |
| M14 | sorted: the value not put back | P1 4, P3 6, P6 4 |
| M16 | sorted: each pull costing one more | P1 178, P3 4, P5 72, P6 178 |
| M19 | struct: the cost counted twice | P1 178, P5 102, P6 178 |
| M20 | struct: the top kept | P1 49, P2 86, P5 8, P6 49 |
| M21 | struct: every value pushed twice | P1 49, P2 83, P5 5, P6 49 |
| M22 | iter: the scan's minimum not carried | P1 67, P2 52, P5 23, P6 67 |
| M23 | iter: the scan seeded at 0 | P1 178, P5 178, P6 178 |
| M25 | iter: the answer at the last candidate | P1 16, P2 40, P5 2, P6 16 |
| M29 | solution: the cost as the top | P1 90, P3 178, P4 178, P5 41, P6 90 |
| M31 | solution: the test reversed | P1 288, P3 143, P5 288, P6 288 |

P1 and P6 kill all seventeen, P5 fifteen, P3 ten, P2 eight, and P4
one. P5 catches anything that charges an array already sorted, or
charges more than flattening it would; the two it misses, the distance
squared and the value not put back, only undercharge. P4 catches only
the template's cost taken as the top itself, the one edit whose answer
depends on the values rather than their differences. M14 shows how
little the second push matters: a value that pulls the top down and is
pushed only once is wrong in only 4 of 360 cases.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Thirteen fail as a kept one does: one direction
only, by the array never reversed in the ★, sorted and template arms,
the struct arm's falling slope fed the values or its rising cost
alone, and the iter arm's rising candidates alone (M6, M15, M27, M17,
M18, M24), as M3; every answer 0, by the ★ arm's min-first heap, the
dp arm's minimum seeded at 0 and the sorted arm's first element as the
top (M4, M11, M13), as M23; the ★ arm's and the template's value
pushed once (M1, M28) as the sorted arm's not put back (M14); the iter
arm's distance doubled (M26) as the struct arm's cost counted twice
(M19); and the template's larger direction (M30) as the ★ arm's (M5).
One fails in a way of its own and is left out because its arm keeps
enough: the dp arm's answer at the last candidate (M10).

## Verification

Every arm prints the same output as `convert.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the sorted arm takes 0.4 s, the ★ and struct
arms 0.9 s, the template and the differential 1.1 s, the dp arm 3.4 s,
and the iter arm 16.5 s. The iter arm's `fold` builds a new `Vec` of
costs per element, about 4 * 10^6 candidate steps over the three long
arrays, each through a `zip` and a `scan`.

## Benchmarks

The bench answers 400 arrays of the constraints' longest, 1000 values
from 0 to 1000, with the ★ arm in all five languages. Every
implementation prints `400 arrays of 1000: checksum 256592874`. Rust
uses `BinaryHeap`, Go `container/heap`, Python `heapq` on negated
values, and C a binary max-heap in an array, reading the array
backwards for the second pass where the others reverse a copy.

BENCHTAB
