# 2038. Remove Colored Pieces if Both Neighbors are the Same Color

There are `n` pieces arranged in a line, and each piece is colored either
by `'A'` or by `'B'`. You are given a string `colors` of length `n` where
`colors[i]` is the color of the `i`-th piece. Alice and Bob are playing a
game where they take alternating turns removing pieces from the line, Alice
first. Alice may only remove a piece colored `'A'` if both its neighbors
are also colored `'A'`, and Bob may only remove a piece colored `'B'` if
both its neighbors are also colored `'B'`. Neither may remove a piece from
the edge of the line. If a player cannot move on their turn, that player
loses and the other wins. Assuming both play optimally, return `true` if
Alice wins, or `false` if Bob wins.

```
colors = "AAABABB"       ->  true
colors = "AA"            ->  false
colors = "ABBBBBBBAAA"   ->  false
```

**Constraints:** `1 <= colors.length <= 10^5`; `colors` consists of only
the letters `'A'` and `'B'`.

The game is decided before it starts. Alice may remove an `A` only from
inside a run of `A`s, which leaves the run one shorter and touches no `B`,
and Bob's moves are the same over `B`s. Neither player's moves change the
other's, so each has a fixed number: one per piece inside a run of their
color, `len - 2` for a run of `len >= 3`. Alice moves first and is the
first to run out unless she has more.

## Approaches

| file | mechanism |
|---|---|
| `colors.kara` ★ | the pieces collected into a `Vec[char]`, every interior piece whose neighbours share its color counted for its player. O(n) |
| `colors_windows.kara` | `windows(3)` over the pieces and a closure `moves(color)` counting the windows that are all one color, called for `'A'` and `'B'`. O(n) |
| `colors_runs.kara` | run lengths: one scan measures each run, which gives its player `(len - 2).max(0)` moves. O(n) |
| `colors_bytes.kara` | `bytes()` read in place, `b'A'` compared, one balance counting Alice's moves up and Bob's down. O(n) |
| `colors_fold.kara` | one `fold((None, None, 0, 0), \|(before, last, alice, bob), c\| ..)` over the chars, the two pieces before this one carried as `Option`s and compared with `Some(c)`. O(n) |
| `colors_solution.kara` | LeetCode's Rust template (`impl Solution`, `as_bytes()`, `let (mut a, mut b)`, `&&`, an index loop to `len().saturating_sub(1)`), carried by `karac fix` in two rounds to a clean check |
| `differential.kara` | the six arms against the game played out, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's three
examples and six more; then how many of 2000 rows of 1 to 40 pieces Alice
wins, with a checksum of the answers in order, and the same for 4 rows of
100000 pieces, the most the constraints allow (runs from short to long).
`colors.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the game played out from the row, every move tried, the player
to move winning when some move leaves the other losing (memoized on the
row and whose turn it is). It checks 1500 rows of 1 to 10 pieces whose
runs run from single pieces to the whole row, each with a place to double
an `A`. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the game played out |
| P2 | the row reversed leaves the answer |
| P3 | Alice never wins both the row and the row with its colors swapped |
| P4 | an `A` doubled where one is (or added, in a row of `B`s) never turns Alice's win into a loss |
| P5 | every run cut to two pieces leaves Alice no move, so she loses |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 rows: checksum 62109702, 54000 checks over 6
arms: 0 failures` under every lane in Verification. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. All thirty are killed, each
fails the same way under both backends, none by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a triple wanting only one matching neighbour (`or` for `and`) | P1 115, P5 284, P6 115 |
| M2 | ★: the colors' moves swapped | P1 619, P4 62, P6 619 |
| M3 | ★: the last triple skipped | P1 66, P2 85, P6 66 |
| M4 | windows: pairs counted for triples (`windows(2)`) | P1 122, P5 347, P6 122 |
| M5 | windows: windows of four counted | P1 115, P6 115 |
| M6 | windows: Alice's moves weighed against her own | P1 314, P6 314 |
| M7 | runs: a short run's negative moves counted (`.max(0)` dropped) | P1 273, P4 72, P5 416, P6 273 |
| M8 | runs: runs cut at four pieces | P1 2, P6 2 |
| M9 | runs: the piece after each run skipped | P1 52, P2 88, P6 52 |
| M10 | bytes: Bob's moves never counted | P1 85, P3 111, P6 85 |
| M11 | bytes: a triple's ends compared without its middle | P1 124, P5 205, P6 124 |
| M12 | bytes: Alice's moves counted twice | P1 43, P3 45, P6 43 |
| M13 | fold: Bob's moves counted twice | P1 13, P6 13 |
| M14 | fold: two phantom `A`s before the row | P1 450, P2 433, P3 45, P5 743, P6 450 |
| M15 | fold: every `A` counted a move | P1 892, P3 886, P5 1330, P6 892 |
| M16 | solution: Alice winning a tie (`>=` for `>`) | P1 881, P3 881, P5 1500, P6 881 |
| M17 | solution: a triple's ends compared without its middle | P1 186, P4 133, P5 224, P6 186 |

