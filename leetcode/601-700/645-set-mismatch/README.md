# 645. Set Mismatch

An array `nums` of `n` values should hold every number from 1 to `n`
once, but one of them was overwritten with a copy of another. Return the
copy and the number it replaced, in that order.

```
nums = [1,2,2,4]  ->  [2,3]
nums = [1,1]      ->  [1,2]
```

**Constraints:** `n` from 2 to 10,000; every value from 1 to `n`.

## Approaches

Every arm is `fn find_error_nums(nums: Vec[i64]) -> Vec[i64]`, returning
the copy and then the missing value.

| file | mechanism |
|---|---|
| `set_mismatch.kara` ★ | one pass counts how often each value appears; the value seen twice is the copy and the one never seen is missing; O(n) time and space |
| `set_mismatch_sums.kara` | with the copy `d` in place of the missing `m`, the values add up to `d - m` more than 1 + ... + n and their squares to `d^2 - m^2` more than the first n squares, so the second difference over the first is `d + m`; O(n) time, O(1) space |
| `set_mismatch_xor.kara` | the exclusive or of the values and of 1 to n is `d ^ m`; its lowest set bit splits both lists into a half holding `d` and a half holding `m`, and a last pass tells which is the copy; O(n) time, O(1) space |
| `set_mismatch_sorted.kara` | a sorted copy runs 1, 2, ... with two equal neighbours at the copy and a jump of two at the gap, or a missing 1 or `n` at an end; O(n log n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: the two LeetCode examples; six more
(the copy and the gap next to each other and far apart, at either end of
the values, the smallest value copying the largest and the largest the
smallest), each with its answer; the sums of the copies, of the missing
values and of the gaps between them over 300 random cases of 2 to
40 values; and three cases of the problem's largest size, 10,000 values.
`set_mismatch.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every value from 1 to `n` counted from scratch. Each of 1,000 cases is
1 to `n` shuffled, `n` from 2 to 30, with the value at one random place
overwritten with the value at another.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the missing value put back in place of one copy gives every value from 1 to `n` once |
| P3 | the copy appears twice and the missing value never |
| P4 | the values in reverse give the same answer |
| P5 | every value `v` turned into `n + 1 - v` turns the answer the same way |

It prints `1000 cases (15943 values), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the value `n` never looked at | P1 215, P2 215, P3 105, P5 356 |
| M2 | ★: a value seen once taken as missing | P1 851, P2 851, P3 851, P5 966 |
| M3 | sums: the copy found as the half difference | P1 1000, P2 1000, P3 1000 |
| M4 | sums: 1 + ... + (n - 1) taken as the sum | P1 1000, P2 1000, P3 881, P5 1000 |
| M5 | xor: the other half's value looked for | P1 1000, P2 1000, P3 1000 |
| M6 | xor: the index split by its own bit, not its value's | P1 561, P2 561, P3 561, P5 598 |
| M7 | sorted: counting from 1 before the first value | P1 110, P2 110, P3 110, P5 220 |
| M8 | sorted: `n - 1` taken as missing when nothing jumps | P1 110, P2 110, P3 110, P5 220 |
| E1 | ★: one slot too many counted | 0 |
| E2 | sums: the missing value as the sum less the copy | 0 |
| E3 | xor: the lowest set bit spelled `both & ~(both - 1)` | 0 |
| E4 | sorted: a value at most the last taken as the copy | 0 |

P1 and P2 kill all eight. P3 misses part of M1: when `n` is the missing
value, M1 leaves it as 0, which never appears either, so only the cases
where `n` is the copy fail P3. P4 sees nothing, and cannot: every arm's
answer depends only on which values appear how often, never on their
order, so a reversed array gives a mutant the same wrong answer. P5 sees
every mutant but M3 and M5, whose wrong answers are still the copy and
the missing value combined with weights adding to 1 (M3 returns `m` and
`2m - d`, M5 the two swapped), and `v -> n + 1 - v` carries such an
answer along exactly as it carries the right one. The four survivors
cannot change an answer: the extra slot is never read; the sum of the
two less the copy is the missing value; `-x` and `~(x - 1)` are the same
bits in two's complement; and in sorted values no value is below the one
before it.

## Verification

Every arm prints the same output as `set_mismatch.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All at kara `8d40e1a762`, debug and
release builds, with runtime archives newer than the last `runtime/src`
change.

The frozen legacy backends refuse every arm and the differential at type
checking: each reads `*x` from `nums.iter()`, and legacy types those
items by value; the harness also hands `seed`, already a `mut ref`
parameter, on with the `mut` marker design.md asks for, which legacy
rejects. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 arrays of 100,000 values
once, each 1 to 100,000 shuffled with one value overwritten by another;
then 2,000 rounds each find the copy and the missing value of one array,
picked by the round, adding them up. Every implementation prints
`2000 rounds over 20 arrays of 100000 values: copies add to
45529300, missing values to 45761600`, the Kāra program under `karac
__mir-run` included (in 315 s).

Each implementation counts into a zeroed array of `n + 1` slots and
scans it: Rust over a `&[i64]` returning a `[i64; 2]`, C over an
`int64_t` array writing a two-slot result, Go over a slice and Python
over a list. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine), each
including making the arrays, which is most of the time:

| | time |
|---|---|
| C (`clang -O3`) | 0.42 to 0.46 s |
| Rust (`rustc -O`) | 0.46 to 0.49 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.47 to 0.50 s |
| Go | 0.65 to 0.72 s |
| Python | 18.2 to 18.5 s |
| Kāra (`karac build --mir`) | 0.46 to 0.59 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: it reads `*x` from `nums.iter()`, which legacy types by value,
and handing `arrays[r % 20]` to `find_error_nums` moves an element out
of a `Vec` while parameters are owned. That edit is by hand, on top of
the `scripts/new-bench.sh` output. A copy outside the kata that reads
`x` and makes the parameter `ref Vec[i64]` builds under legacy and takes
0.54 to 0.58 s. Under `karac __mir-llvm-run` the program prints the same
line in 3.0 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy, a little behind C and Rust and
ahead of Go; six of its seven runs fell between 0.46 and 0.51 s. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
