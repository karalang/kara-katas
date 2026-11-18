# 1191. K-Concatenation Maximum Sum

Given an integer array `arr` and an integer `k`, modify the array by
repeating it `k` times. For example, if `arr = [1, 2]` and `k = 3` then the
modified array will be `[1, 2, 1, 2, 1, 2]`. Return the maximum sub-array
sum in the modified array. Note that the length of the sub-array can be
`0` and its sum in that case is `0`. As the answer can be very large,
return the answer modulo `10^9 + 7`.

```
arr = [1, 2],      k = 3  ->  9
arr = [1, -2, 1],  k = 5  ->  2
arr = [-1, -2],    k = 7  ->  0
```

**Constraints:** `1 <= arr.length <= 10^5`, `1 <= k <= 10^5`,
`-10^4 <= arr[i] <= 10^4`.

The arms are `fn k_concatenation_max_sum(arr: Vec[i64], k: i64) -> i64`.
The two Rust arms keep the method LeetCode gives Rust users, over
`Vec<i32>` and an `i32` answer, inside `impl Solution`, and a one-line
`k_concatenation_max_sum` converts the values and calls it.

## Approaches

A best subarray either lies within one copy, or runs from a suffix of one
copy through whole copies to a prefix of a later one; whole copies help
only when the array sums above zero, and then all `k - 2` middle copies
help. Two copies hold every shape but the middle, so no arm walks more than
two. The true maximum reaches `10^5 · 10^4 · 10^5 = 10^14`, which fits an
`i64`; each arm takes the remainder once, at the end.

| file | mechanism |
|---|---|
| `k_concatenation_max_sum.kara` ★ | Kadane's scan, the empty subarray allowed, over one copy or two; then `(k - 2) · sum` when the sum is above zero. O(n) |
| `k_concatenation_max_sum_ends.kara` | the best run within one copy against the best suffix, the middle copies' sum when it helps, and the best prefix. O(n) |
| `k_concatenation_max_sum_power.kara` | each run of copies summed up as four numbers (sum, best prefix, best suffix, best), which join associatively, and k copies joined by repeated squaring. O(n + log k) |
| `k_concatenation_max_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (one loop over `0..n * reps` reading `arr[i % n]`, in `i64` against `i32` values), carried to Kāra by `karac fix` |
| `k_concatenation_max_sum_chain.kara` | another Rust solution, in iterator chains (`arr.iter().cycle().take(arr.len() * times).scan(0i64, \|cur, &x\| ..).max()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six more properties |

