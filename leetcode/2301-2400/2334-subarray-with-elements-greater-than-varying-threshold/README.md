# 2334. Subarray With Elements Greater Than Varying Threshold

You are given an integer array `nums` and an integer `threshold`.

Find any subarray of `nums` of length `k` such that **every** element
in the subarray is **greater** than `threshold / k`.

Return *the **size** of **any** such subarray*. If there is no such
subarray, return `-1`.

A **subarray** is a contiguous non-empty sequence of elements within an
array.

```
nums = [1,3,4,3,1], threshold = 6    ->  3
nums = [6,5,6,5,8], threshold = 7    ->  1   (any of 1 to 5 is accepted)
```

**Constraints:** `1 <= nums.length <= 10^5`;
`1 <= nums[i], threshold <= 10^9`.

Any size that works may be returned. Every arm here returns the
largest, so that their answers can be compared line by line; for the
second example that is 5.

A subarray of length `k` works when its least element times `k`
exceeds the threshold. If one with least element `nums[i]` works, so
does the longest subarray in which `nums[i]` is the least, which runs
between the nearest smaller elements on either side of `i`. So the
largest size that works is the widest of those runs whose least element
passes, and a monotonic stack finds every run in one pass. The product
reaches `10^9 * 10^5`, so it is an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `threshold.kara` ★ | a monotonic stack: each index popped by the first value after it no larger sets its right edge, and the index under it on the stack is its left; the widest run whose least times width passes. O(n) |
| `threshold_naive.kara` | every subarray: from each start the end moves right keeping the least so far, and every length that passes is a candidate. O(n^2) |
| `threshold_union.kara` | union-find: the indices taken largest value first, each joined to the neighbours already taken, so the run it lands in holds no smaller value and its own is the least; the run's size times the value against the threshold. O(n log n) |
| `threshold_split.kara` | divide and conquer: a range's least element is the least of the whole range, so the range's length is tried against it, then the parts on either side of it. O(n log n) on random values, O(n^2) at worst |
| `threshold_iter.kara` | iterators: each index's nearest smaller element on the left from `rev` and `find`, on the right from `find`, `map`ped to its run; the runs that pass kept by `filter`, and the widest by `max`. O(n^2) at worst |
| `threshold_solution.kara` | LeetCode's Rust template: `vec!` edges of `i32`, a `Vec<usize>` stack read through `while let Some(&top) = stack.last()`, and the product widened to `i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; no size
that works; one element just short and just over; the rising run 1 to
100 against 2500; 2000 values up to `10^9` against `10^9`; then 2000
random cases of 1 to 12 values from 1 to 20, threshold 1 to 60, with a
checksum and how many have a size. `threshold.py` mirrors the ★ arm and
its output is byte-identical.

`karac fix` carries the template in one call, reporting 23 edits.
`check` first reports ten errors and offers 16 edits for them:
`struct Solution;` to `struct Solution {}`; the eight brackets of the
four `Vec<..>`; `Vec::new` to `Vec.new`; the two `Some(&top)` from
`stack.last()` to `Some(top)` from `stack.last().cloned()`, two edits
each, as the `&` there copies the value out of a borrowed `Some`; the
`&` of `|&x|` dropped; and `Solution::` to `Solution.` in the harness's
wrapper. The other seven follow from those: the two `vec!` to
`Vec.filled`; the stack's `Vec[usize]` to `Vec[i64]`, since an index is
an `i64`; `ans` annotated `i32`, as its `-1` would otherwise be an
`i64` against the `i32` answer; the two `as i64` that widen the product
and the threshold dropped, since `i32` widens to `i64` on its own; and
the wrapper's `as i64` on the answer dropped likewise. The `i as i32`
and `top as i32` that fill the edges stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every length `k` from `n` down, and every subarray of that
length, each element held to being greater than `threshold / k`, read
as the fraction it is, so that the element times `k` must exceed the
threshold; the first length with a subarray that passes is the answer.
No stack and no runs. It checks 300 random cases of 1 to 8 values from
1 to 10, threshold 1 to 40; then 30 of up to 30 values from 1 to 3, so
that equal values run together, threshold 1 to 60; then 30 of up to
300 values up to `10^9`, threshold up to `10^9`. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | up to 30 values, the answer is the literal reading's |
| P2 | the answer is -1, or from 1 to `n` and some subarray of that length passes |
| P3 | the values reversed: the same answer |
| P4 | the threshold one lower: no smaller an answer; just below the least value times `n`, where that is at most `10^9`: `n` |
| P5 | no length longer than the answer has a subarray that passes |
| P6 | each arm agrees with at least three of the other five |

