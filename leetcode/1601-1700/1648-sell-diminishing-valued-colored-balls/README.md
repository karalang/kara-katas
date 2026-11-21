# 1648. Sell Diminishing-Valued Colored Balls

You have an `inventory` of different colored balls, and there is a
customer that wants `orders` balls of **any** color.

The customer weirdly values the colored balls. Each colored ball's value
is the number of balls **of that color** you currently have in your
`inventory`. For example, if you own `6` yellow balls, the customer would
pay `6` for the first yellow ball. After the transaction, there are only
`5` yellow balls left, so the next yellow ball is then valued at `5`
(i.e., the value of the balls decreases as you sell more to the
customer).

You are given an integer array, `inventory`, where `inventory[i]`
represents the number of balls of the `i`th color that you initially
own. You are also given an integer `orders`, which represents the total
number of balls that the customer wants. You can sell the balls **in any
order**.

*Return the **maximum** total value that you can attain after selling*
`orders` *colored balls*. As the answer may be too large, return it
**modulo** `10^9 + 7`.

```
inventory = [2,5], orders = 4  ->  14
inventory = [3,5], orders = 6  ->  19
```

**Constraints:** `1 <= inventory.length <= 10^5`;
`1 <= inventory[i] <= 10^9`;
`1 <= orders <= min(sum(inventory[i]), 10^9)`.

## Approaches

| file | mechanism |
|---|---|
| `balls.kara` ★ | the counts sorted largest first and sold from the top down in layers: the `i + 1` largest stand level, and selling them down to the next color's count is whole rows of an arithmetic series, summed by a closure; when the orders run out partway, the full rows left and then a part row. O(n log n) |
| `balls_search.kara` | a binary search on the last price t: every ball worth more than t is sold, and the rest of the orders at t, for the lowest t with no more balls above it than orders. O(n log m) |
| `balls_heap.kara` | the counts in a largest-first heap, a `PriorityQueue` of `Reverse` counts; the colors at the top level are popped together and sold down to the next level as one block. O(n log n) |
| `balls_solution.kara` | LeetCode's Rust template: `sort_unstable_by(\|a, b\| b.cmp(a))` and the layers, with a `range_sum` closure. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, one color
sold out (28), three colors level (18), and one color of `10^9` balls all
sold, which wraps the modulus (21); then the profits summed and a
checksum for 3000 random inventories of up to 4 colors of up to 6 balls,
1000 of up to 100 colors of up to `10^9`, and 20 of up to `10^5` colors
of up to `10^9`, each with an order for 1 to all of the balls, at most
`10^9`. `balls.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: one ball at a time, each from a color with the most balls
left, worth that many. It checks 3000 random inventories of 1 to 5
colors with 1 to 8 balls each, and an order for 1 to all of the balls,
small enough that no profit reaches the modulus. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the profit is the statement read literally |
| P2 | the inventory reversed gives the same profit |
| P3 | one more order, while balls are left, adds between 0 and the largest count |
| P4 | one more color of a single ball leaves the profit as it is |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 233935953, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. One first try was replaced: the heap
arm forgetting to widen the block for a color it pops (`width += 1`
dropped) hangs on both backends, since the orders then never run out.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the part row priced one too low | P1 1331, P3 69, P4 361, P5 1331 |
| M2 | ★: the counts left smallest first | P1 612, P4 1237, P5 612 |
| M3 | ★: a whole layer counted as one row of orders | P1 1036, P3 100, P4 738, P5 1036 |
| M4 | search: the orders left priced past one price too low | P1 2593, P3 324, P4 288, P5 2593 |
| M5 | search: each color's series one ball short | P1 2954, P3 132, P4 274, P5 2954 |
| M6 | heap: the block sold down one level short | P1 2526, P3 123, P4 232, P5 2526 |
| M7 | heap: the part row never sold | P1 1331, P3 392, P4 361, P5 1331 |
| M8 | template: the part row never sold | P1 1331, P3 392, P4 361, P5 1331 |
| M9 | template: the colors sold down to 1, not 0 | P1 769, P5 769 |
| M10 | template: each layer one color wider | P1 2559, P5 2559 |

## Benchmarks

The bench draws 100 random inventories of `10^5` colors with up to
`10^9` balls each, and an order for up to `10^9` of them, all of them
first, then answers each by the ★ arm in all five languages, the counts
copied and sorted per call in each. Every implementation prints `100
inventories of 100000 colors: profits sum to 43174257685, checksum
581166886`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| Kāra (`karac build`) | 0.239 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.240 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.271 s |
| Rust (`rustc -O`) | 0.286 s |
| C (`clang -O3`) | 1.431 s |
| Go | 1.802 s |
| Python | 7.3 s |

The sequential Kāra build is 16% faster than Rust and 11% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.257 s and
0.269 s on one run).

## Verification

All four arms print the same output as `balls.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ arm checked clean as first written, `const MOD` in the body and
the `series` closure included. The search arm first declared its bounds
Rust's way, `let (mut low, mut high) = ..`, and `karac fix` moved the
`mut` before the pattern. The heap arm pushed `Reverse { value: b as i64
}`, and the `lossless_cast` lint dropped the cast.

LeetCode's Rust template takes one `karac fix` of 9 edits: `struct
Solution;` to `struct Solution {}`, the `mut inventory: Vec<i32>`
parameter to `inventory: own Vec[i32]` with `let mut inventory =
inventory;` first in the body (and the wrapper's parameter to `own` to
match), `sort_unstable_by` to `sort_by`, the closure's `-> i64` dropped,
and `(i + 1) as i64` to `i + 1`. The arm then checks and agrees with no
hand edit.
