# 2208. Minimum Operations to Halve Array Sum

You are given an array `nums` of positive integers. In one operation, you
can choose **any** number from `nums` and reduce it to **exactly** half
the number. (Note that you may choose this reduced number in future
operations.)

Return *the **minimum** number of operations to reduce the sum of*
`nums` *by **at least** half.*

```
nums = [5, 19, 8, 1]  ->  3
nums = [3, 8, 20]     ->  3
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^7`.

Halving the largest number takes the most off the sum, and leaves the
others as they were, so greedily halving the largest until half the sum
is gone is optimal; a heap keeps the largest at hand. O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `halve.kara` ★ | a `PriorityQueue[Reverse[F64]]`, the largest popping first, each popped number halved and pushed back, until the halves taken reach half the `f64` sum |
| `halve_scaled.kara` | every number shifted left 20 places, so each half stays an exact integer, in a `PriorityQueue[Reverse[i64]]` |
| `halve_queues.kara` | no heap: the numbers sorted largest first, and each half sent to the back of a `VecDeque`; the halves come out no larger than the one before, so the largest left is at the front of one of the two |
| `halve_struct.kara` | a hand-written binary `MaxHeap` of `f64` over a `Vec`, sifting up on a push and down on a halving of its top, which never leaves the heap |
| `halve_iter.kara` | the scaled numbers `collect`ed into a `PriorityQueue[Reverse[i64]]`, the sum by `sum`, and the halvings counted by `take_while` over an endless `repeat` |
| `halve_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out, the numbers shifted left 20 places and `collect`ed into a `BinaryHeap<i64>`, the largest first; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and four
more (one number, two alike, one large among small ones, and both ends of
the range), each with its answer; then the most and a checksum for 2000
random arrays of 1 to 12 numbers up to 10, 1000 and 10^7 in turn; then
the constraints' largest, 10^5 numbers all 10^7, random up to 10^7, and
one 10^7 among ones. `halve.py` mirrors the ★ arm with `heapq` over
negated floats, and its output is byte-identical.

`karac fix` carries the template in three rounds of 7, 2 and 2 edits:
first the `use` dropped, `Vec<i32>` and `BinaryHeap<i64>` to brackets,
`|&x|` to `|x|`, `struct Solution;` to `struct Solution {}` and
`Solution::` to `Solution.`; then the heap, because Rust's `BinaryHeap`
pops the largest first and Kāra's `PriorityQueue` the smallest:
`BinaryHeap[i64]` to `PriorityQueue[i64]` and the `collect()` wrapped in
`PriorityQueue.max_first_from(..)`; then `0i64` to `0` and the adapter's
`as i64` on an `i32` result dropped. The iter arm wrote
`std.iter.repeat`, and the fix made it `repeat`.

The kata found three gaps in kara, all fixed:

- `B-2026-11-15-78`: the ★ arm's `PriorityQueue[Reverse[F64]]` was refused
  by the MIR builder, which had no lowering for `T.cmp` under `T: Ord`
  at `F64`, the total order Kāra gives floats.
- `B-2026-11-15-79`: `let Reverse { value: top } = heap.pop().unwrap();` over
  `i64` read `top` as moved after one use, since a field of a generic
  struct bound by a `let` pattern took the declared `T` rather than
  `i64`.
- `B-2026-11-15-80`: the template's `let mut heap: BinaryHeap<i64> =
  ...collect();` was renamed to a `PriorityQueue`, which pops the
  smallest first, so the fixed program halved the smallest number and
  printed wrong counts with no error. The fix now writes
  `PriorityQueue.max_first_from(..collect())`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for k = 1, 2, ... every way to share k halvings among the
numbers tried, each number's halvings worked exactly on the number
shifted left 20 places, until one way takes off half the sum; no heap,
no greed. It checks 300 random arrays of 1 to 8 numbers up to 10, 1000
and 10^7 in turn; then 30 of one number repeated; then 30 with one
number far above the rest. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | it is at least 1 and at most n, one halving of every number |
| P3 | the array reversed: the same count |
| P4 | every number doubled: the same count |
| P5 | the array followed by itself: no fewer, and at most twice as many |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 21301671, 12960 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers was checked against a Python breadth-first search
over the multisets of halved values in exact `Fraction`s. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-eight edits to the differential, six to the ★ arm, five to the
scaled arm and to the template arm, seven to the queues and struct arms,
and eight to the iter arm, each run under `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the sum counted at half | P1 302, P6 302 |
| M3 | ★: a halved number dropped from the heap | P1 122, P6 122 |
| M5 | ★: the count starting at 1 | P1 360, P2 238, P6 360 |
| M8 | scaled: more than half wanted | P1 133, P2 123, P6 133 |
| M10 | scaled: the number pushed back at a quarter | P1 89, P6 89 |
| M11 | scaled: the first number left out | P1 300, P2 58, P3 46, P5 210, P6 300 |
| M16 | queues: a halving counted as a third | P1 360, P2 338, P5 32, P6 360 |
| M32 | queues: the total without the largest number | P1 360, P2 58, P5 290, P6 360 |
| M33 | queues: a half weighed against the sorted number after next | P1 46, P2 11, P5 39, P6 46 |
| M19 | struct: two counted per halving | P1 360, P2 339, P6 360 |
| M21 | struct: a push never compared with the root | P1 17, P3 14, P6 17 |
| M35 | struct: every number pushed twice | P1 177, P6 177 |
| M24 | iter: the whole number pushed back | P1 184, P6 184 |
| M36 | iter: the total of the numbers above 5 only | P1 93, P2 20, P4 72, P6 93 |
| M37 | iter: the count one short | P1 360, P2 58, P5 224, P6 360 |
| M30 | solution: the number pushed back at three quarters | P1 112, P6 112 |
| M31 | solution: the adapter's numbers capped at 10^6 | P1 39, P6 39 |

