# 2212. Maximum Points in an Archery Competition

Alice and Bob are opponents in an archery competition. The competition
has set the following rules:

1. Alice first shoots `numArrows` arrows and then Bob shoots `numArrows`
   arrows.
2. The points are then calculated as follows:
   - The target has integer scoring sections ranging from `0` to `11`
     **inclusive**.
   - For **each** section of the target with score `k` (in between `0`
     to `11`), say Alice and Bob have shot `ak` and `bk` arrows on that
     section respectively. If `ak >= bk`, then Alice takes `k` points. If
     `ak < bk`, then Bob takes `k` points.
   - However, if `ak == bk == 0`, then **nobody** takes `k` points.

You are given the integer `numArrows` and an integer array `aliceArrows`
of size `12`, which represents the number of arrows Alice shot on each
scoring section from `0` to `11`. Now, Bob wants to **maximize** the
total number of points he can obtain.

Return *the array* `bobArrows` *which represents the number of arrows
Bob shot on **each** scoring section from* `0` *to* `11`. The sum of the
values in `bobArrows` should equal `numArrows`.

If there are multiple ways for Bob to earn the maximum total points,
return **any** one of them.

```
numArrows = 9, aliceArrows = [1,1,0,1,0,0,2,1,0,1,2,0]  ->  [0,0,0,0,1,1,0,0,1,2,3,1]   (47 points)
numArrows = 3, aliceArrows = [0,0,1,0,0,0,0,0,0,0,0,2]  ->  [0,0,0,0,0,0,0,0,1,1,1,0]   (27 points)
```

**Constraints:** `1 <= numArrows <= 10^5`; `aliceArrows.length ==
bobArrows.length == 12`; `0 <= aliceArrows[i], bobArrows[i] <=
numArrows`; `sum(aliceArrows[i]) == numArrows`.

Bob wins section k only by shooting one arrow more than Alice there, and
anything more is wasted, so a plan is a set of sections, costing
alice[k] + 1 arrows each; any arrows left over can go anywhere, here
section 0. With 12 sections there are 4096 sets to try. O(2^12 * 12).

Since any best plan is accepted, the arms may return different arrays.
Every harness therefore prints the points Bob's array wins, after
checking it is 12 counts of at least 0 adding up to his arrows (`-1`
otherwise), and that is what the arms and the mirror agree on.

## Approaches

| file | mechanism |
|---|---|
| `archery.kara` ★ | every mask `0..4096` priced bit by bit, the best Bob can afford kept, and his arrows laid out with the rest in section 0 |
| `archery_knapsack.kara` | a 0/1 knapsack with the roles turned: the table runs over sections and the 67 possible point totals, keeping the fewest arrows that reach each, so the 10^5 arrows never index it; the plan is read back from the table |
| `archery_search.kara` | a depth-first search from section 11 down, each section won or given up, the best plan kept through `mut ref` parameters, and a branch cut when every section below it could not beat the best |
| `archery_struct.kara` | a `struct Plan` of a mask, whose `wins`, `cost`, `points` and `arrows` (`ref self`) price it against Alice's arrows and lay it out; every plan made and the best affordable one kept |
| `archery_iter.kara` | the masks `filter`ed to those Bob can afford, the best by `max_by_key` on two closures, `cost` and `points`, and his arrows laid out by `map` |
| `archery_solution.kara` | LeetCode's Rust template: an `i32` and a `Vec<i32>` in, `Vec<i32>` out, the masks `0..(1u32 << 12)`, the cost summed into an `i32`, `points += k as i32`, and Bob's arrows from `vec![0; 12]`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one arrow, Alice's arrows all in section 11, all in section 0, and one
in each), each with Bob's points; then a checksum of 3000 random
contests, 2000 of 1 to 30 arrows and 1000 of up to 10^5; then the
constraints' largest, 10^5 arrows with Alice's spread evenly and nearly
all in section 11. `archery.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 16 edits: the five
`Vec<..>` to `Vec[..]`, `&&` to `and`, `vec![0; 12]` to `Vec.filled(12,
0)`, `struct Solution;` to `struct Solution {}`, the two `|&x|` to `|x|`
and `Solution::` to `Solution.`. The `0u32`, `1u32 << 12` and `mask &
(1 << k) != 0` stay as they are.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to shoot Bob's arrows into the 12 sections tried,
section by section, and the most points any of them wins; no masks, no
sets of sections. It checks 300 random contests of 1 to 6 arrows; then
30 with Alice's arrows all in section 0; then 30 with them all in one
section. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the points of the arm's arrows are the statement read literally |
| P2 | the arm's arrows are 12 counts of at least 0 adding up to Bob's |
| P3 | the points are at least those of the best section Bob can afford alone, and at most 66 |
| P4 | one more arrow each, Alice's in section 0: no fewer points |
| P5 | 11 more arrows each, Alice's in section 0: all 66 points |
| P6 | each arm agrees with at least three of the other five |

P5 holds because Bob then has alice[k] + 1 arrows for every section from
1 to 11, which is what winning all of them costs.

The differential prints `360 cases: checksum 829096245, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that tries
every multiset of sections for Bob's arrows with
`itertools.combinations_with_replacement`. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-seven edits to the differential, six to the ★ arm, five to the
knapsack and search arms, seven to the struct and iter arms and to the
template arm, each run under `karac __mir-llvm-run`. The interpreter
takes over two minutes on the differential, so the kept ones were run
again under `karac __mir-run` with a longer limit. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a section won by tying Alice | P1 360, P2 360, P3 360, P6 360 |
| M2 | ★: a plan costing all the arrows refused | P1 360, P3 55, P5 231, P6 360 |
| M5 | ★: a section worth one point more | P1 32, P6 32 |
| M8 | knapsack: the best points sought from 65 | P5 360 |
| M9 | knapsack: the read-back taking the section one up | P1 2, P2 2, P3 2, P4 4, P5 231, P6 2 |
| M11 | knapsack: the leftover dropped | P5 129 |
| M13 | search: the cut on the points so far alone | P1 118, P4 4, P6 118 |
| M15 | search: the search from section 10 | P1 311, P3 45, P5 360, P6 311 |
| M16 | search: a section won taking two arrows more | P1 360, P2 226, P3 226, P4 134, P5 360, P6 360 |
| M17 | struct: a section won by tying Alice | P1 360, P2 360, P3 360, P5 360, P6 360 |
| M20 | struct: a plan equal in points taken | P1 11, P6 11 |
| M33 | struct: a won section above 8 laid out with Alice's arrows alone | P1 359, P2 359, P3 359, P5 360, P6 359 |
| M23 | iter: the fewest points kept | P1 360, P3 360, P5 360, P6 360 |
| M26 | iter: the masks only to 2^10 | P1 354, P3 49, P5 360, P6 354 |
| M34 | iter: the points weighed as squares | P1 61, P4 1, P6 61 |
| M29 | solution: a section's points doubled | P1 104, P4 3, P6 104 |
| M36 | solution: section 11 never laid out | P1 311, P3 116, P4 6, P5 360, P6 311 |

