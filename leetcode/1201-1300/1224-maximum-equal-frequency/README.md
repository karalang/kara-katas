# 1224. Maximum Equal Frequency

Given an array `nums` of positive integers, return the longest possible
length of an array prefix of `nums`, such that it is possible to remove
**exactly one** element from this prefix so that every number that has
appeared in it will have the same number of occurrences.

If after removing one element there are no remaining elements, it's still
considered that every appeared number has the same number of occurrences
(0).

```
nums = [2,2,1,1,5,3,3,5]                ->  7     [2,2,1,1,5,3,3] less the 5
nums = [1,1,1,2,2,2,3,3,3,4,4,4,5]      ->  13
```

**Constraints:** `2 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^5`.

The arms are `fn max_equal_freq(nums: Vec[i64]) -> i64`. The two Rust
arms keep the method LeetCode gives Rust users, on `i32`, inside `impl
Solution`, and a short `max_equal_freq` converts to and from it.

## Approaches

| file | mechanism |
|---|---|
| `maximum_equal_frequency.kara` ★ | walk the prefixes keeping each number's count and how many numbers have each count. A prefix of length `len` works when every number appears once, or all share the top count but one number that appears once, or all share one count less than the top but one number that has the top. O(n) |
| `maximum_equal_frequency_maps.kara` | each number's count in a `Map`, and how many numbers have each count in another, a count dropped when no number has it; a prefix works when its counts are one value that is 1 or held by one number, or two values: 1 held by one number, or two neighbours whose larger is held by one number |
| `maximum_equal_frequency_ordered.kara` | the same walk with how many numbers have each count in a `SortedMap`, the least and the greatest count read off its ends by `first()` and `last()`. O(n log n) |
| `maximum_equal_frequency_backwards.kara` | from the whole array down: count everything, then take numbers off the end until what is left works, reading the least and greatest count off the `SortedMap`'s ends. O(n log n) |
| `maximum_equal_frequency_counts.kara` | a Rust solution as LeetCode's Rust users write it (`cnt` and `freq` as `vec![0usize; 100001]`, the numbers cast `as usize`, the three shapes tested on `usize` lengths), carried to Kāra by `karac fix` |
| `maximum_equal_frequency_hashed.kara` | another Rust solution (the counts and the counts' counts in two `HashMap<i32, i32>`s updated through `entry(..).or_insert(0)`, read back by a closure `\|k\| *freq.get(&k).unwrap_or(&0)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's two examples, `[1, 1]`
(`2`) and `1` to `9` (`9`), the total and a checksum of the answers for
1000 random arrays of 2 to 31 numbers (`9423`, `792469661`), and three
answers at the constraints' top, 10^5 numbers: all different (`100000`),
316 blocks of 316 equal numbers and one more number (`99857`, the whole
array less its last), and random numbers up to 10^5 (`338`).
`maximum_equal_frequency.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★ and ordered arms check clean as written. The maps
arm was first written `let before = count.get(x).unwrap_or(0)`, which
keeps a reference into the map it then writes, and the fix reads the
count out, `*count.get(x).unwrap_or(0)`. The backwards arm was first
written with Rust's `first_key_value()` and `last_key_value()`, and the
fix renames them `first()` and `last()`. The counts arm takes one round
of 15 fixes (among them `Vec<i32>` to `Vec[i32]`, `vec![0usize; 100001]`
to `Vec.filled(100001, 0)`, `&x` to `x`, `as usize` to `as i64`, and
`||` to `or`) and the hashed arm one round of 20 (among them `HashMap` to
`Map`, `get(&k).unwrap_or(&0)` to `get(k).unwrap_or(0)`), and both check
clean.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every prefix, and every element of it taken out, kept when the
numbers left all appear the same number of times (or none are left). 2000
cases of 2 to 20 numbers, each case drawn from 1 to 6 values, so that
counts repeat, with 1 to 5 more numbers drawn for P4.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | from 2 to the array's length |
| P3 | the numbers renamed (`x` to `100001 − 997 x`) give the same answer |
| P4 | a longer array never has a shorter answer |
| P5 | the answer's prefix works whole |
| P6 | the ★ arm's answer |

P2 holds because any two numbers work: take one out and one is left. P4
holds because a prefix of the array is a prefix of the longer one. P5
asks an arm of its answer's prefix alone, which must give that prefix's
whole length.

All 72,000 checks pass on every arm: `2000 cases: checksum 168305847,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python's brute force
for the same cases gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: one number with one extra not a shape | P1 1304, P2 395, P5 395, P6 6520 |
| S2 | ★: the length one short | P1 1568, P2 517, P5 2000, P6 7840 |
| A1 | maps: one number repeated not a shape | P1 395, P2 395, P5 395, P6 395 |
| A2 | maps: the smaller of two neighbouring counts held once | P1 665, P6 665 |
| O1 | ordered: a count of one never moved on | P1 1053, P6 1053 |
| O2 | ordered: a single number however many share count 1 | P1 508, P6 508 |
| W1 | backwards: a number taken off but still counted | a runtime error, `key not found` |
| W2 | backwards: the answer one longer | P1 2000, P2 794, P5 794, P6 2000 |
| R1 | counts: a number's old count never dropped | P1 1648, P2 395, P5 395, P6 1648 |
| R2 | counts: the top count the last number's | P1 767, P6 767 |
| H1 | hashed: the count read before the increment | P1 1509, P2 106, P5 106, P6 1509 |
| H2 | hashed: one extra top count not added | P1 1304, P2 395, P5 395, P6 1304 |

All twelve are caught. A mutation of the ★ arm fails P6 on the five
other arms, and P1, the statement read literally, catches every one but
W1, which never gets that far: a number taken off but still counted
leaves its count's tally at zero, the tally is dropped from the map, and
the next number with that count reads a key that is gone, so the
differential stops with "key not found". Four mutations (S1, A1, R1, H2)
fail P2 and P5 on the same 395 cases, where the answer falls out of
bounds and its prefix, asked alone, gives another length. S2 and
W2 answer one off every time, so P5, which asks an arm of its answer's
prefix alone, catches S2 in all 2000 cases, and P2 catches W2 wherever
its answer passes the array's end. A2, O1, O2 and R2 answer a shorter
prefix that still works, inside the bounds and whole, so only P1 and P6
see them. P3, the numbers renamed, catches none: no mutation looks at a
number's value, only at its counts. P4, a longer array never shorter,
catches none either.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, each number's count and how many numbers have each count, over 10
random arrays of 10^5 numbers drawn once, 5 passes; checksum of the
answers. Every program prints `10 arrays of 10^5 numbers, 5 passes:
lengths total 283720, checksum 994874409`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.033 to 0.054 s | 0.037 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.032 to 0.051 s | 0.035 s |
| Rust (`rustc -O`) | 0.027 to 0.043 s | 0.036 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.031 to 0.046 s | 0.034 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.031 to 0.048 s | 0.036 s |
| C (`clang -O3`) | 0.029 to 0.035 s | 0.031 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.024 to 0.038 s | 0.031 s |
| Go | 0.054 to 0.068 s | 0.060 s |
| Python | 1.954 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.034 s
against 0.035 s), and the two ranges overlap. C is about 11% ahead of
Kāra (0.031 s against 0.035 s); Go takes about 1.7x Kāra's time. Python
takes about 56x Kāra's time. No profile was taken.
