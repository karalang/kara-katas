# 2154. Keep Multiplying Found Values by Two

You are given an array of integers `nums`. You are also given an integer
`original` which is the first number that needs to be searched for in
`nums`.

You then do the following steps:

1. If `original` is found in `nums`, **multiply** it by two (i.e., set
   `original = 2 * original`).
2. Otherwise, **stop** the process.
3. **Repeat** this process with the new number as long as you keep
   finding the number.

Return *the **final** value of* `original`.

```
nums = [5, 3, 6, 1, 12], original = 3  ->  24
nums = [2, 7, 9],        original = 4  ->  4
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i], original <=
1000`.

The value only doubles, so what matters is which of its doubles the list
holds: a set of the numbers answers each search at once. O(n + log of
the greatest number).

## Approaches

| file | mechanism |
|---|---|
| `doubling.kara` ★ | the numbers `collect`ed into a `Set[i64]`, and the value doubled while the set `contains` it |
| `doubling_sorted.kara` | no set: the numbers sorted, and one walk that doubles the value each time the number met is the value, since the value only grows and is sought in rising order |
| `doubling_bits.kara` | a mask: each number that is the start times 2^k sets bit k, and the value stops at the start shifted by the mask's `trailing_ones` |
| `doubling_struct.kara` | a `struct Ledger` of how many times each number was met, a `Map[i64, i64]` made `of` the list, that `has` a value (`ref self`) and `follow`s a start up its chain of doubles |
| `doubling_rec.kara` | the statement as a recursion over the list itself: if the list `contains` the value, the answer from its double, otherwise the value |
| `doubling_solution.kara` | LeetCode's Rust template: a `mut original: i32` parameter, a `HashSet<i32>` collected by `into_iter`, `contains(&original)`, `struct Solution;`, `Solution::`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one number found, every power of two from 1, a chain broken at its
first step, and the constraints' greatest found), each with its final
value; then the total and a checksum over 2000 random lists of 1 to 15
numbers, of 1 to 16 and of a start's chain in part shuffled among
others in turn; then the constraints' largest, 1000 numbers: every
number from 1, every number but 512, and at random. `doubling.py`
mirrors the ★ arm and its output is byte-identical.

The bits arm's `trailing_ones` was at first refused, "no method
'trailing_ones' on type 'i64'", though Kāra had the other four bit
counts Rust has; that is ledger row B-2026-11-15-27, fixed in karac b545bd3ba1, which
gives every integer `trailing_ones` and `leading_ones` as `i64`.

