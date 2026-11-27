# 1801. Number of Orders in the Backlog

You are given a 2D integer array `orders`, where each `orders[i] =
[price_i, amount_i, orderType_i]` says that `amount_i` orders of type
`orderType_i` were placed at the price `price_i`: a `0` is a batch of
buy orders, a `1` a batch of sell orders. The orders are placed in the
order they are given. The backlog starts empty. When a buy order is
placed, it looks at the sell order with the smallest price in the
backlog: if that price is smaller than or equal to its own, the two
match and are executed, and the sell order is removed from the backlog;
else the buy order joins the backlog. When a sell order is placed, it
looks at the buy order with the largest price in the backlog the same
way, matching when that price is larger than or equal to its own. Return
the total amount of orders in the backlog after every order is placed,
modulo `10^9 + 7`.

```
orders = [[10,5,0],[15,2,1],[25,1,1],[30,4,0]]                          ->  6
orders = [[7,1000000000,1],[15,3,0],[5,999999995,0],[5,1,1]]            ->  999999984
```

**Constraints:** `1 <= orders.length <= 10^5`, `1 <= price_i, amount_i
<= 10^9`, and `orderType_i` is `0` or `1`.

The arms are `fn get_number_of_backlog_orders(orders: Vec[Vec[i32]]) ->
i32`.

## Approaches

