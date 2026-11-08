# 733. Flood Fill

An image is an m x n grid of integers, `image[i][j]` the color of a
pixel. Given a starting pixel (`sr`, `sc`) and a new color, paint the
starting pixel and every pixel connected to it through steps up, down,
left or right over pixels of the starting pixel's color, all with the
new color, and return the image.

```
image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]], sr = 1, sc = 1, color = 2
    ->  [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
image = [[0, 0, 0], [0, 0, 0]], sr = 0, sc = 0, color = 0
    ->  [[0, 0, 0], [0, 0, 0]]
```

**Constraints:** 1 <= m, n <= 50; 0 <= `image[i][j]`, `color` <
2^16; 0 <= `sr` < m; 0 <= `sc` < n.

## Approaches

Every arm visits the region once, each pixel painted as it is reached;
they differ in the order. When the new color is the old one, every arm
returns the image as it is, since painting would leave each pixel
looking unvisited and a fill that tests for the old color would never
stop.

| file | mechanism |
|---|---|
| `flood_fill.kara` ★ | depth first with a stack of places: pop one, and if it is inside the image and still has the old color, paint it and push its four neighbours; O(m n) time and space |
| `flood_fill_recursive.kara` | depth first by recursion, a pixel painted and then each neighbour of the old color filled in turn; recursion as deep as the region is long, up to m n |
| `flood_fill_bfs.kara` | breadth first with a `VecDeque`, each neighbour painted as it is queued so that none is queued twice; O(m n) time and space |
| `flood_fill_scanline.kara` | by runs along each row: a run of the old color is walked to both its ends and painted whole, and one place is pushed for each run of the old color touching it in the rows above and below; O(m n) time |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 11 lines: the two LeetCode examples; a single
pixel; a cross of colors where only the middle changes; a region that
winds around walls; a block filled to the color around it, which leaves
the image one color; a 50 x 50 image, the problem's largest, two thirds
0s at random, from the middle; a 50 x 50 winding path, one pixel wide in
places, 1,275 pixels long; a 50 x 50 image of one color; a 50 x
50 checkerboard, where only the start changes; and 300 random images of
up to 8 x 8 pixels with how many pixels changed and a checksum.
`flood_fill.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which marks the start and then sweeps the whole image again and again,
marking every pixel of the start's color next to a marked one, until a
sweep marks nothing, and then paints the marked pixels. 3,000 random
images are checked, each of 1 to 8 by 1 to 8 pixels in 1 to 3 colors,
filled with one of 4 colors from a random place, so the new color is
sometimes the old one, sometimes absent and sometimes elsewhere in the
image; 21,883 pixels change in all.

| | property |
|---|---|
| P1 | the image is the definition's |
| P2 | every changed pixel had the start's color and has the new one, the start has the new color, and no pixel of the start's color is left next to a changed one |
| P3 | when the new color appears nowhere in the image, filling back from the start with the old color restores it |
| P4 | the image transposed, started at (`sc`, `sr`), gives the answer transposed |

It prints `3000 images (21883 pixels changed), 4 arms, 42188 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left neighbour never pushed | P1 1054, P2 1054, P4 1473 |
| M2 | ★: the neighbour below pushed one column right | P1 544, P2 423, P4 769 |
| M3 | ★: every pixel not yet the new color painted | P1 1099, P2 1099, P3 732 |
| M4 | recursive: the top row never reached from below | P1 845, P2 845, P4 1177 |
| M5 | recursive: a right neighbour of any other color filled | P1 655, P2 655, P3 470, P4 874 |
| M6 | recursive: the bottom row never reached from above | P1 804, P2 804, P4 1179 |
| M7 | bfs: steps left lost, right taken twice | P1 1054, P2 1054, P4 1473 |
| M8 | bfs: the start not painted when queued | P1 437, P2 437 |
| M9 | bfs: the last column never reached | P1 1279, P2 1279, P4 1494 |
| M10 | scanline: a run never walked left | P1 1054, P2 1054, P4 1473 |
| M11 | scanline: only the row below searched | P1 1086, P2 1086, P4 1473 |
| M12 | scanline: one run pushed per row, not one per run | P1 103, P2 103, P4 162 |
| E1 | ★: the bounds test as not inside | 0 |
| E2 | bfs: the steps tried in the other order | 0 |
| E3 | scanline: a place skipped when it already has the new color | 0 |

