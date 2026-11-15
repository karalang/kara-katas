# 2184. Number of Ways to Build Sturdy Brick Wall

You are given integers `height` and `width` which specify the dimensions
of a brick wall you are building. You are also given a **0-indexed**
array of **unique** integers `bricks`, where the `ith` brick has a
height of `1` and a width of `bricks[i]`. You have an **infinite**
supply of each type of brick and bricks may **not** be rotated.

Each row in the wall must be exactly `width` units long. For the wall
to be **sturdy**, adjacent rows in the wall should **not** join bricks
at the same location, except at the ends of the wall.

Return *the number of ways to build a **sturdy** wall.* Since the answer
may be very large, return it **modulo** `10^9 + 7`.

```
height = 2, width = 3, bricks = [1, 2]  ->  2
height = 1, width = 1, bricks = [5]     ->  0
```

**Constraints:** `1 <= height <= 100`; `1 <= width <= 10`; `1 <=
bricks.length <= 10`; `1 <= bricks[i] <= 10`; all the values of
`bricks` are unique.

A row is known by where its joints fall, a bit mask of the places 1 to
width - 1; there are at most 2^9 = 512 rows. Two rows can sit one on the
other when their masks share no bit, at most 3^9 pairs. Then the rows
are stacked: the ways to build a wall whose top row is each mask, one
row more at a time. O(rows^2 + height * pairs).

## Approaches

