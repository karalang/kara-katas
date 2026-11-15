# 2191. Sort the Jumbled Numbers

You are given a **0-indexed** integer array `mapping` which represents
the mapping rule of a shuffled decimal system. `mapping[i] = j` means
digit `i` should be mapped to digit `j` in this system.

The **mapped value** of an integer is the new integer obtained by
replacing each occurrence of digit `i` in the integer with `mapping[i]`
for all `0 <= i <= 9`.

You are also given another integer array `nums`. Return *the array*
`nums` *sorted in **non-decreasing** order based on the **mapped
values** of its elements.*

**Notes:**

- Elements with the same mapped values should appear in the **same
  relative order** as in the input.
- The elements of `nums` should only be sorted based on their mapped
  values and **not be replaced** by them.

```
mapping = [8, 9, 4, 0, 2, 1, 3, 5, 7, 6], nums = [991, 338, 38]  ->  [338, 38, 991]
mapping = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], nums = [789, 456, 123] ->  [123, 456, 789]
```

**Constraints:** `mapping.length == 10`; `0 <= mapping[i] <= 9`; all the
values of `mapping[i]` are unique; `1 <= nums.length <= 3 * 10^4`;
`0 <= nums[i] < 10^9`.

Each number's mapped value is worked out once, and the numbers sorted by
it with a stable sort, or by the pair of it and the number's place.
Since the mapping is a permutation, two different numbers map alike only
when a leading digit maps to 0 and vanishes: with 1 sent to 0, 15 and 5
both map to the same value. O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `jumbled.kara` ★ | each number's mapped value worked out once, digit by digit from the last, kept with its place as a pair; the pairs `sort`ed, so a tie keeps the order of the places, and the numbers read back |
| `jumbled_by_key.kara` | the numbers sorted in place by `sort_by_key`, the key worked out from the first digit; the sort is stable, so numbers that map alike keep their order |
| `jumbled_text.kara` | the mapped value read as text: the number written out by `to_string`, each `char` turned to its digit by `to_digit`, mapped, and back by `char.from_digit`, the text parsed by `i64.parse`; the (value, number) pairs sorted by `sort_by` on the value alone, stably |
| `jumbled_struct.kara` | a `struct Cipher` holding the mapping, which `encode`s a number by recursion (`ref self`); a `struct Coded` of each number's code, place and value, ordered by an `impl Ord for Coded` on the code and then the place, so a plain `sort` keeps ties in order |
| `jumbled_iter.kara` | the mapped value as one chain: a number's digits from the last by `successors`, each `map`ped, `zip`ped with the powers of ten from another `successors`, and `sum`med; the numbers `enumerate`d into (value, place, number), `collect`ed, sorted, and `map`ped out |
| `jumbled_solution.kara` | LeetCode's Rust template: `Vec<i32>`, a closure `\|mut x: i32\| -> i32` with `as usize` indexing, `let mut nums = nums`, and `nums.sort_by_cached_key(\|&x\| map(x))`, `struct Solution;`, `Solution::`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one number, a zero among others, numbers that map alike once their
leading 0s go, and 0 and 9 swapped), each with its sorted list; then the
first numbers' total and a checksum over 2000 random cases of 1 to 30
numbers below 10, 1000 and 10^9 in turn, each with a random mapping of
its own; then the constraints' longest, 30000 numbers below 10^9, by its
first, last and checksum. `jumbled.py` mirrors the ★ arm and its output
is byte-identical.

`karac fix` carries the template in three rounds of 12, 3 and 1 edits:
first Rust's spellings (`Vec<..>` to brackets, the closure's `mut x` to
a `let mut x = x` in its body and its `-> i32` dropped, the `&x`
pattern to `x`, `struct Solution;` to `struct Solution {}`, and
`Solution::` to `.`, among them); then the parameter that `let mut nums
= nums` takes marked `own`, the counter `r` typed `i32` to match the
closure's result, and `sort_by_cached_key` renamed to `sort_by_key`,
the same stable sort, whose key calls the library leaves unspecified
(kara B-2026-11-15-31, fixed at c93ef18010: before it the call was refused with
a bare "no method", though the interpreter and the backend already took
the name); then the counter `p` typed `i32` as well.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each number's mapped value its digits written out, each
replaced by the mapping and read back; the numbers then taken one at a
time, each time the first one left with the smallest mapped value. No
sort. It checks 300 random cases of 1 to 12 numbers below 10, 100 and
1000 in turn; then 30 of numbers below 20 with a mapping that sends 1
to 0, so a leading 1 vanishes and 1x ties x; then 30 of numbers below
10^9. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer holds the same numbers, as many times each |
| P3 | the answer's mapped values never fall, and the numbers of each mapped value come in their order in the list |
| P4 | the answer sorted again: the same answer |
| P5 | the list reversed: the answer with each run of one mapped value reversed |
| P6 | each arm agrees with at least three of the other five |