P1 kills all twelve. M1, M7 and M10 are one mistake in three arms, the
step left lost, and fail the same images. P3 sees only M3 and M5, the
two edits that paint pixels of another color, since filling back with
the old color then cannot undo them. P4 sees all but M3 and M8, whose
mistakes are the same in the image transposed. M12 fails only
103 images, the ones where two separate runs of the old color touch one
run in the next row. E1 writes the bounds test as not inside; E2 tries
the four steps in another order, which paints the same pixels; E3 skips
a popped place when it has the new color rather than when it lacks the
old one, which is the same test, since a place is pushed only when it
has the old color and can change only to the new one.

## Verification

Every arm prints the same output as `flood_fill.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`969445f00a`, whose last compiler change is `b830c8f243`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms, the differential and
the bench program. Every arm prints the same output under the legacy
interpreter, `karac run` and `karac build`, and under
`KARAC_AUTO_PAR=1`. The differential prints its line too, after an
ownership warning that `image` is used at line 230 after a move at line
227, where it is passed to the definition: legacy takes a bare parameter
as owned, where v2 borrows it. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes a
1000 x 1000 image once, two thirds 0s at random and the rest 1s, so that
the 0s form one great region and the 1s small ones, and in each of
40 rounds fills from a random place with 2, a color the image does not
have, counts the 2s in that place's row, and fills back with the place's
own color, which restores the image. The image is far beyond the
problem's 50 x 50, to give the fills work worth timing. The C program's
image is an array of row pointers, as Rust's is a vector of vectors.
Every implementation prints `40 rounds on a 1000 x 1000 image:
16138 painted in their rows, 665997 0s after`, the Kāra program under
`karac __mir-run` included (in 2.6 minutes).

### Apple M5 Pro, 2026-11-08

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.1-dev.15070+g1584bfa0b`
(g1584bfa0b, the v2/MIR backend), measured 2026-11-08, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first M5 measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| c `clang -O3` | 294.5 ms ± 1.9 | 1.12× |
| **kāra `karac build`, seq** | **330.0 ms ± 4.5** | **—** |
| rust `-O` | 334.0 ms ± 2.6 | 0.99× |
| rust `-O -C overflow-checks=on` (equal-safety) | 335.5 ms ± 2.8 | 0.98× |
| go `go build` | 370.8 ms ± 4.1 | 0.89× |

Kāra is 0.99× `rustc -O`, 0.98× equal-safety Rust, 1.12× C and 0.89× Go. The gaps were not investigated on this host. Against the legacy backend (exact counts, dd86e3955, `KARAC_AUTO_PAR=0`) Kāra executes 0.88× the instructions in 0.90× the cycles.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 48.4 ms ± 0.3 | 32.8 KiB | 250.5 MiB |
| rust | 99.6 ms ± 1.7 | 455.6 KiB | 248.4 MiB |
| kāra | 164.4 ms ± 1.8 | 66.9 KiB | 248.3 MiB |
| go | — | 2450.5 KiB | 37.5 MiB |

`karac build` is 3.4× clang's cold compile and 1.7× rustc's. Kāra's
68,504-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`40 rounds on a 1000 x 1000 image: 16138 painted in their rows, 665997 0s after`).

### Container x86-64 history

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.66 to 0.77 s |
| Rust (`rustc -O`) | 0.73 to 0.86 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.71 to 0.86 s |
| Go | 1.36 to 2.02 s |
| Python | 16.0 to 16.1 s |
| Kāra (`karac build --mir`) | 0.78 to 0.84 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
4.0 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is a seventh behind C and level with Rust at the medians
of the interleaved runs (0.80 s against 0.70 and 0.77), level with Rust
under overflow checks (0.76), and more than twice as fast as Go
(1.84). Under valgrind's cachegrind it runs 4.5 billion instructions
against C's 3.1 and Rust's 4.0, and 0.81 billion branches against
0.58 and 0.77, with 32 to 35 million mispredicted in the three, the
tests of each neighbour's color on a random image. The legacy build of
the same program ran 0.73 to 0.95 s in a second round of five
interleaved runs, where v2 ran 0.77 to 0.86 s, so the two are level,
well within M2's limit of twice legacy; new katas' benches are outside
M2's frozen set in any case. Where the extra instructions go was not
traced. The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