Every arm prints the same 11 lines: LeetCode's three examples; one value
(`[5] k=1: 5`); a sum of zero around a peak (`[-5, 10, -5] k=3: 10`); a
small array repeated LeetCode's most times (`[2, -1, 2] k=100000:
300000`); every value negative but one (`[-3, -3, 4, -3] k=4: 4`); the
largest answer, `10^14` before the remainder (`[10000; 100000] k=100000:
999300007`); 2000 random arrays of 1 to 8 values repeated 1 to 6 times
(`2000 random arrays: checksum 385010717`); and the constraints' longest,
10^5 values repeated 10^5 times, at random (`100000 random values
k=100000: 246754544`) and lifted to sum well above zero (`100000 lifted
values k=100000: 417184575`). `k_concatenation_max_sum.py` mirrors the ★
arm and its output is byte-identical; it also checks every answer whose
copies hold at most 60 values against the statement read literally. Every
arm gives the same output under `karac run` and `karac build`, and under
the AddressSanitizer build.

The Mend loop: the ★, ends and power arms check clean as written. The
solution arm takes one round of 15 fixes (among them `Vec<i32>` to
`Vec[i32]`, the `&` of `|&x|`, `&&` to `and`, the suffixes of `0i64`, and
the `as i64` of `arr[i % n] as i64`, which widens implicitly) and its
output matches. The chain arm takes one round of 15 (among them
`k.min(2) as usize` to `as i64`, and Rust's `scan` closure, `|cur, &x| {
*cur = (*cur + x as i64).max(0); Some(*cur) }`, to Kāra's, which returns
the next state with the item, `|cur, x| { let cur = (cur + x as
i64).max(0); Some((cur, cur)) }`) and its output matches. No gap was
found.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray of the `k` copies laid end to end, the empty one
included. 2000 random arrays of 1 to 8 values, each repeated 1 to 6 times;
the first 200 from `-3..=3`, the rest from `-10..=10`.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at least zero, and at least the largest value |
| P3 | one more copy never lowers it |
| P4 | the array reversed gives the same answer |
| P5 | past two copies, one more adds the sum when it is above zero |
| P6 | past two copies, one more changes nothing when the sum is not above zero |
| P7 | the ★ arm's answer |

All 70,000 checks pass on every arm: `2000 arrays: checksum 426808278,
70000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All ten
are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: one copy scanned, whatever `k` is | P1 817, P7 3268 |
| S2 | ★: `k - 1` middle copies added | P1 596, P5 165, P7 2384 |
| E1 | ends: the middle copies added when their sum is below zero | P1 41, P3 10, P6 10, P7 41 |
| E2 | ends: a run across copies tried when `k` is 1 | P1 21, P7 21 |
| W1 | power: no run across a join | P1 1203, P5 761, P7 1203 |
| W2 | power: a prefix that skips the left part's sum | P1 1017, P4 972, P5 484, P7 1017 |
| X1 | solution: three copies scanned | P1 761, P7 761 |
| X2 | solution: the run never restarts | P1 992, P2 622, P4 1217, P7 992 |
| C1 | chain: the middle copies added when their sum is below zero | P1 665, P2 631, P3 805, P6 805, P7 665 |
| C2 | chain: three copies scanned | P1 596, P5 165, P7 596 |

A mutation of the ★ arm fails P7 on every arm. S2 and C2 are one fault in
two arms, a middle copy counted twice, and fail alike. E1 and C1 are one
fault too, but E1 is the weakest catch, 41 failures: when the sum is
below zero the best run across copies joins two neighbours and skips the
rest, and the mutation charges it every middle copy, which shows only when
that crossing run would have beaten every run within one copy.
P4, the reversal, catches the faults that break the symmetry between a
prefix and a suffix (W2) or between a run's start and its end (X2).

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 4 arrays of 10^5 values, LeetCode's longest, built once (random
from -10^4 to 10^4, the same lifted to sum above zero, every value
negative, and values alternating in sign); then 200 rounds over the
arrays, round `r` repeating each `10^5 - r` times, each answer folded
into a checksum. Every program prints `200 rounds of 4 arrays of 100000
values: checksum 417635714`. Each call sums the array, scans it once or
twice, and allocates nothing.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `e8dc4f7aa2`
plus the typechecker fix pushed as `ab7613763c`, on LLVM 22. A plain
`karac build` targets x86-64-v2, so the C and overflow-checked Rust
programs are also built at x86-64-v3 for comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.188 to 0.245 s | 0.206 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.197 to 0.228 s | 0.209 s |
| Rust (`rustc -O`) | 0.129 to 0.192 s | 0.138 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.177 to 0.223 s | 0.194 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.207 to 0.262 s | 0.231 s |
| C (`clang -O3`) | 0.121 to 0.148 s | 0.135 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.185 to 0.225 s | 0.206 s |
| Go | 0.242 to 0.270 s | 0.255 s |
| Python | 9.620 to 9.718 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Plain Rust and C are about a third faster than Kāra (0.138 s and
0.135 s against 0.209 s), and Rust with overflow checks on, Kāra's
equal-safety twin, is about 7% ahead. The x86-64-v3 builds of C and Rust
are slower than their plain builds here (C 0.206 s against 0.135 s) and
land level with Kāra; no profile was taken, so why the wider ISA loses
on this scan is not known. Kāra is about 20% ahead of Go. Python takes
about 46x Kāra's time.
