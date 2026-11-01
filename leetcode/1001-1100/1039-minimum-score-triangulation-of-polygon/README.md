# 1039. Minimum Score Triangulation of Polygon

You have a convex `n`-sided polygon where each vertex has an integer
value. You are given an integer array `values` where `values[i]` is the
value of the `i`th vertex in clockwise order.

Polygon triangulation is a process where you divide a polygon into a
set of triangles, and the vertices of each triangle must also be
vertices of the original polygon. Note that no other shapes other than
triangles are allowed in the division. This process will result in
`n - 2` triangles.

You will triangulate the polygon. For each triangle, the weight of that
triangle is the product of the values at its vertices. The total score
of the triangulation is the sum of these weights over all `n - 2`
triangles.

Return the minimum possible score that you can achieve with some
triangulation of the polygon.

```
values = [1,2,3]          ->  6
values = [3,7,4,5]        ->  144
values = [1,3,1,4,1,5]    ->  13
```

**Constraints:** `n == values.length`; `3 <= n <= 50`;
`1 <= values[i] <= 100`.

## Approaches

Every arm rests on one split: in any triangulation the edge from vertex
`i` to vertex `j` is a side of exactly one triangle, whose third vertex
`k` lies between them, and that triangle leaves the polygons `i..k` and
`k..j` to triangulate on their own.

| file | mechanism |
|---|---|
| `triangulation.kara` ★ | interval table, by length: `best[i][j]`, the least score for the vertices `i` to `j`, is the least over `k` of `best[i][k] + best[k][j] + v[i] v[k] v[j]`, filled for ever longer stretches in a `Vec` of rows. O(n^3) time, O(n^2) space |
| `triangulation_memo.kara` | recursion with a memo: the same split asked from the top, each answer kept in a table that holds -1 until it is known. O(n^3) |
| `triangulation_flat.kara` | one flat table, filled from the last vertex back: `best[i * n + j]` needs only a larger `i` or a smaller `j`, so `i` runs from `n - 3` down and `j` from `i + 2` up. O(n^3) |
| `triangulation_map.kara` | the answers kept in a Map: the memo arm's recursion with a `Map[(i64, i64), i64]` keyed by the stretch's two ends. O(n^3) |
| `triangulation_iter.kara` | each entry the min of an iterator: the ★ table with every entry written as `(i + 1..j).map(..).min()`, a closure reading the shorter stretches. O(n^3) |
| `differential.kara` | the five arms against the statement read literally, four properties |

