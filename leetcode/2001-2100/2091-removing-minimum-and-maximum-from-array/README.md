# 2091. Removing Minimum and Maximum From Array

You are given a 0-indexed array of distinct integers `nums`.

There is an element in `nums` that has the lowest value and an element
that has the highest value. We call them the minimum and maximum
respectively. Your goal is to remove both these elements from the
array.

A deletion is defined as either removing an element from the front of
the array or removing an element from the back of the array.

Return the minimum number of deletions it would take to remove both the
minimum and maximum element from the array.

```
nums = [2,10,7,5,4,1,8,6]     ->  5
nums = [0,-4,19,1,8,-2,-3,5]  ->  3
nums = [101]                  ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^5 <= nums[i] <=
10^5`; the integers in `nums` are distinct.

Only the two places matter. With `i` the nearer to the front and `j` the
farther, the deletions either all come from the front (`j + 1`), all
from the back (`n - i`), or from the front up to `i` and from the back
down to `j` (`i + 1 + n - j`). One walk finds the places, O(n). The
approaches differ in how they find the places and choose among the
ways.

## Approaches

| file | mechanism |
|---|---|
| `deletions.kara` ★ | one `for` over the places keeping the least's and the greatest's in a `let mut (lo, hi)`, then the fewest of the three ways by `min`. O(n) |
| `deletions_position.kara` | by the library: the values from `iter().min()` and `max()`, their places from `position`, the fewest way from `[..].iter().min()`. O(n), three walks |
| `deletions_fold.kara` | one `fold` over `iter().enumerate()` carrying both places as a tuple, the three ways named `front`, `back` and `both`. O(n) |
| `deletions_split.kara` | every split: for each count `f` deleted from the front, the fewest from the back to reach whichever place the front left, the best of the `n + 1` counts by `map(..).min()`. O(n) |
| `deletions_ends.kara` | a `struct Ends` of a front, a back and a count, with `from_front`, `from_back` and `holds(place)`, walked for each of the three ways until neither place is held. O(n) a way |
| `deletions_solution.kara` | LeetCode's Rust template (`nums: Vec<i32>` returning `i32`, `(0usize, 0usize)` places from `iter().enumerate()`, `std::cmp::min`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more, each array and its deletions; then the sum and a checksum of the
deletions for 2000 random arrays of 1 to 100 distinct values from
-100000 on; then the constraints' largest, 100000 distinct values
shuffled, then in increasing order, and with the least and the greatest
both in the middle. `deletions.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way of deleting `f` values from the front and `b` from
the back, kept when the least and the greatest are both among those
deleted, and the fewest `f + b` kept. It checks 300 random arrays of 1
to 12 distinct values; then 20 in increasing order, and 20 in
decreasing. All 340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the deletions are the statement read literally |
| P2 | the array reversed takes the same deletions |
| P3 | every value negated takes the same deletions |
| P4 | the deletions are at least 1, at least 2 for two values or more, and at most a third of `2n + 2` |
| P5 | a new greatest value at the back takes the fewer of `lo + 2` and `n + 1 - lo`, `lo` the least value's place |
| P6 | each arm agrees with at least three of the other five |

P4's bound holds because the three ways add up to `2n + 2`, so the
fewest is at most a third of that.

The differential prints `340 arrays: checksum 530498317, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal deletions was checked against a Python reading of the
same arrays. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second value never looked at | P1 57, P2 76, P4 23, P5 71, P6 57 |
| M2 | ★: the two-ended way a deletion short | P1 152, P4 72, P5 185, P6 152 |
| M3 | ★: the greatest's place tracking the least | P1 236, P3 219, P4 122, P5 185, P6 236 |
| M4 | position: the most of the three ways | P1 316, P4 316, P5 309, P6 316 |
| M5 | position: the places not ordered | P1 169, P2 309, P3 309, P4 112, P6 169 |
| M6 | position: all from the front one short | P1 152, P2 167, P4 79, P5 31, P6 152 |
| M7 | fold: the greatest compared with the least | P1 139, P2 161, P3 166, P6 139 |
| M8 | fold: all from the back only to the farther | P1 245, P2 219, P4 140, P5 340, P6 245 |
| M9 | fold: the two-ended way a deletion long | P1 105, P4 11, P5 123, P6 105 |
| M10 | split: a place at the front count counted gone | P1 270, P2 144, P4 128, P5 185, P6 270 |
| M11 | split: the back one short | P1 266, P2 144, P4 131, P5 340, P6 266 |
| M12 | split: the most over the splits | P1 286, P4 286, P5 309, P6 286 |
| M13 | ends: the two-ended way from the front past the farther | P1 105, P4 79, P5 123, P6 105 |
| M14 | ends: a deletion from the back counted twice | P1 188, P2 208, P4 84, P5 309, P6 188 |
| M15 | ends: the best starting at `n - 1` | P1 54, P4 54, P5 31, P6 54 |
| M16 | solution: the adapter's values taken mod 3 | P1 190, P2 122, P4 44, P5 210, P6 190 |
| M17 | solution: the least found as the greatest | P1 254, P3 219, P4 151, P5 340, P6 254 |

