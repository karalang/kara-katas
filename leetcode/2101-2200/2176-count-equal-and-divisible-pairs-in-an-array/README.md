# 2176. Count Equal and Divisible Pairs in an Array

Given a **0-indexed** integer array `nums` of length `n` and an integer
`k`, return *the **number of pairs*** `(i, j)` *where* `0 <= i < j < n`,
*such that* `nums[i] == nums[j]` *and* `(i * j)` *is divisible by* `k`.

```
nums = [3, 1, 2, 2, 2, 1, 3], k = 2  ->  4
nums = [1, 2, 3, 4],          k = 1  ->  0
```

**Constraints:** `1 <= nums.length <= 100`; `1 <= nums[i], k <= 100`.

At most 100 numbers, so every pair of indices can be tried. A faster
reading groups the indices by number, or counts, for each index j, the
earlier ones with its number that are multiples of k / gcd(j, k), which
is exactly when the product is a multiple of k. O(n^2).

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | every pair of indices, equal numbers whose product is a multiple of k |
| `pairs_grouped.kara` | the indices grouped by number in a `SortedMap[i64, Vec[i64]]` (`entry`, `or_insert`), and only the pairs within a group tried |
| `pairs_gcd.kara` | by divisors: each index asks a `Map[(i64, i64), i64]` how many earlier indices with its number are multiples of k / gcd(j, k), then adds itself under every divisor of k it is a multiple of; O(n * the divisors of k) |
| `pairs_struct.kara` | a `struct Tally` of the indices met for each number and k, made `of` k; each index `meets` (`mut ref self`) the earlier ones it `pairs_with` (`ref self`) and is recorded |
| `pairs_iter.kara` | for each index the later ones `filter`ed and `count`ed, `map`ped from every index, and their `sum` |
| `pairs_solution.kara` | LeetCode's Rust template: two index loops, `&&`, `(i * j) % k as usize == 0`, `struct Solution;`, `Solution::`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one number, two equal numbers that pair through index 0, equal numbers
at indices whose product misses k, and every pair divisible), each with
its count; then the total and a checksum over 2000 random lists of 1 to
30 numbers of 1 to 3 or 1 to 10 in turn, with a k of 1 to 12; then the
constraints' largest, 100 numbers: all one number with k 1 and with k
100, and at random from 1 to 4 with k 6. `pairs.py` mirrors the ★ arm
and its output is byte-identical.

`karac fix` carries the template in three rounds of 9, 2 and 2 edits:
Rust's spellings (`Vec<i32>` to `Vec[i32]`, `&&` to `and`, `struct
Solution;` to `struct Solution {}`, the adapter's `&Vec<i64>` to `ref
Vec[i64]`, its closure's `&x` to `x`, and `Solution::` to `.`, among
them); then `k as usize` to `k as i64`, since an index is an `i64`, and
the adapter's widening `as i64` dropped; then the `as i64` on `k`
dropped too, as the `i32` widens where it meets the `i64` product, and
the adapter's `ref` dropped, since a parameter borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every ordered pair of different indices with equal numbers
whose product is a multiple of k, counted, and halved, since each pair
is met in both orders. It checks 300 random lists of 1 to 12 numbers of
1 to 2, 1 to 4 or 1 to 20 in turn, with a k of 1 to 12; then 30 of one
number throughout; then 30 with k a prime above the length, 13, 17 or
19. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | every number 7 more: the same count |
| P3 | every number x made 3x + 1: the same count |
| P4 | a number not in the list put at its end: the same count |
| P5 | the count at most the pairs of equal numbers, and at least the equal numbers' pairs with index 0 |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 hold since each renames the numbers one to one, and the count
reads only which indices hold equal numbers. P4 holds since the added
number equals none before it. P5 holds since a counted pair is a pair of
equal numbers, and one with index 0 has a product of 0.

The differential prints `360 lists: checksum 889374979, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
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
| M1 | ★: the inner loop from i, so each index pairs with itself | P1 360, P4 94, P5 188, P6 360 |
| M3 | ★: indices counted from 1 | P1 210, P5 114, P6 210 |
| M5 | ★: numbers equal or one apart | P1 255, P3 255, P5 145, P6 255 |
| M7 | grouped: the groups by number mod 5 | P1 71, P4 44, P5 60, P6 71 |
| M8 | grouped: every pair in a group | P1 231, P6 231 |
| M10 | grouped: the last group never walked | P1 152, P4 152, P5 97, P6 152 |
| M11 | gcd: the need k itself | P1 121, P6 121 |
| M13 | gcd: the gcd taken with k + 1 | P1 166, P5 30, P6 166 |
| M15 | gcd: the divisors short of k | P1 203, P5 126, P6 203 |
| M17 | struct: the product's remainder by k + 1 | P1 155, P6 155 |
| M19 | struct: a number not met before counted once | P1 360, P4 360, P5 219, P6 360 |
| M20 | struct: the indices met kept by the index mod 4 | P1 248, P2 134, P3 134, P5 180, P6 248 |
| M23 | iter: a product's remainder under 2 | P1 88, P6 88 |
| M24 | iter: the most of any index, not the sum | P1 129, P6 129 |
| M25 | iter: the later numbers compared with the next index's | P1 253, P4 164, P5 154, P6 253 |
| M27 | solution: the adapter's k doubled | P1 112, P6 112 |
| M28 | solution: the adapter's numbers halved | P1 102, P2 239, P3 102, P5 45, P6 102 |

P1 and P6 kill all seventeen, P5 eleven, P4 five, P3 three and P2 two.
P5 bounds the count by the pairs of equal numbers and by those with
index 0, and misses an edit that counts too few or too many divisible
pairs but never a pair of unequal numbers nor fewer than index 0 gives:
every pair in a group (M8), the need k (M11), the remainder by k + 1
(M17), under 2 (M23), the most of one index (M24), and k doubled (M27).
P4 adds a number found nowhere else, and sees an edit whose answer moves
with the length or with which number comes last: an index paired with
itself (M1), the groups mod 5 (M7), the last group left out (M10), an
unmet number counted (M19), and the next index's number (M25). P3 and P2
rename the numbers, and see an edit that reads their values: one apart
(M5), the index mod 4 that mixes numbers (M20, which a renaming turns
into another mix), and the halving that merges them (M28).

Of the twenty-eight, eleven were not kept, none of them equivalent.
Four fail as a kept one does: the gcd arm asking after adding itself,
the struct arm recording an index before it meets, and the iter arm's
later indices from i, as M1; the grouped arm's indices pushed one more,
as M3. Seven were left out to keep three to an arm: the ★ arm's sum
for the product (M2) and its last index never paired (M4), the grouped
arm's pairs from its second (M6), the gcd arm's index added under 1 only
(M12), the struct arm's first earlier index only (M18), the iter arm's
first index left out (M22), and the template's pairs from i + 2 (M26).

## Verification

Every arm prints the same output as `pairs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s to 0.8 s, and the
differential 0.6 s.

## Benchmarks

The bench builds one row of 100000 numbers from 1 to 5 once; then
solves 20000 windows of 100 numbers, the constraints' longest, each at a
random start and with a k of 1 to 100, so that no solve repeats one
before, with the ★ arm in all five languages. C works over a pointer and
a length, the others over a slice. Every implementation prints `20000
solves: checksum 414036404`.

BENCHTAB
