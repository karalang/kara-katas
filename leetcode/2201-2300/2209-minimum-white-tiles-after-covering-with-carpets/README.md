# 2209. Minimum White Tiles After Covering With Carpets

You are given a **0-indexed binary** string `floor`, which represents the
colors of tiles on a floor:

- `floor[i] = '0'` denotes that the `i`th tile of the floor is colored
  **black**.
- On the other hand, `floor[i] = '1'` denotes that the `i`th tile of the
  floor is colored **white**.

You are also given `numCarpets` and `carpetLen`. You have `numCarpets`
**black** carpets, each of length `carpetLen` tiles. Cover the tiles with
the given carpets such that the number of **white** tiles still visible
is **minimum**. Carpets may overlap one another.

Return *the **minimum** number of white tiles still visible.*

```
floor = "10110101", numCarpets = 2, carpetLen = 2  ->  2
floor = "11111", numCarpets = 2, carpetLen = 3     ->  0
```

**Constraints:** `1 <= carpetLen <= floor.length <= 1000`; `floor[i]` is
either `'0'` or `'1'`; `1 <= numCarpets <= 1000`.

Among the first i tiles with j carpets, the last tile is either left as
it is, adding itself if white, or covered by a carpet that ends there,
which takes one carpet and the len tiles before i with it; so a table of
the fewest visible tiles, by carpets and tiles, fills row by row.
O(n * carpets).

## Approaches

| file | mechanism |
|---|---|
| `tiles.kara` ★ | the whole table, a `Vec[Vec[i64]]` from `Vec.filled`, `best[j][i]` the smaller of leaving tile i - 1 and ending a carpet there, from row j - 1 at `(i - len).max(0)` |
| `tiles_rolling.kara` | a prefix count of white tiles, and only two rows kept, the one for a carpet fewer and the one being filled, swapped by `mem.swap` after each carpet |
| `tiles_memo.kara` | top-down: the fewest visible from tile i on with j carpets in hand, a black tile passed and a white one left or covered by a carpet starting there, remembered in a flat `Vec` |
| `tiles_struct.kara` | a `struct Floor` of the prefix count and the carpet's length, whose `with_one_more` (`ref self`) turns the row for some carpets into the row for one more |
| `tiles_iter.kara` | the row with no carpet a `scan` of running white counts after `once(0)`, each later row a `scan` carrying the row's last entry, and the carpets laid by a `fold` over `0..num_carpets` |
| `tiles_solution.kara` | LeetCode's Rust template: a `String` and two `i32` in, `i32` out, the floor by `as_bytes()`, the table a `vec![vec![0i32; n + 1]; k + 1]` indexed by `usize`, each white tile a `bool` cast `as i32`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and four
more (one tile, no white tile, a carpet as long as the floor, and more
carpets than tiles), each with its answer; then a checksum of 2000
random floors of 1 to 40 tiles, white 2, 4 and 7 times in 8, under 1 to
6 carpets of random length; then the constraints' largest, 1000 tiles
under 1000 carpets of 1, and the same tiles under 100 carpets of 3, 30
of 7 and one of 999. `tiles.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in three rounds of 2, 5 and 1 edits:
first `struct Solution;` to `struct Solution {}` and `Solution::` to
`Solution.`; then `as_bytes()` to Kāra's `bytes()`, the two `as usize`
to `as i64`, the inner `vec![0i32; n + 1]` to `Vec.filled(n + 1, 0i32)`,
and the adapter's `as i64` on an `i32` result dropped, since it widens
by itself; then the outer `vec![..; k + 1]` to `Vec.filled`.

Two arms went through the fix loop as first written. The rolling arm
wrote `std.mem.swap`, and the fix made it `mem.swap`. The iter arm wrote
its `scan` closures as Rust's, writing the state through `*seen`; the
check explains that Kāra's `scan` hands the state over by value and
takes `Some((next_state, item))` back, and the fix rewrote both
closures that way. It then wrote the row's leading 0 as
`[0].iter().chain(..)`, which the check refuses: the list's iterator
gives `ref i64` and the `scan` gives `i64`, and the message points at
`.cloned()`; `once(0)` says it directly.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to lay the carpets tried, each carpet at every
start in turn, no earlier than the one before, and the white tiles no
carpet covers counted; no table. It checks 300 random floors of 1 to 10
tiles, white 2, 4 and 7 times in 8 in turn, under 1 to 4 carpets; then
30 floors all white; then 30 whose carpets together reach past the
floor's end. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | it is at most the white tiles, and at least the white tiles less what the carpets can cover |
| P3 | the floor reversed: the same count |
| P4 | one more carpet: no more, and no fewer than one carpet's length less |
| P5 | a black tile added at the front, and one at the back: the same count |
| P6 | each arm agrees with at least three of the other five |

P5 holds because a carpet over the added black tile can slide back by
one onto the old floor and cover everything it covered there.

The differential prints `360 cases: checksum 767487691, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading over
`itertools.combinations_with_replacement` of the starts. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-three edits to the differential, six to the ★ arm, five to the
rolling, memo and struct arms, seven to the iter arm and five to the
template arm, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a carpet one tile long | P1 51, P2 43, P4 9, P6 51 |
| M5 | ★: the last tile never white | P1 46, P2 38, P3 24, P5 46, P6 46 |
| M6 | ★: a black tile counted as white | P1 93, P2 43, P5 144, P6 93 |
| M9 | rolling: the white count from the tile before | P1 29, P3 40, P5 67, P6 29 |
| M10 | rolling: a carpet ending here reaching back from the row before's end | P1 152, P3 101, P5 152, P6 152 |
| M11 | rolling: the tiles left visible from the row before | P1 46, P3 66, P5 87, P6 46 |
| M12 | memo: a black tile counted | P1 159, P2 39, P3 121, P5 201, P6 159 |
| M13 | memo: a carpet covering one tile less | P1 132, P6 132 |
| M14 | memo: a carpet costing nothing to keep | P1 61, P2 50, P6 61 |
| M17 | struct: a white tile counted from the next tile | P1 46, P2 38, P3 4, P6 46 |
| M19 | struct: one carpet laid fewer | P1 129, P6 129 |
| M20 | struct: the count of the first tile lost | P1 40, P2 31, P3 24, P5 40, P6 40 |
| M23 | iter: the running count not carried | P1 42, P2 37, P3 24, P5 47, P6 42 |
| M24 | iter: the bare row counting every tile | P1 33, P3 50, P5 65, P6 33 |
| M33 | iter: the bare row starting at 1 | P1 52, P3 23, P5 31, P6 52 |
| M28 | solution: a carpet reaching the start counted as nothing covered | P1 52, P5 13, P6 52 |
| M31 | solution: the tile read is the one after | P1 9, P2 5, P3 23, P5 41, P6 9 |

