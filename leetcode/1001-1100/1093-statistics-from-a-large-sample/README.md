# 1093. Statistics from a Large Sample

You are given a large sample of integers in the range `[0, 255]`. Since
the sample is so large, it is represented by an array `count` where
`count[k]` is the **number of times** that `k` appears in the sample.

Calculate the following statistics:

- `minimum`: the minimum element in the sample.
- `maximum`: the maximum element in the sample.
- `mean`: the average of the sample, the total sum of all elements
  divided by the total number of elements.
- `median`: if the sample has an odd number of elements, the middle
  element once the sample is sorted; if it has an even number, the
  average of the two middle elements once the sample is sorted.
- `mode`: the number that appears the most in the sample. It is
  guaranteed to be **unique**.

Return the statistics of the sample as an array of floating-point
numbers `[minimum, maximum, mean, median, mode]`. Answers within `10^-5`
of the actual answer are accepted.

```
count = [0,1,3,4,0,...,0]    ->  [1.00000, 3.00000, 2.37500, 2.50000, 3.00000]
count = [0,4,3,2,2,0,...,0]  ->  [1.00000, 4.00000, 2.18182, 2.00000, 1.00000]
```

**Constraints:** `count.length == 256`; `0 <= count[i] <= 10^9`;
`1 <= sum(count) <= 10^9`; the mode of the sample is unique.

The arms are `fn sample_stats(count: Vec[i64]) -> Vec[f64]`. The mean is
the exact sum over the exact total, one division, so every arm gives the
same `f64` and the harness compares them exactly.

## Approaches

| file | mechanism |
|---|---|
| `sample_stats.kara` ★ | two walks over the counts: the first finds the smallest and largest value present, the sum, the total and the mode; the second walks the running total to the middle place, or the two middle places `(total - 1) / 2` and `total / 2` when the total is even, and `break`s at the second. The sample is never built. O(256) |
| `sample_stats_ends.kara` | the median from both ends: the ends by `position` and `rposition`, then values taken off both ends at once from a copy of the counts, as many from each as the smaller end has left, until the ends meet on one value or run out together on two; the result of a `loop` with `break value`. The mean and the mode come from one walk between the ends (`low..=high`). O(256) |
| `sample_stats_chain.kara` | iterator chains: the ends by `position` / `rposition`, the total and the sum by `sum` (over `enumerate` weighted by value), the mode by `max_by_key` on the count, and each middle place by a closure that `scan`s the running total and takes the first `position` past it. O(256) |
| `sample_stats_prefix.kara` | prefix sums and a binary search: `before[k]` how many of the sample are below value k, so the value at place p is the last k with `before[k] <= p`, found with `partition_point` in a closure; the ends are the values at places 0 and `total - 1`, the mode the largest step of `before`. O(256) |
| `sample_stats_map.kara` | a `SortedMap` of the values present to their counts: `first()` and `last()` are the ends, a walk in key order gives the sum, the total and the mode as a tuple `(value, count)`, and a second walk fills the two middle values with a `while` that can take both at one value. O(m log m) for the m values present |
| `sample_stats_solution.kara` | LeetCode's Rust template (`impl Solution` over a `Vec<i32>`, `-1i32`, `0usize`, `for (i, &c) in count.iter().enumerate()`, a closure `\|k: i64\| -> i32` that `return`s the value at a place, `vec![..]`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more (one value counted once at either end, both ends, one value counted
10^9 times, 10^9 values split 499,999,999 at 0 and 500,000,001 at 255 so
that both middles are the first 255, and three spread samples), then a
sum of modes and a checksum over 2000 random samples of 1 to 12 values
counted 1 to 20 or up to 10^8 times (`modes sum to 245126, checksum
277522457`), and a sample spread over all 256 places with 10^9 values in
all, LeetCode's largest (`[0.0, 239.0, 117.61268, 121.0, 145.0]`).
`sample_stats.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the sample written out, every value as many times as it is
counted, and sorted; the smallest is the first, the largest the last,
the mean the sum over the size, the median the middle one or the
halfway point of the middle two, and the mode the value with the
longest run. It checks 2000 samples in four kinds of 500: 1 to 12
values counted 1 to 20 times; 1 to 4 values counted 1 to 2000 times; 1
or 2 values counted up to 9 * 10^7 times; and 30 to 80 values counted 1
to 50 times. A shared largest count is broken as LeetCode promises, by
counting the first value with it once more. The 1500 samples of up to
20,000 values are read literally; the 500 large ones are checked by the
properties alone. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the five numbers are the statement read literally (samples of up to 20,000 values) |
| P2 | the smallest and largest are the first and last values counted, the mean and the median lie between them, and the mode is the value counted most |
| P3 | every value moved up by the same amount (or down to 0 when 255 is counted) moves all five numbers by it, the mean to within 10^-9 |
| P4 | every count multiplied by 2 to 5 (while the sample stays within 10^9) gives the same five numbers, exactly |
| P5 | every value k read as 255 - k turns the five numbers round: the smallest is 255 less the largest, and so on, the mean to within 10^-9 |
| P6 | a new value counted fewer times than the mode, past the largest or below the smallest, keeps the mode, becomes the new end and moves the median only that way; with no room past either end, more of the mode keeps both ends |

All 69,000 checks pass on every arm: `2000 samples: checksum 955858004,
69000 checks over 6 arms (9000 read literally): 0 failures`. A Python
reading of the same samples, by running totals, gives the same checksum
over the ★ arm's answers.

P4 asks for the mean exactly: the sum and the total are both multiplied,
both stay below 2^53, and `f64` division is correctly rounded, so the
same fraction gives the same `f64`.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught, two of them by an index out of
bounds inside the arm. Fifteen are kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the upper middle found a place early | P1 76, P2 12, P3 44, P4 45, P5 116, P6 38 |
| M2 | ★: the mean divided as integers | P1 1304, P5 1574 |
| M3 | ★: an even sample takes the upper middle twice | P1 31, P5 31 |
| M4 | ends: the larger end taken off both | P1 1313, P6 113 |
| M5 | ends: the high end jumping down to the low one | P1 352, P5 363, P6 255 |
| M6 | ends: the largest value left out of the sums | P1 1500, P2 757, P3 415, P4 415, P5 2000, P6 341 |
| M7 | chain: a place found one early | P1 108, P2 7, P3 7, P4 77, P5 176 |
| M8 | chain: the least counted as the mode | P1 1500, P2 2000, P3 1976, P5 2000, P6 38 |
| M9 | chain: a value counted once never the largest | P1 26, P2 26, P4 26, P5 63, P6 49 |
| M10 | prefix: a place found one early | index out of bounds |
| M11 | prefix: the smallest read one place late | P1 37, P2 37, P4 37, P5 63, P6 3 |
| M12 | map: a mode needs to win by two | P1 142, P2 142, P4 142, P5 484, P6 12 |
| M13 | map: the smallest read from the wrong end | P1 1315, P2 1585, P5 1585, P6 1976 |
| M14 | solution: the median half high | P1 1500, P2 649, P5 2000 |
| M15 | solution: the largest count taken for the largest value | P1 1500, P2 2000, P3 1976, P4 2000, P5 2000, P6 1904 |

Of the fourteen that fail by property, P1 catches all fourteen, P5
thirteen, P2 and P6 ten each, P4 seven and P3 five. P5 is the strongest
property because the mirror turns an error at one end into an error at
the other, and an arm that leans one way (the upper middle, the last
value) fails it. P3 is the weakest: a shift moves every value together,
so an edit that is off by the same amount everywhere (the integer mean,
M2) shifts with it. The even-sample edits (M3 and the three like it) are
the hardest to see: the two middle places straddle two values in only 31
of the 2000 samples.

Four edits first written turned out to change nothing, and were
replaced: the ★ and solution arms keeping the last of equal counts for
the mode, and the ends arm starting its mode search at the largest
value (all three only matter for a shared largest count, which the
problem rules out), and the ends arm stopping on `next_lo > hi` for
`next_lo >= hi` (when they meet, `next_hi` is already below `next_lo`).

Of the fifteen caught but not kept, four fail exactly as M3 (the ends
arm reading two middles as the lower one or half high, the chain arm
taking the upper middle twice, the map arm the lower middle twice), and
three as another kept edit: the prefix arm reading the largest one place
early as M9, the solution arm finding a place one early as M7, and the
map arm taking one middle per value at most, out of bounds as M10. Eight
fail in ways of their own but were not needed: the ★ arm never moving
the largest value and summing each value once, the chain arm summing
values one high, the prefix arm taking the least counted as the mode
and doubling the sum, the map arm counting every value once more, and
the solution arm counting values instead of their counts and summing
the counts instead of the values.

## Verification

Every arm prints the same output as `sample_stats.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing
on any file, and `karac fix` has nothing to apply.

