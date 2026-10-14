# 633. Sum of Square Numbers

Given a non-negative integer `c`, decide whether there are two integers
`a` and `b` with `a * a + b * b == c`.

```
c = 5  ->  true    (1 * 1 + 2 * 2)
c = 3  ->  false
```

**Constraints:** `c` from 0 to 2^31 - 1.

## Approaches

Every arm is `fn judge_square_sum(c: i64) -> bool`. Only `a` and `b` of
0 or more need trying, and with `a <= b`, since signs and order do not
change the sum.

| file | mechanism |
|---|---|
| `judge_square_sum.kara` ★ | two pointers, `a` up from 0 and `b` down from the integer square root of `c`, found by binary search, moving whichever brings the sum toward `c`; O(sqrt c) |
| `judge_square_sum_squares.kara` | every square up to `c` put in a `Set` as it is made, and each looked up as `c - a * a`; O(sqrt c) inserts and lookups |
| `judge_square_sum_roots.kara` | for each `a` with `2 * a * a <= c`, the integer square root of `c - a * a` by Newton's method, squared back; O(sqrt c log c) |
| `judge_square_sum_primes.kara` | Fermat's theorem: trial division, and `false` as soon as a prime that leaves 3 on division by 4 divides an odd number of times; O(sqrt c) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 16 lines: the two LeetCode examples; twelve
more (0, 1, 2 and 4; 13, a prime that leaves 1 on division by 4; 9 and
18, 3 squared alone and doubled; 21, 3 times 7; a million; and 2^31 -
2, 2^31 - 1 and 46340 squared); a count and checksum of the sums of two
squares from 0 to 20,000; and the same over 300 random values from 0 to
2^31 - 1. `judge_square_sum.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
some `a` and `b` from 0 up, with `a <= b`, square and add up to `c`,
tried one pair at a time. Each of 1,000 cases is two random values `c`
and `d` from 0 to 3,000.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | `4 * c` has the same answer |
| P3 | `2 * c` has the same answer |
| P4 | when `c` and `d` both are sums of two squares, so is `c * d` |
| P5 | `c * c` is one, and `4 * c + 3` is not |

It prints `1000 cases (283 sums of two squares), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pointers stopping before they meet | P1 13, P3 22, P5 1 |
| M2 | ★: the root of a square found one too small | P1 10, P3 22, P5 409 |
| M3 | squares: the square equal to `c` never made | P1 11, P3 22, P5 410 |
| M4 | squares: only even `a` tried | P1 203, P2 203, P3 75, P5 500 |
| M5 | roots: `a` never as large as `b` | P1 13, P3 22, P5 1 |
| M6 | roots: the root taken of one less than the rest | P1 283, P5 1000 |
| M7 | primes: any prime that leaves 3 refused, even squared | P1 51, P5 768 |
| M8 | primes: a large leftover prime never checked | P1 324, P4 189, P5 538 |
| E1 | ★: a sum equal to `c` treated as too small | 0 |
| E2 | squares: only a rest no larger than `a * a` looked up | 0 |
| E3 | roots: Newton's method started from half of `n` | 0 |
| E4 | primes: only 2 and odd numbers tried | 0 |

P1 kills all eight. P2 sees only M4: `4 * c` has an answer with both
numbers even, which M4 still finds, while `c` itself may need an odd
`a`. P3 sees M1 to M5: twice a square `b * b` is `b * b + b * b`, which
needs `a == b`, never reached by M1 and M5, and M2 and M3 already miss
the square itself. P4 sees only M8, the one mutant that says yes where
the answer is no. P5 sees six: `c * c` is `0 + c * c`, which M2 and
M3 miss and M6 and M7 refuse, and M8 says yes to some `4 * c + 3`. The
four survivors cannot change an answer: an equal sum has already
returned before the comparison; a rest larger than `a * a` is a square
not yet added, which is found later from the other side; from 4 up half
of `n` is at least its root, and for 2 and 3 it is 1, so Newton's method
ends on the same root; and an even number above 2 divides nothing once
the 2s are taken out.

## Verification

Every arm prints the same output as `judge_square_sum.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `1cccf0bcce` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends run every arm under the JIT, `karac build`
and `KARAC_AUTO_PAR=1 karac build`, all with identical output, and the
differential prints its line under `karac build`. Under the legacy
interpreter the primes arm matches; the other three printed their first
lines identically and then ran past the 60 s budget, and the
differential printed nothing within it. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 10,000 random values from
0 to 2^31 - 1 once, then answers each in turn, counting the sums of two
squares and putting each of them into a checksum. Every implementation
prints `10000 values: 1739 sums of two squares, checksum 717805259`, the
Kāra program under `karac __mir-run` included (in 45 s).

Each implementation is the same loop over 64-bit integers, with the same
binary search for the root. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine), each including making the values:

| | time |
|---|---|
| C (`clang -O3`) | 0.91 to 0.93 s |
| Rust (`rustc -O`) | 0.91 to 0.92 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.42 to 0.45 s |
| Go | 0.30 to 0.32 s |
| Python | 20.8 to 21.0 s |
| Kāra (`karac build --mir`) | 0.48 to 0.53 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: it types the items of a `Vec`'s `iter()` by value, so `*c` is
an error. That edit is by hand, on top of the `scripts/new-bench.sh`
output. A copy outside the kata without the two `*`s builds under legacy
and takes 0.43 to 0.46 s, so the v2 build is level with legacy. Under
`karac __mir-llvm-run` the program prints the same line in 2.4 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

The Kāra build is about half the C build and level with Rust with
overflow checks, and Go is fastest. The disassembly suggests why, as an
inference rather than a profile: `clang -O3` turns the choice between `a
+= 1` and `b -= 1` into branchless `setl` and `setge` arithmetic, which
puts the two multiplies of each step on the loop's dependency chain,
while the Kāra build keeps a conditional jump, which predicts well
because `a` and `b` move in long runs. `rustc -O` without overflow
checks takes as long as C and with them about half as long, which fits
the same reading, but the Rust and Go binaries were not disassembled.

## Compiler findings

None. The legacy refusal of the bench program is not filed because
legacy is frozen.
