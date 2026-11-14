# 1533. Find the Index of the Large Integer

You are given an integer array `arr` whose values are all equal except
one, which is larger. You cannot read the array; you only have an
`ArrayReader` API:

- `compareSub(l, r, x, y)` compares the sum of `arr[l..=r]` with the sum of
  `arr[x..=y]` and returns `1` if the first is larger, `0` if they are
  equal, `-1` if it is smaller (`0 <= l, r, x, y < length`, `l <= r`,
  `x <= y`);
- `length()` returns the array's length.

Return the index of the larger value. You may call `compareSub` at most
20 times.

```
arr = [7,7,7,7,10,7,7,7]  ->  4
arr = [6,6,12]            ->  2
```

**Constraints:** `2 <= arr.length <= 5 * 10^5`; `1 <= arr[i] <= 100`; all
values are equal but one, which is larger.

## Approaches

Every arm is `fn get_index(reader: ArrayReader) -> i64` over the same
reader. `ArrayReader` is the judge's side, written with LeetCode's `i32`
API: a `shared struct` holding the array's prefix sums, so a comparison
is O(1), and a `mut calls` count. It is `shared` because the API takes the
reader by a plain borrow, as LeetCode's `&self` does, while the judge still
counts every call; that lets the differential hold each arm to its own
number of calls.

| file | mechanism |
|---|---|
| `index.kara` ★ | ternary search: the range is cut into three parts, the first two the same size; comparing those two says which holds the larger value, and equal sums put it in the third. A third kept per call, so 500000 values take at most 13 calls |
| `index_halves.kara` | binary search, half against half; an odd range leaves its middle out of both, and equal halves mean the middle is the answer. At most 18 calls on 500000 values |
| `index_scan.kara` | the values in pairs from the front, each pair compared one against the other; with no difference, the last value. O(n) calls, far over the 20 allowed, and here to be held to its own bound |
| `index_iter.kara` | the scan with iterators: `(0..n - 1).step_by(2)` and `find_map` over the comparisons, `unwrap_or(n - 1)` |
| `index_solution.kara` | LeetCode's Rust template (`get_index(reader: &ArrayReader) -> i32`, the ★ arm with `let (mut lo, mut hi)`), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples, `[1, 2]`,
`[2, 1]` and `[99, 100, 99]`; 500000 values with the larger at 0, 1, the
middle two places and the last two; then checksums of the answers for
3000 random arrays of 2 to 12 values, 300 of 2 to 1000 and 30 of 2 to
500000, each all one value from 1 to 99 but for one larger, up to 100, at
a random place. `index.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the place whose value is above every other, read off the array
itself. It checks 3000 arrays of 2 to 41 values, every random choice
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the arm keeps to its own bound on calls: a third kept per call (plus the last pair) for the ternary arms, a half per call for the binary one, one call per pair for the scans |
| P3 | every value raised by the same amount leaves the answer |
| P4 | the array reversed moves the answer to `n - 1 - answer` |
| P5 | one more equal value in front moves the answer up by one |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 648891478, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. All eleven are
killed, each the same way under both backends; M5 by a hang (the range
stops shrinking), stopped after 40 s under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the third taken as `(hi - lo) / 3` | P1 356, P4 638, P5 762, P6 356 |
| M2 | ★: equal sums keep the third part and the last place of the second | P2 274 |
| M3 | ★: the last pair's answer swapped | P1 1152, P4 1214, P5 1758, P6 1152 |
| M4 | halves: equal halves answer the place before the middle | P1 686, P4 686, P5 1057, P6 686 |
| M5 | halves: a lighter left half keeps one place too many | hangs |
| M6 | scan: the pairs stepped by 1 | P2 1256 |
| M7 | scan: with no difference, the place before the last | P1 104, P4 205, P5 227, P6 104 |
| M8 | iter: the pairs stop one place early | P1 133, P4 261, P5 230, P6 133 |
| M9 | iter: a heavier right value answered with the left place | P1 1435, P4 2198, P5 3000, P6 1435 |
| M10 | template: a heavier first part loses its last place | P1 324, P4 634, P5 553, P6 324 |
| M11 | template: the last pair's comparison read backwards | P1 1152, P4 1214, P5 1758, P6 1152 |

M2 is a correct search that spends more calls than its bound, so only P2
sees it, which is why the call count is a property.

## Benchmarks

The bench builds 100 readers of 2 to 100000 values once, each with one
larger value at a random place, and searches each 20000 times by the ★
arm, in all five languages. Each language's reader keeps the call count
as the API's judge would: Kāra's in a `shared struct`'s `mut` field,
Rust's in a `Cell` behind `&self`, C's and Go's through a pointer. Every
implementation prints `20000 passes over 100 readers of up to 100000
values: checksum 242442159, 19620000 calls`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `fcd87e1f1` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.113 s |
| Rust (`rustc -O`) | 0.123 s |
| Go | 0.127 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.133 s |
| Kāra (`karac build`) | 0.135 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.137 s |
| Python | 7.2 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.12 s and 0.14 s on one run).

Kāra is 1.03x Rust under overflow checks by median. Not traced. Each
search is about ten calls, each two random reads of a prefix-sum table
up to 800 KB, so the time is mostly those reads and the rows sit close
together.

## Verification

All five arms print the same output as `index.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `fcd87e1f1`.

## Writing it

The iterator arm was written in Kāra and checked as written. The ★,
halves and scan arms each took one edit from `karac fix`: `let mut lo = 0`
(the scan's `let mut i = 0`) to `let mut lo: i32 = 0`. Each loop starts
with a comparison against the reader's `i32` length, `while lo < hi`, and
a comparison beside an `i32` leaves a literal at its `i64` default where
it stands, so the `compare_sub(lo, ..)` arguments further down were
refused as narrowing. With the argument first and the comparison after,
the same literal is fixed to `i32` and checks; that order dependence is
filed as B-2026-11-14-1. The refusal names the binding and offers the
annotation, and the arms keep it.

The Rust template took 3, 2 and 1 edits over three rounds: `&ArrayReader`
to `ref ArrayReader`, `let (mut lo, mut hi)` to `let mut (lo, hi)` and
`Solution::get_index(&reader)` to `Solution.get_index(reader)`; then the
tuple's `0` to `0i32` (the same comparison settling it) and the closing
`as i64` dropped (an `i32` widens); then `ref ArrayReader` to
`ArrayReader`, since a parameter borrows already. It checks and agrees
with no hand edit.
