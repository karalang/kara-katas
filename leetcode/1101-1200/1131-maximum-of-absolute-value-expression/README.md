# 1131. Maximum of Absolute Value Expression

Given two arrays of integers with equal lengths, return the maximum
value of:

`|arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|`

where the maximum is taken over all `0 <= i, j < arr1.length`.

```
arr1 = [1,2,3,4], arr2 = [-1,4,5,6]                 ->  13
arr1 = [1,-2,-5,0,10], arr2 = [0,-2,-1,-7,-4]       ->  20
```

**Constraints:** `2 <= arr1.length == arr2.length <= 40000`;
`-10^6 <= arr1[i], arr2[i] <= 10^6`.

The arms are `fn max_abs_val_expr(arr1: Vec[i64], arr2: Vec[i64]) -> i64`.

## Approaches

The expression is the L1 distance between the points `(arr1[i],
arr2[i], i)` and `(arr1[j], arr2[j], j)`. For `i < j` it is `p *
(arr1[j] - arr1[i]) + q * (arr2[j] - arr2[i]) + (j - i)` for the signs
`p` and `q` that make each difference positive, and no other signs give
more. So under each of the four sign pairs every index gets the value
`p * arr1[i] + q * arr2[i] + i`, and the answer is the widest spread of
those values under any pair.

| file | mechanism |
|---|---|
| `max_abs_val_expr.kara` ★ | the four sign pairs `(p, q)`, each a pass keeping the highest and lowest of `p * arr1[i] + q * arr2[i] + i`; the widest spread. O(n) |
| `max_abs_val_expr_eight.kara` | all eight sign vectors over the three coordinates, from the bits of `0..8`, each a list of values and its largest less its smallest. O(n) |
| `max_abs_val_expr_sort.kara` | under each sign pair the values listed and sorted, the spread the last less the first. O(n log n) |
| `max_abs_val_expr_running.kara` | one pass: each index against the smallest value seen so far under each of the four pairs, the minima kept in `[i64.MAX; 4]`. O(n) |
| `max_abs_val_expr_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `Vec<i32>` arrays, a `for &(p, q) in &[(1, 1), (1, -1), (-1, 1), (-1, -1)]` loop, `i32::MIN` and `i32::MAX` bounds, `i as i32`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's two
examples and six more (two zeros, all alike, rising against falling, the
widest values, a zigzag, and a mix), then over 2000 random pairs of 2 to
60 values from -10^6 to 10^6 the answers summed and a checksum (`2000
random pairs: answers total 6268540700, checksum 886866049`), and two of
LeetCode's largest: 40000 values at random each (`3982742`), and 40000
rising against 40000 falling (`119997`). `max_abs_val_expr.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the expression over every pair of indices, and the largest.
It checks 2000 problems of 2 to 12 values in five kinds of 400: values
from -10^6 to 10^6; from -3 to 3, so many tie; the second array the
first; the first sorted rising and the second falling; and every value
alike. Every random choice, the shift P5 uses among them, is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the two arrays swapped give the same answer |
| P3 | both arrays reversed give the same answer |
| P4 | every value negated gives the same answer |
| P5 | a constant added to every value of the first array gives the same answer |
| P6 | the answer is at least `n - 1`, the indices' spread, and at least the answer with the last pair of values dropped |

All 60,000 checks pass on every arm: `2000 problems: checksum 72161937,
60000 checks over 5 arms: 0 failures`. A Python reading of the same
problems, the expression over every pair, gives the same checksum.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-nine are caught. The one
that survives is equivalent: the eight arm with the first array's sign
`0` in place of `-1` keeps the four vectors whose first sign is `1`,
one of each pair `s` and `-s`, whose spreads are equal, and a vector
with a `0` never spreads further than the distance. Fifteen are kept, no
two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pair `(-1, -1)` left out | P1 375, P3 749, P4 749 |
| M2 | ★: the index left out | P1 2000, P6 462 |
| M3 | ★: the lowest started at 0 | P1 505, P3 98, P5 930 |
| M4 | eight: the index counted twice | P1 2000 |
| M5 | eight: the first value taken for the smallest | P1 639, P3 833 |
| M6 | eight: only the last sign vector's spread kept | P1 1183, P3 1564, P4 1564, P6 35 |
| M7 | sort: the second smallest taken for the smallest | P1 1966, P3 1384, P6 537 |
| M8 | sort: the values never sorted | P1 878, P6 476 |
| M9 | sort: the index squared | P1 1771, P3 741 |
| M10 | running: the second index never paired | P1 233, P3 128, P6 169 |
| M11 | running: the last value kept, not the least | P1 1539, P6 448 |
| M12 | running: two sign pairs walked twice | P1 579, P2 881, P3 1546, P4 1546, P6 14 |
| M13 | solution: the highest at least 0 | P1 478, P3 67, P5 930 |
| M14 | solution: the first array's values above 9 clipped to 9 | P1 1153, P2 795, P4 1200, P5 1316 |
| M15 | solution: an odd last index skipped | P1 567, P3 479, P6 180 |

