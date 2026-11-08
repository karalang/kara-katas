# 2027. Minimum Moves to Convert String

You are given a string `s` of `n` characters, each `X` or `O`. A move
picks three consecutive characters and makes all three `O`; a character
already `O` stays `O`. Return the fewest moves that make every character
`O`.

```
s = "XXX"   ->  1
s = "XXOX"  ->  2
s = "OOOO"  ->  0
```

**Constraints:** `3 <= s.length <= 1000`; `s[i]` is `X` or `O`.

Some move must cover the leftmost `X`, and the move that starts at it
covers the most of what lies beyond, so taking it is never worse: the
greedy takes it and goes on three places later.

## Approaches

| file | mechanism |
|---|---|
| `moves.kara` ★ | the string's `chars()` collected; a `while` loop that takes a move at each `X` and jumps three places, else steps one. O(n) |
| `moves_fold.kara` | the greedy as a `fold` over `chars().enumerate()`, its state the moves so far and the first place the last move does not cover |
| `moves_dp.kara` | a table from the right over `bytes().to_vec()`: `best[i]` is the fewest moves that clear `s[i..]`, `best[i + 1]` after an `O` and `1 + best[i + 3]` after an `X`, padded three places past the end |
| `moves_simulate.kara` | the moves made: a `Vec[char]` changed in place from the leftmost `X` (`position`), three places at a time, until `contains('X')` finds none. O(n^2) at worst |
| `moves_find.kara` | `find("X")` on the rest of the string, `s[from..s.len()]`; each `X` it finds starts a move and the search goes on three places later |
| `moves_solution.kara` | LeetCode's Rust template (`as_bytes()`, `b'X'`, a `usize` index stepped by 3, a unit struct after `impl Solution`, a `&String` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the total and a checksum of the answers for
3000 strings of 3 to 30 places, each with its own share of `X`, and for 6
strings of 1000 places, the longest the constraints allow. `moves.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a breadth-first search over the sets of places still `X`, held
as bits, where a move at `j` clears places `j` to `j + 2`; the depth at
which the set first empties is the fewest moves. It checks 1500 strings of
3 to 12 places, each with its own share of `X` from 0 to 1. Every random
choice of a problem is drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the string reversed leaves the count |
| P3 | `OOO` added at both ends leaves the count |
| P4 | the string, `OO` and the string again doubles the count |
| P5 | the first `O` turned into an `X` raises the count by 0 or 1 |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a set of moves covering the string covers it backwards
too. P4 holds because a move covers three places, so none reaches across
`OO` from one copy into the other with an `X` on both sides. P5 holds
because one more move at the new `X` covers it, and a cover of the new
string covers the old one.

The differential prints `1500 problems: checksum 550552995, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a jump of two | P1 673, P6 673 |
| M2 | ★: the first place skipped | P1 317, P2 355, P3 317, P4 317, P6 317 |
| M3 | ★: a move at the first place reaching only two | P1 228, P2 193, P3 228, P4 228, P6 228 |
| M4 | fold: a move reaching four places | P1 446, P4 111, P6 446 |
| M5 | fold: the first free place taken as covered | P1 663, P2 254, P3 241, P4 233, P6 663 |
| M6 | fold: the next free place counted from the last one | P1 274, P2 262, P3 874, P4 473, P6 274 |
| M7 | dp: an `O` clearing the place after it as well | P1 383, P2 392, P3 910, P4 336, P5 160, P6 383 |
| M8 | dp: the last place never read | P1 308, P2 355, P3 308, P4 308, P6 308 |
| M9 | dp: the places past the end needing a move | P1 1500, P4 1500, P6 1500 |
| M10 | simulate: the move made at the rightmost `X` | P1 998, P6 998 |
| M11 | simulate: the first move counted twice | P1 1277, P4 1277, P5 223, P6 1277 |
| M12 | simulate: at most three moves | P1 123, P4 852, P6 123 |
| M13 | find: a move at the search start reaching four | P1 345, P2 104, P3 183, P4 306, P6 345 |
| M14 | find: a move only at a pair of `X` | P1 910, P6 910 |
| M15 | find: an `X` just past a move taken as covered | P1 661, P2 250, P4 186, P5 105, P6 661 |
| M16 | Rust: an `O` in the second place taken as an `X` | P1 369, P2 235, P3 814, P4 369, P6 369 |
| M17 | Rust: the first move reaching four places | P1 276, P2 103, P4 276, P5 6, P6 276 |

