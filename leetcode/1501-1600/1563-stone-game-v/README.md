# 1563. Stone Game V

There are several stones arranged in a row, each with an associated value
given in `stoneValue`. In each round of the game, Alice divides the row
into two non-empty rows; Bob calculates the value of each row (the sum of
its stones' values) and throws away the row with the maximum value.
Alice's score increases by the value of the remaining row. If the two
rows are equal, Bob lets Alice decide which row is thrown away. The game
ends when there is only one stone remaining, and Alice's score starts at
zero. Return the maximum score that Alice can obtain.

```
stoneValue = [6,2,3,4,5,5]     ->  18
stoneValue = [7,7,7,7,7,7,7]   ->  28
stoneValue = [4]               ->  0
```

**Constraints:** `1 <= stoneValue.length <= 500`;
`1 <= stoneValue[i] <= 10^6`.

## Approaches

Every row Alice plays on is a stretch of the original, so the best score
of each stretch `[i, j]` is a table over pairs, built from shorter
stretches.

| file | mechanism |
|---|---|
| `stones.kara` ★ | the best of every stretch, shortest first, in a `Vec` of `Vec`s: each split's smaller side (either side when equal) scores its sum plus its own best, sums from a prefix table. O(n³) |
| `stones_memo.kara` | the game searched from the whole row down, each stretch's best kept in a `Map[(i64, i64), i64]` (an `if let` on `get`), through a recursive helper taking `mut ref` the map. O(n³) |
| `stones_quadratic.kara` | O(n²): for a stretch `[i, j]` the splits whose left side is smaller form a run from `i`, and the split point between them moves right as `j` grows; with `left[i][j]`, the best of `sum(i..k) + best[i][k]` over `k` up to `j`, and `right[i][j]` its mirror, each stretch reads its answer in O(1). The sums come from a closure over the prefix table |
| `stones_solution.kara` | LeetCode's Rust template (`stone_game_v(stone_value: Vec<i32>) -> i32`, the ★ arm in `i32`), carried by `karac fix` and one hand edit |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples, then
`[1, 1]`, `[1, 2]`, `[2, 1, 1]`, four stones of 1, `[10, 1, 1, 1]` and 1
to 10; then the total and a checksum of the answers for 3000 random rows
of up to 8 stones of up to 10, 300 of up to 60 and 20 of up to 300 stones
of up to 10^6. `stones.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every round played every way with no table, Alice trying each
split, Bob throwing away the side worth more (Alice picking when they are
equal), until one stone is left. It checks 3000 rows of 1 to 7 stones of
1 to at most 10, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is 0 exactly when there is one stone, and less than the row's sum |
| P3 | the row reversed leaves the answer |
| P4 | every stone doubled doubles the answer |
| P5 | a stone worth the whole row put after it scores at least the row's sum more |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 547185228, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M5, the memo read at `(i, i)`,
was equivalent (no such entry is ever stored, so it only turned the memo
off) and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the larger side kept when the left is smaller | P1 2252, P2 1972, P3 1986, P6 2252 |
| M2 | ★: an equal split always keeps the left | P1 170, P3 311, P6 170 |
| M3 | ★: the first split never tried | P1 1968, P2 429, P3 928, P5 437, P6 1968 |
| M4 | memo: an equal split never keeps the left | P1 180, P3 311, P5 2543, P6 180 |
| M5 | memo: a stretch's best read from the stretch one shorter | P1 211, P3 423, P5 821, P6 211 |
| M6 | quadratic: the split point past an equal split | P1 170, P3 311, P6 170 |
| M7 | quadratic: an equal split's left never kept | P1 180, P3 311, P5 2543, P6 180 |
| M8 | quadratic: `right` never takes the stretch's own score | P1 786, P3 1371, P6 786 |
| M9 | template: the right side's best read one stone early | P1 1552, P2 98, P3 1491, P6 1552 |
| M10 | template: the last stretch of each length skipped | P1 2563, P2 2563, P5 3000, P6 2563 |

## Benchmarks

The bench draws 5 rows of 400 stones of 1 to 10^6 once and asks each
twice by the ★ arm, in all five languages. Kāra, Rust and Go keep the
table as rows of vectors; C keeps it as one block. Every implementation
prints `2 passes over 5 rows of 400 stones: 2009157410 points, checksum
883424553`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.113 s |
| Rust (`rustc -O`) | 0.147 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.189 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.195 s |
| Kāra (`karac build`) | 0.202 s |
| Go | 0.235 s |
| Python | 16.4 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.19 s and 0.19 s on one run).

Kāra is 1.03x Rust under overflow checks by median. Not traced. The
inner loop is two prefix loads, a compare and a load from a row of the
table that changes with every split, so the row lookups C's single block
avoids are a share of every other compiled row.

## Verification

All four arms print the same output as `stones.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, memo and quadratic arms were written in Kāra and checked as
written.

The Rust template took five rounds of `karac fix`, 3 changed lines, then
1 added, then 3, 1 and 1 changed, and then one hand edit:

1. the `Vec<..>` types to `Vec[..]`, the wrapper's `|&v|` to `|v|` and
   `Solution::` to `Solution.`;
2. `struct Solution {}` added;
3. `vec![0; n + 1]` for the prefix sums to `Vec.filled(n + 1, 0)`, the
   inner `vec![0; n]` of the table to `vec![0i32; n]` (from a refusal at
   the `i32` return that names the table's literal as having taken the
   default `i64`), and the wrapper's closing `as i64` dropped;
4. and 5. the table's two `vec!`s to `Vec.filled`.

Three refusals were left, one per `max` call: `` `max` expects an
argument of type `i32`, got `i64` ``. The `i64` is the split's sums,
read from the prefix table, whose literal took the default `i64` when
round 3 rewrote `vec![0; n + 1]`; in Rust that literal is `i32` from its
later uses. The refusal names nothing to change, though the same fix
(`0i32`) is offered for the table's literal when the value reaches the
return. Filed as B-2026-11-14-17. The prefix table's literal was edited
by hand to `Vec.filled(n + 1, 0i32)`, after which the template checks
and agrees.
