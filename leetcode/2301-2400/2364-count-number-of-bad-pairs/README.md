# 2364. Count Number of Bad Pairs

You are given a **0-indexed** integer array `nums`. A pair of indices
`(i, j)` is a **bad pair** if `i < j` and `j - i != nums[j] - nums[i]`.

Return *the total number of **bad pairs** in* `nums`.

```
nums = [4,1,3,3]    ->  5
nums = [1,2,3,4,5]  ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`.

A pair is good exactly when `nums[i] - i == nums[j] - j`, so the pairs
split by that key: places with the same key make good pairs, and every
other pair is bad. `10^5` places make `4999950000` pairs, past `i32`,
which is why LeetCode's answer is an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `bad.kara` ★ | each place's key counted in a `Map` as the places go by; the places before `j` with its key are its good pairs, and the bad pairs are all `n (n - 1) / 2` less the good ones. O(n) |
| `bad_sort.kara` | the keys sorted so that equal ones stand together, and each run of `c` equal keys taking its `c (c - 1) / 2` good pairs from all the pairs. O(n log n) |
| `bad_direct.kara` | the bad pairs counted directly: place `j` adds `j` less the places before it with its key, kept in a `SortedMap`. O(n log n) |
| `bad_halves.kara` | divide and conquer, as merge sort: each half's keys sorted and its good pairs counted by recursion, and the good pairs that cross the middle counted while the halves are merged, a run of a key on the left times its run on the right. O(n log n) |
| `bad_iter.kara` | iterators: the keys by `enumerate` and `map`, folded into a `Map` of counts, and the good pairs as the sum over its `values` of `c (c - 1) / 2` |
| `bad_solution.kara` | LeetCode's Rust template: a `HashMap` of counts through `entry(..).or_insert(0)`, each place adding the places before it with another key; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one value;
`10^5` values rising by one, every pair good; `10^5` equal values,
every pair bad; `10^5` values in four interleaved keys; then 2000
random arrays of 1 to 40 values, each the place plus a small offset or,
with a chance of 1 in 8, a random value up to `10^9`, with a checksum
and how many have no bad pair. `bad.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked against every pair
on 3000 random arrays.

A fifth arm was first written from the statement, every pair checked.
Its work is `n^2 / 2` steps, `5 * 10^9` on each long line of the
harness, so it was replaced by divide and conquer, and the
differential's literal reading stands in for it.

`check` first reports 7 errors on the template, and `karac fix` carries
it in one call, reporting 13 edits: the `use std::collections::HashMap`
line deleted, since Kāra's `Map` is in the prelude; `HashMap` renamed
`Map` and its `::new` written with a dot; `struct Solution;` given its
braces; `Vec<..>` and `HashMap<..>` their brackets; the `&` of
`(i, &x)` dropped; the `as i64` on `i`, an index that is already an
`i64`, dropped twice; and `Solution::` written with a dot. The
`let same = seen.entry(key).or_insert(0);` binding, read through
`*same` and raised through `*same += 1`, stands as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair `i < j` checked for `j - i != nums[j] - nums[i]`.
No keys. It checks 300 random arrays of 1 to 40 values, each the place
plus a small offset or, with a chance of 1 in 8, a random value up to
`10^9`; then 30 of up to 2000 values; then 30 of up to 300 values whose
keys come from at most 1 to 4 numbers. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | from 0 to `n (n - 1) / 2` |
| P3 | the first value removed: the answer less the bad pairs it made |
| P4 | the values reversed and negated: the same answer |
| P5 | a value one more than the last appended: the answer plus `n`, less the places whose key is the last's |
| P6 | each arm agrees with at least three of the other five |

P3 holds because removing the first place moves every other place down
by one, which shifts every key by the same one and so keeps which keys
are equal. It was first every value raised by the same amount, which
holds for the same reason but failed none of the 28 edits first run
against it: no arm
reads a value except through its key, and no slip in one made the
answer depend on where the values start. P4 holds because the pair `(i, j)` of the new array is the pair
`(n - 1 - j, n - 1 - i)` of the old one, with the same distance and
the same difference of values. P5 holds because the new place's key is
the last place's, so it makes a good pair with every place that shares
that key and a bad pair with the rest.

The differential prints `360 cases: checksum 452145393, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and checks every pair. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the good pairs returned | P1 351, P3 346, P5 349, P6 351 |
| M5 | ★: all the pairs counted as n squared over two | P1 354, P2 22, P3 191, P5 169, P6 354 |
| M6 | ★: the key taken from the value alone | P1 340, P3 296, P5 357, P6 340 |
| M7 | sort: the keys left unsorted | P1 318, P3 268, P5 265, P6 318 |
| M8 | sort: the last run left out | P1 58, P3 42, P4 310, P5 55, P6 58 |
| M10 | sort: the run never moved on | P1 339, P2 333, P3 339, P4 275, P5 339, P6 339 |
| M14 | direct: the place counted from one | P1 360, P2 74, P3 354, P5 360, P6 360 |
| M15 | direct: keys within one taken as the same | P1 251, P2 104, P3 151, P4 224, P5 143, P6 251 |
| M16 | direct: the first place skipped | P1 294, P3 318, P4 188, P5 126, P6 294 |
| M17 | halves: the crossing pairs added, not multiplied | P1 291, P3 247, P4 140, P5 255, P6 291 |
| M18 | halves: a half of two never split | P1 331, P3 288, P4 292, P5 325, P6 331 |
| M19 | halves: the merged keys never written back | P1 308, P3 284, P4 304, P5 286, P6 308 |
| M23 | iter: the counts taken as pairs, not their pairs | P1 320, P3 263, P5 283, P6 320 |
| M24 | iter: the key from the value and the place summed | P1 343, P3 295, P5 359, P6 343 |
| M25 | iter: each key counted at 1 | P1 345, P3 294, P5 360, P6 345 |
| M30 | solution: the count raised before it is read | P1 360, P2 45, P3 354, P5 360, P6 360 |
| M31 | solution: the key halved | P1 194, P3 235, P4 120, P5 105, P6 194 |

