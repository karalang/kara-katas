# 2214. Minimum Health to Beat Game

You are playing a game that has `n` levels numbered from `0` to `n - 1`.
You are given a **0-indexed** integer array `damage` where `damage[i]` is
the amount of health you will lose to complete the `i`th level.

You are also given an integer `armor`. You may use your armor ability
**at most once** during the game on **any** level which will protect you
from **at most** `armor` damage.

You must complete the levels in order and your health must be **greater
than** `0` at all times to beat the game.

Return *the **minimum** health you need to start with to beat the game.*

```
damage = [2, 7, 4, 3], armor = 4  ->  13
damage = [2, 5, 3, 4], armor = 7  ->  10
damage = [3, 3, 3],    armor = 0  ->  10
```

**Constraints:** `n == damage.length`; `1 <= n <= 10^5`; `0 <=
damage[i] <= 10^5`; `0 <= armor <= 10^5`.

Health only falls, so it is enough for it to end above 0: the start must
exceed all the damage taken. The armor takes the most off on the level
that hurts most, so the answer is the total less the smaller of the
largest level and the armor, plus 1. The total reaches 10^10, past
`i32`. O(n).

## Approaches

| file | mechanism |
|---|---|
| `health.kara` ★ | one pass summing the damage and keeping the largest level, then `total - worst.min(armor) + 1` |
| `health_levels.kara` | the total first, then the armor tried on every level in turn and the cheapest kept |
| `health_search.kara` | a binary search over the starting health, each guess played level by level with the most health left before and after the armor is used; a guess wins when it ends above 0. O(n log(sum)) |
| `health_struct.kara` | a `struct Game` of the damage so far and the worst level, `play` (`mut ref self`) taking one level and `health` (`ref self`) giving the answer |
| `health_iter.kara` | the total by `sum`, the worst level by `max().unwrap_or(0)`, and the armor's saving by `min` |
| `health_solution.kara` | LeetCode's Rust template: a `Vec<i32>` and an `i32` in, `i64` out, the total by `sum::<i64>()` over the damage cast `as i64`, the worst level by `*damage.iter().max().unwrap()`, and the saving by `std::cmp::min`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (one level, no damage at all, armor beyond every level, and the
largest level twice), each with its answer; then a checksum of 3000
random games of 1 to 30 levels, the damage and the armor up to 10, 1000
and 10^5 in turn; then the constraints' largest, 10^5 levels of 10^5
damage with 10^5 armor and 10^5 random levels with none, both past
`i32`. A number up to 10^5 is drawn from two draws, since one stops at
32767. `health.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 14 edits: `Vec<..>` to
`Vec[..]` three times, `sum::<i64>()` to `sum()` with the type moved to
the binding, `let total: i64`, `std::cmp::min` to the prelude's `min`
and the `as i64` after it dropped, since an `i32` widens to `i64` on
its own, the two `|&d|` to `|d|`, `struct Solution;` to `struct
Solution {}` and `Solution::` to `Solution.`. The
`*damage.iter().max().unwrap()` stays as it is.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every starting health from 1 upward tried, with the armor
worn on each level in turn or on none, the game played level by level
and lost as soon as health is not above 0; the first health that wins
any way. No sum and no largest level. It checks 300 random games of 1 to
8 levels, the damage and the armor up to 3, 10 and 20 in turn; then 30
with no armor; then 30 with armor beyond every level. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the health is the statement read literally |
| P2 | it is at least 1, and from the total damage less the armor, plus 1, to the total damage plus 1 |
| P3 | the levels in reverse order: the same health |
| P4 | a level of no damage added at the end: the same health |
| P5 | every damage and the armor doubled: twice the health, less 1 |
| P6 | each arm agrees with at least three of the other five |

P5 holds because doubling every damage and the armor doubles what the
health must exceed, so the least start goes from h to 2(h - 1) + 1.

The differential prints `360 cases: checksum 70377040, 12960 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers was checked against a Python reading that tries
each starting health and armored level over `itertools.accumulate` of
the damage taken. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and to the
search arm, five to each of the other Kāra arms and to the template arm,
each run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen
are kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the 1 health to end on left out | P1 360, P2 304, P5 360, P6 360 |
| M3 | ★: the worst level taken as the last | P1 107, P3 166, P4 256, P6 107 |
| M4 | ★: the levels above 15 not summed | P1 70, P2 70, P5 178, P6 70 |
| M7 | levels: the cheapest starting at 0 | P1 330, P2 317, P6 330 |
| M10 | levels: the first level never armored | P1 56, P3 50, P6 56 |
| M11 | levels: the armor one short | P1 213, P5 213, P6 213 |
| M12 | search: ending on 0 health a win | P1 330, P2 274, P5 330, P6 330 |
| M15 | search: a winning guess cut one below | P1 123, P2 95, P5 174, P6 123 |
| M17 | search: the level taken twice before the armor | P1 285, P6 285 |
| M19 | struct: the total only the last level | P1 309, P2 301, P3 278, P4 316, P6 309 |
| M21 | struct: a new game's worst level 5 | P1 42, P2 18, P5 37, P6 42 |
| M22 | struct: a level of no damage taking 1 | P1 134, P2 45, P4 360, P5 134, P6 134 |
| M23 | iter: the least level armored | P1 214, P4 186, P6 214 |
| M25 | iter: the saving the larger of level and armor | P1 328, P2 282, P6 328 |
| M26 | iter: the worst of the first four levels | P1 11, P3 28, P6 11 |
| M27 | solution: the adapter's damage capped at 15 | P1 63, P2 61, P5 184, P6 63 |
| M31 | solution: the worst level taken as the first | P1 121, P3 166, P6 121 |

