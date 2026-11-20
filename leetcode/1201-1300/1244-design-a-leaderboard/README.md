# 1244. Design A Leaderboard

Design a `Leaderboard` class, which has 3 functions:

1. `addScore(playerId, score)`: update the leaderboard by adding `score`
   to the given player's score. If there is no player with that id on the
   leaderboard, add them with the given `score`.
2. `top(K)`: return the score sum of the top `K` players.
3. `reset(playerId)`: reset the score of the player with the given id to
   0 (in other words, erase it from the leaderboard). It is guaranteed
   that the player was added to the leaderboard before calling this
   function.

Initially, the leaderboard is empty.

```
addScore(1, 73); addScore(2, 56); addScore(3, 39); addScore(4, 51); addScore(5, 4)
top(1)                        ->  73
reset(1); reset(2); addScore(2, 51)
top(3)                        ->  141   (51 + 51 + 39)
```

**Constraints:** `1 <= playerId, K <= 10000`; `K` is at most the number
of players on the board; `1 <= score <= 100`; at most 1000 calls.

The arms are a `struct Leaderboard` with `fn new()`, `fn add_score(mut
ref self, player_id: i64, score: i64)`, `fn top(self, k: i64) -> i64`
and `fn reset(mut ref self, player_id: i64)`.

## Approaches

| file | mechanism |
|---|---|
| `leaderboard.kara` ★ | each player's total in a `Map`; a top collects the `values()`, sorts them from the highest with `sort_by` and adds the first `k` with `take(k).sum()` |
| `leaderboard_buckets.kara` | counting: beside the `Map`, a `Vec` of how many players have each total, grown as totals grow; a top walks it down from the highest total, taking as many players of each as are still wanted |
| `leaderboard_sorted.kara` | a multiset: beside the `Map`, a `SortedMap` from each total to how many players have it; a top walks it from the highest with `iter().rev()` |
| `leaderboard_heap.kara` | a bounded heap: a top keeps the `k` highest totals seen so far in a `PriorityQueue`, which pops the smallest first, each total that beats the least of them replacing it |
| `leaderboard_solution.kara` | a Rust solution as LeetCode's Rust users write it (`HashMap<i32, i32>`, `entry().or_insert(0)`, `sort_unstable_by`, `take(k as usize)`), carried to Kāra by `karac fix`, under its own name behind an `i64` `Leaderboard` |
| `differential.kara` | the five arms against the statement read literally, four more properties |

