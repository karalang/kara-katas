# 476. Number Complement

The complement of an integer is the integer you get when you flip all
the 0's to 1's and all the 1's to 0's in its binary representation.

For example, the integer 5 is `"101"` in binary and its complement is
`"010"`, which is the integer 2.

Given an integer `num`, return its complement.

```
num = 5  ->  2
num = 1  ->  0
```

**Constraints:** `1 <= num < 2^31`.

## Approaches

Every arm is `fn find_complement(num: i64) -> i64`. Only the bits from
the highest set bit down are flipped; the zeros above it are not part
of the binary representation.

| file | mechanism |
|---|---|
| `number_complement.kara` ★ | a mask of ones grown one bit at a time until it is at least the number, then `num ^ mask`. O(bits) |
| `number_complement_zeros.kara` | the width from `leading_zeros()`, the mask `(1 << width) - 1`, and `~num & mask` |
| `number_complement_bits.kara` | the number halved bit by bit, adding the bit's place value to the answer when the bit is 0 |
| `number_complement_text.kara` | the number written in binary with `f"{num:b}"`, every digit flipped, and read back with `i64.from_str_radix(.., 2)` |
| `differential.kara` | the four arms on 1,500 random numbers, five properties |

Every arm prints the same 12 lines: the two LeetCode examples, 2, 7, 8
and 10, `1023` and `1024` (all ones, and one more), `2^31 - 1` and
`2^30` (the largest number and the largest power of two allowed),
`1431655765` (`1010..101`, 31 bits), each with its binary form, and for
1,000 random numbers (a random width of 1 to 31 bits, the highest bit
set and the rest random) how many complements are 0 and a checksum of
them in order. `number_complement.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random numbers of 1 to 30 bits, each with a second random number
of the same width.

| | property |
|---|---|
| P1 | the complement plus the number is `2^width - 1`, and they share no bit |
| P2 | the complement is at least 0 and below the number's highest bit |
| P3 | the complement of `2n` is `2c + 1` (one more bit, a 0 that flips to 1) |
| P4 | the complement of `2n + 1` is `2c` |
| P5 | another number of the same width gives the same number plus complement |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, in 0.5 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the mask stops one bit short (`mask < num / 2`) | P1 1440, P2 1440, P3 60, P4 60 |
| M2 | ★: the mask grows by doubling, not by one more 1 | P1 1440, P2 1376, P3 1500, P4 1500, P5 1391 |
| M3 | zeros: the width is one too many | P1 1500, P2 1500 |
| M4 | zeros: `~(num - 1) & mask` | P1 1500, P2 124, P3 1500, P4 1500 |
| M5 | bits: the bit is copied, not flipped | P1 1500, P2 1500, P3 1500, P4 1500, P5 1391 |
| M6 | bits: `answer += place * 2` | P1 1386, P2 731, P3 1500, P5 1391 |
| M7 | text: the answer cut to its low 29 bits (`% (1 << 29)`) | P3 28, P4 28 |
| M8 | text: a 0 stays 0 and a 1 becomes 0 | P1 1386, P3 1500, P5 1391 |

M1 is wrong for every number of two or more bits and right for the 60
of one bit. P3 and P4 fail on exactly those 60: elsewhere the mask is
one bit short on both sides of the property and the error cancels, but
doubling a one-bit number gives a two-bit one, where the arm goes
wrong. M7 is the narrow one: no number drawn is wider than 30 bits, so
only the complement of `2n` or `2n + 1` for a 30-bit `n` whose bit 28
is 0 reaches bit 29 and loses it, 28 times. P5 cannot see M1, M3 or M4,
which are wrong by the same amount for every number of a width. One
first draft was equivalent and was replaced: "the mask minus its top
bit" for the zeros arm, since the top bit of `~num` within the width is
always 0 anyway.

## Verification

All four arms print the same output as `number_complement.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree too: `karac run --interp`, LLJIT,
legacy `karac build` and a `KARAC_AUTO_PAR=1` build all print the same
output on every arm, and the differential prints `0 failures` on the
legacy interpreter and a legacy build.

## Benchmarks

The bench program uses the ★ arm on 30,000,000 numbers, each of a
random width from 1 to 31 bits with the highest bit set and the rest
random. Every implementation prints `30000000 numbers: complements add
up to 1039831226189805, checksum 754495232`, the Kāra program under
`karac __mir-run` included (in 119 s).

Every mirror grows the mask one bit at a time, as the ★ arm does, and
draws the numbers from the same generator. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.69 to 0.71 s |
| Rust (`rustc -O`) | 0.68 to 0.70 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.68 to 0.71 s |
| Go | 1.13 to 1.18 s |
| Python | 49.2 to 51.5 s |
| Kāra (`karac build`) | 0.67 to 0.70 s |
| Kāra (`karac build --mir`) | 0.68 to 0.75 s |

The legacy `karac build` builds and runs this program correctly, so
`bench.sh` is the `scripts/new-bench.sh` output unchanged and times
that build. The `--mir` row is the v2 compiled backend, timed for
comparison. Both Kāra rows are timed at kara `b0b1557b39`. Under
`karac __mir-llvm-run` the program prints the same line in 2.8 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

No new findings. `f"{num:b}"`, `i64.from_str_radix`, `leading_zeros()`
and `~` all run on both MIR backends.
