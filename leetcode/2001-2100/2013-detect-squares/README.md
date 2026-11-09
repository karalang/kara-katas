# 2013. Detect Squares

You are given a stream of points on the X-Y plane. Design a structure that
adds each new point to a data structure (duplicate points are allowed and
counted apart), and given a query point, counts the ways to choose three
points from the structure such that they and the query point form an
axis-aligned square of positive area.

- `DetectSquares()` starts with an empty structure.
- `add(point)` adds `point = [x, y]`.
- `count(point)` returns the number of ways described above.

```
add([3,10]); add([11,2]); add([3,2])
count([11,10])  ->  1
count([14,8])   ->  0
add([11,2])
count([11,10])  ->  2
```

**Constraints:** `point.length == 2`; `0 <= x, y <= 1000`; at most 3000
calls to `add` and `count` in total.

A square through the query `(x, y)` is fixed by its opposite corner
`(px, py)`, which needs `|px - x| == |py - y| > 0`; its other two corners
are then `(x, py)` and `(px, y)`, and the ways multiply the three counts.

## Approaches

| file | mechanism |
|---|---|
| `squares.kara` ★ | the counts on a 1001 by 1001 grid whose rows are filled on first use, each distinct point also kept once in a list; a count walks the list for opposite corners. O(1) per add, O(distinct) per count |
| `squares_map.kara` | the counts in a `Map` from point to count; a count walks the map's entries for opposite corners and looks up the other two. O(1) per add, O(distinct) per count |
| `squares_columns.kara` | a `Map` from each x to a `Map` of the counts in that column; a count walks its own column, each other point there fixing the side, and looks for the square to the left and to the right. O(column) per count |
| `squares_brute.kara` | every point added kept in a list, repeats and all; a count takes each as an opposite corner and walks the list again for copies of the other two. O(n^2) per count |
| `squares_sorted.kara` | the counts in a `SortedMap` keyed by `(x, y)`, so a column is one run of keys read with `range_inclusive`; each other point there closes a square on each side. O(column log n) per count |
| `squares_solution.kara` | LeetCode's Rust template (`HashMap<(i32, i32), i32>`, `&mut self`, `for &(px, py) in &self.pts`, `self.cnt[&(px, py)]`, `get(&..).unwrap_or(&0)`), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: the answers for LeetCode's example and
four more counts, one of them a square on the grid's far corners; then the
sum and a checksum of the answers for 200 runs of 1 to 40 operations on
patches of 1 to 6 points a side, and for 4 runs of 400 operations on
patches of 10, 20, 40 and 1001 a side. `squares.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the
statement read literally: for each count, every three of the points added
so far (copies counted apart), kept when the four points have two x values
and two y values the same distance apart. It checks 600 problems of 1 to 25
operations on patches of 1 to 5 points a side, each one in 2 to 4 a count.
Every random choice of a problem (the operations, a move) is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every point's x and y swapped leaves the answer |
| P3 | every point moved by the same `(dx, dy)` leaves the answer |
| P4 | every `x` turned into `1000 - x` leaves the answer |
| P5 | every add made twice multiplies each count by 8 |
| P6 | each arm agrees with at least three of the other five |

The differential prints `600 problems: checksum 204827795, 21600 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each of the five Kāra arms and two to the Rust arm. All thirty are killed,
each fails the same way under both backends, none by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the query's own point taken as its opposite corner | P1 386, P6 386 |
| M2 | ★: a point counted once however often added | P1 126, P5 154, P6 126 |
| M3 | ★: the third corner read at the query | P1 186, P2 177, P6 186 |
| M4 | map: the corner `(x, py)` read as `(py, x)` | P1 153, P3 1, P4 1, P6 153 |
| M5 | map: every add counted twice | P1 154, P6 154 |
| M6 | map: only the squares above the query | P1 104, P2 111, P6 104 |
| M7 | columns: the far corner read on the query's row | P1 222, P2 154, P6 222 |
| M8 | columns: the column point's count left out | P1 99, P2 109, P5 154, P6 99 |
| M9 | columns: an empty column answered with 1 | P1 390, P2 266, P5 390, P6 390 |
| M10 | brute: the same row matched on `y` alone | P1 206, P2 224, P6 206 |
| M11 | brute: the opposite corner never checked for a diagonal | P1 237, P2 239, P6 237 |
| M12 | brute: the two corners' counts added | P1 279, P5 279, P6 279 |
| M13 | sorted: the column's first point skipped | P1 119, P2 98, P6 119 |
| M14 | sorted: the far corner read at `(y2, px)` | P1 154, P3 1, P4 1, P6 154 |
| M15 | sorted: the row's corner taken as at most 1 | P1 87, P2 109, P5 154, P6 87 |
| M16 | Rust: the corner `(px, y)` read at `(py, x)` | P1 154, P2 1, P3 1, P4 1, P6 154 |
| M17 | Rust: a missing corner counted as one | P1 170, P2 239, P5 170, P6 170 |

