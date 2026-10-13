# 497. Random Point in Non-overlapping Rectangles

You are given an array of non-overlapping axis-aligned rectangles
`rects` where `rects[i] = [ai, bi, xi, yi]` indicates that `(ai, bi)`
is the bottom-left corner point of the `i`th rectangle and `(xi, yi)`
is the top-right corner point of the `i`th rectangle. Design an
algorithm to pick a random integer point inside the space covered by
one of the given rectangles. A point on the perimeter of a rectangle
is included in the space covered by the rectangle.

Any integer point inside the space covered by one of the given
rectangles should be equally likely to be returned.

Note that an integer point is a point that has integer coordinates.

Implement the `Solution` class:

- `Solution(int[][] rects)` Initializes the object with the given
  rectangles `rects`.
- `int[] pick()` Returns a random integer point `[u, v]` inside the
  space covered by one of the given rectangles.

```
Solution([[-2,-2,1,1],[2,2,4,6]])
pick() -> [1,-2], pick() -> [1,-1], pick() -> [-1,-2], ...
(any of the 31 covered points, each equally likely)
```

**Constraints:** `1 <= rects.length <= 100`; `rects[i].length == 4`;
`-10^9 <= ai < xi <= 10^9`; `-10^9 <= bi < yi <= 10^9`;
`xi - ai <= 2000`; `yi - bi <= 2000`; all the rectangles do not
overlap; at most `10^4` calls will be made to `pick`.

## Approaches

Every arm is a `Solution` with `fn new(rects: own Vec[Vec[i64]], seed:
i64) -> Solution` and `fn pick(mut ref self) -> Vec[i64]`. The problem
allows the language's own random numbers; the arms draw from a seeded
generator of their own (`Draw`, a linear congruential generator giving
15 bits a step), so that every run, and the Python mirror, draws the
same values. `below(n)` puts two steps together into 30 bits and draws
again when they land in the last, incomplete run of `n`, so it is
exactly uniform on `[0, n)`; the most points the rectangles can cover,
100 × 2001², is under 2^30.

| file | mechanism | draws per pick |
|---|---|---|
| `random_point_rects.kara` ★ | prefix sums: number every point rectangle by rectangle and row by row, draw one number below the total, find its rectangle by binary search on the running counts, and turn the rest into a column and a row | 1 |
| `random_point_rects_walk.kara` | the same numbering, but the rectangle is found by walking the rectangles and taking each one's count off the number | 1 |
| `random_point_rects_reservoir.kara` | a weighted reservoir: each rectangle replaces the one kept so far with chance its count over the count seen so far; then the column and the row are drawn separately | one per rectangle, + 2 |
| `random_point_rects_alias.kara` | Walker's alias method in whole numbers: each rectangle's column holds `total` units, its own share (n × its count) as far as it goes and the rest from one larger rectangle; draw a column and a unit, then a point in the rectangle | 3 |
| `differential.kara` | each arm held to five properties |

The ★ and walk arms make the same picks from the same seed; the other
two draw differently, so the harness prints only what every correct
arm must make true. Every arm prints the same 8 lines: for six sets of
rectangles (the LeetCode example; one point; a single column; a row
and a column; squares of 1, 4, 9 and 16 points; two small rectangles
in opposite corners of the range) and a thousand picks per covered
point, whether every pick is covered and whether every point got its
share within 5 standard deviations; for the problem's largest, 100
rectangles of 2,001 by 2,001 spread across the range and 40,000 picks,
whether every pick is covered, every rectangle got its share, and 20
bands of columns and 20 bands of rows got theirs; and whether one seed
twice gives the same 1,000 picks and another seed other ones. All of
them read `true`. `random_point_rects.py` mirrors the ★ arm, draws the
same picks, and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, sharing one copy of
`Draw`. Each arm is held to the properties below on its own: 1,500
random sets of 1 to 8 rectangles of up to 3, 40 or 2,001 on a side in
turn, anywhere in the range, with 20 picks each for P1 and P2, and ten
seeded runs of 8,000 picks for P3 to P5.

| | property |
|---|---|
| P1 | every pick is a point some rectangle covers |
| P2 | the rectangles moved by `(dx, dy)` give the same picks moved by `(dx, dy)` |
| P3 | every point of 1 to 4 rectangles of up to 4 by 4 gets its share, within 5 standard deviations |
| P4 | so does every rectangle, by its count of points |
| P5 | in one rectangle of 2 to 12 by 2 to 12, so does every column and every row |

