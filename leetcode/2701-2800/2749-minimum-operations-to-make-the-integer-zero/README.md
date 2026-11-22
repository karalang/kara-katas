# 2749. Minimum Operations to Make the Integer Zero

You are given two integers `num1` and `num2`.

In one operation, you can choose integer `i` in the range `[0, 60]` and
subtract `2^i + num2` from `num1`.

Return *the integer denoting the **minimum** number of operations
needed to make* `num1` *equal to* `0`.

If it is impossible to make `num1` equal to `0`, return `-1`.

```
num1 = 3, num2 = -2  ->  3
num1 = 5, num2 = 7   ->  -1
```

**Constraints:** `1 <= num1 <= 10^9`, `-10^9 <= num2 <= 10^9`.

## Approaches

k operations take away k `num2`s and k powers of two, so they reach
zero exactly when `t = num1 - k num2` is a sum of k powers of two: that
needs at least as many as t has set bits, and no more than t itself,
since each power is at least 1; any count between is reached by halving
pieces. The answer is the least such k; once k passes the bits of t,
which never exceed 36 here, it is reached by 60 or never.

| file | mechanism |
|---|---|
| `zero.kara` ★ | the least k from 1 to 60 with `t.count_ones() <= k` and `k <= t`. O(60) |
| `zero_kernighan.kara` | the same test with t's set bits counted by hand, `t &= t - 1` once a bit, stopping as soon as there are more than k. O(60 log t) |
| `zero_split.kara` | for each k, t cut into its powers of two, counted by exponent in a `Vec`, and the largest piece above 1 split in halves until there are k pieces or every piece is 1; the first k by `find` with `unwrap_or(-1)`. O(60 (log t + k)) |
| `zero_binary.kara` | t written out in base 2 by an f-string's `:b`, its set bits the `'1'`s counted by `filter` and `count`. O(60 log t) |
| `zero_solution.kara` | a Rust solution as LeetCode's Rust users write it, `1..=60i64` with the inputs widened `as i64`, `continue` while t is below k, and `count_ones()` cast back, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; one step of
`2^0`; a power of two less one; three of LeetCode's extremes; 2000
random pairs with num1 up to 100 and num2 from -10 to 10; and 100000
across LeetCode's whole range, the last two with the sum of the answers
and a checksum. `zero.py` mirrors the ★ arm and its output is
byte-identical.

```
3
-1
1
10
12
-1
13
2000 small pairs: steps sum to 5930, checksum 604303977
100000 pairs: steps sum to 748920, checksum 505778889
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: k operations from 1 to 60, each tried as every way of picking
k powers `2^i` with i from 0 to 60, largest first, whose sum with k
`num2`s is num1, with no counting of set bits. It draws 1000 random pairs
with num1 from 1 to 30 and num2 from -3 to 3, then 3000 across
LeetCode's whole range, all before any arm answers; the literal reading
is asked only of the first 1000.

| | property |
|---|---|
| P1 | num1 up to 30, the answer is the literal reading's |
| P2 | -1 or from 1 to 60; and for an answer k, t = num1 - k num2 has at most k set bits and is at least k |
| P3 | num1 and num2 both doubled: no more steps, unless there was no way |
| P4 | num2 made 0: as many steps as num1 has set bits |
| P5 | num1 up to 30, an answer k from 2 on: one step of the right power first leaves k - 1 steps, and no step leaves fewer |
| P6 | each arm agrees with at least three of the other four |

P5 takes each step of `2^i + num2` for i up to 40 and asks the arm
again; the num1 left may be 0 or below, which the arms answer by the
same rule.

The differential prints `4000 cases: checksum 358344821, 120000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same search gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M4 fail the same checks, both refusing
exactly k set bits; so do M2 and M3, both refusing a t of exactly k. Two
first tries survived and were replaced: the kernighan arm's loop stopped
at a t of 1, which a loop clearing the lowest bit first reaches only
from t = 1, where k = 1 answers anyway; and the split arm kept a split
piece whole, which can change an answer only when k passes t, and
changed none of the drawn cases.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: exactly k set bits refused | P1 605, P4 4000, P5 110, P6 1188 |
| M2 | ★: t of exactly k refused | P1 28, P4 33, P6 28 |
| M3 | kernighan: t of exactly k refused | P1 28, P4 33, P6 28 |
| M4 | kernighan: exactly k set bits refused | P1 605, P4 4000, P5 110, P6 1188 |
| M5 | split: only pieces of 2 ever split | P1 321, P3 236, P5 136, P6 1210 |
| M6 | split: the ones bit never counted | P1 372, P2 663, P3 663, P4 2012, P6 686 |
| M7 | binary: the zeros counted, not the ones | P1 885, P2 2252, P3 1161, P4 3550, P5 140, P6 2520 |
| M8 | binary: any t from 0 let through | P1 21, P2 21, P5 6, P6 21 |
| M9 | solution: one step never tried | P1 146, P4 139, P5 436, P6 146 |
| M10 | solution: t one below k let through | P1 15, P2 15, P6 15 |

## Benchmarks

The bench draws `10^6` pairs across LeetCode's whole range, all of them
first, then answers each 10 times by the ★ arm in all five languages:
the set bits are `count_ones` in Kāra and Rust, `__builtin_popcountll`
in C, `bits.OnesCount64` in Go and `int.bit_count` in Python. Every
implementation prints `1000000 pairs, 10 rounds: steps sum to 74967540,
checksum 941969559`.

BENCHTAB

## Verification

All five arms print the same output as `zero.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The kernighan, split and binary arms checked clean as first written.
The ★ arm cast `t.count_ones() as i64`, and `karac check` warned that
the cast is redundant, `count_ones` giving an `i64`; `karac fix` took it
off.

LeetCode's Rust template took 7 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `1..=60i64` lost its suffix and
`num1 as i64` and `num2 as i64` their casts, since an `i32` widens into
`i64` arithmetic by itself; the `(x.count_ones() as i64)` cast went too;
and `Solution::` became `Solution.`, with the wrapper's `as i64`
dropped.

The differential first compared `after.iter().min() == Some(value -
1)`, an `Option[ref i64]` against an `Option[i64]`; `karac check`
refused it and `karac fix` wrote `.min().cloned()`.
