# 2239. Find Closest Number to Zero

Given an integer array `nums` of size `n`, return *the number with the
value **closest** to* `0` *in* `nums`. If there are multiple answers,
return *the number with the **largest** value*.

```
nums = [-4, -2, 1, 4, 8]  ->  1
nums = [2, -1, 1]         ->  1    (-1 and 1 are as close; 1 is larger)
```

**Constraints:** `1 <= n <= 1000`; `-10^5 <= nums[i] <= 10^5`.

One scan, the closest kept: a number replaces it when nearer to zero,
or as near and larger, so a tie goes to the positive one. O(n).

## Approaches

| file | mechanism |
|---|---|
| `closest.kara` ★ | one `for` over the numbers, the best replaced on `x.abs() < closest.abs() or (x.abs() == closest.abs() and x > closest)` |
| `closest_sort.kara` | a copy `sort_by` a comparison, the distance from zero by `cmp` first and the larger number first among equals, and the first element taken |
| `closest_twice.kara` | two passes: the least distance from zero by `min`, then `contains` for whether a positive number reaches it, the answer that number or its negation |
| `closest_struct.kara` | a `struct Nearest` of the best so far, with `beats` (`ref self`) and `offer` (`mut ref self`) |
| `closest_iter.kara` | `min_by_key` with the key the pair `(x.abs(), -x)`, so that among the nearest the larger number has the smaller key |
| `closest_solution.kara` | LeetCode's Rust template: `nums.into_iter().min_by_key(\|&x\| (x.abs(), -x)).unwrap()`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and five
more (one negative number, a tie at both ends, a zero, the constraints'
ends, and a tie whose negative half comes first and twice), each with
its answer; then a checksum of 3000 random arrays of 1 to 50 numbers up
to 10, 1000 and 10^5 in size in turn, with how many answers are
positive; then 1000 random numbers, and 1000 numbers all past 500 from
zero, the nearest -501 (twice) and 502. `closest.py` mirrors the ★ arm
and its output is byte-identical.

`karac fix` carries the template in one round of 9 edits: `Vec<i32>` to
`Vec[i32]`, the `&` of the closure pattern `|&x|` dropped, `struct
Solution;` to `struct Solution {}`, `Solution::find_closest_number` to
`Solution.find_closest_number`, and the adapter's `as i64` on the `i32`
result dropped as a lossless cast. Since a bare parameter borrows,
`nums.into_iter()` became `nums.clone().into_iter()`; the tuple key
`(x.abs(), -x)` is Kāra's too.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the numbers with no other number strictly closer to zero,
and the largest of them; no running best and no key. It checks 300
random arrays of 1 to 8 numbers from -10 to 10; then 30 of negative
numbers only; then 30 in which every number comes with its negation.
All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the largest of the closest, read literally |
| P2 | the numbers reversed: the same answer |
| P3 | the answer is one of the numbers, and none is closer to zero |
| P4 | a 0 appended: 0 |
| P5 | the answer's negation appended: its distance from zero, positive |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 526632755, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that sorts
the numbers by `(distance, -number)` and takes the first. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-two edits to the differential, six to the ★ arm and the
template and five to each of the others, each run under `karac
__mir-llvm-run`, and the kept ones under `karac __mir-run` too.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends
and not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the smallest number, not the nearest | P1 267, P2 72, P3 259, P4 280, P5 70, P6 267 |
| M5 | ★: the last of the nearest, `<=` | P1 24, P2 49, P5 156, P6 24 |
| M6 | ★: the distance kept, not the number | P1 76, P2 49, P3 76, P6 76 |
| M8 | sort: the farthest first | P1 305, P3 305, P4 357, P6 305 |
| M10 | sort: ties left in their order, `a != b` for the distances | P1 33, P2 49, P5 150, P6 33 |
| M11 | sort: sorted by value | P1 254, P2 65, P3 254, P4 305, P5 238, P6 254 |
| M12 | twice: a tie to the negative | P1 297, P3 241, P5 180, P6 297 |
| M15 | twice: the least distance started one short | P1 136, P2 136, P3 136, P4 14, P5 14, P6 136 |
| M16 | twice: always the positive distance | P1 117, P3 117, P6 117 |
| M18 | struct: the best stored negated | P1 168, P2 136, P3 146, P5 133, P6 168 |
| M19 | struct: the best started at 0 | P1 297, P3 297, P6 297 |
| M20 | struct: a tie to the negative | P1 56, P5 297, P6 56 |
| M23 | iter: the key `(x, x.abs())`, the smallest | P1 276, P3 265, P4 308, P5 350, P6 276 |
| M24 | iter: `max_by_key`, the largest key | P1 312, P3 305, P4 357, P5 357, P6 312 |
| M26 | iter: the distance halved in the key | P1 45, P3 45, P4 65, P6 45 |
| M29 | solution: a positive number's distance doubled | P1 138, P3 82, P5 297, P6 138 |
| M32 | solution: distances capped at 3 in the key | P1 69, P3 69, P6 69 |

P1 and P6 kill all seventeen, P3 fourteen, P5 eleven, and P2 and P4
seven each. P3 needs no reading of the tie rule, only that the answer
is a number of the array at the least distance, so it catches every
edit that answers far from zero or with a value not in the array. P5
adds the answer's negation and so makes a tie on purpose: it catches
the edits that break ties the wrong way, which P1 alone sees only where
the random arrays happen to hold one. P2, the reversal, catches the
edits whose answer depends on order: the first or last of a tie kept,
and a sort that leaves ties where they were.

Of the thirty-two, fifteen were not kept, and none crashes, survives,
or differs between the backends. All fifteen fail as a kept one does: a
tie to the negative in the ★, sort, twice, iter and template arms (M1,
M7, M13, M22, M27) as in the struct arm (M20); the ★ arm's best from 0
(M3) as the struct arm's (M19); the first of a tie in the ★ and iter
arms (M4, M25) as the sort arm's ties in order (M10); the sort arm's
last element, the struct arm's offer when not beaten and the template's
largest key (M9, M21, M28) as the iter arm's largest key (M24); the
greatest distance in the twice, struct and template arms (M14, M17,
M31) as the sort arm's farthest first (M8); and the template's distance
handed back (M30) as the twice arm's always positive (M16). The
template's sixth edit, distances capped at 3 (M32), was added because
its first five all fail as edits kept elsewhere.

## Verification

Every arm prints the same output as `closest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 s to 0.7 s, and the
differential 0.4 s.

## Benchmarks

The bench draws 1000 numbers from -10^5 to 10^5 once, then makes 100000
passes, one number drawn again before each, with the ★ arm in all five
languages. Every implementation prints `100000 passes over 1000
numbers: checksum 117857180`.

BENCHTAB