Every arm prints the same 3 lines: LeetCode's example (`73 141`); the
number of tops and a checksum of their answers over 1000 random sessions
of 1 to 300 calls on 1 to 50 players (`38006 tops, checksum
531308558`); and one session at the constraints' top, 3000 calls on
players up to 10000. Each session adds to a random player half the time,
asks a random `top(K)` with `K` at most the players on the board, and
resets a random player on it. `leaderboard.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build. No
arm prints anything that depends on a `Map`'s order: each total is
summed, and the walks that need an order sort or use a `SortedMap`.

The Mend loop: the ★ and bucket arms checked clean as first written. The
sorted arm was first written `let now = match self.scores.get(player_id)
{ Some(old) => { self.drop_score(old); old + score } None => score };`.
`get` returns an `Option[ref i64]`, so `old` borrows `self` across the
`mut ref self` call, and E0516 is right; the fix is `.cloned()` on the
scrutinee, which `karac fix` gives a bare `match` but did not give one
that is a `let`'s initializer (gap 2 below). The heap arm was first
written with Rust's habits: `import std.collections.{PriorityQueue,
Reverse};`, which was refused as an unknown module with no fix (gap 1),
then `Reverse(score)` and `.0`, which `karac fix` rewrites to `Reverse {
value: score }` and `.value`. That arm then gave wrong answers (`73 94`),
and the cause was the author's, not the compiler's: Kāra's
`PriorityQueue.new()` pops the smallest first, the opposite of Rust's
`BinaryHeap`, so the `Reverse` that makes Rust's heap a min-heap made
this one a max-heap. The arm keeps plain `i64` scores, which is the
min-heap a bounded top wants. The solution arm takes `karac fix`'s Rust
rewrites (`use std::collections::HashMap;` gone, `HashMap` to `Map`,
`&mut self` to `mut ref self`, `&self` to `self`, `Vec<i32>` to
`Vec[i32]`, `HashMap::new()` to `Map.new()`, `sort_unstable_by` to
`sort_by`, `remove(&player_id)` to `remove(player_id)`, `k as usize` to
`k as i64`), and a second round removes the `as i64`, which an `i32`
does not need to widen. All five check clean.

## Gaps

Two, both in `karac fix`'s reach, both fixed with the kata:

1. **B-2026-11-20-80:** `import std.collections.{PriorityQueue,
   Reverse};` was refused as "unknown module `std.collections`" with
   nothing more. An import whose every item is in the prelude already
   got a note and a deletion (B-2026-11-17-149), but one mixing prelude
   names with another module's got neither. The error now says
   `PriorityQueue` is in the prelude and `Reverse` is `std.cmp`'s, and
   `karac fix` rewrites the line to `import std.cmp.Reverse;`.
2. **B-2026-11-20-81:** E0516 in a `match` on a borrow gets `.cloned()`
   on the scrutinee as a fix (B-2026-11-15-49), but not when the `match`
   is itself a `let`'s initializer, `let now = match m.get(k) {`: the
   fix read the `let` and looked for a borrow ending at its `;`. It now
   reads the `match`.

## Differential

`differential.kara` holds copies of the five arms, renamed, and the
statement read literally: the players and their totals side by side in
two lists, each add a linear search, each top a sorted copy of the
totals and the first `k` of it. 2000 sessions of 1 to 80 calls, a third
on 1 to 4 players (many equal totals), a third on 5 to 24 and a third
on 25 to 224, the same calls applied to the five arms and the literal
board.

| | property |
|---|---|
| P1 | the statement read literally, at every top |
| P2 | one more player adds a positive score: `top(k)` exceeds `top(k - 1)` |
| P3 | the top of every player is the sum of every total |
| P4 | the top one is the highest total |
| P5 | a reset takes exactly that player's total out of the board's sum |
| P6 | the ★ arm's answer |

P3 and P4 are checked before every top and every reset, P1 and P2 at
every top, P5 at every reset. All 1,115,430 checks pass on every arm:
`2000 sessions: checksum 715491640, 1115430 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and the
AddressSanitizer build. Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. H2
makes the heap's answer depend on the order in which the `Map` hands
over its totals, which differs from process to process, so its counts
are taken with `KARAC_HASH_SEED=7`, the same under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the totals sorted from the lowest | P1 10448, P4 28035, P6 41792 |
| S2 | ★: an add replaces the player's total instead of adding to it | P1 8986, P3 18988, P4 16766, P5 5031, P6 63156 |
| B1 | buckets: a top stops one player short | P1 18282, P2 8387, P3 36390, P4 37181, P5 8228, P6 32038 |
| B2 | buckets: an add leaves the player's old total counted | P1 7738, P3 20804, P4 7233, P5 5347, P6 15640 |
| O1 | sorted: a total dropped while one player still has it | stops: `key not found` |
| O2 | sorted: a top walks from the lowest total | P1 10448, P4 28035, P6 10448 |
| H1 | heap: one total too many kept | P1 10460, P2 3552, P4 28088, P6 10460 |
| H2 | heap: a better total pushed without the least popped | P1 8500, P2 7165, P4 20951, P6 8500 |
| L1 | solution: the highest total skipped | P1 18481, P2 8085, P3 37181, P4 36655, P5 8127, P6 32557 |
| L2 | solution: a reset adds 0 instead of erasing | P1 14717, P3 32034, P4 23726, P5 15767, P6 28004 |

All ten are caught: nine by P1, the statement read literally, and O1 by
the `SortedMap` itself, whose `counts[score]` stops on a total it no
longer holds. P6 fails on the other four arms too when the ★ arm is the
one mutated (S1, S2). P4, the top one, catches every wrong answer,
since a top of one is asked before every top and reset. P3, the whole
board, catches the five that lose or misplace a total (S2, B1, B2, L1,
L2) but not the four that only pick the wrong `k` (S1, O2, H1, H2 keep
every total, and a top of all of them is right). P5 catches the five
whose board's sum is wrong after a reset. P2 catches the arms that can
return a top no larger than the one before (B1, H1, H2, L1).

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (each player's total in a `Map`; a top sorts the totals from the
highest and adds the first `k`) on 100 sessions of 3000 random calls on
players up to 10000; the tops' answers folded into a checksum. Every
program prints `100 sessions of 3000 calls on 10000 players: 74815 tops,
checksum 413597999`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.365 to 1.632 s | 1.447 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.388 to 1.510 s | 1.429 s |
| Rust (`rustc -O`) | 0.424 to 0.557 s | 0.465 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.425 to 0.596 s | 0.440 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.413 to 0.503 s | 0.425 s |
| C (`clang -O3`) | 1.900 to 2.219 s | 1.928 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.909 to 2.252 s | 1.987 s |
| Go | 2.519 to 2.761 s | 2.601 s |
| Python | 2.479 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 3.2x Rust with overflow checks on's time (1.429
s against 0.440 s). Kāra is about 26% ahead of C (1.429 s against 1.928
s); Go takes about 1.8x Kāra's time. Python takes about 2x Kāra's time.
No profile was taken.