| file | mechanism |
|---|---|
| `get_number_of_backlog_orders.kara` ★ | the buys in a `PriorityQueue.max_first()` of `(price, amount)`, the sells in a `PriorityQueue.new()`, which gives the lowest first; each batch matched against the other side's best while it crosses, taking whole batches off and pushing back what is left of the last. O(n log n) |
| `get_number_of_backlog_orders_sorted.kara` | each side a `SortedMap` from price to the amount resting there, a buy taking the sells from `first()` up and a sell the buys from `last()` down, the side chosen once as a pair of `mut ref`s. O(n log n) |
| `get_number_of_backlog_orders_negate.kara` | both sides in queues that give the largest first, a sell's price written negated so that its lowest comes out first, as Python's `heapq` users write a max-heap. O(n log n) |
| `get_number_of_backlog_orders_sortedvec.kara` | each side a `Vec` kept sorted with its best price last, the buys rising and the sells falling: a match comes off the end, and a resting batch goes in at its place by `partition_point` and `insert`. O(n^2) at worst, for the moves |
| `get_number_of_backlog_orders_solution.kara` | a Rust solution as LeetCode's Rust users write it (`BinaryHeap<(i32, i32)>`, `BinaryHeap<Reverse<(i32, i32)>>`, `sell.peek().unwrap().0 .0`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`6
999999984`); six edges, one order, a buy below a sell, which never meet,
a buy and a sell that cancel, a sell met by a buy at its own price, a
buy that clears three sells and rests, and two buys of `10^9`, which
pass the modulus (`3 5 0 3 4 999999993`); the constraints' most, `10^5`
buys of `10^9` and `10^5` orders at random of prices and amounts of up
to `10^9` (`the most: 999300007 358025303`); and 3000 random cases of 1
to 20 orders of prices and amounts of 1 to 10 (`3000 random cases:
checksum 36415657`). `get_number_of_backlog_orders.py` mirrors the ★ arm
with `heapq`, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the bench and the harness check clean as first written.
The ★ arm was first written with Rust's `.sum::<i64>()`, which check
refuses as a turbofish, and with `Some((p, _)) if *p <= price` over
`sells.peek()`, where the pattern binds `p` as the copied `i32` and
check says to drop the `*`; `karac fix` applied the 4 edits. The sorted
arm picked its two sides as `(mut buys, mut sells)`, the marker a call
argument takes, where a borrow for writing is `mut ref buys`, and read a
price's amount with Rust's `.copied()`, where Kāra's `Option[ref T]` has
`.cloned()`; `karac fix` wrote both, 5 fixes. The negate and sortedvec
arms each dropped a `*` from a closure's tuple pattern the same way, 1
fix and 2.

The Rust solution checked with 17 errors. Against main, `karac fix`
applied 36 edits in its first round: `use std::collections::BinaryHeap`
deleted, as `PriorityQueue` is in the prelude; `BinaryHeap::new()` to
`PriorityQueue.max_first()`, since Rust's heap gives its largest first;
`use std::cmp::Reverse` to `import std.cmp.Reverse`; `Reverse((p, a))`
to `Reverse { value: (p, a) }` in the `let` and the pushes, and `.0 .0`
to `.value .0`; `let (price, mut amount, t)` to `let mut (price, amount,
t)`; `&&` and `!` to `and` and `not`; `struct Solution {}`, `Vec[..]`
and `Solution.`. It skipped the same rewrite in `for Reverse((_, a)) in
sell`, "applying it would not parse; please report it", and check kept
the E0273 there. The parser read `for Reverse { value: (_, a) } in sell
{` as Go's `for cond {`, the pattern's `{` taken for the body's, and
refused it with advice to write `while`; design.md parenthesizes a
struct literal in a `for`'s collection, not its pattern. That is
B-2026-11-27-57, fixed in the parser at 49e265ce46: the Go-loop reading
leaves a brace group that an `in` follows. With it, `karac fix` takes
the whole solution in one round of 40 fixes, the `for` included, and
drops the two `as i64` casts that the totals widen to on their own.
Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a batch of `a` orders is `a` orders placed one at a time,
each buy looking through the backlog's sells for the one with the
smallest price and each sell through its buys for the largest, the
backlog a plain list. LeetCode's examples, the six edges, 2000 orders of
prices and amounts of up to `10^9`, and 1991 random cases of 1 to 14
orders of prices and amounts of 1 to 10. Each arm meets six properties
on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, while there are at most 400 orders in all |
| P2 | every batch of more than one split in two, the same price and type, gives the same answer |
| P3 | every price `p` made `2p - 1` keeps every comparison, so gives the same answer, while the prices are at most `5 * 10^8` |
| P4 | every buy made a sell and every sell a buy, each price `p` made `10^9 + 1 - p`, gives the same answer |
| P5 | each match takes one buy and one sell, so the answer is no less than the larger side's excess, no more than every order, and has the parity of every order, while that is below the modulus |
| P6 | the ★ arm's answer |

The differential checks clean as first written. All 59,975 checks pass
on every arm: `2000 cases: checksum 674157466, 59975 checks over 5 arms:
0 failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the ★ arm's mirror over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a sell at the buy's own price not matched | P1 346, P4 607, P6 1384 |
| M2 | ★: what is left of a sell after a match dropped | P1 832, P2 548, P4 1305, P5 568, P6 3336 |
| M3 | sorted: a part-filled order left at its full amount | P1 1327, P2 937, P5 739, P6 1329 |
| M4 | sorted: each side's worst price taken as its best | P1 953, P6 954 |
| M5 | negate: a buy's reach taken from its own price, not its negation | P1 1078, P4 1470, P6 1080 |
| M6 | negate: an order at the best price not matched | P1 652, P6 653 |
| M7 | sortedvec: a resting buy put in at the falling side's place | P1 507, P4 918, P6 508 |
| M8 | sortedvec: a part-filled sell left with the buy's amount | P1 754, P2 852, P4 1209, P5 461, P6 756 |
| M9 | solution: a buy at the sell's own price not matched | P1 365, P4 607, P6 366 |
| M10 | solution: a resting sell put among the buys | P1 1365, P2 1461, P4 1691, P5 342, P6 1367 |

## Benchmarks

The bench builds 400 random lists of 500 orders of prices and amounts of
1 to 1000 once, and makes 10000 calls of the ★ arm, each list drawn from
the checksum so far. It checks clean as first written. Rust's mirror
uses `BinaryHeap` with `Reverse`, Go's `container/heap`, Python's
`heapq` with the buys' prices negated, and C's a binary heap written
out. Every implementation prints `10000 calls over 400 lists of 500
orders: checksum 757910286`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.28 s against Rust's 0.26 s (0.27 s with overflow checks
on), C's 0.40 s and Go's 0.88 s; Python takes 2.3 s.
