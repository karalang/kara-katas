# 1243. Array Transformation

Given an initial array `arr`, every day you produce a new array using the
array of the previous day.

On the `i`-th day, you do the following operations on the array of day
`i - 1` to produce the array of day `i`:

1. If an element is smaller than both its left neighbor and its right
   neighbor, then this element is incremented.
2. If an element is bigger than both its left neighbor and its right
   neighbor, then this element is decremented.
3. The first and last elements never change.

After some days, the array does not change. Return *that final array*.

```
arr = [6, 2, 3, 4]        ->  [6, 3, 3, 4]
arr = [1, 6, 3, 4, 3, 5]  ->  [1, 4, 4, 4, 4, 5]
```

**Constraints:** `3 <= arr.length <= 100`; `1 <= arr[i] <= 100`.

The arms are `fn transform_array(arr: Vec[i64]) -> Vec[i64]`, the array
taken by value (`own`) where the arm changes it.

## Approaches

| file | mechanism |
|---|---|
| `array_transformation.kara` ★ | day by day: each day's array a `clone` of the last, every inner value smaller than both neighbours of the last day raised by one and every one larger than both lowered by one, until the new day `==` the old |
| `array_transformation_inplace.kara` | in place: one array, each day a pass that keeps the value its left neighbour had before the pass in `prev`, since the neighbour may already have moved, and a `changed` flag |
| `array_transformation_windows.kara` | by windows: each day the first value, then `windows(3)` mapped by a `fn step(w: Slice[i64])` that moves the middle value of a valley or a peak, then the last value |
| `array_transformation_iter.kara` | by index ranges: each day collected from `(0..n).map(..)`, the ends kept, and the values that moved counted with `filter` and `count`; the days end at a count of zero |
| `array_transformation_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let mut arr = arr;`, a `prev` clone each day, `&&`, `!changed`, `Vec<i32>`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples; the total of
the final values and a checksum of them for 1000 random arrays of 3 to
100 values from 1 to 100 (`total 2716761, checksum 80997141`); and two
arrays at the constraints' top, 100 values alternating 1 and 100 and 100
values stepping by 37 around 1 to 100, five of their final values each.
`array_transformation.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★ and in-place arms were first written with a bare
`arr: Vec[i64]` whose array they keep or change, E0200 ("cannot give
away `cur`, bound out of parameter `arr`") and, in the in-place arm,
E0517 at each write; one fix makes the parameter `own`. The windows arm
was first written with Rust's `vec![cur[0]]` and `cur.windows(3).map(step)`,
and the fix writes `[cur[0]]` and adds the `.into_iter()`. The index arm
was first written with `||`, `&&` and `next[*i]` in the `filter`, which
the fix writes `or`, `and` and `next[i]`. The solution arm takes one
round of fixes, 12 by `karac fix`'s count (`struct Solution;` to `struct Solution {}`, `Vec<i32>`
to `Vec[i32]` twice, the parameter to `own`, the two `&&` to `and`,
`!changed` to `not changed`, `Solution::` to `Solution.`, and the `|&x|`
patterns to `|x|`). All five check clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the days, each made from the one before by the rule as
written, kept in a list until one equals the day before it. 2000 cases,
a third with 3 to 12 values from 1 to 5 (many runs of equal values), a
third with 13 to 40 values and a third with 41 to 100, both from 1 to
100.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | one more day changes nothing |
| P3 | the ends kept, and every value within the input's least and greatest |
| P4 | the array reversed gives the answer reversed |
| P5 | every value raised by 7 gives the answer raised by 7 |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 313802772,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a value compared with its left neighbour's new value | P1 1072, P4 1350, P6 4288 |
| S2 | ★: the last inner value never moved | P1 1208, P2 1019, P4 1619, P6 4832 |
| I1 | in place: `prev` the left neighbour's moved value | P1 1331, P4 1331, P6 1331 |
| I2 | in place: a lowered peak not counted as a change | P1 634, P2 634, P6 634 |
| W1 | windows: the last value taken from one place early | P1 1734, P3 1734, P4 1918, P6 1734 |
| W2 | windows: a peak level with its right neighbour lowered | P1 1777, P4 1786, P6 1777 |
| T1 | index: the days ended while one value still moves | P1 1175, P2 1175, P6 1175 |
| T2 | index: a valley raised to its left neighbour | P1 1631, P4 1667, P6 1631 |
| R1 | solution: the first inner value never moved | P1 1213, P2 1021, P4 1619, P6 1213 |
| R2 | solution: a peak lowered by two | P1 1714, P6 1714 |

All ten are caught, every one by P1, the statement read literally, and
by P6, which fails on the other four arms too when the ★ arm is the one
mutated (S1, S2). P4, the array reversed, catches the six that treat the
two sides of a value differently: the left neighbour read after it moved
(S1, I1), a peak level only with its right neighbour lowered (W2), a
valley raised to its left neighbour's value (T2), and an end of the
array left out of the pass (S2, R1), which reversed is the other end.
P2, one more day changes nothing, catches the four that stop with a
value still free to move: the ends left out (S2, R1), the in-place arm
not counting a lowered peak as a change (I2), and the index arm stopping
with one value still moving (T1). P3 catches only W1, whose last value is
copied from its neighbour. P5, every value raised by 7, catches none: no
mutation here depends on the values themselves, only on how they
compare, and that is unchanged by adding a constant.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm on 5000 random arrays of 100 values from 1 to 100, built once, then
10 rounds over them; every answer folded into a checksum. Every program
prints `10 rounds of 5000 arrays of 100 values: checksum 656385601`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.924 to 1.025 s | 0.952 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.926 to 1.017 s | 0.956 s |
| Rust (`rustc -O`) | 0.883 to 1.000 s | 0.934 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.826 to 0.884 s | 0.865 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.823 to 0.932 s | 0.890 s |
| C (`clang -O3`) | 0.772 to 0.890 s | 0.800 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.276 to 0.337 s | 0.312 s |
| Go | 1.439 to 1.645 s | 1.539 s |
| Python | 28.92 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 10% ahead of Kāra (0.865 s
against 0.956 s). C is about 16% ahead of Kāra (0.800 s against 0.956
s); Go takes about 1.6x Kāra's time. Python takes about 30x Kāra's time.
No profile was taken.
