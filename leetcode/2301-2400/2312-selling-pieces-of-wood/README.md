# 2312. Selling Pieces of Wood

You are given two integers `m` and `n` that represent the height and
width of a rectangular piece of wood. You are also given a 2D integer
array `prices`, where `prices[i] = [h_i, w_i, price_i]` indicates you
can sell a rectangular piece of wood of height `h_i` and width `w_i` for
`price_i` dollars.

To cut a piece of wood, you must make a vertical or horizontal cut
across the **entire** height or width of the piece to split it into two
smaller pieces. After cutting a piece of wood into some number of
smaller pieces, you can sell pieces according to `prices`. You may sell
multiple pieces of the same shape, and you do not have to sell all the
shapes. The grain of the wood makes a difference, so you **cannot**
rotate a piece to swap its height and width.

Return *the **maximum** money you can earn after cutting an* `m x n`
*piece of wood*.

Note that you can cut the piece of wood as many times as you want.

```
m = 3, n = 5, prices = [[1,4,2],[2,2,7],[2,1,3]]   ->  19
m = 4, n = 6, prices = [[3,2,10],[1,4,2],[4,1,3]]  ->  32
```

**Constraints:** `1 <= m, n <= 200`; `1 <= prices.length <= 2 * 10^4`;
`prices[i].length == 3`; `1 <= h_i <= m`; `1 <= w_i <= n`;
`1 <= price_i <= 10^6`; all the shapes of wood `(h_i, w_i)` are
pairwise **distinct**.

Every cut runs across the whole piece, so whatever is done to an `h` by
`w` piece is either selling it whole or one first cut and then the best
for each of the two sides on their own. The best for each size, from
the smallest up, is its price against every first cut: `m n` sizes,
`m + n` cuts each. The most is `200 * 200 * 10^6`, so it is an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `wood.kara` ★ | `best[h][w]` bottom up in a `Vec[Vec[i64]]`, each size its price against every horizontal cut `i` and vertical cut `j`. O(m n (m + n)) |
| `wood_memo.kara` | top down: `most(h, w)` recursing on every cut's two sides, through a `mut ref` table held at -1 until a size is found |
| `wood_half.kara` | the ★ arm's table with the cuts only up to the middle, since a cut at `i` and one at `h - i` leave the same two pieces |
| `wood_map.kara` | the prices in a `Map[(i64, i64), i64]` and the answers memoized in another, the recursion of the memo arm |
| `wood_iter.kara` | each size's best cut from `(1..h).map(..).chain((1..w).map(..)).max()`, `unwrap_or(0)` for a 1 by 1 piece |
| `wood_solution.kara` | LeetCode's Rust template: `i32` sizes and prices in a `Vec<Vec<i32>>`, a `vec![vec![0i64; n + 1]; m + 1]` table indexed by `usize`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; a piece
whose own price beats any cut; one whose only price leaves a strip
unsold; one where a 1 by 1 price beats every larger one; a 100 by 100
piece with 2000 prices up to `10^6`; then 300 random pieces of 1 to 12
by 1 to 12 with up to 20 prices of up to 100, with a checksum and the
money in all. `wood.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one call, reporting 17 edits.
`check` first reports five errors and offers 9 edits for them: `struct
Solution;` to `struct Solution {}`; the six brackets of the two
`Vec<Vec<i32>>`, the method's parameter and the wrapper's rows; `&prices`
to `ref prices`; and `Solution::` to `Solution.` in the wrapper. The
other eight follow from those: the two `as usize` on `m` and `n` to `as
i64`; the two `vec!` of the table to `Vec.filled`, and the suffix of
`0i64` dropped; the two `as usize` on a price's height and width
dropped, since an index may be any integer; and the wrapper's
`vec![h as i32, w as i32, p as i32]` to an array literal, collected as
it is into the rows.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a piece fetches the price listed for its shape, found by
walking the list, or whatever any one cut across it makes of its two
sides, each read the same way, with nothing remembered. No table and no
memo. It checks 300 random pieces of 1 to 5 by 1 to 5 with up to 8
prices of up to 20; then 30 with every shape that fits priced near its
area, where many ways tie; then 30 of 5 by 5 with one or two prices of
up to 1000, where strips are left unsold. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at least any fitting shape's price times how many such pieces tile the wood, and at most the area times the largest price |
| P3 | the piece and every shape turned on their side: the same answer |
| P4 | every price doubled: the answer doubled |
| P5 | the whole piece priced at one more than the answer: one more |
| P6 | each arm agrees with at least three of the other five |

P3 holds because turning the wood turns every cut with it, and P5
because no way of cutting made more than the answer, so selling the
piece whole is now the best.

The differential prints `360 cases: checksum 834980703, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and runs the same recursion, memoized. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the cut at height 1 never made | P1 154, P2 151, P3 249, P6 154 |
| M5 | ★: the answer one width short | P1 311, P2 298, P3 293, P5 360, P6 311 |
| M6 | ★: the full height never cut | P1 321, P2 321, P6 321 |
| M8 | memo: a horizontal cut's lower side one shorter | P1 197, P2 175, P3 258, P6 197 |
| M9 | memo: the last vertical cut never made | P1 165, P2 158, P3 249, P6 165 |
| M10 | memo: a vertical cut worth its better side alone | P1 220, P2 212, P3 275, P6 220 |
| M13 | half: a vertical cut's right side one narrower | P1 225, P2 211, P3 267, P6 225 |
| M14 | half: the last horizontal cut kept, not the best | P1 151, P2 138, P3 180, P5 301, P6 151 |
| M15 | half: the widths walked from 2 | P1 44, P2 43, P3 83, P6 44 |
| M17 | map: the price of the shape turned | P1 128, P2 92, P5 252, P6 128 |
| M18 | map: the memo read by height alone | P1 231, P2 133, P3 254, P6 231 |
| M20 | map: the memo written for the shape turned | P1 106, P2 61, P3 130, P6 106 |
| M22 | iter: the worst cut, not the best | P1 189, P2 183, P6 189 |
| M24 | iter: no vertical cut | P1 253, P2 251, P3 256, P6 253 |
| M26 | iter: a cut preferred to the price | P1 65, P2 55, P5 334, P6 65 |
| M27 | solution: each price one less | P1 360, P2 330, P4 360, P5 360, P6 360 |
| M29 | solution: height 1 never cut | P1 39, P2 39, P3 83, P6 39 |

