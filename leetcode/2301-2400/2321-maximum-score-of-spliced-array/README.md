# 2321. Maximum Score Of Spliced Array

You are given two **0-indexed** integer arrays `nums1` and `nums2`, both
of length `n`.

You can choose two integers `left` and `right` where `0 <= left <=
right < n` and **swap** the subarray `nums1[left...right]` with the
subarray `nums2[left...right]`.

- For example, if `nums1 = [1,2,3,4,5]` and `nums2 =
  [11,12,13,14,15]` and you choose `left = 1` and `right = 2`, `nums1`
  becomes `[1,12,13,4,5]` and `nums2` becomes `[11,2,3,14,15]`.

You may choose to apply the mentioned operation **once** or not do
anything.

The **score** of the arrays is the **maximum** of `sum(nums1)` and
`sum(nums2)`, where `sum(arr)` is the sum of all the elements in the
array `arr`.

Return *the **maximum possible score***.

A **subarray** is a contiguous sequence of elements within an array.
`arr[left...right]` denotes the subarray that contains the elements of
`nums` between indices `left` and `right` (**inclusive**).

```
nums1 = [60,60,60], nums2 = [10,90,10]                  ->  210
nums1 = [20,40,20,70,30], nums2 = [50,20,50,40,20]      ->  220
nums1 = [7,11,13], nums2 = [1,1,1]                      ->  31
```

**Constraints:** `n == nums1.length == nums2.length`; `1 <= n <=
10^5`; `1 <= nums1[i], nums2[i] <= 10^4`.

A swap of `left..=right` adds to `nums1`'s sum the subarray's `nums2[i]
- nums1[i]`, and takes the same from `nums2`'s. So the best for `nums1`
is its sum plus the largest subarray sum of those differences, or
nothing when every swap loses, which is Kadane's walk; the best for
`nums2` is the same with the differences negated; the answer is the
larger. O(n). The largest score is `2 * 10^9`, past `i32`.

## Approaches

| file | mechanism |
|---|---|
| `spliced.kara` ★ | Kadane's walk over the differences once each way round, the run cut at 0, added to each array's `sum` and the larger taken |
| `spliced_naive.kara` | every splice: for each `left`, the swap grown one place at a time to the right with both sums kept as it grows, and the best of every score and the sums untouched. O(n^2) |
| `spliced_prefix.kara` | prefix sums of the differences in a `Vec.filled`: the largest rise over the lowest prefix before it helps `nums1`, the largest fall under the highest helps `nums2` |
| `spliced_states.kara` | three states for each array, the swap not yet begun, under way, or over, each place taking its number from the other array only while it is under way; `i64.MIN / 2` for a state not reached |
| `spliced_iter.kara` | iterators: the differences from `zip` and `map`, and Kadane's walk as a `fold` carrying the best and the run as a tuple, its `.0` the gain |
| `spliced_solution.kara` | LeetCode's Rust template: `i32` numbers and answer, a `kadane` nested in the method taking two `&[i32]` slices, `std::cmp::max`, and `sum::<i32>()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; one
number each; a splice that pays only in the middle; two arrays of
1000 numbers up to `10^4`; then 2000 random pairs of 1 to 30 numbers up
to 20, with a checksum and the scores in all. `spliced.py` mirrors the
★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 36 edits.
`check` first reports twenty errors and offers 31 edits for them:
`struct Solution;` to `struct Solution {}`; the twenty brackets of the
six `Vec<i32>` and `Vec<i64>`, in the method and in the harness's
wrapper; the two `&[i32]` to `Slice[i32]`, two edits each; the three
`std::cmp::` dropped, as `max` needs no path; the two turbofish
`sum::<i32>()` to a `sum()` with `: i32` on its `let`, two edits each;
the four `&` at the calls to `kadane` dropped; and, in the wrapper, the
two `&x` patterns to `x` and `Solution::` to `Solution.`. The other
five follow from those: the nested `fn kadane`, which captures
nothing, moved above `impl Solution`, one edit to write it there and
one to delete it here; `: i32` written on its `best` and `cur`, whose
`0` would otherwise be an `i64`; and the wrapper's `as i64` on the
`i32` answer dropped, as it widens on its own. The `as i32` in the
wrapper stands as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: no swap, and every `left <= right`, each swap carried out on
copies of the two arrays whose sums are then added up afresh; the score
is the larger sum, and the answer the best score. No differences and no
running sums. It checks 300 random pairs of 1 to 30 numbers up to 20;
then 30 of numbers 1 and 2 only, where swaps tie; then 30 of up to 80
numbers up to `10^4`. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at least the larger sum and at most the sum of the larger number at each place |
| P3 | the two arrays swapped: the same answer |
| P4 | both arrays reversed: the same answer |
| P5 | every number doubled: the answer doubled |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 585932677, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and every swapped pair of lists by slicing. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: only `nums1` helped | P1 125, P3 264, P6 125 |
| M5 | ★: the run cut at 1, not 0 | P1 360, P2 80, P5 360, P6 360 |
| M6 | ★: the walk over every other place | P1 291, P4 141, P6 291 |
| M8 | naive: no swap longer than 5 places | P1 114, P6 114 |
| M10 | naive: only swaps of one place | P1 265, P6 265 |
| M11 | naive: the swaps from the third place | P1 57, P4 87, P6 57 |
| M12 | prefix: the rise capped at 10 | P1 113, P3 224, P5 35, P6 113 |
| M13 | prefix: `nums2`'s sum taken as `nums1`'s | P1 244, P2 85, P3 347, P6 244 |
| M15 | prefix: every other prefix looked at | P1 214, P4 165, P6 214 |
| M17 | states: the swap begun again after it ends | P1 280, P6 280 |
| M18 | states: the swap never ended | P1 269, P6 269 |
| M19 | states: the swap never begun | P1 337, P6 337 |
| M23 | iter: the difference the wrong way | P1 337, P2 186, P6 337 |
| M25 | iter: the differences doubled | P1 357, P2 299, P6 357 |
| M26 | iter: only `nums2` helped | P1 139, P3 264, P6 139 |
| M29 | solution: the score the smaller of the two | P1 264, P6 264 |
| M30 | solution: the run cut at the first place's difference | P1 231, P4 258, P6 231 |

