# 2225. Find Players With Zero or One Losses

You are given an integer array `matches` where `matches[i] = [winner_i,
loser_i]` indicates that the player `winner_i` defeated player `loser_i`
in a match.

Return *a list* `answer` *of size* `2` *where:*

- `answer[0]` is a list of all players that have **not** lost any
  matches.
- `answer[1]` is a list of all players that have lost exactly **one**
  match.

The values in the two lists should be returned in **increasing** order.

**Note:**

- You should only consider the players that have played **at least**
  one match.
- The testcases will be generated such that **no** two matches will have
  the **same** outcome.

```
matches = [[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8],[4,9],[10,4],[10,9]]  ->  [[1,2,10],[4,5,7,8]]
matches = [[2,3],[1,3],[5,4],[6,4]]                                          ->  [[1,2,5,6],[]]
```

**Constraints:** `1 <= matches.length <= 10^5`; `matches[i].length ==
2`; `1 <= winner_i, loser_i <= 10^5`; `winner_i != loser_i`; all
`matches[i]` are unique.

A map from player to losses: a winner entered with 0 if new, a loser's
count raised. Then the players with 0 and with 1 are collected and
sorted, since a hash map walks in no set order. O(m log m).

## Approaches

| file | mechanism |
|---|---|
| `players.kara` ★ | a `Map[i64, i64]` of losses, a winner entered with 0 when `contains_key` says it is new; the players with 0 and 1 collected from the walk and sorted |
| `players_array.kara` | a count per player number, `Vec.filled(largest + 1, -1)` with -1 for a number that never played; one walk up the numbers lists both answers already in order, with no sort |
| `players_sorted.kara` | a `SortedMap[i64, i64]` of losses, which walks in key order, so both lists come out sorted; a `match` on the count |
| `players_struct.kara` | a `struct Tournament` holding a `Set` of everyone seen and a `Map` of losses, with `record` (`mut ref self`), and `unbeaten` and `beaten_once` (`ref self`) both reading a shared `with_losses` |
| `players_iter.kara` | the matches folded into a `Map` by a closure taking it `own`, then each answer a `filter` and `map` over its entries, collected and sorted, by a closure called twice |
| `players_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in and out, a `HashMap<i32, i32>` filled through `entry(..).or_insert(0)` and `*... += 1`, walked as `(&player, &count)`, both lists sorted and returned as `vec![zero, one]`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one match, a cycle of three, a player losing twice, and a chain), each
with its answer; then a checksum of 3000 random tournaments of 1 to 30
matches among 5, 30 and 10^5 players in turn; then the constraints'
largest, 10^5 matches among 10^5 players, with 23350 unbeaten and 36870
beaten once. The random matches are drawn from two draws each, since one
stops at 32767, and keep the constraints: no player against itself, and
no match twice. `players.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 20 edits: `use
std::collections::HashMap` dropped, `HashMap<i32, i32>` and
`HashMap::new()` to `Map[i32, i32]` and `Map.new()`, `Vec<...>` to
`Vec[...]`, `for m in &matches` to `for m in ref matches`, `for
(&player, &count) in &losses` to `for (player, count) in ref losses`,
`vec![]` to `Vec.new()`, `vec![zero, one]` to `[zero, one]`, and
`struct Solution;` to `struct Solution {}`.
`entry(..).or_insert(0)` and `*... += 1` through the reference it hands
back are Kāra's too.

