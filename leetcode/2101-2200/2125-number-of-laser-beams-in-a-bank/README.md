# 2125. Number of Laser Beams in a Bank

Anti-theft security devices are activated inside a bank. You are given
a 0-indexed binary string array `bank` representing the floor plan of
the bank, which is an `m x n` 2D matrix. `bank[i]` represents the `i`th
row, consisting of `'0'`s and `'1'`s. `'0'` means the cell is empty,
while `'1'` means the cell has a security device.

There is one laser beam between any two security devices if both
conditions are met:

- The two devices are located on two different rows: `r1` and `r2`,
  where `r1 < r2`.
- For each row `i` where `r1 < i < r2`, there are no security devices
  in the `i`th row.

Laser beams are independent, i.e., one beam does not interfere nor
join with another.

Return the total number of laser beams in the bank.

```
bank = ["011001","000000","010100","001000"]  ->  8
bank = ["000","111","000"]                    ->  0
```

**Constraints:** `m == bank.length`; `n == bank[i].length`; `1 <= m, n
<= 500`; `bank[i][j]` is either `'0'` or `'1'`.

A beam joins every device of one row with every device of the next row
that has any, so each such row adds its count times the count of the
last such row above it. One pass over the cells, O(m * n).

## Approaches

| file | mechanism |
|---|---|
| `beams.kara` ★ | each row's devices counted with `bytes().iter().filter(..).count()`; the last nonempty row's count carried in a `for` loop |
| `beams_counts.kara` | the nonempty rows' counts gathered into a `Vec` by a loop over `chars()`, then each times the next summed through `zip` with `skip(1)` |
| `beams_iter.kara` | one chain: `map` to the counts, `filter` the empty rows out, and a `fold` carrying the last count and the beams in a pair, read with `.1` |
| `beams_scan.kara` | index loops over the rows and over each row's `bytes()`; each device takes a beam from every device of the last row that had one |
| `beams_struct.kara` | a `struct Bank { last_devices, beams }` whose `add_row` (`mut ref self`) takes one row at a time |
| `beams_solution.kara` | LeetCode's Rust template: an `i32` count per row through `chars().filter(\|&ch\| ..).count() as i32`, carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (one row, two full rows, empty rows between devices, no device),
each with its answer; then the total and a checksum of the answers over
2000 random banks of 1 to 10 rows of 1 to 10 cells, each a device with
chance a quarter, a half or three quarters in turn; then the
constraints' largest, 500 by 500 all devices and half devices.
`beams.py` mirrors the ★ arm and its output is byte-identical.

The adapter, written as Rust, hands the template its bank with
`bank.clone()`, which Rust's by-value `Vec<String>` needs. Carried, the
parameter is a bare `Vec[String]`, which borrows, so the clone copies
every row on each call for nothing, and neither `karac check` nor
`karac fix` says so. That is filed as karac B-2026-11-14-3, with the 47
kata adapters of the same shape; the arm keeps the clone until a lint
offers to drop it.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of devices in two different rows, counted when
every row between them has no device. It checks 300 random banks of 1
to 5 rows of 1 to 5 cells, each a device with chance a quarter, a half
or three quarters in turn; then 30 of up to 8 rows of up to 8 cells, an
eighth devices, so that empty rows are common; then 30 of one column of
up to 12 rows. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the rows in reverse order: the same answer |
| P3 | a row with no device put after the first: the same answer |
| P4 | a row of devices only put at the bottom: the answer plus its width times the devices of the last row that has any |
| P5 | every row written twice over: four times the answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 banks: checksum 191186197, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
banks. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the first row with devices remembered | P1 100, P2 81, P4 98, P6 100 |
| M4 | ★: the two rows' devices added, not multiplied | P1 315, P2 98, P4 339, P5 327, P6 315 |
| M32 | ★: a row's last cell never read | P1 209, P4 327, P5 204, P6 209 |
| M7 | counts: every other count skipped | P1 225, P4 193, P6 225 |
| M9 | counts: each count squared | P1 129, P2 98, P4 200, P6 129 |
| M10 | counts: every row's count one too many | P1 300, P3 314, P4 360, P5 300, P6 300 |
| M13 | iter: the first row with devices lit from above | P1 327, P2 98, P4 33, P5 327, P6 327 |
| M14 | iter: the last count answered | P1 283, P2 98, P4 360, P5 327, P6 283 |
| M15 | iter: the largest count so far carried | P1 63, P2 61, P4 78, P6 63 |
| M17 | scan: a device beamed to the devices beside it | P1 174, P4 261, P5 327, P6 174 |
| M19 | scan: the first cell of each row skipped | P1 211, P4 327, P5 209, P6 211 |
| M20 | scan: the first row skipped | P1 199, P2 143, P4 67, P6 199 |
| M22 | struct: an empty row clearing the row above | P1 57, P3 169, P4 79, P6 57 |
| M23 | struct: the last row never remembered | P1 233, P4 327, P6 233 |
| M26 | struct: every cell taken as a device | P1 286, P3 360, P4 233, P6 286 |
| M27 | solution: a row of one device skipped | P1 159, P4 191, P5 159, P6 159 |
| M30 | solution: the empty cells counted | P1 263, P3 330, P4 327, P6 263 |

