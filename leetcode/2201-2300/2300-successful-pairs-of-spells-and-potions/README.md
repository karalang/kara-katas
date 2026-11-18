# 2300. Successful Pairs of Spells and Potions

You are given two positive integer arrays `spells` and `potions`, of
length `n` and `m` respectively, where `spells[i]` represents the
strength of the `i`th spell and `potions[j]` represents the strength of
the `j`th potion.

You are also given an integer `success`. A spell and potion pair is
considered **successful** if the **product** of their strengths is
**at least** `success`.

Return *an integer array* `pairs` *of length* `n` *where* `pairs[i]` *is
the number of potions that will form a successful pair with the* `i`*th
spell.*

```
spells = [5,1,3], potions = [1,2,3,4,5], success = 7   ->  [4,0,3]
spells = [3,1,2], potions = [8,5,8], success = 16      ->  [2,0,2]
```

**Constraints:** `n == spells.length`; `m == potions.length`;
`1 <= n, m <= 10^5`; `1 <= spells[i], potions[i] <= 10^5`;
`1 <= success <= 10^10`.

A spell succeeds with a potion exactly when the potion is strong
enough, and a stronger potion succeeds wherever a weaker one does, so
in sorted order a spell's successful potions are the last ones. Sort
the potions once and binary-search each spell's first: O((n + m) log
m). The products reach 10^10, past `i32`.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | the potions sorted once; each spell's count is the number past the `partition_point` of the potions whose product with it falls short of `success` |
| `pairs_naive.kara` | every pair tried: for each spell, a count of the potions whose product with it reaches `success`. O(n * m) |
| `pairs_table.kara` | `at_least[v]`, the number of potions of strength `v` or more, summed down from the strongest; a spell needs `success / spell` rounded up and reads its count there, or 0 past the strongest. O(n + m + top) |
| `pairs_sweep.kara` | the spells' indices sorted by strength with `sort_by_key`, and a pointer into the sorted potions that only moves down, since a stronger spell succeeds with every potion a weaker one did. O(n log n + m log m) |
| `pairs_struct.kara` | `struct Shelf` holds the sorted potions and `at_least(need)` binary-searches by hand for the first of strength `need`; the spells are `map`ped through it |
| `pairs_solution.kara` | LeetCode's Rust template: `mut potions: Vec<i32>` sorted with `sort_unstable`, each spell `map`ped to `m - potions.partition_point(..)` with the product taken in `i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; a success
every pair reaches; one only the strongest pairs reach, `10^5 * 10^5 =
10^10`; one no pair reaches; then 2000 random cases of 1 to 40 spells
and 1 to 40 potions from 1 to 50 and a success from 1 to 2600, with a
checksum and the sum of every answer. `pairs.py` mirrors the ★ arm and
its output is byte-identical.