| file | mechanism |
|---|---|
| `sturdy_wall.kara` ★ | every row found by a recursion over the bricks, pushing its joint mask onto a list passed `mut ref`; the rows each can sit on listed once in a `Vec[Vec[i64]]`; the rows stacked a row at a time |
| `sturdy_wall_bits.kara` | every one of the 2^(width - 1) joint masks tried, kept as a row when every gap is a brick's length, read from a `Vec.filled(width + 1, false)`; the rows stacked with each pair compared afresh; O(height * rows^2) |
| `sturdy_wall_memo.kara` | top down: the ways to lay the rows still to go on a row below, the sum over every row that fits on it, each answer kept in a `Vec[Vec[i64]]` memo passed `mut ref` |
| `sturdy_wall_struct.kara` | a `struct Courses` of the rows, grown brick by brick from a stack of partial rows popped by `while let`, and the rows each one `carries`, made `of` a width and the bricks; it says how many walls it can `stack` to a height (`ref self`) |
| `sturdy_wall_iter.kara` | the joint masks `filter`ed to those whose cuts, a range `filter`ed with the ends `chain`ed on, give gaps by `windows` that are `all` bricks; the rows each carries `filter`ed and `collect`ed; the stacking a `fold` over the height, each count a `fold`ed sum |
| `sturdy_wall_solution.kara` | LeetCode's Rust template: `i32` sizes, an inner `fn dfs` over `&Vec<i32>` pushing `u32` masks into `&mut Vec<u32>`, a `const MOD: i64`, `vec![1i64; n]`, `.sum::<i64>()`; carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and four
more (one row of every brick, a column of one brick, two rows that must
share a joint, and the constraints' largest wall of three bricks), each
with its count; then the total and a checksum over 300 random walls up
to 10 x 10, each length of brick from 1 to 10 had with a chance of a
third; then three walls of the constraints' largest size, 100 x 10: of
every brick, of 1 and 2, which leave only one wall, and of 2, 3 and 5.
`sturdy_wall.py` mirrors the ★ arm and its output is byte-identical.

The iterator arm went through `karac fix` twice: its `[0].iter()` and
`[width].iter()`, chained to a range of `i64`s, each took a `.cloned()`
(the second only once the first was in), and `cuts.windows(2)`, which
is a `Vec` of slices in Kāra, took an `.into_iter()` before its `all`.

`karac fix` carries the template in four rounds of 22, 2, 5 and 3
edits: Rust's spellings (`Vec<..>` to `Vec[..]`, `&Vec<i32>` to `ref
Vec[i32]`, `&mut Vec<u32>` to `mut ref Vec[u32]`, the `&b` pattern and
the `&bricks` and `&mut rows` arguments, `.sum::<i64>()`'s turbofish,
`struct Solution;` and `Solution::`, among them); then the inner `fn
dfs` moved out to the top level, as Kāra has no nested items; then
`mut` on the two recursive calls' `rows`, the `i64` suffixes of `vec![1i64;
n]` and `vec![0i64; n]`, and the adapter's widening `as i64` dropped;
then each `vec![v; n]` to `Vec.filled(n, v)` and the `ref` on `bricks`
dropped, since a parameter borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every wall laid brick by brick, row by row, a brick refused
when it would end where a brick of the row below ends inside the wall,
and the walls that fill every row counted. No joint masks and no
row-by-row count. It checks 300 random walls of 1 to 3 rows of width 1
to 5, each length of brick from 1 to 6 had with a chance of a half;
then 30 with a brick of 1 among them; then 30 of 4 or 5 rows of width 1
to 4. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the bricks in the other order: the same count |
| P3 | a brick longer than the width added: the same count |
| P4 | one row more: at most the count times the ways to lay one row |
| P5 | one row: the ways to make the width of the bricks, counted on their own; and at least 1 when a brick is the width |
| P6 | each arm agrees with at least three of the other five |

P2 holds since a wall does not care in what order the bricks were
offered. P3 holds since a brick longer than the width fits in no row.
P4 holds since a wall one row higher is a wall with a row on top, and
not every row fits on every wall. P5 holds since the walls of one row
are the rows, each a run of bricks adding up to the width, and a brick
as wide as the wall makes a wall of any height, one brick a row, with
no joints at all.

The differential prints `360 walls: checksum 380614371, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
walls. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-eight edits to the differential, five to each Kāra arm and three
to the template, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the wall's end taken as a joint | P1 149, P5 116, P6 149 |
| M3 | ★: a brick past the end let finish a row | P1 346, P3 360, P5 349, P6 346 |
| M4 | ★: one row too many | P1 135, P5 185, P6 135 |
| M6 | bits: the last gap never checked | P1 243, P5 243, P6 243 |
| M8 | bits: no joint just before the end | P1 143, P5 168, P6 143 |
| M10 | bits: a bad gap never refused | P1 272, P5 272, P6 272 |
| M13 | memo: the memo by the rows left alone | P1 94, P2 94, P6 94 |
| M14 | memo: a row fitting when it differs | P1 146, P5 52, P6 146 |
| M15 | memo: the first row never at the bottom | P1 216, P2 94, P4 55, P5 275, P6 216 |
| M18 | struct: the first row carried by none | P1 149, P2 7, P5 73, P6 149 |
| M19 | struct: one row too few | P1 92, P6 92 |
| M20 | struct: each top row's ways squared | P1 73, P4 100, P6 73 |
| M21 | iter: a row kept when any gap is a brick | P1 137, P5 137, P6 137 |
| M22 | iter: the end taken one short | P1 251, P5 242, P6 251 |
| M25 | iter: the largest top row's ways, not their sum | P1 147, P4 112, P5 147, P6 147 |
| M27 | solution: one more for every row that fits | P1 149, P4 122, P6 149 |
| M28 | solution: the adapter's bricks one longer | P1 258, P5 249, P6 258 |

P1 and P6 kill all seventeen, P5 thirteen, P4 four, P2 three and P3
one. P5 counts the rows on its own and asks whether a brick as wide as
the wall builds one; it misses an edit that gets one row right and goes
wrong only as rows are stacked: the memo keyed by the rows left (M13),
one row too few (M19), the ways squared (M20), and one more for every
row that fits (M27). P2 offers the bricks in the other order, which
changes the order the rows are found in, and so which row is first: it
sees the edits that treat one row or one place in the memo apart (M13,
M15, M18). P4 adds a row, and sees an edit whose count grows faster
than a row's choices allow: the ways squared (M20), the largest top
row's ways (M25), one more for every fit (M27), and the first row
never at the bottom (M15). P3 adds a brick too long for the wall, and
only the ★ arm's brick let past the end (M3) uses it.

Of the twenty-eight, eleven were not kept. Two are equivalent: the
memo never read (M11), the same recursion, slower, and the struct arm's
every joint one place early (M16), which moves every row's joints by
the same amount, so the same rows fit. Three fail as a kept one does:
the template's every row a joint at 0, as M1; the iter arm's one row
too many, as M4; and the struct arm's no brick ending one before the
end, as M8. Six were left out to keep three to an arm: the ★ arm's two
rows fitting when they share one joint (M2) and its row's own ways
carried up (M5), the bits arm's every brick one shorter (M7) and its
row fitting on itself (M9), the memo arm's last row counted as none
(M12), and the iter arm's masks never shifted (M23).

## Verification

Every arm prints the same output as `sturdy_wall.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ and struct arms take 0.8 s, the iter arm
3.2 s, and the memo, template and bits arms 4.6 s to 5.1 s: those three
compare every pair of rows for every row of the wall, 512^2 pairs a
row at the largest. The differential takes 1.0 s.

## Benchmarks

The bench builds 1000 walls of width 10 and a height of 50 to 100, each
with a random set of brick lengths that holds 1, with the ★ arm in all
five languages: each solve finds the rows, lists the pairs that fit,
and stacks them. Every implementation prints `1000 walls: checksum
367490299`.

BENCHTAB
