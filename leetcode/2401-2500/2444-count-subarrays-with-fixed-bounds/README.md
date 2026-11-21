# 2444. Count Subarrays With Fixed Bounds

You are given an integer array `nums` and two integers `minK` and
`maxK`.

A **fixed-bound subarray** of `nums` is a subarray that satisfies the
following conditions:

- The **minimum** value in the subarray is equal to `minK`.
- The **maximum** value in the subarray is equal to `maxK`.

Return *the **number** of fixed-bound subarrays*.

A **subarray** is a **contiguous** part of an array.

```
nums = [1,3,5,2,7,5], minK = 1, maxK = 5  ->  2
nums = [1,1,1,1], minK = 1, maxK = 1      ->  10
```

**Constraints:** `2 <= nums.length <= 10^5`;
`1 <= nums[i], minK, maxK <= 10^6`.

A subarray ending at `i` is fixed-bound exactly when it starts after the
last value outside `[minK, maxK]` and no later than both the last `minK`
and the last `maxK` up to `i`. So one pass that keeps those three last
places adds, at each end, the number of starts between them, and the
whole count is O(n). The counts reach `n (n + 1) / 2`, past an `i32`, so
the answer is an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `bounds.kara` ★ | one pass keeping the last place outside the bounds, the last `min_k` and the last `max_k`, adding `(min(last_min, last_max) - bad).max(0)` at each end. O(n) |
| `bounds_naive.kara` | the statement read directly: every start, and every end from it with the running minimum and maximum, counted when they are the bounds. O(n^2) |
| `bounds_window.kara` | the array split at every value outside the bounds, and each run counted by a sliding window whose left end advances while the window still holds both bounds, every start before it then working. O(n) |
| `bounds_exclude.kara` | inclusion and exclusion: the subarrays wholly within the bounds, less those avoiding `min_k`, less those avoiding `max_k`, plus those avoiding both, each family counted by the run of allowed values ending at each place. O(n) |
| `bounds_iter.kara` | iterators: a `fold` over `enumerate` carrying the three last places and the count as one tuple. O(n) |
| `bounds_solution.kara` | LeetCode's Rust template: the count and the three places declared together by `let (mut ans, mut bad, mut mn, mut mx): (i64, ..) = (..)`, the values read by `for (i, &x) in ..enumerate()`, `i as i64`, and `0.max(..)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; bounds the
wrong way round; one value at `10^6`, the constraints' largest; then
5000 values all equal against bounds equal to them; 5000 random values
from 1 to 5 against 1 and 5; and 5000 random values from `2 * 10^5` to
`8 * 10^5`, every 50th one `10^6`, against `2 * 10^5` and `8 * 10^5`,
four places set to the bounds; and 3000 random arrays of 1 to 10 values
from 1 to 4, bounds from 1 to 4, as a checksum and the total. The
largest cases hold 5000 values, not the constraints' `10^5`, because the
naive arm tries every subarray. `bounds.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked on 30000 random
arrays of 1 to 12 values against every subarray's minimum and maximum.

`check` first reports 8 errors on the template, and `karac fix` carries
it in one call, reporting 11 edits: the brackets of `Vec<i32>`; the four
`mut`s inside the tuple pattern moved before it as one `let mut (..)`,
which makes every binding mutable; the `&` dropped from the pattern
`&x`; `||` written `or`; `struct Solution;` given its braces; and, once
the template parses, the cast in `let i = i as i64` dropped, since the
index is already an `i64`, which leaves `let i = i` standing. The tuple
type `(i64, i64, i64, i64)`, `mn.min(mx)` and `0.max(..)` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray by its two ends, its minimum and maximum found
by walking it afresh, and counted when they are the bounds. No last place
is kept. It checks 300 random arrays of 1 to 10 values from 1 to `m`,
`m` from 1 to 5, bounds from 1 to `m`; then 30 of 20 to 60 values from 1
to 6 against 2 and 5; then 30 of 20 to 60 values from 1 to 3 against 2
and 2 or 1 and 3. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the array reversed: the same answer |
| P3 | a value below `min_k` put first: the same answer |
| P4 | every value taken from 2000, the bounds swapped likewise: the same answer |
| P5 | the array, a value above `max_k`, the array again: twice the answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because reversing keeps every subarray's values. P3 holds
because no fixed-bound subarray can hold the new value. P4 holds
because `2000 - x` turns minima into maxima. P5 holds because no
fixed-bound subarray can cross the value between the copies.

The differential prints `360 cases: checksum 418111252, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and takes every subarray's minimum and maximum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value above max_k let through | P1 89, P4 122, P5 213, P6 89 |
| M2 | ★: the later bound used | P1 111, P6 111 |
| M3 | ★: a negative count added | P1 232, P3 360, P5 360, P6 232 |
| M8 | naive: the minimum the last value | P1 113, P2 115, P3 183, P4 142, P6 113 |
| M9 | naive: either bound enough | P1 247, P3 249, P5 274, P6 247 |
| M11 | naive: one end at most per start | P1 169, P2 56, P6 169 |
| M13 | window: one start at most per end | P1 172, P2 56, P6 172 |
| M14 | window: the runs never cut | P1 116, P2 115, P5 241, P6 116 |
| M15 | window: the last run left out | P1 150, P2 57, P5 150, P6 150 |
| M17 | exclude: those avoiding both never added back | P1 65, P6 65 |
| M18 | exclude: each place counting one | P1 187, P6 187 |
| M20 | exclude: the whole family taken twice | P1 249, P4 96, P6 249 |
| M22 | iter: a value below min_k let through | P1 80, P3 190, P4 122, P6 80 |
| M23 | iter: one start fewer | P1 231, P2 56, P6 231 |
| M26 | iter: the bounds swapped each step | P1 86, P6 86 |
| M28 | solution: nothing ever outside | P1 161, P3 274, P5 274, P6 161 |
| M29 | solution: both bounds seen at 0 | P1 79, P2 77, P3 79, P5 79, P6 79 |


