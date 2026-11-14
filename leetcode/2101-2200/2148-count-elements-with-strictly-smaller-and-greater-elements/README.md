# 2148. Count Elements With Strictly Smaller and Greater Elements

Given an integer array `nums`, return *the number of elements that have
**both** a strictly smaller and a strictly greater element appear in*
`nums`.

```
nums = [11,7,2,15]  ->  2
nums = [-3,3,3,90]  ->  2
```

**Constraints:** `1 <= nums.length <= 100`; `-10^5 <= nums[i] <= 10^5`.

A number has a strictly smaller one in the list exactly when it is above
the list's least, and a strictly greater one exactly when it is below
the list's greatest; so the answer is how many lie strictly between the
two, none when the least and the greatest are one value. O(n).

## Approaches

| file | mechanism |
|---|---|
| `elements.kara` ★ | the least and the greatest by `iter().min()` and `max()`, then the numbers between them by `filter` and `count` |
| `elements_sorted.kara` | sorted; the copies of the least and of the greatest walked off the two ends by `position` and `rposition`, the two results matched as a pair under a guard |
| `elements_tally.kara` | one pass keeping the least and the greatest so far and how many times each has been met, a new one resetting its tally; the list's length less the two tallies |
| `elements_struct.kara` | a `struct Bounds` built `of` the list by one `fold`, asked whether a number lies `inside` it (`ref self`) |
| `elements_map.kara` | the numbers tallied in a `SortedMap[i64, i64]` through `entry().or_insert(0)`; every tally but the first and last, by `values().skip(1).take(..)` and `sum` |
| `elements_solution.kara` | LeetCode's Rust template: `*nums.iter().min().unwrap()`, the `|&&x|` pattern, `&&`, the count `as i32`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(one number, three equal, two apart, and every value met twice), each
with its count; then the total and a checksum over 2000 random lists of
1 to 12 numbers of 1 to 3, of 1 to 5, and of -100000 to 100000 in turn;
then the constraints' largest, 100 numbers: one of each from -50 to 49,
every one -100000, and at random from the whole range. `elements.py`
mirrors the ★ arm and its output is byte-identical.

No compiler gap was met. `karac fix` carries the template in two rounds
of 10 and 2 edits: Rust's spellings (`Vec<..>` to `Vec[..]`, the
`|&&x|` and `|&x|` patterns to bare ones, `&&` to `and`, `struct
Solution;` to `struct Solution {}`, the adapter's `&Vec` to `ref Vec`,
`Solution::` to `.`); then the adapter's `as i64` dropped, since an
`i32` widens on return, and the `ref` dropped from its parameter, which
borrows already. The template's `*` on `min().unwrap()` stays: Kāra's
`min` over `iter()` gives a `ref`, as Rust's does.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each number is checked against every other for one strictly
smaller and one strictly greater, with no least or greatest found first.
It checks 300 random lists of 1 to 10 numbers of 1 to 2, 1 to 4 or -1000
to 1000 in turn; then 30 of numbers all equal; then 30 of 1 to 10
distinct numbers, three apart and shuffled. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the list reversed: the same count |
| P3 | every number negated: the same count |
| P4 | every number listed twice: twice the count |
| P5 | a number below every one and a number above every one added: the whole length of the list |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 425917204, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal counts was checked against a Python reading of the same
lists by the same comparison of every pair. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, five to six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Eighteen are kept,
three to each arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the least counted in | P1 286, P3 128, P5 360, P6 286 |
| M4 | ★: either side enough | P1 286, P5 360, P6 286 |
| M5 | ★: the first number never counted | P1 106, P2 103, P4 106, P6 106 |
| M6 | sorted: the numbers unsorted | P1 126, P4 286, P6 126 |
| M8 | sorted: one short between the ends | P1 186, P4 186, P5 360, P6 186 |
| M9 | sorted: the least read from the middle | P1 244, P3 128, P5 360, P6 244 |
| M11 | tally: a new least tallied as none | P1 196, P2 135, P3 180, P4 196, P5 360, P6 196 |
| M14 | tally: the first number tallied twice | P1 90, P2 134, P3 180, P4 90, P5 360, P6 90 |
| M15 | tally: the greatest's copies tallied at the least | P1 175, P2 260, P3 274, P4 173, P5 360, P6 175 |
| M16 | struct: the greatest started at 0 | P1 17, P3 202, P6 17 |
| M17 | struct: the least kept by `max` | P1 186, P5 360, P6 186 |
| M19 | struct: the count started at one | P1 360, P4 360, P5 360, P6 360 |
| M22 | map: the least's tally kept | P1 59, P3 66, P5 150, P6 59 |
| M23 | map: the greatest's tally kept | P1 186, P3 58, P5 360, P6 186 |
| M25 | map: the values summed for the tallies | P1 167, P3 186, P4 186, P5 336, P6 167 |
| M28 | solution: the adapter halving every number | P1 16, P6 16 |
| M30 | solution: the template's least read as the first number | P1 144, P2 146, P3 162, P5 360, P6 144 |
| M31 | solution: the template's greatest one lower | P1 62, P3 49, P6 62 |

P1 and P6 kill all eighteen, P5 thirteen, P3 eleven, P4 eight and P2
five. The count depends only on how many numbers lie strictly between
the ends, so a wrong edit shows against the literal reading; the other
properties say what it gets wrong. P5 brackets the list with a new least
and a new greatest, so that every number of the list lies between them:
it sees any edit that counts an end or misses one in (M1, M4, M8, M9,
M17, M22, M23), and any that miscounts the list's own length (M11, M14,
M15, M19, M25, M30). P3 negates every number, which swaps the least and
the greatest: it sees an edit that treats one end apart from the other
(M1, M9, M11, M14, M15, M16, M22, M23, M31). P4 lists every number
twice, which doubles the count: it sees an edit that adds or loses a
fixed amount (M5, M8, M19) or reads the list's order (M6, M15). P2
reverses the list, which sees an edit tied to which number comes first
(M5, M14, M30) or to the order a tally meets its numbers in (M11, M15).

Of the thirty-one, thirteen were not kept. Five are equivalent: the
sorted arm's ends allowed to meet one past each other, which then count
none between them; its greatest's copies found as the first copy less
one, which is the same place in a sorted list; the struct asking only
that a number not be the greatest, which a number above the least and
no greater than the greatest already is not; the map letting two kinds
through, which then sums no tally; and the template letting in any
number but the greatest, as the struct's. One fails by a crash: the
adapter dropping the first number, which leaves a list of one empty.
Six fail as a kept one does: the ★ arm's greatest counted in, the
struct's greatest inside and the template's least counted in, as M1;
the ★ arm's greatest read as the least, as M17; the tally's new least
tallied twice, as M11; and every map tally started at one, as M8. One is
killed with checks of its own but was left out because its arm keeps
its share: the tally letting a list of one value through (P1 74, P6
74).

## Verification

Every arm prints the same output as `elements.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s to 0.3 s and the
differential 0.4 s.

## Benchmarks

The bench builds a pool of 100000 numbers of -100000 to 100000 once;
then counts 200000 times over the 100 numbers of the pool from a random
place on, the constraints' longest list, copied out of the pool; one
number of the pool is redrawn from -10 to 10 before each count so that
no count repeats one before, and the pool fills with ties as it goes.
The ★ arm in all five languages. Every implementation prints `200000
counts: 19157153 counted in all, checksum 7068252`.

BENCHTAB
