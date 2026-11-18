# 2234. Maximum Total Beauty of the Gardens

Alice is a caretaker of `n` gardens and she wants to plant flowers to
maximize the total beauty of all her gardens.

You are given a **0-indexed** integer array `flowers` of size `n`, where
`flowers[i]` is the number of flowers already planted in the `i`th
garden. Flowers that are already planted **cannot** be removed. You are
then given another integer `newFlowers`, which is the **maximum** number
of flowers that Alice can additionally plant. You are also given the
integers `target`, `full`, and `partial`.

A garden is considered **complete** if it has **at least** `target`
flowers. The **total beauty** of the gardens is then determined as the
**sum** of the following:

- The number of **complete** gardens multiplied by `full`.
- The **minimum** number of flowers in any of the **incomplete**
  gardens multiplied by `partial`. If there are no incomplete gardens,
  then this value will be `0`.

Return *the **maximum** total beauty that Alice can obtain after planting
at most* `newFlowers` *flowers.*

```
flowers = [1, 3, 1, 1], newFlowers = 7,  target = 6, full = 12, partial = 1  ->  14
flowers = [2, 4, 5, 3], newFlowers = 10, target = 5, full = 2,  partial = 6  ->  30
```

**Constraints:** `1 <= flowers.length <= 10^5`;
`1 <= flowers[i], target <= 10^5`; `1 <= newFlowers <= 10^10`;
`1 <= full, partial <= 10^5`.

Sorted, with every garden capped at the target, the incomplete gardens
are always a prefix: completing the largest costs least, and the
smallest set the minimum. So every split is tried, the gardens from `c`
on completed at a cost kept as a running sum, and the flowers left raise
the first `c` as high as they go, below the target. The ★ arm finds
that level by a binary search on the level, each level's cost by a
binary search for how many gardens lie below it and the prefix sums.
O(n log n log target).

## Approaches

