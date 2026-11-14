# 2137. Pour Water Between Buckets to Make Water Levels Equal

You have `n` buckets each containing some gallons of water in it,
represented by a **0-indexed** integer array `buckets`, where the `i`th
bucket contains `buckets[i]` gallons of water. You are also given an
integer `loss`.

You want to make the amount of water in each bucket equal. You can pour
any amount of water from one bucket to another bucket (not necessarily
an integer). However, every time you pour `k` gallons of water, you
spill `loss` **percent** of `k`.

Return *the **maximum** amount of water in each bucket after making the
amount of water equal.* Answers within `10^-5` of the actual answer will
be accepted.

```
buckets = [1,2,7], loss = 80       ->  2.00000
buckets = [2,4,6], loss = 50       ->  3.50000
buckets = [3,3,3,3], loss = 40     ->  3.00000
```

**Constraints:** `1 <= buckets.length <= 10^5`;
`0 <= buckets[i] <= 10^5`; `0 <= loss <= 99`.

A level L can be reached when the water above L, less what spills on
the way, fills every bucket below L. Raising L leaves less to pour and
more to fill, so the test is monotone and the highest level is found by
halving, from 0 to the fullest bucket. O(n log(max / precision)).

## Approaches

| file | mechanism |
|---|---|
| `water.kara` ★ | 64 halvings of the level, each test one pass summing what pours from above, less the spill, against what fills below |
| `water_sorted.kara` | exact: with the i lowest buckets below the level, the level is a line's root, a fraction of integers; the buckets sorted and summed as they go, the one i whose root falls between the i-th bucket and the next found by comparing without dividing, and one `f64` division at the end |
| `water_newton.kara` | Newton's method: what is left over at level L is concave in L, made of straight pieces, so from the mean each step follows its piece to that piece's zero, never passing the level sought, until a step no longer moves; the helper returns the pair (left over, slope) as a tuple |
| `water_fold.kara` | the halving as one `fold` over `0..64` carrying the pair (low, high), its closure taking a tuple pattern; the test a closure `reaches`, itself a `fold` over the buckets |
| `water_struct.kara` | a `struct Pour` built `of` the buckets and the loss, asked whether it `reaches` a level (`ref self`), and a `struct Range` that `narrows` (`mut ref self`) until no float lies between its ends |
| `water_solution.kara` | LeetCode's Rust template: 100 halvings over `for &b in &buckets`, the maximum read through `*`, in `i32`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (one bucket, every bucket empty, no loss, and the most loss
between the widest pair), each with its level to five places; then the
total and a checksum over 2000 random lists of 1 to 10 buckets of 0 to
10, 0 to 100 or 0 to 100000 in turn, each at a random loss; then the
constraints' largest, 100000 buckets of 0 to 100000 at no loss, half
and 99. `water.py` mirrors the ★ arm and its output is byte-identical.

The levels are fractions and the arms reach them by different float
steps, so no arm prints a level rounded where the exact level could lie
halfway. The random lists are counted on a grid of 2^-20, by
`floor(level * 2^20 + 0.5)`: a multiple of a power of two is exact in a
float, and a level here never falls halfway between two steps of that
grid. Their exact levels, worked out in Python as fractions, lie at
least 9.9e-10 from such a halfway point, and the seven shown and the
three largest at least 9.2e-7 from one at five places, against an error
in each arm far below either.

No compiler gap was met. `karac fix` carries the template in two rounds
of 12 and 1 edits: Rust's spellings (`<..>` to `[..]`, `for &b in
&buckets` to `for b in ref buckets`, the adapter's `|&v|` to `|v|`,
`struct Solution;` to `struct Solution {}`, the adapter's `&Vec` to
`ref Vec`, `Solution::` to `.`); then the `ref` dropped from the
adapter's parameter, which borrows already. The `*` before
`buckets.iter().max().unwrap()` stays, since `max` over `iter()` gives a
`ref i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a level counts as reached when pours, one at a time, each
from the fullest bucket over the level into the emptiest under it, as
much as fills the one or empties the other's surplus, and each spilling
its share on the way, leave no bucket under it; the highest level
reached is found by halving. No sum over the buckets is formed. It
checks 300 random lists of 1 to 6 buckets of 0 to 10 at a random loss;
then 30 at no loss or at 99; then 30 of 1 to 6 buckets of 0 to 100000.
All 360 are drawn before any arm answers. Two levels agree when they
differ by at most a millionth of the larger, or of 1.

