# 1150. Check If a Number Is Majority Element in a Sorted Array

Given an integer array `nums` sorted in non-decreasing order and an
integer `target`, return `true` if `target` is a **majority** element, or
`false` otherwise.

A **majority** element in an array `nums` is an element that appears more
than `nums.length / 2` times in the array.

```
nums = [2,4,5,5,5,5,5,6,6], target = 5  ->  true
nums = [10,100,101,101], target = 101   ->  false
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i], target <= 10^9`;
`nums` is sorted in non-decreasing order.

The arms are `fn is_majority_element(nums: Vec[i64], target: i64) -> bool`.

## Approaches

In a sorted list the copies of the target are one run, so the target is a
majority exactly when the run is longer than half the list, and then the
value `n / 2` places after the run's start is still the target.

| file | mechanism |
|---|---|
| `is_majority_element.kara` ★ | one binary search: `partition_point` finds the run's start, and the value `n / 2` places on decides. O(log n) |
| `is_majority_element_bounds.kara` | both ends of the run by `partition_point`, and twice its length against the list's. O(log n) |
| `is_majority_element_count.kara` | every value counted with `filter` and `count`, the order unused. O(n) |
| `is_majority_element_search.kara` | the binary search written out, `low` and `high` closing in on the run's start. O(log n) |
| `is_majority_element_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `nums: Vec<i32>`, the run's two ends by `partition_point(\|&x\| ...)` and its length times two against `nums.len()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 18 lines: LeetCode's two examples; one value
equal to the target (true) and not (false); `[1, 1, 2, 2]` for either
value, exactly half (false); `[1, 2, 2]` and `[1, 1, 2]`, one more than
half at either end (true); a target below and above every value (false).
Then 2000 random sorted lists of 1 to 60 values in four kinds (values 1
to 3; values up to 10^9 and a target from the list; about half the list
the target and the rest above and below it; values 1 to 2 and the middle
value as the target), with the count of majorities and a checksum (`2000
random lists: majority 668, checksum 286058900`), and seven lists at the
constraints' end: 1000 copies of 10^9 (true), and 501 or 500 copies of 7
among 1000 values starting at the front, the middle or the back (true,
false). `is_majority_element.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the target appears more than `nums.len() / 2` times. It checks
2000 sorted lists of 1 to 30 values in four kinds of 500: values 1 to 2
and a target 0 to 3; values 1 to 4 and a target 0 to 5; about half the
list one target and the rest above and below it, values up to 10^9; and
runs of the target's neighbours below, the target, and above. Every
random choice, P3's names and P6's value among them, is drawn before any
arm answers. 416 of the 2000 answers are true, and in 107 lists the
target fills exactly half.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | every value mirrored to 10^9 + 1 - x, the list reversed to stay sorted, and the target with them, gives the same answer |
| P3 | the values renamed in order, the k-th distinct value to `offset + gap * k`, gives the same answer (a target the list lacks goes between its neighbours' names) |
| P4 | every value twice gives the same answer |
| P5 | one more copy of the target gives true exactly when the answer was true or the target filled exactly half |
| P6 | one more value that is not the target never makes a majority |
| P7 | a majority holds both middle places of the list |

All 70,000 checks pass on every arm: `2000 problems: checksum 409966077,
70000 checks over 5 arms: 0 failures`. A Python reading of the same
lists, with the seven properties asserted against the ★ arm's mirror,
gives the same line.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-eight are caught; two are
equivalent: the written-out search starting `high` at `n - 1`, which
only stops it from landing past the last value, where no run can start
that the check after it would accept; and the solution arm finding the
run's end as the first value not below `target + 1`, which for integers
is the first value above `target`. Nineteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run of exactly half taken | P1 81, P2 47, P5 92, P7 21 |
| M2 | ★: the search lands past the run | P1 416, P5 107 |
| M3 | ★: a run that ends the list never counted | P1 80, P2 86, P4 36, P5 62, P6 12 |
| M4 | ★: only the middle value read | P1 356, P5 53, P6 36 |
| M5 | ★: any copy taken for a majority | P1 948, P5 636, P7 592 |
| M6 | ★: the run starts at the value below | P1 197, P2 155, P3 197, P5 123, P6 48, P7 78 |
| M7 | bounds: exactly half taken | P1 107, P5 141, P7 47 |
| M8 | bounds: one more than half needed by two | P1 114, P4 114, P5 221 |
| M9 | bounds: the run takes in the value above | P1 374, P2 728, P3 373, P5 52, P6 21, P7 263 |
| M10 | bounds: the run's first copy lost | P1 220, P4 106, P5 213 |
| M11 | bounds: the run takes in the value below | P1 556, P2 728, P3 556, P5 57, P6 42, P7 437 |
| M12 | count: values below counted | P1 1045, P2 1216, P5 35, P6 28, P7 689 |
| M13 | count: values above counted | P1 883, P2 1216, P5 30, P6 20, P7 527 |
| M14 | count: the first value never counted | P1 76, P2 86, P4 40, P5 61, P6 20 |
| M15 | count: twice the count against half the length | P1 595, P5 211, P7 280 |
| M16 | search: `high` moved past `mid` | P1 68, P2 91, P4 42, P5 99, P6 34, P7 26 |
| M17 | search: the search stops one short | P1 74, P2 70, P4 82, P5 81, P6 23, P7 15 |
| M18 | search: any copy taken, the length still checked | P1 597, P2 592, P5 316, P6 14, P7 241 |
| M19 | solution: one copy counted too many | P1 248, P4 141, P5 146, P7 140 |

P1 and P5 catch all twenty-eight. P5 is the sharpest of the properties
that do not compute the answer: one more copy of the target turns a run
of exactly half into a majority, so an edit that is off by one copy
either way, or that never answers true (M2), misses it on the 107 lists
at exactly half. P7 catches sixteen, the edits that call a run a majority
when it does not cover the middle (M1, M5, M15, M18). P2 and P6 catch
twelve each: mirroring turns the run's start into its end, so an edit
that treats the two ends unlike (M3, M14, M16, M17) answers the mirror
differently, and an added value that is not the target shifts the
middle, which an edit that reads a fixed place (M4) or counts
neighbours (M12, M13) mistakes for a run. P4 catches ten, the edits off
by a fixed count that doubling the list does not double (M3, M8, M10,
M19). P3 catches only the four edits that let the run take in a
neighbouring value: renaming in order keeps every comparison but moves
the values apart, so `target - 1` and `target + 1` no longer name the
neighbours (M6, M9, M11, and the same edit in the solution arm).

Of the nine caught and not kept, each fails exactly as a kept one: the
bounds arm finding the run's end at its start, the count arm not doubling
the count, and the written-out search landing past the run, as M2; the
count and solution arms taking exactly half, as M7; the written-out
search rounding half up, as M8; the solution arm losing the run's last
copy or needing one more than half by three, as M10; and the solution
arm taking in the value below, as M11.

## Verification

Every arm prints the same output as `is_majority_element.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, bounds, count and search arms were written as Kāra and checked
clean as written. `karac fix` carried the solution arm in three rounds:
`Vec<i32>` to `Vec[i32]`, the `|&x|` patterns to `|x|`, the adapter's
`&Vec<i64>` to `ref Vec[i64]` and `Solution::` to `Solution.`; then
`struct Solution {}` declared; then the adapter's `ref` dropped, a
parameter borrowing by default. In the differential `karac fix` added
the `.into_iter()` that `flat_map` needs on the `[x, x]` each value
becomes, and in the bench it borrowed `lists[q % 64]`, which a plain
`let` would move out of the list.

