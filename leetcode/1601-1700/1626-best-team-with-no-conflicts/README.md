# 1626. Best Team With No Conflicts

You are the manager of a basketball team. For the upcoming tournament,
you want to choose the team with the highest overall score. The score of
the team is the **sum** of scores of all the players in the team.

However, the basketball team is not allowed to have **conflicts**. A
**conflict** exists if a younger player has a **strictly higher** score
than an older player. A conflict does **not** occur between players of
the same age.

Given two lists, `scores` and `ages`, where each `scores[i]` and
`ages[i]` represents the score and age of the `ith` player,
respectively, return *the highest overall score of all possible
basketball teams*.

```
scores = [1,3,5,10,15], ages = [1,2,3,4,5]  ->  34
scores = [4,5,6,5],     ages = [2,1,2,1]    ->  16
scores = [1,2,3,5],     ages = [8,9,10,1]   ->  6
```

**Constraints:** `1 <= scores.length, ages.length <= 1000`;
`scores.length == ages.length`; `1 <= scores[i] <= 10^6`;
`1 <= ages[i] <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `team.kara` ★ | sorted by age, then score, a team has no conflict exactly when its scores never fall along that order; the best team ending at each player is its score plus the best ending at an earlier player scoring no higher, as in a longest rising run. O(n^2) |
| `team_byscore.kara` | the same turned round: sorted by score, then age, into a `Vec` of `Player` structs, a team has no conflict exactly when its ages never fall. O(n^2) |
| `team_tree.kara` | sorted by age, then score; the best team among earlier players scoring no higher is a prefix maximum, kept in a Fenwick tree indexed by each score's rank among the distinct scores. O(n log n) |
| `team_solution.kara` | LeetCode's Rust template: the players zipped into `(age, score)` pairs, sorted, and the rising-run count with a running answer. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples, one player
alone, and four players of one age, who never conflict (22); then the
best scores summed and a checksum for 3000 random teams of up to 10
players with scores up to 10 and ages up to 5, 300 of up to 100 with
scores up to 1000, and 10 of up to 1000 with scores up to 30000.
`team.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every subset of the players, kept when no younger player in
it scores strictly more than an older one, and the largest sum taken. It
checks 3000 random teams of 1 to 10 players, every other one with scores
and ages in `1..=4`, so ties are common, the rest in `1..=50`. Every
random choice is drawn before any arm answers. The interpreter takes
about 9 s.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the players listed backwards leave the answer |
| P3 | one more player, older than all and scoring the top score, adds exactly that score |
| P4 | every score doubled doubles the answer |
| P5 | the answer is at least the top score and at most all scores summed |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 497570764, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P2 is what catches a sort that leaves
ties in their given order (M1, M4): only a different order of the same
players shows it.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: sorted by age alone, ties left as given | P1 684, P2 953, P6 684 |
| M2 | ★: an equal score does not extend a team | P1 1255, P3 2647, P6 1255 |
| M3 | ★: a team ending at a player starts at 0, not its score | P1 3000, P5 532, P6 3000 |
| M4 | by score: sorted by score alone, ties left as given | P1 723, P2 939, P6 723 |
| M5 | by score: an older earlier player extends, not a younger one | P1 2564, P3 3000, P6 2564 |
| M6 | tree: the prefix query skips one rank on its way down | P1 1620, P3 512, P6 1620 |
| M7 | tree: one age's players visited by falling score | P1 1063, P6 1063 |
| M8 | tree: the prefix query never reads rank 1 | P1 322, P3 336, P6 322 |
| M9 | template: sorted by score, then age, the age test still the score's | P1 2323, P6 2323 |
| M10 | template: the last player's team kept, not the best | P1 1336, P3 1336, P5 747, P6 1336 |

## Benchmarks

The bench draws 100 random teams of 1000 players, scores up to `10^6`
and ages up to 1000, all of them first, then each one's best score by
the ★ arm in all five languages. Every implementation prints `100 teams
of 1000 players: best scores sum to 3387718399, checksum 948901714`. The
C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `eb32a1ff0` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.064 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.083 s |
| C (`clang -O3`) | 0.085 s |
| Kāra (`karac build`) | 0.085 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.091 s |
| Go | 0.128 s |
| Python | 3.1 s |

Kāra is level with C and ahead of Rust with overflow checks; plain Rust
is a quarter faster than both. The work is the half of the 1000 x 1000
pairs below the diagonal, a compare and a maximum each; why plain Rust
pulls ahead was not looked into.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (0.078 s and 0.083 s on one run).

## Verification

All four arms print the same output as `team.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`eb32a1ff0`.

## Writing it

The three arms of my own checked clean as first written, the ★ arm's
`ages.iter().zip(scores.iter()).collect()` into a `Vec[(i32, i32)]` and
the tree arm's `k & -k` included. The harness first drew the largest
batch's scores up to `10^6` from a draw below 32768; it now says 30000.

LeetCode's Rust template takes one `karac fix` of 13 edits:
`struct Solution {}`, the `Vec<..>` types to `Vec[..]`,
`ages.into_iter()` and `scores.into_iter()` to `.clone().into_iter()`
(a Kāra parameter borrows, so taking its items means copying them; an
`own Vec[i32]` parameter is the other way), `sort_unstable()` to
`sort()`, `vec![0; n]` to `Vec.filled(n, 0)`, `let mut ans = 0` to
`let mut ans: i32 = 0`, and `Solution::` to `Solution.`. It then checks
and agrees with no hand edit. No compiler gap was met.
