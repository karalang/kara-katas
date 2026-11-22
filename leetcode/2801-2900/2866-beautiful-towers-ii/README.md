# 2866. Beautiful Towers II

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

**Constraints:** `1 <= n == maxHeights.length <= 10^5`; `1 <=
maxHeights[i] <= 10^9`.

## Approaches

The problem is [2865](../2865-beautiful-towers-i/) with 10^5 towers in
place of 10^3, so trying every peak in O(n) each is out; every arm here
is O(n) or O(n log n).

| file | mechanism |
|---|---|
| `towers.kara` ★ | with the peak at i, the best left side is the best left side of the last tower left of i that is no taller, then i's height at every place after it; a stack of indices with rising heights finds that tower, so left[i] = left[j] + (i - j) * h[i] in one pass, and right[i] the same from the right |
| `towers_jumps.kara` | the same sides without a stack: from i - 1, while the tower is taller than i's, jump to the tower its own search found, which skips every tower between that was taller than it and so taller than i's; the right side by the same function over the reversed array |
| `towers_runs.kara` | the left side's sum kept as a stack of runs, `(height, count)`: each new tower caps every run taller than it, so those are popped, their sum taken off, and merged with it into one run of its height; the running sum is the best left side with the peak there |
| `towers_split.kara` | divide at the lowest tower, as 2865's split arm does, with the lowest tower of a range from a sparse table and the ranges worked from a list, children before parents, rather than by recursion 10^5 deep |
| `towers_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `Vec<usize>` stack popped with `while !st.is_empty() && max_heights[*st.last().unwrap()] as i64 > x`, `if let Some(&j) = st.last()` for the side sums, and `(0..n).map(..).max().unwrap()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's three examples; 10^5
towers, LeetCode's most, all 10^9, rising from 1, and a valley falling
to 1 and rising again; then 3000 random arrays of 1 to 8 towers of most
1 to 6, and 30 of 10^4 to 10^5, every other one up to 10^9 and the rest
up to 50, as a total of the sums and a checksum. `towers.py` mirrors the
★ arm and its output is byte-identical.

```
13 22 18
100000000000000 5000050000 1250125000
3000 short arrays: sums total 40890, checksum 323001850
30 long arrays: sums total 373917171237, checksum 936064523
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every way to give each tower a height from 1 to its
most, kept when the heights rise to a peak and then fall, and the
largest sum taken. It draws 2000 random arrays of 1 to 6 towers of most
1 to 4, then 50 of up to 20000, every other one up to 10^9 and one in four
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

The differential prints `2050 cases, sums total 474208891755: checksum
510074405, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a left side with no lower tower one place short | P1 2000, P2 1262, P5 1587, P6 2050 |
| M2 | ★: the right side one place short | P1 982, P2 1395, P4 1707, P5 759, P6 1019 |
| M3 | jumps: the jump taken one past the found tower | P1 890, P4 437, P5 651, P6 927 |
| M4 | runs: a popped run's count not merged | P1 788, P5 348, P6 825 |
| M5 | runs: a popped run's sum left in | P1 158, P4 25, P5 71, P6 208 |
| M6 | split: the sparse table's right block never looked at | P1 199, P2 442, P4 644, P5 164, P6 235 |
| M7 | split: the left part's best dropped | P1 982, P2 1403, P4 1534, P5 810, P6 1019 |
| M8 | split: the lowest tower's height on its own side only once | P1 982, P2 1305, P4 1336, P5 634, P6 1019 |
| M9 | solution: the left side one place short | P1 1034, P2 1395, P5 814, P6 1084 |
| M10 | solution: the peak counted twice | P1 2000, P5 1974, P6 2050 |

## Benchmarks

The bench draws 50 arrays of 10^5 towers, LeetCode's most, every other
one up to 10^9 and the rest up to 50, all of them first, then answers
each 10 times by the ★ arm in all five languages; C allocates the stack
and both sides on each call, as the other languages' vectors are. Every
implementation prints `50 arrays of 100000, 10 rounds: sums total
6778972256060, checksum 151000468`.

BENCHTAB

## Verification

All five arms print the same output as `towers.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ and jumps arms are 2865's, written there through the Mend loop;
the runs and split arms checked clean as first written.

LeetCode's Rust template took 30 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]` and `Vec<usize>` became `Vec[i64]`; `vec![0i64; n]`
became `Vec.filled(n, 0)`; `!` and `&&` became `not` and `and`; `Some(&j)
= st.last()` became `Some(j) = st.last().cloned()`; every `as i64`
but `let x = max_heights[i] as i64` went, each an `i32` or index
widening, the one in the stack's comparison too; `|&x|` lost its `&`, and `Solution::` took `.`.
`*st.last().unwrap()` as an index and `st.clear()` were accepted as
written.
