# 2218. Maximum Value of K Coins From Piles

There are `n` **piles** of coins on a table. Each pile consists of a
**positive number** of coins of assorted denominations.

In one move, you can choose any coin on **top** of any pile, remove it,
and add it to your wallet.

Given a list `piles`, where `piles[i]` is a list of integers denoting
the composition of the `ith` pile from **top to bottom**, and a positive
integer `k`, return *the **maximum total value** of coins you can have
in your wallet if you choose **exactly*** `k` *coins optimally*.

```
piles = [[1, 100, 3], [7, 8, 9]], k = 2                                       ->  101
piles = [[100], [100], [100], [100], [100], [100], [1, 1, 1, 1, 1, 1, 700]], k = 7  ->  706
```

**Constraints:** `n == piles.length`; `1 <= n <= 1000`;
`1 <= piles[i][j] <= 10^5`; `1 <= k <= sum(piles[i].length) <= 2000`.

From each pile some count of its top coins is taken, so the piles are
the groups of a knapsack: `best[j]` is the most `j` coins are worth from
the piles so far, and a pile is added by trying every count `t` of its
top coins, worth the prefix sum of `t`, with `j - t` taken from the
piles before; `j` runs down so each pile is used once. Every coin is
worth at least 1, so the most for at most `j` coins takes exactly `j`,
and the row can start at 0. O(k * total coins).

## Approaches

| file | mechanism |
|---|---|
| `coins.kara` ★ | one knapsack row of k + 1, each pile's prefix sums built first, the counts running down and every count of the pile's top coins tried |
| `coins_memo.kara` | top down: the most `left` coins are worth from the piles from `at` on, over taking 0 to all of pile `at`'s top coins, remembered in a `Vec[Vec[i64]]` passed as `mut ref`, -1 where the piles left hold too few coins |
| `coins_table.kara` | the whole table, a row for each pile cloned from the one before and raised by every count of the pile's top coins, summed as they are tried |
| `coins_struct.kara` | a `struct Chest` holding the best for every count up to its capacity, with `add` (`mut ref self`) taking one pile in by two `while` loops and `best` (`ref self`) reading a count back |
| `coins_iter.kara` | a `fold` over the piles carrying the row, the prefix sums by a `fold` of their own, and each new row by `map` over the counts and `max` over the coins taken |
| `coins_solution.kara` | LeetCode's Rust template: a `Vec<Vec<i32>>` and an `i32` in, `i32` out, the row a `vec![0; k + 1]` indexed by `usize`, and each pile's top coins by `enumerate().take(j)`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one pile, every coin taken, a deep coin worth the shallow ones above
it, and one coin), each with its answer; then a checksum of 3000 random
cases of 1 to 6 piles of 1 to 5 coins, worth up to 10, 1000 and 10^5 in
turn, with k from 1 to every coin; then the constraints' largest, 1000
piles of 2 coins with k = 1999 and 10 piles of 200 with k = 1000. A coin
worth up to 10^5 is drawn from two draws, since one stops at 32767.
`coins.py` mirrors the ★ arm and its output is byte-identical.

The iter arm was first written with `|mut sums, coin|` on the inner
`fold`'s closure, Rust's way to take an accumulator by value and change
it; `karac check` names that Kāra has no `mut` in a pattern, and `karac
fix` rewrote it to `|sums, coin|` with `let mut sums = sums;` at the top
of the body.

`karac fix` carries the template in one round of 18 edits: `Vec<..>` to
`Vec[..]`, `let k = k as usize` to `let k = k as i64`, `vec![0; k + 1]`
to `Vec.filled(k + 1, 0i32)`, `let mut sum = 0` to `let mut sum: i32 =
0`, as `dp` holds `i32`, the `(t, &c)` and `|&c|` patterns to `(t, c)`
and `|c|`, the adapter's `as i64` on the `i32` result dropped, since an
`i32` widens to `i64` on its own, `struct Solution;` to `struct Solution
{}` and `Solution::` to `Solution.`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every count of each pile's top coins tried, the ways that
take k coins in all kept, and the most any of them is worth; no table.
It checks 300 random cases of 1 to 4 piles of 1 to 4 coins, worth up to
10, 1000 and 10^5 in turn, with k from 1 to every coin; then 30 of one
pile; then 30 whose coins are all worth the same. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the most is the statement read literally |
| P2 | it is at least k times the cheapest coin and at most the k dearest coins together |
| P3 | the piles reversed: the same most |
| P4 | a pile of one coin dearer than all the others put in front, and k one more: the most grows by that coin |
| P5 | k one fewer gives less, and k one more, while coins are left, gives more |
| P6 | each arm agrees with at least three of the other five |

