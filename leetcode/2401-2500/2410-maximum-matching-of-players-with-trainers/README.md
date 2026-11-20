# 2410. Maximum Matching of Players With Trainers

You are given a **0-indexed** integer array `players`, where `players[i]`
represents the **ability** of the `i`th player. You are also given a
**0-indexed** integer array `trainers`, where `trainers[j]` represents
the **training capacity** of the `j`th trainer.

The `i`th player can **match** with the `j`th trainer if the player's
ability is **less than or equal to** the trainer's training capacity.
Additionally, the `i`th player can be matched with at most one trainer,
and the `j`th trainer can be matched with at most one player.

Return *the **maximum** number of matchings between* `players` *and*
`trainers` *that satisfy these conditions.*

```
players = [4,7,9], trainers = [8,2,5,8]   ->  2
players = [1,1,1], trainers = [10]        ->  1
```

**Constraints:** `1 <= players.length, trainers.length <= 10^5`; `1 <=
players[i], trainers[j] <= 10^9`.

A trainer that can hold a stronger player can hold any weaker one, so
matching the weakest players to the weakest trainers that fit them is
never worse than any other matching.

## Approaches

| file | mechanism |
|---|---|
| `match.kara` ★ | two sorted lists: walking the trainers upward, each takes the weakest player not yet matched if it is strong enough. O(n log n + m log m) |
| `match_sorted.kara` | a `SortedMap` of trainers counted by capacity: each player, weakest first, takes the map's `ceiling` and lowers its count. O((n + m) log m) |
| `match_desc.kara` | strongest first: both sorted downward by `sort_by` with `b.cmp(a)`, the strongest trainer left taking the strongest player it can. O(n log n + m log m) |
| `match_binary.kara` | binary search on the answer: k matches exist exactly when the k weakest players fit the k strongest trainers paired in order. O((n + m) log(n + m)) |
| `match_iter.kara` | iterators: the ★ walk as a `fold` over the sorted trainers carrying the count matched. O(n log n + m log m) |
| `match_solution.kara` | LeetCode's Rust template: `mut` parameters sorted in place by `sort_unstable`, two indexes walked in a `while`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one player
and one trainer, too weak and then strong enough; every player stronger
than every trainer; `10^5` of each up to `10^9`; `10^5` players against
`5 * 10^4` trainers drawn higher; then 2000 random cases of up to 20
players and 20 trainers from 1 to 30, with a checksum and the total of
the answers. `match.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 20000 random cases of up
to 6 of each against trying every matching.

`check` first reports 8 errors on the template, and `karac fix` carries
it in one call, reporting 15 edits: `mut players: Vec<i32>` and `mut
trainers: Vec<i32>` written `players: own Vec[i32]` and `trainers: own
Vec[i32]` with a `let mut` rebinding of each at the body's start; the
`mut` of `(mut i, mut j)` moved before the whole pattern; `&&` written
`and`; `struct Solution;` given its braces; `sort_unstable` written
`sort`; and the wrapper's widening `as i64` removed. `i as i32` stands
as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to give each player a different trainer or none,
by backtracking, a player only to a trainer of at least its ability, and
the most players placed. No sorting. It checks 300 random cases of 1 to
8 players and 1 to 8 trainers from 1 to 12, which the literal reading
answers; then 30 of up to 400 of each up to `10^9`; then 30 of up to
3000 of each up to 50. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 8 players and 8 trainers, the answer is the literal reading's |
| P2 | up to 400 of each, the answer is the players less the worst shortfall, over every ability `v`, of trainers of at least `v` against players of at least `v` |
| P3 | players and trainers swapped, every value `v` written `m + 1 - v` for `m` the largest: the same answer |
| P4 | both lists reversed: the same answer |
| P5 | one more trainer as strong as the strongest player: one more match, unless every player was already matched |
| P6 | each arm agrees with at least three of the other five |

P2 is Hall's theorem for this graph: the players of at least `v` can
only use the trainers of at least `v`, so the worst such shortfall goes
unmatched, and no other set of players is worse. P3 holds because `p <=
t` exactly when `m + 1 - t <= m + 1 - p`, P4 because the order given
does not matter, and P5 because the new trainer can hold any player, so
an unmatched one, if there is one, gains it.

The differential prints `360 cases: checksum 725060871, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and backtracks the same way. On a failure it prints the
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
| M4 | ★: every trainer matched | P1 104, P2 120, P6 128 |
| M5 | ★: the strongest player left tried | P1 213, P2 243, P3 256, P6 273 |
| M6 | ★: the weakest trainer skipped | P1 107, P2 113, P3 223, P6 123 |
| M7 | sorted: the strongest trainer below taken | P1 237, P2 263, P3 238, P5 223, P6 281 |
| M10 | sorted: the players never sorted | P1 102, P2 124, P3 215, P4 151, P5 106, P6 142 |
| M11 | sorted: each capacity counted once | P1 46, P2 46, P3 57, P5 82, P6 76 |
| M12 | desc: a trainer needing more than the ability | P1 68, P2 68, P5 72, P6 98 |
| M13 | desc: the trainers sorted upward | P1 216, P2 246, P3 256, P5 306, P6 276 |
| M15 | desc: the players sorted upward | P1 120, P2 150, P5 137, P6 180 |
| M19 | binary: the full count never tried | P1 196, P2 210, P5 157, P6 232 |
| M20 | binary: a failed count lowering the bound by two | P1 16, P2 19, P5 28, P6 22 |
| M21 | binary: the weakest pair unchecked | P1 32, P2 35, P3 57, P6 35 |
| M23 | iter: the trainers never sorted | P1 79, P2 103, P3 115, P4 118, P6 130 |
| M24 | iter: each match counted twice | P1 234, P2 260, P3 201, P5 150, P6 283 |
| M25 | iter: the first player taken as matched | P1 103, P2 111, P3 223, P6 121 |
| M29 | solution: the players never sorted | P1 161, P2 190, P3 249, P4 212, P6 220 |
| M31 | solution: the trainers walked returned | P1 176, P2 200, P3 296, P5 72, P6 220 |

