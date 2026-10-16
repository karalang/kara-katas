# 643. Maximum Average Subarray I

Given an array `nums` of `n` integers and a width `k`, find the
contiguous subarray of exactly `k` values with the largest average, and
return that average. Answers within 10^-5 are accepted.

```
nums = [1,12,-5,-6,50,3], k = 4  ->  12.75000    (12 - 5 - 6 + 50) / 4
nums = [5], k = 1                ->  5.00000
```

**Constraints:** `k` from 1 to `n`, `n` up to 100,000; every value from
-10,000 to 10,000.

## Approaches

Every arm is `fn find_max_average(nums: Vec[i64], k: i64) -> f64`. All
windows have the same width, so the largest average belongs to the
largest sum: each arm finds the largest window sum as an integer and
divides it by `k` once, so the four return the same `f64` bit for bit.

| file | mechanism |
|---|---|
| `max_average.kara` ★ | a sliding sum: the first window added up once, then each step adding the value taken in and taking off the one left behind; O(n) time, O(1) space |
| `max_average_prefix.kara` | prefix sums, each window's sum the difference of two of them; O(n) time and space |
| `max_average_queue.kara` | the window's values held in a `VecDeque` with their sum, the oldest leaving once there are more than `k`; O(n) time, O(k) space |
| `max_average_zipped.kara` | the slide as a zip: `nums.iter().zip(nums[k..].iter())` pairs each value leaving with the one arriving, the first window summed with `sum()`; O(n) time, O(1) space |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: the two LeetCode examples; seven
more (every value negative; the whole array; a width of one; the best
window at the start and at the end; an average that is not a whole
number; and the extremes of the values), each with its answer to five
places; the sum of the answers to 300 random arrays of 1 to 30 values
from -20 to 20, with how many are whole numbers; and the problem's
largest, 100,000 values from -10,000 to 10,000, at widths
1, 1,000, 50,000 and 100,000. `max_average.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every window summed from scratch, and the largest sum divided by `k`.
Each of 1,000 cases has 1 to 25 values from -15 to 15 and a width from
1 to `n`.

| | property |
|---|---|
| P1 | the answer is the definition's, exactly |
| P2 | some window's average is exactly the answer |
| P3 | no window's average is larger |
| P4 | the values in reverse give the same answer |
| P5 | every value doubled doubles the answer, exactly |

It prints `1000 cases (12707 values), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the smallest sum kept | P1 863, P3 863 |
| M2 | ★: the value one place in from the one left behind taken off | P1 696, P2 498, P3 406, P4 818 |
| M3 | prefix: the last window not read | P1 193, P3 193, P4 412 |
| M4 | prefix: each window read one value short at its start | P1 647, P2 530, P3 393, P4 577 |
| M5 | queue: the newest value taken out, not the oldest | P1 631, P3 631, P4 849 |
| M6 | queue: a window not yet full counted | P1 354, P2 354, P4 464 |
| M7 | zipped: each arriving value paired one place early | P1 704, P2 518, P3 354, P4 870 |
| M8 | zipped: the smallest sum kept | P1 863, P3 863 |
| E1 | ★: a later window kept when it ties | 0 |
| E2 | prefix: the first window read again | 0 |
| E3 | queue: values taken out while the window is too long | 0 |
| E4 | zipped: the arriving values found by `skip(k)` | 0 |

P1 kills all eight. P3 sees every mutant that can return less than the
best, which is all but M6: a window not yet full is shorter than `k` but
still divided by `k`, so its average can only be wrong, never missing.
P2 sees the mutants that return a sum no window has, M2, M4, M6 and
M7, while the others return some window's sum, only the wrong one.
P4 sees every mutant that treats the two ends differently; M1 and M8 do
not, since the smallest window is the smallest either way. P5 sees none:
every mutant still adds and takes off values, so doubling them doubles
whatever it gets wrong. The four survivors cannot change an answer: a
tie keeps the same sum; the first window is already the starting best;
the window never holds more than one value too many; and `skip(k)` and
`nums[k..]` give the same values.

## Verification

Every arm prints the same output as `max_average.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `d6111aa22a` for the
debug build, with the runtime archives rebuilt from that tree, and
`51eb3cb129` for the release build that runs `check` and `__mir-run`,
except `check` on the zipped arm and the differential: it refused them
at first with two errors each, typing the items of
`nums.iter().zip(nums[k..].iter())` by value, so `*arriving - *out` was
rejected, though design.md writes the same shape in its own `Vec`
equality (B-2026-10-15-1). The zipped arm was kept as written, and
`check` passes it since kara `078a101ad6` (checked at `f75dd289bc`,
with the same output on `__mir-run`).

The frozen legacy backends refuse every arm and the differential at type
checking. The prefix, queue and zipped arms read `*x` from
`nums.iter()`, and legacy types those items by value; the ★ arm's
harness hands `seed`, already a `mut ref` parameter, on to
`next_random(mut seed)` with the `mut` marker design.md asks for, and
legacy rejects that marker. Legacy is frozen, so these are noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 arrays of 100,000 values
from -10,000 to 10,000 once; then 4,000 rounds each find the best
average of one array, picked by the round, at a width from 1 to
100,000 also picked by the round, adding up the answers. Every
implementation prints `4000 rounds over 20 arrays of 100000 values:
answers adding to -5360467.19558`, the Kāra program under `karac
__mir-run` included (in 79 s).

Each implementation is the same sliding sum over a fixed array: Rust
over a `&[i64]`, C over an `int64_t` array, Go over a slice and Python
over a list. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine), each
including making the arrays:

| | time |
|---|---|
| C (`clang -O3`) | 0.23 to 0.24 s |
| Rust (`rustc -O`) | 0.24 to 0.26 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.32 to 0.35 s |
| Go | 0.31 to 0.36 s |
| Python | 20.7 to 20.8 s |
| Kāra (`karac build --mir`) | 0.36 to 0.37 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: handing `arrays[r % 20]` to `find_max_average` moves an element
out of a `Vec` while parameters are owned. That edit is by hand, on top
of the `scripts/new-bench.sh` output. A copy outside the kata that makes
the parameter `ref Vec[i64]` builds under legacy and takes 0.34 to
0.39 s. Under `karac __mir-llvm-run` the program prints the same line in
2.5 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So the v2 build is level with legacy, and sits just past Rust and Go
with their overflow checks on. The loop's every step is an add, a
subtract and a compare, each add checked for overflow in the Kāra; the
comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-15-1 (found by this kata, fixed in kara `078a101ad6`):
`karac check` typed the items of a `zip` (and a `chain`) by value, so
`*x` on them was rejected; both v2 backends accepted and ran the zipped
arm. The legacy refusals above are not filed because legacy is
frozen.
