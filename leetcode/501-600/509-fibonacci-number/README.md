# 509. Fibonacci Number

The Fibonacci numbers, commonly denoted `F(n)`, form a sequence, called
the Fibonacci sequence, such that each number is the sum of the two
preceding ones, starting from 0 and 1. That is,

```
F(0) = 0, F(1) = 1
F(n) = F(n - 1) + F(n - 2), for n > 1.
```

Given `n`, calculate `F(n)`.

```
n = 2  ->  1    (F(2) = F(1) + F(0) = 1 + 0 = 1)
n = 3  ->  2
n = 4  ->  3
```

**Constraints:** `0 <= n <= 30`.

## Approaches

Every arm is `fn fib(n: i64) -> i64`.

| file | mechanism |
|---|---|
| `fib.kara` ★ | two running values, F(i) and F(i + 1), stepped n times. O(n) time, O(1) space |
| `fib_memo.kara` | the recurrence as written, each value kept the first time it is worked out in a `Vec[Option[i64]]`, `None` for not yet known, which goes down the recursion as `mut ref`. O(n) |
| `fib_doubling.kara` | fast doubling: from the pair (F(k), F(k + 1)), F(2k) = F(k) (2 F(k + 1) - F(k)) and F(2k + 1) = F(k)^2 + F(k + 1)^2 give the pair at 2k and 2k + 1, so halve n down to 0 and double back up, returning the pair as a tuple. O(log n) |
| `fib_binet.kara` | Binet's formula: F(n) is phi^n / sqrt 5 rounded to the nearest whole number, with phi^n written `phi.powi(n as i32)`, in `f64` |
| `differential.kara` | the four arms on 1,500 pairs of random n, five properties |

Every arm prints the same 5 lines: the three LeetCode examples, F(0)
to F(30), and for 300 random n from 0 to 30 the total and a checksum.
`fib.py` mirrors the ★ arm and its output is byte-identical.

The Binet arm writes phi^n as `phi.powi(n as i32)`, the method
design.md's own example uses on an `f64`. Until kara B-2026-10-13-22
was fixed (below), `karac check` and every backend refused the arm and
the differential, which holds a copy of it. The differential and the
mutants below were run then, on copies that wrote `phi.pow(n as f64)`
instead. Both files were rechecked as written at kara `0736eef763`,
after the fix.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 pairs of random n and m from 0 to 30.

| | property |
|---|---|
| P1 | F(n) is the reference's, a table built by adding up from F(0) and F(1) |
| P2 | F(k + 2) = F(k + 1) + F(k), with k = n, or n - 2 when n + 2 would pass 30 |
| P3 | Cassini's identity, F(k - 1) F(k + 1) - F(k)^2 = (-1)^k, with k = n held between 1 and 29 |
| P4 | gcd(F(n), F(m)) = F(gcd(n, m)) |
| P5 | F(2k) = F(k) (2 F(k + 1) - F(k)), with k = n % 16 |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under `karac
__mir-run`, as written and on the copy described under Approaches.

## Mutation testing