P3 is the statement's two rules, the order of the values and of the
ties, checked without the literal reading's answer. P4 holds since the
answer is already in order and a stable sort keeps it. P5 holds since
reversing the list reverses each tie's order and nothing else.

The differential prints `360 cases: checksum 542362090, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
cases. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five to each Kāra arm and six to
the template, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 0 mapped to 0 | P1 45, P3 45, P5 16, P6 45 |
| M2 | ★: the digits read back to front | P1 217, P3 217, P5 4, P6 217 |
| M4 | ★: the first digit left out | P1 300, P3 300, P5 195, P6 300 |
| M7 | key: the last digit dropped | P1 165, P3 165, P5 205, P6 165 |
| M8 | key: sorted largest first | P1 336, P3 336, P6 336 |
| M10 | key: sorted by the last digit's mapping | P1 195, P3 195, P5 149, P6 195 |
| M13 | text: the values compared as text | P1 129, P3 129, P6 129 |
| M14 | text: ties by the number | P1 11, P3 11, P5 15, P6 11 |
| M15 | text: the mapping one digit on | P1 302, P3 302, P5 4, P6 302 |
| M16 | struct: a single digit unmapped | P1 287, P3 287, P5 2, P6 287 |
| M19 | struct: the last digit weighted ten | P1 217, P3 217, P5 23, P6 217 |
| M20 | struct: ordered by the number | P1 290, P3 290, P5 1, P6 290 |
| M23 | iter: the mapped digits added up | P1 176, P3 176, P5 126, P6 176 |
| M24 | iter: the first digit left out | P1 191, P3 191, P5 79, P6 191 |
| M25 | iter: ties in reverse order of place | P1 15, P3 15, P4 15, P6 15 |
| M27 | solution: the adapter's mapping reversed | P1 302, P3 302, P5 7, P6 302 |
| M30 | solution: the adapter's answer reversed | P1 336, P3 336, P4 15, P6 336 |

P1, P3 and P6 kill all seventeen, P5 thirteen, P4 two and P2 none.
Every edit still hands back the numbers it was given, in some order, so
P2 has nothing to see; it guards the arms that copy and rebuild the
list. P4 sorts the answer again, and an edit that sorts stably by a
wrong key is already sorted by that key, so P4 kills only the two
orders no key gives: the ties reversed (M25) and the answer reversed
(M30). P5 reverses the list and expects each run of one mapped value
reversed, and misses the edits that still sort stably by something that
keeps the true ties together: largest first (M8), the values compared
as text (M13), and the same two, M25 and M30, whose runs come out
reversed as P5 expects. The ties are rare in random cases, since the
mapping is a permutation; the 30 cases below 20 with 1 sent to 0 are
what see them (M14, M25: 11 and 15 cases).

Of the thirty-two, fifteen were not kept. One is equivalent: the iter
arm's powers of ten from 10 (M22), which scales every value alike. One
crashes: the template's place stepping by 100 (M29), an `i32` overflow
on the 10^9 cases. Thirteen fail as a kept one does: the ★ and struct
arms' ties reversed (M3, M18) as M25; the ★, text and iter arms' numbers
sorted as they are, unmapped (M5, M11, M26), as M20; the key arm's and
the struct arm's leading digit dropped (M6, M21) as M24; the key arm's
mapped digits added up (M9) as M23; the text arm's text reversed (M12)
as M2; the struct arm's ties by the number (M17) as M14; and the
template's 0 mapped to 0 (M28), last digit dropped (M31) and key negated
(M32) as M1, M7 and M8.


## Verification

Every arm prints the same output as `jumbled.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, key, template and struct arms take 0.4 s
to 0.9 s, the text arm 1.8 s, which writes out and parses back every
number, and the iter arm 3.5 s, two `successors` chains a number. The
differential takes 2.1 s.

## Benchmarks

The bench builds one row of 10^6 numbers below 10^9 once; then solves
200 windows of 30000 numbers, the constraints' longest, each at a random
start and with a random mapping of its own, with the ★ arm in all five
languages. C sorts an array of (value, place) structs with `qsort`, Rust
a `Vec<(i64, usize)>` with `sort`, Go a slice of structs with
`sort.Slice`, Python a list of tuples with `sorted`; C works over a
pointer and a length, Rust and Go over a slice of the row, Kāra and
Python copy each window into a list of its own. Every implementation
prints `200 solves: checksum 13899540`.

BENCHTAB
