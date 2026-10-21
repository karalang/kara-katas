# 835. Image Overlap

You are given two binary images `img1` and `img2`, square matrices of
size `n x n` holding only `0`s and `1`s. Translate one image however you
choose, sliding all its `1` bits left, right, up and/or down by any
number of units, and lay it on top of the other; its overlap is the
number of positions that hold a `1` in both images. A translation does
not rotate the image, and any `1` bit moved outside the matrix borders
is erased. Return the largest possible overlap.

```
img1 = [[1,1,0],[0,1,0],[0,1,0]], img2 = [[0,0,0],[0,1,1],[0,0,1]]  ->  3
img1 = [[1]], img2 = [[1]]                                           ->  1
img1 = [[0]], img2 = [[0]]                                           ->  0
```

**Constraints:** `n == img1.length == img1[i].length == img2.length ==
img2[i].length`, `1 <= n <= 30`, and every cell is `0` or `1`.

## Approaches

Every arm slides the first image over the second; a shift by `(dr, dc)`
moves a one at `(r, c)` to `(r + dr, c + dc)`, and there are `(2n -
1)^2` shifts that leave any cell inside the square.

| file | mechanism |
|---|---|
| `largest_overlap.kara` ★ | shifts counted over pairs of ones: every pair of a one in each image votes for the shift between them, in a flat table of the `(2n - 1)^2` shifts, and the most votes is the answer. O(ones1 * ones2 + n^2) |
| `largest_overlap_brute.kara` | every shift tried: for each shift, the cells that stay inside the square compared with the second image and the ones both hold counted. O(n^4) |
| `largest_overlap_bits.kara` | rows as bit masks: each row an integer with a bit per one, a shift moving rows down and bits left or right, the bits leaving the square cut off by a mask, and each landed row ANDed with the row under it and its ones counted with `count_ones`. O(n^3) word operations |
| `largest_overlap_map.kara` | as the ★ arm, but the votes kept in a `Map` keyed by the shift, so only shifts some pair gives are stored. O(ones1 * ones2) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 14 lines: LeetCode's three examples; seven
more (two full images, a single one that must travel from one corner to
the other and back, two checkerboards, a full image against an empty
one, a square that must move up and left, and a cross against a ring);
three pairs of LeetCode's greatest size, 30 by 30, with ones at 50%, 5%
and 95%; and 100 random pairs of 1 by 1 to 30 by 30 at any density, with
their total and a checksum. `largest_overlap.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for every shift, the first image is copied into a fresh
square of zeros at its new place, the cells moved outside dropped, and
the cells holding a one in both it and the second image counted. Its
1,600 cases come in four kinds of 400: images of 1 by 1 to 4 by 4 at any
density; images up to 10 by 10 at any density; images up to 10 by 10
with 0 to 3 ones each, so the best shift may reach a corner; and a
random image against itself moved by a random shift with up to 5% of its
cells flipped.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the two images swapped give the same answer |
| P3 | both images transposed give the same answer |
| P4 | both images turned half a turn give the same answer |
| P5 | the answer is no more than either image's ones, at least the overlap with no shift, and at least 1 when both images hold a one |

It prints `1600 cases, 32000 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the shift keyed by the sum of its two parts | P1 852, P5 731 |
| M2 | ★: the second image's ones read from the first | P1 1022, P2 1147, P5 726 |
| M3 | ★: a vote setting its shift to 1, not adding 1 | P1 723, P5 615 |
| M4 | every shift: only shifts down tried | P1 130, P2 269, P3 206, P4 269, P5 40 |
| M5 | every shift: the second image's first column left out | P1 650, P2 407, P3 515, P4 578, P5 527 |
| M6 | every shift: cells with a one in either image counted | P1 1319, P5 1319 |
| M7 | bits: a shift right taken as a shift left | P1 134, P2 271, P3 216, P4 271, P5 53 |
| M8 | bits: the second image's first row left out | P1 642, P2 381, P3 515, P4 585, P5 531 |
| M9 | bits: the furthest shift down not tried | P1 115, P2 20, P3 30, P4 20, P5 115 |
| M10 | map: the shift keyed by its row alone | P1 913, P3 634, P5 815 |
| M11 | map: a new shift's count starting at 2 | P1 1177, P5 604 |
| M12 | map: each image's first column left out | P1 775, P3 539, P4 599, P5 594 |

