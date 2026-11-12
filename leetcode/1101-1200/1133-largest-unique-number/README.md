# 1133. Largest Unique Number

Given an integer array `nums`, return the largest integer that only
occurs once. If no integer occurs once, return `-1`.

```
nums = [5,7,3,9,4,9,8,3,1]  ->  8
nums = [9,9,8,8]            ->  -1
```

**Constraints:** `1 <= nums.length <= 2000`; `0 <= nums[i] <= 1000`.

The arms are `fn largest_unique_number(nums: Vec[i64]) -> i64`.

## Approaches

Every value has to be counted before any can be called alone, so each
arm makes one pass to count and then looks for the largest count of 1.
The values are bounded, so the counts fit a fixed array of 1001.

| file | mechanism |
|---|---|
| `largest_unique_number.kara` ★ | every value counted in a fixed array `[0; 1001]`, then the counts read from 1000 down for the first that is 1. O(n + 1001) |
| `largest_unique_number_map.kara` | a `Map` from each value to its count, then the largest key whose count is 1, over a walk in whatever order the map keeps. O(n) |
| `largest_unique_number_sort.kara` | the values sorted, then the runs of equal values walked from the largest down, the first run of one value the answer. O(n log n) |
| `largest_unique_number_sets.kara` | two `Set`s: a value goes in `seen` the first time and in `repeated` every time after, and the answer is the largest of `seen` not in `repeated`. O(n) |
| `largest_unique_number_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, a `Vec<i32>`, a `HashMap` counted with `*count.entry(n).or_insert(0) += 1` over `for &n in &nums`, then `into_iter().filter(..).map(..).max().unwrap_or(-1)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The map, sets and solution arms walk a `Map` or `Set`, whose order is
random per process, but each folds the walk to a largest value, so what
they print does not depend on it.

Every arm prints the same 11 lines: the answers for LeetCode's two
examples and six more (one value, the largest alone, the largest twice,
one value three times, every value twice but 0, and a mix), then over
2000 random arrays of 1 to 60 values, each below a drawn top of 5, 31 or
1001, the answers summed, how many have none, and a checksum (`2000
random arrays: answers total 700206, 491 with none, checksum
529531116`), and two of LeetCode's largest: 2000 values from 0 to 1000
at random (`994`), and every value from 0 to 999 twice (`-1`).
`largest_unique_number.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each value, how often it occurs, counted through the
whole array; the largest value that occurs once, or -1. It checks 2000
problems of 1 to 12 values in five kinds of 400: values from 0 to 1000;
from 0 to 3, so most repeat; 0 and 1000 alone, the ends of the range;
distinct values each twice, with one more alone when the length is odd;
and distinct values once each. Every random choice is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the values reversed give the same answer |
| P3 | the values sorted give the same answer |
| P4 | every value appended a second time leaves none alone: the answer is -1 |
| P5 | the largest value from 0 to 1000 not in the array, appended once, makes the answer the larger of it and the old answer |
| P6 | the answer appended a second time gives an answer below it; with no answer, the first value appended again leaves none |

All 60,000 checks pass on every arm: `2000 problems: checksum
113847577, 60000 checks over 5 arms: 0 failures`. A Python reading of
the same problems, each value's count taken with `list.count`, gives the
same checksum.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`
(three arms keep a `Map` or `Set`), each failing the same way under
both. All thirty are caught. Fifteen are kept, no two failing the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the largest value seen at all | P1 865, P4 2000, P6 2000 |
| M2 | ★: 1000 never read | P1 66, P5 1626 |
| M3 | ★: 0 never the answer | P1 86 |
| M4 | map: the last key with a count of 1 in walk order | P1 657, P2 678, P3 662, P5 974, P6 453 |
| M5 | map: a value seen twice taken as alone | P1 604, P4 1422, P6 1205 |
| M6 | map: the first value skipped | P1 807, P2 803, P3 575, P4 1041, P6 236 |
| M7 | sort: the values never sorted | P1 1396, P2 1316, P3 1396, P4 1729, P5 167, P6 1015 |
| M8 | sort: the smallest value never the answer | P1 281, P5 31 |
| M9 | sort: the largest value answered for any lone run | P1 287, P5 269, P6 1115 |
| M10 | sets: a value marked repeated the first time it is seen | P1 1422, P5 2000 |
| M11 | sets: none answered as 0 | P1 578, P4 2000, P6 664 |
| M12 | sets: the smallest such value | P1 865, P5 1422, P6 865 |
| M13 | solution: a value three times taken as alone | P1 440, P4 1069, P6 679 |
| M14 | solution: 1000 clipped to 999 | P1 66, P5 2000 |
| M15 | solution: an odd answer rounded down to even | P1 693, P5 308, P6 693 |

