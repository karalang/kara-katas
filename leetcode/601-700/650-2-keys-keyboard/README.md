# 650. 2 Keys Keyboard

A notepad shows one `A`. Each step is one of two keys: Copy All copies
everything on the screen to the clipboard (no partial copy), and Paste
adds the clipboard to the screen. Return the fewest steps that leave
exactly `n` copies of `A` on the screen.

```
n = 3  ->  3    Copy All, Paste, Paste
n = 1  ->  0    already there
```

**Constraints:** 1 <= n <= 1000.

## Approaches

Every arm is `fn min_steps(n: i64) -> i64`.

| file | mechanism |
|---|---|
| `keys_keyboard.kara` ★ | the sum of the prime factors of `n`, counted with repeats, by trial division; O(sqrt(n)) |
| `keys_keyboard_table.kara` | the fewest steps for every count up to `n`, each the least over its pairs of divisors of the steps to one plus the other; O(n sqrt(n)) |
| `keys_keyboard_search.kara` | a breadth-first search over the counts on the screen and the clipboard, with a `VecDeque` and a `Vec[bool]` of the states seen; O(n^2) |
| `keys_keyboard_divide.kara` | the largest proper divisor `d`, found counting down from `n / 2`; `n / d` steps plus the steps to `d`, recursively; O(n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: the two LeetCode examples; eleven
more counts (the smallest copy, 2; powers of 2 and 3; a product of two
primes and the square of a prime; the largest prime allowed, 997, and
the largest count, 1000, with a few large counts between), each with its
answer; and the total and a checksum of the answers for every count from
1 to 200. `keys_keyboard.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which assumes nothing about factors: the two keys tried a step at a time
from one `A` and an empty clipboard, every screen and clipboard reached
kept in a `Set`, until `n` is on the screen. It checks every count from
1 to 300.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | a count that is a product of two factors takes the steps of the two added |
| P3 | never more than `n` steps, one Copy All and `n - 1` Pastes |
| P4 | exactly `n` steps for a prime and for 4, fewer for any other count above 1 |
| P5 | doubling the count adds two steps |

It prints `300 counts, 4 arms, 6000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each prime counted once however often it divides | P1 82, P2 100, P5 148 |
| M2 | ★: the prime left over at the end dropped | P1 259, P2 237, P4 62, P5 2 |
| M3 | table: the last Copy All tried only at the smaller divisor | P1 79, P2 79, P5 101 |
| M4 | table: square roots never tried as divisors | P1 10, P2 52, P4 6, P5 10 |
| M5 | search: a Paste reaching `n` exactly not allowed | P1 299, P2 237, P4 63, P5 300 |
| M6 | search: Copy All taking no step | P1 299, P4 63, P5 300 |
| M7 | divide: a prime taking one Paste too few | P1 299, P2 237, P4 63, P5 1 |
| M8 | divide: the factors taken the other way round | P1 142, P2 142, P5 236 |
| E1 | ★: trial division up to the rest itself | 0 |
| E2 | table: the last Copy All tried only at the larger divisor | 0 |
| E3 | search: a Copy All tried when the clipboard already holds the screen | 0 |
| E4 | divide: the search for a divisor stopped by 1 dividing everything | 0 |

P1 kills all eight, and P3 none: every mutant still answers `n` steps or
fewer. P2 misses only M6, whose free Copy All leaves each prime factor
`p` costing `p - 1` Pastes, a sum over the factors just as the true
answer is. P5 sees M7 once, at `n = 1`, since a doubled count above 2 is
never prime. A first M7, the search for a divisor started at `n /
3`, survived and was replaced: it is equivalent, because the smallest
factor of `n` that is 3 or more is a prime or 4, and splitting off a
4 costs 4 steps as splitting off two 2s does. The four survivors cannot
change an answer: once `p * p` passes the rest, the rest is prime and is
consumed whole either way; taking the smallest prime factor last reaches
the optimum without the other order; a Copy All when the clipboard
already holds the screen makes a state already seen; and 1 divides every
`n`, so the countdown stops there without the guard.

## Verification

Every arm prints the same output as `keys_keyboard.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`8d40e1a762` for the debug build and `803e7dac6a` for the release build
that runs `check` and `__mir-run`, with runtime archives newer than the
last `runtime/src` change.

The frozen legacy backends agree too: every arm prints the same output
under `karac run --interp`, `karac run` and `karac build`, and under a
`KARAC_AUTO_PAR=1` build, and the differential prints its line under the
interpreter and `karac build`.

## Benchmarks

The bench program uses the ★ arm. It finds the fewest steps for every
count from 1 to 1,000,000, far past the problem's limit, and adds them
up and puts them into a checksum in order. Every implementation prints
`1 to 1000000: total 64989338772, checksum 691736263`, the Kāra program
under `karac __mir-run` included (in 27 s).

Each implementation is the same trial division, in 64-bit integers. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.43 to 0.44 s |
| Rust (`rustc -O`) | 0.44 to 0.45 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.44 to 0.46 s |
| Go | 0.70 to 0.73 s |
| Python | 9.07 to 9.18 s |
| Kāra (`karac build --mir`) | 0.43 to 0.48 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The legacy `karac build` builds the bench
program unchanged and takes 0.43 to 0.46 s over six runs. Under `karac
__mir-llvm-run` the program prints the same line in 1.6 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

So the v2 build is level with legacy, C and both Rust builds: the time
is the hardware divide in `rest % p`, which every compiled
implementation issues once per trial. Go takes about half as long again.

## Compiler findings

None. All four arms, the differential and the bench program pass `karac
check` and run the same on every backend, v2 and legacy.