P1 kills all twelve and P5 all twelve as well. P2, the images swapped,
sees only the edits that treat the two images differently or one
direction of shift differently (M2, M4, M5, M7 to M9); the other six
treat both images alike and come out the same when every shift is turned
round. P3, the images transposed, sees the edits that treat rows and
columns differently, and P4, the images turned, those that treat one
side of the square or one direction of shift differently; neither sees
M10, since turning both images turns every shift round and keying by the
row alone loses the same columns either way. M9 is the weakest kill,
with 115 failures: only a pair whose best shift moves a one from the top
row to the bottom row needs the furthest shift down, and the third kind
of case, with a few ones each, builds most of them.

Two edits first tried are equivalent mutants and were replaced: one part
of the shift taken the other way round in the ★ arm (`r1 - r2` for `r2 -
r1`) and in the map arm (`c1 - c2` for `c2 - c1`). Both rename the
shifts one for one, so the votes fall into the same counts under other
names and the largest count does not change; both survived every case. A
third is equivalent by the same check: the bit-mask arm with its mask
`full` left off. The bits a shift pushes past the last column meet only
zeros in the second image's row, so the AND drops them anyway, and the
mask is there to keep each moved row inside the square, not for the
count.

## Verification

Every arm prints the same output as `largest_overlap.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `13fdc32828`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 1.6 s (bit
masks), 5.5 s (★), 14 s (every shift) and 23 s (map), and the
differential 26 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy JIT (`karac run`), `karac build` and an auto-parallel
build print the same output for all four arms and the differential, and
the legacy interpreter (`karac run --interp`) prints the differential's
line. The legacy interpreter does not finish any arm within 60 s: it
prints the small cases and stalls in the three 30 by 30 pairs. Legacy
`karac build` refuses the bench program as moving an image out of
`images[2 * k]`, which v2's borrowing parameters do not do. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
pairs of images once, each of LeetCode's greatest size, 30 by 30, the
share of ones running from 2% to 98% over the pairs. Each of 4,000
rounds solves the next pair. Every implementation prints `4000 rounds of
64 pairs: overlaps total 1183127, checksum 267528664`, the Kāra program
under `karac __mir-run` included, in 582 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.92 to 1.12 s |
| Rust (`rustc -O`) | 1.37 to 1.49 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.41 to 2.75 s |
| Go | 1.87 to 2.13 s |
| Python | 123 to 125 s |
| Kāra (`karac build --mir`) | 2.94 to 3.44 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 3.12 s, against C's
1.06, Rust's 1.43 (2.52 under overflow checks) and Go's 1.89: 1.24 times
Rust's time under overflow checks, 2.9 times C's and 1.65 times Go's.
Under valgrind's cachegrind C runs 14.4 billion instructions and 0.68
billion branches, Rust 18.1 and 2.27 billion, and v2 41.3 and 10.7
billion, nearly all of them conditional and almost never mispredicted.
The work is the inner loop over pairs of ones, 1.05 billion votes in
all, and per vote v2 spends about 39 instructions and 10 branches, Rust
17 and 2.2, and C 14 and 0.65, its loop all but free of branches. Most
likely they are the checks on each vote: the shift's index computed in
checked arithmetic, two bounds checks on `votes[k]`, and a checked
increment, which the overflow-checked Rust build pays for too and C does
not (not traced). Built for `x86-64-v3`, the target `karac build` uses,
C takes 0.94 to 1.03 s and Rust with overflow checks 2.48 to 2.73 s,
against v2's 2.85 to 3.22 s in the same five interleaved runs. Python
takes 124 s, about 120 times C's time. The comparison with C and Rust
waits until after M4.

## Compiler findings

None on v2: every arm, the differential and the bench program pass
`karac check` and run on both v2 backends as written. `count_ones`
returns a `u32`, as in Rust, so the bit-mask arm writes `as i64` to add
it to an `i64` count.
