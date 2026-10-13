# 475. Heaters

Winter is coming! During the contest, your first job is to design a
standard heater with a fixed warm radius to warm all the houses.

Every house can be warmed, as long as the house is within the heater's
warm radius range.

Given the positions of `houses` and `heaters` on a horizontal line,
return the minimum radius standard of heaters so that those heaters
could cover all houses.

Notice that all the heaters follow your radius standard, and the warm
radius will be the same.

```
houses = [1,2,3],   heaters = [2]    ->  1
houses = [1,2,3,4], heaters = [1,4]  ->  1
houses = [1,5],     heaters = [2]    ->  3
```

**Constraints:** `1 <= houses.length, heaters.length <= 3 * 10^4`;
`1 <= houses[i], heaters[i] <= 10^9`.

## Approaches

Every arm is `fn find_radius(houses: Vec[i64], heaters: Vec[i64]) ->
i64`, and borrows both lists. The radius has to reach each house's
nearest heater, so the answer is the largest of those distances.

| file | mechanism |
|---|---|
| `heaters.kara` ★ | the heaters sorted; for each house a binary search finds the first heater at or after it, and the nearest is that one or the one before. O((houses + heaters) × log heaters) |
| `heaters_pointers.kara` | both lists sorted; walking the houses left to right, the nearest heater never moves left, so one pointer moves on while the next heater is at least as close |
| `heaters_guess.kara` | binary search on the radius: a radius is enough when walking the sorted houses and heaters covers every house, and a larger radius covers more. O((houses + heaters) × log span) |
| `heaters_ordered.kara` | the heaters as keys of a `SortedMap[i64, i64]`; a house's `floor` and `ceiling` are its nearest heaters on each side |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

The library's `SortedSet` has no `floor` or `ceiling`, so the ordered
arm keeps the heaters in a `SortedMap` that maps each to itself.

Every arm prints the same 10 lines: the three LeetCode examples, a
house on its heater, both ends of the range with a heater on each, the
same two houses with one heater halfway, houses all left of the heaters
and in descending order, repeated houses between repeated heaters, a
house far from both heaters, and for 300 random cases (1 to 30
houses and 1 to 10 heaters at positions from 1 to 100, or from 1 to
10^9 in one case in ten, in any order and possibly repeated) the sum of
the radii and a checksum of them in order. `heaters.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases: 1 to 12 houses and 1 to 6 heaters at positions from
1 to 50, or from 1 to 1,000,000 in one case in five.

| | property |
|---|---|
| P1 | the arm's radius is the largest distance from a house to its nearest heater, every pair compared |
| P2 | the houses and the heaters in another order give the same radius |
| P3 | every position times k (1 to 5) plus d (0 to 999) gives k times the radius |
| P4 | one more heater never makes the radius larger, and one more house never makes it smaller |
| P5 | every position mirrored (x to span + 1 - x) gives the same radius |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, in about 1 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the heater after the house is counted one unit farther | P1 725, P3 574, P5 1410 |
| M2 | ★: the heater before the house is never looked at | the run stops: integer overflow |
| M3 | pointers: the pointer moves on only to a strictly closer heater | P1 78, P4 37, P5 116 |
| M4 | pointers: the houses are not sorted | P1 841, P2 435, P4 120, P5 995 |
| M5 | guess: a heater exactly a radius away does not cover the house | P1 598, P3 467, P4 25, P5 1159 |
| M6 | guess: the search stops one short of the smallest radius | P1 306, P3 409, P4 90 |
| M7 | ordered: the heater after the house counts only when none is at or before it | P1 583, P4 44, P5 691 |
| M8 | ordered: the radius is the last house's need, not the largest | P1 1070, P2 1043, P4 700 |

M2 can leave a house with no heater counted at all, at a distance of
`i64.MAX`, and P3 multiplies that by k, so the run stops on Kāra's
overflow check before it can print a count. M3 is the subtle one: it
fails only on two heaters at the same position, where the pointer never
gets past the first copy and the houses beyond are measured to it. P2
sees only M4 and M8, the two that depend on which house comes last; P3
sees only M1, M5 and M6, whose error is a fixed unit that scaling does
not scale. Two first drafts were equivalent and were replaced: "the
binary search finds the first heater after the house, not at it" (the
heater at the house is then the one before, at distance 0 all the same)
and "the floor is taken one position left of the house" (the heater at
the house is then the ceiling). A third draft, which compared `need ==
i64.MAX` in an `if`, did not parse when the kata was written; that
was B-2026-10-13-8.

## Verification

All four arms print the same output as `heaters.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends get the random cases wrong. Under
`karac run --interp`, LLJIT and legacy `karac build`, the ★, pointer
and guess arms print the nine fixed cases right and then a different
last line (`radii add up to 8613340262, checksum 311058431`): legacy
calls `next_random` twice for the bound of `for _ in 0..1 +
next_random(mut seed) % 30 { .. }`, so the lists it draws are not the
ones MIR and Python draw (with a counter for `next_random`, `for _ in
0..2 + next_random(mut seed) { v.push(next_random(mut seed)); }` runs 4
times on legacy and 3 on MIR). The ordered arm and the differential do
not type-check on legacy, which reads the keys `Map.floor` and
`Map.ceiling` return as `i64` and refuses `*before`. Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 30,000 houses (the
problem's most) at random positions from 1 to 10^9 once, then runs 200
rounds, each with 30,000 new heaters in the same range. Every
implementation prints `200 rounds of 30000 houses and 30000 heaters:
radii add up to 36425753, checksum 115276037`, the Kāra program under
`karac __mir-run` included (in 44 s).

Every mirror copies and sorts the heaters with the language's own sort
(`qsort` with a comparison function in C, which is why C is slower than
Rust here) and runs the same hand-written binary search per house. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.45 to 1.54 s |
| Rust (`rustc -O`) | 0.73 to 0.78 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.73 to 0.88 s |
| Go | 1.56 to 1.59 s |
| Python | 10.9 to 11.4 s |
| Kāra (`karac build`) | 0.81 to 0.94 s |
| Kāra (`karac build --mir`) | 0.77 to 0.82 s |

The legacy `karac build` builds and runs this program correctly (its
loops have constant bounds), so `bench.sh` is the
`scripts/new-bench.sh` output unchanged and times that build. The
`--mir` row is the v2 compiled backend, timed for comparison. Both Kāra
rows are timed at kara `b0b1557b39`. Under `karac __mir-llvm-run` the
program prints the same line in 4.8 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-8** (parser, fixed in kara `3ac940fe84`): a
  primitive's associated constant right before a block was misparsed.
  `if need == i64.MAX { .. }`, `while x < i64.MAX { .. }`, `match x ==
  i64.MAX { .. }` and `for i in 0..i64.MAX { .. }` were refused with
  "no associated function 'MAX' on type 'i64'" by `karac check`, the
  legacy interpreter and both MIR backends, while `let b = need ==
  i64.MAX;` and `if (need == i64.MAX) { .. }` worked. Met in mutant M7;
  the arms write `let mut nearest = i64.MAX;` and compare against a
  bound value, which always parsed.