P1 catches all fifteen, P6 ten, P5 nine, P4 six, and P2 and P3 three
each. P2 and P3 change only the order of the values, so they see only
the edits whose answer depends on it: the map's walk order (M4, whose
counts are those of `KARAC_HASH_SEED=1`), the first value skipped (M6),
and runs read without sorting (M7). P4 sees the edits that answer
something when every value repeats: any value seen at all (M1), a value
seen twice or three times taken as alone (M5, M13), a skipped first
value that leaves its twin alone (M6), runs read unsorted (M7), and none
answered as 0 (M11). P5 sees nine: edits that miss a lone value, such as
1000 never read or clipped (M2, M14) or every value marked repeated
(M10), and edits that answer a lone value other than the largest (M12,
M15). P6 sees ten: the answer appended again must move the answer down,
and an edit that answers a repeated value, or the smallest lone one,
does not move it down. Only P1 sees 0 never answered (M3): no
property moves the answer to 0, and the literal answer is 0 on 86 of the
2000 problems.

Of the fifteen not kept, eight fail exactly as a kept one: a value
counted once however often in the ★ and map arms, as M1; the counts read
from 0 up in the ★ arm and the smallest value taken in the solution arm,
as M12; each count started at 1 in the solution arm, as M10; 0 never
counted in the solution arm, as M3; and none answered as 0 in the ★ and
map arms, as M11. The other seven fail each in a way of its own and were
not needed.

## Verification

Every arm prints the same output as `largest_unique_number.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found no gap. The ★, map, sort and sets arms were written as
Kāra and checked clean as written. `karac fix` carried the solution arm
in three rounds: `Vec<..>` to `Vec[..]`, the `use std::collections::HashMap`
line dropped, `HashMap::new()` to `HashMap.new()`, `for &n in &nums` to
`for n in ref nums`, the `&(_, c)` and `&x` patterns to `(_, c)` and `x`,
and `::` to `.`; then `HashMap` to `Map` and `struct Solution {}`
declared; then the `as i64` at the call dropped, an `i32` widening by
itself. `*count.entry(n).or_insert(0) += 1` is Kāra as written.

## Benchmarks

The bench builds 256 arrays of 2000 values once, LeetCode's largest,
their values from 0 to 1000. Each of 1000 rounds changes one value of
every array and answers the array with the ★ arm: 256,000 calls. Every
implementation prints `1000 rounds over 256 arrays of 2000 values:
answers total 255282101, checksum 994782431`. Each keeps an array as its
own allocation (`Vec[i64]`, `Vec<i64>`, `[]int64`, a Python list, and
C's `int64_t *`) and counts into a fixed array of 1001 on the stack in
every call (`[0; 1001]`, `[0i64; 1001]`, `[1001]int64`, `int64_t[1001]`;
Python's is a list).

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `73ec8b248f`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.314 to 0.440 s | 0.328 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.287 to 0.506 s | 0.333 s |
| Kāra (`karac build`) | 0.297 to 0.398 s | 0.369 s |
| Go | 0.301 to 0.398 s | 0.371 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.297 to 0.402 s | 0.386 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.366 to 0.458 s | 0.388 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.320 to 0.467 s | 0.399 s |
| Rust (`rustc -O`) | 0.379 to 0.575 s | 0.400 s |
| Python | 14.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 1.18x C's time and about Rust's (0.99x Rust under
overflow checks, 0.97x plain `rustc -O`): each call clears 1001 counts,
adds one for each of 2000 values, a load and a store to a place the
value picks, and reads the counts back from the top. Go takes about
0.96x Kāra's time. Python takes about 37x Kāra's time.
