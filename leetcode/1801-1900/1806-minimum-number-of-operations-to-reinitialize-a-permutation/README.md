# 1806. Minimum Number of Operations to Reinitialize a Permutation

You are given an even integer `n`. You initially have a permutation
`perm` of size `n` where `perm[i] == i` (0-indexed). In one operation,
you will create a new array `arr`, and for each `i`: if `i % 2 == 0`,
then `arr[i] = perm[i / 2]`; if `i % 2 == 1`, then `arr[i] = perm[n /
2 + (i - 1) / 2]`. You will then assign `arr` to `perm`. Return the
minimum non-zero number of operations you need to perform on `perm` to
return the permutation to its initial value.

```
n = 2  ->  1
n = 4  ->  2
n = 6  ->  4
```

**Constraints:** `2 <= n <= 1000`, and `n` is even.

The arms are `fn reinitialize_permutation(n: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `reinitialize_permutation.kara` ★ | the operation applied as the statement writes it, a new `arr` built from `perm` by its two rules each time, until `perm` equals the permutation it started as. O(n * answer), at most O(n^2) |
| `reinitialize_permutation_track.kara` | one position followed: position `i` reads from `i / 2` or `n / 2 + (i - 1) / 2`, and every cycle of that map has a length dividing the length of the cycle through position 1, so the answer is that length. O(answer) |
| `reinitialize_permutation_cycles.kara` | the permutation's cycles, each walked once and marked in a `Vec[bool]`, and the answer the least common multiple of their lengths, through a recursive `gcd`. O(n log n) |
| `reinitialize_permutation_order.kara` | number theory: the operation moves the value at position `j` to `2 * j mod (n - 1)` for every `j` but the last, so the answer is the multiplicative order of 2 modulo `n - 1`, and 1 when `n - 1` is 1. O(answer) |
| `reinitialize_permutation_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let n = n as usize;` shadowing the parameter, a `Vec<usize>` collected from `0..n`, `vec![0; n]`, `perm == target`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples (`1 2 4`);
five edges, `n = 66` and `n = 514`, which are `2^k + 2` and have the
least answer for their size, `2k`, `n = 12` and `n = 14`, where `n - 1`
is a prime with 2 a primitive root and the answer is `n - 2`, and the
constraints' most, `n = 1000` (`12 18 10 12 36`); and every even `n`
from 2 to 1000, every case the constraints allow (`every even n to 1000:
checksum 6768435, total 81101, most 946`). `reinitialize_permutation.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★, track, cycles and order arms and the harness check
clean as first written. The Rust solution takes 15 fixes by `karac
fix`'s count, and its diff is: `struct Solution {}` added above the
`impl`, which LeetCode's editor supplies; `n as usize` to `n as i64` and
`Vec<usize>` to `Vec[i64]`; `vec![0; n]` to `Vec.filled(n, 0)`; and
`Solution::` to `Solution.` in the harness. Every arm's output matches
on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: `perm` built from `0..n`, each operation pushing `arr` by the
two rules, and the operations counted until `perm[i] == i` holds for
every `i`. It runs every case the constraints allow, each even `n` from
2 to 1000. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the answer is at least 1, and at most `n - 2` once `n` passes 2 |
| P3 | 2 to the answer is 1 modulo `n - 1` |
| P4 | the answer divides Euler's totient of `n - 1` |
| P5 | 2 to the answer is at least `n`, as it is 1 more than a multiple of `n - 1` |
| P6 | the ★ arm's answer |

Check warned twice that a cast from `i32` to `i64` is one Kāra makes
implicitly (`lossless_cast`), and `karac fix` removed both, 2 fixes. P5
first shifted 1 by the answer as it came, and the first two mutants of
the cycles arm crashed the differential, one with a shift by a negative
answer and one with a division by zero inside the mutated `gcd`; P5 now
takes an answer below 1 as failing, and those two mutants were replaced
by the two in the table. All 15,000 checks pass on every arm: `500
cases: checksum 6768435, 15000 checks over 5 arms: 0 failures`, under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, running the ★ arm's mirror over the same cases,
gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: only the last place compared, which never moves | P1 499, P3 499, P5 499, P6 1996 |
| M2 | ★: the two halves read the wrong way round | P1 494, P2 66, P3 479, P4 442, P6 1976 |
| M3 | track: the count started at 1 | P1 500, P2 67, P3 499, P4 499, P6 500 |
| M4 | track: a first step back to 1 not taken as the end | P1 1, P4 1, P6 1 |
| M5 | cycles: only the last cycle's length kept | P1 499, P3 499, P5 499, P6 499 |
| M6 | cycles: each cycle counted twice its length | P1 500, P2 79, P4 100, P6 500 |
| M7 | order: the exponent started at 0 | P1 499, P3 499, P4 493, P5 8, P6 499 |
| M8 | order: taken modulo n + 1, not n - 1 | P1 494, P2 66, P3 479, P4 442, P6 494 |
| M9 | solution: only the first place compared, which never moves | P1 499, P3 499, P5 499, P6 499 |
| M10 | solution: the permutation built two places too long | P1 494, P2 66, P3 479, P4 442, P6 494 |

## Benchmarks

The bench makes 3000 calls of the ★ arm, each `n` an even number to 1000
drawn from the checksum so far. It checks clean as first written. Every
implementation prints `3000 calls of even n to 1000: checksum
651957339`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.42 s against Rust's 0.37 s (0.32 s with overflow checks
on), C's 0.12 s and Go's 1.6 s; Python takes 24.7 s.
