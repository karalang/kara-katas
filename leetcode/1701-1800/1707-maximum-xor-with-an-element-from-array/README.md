# 1707. Maximum XOR With an Element From Array

You are given an array `nums` consisting of non-negative integers. You
are also given a `queries` array, where `queries[i] = [xi, mi]`.

The answer to the `ith` query is the maximum bitwise `XOR` value of `xi`
and any element of `nums` that does not exceed `mi`. In other words, the
answer is `max(nums[j] XOR xi)` for all `j` such that `nums[j] <= mi`.
If all elements in `nums` are larger than `mi`, then the answer is `-1`.

Return *an integer array* `answer` *where* `answer.length ==
queries.length` *and* `answer[i]` *is the answer to the* `ith` *query.*

```
nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]          ->  [3,3,7]
nums = [5,2,4,6,6,3], queries = [[12,4],[8,1],[6,3]]       ->  [15,-1,5]
```

**Constraints:** `1 <= nums.length, queries.length <= 10^5`;
`queries[i].length == 2`; `0 <= nums[j], xi, mi <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `xor.kara` ★ | the queries answered offline: the values sorted, the queries taken in order of their limit, and before each one every value up to m put into a 30-bit binary trie, a `Vec[Array[i64, 2]]` of children; the query walks down taking the other bit wherever it can. O((n + q) * 30) after the sorts |
| `xor_online.kara` | one trie of all the values, built at once, whose every node, a `struct`, keeps the smallest value below it; a query walks down taking the other bit where that child holds a value no larger than m, and answers in its own order. O((n + q) * 30) |
| `xor_ranges.kara` | no trie: the answer's bits chosen highest first, the values starting with the bits chosen so far being one stretch of the sorted values, and each half of it, the one with x's other bit first, tried by `partition_point` for a value no larger than m. O(n log n + q * 30 * log n) |
| `xor_solution.kara` | a Rust solution as LeetCode's Rust users write it, the offline trie as a `Vec<[usize; 2]>`, `mut nums` sorted in place by `sort_unstable`, and the queries by `sort_unstable_by_key` on an index list, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

The answers print as a list. Every arm prints the same 7 lines:
LeetCode's two examples, no value small enough, and the largest values;
then the answers summed and a checksum for 3000 random problems of up to
8 values and 8 queries below 16, 300 of up to 1000 below `10^9`, and 3 of
up to `10^5`, LeetCode's largest. `xor.py` mirrors the ★ arm and its
output is byte-identical.

```
[3, 3, 7]
[15, -1, 5]
[-1, -1]
[610612735]
3000 problems of up to 8 values below 16: answers sum to 105281, checksum 275379831
300 problems of up to 1000 values below 1000000000: answers sum to 111506949462541, checksum 888836732
3 problems of up to 100000 values below 1000000000: answers sum to 130822038185179, checksum 760327025
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each query, every value of `nums` that does not exceed m,
XORed with x, the largest kept, -1 when none is small enough. It checks
3000 random problems of 1 to 6 values and 1 to 6 queries, every number
below 32. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values in reverse order give the same answers |
| P3 | a value above every limit added changes nothing |
| P4 | every answer but -1 is x XOR some value no larger than m |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 312239319, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M10 was a contrived shift
chain and was replaced by a plain one. P3 sees only M4, the online trie
that stops checking each child's smallest value: a large value then
lures the walk into a branch it cannot finish within m.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: values equal to the limit left out | P1 550, P5 550 |
| M2 | ★: only the low 4 bits put in the trie | P1 2709, P4 2709, P5 2709 |
| M3 | ★: a query with no value small enough answered 0 | P1 1390, P4 1390, P5 1390 |
| M4 | online: a child taken whatever its smallest value | P1 1515, P3 2723, P4 1515, P5 1515 |
| M5 | online: each node's smallest overwritten by the last value | P1 537, P2 824, P4 311, P5 537 |
| M6 | online: the same bit as x sought, not the other | P1 2723, P4 2723, P5 2723 |
| M7 | ranges: a half's end taken in | P1 1989, P4 1989, P5 1989 |
| M8 | ranges: the half's first value itself skipped | P1 2404, P4 2199, P5 2404 |
| M9 | solution: values one above the limit let in | P1 543, P4 543, P5 543 |
| M10 | solution: each bit found overwriting the ones before | P1 2654, P4 2622, P5 2654 |

## Benchmarks

The bench draws 4 random problems of `10^5` values and `10^5` queries,
LeetCode's largest, every number below `10^9`, all of them first, then
answers each 3 times by the ★ arm in all five languages; C sorts with
`qsort` and builds its trie in one block of n * 30 + 1 nodes, the
others grow theirs as Kāra does. Every implementation prints `4 problems
of 100000 values and 100000 queries, 3 rounds: answers sum to
941597942112732, checksum 999170334`. The C build also runs clean under
gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.815 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.830 s |
| Rust (`rustc -O`) | 0.882 s |
| Kāra (`karac build`) | 0.900 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.917 s |
| Go | 2.606 s |
| Python | 19 s |

The sequential Kāra build takes 1.04x Rust's time and 1.10x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.815 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.705 s and 0.836 s on one
run).

## Verification

All four arms print the same output as `xor.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★, online and ranges arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 29 edits. `mut nums:
Vec<i32>` became `nums: own Vec[i32]` with `let mut nums = nums;` at the
body's start, and the harness's wrapper, which hands its vector on, took
it `own` too. `sort_unstable` and `sort_unstable_by_key` became `sort`
and `sort_by_key`; every `Vec<..>` was written in brackets, `[usize; 2]`
as `Array[i64, 2]`, and `vec![[0, 0]]` and `vec![-1; queries.len()]` as a
list literal and `Vec.filled`; `usize` became `i64` throughout, in the
index list and in the `as usize` of each bit; `|&i|` and `for &i in
&idx` dropped their `&`s, the loop borrowing `ref idx`; and `&&` became
`and`.

The differential's P4 first cast each XOR `as i64` to compare it with an
answer; the `lossless_cast` lint saw that `i32` widens by itself there,
and `karac fix` dropped the cast. `arm_name` indexes a list of string
literals for a `Str`, as #1662's does (B-2026-11-19-131).