P1, P2 and P6 kill all seventeen, P3 twelve, P5 ten, and P4 three. P4
reverses both lists, so it catches only a mutant whose answer depends
on the order they come in: a list never sorted (M10, M23, M29).

Of the thirty-one, fourteen were not kept, each failing the same checks
as a kept one or, for five, left over: the players never sorted in the
★ and iter arms (M1, M26) as the template's (M29); the trainers never
sorted in the ★ arm and template (M2, M28) as the iter arm's (M23); a
trainer needing more than the ability in the ★, iter and template arms
(M3, M22, M27), and the binary arm's pair of equals refused (M17), as
the desc arm's (M12); and every trainer of a capacity removed at once
(M9) as the sorted arm's each capacity counted once (M11). The sorted
arm's trainer's count never lowered (M8), the desc arm's trainer used
again (M14) and strongest player skipped (M16), the binary arm's
weakest trainers tried (M18) and the template's strongest trainer never
tried (M30) fail apart from every kept one, and were left out because
those arms keep their share already.

## Verification

Every arm prints the same output as `match.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.3 to 4.1 s, except the sorted
arm at 26.9 s. The differential takes 8.4 s there, 1.8 s under `karac
__mir-llvm-asan` and 0.8 s under `karac run`.

## Benchmarks

The bench builds 10 cases of `10^5` players up to `10^9` and `10^5`
trainers, case `i`'s from `1 + 10^7 i` to `9 * 10^8 + 10^7 i`, once from
the harness's generator, then makes 5 passes, answering every case and
folding each answer plus the pass into the checksum, with the ★ arm in
all five languages. Every implementation prints `5 passes over 10 cases
of 10^5 players and trainers: checksum 385876473`. Each copies both
lists and sorts the copies: Kāra and Rust with `sort`, Go with
`slices.Sort`, Python with `sorted`, and C with `qsort` through a
comparison function, which pays a call per comparison; C and Go were
both measured slower than Kāra and Rust here.

BENCHTAB