P1 and P6 kill all seventeen, P2 ten, P5 eight, P3 five and P4 four.
P5 doubles every damage and the armor, so it kills the edits that hold
a fixed number apart from the scale: the 1 to end on, a cut at 15 or at
5, the armor one short, a level of no damage taking 1 (M1, M4, M11,
M12, M15, M21, M22, M27). P3 reverses the levels and kills the five
edits that treat one position apart: the first or last level, or the
first four (M3, M10, M19, M26, M31). P4 adds a level of no damage at the
end, which becomes the last level and the least, so it kills the edits
that read either (M3, M19, M22, M23).

Of the thirty-one, fourteen were not kept, and every one is killed;
none crashes, none differs between the backends, and none survives.
Four fail as a kept one does: the ★ arm's and the template's saving the
larger of level and armor (M2, M28) as the iter arm's M25, the search
arm's armor only on the last level (M13) as the ★ arm's M3, and the
struct arm's worst level kept as the least (M18) as the search arm's
M17, since both answer the total plus 1 whatever the armor: the least
of levels and 0 is always 0, and a level taken twice before the armor
leaves the armored health below the unarmored. Six fail in pairs and neither of a pair is kept: the armor taken
as unlimited in the ★ and levels arms (M5, M9), the armor at half in
the struct arm and the template's adapter (M20, M29), and the first
level not summed in the iter arm and the template (M24, M30). Four fail
their own way and are left out for the count of three: the ★ arm's
worst level starting at 1 (M6), the levels arm's armor worn on every
level (M8), and the search arm's top the total damage and its armor
giving health back (M14, M16).

## Verification

Every arm prints the same output as `health.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 s to 0.7 s, the search arm
3.6 s, and the differential 0.3 s.

## Benchmarks

The bench draws 100 games of 10^5 levels once, the damage up to 10,
1000 and 10^5 in turn, then punches each game 20 times, one level
hurting by one more each time, answering it after each punch for an
armor of 0 to 95000 with the ★ arm in all five languages; the punch
keeps a compiler from answering the 20 armors off one pass. Every
implementation prints `100 games of 10^5, 20 armors: checksum
606701484`.

BENCHTAB
