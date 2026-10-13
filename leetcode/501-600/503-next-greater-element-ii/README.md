# 503. Next Greater Element II

Given a circular integer array `nums` (i.e., the next element of
`nums[nums.length - 1]` is `nums[0]`), return the next greater number
for every element in `nums`.

The next greater number of a number `x` is the first greater number to
its traversing-order next in the array, which means you could search
circularly to find its next greater number. If it doesn't exist, return
`-1` for this number.

```
nums = [1,2,1]      ->  [2,-1,2]
nums = [1,2,3,4,3]  ->  [2,3,4,-1,4]
```

**Constraints:** `1 <= nums.length <= 10^4`; `-10^9 <= nums[i] <= 10^9`.

## Approaches

Every arm is `fn next_greater_elements(nums: Vec[i64]) -> Vec[i64]`.

| file | mechanism |
|---|---|
| `next_greater_elements.kara` ★ | walk the array twice, index `i % n`, with a stack of the indices still waiting for a greater number; each number answers every waiting index below it (`while let Some(top) = waiting.last()`), and indices are pushed only on the first lap. O(n) |
| `next_greater_elements_brute.kara` | for each number, look at the next `n - 1` around the circle and take the first greater one. O(n^2) |
| `next_greater_elements_backward.kara` | walk the circle backward twice, `(0..2 * n).rev()`, with a stack of candidate values: every candidate not greater than the current number is popped, and on the second lap the top is the answer. O(n) |
| `next_greater_elements_doubled.kara` | make the circle a line: `doubled = nums.clone()` and `doubled.extend(nums.iter().cloned())`, then the usual backward stack over the `2n` numbers and `next.truncate(n)`. O(n) |
| `differential.kara` | the four arms on 1,500 random arrays, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, one
number, all equal, falling, rising, the extremes of the range, the
largest number twice, and for 300 random arrays of 1 to 30 numbers
(from 0 to 9, or from the whole range, in turn) the count of numbers,
how many have a greater one, and a checksum of the answers.
`next_greater_elements.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random arrays of 1 to 25 numbers, from 0 to 2, from 0 to 9, or
from the whole range -10^9 to 10^9, in turn.

| | property |
|---|---|
| P1 | the answers are the reference's, which walks each number's steps 1 to n - 1 around the circle for the nearest greater one |
| P2 | rotating the array rotates the answers |
| P3 | a number's answer is -1 when it is the largest, else greater than it |
| P4 | doubling every number doubles every answer |
| P5 | the array written twice answers twice |

As written, the doubled arm is refused by `karac check` and every
backend (see Compiler findings), and so is the differential, which
holds a copy of it. It was run on a copy that writes the doubled arm's
second half as `doubled.extend(nums.clone())`. That copy prints `1500
cases, 4 arms, 30000 checks, 0 failures` under `karac __mir-run`. The
files here keep the spec's spelling, and should pass as they stand once
the row is fixed.

## Mutation testing

Ten edits to the copy of `differential.kara`, two to each arm and two
equivalent ones, each run under `karac __mir-run`. All eight
non-equivalent ones are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal number answers a waiting one (`>` for `>=`) | P1 1500, P3 1500, P4 1500 |
| M2 | ★: one lap, no wrap-around (`0..n`) | P1 1119, P2 1197, P3 1045, P4 1119, P5 1119 |
| M3 | brute: the last step is not tried (`1..n - 1`) | P1 154, P3 129, P4 154, P5 154 |
| M4 | brute: an equal number answers (`>=` for `>`) | P1 881, P3 881, P4 683, P5 817 |
| M5 | backward: equal candidates are kept (`< x` for `<= x`) | P1 1500, P3 1500, P4 1500 |
| M6 | backward: one lap, no wrap-around (`(0..n).rev()`) | P1 1119, P2 1197, P3 1045, P4 1119, P5 1119 |
| M7 | doubled: an equal number stays on the stack (`>=` for `>`) | P1 1500, P3 1500, P4 1500 |
| M8 | doubled: no `truncate`, so `2n` answers | P1 1500, P2 1500, P3 1500, P4 1500, P5 1119 |
| E1 | backward: the walk starts at `2n - 2` (`(0..2 * n - 1).rev()`) | 0 |
| E2 | brute: step `n` is tried too (`1..=n`) | 0 |

E1 is equivalent because the number at `2n - 1` is the last one, and
it matters only to the number before it on the second lap, index
`n - 1`, whose `n - 1` steps around the circle end at index `2n - 2`.
E2 is equivalent because step `n` lands on the number itself, which is
never greater than itself.

M1, M5 and M7 are one wrong rule, "an equal number counts as greater",
written into three arms, and fail every case: each number meets itself
one lap later, so it is always answered, the largest by itself, where
it must get -1. M2 and M6 are the same lap missing from two arms:
both give the answers of a line, not a circle, so they fail the same
cases. M3 passes P2 because missing the last step is missing it from
every rotation alike, and M1, M5 and M7 pass P2 and P5 for the same
reason: the rule is wrong the same way on every rotation and on the
array written twice. M8 gives `2n` answers, which P1 to P4
reject in every case.

## Verification

The ★, brute and backward arms print the same output as
`next_greater_elements.py` under `karac __mir-run` (the v2 MIR
interpreter) and `karac __mir-llvm-run`, and run clean under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output
identical, no error, no leak. So do the copies of the doubled arm and
the differential described under Differential. `karac check` passes on
the ★, brute and backward arms and the bench program, and refuses the
doubled arm and the differential (see Compiler findings).

On the frozen legacy backends, `karac run --interp` prints the same
output for the ★, brute and backward arms, but LLJIT and legacy `karac
build` fail on all three at codegen: "Module verification failed: Call
parameter type does not match function signature!", at the harness's
calls to `show`, whose first parameter is a `Str` given a string
literal (as in katas 501 and 502). The doubled arm and the differential
are refused on legacy as on v2. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It builds 120 arrays of 10,000
numbers (the problem's most) once, from 0 to 9, from the whole range
-10^9 to 10^9, or falling, in turn. Then it solves each array 100 times,
folding the sum of the answers into a checksum. Every implementation
prints `120 arrays of 10000 numbers, 100 times each: 116010000 with a
greater one, checksum 788858582`, the Kāra program under `karac
__mir-run` included (in 440 s).

Every mirror allocates a fresh answer array and a fresh index stack for
each call, as the ★ arm's `vec![-1; n]` and `Vec.new()` are fresh Vecs:
Rust `vec!` and `Vec::new()`, Go `make` and `append`, Python lists, and
C two `malloc`'d arrays. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.23 to 1.36 s |
| Rust (`rustc -O`) | 1.53 to 1.57 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.59 to 1.64 s |
| Go | 2.36 to 2.43 s |
| Python | 30.5 to 30.9 s |
| Kāra (`karac build --mir`) | 1.60 to 1.79 s |

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `all[c]` in the call to `next_greater_elements`,
which v2 reads as a borrow. So `bench.sh` builds the Kāra program with
`karac build --mir`, the v2 compiled backend. That edit is by hand, on
top of the `scripts/new-bench.sh` output. The `--mir` row is timed at
kara `486f47f97d`. Under `karac __mir-llvm-run` the program prints the
same line in 4.2 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

kara B-2026-10-13-19 (missing-feature, open): `Vec.extend` accepts only
a `Vec`, `Slice` or `Array`. The spec gives `fn extend[I:
IntoIterator[Item = T]](mut ref self, items: own I)`
(docs/library/collections.md), and `cloned` is the spec's way to get
owned copies of viewed items, so the doubled arm appends the second
copy with `doubled.extend(nums.iter().cloned())`. `karac check`, `karac
run --interp` and both v2 backends refuse it with "no method 'extend'
on type 'Vec'", which names the method as missing where the refusal is
the argument's type. `doubled.extend(nums.clone())` passes and runs, at
the cost of copying the whole `Vec` first. So the doubled arm, and the
differential with it, runs on no backend as written.
