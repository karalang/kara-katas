# 1299. Replace Elements with Greatest Element on Right Side

Given an array `arr`, replace every element in that array with the
greatest element among the elements to its right, and replace the last
element with `-1`.

After doing so, return the array.

```
arr = [17,18,5,4,6,1]  ->  [18,6,6,6,1,-1]
arr = [400]            ->  [-1]
```

**Constraints:** `1 <= arr.length <= 10^4`, `1 <= arr[i] <= 10^5`.

Each arm is `fn replace_elements(arr: Vec[i64]) -> Vec[i64]`; the two
Rust solutions keep LeetCode's `i32` signature inside a `Solution` and
are reached through a wrapper that converts.

## Approaches

| file | mechanism |
|---|---|
| `replace_elements.kara` ★ | one walk from the right end, each place given the greatest seen so far, -1 before anything has been seen, and the greatest then taking in the number that was there. O(n) |
| `replace_elements_naive.kara` | the statement as written: each place given the greatest of all the numbers after it, found by looking at every one, or -1 when there are none. O(n^2) |
| `replace_elements_recursive.kara` | a call for each place fills the places after it first and returns the greatest number from its place to the end, which the call before writes into its own place. O(n), n calls deep |
| `replace_elements_heap.kara` | every number with its place in a largest-first `PriorityQueue`; for each place from the left, the entries at or before it popped off the top as they come up, the top left then being the greatest after it. O(n log n) |
| `replace_elements_solution.kara` | a Rust solution as LeetCode's Rust users write it (the array taken as `mut arr` and overwritten in place from the right, `max = max.max(cur)`), carried to Kāra by `karac fix` |
| `replace_elements_scan.kara` | a second Rust solution (the array walked backwards by `iter().rev().scan(-1, ..)`, each step yielding the greatest so far before taking in its number, then collected and reversed), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples
(`18,6,6,6,1,-1 -1`); rising, falling, all equal, and the greatest at
either end (`4,4,4,-1 3,2,1,-1 7,7,-1 2,2,-1 9,9,-1`); and 3000 random
arrays of 1 to 300 numbers up to 10, 1000 or 10^5, then one of 3000
(`3001 random arrays: sum of answers 14802072649, checksum 872866943`).
`replace_elements.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, every-pair, recursive and heap arms check clean as
first written. The Rust solution takes 10 fixes by `karac fix`'s count:
`struct Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`,
the `mut arr: Vec<i32>` parameter to `arr: own Vec[i32]` with `let mut
arr = arr;` as the body's first line, `Solution::` to `Solution.`, and
the `&` dropped from the wrapper's `|&x|` patterns. The scan solution
takes 13: those, and Rust's scan closure, which writes its state through
`*m = (*m).max(x)` and yields `Some(r)`, rewritten to Kāra's, which
returns the next state with the item, `|m, x| { let r = m; let m =
m.max(x); Some((m, r)) }`. Its seed `-1` kept the default `i64` beside
the `i32` items, and the `collect` into a `Vec[i32]` was refused with
only "`C: FromIterator[i64]` is not satisfied" and no fix, where a seed
of `0` got the `0i32` suffix; B-2026-11-25-18, fixed at b45cd107b3,
gives the negated seed the same fix, and `karac fix` now writes
`scan(-1i32, ..)`. Both match on the first run.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for each place, the numbers to its right gathered and sorted,
the last of them the greatest; -1 where there are none. 2000 arrays of 1
to 12 numbers in four kinds, 500 each: numbers up to 5, so that ties are
common; up to 10^5; rising; and falling. Every array, shift, extra
number and cut is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | every number shifted up: every answer shifted up but the last -1 |
| P3 | one number appended: the earlier answers raised to it, and the new last -1 |
| P4 | the numbers from a cut on: the same answers there |
| P5 | one number put in front: the rest unchanged, and the new first the greatest of the old numbers |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 arrays: checksum 287604756,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, sorting each
place's right side, gives the same checksum.

## Mutation testing

Twelve edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each place counted among the numbers on its right | P1 2000, P2 2000, P3 2000, P5 1078, P6 10000 |
| M2 | ★: nothing seen yet counted as 0 | P1 2000, P2 2000, P3 2000, P6 10000 |
| M3 | every pair: the next number skipped | P1 1833, P2 1833, P3 2000, P5 747, P6 1833 |
| M4 | every pair: the last number never counted | P1 1833, P2 1833, P3 2000, P5 764, P6 1833 |
| M5 | recursive: a place's own number returned alone | P1 1176, P3 1251, P5 1166, P6 1176 |
| M6 | recursive: the recursion stopped a place early | P1 2000, P2 2000, P3 2000, P5 764, P6 2000 |
| M7 | heap: a place's own number counted | P1 2000, P2 2000, P3 2000, P5 1078, P6 2000 |
| M8 | heap: the least number on the right taken | P1 1642, P3 1815, P5 1820, P6 1642 |
| M9 | solution: the first place left as it was | P1 1913, P2 167, P3 1223, P4 1432, P5 1988, P6 1913 |
| M10 | solution: each number taken one too small | P1 1833, P3 2000, P5 2000, P6 1833 |
| M11 | scan: the scan walking from the left | P1 1780, P3 1971, P4 1076, P5 1971, P6 1780 |
| M12 | scan: the answers not turned back round | P1 1833, P2 1833, P3 2000, P4 1492, P5 2000, P6 1833 |

## Benchmarks

The bench runs the ★ arm over 50 arrays of 10^4 numbers up to 10^5,
built once; then 1000 passes, each setting one number of every array
from the checksum so far, answering it, and folding two of its answers,
chosen by the checksum, into the checksum. Every implementation prints
`1000 passes over 50 arrays of 10^4: checksum 64805080`.

BENCHTAB
