# 1198. Find Smallest Common Element in All Rows

Given an `m x n` matrix `mat` where every row is sorted in strictly
increasing order, return the smallest common element in all rows. If
there is no common element, return `-1`.

```
mat = [[1,2,3,4,5],[2,4,5,8,10],[3,5,7,9,11],[1,3,5,7,9]]  ->  5
mat = [[1,2,3],[2,3,4],[2,3,5]]                          ->  2
```

**Constraints:** `1 <= m, n <= 500`; `1 <= mat[i][j] <= 10^4`; `mat[i]`
is sorted in strictly increasing order.

The arms are `fn smallest_common_element(mat: Vec[Vec[i64]]) -> i64`.
The two Rust arms keep the method LeetCode gives Rust users, on
`Vec<Vec<i32>>` and `i32`, inside `impl Solution`, and a one-line
`smallest_common_element` calls it.

## Approaches

| file | mechanism |
|---|---|
| `smallest_common_element.kara` ★ | a `[0; 10001]` count of each value over the whole matrix: a row holds a value at most once, so a value is in every row exactly when its count is `m`, and the first row, sorted, gives the candidates smallest first. O(mn) |
| `smallest_common_element_search.kara` | each value of the first row, smallest first, looked up in every other row by `binary_search`. O(n m log n) |
| `smallest_common_element_pointers.kara` | a pointer into each row, the way sorted lists are merged: every row whose value is below the largest pointed at moves on, until all point at one value or a row runs out. O(mn) |
| `smallest_common_element_sets.kara` | the rows as `Set[i64]`s, intersected one by one, and the least of what is left |
| `smallest_common_element_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `vec![0; 10001]` count indexed by `v as usize`, then the first value of `&mat[0]` counted `mat.len()` times), carried to Kāra by `karac fix` |
| `smallest_common_element_chain.kara` | another Rust solution, one iterator chain (`mat[0].iter().find(|&&v| mat.iter().all(|row| row.binary_search(&v).is_ok())).copied().unwrap_or(-1)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 10 lines: LeetCode's two examples; two rows
with nothing in common (`-1`); one row of one value; a common value at
the constraints' top, `10000`; three rows sharing 3 and 5 (`3`); one row
of 500 (`1`); 1000 random matrices of up to 6 rows of up to 12 values
(`1000 random matrices: 571 with a common element, checksum
709706114`); and 500 rows of 500, the constraints' most, from 1 to 10000
(`-1`) and from 1 to 520 (`77`). `smallest_common_element.py` mirrors the
★ arm and its output is byte-identical. Every arm gives the same output
under `karac run` and `karac build`, and under the AddressSanitizer
build.

The Mend loop: the ★ and pointers arms check clean as written. The
search arm was first written with Rust's `row.binary_search(v).is_ok()`;
Kāra's `binary_search` gives an `Option`, and `karac fix` rewrites the
call to `is_some()`. The sets arm was first written as Rust intersects,
`common.intersection(here).collect()`; Kāra's `intersection` already
gives a `Set`, and `karac fix` makes it `.into_iter().collect()`, which
compiles and gives the same answers; the arm as kept drops the
`.collect()`, the Kāra a reader would write. The solution arm takes one
round of 11 fixes (among them `vec![0; 10001]` to `Vec.filled(10001,
0)`, `for row in &mat` to `for row in ref mat`, `for &v in row` to `for v
in row`, and `Solution::` to `Solution.`), and the chain arm one round of
10 (among them `|&&v|` to `|v|`, `binary_search(&v).is_ok()` to
`binary_search(v).is_some()`, and `.copied()` to `.cloned()`). Both
outputs match. The kata found no gap.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each value from 1 up, looked for in every row one entry at a
time with `contains`, and the first found in all of them. 2000 random
matrices of 1 to 6 rows of 1 to 12 values, each row strictly increasing
from 1 to at most 41.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the rows reversed give the same |
| P3 | the first row repeated as a new last row gives the same |
| P4 | every value 7 higher gives an answer 7 higher, or still `-1` |
| P5 | the last row taken off gives a common value, and one as small or smaller |
| P6 | 10000 put at the end of every row gives the same, or 10000 for `-1` |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 matrices: checksum 889673149,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same matrices, intersecting the rows as sets, gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a value in all rows but one taken | P1 933, P2 626, P7 4665 |
| S2 | ★: the first row read from its largest | P1 843, P5 106, P6 1170, P7 4215 |
| Q1 | search: the second row never searched | P1 567, P2 571, P7 567 |
| Q2 | search: a value found in no other row | P1 1499, P2 1390, P3 1554, P6 446, P7 1499 |
| T1 | pointers: the first row's value taken for the largest | P1 1315, P2 1245, P6 138, P7 1315 |
| T2 | pointers: the first row never moves | P1 440, P2 676, P3 440, P7 440 |
| E1 | sets: the greatest of what is left | P1 843, P5 106, P6 1170, P7 843 |
| E2 | sets: the rows united | P1 1515, P5 336, P7 1515 |
| X1 | solution: a value in exactly all rows but one taken | P1 1640, P2 742, P5 445, P6 865, P7 1640 |
| X2 | solution: each value counted twice | P1 1538, P2 709, P3 1278, P5 769, P6 1231, P7 1538 |
| C1 | chain: none found reads as 0 | P1 830, P4 830, P5 830, P6 830, P7 830 |
| C2 | chain: a value in any row taken | P1 1453, P2 1286, P7 1453 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. S2 and E1 are one fault in two arms, the greatest common
value for the least, and fail alike. P2, the rows reversed, catches every
fault that reads the first row differently from the others (S1, Q1, Q2,
T1, T2, X1, X2, C2), since reversing moves another row first; S2 and E1 read
every row alike and only take the wrong end, so P2 misses them. P4,
every value 7 higher, catches only C1, whose wrong `0` for none does not
move with the values.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 20 matrices of 500 x 500, the constraints' most, built once,
with rows of values from 1 to 520, 1000, 5000 and 10000 in turn; then
100 rounds over the matrices, each answer folded into a checksum. Every
program prints `100 rounds of 20 matrices of 500 x 500: checksum
177046203`. Each call clears a count of 10001 entries and reads every
value of the matrix once.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `e8dc4f7aa2`
plus the typechecker fix pushed as `ab7613763c`, on LLVM 22. A plain
`karac build` targets x86-64-v2, so the C and overflow-checked Rust
programs are also built at x86-64-v3 for comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.376 to 0.452 s | 0.406 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.383 to 0.471 s | 0.415 s |
| Rust (`rustc -O`) | 0.373 to 0.437 s | 0.383 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.364 to 0.443 s | 0.400 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.387 to 0.474 s | 0.405 s |
| C (`clang -O3`) | 0.357 to 0.458 s | 0.398 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.335 to 0.406 s | 0.383 s |
| Go | 0.391 to 0.462 s | 0.420 s |
| Python | 14.96 to 15.24 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Every compiled language lands within the others' spread, from
0.383 s (plain Rust, and C at x86-64-v3) to Go's 0.420 s, with Kāra at
0.415 s and Rust with overflow checks on at 0.400 s: the work is a pass
over 250000 values per call, and none of the five pulls ahead. Python
takes about 36x Kāra's time.
