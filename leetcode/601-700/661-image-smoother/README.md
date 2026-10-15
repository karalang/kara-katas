# 661. Image Smoother

Given an `m` by `n` grayscale image, return the image smoothed: each
cell becomes the average of itself and the up to eight cells around it
that lie inside the image, rounded down.

```
img = [[1,1,1],[1,0,1],[1,1,1]]
    ->  [[0,0,0],[0,0,0],[0,0,0]]
img = [[100,200,100],[200,50,200],[100,200,100]]
    ->  [[137,141,137],[141,138,141],[137,141,137]]
```

**Constraints:** 1 <= `m`, `n` <= 200; pixels from 0 to 255.

## Approaches

Every arm is `fn image_smoother(img: Vec[Vec[i64]]) -> Vec[Vec[i64]]`.

| file | mechanism |
|---|---|
| `image_smoother.kara` ★ | for each cell, the 3x3 window clipped to the image, summed and counted; O(m * n * 9) |
| `image_smoother_prefix.kara` | a table of two-dimensional prefix sums, so each window is four lookups and its count its width times its height; O(m * n) |
| `image_smoother_rows.kara` | each cell's sum with its left and right neighbours first, then those sums over the rows above and below; O(m * n * 6) |
| `image_smoother_packed.kara` | the answers written into the bits above each pixel of one copy of the image, read through `& 255`, then shifted down; no second grid |
| `differential.kara` | the four arms against a definition with no window, five properties |

Every arm prints the same 10 lines: the two LeetCode examples and five
more images (one pixel; one row; one column; two by two; and all white),
each with its smoothed image; a checksum of 200 random images of 1 to
12 by 1 to 12; and one of the problem's largest, 200 by 200, smoothed
once and then again, each with a checksum. `image_smoother.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which uses no window: for each cell, look at every cell of the image and
keep those at most one row and one column away. Each of 1,000 random
images is 1 to 8 by 1 to 8, its pixels from 0 to 255, or from 0 to 3 so
that sums are small and the rounding shows.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the image transposed smooths to the answer transposed |
| P3 | the image mirrored left to right smooths to the answer mirrored |
| P4 | a flat image stays as it is |
| P5 | every cell lies between the smallest and largest pixel of its window |

It prints `1000 images (21436 pixels), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the column to the right left out | P1 861, P2 968, P3 882 |
| M2 | ★: every sum divided by 9 | P1 997, P4 992, P5 725 |
| M3 | prefix: the table's corner added rather than taken off | P1 777, P3 773, P4 775, P5 757 |
| M4 | prefix: the row above left out | P1 841, P2 967 |
| M5 | rows: the last column's width taken at the one before it | P1 981, P2 987, P3 889, P4 992, P5 443 |
| M6 | rows: the row below left out on the last row but one | P1 707, P2 873 |
| M7 | packed: the answer packed only 4 bits up, over the pixel | P1 997, P2 779, P3 884, P4 992, P5 974 |
| M8 | packed: the answers shifted down one bit short | P1 997, P4 992, P5 879 |
| E1 | ★: the remainder taken off before dividing | 0 |
| E2 | prefix: the table two wider and two taller | 0 |
| E3 | rows: the width kept at least 1 | 0 |
| E4 | packed: the answer added on rather than or-ed in | 0 |

P1 kills all eight. The symmetries split them by shape. M1, M4 and
M6 drop one side of the window, so a transposed image (P2) sees them
all, and a mirrored one (P3) sees M1, the side it swaps, but not M4 or
M6, which drop a row and are unchanged by a left-right flip. M3, the
prefix table's corner added rather than taken off, is wrong the same way
along rows and columns, so P2 misses it. M2 and M8 get every cell's
value wrong without a direction, so neither symmetry sees them, while
M7's answers spill into the pixel bits of the cells read after them,
which depends on the order of the scan. The flat image (P4) sees
M2, M3, M5, M7 and M8. P5, the window's range, sees the four that push
values outside it, M2, M3, M7 and M8, and M5, but misses the ones that
only drop a neighbour, since an average over fewer cells still lies
inside the window's range. The four survivors cannot change an answer:
taking off the remainder first divides to the same floor; the bigger
table's extra row and column are never read; the width is never 0; and
with the pixel below bit 8 and the answer above it, `+` and `|` agree.

## Verification

Every arm prints the same output as `image_smoother.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `057e29e74f` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends print the same output for every arm under the
interpreter, the JIT and `karac build`, with and without
`KARAC_AUTO_PAR=1`, with ownership warnings that `img` is moved and then
used. Their interpreter runs the differential too, but their `karac
build` refuses it, at the `for row in out.iter_mut()` loop that mirrors
an image for one of its properties: that loop shape is not supported in
legacy code generation. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes one random 1,000 by
1,000 image and smooths it 20 times over, each pass taking the last
one's output, then puts the result into a checksum. Every implementation
prints `1000x1000, 20 passes: checksum 458182897`, the Kāra program
under `karac __mir-run` included (in 96 s).

Each implementation is the same clipped window, each pass allocating a
new image: Kāra's and Rust's rows are `Vec`s, Go's slices, Python's
lists, and C's `malloc`ed rows, the input's freed after each pass. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine), each including making the
image:

| | time |
|---|---|
| C (`clang -O3`) | 0.22 to 0.24 s |
| Rust (`rustc -O`) | 0.23 to 0.28 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.26 to 0.27 s |
| Go | 0.43 to 0.48 s |
| Python | 34 s |
| Kāra (`karac build --mir`) | 0.27 to 0.28 s |
| Kāra, legacy (`karac build`) | 0.27 to 0.33 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 2.6 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy and within a few hundredths of a
second of Rust and C, with Go behind. The comparison with C and Rust
waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
