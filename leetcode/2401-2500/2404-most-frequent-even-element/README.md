# 2404. Most Frequent Even Element

Given an integer array `nums`, return *the most frequent even element*.

If there is a tie, return the **smallest** one. If there is no such
element, return `-1`.

```
nums = [0,1,2,2,4,4,1]              ->  2
nums = [4,4,4,9,2,4]                ->  4
nums = [29,47,21,41,13,37,25,7]     ->  -1
```

**Constraints:** `1 <= nums.length <= 2000`; `0 <= nums[i] <= 10^5`.

Every even value is counted, and the answer is the one with the largest
count, the smallest among equal counts. A `Map` of counts is read in its
per-process order, so the tie must be broken by value, not by which
entry comes first.

## Approaches

| file | mechanism |
|---|---|
| `even.kara` ★ | a `Map[i64, i64]` of the even values' counts, every entry then read, the most frequent kept and the smaller among equal counts, so the Map's order never shows. O(n) |
| `even_array.kara` | a counting array of `10^5 + 1`, scanned over the even indexes from the smallest, the first of the most frequent kept. O(n + 10^5) |
| `even_sort.kara` | the even values gathered and sorted, equal ones then in runs, smallest first; the first longest run wins. O(n log n) |
| `even_sorted.kara` | a `SortedMap` of counts, read in key order, so only a strictly larger count replaces the best. O(n log n) |
| `even_iter.kara` | iterators: the evens by `filter`, counted by `fold` into a `Map`, the answer by `max_by_key` on (count, the value negated), then `map` and `unwrap_or(-1)`. O(n) |
| `even_solution.kara` | LeetCode's Rust template: a `HashMap<i32, i32>` by `*cnt.entry(x).or_insert(0) += 1`, its entries read with `(&k, &v)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; 0 alone
and one odd value; a tie of three evens beside a more frequent odd;
2000 values up to `10^5`; 2000 values whose evens are drawn from 2 to
20; then 3000 random arrays of 1 to 30 values below 1 to 40, with a
checksum and the count of -1. `even.py` mirrors the ★ arm and its output
is byte-identical, and the mirror was checked on 30000 random arrays of
up to 15 values against counting every even value.

`check` first reports 10 errors on the template, and `karac fix`
carries it in one call, reporting 14 edits: `use
std::collections::HashMap;` deleted; `struct Solution;` given its
braces; `Vec<i32>` and `HashMap<i32, i32>` their brackets, `HashMap`
written `Map` and `HashMap::new` `Map.new`; the `&` of `&x`, `&k` and
`&v` in the patterns dropped; and `||` and `&&` written `or` and `and`.
`*cnt.entry(x).or_insert(0) += 1` stands as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every even value in the array, every place counted where
that value stands, and the value with the most kept, the smaller of
equal counts. No table of counts. It checks 300 random arrays of 1 to
12 values below 1 to 30, which the literal reading answers; then 30 of
up to 2000 values up to `10^5`; then 30 of up to 2000 values whose
evens are drawn from 2 to 20. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 values, the answer is the literal reading's |
| P2 | the answer is -1 exactly when no value is even, and otherwise the smallest even value with the largest count, by a table of counts |
| P3 | the values reversed: the same answer |
| P4 | every odd value removed: the same answer |
| P5 | the answer, when there is one, appended again: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 answers every case, the large ones too, from one table of counts
built in the harness. P3 holds because counts do not depend on order,
P4 because odd values are never counted, and P5 because one more copy
of the most frequent value leaves it the most frequent, now alone.

