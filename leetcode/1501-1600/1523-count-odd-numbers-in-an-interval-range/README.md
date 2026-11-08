# 1523. Count Odd Numbers in an Interval Range

Given two non-negative integers `low` and `high`, return the count of odd
numbers between `low` and `high`, inclusive.

```
low = 3, high = 7   ->  3   (3, 5, 7)
low = 8, high = 10  ->  1   (9)
```

**Constraints:** `0 <= low <= high <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `count.kara` ★ | `0..=high` holds `(high + 1) / 2` odd numbers and `0..low` holds `low / 2`, so the interval holds the difference. O(1) |
| `count_parity.kara` | the `high - low` steps between the ends pair off into one odd number each, and one more is left over when either end is odd. O(1) |
| `count_ends.kara` | the first odd number is `low \| 1` and the last is `high`, less one when it is even; odd numbers two apart from one to the other. O(1) |
| `count_solution.kara` | LeetCode's Rust template (`i32`, `&&`, `(low & 1) == 1`): the length halved, and one more when it is odd and starts odd. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

There is no iterator arm: an iterator over the interval is the
statement read literally, too slow for an interval of `10^9`, and it
is the differential's literal reading instead.

Every arm prints the same 8 lines: LeetCode's two examples and four
more at the edges (`0` to `0`, `5` to `5`, `0` to `10^9`, `10^9 - 1` to
`10^9`), then checksums of the answers for 3000 random intervals within
0 to 20 and 3000 within 0 to 10^9. `count.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: `(low..=high).filter(|x| x % 2 == 1).count()`. It checks 3000
intervals with both ends in 0 to 30, every random choice drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the interval moved up by 2 leaves the answer |
| P3 | the interval cut in two at a random place: the two answers sum to it |
| P4 | the answer and the answer for the interval moved up by 1 sum to its length |
| P5 | the interval from `2 low` to `2 high` holds `high - low` odd numbers |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 387700136, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Eight are killed, each the
same way under both backends; two survive, and both are equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `high / 2` for `(high + 1) / 2` | P1 1400, P3 1261, P4 3000, P6 1400 |
| M2 | ★: `(low + 1) / 2` for `low / 2` | P1 1485, P3 1219, P4 3000, P6 1485 |
| M3 | parity: `and` for `or` | P1 1477, P3 2480, P4 1477, P6 1477 |
| M4 | parity: the length, not the steps, halved | P1 1477, P3 2480, P4 1477, P6 1477 |
| M5 | ends: `low + 1` for `low \| 1` | P1 1485, P3 1219, P4 3000, P6 1485 |
| M6 | ends: `>=` for `>` | P1 336, P3 950, P4 475, P5 178, P6 336 |
| M7 | ends: high always less one | P1 1400, P3 1261, P4 3000, P6 1400 |
| M8 | template: the odd-length test dropped | P1 781, P3 1268, P4 1477, P6 781 |

The survivors are both in the template: testing `high`'s parity for
`low`'s (M9), since an odd length starts and ends on the same parity,
and `(n + 1) / 2` for `n / 2 + 1` (M10), since `n` is odd there.

## Benchmarks

The bench builds 2000000 random intervals within 0 to 10^9 once and
answers each 100 times by the ★ arm, in all five languages, summing each
pass. Every implementation prints `100 passes over 2000000 intervals
within 0 to 10^9: checksum 25275652`. The answer is two divisions, so
the pass is a loop the compilers may vectorize, and building the
intervals is a large share of the time.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `38553609c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.267 s |
| Rust (`rustc -O`) | 0.278 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.316 s |
| Kāra (`karac build`) | 0.314 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.369 s |
| Go | 0.431 s |
| Python | 19.2 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.31 s and 0.26 s on two runs).

Kāra is 0.86x Rust under overflow checks by median. The runs were noisy
(Kāra's eight ranged from 0.287 s to 0.411 s), so the order of the
middle rows is not firm. Not traced.

## Verification

All four arms print the same output as `count.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change.

## Writing it

The ★, parity and ends arms were written in Kāra and `karac fix` had
nothing to change. The Rust template took one edit in one round, `&&` to
`and`; the parenthesized `(low & 1) == 1` stays as it is, since Kāra's
`&` binds tighter than `==`. It checks and agrees with no hand edit.
