# 1137. N-th Tribonacci Number

The Tribonacci sequence Tn is defined as follows:

T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0.

Given `n`, return the value of Tn.

```
n = 4   ->  4         (T3 = 0 + 1 + 1 = 2, T4 = 1 + 1 + 2 = 4)
n = 25  ->  1389537
```

**Constraints:** `0 <= n <= 37`; the answer is guaranteed to fit within a
32-bit integer, `answer <= 2^31 - 1`.

The arms are `fn tribonacci(n: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `tribonacci.kara` ★ | three running values, T(i), T(i + 1) and T(i + 2), each step replacing the oldest with the sum of all three; after `n` steps the first is T(n). O(n) |
| `tribonacci_memo.kara` | recursion on the definition, each value remembered once found in a `Vec.filled(n.max(2) + 1, -1)` passed down as `mut ref`, so every T(k) is computed once. O(n) |
| `tribonacci_table.kara` | the whole sequence up to `n` in a list, each entry the sum of the three before it. O(n) |
| `tribonacci_matrix.kara` | the step as a 3 by 3 matrix of `Array[Array[i64, 3], 3]`, raised to the `n`th power by squaring; the power holds T(n) in its first column's middle row. O(log n) |
| `tribonacci_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `n: i32`, a `[0, 1, 1]` array indexed through `as usize`, rotated in place over `3..=n`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 8 lines: the answers for LeetCode's two
examples, every T(n) the constraints allow, 0 to 37, eight to a line,
and over 2000 random `n` from 0 to 37 the answers summed and a checksum
(`2000 random n: answers total 214323041485, checksum 360753159`).
`tribonacci.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: T(0), T(1) and T(2) given, and each later term the sum of the
three before it, every term kept in a list. That is the table arm's own
construction, since the statement is the algorithm here; the five
properties below compute no answer. The constraints allow 38 inputs, so
the differential checks every one, on every arm.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | three terms in a row sum to the next |
| P3 | no term is smaller than the one before |
| P4 | T(n) is even exactly when `n` leaves 0 or 3 over 4 |
| P5 | T(m + k) = T(m + 1) T(k) + (T(m) + T(m - 1)) T(k - 1) + T(m) T(k - 2), at every split of `n` with `m >= 1` and `k >= 2` |
| P6 | over 3 the terms repeat every 13 |

All 4015 checks pass on every arm: `38 n from 0 to 37: checksum
613603080, 4015 checks over 5 arms: 0 failures`. A Python reading
(the sequence, the six properties asserted over it, the same count and
checksum) gives the same line.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-eight are caught; two are
equivalent. Keeping terms modulo 2^31 - 1 in the table arm changes
nothing, because the largest term the constraints allow, T(37) =
2082876103, is below 2147483647. Sending `n = 2` through the solution
arm's loop (`if n < 2` for `if n < 3`) changes nothing either: `3..=2`
is empty and `t[2]` is already T(2). Fifteen are kept, no two failing
the same checks; two of them stop the run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each term the sum of the two before it | P1 34, P2 34, P4 18, P5 629, P6 19 |
| M2 | ★: the middle value returned | P1 37, P4 19, P5 630 |
| M3 | ★: terms capped at 10^9 | P1 2, P2 2, P4 1, P5 69, P6 1 |
| M4 | memo: T(n - 2) taken twice | P1 35, P2 34, P4 18, P5 628, P6 17 |
| M5 | memo: every term remembered as 0 | P1 35, P2 3, P3 1, P4 17, P5 8, P6 2 |
| M6 | memo: each term remembered one too large | P1 33, P2 33, P4 17, P5 625, P6 2 |
| M7 | table: the list one term short | stops: index out of bounds |
| M8 | table: the list's last term returned | P1 1, P2 1, P4 1, P5 69, P6 1 |
| M9 | table: terms kept modulo 10^9 + 7 | P1 2, P2 2, P3 2, P4 1, P5 69, P6 2 |
| M10 | matrix: the product reads `y` transposed | P1 34, P2 35, P5 630, P6 9 |
| M11 | matrix: the zero bits multiplied in | P1 36, P2 35, P3 28, P4 1, P5 613, P6 17 |
| M12 | matrix: the step not squared before the last bit | P1 35, P2 12, P3 3, P4 5, P5 531, P6 14 |
| M13 | solution: the middle value returned | P1 35, P2 2, P4 18, P5 563, P6 1 |
| M14 | solution: the rotation done in the wrong order | stops: integer overflow |
| M15 | solution: the first three read backwards | P1 2, P2 2, P3 1, P4 2, P5 195, P6 2 |

Every input is checked, so P1 catches all thirteen edits that let the
run finish, and P5 does too: it ties each term to every pair of smaller
ones, so a single wrong term fails up to 35 splits, and an edit wrong
only at `n = 0` (M8) still fails 69 checks there, every split that reads
T(0). P2, P4 and P6 each catch twelve. P2 misses the middle value
returned (M2), which is T(n + 1) and obeys the recurrence as well as
T(n) does; so does P6, whose period holds for any shift of the
sequence. P4 misses the transposed product (M10), whose wrong answers
all happen to keep T(n)'s parity. P3 catches five, the edits whose
answers fall somewhere (M5, M9, M11, M12, M15); every shifted or
inflated sequence still grows. The two that stop the run do so on the
backends' own checks: the table arm's list one term short reads past its
end, and the solution arm's rotation in the wrong order copies `t[2]`
into both older places, so each term is twice the one before and the sum
for `n = 33` overflows the `i32` LeetCode's signature uses.

Of the thirteen caught and not kept, seven fail exactly as a kept one:
the middle value returned in the matrix arm (the top row's term) as M2;
each term the sum of two in the table arm, the step dropping its third
term and the product dropping its last term in the matrix arm, and the
middle value counted twice in the solution arm, as M1; one step too few
in the solution arm as M13; and a remembered 0 recomputed in the memo
arm stops on an index out of bounds as M7 does. The other six (T(2) or
T(0) started wrong, one step too few in the ★ arm, T(1) set to 0 in the
memo arm) each fail in a way of their own and were not needed.

## Verification

Every arm prints the same output as `tribonacci.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, memo and table arms were written as Kāra and checked clean as
written. `karac fix` carried the solution arm in three rounds:
`Solution::tribonacci` to `Solution.tribonacci`; then `struct Solution
{}` declared; then the `as i64` that widens the call's `i32` for nothing
dropped. `karac fix` carried the matrix arm in one round, once the gap
below was fixed: it declared `result` and `step` as
`Array[Array[i64, 3], 3]`.

