# 1590. Make Sum Divisible by P

Given an array of positive integers `nums`, remove the smallest subarray
(possibly empty) such that the sum of the remaining elements is divisible
by `p`. It is not allowed to remove the whole array.

Return the length of the smallest subarray that you need to remove, or
`-1` if it's impossible.

A subarray is defined as a contiguous block of elements in the array.

```
nums = [3,1,4,2], p = 6  ->  1
nums = [6,3,5,2], p = 9  ->  2
nums = [1,2,3],   p = 3  ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`;
`1 <= p <= 10^9`.

## Approaches

The part removed must have the whole sum's remainder `need`; a part
`nums[i..j)` does when the prefix sums before `i` and before `j` differ
by `need` modulo `p`.

| file | mechanism |
|---|---|
| `divisible.kara` ★ | the latest prefix with each remainder in a `Map[i64, i64]`, each end matched with the latest prefix of remainder `prefix(j) - need`. O(n) |
| `divisible_sorted.kara` | no hash map: every prefix remainder paired with its place as an `(i64, i64)` tuple, the pairs sorted, and each end a hand-written binary search by tuple comparison for the last earlier prefix with the remainder it needs. O(n log n) |
| `divisible_kept.kara` | what is kept: a prefix and a suffix whose sums add to a multiple of `p`; walking the start from the right, a `SortedMap` holds each suffix remainder's nearest start. O(n log n) |
| `divisible_solution.kara` | LeetCode's Rust template (a `HashMap<i64, i32>`, `rem_euclid`, `if let Some(&j)`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and five
more (one with no answer, three values of `10^9`, one where only the
whole array would do, and a single value either way), then the count
impossible and a checksum for 3000 random problems of up to 8 values up
to 9 with `p` up to 12, 300 of up to 1000 values up to `10^9` with `p` up
to 1000, and 10 of up to 100000 values with `p` up to 100000.
`divisible.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every subarray shorter than the whole array, the empty one
too, removed in turn by length and what is left summed. It checks 3000
problems of 1 to 8 values from 1 to 9 and `p` from 1 to 12, every random
choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed leaves the answer |
| P3 | every value raised by `p` leaves the answer |
| P4 | every value and `p` multiplied by 3 leave the answer |
| P5 | every value made its remainder (a 0 made `p`) leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 211264179, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

One first choice was replaced: searching the sorted arm for `<=` in
place of `<` is equivalent, since the pair it would pass is `(prefix(j),
j)`, and that needs `need == 0`, which returns first.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty prefix (remainder 0 before place 0) never stored | P1 258, P2 508, P6 258 |
| M2 | ★: each remainder keeps its first place, not its latest | P1 425, P2 747, P6 425 |
| M3 | ★: no `-1` when nothing short enough works | P1 731, P6 731 |
| M4 | sorted: any earlier pair accepted, whatever its remainder | P1 1592, P2 1143, P6 1592 |
| M5 | sorted: the search stops one place too early | P1 1090, P6 1090 |
| M6 | kept: the empty suffix never stored | P1 250, P2 508, P6 250 |
| M7 | kept: the remainder wanted not reduced modulo `p` | P1 636, P6 636 |
| M8 | kept: the last value never taken as a start | P1 1011, P2 823, P6 1011 |
| M9 | template: `%` in place of `rem_euclid` | P1 247, P2 205, P6 247 |
| M10 | template: no early 0 when the sum already divides | P1 750, P6 750 |

## Benchmarks

The bench runs the ★ arm on 40 problems of 100000 values up to 10^9, p
up to 10^5, all drawn first, in all five languages. Every implementation
prints `40 problems of 100000 values: lengths 44, checksum 568685717`. C
has no map; the C mirror uses an open-addressing table of remainders
with linear probing and a multiplicative hash, grown at half full and
allocated per call, as Kāra's `Map` is.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.174 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.251 s |
| Kāra (`karac build`) | 0.264 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.269 s |
| Rust (`rustc -O`) | 0.271 s |
| Go | 0.329 s |
| Python | 3.2 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (0.237 s and 0.246 s on one run).

## Verification

All four arms print the same output as `divisible.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The sorted and kept arms were written in Kāra and checked as written.
The ★ arm wrote `prefix + *v as i64`, and `karac fix` dropped the cast;
the harness wrote `min_subarray(nums, *p)`, and `karac fix` dropped the
`*`, as a tuple pattern over a borrowed `(Vec[i32], i32)` binds the
`i32` by copy.

The Rust template took three rounds of `karac fix`:

1. `use std::collections::HashMap` dropped, `struct Solution;` to
   `struct Solution {}`, the `<..>` types to `[..]`, `HashMap::new()` to
   `HashMap.new()`, the `|&x|` and `(i, &x)` patterns to plain names,
   `if let Some(&j) = seen.get(&target)` to
   `if let Some(j) = seen.get(target).cloned()`, and `Solution::` to
   `Solution.`;
2. `HashMap[i64, i32]` to `Map[i64, i32]`;
3. `0i64` to `0`.

It then checks and agrees with no hand edit; `rem_euclid` is Kāra's as
well.
