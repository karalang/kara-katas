# 1074. Number of Submatrices That Sum to Target

Given a `matrix` and a `target`, return the number of non-empty
submatrices that sum to `target`. A submatrix `x1, y1, x2, y2` is the set
of all cells `matrix[x][y]` with `x1 <= x <= x2` and `y1 <= y <= y2`. Two
submatrices are different if they differ in any coordinate.

```
matrix = [[0,1,0],[1,1,1],[0,1,0]], target = 0  ->  4
matrix = [[1,-1],[-1,1]],           target = 0  ->  5
matrix = [[904]],                   target = 0  ->  0
```

**Constraints:** `1 <= matrix.length <= 100`; `1 <= matrix[0].length <=
100`; `-1000 <= matrix[i][j] <= 1000`; `-10^8 <= target <= 10^8`.

A submatrix is a band of rows and a run of columns. For one band, the sums
of each column between its top and bottom row make a line of numbers, and
the submatrices in the band are that line's runs. A run sums to `target`
when the running total at its right end is `target` more than the running
total just before its left end, so a map of the running totals seen so far
counts the runs ending at each column in one lookup: O(m^2 n) over all
bands.

The arms take the matrix as `Vec[Vec[i64]]` and return the count as `i64`.

## Approaches

| file | mechanism |
|---|---|
| `submatrix_sum.kara` ★ | for each top row the columns' sums grown a row at a time down to each bottom row, read left to right as a running total; a `Map[i64, i64]` of the totals seen, starting from `0 => 1`, counts the earlier ones `target` below. O(m^2 n) |
| `submatrix_sum_brute.kara` | the matrix's sums from the top-left corner built once, and every one of the O(m^2 n^2) rectangles summed from its four corners |
| `submatrix_sum_columns.kara` | the ★ arm on its side: each row's sums from the left, then for each pair of columns the rows' strip sums read top to bottom, the map updated through `*seen.entry(total).or_insert(0) += 1` and read through `if let Some(k)`. O(n^2 m) |
| `submatrix_sum_sorted.kara` | the corner sums built row by row; for each pair of rows a strip's sum up to column `c` is two corners apart, counted with a `SortedMap`. O(m^2 n log n) |
| `submatrix_sum_iter.kara` | in iterators: each band's column sums `zip`ped from the rows, their running totals `fold`ed into a list, every pair of totals `target` apart counted with `filter(..).count()`, and the bands `map(..).sum()`med. O(m^2 n^2) |
| `submatrix_sum_solution.kara` | LeetCode's Rust template (`use std::collections::HashMap;`, `struct Solution;`, `Vec<Vec<i32>>`, `vec![vec![0; n + 1]; m]`, `HashMap::new()`, `count.get(&(sum - target))`, `*count.entry(sum).or_insert(0) += 1`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 16 lines: the counts for LeetCode's three
examples and six more; the sum and a checksum of the counts for 3000
random matrices up to 5 by 5 and 20 up to 30 by 30, each with a random
target; and the counts for 30 by 30 matrices of zeros, of ones (targets 1
and 30) and of alternating signs, and for one row of 100 alternating
1000 and -1000. `submatrix_sum.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every submatrix, its cells added up one by one. It checks 2000
problems, 1000 matrices up to 4 by 4 and 1000 up to 8 by 8 with cells from
-2 to 2; one time in two the target is the sum of a submatrix drawn at
random, otherwise a number from -4 to 4. Every random choice is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the matrix transposed gives the same count |
| P3 | the matrix turned half a turn gives the same count |
| P4 | every cell and the target negated give the same count |
| P5 | the whole matrix's sum is counted at least once, and a target past the sum of the cells' absolute values is counted never |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 167998974, 72000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python
reading of the same 2000 problems gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All thirty are caught, each the
same way under both backends and none by a crash. Fifteen are kept, two
or three to each arm, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the lookup with its sign wrong (`target - total`) | P1 1256, P2 1433, P3 1257, P5 103, P6 1256 |
| M2 | ★: a total recorded before it is looked up | P1 281, P2 230, P6 281 |
| M3 | ★: a total seen twice counted once | P1 890, P2 993, P3 787, P6 890 |
| M4 | brute: the corner sums count the overlap twice | P1 1103, P3 1100, P5 372, P6 1103 |
| M5 | brute: the top-left corner subtracted | P1 963, P3 1034, P5 12, P6 963 |
| M6 | brute: the last row never a top | P1 1118, P2 1267, P3 906, P5 389, P6 1118 |
| M7 | columns: strips one column wide skipped | P1 1551, P2 1314, P5 372, P6 1551 |
| M8 | columns: a new total counted twice (`or_insert(1)`) | P1 1199, P2 1252, P3 1128, P6 1199 |
| M9 | sorted: the top corner a column to the left | P1 1226, P2 1452, P3 1264, P6 1226 |
| M10 | sorted: a strip recorded `target` lower | P1 1220, P2 1328, P3 1137, P5 1428, P6 1220 |
| M11 | iter: the band only its bottom row | P1 1248, P2 1453, P3 1089, P5 680, P6 1248 |
| M12 | iter: the target's sign dropped (`target.abs()`) | P1 722, P4 1431, P5 540, P6 722 |
| M13 | iter: the cells squared | P1 1589, P2 711, P4 1228, P5 1494, P6 1589 |
| M14 | solution: the lookup with its sign wrong | P1 1237, P2 1433, P3 1270, P5 103, P6 1237 |
| M15 | solution: the running total carried across strips | P1 1022, P2 1255, P3 1111, P5 317, P6 1022 |

P1 and P6 catch all fifteen, P2 twelve, P3 eleven, P5 eleven and P4 two.
P4 sees only the edits that treat a number and its negation unequally,
the dropped sign and the squared cells (M12, M13): every other edit errs
the same way on the negated problem. P2 misses the edits that keep the
count symmetric in rows and columns (M4, M5, M12), and P5 those whose
error never empties or invents the whole matrix's run (M2, M3, M8, M9).

Of the fifteen not kept, twelve fail as a kept edit or as each other, since
the arms share their loops: the empty left edge never counted (★, iter)
and the first column never a left edge (brute) fail alike; so do the
band started a row below its top (★) and the top row never counted
(solution), the cells kept for a row's sums (columns, solution), the
running total not kept (columns) and the corner sums of one row (sorted),
the last column never a right edge (sorted, iter), and the strips one
column wide skipped in the solution as in the columns arm (M7). The other
three, the brute arm's last row never a bottom, the columns arm's one
count however often a total was seen, and the sorted arm's bands one row
high skipped, fail in ways of their own and are left out to keep two or
three to each arm.

## Verification

Every arm prints the same output as `submatrix_sum.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.5 s to 3.1 s (the iter
arm the slowest) and the differential 18.5 s.

