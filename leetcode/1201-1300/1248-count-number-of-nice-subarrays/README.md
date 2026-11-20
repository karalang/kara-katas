# 1248. Count Number of Nice Subarrays

Given an array of integers `nums` and an integer `k`, a continuous
subarray is called **nice** if there are `k` odd numbers in it.

Return *the number of nice subarrays*.

```
nums = [1, 1, 2, 1, 1], k = 3                    ->  2    ([1, 1, 2, 1] and [1, 2, 1, 1])
nums = [2, 4, 6], k = 1                          ->  0
nums = [2, 2, 2, 1, 2, 2, 1, 2, 2, 2], k = 2     ->  16
```

**Constraints:** `1 <= nums.length <= 50000`; `1 <= nums[i] <= 10^5`;
`1 <= k <= nums.length`.

The arms are `fn number_of_subarrays(nums: Vec[i64], k: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `number_of_subarrays.kara` ★ | prefix counts: walking the array with the number of odd values so far, each step adds how many earlier prefixes had `k` fewer, kept in a `Vec` indexed by count |
| `number_of_subarrays_window.kara` | sliding windows: the subarrays with at most `k` odd values, counted by a window whose left end moves only as far as it must, less those with at most `k - 1` |
| `number_of_subarrays_gaps.kara` | by the odd values' places, fenced with `-1` and `n`: each run of `k` consecutive odd values adds the product of the gaps before and after it |
| `number_of_subarrays_map.kara` | the prefix counts in a `Map`, the array read with an iterator `fold` whose closure updates the map it captures |
| `number_of_subarrays_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![0; n + 1]`, `for &x in nums.iter()`, `(x & 1) as usize`, `k as usize`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, four more properties |

Every arm prints the same 3 lines: LeetCode's three examples; the total
of the answers and a checksum of them for 1000 random arrays of 1 to
2000 values from 1 to 10^5, each array with its own chance of an odd
value and a `k` from 1 to two past its number of odd values (`total
2090316, checksum 134084062`); and three arrays of 50000 values, the
constraints' top: all odd with `k = 1` and `k = 25000`, and one odd value
in the middle of even ones, 625,025,000 nice subarrays.
`number_of_subarrays.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, window and gaps arms checked clean as first
written. The map arm was first written `let more =
seen.get(odd - k).unwrap_or(0);` before `*seen.entry(odd).or_insert(0)
+= 1;`. `get` returns an `Option[ref i64]`, so `more` is a `ref i64`
into the map while the `entry` call writes it, and E0516 is right;
`karac fix` reads the value out, `let more = *seen.get(..)..`. Inside
the `fold`'s closure, though, the error names neither the map nor
`more`: "mutable borrow of (*a temporary value) while it is borrowed",
where the same lines in a plain `for` loop say "cannot mutably borrow
`seen` while `more` still holds a borrow of it" (B-2026-11-19-137,
below). The solution arm takes one round of fixes, 8 by `karac fix`'s
count, and then checks clean: `struct Solution;` to `struct Solution
{}`, `Vec<i32>` to `Vec[i32]`, `vec![0; n + 1]` to `Vec.filled(n + 1,
0)`, `let (mut odd, mut ans)` to `let mut (odd, ans)`, and `for &x` to
`for x`. Its `usize` casts carry over as written.

## Gaps

One, in the wording of a diagnostic, filed by the review thread:

1. **B-2026-11-19-137:** an E0516 inside a closure names a captured
   variable as "(*a temporary value)" and names no holder. The closure
   body reads its captures through its environment, and the borrow
   checker has no names for the environment's fields. The machine fix is
   the same as outside a closure, so the Mend loop still ends clean.

## Differential

`differential.kara` holds copies of the five arms, renamed, and the
statement read literally: every subarray, its odd values counted one by
one. 2000 random arrays of 1 to 30 values from 1 to 100, each with its
own chance of an odd value, `k` from 1 to two past the number of odd
values.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | each value swapped for another of the same parity gives the same answer |
| P4 | the answers for every `k` from 1 to the number of odd values add up to every subarray that holds an odd value: all `n (n + 1) / 2` of them, less `r (r + 1) / 2` for each run of `r` even values |
| P5 | none for a `k` past the number of odd values, and at least one for a `k` up to it |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 242372714,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the
same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a subarray starting at the array's start, with exactly `k`, missed | P1 1290, P2 641, P4 1773, P5 272, P6 5160 |
| S2 | ★: the empty prefix not counted | P1 1290, P2 615, P4 1773, P5 145, P6 5160 |
| W1 | window: the left end moved one place at most per step | P1 862, P2 924, P4 1511, P6 862 |
| W2 | window: every value leaving the window counted as odd | P1 904, P2 867, P4 1511, P6 904 |
| G1 | gaps: the last run of `k` odd values left out | P1 1290, P2 641, P4 1773, P5 272, P6 1290 |
| G2 | gaps: one end fewer after each run | P1 1290, P2 867, P4 1773, P5 356, P6 1290 |
| M1 | map: the empty prefix counted twice | P1 1290, P2 615, P4 1773, P6 1290 |
| M2 | map: the count replaced at each step, not added to | P1 1171, P2 615, P4 1712, P6 1171 |
| L1 | solution: each prefix count set to 1, not raised | P1 904, P2 867, P4 1511, P6 904 |
| L2 | solution: a prefix with exactly `k` odd values never used | P1 1290, P2 641, P4 1773, P5 272, P6 1290 |

All ten are caught, every one by P1, the statement read literally, P4,
every `k` added up, and P6, which fails on the other four arms too when
the ★ arm is the one mutated (S1, S2). P2, the array reversed, catches
all ten too, and P5 five (S1, S2, G1, G2, L2). P3, each value swapped for another of its parity, catches
none: every arm looks only at the parity. A first W1, the window's
count `right - left` instead of `right - left + 1`, survived and is
equivalent: both windows lose one subarray per step, `n` in all, and the
difference of the two counts is unchanged.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (prefix counts of odd values in a `Vec` indexed by count) on 50
random arrays of 50000 values built once, each with its own chance of an
odd value, each asked with 10 random k; every answer folded into a
checksum. Every program prints `50 arrays of 50000 values, 100 k each:
checksum 379691760`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.456 to 0.544 s | 0.471 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.445 to 0.520 s | 0.466 s |
| Rust (`rustc -O`) | 0.396 to 0.494 s | 0.422 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.463 to 0.535 s | 0.502 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.464 to 0.603 s | 0.502 s |
| C (`clang -O3`) | 0.359 to 0.446 s | 0.387 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.335 to 0.465 s | 0.357 s |
| Go | 0.567 to 0.695 s | 0.615 s |
| Python | 24.75 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 7% ahead of Rust with overflow checks on (0.466 s
against 0.502 s), and the two ranges overlap. C is about 17% ahead of
Kāra (0.387 s against 0.466 s); Kāra is about 24% ahead of Go (0.466 s
against 0.615 s). Python takes about 53x Kāra's time. No profile was
taken.
