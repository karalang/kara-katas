# 461. Hamming Distance

The Hamming distance between two integers is the number of positions
at which their bits differ. Given two integers `x` and `y`, return the
Hamming distance between them.

```
x = 1, y = 4  ->  2   (0001 and 0100)
x = 3, y = 1  ->  1
```

**Constraints:** `0 <= x, y <= 2^31 - 1`.

## Approaches

Every arm is `fn hamming_distance(x: i64, y: i64) -> i64`. The bits
where `x` and `y` differ are the set bits of `x ^ y`.

| file | mechanism |
|---|---|
| `hamming_distance.kara` ★ | `z & (z - 1)` clears the lowest set bit of `z = x ^ y`; count how many times that runs before `z` is 0. O(differing bits) |
| `hamming_distance_ones.kara` | `(x ^ y).count_ones()`, the library's population count |
| `hamming_distance_table.kara` | a table of the set bits of every byte, built from the byte shifted right by one, then four lookups for the four bytes of `x ^ y`; every call rebuilds the table |
| `hamming_distance_compare.kara` | the plain reference: compare bit `i` of `x` and of `y` for each of the 31 positions |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 10 lines: the two LeetCode examples, two
zeros, 0 against `2^31 - 1`, `2^31 - 1` against itself, 5 against 10,
a single high bit, the alternating patterns `0101...` and `1010...`,
123456789 against 987654321, and for 300 random pairs of 31-bit numbers
(a third with `y` made sparse, a third with `y` two bit flips from `x`)
the total distance and a checksum. `hamming_distance.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on `x` and `y` below 256, the distance is brute force's, which compares the last binary digits with `% 2` and halves both numbers |
| P2 | the distance is symmetric |
| P3 | flipping the same bits of `x` and `y` (xor with a random mask) keeps the distance |
| P4 | the distance obeys the triangle inequality |
| P5 | flipping `k` distinct bits of `x`, for `k` from 0 to 31, gives distance `k` |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the loop stops at `z == 1`, so `x ^ y == 1` counts 0 | P1 7, P5 2 |
| M2 | ★: bits set in either number are counted (`x \| y`) | P1 1343, P3 1284, P5 1402 |
| M3 | ones: the lowest bit is skipped | P1 765, P5 764 |
| M4 | ones: the difference `x - y` is counted instead of the xor | P1 1220, P2 1500, P3 1400, P5 1364 |
| M5 | table: bytes from 128 up count as no bits | P1 739, P4 102, P5 1126 |
| M6 | table: the top byte is left out | P5 1311 |
| M7 | compare: the top bit is not compared | P5 742 |
| M8 | compare: only a 1 in `x` over a 0 in `y` counts | P1 1356, P2 1340, P3 1285, P5 1402 |

P5, the property with a known answer at full width, sees all eight; P1
sees the six that matter below 256 and none of M6 and M7, which only
touch bits 24 to 30. M1 is the faintest: Kernighan's loop clears the
lowest bits first, so the last `z` it sees is the highest differing
bit, and stopping at `z == 1` errs only when that bit is bit 0, that is
when `x ^ y == 1`. P4 sees little, because a mutant that counts the
wrong bits consistently still keeps most triangles.

## Verification

All four arms print the same output as `hamming_distance.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

The frozen legacy backends agree too: every arm matches under
`karac run --interp`, `karac run` (LLJIT) and `karac build`, and with
`KARAC_AUTO_PAR=1`; the differential prints `0 failures` under
`karac run --interp` and `karac build`.

## Benchmarks

The bench program uses the ★ arm. It builds 1,000,000 random 31-bit
numbers once; each of 20 rounds replaces one of them with a new random
number and adds up the distance of every neighbouring pair. Every
implementation prints `20 rounds on 1000000 numbers: total distance
310056830, checksum 453701316`, the Kāra program under
`karac __mir-run` included (in 36 s).

The mirrors keep the ★ arm's loop. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.33 to 0.36 s |
| Rust (`rustc -O`) | 0.32 to 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.43 to 0.46 s |
| Go | 0.33 to 0.37 s |
| Python | 19.9 to 21.6 s |
| Kāra (legacy `karac build`) | 0.49 to 0.53 s |
| Kāra (`karac build --mir`) | 0.43 to 0.48 s |

Nearly all the time is Kernighan's loop, about 15 steps a pair. Kāra
checks `count += 1` and `z - 1` for overflow, as Rust does with
`overflow-checks=on`, and lands next to that column. Under
`karac __mir-llvm-run` the program prints the same line in 1.7 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

No new findings.
