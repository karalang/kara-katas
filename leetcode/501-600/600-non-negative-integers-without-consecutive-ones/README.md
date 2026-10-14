# 600. Non-negative Integers without Consecutive Ones

Given a positive integer `n`, return the number of the integers in the
range `[0, n]` whose binary representations do not contain consecutive
ones.

```
n = 5  ->  5    (0, 1, 2, 4 and 5; 3 is 11)
n = 1  ->  2
n = 2  ->  3
```

**Constraints:** `1 <= n <= 10^9`.

## Approaches

Every arm is `fn find_integers(n: i64) -> i64`. Call a bit string free
when it has no two ones side by side. The free strings of k bits number
fib[k], 1, 2, 3, 5, 8 and on: a free string starts with 0 and k - 1 free
bits, or with 10 and k - 2.

| file | mechanism |
|---|---|
| `find_integers.kara` ★ | n's bits from the top: at each one, the numbers with a 0 there and any free bits below are smaller, fib[k] of them, and the walk goes on with the one fixed; two ones together in n end it, and if it reaches the bottom, n itself counts; O(log n) |
| `find_integers_grow.kara` | every free number grown from 1 with a stack, a 0 bit added on the right, or a 1 when the last bit is 0, while it stays at most n, and counted; O(answer), about n^0.69 |
| `find_integers_memo.kara` | digit DP from the top bit with the state (position, last bit a one, still equal to n's prefix), the states already below n memoized; O(log n) |
| `find_integers_table.kara` | every number up to n is n or first drops below it at one of n's one bits, turned to 0 under a prefix copied from n; the prefix must be free, and the bits below are free strings counted by their top bit in two tables; O(log n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 10 lines: the three examples above; five more
(3, two ones together at the top; 4, a lone one; 699,050, ones and zeros
alternating over 20 bits; 2^30 - 1, every bit set; and 10^9, the
problem's largest); the answers for n from 1 to 40; and a total and
checksum over 300 random n up to 1,000,000. `find_integers.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every integer from 0 to n, its binary
digits read off by halving, counted when no two ones stand side by side.
It is kept as running counts up to 4,096, so each case reads its answer.
Each of 1,000 random cases has n from 4 to 4,096; 921 of them have two
ones together.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is one more than n - 1's exactly when n has no two ones together, and the same otherwise |
| P3 | with t the top bit of n, the answer is the answer for t - 1 plus the answer for the smaller of n - t and t / 2 - 1, since a number from t up has a 0 after t's one |
| P4 | the answer for 2n + 1 is the answer for n plus the answer for n / 2: the even numbers up to it are the free numbers up to n doubled, and the odd ones the free even ones doubled with a 1 after |
| P5 | the answer for 2t - 1 is the answer for t - 1 plus the answer for t / 2 - 1, the Fibonacci step |

It prints `1000 cases (921 with two ones together), 4 arms,
20000 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: n itself never counted | P1 79, P2 65, P4 101 |
| M2 | ★: the walk not stopped at two ones together | P1 921, P2 824, P3 995, P4 488, P5 1000 |
| M3 | grow: a 1 grown after any number | P1 1000, P2 921, P3 512, P4 1000, P5 1000 |
| M4 | grow: n itself never reached | P1 79, P2 65, P4 101 |
| M5 | memo: a memo read while still tight | P1 336, P2 79, P3 270 |
| M6 | memo: two ones together allowed | P1 1000, P2 921, P3 512, P4 1000, P5 1000 |
| M7 | table: only free strings starting with 0 counted below | P1 1000, P2 28, P4 56 |
| M8 | table: the prefix never checked | P1 921, P2 824, P3 995, P4 488, P5 1000 |
| E1 | ★: a bit read by `% 2` | 0 |
| E2 | grow: doubling by adding | 0 |
| E3 | memo: a third memo slot never used | 0 |
| E4 | table: the free strings below as one entry further up | 0 |

Three pairs of mutants make the same mistake in different arms and fail
on the same cases. M1 and M4 both leave n out, which matters only when n
is free, so the definition sees them on just the 79 such cases; P2 and
P4 compare counts at two or three numbers and see the mistake when those
differ in being free. M2 and M8 both go on past two ones together, and
M3 and M6 both count every number, n + 1, which no property but P3 can
let through, and P3 only when n - t is the smaller term. P5 sees only
mutants that break the Fibonacci step itself; M1, M4, M5 and M7 keep it,
M7 while being wrong on every case. E4 is safe because the free strings
of k + 1 bits starting with 0 number those of k bits.

## Verification

Every arm prints the same output as `find_integers.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. All at kara
`2d241d9b05`.

The frozen legacy backends agree: every arm prints the same output under
`karac run --interp`, `karac run` and `karac build`, and under
`KARAC_AUTO_PAR=1 karac build`, but for the grow arm under `karac run
--interp`, which had printed 7 of its 10 lines, all right, when the
60-second limit stopped it. The differential prints its line under
`karac build`; under `karac run --interp` it too ran past 60 seconds.

## Benchmarks

The bench program uses the ★ arm. It makes 1,000,000 values of n from
1 to 10^9 once, and then 20 times over solves every one. Every
implementation prints `1000000 values, 20 rounds: total
26925461565280, checksum 758722537`, the Kāra program under `karac
__mir-run` included (313 s).

Each implementation builds the Fibonacci counts on every call, as the ★
arm does: a `Vec` in Rust, a slice appended to in Go, a list in Python,
and in C an array on the stack. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.58 to 0.61 s |
| Rust (`rustc -O`) | 2.78 to 2.96 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.20 to 3.42 s |
| Go | 4.78 to 5.15 s |
| Python | 52.9 to 55.0 s |
| Kāra (`karac build`, legacy) | 2.61 to 2.71 s |
| Kāra (`karac build --mir`) | 3.42 to 3.59 s |

Both Kāra rows are at kara `2d241d9b05`; here the v2 compiled backend is
about 1.3 times slower than legacy. Under `karac __mir-llvm-run` the
program prints the same line in 11.8 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

Every implementation but C's builds the counts on the heap on every
call, growing them four times from 2 to 32. The Kāra row is about
1.2 times Rust's, and C's, which keeps them on the stack, is 5 to
6 times faster than both. In callgrind profiles at 2 rounds, the
v2 program runs 3.40 billion instructions to legacy's 2.64 billion, with
the same number of `malloc` and `free` calls: 0.30 billion of the
difference is `karac_mir_vec_reserve`, which the v2 code calls when a
push finds the `Vec` full and which then calls the same `realloc`
wrapper legacy calls directly, and 0.41 billion is in the program's own
code, about 200 instructions more a call. That this is where the
difference lies is read from the profiles; it is not measured by
changing the program.

## Compiler findings

None. The legacy timeouts above are not filed because legacy is frozen.