P1 and P6 kill all seventeen, P5 eight, P3 five, P2 three and P4 three. P2
sees the edits that treat the two ends of the row differently: the last
triple skipped (M3), a piece skipped after each run (M9), and `A`s
imagined before the row (M14). P3 sees the edits that favour one color, so
that a row and its swap can both be Alice's: Bob's moves dropped or Alice's
doubled (M10, M12), every `A` a move (M15), phantom `A`s (M14), and a tie
handed to Alice (M16). P4 sees the edits under which one more `A` can cost
Alice: with the colors swapped, a longer run of `A`s is a move for Bob (M2);
with negative moves counted, an `A` added to a row of `B`s is a run of one
and a move lost (M7); and with only a triple's ends compared, doubling the
`A` in `BAB` removes the pattern the edit counted for her (M17). P5 sees
the edits that find moves in a row that has none: a triple with one
matching neighbour or a pair (M1, M4), a `.max(0)` dropped so Bob's single
pieces count against him (M7), a triple's ends alone (M11, M17), phantom
or free `A` moves (M14, M15), and the tie that a row with no moves is
(M16).

The other thirteen fail as a kept one does. The first triple skipped in
the ★ and bytes arms fails as the windows arm's first piece dropped. Alice
winning a tie fails alike in the ★, windows and bytes arms and as M16. The
colors' moves swapped in the runs and Rust arms fail as M2. A run giving
`len - 1` moves, and the fold arm's triple wanting only the last piece or
carrying this piece as the one before, all count pairs, and fail as M4.
The Rust arm's last triple skipped fails as M3 and its Bob counted twice as
M13. One first draft survived and was replaced: the windows arm counting a
window with any piece of the color, `any` for `all`. A mixed window then
counts for both players and cancels, so the comparison is the true one.

## Verification

Every arm prints the same output as `colors.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 1.0 s (★) to 4.9 s (windows) and the
differential 1.1 s, on kara 991c45adcd.

The fold arm first stopped at the type check twice over, after kata 2036's
fix to `fold` accumulators that start `None`. `before == Some(c)` compared
the accumulator's `Option[?T]`, still open, with an `Option[char]` and was
refused "cannot compare"; two operands of one constructor are now unified
first, as Rust's comparison infers. And the tail `(last, Some(c), ..)`
handed `last`, the second part's `Option[?B]`, to the first part's
`Option[?A]` and was refused; two open types of one shape are now one (kara
3fd9eed398, `tests/kata_2038_fold_compare.rs`).

For the runs arm, Rust's `chunk_by(|a, b| a == b)` on the pieces was tried
first. `karac fix` rewrote it to `c.iter().chunk_by(..)`, as for an
iterator adaptor called on a `Vec`, and that is refused in turn: no
iterator in the library has `chunk_by`, and the `|a, b|` closure adds a
"cannot compare" of two unknowns. B-2026-11-09-31 tracks the method and the
fix that points at it. The arm measures each run itself.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds (four edits, then one) to a clean check: `let (mut alice,
mut bob)` to `let mut (alice, bob)`, `&&` to `and`, and `as_bytes()` to
`bytes()`, Kāra's `Slice[u8]` of a string's bytes. `b'A'` and
`saturating_sub` carry as they are.

## Benchmarks

The bench builds 4 rows of 100000 pieces once in all five languages, the
most the constraints allow, and runs the ★ arm for 100 rounds, one piece of
every row flipped before each call on a fresh string: 400 calls. Every
implementation prints `400 calls: Alice wins 300, checksum 854152627`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `991c45adcd` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.140 to 0.163 s | 0.147 s |
| Rust (`rustc -O`) | 0.192 to 0.198 s | 0.196 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.206 to 0.236 s | 0.214 s |
| Kāra (`karac build`) | 0.206 to 0.251 s | 0.214 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.262 to 0.312 s | 0.269 s |
| Go | 0.476 to 0.539 s | 0.505 s |
| Python | 4.1 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.209 s) is not above its real time (0.214 s).

The sequential Kāra program is 0.80x Rust under overflow checks and 1.45x
C.
