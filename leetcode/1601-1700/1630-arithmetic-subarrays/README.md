# 1630. Arithmetic Subarrays

A sequence of numbers is called **arithmetic** if it consists of at
least two elements, and the difference between every two consecutive
elements is the same. More formally, a sequence `s` is arithmetic if and
only if `s[i+1] - s[i] == s[1] - s[0]` for all valid `i`.

You are given an array of `n` integers, `nums`, and two arrays of `m`
integers each, `l` and `r`, representing the `m` range queries, where
the `ith` query is the range `[l[i], r[i]]`. All the arrays are
**0-indexed**.

Return *a list of* `boolean` *elements* `answer`*, where* `answer[i]`
*is* `true` *if the subarray* `nums[l[i]], nums[l[i]+1], ... ,
nums[r[i]]` *can be **rearranged** to form an **arithmetic** sequence,
and* `false` *otherwise.*

```
nums = [4,6,5,9,3,7], l = [0,0,2], r = [2,3,5]  ->  [true,false,true]
nums = [-12,-9,-3,-12,-6,15,20,-25,-20,-15,-10],
l = [0,1,6,4,8,7], r = [4,4,9,7,9,10]          ->  [false,true,false,false,true,true]
```

**Constraints:** `n == nums.length`; `m == l.length`; `m == r.length`;
`2 <= n <= 500`; `1 <= m <= 500`; `0 <= l[i] < r[i] < n`;
`-10^5 <= nums[i] <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `subarrays.kara` ★ | a run can be rearranged into an arithmetic sequence exactly when it is one once sorted: each query, mapped over `l.iter().zip(r.iter())`, copies `nums[a..=b]` out, sorts it, and checks every neighbouring pair against the first pair's difference with `windows(2)`. O(m · n log n) |
| `subarrays_set.kara` | no sort: the smallest and largest fix the step, which must divide their difference into k - 1 equal parts; for a step above 0, every number must be a whole number of steps above the smallest and none may repeat, checked with a `Set[i64]`. The run is passed as a `Slice[i32]`. O(m · n) |
| `subarrays_slots.kara` | no sort and no set: the same step, and each number marks its slot `(x - smallest) / step` in a `Vec[bool]` of k slots; a number between slots or on a marked one fails the run. O(m · n) |
| `subarrays_solution.kara` | LeetCode's Rust template: each run copied into a `Vec`, sorted, and checked with an index loop. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples, a run of one
repeated number, which is arithmetic with step 0, and runs where a
repeat keeps an otherwise even spacing from being arithmetic; then the
arithmetic answers counted and a checksum for 3000 random problems of up
to 8 numbers from -2 to 2 and 6 queries, 300 of up to 500 numbers up to
`10^5` in size and 50 queries, and 20 of up to 500 numbers from -3 to 3
and 500 queries. `subarrays.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, with no sort and no arithmetic on the smallest and largest:
a run can be rearranged when some first number and some second one,
with their difference as the step, make a sequence whose numbers are the
run's, each as often. It checks 3000 random problems of 2 to 8 numbers
and 1 to 6 queries, every other one with numbers from -2 to 2, so
repeats and arithmetic runs are common, and the rest from -20 to 20.
Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | every number negated leaves the answers |
| P3 | every number x made 3x + 7 leaves the answers |
| P4 | the numbers reversed, with each query's run mirrored, leave the answers |
| P5 | each query asked alone gets the answer it got among the others |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 65079643, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P3's `3x + 7` is what catches a
divisibility test loosened to a remainder of 1 (M6): it spreads every
step by 3, so a remainder the original numbers did not show appears.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the run left unsorted | P1 181, P6 181 |
| M2 | ★: `windows(3)`, so the last pair goes unchecked | P1 1433, P2 210, P6 1433 |
| M3 | ★: `any` pair at the step, not `all` | P1 1969, P6 1969 |
| M4 | set: a step of 0 counts only for runs of two | P1 39, P6 39 |
| M5 | set: a repeat no longer fails the run | P1 405, P3 92, P6 405 |
| M6 | set: a remainder of 1 passes the divisibility test | P1 422, P3 422, P6 422 |
| M7 | slots: the smallest found with `max` | P1 1969, P6 1969 |
| M8 | slots: a marked slot may be marked again | P1 405, P3 92, P6 405 |
| M9 | template: the loop starts at the third pair | P1 1452, P2 47, P6 1452 |
| M10 | template: the run left unsorted | P1 181, P6 181 |

## Benchmarks

The bench draws 200 problems of 500 numbers and 500 queries, all of them
first: every other problem a shuffled arithmetic sequence `3i - 700`, so
long runs are sometimes arithmetic, and the rest random numbers up to
`10^5` in size. Each query is answered by the ★ arm in all five
languages, each sorting with its standard library (C with `qsort`).
Every implementation prints `200 problems of 500 numbers and 500
queries: 1363 arithmetic, checksum 662061079`. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `60902ec48` on LLVM 22:

| | median |
|---|---|
| Kāra (`karac build`) | 0.154 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.158 s |
| Rust (`rustc -O`) | 0.169 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.170 s |
| Go | 0.491 s |
| C (`clang -O3`) | 0.688 s |
| Python | 1.3 s |

Kāra is level with Rust, both well ahead of Go and C. The work is
100000 sorts of runs averaging about 125 numbers; Kāra's and Rust's
sorts are inlined and specialized to `i32`, while C's `qsort` calls its
comparator through a pointer for every comparison, so the C row here
measures `qsort` more than the algorithm.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.148 s and
0.149 s on one run).

## Verification

All four arms print the same output as `subarrays.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`60902ec48`.

## Writing it

The ★ arm as first written checked clean once `karac fix` had made
`run.windows(2).all(..)` into `run.windows(2).into_iter().all(..)`
(`windows` returns a `Vec[Slice[T]]` in Kāra, and adaptors want an
explicit iterator), and then **failed to compile**: `nums[a..=b]`, with
`a` and `b` the `ref i32` items of `l.iter().zip(r.iter())`, built MIR
that cast the reference itself to `usize` ("invalid MIR: IntToInt cast
from ref i32 to u64"). A plain `nums[a]` read the bound through; the
range did not. Kara `60902ec48` reads a range's `ref` bounds through as
well (kara `B-2026-11-19-40`), and the ★ arm is as first written.

The set and slots arms each drew one `lossless_cast` warning, an
`x as i64` where the `i32` widens by itself, which `karac fix` removed.
LeetCode's Rust template takes one `karac fix` of 14 edits:
`struct Solution {}`, the `Vec<..>` types to `Vec[..]`,
`Vec::with_capacity` to `Vec.with_capacity`, `sort_unstable()` to
`sort()`, and `Solution::` to `Solution.`; its `l[i] as usize..=r[i] as
usize` range stays. It then checks and agrees with no hand edit.
