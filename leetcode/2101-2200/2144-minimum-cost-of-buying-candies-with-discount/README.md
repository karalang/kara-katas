# 2144. Minimum Cost of Buying Candies With Discount

A shop is selling candies at a discount. For **every two** candies sold,
the shop gives a **third** candy for **free**.

The customer can choose **any** candy to take away for free as long as
the cost of the chosen candy is less than or equal to the **minimum**
cost of the two candies bought.

- For example, if there are `4` candies with costs `1`, `2`, `3`, and
  `4`, and the customer buys candies with costs `2` and `3`, they can
  take the candy with cost `1` for free, but not the candy with cost
  `4`.

Given a **0-indexed** integer array `cost`, where `cost[i]` denotes the
cost of the `i`th candy, return *the **minimum cost** of buying **all**
the candies*.

```
cost = [1,2,3]          ->  5
cost = [6,5,7,9,2,2]    ->  23
cost = [5,5]            ->  10
```

**Constraints:** `1 <= cost.length <= 100`; `1 <= cost[i] <= 100`.

The dearest candy can never be had free, since nothing costs more to
pair it with; so it is bought with the next dearest, and the third
dearest, the most a free candy can then cost, is taken free. Repeating
from the dearest down, every third candy is free. O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `candies.kara` ★ | sorted dearest first by `sort_by`, and paid for by `enumerate`, `filter` on the place mod 3, `map` and `sum` |
| `candies_count.kara` | no sort: the candies counted by price, at most 100, and the prices walked from 100 down, each candy taking its place in the line; every third place free. O(n + 100) |
| `candies_chunks.kara` | sorted and `reverse`d, cut by `chunks(3)` into the sales the shop makes, each paying for its first two by `take(2)`; the last sale may be short |
| `candies_struct.kara` | a `struct Till` that `ring`s up the candies dearest first (`mut ref self`), each two paid for earning the next free, and gives its `total` (`ref self`) |
| `candies_free.kara` | the whole bill less what is given away: sorted cheapest first, the free candies read off the dearest end by `rev`, `skip(2)` and `step_by(3)` |
| `candies_solution.kara` | LeetCode's Rust template: a `mut cost` parameter sorted in place by `sort_unstable_by`, every third skipped with `enumerate` and `filter` over `\|(i, _)\|` and `\|(_, &c)\|` patterns; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and three
more (one candy, three equal, and a free candy as cheap as the cheaper
of the two bought), each with its cost; then the total and a checksum
over 2000 random baskets of 1 to 20 candies of 1 to 100 or 1 to 5 in
turn; then the constraints' largest, 100 candies: every one 100, one of
each price from 1 to 100, and at random. `candies.py` mirrors the ★ arm
and its output is byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 11, 2 and 1 edits: Rust's spellings (`mut cost: Vec<i32>` to
`cost: own Vec[i32]` with a `let mut cost = cost;`, `Vec<..>` to
`Vec[..]`, the `&c` patterns to `c`, `struct Solution;` to `struct
Solution {}`, the adapter's `&Vec` to `ref Vec`, `Solution::` to `.`);
then `sort_unstable_by` to `sort_by`, since a stable sort is also an
unstable one and the library has only the stable one, and the adapter's
`as i64` dropped, since an `i32` widens on return; then the `ref`
dropped from the adapter's parameter, which borrows already. That last
edit is the `redundant_ref_param` style lint, which `karac fix` turns on
and `karac check` leaves off, so `karac check --output=json` reports
nothing after the second round.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to split the candies into sales is tried, a sale
being one candy bought alone, two bought, or two bought and a third no
dearer than either taken free, and the cheapest split is the answer,
the candies left remembered as a set; no sort is made and no
every-third rule is assumed. It checks 300 random baskets of 1 to 10
candies of 1 to 9 or 1 to 3 in turn; then 30 of candies all one price;
then 30 of 1 to 10 candies of 1 to 49, so that every price the
properties make stays within the 100 the constraints allow. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the cost is the statement read literally |
| P2 | the candies in reverse order: the same cost |
| P3 | every price doubled: twice the cost |
| P4 | three candies of 100 added, dearer than any: the cost and 200 more |
| P5 | every candy listed three times: twice the whole price of the basket |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 baskets: checksum 663530849, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal costs was checked against a Python reading of the same
baskets that splits them into sales its own way. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-three edits to the differential, four to nine to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: sorted cheapest first | P1 172, P6 172 |
| M4 | ★: the free ones paid for instead | P1 360, P4 360, P5 360, P6 360 |
| M5 | ★: unsorted | P1 186, P2 178, P6 186 |
| M7 | count: every candy of a price counted once | P1 252, P4 360, P5 360, P6 252 |
| M9 | count: the place moved only when paid | P1 251, P4 360, P5 324, P6 251 |
| M10 | count: the price 100 never walked | P4 360 |
| M12 | chunks: cut in twos | P1 289, P4 360, P5 360, P6 289 |
| M13 | chunks: each sale paying for one | P1 324, P4 360, P5 360, P6 324 |
| M15 | chunks: a short last sale free | P1 228, P6 228 |
| M16 | struct: the free candy earned after one | P1 307, P4 322, P5 324, P6 307 |
| M17 | struct: the count never reset | P1 190, P4 289, P5 324, P6 190 |
| M20 | struct: the till started one sale in | P1 249, P6 249 |
| M22 | free: the dearest free | P1 344, P6 344 |
| M30 | free: half of each free one taken off | P1 289, P3 155, P4 360, P5 360, P6 289 |
| M33 | free: every fourth free | P1 154, P4 212, P5 324, P6 154 |
| M27 | solution: the adapter dropping the first candy | P1 300, P2 208, P6 300 |
| M29 | solution: the adapter halving the prices and doubling the cost | P1 316, P3 316, P5 323, P6 316 |