The iter arm was first written with its fold's accumulator a bare
`|table: Map[i64, i64], ...|`, which borrows; `karac check` reported
that the closure writes and gives it away, and `karac fix` made it `own`.
The struct arm was first written with Rust's typed receivers, `self: ref
Tournament` and `self: mut ref Tournament`; `karac check` rejected them
and named the Kāra spellings, but `karac fix` carried a typed receiver
only when the type was written `Self`, so these two were rewritten by
hand to `ref self` and `mut ref self`. karac now fixes the impl's own type
name the same way (kara B-2026-11-17-142).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each number from 1 to the largest player tried in order,
kept if it played at all, and its losses counted by a walk over every
match; no table. It checks 300 random tournaments of 1 to 20 matches
among 5, 10 and 40 players in turn; then 30 where player 1 beats every
other of 2 to 13; then 30 cycles, each player beating the next and the
last beating the first. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | two lists, each strictly increasing, sharing no player, and every player in them one who played |
| P3 | the matches in reverse order: the same answers |
| P4 | every player numbered 7 higher: every answer 7 higher |
| P5 | one more match, a new player above all the others beating a random one who played: the new player last among the unbeaten, and the beaten one moved from unbeaten to once, or from once out |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 221761595, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading with
`collections.Counter`. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
of the others, each run under `karac __mir-llvm-run`, and the kept ones
under `karac __mir-run` too. Seventeen are kept, three to each Kāra arm
and two to the Rust-template arm. Each kept one is killed, fails the
same checks under both backends and not by a crash, and no two kept ones
fail the same way.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a winner's count reset to 0 by every win | P1 269, P3 285, P6 269 |
| M4 | ★: the unbeaten left unsorted | P1 135, P2 135, P3 148, P5 210, P6 135 |
| M5 | ★: players beaten twice listed with those beaten once | P1 206, P5 154, P6 206 |
| M8 | array: the largest player never listed | P1 253, P5 360, P6 253 |
| M10 | array: a loser's first loss counted from -1 | P1 327, P3 260, P6 327 |
| M11 | array: a number that never played counted as unbeaten | P1 163, P2 163, P4 360, P6 163 |
| M13 | sorted: the second list those beaten twice | P1 344, P5 227, P6 344 |
| M14 | sorted: the two lists swapped | P1 329, P5 360, P6 329 |
| M15 | sorted: each loss counted twice | P1 318, P5 73, P6 318 |
| M17 | struct: a winner never recorded as a player | P1 267, P5 360, P6 267 |
| M18 | struct: both lists left unsorted | P1 260, P2 260, P3 269, P5 297, P6 260 |
| M21 | struct: losses capped at 1 | P1 243, P5 287, P6 243 |
| M22 | iter: each list every player with at most that many losses | P1 267, P2 267, P5 360, P6 267 |
| M23 | iter: the counts listed, not the players | P1 324, P2 317, P4 329, P5 360, P6 324 |
| M25 | iter: both lists left unsorted | P1 267, P2 267, P3 269, P5 283, P6 267 |
| M29 | solution: the once-beaten left unsorted | P1 231, P2 231, P3 250, P5 219, P6 231 |
| M31 | solution: a loser's count starting at 1 | P1 287, P3 229, P6 287 |

The four unsorted edits (M4, M18, M25, M29) list players in the map's
walk order, which is random per process, so their counts change from run
to run and between the two backends; the properties they fail (P1, P2,
P3, P5, P6) do not. The table shows one `__mir-llvm-run`.

P1 and P6 kill all seventeen, P5 thirteen, P2 and P3 seven each, and P4
two. P4 renumbers every player, and every edit here miscounts the same
way whatever the numbers are, so the wrong answer moves along with the
right one; only the two that list something other than the players who
played (M11, M23) break it. P3 kills the edits whose answer hangs on the
order of the matches: a win that erases earlier losses (M2), a count
whose start depends on which match came first (M10, M31), and the
unsorted lists, whose walk order shifts as the map fills in another
order.

Of the thirty-one, fourteen were not kept. None survives and none
differs between the backends. One crashes: the array arm sized by the
winners alone (M7) indexes past its table. Twelve fail as a kept one
does: the ★, array, struct and template arms' winner never entered (M1,
M9, M20, M27) as the struct arm's winner never recorded (M17); the
sorted and iter arms' winner reset (M12, M24) as the ★ arm's (M2); the ★
arm's loss stored as 1 and the template's `count >= 1` (M3, M30) as the
struct arm's cap (M21); the sorted arm's winner losing too and the iter
arm's lists swapped (M16, M26) as the sorted arm's swap (M14); the
struct arm's `beaten_once` reading 2 (M19) as the sorted arm's (M13);
and the template's winner losing (M28) as the ★ arm's roles swapped
(M6). M6 itself is left out for the count of three.

## Verification

Every arm prints the same output as `players.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.7 s to 2.7 s, the `SortedMap`
arm 6.5 s, and the array arm 17.7 s: it fills a table as long as the
largest player for each of the 3000 tournaments, a third of them among
10^5 players. The differential takes 1.0 s.

## Benchmarks

The bench draws 4 tournaments of 10^5 matches among 10^5 players once,
then answers each 25 times, one match drawn again before each answer,
with the ★ arm in all five languages; C's map of losses is an
open-addressing table, since C has none of its own, and its lists are
sorted by `qsort`. The bench's matches keep no player against itself
but are not kept unique: a repeat is rare among 10^10 pairs and the
count takes it as it comes. Every implementation prints `100
tournaments: 5998928 players listed in all, checksum 97529738`.

BENCHTAB
