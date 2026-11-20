# 2367. Number of Arithmetic Triplets

You are given a **0-indexed**, **strictly increasing** integer array
`nums` and a positive integer `diff`. A triplet `(i, j, k)` is an
**arithmetic triplet** if the following conditions are met:

- `i < j < k`,
- `nums[j] - nums[i] == diff`, and
- `nums[k] - nums[j] == diff`.

Return *the number of unique **arithmetic triplets***.

```
nums = [0,1,4,6,7,10], diff = 3  ->  2
nums = [4,5,6,7,8,9], diff = 2   ->  2
```

**Constraints:** `3 <= nums.length <= 200`; `0 <= nums[i] <= 200`;
`1 <= diff <= 50`; `nums` is strictly increasing.

Since the values rise strictly, each value stands at one place, so a
triplet is fixed by its first value `x`, and it exists exactly when
`x + diff` and `x + 2 diff` are values too.

## Approaches

| file | mechanism |
|---|---|
| `triplets.kara` ★ | a `Set` of the values, and each value `x` counted when the set holds `x + diff` and `x + 2 diff`. O(n) |
| `triplets_brute.kara` | every three places `i < j < k` tried, the triplet counted when both gaps are `diff`. O(n^3), at most `200^3 / 6` steps |
| `triplets_pointers.kara` | three pointers: as `x` moves on, the places of `x + diff` and `x + 2 diff` only move on too, so two pointers walk up behind it. O(n) |
| `triplets_table.kara` | a table of 201 marks for the values present, and each value `x` the middle of a triplet when `x - diff` and `x + diff` are marked. O(n + 200) |
| `triplets_iter.kara` | iterators: the values collected into a `Set`, and the triplets counted by `filter` and `count` |
| `triplets_solution.kara` | LeetCode's Rust template: a `HashSet` collected by `iter().cloned()`, read by `contains(&(x + diff))`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; three
values; every value from 0 to 199 with a diff of 1 and of 50; then 3000
random sets of 3 to 40 values from 0 to 3 to 200, with a diff of 1 to
50, with a checksum and how many have no triplet. `triplets.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
against every three places on 3000 random sets.

`check` first reports 10 errors on the template, and `karac fix`
carries it in one call, reporting 18 edits: the
`use std::collections::HashSet` line deleted, since Kāra's `Set` is in
the prelude; `HashSet` renamed `Set`; `struct Solution;` given its
braces; `Vec<..>` and `HashSet<..>` their brackets; `for &x in &nums`
written `for x in ref nums`; the `&` of each `contains(&(..))` dropped
and `&&` written `and`; the `as i64` widening the template's `i32`
answer in the glue dropped; and `Solution::` written with a dot.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every three places `(i, j, k)` tried, each from the first
place to the last, and the triple counted when `i < j < k` and both gaps
are `diff`. No use of the values rising. It checks 300 random sets of 3
to 40 values from 0 to 3 to 200 with a diff of 1 to 50; then 30 dense
sets, all but at most three of the values from 0 to up to 60, with a
diff of 1 to 10; then 30 of up to 200 values from 0 to 200 with a diff
of 1 to 50. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | from 0 to `n - 2` |
| P3 | every value lowered by the smallest: the same answer |
| P4 | every value `x` written `200 - x`, in rising order: the same answer |
| P5 | the last value removed: one fewer exactly when it ends a triplet |
| P6 | each arm agrees with at least three of the other five |

P3 holds because the gaps do not change, and P4 because the triplet
`(i, j, k)` becomes `(n - 1 - k, n - 1 - j, n - 1 - i)` with the same
gaps. P5 holds because the last value can only be the last of a
triplet, and of at most one.

The differential prints `360 cases: checksum 631012415, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every three places. On a failure it prints the
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
| M1 | ★: only x + diff looked up | P1 268, P5 53, P6 268 |
| M3 | ★: either lookup enough | P1 281, P2 3, P5 99, P6 281 |
| M6 | ★: only whether there is a triplet | P1 93, P5 44, P6 93 |
| M7 | brute: the third place two past the second | P1 28, P4 20, P5 3, P6 28 |
| M8 | brute: the second gap at least diff | P1 208, P2 120, P4 210, P5 208, P6 208 |
| M10 | brute: the gaps only equal to each other | P1 306, P2 187, P5 256, P6 306 |
| M12 | pointers: the second pointer walking past equal | P1 143, P5 48, P6 143 |
| M13 | pointers: the third value never checked | P1 186, P4 146, P5 43, P6 186 |
| M15 | pointers: the second pointer moved once a step | P1 124, P4 20, P5 44, P6 124 |
| M17 | table: only even values marked | P1 103, P3 38, P5 18, P6 103 |
| M18 | table: 200 never the third value | P1 5, P3 2, P4 35, P5 5, P6 5 |
| M20 | table: the middle value checked for the third | P1 267, P3 3, P4 184, P5 55, P6 267 |
| M22 | iter: the third value x + diff squared | P1 135, P4 21, P5 38, P6 135 |
| M25 | iter: the set holding each value plus one | P1 136, P4 95, P5 22, P6 136 |
| M26 | iter: exactly one of the two lookups | P1 278, P5 147, P6 278 |
| M29 | solution: the third value one short | P1 124, P4 95, P5 36, P6 124 |
| M31 | solution: multiples of three left out of the set | P1 116, P3 46, P4 65, P5 28, P6 116 |

