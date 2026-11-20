# 2383. Minimum Hours of Training to Win a Competition

You are entering a competition, and are given two **positive** integers
`initialEnergy` and `initialExperience` denoting your initial energy and
initial experience respectively.

You are also given two **0-indexed** integer arrays `energy` and
`experience`, both of length `n`.

You will face `n` opponents **in order**. The energy and experience of
the `i`th opponent is denoted by `energy[i]` and `experience[i]`
respectively. When you face an opponent, you need to have both
**strictly** greater experience and energy to defeat them and move to
the next opponent if available.

Defeating the `i`th opponent **increases** your experience by
`experience[i]`, but **decreases** your energy by `energy[i]`.

Before starting the competition, you can train for some number of hours.
After each hour of training, you can **either** choose to increase your
initial experience by one, or increase your initial energy by one.

Return *the **minimum** number of training hours required to defeat all*
`n` *opponents*.

```
initialEnergy = 5, initialExperience = 3, energy = [1,4,3,2], experience = [2,6,3,1]  ->  8
initialEnergy = 2, initialExperience = 4, energy = [1], experience = [3]              ->  0
```

**Constraints:** `n == energy.length == experience.length`;
`1 <= n <= 100`; `1 <= initialEnergy, initialExperience, energy[i],
experience[i] <= 100`.

Energy and experience are trained apart, and neither depends on the
other. Energy only falls, so the start must be above the sum of all the
opponents' energy. Experience only grows, so it is walked through the
opponents, trained up to one above each one it does not already beat.

## Approaches

| file | mechanism |
|---|---|
| `training.kara` ★ | the energy trained to one above the opponents' sum, the experience walked through the opponents and trained up to one above each it does not beat. O(n) |
| `training_each.kara` | hour by hour: each opponent met in turn, an hour of energy trained while the energy left does not beat theirs and one of experience while the experience does not. O(n + the hours) |
| `training_search.kara` | binary search: energy and experience each the least start, between none and the opponents' sum plus one, that beats every opponent in turn. O(n log(sum)) |
| `training_prefix.kara` | the largest shortfall: before each opponent the energy left and the experience gained so far, each trained by its largest shortfall over all the opponents. O(n) |
| `training_iter.kara` | iterators: the energy from the opponents' `sum`, the experience by a `fold` carrying what it has and the hours trained so far |
| `training_solution.kara` | LeetCode's Rust template: the energy from an `i32` sum, the experience walked with `for &e in &experience`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; one
opponent met exactly, a tie on both; 100 opponents of 100 from a start
of 1 and 1, and of 100 and 100; then 3000 random contests of 1 to 100
opponents of 1 to 100, starting from 1 to 100, with a checksum, the
total hours and how many need none. `training.py` mirrors the ★ arm and
its output is byte-identical, and the mirror was checked on 3000 random
contests of up to 6 opponents of up to 10 against every split of every
number of hours, played out.

`check` first reports 12 errors on the template, and `karac fix` carries
it in one call, reporting 19 edits: `struct Solution;` given its braces;
`Vec<..>` its brackets; `for &e in &experience` written `for e in ref
experience`; the `&` of the wrapper's `|&v|` dropped; `Solution::`
written with a dot; and the wrapper's `as i64` on the `i32` answer
dropped, as a cast that widens anyway. The `let total: i32 =
energy.iter().sum();`, `.max(0)` and the `as i32` casts stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number of hours from none upward, and every split of
them between energy and experience, the contest played out, until one
split wins. No shortfall worked out. It checks 300 random contests of 1
to 6 opponents of 1 to 10, starting from 1 to 10, which the literal
reading answers; then 30 of up to 100 opponents of up to 100, starting
from up to 100; then 30 of up to 100 opponents of 1 to 3, starting from
1 to 3, where ties are many and a tie loses. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | up to 6 opponents of up to 10, the answer is the literal reading's |
| P2 | at least the energy short of one above the opponents' sum, and at most that plus the experience short of one above the strongest |
| P3 | the answer's hours, the energy trained to one above the sum and the rest to experience, win the contest |
| P4 | one hour fewer loses, whether the energy or the experience goes without it |
| P5 | each start one more: the same answer or up to two less |
| P6 | each arm agrees with at least three of the other five |