P1 and P6 kill all seventeen, P5 twelve, P3 eleven, P2 nine and P4 one.
P2 holds for any answer between the white tiles and what the carpets
could cover, so it misses the edits that only misjudge which tiles a
carpet reaches or how many carpets there are (M9, M10, M11, M13, M19,
M24, M28, M33). P3 and P5 kill the edits that treat one end of the floor
apart, which the reversal and the added black tiles move. P4 kills only
the carpet one tile long (M2), where one more carpet takes off more than
a carpet's length.

Of the thirty-three, sixteen were not kept. Fifteen are killed and fail
as a kept one does or their own way: a carpet one tile short in the ★,
iter and template arms (M1, M22, M30) as M13; a carpet one tile long in
the struct arm and the template's adapter (M18, M27) as M2; the ★ arm's
carpet ending here taken from the same row, the rolling arm's no-carpet
row all zero, the memo arm's key ignoring the carpets and its white tile
left with no carpet free, and the template's first row never counting
(M3, M8, M15, M16, M29) as M14, each answering 0 or less than the white
tiles allow; one carpet fewer in the ★ and iter arms (M4, M25) as M19;
the iter arm's row entry one tile early (M26) as M5; the struct arm's
visible tiles carried from the row before (M21) as M11; and the iter
arm's one carpet more (M32) fails its own way and is left out for the
count of three. One survives and is equivalent: the rolling arm's rows
copied rather than swapped (M7), since every entry of the row being
filled but its first, always 0, is written before it is read.

## Verification

Every arm prints the same output as `tiles.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 s to 1.7 s, the iter arm
6.8 s, as each of its rows is a new `Vec` collected through `once`,
`chain` and `scan`, and the differential 1.1 s.

## Benchmarks

The bench builds 8 floors of 1000 tiles once, white 1 to 7 times in 8,
then asks each 40 times with the ★ arm in all five languages, 10 to 249
carpets of 1 to 20 tiles. Every implementation prints `40 passes over 8
floors: checksum 269726929`.

BENCHTAB
