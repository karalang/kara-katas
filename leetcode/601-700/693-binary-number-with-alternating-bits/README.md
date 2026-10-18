# 693. Binary Number with Alternating Bits

Given a positive integer, check whether it has alternating bits: whether
two adjacent bits always have different values.

```
n = 5   ->  true    (101)
n = 7   ->  false   (111)
n = 11  ->  false   (1011)
```

**Constraints:** 1 <= `n` <= 2^31 - 1.

## Approaches

Every arm is `fn has_alternating_bits(n: i64) -> bool`.

| file | mechanism |
|---|---|
| `has_alternating_bits.kara` ★ | `x = n ^ (n >> 1)` is a run of ones exactly when the bits alternate, and a run of ones shares no bit with itself plus one; O(1) |
| `has_alternating_bits_loop.kara` | the bits read from the bottom, each against the one before it; O(log n) |
| `has_alternating_bits_count.kara` | `n ^ (n >> 1)` has a one for each pair of neighbours that differ plus the top bit, so it must hold as many ones as n has bits: `count_ones` against 64 less `leading_zeros`; O(1) |
| `has_alternating_bits_grow.kara` | there is one alternating number of each length, 1, 10, 101, 1010, each the last with the opposite bit added below; they are built until one reaches n; O(log n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 6 lines: the three LeetCode examples; 1 to
4; 2^31 - 1 and the two largest alternating numbers below it,
1431655765 and 715827882; the 20 alternating numbers from 1 to
1,000,000 and their sum; 1431655765 with each of its 31 bits flipped in
turn, of which only the top flip still alternates; and a million random
numbers below 2^31, half of them an alternating number with low bits
changed, with a count and a checksum. `has_alternating_bits.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: write n's binary
digits out by halving it, and check that every two neighbours differ.
20,000 numbers are checked: a third random, of a random length from 1 to
31 bits, a third alternating numbers of every length, and a third
alternating numbers with up to two bits flipped.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | for n below 2^30, a bit added below n, opposite to its lowest, keeps the answer, and the same bit added makes it false |
| P3 | for n > 1, n alternates when n without its lowest bit does and the two lowest bits differ |
| P4 | for n > 1 of b bits, n alternates when n with all b bits flipped alternates and has b - 1 bits |

It prints `20000 numbers, 4 arms, 320000 checks, 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`. P4 needs its length condition: a first version
without it failed 1,456 checks, because flipping `1101` below its top
bit gives `10`, which alternates once its leading 0 is dropped, while
`1101` does not.

## Mutation testing

Thirteen edits to the differential, three to each arm that change its
answers and one that does not, each run under `karac __mir-run`. All
twelve that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a power of two tested for, not a run of ones | P1 9297, P2 731, P3 689, P4 723 |
| M2 | ★: n against itself shifted by two | P1 9286, P2 564, P3 552, P4 683 |
| M3 | ★: and in place of xor | P1 3610, P2 12654, P3 1387, P4 4061 |
| M4 | loop: a different neighbour answering no | P1 9297, P2 731, P3 689, P4 723 |
| M5 | loop: the top bit never read | P1 320, P2 495, P3 125, P4 508 |
| M6 | loop: every bit held against the lowest | P1 8804, P2 689, P3 553, P4 607 |
| M7 | count: the length one short | P1 10242, P2 9261, P3 796, P4 320 |
| M8 | count: n against itself shifted left | P1 5417, P2 9941, P3 10142, P4 9641 |
| M9 | count: twice the ones in n taken as the changes | P1 5845, P2 12014, P3 10952, P4 10425 |
| M10 | grow: one step past n | P1 9556, P3 495 |
| M11 | grow: the same bit added below | P1 9297, P2 731, P3 689, P4 723 |
| M12 | grow: starting from 2, not 1 | P1 495, P2 495, P3 850, P4 355 |
| E1 | count: at least as many changes as bits | 0 |

M1, M4 and M11 fail exactly the same checks, since all three answer
whether n is all ones: a power of two is `n ^ (n >> 1)` only for such an
n, equal neighbours everywhere is the same, and growing by the same bit
builds 1, 11, 111. M12 differs from the arm only at n = 1, which the
alternating numbers shifted all the way down reach 495 times. E1 is
equivalent: `n ^ (n >> 1)` has its top bit where n has, so it never
holds more ones than n has bits, and `>=` is `==`. It was replaced as
M9.

## Verification

Every arm prints the same output as `has_alternating_bits.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`de50d67b07` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends accept this kata, with nothing but integers
in it: `karac run` (the JIT), `karac build`, and `karac build` under
`KARAC_AUTO_PAR=1` print the same output for all four arms, and the
differential prints its line under `karac run --interp` and `karac
build`. The legacy tree-walk interpreter, `karac run --interp`, prints
it too for all four arms, but past the 60-second budget of the usual
run: the ★ arm took 86 s on the debug build. Nothing here is filed.

## Benchmarks

The bench program uses the ★ arm, the same in all five languages. It
tests 100 million numbers, each an alternating number of random length
with its two lowest bits changed at random, so that a quarter alternate,
counting them and putting each into a checksum. Every implementation
prints `100000000 numbers: 26613042 alternate, checksum 85420090`, the
Kāra program under `karac __mir-run` included (in 46 s).

The test itself is three instructions, so most of the time goes to the
random numbers and the checksum, two `%` each; the bench says how well
each compiler handles that loop, not the bit trick. Spot timings on a
shared 4-core container, eight runs of each compiled program, five of
them interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.34 to 0.37 s |
| Rust (`rustc -O`) | 0.30 to 0.39 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.29 to 0.38 s |
| Go | 0.56 to 0.69 s |
| Python | 29.3 to 29.5 s |
| Kāra (`karac build --mir`) | 0.27 to 0.37 s |
| Kāra, legacy (`karac build`) | 0.30 to 0.41 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds the same file, and
its row is above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.4 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is level with legacy, C and both Rust builds here, and
ahead of Go. The comparison with C and Rust waits until after M4.

## Compiler findings

None. `karac check` passed all four arms, the harness, the differential
and the bench program as first written.
