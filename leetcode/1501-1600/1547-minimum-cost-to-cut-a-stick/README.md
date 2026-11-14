# 1547. Minimum Cost to Cut a Stick

Given a wooden stick of length `n` units, labelled from `0` to `n`, and an
array `cuts` of the places to cut it, perform the cuts in any order. The
cost of one cut is the length of the stick being cut, and the total cost
is the sum of the costs of all cuts. Return the minimum total cost.

```
n = 7, cuts = [1,3,4,5]    ->  16   (3, then 5, then 1, then 4: 7 + 4 + 3 + 2)
n = 9, cuts = [5,6,1,4,2]  ->  22
```

**Constraints:** `2 <= n <= 10^6`; `1 <= cuts.length <= min(n - 1, 100)`;
`1 <= cuts[i] <= n - 1`; the cuts are distinct.

## Approaches

| file | mechanism |
|---|---|
| `cut.kara` ★ | an interval DP over the cuts sorted between 0 and `n`: the cheapest way to make every cut strictly inside the piece from point `i` to point `j` is the piece's length plus the best split `k` of the two sides, filled in a `Vec.filled(m, Vec.filled(m, 0))` table shortest piece first. O(m³) |
| `cut_memo.kara` | the same recurrence asked top down: `cheapest(points, i, j, memo)` recursing on both sides, each answer kept in a `Map[(i64, i64), i64]` keyed by the pair (an `if let` on `get`). O(m³) |
| `cut_knuth.kara` | the ★ DP with Knuth's speed-up: the piece's length satisfies the quadrangle inequality, so the best first cut of `(i, j)` lies between those of `(i, j - 1)` and `(i + 1, j)`, kept in a second `split` table. O(m²) |
| `cut_solution.kara` | LeetCode's Rust template (`min_cost(n: i32, cuts: Vec<i32>) -> i32`, the ★ arm over `i32` points and `usize` places), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples, then
`n = 2` with `[1]`, `n = 10` with `[5]` and with `[1, 9]`, `n = 1000000`
with `[1, 999999, 500000]` and `n = 101` cut at every place; then
checksums of the answers for 3000 random sticks of up to 30 with up to 6
cuts, 300 of up to 1000000 with up to 40 and 3 of up to 1000000 with up
to 100, the cuts distinct and in a random order. `cut.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every order of the cuts tried, each cut paying the length of
the piece it falls in. It checks 3000 sticks of 2 to 30 with 1 to 6
distinct cuts in a random order, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least `n` and at most `n` times the number of cuts |
| P3 | the cuts mirrored, `n - c`, leave the answer |
| P4 | the stick and every cut doubled double the answer |
| P5 | the cuts given in reverse order leave the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 35837012, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends; M1 by a crash, an integer overflow,
under both. Two first choices were equivalent and were replaced: an edit to
the pair the memo stores its answer under, and Knuth's `split[i][i + 1]`
started at `i` (the `.max(i + 1)` clamp lifts it anyway).

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the split stopping one short, `i + 1..j - 1` | integer overflow |
| M2 | ★: the piece's length from `points[i + 1]` | P1 3000, P2 1019, P3 2401, P6 3000 |
| M3 | ★: the points left unsorted | P1 3000, P2 3000, P3 2832, P5 2426, P6 3000 |
| M4 | memo: a piece with one cut inside answered 0 (`j - i < 3`) | P1 3000, P2 563, P6 3000 |
| M5 | memo: the last split kept, not the best (`best = here`) | P1 1951, P3 2049, P6 1951 |
| M6 | knuth: the upper bound clamped to the lower one | P1 1970, P3 2049, P6 1970 |
| M7 | knuth: only the first split in range taken | P1 1970, P3 2049, P6 1970 |
| M8 | knuth: the recorded split the range's start, not the best | P1 911, P3 1303, P6 911 |
| M9 | template: the two sides combined by `max`, not `+` | P1 1750, P6 1750 |
| M10 | template: the 0 end left out of the points | P1 3000, P2 1282, P3 1922, P6 3000 |

## Benchmarks

The bench builds 100 sticks of up to 1000000 with up to 100 distinct cuts
once and asks each 4 times by the ★ arm, in all five languages. Every
implementation prints `4 passes over 100 sticks of up to 1000000 with up
to 100 cuts: checksum 976388973`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.015 s |
| Rust (`rustc -O`) | 0.021 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.022 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.022 s |
| Kāra (`karac build`) | 0.022 s |
| Go | 0.028 s |
| Python | 1.25 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time equals its real time (0.02 s and 0.02 s on one run).

Kāra is 1.00x Rust under overflow checks by median. Not traced. The run
is short, about 20 ms, so process start and the table allocations are a
visible share of every compiled row and the differences between them are
small in absolute terms.

## Verification

All four arms print the same output as `cut.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, memo and Knuth arms were written in Kāra and checked as written.

The Rust template took four rounds of `karac fix`: the `Vec<i32>` types
to `Vec[i32]`, `i32::MAX` to `i32.MAX`, `|&c|` to `|c|` and `Solution::`
to `Solution.`; then `struct Solution {}` added; then the inner
`vec![0i32; m]` to `Vec.filled(m, 0i32)` and the closing `as i64` dropped
(an `i32` widens); then the outer `vec![..; m]` to `Vec.filled(m, ..)`.
The nested `vec!` took two rounds, the inner one first. It checks and agrees with no hand
edit.