| file | mechanism |
|---|---|
| `beauty.kara` ★ | the splits walked from none completed to all, a `while` loop that `break`s once completing costs too much; the level a binary search on the level, with an inner binary search over the prefix sums |
| `beauty_pointer.kara` | the same walk with `(0..=n).rev()`: the flowers left fall as more gardens are completed, so the number `p` of the smallest gardens worth raising only falls, one pointer moved down; the level the flowers spread evenly over those `p` |
| `beauty_rising.kara` | the walk the other way, from every garden completed to none, the completing cost starting at its whole and falling, so `p` only rises; the walk stops at the first garden already at the target |
| `beauty_struct.kara` | a `struct Gardens` of the sorted gardens, their prefix sums and the cost of completing every suffix, with `raise_cost`, `level` (a binary search on `p`) and `beauty` of one split (`ref self`), `-1` for a split that cannot be had |
| `beauty_iter.kara` | the prefix sums and suffix costs built by `fold`s that push onto a `Vec` taken `own`, the level a closure, and the answer `(0..=n).filter(...).map(...).max()` |
| `beauty_solution.kara` | LeetCode's Rust template: `Vec<i32>` and `i32` in, the gardens widened and capped by `map(\|&x\| (x as i64).min(target))`, `sort_unstable`, the prefix sums in `vec![0i64; n + 1]`, the walk `(0..=n).rev()` with one pointer and `continue`, `usize` counts cast `as i64`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and five
more (every garden complete already, one garden, flowers enough to
complete everything yet one garden better left just short, full worth
far more than partial, and gardens past the target), each with its
answer; then a checksum of 3000 random cases of 1 to 20 gardens, the
flowers and the target up to 10, 1000 and 10^5 in turn, up to three
times the target per garden in new flowers, and full and partial up to
10^5; then the constraints' largest, 10^5 gardens of up to 10^5 flowers
with the target, full and partial 10^5, and 10^10, 10^9 and 10^5 new
flowers. `beauty.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 15 edits: `Vec<i32>`
and `Vec<i64>` to `Vec[i32]` and `Vec[i64]`, the `&` of the closure
pattern `|&x|` dropped, `sort_unstable` to `sort`, `vec![0i64; n + 1]`
to `Vec.filled(n + 1, 0)`, `&&` to `and`, and `struct Solution;` to
`struct Solution {}`. Since `len()` is an `i64` in Kāra, the casts of the
counts (`(n - c) as i64`, `p as i64`) were redundant and went, and the
`i64` suffixes of `0i64` with them, the types following anyway.

The iter arm was first written pushing onto the sums inside the fold as
`pushed(sums, sums[sums.len() - 1] + f)`, moving `sums` into the call
and reading it again in the next argument. `karac check` reports the
move, and `karac fix` would clone `sums` at the move site, which copies
the whole `Vec` for every garden, quadratic over 10^5 gardens; the read
was bound to a `let` before the call by hand instead, which the help
text names as restructuring. A fix that hoists the later argument when
the earlier ones are plain values is noted for `karac fix` (kara
B-2026-11-17-145).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way of planting at most the new flowers among the
gardens tried, recursively, each garden then complete when it holds at
least the target, the beauty the complete ones times `full` plus the
fewest flowers of an incomplete one times `partial`, and the largest; no
sorting, no capping and no splits. It checks 300 random cases of 1 to 4
gardens of up to 6 flowers, the target up to 7, up to 6 new flowers, and
full and partial up to 10; then 30 with gardens up to 10 flowers and the
target up to 4, so that many are complete already; then 30 with full up
to 3 and partial from 50 to 100, so that leaving a garden incomplete
pays. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the largest beauty, read literally |
| P2 | the answer is at least the beauty with nothing planted, and at most every garden complete plus `partial` times one short of the target |
| P3 | the gardens reversed: the same answer |
| P4 | one new flower more: no smaller answer |
| P5 | `full` one higher, and `partial` one higher: no smaller answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 39903453, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that tries
every assignment of each new flower to a garden or to none
(`itertools.product`) and takes the largest beauty. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: a garden at the target left among the incomplete | P1 89, P2 65, P6 89 |
| M5 | ★: never every garden complete | P1 160, P2 139, P6 160 |
| M6 | ★: the last split kept, not the best | P1 34, P4 8, P6 34 |
| M7 | pointer: the pointer never brought back to the split | P1 12, P6 12 |
| M10 | pointer: never no garden completed | P1 63, P2 38, P6 63 |
| M11 | pointer: the completing cost never taken from the flowers | P1 60, P6 60 |
| M13 | rising: one flower refunded too many per garden left incomplete | P1 89, P6 89 |
| M15 | rising: a split that costs too much ends the walk | P1 46, P2 46, P6 46 |
| M16 | rising: one garden too many counted complete | P1 221, P6 221 |
| M17 | struct: each suffix's cost only its first garden | P1 21, P6 21 |
| M18 | struct: never all `c` gardens raised | P1 23, P6 23 |
| M19 | struct: the level not capped below the target | P1 101, P2 87, P6 101 |
| M22 | iter: the suffix costs read from the wrong end | P1 91, P2 8, P6 91 |
| M24 | iter: `partial` paid with every garden complete | P1 179, P2 61, P6 179 |
| M26 | iter: the worst split, `min` for `max` | P1 185, P2 61, P4 28, P6 185 |
| M27 | solution: a garden at the target ends the walk | P1 251, P2 251, P6 251 |
| M29 | solution: the level spread over one garden more | P1 155, P2 23, P6 155 |

P1 and P6 kill all seventeen, P2 ten, P4 two, and P3 and P5 none. P2's
two bounds catch the edits that lose a split or overpay one: too low
when the best split is never tried (M5, M10, M15, M27) or the level is
spread too thin (M29), too high when a capped level or an incomplete
garden is overpaid (M3, M19, M24). P4 catches only the edits that do not
take the best of the splits (M6, M26), since one more flower can then
change which split comes last. P3 cannot fail on any arm that sorts
first, which all six do, and P5 not on any that takes the largest of
splits whose beauty grows with `full` and `partial`, whatever is wrong
with how each split is valued.

Of the thirty-one, fourteen were not kept. One survives and is
equivalent: the iter arm refusing a raise that costs exactly the
flowers left (M23), since raising one garden fewer then spreads to the
same level. Two crash: the pointer arm refusing an exactly affordable
raise (M8), whose pointer then runs to 0 when no flowers are left and
indexes below the start, and the iter arm's suffix costs not net of the
flowers already planted (M25), which leaves no split affordable and
unwraps an empty `max`. None differs between the backends. Two fail as
a kept one does: the rising and struct arms never every garden complete
(M12, M21) as the ★ arm's (M5). Nine fail their own way and are left
out for the count of three (two for the template): the ★ and pointer
arms' level allowed up to the target (M1, M9, which fail alike), the ★
arm's exactly affordable level refused and its gardens never capped
(M2, M4), the rising arm's raise undercharged and the struct arm's raise
one garden short (M14, M20, which fail alike), and the template's one
flower short per completed garden, complete gardens paid `partial`, and
gardens never capped (M28, M30, M31).

## Verification

Every arm prints the same output as `beauty.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ arm takes 7.4 s, its two binary searches
the slowest, the other arms 1.1 s to 3.0 s, and the differential 0.4 s.

## Benchmarks

The bench draws 20000 gardens of up to 10^5 flowers once, then makes 20
passes, one garden drawn again before each and the new flowers drawn
anew up to 1.2 * 10^9, each pass the ★ arm with the target, full and
partial 10^5. C sorts with `qsort` and Go with `sort.Slice`. Every
implementation prints `20 passes over 20000 gardens: checksum
217439964`.

BENCHTAB
