# 2216. Minimum Deletions to Make Array Beautiful

You are given a **0-indexed** integer array `nums`. The array `nums` is
**beautiful** if:

- `nums.length` is even.
- `nums[i] != nums[i + 1]` for all `i % 2 == 0`.

Note that an empty array is considered beautiful.

You can delete any number of elements from `nums`. When you delete an
element, all the elements to the right of the deleted element will be
**shifted one unit to the left** to fill the gap created and all the
elements to the left of the deleted element will remain **unchanged**.

Return *the **minimum** number of elements to delete from* `nums` *to
make it* *beautiful.*

```
nums = [1, 1, 2, 3, 5]     ->  1
nums = [1, 1, 2, 2, 3, 3]  ->  2
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^5`.

Walking left to right, a number that would start a pair is deleted when
the number after it is the same: keeping it could only force a deletion
later, and deleting it shifts the rest, so the index a number keeps is
its own less the deletions so far. An odd length left at the end costs
one more. O(n).

## Approaches

| file | mechanism |
|---|---|
| `beautiful.kara` ★ | one pass over the indices, a number deleted when it would start a pair, by its index less the deletions, and the next is the same; then one more for an odd length |
| `beautiful_stack.kara` | the kept numbers built up in a `Vec`: a number kept when it starts a pair or differs from the pair's first, a last unpaired number popped |
| `beautiful_pairs.kara` | two indices, a pair's first number and its partner, the first number after it that differs; every pair found keeps two |
| `beautiful_struct.kara` | a `struct Beautifier` of the numbers seen, the pairs made and the pair still open, an `Option[i64]`, with `offer` (`mut ref self`) matching on it with a guard and `deletions` (`ref self`) |
| `beautiful_iter.kara` | a `fold` over the numbers carrying the pairs made and the open number as `(i64, Option[i64])`, the closure a `match` with a guard |
| `beautiful_solution.kara` | LeetCode's Rust template: a `Vec<i32>` in, `i32` out, an index stepping by one past a deleted number and by two past a pair, `usize` throughout, and `(n - ans as usize) % 2`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one number, two alike, already beautiful, and one value throughout),
each with its answer; then a checksum of 3000 random arrays of 1 to 30
numbers up to 1, 3 and 10^5 in turn; then the constraints' largest,
10^5 numbers of 0 and 1 and 10^5 alike. A number up to 10^5 is drawn
from two draws, since one stops at 32767. `beautiful.py` mirrors the ★
arm and its output is byte-identical.

`karac fix` carries the template in one round of 13 edits: `Vec<..>` to
`Vec[..]` three times, `let mut ans = 0` to `let mut ans: i32 = 0`, as
the function returns it, `i: usize` to `i: i64`, `n - ans as usize` to
`n - ans`, since an `i32` widens to `i64` on its own, the `|&x|` to
`|x|`, the adapter's `as i64` on the `i32` result dropped, `struct
Solution;` to `struct Solution {}` and `Solution::` to `Solution.`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to keep some of the numbers in order tried, each
kept array checked for an even length and no pair at an even index
alike, and the fewest deletions that leave a beautiful array; no greed.
It checks 300 random arrays of 1 to 12 numbers up to 1, 3 and 10^5 in
turn; then 30 of one value; then 30 of runs of 1 to 4 alike. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the deletions are the statement read literally |
| P2 | they are from 0 to n, and n less them is even |
| P3 | every number x made 10^5 - x: the same deletions |
| P4 | a pair 0, 1 put in front: the same deletions |
| P5 | the first number appended again: one deletion more or one fewer |
| P6 | each arm agrees with at least three of the other five |

P5 holds because the kept length is even and can grow by at most two
when a number is added, never shrink, so the deletions move by one
either way.

The differential prints `360 cases: checksum 136122024, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading over
`itertools.combinations` of the kept indices. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm, five to each of
the other Kāra arms and to the template arm, each run under `karac
__mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an odd length left as it is | P1 236, P2 236, P5 245, P6 236 |
| M4 | ★: the last pair never looked at | P1 81, P6 81 |
| M5 | ★: two alike above 3 kept | P1 10, P3 153, P6 10 |
| M7 | stack: a number alike its pair's first kept | P1 57, P3 57, P6 57 |
| M10 | stack: a first number of 0 counted as a deletion | P1 91, P2 91, P3 91, P4 269, P6 91 |
| M11 | stack: the first number never kept | P1 117, P4 66, P6 117 |
| M12 | pairs: a partner looked for from the pair's own number | P1 360, P2 360, P4 360, P6 360 |
| M14 | pairs: every pair counted once for the deletions | P1 273, P2 149, P4 360, P5 121, P6 273 |
| M15 | pairs: a partner at most two on | P1 88, P6 88 |
| M17 | struct: a pair closed by a number alike | P1 286, P4 292, P6 286 |
| M18 | struct: a closed pair left open | P1 207, P2 172, P4 249, P6 207 |
| M21 | struct: a pair of numbers above 50000 not counted | P1 73, P3 255, P6 73 |
| M23 | iter: a number alike its open first opening anew | P1 65, P6 65 |
| M24 | iter: the deletions one pair short | P1 273, P4 87, P6 273 |
| M26 | iter: a pair closed by any number above 2 | P1 34, P3 135, P6 34 |
| M30 | solution: the walk starting at the second number | P1 122, P4 59, P6 122 |
| M31 | solution: a pair skipping three | P1 60, P4 128, P6 60 |

P1 and P6 kill all seventeen, P4 nine, P2 and P3 five each, and P5 two.
P4 puts a beautiful pair in front, so it kills the edits that treat the
start of the array apart or step through pairs wrongly (M10, M11, M12,
M14, M17, M18, M24, M30, M31). P3 turns every number x into 10^5 - x,
and kills the edits that read a number's size: above 3, 50000 or 2, or
equal to 0 (M5, M7, M10, M21, M26). P2 kills the edits whose answer
leaves an odd length or runs past n (M1, M10, M12, M14, M18). P5 kills
only the two that ignore the parity altogether (M1, M14); every other
edit still moves by one when a number is added.

Of the thirty-one, fourteen were not kept, and every one is killed;
none crashes, none differs between the backends, and none survives.
Four fail as a kept one does: an odd length costing two in the ★ arm,
the stack arm's last unpaired number kept and the template's odd length
left as it is (M6, M8, M29), as the ★ arm's M1; and the iter arm's fold
from the second number (M25) as the stack arm's first number never kept
(M11). Six fail in pairs and neither of a pair is kept: the ★ arm's
index not shifted by deletions and the template's deleted number
skipping two (M2, M28); the ★ arm's pair alike at an odd index deleted
too and the stack arm's new pair opened only on a new number (M3, M9);
and the pairs arm's next pair from the partner and the iter arm's pair
closed keeping the second open (M13, M22). Four fail their own way and
are left out for the count of three (two for the template): the pairs
arm's walk stopping at the first long run (M16), the struct arm's
number alike its open first replacing it and its numbers seen from the
second (M19, M20), and the template's numbers made 0 and 1 (M27).

## Verification

Every arm prints the same output as `beautiful.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 s to 0.6 s, and the
differential 0.9 s.

## Benchmarks

The bench draws 60 arrays of 10^5 numbers once, up to 1, 3 and 10^5 in
turn, then punches each array 20 times, one number taking its
neighbour's value each time, and answers it after each punch with the ★
arm in all five languages. Every implementation prints `60 arrays of
10^5, 20 punches: checksum 124460599`.

BENCHTAB
