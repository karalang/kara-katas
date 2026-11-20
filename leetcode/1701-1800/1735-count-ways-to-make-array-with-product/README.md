# 1735. Count Ways to Make Array With Product

You are given a 2D integer array, `queries`. For each `queries[i]`,
where `queries[i] = [ni, ki]`, find the number of different ways you can
place positive integers into an array of size `ni` such that the product
of the integers is `ki`. As the number of ways may be too large, the
answer to the `i`th query is the number of ways **modulo** `10^9 + 7`.

Return *an integer array* `answer` *where* `answer.length ==
queries.length`*, and* `answer[i]` *is the answer to the* `i`*th query.*

```
queries = [[2,6],[5,1],[73,660]]              ->  [4,1,50734910]
queries = [[1,1],[2,2],[3,3],[4,4],[5,5]]     ->  [1,2,3,10,5]
```

**Constraints:** `1 <= queries.length <= 10^4`;
`1 <= ni, ki <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `ways.kara` ★ | an array of n positive integers multiplies to k exactly when, for each prime p of k, the exponents of p in its places sum to p's exponent e in k, and the primes are shared out independently. Sharing e among n places is choosing where n - 1 dividers fall among e + n - 1 slots, C(n + e - 1, e) ways, so the answer is the product of those. k is factored by trial division, and C(m, e) is read off factorials and their inverses up to the largest n + 14, the inverses by Fermat's little theorem. O(N + q sqrt(k)) |
| `ways_pascal.kara` | no k up to `10^4` holds a prime more than 13 times (`2^13 = 8192`), so C(m, e) is only wanted for e up to 13: Pascal's rule fills those 14 columns for every m up to the largest n + 13, with no division at all. k is factored by trial division. O(14 N + q sqrt(k)) |
| `ways_sieve.kara` | a sieve up to the largest k records each number's smallest prime factor, so k comes apart by repeated division, and C(n + e - 1, e) is the product of (n - 1 + j) / j for j from 1 to e, each division a multiplication by j's inverse. O(K log log K + q log k) |
| `ways_solution.kara` | a Rust solution as LeetCode's Rust users write it, factorials and inverses up to a fixed 10014 in `vec![1i64; max_n + 1]`, a `comb` closure over `usize`, and `queries.iter().map(..).collect()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 6 lines: LeetCode's two examples, and one
list of the largest n and k, a prime k, and `2^13` over many places and
over one; then
the ways summed and a checksum for 3000 random lists of up to 5 queries
with n and k up to 36, 300 lists of up to 100 queries up to `10^4`, and
3 of up to `10^4` queries up to `10^4`, LeetCode's limits. `ways.py`
mirrors the ★ arm and its output is byte-identical.

```
[4, 1, 50734910]
[1, 2, 3, 10, 5]
[418224726, 10000, 83600675, 1]
3000 lists of up to 5 queries up to 36: ways sum to 87378299, checksum 837563803
300 lists of up to 100 queries up to 10000: ways sum to 4403328270924, checksum 430466689
3 lists of up to 10000 queries up to 10000: ways sum to 2951372544091, checksum 515182543
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the arrays of n positive integers whose product is k, counted
by choosing each place's value among the divisors of what is left and
the rest of the places from there. It checks 3000 random lists of 1 to 4
queries, each n from 1 to 6 and k from 1 to 36. Every case is drawn
before any arm answers. The queries P3 and P4 ask about go to each arm
in one list, since the template arm builds its factorials anew on every
call.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the queries reversed give the answers reversed |
| P3 | k split into its smallest prime's power and the rest, coprime, gives two answers whose product is the answer |
| P4 | the answer for n + 1 places is the sum, over the divisors d of k, of the answers for n places and product d |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 92271281, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the same count one place at a time, itself
checked against every `itertools.product` of n values up to k for n up
to 3 and k up to 12, gives the same checksum. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. No edit fails P2: each arm still
answers every query on its own. M8 counts every prime's share as C(n +
e, e), which is the true answer for n + 1 places, so it keeps P3 and P4,
which hold for any n, and fails P1 on all but the 26 problems whose k is
1. M5 makes the same change only for the primes trial division finds,
not a prime left over, and fails P3 and P4 too.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a prime left over after trial division counted as 2 ways, not n | P1 2515, P3 1573, P4 2945, P5 2515 |
| M2 | ★: each prime's share C(n + e - 1, 0), always 1 | P1 2405, P3 1554, P4 2627, P5 2405 |
| M3 | ★: trial division stops below the square root, `p * p < k` | P1 766, P3 610, P4 1760, P5 766 |
| M4 | pascal: each entry twice the one up and to the left | P1 2545, P3 1573, P4 2627, P5 2545 |
| M5 | pascal: each share read one row too low, C(n + e, e) | P1 2627, P3 1788, P4 2627, P5 2627 |
| M6 | pascal: a prime left over counted as n + 1 ways | P1 2707, P3 1788, P4 2627, P5 2707 |
| M7 | sieve: the sieve stops below the square root of the largest k | P1 140, P4 171, P5 140 |
| M8 | sieve: each share's running product over (n + j) / j | P1 2974, P5 2974 |
| M9 | solution: each share C(n + e - 1, e - e / 2) | P1 1677, P4 1881, P5 1677 |
| M10 | solution: a prime left over counted only when above 2 | P1 186, P3 1148, P4 2051, P5 186 |

## Benchmarks

The bench draws 10 random lists of `10^4` queries with n and k up to
`10^4`, LeetCode's largest, all of them first, then answers each 60
times by the ★ arm in all five languages; each answer builds its
factorials anew. Every implementation prints `10 lists of 10000
queries, 60 rounds: first answers sum to 69377126220, checksum
824049986`. Kāra, Rust and Go hold each query as a list of two; C holds
the queries as one array of pairs. The C build also runs clean under
gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ad6400d909` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.932 s |
| Rust (`rustc -O`) | 0.949 s |
| Kāra (`karac build`) | 0.963 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.987 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.053 s |
| Go | 1.188 s |
| Python | 30 s |

The sequential Kāra build is level with Rust and 6% faster than Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.932 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.069 s and 1.078 s on one
run).

## Verification

All four arms print the same output as `ways.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `ad6400d909`.

## Writing it

The ★, Pascal and sieve arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 19 edits:
`struct Solution {}` added, `Vec<..>` written `Vec[..]`,
`vec![1i64; max_n + 1]` written `Vec.filled(max_n + 1, 1)`, the `as
i64` casts of a loop index dropped, `Self::pow` written `Solution.pow`,
the closure's `-> i64` dropped, `res`'s `1i64` written `1` and `p`
declared `: i32` to meet the `i32` k, and `fn pow(mut b: i64, mut e:
i64)` rewritten to plain parameters rebound by `let mut`. The `comb`
closure's `usize` parameters and `q[0] as usize` carried over as
written: `n` is a `usize` throughout, never meeting an `i64`, and
`karac check` accepts it.

The differential took `karac fix` for 9 edits: `p` and `power` in
`split`, plain literals meeting the `i32` k only through operators,
declared `: i32`; five casts the `i32` values took to `i64` by
themselves dropped; and two `.clone()`s of a list passed to `arm`,
which only borrows it, dropped. `arm_name` in it indexes a list of
string literals for a `Str`, as #1662's does (B-2026-11-19-131).
