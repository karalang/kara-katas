# 1518. Water Bottles

There are `numBottles` water bottles that are initially full of water. You
can exchange `numExchange` empty water bottles from the market with one
full water bottle. Drinking a full bottle turns it into an empty bottle.
Given `numBottles` and `numExchange`, return the maximum number of water
bottles you can drink.

```
numBottles = 9,  numExchange = 3  ->  13
numBottles = 15, numExchange = 4  ->  19
```

**Constraints:** `1 <= numBottles <= 100`; `2 <= numExchange <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `bottles.kara` ★ | rounds: drink every full bottle, trade the empties in whole lots, keep the remainder, until fewer empties than one trade are left. O(log n) rounds |
| `bottles_one.kara` | one trade at a time: each trade gives `k` empties for a bottle that is drunk and comes back empty, so the empties fall by `k - 1`. O(n / k) |
| `bottles_formula.kara` | closed form `n + (n - 1) / (k - 1)`: every trade costs `k - 1` empties net, and the last empty can never be traded. O(1) |
| `bottles_rec.kara` | recursion on (full, empty): drink the full ones, trade what the empties buy, recur on the rest |
| `bottles_solution.kara` | LeetCode's Rust template (`let (mut drunk, mut full, mut empty) = (0, num_bottles, 0)` over `i32`), the ★ arm, carried by `karac fix`. **Blocked by B-2026-11-08-18**: see below |
| `differential.kara` | the four arms that check against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples, one bottle and
100 bottles at 2 for 1, then checksums of the answers for every pair of 1
to 100 bottles and 2 to 100 for 1, and for 1000 random pairs of up to
1000000 bottles and 2 to 21 for 1. `bottles.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: one bottle at a time is drunk, its empty kept, and a trade made
as soon as `k` empties are in hand. It checks 3000 problems of 1 to 300
bottles and 2 to 30 for 1.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | one more bottle gives at least one more drink |
| P3 | a dearer trade (`k + 1`) never gives more |
| P4 | `n <= answer <= 2 n - 1` |
| P5 | with `n >= k`, the answer is `k` plus the answer for `n - k + 1` (drink `k`, trade them for one more full bottle) |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 526349344, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Eleven edits to the differential, two to four to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All eleven are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the remainder of a trade thrown away (`empty = 0`) | P1 1320, P5 453, P6 1320 |
| M2 | ★: the empties replaced, not added to | P1 1320, P5 453, P6 1320 |
| M3 | ★: trades priced at `k + 1` | P1 1764, P2 246, P3 313, P5 616, P6 1764 |
| M4 | ★: stop with one full bottle left | P1 1449, P2 43, P4 9, P5 437, P6 1449 |
| M5 | one: a trade only with more than `k` empties | P1 415, P5 11, P6 415 |
| M6 | one: a trade costs `k`, not `k - 1` | P1 1634, P5 269, P6 1634 |
| M7 | one: one bottle fewer to start | P1 3000, P4 162, P6 3000 |
| M8 | formula: `n / (k - 1)` | P1 379, P4 102, P6 379 |
| M9 | formula: `(n - 1) / k` | P1 1761, P5 333, P6 1761 |
| M10 | rec: the recursion trades at `k + 1` from the second round | P1 798, P5 72, P6 798 |
| M11 | rec: the remainder dropped | P1 1320, P5 453, P6 1320 |

P1 and P6 kill all eleven, P5 nine, P4 three, P2 two, P3 one. M1, M2 and
M11 fail the same problems: each loses exactly the empties a trade leaves
over.

## Rust template: B-2026-11-08-18

LeetCode's Rust template, written as Rust writes it:

```rust
let (mut drunk, mut full, mut empty) = (0, num_bottles, 0);
while full > 0 {
    drunk += full;
    empty += full;
    full = empty / num_exchange;
    empty %= num_exchange;
}
drunk
```

`karac fix` made 6 edits (`struct Solution;` to `struct Solution {}`, the
pattern to `let mut (drunk, full, empty) = ..`, `Solution::` to
`Solution.`), and then `karac check` refuses `full = empty / num_exchange`
and `drunk` with "implicit coercion from 'i64' to 'i32' would narrow".
Rust fixes the two `0`s to `i32` from `drunk += full`; Kāra leaves them
`i64`, and a compound assignment widens the right side instead. The same
happens without a tuple: `fn f(n: i32) -> i32 { let mut a = 0; a += n; a }`
is refused. That extends B-2026-11-08-18 (a literal never fixed to `u64`
or `usize`, kata 1510). The file is kept as `karac fix` left it; typed
`let mut (drunk, full, empty): (i32, i32, i32) = (0, num_bottles, 0);` it
checks and prints the same output as the other arms, so it is left out of
the differential.

## Benchmarks

The bench asks the ★ arm 20000000 questions, `n = i * 7919 mod 10^9 + 1`
bottles and `k = i mod 99 + 2`, in all five languages: from 4 rounds of two divisions (at `k` near 100)
to 30 (at `k = 2`) per question. Every implementation prints
`20000000 questions up to 10^9 bottles and 2 to 100 for 1: checksum
447719839`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `d8a8878fe` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.389 s |
| Rust (`rustc -O`) | 0.394 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.396 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.404 s |
| Kāra (`karac build`) | 0.406 s |
| Go | 0.479 s |
| Python | 11.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (0.394 s and 0.399 s on one run).

Kāra is 1.02x Rust under overflow checks by median: the time is the
latency of the dependent divisions, the same in every compiled language.

## Verification

All four checking arms print the same output as `bottles.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.1 to 0.2 s, the one-trade arm
6.1 s, and the differential 0.2 s.

## Writing it

The Kāra arms were written in Kāra and `karac fix` had nothing to change.
