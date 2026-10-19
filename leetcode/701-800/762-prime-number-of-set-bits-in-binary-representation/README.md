# 762. Prime Number of Set Bits in Binary Representation

Given two integers `left` and `right`, return how many numbers in the
range from `left` to `right`, inclusive, have a prime number of set bits
in binary.

```
left = 6,  right = 10  ->  4    (110, 111, 1001 and 1010)
left = 10, right = 15  ->  5
```

**Constraints:** 1 <= `left` <= `right` <= 10^6; `right` - `left` <=
10^4.

## Approaches

| file | mechanism |
|---|---|
| `prime_set_bits.kara` ★ | count each number's bits by clearing the lowest set bit until none is left, and `match` the count against the primes up to 19; O((right - left) x bits) |
| `prime_set_bits_mask.kara` | `count_ones` for the bits, and 665772, whose set bits are the primes up to 19, shifted right by the count for the answer; O(right - left) |
| `prime_set_bits_table.kara` | a table of the bit counts of 0 to 1023, built from halves, read for each 10-bit piece of a number, and a sieve of the primes up to 64 |
| `prime_set_bits_binomial.kara` | count the numbers up to `n` with k bits without visiting them, adding a binomial C(i, k - ones so far) wherever `n` has a 1; up to `right` less up to `left - 1`, for each prime k; O(bits^2) whatever the range |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: the two LeetCode examples; 1, whose
one bit is not a prime number of bits, and 3; 1 to 10,000; 990,000 to
10^6; 524,287 and 524,288, nineteen bits and one; then 300 random ranges
of up to 10,001 numbers from 1 to about 10^6, with their total count and
a checksum. `prime_set_bits.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which writes each number out in binary as a string, counts the 1s and
tests the count for primality by trial division. 1,500 random ranges of
up to 200 numbers below about 3,200 and 300 of up to 10,001 numbers from
1 to about 10^6 are checked.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | split at a random point, the two parts' answers add up to it |
| P3 | one more number at the end adds 0 or 1, that number's own answer |
| P4 | from 1 to 2^k - 1, for k from 1 to 12 in turn, the answer is the sum of the binomials C(k, j) over the primes j |

It prints `1800 ranges (573478 numbers counted), 4 arms, 28800 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error; the count of numbers
is the ★ arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 2 left out of the primes | P1 819, P4 1650 |
| M2 | ★: 1 taken for a prime | P1 283, P4 1800 |
| M3 | ★: `right` itself left out | P1 826, P2 851, P3 826, P4 750 |
| M4 | mask: 19 left out of the mask | P1 10 |
| M5 | mask: shifted by one bit too many | P1 1729, P4 1800 |
| M6 | mask: `left` itself left out | P1 838, P2 814, P3 807 |
| M7 | table: every number up to 1023 given one more bit than half of it | P1 1792, P4 1650 |
| M8 | table: pieces read as 9 bits but cut as 10 | P1 1111, P4 450 |
| M9 | table: the sieve never run | P1 1798, P4 1350 |
| M10 | binomial: the number itself never counted | P1 1081, P3 1009, P4 1200 |
| M11 | binomial: `left` itself left out | P1 838, P2 814, P3 807 |
| M12 | binomial: all the lower bits set never counted | P1 1388, P3 734, P4 750 |
| E1 | ★: 23 counted as a prime too | 0 |
| E2 | table: the sieve run up to 64 | 0 |
| E3 | binomial: bits walked from 40, not 62 | 0 |

P1 kills all twelve. M4 is seen only 10 times: leaving 19 out of the
mask matters only for a number with nineteen 1s, and up to 10^6 +
10^4 there are four (524,287, 786,431, 917,503 and 983,039), so only a
long range that covers one sees it. The first version of the
differential held the long ranges to P2 to P4 alone, and they missed
M4 entirely, since an error made the same way for every number keeps the
parts adding up; the definition now checks the long ranges too. P2 and
P3 see only the edits that drop an end of the range, and P3 also sees
M10 and M12, whose errors in the binomial count do not come one number
at a time. P4 misses M6 and M11, which drop `left`, because its ranges
start at 1, whose one bit is not a prime count anyway. E1 adds 23, but
no number up to 10^6 + 10^4 has 23 bits; E2 sieves with factors past
8, which cross off nothing new up to 64; E3 starts the walk at bit
40, and no number here has a bit that high.

## Verification

Every arm prints the same output as `prime_set_bits.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a62eacd307`, whose last compiler change is `7d736aae75`. This paragraph
said the runtime archives were built after the last runtime change,
`b09cd37112`; in fact they predated a later one, `176f59738b`, which
changed only the order in which the runtime's merge sort makes its
merges, so it could not change any result here. Every arm and the
differential were checked again at kara `8a2af7d554`, whose last
compiler change is `60d9973e03`, with the archives rebuilt after
`176f59738b`: each prints the same under `karac __mir-llvm-run` and
`karac __mir-llvm-asan` with no error, and the bench program built by
`karac build --mir` prints the same line. The timings below are from the
earlier build.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept every arm, the differential and the
bench: each arm prints the same output under `karac run`, `karac build`
and an auto-par build, and the differential its line under `karac
build`. Under the legacy interpreter of the debug build the mask, table
and binomial arms print the same output, while the ★ arm and the
differential ran past the check's 60 s limit.

## Benchmarks

The bench program uses the ★ arm in all five languages, on 10,000 random
ranges of 10,001 numbers from 1 to 10^6, the widest LeetCode allows,
adding up the counts and a checksum. Every implementation prints
`10000 ranges of 10001 numbers: 32154723 counted, checksum
870677409`, the Kāra program under `karac __mir-run` included (in 93 s).
C and Go test the count with a `switch`, Rust with a `match` as the Kāra
program does, and Python with a tuple.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.50 to 0.61 s |
| Rust (`rustc -O`) | 0.44 to 0.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.50 to 0.66 s |
| Go | 0.72 to 0.86 s |
| Python | 50.5 to 52.2 s |
| Kāra (`karac build --mir`) | 0.56 to 0.76 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
5.3 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.61 s,
against C's 0.56, Rust's 0.44 (0.54 under overflow checks) and Go's
0.75. Under valgrind's cachegrind v2 runs 8.2 billion instructions, Rust
5.0 billion and C 4.9 billion, and all three mispredict about
145 million branches, presumably the exit of the bit-clearing loop,
whose trip count is each number's bit count (inferred, not profiled).
The legacy build of the same program ran 0.47 to 0.56 s, a median of
0.51 s in the interleaved runs, so v2 takes 1.2 times as long as legacy,
inside M2's limit of twice legacy; new katas' benches are outside M2's
frozen set in any case. The comparison with C and Rust waits until after
M4.

## Compiler findings

None new.
