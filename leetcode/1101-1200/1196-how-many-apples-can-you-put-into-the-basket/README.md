# 1196. How Many Apples Can You Put into the Basket

You have some apples and a basket that can carry up to `5000` units of
weight. Given an integer array `weight` where `weight[i]` is the weight
of the `i`th apple, return the maximum number of apples you can put in
the basket.

```
weight = [100, 200, 150, 1000]            ->  4
weight = [900, 950, 800, 1000, 700, 800]  ->  5
```

**Constraints:** `1 <= weight.length <= 10^3`; `1 <= weight[i] <= 10^3`.

The arms are `fn max_number_of_apples(weight: own Vec[i64]) -> i64`, or
`weight: Vec[i64]` for an arm that only reads the weights. The two Rust
arms keep the method LeetCode gives Rust users, taking a `Vec<i32>` and
returning `i32`, inside `impl Solution`, and a one-line
`max_number_of_apples` calls it.

## Approaches

No `k` apples weigh less than the `k` lightest, so the answer is how many
of the lightest apples fit before the next one would take the load past
5000.

| file | mechanism |
|---|---|
| `max_number_of_apples.kara` ★ | the weights sorted, and the lightest put in one at a time until the next would take the load past 5000. O(n log n) |
| `max_number_of_apples_count.kara` | a counting sort, since a weight is at most 1000: the apples counted by weight in a `[0; 1001]`, then as many of each weight as the room left allows, lightest first, until a weight runs out of room. O(n + 1000) |
| `max_number_of_apples_heap.kara` | every apple in, then the heaviest taken out while the load is past 5000, from a largest-first `PriorityQueue`. O(n + k log n) for `k` taken out |
| `max_number_of_apples_prefix.kara` | the sorted weights' running totals in an iterator chain, a closure keeping the load, and `take_while(..).count()` of those within 5000. O(n log n) |
| `max_number_of_apples_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut weight: Vec<i32>` sorted in place and summed in a `for (i, &w)` loop until the sum passes 5000), carried to Kāra by `karac fix` |
| `max_number_of_apples_chain.kara` | another Rust solution, in an iterator chain (`sort_unstable`, then `scan` for the running totals, `take_while` and `count`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 14 lines: LeetCode's two examples; five apples
of 1000 (`5`) and six (`5`); one apple; a load of exactly 5000 (`[1000,
1000, 1000, 1000, 999, 1]: 6`) and one past it by one (`[1000, 1000,
1000, 1000, 999, 2]: 5`); heavy and light apples alternating (`9`);
10^3 apples of 1 (`1000`) and of 1000 (`5`); 2000 random baskets of up
to 40 apples (`2000 random baskets: 36040 apples, checksum 479362455`);
and 10^3 apples, the constraints' most, of 1 to 1000 (`103`) and of 1
to 20 (`695`). `max_number_of_apples.py` mirrors the ★ arm and its
output is byte-identical. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, heap and prefix arms check clean as written. The
count arm, which only reads its weights, takes one fix, the harness's
`max_number_of_apples(c.clone())` to `max_number_of_apples(c)`, since
the call borrows. The solution arm takes one round of 9 fixes (among
them `struct Solution;` to `struct Solution {}`, `mut weight: Vec<i32>`
to `weight: own Vec[i32]` and a `let mut weight = weight;`, `&w` to `w`
in the loop's pattern, `Solution::` to `Solution.`, and the `as i64` on
the widening call dropped) and its output matches. The chain arm takes
one round of 11 (among them `sort_unstable()` to `sort()`, and the
`scan` closure `|sum, &w| { *sum += w; Some(*sum) }` to `|sum, w| { let
sum = sum + w; Some((sum, sum)) }`, Kāra's `scan` taking the state and
returning the next state with the item) and its output matches. The kata
found no gap.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subset of the apples weighed, and the most apples in
any subset within 5000 kept. 2000 random baskets of 4 to 12 apples, each
of `low` to 1000 for a `low` of 1, 300, 500 or 700, or one basket in
five of 500s and 1000s, which often fill the basket exactly.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at least `min(n, 5)` apples, since five apples weigh at most 5000, and at most `n` |
| P3 | the apples reversed put in as many |
| P4 | one more apple puts in as many or one more |
| P5 | the first apple taken out puts in as many or one fewer |
| P6 | every weight halved, rounded up, puts in as many or more |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 baskets: checksum 359638730,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same baskets, weighing every subset, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a load of exactly 5000 refused | P1 147, P2 2, P7 735 |
| S2 | ★: the apple that does not fit counted | P1 1149, P7 5745 |
| K1 | count: apples of weight 1000 never counted out | P1 400, P2 241, P7 400 |
| K2 | count: the basket holds 4999 | P1 147, P2 2, P7 147 |
| H1 | heap: a load of exactly 5000 refused | P1 147, P2 2, P7 147 |
| H2 | heap: the lightest taken out first | P1 915, P4 201, P5 209, P7 915 |
| R1 | prefix: the weights left unsorted | P1 580, P3 428, P5 148, P7 580 |
| R2 | prefix: the load starts at 1 | P1 147, P2 2, P7 147 |
| X1 | solution: one apple fewer than fit | P1 1149, P2 119, P4 152, P5 200, P7 1149 |
| X2 | solution: the basket holds 4000 | P1 1442, P2 219, P7 1442 |
| C1 | chain: a load of exactly 5000 refused | P1 147, P2 2, P7 147 |
| C2 | chain: the heaviest first | P1 915, P4 201, P5 209, P7 915 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. S1, K2, H1, R2 and C1 are one fault in five arms, a load of
exactly 5000 turned away, and fail alike on the 147 baskets the lightest
apples fill exactly; a first draw of baskets of `low` to 1000 alone
caught them only twice, which is why one basket in five is made of 500s
and 1000s. S2 and X1 are the answer off by one either way
whenever not every apple fits, and H2 and C2 one fault too, the heaviest
apples kept. P3, the apples reversed, catches only R1, the one fault
that reads the apples' order. P6 catches none: every mutation still puts
in as many apples or more when they weigh less.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 200 baskets of 10^3 apples, the constraints' most, built once,
from weights of 1 to 1000, 1 to 20, 300 to 1000 and 1 to 100 in turn;
then 200 rounds over the baskets, each call sorting its own copy, each
answer folded into a checksum. Every program prints `200 rounds of 200
baskets of 1000 apples: checksum 229818506`. The sort is the work: C
sorts with `qsort`, Rust with the standard `sort`, Go with
`slices.Sort`, and Python with `sorted`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `e8dc4f7aa2`
plus the typechecker fix pushed as `ab7613763c`, on LLVM 22. A plain
`karac build` targets x86-64-v2, so the C and overflow-checked Rust
programs are also built at x86-64-v3 for comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.343 to 0.441 s | 0.353 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.337 to 0.398 s | 0.350 s |
| Rust (`rustc -O`) | 0.425 to 0.584 s | 0.474 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.439 to 0.569 s | 0.487 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.478 to 0.574 s | 0.503 s |
| C (`clang -O3`) | 2.295 to 2.525 s | 2.491 s |
| C (`clang -O3 -march=x86-64-v3`) | 2.433 to 2.577 s | 2.489 s |
| Go | 1.608 to 1.718 s | 1.671 s |
| Python | 3.664 to 3.759 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 28% ahead of Rust with overflow checks on (0.350 s
against 0.487 s) and of plain Rust. C takes about 7x Kāra's time and Go
about 4.8x: `qsort` calls its comparison through a pointer for every
pair it weighs; no profile was taken, so what holds Go back is not
known. Python takes only about 10.6x Kāra's time, since its `sorted`
runs in C.
