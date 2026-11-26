# 1406. Stone Game III

Alice and Bob continue their games with piles of stones. There are
several stones arranged in a row, and each stone has an associated value
which is an integer given in the array `stoneValue`.

Alice and Bob take turns, with Alice starting first. On each player's
turn, that player can take `1`, `2`, or `3` stones from the first
remaining stones in the row.

The score of each player is the sum of the values of the stones taken.
The score of each player is `0` initially.

The objective of the game is to end with the highest score, and the
winner is the player with the highest score and there could be a tie.
The game continues until all the stones have been taken.

Assume Alice and Bob play optimally.

Return `"Alice"` if Alice will win, `"Bob"` if Bob will win, or `"Tie"`
if they will end the game with the same score.

```
stoneValue = [1, 2, 3, 7]   ->  "Bob"     Alice loses whatever she takes
stoneValue = [1, 2, 3, -9]  ->  "Alice"   she takes all three, Bob the -9
stoneValue = [1, 2, 3, 6]   ->  "Tie"
```

**Constraints:** `1 <= stoneValue.length <= 5 * 10^4`, `-1000 <=
stoneValue[i] <= 1000`.

Each arm is `fn stone_game_iii(stone_value: Vec[i32]) -> String`. A lead
is at most 5 * 10^7, inside `i32`.

## Approaches

| file | mechanism |
|---|---|
| `stone_game_iii.kara` ★ | bottom-up: `best[i]` is how far ahead the player to move from stone i can end, the most of taking 1, 2 or 3 stones less the other's lead from there, filled from the last stone back. O(n) |
| `stone_game_iii_rolling.kara` | the same lead with only the next three kept, a `(i32, i32, i32)` tuple shifted along, and the winner read from `signum()`. O(n), O(1) space |
| `stone_game_iii_memo.kara` | top-down recursion on the lead, memoized in a `Vec[Option[i32]]`; filled from the last stone back first, so no call goes deeper than three. O(n) |
| `stone_game_iii_suffix.kara` | scores instead of leads: the player to move from stone i ends with what is left, the suffix sum, less the most the other can then get, the least of the next three; Alice's score against the rest compared by `cmp` and matched on `Ordering`. O(n) |
| `stone_game_iii_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![i32::MIN; n + 1]`, the same lead, and `match dp[0].cmp(&0)` on `std::cmp::Ordering`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and three
more (`Bob Alice Tie Bob Tie Tie`); the constraints' most, 5 * 10^4
stones of 1000, of -1000, and drawn (`5 * 10^4 stones: Alice Tie Bob`);
and 3000 random rows of 1 to 40 stones, how many each wins (`3000 random
rows: Alice 2069, Bob 748, Tie 183, checksum 467591693`).
`stone_game_iii.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the rolling and suffix arms check clean as first written.
The ★ and memo arms' `let mut taken = 0;` took `taken +=
stone_value[..]`; an operator does not fix a literal's type (design.md
§8 Literals), so `taken` kept `i64` and could not go to `max` on an
`i32`, check says so and names `taken: i32`, and `karac fix` writes it,
1 fix each. The Rust solution takes one round of 23 fixes by `karac
fix`'s count: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, `vec![i32::MIN; n + 1]` to `Vec.filled(n + 1, i32.MIN)`,
`let mut take: i32`, the `&` dropped from `cmp(&0)`,
`std::cmp::Ordering::Greater` and its two siblings to
`Ordering.Greater`, and `Solution::` to `Solution.`. Its output matches
on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way the game can go played out, each player taking the
move that gives the highest score of their own, both scores kept, on up
to 12 stones. LeetCode's examples, seven edge cases (one stone of each
sign and 0, all 0, three negatives, 1000 and -1000 alternating) and the
constraints' most, 5 * 10^4 stones drawn, and 1993 random rows, 1 to 12
stones two times in three and else 13 to 400, from -1000 to 1000, from
-50 to 20, or from -3 to 3 half the time.

The example rows are pushed into a `Vec[Vec[i32]]` as `[1, 2, 3,
7].to_vec()`, which check refuses as a `Vec[i64]`, with no fix, though
the same literal through `.to_vec()` takes `i32` from a `let` annotation
or a function's parameter; that is B-2026-11-26-6. The differential suffixes
each row's first literal, `[1i32, 2, 3, 7].to_vec()`, as the error
advises.

| | property |
|---|---|
| P1 | the statement read literally, on up to 12 stones |
| P2 | every value doubled doubles every score, so the winner is the same, when every value is within 500 |
| P3 | three stones worth 0 after the last change nothing: a move that reaches past the last real stone is worth what taking up to it is |
| P4 | Alice can take a row of up to three stones whole, so she wins one whose sum is more than nothing |
| P5 | one of the three answers the statement allows |
| P6 | the ★ arm's answer |

All 45,040 checks pass on every arm (P1, P2 and P4 apply to some cases
only): `2003 cases: checksum 950012118, 45040 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, by the lead from the last stone back,
gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the other's lead added, not taken away | P1 603, P6 3824 |
| M2 | ★: at most two stones a turn | P1 352, P4 10, P6 2428 |
| M3 | rolling: the two leads behind swapped as they are shifted along | P1 293, P4 3, P6 496 |
| M4 | rolling: taking three stones answered by the lead from two stones on | P1 311, P4 3, P6 539 |
| M5 | memo: a lead under 0 kept as 0 | P1 629, P6 974 |
| M6 | memo: the lead past the last stone 1, not 0 | P1 164, P2 112, P3 126, P4 16, P6 244 |
| M7 | suffix: the other given the most of the next three, not held to the least | P1 619, P4 40, P6 917 |
| M8 | suffix: Bob's score taken from the second stone's suffix | P1 214, P4 6, P6 327 |
| M9 | solution: at most two stones a turn | P1 352, P4 10, P6 607 |
| M10 | solution: the lead past the last stone 1, not 0 | P1 164, P2 112, P3 126, P4 16, P6 244 |

M2 and M9, and M6 and M10, are the same edit to two arms, and each pair
fails the same checks against the literal reading; P6 counts differ for
M2 and M9 because the ★ arm is itself the mutant in M2.

## Benchmarks

The bench draws a pool of 10^5 stone values from -20 to 20 and runs the
★ arm on 1000 rows of 5 * 10^4 stones in a row, each row's start drawn
from the checksum so far. Every implementation prints `1000 rows of 5 *
10^4 stones: checksum 229847050`.

BENCHTAB