P1, P2 and P6 kill all seventeen, P3 twelve, P5 five and P4 one. P2's
floor, a shape's price times how many of it tile the wood, is reached
by cutting alone, so nearly every edit that loses a cut falls under it.
P3, the wood turned, fails where an edit treats the two directions
apart: a cut at one height or width missing, one side of a cut in one
direction misread, a memo keyed by height alone. P5, the whole piece
priced one more, fails where the piece's own price is not weighed
against its cuts as it should be: the answer read one width short, the
last cut kept rather than the best, a cut preferred to the price, the
price of the shape turned, and the prices one less. P4, every price
doubled, fails only for the prices one less, the one edit whose error
does not double with them.

Of the thirty-one, fourteen were not kept. The ★ arm's no vertical cut
(M3) fails as the iter arm's (M24); the ★ (M4) and iter (M25) arms'
horizontal cut's two sides alike fail alike, the half arm's middle
height never cut (M12) as the map arm's horizontal cuts only below the
middle (M19), and the map arm's unpriced piece worth 1 (M21) as the iter
arm's piece with no cut worth one more (M23), and none of those six is
kept; the template's last width never filled (M28) fails as the ★
arm's full height never cut (M6). The ★ arm's prices never read (M1),
the memo arm's unset memo trusted (M7) and memo read by height alone
(M11), the half arm's price only for a square piece (M16), and the
template's answer from the square (M30) and cut's lower side one
narrower (M31) fail apart from every kept one, and were left out to
keep three to an arm. M8 replaces the memo arm's lower side one
narrower, which reached a width of -1 and crashed on the index.

## Verification

Every arm prints the same output as `wood.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the half arm takes 0.5 s, the ★, template, memo
and iter arms 1.1 to 1.6 s, most of it the 100 by 100 piece, and the map
arm, hashing a pair for every lookup, 2.9 s. The differential takes 7.1
s there, most of it the literal reading's recursion without a memo, and
0.7 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 lists of up to 2000 prices for pieces up to 200 by
200 once, each shape at most once, then makes 2 passes, pass `p` adding
`p` to every price of a fresh copy of each list, and sells a 200 by 200
piece for each with the ★ arm in all five languages. Every
implementation prints `2 passes over 10 lists of 2000 prices on 200 by
200: checksum 219883353`. Each fills a table of `201 * 201` 64-bit
integers for every call: a `Vec` of `Vec`s in Kāra, Rust, Go and
Python, and one static two-dimensional array in C, cleared each time.

BENCHTAB
