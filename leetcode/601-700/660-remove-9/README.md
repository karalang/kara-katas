# 660. Remove 9

Start from 1 and remove every integer whose decimal digits include a
9: 9, 19, 29, ..., 90, 91, and so on. Given `n`, return the `n`-th
integer left, counting from 1.

```
n = 9   ->  10
n = 10  ->  11
```

**Constraints:** 1 <= `n` <= 800,000,000.

## Approaches

Every arm is `fn new_integer(n: i64) -> i64`. The integers with no 9 are
exactly those written in the digits 0 to 8, and in counting order, so
the `n`-th is `n` in base 9 read as a decimal number. Three arms use
that fact in different ways; the fourth does not.

| file | mechanism |
|---|---|
| `remove_9.kara` ★ | base-9 digits peeled off the bottom with `% 9` and `/ 9`, laid down as decimal digits; O(log n) |
| `remove_9_top.kara` | from the top: the largest power of 9 not above `n`, then one digit per power down to 1; O(log n) |
| `remove_9_search.kara` | a binary search for the smallest `x` with `n` integers free of 9 up to it, counted digit by digit; O(log^2 n) |
| `remove_9_text.kara` | the base-9 digits written into a string with `f"..."` and read back with `i64.parse`; O(log n) |
| `differential.kara` | the four arms against counting up, five properties |

Every arm prints the same 13 lines: the two LeetCode examples; nine more
values of `n` (the first numbers, both sides of the first powers of
9, and the largest `n`), each with its answer; every `n` from 1 to
20,000 checked against counting up, with a checksum; and a checksum of
1,000 values spread up to 800,000,000. `remove_9.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
count up from 1, skipping every number with a 9. That is too slow beyond
small `n`, so it covers every `n` from 1 to 3,000, and 1,000 more values
spread up to 800,000,000 are held to the other four properties only.

| | property |
|---|---|
| P1 | the answer is the one counting up gives (for `n` up to 3,000) |
| P2 | the answer has no 9 in it |
| P3 | the answer for `n + 1` is larger, and every number between the two has a 9 (checked when they are at most 2,000 apart) |
| P4 | the answer for `9m` is ten times the answer for `m` |
| P5 | the answer has as many decimal digits as `n` has base-9 digits |

It prints `4000 values of n, 4 arms, 80000 checks, 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the digits taken in base 10 | P1 2992, P2 1375, P3 741, P4 3609 |
| M2 | ★: the digits laid down in base 9 | P1 2992, P2 1417, P4 4000, P5 875 |
| M3 | top: the first power one too small at a power of 9 | P1 3, P2 3, P3 3, P4 8, P5 3 |
| M4 | top: the powers stepped down by 10 | P1 2992, P2 1013, P3 3330, P4 3608, P5 3992 |
| M5 | search: `x` itself never counted | P1 3000, P2 437, P3 437, P4 4000 |
| M6 | search: a 9 freeing only eight blocks | P1 635, P3 1322, P4 442, P5 73 |
| M7 | text: the digits left least significant first | P1 2884, P3 3097, P4 4000, P5 448 |
| M8 | text: each digit written one too high | P1 3000, P2 1522, P3 305, P4 4000 |
| E1 | ★: the loop running while anything is left | 0 |
| E2 | top: the power compared with n divided by 9 | 0 |
| E3 | search: the upper bound starting at n | 0 |
| E4 | text: a leading 0 written first | 0 |

P1 and P4 each kill all eight. M3 fails the fewest checks because it
goes wrong only when `n` is a power of 9, and there are just three of
those up to 3,000. P5 misses M1, M5 and M8, whose answers are wrong but
the right length, and P2 misses M6 and M7, whose answers are wrong but
still free of 9. P3 misses only M2, which lays the base-9 digits down in
base 9 again and so returns `n` itself, a sequence that still counts up
one at a time. The four survivors cannot change an answer: `rest` is
never negative; `power * 9 <= n` and `power <= n / 9` agree for whole
numbers; the search's upper bound doubles until it is high enough
wherever it starts; and `i64.parse` reads a leading 0 as nothing.

## Verification

Every arm prints the same output as `remove_9.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `057e29e74f` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends print the same output for every arm and the
differential under the JIT and `karac build`, with and without
`KARAC_AUTO_PAR=1`. Their interpreter does too for three arms, but takes
over 60 s on the search arm and the differential. Legacy is frozen, so
that is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It takes 50,000,000 values of `n`,
every 16th from 1 to 800,000,000, and puts each answer into a checksum.
Every implementation prints `50000000 values of n: checksum
61528713`, the Kāra program under `karac __mir-run` included (in 127 s).

Each implementation is the same loop of `% 9`, `/ 9` and `* 10`. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.69 to 0.71 s |
| Rust (`rustc -O`) | 0.67 to 0.76 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.71 to 0.83 s |
| Go | 0.79 to 1.00 s |
| Python | 42 to 46 s |
| Kāra (`karac build --mir`) | 0.74 to 0.86 s |
| Kāra, legacy (`karac build`) | 0.76 to 0.79 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 6.2 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy, Rust and C: all of them spend the
time in the same divisions by 9. The comparison with C and Rust waits
until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
