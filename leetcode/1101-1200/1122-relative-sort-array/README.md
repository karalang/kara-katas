# 1122. Relative Sort Array

Given two arrays `arr1` and `arr2`, the elements of `arr2` are distinct,
and all elements in `arr2` are also in `arr1`. Sort the elements of
`arr1` such that the relative ordering of items in `arr1` are the same
as in `arr2`. Elements that do not appear in `arr2` should be placed at
the end of `arr1` in ascending order.

```
arr1 = [2,3,1,3,2,4,6,7,9,2,19], arr2 = [2,1,4,3,9,6]  ->  [2,2,2,1,4,3,3,9,6,7,19]
arr1 = [28,6,22,8,44,17], arr2 = [22,28,8,6]           ->  [22,28,8,6,17,44]
```

**Constraints:** `1 <= arr1.length, arr2.length <= 1000`; `0 <=
arr1[i], arr2[i] <= 1000`; the values of `arr2` are distinct, and each
is in `arr1`.

The arms are `fn relative_sort_array(arr1: Vec[i32], arr2: Vec[i32]) ->
Vec[i32]`. The values are small, so a count of each over the range 0 to
1000 sorts them in one pass: `arr2`'s values written out in its order,
then the counts left walked in ascending order.

## Approaches

| file | mechanism |
|---|---|
| `relative_sort_array.kara` ★ | a counting sort: each value's count in an array over 0 to 1000, `arr2`'s values written out in its order, then every value left in ascending order. O(n + 1001) |
| `relative_sort_array_key.kara` | a sort by key: each value of `arr2` mapped to its place in a `Map`, and every value sorted by `(0, place)`, or `(1, value)` for one with no place. O(n log n) |
| `relative_sort_array_compare.kara` | a comparison sort: each value's place in an array over 0 to 1000, -1 for none, and a comparator that orders two placed values by place, a placed value before one with none, and two with none by value. O(n log n) |
| `relative_sort_array_buckets.kara` | a pass over `arr1` for each value of `arr2`, taking every copy of it, then the values `arr2` does not hold, sorted. O(n * m + n log n) |
| `relative_sort_array_sorted.kara` | each value's count in a `SortedMap`: `arr2`'s values removed in its order, then the rest walked in key order. O(n log d) for `d` distinct values |
| `relative_sort_array_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, a `HashMap` of places collected from `enumerate`, `sort_by_key` on a tuple), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five properties |

Every arm prints the same 8 lines: the answers for LeetCode's two
examples and five more (every value named, one value named and the rest
left, one value, both ends of the range, and repeats of a value left
over), then over 2000 random problems of up to 1000 values from 0 to a
top of 0 to 1000, `arr2` a random choice of their distinct values in a
random order, how many values `arr2` placed and a checksum (`2000 random
problems: 492604 values placed by arr2, checksum 454311607`).
`relative_sort_array.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: `arr2`'s values in its order, every copy of each, then the
values left, the smallest of them taken each time. It checks 2000
problems in four kinds of 500: up to 10 values from 0 to 3, up to 10
from 0 to 1000, and up to 300 from 0 to a top of 0 to 300, each with
`arr2` some of their distinct values in a random order; and up to 300
values from 0 to a top of 0 to 1000 with `arr2` all of their distinct
values or one. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the answer holds the same values as `arr1`, as often |
| P3 | every value may come before the one after it: both in `arr2` in its order, one in it before one not, or neither in ascending order |
| P4 | `arr1` in another order gives the same answer |
| P5 | a value `arr2` left out, added to its end, moves that value's copies to just after the values `arr2` held |
| P6 | every value of `arr1` twice gives every value of the answer twice |

