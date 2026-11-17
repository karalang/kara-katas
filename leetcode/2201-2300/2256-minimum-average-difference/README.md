# 2256. Minimum Average Difference

You are given a **0-indexed** integer array `nums` of length `n`.

The **average difference** of the index `i` is the **absolute**
**difference** between the average of the **first** `i + 1` elements of
`nums` and the average of the **last** `n - i - 1` elements. Both
averages should be **rounded down** to the nearest integer.

Return *the index with the **minimum average difference***. If there
are multiple such indices, return the **smallest** one.

**Note:** the average of `n` elements is their sum divided by `n`,
rounded down; the average of `0` elements is considered to be `0`.

```
nums = [2,5,3,9,5,3]  ->  3
nums = [0]            ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^5`.

The sums reach 10^10, past `i32`, so they are kept in `i64`. With the
total known, one pass keeps the sum of the first `i + 1` values and
takes the rest's as the total less it; the last index's right side is
empty and its average 0. A strict `<` keeps the first of equal gaps.
O(n).

## Approaches

| file | mechanism |
|---|---|
| `average.kara` ★ | one pass with the total from `iter().sum()`: the left sum grown as the loop goes, the right the total less it, the best kept by a strict `<` from a gap of -1 meaning none yet |
| `average_prefix.kara` | a prefix-sum array, `prefix[k]` the sum of the first `k` values, built once in `Vec.filled(n + 1, 0)`; a second loop takes each side's sum from it, the best gap begun at `i64.MAX` |
| `average_suffix.kara` | from the right: a suffix-sum array built by a loop over `(0..n).rev()`, the left side the total `suffix[0]` less `suffix[i + 1]`; the indices still tried left to right so a tie keeps the first |
| `average_struct.kara` | a `struct Split` of the two sides' sums and counts, all on the right at first, whose `shift` (`mut ref self`) moves one value left and whose `gap` (`ref self`) differences the two averages through `average`, which takes an empty side as 0; the best an `Option[(gap, index)]` replaced in a `match` with a guard |
| `average_iter.kara` | iterator chains: the running sums by `scan`, `enumerate`d, each made a `(gap, index)` by `map`, and the first smallest gap by `min_by_key`, which keeps the first of equal keys |
| `average_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out, the total by `map(\|&x\| x as i64).sum()`, the left sum an `i64` grown in `for (i, &x) in nums.iter().enumerate()`, and the best kept as `let (mut best, mut ans) = (i64::MAX, 0)`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four
more (every value alike, where the first index wins the tie; a small
case whose middle gap is 0; one where the last index's empty side
matters; and the constraints' largest values), each with its index;
then the sum of the indices over 2000 cases of 1 to 12 values from 0
to 10, with a checksum; then the constraints' largest, 10^5 values, as
any value up to 10^5, values near 10^5, and the values 1 to 10^5.
`average.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 13 edits: `Vec<i32>`
to `Vec[i32]`, the `&` patterns dropped from the closure and the `for`,
`i64::MAX` to `i64.MAX`, `let (mut best, mut ans)` to `let mut (best,
ans)` with the `0` made `0i32`, `nums.len() as i64` and `i as i64`
dropped as lossless, `struct Solution;` to `struct Solution {}`, and
`Solution::` to `Solution.`. Dropping `i as i64` leaves `let i = i;`
behind.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every index, the two sides summed afresh over their own
ranges and their averages rounded down, an empty side's 0, and the
first index with the smallest gap found by comparing every pair; no
running sums. It checks 300 random cases of 1 to 12 values from 0 to
10; then 30 of values up to 10^5; then 30 of 2 to 12 values of 0 or 1,
where ties are many. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the index is the literal reading's |
| P2 | the index is in range |
| P3 | no index has a smaller gap than the index given |
| P4 | no index before it has as small a gap |
| P5 | every value set to the first: the index 0 |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 378865235, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading with
slices and `min` over `(gap, index)`. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the rest's average over one more value | P1 162, P3 143, P4 95, P6 162 |
| M3 | ★: the first side's average over one more value | P1 208, P3 165, P4 127, P5 233, P6 208 |
| M4 | ★: the gap without `abs` | P1 231, P3 186, P4 231, P6 231 |
| M7 | prefix: each prefix only its last value | P1 269, P3 242, P4 220, P5 297, P6 269 |
| M10 | prefix: the best gap begun at 0 | P1 229, P3 229, P6 229 |
| M11 | prefix: the last index never tried | P1 11, P3 11, P6 11 |
| M12 | suffix: the values added in reverse | P1 254, P3 225, P4 161, P6 254 |
| M14 | suffix: the empty side's average the whole's | P1 165, P3 155, P4 165, P6 165 |
| M15 | suffix: the last value never added | P1 175, P3 160, P4 105, P5 61, P6 175 |
| M17 | struct: the last of equal gaps kept | P1 167, P4 167, P5 314, P6 167 |
| M19 | struct: a side of one value averaged as 0 | P1 105, P3 68, P4 68, P5 252, P6 105 |
| M20 | struct: the gap read before the shift | P1 315, P3 240, P4 294, P5 297, P6 315 |
| M22 | iter: the sum before the value yielded | P1 262, P3 227, P4 227, P5 297, P6 262 |
| M23 | iter: the largest gap | P1 341, P3 326, P4 304, P5 341, P6 341 |
| M25 | iter: the index counted from the end | P1 324, P2 131, P3 304, P4 312, P5 360, P6 324 |
| M29 | solution: each value counted twice on the left | P1 233, P3 223, P4 122, P6 233 |
| M31 | solution: the index one past | P1 360, P2 30, P3 255, P4 360, P5 360, P6 360 |

P1 and P6 kill all seventeen, P3 sixteen, P4 fifteen, P5 ten, and P2
two. P3 and P4 split what P1 sees: P3 fails an index whose gap is not
the smallest, P4 one with an equal gap earlier. The tie edit (M17)
passes P3 and fails P4, and the edits that skip the last index or start
the best at 0 (M10, M11) pass P4 and fail P3. P5 sets every value to
the first, where every split but the last has a gap of 0 and index 0
must win, so it catches the tie edit and every edit that miscounts a
side. P2 fails only the edits that can give an index past the end (M25,
M31).

Of the thirty-one, fourteen were not kept, and none survives, crashes
or differs between the backends. Five fail as a kept one does: the last
of equal gaps kept in the ★, suffix, iter and template arms (M1, M16,
M26, M27) as the struct arm's (M17), and the ★ arm's empty side given
the other side's average (M6) as the suffix arm's given the whole's
(M14). Four fail in pairs: the ★ arm's rest taken before the
value moves and the prefix arm's rest one value long (M5, M9), and the
first side one value short in the prefix and suffix arms (M8, M13).
The other five fail in ways of their own and are left out because their
arms keep three: the struct arm's right count never lowered and first
value left out of the right (M18, M21), the iter arm's rest taken as
the whole (M24), and the template's first average one more and gaps
charged by their index (M28, M30).

## Verification

Every arm prints the same output as `average.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ and prefix arms take 0.6 s, the suffix
arm 0.7 s, the struct arm 0.8 s, the template 1.0 s, the iter arm 1.7
s, and the differential 0.4 s.

## Benchmarks

The bench answers 20 cases of 10^5 values from 0 to 10^5 with the ★
arm in all five languages. Every implementation prints `20 cases of
10^5 values: checksum 987242454`.

BENCHTAB