P1, P3, P5 and P6 kill all seventeen, P4 eight and P2 five. P2 fails
only the edits that count more pairs than there are, or a bad pair
where every pair is good: the good pairs counted after the place
itself, the pairs counted as `n^2 / 2` or with the place from one,
keys within one taken as the same, the run never moved on. P4, the
values reversed and negated, fails the edits that treat one end of the
array unlike the other or that read a key's size and not only whether
two keys are equal: the last run or the first place left out, keys
within one taken as the same, the key halved, which rounds a negative
key the other way, and the three slips of the merge.

The ★ arm's count never stored first stood where its all the pairs
counted as `n^2 / 2` (M5) now is; it failed as each key counted at 1
in the iter arm (M25), the place added in the direct arm (M12) and the
template's count never raised (M28), and the ★ arm had no other edit
left to keep.

Of the thirty-one, fourteen were not kept. The key the sum, not the
difference, in the ★ arm (M1) fails as in the iter arm (M24); the good
pairs counted after the place itself (M2) and each run or count taken as
`c (c + 1) / 2` in the sort and iter arms (M9, M22) as the template's
count raised before it is read (M30); all the pairs counted with
`i <= j` (M3) and the template's place counted from one (M27) as the
direct arm's (M14); the place added, not the others (M12), and the
template's count never raised (M28) as each key counted at 1 (M25); the
count set to one in the direct arm (M13) as the counts taken as pairs
in the iter arm (M23); the first value skipped in the iter arm (M26) as
the first place skipped in the direct arm (M16); and the template's key
from the value alone (M29) as the ★ arm's (M6). The sort arm's place
counted twice in the key (M11) and the merge's only the first key of a
run on the left (M20) and right half not recursed (M21) fail apart from
every kept one, and were left out to keep three to an arm and two to
the template.

## Verification

Every arm prints the same output as `bad.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.8 to 2.3 s, the merge 4.8 s, but
the direct arm 14.8 s. On the line of equal values the keys
`nums[j] - j` fall from place to place, so its `SortedMap` takes `10^5`
keys from the largest down, each insert at the front, and the interpreter's sorted table shifts every later entry on
each insert, so that line is quadratic there: `10^5` such inserts alone
take 14 s, against 3.2 s for half as many and 0.87 s for a quarter.
Under `karac __mir-llvm-run` it is not (B-2026-11-21-50). The differential takes
8.5 s under `karac __mir-run` and 0.79 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 arrays of `10^5` values once from the harness's
generator, array `a` holding the place plus one of `4^a` offsets (at
most `10^5`) below `999 * 10^6`, so that the keys run from one to tens
of thousands, then makes 20 passes, pass `p` folding each answer plus
`p` into the checksum, with the ★ arm in all five languages. Every
implementation prints `20 passes over 10 arrays of 10^5 values:
checksum 539911154`. Rust uses `HashMap` and Go its `map`, both seeded
hash maps as Kāra's `Map` is, and Python its dict. C has no hash map in
its standard library, so it carries one of open addressing with linear
probing over `2^18` slots, the key mixed by splitmix64's finalizer: the
same algorithm over a different table, which the comparison should be
read with. Every implementation builds its map afresh in each call.

BENCHTAB
