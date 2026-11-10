# 2093. Minimum Cost to Reach City With Discounts

A series of highways connect `n` cities numbered from `0` to `n - 1`.
You are given a 2D integer array `highways` where `highways[i] =
[city1i, city2i, tolli]` indicates that there is a highway that connects
`city1i` and `city2i`, allowing a car to go from `city1i` to `city2i`
and vice versa for a cost of `tolli`.

You are also given an integer `discounts` which represents the number
of discounts you have. You can use a discount to travel across the `i`th
highway for a cost of `tolli / 2` (integer division). Each discount may
only be used once, and you can only use at most one discount per
highway.

Return the minimum total cost to go from city `0` to city `n - 1`, or
`-1` if it is not possible to go from city `0` to city `n - 1`.

```
n = 5, highways = [[0,1,4],[2,1,3],[1,4,11],[3,2,3],[3,4,2]], discounts = 1    ->  9
n = 4, highways = [[1,3,17],[1,2,7],[3,2,5],[0,1,6],[3,0,20]], discounts = 20  ->  8
n = 4, highways = [[0,1,3],[2,3,2]], discounts = 0                             ->  -1
```

**Constraints:** `2 <= n <= 1000`; `1 <= highways.length <= 1000`;
`highways[i].length == 3`; `0 <= city1i, city2i <= n - 1`; `city1i !=
city2i`; `0 <= tolli <= 10^5`; `0 <= discounts <= 500`; there are no
duplicate highways.

A trip is a city and the number of discounts spent so far: from `(city,
used)` a highway leads to `(other, used)` at its toll, or to `(other,
used + 1)` at half its toll while a discount is left. That is a graph of
`n (k + 1)` states with costs that are never negative, so Dijkstra over
it finds the cheapest arrival at city `n - 1` with any number used. A
cheapest trip visits no city twice, so it never needs more than `n - 1`
discounts. The approaches differ in how they search the states.

## Approaches

| file | mechanism |
|---|---|
| `discounts.kara` ★ | Dijkstra over the `(city, used)` states, a `PriorityQueue[(i64, i64, i64)]` of `(cost, city, used)`, smallest first, the costs in one flat `Vec` indexed `city * k + used`; the first pop of the last city is the answer. O((n + m) k log(nk)) |
| `discounts_layers.kara` | layer by layer: the cheapest cost to each city with at most `d` discounts, each layer one Dijkstra at full tolls (a `PriorityQueue[(i64, i64)]`) seeded from the layer below with one more highway at half its toll. O(k (n + m) log n) |
| `discounts_sorted.kara` | Dijkstra with a `SortedSet[(i64, i64)]` frontier: a state's entry taken out and put back when a cheaper cost is found, so each state is in the set at most once and `pop_first` takes the cheapest |
| `discounts_bellman.kara` | Bellman-Ford over the layers, a `Vec[Vec[i64]]` per discount count: every highway, both ways, relaxed at its full toll within a layer and at half into the next, pass after pass until a pass improves nothing. O(n m k) at worst |
| `discounts_queue.kara` | a `struct Roads` holding the highways and the cheapest cost to each state, with `offer` and `settle` methods on `mut ref self`, relaxed by a work queue (SPFA): a `VecDeque` of the states whose cost fell |
| `discounts_solution.kara` | LeetCode's Rust template (`highways: Vec<Vec<i32>>`, a `BinaryHeap` of `Reverse((d, u, used))`, `vec![vec![i32::MAX; k + 1]; n]`), carried by `karac fix` in six rounds and one edit by hand |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more, each map and its cost; then the sum and a checksum of the costs
of 2000 random maps of 2 to 30 cities and up to 40 highways, tolls below
10, 100 or 100001, with up to 5 discounts; then the constraints' largest,
1000 cities and 1000 highways with none, 3 and 500 discounts, and a road
of 999 highways of toll 100000. `discounts.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every path from city 0 to city `n - 1` that visits no city
twice, found by a depth-first walk, its tolls sorted and the largest
halved while discounts last, and the cheapest of them, or -1 when there
is none. It checks 300 random maps of 2 to 7 cities and up to 10
highways, tolls below 20 or 1000, with up to 4 discounts; then 20 with
no discount, and 20 with a discount for every highway. All 340 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the cost is the statement read literally |
| P2 | one discount more never costs more, and -1 stays -1 |
| P3 | the highways listed in reverse, each with its ends swapped, give the same cost |
| P4 | the cost is -1 exactly when city `n - 1` cannot be reached, and otherwise at most the cost with no discount and at least half of it, less a half for each of the at most `n - 1` tolls rounded down |
| P5 | the cities between the first and the last numbered the other way round give the same cost |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 maps: checksum 815255914, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal costs was checked against a Python reading of the same
maps. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the half toll rounded up | P1 109, P6 109 |
| M2 | ★: the last city taken only with every discount used | P1 123, P2 99, P4 83, P6 123 |
| M3 | ★: the discount taken off the cost so far | P1 52, P4 40, P6 52 |
| M4 | layers: one layer fewer | P1 95, P6 95 |
| M5 | layers: each layer exactly its discounts, not at most | P1 82, P2 50, P4 49, P6 82 |
| M6 | layers: the discount one way only | P1 108, P3 180, P6 108 |
| M7 | sorted: the dearest taken first | P1 190, P2 50, P4 58, P5 2, P6 190 |
| M8 | sorted: only the discounted move | P1 64, P2 44, P4 238, P6 64 |
| M9 | sorted: the answer from the first state found | P1 181, P6 181 |
| M10 | bellman: one pass only | P1 15, P2 5, P3 25, P4 38, P6 15 |
| M11 | bellman: the answer from the full-price layer only | P1 183, P6 183 |
| M12 | bellman: one discount fewer allowed | P1 52, P6 52 |
| M13 | queue: the queued mark never cleared | P3 2, P4 1 |
| M14 | queue: the discounted step staying in its layer | P1 14, P6 14 |
| M15 | queue: the highways one way only | P1 139, P3 204, P4 127, P6 139 |
| M16 | solution: the adapter's discounts one more | P1 63, P6 63 |
| M17 | solution: the adapter's tolls halved | P1 231, P6 231 |

P1 and P6 kill sixteen, P4 eight, P2 five, P3 four, and P5 one. P4 sees
-1 for a city that can be reached, when an arm needs more discounts than
the path has highways (M2, M5, M8) or a highway goes one way only (M15),
and a cost below half the plain one when the discount comes off
everything paid so far (M3). P3 sees the highways' order and direction
matter, which they do once a highway is used one way only (M6, M15) or a
single pass meets them in one order (M10). P2 sees one discount more
cost more, or reach nothing (M2, M5, M7, M8, M10). M13 is the one P1 misses: a state that was queued once is never
queued again when its cost falls later, so its neighbours keep the old
cost, and of the 340 maps none walks the states in an order where that
matters; two of their reversed listings do.

Of the thirty, thirteen were not kept, and none survives. Nine fail as a
kept one: a discount's state counted as none used, in the ★, sorted and
Rust arms, and the sorted arm's discounts used forgotten, as M14; the
highways one way only in the ★, bellman and Rust arms as M15; the sorted
arm's discounted move at full toll and the queue arm's full-price layer
as M11; the Rust arm's full toll never tried as M8. Two are killed with
checks of their own but were left out because their arm keeps three:
the layers arm's spread seeded from city 0 only (P1 5) and its discount
at full toll (P1 101, P3 180). Two ran past the 300 s limit and are not
kept: the bellman arm's discount into the same layer and the queue arm's
offer taken when no cheaper, each a relaxation that never stops once a
toll halves to 0.

## Verification

Every arm prints the same output as `discounts.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 6.8 s to 25 s, and the
differential 1.4 s (timed while other work shared the machine).

