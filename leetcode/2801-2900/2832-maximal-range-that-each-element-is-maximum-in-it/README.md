# 2832. Maximal Range That Each Element Is Maximum in It

You are given a **0-indexed** array `nums` of **distinct** integers.

Let us define a **0-indexed** array `ans` of the same length as `nums`
in the following way:

- `ans[i]` is the maximum length of a subarray `nums[l..r]`, such that
  the maximum element in that subarray is equal to `nums[i]`.

Return *the array* `ans`.

**Note** that a **subarray** is a contiguous part of the array.

```
nums = [1,5,4,3,6]  ->  [1,4,2,1,5]
nums = [1,2,3,4,5]  ->  [1,2,3,4,5]
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^5`;
all elements in `nums` are distinct.

## Approaches

| file | mechanism |
|---|---|
| `ranges.kara` ★ | two passes of a falling stack through `while let Some(top) = stack.last()`, the nearest greater number on the left and on the right of each place; nums[i] is the maximum of every range strictly between them, so the longest is right - left - 1 |
| `ranges_once.kara` | one pass of a falling stack: a number popped by a greater one has found its right end, the number below it on the stack is its left end, and a sentinel step past the end empties what is left |
| `ranges_spread.kara` | from each place, a walk left and then right while the numbers are smaller; O(n^2) on a sorted array, for the harness's shuffled ones |
| `ranges_linked.kara` | smallest first: the places in a doubly linked list held by a struct with a `mut ref self` method, taken out in rising order of their numbers, so a place's two neighbours still in the list when it goes are its nearest greater numbers |
| `ranges_solution.kara` | a Rust solution as LeetCode's Rust users write it: `vec![-1i32; n]` and `vec![n as i32; n]` for the ends, a `Vec<usize>` stack walked twice with `while let Some(&j) = stk.last()`, and the answer collected as `i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one
number; a falling array; 1 to 10^5 shuffled, LeetCode's most, as its
length, sum and a digest; then 3000 random arrays of 1 to 12 distinct
numbers and 50 of up to 3000, as checksums. `ranges.py` mirrors the ★
arm and its output is byte-identical.

```
[1, 4, 2, 1, 5]
[1, 2, 3, 4, 5]
[1]
[5, 4, 3, 2, 1]
100000 2210730 802396888
3000 short arrays: checksum 166635722
50 long arrays: checksum 244691322
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: for each place, every range around it, kept when no
number in it is greater, and the longest. It draws 2000 random arrays
of 1 to 12 distinct numbers, then 50 of up to 2000, all before any arm
answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 numbers, the answer is the literal reading's |
| P2 | the numbers reversed: the answer reversed |
| P3 | every number doubled and one added: the same answer |
| P4 | a number greater than all appended: the old answers unchanged, and n + 1 for it |
| P5 | the largest number's answer is n, and none is below 1 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 606835818, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a number with no greater one on its right stopped one short | P1 2000, P2 1890, P4 2050, P5 2050, P6 2050 |
| M2 | ★: the ends counted into the range | P1 2000, P4 2050, P5 2050, P6 2050 |
| M3 | once: the left end taken as the place before | P1 1725, P2 1825, P4 2050, P5 1557, P6 1775 |
| M4 | once: the stack never emptied at the end | P1 2000, P2 1890, P4 2050, P5 2050, P6 2050 |
| M5 | spread: the walk left stops before the first place | P1 1508, P2 1658, P4 2050, P5 1557, P6 1557 |
| M6 | spread: the range counted one short | P1 2000, P4 2050, P5 2050, P6 2050 |
| M7 | linked: the places taken out largest first | P1 1840, P4 2050, P5 1890, P6 1890 |
| M8 | linked: the right neighbour's link never mended | P1 1725, P2 1790, P4 2050, P5 1775, P6 1775 |
| M9 | solution: the right default as -1 | P1 2000, P2 1890, P4 2050, P5 2050, P6 2050 |
| M10 | solution: the right end set to the place itself | P1 1725, P2 1890, P4 2050, P5 1775, P6 1775 |

## Benchmarks

The bench shuffles 1 to 10^5 twenty times, LeetCode's most, all of
them first, then answers each 20 times by the ★ arm in all five
languages, folding every answer into the checksum. Every
implementation prints `20 arrays of 100000, 20 rounds: ranges total
845272860, checksum 735974405`.

BENCHTAB

## Verification

All five arms print the same output as `ranges.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The harness's large
case was first a rising-then-falling hill of 10^5; the spreading arm
walks n^2 / 4 steps on it, which the compiled lanes finish in seconds
but the interpreter would not, so it became a shuffle, as the
statement's distinct numbers allow.

Checking the kara fix this batch rode on against an older fixture
turned up a gap the kata itself does not reach: a tuple of an indexed
place and a number literal lent to a parameter of `ref` elements,
`g((a[0], 2))` for `p: (ref i64, ref i64)`, is refused, where `g((x,
2))` and `g((a[0], b[0]))` are accepted. It is not in the kara ledger yet: the kata rows are at their cap, so
the row waits for a free slot.

LeetCode's Rust template took 25 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`;
`Vec<..>` became `Vec[..]` and `usize` `i64`; `vec![-1i32; n]` and
`vec![n as i32; n]` became `Vec.filled(n, ..)`; `Vec::new()` took
`.`; each of the four `while let Some(&j) = stk.last()` and `if let
Some(&j) = stk.last()` lost its `&` and gained `.cloned()` on the
`last()`, a copy the own arms never write, since `last()` of an `i64`
list binds a value either way; `Solution::` took `.`, and `|&v|` lost
its `&`.