The differential prints `360 cases: checksum 919750821, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts each even value. On a failure it prints the
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
| M1 | ★: the odd values counted | P1 300, P2 360, P4 290, P6 360 |
| M5 | ★: only multiples of 4 counted | P1 98, P2 137, P6 137 |
| M6 | ★: the first value ignored | P1 61, P2 61, P3 92, P4 44, P6 61 |
| M7 | array: only multiples of 6 read | P1 129, P2 171, P6 171 |
| M10 | array: an absent value taken first | P1 27, P2 27, P6 27 |
| M11 | array: 0 never read | P1 103, P2 103, P6 103 |
| M12 | sort: the evens never sorted | P1 82, P2 137, P3 163, P6 137 |
| M14 | sort: each record one longer | P1 48, P2 74, P6 74 |
| M16 | sort: the smallest even skipped | P1 149, P2 156, P6 156 |
| M17 | sorted: a tie going to the larger | P1 110, P2 138, P6 138 |
| M18 | sorted: each value counted once | P1 63, P2 110, P6 110 |
| M19 | sorted: the smallest even ignored | P1 210, P2 223, P6 223 |
| M24 | iter: the multiples of 6 never counted | P1 144, P2 162, P6 162 |
| M25 | iter: the least frequent taken | P1 204, P2 264, P5 222, P6 264 |
| M26 | iter: each count the value itself | P1 169, P2 227, P6 227 |
| M28 | solution: the value 2 never counted | P1 49, P2 55, P6 55 |
| M29 | solution: a value seen once never the answer | P1 136, P2 143, P6 143 |

P1, P2 and P6 kill all seventeen, P3 and P4 two each, and P5 one. P3,
the values reversed, fails only the two edits that skip the first value
(M6) or sort nothing (M12), since every other edit counts the same
values whatever their order; P4, the odd values removed, fails the ★
arm's odd values counted (M1) and M6; and P5, the answer appended again,
fails only the iter arm's least frequent taken (M25), the one edit whose
answer a further copy of itself can move.

Of the thirty-one, fourteen were not kept, each failing the same checks
as a kept one: every tie going to the larger (M2, M9, M13, M23, M31) as
the sorted arm's (M17); each value counted once (M3, M27) as M18; 0 or
-2 when there is no even (M4, M20, M24 as first written, M28 as first
written) as the array arm's absent value taken first (M10); the array
arm's every other even skipped (M8) as the ★ arm's multiples of 4 (M5);
the sort arm's 0 never counted (M15) as the array arm's (M11); the
sorted arm's later value needing two more (M21) as the sort arm's each
record one longer (M14); the iter arm's odd values counted (M22) as M1;
and the template's first value ignored (M30) as M6. Three were replaced
by edits that fail apart from every kept one. The array arm's 10^5
never read (M7 as first written) survived, since 10^5 would be the
answer only as the most frequent even value, which no case makes it;
its first replacement, the smallest even present taken, failed as M18;
it is now only multiples of 6 read. The iter arm's 0 when there is no
even (M24) is now the multiples of 6 never counted, after a first
replacement, a tie going to the smallest modulo 8, failed differently
under the two backends: its ties fell to the map's walk order, which is
random per process. The template's -2 when there is no even (M28) is
now the value 2 never counted.

## Verification

Every arm prints the same output as `even.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.3 to 0.6 s, but for the array
arm, 29 s: it fills and walks a table of `10^5 + 1` counts in every
call, the 2000 random cases included. The differential takes 21 s there,
5.5 s under `karac __mir-llvm-asan` and 0.8 s under `karac run`.

## Benchmarks

The bench builds 200 arrays of 2000 values, array `i` below `1 + 50 i`,
once from the harness's generator, then makes 100 passes, answering
every array and folding each answer plus the pass into the checksum,
with the ★ arm in all five languages. Every implementation prints `100
passes over 200 arrays of 2000 values: checksum 111876912`. Kāra counts
in its `Map`, hashed by SipHash-1-3, Rust in a `HashMap`, hashed by
SipHash too, Python in a dict and Go in a map, each built afresh in
every call; C counts in a fixed open-addressing table of 4096 slots,
cleared in every call, with a multiplicative hash.

BENCHTAB