P1 and P6 kill sixteen, P4 and P5 ten each, and P2 and P3 two each.
P4 adds three candies of 100, dearer than any, which make the first
sale of their own and pay 200; it sees an edit that gets the rhythm of
the sales wrong, since the three must pay for two and leave the rest as
they were (M4, M7, M9, M12, M13, M16, M17, M33), half a free one taken
off (M30), and the count arm never walking the price 100 (M10), which
no basket of the differential holds and only P4 reaches. P5 lists every
candy three times, which makes every sale three of one price; it sees
the same edits to the rhythm, the half taken off, and the template's
halved prices (M29), whose rounding a basket of odd prices shows. P2
reverses the basket, which every right answer ignores, since each arm
sorts first; it sees the ★ arm left unsorted (M5) and the adapter's
lost first candy (M27). P3 doubles every price; it sees an edit that
does not scale, the half taken off (M30) and the template's halved
prices (M29), which doubling makes exact.

Of the thirty-three, sixteen were not kept, and none is equivalent or
fails by a crash. Fourteen fail as a kept one does: the count arm
walking from the cheapest, the chunks never reversed, the struct rung
up cheapest first, the free arm's free ones from the cheapest end, and
the template sorted cheapest first, as M1; the first of every three
free and the chunks paying for their last two, as M22; every second
free in the ★ and the free arm, as M16; the count's place started at
one and the template's second of three free, as M20; the struct's free
candy paid for too and the free arm's free ones paid twice, as M12; and
the free arm's first free one alone taken off, as M17. Two are killed
with checks of their own but were left out because their arm keeps its
share: the free arm unsorted (P1 191, P2 178, P6 191) and its first
free one the fourth (P1 241, P4 360, P5 360, P6 241).

## Verification

Every arm prints the same output as `candies.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s to 0.3 s and the
differential 1.2 s.

## Benchmarks

The bench builds 1000 baskets of 100 candies of 1 to 100 once; then
solves every basket 100 times, one candy redrawn before each solve so
that no solve repeats one before, with the ★ arm in all five languages;
C sorts by a merge sort, stable like the others' library sorts, since C
has none. Every implementation prints `100000 solves: 339840407 paid in
all, checksum 348425396`.

BENCHTAB
