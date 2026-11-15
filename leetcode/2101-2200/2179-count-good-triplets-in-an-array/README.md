# 2179. Count Good Triplets in an Array

You are given two **0-indexed** arrays `nums1` and `nums2` of length
`n`, both of which are **permutations** of `[0, 1, ..., n - 1]`.

A **good triplet** is a set of `3` **distinct** values which are present
in **increasing order** by position both in `nums1` and `nums2`. In
other words, if we consider `pos1v` as the index of the value `v` in
`nums1` and `pos2v` as the index of the value `v` in `nums2`, then a
good triplet will be a set `(x, y, z)` where `0 <= x, y, z <= n - 1`,
such that `pos1x < pos1y < pos1z` and `pos2x < pos2y < pos2z`.

Return *the **total number** of good triplets*.

```
nums1 = [2, 0, 1, 3],    nums2 = [0, 1, 2, 3]     ->  1
nums1 = [4, 0, 1, 3, 2], nums2 = [4, 1, 0, 2, 3]  ->  4
```

**Constraints:** `n == nums1.length == nums2.length`; `3 <= n <=
10^5`; `0 <= nums1[i], nums2[i] <= n - 1`; `nums1` and `nums2` are
permutations of `[0, 1, ..., n - 1]`.

Read in nums1's order, the values' places in nums2 form one sequence,
and a good triplet is three places in it that rise. Each value is a
middle: the earlier ones with a smaller place, times the later ones with
a larger place. A Fenwick tree over the places counts the earlier
smaller ones as they are met; the later larger ones follow, since of the
n - 1 - p places above p, the earlier ones not below it are i - smaller.
O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `triplets.kara` ★ | a Fenwick tree in a `Vec.filled(n + 1, 0)` over the places in nums2, asked for the earlier smaller ones of each middle, then marked |
| `triplets_merge.kara` | by merge sort: the places sorted by merging halves, each element of the right half adding the left half's elements already taken to its count; the sort's order and the counts passed `mut ref` |
| `triplets_segment.kara` | a segment tree of counts laid out bottom up, its leaves at n and up; the count below a place summed from the leaves to the root over the halves left open |
| `triplets_struct.kara` | a `struct Fenwick`, made `of` a size, that `mark`s a place met (`mut ref self`) and counts the places met `below` one (`ref self`); the arrays walked by `enumerate` |
| `triplets_iter.kara` | a sorted list of the places met: each place's earlier smaller ones its `partition_point`, where it is then `insert`ed, inside a `map` that `collect`s the counts; the middles' products by `zip`, `enumerate`, `map` and `sum`; O(n^2) moves at worst |
| `triplets_solution.kara` | LeetCode's Rust template: `Vec<i32>`, `vec![0usize; n]`, `vec![0i64; n + 1]`, `v as usize` indices, `j & (!j + 1)` for the lowest bit, `struct Solution;`, `Solution::`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one triplet, the same three reversed, a permutation against itself, and
three swapped neighbours, one of each pair to choose), each with its
count; then the total and a checksum over 2000 random pairs of
permutations of 3 to 10 or 3 to 32 values in turn; then the constraints'
largest, 10^5 values: one order twice, against its reverse, and two at
random. `triplets.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in three rounds of 20, 6 and 4 edits:
Rust's spellings (`Vec<..>` to `Vec[..]`, the closures' and patterns'
`&v` and `&x` to `v` and `x`, `!j` to `~j`, `struct Solution;` to
`struct Solution {}`, and `Solution::` to `.`, among them); then the
`usize`s: the suffix on `vec![0usize; n]` and the `i64` one on `vec![0i64;
n + 1]` dropped, `v as usize` to `v as i64` where it indexes, and the
`as i64` casts on the count of later ones dropped, since the index is an
`i64` already; then each `vec![0; ..]` to `Vec.filled(.., 0)`, and the
`as i64` on `v` dropped, as an `i32` widens to the `i64` index.

The merge arm was written with its sequence as `seq: ref Vec[i64]`;
`karac fix` drops the `ref`, since a parameter borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every three values tried, each value's place looked up in
both arrays, and counted when the places rise in both. No places read
in one order, no tree and no sort. It checks 300 random pairs of
permutations of 3 to 9 values; then 30 of one permutation twice; then
30 of one against its reverse. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the two arrays swapped: the same count |
| P3 | every value v made n - 1 - v in both: the same count |
| P4 | both arrays reversed: the same count |
| P5 | a new value n put at the end of both: the count, plus the pairs of values in the same order in both |
| P6 | each arm agrees with at least three of the other five |

A good triplet is a set of three values whose order is the same in both
arrays. P2 holds since that reads the arrays alike; P3 since a renaming
moves no value's place; P4 since reversing both reverses every order in
each, and two orders that agreed still agree. P5 holds since the new
value comes last in both, so it makes a good triplet with exactly the
pairs in the same order in both.

The differential prints `360 pairs: checksum 597914749, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
pairs. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-eight edits to the differential, five to each Kāra arm and three
to the template, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the smaller ones counted below the place before | P1 269, P2 120, P4 203, P5 360, P6 269 |
| M4 | ★: the place nums1's own value | P1 267, P2 260, P3 309, P4 309, P5 318, P6 267 |
| M5 | ★: the lookup the wrong way round | P1 224, P2 218, P3 246, P4 246, P5 219, P6 224 |
| M7 | merge: a right element counting the left not yet taken | P1 351, P2 220, P4 257, P5 330, P6 351 |
| M8 | merge: the right half never sorted | P1 270, P2 217, P4 255, P5 355, P6 270 |
| M9 | merge: a pair never split | P1 263, P2 207, P4 233, P5 355, P6 263 |
| M11 | segment: a left end taken when even | P1 291, P2 192, P4 245, P5 354, P6 291 |
| M14 | segment: the larger ones less the smaller | P1 292, P2 220, P4 265, P5 360, P6 292 |
| M15 | segment: an odd left end stepped past untaken | P1 168, P2 108, P4 147, P5 312, P6 168 |
| M17 | struct: a count stopping at the first slot | P1 119, P2 116, P4 131, P5 179, P6 119 |
| M18 | struct: the count below the mirrored place, if fewer | P1 211, P2 167, P4 163, P5 276, P6 211 |
| M20 | struct: nums2's places reversed | P1 317, P5 315, P6 317 |
| M22 | iter: each place pushed to the end | P1 208, P2 230, P4 230, P5 195, P6 208 |
| M23 | iter: the larger ones the later less the earlier | P1 226, P4 121, P5 315, P6 226 |
| M24 | iter: the first two middles skipped | P1 102, P2 116, P4 129, P5 156, P6 102 |
| M26 | solution: the adapter's second array the first | P1 329, P5 329, P6 329 |
| M27 | solution: the query stepping by one | P1 286, P2 184, P4 232, P5 360, P6 286 |

