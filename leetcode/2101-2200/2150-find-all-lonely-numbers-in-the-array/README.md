# 2150. Find All Lonely Numbers in the Array

You are given an integer array `nums`. A number `x` is **lonely** when it
appears only **once**, and no **adjacent** numbers (i.e. `x + 1` and
`x - 1`) appear in the array.

Return ***all** lonely numbers in* `nums`. You may return the answer in
**any order**.

```
nums = [10,6,5,8]  ->  [10,8]
nums = [1,3,5,3]   ->  [1,5]
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^6`.

Count every number; a number is lonely when its count is one and the
counts of the numbers one below and one above it are none. O(n) with a
hash map.

## Approaches

| file | mechanism |
|---|---|
| `lonely.kara` ★ | the numbers counted in a `Map[i64, i64]` through `entry().or_insert(0)`; the counted numbers kept by `filter` on their count and on `contains_key` for each neighbour |
| `lonely_sorted.kara` | no map: sorted, a number is lonely when the one before it is more than one below and the one after more than one above, which leaves out a copy and a neighbour alike; the last found by `get` past the end |
| `lonely_count.kara` | counted by value in a `Vec.filled` as long as the greatest number and three more, each number one place on, so that both neighbours of every number are places of the table; read off in value order by a range under `filter` |
| `lonely_struct.kara` | a `struct Census` taken `of` the list, holding a `SortedMap` of counts built by `get` and `insert`, and asked how often a number was `met` and whether it is `alone` (`ref self`) |
| `lonely_sets.kara` | no counts: two `Set[i64]`s, the numbers seen and those seen again, the second filled when `insert` into the first answers false |
| `lonely_solution.kara` | LeetCode's Rust template: `use std::collections::HashMap`, `*count.entry(x).or_insert(0) += 1` over `for &x in &nums`, `filter` over `|(&x, &c)|` with `contains_key(&(x - 1))`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Any order is allowed, so the harness sorts each answer before printing
it. Every arm prints the same 10 lines: LeetCode's two examples and four
more (one number, one number twice, a run with no gap, and 0 beside the
constraints' greatest), each with its lonely numbers; then the total and
a checksum over 2000 random lists of 1 to 12 numbers of 0 to 9, 0 to 30
and 0 to 1000 in turn; then the constraints' largest, 100000 numbers:
every even number from 0, every number from 0 once and the first half
again, and at random from the whole range. `lonely.py` mirrors the ★ arm
and its output is byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 32, 2 and 1 edits: Rust's spellings (the `use` dropped, `<..>`
to `[..]`, `HashMap::new` to `HashMap.new`, `for &x in &nums` to `for x
in ref nums`, the `|(&x, &c)|` and `|&x|` patterns to bare ones, `&&` and
`!` to `and` and `not`, the `&` dropped from `contains_key(&(..))`,
`struct Solution;` to `struct Solution {}`, the adapter's `&Vec` to `ref
Vec`, `Solution::` to `.`); then `HashMap` to `Map`; then the `ref`
dropped from the adapter's parameter, which borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each number is checked against the whole list for another
copy of itself and for a number one below or one above, by counting; no
map, set or sort finds them. Every answer is sorted before it is
compared. It checks 300 random lists of 1 to 10 numbers of 0 to 5, 0 to
15 or 0 to 100 in turn; then 30 of 1 to 10 even numbers; then 30 runs of
numbers one apart, one of them met twice in some. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the lonely numbers are the statement read literally |
| P2 | the list reversed: the same lonely numbers |
| P3 | every number moved up by 5: every lonely number moved up by 5 |
| P4 | every number doubled: the numbers met once, doubled |
| P5 | the list followed by itself: none lonely |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 68977532, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists by the same counting. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-llvm-run` and `karac __mir-run`. Eighteen are kept: three
to each arm but the sets arm, which keeps two, and four to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a number met twice kept | P1 83, P4 173, P5 276, P6 83 |
| M3 | ★: the neighbour above asked two up | P1 146, P4 167, P6 146 |
| M5 | ★: the neighbour below asked two down | P1 149, P4 174, P6 149 |
| M6 | sorted: the numbers unsorted | P1 230, P2 274, P4 276, P5 193, P6 230 |
| M7 | sorted: the neighbour below let through | P1 154, P6 154 |
| M8 | sorted: the neighbour above let through | P1 149, P6 149 |
| M11 | table: each number counted at its own place | P1 253, P3 44, P4 355, P6 253 |
| M12 | table: a number never met kept | P1 272, P3 360, P4 338, P5 272, P6 272 |
| M13 | table: the greatest never tried | P1 204, P4 298, P6 204 |
| M18 | struct: a number met twice alone | P1 73, P4 157, P5 253, P6 73 |
| M19 | struct: the least never asked | P1 208, P4 297, P6 208 |
| M20 | struct: 0 never alone | P1 44, P3 44, P4 73, P6 44 |
| M21 | sets: every number taken as seen again | P1 253, P4 355, P6 253 |
| M25 | sets: the neighbour below asked among the repeats | P1 116, P6 116 |
| M26 | solution: the template keeping numbers met twice | P1 272, P4 360, P5 253, P6 272 |
| M27 | solution: the adapter halving every number | P1 244, P3 210, P4 345, P6 244 |
| M29 | solution: the adapter dropping the first number | P1 243, P2 227, P4 332, P5 178, P6 243 |
| M30 | solution: the template's neighbour above asked two down | P1 176, P4 174, P6 176 |

P1 and P6 kill all eighteen, P4 fifteen, P5 six, P3 four and P2 two. P4
doubles every number, which takes every number's neighbours away, so
that every number met once is lonely: it sees an edit that loses a
lonely number or keeps one it should not, whatever the neighbours (M1,
M3, M5, M6, M11, M12, M13, M18, M19, M20, M21, M26, M27, M29, M30), and
passes the edits that only let a neighbour through, since the doubled
list has none (M7, M8, M25). P5 lists every number twice, which leaves
none lonely: it sees an edit that keeps a number met more than once
(M1, M6, M12, M18, M26, M29). P3 moves every number up by 5, which sees
an edit tied to the numbers' own values rather than how they stand to
each other: the table's places read as the numbers (M11) or a number
never met kept, which the move puts in sight (M12), 0 never alone (M20),
and the adapter's halving (M27). P2 reverses the list, which sees an
edit tied to the list's order: the sorted arm unsorted (M6) and the
adapter dropping the first number (M29).

Of the thirty, twelve were not kept, and each fails as a kept one does:
the ★ arm never asking the neighbour below, as M7; the ★ arm's counts
started at one, the table's places read as the numbers, the struct
counting each number twice and the adapter's answer one up, which all
leave nothing or nothing right, as M21; the sorted arm's last never
lonely or never tried, as M13; a neighbour below met once let through by
the table and by the struct, as M25; the sets arm keeping a number seen
again, and taking the number above as seen again, which leaves the
number itself to be kept, as M1; and the sets arm never asking the
neighbour above, as M8.

## Verification

Every arm prints the same output as `lonely.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.9 s to 9.2 s and the
differential 0.6 s.

## Benchmarks

The bench builds 4 lists of 100000 numbers of 0 to 1000000 once; then
searches every list 25 times, one number redrawn before each so that no
search repeats one before, with the ★ arm in all five languages; C's map
of counts is an open-addressing table, since C has none of its own. The
lonely numbers come in any order, so each answer is folded to its
length and its sum. Every implementation prints `100 searches: 7414682
lonely in all, checksum 412270009`.

BENCHTAB
