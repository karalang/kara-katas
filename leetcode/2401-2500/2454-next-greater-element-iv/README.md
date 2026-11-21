# 2454. Next Greater Element IV

You are given a **0-indexed** array of non-negative integers `nums`. For
each integer in `nums`, you must find its respective **second greater**
integer.

The **second greater** integer of `nums[i]` is `nums[j]` such that:

- `j > i`
- `nums[j] > nums[i]`
- There exists **exactly one** index `k` such that `nums[k] > nums[i]`
  and `i < k < j`.

If there is no such `nums[j]`, the second greater integer is considered
to be `-1`.

Return *an integer array* `answer`*, where* `answer[i]` *is the second
greater integer of* `nums[i]`*.*

```
nums = [2,4,0,9,6]  ->  [9,6,6,-1,-1]
nums = [3,3]        ->  [-1,-1]
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^9`.

Reading left to right, an index waits first for one greater value and
then for another. The indices still waiting for their first fall in
value from the oldest, as in the stack for the next greater element; so
do those waiting for their second, once the ones a value moves across
keep their order. Each value then answers the second stack's smaller
tops and moves the first stack's smaller tops across, and every index
is pushed and popped at most twice.

## Approaches

| file | mechanism |
|---|---|
| `second.kara` ★ | two monotonic stacks of indices: each value pops the second stack's smaller tops as answered, then moves the first stack's smaller tops, in their order, onto the second, by a cut point and `truncate`. O(n) |
| `second_naive.kara` | the statement read directly: from each index the values to its right scanned, those greater counted, and the second of them is the answer. O(n^2) |
| `second_heap.kara` | two smallest-first `PriorityQueue`s of `(value, index)`: each index waits in the first for one greater value and in the second for another, each value popping the smaller entries of both by `while let` on `peek`. O(n log n) |
| `second_sorted.kara` | by value: the indices sorted from the largest value down by `sort_by_key`, each run of equal values answered before it joins a `SortedSet` of greater values' indices, the answer at the second index after `i` by `range` and `nth(1)`. O(n log n) |
| `second_iter.kara` | iterators: for each index, the values after it by `skip`, the greater ones kept by `filter`, and the second taken by `nth(1)`, or -1 by `unwrap_or`. O(n^2) |
| `second_solution.kara` | LeetCode's Rust template: two stacks of `usize` read by `while let Some(&j) = s.last()`, the first stack's smaller tops popped into `moved` and put on the second by `s2.extend(moved.into_iter().rev())`, the answer `vec![-1; n]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; one value;
rising, every answer two ahead; falling, none; repeats, two equal
greater values counted as two; 0 and `10^9`, the constraints' least and
most; then 2000 random values up to `10^9` and 2000 up to 3, each as a
checksum; and 3000 random arrays of 1 to 8 values up to 9, as a
checksum. `second.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 50000 random arrays of up
to 10 values against the statement's three conditions tested for every
`j`. The random arrays stop at 2000 values, not the constraints'
`10^5`, because the naive and iter arms are quadratic; the bench takes
`10^5`.

