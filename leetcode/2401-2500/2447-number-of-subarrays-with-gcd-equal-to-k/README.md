# 2447. Number of Subarrays With GCD Equal to K

Given an integer array `nums` and an integer `k`, return *the number of
**subarrays** of* `nums` *where the greatest common divisor of the
subarray's elements is* `k`.

A **subarray** is a contiguous non-empty sequence of elements within an
array.

The **greatest common divisor of an array** is the largest integer that
evenly divides all the array elements.

```
nums = [9,3,1,2,6,3], k = 3  ->  4
nums = [4], k = 7            ->  0
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i], k <= 10^9`.

As a subarray grows to the right its GCD can only divide down, and it
changes at most `log V` times, since each change at least halves it. So
from each start the GCD is `k` on one run of ends at most, and once it
is no multiple of `k` no longer subarray from that start can return to
`k`.

## Approaches

| file | mechanism |
|---|---|
| `gcd.kara` ★ | from each start, the GCD kept as the subarray grows by Euclid's algorithm in a loop, the walk stopped once it is no multiple of `k`. O(n^2 log V) at worst |
| `gcd_naive.kara` | the statement read directly: every subarray, its GCD carried from the one a value shorter by Euclid's algorithm written recursively, counted when it equals `k`; no walk stops early. O(n^2 log V) |
| `gcd_list.kara` | the distinct GCDs of the subarrays ending at each place with how many subarrays have each, a `Vec[(i64, i64)]` of at most `log V` entries, each step the last list folded with the new value and merged where neighbours meet. O(n log^2 V) |
| `gcd_sparse.kara` | a `Sparse` struct, a table of GCDs over spans of `2^p` values, so a range's GCD is two lookups; from each start the run of ends whose GCD is `k` found by two binary searches. O(n log n log V) |
| `gcd_iter.kara` | iterators: from each start, the running GCD by `scan`, cut by `take_while` once it is no multiple of `k`, the ends at `k` counted by `filter` and `count`, every start added by `map` and `sum`. O(n^2 log V) at worst |
| `gcd_solution.kara` | LeetCode's Rust template: a `gcd` nested inside the method, the values `i32`, and each start's walk stopped once the GCD falls below `k`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; one value
equal to `k`; `k` larger than every value; `k` of `10^9`; then 1000
values, the constraints' most, all equal to `k`; random multiples of 6
up to 6000 against 6; random values from 1 to `10^9` against 1;
multiples of 12 with every hundredth value 18, against 6; and 3000
random arrays of 1 to 12 values from 1 to 12, `k` from 1 to 6, as a
checksum and the total. `gcd.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 20000 random arrays of up
to 9 values against every subarray's GCD taken by `math.gcd`.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 6 edits: the brackets of `Vec<i32>`; the
nested `fn gcd` moved above the `impl` in two edits, an insertion and a
deletion, since Kāra has no nested items and a nested `fn` captures
nothing; `struct Solution;` given its braces; and, once the template
parses, the harness's `as i64` on the `i32` the template returns, a
widening Kāra makes implicitly. The recursion, `if b == 0 { a } else
{ .. }` as an expression, `let mut g = 0` and `nums[j]` stand as Kāra.

`gcd_list.kara` starts each step's list as `[(x, 1)].to_vec()`, where
`x` is the `ref i64` that `nums.iter()` yields. Kāra reads a `Copy`
value through a reference wherever an `i64` is expected, and it does so
for `[x].to_vec()` into a `Vec[i64]` and for `(x, 1)` into an `(i64,
i64)`, but the tuple inside the array literal was refused as a
`Vec[(ref i64, i64)]` until B-2026-11-24-24, which checks a literal of tuples
against the slot's tuple of scalars.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray tested value by value, and counted when `k`
divides every value and no larger multiple of `k`, up to the least
value, divides them all. A common divisor larger than `k` would make
the GCD a multiple of `k` larger than `k`, so those are the only ones
to try. No remainder chain is run. It checks 300 random arrays of 1 to
10 values from 1 to 60, `k` from 1 to 12; then 30 of up to 30 values,
each `k` times 1 to 30, `k` up to `10^6`; then 30 of up to 60 values
from 1 to 12, `k` 1 or 2. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the values reversed: the same answer |
| P3 | every value put twice in a row: four times the answer, less the count of values equal to `k` |
| P4 | `k` appended: the answer plus one more than the length of the run of multiples of `k` that ends the array |
| P5 | a value that is no multiple of `k` put at a place, when `k` is above 1: the two parts' answers added |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a subarray reversed has the same GCD. P3 holds because
the doubled array's subarrays are the original's with each end doubled
or not, which has the same GCD: four for each subarray of two or more
values, and three for each single value. P4 holds because the new
subarrays all end at `k`, and their GCD is `k` exactly when every value
in them is a multiple of `k`. P5 holds because no subarray across the
new value has a GCD that `k` divides.

The differential prints `360 cases: checksum 247115814, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries the same multiples. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the GCD carried across starts | P1 111, P2 58, P3 94, P4 293, P5 39, P6 111 |
| M4 | ★: stopped once the GCD no longer divides k | P1 96, P2 31, P4 119, P6 96 |
| M5 | ★: every multiple of k counted | P1 234, P3 234, P6 234 |
| M8 | naive: the first value of each start skipped | P1 53, P3 53, P4 360, P6 53 |
| M10 | naive: counted when the GCD divides k | P1 257, P3 47, P4 289, P5 307, P6 257 |
| M11 | naive: the last start never tried | P1 5, P2 11, P3 5, P4 355, P5 6, P6 5 |
| M12 | list: each merged count lost | P1 81, P2 55, P3 116, P4 124, P6 81 |
| M14 | list: the GCDs folded with the first value | P1 107, P2 98, P3 106, P4 133, P5 60, P6 107 |
| M15 | list: counted against the new value | P1 109, P2 50, P4 289, P5 28, P6 109 |
| M17 | sparse: the run begun at twice k | P1 94, P3 61, P6 94 |
| M19 | sparse: every row built from the values | P1 68, P2 64, P3 85, P4 56, P5 38, P6 68 |
| M21 | sparse: the stop at k dropped | P1 116, P3 53, P4 360, P6 116 |
| M23 | iter: the state before the value handed back | P1 73, P2 58, P3 73, P4 360, P5 34, P6 73 |
| M24 | iter: each start from the next value | P1 72, P2 58, P3 72, P4 71, P5 33, P6 72 |
| M26 | iter: at most one end per start | P1 77, P2 55, P3 116, P4 73, P6 77 |
| M28 | solution: the answer started at 1 | P1 360, P3 360, P5 328, P6 360 |
| M31 | solution: the first value folded into every start | P1 119, P2 87, P3 106, P4 236, P5 42, P6 119 |


