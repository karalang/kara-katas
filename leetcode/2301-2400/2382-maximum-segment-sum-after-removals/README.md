# 2382. Maximum Segment Sum After Removals

You are given two **0-indexed** integer arrays `nums` and `removeQueries`,
both of length `n`. For the `i`th query, the element in `nums` at the
index `removeQueries[i]` is removed, splitting `nums` into different
segments.

A **segment** is a contiguous sequence of **positive** integers in
`nums`. A **segment sum** is the sum of every element in a segment.

Return *an integer array* `answer`*, of length* `n`*, where* `answer[i]`
*is the **maximum** segment sum after applying the* `i`*th removal.*

**Note:** The same index will **not** be removed more than once.

```
nums = [1,2,5,6,1], removeQueries = [0,3,2,4,1]  ->  [14,7,2,2,0]
nums = [3,2,11,1], removeQueries = [3,2,1,0]     ->  [16,5,3,0]
```

**Constraints:** `n == nums.length == removeQueries.length`;
`1 <= n <= 10^5`; `1 <= nums[i] <= 10^9`; `0 <= removeQueries[i] < n`;
all the values of `removeQueries` are **unique**.

Removing only splits segments, which is hard to track; putting values
back only joins them. Undone from the last removal, each value put back
joins the segments on either side, and the largest sum so far is the
answer before it was put back.

## Approaches

| file | mechanism |
|---|---|
| `segments.kara` ★ | the removals undone in reverse with a union-find, a root keeping its segment's sum, the largest sum so far each answer. O(n α(n)) |
| `segments_ends.kara` | the removals undone in reverse, each segment known by its two ends: a value put back takes the outer ends of its neighbours' segments, and the sum is a difference of prefix sums. O(n) |
| `segments_sorted.kara` | forward, with a `SortedMap` of segments from start to end and a `SortedMap` counting the sums; a removal finds its segment by `floor`, splits it, and the answer is the counts' last key. O(n log n) |
| `segments_rescan.kara` | every segment summed afresh after each removal, a walk along the values. O(n^2) |
| `segments_iter.kara` | iterators: the removals as a running set of flags by `scan`, each folded with the values by `zip` and `fold` into the running segment and the largest. O(n^2) |
| `segments_solution.kara` | LeetCode's Rust template: a union-find over `Vec<usize>` with a recursive `Self::find` taking `&mut Vec<usize>`, and `vec![0i64; n]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; one value;
3000 values of `10^9` removed from the left, and from the middle
outward, and 3000 random values removed in a random order, as
checksums; then 2000 random arrays of 1 to 40 values, removed in a
random order, with a checksum and the sum of the first answers. Values
up to `10^9` are drawn from 30 random bits, two draws of the harness's
15-bit generator. `segments.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random arrays
against every segment summed after each removal.

The sorted arm takes its segment as `let (l, r) =
segments.floor(x).unwrap();` and then removes it from `segments`.
`check` reports that `remove` mutably borrows `segments` while `l` and
`r` still borrow it, three times, and suggests a copy, but offers no
machine fix, though `l` and `r` are `i64`s and the copy is all it
takes (B-2026-11-21-46). The arm carries the copy by hand, `let (l, r) =
(l.clone(), r.clone());`.

`check` first reports 20 errors on the template, and `karac fix` carries
it in one call, reporting 41 edits: `struct Solution;` given its
braces; `Vec<..>` its brackets; `&mut Vec<usize>` written `mut ref
Vec[i64]` and the calls' `&mut p` written `mut p`; `usize` written
`i64`, with the `as usize` on a query written `as i64`; `Self::find`
and `Solution::` written with a dot; `vec![0i64; n]` written
`Vec.filled(n, 0)` and the `0i64` suffixes dropped; and the `&` of the
wrapper's `|&v|` dropped. The recursive `find`, the `sum[r] > 0` test
for a neighbour already back (every value is at least 1) and the
`as i32` / `as i64` casts stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: after each removal, every range of places checked for a
removed one, the sum of each range with none, and the largest kept. No
union-find and no running segment. It checks 300 random arrays of 1 to
12 values, which the literal reading answers; then 30 of up to 300
values; then 30 of up to 300 values from 1 to 3, where many segments
tie. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 values, the answers are the literal reading's |
| P2 | `n` answers, never rising, the last 0 |
| P3 | the values and the removals mirrored: the same answers |
| P4 | every value doubled: every answer doubled |
| P5 | the first answer the larger sum on either side of the first removal; the one before the last the last value standing |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a removal only splits segments, so no sum grows, and
after the last removal nothing is left. P3 holds because mirroring the
array mirrors every segment and keeps its sum, and P4 because every
segment's sum doubles with its values.

The differential prints `360 cases: checksum 821340263, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and sums every range after each removal. On a failure it
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
| M1 | ★: the answer one place late | P1 273, P2 332, P5 332, P6 332 |
| M2 | ★: a left neighbour at place 0 never joined | P1 65, P3 160, P5 71, P6 83 |
| M3 | ★: the largest not kept | P1 188, P2 247, P5 66, P6 247 |
| M7 | ends: the right segment ending at its first value | P1 159, P3 249, P5 216, P6 218 |
| M8 | ends: the left end never told | P1 182, P3 273, P5 199, P6 241 |
| M9 | ends: the sum one place short | P1 273, P3 293, P5 332, P6 332 |
| M12 | sorted: a sum's count never taken down | P2 30, P5 30, P6 30 |
| M13 | sorted: the last answer the whole sum | P1 301, P2 360, P5 28, P6 360 |
| M14 | sorted: the ties counted into the answer | P2 14, P4 29, P6 29 |
| M17 | rescan: a removed value counted against the run | P1 238, P2 56, P3 332, P5 288, P6 297 |
| M19 | rescan: the value at place 0 never removed | P1 301, P2 360, P3 323, P5 195, P6 360 |
| M21 | rescan: the answer the last run | P1 247, P3 332, P5 291, P6 306 |
| M22 | iter: a removed odd place put back | P1 273, P2 332, P3 170, P5 294, P6 332 |
| M24 | iter: the fold starting from a run of one | P1 170, P3 332, P4 210, P5 185, P6 210 |
| M25 | iter: the values zipped one place on | P1 273, P3 332, P5 331, P6 332 |
| M27 | solution: a left neighbour of 1 never joined | P3 29, P4 27, P5 27, P6 27 |
| M31 | solution: a right neighbour's root left in place | P1 171, P3 236, P5 228, P6 230 |

