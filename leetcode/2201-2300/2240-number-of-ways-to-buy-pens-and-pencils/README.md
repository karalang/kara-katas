# 2240. Number of Ways to Buy Pens and Pencils

You are given an integer `total` indicating the amount of money you
have. You are also given two integers `cost1` and `cost2` indicating
the price of a pen and pencil respectively. You can spend **part or
all** of your money to buy multiple quantities (or none) of each kind
of writing utensil.

Return *the **number of distinct ways** you can buy some number of pens
and pencils.*

```
total = 20, cost1 = 10, cost2 = 5   ->  9
total = 5,  cost1 = 10, cost2 = 10  ->  1
```

**Constraints:** `1 <= total, cost1, cost2 <= 10^6`.

For each number of pens the money allows, the pencils the rest buys,
plus buying none; summed over the pens. O(total / cost1). The answer
reaches 500001500001 for `total = 10^6` and both prices 1, so it is an
`i64`.

## Approaches

| file | mechanism |
|---|---|
| `ways.kara` ★ | a `while` over the number of pens, adding `(total - pens * cost1) / cost2 + 1` |
| `ways_dearer.kara` | the prices destructured into `(dear, cheap)` and the walk over the dearer item, which the money buys fewer of |
| `ways_floor.kara` | no loop over the pens: with `P` the most pens and `r` the money left after them, the count is `P + 1` plus the floor sum of `(cost1 * i + r) / cost2` over `i` in `0..P + 1`, computed by Euclid-like reduction that swaps the two prices each round; O(log) |
| `ways_struct.kara` | a `struct Shop` of the money and the two prices, with `most_pens`, `pencils_after` and `ways` (`ref self`) |
| `ways_iter.kara` | `(0..=total / cost1).map(...).sum()` |
| `ways_solution.kara` | LeetCode's Rust template: `i32` in and `i64` out, a `while` with an `i32` count of pens and each term cast `as i64` before it is added; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and five
more (everything costing 1, the constraints' largest with both at 1,
everything at the constraints' top, prices that do not divide the
money, and one price far above it), each with its count; then a
checksum of 3000 random cases with the money and the prices up to 100,
10^4 and 10^6 in turn; then the money at 10^6 with pens at 1 and the
pencils at 2, 999 and 10^6, so that every arm but the floor sum walks a
million pens. `ways.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 3 edits: `struct
Solution;` to `struct Solution {}`, `Solution::ways_to_buy_pens_pencils`
to `Solution.ways_to_buy_pens_pencils`, and the `as i64` on each `i32`
term removed, since adding an `i32` to an `i64` widens it implicitly.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of a number of pens and a number of pencils tried
in a nested loop, and those the money pays for counted; no division. It
checks 300 random cases, the money up to 60 and the prices up to 20;
then 30 with one price above the money; then 30 with the two prices
equal. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the count of affordable pairs, read literally |
| P2 | the two prices swapped: the same answer |
| P3 | one more unit of money: no fewer ways |
| P4 | the prices doubled and the money doubled plus one: the same answer |
| P5 | at least the pens alone, the pencils alone and nothing, and at most every number of pens with every number of pencils |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 659859622, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that counts
the affordable pairs in a comprehension over ranges bounded by the
money. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the two prices mixed up in the term | P1 245, P2 250, P3 32, P4 57, P5 158, P6 245 |
| M5 | ★: two pens a step | P1 294, P2 200, P5 179, P6 294 |
| M6 | ★: the money not spent on pens | P1 266, P6 266 |
| M8 | dearer: the spending never reaching all the money | P1 27, P4 27, P5 6, P6 27 |
| M9 | dearer: the cheap item divided by the dear price | P1 262, P5 196, P6 262 |
| M10 | dearer: the spending doubled each step | P1 266, P5 134, P6 266 |
| M12 | floor: the triangle `(n - 1) * n / 2` one row short | P1 250, P2 120, P3 17, P5 80, P6 250 |
| M13 | floor: the offset's whole part counted once, not `n` times | P1 117, P2 166, P3 7, P6 117 |
| M14 | floor: the prices never swapped | P1 154, P2 213, P5 36, P6 154 |
| M17 | struct: the most pens one fewer at an exact multiple | P1 51, P2 82, P4 51, P5 14, P6 51 |
| M18 | struct: the pencils at the pen's price | P1 262, P2 262, P5 188, P6 262 |
| M21 | struct: two for buying nothing | P1 360, P2 262, P5 144, P6 360 |
| M23 | iter: the pens at the pencils' price | P1 208, P2 242, P3 29, P4 11, P5 73, P6 208 |
| M24 | iter: a pen costing 1 in the money left | P1 252, P2 133, P4 152, P6 252 |
| M26 | iter: the most pens counted by the pencils' price | P1 245, P2 250, P3 29, P4 56, P5 156, P6 245 |
| M28 | solution: the pens stepping by the price | P1 279, P2 247, P4 89, P5 263, P6 279 |
| M30 | solution: the pencils' price handed in for both | P1 262, P2 262, P5 179, P6 262 |

P1 and P6 kill all seventeen, P5 fourteen, P2 thirteen, P4 seven and P3
five. P2's swap catches every edit that treats the two prices
differently, which is nearly all of them; the edits it misses are those
that stay symmetric by accident or go wrong only in the dearer arm,
which swaps the prices itself. P4 scales the money and the prices so
that every exact multiple becomes one short of the next, which is where
an off-by-one at the money's end (M8, M17) shows.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. One survives and is equivalent: the dearer arm
walking the cheaper item instead (M7), since the count is symmetric in
the two prices and only the number of steps changes. Two fail as a kept
one does: the ★ arm's and the template's last pen count missed (M2,
M29) as the struct arm's most pens one fewer (M17), and the struct
arm's pens and pencils at one price (M20) as its pencils at the pen's
price (M18). Nine fail alike in groups of their own: buying no pencils
not counted in the ★ arm and the template (M1, M27); the pens counted
from one in the ★ and iter arms (M3, M25); the dearer arm's nothing for
the last and the floor arm's missing plus one (M11, M15); and the
struct and iter arms' range not inclusive (M19, M22). Two fail their own
way and are left out for the count of three (two for the template): the
floor arm's money left forgotten (M16) and the template's count from one
(M31).

## Verification

Every arm prints the same output as `ways.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the floor and dearer arms take 0.2 s and 0.3 s,
the ★, template and struct arms 0.9 s to 1.2 s, the iter arm 3.9 s, and
the differential 0.2 s.

## Benchmarks

The bench counts 300 cases with the money at 10^6, a pen from 1 to 10
and a pencil up to 10^6, so that each walks 10^5 to 10^6 pens, with the
★ arm in all five languages. Every implementation prints `300 cases of
10^6 money: checksum 280736403`.

BENCHTAB
