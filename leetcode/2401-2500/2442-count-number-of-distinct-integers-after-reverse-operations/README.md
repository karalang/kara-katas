# 2442. Count Number of Distinct Integers After Reverse Operations

You are given an array `nums` consisting of **positive** integers.

You have to take each integer in the array, **reverse its digits**, and
add it to the end of the array. You should apply this operation to the
original integers in `nums`.

Return *the number of **distinct** integers in the final array*.

```
nums = [1,13,10,12,31]  ->  6
nums = [2,2,2]          ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^6`.

A reversal drops any trailing zeros, which become leading ones, so it
is never longer than the value and lies from 1 to `10^6` too. The answer
is the number of distinct values among the `2n`, which a table of flags
over that range counts in one pass.

## Approaches

| file | mechanism |
|---|---|
| `distinct.kara` ★ | each value's digits reversed by `% 10` and `/ 10`, and a table of flags up to the largest of the `2n` values, each counted the first time its flag is set. O(n log V) |
| `distinct_sorted.kara` | the `2n` values sorted, and counted where each differs from the one before. O(n log n) |
| `distinct_set.kara` | a `Set[i64]` of each value and its reversal, the reversal recursive with the number so far carried down; the set's size is the answer, and it is never walked. O(n log V) expected |
| `distinct_text.kara` | the reversal as text: the value written by an f-string, its bytes reversed and read back by `i64.parse`, so a trailing zero drops away; the values in a `SortedSet[i64]`. O(n log V log n) |
| `distinct_iter.kara` | iterators: the values chained with their reversals and collected into a `Set[i64]`, each reversal a `fold` over the digits by `successors`. O(n log V) expected |
| `distinct_solution.kara` | LeetCode's Rust template: `use std::collections::HashSet`, `HashSet::new()`, `for &x in &nums` with each reversal made in place, and `s.len() as i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; `10^6`, the
constraints' largest; 100, 1 and 10, whose reversals all meet; four
palindromes; then `10^5` values, the constraints' most: every value
from 1 to `10^5`, every multiple of 10 up to `10^6`, and random from 1 to
`10^6`; and 3000 random arrays of 1 to 10 values from 1 to 200, as a
checksum and the total. `distinct.py` mirrors the ★ arm and its output
is byte-identical, and the mirror was checked on 30000 random arrays of
1 to 12 values against a Python set of each value and its reversed
decimal text.

