# 1296. Divide Array in Sets of K Consecutive Numbers

Given an array of integers `nums` and a positive integer `k`, check
whether it is possible to divide this array into sets of `k` consecutive
numbers.

Return `true` if it is possible. Otherwise, return `false`.

```
nums = [1,2,3,3,4,4,5,6], k = 4              ->  true    [1,2,3,4] and [3,4,5,6]
nums = [3,2,1,2,3,4,3,4,5,9,10,11], k = 3    ->  true
nums = [1,2,3,4], k = 3                      ->  false
```

**Constraints:** `1 <= k <= nums.length <= 10^5`, `1 <= nums[i] <= 10^9`.

The arms are `fn is_possible_divide(nums: Vec[i64], k: i64) -> bool`.

## Approaches

The smallest number left must start a set, since nothing smaller is left
to come before it; every arm but the literal one in the differential
rests on that.

| file | mechanism |
|---|---|
| `is_possible_divide.kara` ★ | the numbers counted in a `SortedMap` with `*count.entry(x).or_insert(0) += 1`; walking the keys in order, each count still left starts that many sets, taken from the next k - 1 numbers' counts. O(n log n) |
| `is_possible_divide_sort.kara` | the numbers sorted and counted in a `Map`; each number in order that still has a count starts one set, taking one from each of the next k - 1 numbers. O(n log n + nk) |
| `is_possible_divide_heap.kara` | the numbers in a `PriorityQueue`, smallest first; each set starts at the smallest left and pops its way up, a repeat of the number just taken set aside and pushed back after. O(n log n) |
| `is_possible_divide_open.kara` | one pass over the sorted distinct numbers with their counts, keeping how many sets were opened at each of the last k numbers in a `VecDeque`; a number must continue every set still open, its extra count opens new ones, and they close k numbers later. O(n log n) |
| `is_possible_divide_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `BTreeMap<i32, i32>` filled by `*map.entry(x).or_insert(0) += 1`, then `while let Some((&first, _)) = map.iter().next()` taking one set at a time, each count lowered through `get_mut` and removed at 0), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, k of 1, k
of the whole array, two pairs with a gap between them, and two runs that
overlap (`true true false true true true true`); then 3000 random arrays
of up to 40 runs of up to 8 consecutive numbers, their starts spread up
to 10, 100 or `10^9`, shuffled, and half of them with one number moved
by one (`3000 random arrays: 1719 divide, checksum 471045591`).
`is_possible_divide.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, sort and heap arms checked clean as first written.
The open arm wrote Rust's `match runs.last_mut() { Some(last) if last.0
== x => last.1 += 1, _ => runs.push((x, 1)) }`; Kāra's `Vec` has no
`last_mut`, and `E0236` said to write through an index after checking the
vector is not empty, which `karac fix` did (1 fix): `if runs.len() > 0
and runs[runs.len() - 1].0 == x { runs[runs.len() - 1].1 += 1; } else {
runs.push((x, 1)); }`. The fix wrote the `else` block on one line, and it
is laid out here as `karac fmt` lays it out. The Rust arm takes one round
of 17 fixes by `karac fix`'s count, from 12 errors: the `use
std::collections::BTreeMap;` line deleted and `BTreeMap::new()` to
`SortedMap.new()`, `Vec<..>` to `Vec[..]`, `struct Solution;` to `struct
Solution {}`, `::` to `.`, `for &x in &nums` to `for x in ref nums`, the
`(&first, _)` pattern to `(first, _)`, `get_mut(&v)` and `remove(&v)` to
`get_mut(v)` and `remove(v)`, `nums.len() % k as usize` to `nums.len() %
k`, and the wrapper's `|&x|` to `|x|`. Its output matches on the first
run. No correctness gap was met; the ★ arm's `SortedMap` is slow
compiled, below.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the first number not yet in a set goes into some set of k
consecutive numbers that contains it, starting anywhere from k - 1 below
it to itself, made of numbers not yet in a set; every such choice is
tried, and the division is possible when one of them leaves every number
in a set. 2000 arrays of up to 12 numbers in four kinds, 500 each: runs
of k from starts within 6, shuffled; the same with one number moved by
one; any numbers up to 8; and runs with one number more. k is 1 to 4.
Every array, k, shift and run is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed: the same answer |
| P3 | every number moved up by the same amount: the same answer |
| P4 | every number mirrored, x to `max + 1 - x`: the same answer |
| P5 | one more run of k consecutive numbers appended: the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 arrays: checksum 929412278,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Thirteen edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. Three are left out: two change
nothing (the ★ arm taking a count short of the sets it must start as
enough, and the sort arm taking from a count of 0, are each caught at
the next number, where the count left is below 0), and one, the heap arm
closing each set a number short, fails exactly as the sort arm's does.
The ten kept, two to each arm, are each killed, fail the same way under
both backends and not by a crash, and no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one set started from each number, whatever its count | P1 391, P6 1564 |
| M2 | ★: one taken from each count, not one per set | P1 125, P4 12, P5 60, P6 500 |
| M3 | sort: each set one short | P1 437, P5 116, P6 437 |
| M4 | sort: a used-up number starting a set | P1 391, P6 391 |
| M5 | heap: a repeat set aside and lost | P1 217, P4 136, P5 159, P6 217 |
| M6 | heap: a gap in a set accepted | P1 276, P4 251, P5 152, P6 276 |
| M7 | open: a number allowed one fewer than the sets open | P1 9, P4 14, P5 8, P6 9 |
| M8 | open: sets still open at the end allowed | P1 59, P4 123, P5 42, P6 59 |
| M9 | solution: a count of 1 removed with its key | P1 138, P5 182, P6 138 |
| M10 | solution: a missing number passed over | P1 512, P6 512 |

P1 and P6 kill all ten, P5 seven and P4 five; P2 and P3 kill none. Every
arm counts or sorts first, so the order of the array (P2) cannot reach
any of these edits, and none of them depends on where the numbers sit
on the number line (P3). P4, the mirror, turns a set's last number into
its first, so it catches the edits that treat the two ends of a set
differently.

## Benchmarks

The bench builds 20 arrays of 16666 runs of 6 consecutive numbers,
99996 numbers each, near the constraints' longest, starts up to `10^4`
in half of them, so that runs overlap, and up to `10^9` in the other
half, shuffled, once from its own generator; then makes 10 passes, each
swapping two numbers of every array and choosing k from 1 to 6 from the
checksum so far, so no answer carries over, answering it with the ★ arm
and folding the answer plus the pass into the checksum. The counts are a
`SortedMap` in Kāra and a `BTreeMap` in Rust; Go and Python have no
sorted map and sort the counts' keys once per call, and C sorts a copy
of the array and finds each later number's run by binary search. Every
implementation prints `10 passes over 20 arrays of 99996: checksum
27707363`.

The compiled Kāra program took about twice Rust's time in a first run
(8.7 s against 4.3 s, with a gate running beside it). A microbench of
the counting alone, `10^5` random keys into a fresh map 100 times, takes
about 3.4 times Rust's `BTreeMap` with `entry(x).or_insert(0) += 1` and
2.8 times with a plain `insert(x, 1)`: the cost is in the `SortedMap`'s
tree, kara B-2026-11-24-41.

BENCHTAB
