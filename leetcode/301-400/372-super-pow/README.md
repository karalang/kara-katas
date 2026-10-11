# 372. Super Pow

Compute `a^b mod 1337`, where `a` is a positive integer and `b` is a very
large positive integer given as an array of its decimal digits.

```
a = 2, b = [3]                      -> 8
a = 2, b = [1, 0]                   -> 1024
a = 1, b = [4, 3, 3, 8, 5, 2]       -> 1
a = 2147483647, b = [2, 0, 0]       -> 1198
```

**Constraints:** `1 <= a <= 2^31 - 1`; `1 <= b.length <= 2000`;
`0 <= b[i] <= 9`; `b` has no leading zeros.

## Approaches

`b` can have 2,000 digits, so no arm ever forms it as a number. Reducing
`a` mod 1337 first keeps every product below `1337^2`, well inside an
`i64`.

| file | mechanism | time |
|---|---|---|
| `super_pow.kara` ★ | read the digits from the most significant: if the digits so far make `e`, one more digit `d` makes `10e + d`, and `a^(10e + d) = (a^e)^10 · a^d`, so the answer so far goes to its 10th power and gains a factor `a^d` | O(len(b)), about 20 products a digit |
| `super_pow_reverse.kara` | read the digits from the least significant, keeping `a^(10^i)` as a running base that contributes its `d_i`-th power and then goes to its own 10th power; square-and-multiply for each power | O(len(b)) |
| `super_pow_carmichael.kara` | `1337 = 7 · 191` is squarefree with `λ(1337) = lcm(6, 190) = 570`, so `a^(k + 570) = a^k` for every `a` and every `k >= 1`; reduce `b` mod 570 digit by digit, read a remainder of 0 as 570, and do one square-and-multiply | O(len(b)) |
| `super_pow_crt.kara` | work mod 7 and mod 191 apart: mod a prime `p` the answer is 0 when `p` divides `a`, and otherwise depends on `b` mod `p - 1` (Fermat); combine as `r7 · 191 · 4 + r191 · 7 · 82`, the two inverses | O(len(b)) |
| `differential.kara` | the four arms against repeated multiplication, 48,000 checks, five properties | — |

The lift of a remainder 0 to 570 (or to `p - 1`) is what keeps the
Carmichael and CRT arms right when `a` shares a factor with 1337: `7^570`
is 0 mod 7, but `7^0` is 1.

Every arm prints the same 11 lines: the four LeetCode examples, six edge
cases (a multiple of 1337, `1337 + 1`, the factors 7 and 191 as bases, an
exponent of 1, 2,000 nines), and a checksum over 300 random cases with
exponents of up to 200 digits. `super_pow.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. The oracle multiplies
`a` by itself `e` times, so the test keeps `e` at most 9,999. It draws
2,000 cases: a sixth of the bases are multiples of 7 and a sixth multiples
of 191, which share a factor with 1337, a sixth are small, and half are
anywhere up to `2^31 - 1`.

| | property |
|---|---|
| P1 | each arm gives the oracle's answer |
| P2 | leading zeros on `b` change no answer |
| P3 | `a` and `a + 1337` give the same answer |
| P4 | the answer for `a · c` is the product of the answers for `a` and `c` |
| P5 | `b` and `b + 570` give the same answer, on `b` and on a random 60-digit exponent |

It prints `2000 cases, 48000 checks, 0 failures` under `karac __mir-run`,
`karac run --interp`, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac
build`.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | digit: raises to the 10th power after multiplying in the digit | P1, 1693 failures |
| M2 | reverse: moves to the next power of ten before the multiply | P1, 1693 failures |
| M3 | square-and-multiply: multiplies on the even bits | P1 and P5, 5491 failures |
| M4 | Carmichael: a remainder of 0 mod 570 stays 0 | P1, 2 failures |
| M5 | Carmichael: reduces the exponent mod 190 | P1, 637 failures |
| M6 | CRT: takes the inverse of 191 mod 7 as 3 | P1 and P4, 2636 failures |
| M7 | CRT: reduces the exponent mod `p`, not `p - 1` | P1 and P5, 3624 failures |
| M8 | oracle: one multiplication short | P1, 7584 failures |

M1 and M2 both compute `a^(10e)` in place of `a^e`, which is consistent
under every property but P1. M4 is killed by two cases only: it is wrong
just when `a` shares a factor with 1337 and `e` is a multiple of 570, and
P5 cannot see it, since `b` and `b + 570` take the same wrong path.

## Verification

All four arms print the same output as `super_pow.py` under
`karac run --interp`, `karac __mir-run` (the v2 MIR interpreter), LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program answers 500 random bases with exponents of 2,000
digits, the problem's largest, with the ★ arm. The Kāra build and the C,
Rust, Go and Python mirrors all print `checksum 29454962`, and
`karac __mir-run` does too. Timings are not taken yet; they need a quiet
machine.

## Compiler findings

None.