All 68,154 checks pass on every arm: `2000 problems: checksum 787064349,
68154 checks over 6 arms: 0 failures`. A Python reading of the same
problems, sorting by a key, gives the same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Nineteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each value counted twice | P1 2000, P2 2000 |
| M2 | ★: `arr2`'s values written again among the rest | P1 2000, P2 2000, P3 1792, P5 1301 |
| M3 | ★: the zeros left over lost | P1 325, P2 325, P5 75 |
| M4 | ★: the rest in descending order | P1 1105, P3 1105 |
| M5 | ★: one copy of each value of `arr2` lost | P1 2000, P2 2000, P5 1359, P6 2000 |
| M6 | key: `arr2`'s order reversed | P1 1373, P3 1373, P5 1359 |
| M7 | key: the rest first | P1 1359, P3 1359, P5 1359 |
| M8 | key: every place the same | P1 1254, P3 1254, P4 1259, P5 1082 |
| M9 | key: `arr2`'s first value not placed | P1 1792, P3 1792, P5 1359 |
| M10 | compare: a placed value after one that is not | P1 1263, P3 1263, P4 1290, P5 1273, P6 514 |
| M11 | compare: the first place taken for none | P1 1010, P3 1010, P4 1100, P5 672, P6 252 |
| M12 | compare: a value with no place given the first | P1 1324, P3 1324, P4 1242, P5 1334 |
| M13 | buckets: smaller values taken too | P1 1792, P2 1792, P3 1717, P4 1697, P5 1341 |
| M14 | buckets: the rest left unsorted | P1 1022, P3 1022, P4 1029 |
| M15 | buckets: the placed values again for the rest | P1 2000, P2 2000, P3 1373, P5 1359 |
| M16 | buckets: the first value never taken | P1 1205, P2 1205, P4 1094, P5 197, P6 1205 |
| M17 | sorted: each count one too many | P1 2000, P2 2000, P6 2000 |
| M18 | sorted: the first value not counted | P1 2000, P2 2000, P4 1567, P6 2000 |
| M19 | solution: placed values among the rest | P1 613, P3 613, P4 608, P5 696 |

P1 catches all thirty, P3 twenty-three, P5 twenty-one, P2 eleven, P4 ten
and P6 seven. P2 and P3 between them catch every edit too, as they must:
an answer that holds `arr1`'s values and lets each come before the next
is the literal answer, since only equal values tie. P2 sees the edits
that lose, add or repeat a value (M1 to M3, M5, M13, M15 to M18), and P3
the ones that keep the values but misplace them. P4 sees an answer that
depends on the order `arr1` came in: a key or comparison that ties
values that differ, so the sort keeps them as it found them (M8, M10 to
M12, M19), the rest never sorted (M14), or values taken by their
position in `arr1` (M13, M16, M18). P5 misses the edits that misorder
the rest or miscount values without regard to `arr2`, since the answer
it predicts is built from the arm's own. P6 catches a count off by a
fixed amount, one copy lost or one too many, which doubling the array
does not double (M5, M16 to M18), and the two comparators that disagree
with themselves (M10, M11).

Of the eleven not kept, every one fails as a kept edit does: the rest
in descending order in the key, compare, sorted and solution arms as
M4; `arr2`'s order reversed in the compare and solution arms, and
`arr2` walked backwards in the buckets arm, as M6; every place the same
and `arr2`'s first value not placed in the solution arm as M8 and M9;
`arr2`'s values left in the sorted arm's map as M2; and one copy of
each lost in the sorted arm as M5.

## Verification

Every arm prints the same output as `relative_sort_array.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found two gaps, both fixed. The key arm's `match place.get(x) {
Some(i) => (0, i), None => (1, x as i64) }`, with `i` a `ref i64`, was
refused as arms of `(i64, ref i64)` and `(i64, i64)` (B-2026-11-11-64).
A `ref` to a `Copy` value beside the value joins at the value, and now
each element of two tuples does too; a tuple of a `ref String` beside
one of a `String` is still refused. The solution arm was written as Rust
writes it, and `karac fix` carried it to a clean check in four rounds:
`use std::collections::HashMap;` deleted, `Vec<i32>` to `Vec[i32]`, `mut
arr1` to `own` and a `let mut`, `&x` and `&i` patterns to `x` and `i`,
`Solution::` to `Solution.`, `struct Solution {}` declared, `HashMap` to
`Map` and `usize` to `i64`, `*x` to `x`, and a `clone()` where the
harness hands it `arr1`. Deleting the `use` line left the blank lines
either side of it as two in a row; the fix now takes one of them too
(B-2026-11-11-65).

## Benchmarks

The bench builds 4 problems of LeetCode's largest size once, 1000
values from 0 to 1000, 500, 100 and 10, `arr2` half of each one's
distinct values in a random order. Each of 5000 rounds swaps two values
of each `arr1` and two of each `arr2` and sorts it again with the ★ arm:
20000 calls. Every implementation prints `5000 rounds over 4 problems of
1000 values: checksum 972029035`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `c57d79254b`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.120 to 0.150 s | 0.132 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.115 to 0.154 s | 0.138 s |
| Rust (`rustc -O`) | 0.121 to 0.167 s | 0.138 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.137 to 0.174 s | 0.153 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.137 to 0.175 s | 0.161 s |
| Go | 0.178 to 0.211 s | 0.187 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.170 to 0.262 s | 0.195 s |
| Kāra (`karac build`) | 0.152 to 0.238 s | 0.203 s |
| Python | 4.400 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 1.5x C's time, 1.3x overflow-checked Rust's and
about Go's; the gap to C and Rust was not traced. Python takes about 23x
Kāra's time.