The kata found one gap, a perf row: `partition_point` is the branching
binary search where Rust's is branch-free (B-2026-11-13-34; see
Benchmarks).

## Benchmarks

`bench/` times the ★ arm against the same search in C, Rust, Go and
Python. 64 sorted lists of 1000 values, each with 450 to 550 copies of
one value, are built once; then 10,000,000 queries each take a list in
turn and a target (a value of the list, its middle value, one above a
value of the list, or any value). Every program prints `10000000 queries
over 64 lists of 1000 values: majority 2142831, checksum 357578983`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `d59535f2bc`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.361 to 0.393 s | 0.368 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.358 to 0.401 s | 0.371 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.353 to 0.404 s | 0.388 s |
| C (`clang -O3`) | 0.731 to 0.806 s | 0.745 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.727 to 0.816 s | 0.758 s |
| Kāra (`karac build`) | 0.739 to 0.805 s | 0.761 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.745 to 0.845 s | 0.762 s |
| Go | 0.772 to 0.859 s | 0.796 s |
| Python | 8.8 s | |

The two Kāra builds are the same binary: the cost gate parallelizes
nothing here.

Kāra ties C and Go and takes twice Rust's time, and the split is between
two ways to search. Kāra's `partition_point`, the C mirror's loop and
Go's `sort.Search` move `low` or `high` on each comparison, a branch the
processor guesses wrong about half the time on a random target. Rust's
`partition_point` halves a size and picks the next base with a
conditional move, in a loop with no branch on the comparison and, since
the standard library indexes unchecked, no bounds or overflow check
(B-2026-11-13-34, perf, open). The same branch-free loop written in Kāra
took 0.75 to 0.79 s in three runs by hand: compiled, it branches again,
with the overflow check on `base + half` and the bounds check on
`xs[mid]` in the loop. That the checks are what turns the conditional
move back into a branch is inferred, not measured.
