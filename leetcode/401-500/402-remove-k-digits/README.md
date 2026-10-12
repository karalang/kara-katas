# 402. Remove K Digits

Given a non-negative integer `num` written as a string and an integer
`k`, remove `k` digits so that the number left is as small as possible,
and return it as a string with no leading zeros ("0" if nothing is
left).

```
num = "1432219", k = 3  -> "1219"
num = "10200",   k = 1  -> "200"
num = "10",      k = 2  -> "0"
```

**Constraints:** `1 <= k <= num.length <= 10^5`; `num` is digits only
and has no leading zeros except for the number 0 itself.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `remove_k_digits.kara` ★ | a stack that keeps digits rising: read the digits left to right, and while removals remain pop every top digit larger than the next one; removals left at the end come off the top | O(n) | O(n) |
| `remove_k_digits_greedy.kara` | one removal at a time: drop the first digit larger than the one after it, or the last digit if the number never falls, and repeat `k` times | O(n k) | O(n) |
| `remove_k_digits_window.kara` | choose each kept digit: the next of the `n - k` kept digits is the smallest in the window after the last pick that still leaves enough digits, the leftmost on a tie | O(n (k + 1)) | O(n) |
| `remove_k_digits_next.kara` | the window arm's picks from a table: `next[i][d]` is the first position at or after `i` holding digit `d`, so each pick tries `d` = 0, 1, ... until its next position lies inside the window | O(10 n) | O(10 n) |
| `differential.kara` | the four arms on 3,000 random cases, five properties, one of them a brute force over every choice of digits | — | — |

Every arm prints the same 13 lines: the three LeetCode examples, nine
edge cases (a single digit, equal digits, rising and falling numbers,
zeros inside the number, every digit but one removed), and for 3,000
random numbers of 1 to 40 digits with `k` from 0 to the length, how
many digits are kept and a checksum. `k = 0` is outside LeetCode's
constraints and inside every arm's. `remove_k_digits.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. For each of 3,000
random cases it makes a number of 1 to 40 digits, one of up to 10
digits, and one whose digits never fall.

| | property |
|---|---|
| P1 | `k = 0` leaves the number as it is |
| P2 | `k = n` leaves `"0"` |
| P3 | the result is a subsequence of the number, of at most `n - k` digits, with no leading zero unless it is `"0"` |
| P4 | for up to 10 digits, the result is the smallest value left by any choice of `n - k` digits, found by trying all `2^n` |
| P5 | a number whose digits never fall keeps its first `n - k` digits |

It prints `3000 cases, 4 arms, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | stack: an equal digit is popped too | P4 197, P5 949 |
| M2 | stack: removals left at the end are not made | P2 2714, P3 428, P4 1144, P5 2751 |
| M3 | stack: leading zeros are kept | P3 1346, P4 306 |
| M4 | greedy: a number that never falls loses its first digit | P4 500, P5 2236 |
| M5 | greedy: the last peak is removed, not the first | P4 716 |
| M6 | window: a tie takes the rightmost digit | P4 197, P5 949 |
| M7 | window: the window stops one digit short | P4 1176 |
| M8 | next: a picked position may be picked again | P1 2877, P3 1080, P4 1487, P5 2201 |

M1 and M6 fail exactly the same checks: popping an equal digit off the
stack and taking the rightmost of equal digits in a window both keep the
later copy, which leaves fewer digits to choose from. M5 and M7 are seen
only by the brute force; their results are well formed and merely not
the smallest.

## Verification

All four arms print the same output as `remove_k_digits.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints `60000
checks, 0 failures` under `karac __mir-run` and
`karac __mir-llvm-run`. The greedy, window and table arms also match
under `karac run --interp`.

The arms and the differential run under `karac __mir-llvm-run` since
compiler commit 62f5f6de04 added the `String.as_str` native, which
`remove_kdigits` needs because it takes a `Str` and the random cases
pass it a `String`. The frozen legacy backends refuse the rest: its
typechecker refuses `*c` on the items of `stack.iter()` in the ★ arm
and the differential, as in katas 382 to 401, and its codegen has no
`bytes()` or `len()` on a `Str` parameter, which stops LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build` on the other three.
None of these is filed.

## Benchmarks

The bench program uses the ★ arm on 300 random numbers of 100,000
digits (the problem's limit), each with a random `k` from 0 to the
length, built from an LCG. It counts the digits kept and folds them into
a checksum. Every implementation prints `300 numbers of 100000 digits:
24216029 digits kept, checksum 235045434`; a 3-number cut of the Kāra
program under `karac __mir-run` prints the same as the C program cut the
same way. Spot timings on a shared 4-core container (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.29 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.36 s |
| Rust (`rustc -O`) | 0.37 s |
| Go | 0.71 s |
| Python | 9.4 s |

The legacy `karac build` refuses the Kāra program, as above. The
Kāra program prints the same line under `karac __mir-llvm-run` in
5.5 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

No new findings. The kata ran into the missing `String.as_str` native
on `karac __mir-llvm-run`, which every kata since 383 that passes a
`String` to a `Str` parameter hit, and which compiler commit 62f5f6de04
has since added.