`karac fix` carries the template in three rounds of 14, 1 and 3 edits:
Rust's spellings (the `use` dropped, `Vec<i32>` and `HashSet<i32>` to
`[..]`, the `mut original: i32` parameter to `original: i32` and a `let
mut original = original;` at the top of the body, `contains(&original)`
to `contains(original)`, `struct Solution;` to `struct Solution {}`, the
adapter's `&Vec<i64>` to `ref Vec[i64]`, its closure's `&x` to `x`, and
`Solution::` to `.`, among them); then `HashSet` to `Set`, once the `use`
that named it is gone; then a `.clone()` before `into_iter()`, since a
parameter is borrowed, the adapter's `ref` dropped, and its widening `as
i64` dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the list searched from its start for the value, and on each
find the value doubled and the search begun again. No set, sort or
mask. It checks 300 random lists of 1 to 10 numbers of 1 to 8 or 1 to
40 in turn, each with a start of 1 to 5; then 30 holding the start's
chain of doubles in part, shuffled; then 30 without the start's double.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the final value is the statement read literally |
| P2 | the list reversed: the same |
| P3 | every number and the start tripled: three times the final value |
| P4 | the final value itself taken as the start: the same |
| P5 | the final value added to the list: the final value from twice it |
| P6 | each arm agrees with at least three of the other five |

P2 holds since the search asks only whether the list holds a value. P3
holds since the tripled list holds 3v exactly when the list holds v.
P4 holds since the final value is not in the list. P5 holds since the
added number lets the chain take one step more, and the values from
there on are all greater than it.

The differential prints `360 lists: checksum 42379482, 12960 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers was checked against a Python reading of the same
lists. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Twenty-eight edits to the differential, five to each Kāra arm and three
to the template, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: one double at most | P1 45, P4 45, P5 169, P6 45 |
| M3 | ★: the first number left out of the set | P1 31, P2 50, P6 31 |
| M4 | ★: the last double undone | P1 132, P5 323, P6 132 |
| M6 | sorted: never sorted | P1 24, P2 35, P4 24, P5 68, P6 24 |
| M8 | sorted: a number matched when the value is at least it and under its double | P1 96, P6 96 |
| M10 | sorted: the last number never met | P1 25, P5 55, P6 25 |
| M11 | bits: the mask's bits counted, not its trailing run | P1 121, P4 121, P5 121, P6 121 |
| M13 | bits: any multiple of the start taken as a power of two | P1 148, P5 25, P6 148 |
| M14 | bits: each bit set one place up | P1 132, P5 360, P6 132 |
| M18 | struct: the chain followed from the start's double | P1 228, P4 360, P5 313, P6 228 |
| M19 | struct: a value had when its half was met | P1 173, P3 20, P5 320, P6 173 |
| M20 | struct: the chain stopped at 100 | P3 4, P5 1 |
| M22 | rec: an odd miss answered doubled | P1 140, P4 22, P5 140, P6 140 |
| M24 | rec: the list asked for the double | P1 169, P5 360, P6 169 |
| M25 | rec: a find handing down four times the value | P1 100, P5 360, P6 100 |
| M27 | solution: the set of the numbers' doubles | P1 153, P5 360, P6 153 |
| M28 | solution: the adapter's numbers halved | P1 190, P3 51, P5 360, P6 190 |

P1 and P6 kill sixteen, P5 fifteen, P4 five, P3 three and P2 two. The
chain stopped at 100 (M20) is seen by no lifted check: the differential's
lists hold numbers up to 50, so no chain in them reaches 100. P3 triples
every number and P5 adds the final value, and each takes a chain past
it. P5 asks for one more step of the chain, and sees almost every edit
that takes a step wrong; it misses the ★ arm's first number left out
(M3) and the sorted arm's loose match (M8), whose errors stay the same
one step on. P4 starts from the arm's own answer, and sees an edit that
answers a value the list still holds, or that does not stop at once at
a start the list lacks: one double at most (M2), the unsorted walk
(M6), the bits counted (M11), the chain followed from the double (M18),
and the odd miss doubled (M22). P3 sees an edit that reads a number's size:
the stop at 100 (M20), the half (M19), and the halving that rounds
(M28). P2 reverses the list, and sees the edits that care where a
number stands: the first left out (M3) and the walk unsorted (M6).

Of the twenty-eight, eleven were not kept. One is equivalent: the sorted
arm's walk stopped at the first number greater than the value (M9),
since every number after it is greater still and the value no longer
changes. One crashes: the bits arm reading the mask's trailing zeros
(M12) shifts by 64 on a list that holds neither the start nor any
of its doubles. Eight fail as a kept one
does: the ★ arm's value tripled, the bits arm's leading ones of the mask
moved to the top, and the recursion's double handed down tripled, as
M14; the ★ arm asking the set for the double, as M24; the sorted arm
sorted falling and the recursion's find answered with its double, as
M2; the struct arm's numbers counted under their doubles, as M27; and
the template's adapter start doubled, as M18. One was left out to keep
three to an arm: the struct arm's value had only when met twice (M16).

## Verification

Every arm prints the same output as `doubling.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s to 0.3 s, and the
differential 0.3 s.

## Benchmarks

The bench builds one row of 400000 numbers from 1 to 1000 once; then
solves 20000 windows of 1000 numbers, the constraints' longest, each at
a random start and with a start value of 1 to 1000 at random, so that no
solve repeats one before, with the ★ arm in all five languages: each
collects its window into a hash set (an open-addressing table in C). C
works over a pointer and a length, the others over a slice. Every
implementation prints `20000 solves: checksum 985264386`.

BENCHTAB
