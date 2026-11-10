# 2064. Minimized Maximum of Products Distributed to Any Store

You are given an integer `n` indicating there are `n` specialty retail
stores. There are `m` product types of varying amounts, which are given
as a 0-indexed integer array `quantities`, where `quantities[i]`
represents the number of products of the `i`-th product type.

You need to distribute all products to the retail stores following these
rules: a store can only be given at most one product type but can be
given any amount of it. After distribution, each store will have been
given some number of products (possibly 0). Let `x` represent the maximum
number of products given to any store. You want `x` to be as small as
possible, i.e., you want to minimize the maximum number of products that
are given to any store.

Return the minimum possible `x`.

```
n = 6, quantities = [11, 6]       ->  3    (11 as 2, 3, 3, 3; 6 as 3, 3)
n = 7, quantities = [15, 10, 10]  ->  5
n = 1, quantities = [100000]      ->  100000
```

**Constraints:** `m == quantities.length`; `1 <= m <= n <= 10^5`;
`1 <= quantities[i] <= 10^5`.

With at most `x` products to a store, a type of `q` takes `ceil(q / x)`
stores, and only the total matters: `x` works exactly when those add up
to at most `n`. That total only falls as `x` grows, so the least `x` that
works can be searched for. The approaches differ in how they search, and
one does not search at all.

## Approaches

| file | mechanism |
|---|---|
| `stores.kara` ★ | a binary search over `1..=max(q)` for the least load whose stores fit in `n`, the need summed in a loop. O(m log max(q)) |
| `stores_heap.kara` | greedy: every type starts with one store, and each spare store goes to the type whose stores hold the most, kept on top of a max-first `PriorityQueue` of (load, quantity, stores); the answer is the top load at the end. O(n log m) |
| `stores_bits.kara` | the largest load that does not fit, built a bit at a time from `2^16` down, each bit kept when the load with it still does not fit; the answer is one more. The test is a closure `fits` over the quantities, an iterator `map` and `sum` |
| `stores_recursive.kara` | the binary search as recursion over the range still holding the answer, the quantities a `Slice[i64]` and each need a `fold` |
| `stores_jump.kara` | upward from the lower bound `ceil(total / n)`, but from one load to the least larger one at which some type needs a store fewer, `ceil(q / (c - 1))` for a type needing `c`; every load between needs as many stores. A `loop` returning from inside |
| `stores_solution.kara` | LeetCode's Rust template (`n: i32`, `quantities: Vec<i32>`, `let (mut l, mut r) = (1, *quantities.iter().max().unwrap())`, `l + (r - l) / 2`, the need summed as `i32` over `|&q|`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and five
more, each problem and its answer; then the sum of the answers and a
checksum for 500 random problems of 1 to 20 types, quantities up to 1,
10, 1000 or 100000, and from as many stores as types to ten times as
many; then the answer for the constraints' largest, 50000 types in 100000
stores. `stores.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every load from 1 up tried in turn, each type's products put
into stores of that load one store at a time, until the stores used fit
in `n`. It checks 300 random problems of 1 to 8 types, quantities up to
1, 10, 100 or 1000, from as many stores as types to ten times as many;
then 20 with exactly as many stores as types and 20 with a store for
every product. All 340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the types in reverse order have the same answer |
| P3 | one more store never raises the answer |
| P4 | every quantity doubled never lowers the answer and at most doubles it |
| P5 | the answer is at least `ceil(total / n)` and at most the largest quantity, which it is when there are as many stores as types |
| P6 | each arm agrees with at least three of the other five |

P4 holds because a load `x` that fits the quantities makes `2x` fit
their doubles, store for store.

The differential prints `340 problems: checksum 860581182, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
problems. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, four to seven to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones and the
survivors under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed, fails
the same way under both backends and not by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a load that fits ruled out | P1 84, P4 74, P5 33, P6 84 |
| M2 | ★: a type's stores rounded down | P1 158, P5 145, P6 158 |
| M3 | ★: the search stopped one short | P1 82, P4 78, P5 48, P6 82 |
| M4 | heap: a load rounded down | P1 135, P4 81, P5 56, P6 135 |
| M5 | heap: every type starting with no store | P1 181, P6 181 |
| M6 | heap: a type's stores never counted up | P1 218, P6 218 |
| M7 | bits: the load that does not fit taken for the answer | P1 340, P4 182, P5 235, P6 340 |
| M8 | bits: a bit added when the load fits | P1 340, P5 340, P6 340 |
| M9 | bits: the stores wanted to be fewer than `n` | P1 165, P5 32, P6 165 |
| M10 | recursive: a type's stores one too many at an even split | P1 66, P6 66 |
| M11 | recursive: the search starting at 2 | P1 147, P5 90, P6 147 |
| M12 | recursive: the middle tested one higher | P1 193, P4 110, P5 88, P6 193 |
| M13 | jump: the next load one past | P1 94, P3 13, P4 30, P5 13, P6 94 |
| M14 | jump: each type's need one short | P1 119, P5 14, P6 119 |
| M15 | jump: one store too many allowed | P1 101, P5 14, P6 101 |
| M16 | solution: a store too many for every type | P1 184, P6 184 |
| M17 | solution: the adapter halving the quantities | P1 193, P4 34, P5 193, P6 193 |

