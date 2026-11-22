# 2844. Minimum Operations to Make a Special Number

You are given a **0-indexed** string `num` representing a non-negative
integer.

In one operation, you can pick any digit of `num` and delete it. Note
that if you delete all the digits of `num`, `num` becomes `0`.

Return *the **minimum number of operations** required to make* `num`
*special*.

An integer `x` is considered **special** if it is divisible by `25`.

```
num = "2245047"  ->  2
num = "2908305"  ->  3
num = "10"       ->  1
```

**Constraints:** `1 <= num.length <= 100`; `num` only consists of
digits `'0'` through `'9'`; `num` does not contain any leading zeros.

## Approaches

| file | mechanism |
|---|---|
| `special.kara` ★ | a multiple of 25 ends in 00, 25, 50 or 75, or is 0 itself: one pass from the right, a 0 or 5 met after a 0, or a 2 or 7 after a 5, ends the number there; with no such pair a lone 0 is kept if there is one, and otherwise every digit goes |
| `special_endings.kara` | each of the four endings in turn: its last digit's rightmost place by `rposition`, then its first digit's rightmost place before that by `rposition` over the slice, and the fewest deletions over the endings, a lone 0 and deleting everything |
| `special_remainder.kara` | a dynamic programme over remainders mod 25: the most digits a subsequence read so far keeps for each remainder, the empty one keeping none for 0, each digit joining every subsequence or not, `to_digit(10)` reading it |
| `special_pairs.kara` | every pair of places i < j whose two digits make a multiple of 25 tried as the number's last two, by `flat_map` over the pairs, `filter`, `map` and `min()`; O(n^2), for LeetCode's 100 digits |
| `special_solution.kara` | a Rust solution as LeetCode's Rust users write it: the number's `as_bytes()`, `contains(&b'0')` for a lone 0, and for each ending an `if let Some(j)` from `rposition(\|&c\| c == b)`, the answer as `i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's three examples; one or
two digits of each kind; 100 digits, LeetCode's most, with no 0, 2, 5
or 7, and then ending in 25; then 3000 random numbers of 1 to 8 digits
mostly from 0, 5, 2 and 7, and 300 of up to 100 digits from all ten,
as totals and checksums. `special.py` mirrors the ★ arm and its output
is byte-identical.

```
2 3 1
0 1 0 0 2
100 0
3000 short numbers: 6145 operations, checksum 517971269
300 long numbers: 2045 operations, checksum 128539356
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every set of digits to keep, by a bitmask, the kept
digits read as a number (none kept reading as 0), and the fewest
deletions that leave a multiple of 25. It draws 2000 random numbers of
1 to 10 digits mostly from 0, 5, 2 and 7, then 50 of up to 100 digits
from all ten, all before any arm answers; the literal reading is asked
only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 digits, the answer is the literal reading's |
| P2 | 1 and 3, 4 and 6, 8 and 9 swapped, digits no ending uses: the same answer |
| P3 | 25 written after the number: no operation |
| P4 | a 1 written before it: the same answer or one more |
| P5 | at most the count of digits, and that only with no 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 112422053, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 75 not an ending | P1 250, P6 260 |
| M2 | ★: a lone 0 not kept | P1 236, P5 236, P6 236 |
| M3 | ★: the kept digit counted as deleted | P1 1193, P3 2050, P6 1238 |
| M4 | endings: 00 not an ending | P1 278, P6 293 |
| M5 | endings: the first digit looked for at or after the last | P1 978, P6 1004 |
| M6 | remainder: a digit always joined | P1 1663, P4 45, P5 1712, P6 1712 |
| M7 | remainder: the remainder kept mod 5 | P1 1022, P6 1061 |
| M8 | pairs: the digits between the pair left in | P1 599, P6 638 |
| M9 | pairs: a lone 0 not counted | P1 236, P5 236, P6 236 |
| M10 | solution: the ending searched from the left | P1 648, P3 1344, P6 687 |

## Benchmarks

The bench draws 10^5 numbers of 1 to 100 digits, LeetCode's most, all
of them first, then answers each 300 times by the ★ arm in all five
languages. Every implementation prints `100000 numbers, 300 rounds:
214629300 operations, checksum 394044903`.

BENCHTAB

## Verification

All five arms print the same output as `special.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The pairs arm, as first written, gave its inner closure Rust's `move`,
`(i + 1..n).map(move |j| (i, j))`, and `karac check` reported
E_MOVE_NOT_USED, "the `move` keyword is not used in Kāra: delete it";
`karac fix` deleted it. The other arms checked clean.

LeetCode's Rust template took 8 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`;
`as_bytes()` became `bytes()`; `contains(&b'0')` lost its `&`, and both
`|&c|` theirs; in the wrapper `&str` became `Str`, `Solution::` took
`.`, and the `as i64` went. The `if let Some(i) =
s[..j].iter().rposition(..)` over a slice, and the narrowing `i as i32`
and `s.len() as i32`, were accepted as written.
