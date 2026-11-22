# 2827. Number of Beautiful Integers in the Range

You are given positive integers `low`, `high`, and `k`.

A number is **beautiful** if it meets both of the following
conditions:

- The count of even digits in the number is equal to the count of odd
  digits.
- The number is divisible by `k`.

Return *the number of beautiful integers in the range* `[low, high]`.

```
low = 10, high = 20, k = 3  ->  2
low = 1,  high = 10, k = 1  ->  1
low = 5,  high = 5,  k = 2  ->  0
```

**Constraints:** `0 < low <= high <= 10^9`; `0 < k <= 20`.

## Approaches

| file | mechanism |
|---|---|
| `beautiful.kara` ★ | a digit DP, the count up to high less the count up to low - 1: walking the bound's digits, the state is the place, evens less odds, the remainder mod k, whether the prefix still sits on the bound and whether a digit has started; the free started states memoized in a flat `Vec` |
| `beautiful_free.kara` | free suffixes: a `Table` struct, built one length at a time, of the digit strings of each length by balance and remainder; a count up to a bound adds the shorter numbers by their first digit, then walks the bound, each smaller digit at a place leaving a free suffix to look up |
| `beautiful_halves.kara` | halves: a balanced number has 2h digits, a high half and a low half; a table of the low halves by balance and remainder pairs with every high half that cancels them, and at the bound's own length the bound's high half is checked against each low half up to the bound's, one by one |
| `beautiful_map.kara` | both bounds at once: one digit DP over high's digits, low padded with zeros to the same length, the state carrying whether the prefix sits on low and on high, every state memoized in a `Map` keyed by a tuple |
| `beautiful_solution.kara` | a Rust solution as LeetCode's Rust users write it: a digit DP over `n.to_string().bytes()` with `is_limit` and `is_lead`, the balance offset by the length as a `usize`, a `vec![vec![vec![-1i32; k]; ..]; len]` memo passed `&mut`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; the
whole range from 1 to 10^9 for k = 1, 7 and 20; 1234 alone; the
six-digit band for k = 3; 300 random ranges up to 10^9 and 300 of up to
1000 numbers, with k from 1 to 20, as checksums. `beautiful.py` mirrors
the ★ arm and its output is byte-identical; a Python scan of every
number from 100000 to 999999 gives the band's 93760.

```
2
1
0
24894045
3556292
1105750
1
93760
300 wide ranges: checksum 187964012
300 narrow ranges: checksum 473438012
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every number from low to high, its digits counted even
and odd, kept when the counts are equal and k divides it. It draws
2000 random ranges of up to 2000 numbers, each starting below a random
power of ten up to 10^9, then 50 ranges up to 10^9, with k from 1 to
20, all before any arm answers; the literal reading is asked only of
the first 2000.

| | property |
|---|---|
| P1 | up to 2000 numbers, the answer is the literal reading's |
| P2 | the range cut in two at a random point inside it: the two answers sum to the answer |
| P3 | k = 1: no fewer |
| P4 | at least 0, and at most the multiples of k in the range |
| P5 | from 1 to high less from 1 to low - 1: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 464640932, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a leading zero counted as an even digit | P1 575, P3 105, P4 115, P6 587 |
| M2 | ★: the count taken from low, not low - 1 | P1 75, P2 69, P5 77, P6 77 |
| M3 | free: the shorter numbers left out | P1 397, P3 106, P4 106, P6 409 |
| M4 | free: the bound itself never counted | P1 104, P6 105 |
| M5 | halves: the high halves stopping one short of the bound's | P1 707, P3 22, P4 42, P6 720 |
| M6 | halves: the low halves below the bound's own | P1 104, P6 105 |
| M7 | map: the low flag dropped after the first digit | P1 984, P2 1039, P4 509, P5 999, P6 999 |
| M8 | map: the remainder never carried | P1 985, P4 2, P6 995 |
| M9 | solution: the shorter numbers never tried | P1 397, P3 106, P4 106, P6 409 |
| M10 | solution: a leading zero let in | P1 408, P4 15, P6 409 |

## Benchmarks

The bench draws 2000 random ranges up to 10^9, LeetCode's most, with k
from 1 to 20, all of them first, then answers each 5 times by the ★ arm
in all five languages, the memo allocated afresh for every bound as the
arm does. Every implementation prints `2000 ranges, 5 rounds:
7311262345 beautiful, checksum 672338573`.

BENCHTAB

## Verification

All five arms print the same output as `beautiful.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the four own arms checked clean as first written. The map arm
gave its recursive method a `mut self` receiver, Rust's spelling, and
`karac check` reported E0001, naming `mut ref self`; `karac fix` wrote
it. It also padded low to high's length as Rust's `{:0>w$}` does,
`f"{low:0>{hi.len()}}"`; Kāra's format spec takes only a literal width
(design.md §3 Format specifiers, `width := DIGIT+`), so the arm pads
by `"0".repeat(..)`, and the diagnostic, "unsupported type `{`
(expected one of x, X, o, b, d)", reads the nested hole as a type
letter instead of saying a computed width is not in v1. It is not in the kara ledger yet: the kata rows are at their cap, so
the row waits for a free slot.

LeetCode's Rust template took 45 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; every
`Self::` became `Solution.`; `bytes().collect()` took the
`.iter()`; the nested `vec![..; n]` became nested `Vec.filled`;
`usize` became `i64` and the `as usize` casts on `rem` went, an `i32`
index widening; `&[u8]` became `Slice[u8]` and `&mut Vec<..>` `mut ref
Vec[..]`, the calls passing `s` and `mut memo`; `!`, `&&` became
`not`, `and`; `let mut res = 0` took `: i32`, its `+=` of `i32`
results leaving the literal at `i64` by design (design.md §8) where
the return wants `i32`; and the wrapper's `as i64` went.