P1 and P6 kill all seventeen, P4 fourteen, P2 ten, P3 eight and P5 four.
P4 joins two copies with `OO` between, so the count must double; it sees
every edit whose error depends on where a place sits, since the second
copy's places are 2 + n further on, and every edit that counts a move
wrong only once (M9, M11). It misses only the three edits that are wrong
the same way everywhere: a jump of two (M1), every `X` a move of its own
(M10), and `X` pairs alone counted (M14), each of which doubles along
with the string. P2 and P3 see the edits that treat the start or the end
of the string unevenly, the place after a move included (M5, M6, M7, M13,
M15), and P3's `OOO` at the start moves every place three on, which the
first-place edits notice (M2, M3, M16). P5 turns the first `O` into an
`X`; it sees an edit only where that new `X` changes the count by more
than one or less than none: an `O` clearing the place after it (M7), a
first move counted twice (M11), an `X` taken as covered (M15) and a first
move reaching four (M17).

The other thirteen fail as a kept one does. A jump of two in the dp,
simulate, find and Rust arms (a move clearing two places, or started a
place early in the simulate arm) all fail as M1; the ★ arm's every `X` a
move fails as M10; the ★ and Rust arms' last place never looked at and an
`X` in the last place ignored fail as M8; the fold arm's first place taken
as covered, the dp arm's answer read one place in and the Rust arm's first
place skipped fail as M2. The find arm's last place never searched (P1
189, P2 155) and the fold arm counting an `O` at a free first place (P1
499, P3 1001) fail with counts of their own. Two Rust drafts were
replaced. Its last place never examined failed as M8, which left the arm
no failure of its own. And "a move near the end counted twice", written `ans += if i + 3 >= s.len() { 2 } else { 1 }`,
did not check: an `if` of two literals beside `ans` fixes the binding at
`i64` (design.md § Type inference), and the method's `i32` return then
refuses it, the shape B-2026-11-08-20 asks a machine fix for.

## Verification

Every arm prints the same output as `moves.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.2 s to 1.0 s (simulate) and the
differential 1.3 s.

The five arms were written in Kāra and checked clean, with no fix. The
differential's literal reading first read its distance as `let d =
dist.get(state).unwrap()`, a borrow of the map it then inserts into;
`karac check` refused it (E0516) and `karac fix` wrote `*dist.get(state)
.unwrap()`.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in four rounds (3, 2, 1 and 1 edits). The
first carries the unit struct, the `&String` parameter and the `::` path;
the second turns `as_bytes()` into `bytes()` and drops the wrapper's
`as i64`, a widening Kāra does by itself; the third writes the index as
`i64` rather than `usize`, which it meets in `i < s.len()`; the fourth
drops the wrapper's `ref`. `let mut ans = 0` returned as `i32` checks: only
literals were added to it.

## Benchmarks

The bench builds 2000 strings of 1000 places once, each with its own share
of `X` from 0 to 1, in all five languages, and runs the ★ arm on each for
50 rounds: 100000 calls. Every implementation prints `100000 calls:
22186450 moves, checksum 585047128`. Every language copies the string into
an array of its characters first, as the Kāra program does (C with
`malloc` and `memcpy`, Go with `[]rune`).

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.189 to 0.211 s | 0.195 s |
| Rust (`rustc -O`) | 0.267 to 0.321 s | 0.292 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.290 to 0.355 s | 0.307 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.299 to 0.367 s | 0.315 s |
| Kāra (`karac build`) | 0.289 to 0.387 s | 0.323 s |
| Go | 0.499 to 0.569 s | 0.540 s |
| Python | 4.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.322 s) is not above its real time (0.323 s).

The sequential Kāra program is 1.02x Rust under overflow checks and 1.62x
C.