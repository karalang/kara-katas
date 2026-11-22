# 2843. Count Symmetric Integers

You are given two positive integers `low` and `high`.

An integer `x` consisting of `2 * n` digits is **symmetric** if the sum
of the first `n` digits of `x` is equal to the sum of the last `n`
digits of `x`. Numbers with an odd number of digits are never
symmetric.

Return *the **number of symmetric** integers in the range* `[low,
high]`.

```
low = 1, high = 100      ->  9
low = 1200, high = 1230  ->  4
```

**Constraints:** `1 <= low <= high <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `symmetric.kara` ★ | each number written out with `to_string()`, kept when it has an even count of digits and its first half's digits, summed by a closure, come to its second half's; `filter(..).count()` over the range |
| `symmetric_digits.kara` | by arithmetic, no strings: the digits counted by dividing by 10, then the low half's digits taken away from a balance and the high half's added, the number symmetric when that comes to zero |
| `symmetric_prefix.kara` | a prefix count over the whole range LeetCode allows, `up_to[x]` the symmetric numbers from 1 to x, built in one pass from a table of two-digit sums, and the answer a difference of two entries |
| `symmetric_halves.kara` | built from halves rather than tested: for lengths 2 and 4 the second halves grouped by digit sum in a `SortedMap` of sorted lists, through `entry().or_insert()`, and for each first half the second halves that keep the number in range counted by `partition_point` |
| `symmetric_solution.kara` | a Rust solution as LeetCode's Rust users write it: the inclusive range `low..=high` filtered by a closure over each number's `to_string().as_bytes()`, the halves summed with `sum::<i32>()`, and `count() as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; one number
of each kind, 11, 12, 10^4 and 1001; the whole range LeetCode allows,
1 to 10^4; then 3000 random ranges inside it and 3000 of at most 100
numbers, as totals and checksums. `symmetric.py` mirrors the ★ arm and
its output is byte-identical.

```
9 4
1 0 0 1
624
3000 ranges: 693085 in all, checksum 495396063
3000 ranges: 9308 in all, checksum 998800478
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every number from low to high, its digits listed from
`f"{x}"`, counted when there are 2n of them and the first n sum to the
last n. It draws 2000 random ranges of up to 100 numbers inside 1 to
10^4, then 50 of any width, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the range split at its middle: the two parts' answers add up to it |
| P3 | low alone: 1 exactly when the literal reading keeps low |
| P4 | the range one wider at each end, inside 1 to 10^4: no smaller |
| P5 | no more than the numbers in the range |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 562828037, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: odd lengths kept | P1 199, P3 12, P6 199 |
| M2 | ★: the halves split one place late | P1 1511, P3 146, P6 1511 |
| M3 | ★: high left out | P1 117, P2 131, P3 136, P6 117 |
| M4 | digits: the middle digit counted on the low side | P1 1414, P3 151, P6 1414 |
| M5 | digits: a number's length one short | P1 1763, P3 160, P6 1763 |
| M6 | prefix: low itself left out | P1 136, P2 122, P3 136, P6 136 |
| M7 | prefix: the two-digit numbers never kept | P1 30, P3 3, P6 30 |
| M8 | halves: the second half's sum not the first's | P1 1025, P3 119, P6 1025 |
| M9 | halves: the tail at the top of the range left out | P1 117, P2 131, P3 136, P6 117 |
| M10 | solution: odd lengths kept | P1 199, P3 12, P6 199 |

## Benchmarks

The bench draws 5000 random ranges inside 1 to 10^4, all of them
first, then answers each twice by the ★ arm in all five languages.
Kāra, Rust, Go and Python write each number out and copy its halves
out to be summed, as the ★ arm does; C writes it with `snprintf` and
sums the halves in place. Every implementation prints `5000 ranges, 2
rounds: 2339434 in all, checksum 660603729`.

BENCHTAB

## Verification

All five arms print the same output as `symmetric.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ arm, as first written, gave its closure a return type, `|part:
Vec[u8]| -> i64 { .. }`, as Rust allows, and `karac check` reported
E0001, "a closure does not declare its return type; `|..| -> i64` is
Rust syntax"; `karac fix` moved the type to the binding, `let half:
Fn(ref Vec[u8]) -> i64 = |part: Vec[u8]| { .. }`. It then reported
E0516 on `let digits = x.to_string().bytes();`, the `String` a
temporary dropped while `digits` still borrows it, with no
machine-applicable fix, as Rust's E0716 gives only a hint; the
`String` was bound first, as the message says. In the halves arm `let tails = by_sum[..]` drew
E_INDEX_MOVE_NON_COPY, a `Vec` moved out of an index, and `karac fix`
borrowed it, `ref by_sum[..]`. The other arms checked clean.

LeetCode's Rust template took 10 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `|&x|`
and both `|&c|` lost their `&`; `as_bytes()` became `bytes()`; `&&`
became `and`; both `sum::<i32>()` lost their turbofish, the `as i32`
elements fixing the type; `Solution::` took `.`, and the wrapper's `as
i64` went. The inclusive range `low..=high` and the narrowing `count()
as i32` were accepted as written.
