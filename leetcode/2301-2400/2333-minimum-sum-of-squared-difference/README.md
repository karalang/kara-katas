# 2333. Minimum Sum of Squared Difference

You are given two positive **0-indexed** integer arrays `nums1` and
`nums2`, both of length `n`.

The **sum of squared difference** of arrays `nums1` and `nums2` is
defined as the **sum** of `(nums1[i] - nums2[i])^2` for each
`0 <= i < n`.

You are also given two positive integers `k1` and `k2`. You can modify
any of the elements of `nums1` by `+1` or `-1` at most `k1` times.
Similarly, you can modify any of the elements of `nums2` by `+1` or
`-1` at most `k2` times.

Return *the minimum **sum of squared difference** after modifying array
`nums1` at most `k1` times and modifying array `nums2` at most `k2`
times*.

**Note:** You are allowed to modify the array elements to become
**negative** integers.

```
nums1 = [1,2,3,4], nums2 = [2,10,20,19], k1 = 0, k2 = 0    ->  579
nums1 = [1,4,10,12], nums2 = [5,8,6,9], k1 = 1, k2 = 1     ->  43
```

**Constraints:** `n == nums1.length == nums2.length`;
`1 <= n <= 10^5`; `0 <= nums1[i], nums2[i] <= 10^5`;
`0 <= k1, k2 <= 10^9`.

A move on either side shrinks one gap `|nums1[i] - nums2[i]|` by 1, so
only the gaps and `k1 + k2` matter. Taking a gap `g` down to `g - 1`
saves `2g - 1`, more the larger the gap, so every move is best spent on
a largest gap: the largest are brought down together, level by level,
until the moves run short, and the moves left take that many of them
one lower. The sum reaches `10^5 * (10^5)^2 = 10^15`, so it is an
`i64`.

## Approaches

| file | mechanism |
|---|---|
| `squares.kara` ★ | the gaps counted by size in a `Vec` of `10^5 + 1`; from the largest down, all the gaps at a size drop a level while the moves cover them, and the moves left take that many of the rest one lower. O(n + 10^5) |
| `squares_sorted.kara` | the gaps sorted largest first: the `width` largest brought down together to the next gap while the moves cover `width` times the step; where they run short, the moves left shared out evenly, the remainder one lower still. O(n log n) |
| `squares_search.kara` | a binary search on the cap: bringing every gap to at most `cap` costs the sum of the excesses, so the least cap the moves pay for is found by halving, and the moves left over take that many gaps at the cap one lower. O(n log 10^5) |
| `squares_heap.kara` | one move at a time: the gaps in a `PriorityQueue.max_first()`, each move taking the largest down by 1 until the moves run out or the largest is 0. O((n + k) log n) |
| `squares_iter.kara` | iterators: the gaps from `zip` and `map`; `scan` threads the running sum into the cost of bringing the `w` largest down to the next gap, `position` finds the first width the moves cannot pay for, and the gaps past it `map` to squares and `sum` |
| `squares_solution.kara` | LeetCode's Rust template: the gaps from `zip` with `&` patterns, `sort_unstable_by` largest first, and a `usize` walk bringing the largest down together; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; moves
enough to close every gap; no gap at all; one pair `10^5` apart with
`10^9` moves of `k1` alone; 2000 pairs up to `10^5` with 60000 moves;
then 2000 random cases of 1 to 12 pairs up to 30, `k1` and `k2` from 0
to 40, with a checksum and the sums in all. `squares.py` mirrors the ★
arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 26 edits.
`check` first reports 13 errors and offers 20 edits for them:
`struct Solution;` to `struct Solution {}`; the fourteen brackets of
the seven `Vec<..>`; the four `&` of the closures' patterns `|(&a, &b)|`
and `|&x|` dropped; and `Solution::` to `Solution.` in the harness's
wrapper. The other six follow from those: `sort_unstable_by` to
`sort_by`, since a stable sort is also an unstable one; the suffix of
`0usize` dropped, since an index is an `i64`; then the counted `while`
loop becomes a `for i in 0..n`, three edits that take its
`let mut i = 0;`, its condition and its `i += 1`, and the cast of
`(i + 1) as i64`, now already an `i64`, is dropped.

The bench first read each case as `let (nums1, nums2) = cases[c];`,
which would move a tuple of two `Vec`s out of an index. `karac check`
refuses it and `karac fix` writes `ref cases[c]`, one edit.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to spend at most `k1` moves of `+1` or `-1` on
`nums1` and at most `k2` on `nums2`, each value's change tried from
`-k` to `k` with the rest left for the values after it, and the least
sum of squared differences kept. No gaps and no greed. It checks 300
random cases of 1 to 4 pairs up to 8, `k1` and `k2` from 0 to 3; then
30 of up to 12 pairs up to 30 with up to 400 moves, often enough to
close every gap; then 30 of up to 300 pairs up to `10^5` with up to
20000 moves. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 4 pairs and 3 moves a side, the answer is the literal reading's |
| P2 | the answer is at most the sum of the squared gaps, at least the gaps' sum less the moves, squared, over `n`, and 0 when the moves cover every gap |
| P3 | `nums1` and `nums2` swapped and both reversed: the same answer |
| P4 | every value 7 higher and `k1` and `k2` traded: the same answer |
| P5 | one move more saves no more than the move before it, and an odd amount or nothing |
| P6 | each arm agrees with at least three of the other five |

