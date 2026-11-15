# 2200. Find All K-Distant Indices in an Array

You are given a **0-indexed** integer array `nums` and two integers
`key` and `k`. A **k-distant index** is an index `i` of `nums` for which
there exists at least one index `j` such that `|i - j| <= k` and
`nums[j] == key`.

Return *a list of all k-distant indices sorted in **increasing order***.

```
nums = [3,4,9,1,3,9,5], key = 9, k = 1  ->  [1,2,3,4,5,6]
nums = [2,2,2,2,2],     key = 2, k = 2  ->  [0,1,2,3,4]
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i] <= 1000`;
`key` is an integer from the array `nums`; `1 <= k <= nums.length`.

One pass over the key's positions, each covering the indices up to k on
either side; a `next` index not yet listed keeps the windows from
listing an index twice, so the answer comes out sorted. O(n).

## Approaches

| file | mechanism |
|---|---|
| `distant.kara` ★ | the key's positions walked in order, each listing its window of indices from the larger of `j - k` and `next`, the first index not yet listed, to `j + k` clipped to the array |
| `distant_scan.kara` | each index on its own, kept when `any` index of its window, clipped to the array, holds the key. O(n k) |
| `distant_prefix.kara` | prefix counts of the key in a `Vec.filled`, so a window holds the key exactly when the counts at its two ends differ |
| `distant_struct.kara` | a `struct Cover` of merged `struct Reach`es: each of the key's positions adds its window, joined to the last one when they touch or overlap, and `indices` (`ref self`) lists them in order |
| `distant_iter.kara` | the key's positions by `enumerate` and `filter`, each `flat_map`ped to its window clipped by `max` and `min`, and `collect`ed into a `SortedSet`, which drops the indices two windows share. O(n log n) |
| `distant_solution.kara` | LeetCode's Rust template: `Vec<i32>` and two `i32`s in, the window's ends as `usize` by `saturating_sub` and `min`, a `last` index so none is pushed twice, `for (j, &x) in nums.iter().enumerate()`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(windows apart, the key only at the ends, windows that touch, and k past
the whole array), each with its indices; then the count listed and a
checksum for 3000 random arrays of 1 to 50 numbers up to 2, 5 and 1000
in turn, the key one of them and k from 1 to the length; then the
constraints' longest, 1000 numbers up to 100 with key 7 and k 3.
`distant.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in two rounds of 12 and 2 edits: first
Rust's spellings (`Vec<..>` to brackets, `Vec::new()` to `Vec.new()`,
`(j, &x)` to `(j, x)`, `|&x|` to `|x|`, `struct Solution;` to `struct
Solution {}`, `Solution::` to `.`); then `k as usize` to `k as i64` and
`0usize` to `0`, since `nums.len()`, and so `n` and `j`, is an `i64` in
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every index i tried against every index j, and listed when
some j holds the key with |i - j| <= k; no window and no pointer. It
checks 300 random arrays of 1 to 50 numbers up to 2, 5 and 1000 in turn,
the key one of them and k from 1 to the length; then 30 with k the
length; then 30 holding the key once. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the indices are the statement read literally |
| P2 | they rise strictly, lie in the array, and include every index that holds the key |
| P3 | the array reversed: each index i becomes n - 1 - i, in reverse |
| P4 | k one more: every index listed is listed still |
| P5 | every number that is not the key made another one that is not: the same indices |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 516960005, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
cases. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
other arm, each run under `karac __mir-llvm-run` and `karac __mir-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends and
not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the window's start past the last | P1 79, P3 113, P6 79 |
| M3 | ★: the window's end one short | P1 81, P3 115, P6 81 |
| M6 | ★: the next index one past the end | P1 144, P2 107, P3 156, P4 132, P6 144 |
| M7 | scan: the window's end exclusive | P1 108, P2 25, P3 150, P6 108 |
| M8 | scan: the window's start one late | P1 100, P3 136, P6 100 |
| M9 | scan: every number in the window the key | P1 347, P2 347, P4 11, P6 347 |
| M12 | prefix: the window's end one short | P1 93, P3 136, P6 93 |
| M14 | prefix: a count by the number above the key | P1 99, P5 27, P6 99 |
| M15 | prefix: two of the key needed | P1 130, P2 118, P4 18, P6 130 |
| M18 | struct: a joined span not grown | P1 51, P2 20, P3 82, P4 37, P6 51 |
| M19 | struct: a span's last index left out | P1 360, P2 97, P3 350, P6 360 |
| M20 | struct: the reach to the right only | P1 253, P3 315, P6 253 |
| M23 | iter: the window clipped to n | P1 273, P2 273, P3 319, P6 273 |
| M24 | iter: the positions of numbers other than the key | P1 131, P2 24, P6 131 |
| M26 | iter: the first position skipped | P1 196, P2 177, P3 50, P6 196 |
| M28 | solution: the window's start not kept past the last | P1 297, P2 297, P3 319, P6 297 |
| M31 | solution: the key compared with the next number | P1 27, P3 48, P6 27 |

P1 and P6 kill all seventeen, P3 thirteen, P2 ten, P4 four and P5 one.
P3 reverses the array, and misses the four edits that are wrong the same
way from either end: every number in the window the key (M9), a count
by the number above the key (M14), two of the key needed (M15), and the
positions of the numbers other than the key (M24). P2 misses the seven
that list indices in order and keep every key's own index but drop some
of their neighbours (M1, M3, M8, M12, M14, M20, M31). P4 widens k and
kills only the four whose listing can shrink as k grows (M6, M9, M15,
M18). P5 changes only the numbers that are not the key, and kills only
the edit that reads one of them (M14).

Of the thirty-one, fourteen were not kept. Two are equivalent: the
prefix arm's first count started at -1 (M16), which shifts every count
alike, and the struct arm's touching windows kept apart (M17), which
list the same indices. One fails as a kept one does: the prefix arm's
counts from the start's own index (M13) as M8. Eight fail alike in pairs
and are left out to keep three to an arm: the ★ arm's `next` not moved
and its windows from the first index (M2, M5), the last index lost by
the ★ arm's window clipped at n - 2 and by the scan arm's loop stopping
one short (M4, M11), the window from the index itself or to its left
only (M10, M22), and the iter arm's half-width one less with the
template adapter's k one less (M25, M27). Three fail their own way and
are left out for the count: the struct arm's first window alone (M21),
and the template's `last` set to the window's end and its window clipped
at n - 2 (M29, M30).

## Verification

Every arm prints the same output as `distant.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 s to 0.7 s but the iter
arm, 2.6 s, which builds a `SortedSet` for each array. The differential
takes 1.9 s.

## Benchmarks

The bench builds 1000 arrays of 1000 numbers up to 50, 200 or 1000 in
turn once, each with its key and a k from 1 to 20, then lists each one's
indices 600 times over with the ★ arm in all five languages; each list
is checked by its length and its middle index. Every implementation
prints `600 passes over 1000 arrays: checksum 696071814`.

BENCHTAB
