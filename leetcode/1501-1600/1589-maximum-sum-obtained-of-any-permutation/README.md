# 1589. Maximum Sum Obtained of Any Permutation

We have an array of integers, `nums`, and an array of `requests` where
`requests[i] = [start_i, end_i]`. The `i`-th request asks for the sum of
`nums[start_i] + nums[start_i + 1] + ... + nums[end_i - 1] + nums[end_i]`.
Both `start_i` and `end_i` are 0-indexed.

Return the maximum total sum of all requests among all permutations of
`nums`. Since the answer may be too large, return it modulo `10^9 + 7`.

```
nums = [1,2,3,4,5],    requests = [[1,3],[0,1]]        ->  19
nums = [1,2,3,4,5,6],  requests = [[0,1]]              ->  11
nums = [1,2,3,4,5,10], requests = [[0,2],[1,3],[1,1]]  ->  47
```

**Constraints:** `n == nums.length`; `1 <= n <= 10^5`;
`0 <= nums[i] <= 10^5`; `1 <= requests.length <= 10^5`;
`requests[i].length == 2`; `0 <= start_i <= end_i < n`.

## Approaches

The total is each place's value times how many requests cover it, so the
largest value belongs at the most covered place: sort the counts and the
values and multiply them in pairs.

| file | mechanism |
|---|---|
| `max_sum.kara` ★ | the counts by a difference array and its running sum, both lists sorted and multiplied in pairs under the modulus. O(n log n + m) |
| `max_sum_counts.kara` | no comparison sort: how many places have each count and how many copies of each value, both as tallies in `Vec.filled`, walked from the top in runs. O(n + m + max value) |
| `max_sum_sorted.kara` | each request as two events in a `SortedMap` from place to change, swept into runs of equal count, the runs tallied in a second `SortedMap` from count to places and walked from the largest with `iter().rev()`, the values sorted largest first by `sort_by`. O((n + m) log n) |
| `max_sum_solution.kara` | LeetCode's Rust template (a `vec![0i64; n + 1]` difference array, `sort_unstable`, `zip` and `fold` under the modulus, `as usize` indices), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (one value asked twice, zeros, and 100000 values of 100000 asked
whole three times, which wraps the modulus), then a checksum for 3000
random problems of up to 8 values up to 9 and 5 requests, 300 of up to
1000 values up to 100000 and 1000 requests, and 3 of up to 100000 of
each. `max_sum.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every permutation of the values, in lexicographic order of
their places, each request's sum added up, the largest total kept. It
checks 3000 problems of 1 to 6 values from 0 to 9 and 1 to 5 requests,
each with a shuffle of its values drawn for P3, every random choice drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the requests in reverse order leave the answer |
| P3 | the values shuffled leave the answer |
| P4 | every request mirrored (place `i` made `n - 1 - i`) leaves the answer |
| P5 | every value doubled doubles the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 683427730, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

One first choice was replaced: stopping the counts arm's walk one count
early indexed past the tallies and was killed only by a panic.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the request's end place not covered | P1 2903, P6 2903 |
| M2 | ★: the values sorted largest first, paired against counts smallest first | P1 2224, P6 2224 |
| M3 | ★: the running sum starts one place late | P1 1829, P4 1731, P6 1829 |
| M4 | counts: a run takes every place left, not as many as there are values | P1 1700, P6 1700 |
| M5 | counts: a run's count left out of its product | P1 2283, P6 2283 |
| M6 | counts: each place's count read before its own change | P1 2051, P4 1739, P6 2051 |
| M7 | sorted: places covered once left out of the runs | P1 1674, P6 1674 |
| M8 | sorted: the runs walked from the smallest count | P1 1674, P6 1674 |
| M9 | template: the end of a request never closed | P1 1903, P4 1869, P6 1903 |
| M10 | template: the place-0 count dropped, not the one past the end | P1 2264, P4 1598, P6 2264 |

## Benchmarks

The bench runs the ★ arm on 20 problems of 100000 values and 100000
requests, all drawn first, in all five languages. Every implementation
prints `20 problems of 100000 values and 100000 requests: checksum
932753250`. In the C mirror each request is its own malloc and the sorts
are `qsort`'s.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.241 s |
| Kāra (`karac build`) | 0.246 s |
| Rust (`rustc -O`) | 0.251 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.262 s |
| C (`clang -O3`) | 0.482 s |
| Go | 0.764 s |
| Python | 5.0 s |

C trails here because its mirror sorts with `qsort`, through a
comparison function called for every pair, where Kāra, Rust and Go sort
with the comparison compiled in.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is below its real time (0.171 s and 0.227 s on one run).

## Verification

All four arms print the same output as `max_sum.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The counts arm was written in Kāra and checked as written. The ★ arm
wrote `*count * *v as i64` and the harness `max_sum_range_query(..) as
i64`, and the sorted arm `(*place).min(n) as i64 - from as i64` and
`*c * values[next] as i64`; `karac fix` dropped each cast, as an `i32`
widens to `i64` by itself.

The Rust template took five rounds of `karac fix`:

1. `struct Solution;` to `struct Solution {}`, the `Vec<..>` types to
   `Vec[..]`, `for r in &requests` to `for r in ref requests`, the
   closure's `(&f, &x)` pattern to `(f, x)`, and `Solution::` to
   `Solution.`;
2. `vec![0i64; n + 1]` to `vec![0; n + 1]`, both `sort_unstable()` to
   `sort()`, and `fold(0i64, ..)` to `fold(0, ..)`;
3. the `vec!` to `Vec.filled(n + 1, 0)`, and `nums` made `own Vec[i32]`,
   since `let mut nums = nums` sorts it in place;
4. the wrapper's `nums` made `own` too;
5. the harness call given `nums.clone()`, as the harness only borrows
   its examples.

It then checks and agrees with no hand edit. The template's harness is
the one line that differs from the other arms'; the differential clones
for it the same way.