P1 and P6 kill fifteen, P5 eleven, P3 ten, P4 six and P2 five. P1
misses two edits that only show with arrows to spare, which the small
random contests rarely leave: the knapsack arm's best sought from 65
(M8), which no contest of up to 6 arrows reaches, and its leftover
dropped (M11), since Bob's best plan there spends every arrow. P5 gives
Bob all 66 points' worth of arrows with Alice's extra in section 0, and
kills both. P2 kills the edits that lay out arrows not adding up to
Bob's: a won section at Alice's count, or at two more (M1, M9, M16,
M17, M33). P4 adds one arrow to each side, and kills the edits that
weigh the sections wrongly, whose plan can lose points as the contest
grows (M9, M13, M16, M29, M34, M36).

Of the thirty-seven, twenty were not kept. Sixteen are killed and fail
as a kept one does: a section won by tying Alice in the knapsack arm
and the template (M7, M27) as the ★ arm's M1; a plan costing all the
arrows refused in the knapsack and iter arms, and the search arm's
section won only with an arrow to spare (M10, M24, M12), as M2; the ★
arm's masks only to 2^11 (M3), which never wins section 11, as the
search from section 10 (M15); the leftover dropped in the ★, iter and
template arms (M4, M25, M30) as M11; the search arm's section 0 never
searched past 1 arrow and the struct arm's points one short (M14, M19)
as M8; and five as the struct arm's M17, every one laying out arrows
that do not add up to Bob's: the iter arm's tie with Alice and its cost
without section 0 (M22, M35), the struct arm's cost without section 11
(M32), and the template's adapter one arrow short and its sections won
with two more (M28, M31). Four survive, and each is equivalent: every
harness scores Bob's arrows, and any best plan is accepted. The ★ arm's
leftover put in section 11 (M6) can never win it, or the plan with
section 11 added would have been affordable and better. The struct
arm's plans from mask 2 (M18) skip only section 0 alone, worth 0
points. The struct arm's bit for a section read one up (M21) renames
the masks, all 4096 of which are still tried. The template's best kept
from a tie (M37) takes the last best plan instead of the first.

## Verification

Every arm prints the same output as `archery.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the knapsack and search arms take 15 s to 17 s,
the ★ arm and the template 35 s to 40 s, pricing 4096 masks bit by bit
for each contest, the iter arm 210 s and the struct arm 282 s, which
price every mask through closures and method calls, and the
differential 138 s.

## Benchmarks

The bench draws 3000 contests of up to 10^5 arrows once, Alice's shot
into the sections in random shares, then finds Bob's plan for each with
the ★ arm in all five languages; the checksum runs over all 12 counts of
every plan, so the languages must break ties alike, which they do by
keeping the first best mask. Every implementation prints `3000 contests:
checksum 342499004`.

BENCHTAB
