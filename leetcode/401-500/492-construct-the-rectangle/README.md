# 492. Construct the Rectangle

A web developer needs to know how to design a web page's size. Given a
specific rectangular web page's area, design a rectangular web page
whose length `L` and width `W` satisfy:

1. The area of the rectangular web page equals the given target area.
2. The width `W` is not larger than the length `L`, so `L >= W`.
3. The difference between length `L` and width `W` is as small as
   possible.

Return an array `[L, W]`.

```
area = 4      ->  [2,2]
area = 37     ->  [37,1]
area = 122122 ->  [427,286]
```

**Constraints:** `1 <= area <= 10^7`.

## Approaches

Every arm is `fn construct_rectangle(area: i64) -> Vec[i64]`. The width
is the largest divisor of the area whose square is no larger than it.

| file | mechanism |
|---|---|
| `construct_the_rectangle.kara` ★ | down from the square root: start at `(area as f64).sqrt() as i64`, nudge it to the whole square root, then step down to the first width that divides the area |
| `construct_the_rectangle_up.kara` | up through the small widths: every width whose square is no larger than the area, keeping the last that divides it |
| `construct_the_rectangle_divisors.kara` | from the prime factors: factor the area by trial division, build every divisor from the factors, take the largest whose square fits |
| `construct_the_rectangle_bisect.kara` | the star arm's walk down, from an integer square root found by binary search instead of floating point |
| `differential.kara` | the four arms on 1,500 random areas, four properties |

Every arm prints the same 9 lines: the three LeetCode examples, 1, a
prime squared, twice a prime, ten million, the largest prime below ten
million, and for 300 random areas from 1 to ten million how many came
out square, how many have width 1 and a checksum of the differences.
`construct_the_rectangle.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random areas, up to 100, ten thousand or a million in turn, each
with a factor `k` from 2 to 5. The reference walks every divisor pair
and keeps the one with the smallest difference.

| | property |
|---|---|
| P1 | the sides are the reference's |
| P2 | two sides, the length no shorter than the width, the width at least 1, whose product is the area |
| P3 | the area times `k²` gives a difference no larger than `k` times this one (`k` times the sides is one way to make it) |
| P4 | the width squared gives a square |

It prints `1500 cases, 4 arms, 24000 checks, 0 failures` under
`karac __mir-run`, in 1.3 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk down stops at a remainder of 1 | P1 750, P2 750, P3 425 |
| M2 | ★: the sides come out width first | P1 1446, P2 1446, P3 1086 |
| M3 | up: the first divisor is kept, not the last | P1 826, P3 1344 |
| M4 | up: the walk stops one width short | P1 140, P3 4, P4 1247 |
| M5 | divisors: a prime factor left over is dropped | P1 195 |
| M6 | divisors: each prime is taken at most once | P1 362, P3 473 |
| M7 | bisect: the search settles one too high | P1 61, P2 61, P3 61 |
| M8 | bisect: a square too big moves the top two below it | P1 46, P3 17, P4 536 |

Two first drafts were replaced. Making the ★ arm's nudge up stop short
of an exact square changed nothing: the floating-point square root of
every perfect square here came out exact, so that step never had a
square to reach (likely true of every area up to 10^7, not tested).
Stepping the bisect arm's walk down by two failed no property; it
crashed instead, on a division by zero once the width reached 0.

## Verification

All four arms print the same output as `construct_the_rectangle.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and `karac check` passes on every file, the bench
program included. The differential prints `24000 checks, 0 failures` on
both. The four arms and the differential also run clean under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output
identical, no error, no leak.

The frozen legacy backends agree too: `karac run --interp`, LLJIT,
legacy `karac build` and a `KARAC_AUTO_PAR=1` build print the same
output for all four arms, and the interpreter and legacy build print
`24000 checks, 0 failures` for the differential, with no warnings.

## Benchmarks

The bench program uses the ★ arm. It builds 200,000 random areas from
1 to ten million once, then solves each once. Every implementation
prints `200000 areas: 69 squares, 13439 of width 1, checksum
108415498`, the Kāra program under `karac __mir-run` included (in
31 s).

Every mirror takes the floating-point square root the same way (C's
`sqrt`, Rust's `f64::sqrt`, Go's `math.Sqrt`, Python's `math.sqrt`)
and returns the two sides as a fresh two-element array, as the ★ arm
does; C fills a caller's array instead. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.58 to 0.62 s |
| Rust (`rustc -O`) | 0.61 to 0.62 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.59 to 0.61 s |
| Go | 0.99 to 1.04 s |
| Python | 10.2 to 10.8 s |
| Kāra (`karac build`) | 0.60 to 0.62 s |
| Kāra (`karac build --mir`) | 0.61 to 0.64 s |

The compiled rows land together, which fits most of the time going to
the walk down, one integer division per step (inferred, not profiled).
The legacy `karac build` builds and runs this program correctly, so
`bench.sh` times that build. The `--mir` row is the v2 compiled
backend, timed for comparison. Both Kāra rows are timed at kara
`d9a7136c58`. Under `karac __mir-llvm-run` the program prints the same
line in 1.9 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

`bench.sh` is the `scripts/new-bench.sh` output with `-lm` added to
its three `clang` lines, since the C mirror calls `sqrt` and the
linker does not find it without libm. `isa_build_c` in
`scripts/bench-lib.sh` now passes any arguments after the source to
the link line, so the matched-ISA twin gets `-lm` too; every other
caller passes the source alone and is unchanged.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