The kata found one gap, fixed in the compiler:

- The Rust template's median helper is a closure `|k: i64| -> i32 {
  ..; return i as i32; ..; 0 }`. A closure does not declare its return
  type, so `karac fix` deletes the `-> i32`, and the fixed program was
  then refused: "closure returns conflicting types: 'i64' vs 'i32'".
  The closure's type is its tail unified with its `return`s, and the
  tail `0`, with nothing to say otherwise, had already been typed
  `i64`. An unsuffixed integer literal returned or left as the tail now
  waits for the closure's other returns and takes their integer type, as
  it would against a declared one; a literal out of that type's range is
  still refused, and a literal beside a non-integer return still
  conflicts (kara B-2026-11-10-22, pinned by
  `tests/kata_1093_closure_literal_return.rs`).

With that, the Rust arm reaches a clean check in three rounds of `karac
fix`, and gives the text the arm holds. The first round is the syntax:
`Vec<i32>` and `Vec<f64>` to `[..]`, the `&c` patterns to `c`, and the
closure's `-> i32` deleted. The second declares `struct Solution {}`.
The third drops the suffixes the context already gives (`0usize`,
`0i64`), the `as i64` on a value already `i64`, and turns `vec![..]`
into a list literal.

## Benchmarks

The bench builds 64 count arrays of 256 places once, each a sample of 4
to 256 values counted up to 3 * 10^6 times, from 6 million values to
258 million. Each of 10,000 rounds adds one to a count in every
array and answers it with the ★ arm, folding all five numbers into a
checksum. Every implementation prints `10000 rounds over 64 samples:
modes sum to 84160000, checksum 465968662`. C writes the five numbers
into the caller's array; Kāra, Rust and Go return a new five-element
vector from each of the 640,000 calls, and Python a list.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `c51750c190`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.253 to 0.412 s | 0.276 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.258 to 0.445 s | 0.293 s |
| Kāra (`karac build`) | 0.342 to 0.460 s | 0.369 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.357 to 0.487 s | 0.413 s |
| Go | 0.383 to 0.605 s | 0.481 s |
| Rust (`rustc -O`) | 0.471 to 0.537 s | 0.502 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.493 to 0.579 s | 0.521 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.493 to 0.599 s | 0.522 s |
| Python | 30.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone: 0.04 s between their medians is the spread of these runs. Kāra
takes 1.3x to 1.5x C's time, with its bounds and overflow checks on, and
is ahead of Go and of Rust with or without overflow checks. Python takes
about 80x Kāra's time.
