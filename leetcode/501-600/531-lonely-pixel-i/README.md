# 531. Lonely Pixel I

Given an `m x n` `picture` consisting of black `'B'` and white `'W'`
pixels, return the number of black lonely pixels. A black lonely pixel
is a character `'B'` that is located at a specific position where the
same row and same column don't have any other black pixels.

```
picture = WWB    ->  3
          WBW
          BWW

picture = BBB    ->  0
          BBW
          BBB
```

**Constraints:** `1 <= m, n <= 500`; `picture[i][j]` is `'W'` or
`'B'`.

## Approaches

Every arm is `fn find_lonely_pixel(picture: Vec[Vec[char]]) -> i64`.

| file | mechanism |
|---|---|
| `find_lonely_pixel.kara` ★ | count the black pixels of every row and column in one pass, then count the black pixels whose row and column both hold one; O(mn) |
| `find_lonely_pixel_scan.kara` | for each black pixel, look along its row and down its column for another; O(mn(m + n)), no extra space |
| `find_lonely_pixel_single.kara` | for each row, the column of its black pixel when it has exactly one; then the rows whose column holds one black pixel |
| `find_lonely_pixel_transpose.kara` | a transposed copy, so a column's count is a row's: a pixel is lonely when its row in both holds one black pixel |
| `differential.kara` | the four arms against a definition by pairs, five properties |

Every arm prints the same 9 lines: both examples, one black and one
white pixel, two black pixels in a row and two in a column, an all
white picture, then for 300 random pictures of 1 to 20 by 1 to 20,
black with a chance of 2% to 30%, the lonely pixels in all, how many
pictures have none and a checksum, and last the largest case, 500 by
500 black with a chance of 2 in 1,000. `find_lonely_pixel.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a definition
that counts nothing per row or column: every two black pixels that
share a row or a column make each other not lonely, and the black
pixels left over are lonely. Each arm is held to the properties below
on 1,000 random pictures of 1 to 12 by 1 to 12, a third of them sparse
(black with a chance of 2% to 12%) and the rest black with a chance of
0 to 60%.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the transposed picture gives the same answer |
| P3 | the rows in a shuffled order give the same answer |
| P4 | the answer is at most the smaller side and at most the number of black pixels |
| P5 | one more row and column, white but for a black pixel where they cross, give one more |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the column's count never tested | P1 396, P2 542, P4 74 |
| M2 | ★: a row counted as holding one whatever it holds | P1 428, P2 542, P4 79 |
| M3 | scan: the row looked along from the second pixel | P1 52, P2 109 |
| M4 | scan: the pixel itself counted as another in its column | P1 377, P5 1000 |
| M5 | single: a row with several black pixels kept with its last one | P1 307, P2 450 |
| M6 | single: any column with black in it accepted (`>= 1`) | P1 396, P2 542, P4 74 |
| M7 | transpose: the row's count never tested | P1 428, P2 542, P4 79 |
| M8 | transpose: each column copied without its last pixel | P1 190, P2 284, P3 198, P4 3, P5 879 |
| E1 | ★: the three tests in the other order | 0 |
| E2 | scan: the row looked along from the end | 0 |
| E3 | single: a row's first black pixel kept, not its last | 0 |
| E4 | transpose: rows with no black pixel let through (`> 1`) | 0 |

M1 and M6 are one mistake in two arms, a pixel alone in its row
counted whatever its column holds, and fail exactly the same checks;
M2 and M7 are its mirror, alone in its column whatever its row holds.
P2 sees these four most often, since transposing swaps which half of
the test is missing. M4 counts every pixel against itself, so it finds
none at all, which P5's added pixel shows every time. M8 drops the
last row from every column, so it depends on which row is last, and
it is the only mutant P3's shuffle catches. E3 holds because a row's
pixel is kept only when it is the row's only one, so first and last
are the same; E4 because a row with no black pixel has nothing to
count.

## Verification

Every arm prints the same output as `find_lonely_pixel.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints `20000 checks, 0 failures` on the first
two and runs clean under the third. `karac check` passes on every arm,
the differential and the bench program. All of this is at kara
`21ffa33dff`.

On the frozen legacy backends, `karac run --interp` runs the ★ and
scan arms with the same output. LLJIT and legacy `karac build` fail on
those two at codegen, in the harness's `parse` ("no handler for method
'len' on variable 'row'", a `Str` from `rows.iter()`). The other two
arms, the differential and the bench program are refused at type
checking: legacy types the items of a `Vec`'s `iter()` by value, so it
refuses `*s` and `*p`, and it takes `picture[r]` or `pictures[p]`
passed to a borrowing parameter for a move out of the index ("cannot
move out of an index expression"). Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 pictures of 500 by 500
(the problem's largest) once, black with a chance of 1 to 20 in 1,000,
and answers every picture 200 times. Every implementation prints `20
pictures of 500 by 500, 200 times each: total 44400, checksum
997506435`, the Kāra program under `karac __mir-run` included
(in 476 s). The C mirror keeps a picture as one flat array of bytes;
Rust and Go keep rows of 4-byte `char`/`rune`, as Kāra does. Spot
timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.03 to 1.17 s |
| Rust (`rustc -O`) | 1.49 to 1.66 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.69 to 1.80 s |
| Go | 1.92 to 2.09 s |
| Python | 77.1 to 78.6 s |
| Kāra (`karac build --mir`) | 1.81 to 1.97 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. All of these are timed at kara
`21ffa33dff`. Under `karac __mir-llvm-run` the program prints the same
line in 7.9 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
written.
