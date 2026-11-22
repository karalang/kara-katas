# 2811. Check if it is Possible to Split Array

You are given an array `nums` of length `n` and an integer `m`. You need
to determine if it is possible to split the array into `n` arrays of
size 1 by performing a series of steps.

An array is called **good** if its length is one, or the sum of its
elements is greater than or equal to `m`.

In each step, you can select an existing array (which may be the result
of previous steps) with a length of **at least two** and split it into
**two** arrays, if both resulting arrays are good.

Return `true` *if you can split the given array into* `n` *arrays,
otherwise return* `false`.

```
nums = [2,2,1],     m = 4  ->  true
nums = [2,1,3],     m = 5  ->  false
nums = [2,3,3,2,3], m = 6  ->  true
```

**Constraints:** `1 <= n == nums.length <= 100`; `1 <= nums[i] <= 100`;
`1 <= m <= 200`.

## Approaches

| file | mechanism |
|---|---|
| `split.kara` ★ | by two neighbours: one or two numbers always split, a longer array splits just when `windows(2).any` finds a pair summing to at least m, since single numbers can then be peeled off the ends towards it |
| `split_table.kara` | the interval table, as the statement describes the splits: `ok[i][j]` when some cut of `nums[i..=j]` leaves two good parts that split in turn, filled by length with prefix sums. O(n^3) |
| `split_peel.kara` | peeling by recursion with a `Map` memo keyed by the part's ends: a single number off either end, the rest good and itself splitting |
| `split_scan.kara` | a `while` scan keeping the best sum of two neighbours, with an early answer for arrays too short to need one |
| `split_solution.kara` | a Rust solution as LeetCode's Rust users write it, `nums.len() <= 2 \|\| nums.windows(2).any(...)` on `i32`s, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; two
numbers with m at its largest; 100 numbers, LeetCode's most, at 100 with
m at 200, and at 99 with m one more than any two make; 3000 random
arrays of 1 to 7 numbers up to 6 with m up to 12; and 50 of up to 100
numbers up to 100 with m up to 200, the last two with how many split
and a checksum. `split.py` mirrors the ★ arm and its output is
byte-identical.

```
true
false
true
true
true
false
3000 small arrays: 2470 can split, checksum 124310556
50 large arrays: 43 can split, checksum 770749679
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a part of one number is done, and a longer one is split when
some cut leaves two parts, each one number or summing to at least m,
that are themselves split, every cut tried by recursion on copied parts;
no table, no prefix sums and no neighbours. It draws 2000 random arrays
of 1 to 7 numbers up to 6 with m up to 12, then 50 of up to 100 numbers
up to 100 with m up to 200, all before any arm answers; the literal
reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 7 numbers, the answer is the literal reading's |
| P2 | two numbers or fewer: true |
| P3 | m one less: still true when it was true |
| P4 | the numbers reversed: the same answer |
| P5 | m 1: true; m past the whole sum: true just for two numbers or fewer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 422256827, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two numbers made to need a pair | P1 108, P2 108, P5 263, P6 108 |
| M2 | ★: a pair needing more than m | P1 110, P6 110 |
| M3 | table: a part of one number counted only when it reaches m | P1 1079, P2 203, P5 263, P6 1121 |
| M4 | table: the last cut never tried | P1 1342, P2 263, P5 1764, P6 1385 |
| M5 | peel: the left end's rest measured with the end in it | P1 225, P6 229 |
| M6 | peel: only the left end peeled | P1 231, P4 328, P6 252 |
| M7 | scan: the first pair never looked at | P1 73, P4 140, P6 74 |
| M8 | scan: the best pair kept as the least | P1 468, P6 504 |
| M9 | solution: or turned to and | P1 1472, P2 394, P5 2050, P6 1516 |
| M10 | solution: the pairs taken as one number and the next but one | P1 152, P6 157 |

## Benchmarks

The bench draws 100000 arrays of 100 numbers, LeetCode's most, up to
100, with m from 150 to 200 so that most scans run long, all of them
first, then answers each 10 times by the ★ arm in all five languages.
Kāra's `windows(2)` makes a list of the windows before `any` walks it;
C, Rust, Go and Python stop at the first pair. Every implementation
prints `100000 arrays of 100, 10 rounds: 760820 can split, checksum
571760223`.

BENCHTAB

## Verification

All five arms print the same output as `split.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ arm first called `nums.windows(2).any(...)` as Rust does; Kāra's
`windows` returns a list, and `karac fix` wrote `.into_iter()` before
`any`. The other own arms and the harness checked clean as first
written.

LeetCode's Rust template took 9 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `Vec<i32>` and `Vec<i64>` became
`Vec[..]`; `||` became `or`; `windows(2)` took `.into_iter()`; the
wrapper's `nums`, consumed by `into_iter()`, became `own`; and
`Solution::` took `.`.
