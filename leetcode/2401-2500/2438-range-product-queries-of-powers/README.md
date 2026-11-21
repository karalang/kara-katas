# 2438. Range Product Queries of Powers

Given a positive integer `n`, there exists a **0-indexed** array called
`powers`, composed of the **minimum** number of powers of `2` that sum
to `n`. The array is sorted in **non-decreasing** order, and there is
**only one** way to form the array.

You are also given a **0-indexed** 2D integer array `queries`, where
`queries[i] = [left_i, right_i]`. Each `queries[i]` represents a query
where you have to find the product of all `powers[j]` with `left_i <= j
<= right_i`.

Return *an array* `answers`*, equal in length to* `queries`*, where*
`answers[i]` *is the answer to the* `i`th *query*. Since the answer to
the `i`th query may be too large, each `answers[i]` should be returned
**modulo** `10^9 + 7`.

```
n = 15, queries = [[0,1],[2,2],[0,3]]  ->  [2,4,64]
n = 2,  queries = [[0,0]]              ->  [2]
```

**Constraints:** `1 <= n <= 10^9`; `1 <= queries.length <= 10^5`;
`0 <= start_i <= end_i < powers.length`.

The fewest powers of two that sum to `n` are its set bits, at most 30
of them below `10^9`, smallest first. A product of powers of two is two
to the sum of their exponents, so the exponents' prefix sums answer a
query with one subtraction, and two to that sum, at most `0 + 1 + ... +
29 = 435`, is taken by squaring. The other arms multiply the powers
themselves, in a table, by prefix products and inverses, or one by one.

## Approaches

| file | mechanism |
|---|---|
| `powers.kara` ★ | the exponents' prefix sums over `n`'s set bits, and each query two to the difference of two of them, by squaring modulo `10^9 + 7`. O(31 + q log 435) |
| `powers_naive.kara` | the statement read directly: the powers found by taking the largest power of two that still fits from what is left of `n`, put smallest first, and each query's powers multiplied one by one. O(31 + 31 q) |
| `powers_table.kara` | a table of every answer: at most 465 ranges, `table[l][r]` filled row by row, each entry the one before it times the next power, and each query a lookup. O(31^2 + q) |
| `powers_inverse.kara` | prefix products modulo the prime `10^9 + 7`, and a range's product the prefix to its end times the inverse of the prefix before it, by Fermat's little theorem. O(31 + q log p) |
| `powers_iter.kara` | iterators: the powers by `filter` over the bits and `map` to `1 << bit`, and each query by `skip`, `take` and `fold`, the answers by `map` and `collect`. O(31 + 31 q) |
| `powers_solution.kara` | LeetCode's Rust template: a `const MOD` inside the function, the powers pushed as `1i64 << i` into a `Vec::new()`, and each query's product in a closure over an inclusive range of `usize` indices, cast back by `p as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one power;
three queries over the 29 powers of `2^29 - 1`, the most a value up to
`10^9` holds; every query over `2^29 - 1` and over `10^9`, each as a
checksum; the constraints' largest, `10^5` random queries over
999999999; and 3000 random values from 1 to `10^9`, each with 5 random
queries, as a checksum of every answer's checksum. `powers.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
on every value from 1 to 199, its powers found by searching the
multisets of powers of two for the fewest that sum to it, and on 3000
random values up to `10^9`, every query of each against the product
taken exactly with Python's integers.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 9 edits: the brackets of `Vec<Vec<i32>>` and
`Vec<i32>`, five edits; `Vec::new` written `Vec.new`; `struct Solution;`
given its braces; and, once the template parses, the `i64` suffixes of
`1i64 << i` and `let mut p = 1i64` dropped as the default. The `const`
inside the function, `1_000_000_007`, `n >> i & 1`, the inclusive range
and `p as i32` stand as Kāra. So does `q[0] as usize..=q[1] as usize`:
the `usize` it makes indexes `powers` and meets no `i64`, so nothing
rewrites it, although design.md keeps `usize` for FFI and asks for
`i64` indices everywhere else.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: `n`'s binary digits found by halving it, each digit 1 giving
a power, and the powers multiplied one by one for each query modulo
`10^9 + 7`. No exponent is summed and no bit is tested by a shift. It
checks 300 random values from 1 to 1023, each with 1 to 6 random
queries; then 30 from 1 to `10^9` with every query; then 30 runs of 1
to 29 set bits, below `2^30`, with every query. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the queries in reverse order: the answers reversed |
| P3 | each power alone, `[i, i]`: that power |
| P4 | each query split at its middle: the two halves' answers multiplied |
| P5 | a power above all of `n`'s, `2^30`, added: the same answers |
| P6 | each arm agrees with at least three of the other five |

