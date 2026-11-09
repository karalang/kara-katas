# 2032. Two Out of Three

Given three integer arrays `nums1`, `nums2` and `nums3`, return a distinct
array containing all the values that are present in at least two out of
the three arrays. You may return the values in any order.

```
nums1 = [1,1,3,2], nums2 = [2,3], nums3 = [3]  ->  [3,2]
nums1 = [3,1], nums2 = [2,3], nums3 = [1,2]    ->  [2,3,1]
nums1 = [1,2,2], nums2 = [4,3,3], nums3 = [5]  ->  []
```

**Constraints:** `1 <= nums1.length, nums2.length, nums3.length <= 100`;
`1 <= nums1[i], nums2[j], nums3[k] <= 100`.

The answer may come in any order, so every arm here returns it ascending,
which makes the arms comparable line for line. A value repeated inside one
array is still in only one array: each array counts once per value.

## Approaches

| file | mechanism |
|---|---|
| `three.kara` ★ | a mask per value, one bit per array (`mask[x] \|= 1`, `2`, `4`), and the values whose mask has `count_ones() >= 2`, read from 1 to 100. O(n + 100) |
| `three_sets.kara` | each array collected into a `Set`, then every value of their union kept when `sets.iter().filter(\|t\| t.contains(x)).count() >= 2`, and the answer sorted. O(n log n) |
| `three_sorted.kara` | a `SortedMap` from each value to the number of arrays holding it, each array deduplicated through a `SortedSet` first; the map's walk is already ascending. O(n log n) |
| `three_merge.kara` | each array sorted and deduplicated, then the three walked together like a three-way merge: the least head taken each step and kept when two or three heads equal it. O(n log n) |
| `three_count.kara` | one count per value: each array marks the values it holds in a fresh table of flags, so a repeat counts once, and adds its marks to the counts through a `mut ref Vec[i64]`. O(n + 100) per array |
| `three_solution.kara` | LeetCode's Rust template (`use std::collections::HashSet`, `HashSet<i32>`, `into_iter().collect()`, `(1..=100).filter(..).collect()` into a `Vec<i32>`), carried by `karac fix` in three rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then how many values are kept, with a checksum of
the answers in order, for 3000 problems of 1 to 20 values per array from 1
to a top of 1 to 30, and for 2000 problems of three 100-value arrays from 1
to 100, the most the constraints allow. `three.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each value from 1 to 100 tried, each array scanned for it, and
the value kept when two or three scans find it. It checks 1500 problems of
1 to 12 values per array from 1 to a top of 1 to 12. Every random choice is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the three arrays taken in another order leave the answer |
| P3 | each array reversed and appended to itself leaves the answer |
| P4 | the answer rises strictly, and each value in it is in one of the arrays |
| P5 | the smallest value in none of the arrays, appended to the first two, joins the answer and changes nothing else |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 problems: checksum 179902842, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, then two more
to replace two that survived, each run under `karac __mir-run` and `karac
__mir-llvm-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under both
backends and not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second array's bit taken as the first's | P1 699, P2 1041, P5 1500, P6 699 |
| M2 | ★: the third array's bit added, not set | P1 95, P2 176, P5 95, P6 95 |
| M3 | ★: the mask compared as a number | P1 881, P2 887, P5 881, P6 881 |
| M4 | sets: a value kept once per set holding it | P1 1492, P4 1492, P5 1500, P6 1492 |
| M5 | sets: a value kept only when all three hold it | P1 1225, P5 1500, P6 1225 |
| M6 | sets: a value in all three dropped (`== 2`) | P1 1105, P5 1105, P6 1105 |
| M7 | sorted: each array not deduplicated | P1 730, P3 834, P5 730, P6 730 |
| M8 | sorted: the first array skipped | P1 1041, P2 1057, P5 1500, P6 1041 |
| M9 | sorted: a value in all three shifted by one | P1 1105, P4 922, P5 1105, P6 1105 |
| M10 | merge: each list not deduplicated | P1 957, P3 1492, P4 957, P5 957, P6 957 |
| M11 | merge: each list not sorted | P1 1285, P3 933, P4 655, P5 1335, P6 1285 |
| M12 | merge: each list's last value never the least | P1 1112, P5 1274, P6 1112 |
| M13 | count: 1 never marked | P1 1005, P5 1139, P6 1005 |
| M14 | count: the values in no array kept (`!= 1`) | P1 1500, P4 1500, P5 1500, P6 1500 |
| M15 | count: a mark set rather than added | P1 1492, P5 1500, P6 1492 |
| M16 | solution: the third set's check reading the first | P1 1021, P2 1198, P5 1021, P6 1021 |
| M17 | solution: the first set counted twice | P1 635, P2 887, P5 635, P6 635 |

