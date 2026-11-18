# 2302. Count Subarrays With Score Less Than K

The **score** of an array is defined as the **product** of its sum and
its length.

- For example, the score of `[1, 2, 3, 4, 5]` is `(1 + 2 + 3 + 4 + 5) *
  5 = 75`.

Given a positive integer array `nums` and an integer `k`, return *the
**number of non-empty subarrays** of* `nums` *whose score is
**strictly less** than* `k`.

A **subarray** is a contiguous sequence of elements within an array.

```
nums = [2,1,4,3,5], k = 10   ->  6
nums = [1,1,1], k = 5        ->  5
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^5`;
`1 <= k <= 10^15`.

The numbers are positive, so a subarray's score grows as it widens: if
a subarray scores under `k`, so does every subarray inside it. For each
right end, the starts that score under `k` are a run ending at the
right end, and the run's first start only moves right as the right end
does. A sliding window counts them all: O(n). The count reaches
`n (n + 1) / 2`, about `5 * 10^9`, and a score `10^15`, so both are
`i64`.

## Approaches

| file | mechanism |
|---|---|
| `count.kara` ★ | a window over indices: each element joins at the right, a `while` lets elements go at the left until the score is under `k`, and the window's length is added |
| `count_naive.kara` | every subarray scored: for each start the sum grows one element at a time, and each end whose sum times length is under `k` counts. O(n^2) |
| `count_search.kara` | prefix sums, and for each end a binary search for the first start whose score is under `k`; every start from there counts. O(n log n) |
| `count_deque.kara` | the window kept as a `VecDeque[i64]` of its elements: `push_back` each one and `pop_front` while the score is `k` or more, its `len()` the length |
| `count_iter.kara` | `(0..n).fold((0, 0, 0), ..)` of the window's left end, sum and count, the closure narrowing the window with a `while` |
| `count_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `let (mut ans, mut sum, mut l) = (0i64, 0i64, 0usize)` and `as i64` at each widening; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; `k = 1`,
which no subarray is under; a `k` every subarray is under; one
element; 2000 elements of `10^5` with `k = 10^15`, which every one of
the 2001000 subarrays is under; then 2000 random arrays of 1 to 60
elements from 1 to 20 with `k` from 1 to 3000, with a checksum and the
count in all. `count.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one call, reporting 14 edits:
`struct Solution;` to `struct Solution {}`; the brackets of
`Vec<i32>`; the three `mut`s of `let (mut ans, mut sum, mut l)` taken
out of the pattern and one put before it, `let mut (..)`, four edits;
the suffixes of `0i64`, `0i64` and `0usize` dropped, since each
literal takes its type from its use; and the four `as i64` dropped,
since `nums[r]` widens from `i32` and a length is already an `i64`.
Dropping `((r - l + 1) as i64)` leaves `((r - l + 1))`, its inner
parentheses now doubled, and `ans += (r - l + 1)` keeps its own.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray, by its start and end, has its sum taken
afresh from its elements and its score as that sum times its length,
and those under `k` are counted. No window, no prefix sums. It checks
300 random arrays of 1 to 30 elements from 1 to 20 with `k` from 1 to
3000; then 30 whose `k` is the score of one of their own subarrays, so
that some score meets it exactly; then 30 of up to 300 elements up to
`10^5` with `k` up to `10^15`. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is from 0 to `n (n + 1) / 2` |
| P3 | the array reversed: the same answer |
| P4 | `k` doubled: at least as many |
| P5 | the array, then `k` itself as one more element, then the array again: twice the answer |
| P6 | each arm agrees with at least three of the other five |

P5's middle element scores `k` alone, so no subarray under `k` holds
it, and the two copies count apart. It is checked only where `k` is at
most `10^5`, an element the constraints allow: in the last 30 cases `k`
reaches `10^15`, and the template, which takes `Vec<i32>`, would wrap
such an element.

