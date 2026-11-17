# 2215. Find the Difference of Two Arrays

Given two **0-indexed** integer arrays `nums1` and `nums2`, return *a
list* `answer` *of size* `2` *where:*

- `answer[0]` *is a list of all **distinct** integers in* `nums1`
  *which are **not** present in* `nums2`*.*
- `answer[1]` *is a list of all **distinct** integers in* `nums2`
  *which are **not** present in* `nums1`.

**Note** that the integers in the lists may be returned in **any**
order.

```
nums1 = [1, 2, 3],    nums2 = [2, 4, 6]        ->  [[1, 3], [4, 6]]
nums1 = [1, 2, 3, 3], nums2 = [1, 1, 2, 2]     ->  [[3], []]
```

**Constraints:** `1 <= nums1.length, nums2.length <= 1000`; `-1000 <=
nums1[i], nums2[i] <= 1000`.

Each array put in a set, and each list the numbers of one set the other
lacks. O(n + m).

Since the lists may come in any order, and a `Set` walks in an order
that changes from run to run, every harness sorts both lists before it
prints them, and the differential sorts them before it compares.

## Approaches

| file | mechanism |
|---|---|
| `difference.kara` ★ | each array `collect`ed into a `Set`, and each list the set `filter`ed by `not contains` on the other |
| `difference_merge.kara` | both arrays sorted and squeezed by `dedup`, then walked together: the smaller head belongs to its own list, equal heads to neither |
| `difference_marks.kara` | the numbers lie in -1000..1000, so each array marks a table of 2001 `bool`s, and a sweep over the range lists what one table marks and the other does not |
| `difference_struct.kara` | a `struct Bag` holding a `SortedSet`, built by `of`, and `without` (`ref self`) listing its numbers another bag lacks |
| `difference_iter.kara` | each array `collect`ed into a `SortedSet`, and each list Kāra's `difference`, a set, turned into a `Vec` by `into_iter` and `collect` |
| `difference_solution.kara` | LeetCode's Rust template: two `Vec<i32>` in, `Vec<Vec<i32>>` out, each array `collect`ed into a `HashSet<i32>`, and each list `s1.difference(&s2).cloned().collect()` in a `vec![..]`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(the same numbers twice, nothing shared, negatives and repeats, and one
number each), each with its sorted lists; then a checksum of 3000
random pairs of 1 to 30 numbers spread over -3..3, -30..30 and
-1000..1000 in turn; then the constraints' largest, 1000 numbers each
over the whole range and 1000 each that share nothing. `difference.py`
mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 37 edits: the `use`
dropped, `HashSet<i32>` to `Set[i32]` and the `Vec<..>`s to `Vec[..]`,
`nums1.into_iter()` on a borrowed parameter to `nums1.clone().into_iter()`,
`vec![..]` to `[..]`, `&s2` to `s2`, the `.into_iter()` before each
`.cloned()`, the `|&x|`s to `|x|`, `struct Solution;` to `struct Solution
{}` and `Solution::` to `Solution.`.

