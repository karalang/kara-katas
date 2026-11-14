# 2126. Destroying Asteroids

You are given an integer `mass`, which represents the original mass of
a planet. You are further given an integer array `asteroids`, where
`asteroids[i]` is the mass of the `i`th asteroid.

You can arrange for the planet to collide with the asteroids in any
arbitrary order. If the mass of the planet is greater than or equal to
the mass of the asteroid, the asteroid is destroyed and the planet
gains the mass of the asteroid. Otherwise, the planet is destroyed.

Return `true` if all asteroids can be destroyed. Otherwise, return
`false`.

```
mass = 10, asteroids = [3, 9, 19, 5, 21]  ->  true
mass = 5,  asteroids = [4, 9, 23, 4]      ->  false
```

**Constraints:** `1 <= mass <= 10^5`; `1 <= asteroids.length <= 10^5`;
`1 <= asteroids[i] <= 10^5`.

The planet only grows, so whatever it can destroy now it can destroy
later, and taking the lightest asteroid left is never worse than any
other choice. Sorted, the asteroids are destroyed in order until one is
too heavy. The planet's mass reaches `10^5 + 10^10`, past an `i32`.
O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `asteroids.kara` ★ | a copy sorted with `sort`, then a `for` loop that stops at the first asteroid too heavy |
| `asteroids_heap.kara` | a `PriorityQueue` (smallest first) built in one step with `from`, popped lightest first, with an early answer once the planet outweighs the heaviest asteroid |
| `asteroids_counts.kara` | the asteroids counted by mass in a `SortedMap` through `entry().or_insert(0)`, each mass taken in order with all its copies at once |
| `asteroids_iter.kara` | the sorted copy folded with `try_fold`, the planet's mass carried in an `Option` that turns `None` at the first asteroid too heavy |
| `asteroids_struct.kara` | a `struct Planet { mass }` whose `absorb` (`mut ref self`) takes one asteroid and says whether the planet survived, driven by `all` |
| `asteroids_solution.kara` | LeetCode's Rust template: `mut asteroids: Vec<i32>` sorted in place with `sort_unstable`, the mass widened to `i64`, carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four
more (one asteroid as heavy as the planet, one heavier, doubling masses
just caught and just missed), each with its answer; then the cases
destroyed and a checksum over 3000 random cases, a mass of 1 to 20 and
1 to 12 asteroids of up to 10, 30 or 100 in turn; then the constraints'
largest, 100000 asteroids of 1 to 100000 shuffled against a mass of 1,
and 100000 of 100000 against 99999 and 100000. `asteroids.py` mirrors
the ★ arm and its output is byte-identical.

The template compares the planet with an asteroid as `m < a as i64`
and adds it as `m += a as i64`, with `m: i64` and `a: i32`. Both casts
are ones the operator makes itself, since a mixed-width operator widens
its narrower integer operand (design.md § Mixed-width operands), but
the `lossless_cast` lint saw only the one in the compound assignment:
`karac fix` dropped it and left the comparison's. That met a compiler
gap, fixed in karac with a test named for this kata (karac fa7746a0b2,
`tests/kata_2126_compare_cast_lint.rs`): a cast in a comparison is now
flagged as in an arithmetic operator, within one signedness only,
since a comparison refuses mixed signedness outright.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the asteroids may be hit in any order, so every set of them
the planet can destroy in some order is found, one asteroid at a time
from the empty set, and the answer is whether the set of all of them is
among those; no order is assumed. It checks 300 random cases, a mass of
1 to 10 and 1 to 8 asteroids of up to 5, 15 or 40 in turn; then 30 of
up to 10 asteroids that double, each perhaps one heavier, shuffled, so
that the planet is caught or missed by one; then 30 of up to 8
asteroids of one mass. All 360 are drawn before any arm answers; 182 of
them can be destroyed.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the asteroids in reverse order: the same answer |
| P3 | a planet one heavier: true if this one is; a planet as heavy as the heaviest asteroid: true |
| P4 | an asteroid as heavy as the planet and every asteroid together added at the front: the same answer |
| P5 | the planet and every asteroid twice as heavy: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 459737895, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
cases by the same search. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Forty edits to the differential, five to ten to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an asteroid as heavy as the planet not destroyed | P1 33, P3 74, P4 149, P6 33 |
| M5 | ★: half of each asteroid absorbed | P1 41, P4 141, P5 4, P6 41 |
| M6 | ★: the lightest asteroid skipped | P1 60, P4 174, P6 60 |
| M8 | heap: the early answer at the next asteroid | P1 58, P6 58 |
| M11 | heap: an asteroid one heavier destroyed | P1 51, P5 51, P6 51 |
| M34 | heap: the planet starting as heavy as the lightest | P1 102, P6 102 |
| M12 | counts: one copy of each mass absorbed | P1 2, P4 112, P6 2 |
| M14 | counts: the copies all weighed at once | P1 53, P3 74, P6 53 |
| M15 | counts: each mass absorbed before it is weighed | P1 178, P6 178 |
| M17 | iter: the planet starting empty | P1 182, P3 360, P6 182 |
| M20 | iter: a unit gained with each asteroid | P1 27, P5 14, P6 27 |
| M21 | iter: the asteroids never sorted | P1 70, P2 25, P4 112, P6 70 |
| M23 | struct: the planet taking the asteroid's mass | P1 152, P3 286, P4 30, P6 152 |
| M25 | struct: the heaviest first | P1 90, P4 92, P6 90 |
| M35 | struct: each asteroid absorbed twice over | P1 39, P6 39 |
| M30 | solution: the first asteroid dropped by the adapter | P1 47, P2 32, P4 47, P6 47 |
| M37 | solution: the planet halved by the adapter | P1 78, P3 146, P4 104, P6 78 |