P1 and P6 kill all seventeen, P3 fifteen, P4 fourteen, P2 eleven and
P5 ten.

Fourteen are not kept, and each fails exactly as a kept one: the ★
arm's and the template's first value of each start skipped (M1, M30) as
the iter arm's each start from the next value (M24), each start's walk
counting the next start's subarrays; the ★ arm's and the template's
walk stopped at its first match (M3, M29) as the iter arm's at most one
end per start (M26); the ★ arm's last start never tried (M6) as the
naive arm's (M11); the naive arm's base case returning `b` (M7), which
makes every GCD 0 and every answer 0, and the list arm's new value
counted twice (M13) as the sparse arm's stop at `k` dropped (M21),
which answers 0 too; the naive arm's GCD started at `k`, the sparse
arm's run counted from the start, and the iter arm's scan started at
`k` and every multiple at least `k` counted (M9, M18, M22, M25) as the
★ arm's every multiple of `k` counted (M5), each counting the
subarrays whose values are all multiples of `k`; the list arm's each
entry counted once (M16) as its merged count lost (M12), both losing
the subarrays merged into an entry; the sparse arm's last end never
searched (M20) as the iter arm's state before the value handed back
(M23), both missing every subarray that ends at the last value; and
the template's GCD above `k` never left (M27) as the ★ arm's walk
stopped once the GCD no longer divides `k` (M4), both stopping at the
first GCD above `k`.

The first run replaced two things. P3 was every value and `k`
multiplied by one number from 2 to 9, which every mutant passed, since
each arm's answer scales with the values whatever it gets wrong; it was
replaced by every value put twice in a row, and all 31 were run again.
And the sparse arm's span one short, `(2 << p) < r - l + 1`, survived as
an equivalent: when the range is exactly twice the shorter span, its
two spans of `2^p` still tile it. It was replaced by the run begun at
twice `k` (M17), which fails apart.

## Verification

TIMES

## Benchmarks

The bench builds 20 arrays of 1000 values, the constraints' longest,
once from its own generator: each value 6 times 1 to 1000, and one in
40 one more than that, so the walks against `k = 6` run until the next
value that is no multiple. It then makes 90 passes; pass `p` draws one
value of every array afresh, so no answer can be carried from one pass
to the next, then answers every array and folds the answer plus the
pass into the checksum. The bench uses the ★ arm, the running GCD
stopped at the first value no multiple of `k`, in all five languages.
Every implementation prints `90 passes over 20 arrays of 1000 values:
checksum 480321083`.

BENCHTAB