`check` first reports 7 errors on the template, and `karac fix` carries
it in one call, reporting 13 edits: the line `use
std::collections::HashSet` deleted, since `Set` is in Kāra's prelude;
the brackets of `Vec<i32>` and `HashSet<i32>`, and `HashSet` written
`Set`; `HashSet::new` written with a `.`; the `&` dropped from the
pattern `&x` and `&nums` written `ref nums`; `struct Solution;` given its
braces; and, once the template parses, `r` declared `r: i32`, its
literal `0` otherwise keeping the default `i64` against the `i32` digits,
and the harness's `as i64` on the `i64` the template returns. `s.len()
as i32` stands as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the array extended by each value's reversal, the digits read
from the top by dividing by powers of ten and written back from the
bottom, and then every element counted that equals none before it. No
table, sort or set is used. It checks 300 random arrays of 1 to 10
values from 1 to 200; then 30 of 50 to 300 values from 1 to `10^6`; then
30 of 1 to 40 values `d * 10^e`, `d` from 1 to 20 and `e` from 0 to 4,
full of trailing zeros. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the array reversed: the same answer |
| P3 | the array written twice: the same answer |
| P4 | the answer is at least the number of distinct values, and at most twice it |
| P5 | a random value's reversal appended, when that value ends in a nonzero digit: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 and P3 hold because the answer depends only on which values occur.
P4 holds because each distinct value adds at most one more by its
reversal. P5 holds because a value with no trailing zero is its own
reversal's reversal, so the new value and its reversal are both there
already.

The differential prints `360 cases: checksum 889384617, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts a set of each value and its reversed decimal
text. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every other digit skipped | P1 216, P5 255, P6 216 |
| M4 | ★: no flag ever set | P1 210, P3 360, P4 48, P5 306, P6 210 |
| M5 | ★: the count started at 1 | P1 360, P4 162, P6 360 |
| M7 | sorted: never sorted | P1 69, P2 6, P3 358, P4 34, P5 291, P6 69 |
| M9 | sorted: neighbours one apart counted once | P1 103, P6 103 |
| M11 | sorted: the second value never compared | P1 276, P3 276, P5 58, P6 276 |
| M12 | set: each digit placed a place up | P1 248, P5 255, P6 248 |
| M15 | set: one fewer counted | P1 360, P4 4, P6 360 |
| M16 | set: the values themselves left out | P1 356, P4 34, P5 254, P6 356 |
| M19 | text: each reversal ten times over | P1 212, P5 255, P6 212 |
| M20 | text: only the end digits swapped | P1 52, P5 26, P6 52 |
| M21 | text: each value a tenth | P1 207, P5 254, P6 207 |
| M22 | iter: the last two digits kept together | P1 187, P5 254, P6 187 |
| M24 | iter: the first value left out | P1 297, P2 94, P3 297, P5 68, P6 297 |
| M25 | iter: each value reversed twice | P1 342, P5 254, P6 342 |
| M28 | solution: each digit the one above it | P1 215, P5 255, P6 215 |
| M29 | solution: the reversal stopped above 10 | P1 202, P5 254, P6 202 |


P1 and P6 kill all seventeen, P5 fourteen, P4 five, P3 four and P2
two.

Fourteen are not kept. Eight fail exactly as a kept one: the ★ and set
arms' top digit dropped and the sorted arm's each reversal a tenth (M6,
M14, M10) as the template's reversal stopped above 10 (M29), each
losing the reversal's last digit, which is the value's first; the
sorted arm's count started at 0 and the template's one fewer counted
(M8, M30) as the set arm's one fewer counted (M15); the text arm's and
the template's values themselves left out (M18, M27) as the set arm's
(M16); and the iter arm's each digit the one above it (M23) as the
template's (M28). Four more fall into two pairs that fail alike and
apart from every kept one, and neither is kept: the ★ arm's each value
pushed again and the text arm's never reversed (M3, M17), both counting
only the values; and the set and iter arms' reversal started at 1 (M13,
M26), both putting a 1 in front of every reversal. The ★ arm's digits
summed (M2) fails apart from every kept one and was left out because
that arm keeps its share already.

One ends in an integer overflow, not a wrong answer, under both
backends: the template's reversal started at the value (M31) puts the
value in front of its own reversal, which passes the `i32` the template
keeps it in for any value of five digits or more.

## Verification

Every arm prints the same output as `distinct.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.4 to 5.2 s, but for the text
arm, which takes 43 s there against 0.4 s under `karac __mir-llvm-run`,
1.3 s under `karac __mir-llvm-asan` and 0.8 s under `karac run`: the
interpreter's `SortedSet` shifts every later entry on an insert
(B-2026-11-21-50), and `2 * 10^5` inserts in random order make that
quadratic. The differential takes 10.4 s under `karac __mir-run`, 2.3 s
under `karac __mir-llvm-asan` and 0.8 s under `karac run`.

## Benchmarks

The bench builds 4 arrays of `10^5` values from 1 to `10^6`, the
constraints' largest, once from its own generator. It then makes 40
passes; each sets one value of every array, so no answer can be carried
from one pass to the next, then answers every array, folding the answer
plus the pass into the checksum. The bench uses the ★ arm, the
arithmetic reversal and the table of flags, in all five languages, each
answer allocating its list of `2n` values and its table afresh. Every
implementation prints `40 passes over 4 arrays of 10^5 values: checksum
396428331`.

BENCHTAB
