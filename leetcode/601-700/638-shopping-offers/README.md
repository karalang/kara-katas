# 638. Shopping Offers

A store sells n items, item i at `price[i]`. Each special offer is a
list of n + 1 numbers: how many of each item it holds, then its price.
Given `needs[i]`, how many of item i to buy, return the lowest price
that buys exactly those items, using any offer any number of times.
Buying more than is needed is not allowed, even when it would be
cheaper.

```
price = [2,5],   special = [[3,0,5],[1,2,10]],      needs = [3,2]
  ->  14
price = [2,3,4], special = [[1,1,0,4],[2,2,1,9]],  needs = [1,2,1]
  ->  11
```

**Constraints:** 1 to 6 items; every price and need from 0 to 10; 1 to
100 offers, each of n + 1 numbers from 0 to 50; every offer holds at
least one item.

## Approaches

Every arm is `fn shopping_offers(price: Vec[i64], special:
Vec[Vec[i64]], needs: Vec[i64]) -> i64`. A need is a point in a box of
at most 11^6 = 1,771,561 points, and an offer that fits moves it toward
nothing, so every arm prices a need as the cheaper of list price and the
best offer that fits plus the price of what it leaves. They differ in
how the needs are named and in what order they are priced. Each skips an
offer of nothing, which cannot lower a price and would make a search go
round forever.