P2's upper bound holds because experience one above the strongest
opponent beats every one of them whatever it gains. P3 and P4 together
say the answer's hours are enough and one fewer is not, whichever of
the two goes short. P5 holds because
a start one more saves at most the one hour it stands for.

The differential prints `360 cases: checksum 954176649, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and plays out every split of every number of hours. On a
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
| M2 | ★: a tie in experience a win | P1 43, P3 56, P5 25, P6 56 |
| M4 | ★: the experience never gained | P1 91, P4 119, P6 119 |
| M5 | ★: the energy trained even when enough | P1 68, P2 62, P3 44, P6 70 |
| M7 | each: energy trained to two above | P1 232, P2 175, P4 290, P6 290 |
| M8 | each: the energy never spent | P1 206, P2 252, P3 231, P6 264 |
| M10 | each: each hour of experience counted twice | P1 116, P2 107, P4 146, P5 123, P6 146 |
| M12 | search: the search stepping two past a loss | P1 188, P2 162, P4 238, P5 57, P6 238 |
| M13 | search: a tie a win | P1 241, P2 192, P3 172, P6 299 |
| M15 | search: the energy searched from the experience start | P1 230, P2 244, P3 85, P4 139, P6 276 |
| M17 | prefix: the energy shortfall before the opponent's spend | P1 218, P2 214, P3 196, P6 276 |
| M19 | prefix: the experience shortfalls summed | P1 23, P4 31, P5 29, P6 31 |
| M20 | prefix: the energy shortfall at least one | P1 82, P2 78, P4 84, P6 84 |
| M24 | iter: a tie in experience a win | P1 116, P3 146, P6 146 |
| M25 | iter: the fold from no experience | P1 300, P2 310, P4 360, P6 360 |
| M26 | iter: the energy never trained | P1 218, P2 264, P3 243, P6 276 |
| M29 | solution: experience trained to two above | P1 8, P3 13, P6 13 |
| M30 | solution: the first opponent's energy left out | P1 218, P2 211, P3 195, P6 276 |

P1 and P6 kill all seventeen, P2 twelve, P3 ten, P4 eight and P5 four.
P3 and P4 split the edits between them: P3, the answer's hours win,
fails the ones that answer too few, as a tie counted a win (M2, M13,
M24), the energy never spent or never trained (M8, M26) and experience
trained past what it counts (M29); P4, one hour fewer loses, fails the
ones that answer too many, as the experience never gained (M4), energy
trained to two above (M7), each hour of experience counted twice (M10)
and the experience shortfalls summed (M19). The search from the
experience start (M15) answers too few on some contests and too many on
others, and fails both. P5, each start one more, fails the edits whose
answer can then rise, or fall by more than the two hours the starts
stand for: a tie in experience a win (M2), each hour counted twice (M10), the
search stepping two past a loss (M12) and the shortfalls summed (M19).

Of the thirty-one, fourteen were not kept. The ★ arm's hour short for
each opponent not beaten (M3), the each arm's experience trained only
to a tie (M9) and the prefix arm's experience gained before the
opponent (M18) fail as the iter arm's tie in experience a win (M24); the
★ arm's trained experience lost (M6) and the iter arm's lack not carried
(M22) as the prefix arm's shortfalls summed (M19); the iter arm's energy
hours unclamped (M23) as the ★ arm's energy trained even when enough
(M5); and the template's at least an hour of energy (M28) as the prefix
arm's shortfall at least one (M20). A tie in energy a win in the ★ and
prefix arms (M1, M21) fail alike, as do the each arm's opponent's
experience taken away and the search arm's experience falling (M11,
M14); the search arm's match costing one energy more (M16) and the
template's experience gained one less and starting from the energy
(M27, M31) each fail apart from every kept one. All seven were left out
to keep three to an arm and two to the template.

## Verification

Every arm prints the same output as `training.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 to 1.5 s, and the
differential 0.76 s there and 0.53 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 1000 contests of 100 opponents once from the harness's
generator, contest `c`'s opponents from 1 to `1 + c % 100`, then makes
5000 passes, pass `p` starting contest `c` with `(p + c) % 50` more
energy and `(3p + c) % 50` more experience than its own start and
folding each answer plus `p` into the checksum, with the ★ arm in all
five languages. Every implementation prints `5000 passes over 1000
contests of 100 opponents: checksum 384221395`. No implementation
allocates in a call; the Go one ranges over slices, the C one over
arrays of fixed size.

BENCHTAB