The kata found one gap:

- **B-2026-11-12-9** (fixed): the matrix arm binds `let mut result =
  [[1, 0, 0], [0, 1, 0], [0, 0, 1]]` and passes it to `multiply(x:
  Array[Array[i64, 3], 3], ...)`. A list literal with no expected type
  is a `Vec`, so that is refused, and B-2026-11-10-47 already explains
  and fixes the flat case (`let local = [127u8, 0, 0, 1]` into
  `Array[u8, 4]`). But it recorded only the outer length, so a nested
  literal got six bare `expected 'Array[Array[i64, 3], 3]', found
  'Vec[Vec[i64]]'` errors and no fix, and `result = multiply(result,
  step)` counted as another value, though the `Array` it stores has the
  lengths the declaration names. The binding now records its literal's
  shape at every level, storing an `Array` into it keeps the fix, and
  each use says why the binding is a `Vec` and offers `result:
  Array[Array[i64, 3], 3]`.

## Benchmarks

The bench answers 20,000,000 queries, each `n` drawn from 0 to 37, the
whole range the constraints allow, with the ★ arm: about 19 steps of
three additions each. Every implementation prints `20000000 queries, n
from 0 to 37: answers total 2400014784415620, checksum 840019770`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `87bec305bc`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.323 to 0.500 s | 0.426 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.395 to 0.458 s | 0.430 s |
| Rust (`rustc -O`) | 0.402 to 0.487 s | 0.438 s |
| Go | 0.407 to 0.630 s | 0.502 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.437 to 0.641 s | 0.522 s |
| Kāra (`karac build`) | 0.415 to 0.622 s | 0.533 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.408 to 0.634 s | 0.542 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.416 to 0.675 s | 0.567 s |
| Python | 20.6 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. The work is the three running values and the generator,
with no memory touched. Kāra checks every addition for overflow, as
Rust does under `overflow-checks=on`, and the two land within each
other's spread, which runs 0.20 to 0.26 s wide: Rust under overflow
checks takes about 0.92x to 0.96x Kāra's median time. C and Rust
without the checks take about 0.75x and 0.77x, and Go about 0.89x.
Python takes about 36x.
