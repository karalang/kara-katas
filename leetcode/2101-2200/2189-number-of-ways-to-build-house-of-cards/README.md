# 2189. Number of Ways to Build House of Cards

You are given an integer `n` representing the number of playing cards
you have. A **house of cards** meets the following conditions:

- A **house of cards** consists of one or more rows of **triangles** and
  horizontal cards.
- **Triangles** are created by leaning two cards against each other.
- One card must be placed horizontally between **all adjacent**
  triangles in a row.
- Any triangle on a row higher than the first must be placed on a
  horizontal card from the previous row.
- Each triangle is placed in the **leftmost** available spot in the row.

Return *the number of **distinct** **house of cards** you can build
using **all*** `n` *cards.* Two houses of cards are considered distinct
if there exists a row where the two houses contain a different number
of cards.

```
n = 16  ->  2
n = 2   ->  1
n = 4   ->  0
```

**Constraints:** `1 <= n <= 500`.

A row of k triangles takes 2k cards for the triangles and k - 1 laid
flat between them, 3k - 1 in all, and a row above a row of k stands on
its k - 1 flat cards, so it has fewer triangles. A house is so a set of
distinct row widths, read from the bottom up, whose cards add up to n:
a 0/1 knapsack over the widths. O(n^2 / 3).

## Approaches

