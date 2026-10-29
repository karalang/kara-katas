# 1015. Smallest Integer Divisible by K

Given a positive integer `k`, find the length of the smallest positive
integer `n` that is divisible by `k` and whose decimal digits are all 1.
Return that length, or -1 if there is no such `n`. `n` may not fit in a
64-bit signed integer.

```
k = 1  ->  1     (n = 1)
k = 2  ->  -1    (no such n)
k = 3  ->  3     (n = 111)
```

**Constraints:** `1 <= k <= 10^5`.

## Approaches

The numbers `1, 11, 111, ...` are the repunits. They outgrow any integer
type, but `k` divides one exactly when its remainder mod `k` is 0, and
each repunit's remainder follows from the last: `r' = (10r + 1) mod k`.
The arms differ in how they decide when that walk reaches 0, and in
whether they walk it at all.

| file | mechanism |
|---|---|
| `repunit.kara` ★ | remainder walk: at most `k` steps, since a walk of `k` remainders without a 0 has repeated one and cycles; multiples of 2 and 5 are refused first, a repunit ending in 1. O(k) |
| `repunit_set.kara` | the remainders seen: walk until 0 or a remainder met before, assuming nothing about 2 and 5. O(k) expected |
| `repunit_floyd.kara` | tortoise and hare: Floyd's two walkers from the empty repunit's 0 find the cycle and its length; there is an answer exactly when 0 is on the cycle, and it is the cycle's length. O(k) time, O(1) space |
| `repunit_order.kara` | the order of 10: the n-digit repunit is `(10^n - 1) / 9`, so `k` divides it exactly when `10^n` is 1 mod `9k`, and the answer is the multiplicative order of 10 mod `9k`, found by multiplying by 10 until the power comes back to 1. O(k) |
| `repunit_divisors.kara` | divisors of phi: the same order divides `phi(9k)` (Euler), so factor `9k`, build `phi` and its divisors, and test them smallest first with fast exponentiation. O(sqrt(k) + d log k) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 22 lines: the answers for twenty values of
`k`, LeetCode's three examples among them (1, 2, 3, 5, 7, 9, 11, 13,
17, 19, 27, 41, 81, 99, 101, 9091, 99989, 99991, 99999 and 100000);
for every `k` up to 10,000, how many have no answer (6,000, the
multiples of 2 or 5), the sum of the rest, the longest answer (9,972 at
`k = 9981`) and a checksum of the answers in order; and the same count,
sum and checksum for 1,000 random `k` up to 100,000. `repunit.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally as far as `i64` reaches: the repunits of 1 to 18 digits
themselves, divided by `k`. It checks 2,200 values of `k`: every one up
to 2,000 and 200 random up to 100,000.

| | property |
|---|---|
| P1 | the statement, for `k` up to 2,000 whose answer has at most 18 digits; otherwise no answer of at most 18 digits |
| P2 | the answer's repunit is a multiple of `k`, its remainder summed digit by digit from powers of 10 |
| P3 | no answer exactly when `k` shares a factor with 10; otherwise at most `k` digits |
| P4 | the answer for a divisor of `k` (`k` without its smallest prime) divides the answer for `k` |
| P5 | for a partner `b` from 3 to 23 sharing no factor with `k` or 10, the answer for `kb` is the lcm of the answers for `k` and `b` |
| P6 | each arm agrees with at least two of the other four |

