# 1510. Stone Game IV

Alice and Bob take turns playing a game, with Alice starting first.
Initially there are `n` stones in a pile. On each player's turn, that
player makes a move consisting of removing any non-zero square number of
stones from the pile. If a player cannot make a move, they lose. Given
`n`, return `true` if and only if Alice wins the game, assuming both
players play optimally.

```
n = 1   ->  true    (Alice takes 1)
n = 2   ->  false   (1, then Bob takes 1)
n = 4   ->  true    (Alice takes 4)
n = 7   ->  false
n = 17  ->  false
```

**Constraints:** `1 <= n <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `stones.kara` ★ | a pile wins for the player to move when some square taken leaves a pile that loses; the table filled from the empty pile, which loses, upward, each pile stopping at its first winning move. O(n sqrt n) |
| `stones_push.kara` | pushed forward: each pile that loses makes every pile a square above it a win; a pile no losing pile reaches loses. O(n sqrt n) |
| `stones_iter.kara` | iterators: the squares up to each pile by `(1..).map(..).take_while(..)`, and the pile wins if `any` of them leaves a losing pile |
| `stones_solution.kara` | LeetCode's Rust template (`n as usize`, `vec![false; n + 1]`, `let mut k = 1; while k * k <= i`), the ★ arm, carried by `karac fix` to three errors: B-2026-11-08-16 and B-2026-11-08-18 |
| `differential.kara` | the three arms that check against the statement read literally, six properties |

Every arm prints the same 9 lines: the answer for LeetCode's three
examples and four more (7, 17, 8 and 100000), how many of the piles from
1 to 600 Alice wins (516) with a checksum of which, and a checksum for
three random piles up to 100000. `stones.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the three arms that check and the
statement read literally: the game played out by recursion, every move
tried, the player to move winning when some move leaves the other player
a pile they lose. It checks 2000 piles of 1 to 24 stones. Every random
choice of a problem is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a pile that is a square wins: take it all |
| P3 | a pile that loses makes every pile a square above it win |
| P4 | a pile that wins has a move to a pile that loses |
| P5 | a pile that loses has no move to a pile that loses |
| P6 | each arm agrees with at least one of the other two |

The differential prints `2000 problems: checksum 738554212, 36000 checks
over 3 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The Rust arm joins it
once it checks.

## Mutation testing

Eighteen edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept. Seventeen
are killed, each the same way under both backends and none by a crash;
one survives and is equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a square equal to the pile never taken | P1 1594, P2 413, P5 160, P6 1594 |
| M2 | ★: 1 never taken | P1 1022, P2 221, P3 90, P5 491, P6 1022 |
| M3 | ★: only the odd squares taken | P1 931, P2 844, P3 418, P5 930, P6 931 |
| M4 | ★: `k` stones taken, not `k * k` | P1 459, P3 68, P4 435, P5 163, P6 459 |
| M5 | ★: the pile of 1 left a loss | P1 1514, P2 221, P5 80, P6 1514 |
| M6 | push: winning piles of 3 mod 7 pushed as if they lost | P1 574, P4 72, P6 574 |
| M7 | push: never pushed onto the pile asked for | P1 1226, P2 2000, P3 2000, P5 2000, P6 1226 |
| M8 | push: only the squares up to 9 made wins | P2 256, P3 149 |
| M9 | push: winning piles up to 10 pushed as if they lost | P1 774, P4 1681, P6 774 |
| M10 | iter: `all` for `any` | P1 2000, P2 2000, P3 713, P5 740, P6 2000 |
| M11 | iter: only the first five squares tried | P2 234 |
| M12 | iter: the pile of 5 a win | P1 108, P4 108, P6 108 |

P2 kills nine of the twelve, P1 and P6 ten, P5 six, P3 five, P4 four. M8
and M11 change only piles past 24 (a square of 16 or more, the sixth
square), which the literal reading cannot reach in time, so P1 cannot see
them: P2 and P3 ask about larger piles and do.

The other five killed: the push arm starting at pile 1 and the iterator
arm's `<` for `<=` (both as M1), the iterator arm starting at 2 (as M2),
its squares off by `k - 1` (as M3), and the push arm stepping `k` by
doubling (as M8). One survives and is equivalent: the ★ arm without its
`break` (a pile marked a win stays one).

## Rust template: B-2026-11-08-16 and B-2026-11-08-18

The Rust arm was written as LeetCode's Rust template plus a thin `i64`
wrapper. `karac fix` makes 2 edits and then 1 (`vec![false; n + 1]` to
`Vec.filled(n + 1, false)`, `!` to `not`) and leaves three errors.
`Vec.filled(n + 1, false)` with `n: usize` is B-2026-11-08-16 (a `usize`
length is refused and the `as i64` the message asks for has no fix).
`let mut k = 1; while k * k <= i { .. dp[i - k * k] .. }` with `i: usize`
is B-2026-11-08-18: the literal stays an `i64`, so the comparison and the
subtraction mix `i64` and `usize`, though the same literal bound by `let`
is fixed to `i32` or `u32` by such a use. With `let mut k: usize = 1;`
and `Vec.filled((n + 1) as i64, false)` written by hand, the arm checks
and prints the ★ arm's output.

## Benchmarks

The bench answers 40 piles of 50000 to 100000 stones by the ★ arm in all
five languages, each filling its own table. Every implementation prints
`40 piles of 50000 to 100000 stones: Alice wins 40, checksum 699481692`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `acb9d4c5b` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.110 s |
| Rust (`rustc -O`) | 0.111 s |
| Go | 0.126 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.133 s |
| Kāra (`karac build`) | 0.169 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.174 s |
| Python | 7.64 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is its real time (0.168 s and 0.164 s on one run).

Kāra is 1.31x Rust under overflow checks by median. Under callgrind the
Kāra binary runs 2.08 billion instructions to the checked Rust's 1.53
billion, all of them inside `main` (everything is inlined, no runtime
call shows); where the extra 36% goes in the inner loop was not traced.

## Verification

The ★, push and iterator arms print the same output as `stones.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the ★ arm takes 2.3 s, the push arm 0.6 s, the
iterator arm 20.7 s, and the differential 1.8 s.

## Writing it

The arms were written in Kāra. `karac fix` made one edit, to the iterator
arm: `take_while(|s| *s <= pile)` with the `*` dropped, since `s` is a
copied `i64`.
