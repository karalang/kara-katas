# 2089. Find Target Indices After Sorting Array

You are given a 0-indexed integer array `nums` and a target element
`target`.

A target index is an index `i` such that `nums[i] == target`.

Return a list of the target indices of `nums` after sorting `nums` in
non-decreasing order. If there are no target indices, return an empty
list. The returned list must be sorted in increasing order.

```
nums = [1,2,5,2,3], target = 2  ->  [1,2]
nums = [1,2,5,2,3], target = 3  ->  [3]
nums = [1,2,5,2,3], target = 5  ->  [4]
```

**Constraints:** `1 <= nums.length <= 100`; `1 <= nums[i], target <=
100`.

The sort is not needed. Once sorted, every value smaller than the
target comes before it and the target's copies run on together, so the
indices are `less` to `less + equal`, two counts in one or two walks,
O(n). The approaches differ in whether they sort, and how they find the
run.

## Approaches

| file | mechanism |
|---|---|
| `target.kara` ★ | no sort: the smaller values and the copies counted with `filter(..).count()`, the indices `(less..less + equal).collect()`. O(n) |
| `target_sorted.kara` | as the statement says: a sorted copy, and the target's places in it from `iter().enumerate().filter(..)`. O(n log n) |
| `target_search.kara` | a sorted copy searched twice with `partition_point`, for the first value not less than the target and the first greater. O(n log n) |
| `target_counting.kara` | counting sort: the values tallied in a `Vec.filled(101, 0)`, the counts below the target summed with `counts[..target].iter().sum()`. O(n + 100) |
| `target_position.kara` | a sorted copy, the run's first place by `position` and its last by `rposition`, matched as a pair of `Option`s. O(n log n) |
| `target_solution.kara` | LeetCode's Rust template (`mut nums: Vec<i32>` sorted in place, `filter(\|(_, &x)\| x == target)`, `map(\|(i, _)\| i as i32)`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more, each array, target and indices; then the count and a checksum of
the indices for 2000 random arrays of 1 to 100 values from 1 to 3, 10 or
100; then the constraints' largest, 100 copies of the target, and the
values 1 to 50 twice asked for 50 and for 51. `target.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the array sorted by insertion, each value moved down past the
larger ones before it, and every index of the sorted array whose value is
the target. It checks 300 random arrays of 1 to 12 values from 1 to 3, 5
or 10, the target from 1 to one past the largest; then 20 without the
target, and 20 of nothing but the target. All 340 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the indices are the statement read literally |
| P2 | the array reversed gives the same indices |
| P3 | every value and the target doubled give the same indices |
| P4 | the indices run on one by one from the count of smaller values, as many as the target's copies |
| P5 | one more copy of the target gives one more index after the last |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 arrays: checksum 969042918, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal indices was checked against a Python reading of the same
arrays. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first value never counted smaller | P1 55, P2 56, P4 55, P5 152, P6 55 |
| M2 | ★: the indices from 0 | P1 111, P4 111, P5 225, P6 111 |
| M3 | ★: the larger values counted as copies | P1 192, P4 192, P5 192, P6 192 |
| M4 | sorted: the copy not sorted | P1 139, P2 142, P4 139, P5 192, P6 139 |
| M5 | sorted: the places counted from the end | P1 148, P4 148, P5 289, P6 148 |
| M6 | sorted: each index one more | P1 191, P4 191, P5 340, P6 191 |
| M7 | search: the first search in the unsorted array | P1 99, P2 96, P4 99, P5 60, P6 99 |
| M8 | search: the copy not sorted | P1 139, P2 131, P4 139, P5 205, P6 139 |
| M9 | search: the next value's copies taken too | P1 137, P3 137, P4 137, P5 137, P6 137 |
| M10 | counting: every count starting at 1 | P1 340, P3 340, P4 340, P5 340, P6 340 |
| M11 | counting: each value counted once | P1 137, P4 137, P5 267, P6 137 |
| M12 | counting: one index past the copies | P1 340, P4 340, P5 340, P6 340 |
| M13 | position: the last copy found from the front | P1 110, P4 110, P5 191, P6 110 |
| M14 | position: the copy not sorted | P1 139, P2 135, P4 139, P5 217, P6 139 |
| M15 | position: no copy giving index 0 | P1 149, P4 149, P5 149, P6 149 |
| M16 | solution: the adapter's target one more | P1 234, P3 137, P4 234, P5 340, P6 234 |
| M17 | solution: each index halved | P1 157, P4 157, P5 305, P6 157 |

P1, P4, P5 and P6 kill all seventeen, P2 five and P3 three. P4, which
asks the indices to be the run from the count of smaller values, sees
any edit to the run's start, end or step, and P5 any edit that does not
add exactly one index after the last when a copy is added. P2 sees only
what depends on the array's order: an arm that forgets to sort (M4, M8,
M14), the search in the unsorted array (M7), and the first value left
uncounted (M1). P3, doubling the values, sees what leans on the values lying next to
one another, since doubling leaves a gap after each: the next value's
copies taken too (M9) and the adapter's target one more (M16), which
after doubling find nothing, and counts starting at 1 (M10), which then
count every empty value below the target.

Of the thirty, thirteen were not kept, and one survives. Eleven fail as
a kept one: the ★ arm's copies counted among the smaller, the search
arm's second search stopping at the first copy and its last copy
dropped, the counting arm's copies counted among the smaller, and the
position arm's last copy left out, as M6; the ★ arm's one index past the
copies and the Rust arm's every place but the target's as M12; the ★
arm's larger counted as smaller and the Rust arm's sort from the largest
as M5; the sorted arm's larger values' places kept as M3; the sorted
arm's copies merged into one as M11. One is killed with checks of its
own but was left out because its arm keeps two: the Rust adapter's first
index dropped (P1 191, P4 191, P5 149). The survivor is equivalent: the
position arm's first copy found as any value no smaller than the target,
which in a sorted array is the target's first copy when there is one;
when there is none `rposition` finds nothing and the answer is empty
either way.

## Verification

Every arm prints the same output as `target.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.5 s to 0.8 s and the
differential 0.6 s (timed while other work shared the machine).

No arm met a compiler gap. The Rust arm was written as LeetCode's Rust
template. `karac fix` carries it in two rounds of 18 and 1 edits: Rust's
spellings (`Vec<i32>` to brackets, the `&` of `&x` and `&i` dropped, `mut
nums` to `nums: own Vec[i32]` with `let mut nums = nums;`, `struct
Solution;` to `struct Solution {}`, `Solution::` to `.`, the adapter's
`&Vec<i64>` to `ref`); then the adapter's `ref` parameter to a bare one,
which borrows already. The fixed arm reads as the template does.

## Benchmarks

The bench builds 10000 arrays of 100 values from 1 to 100, the
constraints' limit, and asks each for every target from 1 to 100 with
the ★ arm in all five languages, the indices of each answer in a fresh
growable array (a `Vec`, a `Vec`, a slice, a `list`, a `malloc`'d
buffer): `10^6` answers of two counts each. Every implementation prints
`1000000 answers: sum 3324143216, checksum 208269290`.

BENCHTAB
