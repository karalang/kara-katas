# 377. Combination Sum IV

Given an array of distinct positive integers `nums` and a `target`,
return the number of ordered sequences of values from `nums` (each
value may repeat) that sum to `target`. The answer fits in a 32-bit
integer.

```
nums = [1, 2, 3], target = 4   -> 7
nums = [9], target = 3         -> 0
```

**Constraints:** `1 <= nums.length <= 200`; `1 <= nums[i] <= 1000`;
the values are distinct; `1 <= target <= 1000`.

## Approaches

Let `ways[t]` be the number of sequences that sum to `t`. The last value
of such a sequence is some `x <= t`, and what comes before it sums to
`t - x`, so `ways[t]` is the sum of `ways[t - x]`, with `ways[0] = 1`
for the empty sequence. The arms compute the same counts in different
ways.

The promise that the answer fits in 32 bits says nothing about the
counts for other totals. With `[2, 4]` and an odd target the answer is
0, while the counts for the even totals grow like Fibonacci numbers,
far past `i64`. Kāra stops on integer overflow, so a table filled from
0 upward has to deal with them, and each arm says how it does.

| file | mechanism | overflow | time |
|---|---|---|---|
| `combination_sum4.kara` ★ | fill the table from 0 up | each count is capped at 2^31: a count that large cannot feed the answer, because the answer is at least every count it is built from | O(target · n) |
| `combination_sum4_push.kara` | once `ways[t]` is final, add it to `ways[t + x]` for every value | `wrapping_add`, named at the call site: wrapping is exact modulo 2^64 and the answer is below 2^31, so it comes out right however the other counts wrap | O(target · n) |
| `combination_sum4_memo.kara` | the recurrence top down from the target, each total solved once and kept in a table | none possible: only the totals the answer is built from are visited, and each of their counts is at most the answer | O(target · n) |
| `combination_sum4_sorted.kara` | the ★ arm with the values sorted, so the inner loop stops at the first value above the total and totals below the smallest value are skipped | capped, as in the ★ arm | O(n log n + target · n) |
| `differential.kara` | the four arms against an oracle that lists every sequence, and against closed forms, 32,352 checks, six properties | — | — |

Leaving the cap out of the ★ arm stops it with `integer overflow` on
`[2, 4]` with target 999 under `karac __mir-run`.

Every arm prints the same 10 lines: the two LeetCode examples, seven
edge cases (a target below every value, one value that divides the
target and one that does not, `[1, 2]` to 40, `[2, 4]` to 999,
`[3, 33, 333]` to 1000, values near 1000), and a checksum over 200
random cases. Half the random cases use values up to 15 and a target up
to 30; the other half use values from 10 to 199 and a target that is a
sum of one to five of them, so it can be reached. Every answer is below
2^31, as the problem promises. `combination_sum4.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. The oracle walks
every sequence one value at a time and counts the ones that land on the
target, so the random cases have targets up to 14 and up to four values
from 1 to 12; there are 1,500 of them.

| | property |
|---|---|
| P1 | each arm gives the oracle's count |
| P2 | adding a value larger than the target changes nothing |
| P3 | reversing the values changes nothing |
| P4 | doubling every value and the target changes nothing |
| P5 | adding the target itself as a value adds exactly one sequence |
| P6 | closed forms past the oracle's reach: with `[1, 2]` the count to `t` is the Fibonacci number `F(t + 1)`, for every `t` up to 44; with `[2, 4]` it is `F(m + 1)` to `2m` for every even total up to 88, and 0 to every odd total up to 999, where the even counts overflow |

It prints `1500 cases, 32352 checks, 0 failures` under
`karac __mir-run`, `karac __mir-llvm-run`, `karac run --interp`, LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | capped: the cap is 2^30 | P6, 4 failures |
| M2 | capped: takes the largest count instead of the sum | P1, P5 and P6, 1019 failures |
| M3 | push: overwrites the count instead of adding to it | P1, P5 and P6, 1019 failures |
| M4 | push: never pushes from the total just below the target | P1, P4, P5 and P6, 795 failures |
| M5 | memo: the empty sequence counts twice | P1, P5 and P6, 2118 failures |
| M6 | sorted: the values are not sorted | P1, P3 and P5, 1729 failures |
| M7 | sorted: skips the smallest value as a total | P1, P5 and P6, 1121 failures |
| M8 | oracle: a value equal to what is left is never used | P1, 3124 failures |

M1 is killed only by P6: no random case comes near 2^30, and the four
failures are the Fibonacci counts from `F(45)` to `[1, 2]` and from
`F(45)` to `[2, 4]`, one per capped arm each.

## Verification

All four arms print the same output as `combination_sum4.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` (the
same MIR compiled to LLVM), `karac run --interp`, LLJIT, `karac build`
and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program runs the ★ arm on 2,000 cases of 200 distinct values
from 125 to 999 with target 1,000, the problem's largest, and folds the
answers into a checksum. Values from 125 up keep every answer below
2^31 (the largest is 53,300,139, computed without a cap in
Python). The Kāra build and the C, Rust, Go and Python mirrors all print
`checksum 427689463`, and so does `karac __mir-llvm-run`. Timings are
not taken yet; they need a quiet machine.

## Compiler findings

None.
