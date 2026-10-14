# 581. Shortest Unsorted Continuous Subarray

Given an integer array `nums`, you need to find one continuous subarray
such that if you only sort this subarray in non-decreasing order, then
the whole array will be sorted in non-decreasing order. Return the
shortest such subarray and output its length.

```
nums = [2,6,4,8,10,9,15]  ->  5   (sort [6,4,8,10,9])
nums = [1,2,3,4]          ->  0
nums = [1]                ->  0
```

**Constraints:** `1 <= nums.length <= 10^4`; `-10^5 <= nums[i] <= 10^5`.

## Approaches

Every arm is `fn find_unsorted_subarray(nums: Vec[i64]) -> i64`.

| file | mechanism |
|---|---|
| `find_unsorted_subarray.kara` ★ | two sweeps: left to right, the last place below the largest value so far is the end; right to left, the last place above the smallest so far is the start; O(n), O(1) space |
| `find_unsorted_subarray_sorted.kara` | a sorted copy; the subarray runs from the first place that differs from it to the last; O(n log n) |
| `find_unsorted_subarray_stack.kara` | a stack of positions with rising values: each value pops the larger ones above it, and the leftmost popped is the start; a falling stack from the right gives the end; O(n) |
| `find_unsorted_subarray_widen.kara` | the first fall from the left and the first rise from the right bound a middle out of order; its smallest and largest values, `*nums[left..=right].iter().min().unwrap()` and `max`, push the bounds out past every value they must pass; O(n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 16 lines: twelve arrays at the edges (the
three examples, two values out of order, all equal, falling, the ends of
the range, equal values at the edge of the subarray, inside it and
outside it, and a small value late or a large one early that stretches
the subarray to an end), a total and checksum over 300 random arrays of
1 to 30 values, sorted and then 0 to 3 pairs swapped, and the problem's
largest, 10,000 values in order but for the two ends swapped, in order
but for two neighbours in the middle, and falling.
`find_unsorted_subarray.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every stretch of every length from the
shortest up is sorted in a copy of the array, and the first length whose
copy comes out in order is the answer, 0 for an array already in order.
Each arm is held to the properties below on 1,000 random arrays of 1 to
8 values from -3 to 3, now and then an end of the range, every other one
sorted first and then one pair swapped.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the array sorted gives 0, and the answer is 0 only when the array is in order |
| P3 | the array reversed with every value negated gives the same answer |
| P4 | a value at most the smallest put in front and one at least the largest put at the end change nothing |
| P5 | a value below every other put at the end makes the whole array the answer |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value equal to the largest counted out of place | P1 197, P2 555, P3 237, P4 389 |
| M2 | ★: the largest never updated | P1 282, P2 225, P3 309, P4 482 |
| M3 | sorted: the copy sorted falling | P1 735, P2 865, P4 1000, P5 1000 |
| M4 | sorted: the last place never compared | P1 464, P3 345, P4 464, P5 1000 |
| M5 | stack: equal values popped | P1 106, P3 180, P4 268 |
| M6 | stack: the end set to the last place popped | P1 381, P3 228, P5 707 |
| M7 | widen: the start pushed past values equal to the smallest | P1 76, P3 126, P4 193 |
| M8 | widen: the end pushed one place at most | P1 40, P3 73 |
| E1 | ★: the right sweep starting at the last place | 0 |
| E2 | sorted: the comparison written the other way round | 0 |
| E3 | stack: a new stack for the second sweep | 0 |
| E4 | widen: the first fall tested by its negation | 0 |

Equal values are where three of the mutants go wrong: M1, M5 and M7 each
treat a value equal to its neighbour as out of place, so they answer
more than they should; P4 puts values at the ends that can equal values
already there, which is how it catches them. M8 is wrong only when the
end must move more than one place, and only P1 and P3 see it: P3 turns
the array round, so the end the mutant gets wrong becomes the start,
which it widens correctly. M3 and M4 fail P5 on every case, since a
value below all the others put at the end must reach the front of the
sorted copy, and M3's falling copy and M4's skipped last place both miss
it.

One edit meant as a mutant turned out safe: leaving the first sweep's
stack in place for the stack arm's second sweep. What is left on it are
the positions whose value is no larger than any after them, and the
second sweep pops one only when a value before it is larger, which puts
that position inside the subarray anyway. It was replaced by M6. E1 is
safe because the last value is never larger than itself, E3 because a
new stack is as empty as a cleared one, and E2 and E4 because they say
the same thing another way.

## Verification

The four arms print the same output as `find_unsorted_subarray.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on the ★, sorted and stack arms and the bench program; it refuses
the widen arm and the differential at
`*nums[left..=right].iter().min().unwrap()` (B-2026-10-14-24), which
both MIR backends run as written.

The frozen legacy backends: the ★, sorted and stack arms print the right
output under `karac run --interp`, `karac run` and `karac build`, and
under `KARAC_AUTO_PAR=1 karac build`. The widen arm stops at type
checking on the same line and with the same message as `karac check`,
and the differential there and at the harness's `*x` over `nums.iter()`,
where legacy gives the element as an `i64`. Legacy refuses the bench
program too (see Benchmarks). Legacy is frozen, so these are noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes 100 arrays once, each of
10,000 values (the problem's most) drawn from the whole range, sorted,
and then 1 to 3 pairs swapped at random; then 600 times over every array
is answered. Every implementation prints `100 arrays of 10000 values,
600 rounds: total 327684000, checksum 885456182`, the Kāra program under
`karac __mir-run` included (830 s).

Every implementation sorts with its own library sort when it builds the
arrays, outside the timed answers' loop but inside the run. Spot timings
on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.09 to 1.14 s |
| Rust (`rustc -O`) | 1.06 to 1.11 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.06 to 1.16 s |
| Go | 1.08 to 1.22 s |
| Python | 42.6 to 43.8 s |
| Kāra (`karac build --mir`) | 1.10 to 1.17 s |

The legacy `karac build` refuses this program, since it moves `cases[p]`
out of the index where v2 borrows it. So `bench.sh` builds the Kāra
program with `karac build --mir`, the v2 compiled backend; that edit is
by hand, on top of the `scripts/new-bench.sh` output. The `--mir` row is
timed at kara `f6052c659c`. Under `karac __mir-llvm-run` the program
prints the same line in 15.6 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

The five compiled programs take about the same time, the Kāra one
included.

## Compiler findings

One filed: **B-2026-10-14-24**. `karac check` types the result of `min`
and `max` over `v.iter()` as `Option[i64]` where the library declares
`Option[Self.Item]`, an `Option[ref i64]` here, so the widen arm's `let
low = *nums[left..=right].iter().min().unwrap();` is refused ("unary '*'
requires 'ref T' ... found 'i64'"), though both MIR backends run it and
the library's own tests use that spelling. It is the `karac check` half
of B-2026-10-13-7, whose fix added the terminals for the MIR backends.
The arm keeps the `*`. Writing the arm also showed that iterators have
no `clone`, so the first draft's `middle.clone().min()` on a stored
iterator was rewritten as two calls on the slice; nothing in the spec
says iterators are `Clone`, so that is not filed. The legacy failures
above are not filed because legacy is frozen.