P4 and P5 hold because `k` divides the n-digit repunit exactly when the
answer for `k` divides `n`. The differential prints `2200 values of k:
checksum 611279294, 44325 checks over 5 arms: 0 failures` under `karac
__mir-run` (26 s) and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a `k`-digit answer missed | P1 3, P3 7, P4 330, P5 347, P6 7 |
| M2 | ★: one digit too many | P1 71, P2 886, P3 7, P4 616, P5 2835, P6 887 |
| M3 | ★: the walk starts at 1 | P1 70, P2 886, P4 393, P5 2463, P6 886 |
| M4 | set: a remainder recorded before it is checked | P1 70, P3 886, P4 562, P5 691, P6 886 |
| M5 | set: a cycle taken for an answer | P1 315, P2 1313, P3 1313, P6 1313 |
| M6 | set: the wrong step, `11r + 1` | P1 193, P2 1591, P3 1271, P4 77, P5 319, P6 1860 |
| M7 | floyd: the cycle one short | P1 104, P3 887, P4 887, P5 691, P6 920 |
| M8 | floyd: any cycle accepted | P1 340, P2 1256, P3 1256, P6 1256 |
| M9 | floyd: the wrong step, `10r + 11` | P1 16, P2 30, P5 53, P6 30 |
| M10 | order: one short | P1 71, P2 886, P3 1, P4 718, P5 691, P6 887 |
| M11 | order: modulo `3k` | P1 30, P2 193, P5 69, P6 193 |
| M12 | order: modulo `27k` | P1 44, P3 229, P5 217, P6 543 |
| M13 | divisors: a prime's square left whole when factoring | P3 28, P4 30, P5 21, P6 28 |
| M14 | divisors: the wrong bits multiplied in the exponentiation | P1 799, P2 886, P5 691, P6 886 |
| M15 | divisors: the base not squared | P1 66, P2 45, P3 818, P4 517, P5 684, P6 882 |

P6 kills all fifteen, P1 fourteen, P5 thirteen, P3 eleven, P2 ten and
P4 nine. P1 misses M13, so every value it gets wrong has an answer of more
than 18 digits, past the literal reading.
P5 misses the two that turn a value with no answer into one, which P5
never tests. The checks draw no random number that depends on an
answer, so every mutant sees the same values and their counts can be
compared.

Fifteen other edits were tried and set aside. Four change no answer: ★
walking the multiples of 2 and 5 too, which its `k`-step bound ends
with -1; Floyd's slow walker starting one step behind, which still
meets the fast one on the cycle; the order arm's loop also stopping at
a power of 0, which a power of 10 mod `9k` never is; and the divisors
arm pushing a square root twice. Two never end: the order arm modulo
`k` (for `k = 1` its power is 0 forever) and stepping by powers of 100
(an even order is never reached by odd powers); the interpreter stops
them at its step limit and the compiled lane at the 900 s timeout. Two
failed exactly the same checks as a kept one: set one short, as M10,
and Floyd walking one step too many back to the start, as M4. The other
seven were killed too, beyond three per arm: ★ adding the 1 after
reducing and refusing multiples of 3 instead of 5; set not reducing the
first remainder; order not reducing the first power and starting one
power ahead; divisors testing the divisors of `9k` instead of
`phi(9k)` and leaving them unsorted. Set not reducing its first
remainder and order not reducing its first power fail exactly alike.

## Verification

Every arm prints the same output as `repunit.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error; the differential prints its line under all three. `karac
check --output=json` reports no diagnostic for the five arms, the
differential and the bench program, so `karac fix` had nothing to do.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. The release build is kara `56c60bdf7c`, with
runtime archives rebuilt at `ce706dd131`, the last commit before it to
change the runtime. Under `karac __mir-run` the arms take 0.8 s
(divisors) to 20.7 s (floyd); set and floyd walk the multiples of 2 and
5 to their cycles.

No compiler gap turned up writing this kata.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages for every `k` from 1 to
30,000, folding each answer into a sum and a checksum: about 53 million
steps of the walk, each a multiplication and a remainder by `k`. Every
implementation prints `k = 1..30000: 18000 with no answer, the rest sum
to 53054244, checksum 755199146`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.338 to 0.353 s | 0.347 s |
| Rust (`rustc -O`) | 0.342 to 0.362 s | 0.349 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.318 to 0.368 s | 0.331 s |
| Go | 0.408 to 0.480 s | 0.413 s |
| Python | 3.95 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.322 to 0.362 s | 0.333 s |
| Kāra (`karac build`) | 0.323 to 0.336 s | 0.331 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time equals its real time) and runs as fast as the sequential
one.

v2 took 1.01 times Rust's median time under overflow checks and 0.96
times C's: the four compiled programs within a few percent, Go behind.
Each step's remainder feeds the next step's multiplication, so the walk
waits on one division after another; v2's loop, like the others, takes
LLVM's 32-bit `div` when both operands fit and a 64-bit `idiv`
otherwise (read off its disassembly). Python is about 12 times Kāra
here, against 80 to 100 times on the last two katas, since the
division costs the compiled programs most of their time. We did not
measure where.