P4 holds because a product over a range is the product of its two
halves. P5 holds because the new power goes last, past every index a
query names. It takes `n` past `10^9`, outside the constraints, and
below `2^31`, so the template's `i32` still holds it.

The differential prints `360 cases: checksum 884665505, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and takes every product exactly. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the bit plus one summed | P1 360, P3 360, P6 360 |
| M3 | ★: the base never squared | P1 357, P3 360, P4 286, P6 357 |
| M4 | ★: the odd step skipped | P1 359, P3 360, P4 286, P6 359 |
| M7 | naive: the powers left largest first | P1 336, P3 354, P5 360, P6 336 |
| M10 | naive: the product never reduced | P1 75, P4 75, P6 75 |
| M11 | naive: the powers added | P1 359, P3 360, P4 339, P6 359 |
| M12 | table: each row started at its own power | P1 350, P3 360, P4 339, P6 350 |
| M14 | table: the rows from the first power | P1 290, P3 352, P4 336, P6 290 |
| M16 | table: one power past the end | P1 360, P3 360, P4 339, P6 360 |
| M19 | inverse: the prefix divided, not inverted | P1 92, P3 117, P4 93, P6 92 |
| M20 | inverse: each answer times the one before | P1 305, P2 305, P3 352, P4 207, P6 305 |
| M21 | inverse: each prefix times the bit, not its power | P1 357, P3 360, P6 357 |
| M22 | iter: one too many taken | P1 312, P3 354, P4 339, P5 278, P6 312 |
| M23 | iter: skipped one fewer | P1 316, P3 354, P4 253, P6 316 |
| M26 | iter: the clear bits taken | P1 357, P3 360, P5 26, P6 357 |
| M27 | solution: the range exclusive | P1 359, P3 360, P4 336, P6 359 |
| M31 | solution: the powers squared | P1 359, P3 360, P6 359 |


P1 and P6 kill all seventeen, P3 sixteen, P4 twelve, P5 three and P2
one.

Fourteen are not kept. Eight fail exactly as a kept one: the ★ arm's
prefix one short and the naive arm's last power left out (M1, M8) as
the template's range exclusive (M27), all three leaving out the query's
last power; the ★ arm's exponents counted and the iter arm's bits as
powers (M6, M24) as the inverse arm's prefix times the bit (M21); the
inverse arm's prefix before for the inverse and the template's product
started at the first power (M17, M29) as the table arm's row started at
its own power (M12), each dropping the query's first power; the inverse
arm's inverse by `MOD - 1` (M18) as the table arm's rows from the first
power (M14), since by Fermat that power of any prefix is 1, so every
answer is the product from the first power; and the iter arm's product
started at 2 (M25) as the table arm's one power past the end (M16).

Four end in an index out of bounds, not a wrong answer, under both
backends: the ★ arm's and the template's bits from 1 (M5, M28) drop the
power `2^0` of every odd `n`, so a query's last index runs past the
shorter list; the naive arm's power doubled past what is left (M9)
takes a first power larger than `n`, which leaves `left` below 0 and
ends the list at one power; and the template's bit tested above
(M30) shifts every bit down one place and loses the top power.

Two survive, and are equivalent: the table arm's table read across
(M13) takes the larger of `table[i][j]` and `table[j][i]`, and since
only the cells with `i <= j` are ever filled the other is 0; and the
table arm's last bit left out (M15) never looks at bit 30, which no `n`
up to `10^9` sets. P5's `n + 2^30` does set it, but its queries reach
no index past the original powers, so losing that last power changes
no answer.

The first run killed nothing by P2, since every mutation answered each
query on its own. Two of the inverse arm's were replaced by an answer
that depends on the one before it (M20), which reordering the queries
changes, and by each prefix times the bit rather than its power (M21),
which fails apart from every kept one.

## Verification

Every arm prints the same output as `powers.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.0 to 2.4 s, and the
differential 2.9 s; under `karac __mir-llvm-asan` the differential
takes 1.2 s and under `karac run` 0.8 s.

## Benchmarks

The bench builds 100 values from 1 to `10^9` once from its own
generator, each with `10^4` random queries over its powers. It then
makes 10 passes; each answers every value's queries afresh and folds
the answers, each read from a place the pass shifts, plus the pass into
the checksum. The bench uses the ★ arm, the exponents' prefix sums, in
all five languages. Every implementation prints `10 passes over 100
values of 10^4 queries: checksum 966970577`. The queries are lists of
rows in every language, and in C an array of row pointers; each answer
list is allocated afresh.

BENCHTAB
