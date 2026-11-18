# 1621. Number of Sets of K Non-Overlapping Line Segments

Given `n` points on a 1-D plane, where the `ith` point (from `0` to
`n-1`) is at `x = i`, find the number of ways we can draw **exactly**
`k` **non-overlapping** line segments such that each segment covers two
or more points. The endpoints of each segment must have **integral
coordinates**. The `k` line segments **do not** have to cover all `n`
points, and they are **allowed** to share endpoints.

Return *the number of ways we can draw* `k` *non-overlapping line
segments.* Since this number can be huge, return it **modulo**
`10^9 + 7`.

```
n = 4,  k = 2   ->  5
n = 3,  k = 1   ->  3
n = 30, k = 7   ->  796297179
```

**Constraints:** `2 <= n <= 1000`; `1 <= k <= n - 1`.

## Approaches

| file | mechanism |
|---|---|
| `segments.kara` ★ | stretch each segment's end by one point, so segments that share an end no longer touch: `n` points and `k` segments become `n + k - 1` points with `2k` distinct ends. `C(n + k - 1, 2k)` by factorials and a Fermat inverse. O(n + k + log p) |
| `segments_prefix.kara` | `ways[j][i]`, the sets of `j` segments on points `0..=i`: point `i` ends no segment, or ends one that starts at some `s < i`, the sum over `s` kept as a running prefix sum per `j`. O(n k) |
| `segments_pascal.kara` | the same binomial with no inverse: Pascal's triangle by addition, only to row `n + k - 1` and column `2k`. O((n + k) k) |
| `segments_solution.kara` | LeetCode's Rust template, a three-index DP (`dp[i][j][0]` and `dp[i][j][1]`, a segment ending at `i` that may still grow), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples, the
smallest case and the two ends of the range of `k` at 1000 points, then
a checksum over all 780 pairs up to 40 points and one over 30 random
pairs up to 1000. `segments.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every choice of `k` segments, each from one point to a later
one, in order along the line and each starting no earlier than the one
before it ends, counted once. It checks 300 random pairs, every other
one of 2 to 9 points (small enough to count literally), the rest of 2 to
60. Every random choice is drawn before any arm answers. The interpreter
takes about 22 s.

| | property |
|---|---|
| P1 | the answer is the statement read literally (up to 9 points) |
| P2 | `n - 1` segments on `n` points can be placed one way |
| P3 | one segment on `n` points can be placed `n (n - 1) / 2` ways |
| P4 | one more than the sum over every `k` is the Fibonacci number `F(2n - 1)` |
| P5 | `f(n, k) - 2 f(n - 1, k) + f(n - 2, k) = f(n - 1, k - 1)`, with `f(m, 0) = 1` and `f(m, k) = 0` for `m <= k` |
| P6 | each arm agrees with at least two of the other three |

All of it mod `10^9 + 7`. The differential prints `300 problems:
checksum 975092552, 7200 checks over 4 arms: 0 failures` under every
lane in Verification. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the top `n + k`, not `n + k - 1` | P1 172, P2 300, P3 300, P4 300, P5 81, P6 300 |
| M2 | ★: the inverse raised to `MOD - 1` | P1 172, P2 300, P3 300, P4 300, P5 277, P6 300 |
| M3 | ★: the exponent halved twice a step | P1 172, P2 300, P3 300, P4 300, P5 277, P6 300 |
| M4 | prefix: `prev[i]` summed, not `prev[i - 1]` | P1 106, P2 277, P4 277, P5 230, P6 230 |
| M5 | prefix: `row[i] = starts`, the point ending no segment dropped | P1 120, P3 277, P4 277, P5 244, P6 244 |
| M6 | Pascal: each row made left to right | P1 172, P2 300, P3 300, P4 300, P5 230, P6 300 |
| M7 | Pascal: mod `1000000009` | P4 90, P5 39, P6 64 |
| M8 | template: `dp[i][j][1] = 0` before the new segment | P1 120, P3 277, P4 277, P5 244, P6 244 |
| M9 | template: `dp[i - 1][j - 1][1]` dropped | P1 106, P2 277, P4 277, P5 136, P6 230 |
| M10 | template: only `dp[n - 1][k][0]` returned | P1 172, P2 300, P3 300, P4 300, P6 300 |

M7 shows only where a count passes `10^9`, which no case of up to 9
points reaches, so P1 never sees it; P4's Fibonacci check, made with
the right modulus, does.

## Benchmarks

The bench draws 400000 random pairs of up to 1000 points, all of them
first, then each one's count by the ★ arm, the factorials made afresh
for every query as the arm does, in all five languages. Every
implementation prints `400000 random pairs: counts sum to 709423252 mod
10^9 + 7, checksum 203744238`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `457e5b4ec` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 1.405 s |
| Rust (`rustc -O`) | 1.909 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.911 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.939 s |
| Kāra (`karac build`) | 1.947 s |
| Go | 2.485 s |
| Python | 19.6 s |

Kāra is level with both Rust builds and ahead of Go. The work is a
`Vec` of up to 2000 factorials per query, each a multiply and a `%`,
bounds-checked in Kāra, Rust and Go; why C is a quarter faster was not
looked into.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (1.957 s and 2.006 s on one run).

## Verification

All four arms print the same output as `segments.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`457e5b4ec`.

## Writing it

The three arms of my own checked clean as first written. LeetCode's
Rust template takes one `karac fix` of 7 edits: `struct Solution;` to
`struct Solution {}`, both `as usize` to `as i64` (Kāra indexes with
`i64`), `vec![vec![[0i64; 2]; k + 1]; n]` to
`Vec.filled(n, Vec.filled(k + 1, [0; 2]))`, and `Solution::` to
`Solution.`. It then checks and agrees with no hand edit. No compiler gap
was met.
