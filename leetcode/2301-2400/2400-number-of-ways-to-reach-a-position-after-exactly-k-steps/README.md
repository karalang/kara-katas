# 2400. Number of Ways to Reach a Position After Exactly k Steps

You are given two **positive** integers `startPos` and `endPos`.
Initially, you are standing at position `startPos` on an **infinite**
number line. With one step, you can move either one position to the
left, or one position to the right.

Given a positive integer `k`, return *the number of **different** ways
to reach the position* `endPos` *starting from* `startPos`*, such that
you perform **exactly*** `k` *steps*. Since the answer may be very
large, return it **modulo** `10^9 + 7`.

Two ways are considered different if the order of the steps made is
not exactly the same.

**Note** that the number line includes negative integers.

```
startPos = 1, endPos = 2, k = 3   ->  3
startPos = 2, endPos = 5, k = 10  ->  0
```

**Constraints:** `1 <= startPos, endPos, k <= 1000`.

With `d = |endPos - startPos|`, a way takes `(k + d) / 2` steps toward
the end and the rest away, so the answer is `C(k, (k + d) / 2)` when
`k - d` is even and not negative, and 0 otherwise.

## Approaches

| file | mechanism |
|---|---|
| `ways.kara` ★ | counting: the binomial from factorials modulo `10^9 + 7`, each divided out by Fermat's inverse, a power by squaring. O(k + log p) |
| `ways_dp.kara` | step by step: the ways to stand at each offset from the start, `-k` to `k`, each step's row from the last; nothing is clipped to 1 to 1000, since the line has no ends. O(k^2) |
| `ways_pascal.kara` | Pascal's triangle: row `k` built from the rows above by adding neighbours, the binomial read from it. O(k^2) |
| `ways_memo.kara` | memoized recursion on the distance left and the steps left, the ways one step nearer plus one step farther, in a `Vec[Vec[i64]]` passed `mut ref`. O(k^2) |
| `ways_iter.kara` | iterators: the row of ways over offsets folded through `k` steps by `fold`, each new row by `map` over its indexes and `collect`. O(k^2) |
| `ways_solution.kara` | LeetCode's Rust template: Pascal's triangle in a `vec![vec![0i64; k + 1]; k + 1]`, indexed by `usize`, the modulus a `const` inside the method; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; the start
itself in an odd and an even count, the far end exactly `k` away, and
with one step too few; two walks that pass left of 1; `k = 1000` from 500
to five ends; then 400 random cases of `k` up to 120, each end within
`k` of its start, with a checksum and the count of zeros. `ways.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked against walking out every way: every start, end and `k` up to
15, and 300 random cases of `k` up to 300.

`check` first reports 2 errors on the template, and `karac fix` carries
it in one call, reporting 8 edits: `struct Solution;` given its braces;
`||` written `or`; `vec![vec![0i64; k + 1]; k + 1]` written
`Vec.filled(k + 1, Vec.filled(k + 1, 0))`; `usize` made `i64`; and the
harness's widening `as i64` on the template's `i32` answer removed. `const
MOD: i64 = 1_000_000_007;` inside the method, `0..=k`, `1..=i` and
`as i32` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every one of the `2^k` ways to choose left or right at each
step walked out, and those that end at `endPos` counted. It checks 360
cases: a third with `k` up to 12, which the literal reading answers; a
third with `k` from 13 to 120 and an end it can reach; and a third with
`k` from 13 to 120 and an end drawn up to 3 past what it can reach, of
either parity. Every end is kept to 1 to 1000. All 360 are drawn before
any arm answers.

| | property |
|---|---|
| P1 | `k` up to 12: the answer is the literal reading's |
| P2 | start and end swapped: the same answer |
| P3 | start and end both moved 7 along: the same answer |
| P4 | `k` from 2: the ways with `k - 1` steps to the end's two neighbours sum to the answer |
| P5 | `k` up to 40: the answers over every end from `start - k` to `start + k` sum to `2^k` |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a way reversed walks from the end to the start, P3
because the line looks the same from every point, P4 because every way
reaches the end from one of its neighbours, and P5 because each of the
`2^k` ways ends somewhere in that range. P4 and P5 ask about ends
outside 1 to 1000, which the line allows and every arm answers.

The differential prints `360 cases: checksum 381398897, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts the steps right in every choice. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the power taken at even bits | P1 69, P4 246, P5 171, P6 246 |
| M3 | ★: the wrong parity not refused | P1 39, P4 25, P5 186, P6 100 |
| M4 | ★: the inverse one power short | P1 69, P4 240, P5 171, P6 246 |
| M8 | dp: an end exactly k away refused | P1 40, P4 27, P5 186, P6 46 |
| M9 | dp: a step left overwriting | P1 41, P4 212, P5 171, P6 212 |
| M10 | dp: no step right from the second-last offset | P1 14, P2 46, P4 16, P5 186, P6 17 |
| M12 | pascal: each entry its left parent doubled | P1 41, P4 212, P5 162, P6 212 |
| M13 | pascal: each row's second entry left 1 | P1 41, P4 6, P5 171, P6 212 |
| M14 | pascal: the parity read modulo 4 | P1 26, P4 212, P5 171, P6 116 |
| M17 | memo: a gap one past the steps left still walked | P1 39, P5 186, P6 101 |
| M18 | memo: each remembered count one more | P1 60, P4 287, P5 171, P6 287 |
| M19 | memo: both steps taken nearer | P1 81, P4 34, P5 186, P6 258 |
| M22 | iter: only steps from the left | P1 67, P2 46, P4 16, P5 186, P6 241 |
| M24 | iter: a stay taken for a step from the right | P1 85, P2 346, P4 167, P6 288 |
| M26 | iter: no step left to below position 1 | P3 8, P6 8 |
| M28 | solution: the sums modulo one less | P4 57, P5 19, P6 107 |
| M29 | solution: the binomial read at d | P1 36, P4 210, P5 95, P6 205 |

