# 2164. Sort Even and Odd Indices Independently

You are given a **0-indexed** integer array `nums`. Rearrange the values
of `nums` according to the following rules:

1. Sort the values at **odd indices** of `nums` in **non-increasing**
   order.
   - For example, if `nums = [4,1,2,3]` before this step, it becomes
     `[4,3,2,1]` after. The values at odd indices `1` and `3` are sorted
     in non-increasing order.
2. Sort the values at **even indices** of `nums` in **non-decreasing**
   order.
   - For example, if `nums = [4,1,2,3]` before this step, it becomes
     `[2,1,4,3]` after. The values at even indices `0` and `2` are sorted
     in non-decreasing order.

Return *the array formed after rearranging the values of* `nums`.

```
nums = [4,1,2,3]  ->  [2,3,4,1]
nums = [2,1]      ->  [2,1]
```

**Constraints:** `1 <= nums.length <= 100`; `1 <= nums[i] <= 100`.

The two parities never mix, so each is taken out, sorted its own way,
and put back in its own places. O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `parity.kara` ★ | the even places by `step_by(2)` and the odd by `skip(1).step_by(2)`, sorted rising and falling, woven back by place |
| `parity_count.kara` | a counting sort for each parity, since every number is 1 to 100: two arrays of 101 counts, the even places filled from the smallest count up and the odd from the largest down |
| `parity_insertion.kara` | an insertion sort in place over each parity's places, two apart, rising on the even places and falling on the odd; no list taken out |
| `parity_struct.kara` | a `struct Deal` that `deal`s the list into two `VecDeque` hands (`own` the list), `arrange`s them (`mut ref self`) and `weave`s them back (`own self`) by `pop_front` |
| `parity_iter.kara` | each parity by `enumerate` and `filter_map`, the odd one sorted by `sort_by_key` on the negated number, woven by `zip`, `flat_map` and `chain` |
| `parity_solution.kara` | LeetCode's Rust template: `mut nums: Vec<i32>`, `iter().step_by(2).cloned()`, `sort_unstable` and `sort_unstable_by`, written back through `iter_mut().enumerate()`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and four
more (one number, two, already in order, and every number the same),
each with its answer; then a checksum over 2000 random lists of 1 to 12
numbers from 1 to 3, 10 or 100 in turn; then the constraints' largest,
100 numbers at random, falling and rising. `parity.py` mirrors the ★ arm
and its output is byte-identical.

The struct arm was first written with Rust's `VecDeque.from(v)` and
`dq.drain(..)`. Kāra's `VecDeque` has neither, and each was refused with
a bare "no associated function" or "no method", though `Set`,
`SortedSet` and `PriorityQueue` all have `from(v)`. That is ledger row
B-2026-11-14-63, fixed in karac 1617e3a972: each refusal now names the Kāra
spelling. The arm builds each hand by `collect` and takes it back out by
`mem.take`. The iterator arm was carried by `karac fix` in one edit:
the `.into_iter()` that Kāra's `flat_map` wants on the list its closure
gives.

`karac fix` carries the template in two rounds of 14 and 2 edits:
Rust's spellings (`mut nums: Vec<i32>` to `nums: own Vec[i32]` with a
`let mut nums = nums`, `<..>` to `[..]`, `struct Solution;` to `struct
Solution {}`, `Solution::` to `.`, the adapter's `|&x|` to `|x|`); then
`sort_unstable` and `sort_unstable_by` to `sort` and `sort_by`, since a
stable sort is also an unstable one.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: two numbers two places apart swapped whenever they are out of
their parity's order, rising on the even places and falling on the odd,
until a pass swaps none; no sort and no list taken out. It checks 300
random lists of 1 to 12 numbers from 1 to 3, 10 or 100 in turn; then 30
of one or two numbers; then 30 already in the other order, the even
places falling and the odd rising. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every number doubled, when none is over 50: the answer doubled |
| P3 | the numbers at even places put in reverse among themselves: the same answer |
| P4 | every number x made 101 - x: each parity of the answer made so and its order reversed |
| P5 | the answer sorted again: the same answer |
| P6 | each arm agrees with at least three of the other five |

The properties keep every number within 1 to 100, since the counting
arm counts no others: P2 doubles only lists of numbers up to 50, and P4
turns the order around by 101 - x rather than by negating.

The differential prints `360 lists: checksum 134111607, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-eight edits to the differential, four to six to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the even places never sorted | P1 235, P3 267, P4 267, P6 235 |
| M3 | ★: the odd numbers from place 0 | P1 302, P4 136, P6 302 |
| M4 | ★: the even places woven from the end | P1 274, P6 274 |
| M5 | count: a count kept for every place, not each parity | P1 264, P4 318, P6 264 |
| M7 | count: a used count never spent on the even places | P1 274, P4 274, P6 274 |
| M26 | count: an odd place's number counted twice | P1 242, P4 242, P5 161, P6 242 |
| M9 | insertion: the odd places never sorted | P1 193, P4 233, P6 193 |
| M10 | insertion: the walk back stopping one step early | P1 190, P3 250, P4 274, P6 190 |
| M12 | insertion: each number started from the place before | P1 188, P3 186, P4 264, P5 70, P6 188 |
| M13 | struct: the odd hand sorted rising | P1 242, P6 242 |
| M14 | struct: the hands swapped | P1 342, P4 136, P5 302, P6 342 |
| M27 | struct: the weave starting with the odd hand | P1 347, P4 136, P5 307, P6 347 |
| M17 | iter: the last even number never chained | P1 168, P4 136, P6 168 |
| M19 | iter: each pair woven odd first | P1 315, P4 139, P5 307, P6 315 |
| M20 | iter: place 0 left out | P1 360, P3 250, P4 135, P5 285, P6 360 |
| M22 | solution: every place written from the even list | P1 315, P4 136, P6 315 |
| M23 | solution: the adapter's answer reversed | P1 311, P5 174, P6 311 |

P1 and P6 kill all seventeen, P4 fourteen, P5 seven, P3 four and P2
none. P4 turns every number around, which swaps what rising and falling
mean; it sees an edit that treats the two parities' orders, or their
places, differently: all but three (M4, M13, M23), whose wrong answers
turn around with the numbers just as a right one does. P5 sorts the answer again, which
a right answer survives; it sees an edit whose answer is out of order
for its own parities: a list woven the wrong way round (M14, M19, M27),
reversed (M23) or left half sorted (M12), or a number in the wrong
parity (M20, M26). P3 reverses the even places
among themselves, which a sorted answer ignores; it sees an edit that
does not sort them fully (M2, M10, M12, M20). P2 doubles every number,
and every edit here depends only on the numbers' order, which doubling
keeps.

Of the twenty-eight, eleven were not kept. One is equivalent: the
struct arm's weave going on past an empty odd hand, since the next
`pop_front` of the even hand is then empty too and stops it. Four
crash: the counting arm's odd places filled from 99 or rising and its
even places from 2, each of which walks off its array of counts, and
the template's even list taken from place 2, which runs out. Six fail
as a kept one does: the odd places sorted rising in the ★, iterator and
template arms, as M13; the insertion arm's even places sorted falling,
as M4; the struct arm's place 0 dealt to the odd hand, as M14; and its
even hand never sorted, as M2.

## Verification

Every arm prints the same output as `parity.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s to 0.5 s and the
differential 0.9 s.

## Benchmarks

The bench builds 1000 lists of 100 numbers once; then solves each list
200 times, one number replaced before each solve so that no solve
repeats one before, with the ★ arm in all five languages: C by `qsort`.
Every implementation prints `200000 solves: checksum 512438646`.

BENCHTAB
