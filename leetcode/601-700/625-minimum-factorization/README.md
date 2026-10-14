# 625. Minimum Factorization

Given a positive integer `num`, return the smallest positive integer
whose digits multiply to `num`. If there is no such integer, or the
answer does not fit in a 32-bit signed integer, return 0.

```
num = 48  ->  68
num = 15  ->  35
```

**Constraints:** `num` from 1 to 2^31 - 1.

## Approaches

Every arm is `fn smallest_factorization(num: i64) -> i64`. A number
below 10 is its own answer. Above that, no digit of the answer is 0 or
1, since a 0 makes the product 0 and a 1 only adds a digit; so the
answer exists exactly when no prime above 7 divides `num`.

| file | mechanism |
|---|---|
| `smallest_factorization.kara` ★ | the factors 9, 8, ..., 2 taken out greedily, each as often as it divides, and written smallest first; O(log num) |
| `smallest_factorization_primes.kara` | the counts of the primes 2, 3, 5 and 7, the 3s paired into 9s and the 2s grouped into 8s, a leftover 3 and 2 joined into a 6 and two leftover 2s into a 4, then the digits sorted; O(log num) |
| `smallest_factorization_search.kara` | for each length from 2 to 10, a depth-first search that appends digits in nondecreasing order, smallest first, and returns the first number whose digits multiply to `num`; exponential in the length at worst |
| `smallest_factorization_text.kara` | the greedy digits pushed onto a `String` largest first, reversed, compared with `"2147483647"` by length and then as text, and parsed; O(log num) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 17 lines: the two LeetCode examples; thirteen
more (1, a single digit, ten, a prime above 7, products whose leftover
2s and 3s make a 6, a 4 and a 9 with a 6, answers of four and seven
digits, nine 9s, nine 9s and a 2, 2^30 and 2^31 - 1, the last three too
large or impossible); a count, total and checksum over 600 random
numbers, half products of random digits and half random below 2^31; and
the same over every number from 1 to 20,000. `smallest_factorization.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
counting up from 1, the first number whose digits multiply to `num`. It
is built once as a table of the first such number below 100,000 for
every product, which covers every tested number that has an answer,
since those answers have at most five digits. Each of 1,000 cases is
either a product of 1 to 5 random digits from 2 to 9 or a random number
from 1 to 3,000, plus for P5 a product of 6 to 10 digits that is at most
a ninth of 2^31 - 1.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | a nonzero answer's digits multiply to `num`, and above 9 none is a 0 or a 1 |
| P3 | the answer is 0 exactly when a prime above 7 divides `num` |
| P4 | the answer's digits never go down |
| P5 | nine times the larger product gives that product's answer with a 9 put last, or 0 once that passes 31 bits |

It prints `1000 cases (541 with an answer), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the digit 2 never taken | P1 137, P3 137 |
| M2 | ★: answers up to 2^32 - 1 allowed | P5 67 |
| M3 | primes: a leftover 3 joins a 2 only when two 2s are left | P1 70 |
| M4 | primes: the digits left unsorted | P1 358, P4 358, P5 885 |
| M5 | search: any number of the right length accepted | P1 604, P2 604, P3 203, P5 1000 |
| M6 | search: the lowest digit allowed appended instead of the one tried | P1 429, P2 429, P5 107 |
| M7 | text: the digit 6 never taken | P1 127 |
| M8 | text: the digits left largest first | P1 421, P4 421, P5 885 |
| E1 | ★: only 0 and 1 returned as they are | 0 |
| E2 | primes: an answer of exactly 2^31 - 1 refused | 0 |
| E3 | search: ten-digit answers never searched | 0 |
| E4 | text: the limit itself refused | 0 |

P1 kills seven of the eight. M2 is seen by P5 alone: every number P1 to
P4 test has an answer of at most five digits, so a larger limit matters
only once P5 multiplies a large product by nine. P3 sees M1 and
M5, which answer 0 where an answer exists and nonzero where none does.
P2 sees M5 and M6, whose digits no longer multiply to `num`, and P4 sees
M4 and M8, whose digits are out of order. M3 and M7 fail P1 alone: their
digits still multiply to `num` and are sorted, but a 2 and a 3 stand
where a 6 would do. The four survivors cannot change an answer: a single
digit is already its own greedy answer, `2147483647` holds a 1 so is
never an answer, and the smallest ten-digit answer, `2222222222`, is
above 2^31 - 1, so it is 0 whether or not it is searched for.

## Verification

Every arm prints the same output as `smallest_factorization.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `049307dc29` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends run the ★ arm under the interpreter, the JIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`, all with identical
output. They refuse the primes arm and the differential at type
checking, since they type the items of a `Vec`'s `iter()` by value so
`*d` is an error, and the differential also for the old rule that an
argument which is already a `mut ref`, as `seed` is inside
`random_product`, drops its call-site `mut` marker. The search arm
matches under the JIT and `karac build`; the legacy interpreter printed
its first 16 lines identically and then ran past the 60 s budget. The
text arm matches under the interpreter, and the JIT and `karac build`
refuse it: `Iterator.rev()` on `chars()` is not yet supported in legacy
codegen for that chain shape. Legacy is frozen, so these are noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes 200,000 numbers once, every
even one a product of up to 10 random digits from 2 to 9 that stays
within 31 bits and every odd one random from 1 to 2^31 - 1; then
50 rounds answer every one, counting the answers that are not 0 and
putting each into a checksum. Every implementation prints
`200000 numbers, 50 rounds: 4967850 answers, checksum 948459364`, the
Kāra program under `karac __mir-run` included (in 23 s).

Each implementation is the same loop of divisions by 9 down to 2 over a
flat array of 64-bit integers. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine), each including making the numbers:

| | time |
|---|---|
| C (`clang -O3`) | 0.39 to 0.44 s |
| Rust (`rustc -O`) | 0.33 to 0.38 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.33 to 0.34 s |
| Go | 0.73 to 0.79 s |
| Python | 8.8 to 8.9 s |
| Kāra (`karac build --mir`) | 0.59 to 0.63 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the `mut`
markers in `random_numbers`; that edit is by hand, on top of the
`scripts/new-bench.sh` output. A copy outside the kata with those
markers dropped builds under legacy and takes 0.63 to 0.70 s, so the
v2 build is level with legacy or a little ahead. Under `karac
__mir-llvm-run` the program prints the same line in 2.3 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

The Kāra build is about 1.5 times the C build and 1.8 times the Rust
build. The disassembly shows why, as an inference rather than a profile:
both Kāra backends keep one `idiv` in the hot loop, `rest % d` with `d`
a variable, while `clang -O3` and `rustc -O` unroll the eight steps of
the digit loop and divide by constants, which compile to multiplies.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