P1 and P6 kill all seventeen, P2 eleven, P5 six, and P3 and P4 three
each. P2 swaps the axes, so it sees every edit that treats x and y
unevenly: a corner read on the wrong axis (M3, M7, M10), squares sought
only above (M6), a column walk that skips or miscounts (M8, M9, M13, M15),
the opposite corner unchecked (M11), and a missing corner counted as one
(M17). It misses the edits that are symmetric in x and y: the query's own
point as its corner (M1), multiplicities wrong (M2, M5, M12), and two of
the three that read a corner with its coordinates swapped (M4, M14); the
Rust arm's swap (M16) reads `(py, x)` for the corner on the query's row,
which the axis swap turns into a different point, and it fails once. P5
sees the edits that get a count's multiplicity wrong (M2, M8, M9, M12,
M15, M17), and misses every add counted twice (M5), which is wrong by the
same factor before and after the doubling. P3 and P4 catch only the three
coordinate swaps, once each: such an edit reads the wrong point before a
move and after it alike, and differs only in the one problem where the
swapped point lands on a point that was added.

The other thirteen fail as a kept one does, or with counts of their own.
The query's own row taken as a side in the columns arm fails as M1; only
the diagonals rising to the right (★) as only the square to the right
(columns), P1 111 and P4 153; only the diagonals falling to the right (map)
as only the square to the left (sorted), P1 104 and P4 153; a repeat point
listed again, in the ★ and Rust arms, the opposite corner's count left
out, in the map and Rust arms, and the far corner's count squared (sorted)
alike, P1 91 and P5 154; only one copy of a corner counted (brute) as M8.
The brute arm's column corner looked for on the query's row, and the Rust
arm's diagonals with `x` below the query only (P1 104, P2 111, P4 154),
fail with counts of their own. One draft was replaced: the sorted arm
reading its column only up to `y = 999` never fails, since no problem
draws a `y` of 1000.

## Verification

Every arm prints the same output as `squares.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.14 s (columns) to 0.27 s (★) and
the differential 8.6 s.

The five arms were written in Kāra and checked clean. The ★ arm first kept
a full 1001 by 1001 grid per structure, which took 45 s under the
interpreter for the harness's runs; its rows are now filled on first use.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in four rounds (23, 2, 11 and 1 edits).
The first three carry the `use`, `HashMap<..>` and `Vec<..>`, `&mut self`
and `&self`, the `::` paths, `&&`, the pattern `&(px, py)` over
`&self.pts`, and the `&`s on the map's keys and on `unwrap_or(&0)`. That
leaves `let mut ans = 0;` returned as the method's `i32`: the `0` took
`i64` where it was written, where Rust types it `i32` from the `+=` of the
counts' product. Under the ruling in design.md §8 an operator's operand
does not fix a literal, so that is by design; the fourth round writes the
fix the ruling names, `ans: i32` at the binding (B-2026-11-08-20).
`self.cnt[&(px, py)]`, a map indexed by a borrowed key, drew the general
fix to `ref (px, py)` and then a refusal ("only `ref <sequence>[i]` is
supported") with no way on; since kara 68a1f7ae64 the fix drops the `&`.

Under `karac __mir-llvm-asan` the Rust arm first stopped with a
stack-buffer-overflow in `add`: `self.cnt.entry(p).or_insert(0)` over a
`Map[(i32, i32), i32]` built its `0` as an `i64`, and the compiled program
wrote 8 bytes into the entry's 4-byte value. The other lanes printed the
right answer. That was B-2026-11-08-69, fixed in kara 1de47226fa.

## Benchmarks

The bench runs 20 structures of 20000 operations each in all five
languages, each on a 60 by 60 patch of the grid, one operation in three a
count: 133858 counts, each walking up to 3600 distinct points. Every
implementation prints `133858 counts: sum 131732445, checksum 470799517`.
Every language fills a grid row on first use and keeps the distinct points
in a growable list, as the Kāra program does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.535 to 0.590 s | 0.542 s |
| Rust (`rustc -O`) | 0.536 to 0.688 s | 0.556 s |
| Go | 0.656 to 0.746 s | 0.673 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.830 to 0.883 s | 0.847 s |
| Kāra (`karac build`) | 0.854 to 0.925 s | 0.894 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.535 to 2.622 s | 2.586 s |
| Python | 30.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.883 s) is not above its real time (0.894 s).

The sequential Kāra program is 0.33x Rust under overflow checks and 1.56x
C.