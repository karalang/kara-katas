# 2311. Longest Binary Subsequence Less Than or Equal to K

You are given a binary string `s` and a positive integer `k`.

Return *the length of the **longest** subsequence of* `s` *that makes
up a **binary** number less than or equal to* `k`.

Note:

- The subsequence can contain **leading zeroes**.
- The empty string is considered to be equal to `0`.
- A **subsequence** is a string that can be derived from another string
  by deleting some or no characters without changing the order of the
  remaining characters.

```
s = "1001010", k = 5   ->  5      ("00010")
s = "00101001", k = 1  ->  6      ("000001")
```

**Constraints:** `1 <= s.length <= 1000`; `s[i]` is either `'0'` or
`'1'`; `1 <= k <= 10^9`.

A `0` adds nothing to the value wherever it sits, so every `0` can be
taken. A `1` costs `2^p`, where `p` is the number of bits taken to its
right, so reading from the right and taking each `1` while the value
stays at most `k` spends the least on each one. Since `k < 2^30`, no
`1` can sit 30 or more places up. O(n).

## Approaches

| file | mechanism |
|---|---|
| `subsequence.kara` ★ | greedy from the right over `s.bytes()`: each `0` taken, each `1` taken when `value + (1 << taken) <= k`, with fewer than 31 taken |
| `subsequence_naive.kara` | each length from `n` down: the smallest value of that length, the least subsequence in dictionary order, built with a stack that lets a larger bit go while enough bits remain; the first length whose smallest is at most `k`. O(n^2) |
| `subsequence_dp.kara` | `least[l]`, the smallest value of a subsequence of length `l` so far, held at `k + 1` once past `k`; each bit extends every length, longest first. O(n^2) |
| `subsequence_suffix.kara` | counted: `k` has `width` bits, so every `0` before the last `width` places is taken, and those last places whole when their value is at most `k`, all but one of them when not |
| `subsequence_iter.kara` | `s.bytes().iter().rev().fold` of a `(value, taken)` pair, the same rule as the ★ arm |
| `subsequence_solution.kara` | LeetCode's Rust template: `k: i32`, `as_bytes()` walked with `for &b in bytes.iter().rev()`, the value an `i64`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; all ones,
all zeros, one bit, a string whose whole value is `k`, and 36 ones under
`10^9`; 1000 bits, half of them ones, under `10^9`; then 1000 random
strings of 1 to 40 bits, ones one time in 1 to 4, with `k` from 1 to
`2^30`, with a checksum and the lengths in all. `subsequence.py`
mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 10 edits:
`struct Solution;` to `struct Solution {}`; `as_bytes()` to `bytes()`;
the pattern `&b` to `b`; `&&` to `and`; the suffix of the two `1i64`
dropped; `k as i64` to `k`, as an `i32` widens on its own; `taken`
given the type `i32`, which it is returned as; and, in the harness's
wrapper, `Solution::` to `Solution.` and the `as i64` on the answer
dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subsequence, one for each subset of the places, is
read as a binary number, leading zeros and all, and the longest whose
value is at most `k` is the answer. No greedy and no table. It checks
300 random strings of 1 to 14 bits, ones one time in 1 to 4, with `k`
from 1 to `2^29`; then 30 of ones alone, where only the low places can
be taken; then 30 of 16 bits. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at least the number of zeros and at most the length |
| P3 | a `0` appended and `k` made `2 k + 1`: one more |
| P4 | a `0` put in front: one more |
| P5 | `k` raised to at least the string's own value: the whole length |
| P6 | each arm agrees with at least three of the other five |

P3 holds because a `0` at the end doubles every value that takes it,
and `v <= k` exactly when `2 v <= 2 k + 1`; P4 because a leading `0`
changes no value.

