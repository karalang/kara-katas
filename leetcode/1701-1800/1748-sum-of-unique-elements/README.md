# 1748. Sum of Unique Elements

You are given an integer array `nums`. The unique elements of an array
are the elements that appear **exactly once** in the array.

Return *the **sum** of all the unique elements of* `nums`.

```
nums = [1, 2, 3, 2]       ->  4    1 + 3
nums = [1, 1, 1, 1, 1]    ->  0
nums = [1, 2, 3, 4, 5]    ->  15
```

**Constraints:** `1 <= nums.length <= 100`; `1 <= nums[i] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `unique.kara` ★ | one pass with a state per value from 1 to 100: unseen, seen once, or seen more often. The first sight adds the value to the sum, the second takes it back out, and later sights change nothing. O(n) |
| `unique_map.kara` | every value counted in a `Map` with `entry(..).or_insert(0)`, then the values counted once summed with `filter` and `sum`; the sum does not depend on the order the map is walked in. O(n) |
| `unique_sort.kara` | a sorted copy, where a value is unique when it differs from both its neighbours. O(n log n) |
| `unique_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `[0; 101]` count array filled by `for &x in &nums`, then `nums.iter().filter(..).sum()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, then one
value, every value from 1 to 100 once, and every one twice; then the
sum of the answers and a checksum for 3000 random arrays of up to 10
values from 1 to 5, 1000 of up to 100 from 1 to 50, and 1000 of up to
100 from 1 to 100, LeetCode's limits. `unique.py` mirrors the ★ arm and
its output is byte-identical.

```
4
0
15
100
5050
0
3000 arrays of up to 10 values from 1 to 5: unique sums add to 15430, checksum 981362218
1000 arrays of up to 100 values from 1 to 50: unique sums add to 397818, checksum 388041418
1000 arrays of up to 100 values from 1 to 100: unique sums add to 1354511, checksum 561022795
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each value counted by scanning the whole array for it, and
the values that appear exactly once added up. It checks 3000 random
arrays of 1 to 10 values, half from 1 to 6 and half from 95 to 100, so
the top of the range is reached, each with a random value of the same
range to append. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | the array written twice over sums to 0 |
| P4 | one more value adds it if it was absent, takes it away if it was there once, and changes nothing otherwise |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 890097229, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, each value kept when `nums.count(x) == 1`, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second sight no longer takes the value back out | P1 2144, P3 3000, P4 1026, P5 2144 |
| M2 | ★: the state capped at seen once, so every later sight takes the value out again | P1 1125, P3 2144, P4 731, P5 1125 |
| M3 | ★: the value 1 never added on its first sight | P1 834, P3 834, P4 99, P5 834 |
| M4 | map: the values counted once or twice summed | P1 1831, P3 2810, P4 1499, P5 1831 |
| M5 | map: each count set to 1, not added to | P1 2144, P3 3000, P4 1026, P5 2144 |
| M6 | sort: only the left neighbour compared | P1 2144, P3 3000, P4 1026, P5 2144 |
| M7 | sort: a value alone on its left only when the one before it is at least two smaller | P1 1792, P4 1209, P5 1792 |
| M8 | sort: the sorted copy deduplicated | P1 2144, P3 3000, P4 1026, P5 2144 |
| M9 | solution: every value counted at least once summed | P1 2144, P3 3000, P4 1757, P5 2144 |
| M10 | solution: the value 100 never counted | P1 509, P4 200, P5 509 |

## Benchmarks

The bench draws 50000 random arrays of 100 values from 1 to 100,
LeetCode's limits, all of them first, then answers each 10 times by the
★ arm in all five languages; each answer starts from a fresh 101-entry
state array. Every implementation prints `50000 arrays of 100 values, 10
rounds: unique sums add to 931965270, checksum 311180987`. The C build
also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.276 s |
| Go | 0.288 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.291 s |
| Rust (`rustc -O`) | 0.313 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.313 s |
| Kāra (`karac build`) | 0.314 s |
| Python | 4.2 s |

The sequential Kāra build is 7% faster than Rust and 7% faster than Rust with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is the fastest here at 0.276 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.296 s and
0.309 s on one run).

## Verification

All four arms print the same output as `unique.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ and sort arms were first written with `let mut sum = 0;` and took
one `karac fix` each: a literal binding defaults to `i64`, and the
function returns `i32`, so the fix wrote `sum: i32`. The map arm checked
clean as written.

LeetCode's Rust template took one `karac fix` of 9 edits: `struct
Solution {}` added, `Vec<i32>` written `Vec[i32]`, `for &x in &nums`
written `for x in ref nums`, the closure's `|&&x|` pattern written
`|x|`, and `Solution::sum_of_unique` written `Solution.sum_of_unique`.
The `[0; 101]` array and the `x as usize` index carried over as
written.

The differential's `arm` first cast its `i32` answer to `i64` on
return, and one `karac fix` dropped the cast as the widening is
implicit. The bench checked clean as written.