P4's second half holds because the whole array then passes. P2 and
P5 together are the literal reading for any size of case: the answer
passes, and nothing longer does.

The differential prints `360 cases: checksum 734350070, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and holds each element against `Fraction(threshold, k)`.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the width one wider | P1 155, P2 185, P4 354, P6 185 |
| M4 | ★: a product equal to the threshold passing | P1 9, P2 9, P6 9 |
| M5 | ★: the last passing width, not the widest | P1 49, P3 87, P4 151, P5 77, P6 77 |
| M8 | naive: each length one short | P1 104, P4 354, P5 133, P6 133 |
| M9 | naive: the first passing length returned | P1 71, P3 59, P4 152, P5 99, P6 99 |
| M10 | naive: the last start never tried | P1 5, P3 1, P4 39, P5 5, P6 5 |
| M13 | union: only the left neighbour joined | P1 85, P3 82, P4 283, P5 114, P6 114 |
| M14 | union: a run never growing | P1 97, P4 315, P5 126, P6 126 |
| M15 | union: a neighbour joined before it is taken | P1 105, P2 123, P6 123 |
| M17 | split: the least sought from the third element | P1 25, P2 27, P3 39, P6 27 |
| M19 | split: the right part never tried | P1 17, P3 38, P5 29, P6 29 |
| M20 | split: a single element never tried | P1 7, P4 39, P5 7, P6 7 |
| M22 | iter: the left edge sought from the start | P1 89, P2 105, P3 115, P6 105 |
| M23 | iter: the right edge defaulting one short | P1 85, P3 43, P4 354, P5 103, P6 103 |
| M24 | iter: an equal value taken as an edge on both sides | P1 34, P4 91, P5 34, P6 34 |
| M28 | solution: the right edge one further | P1 42, P2 54, P3 61, P6 54 |
| M29 | solution: the threshold doubled | P1 60, P4 354, P5 77, P6 77 |

P1 and P6 kill all seventeen, P4 and P5 eleven each, P3 nine and P2
six. P2 and P5 split the literal reading between them: P2 fails where
an edit answers a size no subarray reaches, a run read too wide or a
product equal to the threshold let through, and P5 where it answers a
size short of the largest, a run read too narrow or a passing run
missed. P4's second half, the whole array passing once the threshold
is just below its least value times `n`, fails for every edit that
cannot reach the full width: a length or a run cut short, a start or a
single element never tried, the threshold doubled. P3, the values
reversed, fails where an edit treats the two sides of a run unalike.

Of the thirty-one, fourteen were not kept. Three are equivalent and
killed by nothing. An equal value left on the stack in the ★ (M1) and
template (M27) arms cuts short the runs of all but the first of a
stretch of equal values, and the first, whose left edge is still the
nearest smaller value and whose right edge is too, keeps the full run.
The union arm's size read at the index, not its root (M16), reads the
same number, since the index just taken is the root that every join
in its step keeps. The ★ arm's left edge never recorded (M2)
and the template's (M31) fail alike, and so do the ★ arm's right edges
left at `n` (M6) and the naive arm's least taken at the start alone
(M7), and the naive arm's most taken, not the least (M11), and the
union arm's values taken smallest first (M12); none of those six is
kept. The split arm's length tried one short (M18) and the template's
least passing width (M30), which with its start at -1 never leaves it,
fail as the naive arm's each length one short (M8), and the iter arm's
width without the minus one (M26) as the ★ arm's width one wider (M3). The
split arm's width counted from the least (M21) and the iter arm's
narrowest passing width (M25) fail apart from every kept one, and were
left out to keep three to an arm.

P5 was first every value and the threshold doubled, which no edit
failed, since every one of them is scale-free; it was replaced by the
check that no longer length passes.

## Verification

Every arm prints the same output as `threshold.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.25 to 0.4 s but the naive
arm, whose every subarray of the 2000 values makes 1.0 s. The
differential takes 3.7 s there and 0.6 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values from 1 to `10^9` once, from
a scramble that never repeats, then makes 5 passes, array `a` in pass
`p` against the threshold `((10a + p) * 7919 mod 1000 + 1) * 10^6`,
with the ★ arm in all five languages. Every implementation prints `5
passes over 10 arrays of 10^5 values: checksum 263514796`. Each
allocates its two edge arrays and its stack afresh for every call, as
64-bit integers.

BENCHTAB
