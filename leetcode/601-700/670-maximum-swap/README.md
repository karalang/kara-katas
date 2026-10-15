# 670. Maximum Swap

Given a non-negative integer `num`, swap two of its digits at most once
and return the largest number that can make.

```
num = 2736  ->  7236   (the 2 and the 7 swapped)
num = 9973  ->  9973   (no swap helps)
```

**Constraints:** 0 <= `num` <= 100,000,000.

## Approaches

Every arm is `fn maximum_swap(num: i64) -> i64` and works on the
number's digits, most significant first, read off by division and put
back by multiplying. The swap to make raises the leftmost digit that can
be raised, to the largest digit to its right, taken from that digit's
last copy.

| file | mechanism |
|---|---|
| `maximum_swap.kara` ★ | each digit's last place noted, then for each place from the left, a larger digit placed later looked for from 9 down; O(digits * 10) |
| `maximum_swap_suffix.kara` | one pass from the right, keeping the place of the largest digit so far, and the last place found smaller than it; O(digits) |
| `maximum_swap_pairs.kara` | every swap of two places tried, the largest number kept; O(digits^3) |
| `maximum_swap_sorted.kara` | the digits sorted falling, and the first place the number differs from them filled from the last copy of the digit sorted there; O(digits log digits) |
| `differential.kara` | the four arms against a definition that tries every swap by arithmetic on the number, five properties |

Every arm prints the same 20 lines: 18 numbers, each with its answer
(the two LeetCode examples; 0; one digit; numbers already at their best;
swaps that must take the last copy of a repeated digit; a 0 that must
not move to the front; and the problem's largest, 100,000,000); how many
of every number below 100,000 a swap raises, with a checksum of the
answers; and a checksum of 10,000 random numbers up to
100,000,000. `maximum_swap.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which never makes a list of digits: swapping the digits `a` and `b` at
the places worth `p` and `q` adds `(b - a) * p + (a - b) * q` to the
number, so it tries every pair of places that way and keeps the largest
result, no swap included. Of the 3,000 numbers, a third are random up to
100,000,000 and the rest have 1 to 9 digits drawn from only two or three
neighbouring digits, so that repeated digits, where the choice of copy
matters, are common.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | it is no smaller than the number |
| P3 | it has the number's digits, at most two of them in other places |
| P4 | it is no larger than the number's digits in falling order |
| P5 | it starts with the number's largest digit |

It prints `3000 numbers (2364 raised), 4 arms, 60000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first place of each digit kept, not the last | P1 1400 |
| M2 | ★: a digit never raised by just one | P1 1239, P5 722 |
| M3 | suffix: the first copy of the largest kept on ties | P1 1054 |
| M4 | suffix: the rightmost place to raise kept, not the leftmost | P1 1973, P5 1393 |
| M5 | pairs: neighbours never swapped | P1 366, P5 218 |
| M6 | pairs: the number left out of the running | P1 314, P2 314, P3 246, P5 297 |
| M7 | sorted: the digits sorted rising | P1 2581, P2 2419, P3 671, P5 2353 |
| M8 | sorted: the digit copied rather than swapped | P1 2364, P3 2364, P4 898 |
| E1 | ★: a later place as at least i + 1 | 0 |
| E2 | suffix: smaller as different, after larger is ruled out | 0 |
| E3 | pairs: every j tried, earlier ones again | 0 |
| E4 | sorted: the first differing place as the first smaller one | 0 |

P1 kills all eight. M1 and M3 are the subtle ones: they make the right
swap with the wrong copy of a repeated digit, leaving a smaller number
that still passes every other property, since it is no smaller than the
number, has its digits, and starts with the largest of them. P5 sees the
five that can leave the leftmost digit unraised: M2, which never raises
a digit by just one; M4, which raises the rightmost digit it can rather
than the leftmost; M5, which never swaps neighbours; M6, which leaves
out the number itself and so must swap even when that lowers it; and
M7, which sorts the wrong way. P2 sees M6 and M7, the two that can give
a smaller number, and P3 sees them and M8, which copies a digit rather
than swapping it. P4 sees only M8, which can copy a large digit twice.
The four survivors cannot change an answer: on whole numbers `>= i +
1` is `> i`; once larger is ruled out, different means smaller; swapping
a place with itself or an earlier one adds nothing new; and at the first
place where a number differs from its digits sorted falling, its digit
is always the smaller.

## Verification

Every arm prints the same output as `maximum_swap.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `83b41fb1d0` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends print the same output for every arm under the
interpreter, the JIT and `karac build`, with and without
`KARAC_AUTO_PAR=1`, and run the differential to the same line under the
interpreter and `karac build`. Their interpreter is slow on the pairs
arm, 131 s against 31 s for the ★ arm, past this check's 60 s limit;
given longer, it prints the same output. Their `karac build` warns on
the pairs arm and the differential that `d` is moved into `number_of`
and then used again, which design.md does not hold, since a parameter
borrows, and builds them anyway.

## Benchmarks

The bench program uses the ★ arm. It finds the answer for
3,000,000 numbers spread up to the problem's largest, 100,000,000, the
`i`-th being `i * 33 + i % 7`, and puts each into a checksum. Every
implementation prints `3000000 numbers: checksum 580996773`, the Kāra
program under `karac __mir-run` included (in 67 s).

Each implementation reads the digits off by division and puts them back
by multiplying. Kāra's, Rust's and Go's make a `Vec` or slice of digits
and one of last places for each number, and Python's lists; C's are two
small arrays on the stack, so it allocates nothing. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.09 s |
| Rust (`rustc -O`) | 0.32 to 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.33 to 0.36 s |
| Go | 0.51 to 0.56 s |
| Python | 4.6 to 4.8 s |
| Kāra (`karac build --mir`) | 0.26 to 0.31 s |
| Kāra, legacy (`karac build`) | 0.37 to 0.39 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 1.8 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is ahead of legacy and level with Rust, all three making
two small vectors for each number. C makes none and is about three times
faster, which is the price of those allocations rather than of the
search. Go is behind; it has not been profiled. The comparison with C
and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy warning
above is not filed because legacy is frozen.