P1, P4 and P6 kill all seventeen, P5 eight, P2 seven and P3 four. P4
sees nearly everything because a full row at the bottom tests the one
step every arm shares, the last count times the new one. P2 sees the
edits that treat the top of the bank unlike its bottom: a count carried
from the first row or the largest one (M1, M15), a first row skipped
(M20) or lit from above (M13), the last count answered (M14), and the
two counts of a pair treated unequally (M4, M9). P3 sees the edits that
a row of zeros changes: one that clears the row above (M22) or counts
as devices (M10, M26, M30). P5 sees the edits whose answer does not grow fourfold when every row's
devices double: a row's own devices beamed together (M17), a cell left
out (M19, M32), a device too many in each row (M10), a sum for a
product (M4), a row of one device skipped (M27), a first row lit from
above (M13) or the last count answered (M14).

Of the thirty-two, fifteen were not kept. Two are equivalent: the ★
arm counting the cells that are not `'0'`, which are the `'1'`s, and
the Rust arm's adapter handing over the rows reversed, since the
answer is the same read from the bottom. None survives. Eight fail as a
kept one does: an empty row clearing the row above in the ★, counts,
iter and scan arms as M22; the ★ arm counting every cell as M26; the
iter arm counting the empty cells as M30; and the struct and Rust arms'
device above the first row as M13. Five are killed with checks of their
own but were left out because their arms keep their share: every row
above summed in the ★ and scan arms (P1 166, P4 233, P6 166), and the
first pair only in the counts arm, the beams overwritten by each row in
the struct and Rust arms (P1 166, P2 93, P4 233, P6 166).

## Verification

Every arm prints the same output as `beams.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 s to 1.1 s, most of it the
two 500 by 500 banks, and the differential 0.57 s.

`karac fix` carries the template in four rounds of 8, 2, 1 and 1 edits:
Rust's spellings (`Vec<..>` to `Vec[..]`, the `&ch` closure pattern to
`ch`, `struct Solution;` to `struct Solution {}`, the adapter's `&Vec<..>`
to `ref Vec[..]` and `Solution::` to `Solution.`); then `ans` annotated
`i32`, since its `0` would otherwise be an `i64` that `prev * c` cannot
be added to, and the adapter's `as i64` dropped, since an `i32` widens
on return; then `prev` annotated `i32` the same way; then the `ref`
dropped from the adapter's parameter, which borrows already.

## Benchmarks

The bench builds 12 banks of 500 rows of 500 cells once, each a device
with chance a quarter, a half or three quarters in turn, then solves
every bank 500 times, one cell flipped before each solve so that no
solve repeats one before, with the ★ arm in all five languages. Every
implementation prints `6000 solves: 218197860941 beams, checksum
600092684`.

BENCHTAB
