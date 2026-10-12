# 391. Perfect Rectangle

Each `rectangles[i] = [x1, y1, x2, y2]` is an axis-aligned rectangle with
bottom-left corner `(x1, y1)` and top-right corner `(x2, y2)`. Return
true if together they cover a rectangular region exactly: no gaps and no
overlaps.

```
[[1,1,3,3],[3,1,4,2],[3,2,4,4],[1,3,2,4],[2,3,3,4]]  -> true
[[1,1,2,3],[1,3,2,4],[3,1,4,2],[3,2,4,4]]            -> false  (a gap)
[[1,1,3,3],[3,1,4,2],[1,3,2,4],[2,2,4,4]]            -> false  (an overlap)
```

**Constraints:** `1 <= rectangles.len() <= 2 * 10^4`; each coordinate is
between `-10^5` and `10^5`; `x1 < x2` and `y1 < y2`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `perfect_rectangle.kara` ★ | the areas add up to the bounding box's area, and toggling every corner point in a `Set` leaves exactly the box's four corners | O(n) expected | O(n) |
| `perfect_rectangle_pairs.kara` | no two rectangles overlap (checked pair by pair), and the areas add up to the box's area | O(n^2) | O(1) |
| `perfect_rectangle_sweep.kara` | a sweep line over x with the open y-intervals in a `SortedMap`, closings before openings at the same x, finds any overlap through `floor`; then the area check | O(n log n) | O(n) |
| `perfect_rectangle_grid.kara` | compress the coordinates, paint each rectangle's cells, and require every cell painted exactly once | O(n · cells), O(n^3) at worst | O(n^2) |
| `differential.kara` | the four arms on 3,000 random tilings and edits of them, against the tiling's construction and a unit-cell painting | — | — |

Every arm prints the same 10 lines: the three LeetCode examples, six edge
cases (one rectangle, the same rectangle twice, two pairs stacked on each
other, an overlap and a gap of the same area, a plus sign over four
corners, a row of strips), and for 2,000 random cases how many are
perfect, with a checksum. Each random case is a box of up to 12 x 12 cut
into up to 10 pieces by straight cuts, then left alone or edited (a piece
dropped, copied, moved one step, or grown one step).
`perfect_rectangle.py` mirrors the ★ arm and its output is byte-identical.

The ★ arm's two checks need each other. The area check alone passes an
overlap and a gap of the same area; the corner check alone passes a
tiling with two extra copies of one piece, since the copies' corners
pair up with each other. The differential's P2 covers the second case,
and mutation M1 shows it is needed.

The sweep arm reads the `floor` entry with `if reach > bottom`. The
library gives `floor` as `Option[(ref K, ref V)]`, so the spec form is
`if *reach > bottom`, but `karac check` refuses the `*`: the items are
typed as values (kara `B-2026-10-12-9`). Revert to `*reach` once that is
fixed. The grid arm collects the sorted coordinates with a `for` loop
and `push`. `xs.iter().cloned().collect()` on the `SortedSet` passes
`karac check`, but `karac __mir-run` stops at `an iterator value is not
lowered yet`. That gap is noted for the MIR builder's owner and not
filed.

## Differential

`differential.kara` holds copies of the four arms, the tiling generator,
and `paint`, which marks every unit cell of the bounding box and requires
each to be covered once. For each of 3,000 random tilings:

| | property |
|---|---|
| P1 | every arm says true for the tiling, which covers its box by construction |
| P2 | every arm says false for the tiling with one or two extra copies of one piece |
| P3 | every arm agrees with `paint` on the tiling after one edit (a piece dropped, moved one step, or grown one step) |
| P4 | shifting every rectangle of the edited tiling by the same amount changes no answer |
| P5 | swapping x and y in every rectangle and reversing their order changes no answer |

It prints `3000 tilings, 677 still perfect after the edit, 60000 checks,
0 failures` under `karac __mir-run`, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | corners: no area check | P2 1475 |
| M2 | corners: more than four unpaired corners pass | P3 150 |
| M3 | pairs: rectangles that touch count as overlapping | P5 192 |
| M4 | pairs: overlap tested on the x axis only | P1 2312, P3 192, P5 160 |
| M5 | sweep: at the same x, openings come before closings | P1 2281, P3 140, P5 160 |
| M6 | sweep: an overlap is an open interval reaching the new top | P3 289, P5 78 |
| M7 | grid: only unpainted cells fail | P2 3000, P3 483 |
| M8 | grid: a cell painted twice counts once | P2 3000, P3 483 |

M1 is caught only by the two-copies half of P2, which was added for it:
with one extra copy, its unpaired corners give it away, and a first
version of P2 used only that. M3 is caught only by P5. The generator
pushes the left or lower piece of each cut first, so in a tiling the
earlier rectangle of a touching pair is never the one on the right, and
`a[0] <= b[2]` only matters once P5 reverses the order.

## Verification

All four arms print the same output as `perfect_rectangle.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` and
`karac run --interp`, and `karac check` passes on every file. The
differential prints `60000 checks, 0 failures` on every backend:
`karac __mir-run`, `karac __mir-llvm-run`, `karac run --interp`, LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

The arms run under `karac __mir-llvm-run` since compiler commit
62f5f6de04 added the `String.as_str` native that the harness's `show`,
which takes a `Str`, needs. They do not run on the legacy compiled
backends: LLJIT and both `karac build` modes fail LLVM module
verification at the `show` calls, which pass a string literal where
`show`'s signature does not expect that layout. That is the frozen
legacy codegen, so it is noted and not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 50 tilings of a 100,000 x
100,000 box, each cut into 20,000 pieces (the problem's limit) by
straight cuts, once. Then for 300 rounds it takes a tiling, leaves it
alone or moves or grows one random piece by one step, checks it, and
undoes the edit, folding the answers into a count and a checksum. The
edit keeps the input changing between rounds, so no answer can be
reused. Every implementation prints `300 rounds over 50 tilings of 20000
pieces: 97 perfect, checksum 27986121`. C has no set type, so its
mirror carries an open-addressing hash set with backward-shift deletion,
toggling corners the same way; Rust, Go and Python use their own hash
sets. Spot timings on a shared 4-core container (`bench.sh` timings need
a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.36 s |
| Rust (`rustc -O`) | 0.78 to 0.84 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.79 to 0.81 s |
| Go | 1.28 to 1.30 s |
| Python | 7.0 s |

The Kāra program prints the same line under `karac __mir-run` (53 s on
a release build) and `karac __mir-llvm-run` (86 s), both measured at
kara `338b9f6bbb`. Neither time is a benchmark: the first is the MIR
interpreter, and the second JITs the MIR's IR without optimization
passes. Both predate kara `989568b252`, which made `Map.remove`
O(log n) (`B-2026-10-12-4`). This workload removes a corner for nearly
every one it inserts; whether that commit speeds up its `Set.remove` is
not measured here. At kara `62f5f6de04`, which includes that commit,
`karac __mir-llvm-run` prints the same line in 43.0 s, compile
included. The legacy `karac build` refuses the program: its
frozen typechecker reads `is_rectangle_cover(tilings[t])` as a move out
of an index, where under the v2 rules a bare parameter borrows.

## Compiler findings

- **`SortedMap.floor` and `ceiling` items are typed as values** (kara
  `B-2026-10-12-9`, extended by this kata). The library gives them as
  `Option[(ref K, ref V)]`; `karac check` refuses `*v` on their items
  and accepts `let a: i64 = k;`. The row was filed by kata 389 for
  `Map.iter()`, which has the same shape.
