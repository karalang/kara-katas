# 2745. Construct the Longest New String

You are given three integers `x`, `y`, and `z`.

You have `x` strings equal to `"AA"`, `y` strings equal to `"BB"` and
`z` strings equal to `"AB"`. You want to choose some (possibly all or
none) of these strings and concatenate them in some order to form a new
string. This new string must not contain `"AAA"` or `"BBB"` as a
substring.

Return *the maximum possible length of the new string*.

A **substring** is a contiguous **non-empty** sequence of characters
within a string.

```
x = 2, y = 5, z = 1  ->  12    "BB" "AA" "BB" "AA" "BB" "AB"
x = 3, y = 2, z = 2  ->  14    "AB" "AB" "AA" "BB" "AA" "BB" "AA"
```

**Constraints:** `1 <= x, y, z <= 50`.

## Approaches

"AA" can be followed only by "BB", and "BB" by "AA" or "AB", so the
"AA"s and "BB"s alternate: all of the fewer kind and one more of the
other, or all of both when there are as many. Every "AB" fits in a run
of them at the front, so all of them are used.

| file | mechanism |
|---|---|
| `longest.kara` ★ | the closed form: `2 x` when `x == y`, else `2 min(x, y) + 1`, pieces of 2 letters with the `z` "AB"s added. O(1) |
| `longest_greedy.kara` | the string built: one "BB" in front when there are more "BB"s, then every "AB", then "AA" and "BB" by turns until the piece due runs out; the answer is its `len()`. O(x + y + z) |
| `longest_memo.kara` | top down over the pieces left and the last piece placed, an `enum Piece { Aa, Bb, Ab, Start }`, with a `struct Builder` holding a flat memo and the rule of which piece may follow which as `match` arms. O(x y z) |
| `longest_table.kara` | the same recurrence bottom up, from no pieces left upward, the last piece as 0 to 3, flat in one `Vec` through an index closure. O(x y z) |
| `longest_solution.kara` | a Rust solution as LeetCode's Rust users write it, the closed form with `std::cmp::min` and an `if` on `x == y`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one of
each; as many "AA" as "BB"; LeetCode's largest counts; every count from
1 to 12 of each piece; and 100 random counts up to 50, the last two with
the sum of the lengths and a checksum. `longest.py` mirrors the ★ arm
and its output is byte-identical.

```
12
14
6
34
300
1728 small counts: lengths sum to 56832, checksum 718098111
100 counts up to 50: lengths sum to 11464, checksum 41849233
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every sequence of the pieces, one at a time, the string built
and searched further only while it holds no "AAA" and no "BBB", with the
longest string reached kept; no rule about which piece may follow which.
It takes every count from 1 to 4 of each piece, then 1000 random counts
up to 20, all before any arm answers; the literal reading is asked only
of the first 64.

| | property |
|---|---|
| P1 | counts up to 4, the answer is the literal reading's |
| P2 | the counts of "AA" and "BB" swapped: the same answer |
| P3 | one more "AB": 2 longer |
| P4 | one more "AA" and one more "BB": 4 longer |
| P5 | even, at most every piece used, and at least every "AB" used |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1064 cases: checksum 375088059, 31920 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same search gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M2 and M9 fail the same checks, both one piece
short when there are as many "AA"s as "BB"s.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: unequal counts given no extra piece | P1 48, P6 1001 |
| M2 | ★: equal counts one piece short | P1 16, P6 63 |
| M3 | greedy: the leading "BB" only when two more | P1 12, P2 115, P6 56 |
| M4 | greedy: the turn never handed to "BB" | P1 60, P2 886, P4 1064, P6 1037 |
| M5 | memo: an "AB" remembered as an "AA" | P1 52, P2 1001, P3 1008, P5 207, P6 1030 |
| M6 | memo: "BB" stored in "AA"'s slot | P1 12, P2 891, P4 64, P6 428 |
| M7 | table: no "BB" at the start | P1 24, P2 1001, P6 492 |
| M8 | table: an "AA" counted as one letter | P1 64, P2 1001, P4 1064, P5 537, P6 1064 |
| M9 | solution: equal counts one "AB" short | P1 16, P6 63 |
| M10 | solution: the larger count alternated | P1 48, P5 1001, P6 1001 |

## Benchmarks

The ★ arm is a formula with nothing to time, so the bench times the
table arm: it draws 1000 random counts up to 50, LeetCode's most, all of
them first, then answers each 3 times by the table in all five
languages, each allocating its flat table once a call. Every
implementation prints `1000 counts, 3 rounds: lengths sum to 357444,
checksum 422097129`.

BENCHTAB

## Verification

All five arms print the same output as `longest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, greedy and table arms checked clean as first written.

The memo arm was first written as Rust would have it: variants `AA`,
`BB` and `AB`, and `matches!(last, Piece.AA)` for the rule. `karac fix`
wrote each `matches!` as `match last { Piece.AA => true, _ => false }`;
the variant names are Const class in Kāra, and `karac check` named the
rename to `Aa` with no fix. That gap was kara `B-2026-11-20-142`, fixed
at `0d28296389`: a private enum's variants are now renamed by `karac fix`
at every use, and the arm reads `Aa`, `Bb` and `Ab`.

LeetCode's Rust template took 4 `karac fix` edits, the wrapper
included: `struct Solution {}` added, `std::cmp::min` became `min`, and
`Solution::` became `Solution.` with the wrapper's `as i64` dropped.
