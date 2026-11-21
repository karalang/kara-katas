# 2488. Count Subarrays With Median K

You are given an array `nums` of size `n` consisting of **distinct**
integers from `1` to `n` and a positive integer `k`.

Return *the number of non-empty subarrays in* `nums` *that have a
**median** equal to* `k`.

**Note:**

- The median of an array is the **middle** element after sorting the
  array in **ascending** order. If the array is of even length, the
  median is the **left** middle element.
  - For example, the median of `[2,3,1,4]` is `2`, and the median of
    `[8,4,3,5,1]` is `4`.
- A subarray is a contiguous part of an array.

```
nums = [3,2,1,4,5], k = 4  ->  3
nums = [2,3,1], k = 3      ->  1
```

**Constraints:** `n == nums.length`; `1 <= n <= 10^5`; `1 <= nums[i], k
<= n`; the integers in `nums` are distinct.

The numbers are distinct, so a subarray has median `k` exactly when it
holds `k` and as many numbers greater than `k` as smaller, or one more
greater. Each number read as +1 above `k` and -1 below, a subarray round
`k`'s place counts when its balance is 0 or 1, and that balance is the
balance of its part left of `k` plus that of its part right of it. So
the balances of every start are counted once, and every end adds the
starts that make 0 or 1 with it. The approaches differ in how they keep
that count.

## Approaches

| file | mechanism |
|---|---|
| `median.kara` ★ | by a `Map`: the balances of the starts, walking left from `k`, counted in a `Map[i64, i64]`, each written `starts[b] = starts.get(b).unwrap_or(0) + 1`; then each end, walking right, adding the starts at `-balance` and `1 - balance`. O(n) |
| `median_array.kara` | by a counting array: the balances lie between `-n` and `n`, so they are counted in a `Vec` of `2 n + 1` offset by `n`. O(n) |
| `median_prefix.kara` | by prefix sums: the sums of the signs over the first `i` numbers, those up to `k`'s place counted in a `Map`, and each end after it looking up its own sum and one less. O(n) |
| `median_sorted.kara` | by a sorted list: the start balances sorted, and each end's starts counted as one range by two `partition_point`s. O(n log n) |
| `median_iter.kara` | iterators: the signs `scan`ned into balances both ways, the starts `fold`ed into a `Map` seeded by `Map.from([(0, 1)])`, the ends `map`ped to their counts and `sum`med. O(n) |
| `median_solution.kara` | LeetCode's Rust template: `Vec<i32>` and `i32` in, `i32` out; a `std::collections::HashMap` filled by `*cnt.entry(bal).or_insert(0) += 1` and read by `get(&..).unwrap_or(&0)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 18 lines: LeetCode's two examples and six
more, each array and what it counts; then a checksum of 2000 random
orders of 1 to 200 numbers, `k` any of them; then the constraints'
largest, `10^5` numbers rising, falling and in a random order, each with
`k` the least, the middle and the greatest. `median.py` mirrors the ★
arm and its output is byte-identical, and the mirror was checked on
5000 random orders of 1 to 12 numbers against every subarray sorted and
its median read off. The two agreed on every order.

