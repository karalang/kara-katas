# 2171. Removing Minimum Number of Magic Beans

You are given an array of **positive** integers `beans`, where each
integer represents the number of magic beans found in a particular magic
bag.

**Remove** any number of beans (**possibly none**) from each bag such
that the number of beans in each remaining **non-empty** bag (still
containing **at least one** bean) is **equal**. Once a bean has been
removed from a bag, you are **not** allowed to return it to any of the
bags.

Return *the **minimum** number of magic beans that you have to remove*.

```
beans = [4, 1, 6, 5]   ->  4
beans = [2, 10, 3, 2]  ->  7
```

**Constraints:** `1 <= beans.length <= 10^5`; `1 <= beans[i] <= 10^5`.

Every bag left keeps as many beans as the smallest bag left, so with the
bags sorted each one in turn is tried as that smallest: the bags before
it are emptied and the ones from it on are cut down to it, which keeps
`beans[i] * (n - i)` beans. The answer is the total less the most any
choice keeps. O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `beans.kara` ★ | a sorted copy of the bags, the total and the most kept by `sorted[i] * (n - i)` in one walk |
| `beans_count.kara` | the bags counted by size in a `SortedMap` (`entry`, `or_insert`), walked from the smallest size up with the bags not yet passed; no sort of the bags |
| `beans_prefix.kara` | the removal itself from prefix sums of the sorted bags: `P[i]` emptied before the choice, and what the bags after it hold above it, `P[n] - P[i] - sorted[i] * (n - i)`; the least |
| `beans_struct.kara` | a `struct Row` of the bags in order and their total, made `from` the bags it owns (`own`), asked what it `keeps` with a bag as the smallest left, and its `removal` |
| `beans_iter.kara` | the sorted bags `enumerate`d and `map`ped to what each choice keeps, their `max`, taken from their `sum` |
| `beans_solution.kara` | LeetCode's Rust template: `mut beans: Vec<i32>`, `sort_unstable()`, `\|&b\| b as i64`, `0i64`, `for (i, &b) in beans.iter().enumerate()`, `i as i64`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one bag, every bag the same, one bag far larger than the rest, and bags
rising one at a time), each with its removal; then the total and a
checksum over 2000 random rows of 1 to 20 bags of up to 10, 1000 or
10^5 beans in turn; then the constraints' largest, 10^5 bags at random
and 10^5 full bags but one. `beans.py` mirrors the ★ arm and its output
is byte-identical.

`karac fix` carries the template in two rounds of 11 and 4 edits: Rust's
spellings (`mut beans: Vec<i32>` to `beans: own Vec[i32]` and a `let mut
beans = beans;` at the top of the body, each `Vec<..>` to `Vec[..]`, the
closures' and the `for` pattern's `&b` to `b`, `struct Solution;` to
`struct Solution {}`, `Solution::` to `.`); then `sort_unstable()` to
`sort()`, `0i64` to `0`, and the `as i64` on `beans.len()` and on `i`
dropped, since Kāra's lengths and indices are `i64` already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every level from 0 to the largest bag, each bag below it
emptied and each at or above it cut down to it, and the beans taken
counted; the least. No sort and no running best. It checks 300 random
rows of 1 to 12 bags of up to 2, 10 or 1000 beans in turn; then 30 rows
of equal bags but one; then 30 of bags that all differ, rising or
falling. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the removal is the statement read literally |
| P2 | the bags turned by one place: the same removal |
| P3 | every bag three times as full: three times the removal |
| P4 | a bag added as full as the largest: the removal no less, and less than the largest more |
| P5 | the removal at most the total less the largest bag, and at most the total less the smallest times the bags |
| P6 | each arm agrees with at least three of the other five |

P3 holds since every level for the tripled bags is three times a level
for the bags, and takes three times the beans. P4 holds since every
level takes from the added bag what it takes from no other, at least 0
and at most the largest less 1. P5 holds since keeping only the largest
bag, or cutting every bag to the smallest, is a choice.

The differential prints `360 rows: checksum 951940701, 12960 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers was checked against a Python reading of the same
rows. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, four to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the bags never sorted | P1 279, P2 292, P5 240, P6 279 |
| M2 | ★: one bag fewer kept | P1 360, P5 207, P6 360 |
| M3 | ★: the first bag left out of the total | P1 360, P5 55, P6 360 |
| M5 | count: the bags left never fewer | P1 321, P5 321, P6 321 |
| M6 | count: a size's bags passed before it is tried | P1 360, P4 39, P5 230, P6 360 |
| M7 | count: each size one bag | P1 147, P5 90, P6 147 |
| M9 | prefix: the emptied bags never counted | P1 321, P6 321 |
| M25 | prefix: every bag counted one bean short | P1 360, P3 360, P4 116, P5 132, P6 360 |
| M31 | prefix: the emptied bags counted twice | P1 233, P5 31, P6 233 |
| M15 | struct: the smallest bag never the smallest left | P1 106, P5 106, P6 106 |
| M27 | struct: each bag kept one bean short | P1 360, P3 360, P4 12, P5 182, P6 360 |
| M28 | struct: the removal never under one | P1 39, P3 39, P5 39, P6 39 |
| M18 | iter: the least kept | P1 330, P4 230, P5 326, P6 330 |
| M29 | iter: the total a bean more for each bag | P1 360, P3 360, P4 49, P5 191, P6 360 |
| M30 | iter: each choice kept its place fewer | P1 233, P3 226, P5 24, P6 233 |
| M24 | solution: the last choice kept | P1 306, P4 360, P5 206, P6 306 |
| M23 | solution: the adapter's bags halved | P1 321, P3 275, P6 321 |

P1 and P6 kill all seventeen, P5 fifteen, P3 six, P4 six and P2 one.
P5 bounds the removal by two choices that are always open, keeping only
the largest bag and cutting every bag to the smallest; it misses the
prefix arm's emptied bags never counted (M9), which answers too little,
and the template's bags halved (M23), whose answer is a right one for
other bags. P3 triples every bag and sees an edit that counts a bean or
a place where a right answer counts beans: a bean short or over (M25,
M27, M29), a place less (M30), a floor of one (M28), and the halving
that rounds (M23). P4 adds a bag as full as the largest, and sees an
edit whose answer at the largest level is off: the last choice kept
(M24), the least kept (M18), a size's bags passed early (M6), and the
bean short or over (M25, M27, M29). P2 turns the bags by one place, and
only an unsorted walk (M1) cares where a bag stands.

Of the thirty-one, fourteen were not kept, none of them equivalent. The
six arms share a walk, and thirteen fail as a kept one does: the
prefix, struct, iter and template arms never sorting, as M1; the
prefix, struct and iter arms keeping one bag fewer, as M2; the struct
and template arms' total without the first bag, as M3; the ★ arm's last
choice kept, as M24; the count arm's sizes walked from the largest and
the iter arm's bags counted from the largest, as M5; and the prefix
arm's best started at none taken, as M9. The prefix arm never trying
the largest bag as the smallest left (M11) runs `i64.MAX` into an
overflow on a row of one bag.

## Verification

Every arm prints the same output as `beans.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 s to 0.8 s, but for the count
arm, 2.3 s, which builds a `SortedMap` of the sizes for the largest
rows; the differential takes 0.5 s.

## Benchmarks

The bench builds one row of 400000 bags once, each of 1 to 10^5 beans
at random; then solves 100 windows of 100000 bags, each at a random
start, so that no solve repeats one before, with the ★ arm in all five
languages: each copies its window and sorts it. C works over a pointer
and a length, the others over a slice. Every implementation prints `100
solves: checksum 462156428`.

BENCHTAB
