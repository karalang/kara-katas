# 447. Number of Boomerangs

You are given `n` distinct points in the plane, `points[i] = [x_i, y_i]`.
A boomerang is a tuple of points `(i, j, k)` such that the distance
between `i` and `j` equals the distance between `i` and `k`; the order
of the tuple matters. Return the number of boomerangs.

```
points = [[0,0],[1,0],[2,0]]  ->  2   ([[1,0],[0,0],[2,0]] and [[1,0],[2,0],[0,0]])
points = [[1,1],[2,2],[3,3]]  ->  2
points = [[1,1]]              ->  0
```

**Constraints:** `1 <= n <= 500`; `-10^4 <= x_i, y_i <= 10^4`; all
points are distinct.

## Approaches

Every arm is `fn number_of_boomerangs(points: Vec[(i64, i64)]) -> i64`
and compares squared distances, which stay integers (at most 8·10⁸)
and keep equal distances equal.

| file | mechanism |
|---|---|
| `number_of_boomerangs.kara` ★ | a map of distances per point: count the points at each squared distance from `i`; `c` of them at one distance give `c * (c - 1)` ordered pairs `(j, k)`. O(n²) expected time, O(n) extra space |
| `number_of_boomerangs_sorted.kara` | per point, sort the squared distances to the others and count each run of `c` equal ones as `c * (c - 1)`. O(n² log n) |
| `number_of_boomerangs_pairs.kara` | each unordered pair's distance computed once and recorded in both points' maps; a point that already has `c` others at that distance gains `2 * c` boomerangs. O(n²) expected time, O(n²) space |
| `number_of_boomerangs_brute.kara` | the plain reference: every ordered triple of distinct points. O(n³) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 7 lines: the three LeetCode examples, a plus
sign of five points, five points on a circle of radius 5 around the
origin, the corners of the full coordinate range, and for 300 random
sets of 1 to 80 distinct points (60 at most on the smallest grid) on
grids of side 10, 20, 1,000 or 20,001, the total count and a checksum.
`number_of_boomerangs.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random sets of 1 to 20 distinct points on grids of side 6, 10,
40 or 20,001. The sets are small because the brute-force arm is cubic.

| | property |
|---|---|
| P1 | the count is the reference's: every (point, squared distance) pair over all the others, sorted, with each run of `c` equal pairs counted as `c * (c - 1)` |
| P2 | turning the points a quarter and moving them keeps the count |
| P3 | mirroring the points and scaling them by 1 to 3 keeps it |
| P4 | listing the points in a random order keeps it |
| P5 | `m` points in a row (`m` up to 20), one apart, hold twice the sum over each point of the number of points to its nearer end |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | maps: unordered pairs `(j, k)` are counted | P1 826, P2 826, P3 826, P4 826, P5 1335 |
| M2 | maps: distances are Manhattan | P1 931, P2 931, P3 931, P4 931 |
| M3 | sorted: only later points are listed | P1 790, P2 790, P3 790, P4 786, P5 1335 |
| M4 | sorted: runs are cut at two | P1 440, P2 440, P3 440, P4 440 |
| M5 | pairs: a new point pairs with the old ones in one order only | P1 826, P2 826, P3 826, P4 826, P5 1335 |
| M6 | pairs: points next to each other in the list are never paired | P1 737, P2 737, P3 737, P4 716, P5 1335 |
| M7 | brute: `j` and `k` may be the same point | P1 1428, P2 1428, P3 1428, P4 1428, P5 1413 |
| M8 | brute: the last point is never `k` | P1 637, P2 637, P3 637, P4 612, P5 1335 |

P2 to P4 compare against the reference count of the untransformed
points, so a mutant that miscounts every set also fails them; only the
mutants that depend on the points' order (M3, M6, M8) fail P4 a little
less often, since the shuffle moves which points they skip. P5 misses
M2 and M4: on a row, Manhattan and straight-line distances agree, and
no distance from a point in a row is shared by more than two others.
M1 and M5 both halve every count and fail the same 826 sets, those
with any boomerang at all.

## Verification

All four arms print the same output as `number_of_boomerangs.py`
under `karac __mir-run` (the v2 MIR interpreter) and
`karac __mir-llvm-run`, and `karac check` passes on every file. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

On the frozen legacy backends the maps and sorted arms match under
`karac run --interp`, and the brute-force arm matches on the six fixed
cases but does not finish the random ones within 300 s there. The pairs
arm fails under `karac run --interp` on `total += 2 * *c` after
`let c = counts[p].entry(d).or_insert(0)` ("operator 'Mul' is not
defined for operands of type 'Int' and 'Unit'"), and the differential
stops on the same line. LLJIT and `karac build` stop in the legacy code
generator on the harness's index into an array literal, and on the
pairs arm's `or_insert` on an indexed map. The bench program builds and
matches under legacy `karac build`. Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10 random sets of 1,000
distinct points on a 300 x 300 grid once, then counts the boomerangs in
each. Every implementation prints `10 sets of 1000 points: 743214
boomerangs, checksum 771091481`, the Kāra program under
`karac __mir-run` included.

The mirrors keep the ★ arm's structure: a fresh hash map per point
from squared distance to count. Rust's `HashMap` hashes with SipHash,
as Kāra's `Map` does; Go uses its built-in map; C uses the small
open-addressing table of #446 (linear probing, a 64-bit mixing hash).

### Apple M5 Pro, 2026-11-07

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14787+g97681763d`
(g97681763d, the v2/MIR backend), measured 2026-11-07, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first M5 measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| **kāra `karac build`, seq** | **168.9 ms ± 1.2** | **—** |
| c `clang -O3` | 211.8 ms ± 1.5 | 0.80× |
| rust `-O` | 298.0 ms ± 1.5 | 0.57× |
| rust `-O -C overflow-checks=on` (equal-safety) | 304.1 ms ± 4.9 | 0.56× |
| go `go build` | 391.5 ms ± 8.3 | 0.43× |

Kāra is 0.57× `rustc -O`, 0.56× equal-safety Rust, 0.80× C and 0.43× Go. The gaps were not investigated on this host. Against the legacy backend (exact counts, dd86e3955, `KARAC_AUTO_PAR=0`) Kāra executes 0.54× the instructions in 0.55× the cycles.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 49.8 ms ± 0.8 | 32.8 KiB | 1.6 MiB |
| rust | 144.9 ms ± 2.7 | 474.2 KiB | 1.7 MiB |
| kāra | 135.2 ms ± 3.2 | 67.1 KiB | 1.5 MiB |
| go | — | 2450.8 KiB | 8.9 MiB |

`karac build` is 2.7× clang's cold compile and 0.9× rustc's. Kāra's
68,744-byte binary is 2.0× clang's and 7.1× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`10 sets of 1000 points: 743214 boomerangs, checksum 771091481`).

### Container x86-64 history

Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.43 to 0.55 s |
| Rust (`rustc -O`) | 0.47 to 0.54 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.47 to 0.49 s |
| Go | 0.85 to 0.89 s |
| Python | 2.7 to 3.0 s |
| Kāra (legacy `karac build`) | 0.67 to 0.69 s |

The Kāra program prints the same line under `karac __mir-llvm-run` in
19 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

kara B-2026-10-14-3, filed from this kata by another session after it
was written and fixed in kara 605f5270da: the row reports that the
every-triple arm, `number_of_boomerangs_brute.kara`, took 87 s under
`karac __mir-run`, past the corpus runner's 60 s cap, with its output
correct. The cost was in how the MIR interpreter calls a small function
with checked arithmetic, `squared_distance` here, about 77M times. Those
times are the row's measurements, not ones taken for this README.