| file | mechanism |
|---|---|
| `shopping_offers.kara` ★ | depth-first search from `needs`, with a `Map[Vec[i64], i64]` memo keyed by the need itself; prices only the needs reached; O(S x offers x n) for those S needs |
| `shopping_offers_coded.kara` | the same search with each need numbered in mixed radix (base needs[i] + 1 for item i), so an offer that fits takes its own number off without a borrow, and the memo a flat `Vec` with -1 for not yet priced |
| `shopping_offers_table.kara` | every need from nothing up to `needs` priced in order of its number, an odometer keeping its digits, so every need an offer leaves is already in the table; O(S x offers x n) for all S needs |
| `shopping_offers_knapsack.kara` | an unbounded knapsack: the table starts at list price and each offer joins in turn, every need upward taking the offer plus the need without it; O(offers x S x n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: the two LeetCode examples; eight
more (no offers at all and an offer of nothing, both outside the
constraints; nothing needed; an offer dearer than list price; offers of
more than is needed; a bargain taken five times; three pair offers that
cover the need between them; and an item that costs nothing), each with
its prices, offers and needs; the total and a checksum of the prices of
300 random cases of 1 to 6 items, a need of 0 to 3 of each and 0 to
12 offers; and a case of 6 items with a need of [10, 9, 8, 3, 2, 1],
23,760 needs in all, and 100 offers of up to 3 of each item, beside its
list price. `shopping_offers.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
try every number of times to take each offer, offer by offer, that stays
within the need, and buy the rest at list price; the answer is the
cheapest of them all. Each of 1,000 cases has 1 to 3 items costing 0 to
10, a need of 0 to 4 of each, and 0 to 4 offers of 0 to 2 of each item
costing 0 to 20, so that about a third of the cases take an offer.

| | property |
|---|---|
| P1 | the price is the definition's |
| P2 | it is between nothing and list price |
| P3 | renumbering the items, in the prices, the needs and the offers, changes nothing |
| P4 | neither does the order of the offers |
| P5 | a new offer of exactly the need at a price q from 0 to 50 makes the price the cheaper of q and the old price |

It prints `1000 cases (298 beat list price), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an offer may overshoot an item by one | P1 353, P2 92, P5 55 |
| M2 | ★: offers given away | P1 462, P5 592 |
| M3 | coded: a digit read in base needs[i] + 2 | index out of bounds |
| M4 | coded: every item priced as the first | P1 493, P2 211, P3 570 |
| M5 | table: the odometer carries one early | index out of bounds |
| M6 | table: an offer may overshoot an item by one | index out of bounds |
| M7 | knapsack: the need equal to an offer skipped | P1 93, P5 339 |
| M8 | knapsack: an offer needs one more of each item than it takes | P1 252, P5 364 |
| E1 | coded: offers that overshoot the need kept by the filter | 0 |
| E2 | table: offers of nothing tried too | 0 |
| E3 | knapsack: offers of nothing tried too | 0 |
| E4 | knapsack: every item checked after one falls short | 0 |

P1 kills the five that change an answer without crashing, and the other
three, which misread a need's number, index out of the table and stop
the run. P2 sees M1 and M4, whose prices can leave the range from
nothing to list price: an overshoot leaves a negative need, priced below
nothing, and pricing every item as the first can cost more than list
price. P3 sees only M4, which prices every item as the first and so
depends on the order of the items. P4 sees none, since every mutant is
wrong whatever order the offers come in. P5 sees M1, M2, M7 and M8: a
free offer, an overshoot, a skipped exact fit and an offer that wants
one more of each item all change what an offer of exactly the need can
do. The four survivors cannot change an answer: the coded search checks
every offer against the need it is pricing, so a filter that lets
through offers too large only costs time; an offer of nothing costs at
least 0 and leaves the need as it was, so it can never make a price
cheaper; and once one item falls short the need cannot hold the offer,
so checking the rest changes nothing.

## Verification

Every arm prints the same output as `shopping_offers.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `d6111aa22a` for the
debug build, with the runtime archives rebuilt from that tree, and
`14acd67779` for the release build that runs `check` and `__mir-run`.

The frozen legacy backends refuse every arm and the differential at
type checking. design.md asks for a `mut` marker on every argument to a
`mut ref` parameter, a `mut ref` binding handed on included, as in
`cheapest(price, special, rest, mut memo)` and `next_random(mut seed)`;
legacy rejects that marker, saying the argument is already a mut-ref.
An earlier version of this kata left those markers out, which v2 also
accepts (B-2026-10-14-35, open); then legacy ran every arm under `karac
run`, `karac run --interp` and `karac build`, sequential and with
`KARAC_AUTO_PAR=1`, and printed the same output, the table arm taking
193 s under `--interp`. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 shops of 6 items once,
each with prices of 1 to 10, a need of 0 to 4 of each item and
100 offers of 0 to 2 of each item costing 0 to 50; then 800 rounds each
price one shop's need from scratch, the shop picked by the round, adding
up the prices and a checksum. Every implementation prints `20 shops,
800 rounds: total 19200, checksum 440449945`, the Kāra program under
`karac __mir-run` included (in 64 s).

Each implementation searches from the need with a memo keyed by the
need: Rust with a `HashMap<Vec<i64>, i64>`, building a `Vec` for every
offer tried as the Kāra does; C with an open-addressing hash table of
six-number keys, the need it leaves on the stack; Go with a map keyed by
a `[6]int64` array; and Python with a dict keyed by tuples. Spot timings
on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine), each including making the
shops:

| | time |
|---|---|
| C (`clang -O3`) | 0.10 to 0.11 s |
| Rust (`rustc -O`) | 0.62 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.62 to 0.65 s |
| Go | 0.28 to 0.29 s |
| Python | 6.01 to 6.02 s |
| Kāra (`karac build --mir`) | 0.55 to 0.56 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses the bench
program: handing `prices[s]` to `shopping_offers` moves an element out
of a `Vec` while parameters are owned, and it rejects the `mut` markers
above. That edit is by hand, on top of the `scripts/new-bench.sh`
output. A copy outside the kata that adds `.clone()` to the three
arguments and leaves out the markers builds under legacy and takes 0.26
to 0.28 s. Under `karac __mir-llvm-run` the program prints the same line
in 3.8 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build takes about twice legacy's time, over the M2 bar of
1.5x, and is filed as B-2026-10-14-69. Every offer tried builds a
six-element `Vec` with six pushes; v2's first block holds 4 elements, so
each such `Vec` is allocated twice, where legacy's first block of
8 allocates once. Linked against a runtime whose first block is
8 elements, the same program takes 0.32 to 0.37 s. Rust's `Vec` also
starts at 4 elements of this size. The C, which keeps the need on the
stack, is fastest by far; the comparison with C and Rust waits until
after M4.

## Compiler findings

B-2026-10-14-69 (open): a short `Vec` grown by `push` allocates twice on
the MIR compiled backend, where legacy allocates once; this kata's bench
is 2.0x legacy, against an M2 bar of 1.5x.

B-2026-10-14-35 (open): v2 accepts a `mut ref` binding handed on to a
`mut ref` parameter without the `mut` marker design.md asks for.

The legacy refusals above are not filed, because legacy is frozen.
