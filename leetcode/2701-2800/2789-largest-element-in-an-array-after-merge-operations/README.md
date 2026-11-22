# 2789. Largest Element in an Array after Merge Operations

You are given a **0-indexed** array `nums` consisting of positive
integers.

You can do the following operation on the array **any** number of
times:

- Choose an integer `i` such that `0 <= i < nums.length - 1` and
  `nums[i] <= nums[i + 1]`. Replace the element `nums[i + 1]` with
  `nums[i] + nums[i + 1]` and delete the element `nums[i]` from the
  array.

Return *the value of the **largest** element that you can possibly
obtain in the final array.*

```
nums = [2, 3, 7, 9, 3]  ->  21
nums = [5, 3, 3]        ->  11
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= nums[i] <= 10^6`.

## Approaches

Merging only ever grows a number, so the number built from the right
end should take in everything it can: a number on its left that is no
greater joins it, and one that is greater is larger than all of it and
starts afresh. The number held never falls, so the last one held is the
answer.

| file | mechanism |
|---|---|
| `merge.kara` ★ | from the right end, the number held taking in `nums[i]` when it is no greater and becoming it otherwise, by an index walked down; the last held is the answer. O(n) |
| `merge_fold.kara` | the ★ arm's walk as one `fold` over `nums.iter().rev()`, starting from 0, which every number exceeds. O(n) |
| `merge_blocks.kara` | by blocks and prefix sums: from the right end, each block grown left while the number before it is no greater than the block's sum, read off the prefix sums; the greatest block's sum. O(n) |
| `merge_stack.kara` | the merges done: the numbers a stack with the last on top, popped by `while let Some(v) = stack.pop()`, each merged into the number built or starting a new one, and the largest built kept. O(n) |
| `merge_solution.kara` | a Rust solution as LeetCode's Rust users write it, `for &x in nums.iter().rev()` with `ans: i64` from 0 taking in each `x as i64` no greater and starting afresh at a greater one, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; `[2, 2, 3]`,
where merging the first pair first leaves 4 and 3, and the answer is 7
only from the right; `10^5` numbers of `10^6`, LeetCode's most; `10^5`
numbers falling from `10^6`, where nothing merges; 3000 random arrays
of 1 to 12 numbers from 1 to 10; and 20 of `10^5` numbers up to `10^6`,
the last two with the sum of the answers and a checksum. `merge.py`
mirrors the ★ arm and its output is byte-identical.

```
21
11
7
100000000000
1000000
3000 small arrays: largest sum to 100518, checksum 81290091
20 arrays of 10^5: largest sum to 999830742145, checksum 76469344
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: from the array as given, every operation that can be done, a
number no greater than the one after it added into that one and taken
out, each array so reached searched in turn, a `Set[Vec[i64]]` keeping
each to one search, and the answer the largest number in any of them; no
walk from the right. It draws 2000 random arrays of 1 to 8 numbers from
1 to 10, then 50 of up to 2000 numbers up to `10^6`, all before any arm
answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 8 numbers, the answer is the literal reading's |
| P2 | every number doubled: the answer doubled |
| P3 | the sum of all put after: twice the sum |
| P4 | three times the greatest put before: the answer and it, when it is no greater than the answer, and it alone otherwise |
| P5 | from the greatest number to the sum of all, and the sum when the numbers are sorted |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 426217620, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same search gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M9 are the same edit in two arms, and
fail the same cases.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal number not merged in | P1 308, P3 219, P4 48, P5 407, P6 308 |
| M2 | ★: the first number never reached | P1 1781, P3 2050, P4 2000, P5 1831, P6 1831 |
| M3 | fold: a greater number dropped, not started from | P1 2000, P3 2050, P4 2050, P5 2050, P6 2050 |
| M4 | fold: the walk started from 10^6, not nothing | P1 2000, P2 2050, P3 2000, P5 2050, P6 2050 |
| M5 | blocks: a block grown while the number before is no greater than its last | P1 528, P4 544, P6 578 |
| M6 | blocks: the rightmost block answered | P1 947, P4 1585, P5 978, P6 978 |
| M7 | stack: a greater number merged in anyway | P1 947, P4 1055, P6 978 |
| M8 | stack: the largest built never kept past the last number | P1 1781, P3 2050, P4 2050, P5 1831, P6 1831 |
| M9 | solution: an equal number not merged in | P1 308, P3 219, P4 48, P5 407, P6 308 |
| M10 | solution: a number no greater taking the place of the one built | P1 1585, P3 2050, P5 1831, P6 1635 |

## Benchmarks

The bench draws 20 arrays of `10^5` numbers up to `10^6`, LeetCode's
most, all of them first, then answers each 100 times by the ★ arm in all
five languages. Every implementation prints `20 arrays of 10^5, 100
rounds: largest sum to 99897199428600, checksum 74759707`.

BENCHTAB

## Verification

All five arms print the same output as `merge.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

All four own arms and the differential checked clean as first written.

LeetCode's Rust template took 8 `karac fix` edits, the wrapper
included: `struct Solution {}` added; the `Vec<..>`s became `Vec[..]`;
`for &x` and the wrapper's `|&v|` dropped their `&`; and `Solution::`
became `Solution.`. The `let x = x as i64;` widening stayed, as did the
`as i32` narrowing in the wrapper.
