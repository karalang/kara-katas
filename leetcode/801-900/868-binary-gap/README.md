# 868. Binary Gap

Given a positive integer `n`, find and return the longest distance
between any two adjacent 1's in the binary representation of `n`. If
there are no two adjacent 1's, return 0. Two 1's are adjacent if there
are only 0's separating them (possibly no 0's). The distance between two
1's is the absolute difference between their bit positions; for example,
the two 1's in "1001" have a distance of 3.

```
n = 22  ->  2    (10110)
n = 8   ->  0    (1000)
n = 5   ->  2    (101)
```

**Constraints:** `1 <= n <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `binary_gap.kara` ★ | one pass over the bits from the lowest up, remembering where the last 1 was; each later 1 is adjacent to it, so the distance between them is a candidate. O(log n) |
| `binary_gap_string.kara` | n written out with `{n:b}` and the string walked from its highest bit, the distance between each '1' and the one before it a candidate |
| `binary_gap_positions.kara` | the positions of the set bits collected in increasing order; two 1s are adjacent exactly when they are neighbours in that list, so the answer is the largest difference between neighbours |
| `binary_gap_lowbit.kara` | from one lowest set bit to the next: `trailing_zeros` gives the lowest 1's position, `rest & (rest - 1)` clears it, and the distance between successive positions is a gap. One step per 1, not per bit |
| `binary_gap_zeros.kara` | a walk from bit 30 down counting the 0s passed since the last 1; at each 1 after the first, that count plus one is the distance back |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 20 lines: LeetCode's three examples, each with
n in binary; fourteen more (one 1, two adjacent 1s, three in a row,
1001, gaps of 6 and 5 in 1041 and 529, 20, 15, a power of two, gaps of
28 and 29 between bits near the top of the range, and 10^9 and 10^9 - 1,
LeetCode's largest); the gaps of every n from 1 to 100,000, summed, with
the largest and a checksum; and the gaps of 100,000 random n up to 10^9,
with a checksum and how many have each length. `binary_gap.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: n's binary digits by repeated division, and the largest j - i
over every pair of positions i < j holding 1s with only 0s between them,
or 0. It checks 7,561 values of n: every n from 1 to 4,096, every n up
to 10^9 with one or two 1s, and 3,000 random n up to 10^9.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | a 0 added below the lowest bit (2n, while at most 10^9) changes nothing |
| P3 | a 1 added k places above the highest bit makes the answer the larger of k and the old one |
| P4 | the bits in reverse order give the same answer |
| P5 | the answer is 0 exactly when n has one 1, and otherwise from 1 to one less than the number of bits |
| P6 | with the lowest 1 cleared, the answer is the larger of the new answer and the distance from that 1 to the next |

It prints `7561 values of n, gaps sum to 34094, 196040 checks over 5
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the zeros between counted, not the distance | P1 7518, P3 2359, P5 95, P6 2052 |
| M2 | ★: a 1 at bit 0 never the previous 1 | P1 428, P2 395, P3 2, P4 762, P5 40, P6 428 |
| M3 | ★: positions counted two at a time | P1 7518, P3 2237, P5 677, P6 1330 |
| M4 | string: every 1 measured from the first | P1 7017, P3 2848, P6 7017 |
| M5 | string: the lowest bit dropped | P1 428, P2 395, P3 2, P4 762, P5 40, P6 428 |
| M6 | string: written in octal | P1 7358, P2 2176, P3 2816, P4 2097, P5 6026, P6 6578 |
| M7 | positions: only the 20 lowest bits | P1 1171, P2 80, P3 1509, P4 1796, P5 245, P6 245 |
| M8 | positions: the two lowest 1s' gap left out | P1 1330, P3 22, P4 1662, P5 501, P6 2165 |
| M9 | positions: every 1 measured from the lowest | P1 7017, P3 2848, P6 7017 |
| M10 | lowbit: every gap measured from the lowest 1 | P1 7017, P3 2848, P6 7017 |
| M11 | lowbit: the first gap measured from bit 0 | P1 1855, P2 2861, P3 20, P4 1558, P6 4452 |
| M12 | lowbit: shifted down a place, the lowest 1 kept | P1 5466, P3 2293, P4 2502, P6 1240 |
| M13 | zeros: the zeros counted, not the distance | P1 7518, P3 2359, P5 95, P6 2052 |
| M14 | zeros: the count never reset at a 1 | P1 6302, P3 2603, P6 3307 |
| M15 | zeros: started at bit 25 | P1 429, P2 66, P3 601, P4 598, P5 110, P6 110 |

P1 kills all fifteen. Some mutations are one fault in two arms and fail
identically: M1 and M13 count the zeros between two 1s instead of the
distance; M4, M9 and M10 measure every 1 from the first or the lowest,
which gives the span from the lowest 1 to the highest; and M2 and M5
both lose a 1 at bit 0 (M5 by dropping that bit, M2 by never measuring
from it). A first M5 that skipped the string's first character with
`bits.bytes().skip(1)` did not compile, since `bytes()` returns a
`Slice` and an adaptor needs `.iter()` first; it was replaced.

## Verification

Every arm prints the same output as `binary_gap.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara
`292a4ca2f0`. Under `karac __mir-run` the arms take 1 to 3 s each and
the differential 2.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends run all five arms through `karac run
--legacy --interp`, `karac run --legacy`, `karac build` and a
`KARAC_AUTO_PAR=1` build with the same output. They run the
differential too, with 0 failures, but `karac run --legacy --interp`
prints `gaps sum to 34143, 196165 checks` where every other lane prints
34094 and 196040, as it miscounted kata 867's differential. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: the gaps of
every n from 1 to 10,000,000, summed, with a checksum. Every
implementation prints `n from 1 to 10000000: gaps sum to 47488255,
checksum 998232014`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.73 to 0.79 s | 0.76 s |
| Rust (`rustc -O`) | 0.71 to 0.78 s | 0.71 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.71 to 0.76 s | 0.73 s |
| Go | 0.83 to 0.91 s | 0.87 s |
| Python | 21.4 s | |
| Kāra (`karac build --mir`) | 0.70 to 0.73 s | 0.71 s |
| Kāra, frozen legacy (`karac build`) | 0.65 to 0.73 s | 0.68 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 867's does.

All six compiled programs land within 0.68 to 0.87 s. The loop is short
and its branch on each bit is a coin toss: under valgrind's cachegrind
every program mispredicts 16 to 18 percent of its branches, about 0.1
billion of them, and runs 2.9 to 3.0 billion instructions, C 2.88, Rust
with overflow checks 2.97, legacy 2.95 and v2 2.90. v2 is 0.97 times
Rust's median time under overflow checks, 0.93 times C's and 1.04 times
legacy's.