Every arm prints the same 15 lines: the answers for eight polygons,
LeetCode's three examples among them, with all values 100, all values
1, alternating values and a polygon of 20; for every polygon of 3 to 7
vertices with values from 1 to 3 (3^n of each), a total and a checksum;
the same for 300 random polygons of 3 to 50 vertices with values from 1
to 100; and the two largest, 50 vertices of 100 (48000000) and the
values 1 to 50 (41648, the fan from vertex 1). `triangulation.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: it lists every triangulation of the polygon, choosing
the third vertex of the triangle on the edge `i..j` in every way and
pairing every triangulation of the part on one side with every one on
the other, and takes the least score in the list. The list's length is
checked against the Catalan number `C(n - 2)`. It checks 1540 polygons:
every polygon of 3 to 6 vertices with values from 1 to 3 (1080), 400
random ones of 3 to 8 vertices and 60 of 9 to 50, values 1 to 100. The
1480 of at most 8 vertices are searched in full.

| | property |
|---|---|
| P1 | the statement read literally, on at most 8 vertices, with `C(n - 2)` triangulations listed |
| P2 | turning the polygon by a random number of places changes nothing |
| P3 | walking it the other way round changes nothing |
| P4 | scaling every value by `c` from 2 to 5 scales the score by `c^3` |
| P5 | the score is at least `n - 2` triangles of the smallest value cubed, and at most the fan from any one vertex |
| P6 | each arm agrees with at least two of the other four |

The differential prints `1540 polygons (1480 searched in full):
checksum 631041131, 45900 checks over 5 arms: 0 failures` under `karac
__mir-run` (14.8 s), `karac __mir-llvm-run` and `karac __mir-llvm-asan`
with no error, and the same line under `karac run` and from a `karac
build` binary.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with a 120 s limit.
Fifteen are kept, three to each arm. All fifteen are killed, each
fails the same way under both backends, and no two kept ones fail the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the triangle's far corner read as its apex | P1 1399, P2 1188, P3 1337, P5 1150, P6 1459 |
| M2 | ★: the right part left out | P1 1352, P2 975, P3 1120, P5 362, P6 1412 |
| M3 | ★: triangles of three vertices never scored | P1 1480, P2 849, P5 340, P6 1540 |
| M4 | memo: every split one short | P1 1480, P4 1540, P5 72, P6 1540 |
| M5 | memo: the stored answer one more than the returned one | P1 898, P2 724, P3 1056, P4 958, P5 882, P6 958 |
| M6 | memo: a sum where a product belongs | P1 1360, P2 938, P3 1226, P4 1540, P5 836, P6 1420 |
| M7 | flat: the answer read one place early | P1 1460, P2 954, P3 1086, P5 353, P6 1520 |
| M8 | flat: a stretch never worse than the one a vertex shorter | P1 1480, P5 1540, P6 1540 |
| M9 | flat: the search started at `1000000 * n`, below some answers | P4 182 |
| M10 | map: the right part one vertex short | P1 1339, P2 979, P3 1172, P5 168, P6 1399 |
| M11 | map: the first third vertex never kept | `integer overflow` |
| M12 | map: an edge scored as 1 | P1 1480, P4 1540, P5 1507, P6 1540 |
| M13 | iter: the last third vertex never tried | `called unwrap() on None` |
| M14 | iter: the largest split kept | P1 1359, P5 1419, P6 1419 |
| M15 | iter: the answer without the first vertex | P1 1460, P2 954, P3 1086, P5 371, P6 1520 |

Of the thirteen that run to the end, P1, P5 and P6 kill twelve, P2
eight, P3 seven and P4 five. The one only P4 sees is M9: a triangle
of values up to 100 weighs at most 10^6, so a search started at
`1000000 * n` is above every answer on the polygons as given, and only
scaling them by up to 5^3 lifts some answers past it. P4 also sees the
edits that add a constant (M4, M12) or mix sums into products (M6),
since those do not grow by `c^3`, and M5, whose stored answers run one
ahead of the returned ones. P2 and P3 see only the edits that break
the polygon's symmetry. Both miss the ones that make the same error
whichever way the polygon is turned or walked (M4, M8, M12, M14), and
P3 misses M3 as well. M11 and M13 never print:
the first runs a sum past `i64.MAX` once no split is kept, and the
second takes the minimum of a range left empty for triangles.

Fifteen other edits were tried and set aside. One is equivalent: the
iter arm's triangle written as `v[i] v[k] v[j] v[0] / v[0]`, which
divides exactly. Two ran past the limit under both backends, since
both empty the memo of the Map arm: answers stored under the ends
turned round, and a stretch looked up under the one a vertex longer;
the recursion is then exponential. The other twelve were killed too,
beyond three per arm. Four overflow as M11 does: ★ never trying the
last third vertex or keeping the largest split, and the memo arm never
trying the first third vertex or keeping the largest split. Three fail
as M2 does: the flat arm filled from the first vertex forward or
reading the right part transposed, and the iter arm reading the right
part as the whole. Two fail as M8 does: ★ skipping the last stretch
of each length, and the iter arm skipping every stretch from vertex 0.
Two fail as M3
does: the memo arm scoring a triangle as nothing, and the flat arm
never scoring triangles of three vertices. One fails as M15 does: the
Map arm leaving the first vertex out.

## Verification

Every arm prints the same output as `triangulation.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error. `karac run` and a `karac build` binary print the same
output for every arm and the differential. `karac check
--output=json` reported nothing on any file. The release build is kara
`6697158faf`, with runtime archives rebuilt at that commit. Under
`karac __mir-run` the arms take 1.0 s (flat) and 1.2 s (★) to 3.4 s
(memo), 5.4 s (map) and 6.7 s (iter, whose closure is called once per
third vertex). Compiled, the iter arm's harness ran in 10 ms against
★'s 6 ms (three runs each, inferred to be the closure call, not
profiled). No gap turned up.

## Benchmarks

The bench builds 2000 random polygons of 50 vertices (the problem's
most) with values from 1 to 100 once in all five languages, then
solves every one 10 times with the ★ arm, adding each score to a total
and folding it into a checksum. Each call allocates its own table: a
`Vec` of rows in Kāra and Rust, a slice of slices in Go, a Python list
of lists, and one `calloc` in C. Every implementation prints `2000
polygons of 50 vertices, 10 rounds: total 6636548320, checksum
640656637`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.296 to 0.388 s | 0.311 s |
| Rust (`rustc -O`) | 0.511 to 0.656 s | 0.561 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.721 to 0.821 s | 0.750 s |
| Go | 0.842 to 1.003 s | 0.901 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.971 to 1.013 s | 0.991 s |
| Kāra (`karac build`) | 0.950 to 1.116 s | 0.993 s |
| Python | 54.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(1.12 s real, 1.10 s user on one run) and runs as fast as the
sequential one.

Kāra took 1.32 times Rust's median time under overflow checks. Rust
without them is faster still, so a good part of the cost is the
checked multiply-add in the inner loop; C's flat table and unchecked
arithmetic lead both (inferred from the sources, not profiled).
