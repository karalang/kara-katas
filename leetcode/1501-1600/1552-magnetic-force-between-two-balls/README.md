# 1552. Magnetic Force Between Two Balls

Rick has `n` empty baskets, the `i`-th at `position[i]`, and `m` balls.
Morty wants to put the balls into the baskets so that the minimum magnetic
force between any two balls is as large as possible. The force between two
balls at positions `x` and `y` is `|x - y|`. Given `position` and `m`,
return the largest possible minimum force.

```
position = [1,2,3,4,7], m = 3                 ->  3           (baskets 1, 4 and 7)
position = [5,4,3,2,1,1000000000], m = 2      ->  999999999
```

**Constraints:** `2 <= n <= 10^5`; `1 <= position[i] <= 10^9`; the
positions are distinct; `2 <= m <= n`.

## Approaches

| file | mechanism |
|---|---|
| `magnetic.kara` ★ | a binary search on the answer: with the positions sorted, `m` balls fit at least `gap` apart exactly when placing each ball at the first position `gap` past the last reaches `m`, and fitting is monotone in `gap`, so the largest gap that fits is found by halving `lo..=hi`. O(n log n + n log D) |
| `magnetic_jump.kara` | the same search, each check jumping ball to ball: the next ball's place is the first position at least `gap` past the last, found by `partition_point` on the sorted positions, so a check costs O(m log n) and stops when the positions run out. The search runs on a half-open `lo..hi` from `span / (m - 1) + 1` |
| `magnetic_fold.kara` | the check as a closure holding a `fold` over the sorted positions, its state the count placed and the last ball's position; the search a climb bit by bit from `1 << 30` down, a bit kept when the gap with it still fits |
| `magnetic_solution.kara` | LeetCode's Rust template (`max_distance(position: Vec<i32>, m: i32) -> i32`, the ★ arm over `i32` positions with the check a closure), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples, then
`[1, 2]` with 2, `[1, 2, 3, 4, 5]` with 5, `[1, 100, 101, 200]` with 3,
`[10, 1, 7, 4]` with 4, `[1, 1000000000, 500000000, 2]` with 3 and 100000
positions 10000 apart with 1000 balls; then checksums of the answers for
3000 random baskets of up to 12 distinct positions up to 30, 300 of up to
1000 up to 10^9 and 30 of up to 100000 up to 10^9, in a random order,
each with 2 to all of them balls. `magnetic.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way to choose `m` of the baskets, its force the least
`|x - y|` over every two of its balls, the most of those. It checks 3000
baskets of 2 to 8 distinct positions from 1 to 30 in a random order, each
with 2 to all of them balls, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least 1 and at most the span over `m - 1` |
| P3 | the positions mirrored, `p` to `31 - p`, leave the answer |
| P4 | every position tripled and moved by 5 triples the answer |
| P5 | two balls give the span, and one ball more never widens the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 334684567, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. One first choice for the fold arm, the
`skip(1)` dropped, was equivalent (the first position is then compared
with itself, a gap of 0 that never fits) and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a ball placed only strictly past the gap | P1 2567, P4 3000, P5 2979, P6 2567 |
| M2 | ★: a gap that fails takes two off the top | P1 578, P4 1158, P6 578 |
| M3 | ★: one ball more than `m` needed | P1 2465, P4 1090, P5 2979, P6 2465 |
| M4 | jump: the next ball strictly past the gap | P1 2567, P4 3000, P5 2979, P6 2567 |
| M5 | jump: the search's top one short | P1 1349, P4 1374, P5 2979, P6 1349 |
| M6 | jump: one ball fewer placed | P1 1456, P4 662, P6 1456 |
| M7 | fold: the climb starting at `1 << 3` | P1 672, P4 1590, P5 2267, P6 672 |
| M8 | fold: a placed ball leaves the last position as it was | P1 1525, P2 1323, P3 1724, P6 1525 |
| M9 | template: the positions left unsorted | P1 2226, P3 1457, P4 2190, P5 2614, P6 2226 |
| M10 | template: one ball fewer needed | P1 1676, P2 1128, P6 1676 |

## Benchmarks

The bench builds 20 baskets of 100000 distinct positions up to 10^9 once
and asks each 5 times by the ★ arm, with its own number of balls every
time, in all five languages. Every call copies and sorts the positions,
as the Kāra arm does: Kāra's and Rust's stable `sort`, Go's
`slices.Sort`, C's `qsort` with a comparison function. Every
implementation prints `5 passes over 20 baskets of 100000 positions:
checksum 757775386`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.870 s |
| Kāra (`karac build`) | 0.878 s |
| Rust (`rustc -O`) | 0.886 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.889 s |
| Go | 1.409 s |
| C (`clang -O3`) | 1.800 s |
| Python | 16.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.87 s and 0.88 s on one run).

Kāra is 0.98x Rust under overflow checks by median. Not traced. C is last
because of `qsort`: the same C program with the search taken out, so it
only builds the baskets and sorts them, ran 1.32 to 1.38 s in three runs.

## Verification

All four arms print the same output as `magnetic.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★ and jump arms were written in Kāra and checked as written. The fold
arm's closure was written `|gap: i64| -> bool { .. }`, Rust's spelling;
the parse error names the rewrite and `karac fix` made it, to
`|gap: i64| { .. }`.

The Rust template took 6 changed lines and one added, then 1 and 3, over
three rounds:
`mut position: Vec<i32>` to `position: own Vec[i32]` with a
`let mut position = position` added, the closure's `-> bool` dropped,
`for &p in` to `for p in`, `let (mut lo, mut hi)` to `let mut (lo, hi)`,
the wrapper's `Vec<i32>` and `|&p|` to `Vec[i32]` and `|p|`, and
`Solution::` to `Solution.`; then `struct Solution {}` added; then
`sort_unstable()` to `sort()` (the library has only the stable sort), the
`1` in `(1, position[..] - position[0])` to `1i32`, and the closing
`as i64` dropped. `lo` needs the `1i32` because its literal settles to
`i64` before `can_place(mid)` asks for an `i32` (design.md §8 Literals);
the refusal names `lo` and offers the suffix. It checks and agrees with
no hand edit.