The differential prints `360 cases: checksum 563297615, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and counts with a running sum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a score equal to `k` kept | P1 39, P5 330, P6 39 |
| M3 | ★: the sum kept when the left element goes | P1 220, P3 202, P5 325, P6 220 |
| M4 | ★: the sum and length added | P1 226, P6 226 |
| M8 | naive: the sum never reset | P1 256, P3 179, P5 325, P6 256 |
| M9 | naive: single elements never scored | P1 358, P3 145, P5 323, P6 358 |
| M11 | naive: each subarray counted twice | P1 358, P2 315, P6 358 |
| M13 | search: the last start never tested | P1 8, P5 330, P6 8 |
| M14 | search: the prefix sums not summed | P1 229, P3 34, P5 330, P6 229 |
| M16 | search: the first end skipped | P1 355, P3 5, P5 325, P6 355 |
| M18 | deque: the newest element let go | P1 195, P3 177, P4 1, P5 328, P6 195 |
| M20 | deque: the sum the largest element | P1 228, P3 28, P5 327, P6 228 |
| M21 | deque: one element let go at most | P1 178, P3 170, P5 328, P6 178 |
| M22 | iter: the window started at 1 | P1 358, P3 170, P5 323, P6 358 |
| M24 | iter: the sum not carried | P1 228, P3 34, P5 327, P6 228 |
| M26 | iter: the left end not carried | P1 213, P3 203, P4 2, P5 330, P6 213 |
| M30 | solution: the first element skipped | P1 328, P3 185, P5 330, P6 328 |
| M31 | solution: the score doubled | P1 252, P6 252 |

P1 and P6 kill all seventeen, P5 fourteen, P3 twelve, P4 two and P2
one. P5, the array twice around an element of `k`, kills nearly
everything: that element alone scores exactly `k`, so an arm that keeps
a score equal to `k` counts it, and any error that leans on where the
array starts or ends shows twice over. It misses only the edits whose
error is the same on each side and nothing at the join: the sum and
length added, each subarray counted twice, and the score doubled. P3,
the array reversed, fails wherever the window's sum or its left end
goes wrong, which depends on the order of the elements. P4, `k`
doubled, fails only where an edit can lose subarrays as `k` grows:
the deque arm letting go its newest element, and the iter arm's left
end not carried, both of which narrow from the wrong end. P2 fails only
for each subarray counted twice.

Of the thirty-one, fourteen were not kept. A score equal to `k` kept or
counted in the naive (M7), search (M12), deque (M17), iter (M25) and
template (M27) arms fails as the ★ arm's (M1); the subarray ending at
the right end not counted in the ★ (M2), iter (M23) and template (M28)
arms and the deque arm's one subarray fewer each time (M19) all alike,
and none is kept; the ★ arm's one element let go at most (M5) as the
deque arm's (M21); the window one short in its score in the ★ arm (M6)
and the naive arm's length one short (M10) alike, and neither is kept;
the search arm's length one long (M15) as the ★ arm's sum and length
added (M4); and the template's right element taken off (M29) as the
deque arm's newest element let go (M18).

## Verification

Every arm prints the same output as `count.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 to 0.4 s but the naive one,
which scores the 2001000 subarrays of the long case one by one, 1.1 s.
The differential takes 5.6 s there and 0.5 s under `karac
__mir-llvm-run`: the literal reading sums each subarray of its last 30
cases afresh, up to 300 elements long.

## Benchmarks

The bench builds 20 arrays of `10^5` numbers from 1 to `10^5` once,
then makes 30 passes over all of them with the ★ arm in all five
languages, array `a` in pass `p` with `k = 10^9 (a + 1) + p`, which
holds a window of about 140 to 630 elements. Every implementation
prints `30 passes over 20 arrays of 10^5: checksum 291977503`. Each
keeps the numbers as 64-bit integers in an array, a `Vec<i64>`, a
`[]int64` and a list.

BENCHTAB