P1 and P6 kill all seventeen, P5 all seventeen too, P4 ten, P3 four and
P2 three. P2 fails only the edits that can count more than `n - 2`: either
lookup enough, in the ★ arm and the template, where every value but the
last can pass, and the second gap taken as at least `diff` or the two
gaps only equal to each other in the brute arm, which count triples of
places and not values. P3, every value lowered by the
smallest, fails only the edits that read a value for itself and not
only its gaps: the table's even values, its bound at 200 and its middle
value, and the template's multiples of three. P4, the values mirrored,
fails the edits that treat the low end of the values unlike the high
end.

Of the thirty-one, fourteen were not kept. The third value looked up at
`x + 3 diff` in the ★ arm (M2) fails as `x` taken as the middle of the
first two in the iter arm (M24): both count the values with a value
`diff` above and `3 diff` above, one of them shifted by `diff`. The
first value never tried in the ★ and pointer arms (M5, M14) and never
marked in the table (M21) fail alike, and either lookup enough in the
template (M27) as in the ★ arm (M3). Only the outer gap read in the
brute arm (M11) is no slip at all: with the outer gap `2 diff` and the
second gap `diff`, the first gap is `diff` too. The third pointer walked
from the second (M16) reads the second pointer's value after it has run
past the end, and stops on an index out of bounds. The last value left out of the set in the ★ arm
(M4), the last three places never the first in the brute arm (M9), 0
never the first value in the table (M19), the first two values never
tried in the iter arm (M23), and the template's first half only and
count started at one (M28, M30) fail apart from every kept one, and were
left out to keep three to an arm and two to the template.

## Verification

Every arm prints the same output as `triplets.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 to 0.7 s but the brute arm,
2.6 s, whose two lines of 200 values try `1313400` triples of places
each. The differential takes 15 s there, most of it the literal
reading's `n^3` steps, and 0.69 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 1000 sets once from the harness's generator, set `s`
keeping each value from 0 to 200 with a chance of `1 + s % 8` in 8 and
always 0, 1 and 2, then makes 50 passes, pass `p` answering each set
with a diff of `1 + (s + p) % 50` and folding each answer plus `p` into
the checksum, with the ★ arm in all five languages. Every
implementation prints `50 passes over 1000 sets of up to 201 values:
checksum 953178045`. Rust uses `HashSet` and Go a `map` to empty
structs, both seeded hash tables as Kāra's `Set` is, and Python its
`set`. C has no hash set in its standard library, so it carries one of
open addressing with linear probing over `2^10` slots, the key mixed by
splitmix64's finalizer: the same algorithm over a different table, which
the comparison should be read with. Every implementation builds its set
afresh in each call.

BENCHTAB