The differential prints `360 cases: checksum 985821719, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that walks
every subset of the places the same way. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the zeros not taken | P1 236, P2 172, P3 295, P4 360, P5 238, P6 236 |
| M5 | ★: each one placed a bit too high | P1 24, P5 89, P6 24 |
| M6 | ★: the last bit never read | P1 299, P2 37, P5 360, P6 299 |
| M7 | naive: a larger bit kept on the stack | P1 46, P2 30, P4 86, P6 46 |
| M8 | naive: a bit let go with one too few left | P1 45, P3 41, P6 45 |
| M10 | naive: the value read from its last bit | P1 49, P3 66, P4 63, P5 37, P6 49 |
| M12 | dp: each length extended shortest first | P1 49, P3 41, P6 49 |
| M13 | dp: the empty subsequence left unset | P1 360, P2 238, P3 360, P4 360, P5 360, P6 360 |
| M15 | dp: the shortest length that fits | P1 323, P2 214, P3 360, P4 360, P5 334, P6 323 |
| M17 | suffix: the width of `k` one bit short | P1 20, P5 90, P6 20 |
| M18 | suffix: a string as long as `k` taken whole | P1 4, P4 4, P6 4 |
| M19 | suffix: the zeros counted through the end | P1 63, P2 36, P3 104, P4 11, P5 67, P6 63 |
| M22 | iter: a one counted when it does not fit | P1 86, P6 86 |
| M24 | iter: each one valued 1 | P1 19, P3 9, P6 19 |
| M26 | iter: a one taken that passes `k` by one | P1 15, P6 15 |
| M27 | solution: a value equal to `k` refused | P1 10, P3 10, P5 87, P6 10 |
| M29 | solution: the guard at 3 bits | P1 206, P3 138, P5 253, P6 206 |

P1 and P6 kill all seventeen, P3 and P5 ten each, P4 seven and P2 six.
P5, `k` raised to the string's own value, fails where an edit refuses
a value it should take, which is most of them: a value equal to `k`, a
one placed too high, a width one bit short. P3 fails where the place of
a bit is miscounted, since the appended `0` moves every bit up one; P4,
the leading `0`, where the zeros are not all taken or the walk starts
from the wrong end. P2 fails for fewer than the zeros or more than the
length. M22 and M26 overcount by a little, only where the literal
reading sees it, as do the suffix arm's string as long as `k` (M18) and
the naive arm's stack edits (M7, M8) for the properties they miss.

Of the thirty-one, fourteen were not kept. The dp arm's guard refusing
a value equal to `k` (M16) is equivalent: a length whose least value is
`k` can only be extended past `k`, which is capped anyway. A value
equal to `k` refused in the ★ (M2), naive (M9) and suffix (M20) arms
fails as the template's (M27); a one taken without its value in the ★
(M3) and template (M30) arms as the suffix arm's tail read without its
first bit (M21), and none of the three is kept, so that no arm leans on
the one shape; the walk from the left in the ★ (M4), dp (M14, a bit
placed above, not below), iter (M23) and template (M31) arms all fail
alike, and none is kept; the naive arm's value capped at `k` (M11) as
the iter arm's one counted when it does not fit (M22); the zeros not
taken in the iter (M25) and template (M28) arms as the ★ arm's (M1).
The iter arm's M26 replaces its fit tested against `k - 1`, which
failed as the value equal to `k` refused.

## Verification

Every arm prints the same output as `subsequence.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, suffix, iter and template arms take 0.2
to 0.3 s, and the naive and dp arms, quadratic in the 1000-bit string,
1.1 and 1.2 s. The differential takes 9.7 s there, most of it the
literal reading's `2^16` subsets for each 16-bit string, and 0.6 s
under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 1000 strings of 1000 bits once, ones one time in 1 to
8, then makes 100 passes over them with the ★ arm in all five
languages, string `a` in pass `p` under `k = 10^7 (p + 1) + a`. Every
implementation prints `100 passes over 1000 strings of 1000 bits:
checksum 211073379`. Each walks the string's bytes from the right with
the value and the count in 64-bit integers, and none allocates in the
loop.

BENCHTAB