No Kāra arm met a compiler gap. The Rust arm was written as LeetCode's
Rust template. `karac fix` carries it in five rounds of 22, 1, 5, 3 and
9 edits: Rust's spellings (`Vec<Vec<i32>>` to brackets, `&` to `ref`,
`::` to `.`, `&&` to `and`, `struct Solution;` to `struct Solution {}`,
the `use` lines dropped); then `BinaryHeap::new()` to
`PriorityQueue.new()` with each `Reverse(..)` unwrapped, since
`PriorityQueue` is smallest first; then `vec![]` to `Vec.new()`,
`vec![x; n]` to `Vec.filled(n, x)` and the adapter's `vec![..]` to a
list; then `usize` to `i64` and the `usize` suffixes of `0usize`
dropped. That leaves three errors, which take the one edit by hand: the
heap is written `PriorityQueue[(i32, i64, i64)]`. Rust types `d` as
`i32` from its later comparisons with `dist`; in Kāra the `0` of
`heap.push((0, 0, 0))` reaches `d + t` and `d > dist[u][used]` beside
an `i32`, which widens rather than fixing the literal (design.md §8
Literals: "Beside a type that does widen, the literal keeps its
default"), so `return d` and the two stores into `dist` were refused as
narrowing. The message points at those three and asks for `as i32` at
each, not at the literal that made `d` an `i64`; that is filed as
DIAGROW. A last round of 1 edit then makes the adapter's `ref` parameter
a bare one, which borrows already. The fixed arm reads as the template
does.

## Benchmarks

The bench draws 60 maps of 20000 cities, each city joined to three
cities ahead of it, tolls up to 100000, and asks each with 0, 2, ..., 22
discounts in turn, with the ★ arm in all five languages: the costs in a
flat growable array and a binary heap of `(cost, city, used)` triples
ordered as tuples (a `PriorityQueue`, a `BinaryHeap` of `Reverse`, a
`container/heap`, `heapq`, and a hand-written heap in a `malloc`'d
array). Every implementation prints `60 answers: sum 6305394, checksum
3714437`.

BENCHTAB