P4 holds because a choice of k + 1 coins without the dear coin can drop
the deepest coin it takes from some pile and take the dear one instead,
for more; so the best choice takes it, and k more from the rest. P5
holds because every coin is worth at least 1.

The differential prints `360 cases: checksum 845894851, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading over
`itertools.product` of the counts taken from each pile. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm, five to each of
the other Kāra arms and to the template arm, each run under `karac
__mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: a pile's t coins added onto the best for j - 1, not j - t | P1 152, P2 134, P3 94, P4 171, P5 106, P6 152 |
| M5 | ★: the best for k - 1 returned | P1 360, P2 153, P6 360 |
| M6 | ★: a coin above 5000 counted twice in the prefix sums | P1 119, P2 110, P4 119, P6 119 |
| M7 | memo: a pile never passed over | P1 94, P3 112, P6 94 |
| M8 | memo: the rest taken from the same pile again | P1 173, P2 142, P3 111, P4 360, P6 173 |
| M9 | memo: piles holding exactly the coins left treated as too few | P1 178, P2 99, P3 113, P4 99, P5 136, P6 178 |
| M13 | table: each row started from 0, not from the row before | P1 75, P3 112, P4 107, P6 75 |
| M15 | table: a pile's coins taken from the bottom | P1 195, P6 195 |
| M16 | table: the answer read from the row before the last pile | P1 293, P2 142, P3 211, P5 212, P6 293 |
| M17 | struct: the best for one coin never worked out | P1 166, P2 105, P3 75, P4 285, P5 17, P6 166 |
| M18 | struct: a pile's last coin never taken | P1 242, P2 75, P4 360, P5 215, P6 242 |
| M20 | struct: a count above 3 read one low | P1 134, P2 16, P4 60, P5 90, P6 134 |
| M23 | iter: the prefix sums starting from 1 | P1 360, P2 221, P4 360, P6 360 |
| M24 | iter: every count's coins added onto the best for j itself | P1 205, P2 195, P4 132, P5 164, P6 205 |
| M25 | iter: the least over the counts tried, not the most | P1 360, P2 360, P4 360, P5 328, P6 360 |
| M30 | solution: a count worth only its deepest coin | P1 231, P2 55, P5 188, P6 231 |
| M31 | solution: each pile's top coin skipped | P1 333, P2 81, P4 360, P5 215, P6 333 |

P1 and P6 kill all seventeen, P2 fourteen, P4 twelve, P5 ten and P3
seven. P3 reverses the piles, so it kills the edits that give the first
or last pile a part of its own or carry the wrong row between piles
(M4, M7, M8, M9, M13, M16, M17). P4 kills the edits that miss the
single dear coin in front or count it wrongly with k one more (M8, M13,
M17, M18, M23, M25, M31 among them). P2's bounds miss only the three
whose answers stay between k cheapest and k dearest (M7, M13, M15).

Of the thirty-one, fourteen were not kept. One crashes under both
backends, as it should: the iter arm's counts tried up to j - 1 leave
nothing to try for j = 0, and `max().unwrap()` panics on the empty
range (M22). The other thirteen are killed, and none differs between
the backends. Seven fail as another does: the ★ arm's counts running up,
the table arm's pile added within its own row and the template's counts
running up (M1, M14, M28) all let a pile be taken twice, alike; the
table arm's counts stopping one short and the template's taking one
fewer (M12, M27) fail as the ★ arm's best for k - 1 (M5); and the memo
arm's rest kept only when above 0, its counts one short and the struct
arm's capacity one less (M10, M11, M19) fail as the iter arm's least
over the counts (M25). Five fail their own way and are left out for the
count of three (two for the template): the ★ arm's counts one short and
its prefix sums of t - 1 (M2, M3), the struct arm's coin t taken as the
next one down (M21), the iter arm's row starting at 1 (M26), and the
template's coins added onto the best for j - t (M29).

## Verification

Every arm prints the same output as `coins.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the memo arm takes 1.2 s, the table, struct and
★ arms 3.8 s to 5.1 s, the iter arm 11 s and the template 14 s, most of
it the two largest cases; the differential takes 0.8 s.

## Benchmarks

The bench draws 20 sets of 100 piles of 10 coins worth up to 10^5 once,
then punches each set 4 times, one coin drawn again each time, and
answers it after each punch with k = 600 with the ★ arm in all five
languages. Every implementation prints `20 sets of 100 piles of 10, k =
600, 4 punches: checksum 951265946`.

BENCHTAB
