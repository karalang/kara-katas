# 1175. Prime Arrangements

Return the number of permutations of 1 to `n` so that prime numbers are at
prime indices (1-indexed.)

(Recall that an integer is prime if and only if it is greater than 1, and
cannot be written as a product of two positive integers both smaller than
it.)

Since the answer may be large, return the answer modulo `10^9 + 7`.

```
n = 5    ->  12          ([1,2,5,4,3] is one; [5,2,3,4,1] is not, 5 at index 1)
n = 100  ->  682289015
```

**Constraints:** `1 <= n <= 100`.

The arms are `fn num_prime_arrangements(n: i64) -> i64`. The two Rust arms
keep the `i32` method LeetCode gives Rust users, inside `impl Solution`,
and a one-line `num_prime_arrangements` calls it.

## Approaches

A permutation that puts every prime on a prime index puts the `p` primes
up to `n` on the `p` prime indices and the other `n - p` values on the
other indices, in any order, so the answer is `p! * (n - p)!`. The arms
differ in how they count the primes and build the product.

| file | mechanism |
|---|---|
| `prime_arrangements.kara` ★ | a sieve of Eratosthenes over a `Vec[bool]` counts the primes, and a `factorial` loop each side, modulo 10^9 + 7 |
| `prime_arrangements_trial.kara` | trial division up to each number's square root, the primes counted with `filter(..).count()`, and one running product over 1..=p and then 1..=n-p |
| `prime_arrangements_place.kara` | one pass over the places 1..=n, each tested against the primes found so far: the k-th prime place can take any of the k primes up to it and the k-th other place any of the k other values, so the product is built as the places are met |
| `prime_arrangements_fold.kara` | through iterators: the primes as `(2..=n).filter(..)` with an `all` over the divisors up to the square root, each factorial a `fold` |
| `prime_arrangements_solution.kara` | a Rust solution as LeetCode's Rust users write it (a primality closure by trial division, `filter(\|&x\| ..).count() as i64`, each factorial a `fold` in `i64`), carried to Kāra by `karac fix` |
| `prime_arrangements_sieve.kara` | another Rust solution (a `vec![true; n + 1]` sieve over `usize`, the primes counted as it runs, the answer multiplied up in `u64` with `i as u64`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, four properties |

Every arm prints the same 5 lines: LeetCode's two examples; n = 1 to 12,
where 1 is not prime and 2 is the first prime (`[1, 1, 2, 4, 12, 36, 144,
576, 2880, 17280, 86400, 604800]`); n = 88, 89, 96, 97 and 99, beside the
last primes below 100; and a checksum over every n the constraints allow
(`n = 1 to 100: checksum 533675857`). `prime_arrangements.py` mirrors the
★ arm and its output is byte-identical; with `lit` it also counts, for n
up to 8, every permutation of 1..=n with each prime value on a prime
index, and prints `literal, n = 1 to 8: [1, 1, 2, 4, 12, 36, 144, 576]`,
the first 8 answers. Every arm gives the same output under `karac run`
and `karac build`.

The Mend loop: the four Kāra arms take no fixes. The Rust arms take one
round each, 9 edits and 5. The closure arm's: `struct Solution;` to
`struct Solution {}`; `Solution::` to `Solution.`; the closures' `->
bool` and `-> i64` dropped; `|&x|` to `|x|`; `1i64` to `1`; and three `as
i64` casts dropped, since `count()` is already `i64` and `i32` widens to
`i64` by itself. The sieve arm's: the same two, `n as usize` to `n as
i64`, `vec![true; n + 1]` to `Vec.filled(n + 1, true)`, and the
harness's `as i64`. Both arms' outputs match on the first run.

One compiler gap came up on the way, fixed in kara `13f42dda1f`:

- `karac fix` broke the sieve arm (kara B-2026-11-16-205). In one round it made
  `let n = n as usize;` into `let n = n as i64;`, so the count and the
  loop's `i` became `i64` too, and in the same round it flagged `ans * i
  as u64 % m` over the old `usize` `i` as a cast that widens by itself,
  and deleted the `as u64`. With `i` an `i64` the product mixed `u64`
  and `i64`, refused with no fix. A `usize` operand that the
  pointer-width fix makes `i64` is no longer flagged, so the `as u64`
  stays and the arm takes the one round above.

The differential takes no fixes.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a number is prime when it has exactly two divisors, and the
literal count, for n up to 8, builds every permutation of 1..=n one
place at a time and counts those with every prime value at a prime
index. Every arm answers every n from 1 to 100, the whole of the
constraints' range.

| | property |
|---|---|
| P1 | for n up to 8, the literal count |
| P2 | one more place multiplies the answer by the number of values of its kind: `f(n + 1) = f(n) * k`, where `k` counts the primes up to n + 1 if n + 1 is prime, and the others if not |
| P3 | the answer lies in 1 to 10^9 + 6, never 0, since 10^9 + 7 is a prime above every factor of `p! * (n - p)!` |
| P4 | the ★ arm's answer |

All 1,842 checks pass on every arm: `n = 1 to 100: checksum 959400679,
1842 checks over 6 arms: 0 failures`, in 1.5 s under `karac __mir-run`,
and the same under `karac __mir-llvm-run` and `karac build`.

## Mutation testing

Eighteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All eighteen are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: each prime's square left unmarked | P1 5, P2 97, P4 470 |
| A2 | ★: 1 sieved as a prime | P1 5, P2 97, P4 485 |
| A3 | ★: each factorial one factor short | P1 6, P2 98, P4 490 |
| T1 | trial: squares of primes counted prime | P1 5, P2 97, P4 94 |
| T2 | trial: 1 counted prime | P1 7, P2 99, P4 96 |
| T3 | trial: the second factorial one factor short | P1 5, P2 74, P4 97 |
| P1 | place: squares of primes counted prime | P1 5, P2 97, P4 94 |
| P2 | place: each other place one choice too many | P1 8, P2 74, P4 100 |
| P3 | place: 1 counted prime | P1 5, P2 97, P4 97 |
| F1 | fold: 1 counted prime | P1 7, P2 99, P4 96 |
| F2 | fold: each factorial one factor short | P1 6, P2 98, P4 98 |
| F3 | fold: squares of primes counted prime | P1 5, P2 97, P4 94 |
| X1 | solution: squares of primes counted prime | P1 5, P2 97, P4 94 |
| X2 | solution: 2 not counted prime | P1 4, P2 99, P4 96 |
| X3 | solution: the second factorial one factor long | P1 8, P2 74, P4 100 |
| S1 | sieve: every other multiple left unmarked | P1 3, P2 93, P4 87 |
| S2 | sieve: the second factorial one factor short | P1 5, P2 74, P4 97 |
| S3 | sieve: each prime's square left unmarked | P1 5, P2 97, P4 94 |

A mutation of the ★ arm fails P4 on every arm, since P4 compares each
arm with the ★ arm; P1 and P2 name the ★ arm itself. Three more edits
look like faults and pass all 1,842 checks under both backends, since
they are equivalent: the ★ sieve marking from `i` rather than `i * i` (a
prime is counted before it is marked), the trial arm's product starting
at 2 rather than 1, and the closure arm counting primes from 2 rather
than 1 (1 is not prime either way).

## Benchmarks

`bench/` times the ★ arm against the same sieve and factorials in C,
Rust, Go and Python: a million calls at an `n` drawn from 1 to 100, the
constraints' range, every answer folded into a checksum. Each call
allocates its sieve (Kāra's `Vec.filled`, Rust's `vec!`, Go's `make`,
Python's list, and C's `calloc`, freed before the call returns). Every
program prints `1000000 calls: checksum 951639764`.

Timings on a 4-core container (Intel Xeon, 2.3 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac
`13f42dda1f` on LLVM 22. karac builds for the x86-64-v3 baseline, so the
C and overflow-checked Rust programs are also built at
`-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.184 to 0.195 s | 0.186 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.184 to 0.210 s | 0.187 s |
| Rust (`rustc -O`) | 0.233 to 0.263 s | 0.239 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.240 to 0.269 s | 0.245 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.241 to 0.300 s | 0.248 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.218 to 0.260 s | 0.223 s |
| C (`clang -O3`) | 0.212 to 0.235 s | 0.224 s |
| Go | 0.239 to 0.293 s | 0.248 s |
| Python | 5.36 to 5.37 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time equals wall time for both Kāra rows, so
both ran on one core. Kāra takes about 0.76x overflow-checked Rust's
time, the equal-safety comparison, 0.84x C's and 0.75x Go's; Python
takes about 29x. Every call does the same few hundred steps, a sieve of
at most 101 flags and two factorial loops of `%` by a constant, so the
programs differ mostly in how each call gets its zeroed sieve and how
the compiler schedules the loops; which of those puts Kāra ahead was not
profiled, and the lead should not be read as general.