P1 and P6 kill all seventeen, P2 nine, P5 five, P3 two and P4 one. The
properties other than P1 are weak here: a wrong greedy step still gives
an answer between 1 and n, the same for the array reversed or doubled,
since every arm treats numbers alike whatever their order or scale, and
within the bounds P5 allows. P3 kills only the edits that treat one
position or one heap slot apart (M11, M21); P4 only the edit that
treats a number by its size (M36); P5 the five whose doubled array falls
outside the bounds.

Of the thirty-eight, twenty-one were not kept. Thirteen are killed and
fail as a kept one does: the ★ arm's total the last number alone, the
struct arm's halving reported whole, the iter arm's total halved and its
whole top counted as removed (M6, M17, M22, M38) as M1; more than half
wanted in the ★, struct, iter and template arms (M2, M20, M23, M28) as
M8; the queues arm's numbers sorted smallest first and every sorted
number taken before any half (M12, M14) as M3; the whole number pushed
back in the ★ and queues arms (M4, M15) as M24; and the template's
first number left out (M27) as M11. Five never finish within the 120 s
limit, each taking halves that shrink before half the sum is gone: the
scaled arm's halving counted as a quarter (M9), the queues arm's halves
taken from the back (M13), the struct arm's sift looking at the left
child only and a number above 1000 pushed at half (M18, M34), and the
iter arm's heap shifted one place less than its total (M25). One stops
with a panic: the iter arm's first number left out of the heap (M26)
pops an empty heap for an array of one. Two survive: the scaled arm
shifting 1 place and the template shifting 2 (M7, M29) round the halves
down after the first one or two of a number, and no case halves a number
often enough for the lost fractions to change a count; they are not
equivalent in general.

## Verification

Every arm prints the same output as `halve.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.6 s (the queues arm, with no
heap) to 10.5 s (the ★ arm, its heap of `Reverse[F64]`), and the
differential 1.6 s.

## Benchmarks

The bench builds 12 arrays of 10^5 numbers once, up to 10, 1000 and
10^7 in turn, then halves each once with the ★ arm in all five
languages: Rust's `BinaryHeap` over a `total_cmp` wrapper, C's
hand-written heap of doubles, Go's `container/heap` and Python's
`heapq`, each popping the top and pushing its half. Every implementation
prints `12 arrays of 10^5: checksum 515617734`.

BENCHTAB