P6 kills all seventeen, P1, P4 and P5 fifteen each, P2 three and P3
one. P3, start and end moved 7 along, fails only the iter arm's no step
left to below position 1 (M26), the one edit that reads where the walk
is rather than how far it has to go, as if the line ended at 1. P2,
start and end swapped, fails the three edits that treat a step left and
a step right unalike (M10, M22, M24). P1 misses M26, whose walks rarely
pass below 1 when `k` is at most 12, and the template's sums modulo one
less (M28), which only matters once a count passes `10^9 + 6`, far
beyond `k = 12`; P4 and P5 catch M28 on the larger `k`.

Of the thirty-one, fourteen were not kept. The ★ arm's every power from
0, the dp arm's start counted twice, the pascal arm's each row's ends 0,
the memo arm's arriving counted twice and the template's each row's
first entry 2 (M6, M7, M16, M21, M27) all fail alike; the dp and iter
arms' one step too few (M11, M23) alike; the ★ arm's each factorial one
factor up (M2) as the dp arm's step left overwriting (M9); and the ★
arm's exponent divided by three (M5) as its power taken at even bits
(M1). The pascal arm's binomial one place left (M15), the memo arm's gap
one wider (M20), the iter arm's start one offset right (M25), and the
template's each row's last entry left 0 and modulus `10^9 + 9` (M30,
M31) each fail apart from every kept one, and were left out to keep
three to an arm and two to the template. The iter arm's M26 was first
no step left into the last offset, which no case killed: the last offset
is reached only on the last step, so reading it never mattered. It was
replaced by no step left to below position 1 (M26).

## Verification

Every arm prints the same output as `ways.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.18 to 5.3 s, except the iter
arm at 13.6 s. The differential takes 32 s there, 7.5 s under `karac
__mir-llvm-asan` and 1.0 s under `karac __mir-llvm-run`.

## Benchmarks

The bench answers 300000 queries from the harness's generator, `k` up
to 1000, each end within `k` of its start at `k`'s parity and kept to 1
to 1000, folding every answer into the checksum, with the ★ arm in all
five languages. Every implementation prints `300000 queries of k up to
1000: checksum 208734606, 37364 zeros`. Every implementation allocates
a fresh table of factorials for each query.

BENCHTAB