Twelve edits to that copy of `differential.kara`, two to each arm that
change its answers, and four that do not, each run under `karac
__mir-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one step too few (`0..n - 1`) | P1 1410, P2 46, P3 1500, P4 1100, P5 1409 |
| M2 | ★: the second value is returned | P1 1449, P3 1500, P4 769, P5 1409 |
| M3 | memo: F(0) is 1 | P1 1449, P3 1500, P4 769, P5 1409 |
| M4 | memo: the table keeps one more than the value | P1 1359, P2 1454, P3 1403, P4 480, P5 1219 |
| M5 | doubling: F(2k) = F(k) (2 F(k + 1) + F(k)) | P1 1351, P2 1500, P3 1403, P4 224, P5 1409 |
| M6 | doubling: n's low bit is read the wrong way round | P1 1410, P2 1500, P3 1500, P4 1078, P5 1409 |
| M7 | Binet: rounded down, not to the nearest | P1 709, P2 791, P3 1500, P4 961, P5 1409 |
| M8 | Binet: psi in place of phi | P1 1454, P3 1500 |
| E1 | ★: the steps counted `1..=n` | 0 |
| E2 | memo: the table one longer | 0 |
| E3 | doubling: the halving stops at `n <= 0` | 0 |
| E4 | Binet: psi^n subtracted, the exact formula | 0 |

E1 and E2 change nothing the arm reads: the loop still runs n times,
and the extra slot is never looked at. E3 is equivalent because n is
never below 0. E4 is equivalent because psi^n / sqrt 5 is what the
rounding throws away: subtracting it first gives a number a rounding
error away from F(n), which rounds the same.

M2 and M3 are the same wrong answer, F(n + 1), written into two arms,
and fail the same cases; the sequence shifted by one still adds up, so
P2 cannot see them. M1 shifts the other way except at 0, which it
leaves at F(0) = 0, so P2 sees it only where it checks F(2) = F(1) +
F(0) (46 cases). M8 gives 0 for every n, since psi^n / sqrt 5 is never
as much as 1/2, and 0 satisfies P2, P4 and P5: only the reference and
Cassini's identity see it. M7 is wrong only for odd n, where psi^n is
below 0 and rounding down loses 1; Cassini's identity, which mixes odd
and even n, sees it in every case.

## Verification

Every arm prints the same output as `fib.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak. The differential prints `30000
checks, 0 failures` on the first two and runs clean under the third.
`karac check` passes on every arm, the differential and the bench
program.

The frozen legacy backends agree on the ★, memo and doubling arms:
`karac run --interp`, LLJIT, legacy `karac build` and a
`KARAC_AUTO_PAR=1` build print the same output. They refuse the Binet
arm and the differential as written: since the fix the type check
passes, and `karac run --interp` stops at run time ("method 'powi' not
found on type 'f64'"), LLJIT and legacy `karac build` at codegen ("no
handler for method 'powi'"). On the copies, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the Binet arm's output right, and the differential prints `30000
checks, 0 failures` under `karac run --interp` and legacy `karac
build`.

## Benchmarks

The bench program uses the ★ arm. It calls `fib(i % 31)` for i from 0
to 150,000,000, every n in the problem's range in turn, and adds up the
results modulo 10^9 + 7. Every implementation prints `150000000 calls:
total 198468302`, the Kāra program under `karac __mir-run` included
(in 242 s).

Every mirror is the same loop of two running values. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.80 to 0.92 s |
| Rust (`rustc -O`) | 0.80 to 0.84 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.19 to 1.25 s |
| Go | 1.13 to 1.62 s |
| Python | 68.6 to 68.8 s |
| Kāra (legacy `karac build`) | 1.30 to 1.33 s |
| Kāra (`karac build --mir`) | 1.21 to 1.36 s |

Kāra checks every addition for overflow, as the Rust row with
`overflow-checks=on` does, and those three rows land together; C and
plain Rust do not check. Legacy `karac build` builds this program, so
`bench.sh` is the
`scripts/new-bench.sh` output unchanged and times the legacy build; the
`--mir` row is timed by hand at kara `10fdedabfc`. Under `karac
__mir-llvm-run` the program prints the same line in 10.6 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

## Compiler findings

kara B-2026-10-13-22 (missing-feature, fixed in kara `95778e966b`):
`f64.powi` did not exist. design.md's example of a destructured parameter computes a
distance with `(x2 - x1).powi(2)`, the only place the spec names a
power method on a float, and the library docs list no float math
methods at all. The Binet arm's `phi.powi(n as i32)` was refused by
`karac check`, the v2 backends and the legacy ones alike: "no method
'powi' on type 'f64'". What the implementation had was `pow`, with an
`f64` exponent, and `phi.pow(n as f64)` passed everywhere. Since the
fix the arm and the differential pass `karac check` and run right on
both v2 backends as written.