P6 kills all seventeen, P5 sixteen, P1 fourteen, P3 twelve, P2 eight
and P4 three. P1 misses the sorted arm's sum's count never taken down
and ties counted into the answer (M12, M14) and the template's left
neighbour of 1 never joined (M27): each goes wrong only where two
segments have the same sum or a value is 1, which the 30 arrays of
values from 1 to 3 bring and the small random arrays almost never do.
P4, every value doubled, fails those last two and the iter arm's fold
from a run of one (M24), each of which adds or compares a fixed 1 that
does not double with the values. P3, the array mirrored, passes the
edits that are as wrong from either end, as the answer one place late
(M1) or the largest not kept (M3).

Of the thirty-one, fourteen were not kept. A join keeping the larger
sum in the ★ arm (M4), a value never marked back in the ends arm (M10),
each run a single value in the rescan arm (M20) and the largest only a
single value in the template (M29) all answer the largest single value,
and fail alike. The ★ arm's value put back one less and the sorted
arm's every value summed one less (M6, M16) fail alike, as do the first
removal never undone in the ★ arm and the template (M5, M30), and the
ends arm's last value left out of the prefix sums and the rescan arm's
last value never walked (M11, M18). The iter arm's largest the last run
(M26) fails as the rescan arm's answer the last run (M21). The sorted
arm's smallest sum the answer (M15), the iter arm's gone value starting
the run (M23) and the template's right neighbour found at the value
itself (M28) each fail apart from every kept one, and were left out to
keep three to an arm and two to the template. Three sorted-arm edits
were replaced: the left part keeping the removed place, the right
part's sum taking the removed value and a right part of one value
dropped each left a sum or a segment the next removal could not find,
and crashed on a missing key or an empty `floor`; they became M13, M14
and M16.

## Verification

Every arm prints the same output as `segments.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.8 to 7 s, but the iter arm 98
s: it folds all the values once per removal, a closure call each, over
the two 3000-value cases. The differential takes 20.7 s there and 1.1 s
under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values once from the harness's
generator, array `a`'s values from 1 to `10^a`, each with its own random
order of removals, then makes 10 passes over the 10 arrays, folding each
answer plus the pass into the checksum, with the ★ arm in all five
languages. Every implementation prints `10 passes over 10 arrays of 10^5
values: checksum 394866778`. Every implementation allocates its
union-find and its answers afresh in each call.

BENCHTAB
