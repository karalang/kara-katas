# 2511. Maximum Enemy Forts That Can Be Captured

You are given a **0-indexed** integer array `forts` of length `n`
representing the positions of several forts. `forts[i]` can be `-1`,
`0`, or `1` where:

- `-1` represents there is **no fort** at the `i`th position.
- `0` indicates there is an **enemy** fort at the `i`th position.
- `1` indicates the fort at the `i`th the position is under your
  command.

Now you have decided to move your army from one of your forts at
position `i` to an empty position `j` such that:

- `0 <= i, j <= n - 1`
- The army travels over enemy forts **only**. Formally, for all `k`
  where `min(i,j) < k < max(i,j)`, `forts[k] == 0`.

While moving the army, all the enemy forts that come in the way are
**captured**.

Return *the **maximum** number of enemy forts that can be captured*. In
case it is **impossible** to move your army, or you do not have any fort
under your command, return `0`*.*

```
forts = [1,0,0,-1,0,0,0,0,1]  ->  4
forts = [0,0,1,-1]            ->  0
```

**Constraints:** `1 <= forts.length <= 1000`; `-1 <= forts[i] <= 1`.

A march captures a run of enemy forts whose two ends are a fort of ours
and an empty one, so the answer is the longest run of zeros between two
nonzero forts of opposite signs. The approaches differ in how those
runs are found.

## Approaches

| file | mechanism |
|---|---|
| `forts.kara` ★ | one pass that keeps the place of the last fort that is not 0; a nonzero fort opposite to it ends a run. O(n) |
| `forts_scan.kara` | from every fort of ours, a march walked left and then right over the enemy forts, counted when it ends at an empty fort. O(n^2) at worst |
| `forts_pairs.kara` | the places of the nonzero forts gathered in order, and every two neighbours there of opposite signs a gap |
| `forts_rec.kara` | a recursion over the places, carrying the last nonzero fort and the run of zeros since it. At most 1000 deep |
| `forts_iter.kara` | iterators: the nonzero places `enumerate`d and `filter`ed, their neighbouring pairs taken by `windows(2)`, those of opposite signs `filter`ed and `map`ped to their gaps, and the `max` `??` 0 |
| `forts_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; one pass with the last nonzero place in an `Option<usize>`, matched by `if let Some(j)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and six
more; then 2000 random lines of 1 to 30 forts with a 0 one time in three
and 2000 with a 0 nine times in ten, each as a count of those that
capture nothing and a checksum; then the constraints' largest, 1000
forts: ours, 998 enemy and an empty one; the same with both ends ours;
-1 and 1 in turn; and random with a 0 nineteen times in twenty.
`forts.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked on 5000 random lines of 1 to 14 forts against every
pair of a fort of ours and an empty fort, and the two agreed on every
line.

In Kāra `windows(2)` gives a `Vec` of the windows, not an iterator, so
the iter arm's `places.windows(2).filter(..)` is refused by `check` with
E0236, which names the `.into_iter()` it needs; `karac fix` inserts it.

`check` first reports 3 errors on the template: `struct Solution;`, and
`Vec<i32>` and `Option<usize>` in angle brackets. `karac fix` carries it
in one call, reporting 8 edits: `struct Solution {}`; the brackets; the
`usize` of the `Option` becomes `i64`, the type of a `Vec`'s index;
`let mut ans = 0` given `: i32`, which its `0` would otherwise not be
beside the `i32` return; and the wrapper's lossless `as i64` dropped.
The `(i - j - 1) as i32` stands.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every fort of ours and every empty fort as a pair, the march
between them allowed when every fort strictly between is an enemy fort,
and the most forts any allowed march passes. No run is followed and no
last fort kept. It checks 300 random lines of 1 to 12 forts, a 0 one
time in three or four in six; then 20 of 1 or 2 forts; and 40 of 40
forts, a 0 eight times in ten. All 360 are drawn before any arm
answers, and 213 of them capture nothing.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | from 0 to `n - 2`, and 0 when no fort is ours or none is empty |
| P3 | the line in the other order: the same answer |
| P4 | every fort negated, ours as empty and empty as ours: the same answer |
| P5 | every enemy fort written twice: twice the answer |
| P6 | each arm agrees with at least three of the other five |

P5 holds because doubling every 0 doubles every run of zeros and moves
no nonzero fort past another, so every march captures twice as many.

The differential prints `360 cases, 213 capture nothing: checksum
431073944, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases and finds the runs with a
regular expression. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a march counting its end | P1 205, P2 2, P5 205, P6 205 |
| M4 | ★: nothing captured worth -1 | P1 155, P2 155, P5 155, P6 155 |
| M6 | ★: the first nonzero fort kept only | P1 173, P3 76, P5 165, P6 173 |
| M8 | scan: a march to our own fort | P1 153, P2 10, P4 132, P6 153 |
| M10 | scan: marches to the left only | P1 63, P3 134, P4 134, P6 63 |
| M11 | scan: marches from every nonzero fort | P1 41, P2 14, P4 78, P6 41 |
| M13 | pairs: a gap one short | P1 147, P5 147, P6 147 |
| M14 | pairs: the first pair never asked | P1 42, P3 62, P6 42 |
| M16 | pairs: the last pair kept, not the most | P1 65, P3 88, P6 65 |
| M19 | rec: the run never reset | P1 144, P3 147, P6 144 |
| M20 | rec: the captures summed | P1 59, P6 59 |
| M21 | rec: the line begun after a fort of ours | P1 61, P2 37, P3 76, P4 105, P6 61 |
| M22 | iter: the last pair never asked | P1 44, P3 62, P6 44 |
| M23 | iter: pairs of like signs | P1 168, P2 24, P6 168 |
| M25 | iter: the least gap | P1 104, P6 104 |
| M30 | solution: the last fort never seen | P1 17, P3 38, P6 17 |
| M31 | solution: nothing captured worth 1 | P1 213, P2 156, P5 213, P6 213 |

P1 and P6 kill all seventeen, P3 eight, P2 seven, P5 five, and P4 four.

Fourteen are not kept, and none survives. Ten fail exactly as a kept
one: the scan, rec, iter and template arms' march or gap counting its
end (M9, M18, M24, M28) as the ★ arm's (M1); the ★, pairs and template
arms' march between like forts (M2, M12, M27) as the iter arm's pairs
of like signs (M23); the pairs arm's every gap from the first place and
the template's first nonzero fort kept only (M15, M29) as the ★ arm's
first nonzero fort kept only (M6), each measuring every gap from the
first nonzero fort; and the iter arm's nothing captured worth 1 (M26)
as the ★ arm's worth -1 (M4), each answer for a line that captures
nothing off 0. Four fail as one another, in two pairs: the ★ arm's
first place never a start and first fort skipped (M3, M5); and the scan
arm's march over empty forts and the rec arm's run never grown (M7,
M17), each capturing nothing on every line.

## Verification

Every arm prints the same output as `forts.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 to 0.6 s and the differential 0.4 s; under `karac __mir-llvm-asan` the arms take 0.3 to 0.4 s and the differential 0.6 s; and under `karac run` the differential takes 0.4 s.

## Benchmarks

The bench builds 2000 lines of 1000 forts once from its own generator,
a 0 from 1 time in 3 up to 50 times in 52, then makes 115 passes. Each
pass, for every line, sets the fort at place `check % 1000` to `(check
+ p) % 3 - 1`, asks, and puts it back, folding the answer plus the pass
into the checksum. The bench uses the ★ arm in all five languages.
Every implementation prints `115 passes over 2000 lines of 1000 forts:
checksum 797859612`.

BENCHTAB