P1 and P6 kill all seventeen, P4 sixteen, P5 fifteen, P2 nine, and P3
four. P4's bounds see nearly every edit, since a wrong count is soon
below 2 or above a third of `2n + 2`; it misses only M7, whose wrong
places still give a count inside them. P5 sees an edit to any of the
ways, as a new greatest at the back makes the two-ended and the
all-from-the-back ways the ones that count. P2, the array reversed, sees
what treats the front and the back unevenly: a way one short or long at
one end only (M6, M8, M11, M14), the places taken in the order found
(M5), the second value skipped (M1). P3, the values negated, swaps the
least and the greatest, so it sees an arm that confuses them: the
greatest tracking the least (M3) or the least found as the greatest
(M17), the places left unordered (M5) and the greatest compared with the
least (M7).

Of the thirty, thirteen were not kept, and none survives. Ten fail as a
kept one: the ★ arm's two-ended way left out and the ends arm's
two-ended way never tried as M13; the ★ arm's places not ordered and the
fold arm's not ordered when the greatest comes first as M5; the
position arm's greatest found as the least as M3; its `n - 1` offered as
a fourth way as M15; the split arm's back reaching the farther as M8;
the ends arm's front place counted gone as M10; the Rust arm's
two-ended way a deletion long as M9; its all from the front one short as
M6. Three are killed with checks of their own but were left out because
their arm keeps three or two: the fold arm's all from the back left out
(P1 70, P2 144, P4 56, P5 155), the split arm's front never left whole
(P1 70, P2 144, P4 15, P5 155), and the Rust adapter's answer one more
(P1 340, P4 127, P5 340).

## Verification

Every arm prints the same output as `deletions.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 1.3 s to 1.9 s, but for the split
arm's 6.0 s, which builds a two-place `Vec` for each of the `n + 1`
splits, and the differential 0.6 s (timed while other work shared the
machine).

No arm met a compiler gap. The Rust arm was written as LeetCode's Rust
template. `karac fix` carries it in three rounds of 16, 3 and 1 edits:
Rust's spellings (`Vec<i32>` to brackets, `let (mut lo, mut hi)` to `let
mut (lo, hi)`, the `&` of `&x` dropped, `std::cmp::min` to `min`, `struct
Solution;` to `struct Solution {}`, `Solution::` to `.`, the adapter's
`&Vec<i64>` to `ref`); then the `usize` suffixes of `(0usize, 0usize)`,
as Kāra's places are `i64`, and the adapter's `as i64`, which the `i32`
widens to anyway; then the adapter's `ref` parameter to a bare one,
which borrows already. The fixed arm reads as the template does.

## Benchmarks

The bench shuffles 20 arrays of 100000 distinct values, the
constraints' limit, and answers each 20 times with the ★ arm in all
five languages, the values in a growable array (a `Vec`, a `Vec`, a
slice, a `list`, a `malloc`'d buffer): 400 walks of `10^5` values.
Every implementation prints `400 answers: sum 11533420, checksum
434559771`.

BENCHTAB