P1 and P6 kill all seventeen, P2 and P5 seven each, P3 six and P4
four.

Fourteen are not kept. Four fail exactly as a kept one: the ★ arm's one
start at most per end (M6) as the window arm's (M13); the window arm's
window shrunk while either is held and the template's later bound used
(M12, M27) as the ★ arm's later bound used (M2), each needing a start
no later than the last of the two bounds rather than the first; and the
exclude arm's every run one long (M21) as its each place counting one
(M18). Seven more fall into groups that fail alike and apart from every
kept one, and none is kept: the ★, naive and iter arms' first place
counted bad, first start skipped and first place counted bad (M4, M10,
M24), each losing every subarray that starts at 0; the ★ and window
arms' value at both bounds never `max_k` and the naive arm's subarrays
of one never tried (M5, M16, M7), each wrong only when `min_k` equals
`max_k`; and the exclude arm's `max_k` itself outside and the iter
arm's every count doubled (M19, M25), each wrong wherever the answer is
not 0. The template's `max_k` taken for `min_k` and one start more
(M30, M31) fail apart from every kept one and were left out because the
template keeps its share already.

The first run's P3, every value and both bounds raised by one constant,
killed no mutant: every arm only compares values with each other and
with the bounds, so no edit to one could notice the shift. It was
replaced by a value below `min_k` put first, and every mutation was run
again against the new differential.

## Verification

Every arm prints the same output as `bounds.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 0.5 s, but for the naive
arm, which tries every subarray: on the cases of 5000 values that is
`1.25 * 10^7` ends each, and it takes 33 s there, 2.5 s under `karac
__mir-llvm-asan` and 0.4 s under `karac run`. The differential takes
1.1 s under `karac __mir-run`, 0.6 s under `karac __mir-llvm-asan` and
0.5 s under `karac run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values from 1 to 20, the
constraints' longest, once from its own generator, and answers them
against 3 and 17. It then makes 100 passes; each sets one value of
every array, so no answer can be carried from one pass to the next,
then answers every array, folding the answer plus the pass into the
checksum. The bench uses the ★ arm, the three last places, in all five
languages. Every implementation prints `100 passes over 10 arrays of
10^5 values: checksum 974321014`.

BENCHTAB
