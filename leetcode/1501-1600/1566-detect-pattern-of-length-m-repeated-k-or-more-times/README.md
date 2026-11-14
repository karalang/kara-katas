# 1566. Detect Pattern of Length M Repeated K or More Times

Given an array of positive integers `arr`, find a pattern of length `m`
that is repeated `k` or more times. A pattern is a subarray of one or
more consecutive elements repeated several times consecutively without
overlapping. Return `true` if there exists a pattern of length `m` that is
repeated `k` or more times, otherwise return `false`.

```
arr = [1,2,4,4,4,4], m = 1, k = 3          ->  true
arr = [1,2,1,2,1,1,1,3], m = 2, k = 2      ->  true
arr = [1,2,1,2,1,3], m = 2, k = 3          ->  false
arr = [1,2,3,1,2], m = 2, k = 2            ->  false
arr = [2,2,2,2], m = 2, k = 3              ->  false
```

**Constraints:** `2 <= arr.length <= 100`; `1 <= arr[i] <= 100`;
`1 <= m <= 100`; `2 <= k <= 100`.

## Approaches

A pattern of length `m` written `k` times is a stretch where every value
equals the one `m` places on, for `m (k - 1)` places in a row.

| file | mechanism |
|---|---|
| `pattern.kara` ★ | one pass counting the current run of `arr[i] == arr[i + m]`; a run of `m (k - 1)` is the pattern. O(n) |
| `pattern_chunks.kara` | every start tried: the `m k` values from it, a slice cut by `chunks(m)`, and the pattern found when every chunk equals the first. O(n m k) |
| `pattern_split.kara` | the agreements `m` apart collected into a `Vec[bool]`, cut by `split` at every place they fail, and a piece of `m (k - 1)` agreements is the pattern. O(n) |
| `pattern_solution.kara` | LeetCode's Rust template (`contains_pattern(arr: Vec<i32>, m: i32, k: i32) -> bool`, the ★ arm with `usize` counts and `saturating_sub`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's five examples, then
`[2, 2]` and `[1, 2]` with `m` of 1 and `k` of 2, and `[3, 1, 2]` written
three times, whole and with its last value changed, with `m` and `k` of
3; then the count of `true` answers and a checksum for 3000 random arrays
of up to 10 values, 300 of up to 100 and 30 of up to 100000, each over its
own first 1 to 4 values, half with a run of one pattern planted, with an
`m` from 1 to 4 and a `k` from 2 to 5. `pattern.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: some start and some count `c` of at least `k`, the `m c`
values from that start each equal to the value at the same place in the
first `m`. It checks 3000 arrays of 2 to 10 values over their own first 1
to 3 values, each with an `m` from 1 to 4 and a `k` from 2 to 4, every
random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is `false` when `m k` is more than the length |
| P3 | the array reversed leaves the answer |
| P4 | every value moved on by one leaves the answer |
| P5 | the first `m` values written `k` times, the array after them, has the pattern |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 579244862, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run of `m k` needed | P1 372, P6 372 |
| M2 | ★: the run never broken | P1 118, P6 118 |
| M3 | ★: the last comparison never made | P1 138, P3 75, P6 138 |
| M4 | chunks: the last start never tried | P1 138, P3 75, P6 138 |
| M5 | chunks: every chunk compared with the array's first `m` | P1 134, P3 131, P6 134 |
| M6 | split: a piece longer than `m (k - 1)` needed | P1 276, P6 276 |
| M7 | split: agreements `m - 1` apart | P1 300, P3 43, P5 1005, P6 300 |
| M8 | template: a broken run kept at up to `m` | P1 100, P3 27, P6 100 |
| M9 | template: a `k` of 2 never found | P1 428, P5 969, P6 428 |
| M10 | template: the first comparison never made | P1 139, P3 75, P6 139 |

## Benchmarks

The bench draws 20 arrays of 100000 values of 1 to 100 once, half with a
pattern written three times near the end, and asks each for `m` from 1 to
50 with `k` of 3 by the ★ arm, in all five languages; most calls scan the
whole array. Every implementation prints `m from 1 to 50 over 20 arrays
of 100000 values: 30 with a pattern, checksum 415269324`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.083 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.084 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.095 s |
| Kāra (`karac build`) | 0.099 s |
| C (`clang -O3`) | 0.103 s |
| Go | 0.145 s |
| Python | 4.9 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.09 s and 0.10 s on one run).

Kāra is 1.13x Rust under overflow checks by median. Not traced. The loop
is two loads, a compare and a counter, and the arrays' construction is a
large share of every row at this size; C sits behind both Rust rows, so
the spread between the compiled rows but Go's is within the noise of a
0.1 s program.

## Verification

All four arms print the same output as `pattern.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★ arm was written in Kāra and checked as written. The chunks and
split arms called `all` and `any` straight on `chunks(m)` and `split(..)`,
which return a `Vec`; each was refused with a message naming
`.into_iter()`, and one round of `karac fix` added it.

The Rust template took 3 changed lines, then 1 added, then 1 changed,
over three rounds of `karac fix`: the `Vec<..>` types to `Vec[..]`, the
wrapper's `|&a|` to `|a|` and `Solution::` to `Solution.`; then
`struct Solution {}` added; then the `m as usize, k as usize` casts to
`as i64`, from refusals that `usize` mixes with the `i64` that
`saturating_sub` and the count take. It checks and agrees with no hand
edit.
