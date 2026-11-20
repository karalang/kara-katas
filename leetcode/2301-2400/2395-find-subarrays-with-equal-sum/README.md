# 2395. Find Subarrays With Equal Sum

Given a **0-indexed** integer array `nums`, determine whether there
exist **two** subarrays of length `2` with **equal** sum. Note that the
two subarrays must begin at **different** indices.

Return `true` *if these subarrays exist, and* `false` *otherwise.*

A **subarray** is a contiguous non-empty sequence of elements within an
array.

```
nums = [4,2,4]      ->  true
nums = [1,2,3,4,5]  ->  false
nums = [0,0,0]      ->  true
```

**Constraints:** `2 <= nums.length <= 1000`; `-10^9 <= nums[i] <=
10^9`.

A subarray of length 2 is a neighbouring pair, so the question is
whether two of the `n - 1` neighbouring sums are equal.

## Approaches

| file | mechanism |
|---|---|
| `subarrays.kara` ★ | each neighbouring sum into a `Set`, a sum already there the answer. O(n) |
| `subarrays_sort.kara` | the neighbouring sums gathered and sorted, two equal ones then side by side. O(n log n) |
| `subarrays_pairs.kara` | every two starting indices compared, each pair of pairs summed afresh; no collection. O(n^2) |
| `subarrays_map.kara` | a `SortedMap` from each sum to the first index it starts at, a later start for a known sum the answer. O(n log n) |
| `subarrays_iter.kara` | iterators: the sums by `zip` with the values after one, `collect`ed into a `Set`; fewer distinct sums than pairs is the answer |
| `subarrays_solution.kara` | LeetCode's Rust template: a `HashSet` whose `insert` says whether the sum was new, over `windows(2)` with `any`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

The `Set`s are only asked what they hold, so their order never shows.

Every arm prints the same 6 lines: LeetCode's three examples; the two
pairs overlapping, and two values alone; then 1000 values from `-10^9`
to `10^9`, as drawn and with its first two values copied to the end;
then 3000 random arrays of 2 to 12 values from `-top` to `top`, `top`
from 0 to 20, with a checksum and the count of yes. `subarrays.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 20000 random arrays of up to 9 values against every two
pairs.

`check` first reports 5 errors on the template, and `karac fix` carries
it in one call, reporting 8 edits: `struct Solution;` given its braces;
`use std::collections::HashSet;` deleted, and `HashSet::new()` written
`Set.new()`, `Set` being in the prelude; `Vec<i32>` its brackets; the
`!` before `seen.insert(..)` written `not`; and `.into_iter()` put after
`windows(2)`, which gives a `Vec` of windows. `insert` answering whether
the value was new, `any` and indexing a window stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray, each a start and an end, the ones of length
2 kept, and every two of those with different starts compared by summing
their elements. It checks 300 random arrays of 2 to 12 values from
`-top` to `top`, `top` from 0 to 20, which the literal reading answers;
then 30 of up to 2000 values from `-10^9` to `10^9`, where a repeat is
rare; then 30 of up to 2000 values from `-top` to `top`, `top` up to 3,
where one is all but certain. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 values, the answer is the literal reading's |
| P2 | the values reversed: the same answer |
| P3 | every value plus the same number: the same answer |
| P4 | every value negated: the same answer |
| P5 | the first two values copied to the end: yes |
| P6 | each arm agrees with at least three of the other five |

P2 holds because reversing keeps the same neighbouring pairs, and P3
and P4 because adding a constant to every value, or negating them all,
moves every sum alike.

The differential prints `360 cases: checksum 747162696, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: each pair's difference | P1 76, P6 76 |
| M5 | ★: each pair its second value | P1 47, P2 32, P6 47 |
| M6 | ★: each sum kept one larger | P1 91, P2 75, P4 75, P5 176, P6 98 |
| M7 | sort: the sums unsorted | P1 52, P5 186, P6 52 |
| M8 | sort: neighbours one apart taken as equal | P1 98, P5 149, P6 105 |
| M9 | sort: the two smallest sums never compared | P1 18, P4 20, P5 15, P6 18 |
| M12 | pairs: overlapping pairs never compared | P1 34, P6 34 |
| M14 | pairs: the later pair its first value twice | P1 71, P2 61, P5 163, P6 71 |
| M16 | pairs: unequal sums taken | P1 139, P5 54, P6 176 |
| M17 | map: an earlier start refused | P1 139, P5 360, P6 169 |
| M19 | map: the second value counted twice | P1 78, P2 82, P6 78 |
| M21 | map: each sum kept by its size | P1 52, P2 47, P3 111, P4 92, P5 119, P6 52 |
| M22 | iter: the pairs two apart | P1 161, P6 191 |
| M24 | iter: one pair too few counted | P1 65, P5 136, P6 65 |
| M26 | iter: each pair its larger value | P1 110, P4 23, P6 140 |
| M28 | solution: windows of three | P1 17, P2 26, P5 136, P6 17 |
| M29 | solution: each window its first value twice | P1 45, P2 32, P6 45 |

P1 and P6 kill all seventeen, P5 ten, P2 seven, P4 four and P3 one.
P5, the first two values copied to the end, passes seven: the three
that only P1 and P6 catch (M3, M12, M22), each pair its larger value
(M26), and three that read a pair's values unalike (M5, M19, M29). P2,
the values reversed, fails the edits that read a pair's two values
unalike (M5, M14, M19, M29), windows of three (M28), and the sums
shifted or keyed by size (M6, M21). P4, every value negated, fails the
edits that treat the large and the small unalike: each sum one larger
(M6), the two smallest never compared (M9), each pair its larger value
(M26), and the sums keyed by size (M21). P3, every value plus a
constant, fails only that last edit (M21): a constant added changes
which sums share a size.

Of the thirty-one, fourteen were not kept. A sum not yet seen taken as
seen (M1), each pair compared with itself (M13), as many sums as pairs
taken as a repeat (M25) and the template's new sum taken as a repeat
(M27) fail as the iter arm's pairs two apart (M22) do; the ★ arm's no
sum ever kept (M2) as the map arm's earlier start refused (M17); the
iter arm's each pair's difference (M23) as the ★ arm's (M3); the sort
and map arms' last pair left out (M11, M20) as the template's windows of
three (M28); and the map arm's each sum kept one larger (M18) as the ★
arm's (M6). The first pair skipped in the ★, pairs and template arms
(M4, M15, M31) fail alike, and apart from every kept one, as does the
sort arm's each pair's product (M10); they were left out to keep three
to an arm. The template's first value counted twice (M30) overflowed
its `i32` on values near `10^9` and stopped with a runtime error under
both backends; a crash is not kept.

## Verification

Every arm prints the same output as `subarrays.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.22 to 0.38 s. The differential
takes 34.8 s there, 6.4 s under `karac __mir-llvm-asan` and 0.78 s
under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 100 arrays of 1000 values from `-top` to `top`, `top`
from 1000 to about `10^6`, once from the harness's generator, so some
have a repeated sum and some do not, then makes 2000 passes, answering
every array and folding each answer plus the pass into the checksum,
with the ★ arm in all five languages. Every implementation prints `2000
passes over 100 arrays of 1000 values: checksum 149795326, 90000 yes`.
Kāra's `Set`, Rust's `HashSet` and Go's map hash with their own
library's hash and grow as they fill; C has no set in its library, and
its open-addressing table of 4096 slots is allocated once and cleared
for each call, which the others cannot match.

BENCHTAB