P2's lower bound is the mean's: `n` gaps whose sum is at least `S - k`
have squares summing to at least `(S - k)^2 / n`. P5 holds because the
best move takes a largest gap `g` down by 1 and saves `2g - 1`, odd,
and the largest gap never grows. It is checked with one move more on
`k1` and then one more on `k2`, so both sides' moves are counted.

The differential prints `360 cases: checksum 495088922, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and takes the least over `itertools.product` of every
change to each side. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a gap taken as the plain difference, floored at 0 | P1 200, P2 208, P3 253, P6 230 |
| M2 | ★: the largest gap never recorded | P1 242, P2 272, P6 272 |
| M5 | ★: the moves `k1` alone | P1 204, P2 45, P4 273, P6 244 |
| M7 | sorted: the gaps sorted smallest first | P1 104, P6 134 |
| M8 | sorted: the moves left over not shared out | P1 125, P5 144, P6 155 |
| M11 | sorted: a step costing one gap fewer | P1 233, P2 231, P5 58, P6 263 |
| M12 | search: the cap searched up to 1000 | P2 30, P6 30 |
| M13 | search: each excess one more | P1 200, P2 25, P5 72, P6 230 |
| M15 | search: a cap of 1 taken as nothing left | P1 42, P2 42, P5 37, P6 42 |
| M17 | heap: the moves stopped at a gap of 1 | P1 26, P2 47, P6 55 |
| M18 | heap: each move taking two | P1 248, P2 256, P5 219, P6 307 |
| M21 | heap: the moves `k2` alone | P1 201, P2 36, P4 273, P5 308, P6 242 |
| M24 | iter: a width the moves fall one short of taken as paid | P1 66, P2 45, P5 42, P6 66 |
| M25 | iter: the rest skipping a gap too many | P1 125, P2 67, P5 51, P6 155 |
| M26 | iter: the spent cost read a width on | P1 149, P2 101, P5 126, P6 178 |
| M28 | solution: the last gap never reached | P1 94, P2 94, P5 18, P6 94 |
| M29 | solution: the moves `k1` counted twice | P1 202, P2 110, P4 250, P5 256, P6 236 |

P6 kills all seventeen, P1 sixteen, P2 fifteen, P5 eleven, P4 three
and P3 one. P1 misses the cap searched only up to 1000, which matters
only for gaps far past the 8 the literal reading reaches, and which
P2's upper bound catches on the large cases. P2 fails for a sum above the
squared gaps, below the mean's bound, or not 0 once the moves cover
every gap, which most miscounts reach; it misses the edits that still
spend the moves on large gaps, only not the largest: the gaps sorted
smallest first and the moves left over not shared out. P5, each move
saving no more than the one before, fails where an edit spends a move
badly at one count of moves and well at the next. P4, the values moved
and `k1` and `k2` traded, fails only where an edit counts one side's
moves differently from the other's: `k1` alone, `k2` alone, and `k1`
counted twice. P3, the arrays swapped and reversed, fails only where
the sign of a difference matters, a gap taken as the plain difference.

Of the thirty-one, fourteen were not kept. The moves left over not
spent in the ★ arm (M3), the remainder not taken one lower in the
sorted arm (M9) and the moves left over ignored in the search arm (M14)
fail alike, and none is kept. The gaps sorted smallest first in the
iter (M22) and template (M27) arms fail as the sorted arm's (M7); the
iter arm's running sum a gap ahead (M23) as the sorted arm's step
costing one gap fewer (M11), and the sorted arm's first gap past the
width left out (M10) as the iter arm's rest skipping a gap too many
(M25). The ★ arm's squares summed from gap 2 (M4) and each gap counted,
not squared (M6), the search stepping two past a cap too low (M16), the
heap arm's one move fewer (M19) and smallest gap taken (M20), and the
template's width one wider (M30) and rest summed from the levelled gap
(M31) fail apart from every kept one, and were left out to keep three
to an arm.

## Verification

Every arm prints the same output as `squares.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the sorted, search, iter and template arms take
0.2 to 0.5 s; the heap arm, one move at a time, 2.6 s; and the ★ arm
4.7 s, as it fills its `10^5 + 1` counts afresh for each of its 2006
calls. The differential takes 27 s there, most of it the ★ arm's counts
and the literal reading's every change, and 0.8 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds 10 cases of `2 * 10^4` pairs up to `10^5` once, from a
scramble that never repeats, then makes 10 passes, case `c` in pass `p`
with `k1 = (10c + p) * 3 * 10^6` modulo `4 * 10^8` and
`k2 = (7p + c) * 5 * 10^6` modulo `3 * 10^8`, with the ★ arm in all
five languages. Every implementation prints `10 passes over 10 cases of
2*10^4 pairs: checksum 316209067`. Each allocates the `10^5 + 1` counts
afresh for every call, as the arm does, and walks them as 64-bit
integers.

BENCHTAB