P1, P5 and P6 kill all seventeen, P2 six, P4 five and P3 three. P5 appends
the smallest value in no array to the first two, which must join the answer
and leave the rest of it; every edit here either loses that value or changes
some other, so P5 sees each one. P2 sees the edits that treat the arrays
unequally: the second array's bit taken as the first's (M1), the third's
added rather than set, so a repeat carries into another bit (M2), the mask
compared as a number, under which the second or third array alone passes
(M3), the first array skipped (M8), and the Rust arm's third check reading
the first set or the first set counted twice (M16, M17). P3 doubles each
array with its own reverse, so it sees the edits that let a repeat count:
an array not deduplicated (M7, M10) and a list merged unsorted, which the
reversed copy reorders (M11). P4 sees the edits whose answer is not a
rising run of values from the arrays: a value kept once per set (M4) or per
repeat (M10), a value shifted out of the arrays (M9), an unsorted merge
(M11), and the values in no array kept (M14).

Two of the first thirty survived, both because the differential draws its
values from 1 to at most 12: the ★ arm's 100 never read and the sorted
arm's values above 50 dropped change nothing that small. The same edits at
10 replaced them, and fail alike, on 138 problems; they are not kept, as
each of those arms keeps three. The rest fail as a kept one does, or are
left out for the same reason: the sets arm's third array taken as the
second and the count arm's third array marked as the second fail alike; the
sets arm's descending sort and the Rust arm's values read downward fail
alike; the merge arm's first holder alone advanced fails as M15; the merge
arm's third list taken from the first, the Rust adapter's first array
handed third and its second set built from the first fail as M16; the ★
arm's value in one array kept and the count arm's every occurrence counted
fail alike; and the sorted arm's values in exactly one array kept fails on
its own pattern.

## Verification

Every arm prints the same output as `three.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 1.4 s (★) to 5.3 s (Rust) and the
differential 7.8 s, on kara 991c45adcd.

The five Kāra arms met no compiler gap and checked as written.

The Rust arm was written as LeetCode's Rust template, and at first `karac
fix` stopped short of a clean check. After the syntax rounds the checker
refused the tail `(1..=100).filter(..).collect()` with "`C:
FromIterator[i64]` is not satisfied": a range of bare literals took `i64`
where it was written, though the function's `Vec<i32>` return should fix
the literals' type, as Rust infers it, and each `s1.contains(x)` on a
`Set[i32]` was refused as an implicit narrowing. B-2026-11-08-86 tracked
it, and kara 1a8ab6b981 fixed it: the return now types the range. `karac
fix` carries the arm in three rounds (fifteen edits, three, then three) to
a clean check: the `use std::collections::HashSet` line deleted (`Set` is
in Kāra's prelude) and `<..>` to `[..]` in every type, then `HashSet` to
`Set`, then a `.clone()` before each `into_iter()`, since a parameter
borrows its array and `into_iter` would take it.

The arm's adapter first turned each `Vec[i64]` into a `Vec[i32]` with one
closure, `let to32 = |v| v.iter().map(|x| x as i32).collect();`, called
three times as the template's arguments. That checks clean and then stops
at lowering, "an expression whose type does not lower
(UnsolvedParam("C"))": a closure's `collect()` takes nothing from the type
its result is later used at, and a Kāra closure cannot declare its return
type, so nothing fixes `C`. B-2026-11-09-34 tracks it; the adapter collects
each array into an annotated `let`.

## Benchmarks

The bench builds 100 problems of three 100-value arrays once in all five
languages, and runs the ★ arm for 4000 rounds, one value of each problem
changed before each call: 400000 calls. Every implementation prints `400000
calls: 27610188 values kept, checksum 845965174`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `991c45adcd` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.320 to 0.361 s | 0.338 s |
| Rust (`rustc -O`) | 0.380 to 0.435 s | 0.394 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.397 to 0.417 s | 0.408 s |
| Kāra (`karac build`) | 0.393 to 0.430 s | 0.414 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.391 to 0.457 s | 0.417 s |
| Go | 0.669 to 0.731 s | 0.696 s |
| Python | 9.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.406 s) is not above its real time (0.414 s).

The sequential Kāra program is 0.98x Rust under overflow checks and 1.21x
C.
