# 1711. Count Good Meals

A **good meal** is a meal that contains **exactly two different food
items** with a sum of deliciousness equal to a power of two.

You can pick **any** two different foods to make a good meal.

Given an array of integers `deliciousness` where `deliciousness[i]` is the
deliciousness of the `ith` item of food, return *the number of different
**good meals** you can make from this list modulo* `10^9 + 7`.

Note that items with different indices are considered different even if
they have the same deliciousness value.

```
deliciousness = [1,3,5,7,9]          ->  4
deliciousness = [1,1,1,3,3,3,7]      ->  15
```

**Constraints:** `1 <= deliciousness.length <= 10^5`;
`0 <= deliciousness[i] <= 2^20`.

## Approaches

| file | mechanism |
|---|---|
| `meals.kara` ★ | one pass: two dishes make at most `2^21`, so for each dish the 22 powers `2^0` to `2^21` each name the one value it pairs with, and a `Map` of the dishes seen so far says how many earlier ones have it. O(22 n) |
| `meals_sorted.kara` | the dishes sorted, and for each power two pointers closing in from both ends; a match counts the runs of equal values at each end, or, when the ends meet in one run, its pairs. O(n log n + 22 n) |
| `meals_counts.kara` | the dishes counted by value in an array as long as the largest dish; each value that occurs pairs with each larger value that makes a power, and with itself when it is half of one, so each pair is counted once, from its smaller value. O(m + 22 n), m the largest dish |
| `meals_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `const MOD: i64` in the function, a `HashMap<i32, i64>` read with `if let Some(&c) = count.get(&target)` and written with `*count.entry(d).or_insert(0) += 1`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, one dish, two
zeros (0 is not a power of two), and two dishes of `2^20`, the largest;
then the answers summed and a checksum for 3000 random lists of up to 12
dishes up to 16, 300 of up to 1000 up to 4096, and 10 of up to `10^5`
up to 1000. `meals.py` mirrors the ★ arm and its output is
byte-identical.

```
4
15
0
0
1
3000 lists of up to 12 dishes up to 16: answers sum to 9057, checksum 922222922
300 lists of up to 1000 dishes up to 4096: answers sum to 24292, checksum 586414885
10 lists of up to 100000 dishes up to 1000: answers sum to 3777198, checksum 119351022
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every two different dishes, by index, whose sum is one of 1,
2, 4, 8, ..., found by doubling from 1 until the sum is reached or
passed. It checks 3000 random lists of 1 to 10 dishes, each below a
random bound from 1 to 17. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the dishes listed in reverse give the same answer |
| P3 | one more dish of 0 adds one meal for each dish that is a power of two |
| P4 | every dish doubled gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 733159669, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, every pair whose sum's `bin` holds one `1`,
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M6, the low pointer stepped
one place instead of past its run, was equivalent: the high pointer has
already moved below its own run, so each step through the rest of the
low run finds the sum too small and steps on. It was replaced. M4 and
M6 miscount the same thing, the pairs within one run, and fail the very
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the power 1 left out | P1 810, P3 1412, P4 810, P5 810 |
| M2 | ★: a value seen again counted once | P1 1062, P2 965, P3 1175, P5 1062 |
| M3 | ★: each dish counted as seen 22 more times, inside the loop over powers | P1 2458, P3 2362, P4 2362, P5 2458 |
| M4 | sorted: a run's pairs `run * run / 2` | P1 1175, P5 1175 |
| M5 | sorted: the two runs' sizes added, not multiplied | P1 521, P3 742, P5 521 |
| M6 | sorted: a run one dish short | P1 1175, P5 1175 |
| M7 | counts: a value paired with smaller values too | P1 1913, P3 2362, P5 1913 |
| M8 | counts: a value's pairs with itself `c (c + 1) / 2` | P1 2362, P5 2362 |
| M9 | solution: a value's first dish counted twice | P1 2064, P2 965, P3 2362, P5 2064 |
| M10 | solution: each power's partner one too small | P1 2033, P3 2325, P4 1901, P5 2033 |

## Benchmarks

The bench draws 10 random lists of `10^5` dishes up to `2^20`,
LeetCode's largest, all of them first, then answers each 3 times by the
★ arm in all five languages; each answer builds its map anew. Every
implementation prints `10 lists of 100000 dishes, 3 rounds: answers sum
to 286503, checksum 320724298`. C has no map: its mirror probes a table
of `2^18` slots linearly, the key hashed by one multiply, which is less
work than Kāra's SipHash `Map`, Rust's SipHash `HashMap` or Go's `map`
do. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.468 s |
| Rust (`rustc -O`) | 0.768 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.807 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.879 s |
| Kāra (`karac build`) | 0.921 s |
| Go | 1.230 s |
| Python | 5.9 s |

The sequential Kāra build takes 1.14x Rust's time and 1.09x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.468 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.913 s and 0.921 s on one
run).

## Verification

All four arms print the same output as `meals.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, sorted and counts arms checked clean as first written. The counts
arm first sized its array `2^20 + 1` whatever the dishes, as the
constraint allows; every answer then filled 8 MB, and the differential,
answering 12000 small lists, took 17 s compiled. It now sizes the array
by the largest dish.

LeetCode's Rust template took one `karac fix` of 13 edits:
`struct Solution {}` added, `use std::collections::HashMap;` deleted
(`Map` is in Kāra's prelude), `Vec<i32>` written `Vec[i32]`,
`HashMap<i32, i64>` and `HashMap::new()` written `Map[i32, i64]` and
`Map.new()`, `for &d` written `for d`, and `if let Some(&c) =
count.get(&target)` written `if let Some(c) =
count.get(target).cloned()`. The `const MOD: i64 = 1_000_000_007;`
inside the function and `*count.entry(d).or_insert(0) += 1` carried
over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