The iter arm was first written with its seed as `[(0, 1)].into_iter()
.collect()`, the `Map` named only by the `fold` closure's `own Map[i64,
i64]` parameter and the `let` it is bound to. `karac check` refuses that
with E0516 "an expression whose type does not lower (UnsolvedParam("C"))
is not lowered yet": neither type reaches the seed through the `scan`
the `fold` is called on, though the same seed checks when the `fold` is
called on `iter()` itself. The arm uses the library's own spelling for
a map of given pairs, `Map.from`, which the collections doc gives; the
refusal is to be filed on the ledger.

`check` first reports 10 errors on the template, all Rust's spellings:
the `use std::collections::HashMap;` line, `struct Solution;`, `Vec<..>`
and `HashMap<..>` in angle brackets, `HashMap::new`, the `&` in `|&x|`,
and the four `&`s of `get(&..)` and `unwrap_or(&0)`. `karac fix` carries
it in one call, reporting 18 edits: the `use` line goes, since `Map` is
in the prelude, and `HashMap` becomes `Map`; the brackets, `.` for `::`
and `struct Solution {}`; the `&`s go; `ans` is annotated `i32`, since
its first value is a bare `0`; and the wrapper's `as i64` on the `i32`
answer goes, since an `i32` widens by itself. The `entry(..).or_insert(0)`
and the `if` as an expression stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray copied, sorted afresh, and its median, the
number at `(len - 1) / 2`, compared with `k`. No balance is used. It
checks 300 random orders of 1 to 12 numbers, then 20 of one or two, and
40 of 20 to 40, `k` any of the numbers. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | at least 1, `[k]` itself, and at most the subarrays that hold `k` |
| P3 | the numbers reversed: the same count |
| P4 | `k` the least, 1: one more than the numbers beside 1 |
| P5 | `k` the greatest, `n`: 1 |
| P6 | each arm agrees with at least three of the other five |

P3 holds because a median does not depend on the order of a subarray,
and reversing the array maps its subarrays onto one another. P4 holds
because a subarray of three or more numbers has its median at sorted
place 1 or later, above 1, while one of two that holds 1 has 1 as its
left middle; so the count is 1 for `[1]` and 1 for each neighbour. P5 holds because
`n` sorts last, so a subarray holding any other number has its median
below `n`, which leaves `[n]` alone.

The differential prints `360 cases: checksum 870137180, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and adds up the same sums. On a failure it prints the
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
| M1 | ★: the start at k never counted | P1 360, P2 149, P3 190, P4 360, P5 360, P6 360 |
| M5 | ★: k itself read as smaller on the right | P1 329, P2 131, P4 261, P5 360, P6 329 |
| M6 | ★: the starts walked from the front | P1 100, P3 145, P6 100 |
| M7 | array: the start at k counted twice | P1 360, P2 61, P3 190, P4 360, P5 360, P6 360 |
| M8 | array: an end looking up its own balance | P1 199, P4 206, P5 214, P6 199 |
| M10 | array: each start counted twice | P1 211, P2 31, P3 190, P4 269, P6 211 |
| M13 | prefix: the ends begun after k | P1 360, P2 154, P3 190, P4 360, P5 360, P6 360 |
| M14 | prefix: one more smaller looked up | P1 323, P4 335, P5 335, P6 323 |
| M16 | prefix: k placed one later | P1 313, P2 157, P3 190, P4 294, P5 360, P6 313 |
| M17 | sorted: a balance of 0 left out | P1 360, P2 131, P4 360, P5 360, P6 360 |
| M19 | sorted: the starts never sorted | P1 165, P2 89, P3 174, P5 270, P6 165 |
| M21 | sorted: the walk left begun at k | P1 210, P2 18, P3 190, P4 316, P6 210 |
| M22 | iter: the start at k given a balance of 1 | P1 252, P3 231, P4 272, P5 279, P6 252 |
| M23 | iter: each end looking up the wrong sign | P1 235, P3 306, P4 240, P5 279, P6 235 |
| M25 | iter: a count set to 1, not added to | P1 95, P3 141, P6 95 |
| M29 | solution: a missing balance of 1 counted once | P1 286, P2 75, P3 310, P4 256, P5 360, P6 286 |
| M30 | solution: the last end never taken | P1 180, P2 92, P3 223, P4 147, P5 81, P6 180 |

P1 and P6 kill all seventeen, P4 fourteen, P3 and P5 thirteen each, and
P2 eleven.

Fourteen are not kept, and none survives. Ten fail exactly as a kept
one: the ★ arm's balance of -1 counted for 1 and the prefix arm's `k`
read as greater (M3, M15) as the prefix arm's one more smaller looked up
(M14), each counting the starts whose balance is 0 or -1, not 0 or 1;
the ★ arm's walk left begun at `k` (M4) as the sorted arm's (M21); the
array and iter arms' ends begun after `k` (M11, M26) as the prefix arm's
(M13); the prefix, sorted and template arms' start at `k` never counted
(M12, M20, M27) as the ★ arm's (M1); and the iter arm's `k` read as
smaller (M24) as the ★ arm's (M5). The other four fail as one another,
in two pairs, whose arms already hold their kept edits: the ★ arm's
balance of 1 never counted and the sorted arm's balance of 1 left out
(M2, M18), which count only the odd subarrays' medians; and the array
arm's and the template's starts counted the other way (M9, M28). The
template's first start never taken (M31) fails in a way of its own, but
the template keeps two.

## Verification

Every arm prints the same output as `median.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.7 to 8.7 s and the differential 0.8 s; under `karac __mir-llvm-asan` the arms take 0.8 to 1.4 s and the differential 0.7 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 20 random orders of 1 to `10^4` once from its own
generator, then makes 400 passes; each swaps two numbers of every order
and asks for a `k`, the places and `k` chosen by the checksum so far, so
no question repeats the last, and folds the answer plus the pass into
the checksum. The bench uses the ★ arm in all five languages: Rust's
map is a `HashMap`, Go's a `map[int64]int64`, and C's an open-addressing
table cleared for every answer. Every implementation prints `400 passes
over 20 orders of 10^4: checksum 778740009`.

BENCHTAB
