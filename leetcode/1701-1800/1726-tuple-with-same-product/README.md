# 1726. Tuple with Same Product

Given an array `nums` of **distinct** positive integers, return *the
number of tuples* `(a, b, c, d)` *such that* `a * b = c * d` *where*
`a`*,* `b`*,* `c`*, and* `d` *are elements of* `nums`*, and*
`a != b != c != d`*.*

```
nums = [2,3,4,6]         ->  8     (2*6 = 3*4, in 8 orders)
nums = [1,2,4,5,10]      ->  16    (1*10 = 2*5 and 2*10 = 4*5)
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i] <= 10^4`;
all elements in `nums` are **distinct**.

## Approaches

| file | mechanism |
|---|---|
| `products.kara` ★ | the values are distinct, so two different pairs with one product share no value, and each such two pairs make 8 tuples; every pair's product counted in a `Map` as it comes, a pair whose product `seen` earlier pairs have adding `8 * seen`. O(n^2) |
| `products_sorted.kara` | no map: every product pushed onto a list, the list sorted, and each run of k equal products giving k(k - 1)/2 two pairs. O(n^2 log n) |
| `products_nested.kara` | with the values sorted, two pairs of one product nest, the smallest and largest of the four in one pair; for each outer pair, two pointers walk inward and count the inner pairs that match. O(n^3) |
| `products_solution.kara` | a Rust solution as LeetCode's Rust users write it, `*map.entry(nums[i] * nums[j]).or_insert(0) += 1` into a `HashMap<i32, i32>` and `map.values().map(\|&c\| c * (c - 1) / 2 * 8).sum()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's two examples, one value,
and the values 1 to 12; then the answers summed and a checksum for 3000
random problems of up to 10 values up to 20, 100 of up to 100 values up
to 200, and 3 of up to 300 values up to `10^4`, each the first values of
a shuffle. The O(n^3) arm keeps the last batch to 300 values.
`products.py` mirrors the ★ arm and its output is byte-identical.

```
8
16
0
136
3000 problems of up to 10 values up to 20: answers sum to 15248, checksum 575326309
100 problems of up to 100 values up to 200: answers sum to 225984, checksum 692448421
3 problems of up to 300 values up to 10000: answers sum to 568, checksum 116511
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every tuple of four places, all different, whose values give
`a * b == c * d`, counted. It checks 3000 random problems of 1 to 7
distinct values from 1 to 12. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values in reverse order give the same answer |
| P3 | every value doubled gives the same answer |
| P4 | 401, a prime above any product of two values, appended gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 839738898, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, `itertools.permutations` of four places,
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1, M2, M4, M8 and M9 each get every
answer above zero wrong, and so fail the very same 574 problems, the
ones with any tuple at all.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each earlier pair of the same product counted 4 tuples, not 8 | P1 574, P5 574 |
| M2 | ★: a product's count never raised | P1 574, P5 574 |
| M3 | ★: a value paired with itself | P1 546, P5 546 |
| M4 | sorted: each run of k equal products counted twice over | P1 574, P5 574 |
| M5 | sorted: the products not sorted | P1 548, P2 83, P4 51, P5 548 |
| M6 | sorted: the next run started one product on, not at the run's end | P1 10, P5 10 |
| M7 | nested: the outer pair at least four places apart, not three | P1 168, P5 168 |
| M8 | nested: an equal product taken for a smaller one | P1 574, P5 574 |
| M9 | solution: the pairs of a run counted in order, not as a set | P1 574, P5 574 |
| M10 | solution: each pair taken in both orders and with itself | P1 2597, P4 3000, P5 2597 |

## Benchmarks

The bench draws 20 random problems of 1000 distinct values up to
`10^4`, LeetCode's largest, all of them first, then answers each 3
times by the ★ arm in all five languages; each answer builds its map
anew from about half a million products. Every implementation prints
`20 problems of 1000 values up to 10000, 3 rounds: answers sum to
6260064, checksum 74324755`. C has no map: its mirror probes a table of
`2^20` slots linearly, the product hashed by one multiply and the table
cleared before each answer, which is less work than Kāra's SipHash
`Map`, Rust's SipHash `HashMap` or Go's `map` do. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.344 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.391 s |
| Rust (`rustc -O`) | 1.397 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.607 s |
| Kāra (`karac build`) | 1.692 s |
| Go | 2.996 s |
| Python | 7.1 s |

The sequential Kāra build takes 1.15x Rust's time and 1.16x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.344 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.466 s and 1.493 s on one
run).

## Verification

All four arms print the same output as `products.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The nested arm checked clean as first written.

The ★ and sorted arms both started `let mut tuples = 0;` as in Rust, then
`tuples += 8 * *seen` and `tuples += 4 * k * (k - 1)`, each an `i32`
added to it, returned as the `i32` answer. In Kāra an operator does not
fix a literal's type (design.md §8 Literals), so `tuples` stayed `i64`
and the return narrowed; `karac check` said to declare it, and `karac
fix` wrote `tuples: i32` in both.

LeetCode's Rust template took one `karac fix` of 10 edits:
`struct Solution {}` added, `use std::collections::HashMap;` deleted,
`Vec<i32>` written `Vec[i32]`, `HashMap<i32, i32>` and `HashMap::new()`
written `Map[i32, i32]` and `Map.new()`, and `|&c|` written `|c|`.
`*map.entry(..).or_insert(0) += 1` and the `sum()` over `values()`
carried over as written; a sum of the counts does not depend on the
map's order.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