The kata found one miscompile, fixed in kara `1de47226fa` with the core pin
`ok_literal_takes_closure_and_entry_slots` and
`tests/kata_1074_literal_slots.rs`:

- **A number literal kept `i64` in a closure's return slot and an entry's
  value.** The Rust arm keeps LeetCode's `Map[i32, i32]` and
  `*count.entry(sum).or_insert(0) += 1`. The checker left the `0` at its
  default `i64` and MIR stored it as one, 8 bytes into a 4-byte value:
  `__mir-llvm-asan` stopped with a stack-buffer-overflow and a `karac
  build` binary counted 2 for LeetCode's first example, where the
  interpreter and `__mir-llvm-run` printed 4. Probing found the same
  root in closures: `|| 5` checked against `Fn() -> i32` or `Fn() -> f32`
  returned an `i64`, so a build read garbage and the interpreter printed
  `5` for `5.0`. Both now take the slot's type. Kara B-2026-11-08-69.

Every file went through `karac fix`. In the ★ arm it dropped the `*` from
`*target`, a tuple part bound by `for (matrix, target) in
examples.iter()`, which is an `i64`; in the iter arm it rebound `|mut acc,
v|` as `let mut acc = acc;`, dropped a turbofish (`.sum::<i64>()`) and a
`*` on a range's closure parameter. The Rust arm reaches a clean check in
four rounds: the syntax (the `use` line deleted, `struct Solution {}`,
`Vec[..]`, `HashMap.new`, the two `&`s), then `HashMap` to `Map`, then
`ans: i32` and one of the two `vec!`s, then the other, which leaves
`Vec.filled(m, Vec.filled(n + 1, 0))`.

## Benchmarks

The bench builds 30 matrices of 100 by 100 once, cells from -3 to 3, in
all five languages, and counts each with the ★ arm for the targets -5, 0
and 7. Every implementation prints `90 calls: 24339475 submatrices,
checksum 589108292`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with kara `dd6a222d70`
on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.486 to 0.550 s | 0.524 s |
| Kāra (`karac build`) | 2.248 to 2.711 s | 2.375 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.260 to 2.628 s | 2.398 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.462 to 2.703 s | 2.646 s |
| Rust (`rustc -O`) | 2.541 to 2.768 s | 2.666 s |
| Go | 3.175 to 3.613 s | 3.363 s |
| Python | 9.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (2.36 s) is below its real time.

The work is 45 million rounds of two map lookups and an insert, a fresh
map for each of the 455,000 bands. Kāra's `Map` and Rust's `HashMap` both
hash with SipHash-1-3, and Kāra runs 9% under Rust. C has no standard
map: its open-addressing table hashes a key with one multiply, so the
4.6x it leads by is mostly the hash, not the language. Go's map takes
1.4x Kāra; it is not broken down here.
