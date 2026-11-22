# 2801. Count Stepping Numbers in Range

Given two positive integers `low` and `high` represented as strings,
find the count of **stepping numbers** in the inclusive range `[low,
high]`.

A **stepping number** is an integer such that all of its adjacent
digits have an absolute difference of **exactly** `1`.

Return *an integer denoting the count of stepping numbers in the
inclusive range* `[low, high]`*.*

Since the answer may be very large, return it **modulo** `10^9 + 7`.

**Note:** A stepping number should not have a leading zero.

```
low = "1", high = "11"     ->  10
low = "90", high = "101"   ->  2
```

**Constraints:** `1 <= int(low) <= int(high) < 10^100`; `1 <=
low.length, high.length <= 100`; `low` and `high` consist of only
digits and don't have any leading zeros.

## Approaches

The bounds have up to 100 digits, so the numbers are never enumerated:
each arm counts by digits, carrying only the last digit and how the
prefix stands against a bound.

| file | mechanism |
|---|---|
| `stepping.kara` ★ | a recursive digit walk to a bound, carrying the last digit, whether the prefix still equals the bound's and whether the number has started, the free started states memoized in a `Vec[Vec[i64]]` by place and last digit; the range is the count to high less the count to low, and low when it steps |
| `stepping_table.kara` | a table `ways[l][d]` of stepping strings of l digits starting with d; every number of fewer digits, then along the bound's digits while they step every smaller digit that steps, each finished from the table; the range is to high less to low - 1, low decreased digit by digit |
| `stepping_layers.kara` | forward, a layer per digit: the counts already below the bound's prefix by last digit, moved to their neighbours, with the digits under the bound's that step from the prefix and a new number started at every place past the first |
| `stepping_pair.kara` | both bounds in one walk, low padded with zeros to high's length, a memoized method on a `Walk` struct carrying whether the prefix still equals low's and high's, memo keyed by a tuple in a `Map`; no subtraction |
| `stepping_solution.kara` | a Rust solution as LeetCode's Rust users write it, with nested `fn dfs` and `fn calc` inside the method, a `vec![vec![-1i64; 10]; n]` memo and low's own check by `windows(2)`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; 1 to
10^100 - 1, LeetCode's widest; a range of one 100-digit stepping
number; the 100-digit numbers; 3000 random ranges within 1 to 10^4;
and 50 of up to 100 digits, every other one made mostly of steps, the
last two with the sum of the counts and a checksum. `stepping.py`
mirrors the ★ arm and its output is byte-identical.

```
10
2
125046265
1
515855978
3000 ranges up to 10^4: counts sum to 80752, checksum 611136309
50 ranges of up to 100 digits: counts sum to 20298646729, checksum 552251160
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every number from low to high in turn, its digits written
out and each next to the one before checked to differ by exactly 1; no
digit walk and no table. It draws 2000 random triples of numbers from 1
to 1000, then 50 of up to 100 digits, every other one made mostly of
steps, each triple sorted into low, mid and high, all before any arm
answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 1000, the count is the literal reading's |
| P2 | low to mid and mid to high: the count, mid counted once |
| P3 | from 1 to high less from 1 to low, and low when it steps: the count |
| P4 | low to low: 1 when low steps, else 0 |
| P5 | from 0 to 10^9 + 6, and high to high as P4 for high |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 980715550, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the tight prefix memoized with the free ones | P1 355, P6 384 |
| M2 | ★: low itself never counted | P1 227, P2 81, P3 235, P4 235, P5 76, P6 235 |
| M3 | table: a digit stepping only upward | P1 1997, P2 59, P3 88, P4 88, P5 53, P6 2047 |
| M4 | table: the walk going on past a digit that does not step | P1 1239, P2 612, P3 628, P4 628, P5 580, P6 1289 |
| M5 | table: a borrow stopping at the first zero | P5 6 |
| M6 | layers: no new number started past the first place | P1 584, P6 634 |
| M7 | layers: the bound itself counted whether it steps or not | P1 285, P6 293 |
| M8 | pair: low's prefix let go whatever the digit | P1 1675, P2 1274, P3 1725, P4 1404, P5 788, P6 1725 |
| M9 | pair: a leading zero starting the number | P1 581, P2 101, P3 630, P6 631 |
| M10 | solution: the steps checked up to 2, not exactly 1 | P1 1992, P6 2042 |

## Benchmarks

The bench draws 400 ranges whose bounds have 100 digits, LeetCode's
longest, made mostly of steps, all of them first, then answers each 20
times by the ★ arm in all five languages, each answer with a fresh memo.
Every implementation prints `400 ranges of 100 digits, 20 rounds:
counts sum to 3883096832740, checksum 145493987`.

BENCHTAB

## Verification

All five arms print the same output as `stepping.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The harness first
wrote `f"1{"0".repeat(99)}"` inside another f-string's hole, which
`karac check` warns is deprecated (design.md §3) with no machine fix;
it is bound to `top` first now, as the warning says.

LeetCode's Rust template took 43 `karac fix` edits, the wrapper
included. The largest were structural: the nested `const MOD`, `fn dfs`
and `fn calc` were hoisted above `impl Solution`, Kāra having no nested
items, and `struct Solution {}` was added. The rest were spellings:
`usize` became `i64`; `&Vec<usize>` became `ref Vec[i64]` and `&mut
Vec<Vec<i64>>` became `mut ref Vec[Vec[i64]]`, with `mut memo` at the
calls; `vec![vec![-1i64; 10]; n]` became `Vec.filled(n, Vec.filled(10,
-1))`; `&str` became `Str`; `!` became `not` and `&&` became `and`;
`.bytes().map(...)` took `.iter()` and `as_bytes().windows(2)` became
`bytes().windows(2).into_iter()`; the `&` on arguments was dropped; and
`Solution::` became `Solution.`, the wrapper's `as i64` dropped.
