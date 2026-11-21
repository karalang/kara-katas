# 2491. Divide Players Into Teams of Equal Skill

You are given a positive integer array `skill` of **even** length `n`
where `skill[i]` denotes the skill of the `i`th player. Divide the
players into `n / 2` teams of size `2` such that the total skill of each
team is **equal**.

The **chemistry** of a team is equal to the **product** of the skills of
the players on that team.

Return *the sum of the **chemistry** of all the teams, or return* `-1`
*if there is no way to divide the players into teams such that the total
skill of each team is equal.*

```
skill = [3,2,5,1,3,4]  ->  22
skill = [3,4]          ->  12
skill = [1,1,2,3]      ->  -1
```

**Constraints:** `2 <= skill.length <= 10^5`; `skill.length` is even;
`1 <= skill[i] <= 1000`.

Every team adds up to the total skill over the number of teams, so the
weakest player can only be matched with the strongest: anyone weaker
than the strongest leaves the weakest short. So, sorted, the players
pair from both ends inwards, and when a division exists it is that one,
and its chemistry with it. The approaches differ in how they find the
pairs.

## Approaches

| file | mechanism |
|---|---|
| `divide.kara` ★ | sorted, paired from both ends inwards, every pair asked for the first pair's sum, the products added up. O(n log n) |
| `divide_count.kara` | by counting: the sum each team needs from the total, which must be whole; the skills counted in an array of 1001, and each skill asked for as many partners as it has players. O(n + 1000) |
| `divide_greedy.kara` | online, by a `Map` of players still waiting: the sum known from the total, each player in input order matched with a waiting partner if one waits, and otherwise waiting. O(n) |
| `divide_heap.kara` | by two priority queues, one giving the weakest player left and one the strongest, each team one from each. O(n log n) |
| `divide_iter.kara` | iterators: sorted, the weaker half `zip`ped with the stronger half reversed, the sums asked by `all`, the products `sum`med. O(n log n) |
| `divide_solution.kara` | LeetCode's Rust template: `mut skill: Vec<i32>` in, `i64` out; `sort_unstable()`, the ends paired inwards, each product widened by `as i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's three examples and six
more; then 2000 random lists of 1 to 100 teams with skills to 1000 and
2000 with skills to 5, each built of pairs with one sum and every other
one spoiled by a skill changed by one, as a count of those that divide
and a checksum; then the constraints' largest, `10^5` players, all of
skill 1000, the pairs `i` and `1001 - i` 50 times over, random pairs,
and those spoiled. `divide.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random lists of 2 to
8 skills to 3 or to 6 against every way of cutting the players into
teams of two; every division of a list into equal teams had the same
chemistry, and the two agreed on every list.

`check` first reports 3 errors on the template: `struct Solution;`, the
`mut` before the parameter's name, and `Vec<i32>`. `karac fix` carries
it in one call, reporting 6 edits: `struct Solution {}`; the parameter
`skill: own Vec[i32]`, rebound `let mut skill = skill;` in the body;
the brackets; and `sort_unstable()` becomes `sort()`. The `as i64`
widenings of the products stand, since an `i32` product of two skills
is what they widen.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way of cutting the players into teams of two tried, by
a recursion that pairs the first player left with each other one that
makes the needed sum, the sum fixed by the first player's partner, and
the chemistry of the first division found, -1 if there is none. No list
is sorted. It checks 300 random lists of 2 to 10 players with skills to
3 or to 6, half of them built of pairs with one sum and half drawn
freely; then 20 of two players, and 40 of 12 built to divide, every
other one then spoiled. All 360 are drawn before any arm answers, and
248 of them divide.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | -1, or a chemistry between n / 2 and n / 2 times 1000 squared |
| P3 | the players in another order: the same answer |
| P4 | every skill doubled: -1 again, or four times the chemistry |
| P5 | two players of skill 1 and the sum less 1 added, when the list divides: the chemistry grows by the sum less 1 |
| P6 | each arm agrees with at least three of the other five |

P4 holds because doubling every skill doubles every team's sum alike
and multiplies every product by four. P5 holds because the new pair is
one more team of the needed sum, whose chemistry is `1 * (sum - 1)`,
and the division of the rest stands.

The differential prints `360 cases, 248 divide: checksum 562229052,
12960 checks over 6 arms: 0 failures` under every lane in Verification;
the checksum of the literal answers was checked against a Python
reading that builds the same cases and adds up the same sums. On a
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
| M1 | ★: the sum from the two weakest | P1 126, P5 215, P6 126 |
| M3 | ★: only half the teams formed | P1 326, P2 105, P5 101, P6 326 |
| M6 | ★: a mismatch answered 0 | P1 112, P2 112, P6 112 |
| M7 | count: the sum rounded down to even | P1 94, P4 94, P5 94, P6 94 |
| M8 | count: the counts never compared | P1 9, P4 18, P6 9 |
| M11 | count: skill 1 passed over | P1 135, P2 33, P4 135, P5 248, P6 135 |
| M12 | greedy: a match never taken out | P1 71, P3 1, P5 78, P6 71 |
| M13 | greedy: a matched player waiting too | P1 130, P3 30, P5 168, P6 130 |
| M16 | greedy: the partner waiting, not the player | P1 114, P4 2, P5 215, P6 114 |
| M17 | heap: both queues weakest first | P1 206, P5 215, P6 206 |
| M18 | heap: the first team's sum one over | P1 183, P4 7, P5 248, P6 183 |
| M20 | heap: one team short | P1 281, P2 97, P6 281 |
| M22 | iter: the stronger half not reversed | P1 71, P5 164, P6 71 |
| M23 | iter: any pair enough | P1 112, P6 112 |
| M24 | iter: sums added for products | P1 233, P4 248, P5 248, P6 233 |
| M28 | solution: the sum from the second strongest | P1 73, P5 156, P6 73 |
| M31 | solution: the first team never formed | P1 248, P2 97, P5 113, P6 248 |

P1 and P6 kill all seventeen, P5 thirteen, P4 six, P2 five, and P3
two.

Fourteen are not kept, and none survives. Four fail exactly as a kept
one: the ★ and greedy arms' sums added for products (M2, M14) as the
iter arm's (M24); and the ★ arm's neighbours paired and the iter arm's
sum from the two weakest (M5, M26) as the ★ arm's sum from the two
weakest (M1). Seven fail as one another, in three sets, none of whose
members could be kept beside the kept edits of their arms: the ★, iter
and template arms' never sorted (M4, M25, M27), which P3 sees on 34
cases since the input order then decides; the count arm's every pair
added twice and partner one short (M9, M10), wrong on all 248 lists that
divide; and the heap arm's and the template's mismatch answered with
the chemistry so far (M19, M29). The greedy arm's every match counted
twice, the heap arm's weaker squared and the template's one more for
every team (M15, M21, M30) fail in ways of their own, but their arms
already hold their kept edits.

One edit was replaced before this table was drawn: the count arm's sum
not asked to be whole, which survived every check. Without the test the
sum is rounded down, but then a skill and its partner add up to less
than the true sum, so the counts cannot all match on both sides of
every pair; whenever they do, the pairs add up to the total and the sum
was whole. It was replaced by the sum rounded down to even (M7).

## Verification

Every arm prints the same output as `divide.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.8 to 3.9 s, but for the heap arm's 17 s, and the differential 1.4 s; under `karac __mir-llvm-asan` the arms take 0.7 to 2.3 s and the differential 0.8 s; and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 20 lists of `10^5` skills once from its own generator,
each of pairs with one sum, from 500 to 1450, and shuffled; then makes
25 passes. Each sets one skill of every list to a value chosen by the
checksum so far, asks, and puts it back, so most answers are -1 found
partway through the sorted list, and folds the answer plus the pass
into the checksum. The bench uses the ★ arm in all five languages,
each sorting a fresh copy for every answer: C with `qsort`, Go with
`slices.Sort`. Every implementation prints `25 passes over 20 lists of
10^5: checksum 27956874`.

BENCHTAB