P1 and P6 kill all seventeen, P5 thirteen, P4 seven and P3 one. P2
kills none, and could not: every arm, the heap's included, reads the
quantities as a multiset, and no edit here made one depend on their
order. P5's bounds catch an answer that is too small to hold the
products or larger than any type needs; P4 the edits whose error does
not scale with the quantities, such as a fixed step too many or too few
(M1, M3, M13); P3 only the jump arm's step past the next load (M13), whose
answer with one more store was sometimes larger.

Of the thirty-two, fifteen were not kept. Two survive, and both are
equivalent: the heap arm with no stop at a load of one (once the top
load is 1 every load is 1, and a spare store leaves it 1), and the jump
arm starting from `total / n` rounded down (any start at most the answer
works, since every jump skips only loads that need as many stores). Two
crash and are not kept: the jump arm's type needing two stores taken as
no help leaves `next` at `i64.MAX` and overflows, and the bits arm's
steps one short reach a load of 0 and divide by it. Ten fail as a kept
one or as each other: the ★, heap and recursive arms' stores wanted
fewer than `n`, the heap arm's store kept back, and the Rust arm's
adapter one store short alike; the ★ arm's search starting at 2 as M11;
the ★, recursive and Rust arms' search topped at the smallest quantity
alike; the jump arm's next load overshot as M13. One is killed with
checks of its own but was left out because its arm keeps three: the
heap arm's every store spare (P1 170, P5 157).

## Verification

Every arm prints the same output as `stores.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 0.5 s to 3.2 s, except the jump
arm at 205 s (3.6 s compiled, 49 s under AddressSanitizer): on the
harness's largest problem it makes a jump for every load between
`ceil(total / n)` and the answer at which some type's need changes,
and each jump reads all 50000 types. The differential takes 1.9 s
(timed while other work shared the machine).

No arm met a compiler gap. The heap arm was written with Rust's
`BinaryHeap`; the checker named Kāra's `PriorityQueue`, which pops the
smallest first unless built max-first, and `karac fix` wrote
`PriorityQueue.max_first()`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 8 and 1 edits: Rust's spellings (`Vec<..>` to
brackets, `let (mut l, mut r)` to `let mut (l, r)`, the `&` of `|&q|`
dropped, `struct Solution;` to `struct Solution {}`, `Solution::` to
`Solution.`), then `1i32` for the literal `l` starts at, which design.md
§8 types `i64` since a comparison does not fix a literal's type, where
Rust infers `i32` from `l < r`. The fixed arm reads as the template
does.

## Benchmarks

The bench answers 200 problems with the ★ arm in all five languages:
50000 product types of 1 to 100000 each and 50000 to 100000 stores.
Every implementation prints `200 problems: sum 11318868, checksum
918868989`.

BENCHTAB
