# 2022. Convert 1D Array Into 2D Array

You are given a 0-indexed array `original` and two integers `m` and `n`.
Build a 2D array of `m` rows and `n` columns from all of `original`: its
values `0` to `n - 1` form the first row, `n` to `2n - 1` the second, and
so on. Return that array, or an empty one when it cannot be built.

```
original = [1,2,3,4], m = 2, n = 2  ->  [[1,2],[3,4]]
original = [1,2,3],   m = 1, n = 3  ->  [[1,2,3]]
original = [1,2],     m = 1, n = 1  ->  []
```

**Constraints:** `1 <= original.length <= 5 * 10^4`; `1 <= original[i] <= 10^5`;
`1 <= m, n <= 4 * 10^4`.

The grid can be built exactly when `original` holds `m * n` values; then
row `i` is the run `original[i * n..(i + 1) * n]`.

## Approaches

| file | mechanism |
|---|---|
| `convert.kara` ★ | the length checked against `m * n`, then row `i` the slice `original[i * n..(i + 1) * n]` copied out by `to_vec()`, through `(0..m).map(..).collect()`. O(m n) |
| `convert_index.kara` | a grid of zeros by `Vec.filled(m, Vec.filled(n, 0))`, filled cell by cell: `(i, j)` takes `original[i * n + j]` |
| `convert_chunks.kara` | `original.chunks(n)`, each chunk copied out by `to_vec()` |
| `convert_push.kara` | one walk over the values, each pushed onto the current row, a full row moved into the grid and a fresh one started; the shape checked last: exactly `m` rows and nothing left over |
| `convert_iter.kara` | one iterator shared by the rows, each taking the next `n` through `by_ref().take(n)`; the shape checked by `count()` |
| `convert_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<i32>`, `as usize`, `vec![]`, `chunks(n as usize)` and `to_vec()`, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the count of grids built and a checksum of
their rows for 3000 arrays of 1 to 24 values, half of them with a shape
that fits, and for 5 arrays of up to 50000 values, among them one row of
50000 and 50000 rows of one. `convert.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: value `k` goes to row `k / n`, column `k % n`, and there is no
grid when the array does not hold exactly `m * n` values. It checks 1500
problems: an array of 1 to 24 values up to 1-1000 and a shape of 1 to 8
rows, with columns that fit, when some do, at even odds, else 1 to 8. Every
random choice of a problem is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a grid, its rows read one after another, is the array |
| P3 | every value doubled doubles every cell |
| P4 | the array reversed reverses the rows and each row |
| P5 | the shape `(n, m)` gives a grid exactly when `(m, n)` does |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 problems: checksum 357862958, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Sixteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a shorter array accepted (`<` for `!=`) | P1 410, P2 410, P4 409, P6 410 |
| M2 | ★: the last row left out | P1 285, P2 182, P4 182, P5 132, P6 285 |
| M3 | index: a cell read by its column first, `original[j * m + i]` | P1 150, P2 150, P6 150 |
| M4 | index: the last column never filled | P1 285, P2 285, P4 250, P6 285 |
| M5 | index: each cell one value late, wrapping | P1 282, P2 282, P4 274, P6 282 |
| M6 | chunks: chunks one value long | P1 250, P6 250 |
| M7 | chunks: a shape of `m + n` values accepted too | P1 54, P4 39, P6 54 |
| M8 | chunks: each row reversed | P1 250, P2 250, P6 250 |
| M9 | push: a value left over accepted | P1 72, P2 72, P4 72, P5 80, P6 72 |
| M10 | push: a row closed one value early | P1 268, P5 171, P6 268 |
| M11 | push: the first row's last value carried into the second | P1 317, P2 32, P4 26, P6 317 |
| M12 | iter: the count one too many when `m` is 1 | P1 221, P4 39, P5 141, P6 221 |
| M13 | iter: a single value never accepted | P1 3, P6 3 |
| M14 | Rust: chunks of `n + 1` | P1 182, P4 144, P6 182 |
| M15 | Rust: each value halved and doubled on the way to `i32` | P1 280, P2 280, P3 280, P6 280 |
| M16 | Rust: no grid when `m` equals `n` | P1 19, P6 19 |

P1 and P6 kill all sixteen, P2 nine, P4 nine, P5 four and P3 one. P2 reads
a grid's rows back as one array, so it sees every edit that builds a grid
from the wrong values or the wrong number of them (M1, M2, M3, M4, M5, M8,
M9, M11, M15), and misses the ones that get the shape wrong while keeping
every value in order (M6, M7, M10, M12, M13, M14, M16): P2 checks only that
a grid, when there is one, holds the array, and those grids do, or are
missing. P4 reverses the array; it sees an edit only where the two ends of
a row or of the array are treated unevenly: a short array, a lost last row
or column, a wrapped value (M1, M2, M4, M5), a value left over or carried
(M9, M11), a shape of `m + n` or `n + 1` that the reversed array cuts
elsewhere (M7, M14), a count off by one (M12). P5 swaps the shape, which
leaves `m * n` alone, so it sees only the edits whose acceptance depends on
`m` and `n` apart: the last row dropped (M2), a leftover value accepted when
the row count matches (M9), a row closed early (M10), and a count off when
`m` is 1 (M12). P3 doubles every value, which an edit sees only if it does
arithmetic on the values (M15).

The other fourteen fail as a kept one does, or with counts of their own.
Four fail P1, P2, P4 and P6 182 times each: the ★ arm's rows overlapping by
one, the index arm reading its first row twice, the iter arm starting a
fresh iterator for every row, and the iter arm skipping a value after its
first row. The chunks arm's every chunk but the last and the Rust arm's
first row dropped fail as M2; the iter arm reading each row backwards fails
as M8; the chunks arm's chunks of `m` and the index arm's `m` by `m` grid
both fail P1 and P6 266 times; the push arm with its row count unchecked
fails as the Rust arm's shape checked against `n` alone (P1 340, P5 410).
The ★ arm's rows in reverse order (P1, P2, P6 182), its whole array as one
row when `n` is 1 (P1, P6 32), and the push arm pushing a value after its
check (P1, P6 285) fail with counts of their own. Three drafts were
replaced, all equivalent: an index edit that wrote the first row twice and
was then overwritten by the original line, a push edit that rebuilt the
fresh row as empty by a roundabout way, and an iter edit `by_ref().take(n +
1).take(n)`, which never skips a value because the outer `take(n)` stops
pulling after `n`, exactly as Rust's iterators do.

## Verification

Every arm prints the same output as `convert.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 1.1 s (index, push) to 3.0 s (Rust)
and the differential 1.6 s.

