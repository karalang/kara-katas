# 1690. Stone Game VII

Alice and Bob take turns playing a game, with **Alice starting first**.

There are `n` stones arranged in a row. On each player's turn, they can
**remove** either the leftmost stone or the rightmost stone from the row
and receive points equal to the **sum** of the remaining stones' values
in the row. The winner is the one with the higher score when there are
no stones left to remove.

Bob found that he will always lose this game (poor Bob, he always
loses), so he decided to **minimize the score's difference**. Alice's
goal is to **maximize the difference** in the score.

Given an array of integers `stones` where `stones[i]` represents the
value of the `i`th stone **from the left**, return *the **difference**
in Alice and Bob's score if they both play **optimally**.*

```
stones = [5,3,1,4,2]               ->  6
stones = [7,90,5,1,100,10,10,2]    ->  122
```

**Constraints:** `n == stones.length`; `2 <= n <= 1000`;
`1 <= stones[i] <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `game.kara` ★ | best(i, j), the most the player to move can lead by on stones i..=j, is the larger of the sum of i + 1..=j less best(i + 1, j) and the sum of i..=j - 1 less best(i, j - 1), the sums from prefix sums; going i down from the right end, one vector holds row i + 1 until each entry is overwritten with row i. O(n^2) time, O(n) space |
| `game_memo.kara` | the same recurrence searched from best(0, n - 1) by recursion, each stretch's answer kept in a table of `Option[i32]`, the stretch's sum carried down. O(n^2) |
| `game_table.kara` | the whole table, every stretch of length 2, then 3, up to n, its sum kept in a second table. O(n^2) time and space |
| `game_solution.kara` | a Rust solution as LeetCode's Rust users write it, prefix sums in `vec![0; n + 1]`, a `vec![vec![0; n]; n]` table filled from the right and `max` as a method, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's two examples, two stones
alike, and two far apart; then the answers summed and a checksum for
3000 random rows of up to 10 stones up to 10, 300 of up to 100 up to
1000 and 30 of up to 1000 up to 1000. `game.py` mirrors the ★ arm and
its output is byte-identical.

```
6
122
1
1000
3000 rows of up to 10 stones up to 10: answers sum to 47826, checksum 167928486
300 rows of up to 100 stones up to 1000: answers sum to 3737972, checksum 667451329
30 rows of up to 1000 stones up to 1000: answers sum to 4021356, checksum 184302079
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every removal played out from the whole row, each scoring the
stones left after it, Alice taking the largest final lead of hers over
Bob and Bob the smallest, with no table. It checks 3000 random rows of 2
to 10 stones from 1 to between 1 and 20. Every case is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the row reversed gives the same answer |
| P3 | every stone doubled doubles the answer |
| P4 | the answer is at least 0 and at most the sum less the smallest stone |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 399088988, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P3 fails for no mutant: every edit is
linear in the stones, as wrong at twice their values as at once. M5 and
M10 both play Bob's side for Alice, `min` for `max`, and fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: taking the left stone scores it too | P1 2484, P2 2158, P4 317, P5 2484 |
| M2 | ★: always the left stone | P1 1302, P2 1421, P5 1302 |
| M3 | ★: the rows filled left to right | P1 2681, P2 2066, P4 431, P5 2681 |
| M4 | memo: one stone left scores itself | P1 3000, P5 3000 |
| M5 | memo: `min` for `max` | P1 2474, P5 2474 |
| M6 | memo: the table keeps the left stone's lead, not the best | P1 222, P2 276, P5 222 |
| M7 | table: a stretch's sum grows by its first stone | P1 2341, P2 2021, P4 77, P5 2341 |
| M8 | table: the right stone's lead adds the other's | P1 2683, P2 2432, P4 2621, P5 2683 |
| M9 | solution: the left stone's lead adds the other's | P1 2681, P2 2432, P4 2635, P5 2681 |
| M10 | solution: `min` for `max` | P1 2474, P5 2474 |

## Benchmarks

The bench draws 40 rows of 1000 stones up to 1000, LeetCode's largest,
all of them first, then answers each 4 times by the ★ arm in all five
languages, each building its two vectors per answer. Every
implementation prints `40 rows of 1000 stones, 4 rounds: answers sum to
40699672, checksum 14907409`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.103 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.175 s |
| Go | 0.175 s |
| Kāra (`karac build`) | 0.176 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.179 s |
| Rust (`rustc -O`) | 0.199 s |
| Python | 11 s |

The sequential Kāra build is 12% faster than Rust and level with Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.103 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.171 s and 0.171 s on one
run).

## Verification

All four arms print the same output as `game.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The table arm checked clean as first written. The ★ arm filled `prefix`
and `best` with a bare `0`, which keeps the literal's `i64`, and returned
`best[n - 1]` as the `i32` the signature names; the refusal (E0200)
named the fill literal, and `karac fix` wrote `0i32` in both.

The memo arm's table is `Vec.filled(n, Vec.filled(n, None))`, its
element type left to the `mut ref Vec[Vec[Option[i32]]]` parameter it is
handed to. A fill of `None` one level deep takes its type that way, but
a fill of fills did not: `karac check` failed with E0516, "an expression
whose type does not lower (`UnknownParam("T")`)", an internal error
rather than a refusal. Since kara `93fd9b2078` (B-2026-11-20-37) the inner fill's
`None` takes its type from the use like the outer one, and the arm checks
as written.

LeetCode's Rust solution took one `karac fix` of 9 edits:
`struct Solution {}` added, `Vec<i32>` written `Vec[i32]`,
`vec![0; n + 1]` written `Vec.filled(n + 1, 0i32)` and
`vec![vec![0; n]; n]` `Vec.filled(n, Vec.filled(n, 0i32))`, the
innermost literal typed for the `i32` the table returns, and the
harness's `stones.clone()` passed as `stones` (`redundant_clone`).

The differential's memo arm names its helper `memo_best`, so it does not
meet the ★ arm's `best` vector. `arm_name` indexes a list of string
literals for a `Str`, as #1662's differential does (B-2026-11-19-131).
