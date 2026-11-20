# 1688. Count of Matches in Tournament

You are given an integer `n`, the number of teams in a tournament that
has strange rules:

- If the current number of teams is **even**, each team gets paired with
  another team. A total of `n / 2` matches are played, and `n / 2` teams
  advance to the next round.
- If the current number of teams is **odd**, one team randomly advances
  in the tournament, and the rest gets paired. A total of `(n - 1) / 2`
  matches are played, and `(n - 1) / 2 + 1` teams advance to the next
  round.

Return *the number of matches played in the tournament until a winner is
decided.*

```
n = 7    ->  6
n = 14   ->  13
```

**Constraints:** `1 <= n <= 200`.

## Approaches

| file | mechanism |
|---|---|
| `matches.kara` ★ | the rounds played out: each plays `n / 2` matches and sends `(n + 1) / 2` teams on. O(log n) |
| `matches_closed.kara` | every match sends one team home and all but the winner go home: `n - 1`. O(1) |
| `matches_recursive.kara` | one round of `n / 2` matches, then the same question for the `n - n / 2` teams left, by recursion. O(log n) calls |
| `matches_solution.kara` | a Rust solution as LeetCode's Rust users write it, the parameter shadowed `let mut n = n;` and the rounds in a `while` loop, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 6 lines: LeetCode's two examples, one team,
and 200; then the matches summed and a checksum for every n from 1 to
200, and for 3000 random n up to `10^9`, past LeetCode's bound, where
the round count reaches 30. `matches.py` mirrors the ★ arm and its
output is byte-identical.

```
6
13
0
199
n from 1 to 200: 19900 matches, checksum 901572118
3000 n up to 1000000000: 1403068893074 matches, checksum 255052169
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the teams kept in a list and paired off in order each round,
the first of each pair winning and an odd last team advancing unplayed,
every match counted. It checks 3000 random n from 1 to 200, each with a
split into two smaller tournaments. Every case is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | one team more plays one match more |
| P3 | fewer matches than teams, and none for one team |
| P4 | tournaments of a and n - a teams, and a final between their winners, play as many matches as one of n |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 856659757, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Edits that make the same mistake in
different arms fail the same checks: M2 and M6 play no match between two
teams, M3, M7 and M9 count the odd team's bye as a match, and M8 and M10
start the count at 1.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the odd team out does not advance | P1 2889, P2 2256, P4 2450, P5 2889 |
| M2 | ★: two teams play no final | P1 2989, P2 11, P4 2856, P5 2989 |
| M3 | ★: a bye counted as a match | P1 2889, P2 2258, P3 2889, P4 2559, P5 2889 |
| M4 | closed: the first round only, `n / 2` | P1 2972, P2 1484, P4 2225, P5 2972 |
| M5 | closed: one more for an odd n | P1 1516, P2 3000, P3 3000, P4 764, P5 1516 |
| M6 | recursive: two teams play no final | P1 2989, P2 11, P4 2856, P5 2989 |
| M7 | recursive: a bye counted as a match | P1 2889, P2 2258, P3 2889, P4 2559, P5 2889 |
| M8 | recursive: one team plays one match | P1 3000, P3 3000, P4 2989, P5 3000 |
| M9 | solution: a bye counted as a match | P1 2889, P2 2258, P3 2889, P4 2559, P5 2889 |
| M10 | solution: the count starts at 1 | P1 3000, P3 3000, P4 2989, P5 3000 |

## Benchmarks

The bench draws 500000 random n up to `10^9`, past LeetCode's bound so
that a tournament runs up to 30 rounds, all of them first, then answers
each 40 times by the ★ arm in all five languages. Every implementation
prints `500000 values of n, 40 rounds: 9373638355745360 matches,
checksum 780099700`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.445 s |
| C (`clang -O3`) | 0.508 s |
| Kāra (`karac build`) | 0.560 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.567 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.615 s |
| Go | 0.895 s |
| Python | 33 s |

The sequential Kāra build takes 1.27x Rust's time and 0.92x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.541 s and 0.546 s on one
run).

## Verification

All four arms print the same output as `matches.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The closed and recursive arms checked clean as first written. The ★ arm
began `let mut played = 0`, which keeps the literal's `i64`, and returned
it as the `i32` the signature names; the refusal (E0200) named the
binding, and `karac fix` declared it `played: i32`.

LeetCode's Rust solution took one `karac fix` of 2 edits:
`struct Solution {}` added, and `let mut res = 0` given `: i32` for the
same reason. Its `let mut n = n;`, a mutable copy shadowing the
parameter, carried over as written.

The differential's recursive arm calls itself by name, so its copy
renames the call along with the function. `arm_name` indexes a list of
string literals for a `Str`, as #1662's differential does (B-2026-11-19-131).