The template found a gap, kara `B-2026-11-17-126`: Rust's `difference`
gives an iterator and Kāra's a set, and the check said only "no method
'cloned' on type 'Set'", with no fix, where a `Vec`'s `.cloned()` is
told to take `.iter()` first and `karac fix` adds it; a `SortedSet`'s
`.map(..)` was read as a typo of `max`. The iterator adaptors and
terminals on a set or a map now name the `.iter()` hop, or
`.into_iter()` on a call's result, with a note that `union`,
`intersection` and `difference` give a set, and the fix inserts it. Until
then a second round could not carry the template.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each number of one array, in order, looked for in the other
array number by number, and listed when it is missing there and not
listed already; no sets and no sorting but the last. It checks 300
random pairs of 1 to 12 numbers spread over -3..3, -30..30 and
-1000..1000 in turn; then 30 pairs of one number repeated; then 30 with
the second array drawn from the first. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the sorted lists are the statement read literally |
| P2 | each list has no number twice, and every number in it is in its own array and not in the other |
| P3 | the arrays swapped: the lists swapped |
| P4 | both arrays reversed: the same lists |
| P5 | each array followed by itself: the same lists |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 175142570, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading with set
differences. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and to the marks
arm, five to each of the other Kāra arms and to the template arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first list everything in the first array | P1 187, P2 187, P3 187, P6 187 |
| M4 | ★: the first array's numbers below 0 left out | P1 318, P2 120, P3 337, P6 318 |
| M6 | ★: the second array's first number left out | P1 244, P2 45, P3 301, P4 246, P5 244, P6 244 |
| M7 | merge: no dedup of the first array | P1 141, P2 141, P3 202, P5 360, P6 141 |
| M9 | merge: the second array not sorted | P1 143, P2 143, P3 168, P4 101, P5 301, P6 143 |
| M11 | merge: the walk ending with the shorter array | P1 276, P6 276 |
| M12 | marks: the second table marked one place up | P1 360, P2 354, P3 360, P6 360 |
| M13 | marks: the sweep from 0 | P1 303, P6 303 |
| M15 | marks: the first array's last number not marked | P1 274, P2 58, P3 302, P4 275, P5 274, P6 274 |
| M17 | struct: a bag of only the first number | P1 326, P2 93, P4 318, P6 326 |
| M18 | struct: every number kept | P1 187, P2 187, P6 187 |
| M21 | struct: the numbers above 500 never in the other bag | P1 7, P2 7, P6 7 |
| M22 | iter: the first list the union | P1 360, P2 360, P3 360, P6 360 |
| M25 | iter: the first set without its largest | P1 360, P2 106, P3 360, P6 360 |
| M26 | iter: the second set doubled | P1 355, P2 355, P3 357, P6 355 |
| M27 | solution: the adapter's numbers capped at 100 | P1 107, P2 104, P3 113, P6 107 |
| M30 | solution: the second array's numbers negated | P1 337, P2 320, P3 349, P6 337 |

P1 and P6 kill all seventeen, P2 fifteen, P3 twelve, P4 and P5 four
each. P2 checks each listed number against both arrays, so it misses
only the two edits that leave numbers out without listing a wrong one:
the merge walk ending with the shorter array and the sweep from 0 (M11,
M13). P3 swaps the arrays and misses the five edits that treat them
alike (M11, M13, M17, M18, M21). P4 reverses the arrays and kills the
edits that read one position (M6, M9, M15, M17); P5 writes each array
twice and kills those and the merge arm's missing dedup (M6, M7, M9,
M15).

Of the thirty-one, fourteen were not kept. Thirteen are killed and fail
as a kept one does or their own way: the merge arm's equal heads both
kept or moving only the first, and the marks arm's second list the
numbers in both (M8, M10, M14), as the ★ arm's M1; four pairs fail
alike and neither of a pair is kept, the second set built from the
first array in the ★ and iter arms (M2, M24), the second list the
numbers shared in the ★ and iter arms (M3, M23), the second list the
first's without the second in the struct arm and the template (M19,
M28), and the ★ arm's lists the wrong way round with the struct arm's
number kept twice (M5, M20), which fail on the same 322 cases, those
with a number to list; and the template's first set from both arrays
and its first list the symmetric difference (M29, M31) fail their own
way and are left out for the count of two. One survives, and it is not
equivalent: the marks arm's sweep stopping at 999 (M16) never lists
1000, and no case of the differential draws 1000 into a list, as only
one number in 2001 of the widest spread is 1000. The arm's own harness
catches it: its random checksum and its 1000 apart, whose second list
holds 1000, both change.

## Verification

Every arm prints the same output as `difference.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 s to 0.8 s, the marks arm
1.6 s, sweeping its 2001 marks for each of the 3000 random pairs, and
the differential 1.4 s.

## Benchmarks

The bench draws 200 pairs of 1000 numbers once, spread over -30..30,
-300..300 and -1000..1000 in turn, then punches each pair 10 times, one
number of the first array moving each time, and answers it after each
punch with the ★ arm in all five languages: Rust's `HashSet`, a C
open-addressing set, Go's `map` and Python's `set`. The lists come in
each language's own set order, so the checksum runs over their lengths
and sums. Every implementation prints `200 pairs of 1000, 10 punches:
checksum 594667923`.

BENCHTAB
