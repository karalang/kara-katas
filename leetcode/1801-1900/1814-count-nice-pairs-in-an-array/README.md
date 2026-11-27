# 1814. Count Nice Pairs in an Array

You are given an array `nums` of non-negative integers. Let `rev(x)` be
the reverse of the non-negative integer `x`: `rev(123) = 321` and
`rev(120) = 21`. A pair of indices `(i, j)` is nice if `0 <= i < j <
nums.length` and `nums[i] + rev(nums[j]) == nums[j] + rev(nums[i])`.
Return the number of nice pairs of indices, modulo `10^9 + 7`.

```
nums = [42, 11, 1, 97]       ->  2
nums = [13, 10, 35, 24, 76]  ->  4
```

**Constraints:** `1 <= nums.length <= 10^5`, `0 <= nums[i] <= 10^9`.

The arms are `fn count_nice_pairs(nums: Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `count_nice_pairs.kara` ★ | `nums[i] + rev(nums[j]) == nums[j] + rev(nums[i])` is `nums[i] - rev(nums[i]) == nums[j] - rev(nums[j])`, so each number's difference from its reverse is counted in a `Map` as the array is walked, and each number makes a nice pair with every earlier one of its difference. The reverse is built digit by digit with `%` and `/`. O(n log m) for numbers up to m |
| `count_nice_pairs_sorted.kara` | the differences collected and sorted, so equal ones stand together, and a run of `k` of them makes `k * (k - 1) / 2` pairs. O(n log n) |
| `count_nice_pairs_text.kara` | the reverse read off the number's decimal text, its chars reversed and parsed back with `i64.parse`, and the differences counted in a `SortedMap` as the ★ arm counts them. O(n log n) |
| `count_nice_pairs_tally.kara` | two passes: every difference tallied in a `Map` first, the reverse folded from the number's digits in a `Vec`, then each tally of `c` numbers adds its `c * (c - 1) / 2` pairs. O(n log m) |
| `count_nice_pairs_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<i32, i64>` of differences, the reverse through `to_string().chars().rev().collect::<String>().parse::<i32>()`, and `map.entry(n - r).or_insert(0)` read and bumped), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`2 4`); six
edges, one number, two zeros, a number and its reverse with a trailing
zero, palindromes only, the largest numbers, and five numbers of one
difference beside one of its negative (`0 1 0 10 1 10`); the
constraints' most, `10^5` equal numbers, whose `4999950000` pairs are
`999949972` modulo `10^9 + 7`, and `10^5` numbers counting up in steps
of 9973 (`the most: 999949972 98063`); and 3000 random arrays of 1 to 40
numbers, small or up to `10^9` (`3000 random arrays: checksum
223704704`). `count_nice_pairs.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, sorted and tally arms check clean as first
written. The harness was first written with Rust's `vec![42, 11, 1,
97]`; check warns that `vec![..]` is deprecated for the list literal
`[..]`, and `karac fix` rewrote the 8 of them. The text arm parsed with
`text.parse[i64]()`; Kāra has no call-site type arguments, check names
the type before the call, and `karac fix` wrote `i64.parse(text)`, 2
fixes by its count. The Rust solution takes 25 fixes by `karac fix`'s
count, and its diff is: `use std::collections::HashMap;` deleted and
`struct Solution {}` added; `Vec<i32>` to `Vec[i32]`; `HashMap<i32,
i64>` and `HashMap::new()` to `Map[i32, i64]` and `Map.new()`;
`n.to_string().chars().rev().collect::<String>().parse::<i32>()` to
`i32.parse(String.from_iter(n.to_string().chars().rev()))`; `Solution::`
to `Solution.` at the harness's 11 calls; and the harness's
`Solution.count_nice_pairs(nums) as i64` to
`Solution.count_nice_pairs(nums)`, an `i32` widening to `i64` without a
cast. `map.entry(n - r).or_insert(0)`, `ans += *e` and `*e += 1` are
Kāra as they stand. The solution takes a `Vec[i32]`, so its harness
builds its arrays as `Vec[i32]`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair `i < j` is tried, the reverse of a number read off
its decimal text, and the pair counted when `nums[i] + rev(nums[j]) ==
nums[j] + rev(nums[i])`. It runs 2000 random arrays of 1 to 12 numbers:
small numbers, numbers up to `10^9`, and numbers of two digits with up
to two zeros after them, so that many share a difference. Each arm meets
six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the array read backwards has as many nice pairs |
| P3 | a copy of the first number put at the end adds a pair for every number of its difference |
| P4 | the array twice over has `4 * pairs + n` nice pairs, as a group of `c` numbers becomes one of `2c` |
| P5 | the count is at least 0 and at most `n * (n - 1) / 2` |
| P6 | the ★ arm's answer |

Check warned once on the differential as first written, that the
solution arm's `as i64` on its `i32` result widens implicitly, and
`karac fix` took the cast off. All 60,000 checks pass on every arm:
`2000 cases: checksum 831320618, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, running the statement read literally over the
same arrays, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the reverse built from each digit's neighbour | P1 655, P3 350, P6 2620 |
| M2 | ★: no number's difference ever counted | P1 614, P3 2000, P4 2000, P6 2456 |
| M3 | sorted: each run's pairs counted twice | P1 614, P3 2000, P4 2000, P5 1, P6 614 |
| M4 | sorted: every run made to take the number after its first | P1 1791, P3 961, P4 1791, P6 1791 |
| M5 | text: the number plus its reverse taken for the difference | P1 601, P3 269, P6 601 |
| M6 | text: the number's text left unreversed | P1 1820, P3 1820, P6 1820 |
| M7 | tally: the digits read back in their own order | P1 1820, P3 1820, P6 1820 |
| M8 | tally: each tally's pairs counted with itself | P1 2000, P3 2000, P4 2000, P5 350, P6 2000 |
| M9 | solution: each number counted before it is paired | P1 2000, P3 2000, P4 2000, P5 350, P6 2000 |
| M10 | solution: each new difference started at one | P1 2000, P3 2000, P4 2000, P5 350, P6 2000 |

## Benchmarks

The bench builds one array of `10^5` numbers once, every other one below
`10^4` so that differences repeat, and makes 200 calls of the ★ arm,
each on the array's first 50000 to 99999 numbers, the count drawn from
the checksum so far. The C mirror counts in an open-addressing hash
table of the differences. It checks clean as first written. Every
implementation prints `200 calls: checksum 60609076`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.64 s against Rust's 0.69 s (0.83 s with
overflow checks on), C's 0.55 s and Go's 1.0 s; Python takes 9.6 s.
