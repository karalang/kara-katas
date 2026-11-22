# 2818. Apply Operations to Maximize Score

You are given an array `nums` of `n` positive integers and an integer
`k`.

Initially, you start with a score of `1`. You have to maximize your
score by applying the following operation at most `k` times:

- Choose any **non-empty** subarray `nums[l, ..., r]` that you haven't
  chosen previously.
- Choose an element `x` of `nums[l, ..., r]` with the highest **prime
  score**. If multiple such elements exist, choose the one with the
  smallest index.
- Multiply your score by `x`.

Here, `nums[l, ..., r]` denotes the subarray of `nums` starting at index
`l` and ending at the index `r`, both ends being inclusive.

The **prime score** of an integer `x` is equal to the number of
distinct prime factors of `x`. For example, the prime score of `300` is
`3` since `300 = 2 * 2 * 3 * 5 * 5`.

Return *the **maximum possible score** after applying at most `k`
operations*. Since the answer may be large, return it modulo
`10^9 + 7`.

```
nums = [8,3,9,3,8],        k = 2  ->  81
nums = [19,12,14,6,10,18], k = 3  ->  4788
```

**Constraints:** `1 <= nums.length == n <= 10^5`; `1 <= nums[i] <=
10^5`; `1 <= k <= min(n * (n + 1) / 2, 10^9)`.

## Approaches

Each number rules the subarrays in which it is the one chosen: those
reaching back no further than the last number whose score is at least
its own, and on no further than the first number whose score is above
it, `(i - left) * (right - i)` of them. The best score takes the
largest numbers first, each as often as it rules, until k runs out.

| file | mechanism |
|---|---|
| `score.kara` ★ | a sieve adding 1 to every multiple of each prime for the prime scores, one monotonic stack giving each index both ends of its stretch as indices are popped and pushed, the indices sorted by `sort_by_key` on the negated value, and each power by squaring |
| `score_walk.kara` | each prime score by trial division, each stretch found by walking out from the index, left past lower scores and right past scores at most its own, the counts summed by value in a `SortedMap`, read largest first by `iter().rev()`; O(n^2) at worst |
| `score_split.kara` | a smallest-prime-factor sieve; a stretch's first index of highest score rules every subarray of the stretch that holds it, and the stretches either side of it are split the same way, recursively; the (value, count) pairs sorted, and each power by recursive squaring |
| `score_heap.kara` | the sieve by `step_by`; one stack walked back for the next score above each index, another forward for the last score at least its own, and every (value, count) pair in a max-first `PriorityQueue`, popped while k lasts |
| `score_solution.kara` | a Rust solution as LeetCode's Rust users write it: an `omega` sieve, one stack of `usize` indices filling `left` and `right` as `i32`, the indices sorted by `sort_by` on `nums[b].cmp(&nums[a])`, and a `pow(mut b, mut e, m)` by squaring, the values `i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; a single
1; [2, 30, 6, 7] with k every subarray; 2000 primes in a cycle of six,
every score 1, with k every subarray; 2000 numbers in six runs of
falling score; then 3000 random arrays of 1 to 10 numbers up to 100
with k up to the count of subarrays, and 50 of up to 2000 numbers up to
10^5 with k up to 10^9, the last two as checksums. `score.py` mirrors
the ★ arm and its output is byte-identical.

```
81
4788
1
415997431
543528290
23784103
3000 small arrays: checksum 74166742
50 large arrays: checksum 424612184
```

The harness first gave the cycle of primes k = 10^9, more than its
2,001,000 subarrays and outside the constraints; the heap arm, which
pops while k lasts, ran its queue dry and failed on `unwrap()` of an
empty pop, where the other arms stop at the last number. The case now
takes every subarray, as the constraint allows.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every subarray, the first of its numbers of highest
prime score, each score counted by asking every p from 2 to v whether
it is a prime dividing v; the chosen numbers sorted largest first and
the first k multiplied. It draws 2000 random arrays of 1 to 10 numbers
up to 100 with k up to the count of subarrays, then 50 of up to 400
numbers up to 10^5 with k up to the count, all before any arm answers;
the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 numbers, the answer is the literal reading's |
| P2 | one operation more, below every subarray: the answer times some number of the array |
| P3 | every subarray walked from each start with the best index carried, scores by trial division: the same answer |
| P4 | between 1 and 10^9 + 6, a product of numbers from 1 up under a prime modulus |
| P5 | k = 1: the largest number |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 414078245, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the stretch stopped at an equal score on the left | P1 1287, P3 1334, P6 1334 |
| M2 | ★: the numbers taken smallest first | P1 1612, P3 1660, P5 1823, P6 1660 |
| M3 | walk: the walk right only past lower scores | P1 1232, P2 665, P3 1279, P6 1279 |
| M4 | walk: a prime past the square root not counted | P1 681, P3 720, P6 720 |
| M5 | split: the last number of highest score taken | P1 1287, P3 1334, P6 1334 |
| M6 | split: the stretch right of the ruler never split | P1 1441, P2 857, P3 1488, P5 1157, P6 1488 |
| M7 | heap: the reach right stopped at an equal score | killed under both: runtime error: called unwrap() on None |
| M8 | heap: the subarrays counted by the left reach alone | killed under both: runtime error: called unwrap() on None |
| M9 | solution: the wrong bit of the exponent read | P1 1998, P2 844, P3 2048, P5 2048, P6 2048 |
| M10 | solution: the indices sorted smallest first | P1 1612, P3 1660, P5 1823, P6 1660 |

## Benchmarks

The bench draws 20 arrays of 10^5 numbers up to 10^5, LeetCode's most,
each with k up to 10^9, all of them first, then answers each 3 times by
the ★ arm in all five languages, the sieve rebuilt for every answer as
the arm does. C sorts by `qsort` and Go by `slices.SortFunc`; Rust's
`sort_by_key` is stable, as Kāra's is, and no answer depends on the
order of equal numbers. Every implementation prints `20 arrays of
100000, 3 rounds: scores sum to 22906882461, checksum 35189091`.

BENCHTAB

## Verification

All five arms print the same output as `score.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 37 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `vec![x; n]` became `Vec.filled(n, x)`; `as usize`
became `as i64`, and the casts on the indices into `omega` and on `i`,
`left[i]` and `right[i]` in the count went, the `i32` values widening
implicitly; `Some(&t) = st.last()` became `Some(t) = st.last().cloned()`;
`|&a, &b|` lost its `&`s and `cmp(&nums[a])` its borrow; `Self::pow`
became `Solution.pow`; the `mut b` and `mut e` parameters became `let
mut` rebindings at the top of the body; and the wrapper's `as i64` went.