`karac fix` carries the template in one call, reporting 12 edits:
`struct Solution;` to `struct Solution {}`; the brackets of the three
`Vec<i32>`; the parameter `mut potions: Vec<i32>` to `potions: own
Vec[i32]` with `let mut potions = potions;` at the top of the body;
the `&` of the closure patterns `|&s|` and `|&p|` dropped; and, once
those parse, `sort_unstable()` to `sort()`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair of a spell and a potion is listed with its
product, the successful ones kept as pairs of indices, and each spell's
answer is the number of kept pairs that name it. No sorting, no search,
no table. It checks 300 random cases of 1 to 30 spells and potions from
1 to 30 and a success from 1 to 500; then 30 whose success is the
product of one of their own pairs, so that some product meets it
exactly; then 30 of strengths up to 10^5 and a success up to 10^10. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | one answer for each spell, each from 0 to the number of potions |
| P3 | the potions in reverse order: the same answer |
| P4 | a stronger spell has at least as many successful pairs as a weaker one |
| P5 | every spell and the success doubled: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 748079888, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and counts each spell's pairs with a generator.
Of the 5861 answers, 1737 are 0 and 516 count every potion. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a product equal to success not enough | P1 86, P6 86 |
| M3 | ★: the potions left unsorted | P1 321, P3 325, P6 321 |
| M4 | ★: `m` the number of spells | P1 353, P2 296, P6 353 |
| M8 | naive: the count never reset | P1 338, P2 312, P4 333, P6 338 |
| M9 | naive: the last potion never tried | P1 252, P3 246, P6 252 |
| M10 | naive: the strengths added | P1 349, P5 23, P6 349 |
| M12 | table: the strength needed rounded down | P1 274, P6 274 |
| M13 | table: the strongest potion never enough | P1 43, P6 43 |
| M14 | table: the sums shifted by one | P1 353, P6 353 |
| M17 | sweep: the spells walked unsorted | P1 327, P4 202, P6 327 |
| M19 | sweep: the failing potions counted | P1 358, P4 330, P6 358 |
| M21 | sweep: the potions sorted strongest first | P1 337, P6 337 |
| M22 | struct: a potion equal to the need passed over | P1 268, P6 268 |
| M23 | struct: the search's upper end moved past mid | P1 276, P6 276 |
| M26 | struct: the shelf left unsorted | P1 323, P3 325, P6 323 |
| M29 | solution: one potion fewer each | P1 360, P2 286, P6 360 |
| M31 | solution: a product one short of success enough | P1 66, P5 66, P6 66 |

P1 and P6 kill all seventeen, P4 three, P2 three, P3 three and P5 two.
P3, the potions reversed, fails where an arm leans on an order the
potions were never put in: left unsorted, in the ★ arm and the struct
arm, or the last one never tried. P4, a stronger spell never worse
off, fails where answers fall as spells grow: a count carried from
spell to spell, the spells walked in the order given, and the failing
potions counted instead. P2 fails where a count can leave `0..=m`: `m`
taken from the spells, a count never reset, one potion fewer than
none. P5, every spell and the success doubled, fails only where a
product is not compared as a product: strengths added, whose sum does
not double with the success, and a product one short of success
counted, a margin that does not double either.

Of the thirty-one, fourteen were not kept. The ★ arm's failing potions
counted (M2) fails as the sweep arm's (M19); its product compared with
success over spell rounded down (M5) as the table arm's strength needed
rounded down (M12); its every spell at least one potion (M6), the table
arm's spell past the strongest given one (M16), the sweep arm's walk
started below the strongest (M20) and the struct arm's strongest
potion never searched (M25) all fail alike, each wrong exactly where no
potion is strong enough, and none is kept; the product equal to success
not enough in the naive (M7), sweep (M18) and template (M27) arms, and
the struct arm's need one more when it divides (M24), as the ★ arm's
(M1); the table arm's top one short (M15) as its strongest potion never
enough (M13); and the template's potions left unsorted (M28) as the ★
arm's (M3). The naive arm's count of 20 at most (M11) and the
template's answers in reverse order (M30) fail in ways of their own,
past the three and two kept for their arms.

## Verification

Every arm prints the same output as `pairs.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 to 0.7 s, the template
the longest. The differential takes 7.2 s there and 0.6 s under `karac
__mir-llvm-run`: in its last 30 cases the table arm fills a table as
long as the strongest potion, up to 2 * 10^5 for P5, three times a
case.

## Benchmarks

The bench builds 10 cases of 10^5 spells and 10^5 potions from 1 to
10^5 once, case `c` with a success of `10^9 c + 7`, then makes 5
passes over all of them with the ★ arm in all five languages, pass `p`
adding `p` to each success. Every implementation prints `5 passes over
10 cases of 10^5 spells and potions: checksum 977746621`. Each sorts a
copy of the potions per call: C with `qsort` and a hand-written binary
search, Rust with `sort` and `partition_point`, Go with `sort.Slice` and
a hand-written search, Python with `sorted` and a hand-written search.

BENCHTAB