The five arms were written in Kāra and checked clean, with no fix.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in four rounds (16, 4, 1 and 1 edits). The
first carries the unit struct, the `Vec<..>` types, the `&Vec` parameter,
the `&x` closure pattern and the `::` path; the second turns `as usize`
into `as i64` and `vec![]` into `Vec.new()`, and adds the `.iter()` that
Kāra's `chunks`, which returns a `Vec` of slices, needs before `map`; the
third drops the wrapper's `ref`, which a parameter borrows by default;
the fourth, since kara B-2026-11-13-7, drops the `as i64` in `chunks(n as
i64)`, as `n: i32` widens by itself.

A first iter arm took each row as `iter().skip(i * n).take(n)`: the same
answers, but quadratic, since Kāra's `skip(k)` walks `k` values on both
backends where Rust's slice iterator jumps. It is filed as B-2026-11-08-52; the
arm now shares one iterator through `by_ref()`, the natural way to write
it.

## Benchmarks

The bench builds 20 arrays of 20000 values once in all five languages,
gives each a row count from the divisors of 20000 and every fifth one a
column count that does not fit, and runs the ★ arm on each for 200 rounds:
4000 calls. Every implementation prints `4000 calls: 517600 rows, checksum
826034535`. Every language copies each row into a fresh array, as the Kāra
program does (C with `malloc` and `memcpy`, Go with `make` and `copy`).

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.037 to 0.053 s | 0.040 s |
| Rust (`rustc -O`) | 0.041 to 0.057 s | 0.042 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.041 to 0.058 s | 0.043 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.042 to 0.061 s | 0.043 s |
| Kāra (`karac build`) | 0.042 to 0.054 s | 0.044 s |
| Go | 0.157 to 0.217 s | 0.175 s |
| Python | 0.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.042 s) is not above its real time (0.044 s).

The sequential Kāra program is 1.00x Rust under overflow checks and 1.08x
C.