P1 and P6 kill all seventeen, P2, P3 and P4 four each, and P5 two.
P3, the arrays swapped, fails where an edit treats the two arrays
differently: one of them alone helped, a cap on the rise and not the
fall, one sum taken for the other. P4, the arrays reversed, fails
where an edit depends on where a swap lies: every other place, swaps
from the third, the first place's difference. P2 fails for a gain
larger than any swap gives: the run cut at 1, the differences the
wrong way or doubled, the wrong sum. P5, every number doubled, fails
only where an edit holds a constant that does not double with the
numbers: the run cut at 1 and the rise capped at 10. It replaces every
number raised by 7, which killed none of the thirty-one, since every
edit here works on differences, which a raise leaves alone, or on sums,
which it moves together.

Most ways to lose part of the search lose nothing, because of a
symmetry: swapping a prefix of the arrays leaves the same two sums as
swapping the rest of them, with the arrays exchanged, and every arm
looks both ways round. So a search that never starts a swap at the
first place, or never ends one at the last, finds every score anyway.
Two edits of the thirty-one are equivalent for that reason or its
like: the states arm's untouched sum not a candidate (M20), since a
swap of everything gives both sums back, and its swap under way from
the start (M21), which is a swap begun at the first place. One more is
killed by nothing though not equivalent: the naive arm's no swap of
one place (M7), which is wrong only when a single place in the middle
is the one best swap, as in the harness's `[5, 1, 5]` and `[1, 9, 1]`,
and no case here has that.

Eleven more fail as kept ones do. The ★ arm's (M1), the iter arm's
(M22) and the template's (M27) run not cut at zero, and the iter arm's
run kept as the best (M24), fail as the states arm's swap never ended
(M18); the ★ arm's difference the wrong way (M2) and its gain added to
the other array (M4), the prefix arm's rise and fall swapped (M16) and
the template's gain added to the other array (M28) as the iter arm's
difference the wrong way (M23); the naive arm's first array alone
scored (M9) and the prefix arm's fall measured from the lowest (M14) as
the ★ arm's `nums1` alone helped (M3); and the template's `nums2`'s sum
taken from `nums1` (M31) as the prefix arm's (M13).

M5, M6, M8, M11, M12, M15, M25, M29 and M30 replace edits that the
symmetry makes equivalent or that failed as others did: in the ★ arm
the best taken before the run moves and the walk from the second
place; in the naive arm the untouched sums left out and the swaps from
the second place; in the prefix arm the lowest begun at the first
prefix and the last prefix never looked at; the iter arm's fold's last
run for its answer; and the template's best the last run and walk one
place short. Edits tried for them that failed as kept ones did are not
listed.

## Verification

Every arm prints the same output as `spliced.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, prefix, states and template arms take
0.35 to 0.45 s, the iter arm 0.55 s, and the naive arm, which tries
every splice of the 1000 numbers, 1.0 s. The differential takes 2.5 s
there, most of it the literal reading's copies of the arrays for every
splice, and 0.4 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 pairs of `10^5` numbers up to `10^4` once, then
makes 200 passes over them with the ★ arm in all five languages, each
pass changing one number of each pair, chosen at random, before
scoring it. Every implementation prints `200 passes over 10 pairs of
10^5 numbers: checksum 741707662`. Each keeps the numbers as 64-bit
integers and walks each pair four times a score: two sums and two
walks of Kadane's.

BENCHTAB
