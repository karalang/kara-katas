# 1712. Ways to Split Array Into Three Subarrays

A split of an integer array is **good** if:

- The array is split into three **non-empty** contiguous subarrays -
  named `left`, `mid`, `right` respectively from left to right.
- The sum of the elements in `left` is less than or equal to the sum of
  the elements in `mid`, and the sum of the elements in `mid` is less
  than or equal to the sum of the elements in `right`.

Given `nums`, an array of **non-negative** integers, return *the number
of **good** ways to split* `nums`. As the number may be too large,
return it **modulo** `10^9 + 7`.

```
nums = [1,1,1]           ->  1
nums = [1,2,2,2,5,0]     ->  3
nums = [3,2,1]           ->  0
```

**Constraints:** `3 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `split.kara` ★ | prefix sums, which never fall: with the left part ending at i and the middle at j, the left is at most the middle when `prefix[j] >= 2 prefix[i]`, and the middle at most the right when `2 prefix[j] <= total + prefix[i]`, so the good j are one run, its ends found by two `partition_point` searches. O(n log n) |
| `split_pointers.kara` | as the left part grows both ends of that run only move right: two pointers walk them across the array once, stopping once the left holds more than a third of the total. O(n) |
| `split_mid.kara` | the cuts counted from the end of the middle instead: the left part may end at any i whose sum is at most half of `prefix[j]` and at least `2 prefix[j] - total`, and both bounds rise with j, so two pointers over i. O(n) |
| `split_solution.kara` | a Rust solution as LeetCode's Rust users write it, `vec![0; n + 1]` prefix sums, `partition_point(\|&x\| x < 2 * prefix[i])` clamped with `.max(i + 1)` and `.min(n)`, and `(hi - lo) as i64`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, five
zeros, and `10^5` values of `10^4`, the largest, whose count passes the
modulus; then the answers summed and a checksum for 3000 random arrays
of up to 12 values up to 4, 300 of up to 1000 up to `10^4`, and 10 of up
to `10^5` up to 3. `split.py` mirrors the ★ arm with `bisect` and its
output is byte-identical.

```
1
3
0
6
833333333
3000 arrays of up to 12 values up to 4: answers sum to 13361, checksum 41868955
300 arrays of up to 1000 values up to 10000: answers sum to 8841861, checksum 39489072
10 arrays of up to 100000 values up to 3: answers sum to 353108443, checksum 758676264
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every cut into three non-empty runs, each run summed afresh,
the good ones counted. It checks 3000 random arrays of 3 to 10 values,
each from 0 to a random bound from 0 to 5, so runs of zeros are common.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every value doubled gives the same answer |
| P3 | a value above the total put at the end makes good every cut whose left part is at most its middle |
| P4 | a value above the total put in front leaves no good cut |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 615987316, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, `sum` of each slice, gives the same checksum.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first drafts of the pointers
mutants were equivalent and were replaced: the early stop loosened to
half the total, since past a third every run of good ends is empty
anyway; and the upper pointer restarted from the left part's end rather
than the lower pointer, since a middle smaller than a left of at most a
third always leaves the right larger, so the pointer passes those ends
by itself. M1 and M7 make the same mistake from the two sides, a middle
equal to the left refused, and fail the very same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a middle equal to the left refused | P1 1782, P3 2318, P5 1782 |
| M2 | ★: the right part let be empty | P1 510, P5 510 |
| M3 | ★: the middle let be empty | P1 1208, P3 1208, P5 1208 |
| M4 | pointers: the middle let be empty | P1 1208, P3 1208, P5 1208 |
| M5 | pointers: the lower pointer stopped one short of the end | P1 38, P3 1844, P5 38 |
| M6 | pointers: a right equal to the middle refused | P1 1503, P5 1503 |
| M7 | mid: a left equal to the middle refused | P1 1782, P3 2318, P5 1782 |
| M8 | mid: the middle never ends at the second last value | P1 809, P3 2927, P5 809 |
| M9 | solution: a right equal to the middle refused, after rounding down | P1 2022, P2 831, P3 1208, P5 2022 |
| M10 | solution: stops once the left is a third of the total | P1 791, P5 791 |

## Benchmarks

The bench draws 20 random arrays of `10^5` values up to `10^4`,
LeetCode's largest, all of them first, then answers each 10 times by the
★ arm in all five languages. Every implementation prints `20 arrays of
100000 values, 10 rounds: answers sum to 166344245830, checksum
88543676`. Rust uses `partition_point`, Go `sort.Search`, Python
`bisect`, and C two hand-written binary searches. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.734 s |
| Kāra (`karac build`) | 0.745 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.763 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.792 s |
| Go | 1.133 s |
| C (`clang -O3`) | 1.393 s |
| Python | 7.4 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.762 s and 0.767 s on one
run).

## Verification

All four arms print the same output as `split.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, pointers and mid arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 7 edits:
`struct Solution {}` added, `Vec<i32>` written `Vec[i32]`,
`vec![0; n + 1]` written `Vec.filled(n + 1, 0)`, the two `|&x|` written
`|x|`, and the cast in `(hi - lo) as i64` dropped, the difference
widening by itself. The fix first left that difference in its
parentheses, `ans += (hi - lo);`; since kara `93fd9b2078` (B-2026-11-20-42) it
drops them with the cast. The `const MOD`, `partition_point`, and
`.max(i + 1)` and `.min(n)` on its result carried over as written. The
prefix sums, `Vec.filled(n + 1, 0)` filled from `i32` values, are
`i64`, the literal's default, where Rust infers `i32`.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
