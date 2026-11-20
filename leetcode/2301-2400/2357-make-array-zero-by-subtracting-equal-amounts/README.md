# 2357. Make Array Zero by Subtracting Equal Amounts

You are given a non-negative integer array `nums`. In one operation, you
must:

- Choose a positive integer `x` such that `x` is less than or equal to
  the **smallest non-zero** element in `nums`.
- Subtract `x` from every **positive** element in `nums`.

Return *the **minimum** number of operations to make every element in*
`nums` *equal to* `0`.

```
nums = [1,5,0,3,5]  ->  3
nums = [0]          ->  0
```

**Constraints:** `1 <= nums.length <= 100`; `0 <= nums[i] <= 100`.

Choosing `x` as the smallest non-zero element clears every copy of it
and keeps the other positive values distinct from each other, and a
smaller `x` clears nothing, so each operation clears exactly one
distinct positive value. The answer is the number of distinct positive
values.

## Approaches

| file | mechanism |
|---|---|
| `zero.kara` ★ | the positive values gathered in a `Set`; its `len` is the answer. O(n) |
| `zero_simulate.kara` | the operations done as the statement says: the least positive value found and subtracted from every positive one, until none is left. O(n d) for `d` distinct positive values |
| `zero_sorted.kara` | the values sorted, and each that differs from the one before it counted, starting from 0. O(n log n) |
| `zero_table.kara` | one flag for each value from 0 to 100, then the flags from 1 up counted. O(n + 100) |
| `zero_iter.kara` | iterators: the positive values kept by `filter` and gathered into a `Set` by `collect` |
| `zero_solution.kara` | LeetCode's Rust template: `nums.into_iter().filter(\|&x\| x > 0).collect::<HashSet<_>>().len() as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; 100 zeros;
1 to 100; 100 copies of 100; then 5000 random arrays of 1 to 100 values
from 0 to 1 up to 0 to 100, with a checksum, the operations summed and
how many arrays were already zero. `zero.py` mirrors the ★ arm and its
output is byte-identical, and the mirror was checked against the
operations done one by one on 3000 random arrays.

`karac fix` carries the template in one call, reporting 9 edits.
`check` first reports 6 errors, each with its edit: the `HashSet`
import deleted, `struct Solution;` given braces, `Vec<i32>` made
square, the `&` of `|&x|` dropped, the `::` call written with `.`, and
the turbofish `collect::<HashSet<_>>()`, whose result is the receiver
of `.len()` and so has no binding to annotate, rewritten as
`Set.from_iter(...)` around the iterator. The rest follow: `nums` taken
`own`, since `into_iter` consumes it. `.len() as i32` stands as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the operation done on a fresh copy of the array each time,
the least positive value found and subtracted from every positive value,
and the operations counted until every value is 0. No distinct values
counted. It checks 300 random arrays of 1 to 100 values from 0 to 1 up
to 0 to 100; then 30 of 100 values from 0 to 100; then 30 of up to 100
values, nine in ten of them 0. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | from 0 to the number of positive values, and 0 exactly when every value is 0 |
| P3 | the values reversed: the same answer |
| P4 | every positive value `x` made `101 - x`: the same answer |
| P5 | the values given twice over and a 0 added: the same answer |
| P6 | each arm agrees with at least three of the other five |

P4 stays inside the constraint, `x` from 1 to 100 going to 100 to 1, so
the table arm's 101 flags still hold every value.

The literal reading does the operations as the simulate arm does,
written apart from it on a fresh vector each round. The differential
prints `360 cases: checksum 877712328, 12960 checks over 6 arms: 0
failures` under every lane in Verification; the checksum of the literal
answers was checked against a Python reading that builds the same
cases and counts the distinct positive values. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 0 counted as a value | P1 230, P2 30, P5 130, P6 230 |
| M4 | ★: the first value skipped | P1 140, P2 5, P3 116, P5 140, P6 140 |
| M5 | ★: 1 not counted | P1 198, P2 4, P4 194, P6 198 |
| M8 | simulate: 1 subtracted each time | P1 312, P2 196, P4 339, P6 312 |
| M9 | simulate: each operation counted twice | P1 355, P2 270, P6 355 |
| M10 | simulate: stopped once the least value is 1 | P1 317, P2 198, P4 261, P6 317 |
| M12 | sorted: values one apart merged | P1 317, P2 4, P4 119, P6 317 |
| M13 | sorted: the previous value never moved | P1 305, P5 355, P6 305 |
| M14 | sorted: the values left unsorted | P1 329, P2 134, P3 34, P5 355, P6 329 |
| M18 | table: 100 never counted | P1 26, P4 194, P6 26 |
| M19 | table: values halved before they are flagged | P1 310, P2 4, P4 194, P6 310 |
| M21 | table: only the first 50 values read | P1 152, P3 122, P6 152 |
| M23 | iter: at most 20 operations | P1 196, P6 196 |
| M24 | iter: only even values counted | P1 347, P2 10, P4 289, P6 347 |
| M26 | iter: values divided by 3 before they are gathered | P1 309, P6 309 |
| M27 | solution: values up to 10 ignored | P1 327, P2 40, P4 327, P6 327 |
| M28 | solution: one operation more | P1 360, P2 55, P6 360 |

P1 and P6 kill all seventeen, P2 twelve, P4 eight, P5 four and P3
three. P3, the values reversed, fails only the edits that read some of
the values by place: the first value skipped, the first 50 read, and
the sorted arm's values left unsorted. P4, the positive values
reflected, fails the edits that treat some values unlike others: 1 not
counted, 100 never counted, values halved or one apart merged, only
even values, values up to 10 ignored, and the simulation's edits that
subtract or stop by a fixed 1. P5, the values twice over with a 0,
fails the edits whose count changes with copies or with a 0: 0 counted
as a value, the first value skipped, the previous value never moved and
the values left unsorted.

Of the thirty-one, fourteen were not kept. 0 counted as a value fails
alike in the sorted, table and iter arms (M15, M17, M22) as in the ★
arm (M1); the first value skipped in the iter arm (M25) and the last
value skipped in the template (M29) as in the ★ arm (M4); and each
value counted twice in the table arm (M20) as each operation counted
twice in the simulate arm (M9). One operation fewer and values 50 apart
merged in the ★ arm (M3, M6), the greatest positive value subtracted
and at most 10 operations in the simulate arm (M7, M11), each distinct
value counted as itself in the sorted arm (M16), and the template's
values 7 apart merged and half the operations (M30, M31) fail apart
from every kept one; they were left out to keep three to an arm and two
to the template.

## Verification

Every arm prints the same output as `zero.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.45 to 0.8 s but the template,
1.4 s, which narrows every array to `i32` first, and the simulate arm,
3.2 s, its rounds over arrays of up to 100 distinct values. The
differential takes 2.7 s there and 0.46 s under `karac
__mir-llvm-run`.

## Benchmarks

The bench builds `2 * 10^4` arrays of 100 values once, each from 0 to
1 up to 0 to 100, then makes 50 passes, pass `p` folding each answer
plus `p` into the checksum, with the ★ arm in all five languages. Every
implementation prints `50 passes over 2 * 10^4 arrays of 100 values:
checksum 996535382`. Each call builds its own set; C has no set, so it
counts in a table of 256 slots by open addressing, cleared for each
call.

BENCHTAB
