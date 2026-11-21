# 1714. Sum Of Special Evenly-Spaced Elements In Array

You are given a **0-indexed** integer array `nums` consisting of `n`
non-negative integers.

You are also given an array `queries`, where `queries[i] = [xi, yi]`.
The answer to the `ith` query is the sum of all `nums[j]` where
`xi <= j < n` and `(j - xi)` is divisible by `yi`.

Return *an array* `answer` *where* `answer.length == queries.length`
*and* `answer[i]` *is the answer to the* `ith` *query **modulo**
`10^9 + 7`.

```
nums = [0,1,2,3,4,5,6,7], queries = [[0,3],[5,1],[4,2]]          ->  [9,18,10]
nums = [100,200,101,201,102,202,103,203], queries = [[0,7]]      ->  [303]
```

**Constraints:** `n == nums.length`; `1 <= n <= 5 * 10^4`;
`0 <= nums[i] <= 10^9`; `1 <= queries.length <= 1.5 * 10^5`;
`0 <= xi < n`; `1 <= yi <= 5 * 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `special.kara` ★ | a step above the square root of n reaches at most that many values, so it is walked; a smaller one may be asked often, so `sums[j] = nums[j] + sums[j + y]` is filled once from the back and each query of it reads one entry. The queries are taken in order of their step, so one array serves each small step in turn. O((n + q) sqrt(n)) |
| `special_direct.kara` | every query walked from x, y apart. O(n q) at worst |
| `special_step.kara` | the same walk as an iterator, `nums[x..].iter().step_by(y)` summed as `i64`. O(n q) at worst |
| `special_memo.kara` | online, in the order given: the first query of a small step fills that step's sums into a `Map` keyed by the step, and every later one reads an entry; a large step is walked. O((n + q) sqrt(n)) |
| `differential.kara` | the four arms against the statement read literally, five properties |

LeetCode offers no Rust template for this problem, so there is no
Rust-template arm. The ★ and memo arms take the root with `n.isqrt()`.

Every arm prints the same 8 lines: LeetCode's two examples, one value
with a step past the end, a step past the end from the middle, and
`5 * 10^4` values of `10^9`, whose sums pass the modulus; then the
answers summed and a checksum for 3000 random problems of up to 12
values and 6 queries, 300 of up to 1000 values and 300 queries, and 10
of up to `5 * 10^4` values and 1000 queries. `special.py` mirrors the ★
arm with `math.isqrt` and its output is byte-identical.

```
[9, 18, 10]
[303]
[5, 5]
[2, 3]
[999650007, 999825007, 1000000000]
3000 problems of up to 12 values and 6 queries: answers sum to 89004, checksum 336317862
300 problems of up to 1000 values and 300 queries: answers sum to 22366090318403, checksum 59913571
10 problems of up to 50000 values and 1000 queries: answers sum to 2242329422722, checksum 541677063
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each query, every j from x to the end, added when `j - x`
divides by y. It checks 3000 random problems of 1 to 12 values, half of
them up to 9 and half up to `10^9`, and 1 to 6 queries of a start in the
array and a step from 1 to one past its length. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | every value doubled doubles every answer, modulo `10^9 + 7` |
| P3 | a query whose step passes the end answers its start's value |
| P4 | a query's answer is its start's value plus the answer of the query a step later, when that starts inside the array |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 737986389, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, `sum(nums[x::y])` for each query, gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first drafts were replaced: the ★
arm's small steps ending below the root rather than at it was
equivalent, since a step equal to the root walked reaches the same
values; and the memo arm filling a step only while the map was empty
panicked on the next step's missing key rather than answering wrong.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the sums filled only for the first small step | P1 308, P3 68, P4 256, P5 308 |
| M2 | ★: the last value never carried a step back | P1 1116, P4 435, P5 1116 |
| M3 | ★: a small step's answer read at `x % y` | P1 1388, P3 622, P4 1351, P5 1388 |
| M4 | direct: the walk starting a step after x | P1 2952, P3 2690, P4 1905, P5 2952 |
| M5 | direct: the answer reduced modulo `10^9 + 9` | P1 691, P2 732, P4 542, P5 691 |
| M6 | step: every step one longer | P1 1907, P4 1907, P5 1907 |
| M7 | step: the first value skipped | P1 2961, P3 2688, P4 1892, P5 2961 |
| M8 | memo: a start's own value left out of its sum | P1 1394, P4 1351, P5 1394 |
| M9 | memo: the answer read at the start rounded down to the step | P1 578, P3 208, P4 396, P5 578 |
| M10 | memo: the sums filled from the front | P1 1401, P4 1368, P5 1401 |

## Benchmarks

The bench draws 5 random problems of `5 * 10^4` values below `10^9` and
`1.5 * 10^5` queries, LeetCode's largest, each step half the time from 1
to 223, the root, and half from 1 to n, all of them first, then answers
each 4 times by the ★ arm in all five languages. Every implementation
prints `5 problems of 50000 values and 150000 queries, 4 rounds: answers
sum to 1474315268840044, checksum 339155862`. The C mirror takes the
root with `sqrt` and corrects it. The C build also runs clean under
gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.641 s |
| C (`clang -O3`) | 0.656 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.659 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.917 s |
| Kāra (`karac build`) | 0.926 s |
| Go | 1.563 s |
| Python | 27 s |

The sequential Kāra build takes 1.43x Rust's time and 1.39x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.048 s and 1.076 s on one
run).

## Verification

All four arms print the same output as `special.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The direct and step arms checked clean as first written. The ★ and memo
arms took the root as Rust 1.84 does, `n.isqrt()`, which Kāra's integers
did not have: `karac check` said there was no method `isqrt` on `i64`.
Since kara `93fd9b2078` `isqrt` exists on the integers up to 64 bits, the floor of the
square root, panicking on a negative value as Rust's does (B-2026-11-20-44),
and both arms check clean as written.

The differential's P2 and P4 first cast an `i32` answer `as i64` to
compare it with an `i64`; the `lossless_cast` lint saw that it widens by
itself, and `karac fix` dropped both casts. `arm_name` indexes a list of string literals for a
`Str`, as #1662's differential does (B-2026-11-19-131).