P1, P5 and P6 kill all seventeen, P4 fifteen, P2 fourteen and P3 two.
P2 and P4 swap or reverse the arrays, and miss only an edit whose
answer is itself symmetric under the change: nums2's places reversed
(M20), which counts the triplets in one order in nums1 and the other in
nums2, and the second array the first (M26), which counts every three
values. P2 also misses the later ones less the earlier (M23), whose wrong
count comes out the same for the arrays swapped on every pair here. P3 renames the values, and sees only an edit
that reads a value where it means a place: nums1's own value taken for
its place (M4) and the lookup built the wrong way round (M5).

Of the twenty-eight, eleven were not kept. Two are equivalent, both
since the values are distinct and each middle asks before it is marked:
the merge arm taking the left on a tie (M6), as no two places tie, and
the struct arm's tree one slot short (M19), which loses only the mark
of the last place, a place no count below asks for. Four fail as a kept
one does: the segment arm's range one place short and the struct arm's
mark from two places on, as M1; the iter arm's partition by the greater,
as M7; and its places read as nums1's values, as M4. Five were left out
to keep three to an arm: the ★ arm's larger ones every later one (M2)
and its mark stepping by one (M3), the merge arm's merge never written
back (M10), the segment arm's mark skipping every other level (M13), and
the template's right one more (M28).

## Verification

Every arm prints the same output as `triplets.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ arm takes 1.5 s, the struct, template,
segment and merge arms 1.9 s to 5.0 s, and the iter arm 28 s: against
its reverse, every place of the 10^5 is inserted at the front of the
sorted list. The differential takes 1.8 s.

## Benchmarks

The bench shuffles two permutations of 10^5 values once; then solves 40
times, the first against the second rotated by a random offset, so that
no solve repeats one before, with the ★ arm in all five languages. C
works over pointers and a length, the others over slices. Every
implementation prints `40 solves: checksum 986298660`.

BENCHTAB