It prints `1500 cases and 10 runs, 4 arms, 12120 checks, 0 failures`
under `karac __mir-run`.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search stops at a running count equal to the draw | P1 452, P3 8, P4 8 |
| M2 | ★: the column wraps at the height, not the width | P1 1135, P3 9, P4 8, P5 10 |
| M3 | walk: the walk stops one too late | P1 452, P3 8, P4 8 |
| M4 | walk: the row is the column again | P1 1169, P3 9, P4 7, P5 10 |
| M5 | reservoir: a rectangle replaces the kept one with chance its count + 1 over the count seen | P3 7, P4 8 |
| M6 | reservoir: every rectangle is equally likely | P3 7, P4 7 |
| M7 | alias: the larger rectangle gives up the small one's share, not what it lends | P3 5, P4 5 |
| M8 | alias: a unit equal to the kept share stays in the column | P3 1, P4 2 |

M1 and M3 are the same mistake in two arms, and the two arms number
the points alike, so they fail the same 452 cases: the first number of
each rectangle after the first lands in the rectangle before it, one
row past its top. M5 to M8 only bend the chances, so
every pick is still covered and only P3 and P4, which count, see them;
M8 moves one unit in `total` per column, the smallest mistake here,
and fails 3 of the arm's 20 counting checks. P2 kills none of them: every
arm draws the same numbers wherever the rectangles are, which is what
P2 checks, and none of these edits touches a coordinate on its own.

One more edit is not caught, and cannot be at this size: drawing 30
bits and taking them modulo `n` with no redraw. That favours the first
`2^30 mod n` numbers by about `n` parts in `2^30`: under one part in
ten million for the 64 points P3 counts at most, far below what 8,000
picks can see. It gives 0 failures.

## Verification

All four arms print the same output as `random_point_rects.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included.
The differential prints `12120 checks, 0 failures` on both. The four
arms and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on all four arms: LLJIT, legacy
`karac build` and a `KARAC_AUTO_PAR=1` build print the same output, and
so does `karac run --interp` on three of them. On the reservoir arm,
which draws once per rectangle on every pick, `karac run --interp` had
printed the first four lines, all right, when the verification
script's 300 s limit stopped it. The differential under `karac run
--interp` and legacy `karac build` prints `12120 checks, 0 failures`.
Legacy `karac build` warns on every arm that `p` is "moved here, used
again here", where the harness lends a pick to `number_of` and then
reads it; the output is right all the same. Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 500 sets of 100
rectangles (the problem's most) of 1 to 2,001 on a side, spread across
the whole range, once. Then each set gets a fresh solution, on its own
copy of the rectangles, and 10,000 picks (the problem's most). Every
implementation prints `500 sets of 100, 10000 picks each: sum of last
three digits 4572380712, checksum 971804711`, the Kāra program under
`karac __mir-run` included (in 47 s). The sink moves each coordinate
up by 10^9 first, so that no remainder is taken of a negative number,
where Python's `%` differs from the others'.

Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.27 to 0.28 s |
| Rust (`rustc -O`) | 0.30 to 0.32 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.31 to 0.35 s |
| Go | 0.42 to 0.45 s |
| Python | 8.3 s |
| Kāra (legacy `karac build`) | 0.30 to 0.32 s |
| Kāra (`karac build --mir`) | 0.33 to 0.38 s |

Legacy `karac build` builds this program, so `bench.sh` is the
`scripts/new-bench.sh` output unchanged and times the legacy build; the
`--mir` row is timed by hand at kara `d9a7136c58`. Under `karac
__mir-llvm-run` the program prints the same line in 2.0 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends. `karac check` refused two lines of the first ★
draft, and its suggestions were right: storing the rectangles in the
`Solution` needs `rects: own Vec[Vec[i64]]`, since a bare parameter
borrows, and `let r = self.rects[low]` cannot move a row out of the
`Vec`. `karac fix` applied both, the second as `.clone()`, which copies
the row on every pick; the arms use the borrow the same diagnostic
offers, `ref self.rects[low]`. That `karac fix` prefers a copy when one
exists is known and not filed again here.