| file | mechanism |
|---|---|
| `cards.kara` ★ | a 0/1 knapsack: each width offered once, the counts for every number of cards updated from the top down in a `Vec.filled(n + 1, 0)` |
| `cards_memo.kara` | top down: the houses of the cards left whose bottom row is narrower than the row below, the sum over that row's width; each answer kept in a `Vec[Vec[i64]]` memo passed `mut ref` |
| `cards_table.kara` | by the widest row: the houses whose bottom row is exactly k wide are the houses a row's cards fewer with every row narrower, read off a running sum of the narrower ones |
| `cards_struct.kara` | a `struct Deck` of how many houses each number of cards up to its size builds, made `of` a size; each width is `offer`ed to it (`mut ref self`, a `rev`ersed range), and it says how many houses `use_all` its cards (`ref self`) |
| `cards_iter.kara` | the widths' cards from `(1..)` `map`ped and `take_while` they fit, and a `fold` over them of the counts, each step a new list `collect`ed from a `map` over the numbers of cards |
| `cards_solution.kara` | LeetCode's Rust template: `n: i32` made `usize`, `vec![0i32; n + 1]`, `1usize`, `(cost..=n).rev()`, `struct Solution;`, `Solution::`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples and three
more (one card, the least house of two rows, and the constraints'
largest, 500), each with its count; then, over every n the constraints
allow, 1 to 500, how many build a house, the houses in all and a
checksum. `cards.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in three rounds of 2 edits each:
`struct Solution;` to `struct Solution {}` and `Solution::` to `.`;
then `vec![0i32; n + 1]` to `Vec.filled(n + 1, 0i32)` and the adapter's
widening `as i64` dropped; then the `usize`s, `n as usize` to `n as
i64` and the suffix of `1usize` dropped, once the list's length is an
`i64`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every house built row by row from the bottom, each row's
triangles fewer than the row's below and its cards two a triangle and
one between each two, until the cards run out exactly; and the houses
that use every card counted. No table and no memo. It checks every n
from 1 to 120.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | n one less than a multiple of 3: at least one house, a single row |
| P3 | three cards more: at least as many houses |
| P4 | three cards more: no more new houses than the houses of n + 1 - 3j cards, summed over j from 1 |
| P5 | a house at all exactly when some number of rows r has n + r a multiple of 3 and n at least 3r(r + 1)/2 - r, the least house of r rows |
| P6 | each arm agrees with at least three of the other five |

P2 holds since a row of k triangles is a house of 3k - 1 cards. P3
holds since a triangle more on the bottom row of each house of n cards
is a house of n + 3, and no two give the same one. P4 holds since a
house of n + 3 cards that is not one of those has a bottom row just one
wider than the row above, j + 1 over j; taken away, it leaves a house of
n + 1 - 3j cards, and no two leave the same one. P5 holds since a house
of r rows of S triangles in all takes 3S - r cards, and r distinct
widths add up to any S from r(r + 1)/2 up.

The differential prints `120 counts: checksum 951826628, 4320 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
counts. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, seven to the ★ arm, five to each
other Kāra arm and three to the template, each run under `karac
__mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: rows from two triangles | P1 107, P2 1, P4 1, P5 6, P6 107 |
| M29 | ★: each row counted two ways | P1 114, P4 1, P6 114 |
| M30 | ★: a lone card a house | P1 114, P3 1, P5 5, P6 114 |
| M6 | memo: a row as wide as the one below | P1 115, P4 3, P5 4, P6 115 |
| M7 | memo: the row above two narrower | P1 101, P5 4, P6 101 |
| M10 | memo: the bottom row's widest left out | P1 78, P2 8, P4 4, P5 10, P6 78 |
| M12 | table: the narrower ones never grown | P1 106, P5 74, P6 106 |
| M14 | table: the total read from the narrower | P1 112, P2 8, P4 5, P5 10, P6 112 |
| M15 | table: a row's cards read a card later | P1 114, P2 40, P5 114, P6 114 |
| M16 | struct: a width offered twice | P1 117, P4 3, P5 3, P6 117 |
| M17 | struct: the deck one card short | P1 110, P2 2, P3 1, P5 10, P6 110 |
| M18 | struct: every width past 2 offered as 2 | P1 111, P2 24, P3 24, P4 23, P5 68, P6 111 |
| M22 | iter: a row's cards 3k + 1 | P1 111, P2 3, P4 4, P5 6, P6 111 |
| M23 | iter: the step keeping only what it adds | P1 104, P5 36, P6 104 |
| M25 | iter: the step from a card further | P1 118, P2 40, P4 38, P5 82, P6 118 |
| M26 | solution: the adapter's n one more | P1 110, P2 4, P5 9, P6 110 |
| M27 | solution: the empty house counted | P1 120, P5 6, P6 120 |

P1 and P6 kill all seventeen, P5 sixteen, P2 and P4 nine each, and P3
three. P5 asks only whether there is a house at all, and misses each
row counted two ways (M29), which doubles every count but makes none
from nothing. P3 asks that three cards more build no fewer houses, and
sees only an edit that breaks the growth: a lone card a house (M30),
which 4 cards do not keep, the deck one short (M17), and every width
past 2 as 2 (M18). P2 asks for the single row, and misses an edit that
still counts it: each row two ways (M29), a lone card (M30), a row as
wide as the one below (M6), two narrower (M7), the narrower never grown
(M12), the knapsack updated with a width twice (M16), the step keeping
only what it adds (M23), and the empty house (M27). P4 bounds the new
houses of three cards more, and misses an edit that adds or takes away
the same at every n, or less: M30, M7, M12, M15, M17, M23, M26 and M27.

Of the thirty, thirteen were not kept. Three are equivalent: the memo
arm's memo read by the cards alone (M8), a slot never written, so the
memo is never read and the recursion gives the same counts, slower;
the table arm's narrower-than counts grown again after they are read
(M11), a write nothing reads; and the iter arm's widths from 0 as 3k +
2 (M21), the same widths. Seven fail as a kept one does: the ★ arm's
width taken any number of times and the struct arm's offer upward, as
M6, each letting a width be taken twice; the ★ arm's row of 3k cards,
as M25; its widest row that fits left out, as M10; and its update
stopped one short and the memo arm's row stopping short of the cards
left, as M15, each losing the house of one row as wide as the cards;
and the struct arm's no empty house, as M17. Three were left out to keep
three to an arm: the table arm's widest row one short (M13) and the
iter arm's widths while below n (M24), which fail alike, and the
template's widths stepping by two (M28).

## Verification

Every arm prints the same output as `cards.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ arm takes 1.9 s, the table, template and
struct arms 4.4 s to 6.2 s, and the memo and iter arms 18 s and 20 s:
the memo arm recurses afresh for every n from 1 to 500, and the iter
arm builds a new list for every width. The differential takes 7.9 s,
as P4 asks each arm about every smaller n.

## Benchmarks

The bench solves 20000 random n of 1 to 500, with the ★ arm in all five
languages; C callocs its list per solve, as the others make theirs.
Every implementation prints `20000 solves: checksum 287734435`.

BENCHTAB