P1 and P6 kill all seventeen, P4 nine, P3 five, P5 three and P2 two.
Every wrong answer is a wrong boolean, so P1 alone would do; the other
properties tell the kinds apart. P4 adds the one asteroid that only a
planet that has destroyed everything else can take, so it sees the
edits that end with the planet too light: asteroids skipped, counted
once, or taken out of order, and too little mass absorbed. P3 sees a
planet that a heavier start does not help, or that fails though it
outweighs everything (M1, M14, M17, M23, M37). P5 sees the edits whose
error does not double with the masses: a unit gained (M20), one
asteroid too heavy allowed (M11), half absorbed with its rounding (M5).
P2 sees only the edits that read the order given: no sort (M21) and
the first asteroid dropped (M30).

Of the forty, twenty-three were not kept. Two are equivalent: the heap
arm's early answer only once the planet is heavier than the heaviest
asteroid, or only once it is twice as heavy, either of which still
reaches the right answer by popping the rest. None survives. The rest
fail as a kept one does or were left out because their arms keep their
share. As M1: an asteroid as heavy as the planet refused, or the planet
one lighter, in the ★, counts, iter and struct arms. As M6: the struct
arm keeping its lightest asteroid back. As M8: the heap arm taking the
lightest for the heaviest or absorbing the heaviest every time, and the
struct arm destroying one asteroid as enough. As M11: the heap arm's
planet one heavier, and the Rust adapter's. As M17: the heap arm's early
answer false. As M20: the Rust arm gaining a unit with each asteroid. As
M21: no sort in the ★ and Rust arms. As M25: the heaviest first in the
★ and heap arms, the planet never growing in the ★ and iter arms, and
the Rust arm's planet as heavy as its heaviest asteroid. As M35: the
counts arm counting each mass once too often. Killed with its own
checks but left out: none.

## Verification

Every arm prints the same output as `asteroids.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 s to 0.9 s, except the counts
arm, 5.3 s, nearly all of it the 100000 distinct masses inserted into
the `SortedMap` in random order, each insert shifting the sorted array
behind it; compiled it takes 0.2 s. The differential takes 0.32 s.

`karac fix` carries the template in three rounds of 10, 3 and 1 edits:
Rust's spellings (`mut asteroids: Vec<i32>` to `asteroids: own
Vec[i32]` with `let mut asteroids = asteroids;` in the body, `<..>` to
`[..]`, `struct Solution;` to `struct Solution {}`, the adapter's `&Vec`
to `ref Vec`, `Solution::` to `Solution.`, `|&a|` to `|a|`); then
`sort_unstable` to `sort` and the two `as i64` on `a` dropped; then the
`ref` dropped from the adapter's parameter, which borrows already. The
`let mut m = mass as i64;` stays: with no type written, the cast is what
makes `m` an `i64`.

## Benchmarks

The bench builds 20 arrays of 100000 asteroids of 1000 to 100000 once,
then solves every array 10 times against a mass of 500 to 1499, one
asteroid set to 1 to 2000 before each solve so that no solve repeats
one before, with the ★ arm in all five languages; each solve sorts a
copy. Every implementation prints `200 solves: 173 destroyed, checksum
506617160`.

BENCHTAB