`check` first reports 10 errors on the template, and `karac fix`
carries it in one call, reporting 19 edits: the angle brackets of the
four `Vec<..>` made square; `Vec::new` written `Vec.new` three times;
each `Some(&j)` pattern written `Some(j)` with `.cloned()` after
`last()`, which copies the index out as the `&` did; `struct Solution;`
given its braces; and, once the template parses, `vec![-1; n]` written
`Vec.filled(n, -1)` and both `usize` written `i64`. `while let`, the
`else { break; }` arms, `moved.into_iter().rev()` and `extend` stand as
Kāra. The values fit an `i32`, as LeetCode's signature has them; the
other arms take `i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each `i`, every `j` after it tried in order, and `j` is
the answer when `nums[j] > nums[i]` and exactly one `k` between them
has `nums[k] > nums[i]`, counted afresh for each `j`. No stack is kept
and no greater value carried over. It checks 300 random arrays of 1 to
10 values up to 9; then 30 of up to 40 values up to `10^8`; then 30 of
up to 40 values up to 2, full of repeats. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every value raised by one constant up to 1000: each answer raised by it, -1 kept |
| P3 | every value doubled: each answer doubled, -1 kept |
| P4 | each answer -1, or a value later in the array and greater than its own |
| P5 | two values above every other put after the end: each answer kept, each -1 that value, and -1 for the two |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 hold because raising or doubling every value keeps which
values are greater than which. P4 is the first two conditions. P5 holds
because the two new values come after every index and are greater than
every old value: an index with a second greater value already has it
first, and one with none has one or none before the end, so the two new
values bring it to two. The middle cases stop at `10^8` so that P3
stays within the constraints' `10^9`.

The differential prints `360 cases: checksum 795351514, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tests the same conditions. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the moved indices left on the first stack | P1 101, P5 253, P6 101 |
| M5 | ★: each index straight to the second stack | P1 295, P6 295 |
| M6 | ★: the value before answered | P1 232, P4 135, P5 250, P6 232 |
| M8 | naive: an equal value counted | P1 165, P4 131, P6 165 |
| M9 | naive: the next value skipped | P1 246, P5 360, P6 246 |
| M11 | naive: a second greater by two needed | P1 103, P3 103, P5 360, P6 103 |
| M13 | heap: an equal value moves an entry on | P1 92, P6 92 |
| M15 | heap: the first greater answered until a second | P1 250, P5 250, P6 250 |
| M16 | heap: its own value answered | P1 253, P4 253, P5 360, P6 253 |
| M18 | sorted: indices before it counted | P1 278, P4 243, P6 278 |
| M20 | sorted: from the least value up | P1 282, P4 251, P5 360, P6 282 |
| M21 | sorted: each index one late | P1 250, P4 149, P5 360, P6 250 |
| M23 | iter: the last index never answered | P1 360, P4 360, P5 360, P6 360 |
| M25 | iter: none answered 0 | P1 360, P2 360, P4 360, P5 360, P6 360 |
| M26 | iter: greater by two needed | P1 135, P3 135, P5 360, P6 135 |
| M27 | solution: an equal value answers | P1 106, P4 106, P6 106 |
| M28 | solution: moved in pop order | P1 80, P6 80 |

P1 and P6 kill all seventeen, P5 eleven, P4 nine, P3 two and P2 one.

Thirteen are not kept, because each fails exactly as a kept one: the ★
and heap arms' equal value answering (M1, M12) as the template's
(M27); the ★ arm's equal value moving an index on (M2) as the heap
arm's (M13); the ★ arm's moved indices reversed (M3) as the template's
moved in pop order (M28), which is the same edit made another way; the
naive arm's none answered by its own value (M7) as the iter arm's last
index never answered (M23), both wrong on every case; the naive arm's
and the template's none answered 0 (M10, M31) as the iter arm's (M25);
the heap arm's raised by one on the move (M14) as the naive arm's
second greater by two needed (M11); the sorted arm's first greater and
the template's each index straight to the second stack (M17, M29) as
the ★ arm's (M5), all answering the first greater value; the iter
arm's third greater (M22) as the naive arm's next value skipped (M9);
the iter arm's equal value counted (M24) as the naive arm's (M8); and
the template's own value answered (M30) as the heap arm's (M16).

One survives, and is equivalent: the sorted arm's each value alone
(M19). With each index answered and then put in the set one at a time,
an equal value already in the set has a smaller index, since `sort` is
stable and the indices start in order, so `range(i + 1, n)` never sees
it. Three more were first written and replaced, each failing as a kept
one: the naive arm's first greater (as M5), the heap arm's straight to
the second heap (as M5) and the iter arm's next value skipped (as M9).

## Verification

Every arm prints the same output as `second.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 to 0.8 s, and the
differential 1.0 s; under `karac __mir-llvm-asan` the differential
takes 0.7 s and under `karac run` 0.6 s.

## Benchmarks

The bench builds 10 arrays of `10^5` values up to `10^9`, the
constraints' largest, once from its own generator. It then makes 20
passes; each sets one value of every array from the checksum so far, so
no answer carries over, then answers every array and folds every answer
plus one, and then the pass, into the checksum. The bench uses the ★
arm, the two stacks with the moved indices cut off the first, in all
five languages. Every implementation prints `20 passes over 10 arrays
of 10^5 values: checksum 506624136`. The answer is a new vector for
every array in every language but C, which fills one buffer and keeps
its two stacks as arrays of `10^5`.

BENCHTAB