P1 catches all fifteen, P3 ten, P6 eight, P4 four, P5 three and P2 two.
Negating every value turns each sign pair's values into its opposite
pair's, so P4 sees the edits that keep a pair without its opposite (M1,
M6, M12) and the clip (M14), which is not symmetric about 0. Reversing
the arrays does the same and also turns the index around, so P3 sees
those and every edit that treats one end of the arrays apart. P5 sees
the edits that look at where the values sit rather than how far apart
they are: a bound started at 0 (M3, M13) and the clip. P2 sees only the
edits that treat the two arrays apart, the running arm's first two pairs
walked twice, both keeping the first array's sign `1`, and the clip of
the first array. The eight that P6 sees all come out too small: an
index left out or skipped, a smallest that is not the smallest, values
never sorted, spreads not all counted.

Of the fourteen caught and not kept, four fail exactly as a kept one:
the pair replaced in the sort and solution arms as M1, the running
minima started at 0 as M3, and the running arm's index counted twice as
M4. Three groups fail alike among themselves: the first index skipped in
the ★, eight and running arms; the second array read as the first in the
★ and eight arms; and each spread one short in the sort and solution
arms. The other three fail each in a way of its own and were not needed.

## Verification

Every arm prints the same output as `max_abs_val_expr.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, eight, sort and running arms were written as Kāra and checked
clean as written. The solution arm found two gaps in `karac fix`, both
fixed in karac:

- `&[(1, 1), (1, -1), ..]` was rewritten to `ref [..]`, which the
  checker then refuses: a list literal is a new value, not a place to
  borrow. The `&` on a list or repeat literal now goes, as it already did
  on a number or a slice view (B-2026-11-12-3).
- With the `&` gone, `p * arr1[i] + q * arr2[i] + i as i32` was an `i64`
  because of both `p` and `q`, literals from the walked list, and had no
  fix at all: the fix gave up when more than one literal binding made a
  value wide. It now types the first, and a later round the next
  (B-2026-11-12-4).

`karac fix` then carried the solution arm in four rounds: `Vec<..>` to
`Vec[..]`, `&[..]` to `[..]`, `i32::MIN` to `i32.MIN`, the `&(p, q)` and
`&x` patterns to `(p, q)` and `x`, and `::` to `.`; then `struct
Solution {}` declared; then the answer declared `i32`, the list's first
`p` as `1i32`, and the `as i64` at the call dropped, an `i32` widening by
itself; then the first `q` as `1i32`.

## Benchmarks

The bench builds 8 pairs of arrays of 40000 values once, LeetCode's
largest, their values from -10^6 to 10^6. Each of 400 rounds changes one
value of every array and answers each pair with the ★ arm: 3200 calls,
each four passes over 40000 values. Every implementation prints `400
rounds over 8 pairs of 40000 values: answers total 12801482800, checksum
820540918`. Each keeps an array as its own allocation (`Vec[i64]`,
`Vec<i64>`, `[]int64`, a Python list, and C's `int64_t *`).

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `73ec8b248f`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.219 to 0.308 s | 0.239 s |
| Go | 0.453 to 0.606 s | 0.558 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.491 to 0.631 s | 0.582 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.538 to 0.671 s | 0.588 s |
| Kāra (`karac build`) | 0.536 to 0.713 s | 0.591 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.519 to 0.667 s | 0.603 s |
| Rust (`rustc -O`) | 0.639 to 0.791 s | 0.729 s |
| C (`clang -O3`) | 0.614 to 0.808 s | 0.730 s |
| Python | 53.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. The inner pass is a running maximum and minimum of a sum of
products, which C at `-march=x86-64-v3` turns into 256-bit vector code
(`vpcmpgtq` on `ymm` registers) and runs in about 0.40x Kāra's time.
Kāra checks each sum and product for overflow, as Rust does under
overflow checks, and neither program is vectorized: Kāra takes about
Rust's time under overflow checks (1.03x at the default target, 1.04x at
x86-64-v3). Plain `clang -O3` and `rustc -O`, built for the x86-64
baseline, which has no 64-bit vector compare, take about 1.2x Kāra's
time. Go takes about 0.93x Kāra's time. Python takes about 89x Kāra's
time.
