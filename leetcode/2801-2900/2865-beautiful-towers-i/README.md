# 2865. Beautiful Towers I

You are given a **0-indexed** array `maxHeights` of `n` integers.

You are tasked with building `n` towers in the coordinate line. The
`i`th tower is built at coordinate `i` and has a height of
`heights[i]`.

A configuration of towers is **beautiful** if the following conditions
hold:

1. `1 <= heights[i] <= maxHeights[i]`
2. `heights` is a **mountain** array.

Array `heights` is a **mountain** if there exists an index `i` such
that:

- For all `0 < j <= i`, `heights[j - 1] <= heights[j]`
- For all `i <= k < n - 1`, `heights[k + 1] <= heights[k]`

Return *the **maximum possible sum of heights** of a beautiful
configuration of towers*.

```
maxHeights = [5,3,4,1,1]    ->  13
maxHeights = [6,5,3,9,2,7]  ->  22
maxHeights = [3,2,5,5,2,3]  ->  18
```

**Constraints:** `1 <= n == maxHeights.length <= 10^3`; `1 <=
maxHeights[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `towers.kara` ★ | with the peak at i, the best left side is the best left side of the last tower left of i that is no taller, then i's height at every place after it; a stack of indices with rising heights finds that tower, so left[i] = left[j] + (i - j) * h[i] in one pass, and right[i] the same from the right: O(n) |
| `towers_jumps.kara` | the same sides without a stack: from i - 1, while the tower is taller than i's, jump to the tower its own search found, which skips every tower between that was taller than it and so taller than i's; the right side by the same function over the reversed array |
| `towers_iter.kara` | every tower tried as the peak, as iterator chains: walking out from the peak each way, `scan` keeps the lowest height seen so far, the tallest the tower there can be; O(n^2) |
| `towers_split.kara` | divide at the lowest tower: in any mountain the side of the lowest tower away from the peak can be no taller than it all the way out, and it is the least there, so that side is its height at every place; the best is the best mountain over the other side plus that height times the rest, by recursion |
| `towers_solution.kara` | a Rust solution as LeetCode's Rust users write it: every index tried as the peak, two loops walking out with a running `mn = mn.min(max_heights[j])`, summed as `i64`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's three examples; 10^3
towers, LeetCode's most, all 10^9, rising from 1, and a valley falling
to 1 and rising again; then 3000 random arrays of 1 to 8 towers of most
1 to 6, and 30 of 100 to 10^3, every other one up to 10^9 and the rest
up to 50, as a total of the sums and a checksum. `towers.py` mirrors the
★ arm and its output is byte-identical.

```
13 22 18
1000000000000 500500 126250
3000 short arrays: sums total 40676, checksum 433237360
30 long arrays: sums total 186968735605, checksum 103910834
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every way to give each tower a height from 1 to its
most, kept when the heights rise to a peak and then fall, and the
largest sum taken. It draws 2000 random arrays of 1 to 6 towers of most
1 to 4, then 50 of up to 300, every other one up to 10^9 and one in four
sorted, all before any arm answers; the literal reading is asked only of
the first 2000.

| | property |
|---|---|
| P1 | up to 6 towers, the answer is the literal reading's |
| P2 | the towers reversed: the same answer |
| P3 | every most doubled: twice the answer |
| P4 | a tower of most 1 added at the end: one more |
| P5 | from max + (n - 1) * min to the sum, and the sum exactly when the mosts already make a mountain |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, sums total 208495702692: checksum
643636999, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a left side with no lower tower one place short | P1 2000, P2 1241, P5 1637, P6 2050 |
| M2 | ★: the right side one place short | P1 1029, P2 1367, P4 1707, P5 812, P6 1066 |
| M3 | jumps: the jump taken one past the found tower | P1 859, P4 449, P5 652, P6 905 |
| M4 | jumps: the peak counted twice | P1 2000, P5 1978, P6 2050 |
| M5 | iter: the lowest height not carried | P1 628, P2 487, P5 526, P6 663 |
| M6 | iter: the right walk from the start | P1 935, P2 1274, P5 697, P6 979 |
| M7 | split: the lowest tower's height for the peak's side too | P1 1029, P2 1373, P4 1544, P5 864, P6 1066 |
| M8 | split: the right part started at the lowest tower | P1 998, P2 1292, P5 701, P6 1047 |
| M9 | solution: the left walk's running minimum reset each step | P1 628, P2 487, P5 526, P6 663 |
| M10 | solution: the right walk left out | P1 1029, P2 1322, P4 1865, P5 750, P6 1066 |

## Benchmarks

The bench draws 2000 arrays of 10^3 towers, LeetCode's most, every other
one up to 10^9 and the rest up to 50, all of them first, then answers
each 20 times by the ★ arm in all five languages; C allocates the stack
and both sides on each call, as the other languages' vectors are. Every
implementation prints `2000 arrays of 1000, 20 rounds: sums total
283656548236520, checksum 353970222`.

BENCHTAB

## Verification

All five arms print the same output as `towers.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

`towers_iter.kara`, as first written, kept the lowest height with
Rust's `scan`, writing the state in place through `*low = (*low).min(..)`
and returning `Some(*low)`. `karac check` reported E0200 at each: Kāra's
`scan` closure takes the state by value and returns `Some((next_state,
item))`. `karac fix` rewrote both closures as `|low, j| { let low =
low.min(max_heights[j]); Some((low, low)) }`, on one line. In
`towers_jumps.kara`, `sides(max_heights.clone())` was flagged as a
redundant clone, the parameter only borrowing, and `karac fix` passed
`max_heights`. The other two arms checked clean.

LeetCode's Rust template took 10 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `0i64` became `0`, its type coming from the sum; the
two `mn as i64` lost their casts, an `i32` widening; `|&x|` lost its
`&`, and `Solution::` took `.`. The `i32` running minimum and
`(0..i).rev()` were accepted as written.
