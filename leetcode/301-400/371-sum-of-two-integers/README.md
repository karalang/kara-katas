# 371. Sum of Two Integers

Given two integers `a` and `b`, return their sum without using the
operators `+` and `-`.

```
a = 1, b = 2   -> 3
a = 2, b = 3   -> 5
```

**Constraints:** `-1000 <= a, b <= 1000`.

## Approaches

`a ^ b` is the sum without carries and `(a & b) << 1` is the carries,
moved to where they land; two's complement makes the same bit work add
negative numbers.

| file | mechanism | time |
|---|---|---|
| `sum.kara` ★ | repeat `x = x ^ carry`, `carry = (x & carry) << 1` on `i64` until the carry is 0 | at most 64 rounds |
| `sum_recursive.kara` | the same step as a recursion, `get_sum(a ^ b, (a & b) << 1)` | at most 64 calls |
| `sum_bits.kara` | a ripple-carry adder over the 64 bits, reading bit `i` with `(a >> i) & 1` and setting it with `<< i` | 64 steps |
| `sum_u32.kara` | the carry loop on `u32`, where the carry out of bit 31 vanishes, read back with `(x as i32) as i64` | at most 32 rounds |
| `differential.kara` | the four arms against `a + b`, 100,000 checks, five properties | — |

The arms lean on three rules of the spec (design.md § Division, remainder
and shifts): `<<` never traps on the bits it shifts out, only on a shift
amount out of range, so a carry can run off the top of an `i64`; `>>` on a
signed integer is arithmetic; and `1 << 63` is a legal shift into the sign
bit. The case `-1 + -1` sends a carry through all 64 bits.

Every arm prints the same 11 lines: the two LeetCode examples, eight edge
cases (zeros, `-1 + 1`, both bounds, opposite bounds, a negative result,
`-1 + -1`, zero and a negative), and a checksum over 5,000 random pairs.
`sum.py` mirrors the ★ arm with a 64-bit mask, since Python's integers are
unbounded, and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms; the oracle is `a + b`.
The test draws 5,000 cases of three numbers, half within the problem's
`[-1000, 1000]` and half anywhere in about `±3.6 × 10^8`, so that even a
sum of three still fits the `u32` arm's `i32`.

| | property |
|---|---|
| P1 | each arm gives `a + b` |
| P2 | swapping `a` and `b` changes nothing |
| P3 | adding 0 on either side gives the number back |
| P4 | a number plus its negation is 0 |
| P5 | the sum is associative |

It prints `5000 cases, 100000 checks, 0 failures` under `karac __mir-run`
(about 15 seconds), `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | loop: the carry is not shifted | P1 and P4, 9905 failures |
| M2 | loop: `x | carry` in place of `x ^ carry` | P1 and P4, 9905 failures |
| M3 | recursive: the carry shifted by 2 | P1 and P4, 9905 failures |
| M4 | bits: stops at bit 62, so the sign bit is never set | P1 and P3, 5878 failures |
| M5 | bits: the carry ignores the case where only `y` and the carry are set | P1, P2, P4 and P5, 18012 failures |
| M6 | u32: reads the result back as unsigned | P1 and P3, 5878 failures |
| M7 | u32: keeps only the low 16 bits of `a` | P1 to P5, 17663 failures |
| M8 | bits: `% 2` in place of `& 1`, which gives -1 for an odd negative | P1 to P5, 14475 failures |

A first M3, `(a | b) << 1`, does not terminate: the recursion overflowed
the MIR interpreter's stack. It was replaced, because a mutant that crashes
says nothing about which property catches it.

## Verification

All four arms print the same output as `sum.py` under
`karac run --interp`, `karac __mir-run` (the v2 MIR interpreter), LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program adds five million random pairs in `[-1000, 1000]` with
the ★ arm. The C mirror shifts through `uint64_t`, since a left shift of a
negative `int64_t` is undefined in C. The Kāra build and the C, Rust, Go
and Python mirrors all print `checksum 428872360`.

### Apple M5 Pro, 2026-11-06

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14606+g162ee7a0e`
(g162ee7a0e, the v2/MIR backend), measured 2026-11-06, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| rust `-O -C overflow-checks=on` (equal-safety) | 76.5 ms ± 0.5 | 1.03× |
| c `clang -O3` | 77.6 ms ± 1.6 | 1.02× |
| **kāra `karac build`, seq** | **78.9 ms ± 1.1** | **—** |
| rust `-O` | 79.1 ms ± 1.0 | 1.00× |
| go `go build` | 99.2 ms ± 1.8 | 0.80× |

Kāra is 1.00× `rustc -O`, 1.03× equal-safety Rust, 1.02× C and 0.80× Go.
The gaps were not investigated on this host.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 38.1 ms ± 0.8 | 32.6 KiB | 1.0 MiB |
| rust | 68.2 ms ± 0.5 | 455.3 KiB | 1.1 MiB |
| kāra | 98.1 ms ± 1.6 | 66.9 KiB | 1.0 MiB |
| go | — | 2450.4 KiB | 2.7 MiB |

`karac build` is 2.6× clang's cold compile and 1.4× rustc's. Kāra's
68,496-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`checksum 428872360`).

## Compiler findings

None.