| | property |
|---|---|
| P1 | the level is the statement read literally |
| P2 | the buckets in reverse order: the same level |
| P3 | every bucket doubled: twice the level |
| P4 | the same buckets at no loss: their mean |
| P5 | every bucket 7 fuller: the level 7 higher |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 537002799, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal levels, each on the grid of 2^-20, was checked against a
Python reading of the same lists by the same pours. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-five edits to the differential, five to eight to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: 16 halvings | P1 329, P4 292, P5 320, P6 329 |
| M26 | ★: the range from 1 | P1 24, P3 24, P4 11, P5 24, P6 24 |
| M34 | ★: the middle rounded down | P1 344, P3 205, P4 258, P5 10, P6 344 |
| M5 | sorted: the spill on the low side | P1 328, P5 230, P6 328 |
| M6 | sorted: the counts' shares swapped | P1 274, P5 316, P6 274 |
| M7 | sorted: the buckets left unsorted | P1 214, P2 229, P6 214 |
| M11 | newton: one step only | P1 86, P6 86 |
| M28 | newton: the mean over one bucket more | P1 236, P4 350, P5 316, P6 236 |
| M29 | newton: stopped once a step moves less than 1 | P1 199, P3 71, P6 199 |
| M13 | fold: the halves swapped | P1 350, P4 350, P5 338, P6 350 |
| M30 | fold: the range up to half the fullest | P1 197, P4 275, P5 338, P6 197 |
| M35 | fold: a gallon to spare asked | P1 350, P3 322, P4 350, P5 51, P6 350 |
| M17 | struct: a share of 99 in place of 100 | P1 292, P4 292, P6 292 |
| M20 | struct: the range stopped once its ends are within 1 | P1 346, P3 212, P4 301, P5 304, P6 346 |
| M32 | struct: the first bucket never counted | P1 292, P2 271, P4 285, P6 292 |
| M21 | solution: the spilt share poured | P1 289, P4 292, P6 289 |
| M22 | solution: the adapter dropping the last bucket | P1 292, P2 271, P4 284, P6 292 |

P1 and P6 kill all seventeen, P4 twelve, P5 ten, P3 five and P2 three.
P4 asks for the mean at no loss, which every right arm gives; it sees
an edit that is wrong with nothing spilt as well: a range or a step cut
short (M2, M13, M20, M26, M30, M34, M35), a share that is not the whole
at no loss (M17, M21), a start off the mean (M28), and a bucket left
out (M22, M32). The rest are right at no loss: the spill put on the
wrong side or count (M5, M6) vanishes with it, and with nothing spilt
the level is the mean, where Newton's method starts (M11, M29) and
which every segment of the unsorted walk gives (M7). P5 raises
every bucket by 7, which raises the level by 7; it sees an edit tied
to 0 or to a fixed scale: a range from 0 or 1, or up to a share of the
fullest, cut short (M2, M13, M26, M30, M34), the spill on the wrong
side or count (M5, M6), a start off the mean (M28), and a fixed gallon
or width (M20, M35). P3 doubles every bucket, which doubles the level;
it sees an edit with a constant in gallons: a range from 1 (M26), a
middle rounded to a whole gallon (M34), a step or a width of 1 (M29,
M20), a gallon to spare (M35). P2 reverses the buckets; it sees an edit
that ties the level to where a bucket is listed: the buckets left
unsorted (M7), and the first or the last bucket left out (M32, M22).

Of the thirty-five, eighteen were not kept. One survives: the fold
arm's 32 halvings, which leave the level within 1e5 / 2^32, about
2.3e-5, of the one sought, inside the differential's tolerance of a
millionth of the level. None fails by a crash. Eight fail as a kept one
does: the ★ arm's range up to the emptiest bucket, the newton arm
started there, and the struct arm's range up to it, as M17; the ★ arm's
spilt share kept, as M21; the struct arm's and the template's halves
swapped, as M13; the ★ arm's first bucket never counted, as M32; and
the struct arm's range from 1, as M26. Eight are killed with checks of
their own, all the same 278, but were left out because their arms keep
their share: each counts the spill wrongly, so every list with a loss
where the spill matters fails P1 and nothing else, since the spill
leaves the properties standing: the ★ arm's spill taken on the filling
too, the sorted arm's first segment always taken, the newton arm's pour
without its spill and its slope below taken as kept, the fold arm's
pour without its spill and a bucket at the level counted as pouring,
and the adapter passing no loss or half the loss. One more is killed
with checks of its own: the sorted arm's level divided as integers (P1
286, P3 147, P4 200, P6 286).

## Verification

Every arm prints the same output as `water.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 s to 18 s, the fold arm the
slowest, its 64 halvings each a closure over 100000 buckets three
times; the differential takes 2 s.

## Benchmarks

The bench builds 10 lists of 100000 buckets once, of 0 to 100000; then
solves every list 10 times, one bucket redrawn and the loss drawn anew
before each solve so that no solve repeats one before, with the ★ arm
in all five languages; each level is counted on the grid of 2^-20. The
C and Go mirrors keep the spill's product out of the sum (its own
statement in C, an explicit `float64(..)` in Go), so that no compiler
fuses the two into one rounding and every language rounds the same
steps. Every implementation prints `100 solves: 1413040763439 in all,
in steps of 2^-20, checksum 223119466`.

BENCHTAB
