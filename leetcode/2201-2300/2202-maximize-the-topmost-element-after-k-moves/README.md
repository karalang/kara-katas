# 2202. Maximize the Topmost Element After K Moves

You are given a **0-indexed** integer array `nums` representing the
contents of a **pile**, where `nums[0]` is the topmost element of the
pile.

In one move, you can perform **either** of the following:

- If the pile is not empty, **remove** the topmost element of the pile.
- If there are one or more removed elements, **add** any one of them
  back onto the pile. This element becomes the new topmost element.

You are also given an integer `k`, which denotes the total number of
moves to be made.

Return *the **maximum value** of the topmost element of the pile possible
after **exactly** `k` moves*. In case it is not possible to obtain a
non-empty pile after `k` moves, return `-1`.

```
nums = [5,2,2,4,0,6], k = 4  ->  5
nums = [2],           k = 1  ->  -1
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i], k <= 10^9`.

The top after exactly k moves is either a number taken off and put back
last, which takes it and everything above it off and one move to put it
back, so any of the first k - 1; or the number left exposed by k
removals, the one at index k. Moves left over are spent taking another
number off and putting it back, which a lone number cannot do: it is on
top only after an even k. O(min(n, k)).

## Approaches

| file | mechanism |
|---|---|
| `top.kara` ★ | a lone number by the parity of k; otherwise the largest of the first k - 1 numbers by `max` in a loop, against the number at index k when there is one |
| `top_prefix.kara` | the running maxima pushed into a `Vec`, so the best of the first k - 1 is one lookup, against the number at index k. O(n) |
| `top_struct.kara` | a `struct Pile` with the numbers and the moves, whose `can_top(i)` says whether index i can be on top after exactly the moves, and `best_top` takes the largest number that can. O(n) |
| `top_iter.kara` | the first k - 1 numbers by `take`, `chain`ed with the one at index k by `skip` and `take(1)`, then `max` and `unwrap_or(-1)` |
| `top_rank.kara` | the indices `sort_by` their numbers, largest first, and the first one that can be on top after exactly k moves returned. O(n log n) |
| `top_solution.kara` | LeetCode's Rust template: `Vec<i32>` and an `i32` in, k turned to a `usize` and the put-back count taken by `saturating_sub`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's two examples and five
more (one number after two moves, the second number after one, every
number removed but the largest last, no move at all, and k far past the
pile), each with its top; then the count of empty piles and a checksum
for 3000 random piles of 1 to 12 numbers up to 20, with k from 0 to 15;
then the constraints' largest, 10^5 numbers up to 10^9 asked at k = 0,
1, the middle, n - 1, n, n + 1 and 10^9. `top.py` mirrors the ★ arm and
its output is byte-identical.

`karac fix` carries the template in two rounds of 3 and 3 edits: first
Rust's spellings (`Vec<i32>` to brackets and `struct Solution;` to
`struct Solution {}`); then `k as usize` to `k as i64`, since
`nums.len()`, and so `n` and the indices, is an `i64` in Kāra, a type
written on `best` so that it stays the template's `i32`, and the
adapter's `as i64` on the `i32` answer dropped, since an `i32` widens
to `i64` implicitly.

The struct arm hands `nums.clone()` to the `Pile` literal. Written
first as `Pile { nums: nums, moves: k }`, it gives away a bare
parameter, and `karac fix` takes the diagnostic's first mend: it writes
`own` on the parameter, then on the harness's `show`, which calls it,
and `.clone()` at a call in a loop, and stops on `println(f"{nums}, k
{k} -> {maximum_top(nums, k)}")` in `show`, where the f-string's
`{nums}` still borrows what the call moves, E0516 with no fix. kara
B-2026-11-15-40 asks for the `.clone()` there. The arm takes the other mend
the first diagnostic names.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every sequence of k moves played out, each a removal of the
top or one of the removed numbers put back, the piles and hands each
move can reach kept once each in a `Set` of text keys, and the largest
top among those left after the last. A long k is cut to the first k
past n + 1 of the same parity; a Python search with no cut, over every
pile of 1 to 5 numbers up to 3 and k up to n + 8, reaches the same top.
It checks 300 random piles of 1 to 6 numbers up to 9, 20 and 10^9 in
turn, with k from 0 to 9; then 30 of a single number; then 30 with k
from 10^8 to 10^9. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the top is the statement read literally |
| P2 | it is one of the pile's numbers, or -1 only for a single number and an odd k |
| P3 | k two more: a top at least as large |
| P4 | every number past index k changed: the same top |
| P5 | every number one more: the top one more, or -1 still |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 154367049, 12960 checks
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
| M1 | ★: a lone number on top after an odd k | P1 85, P2 48, P6 85 |
| M3 | ★: the put-back reach k - 2 | P1 27, P2 3, P3 41, P6 27 |
| M4 | ★: the number at index k never exposed | P1 69, P2 50, P6 69 |
| M7 | prefix: the running maximum restarted at each number | P1 132, P3 27, P6 132 |
| M8 | prefix: the put-back best read one too far | P1 22, P6 22 |
| M9 | prefix: the put-back best from the first number only | P1 116, P3 33, P6 116 |
| M12 | struct: the exposed index one short | P1 83, P2 26, P6 83 |
| M14 | struct: a lone number on top after any k | P1 37, P6 37 |
| M15 | struct: the first index skipped | P1 146, P2 77, P6 146 |
| M17 | iter: the put-back count k | P1 34, P6 34 |
| M18 | iter: the exposed number from index k + 1 | P1 72, P2 7, P3 16, P4 58, P6 72 |
| M19 | iter: the exposed number and the one below it | P1 29, P3 13, P4 30, P6 29 |
| M22 | rank: the indices sorted smallest first | P1 218, P3 43, P6 218 |
| M25 | rank: the first in order taken unchecked | P1 57, P4 30, P6 57 |
| M26 | rank: a lone number left to the ranking | P1 27, P6 27 |
| M30 | solution: the adapter's k one less | P1 152, P2 38, P3 27, P6 152 |
| M31 | solution: the adapter's numbers reversed | P1 79, P4 53, P6 79 |
[('P1', 17), ('P2', 7), ('P3', 7), ('P4', 4), ('P6', 17)]

P1 and P6 kill all seventeen, P2 and P3 seven each, P4 four and P5 none.
P2 kills the seven that can answer -1 for a pile that has a top, or
answer for a lone number after an odd k (M1, M3, M4, M12, M15, M18,
M30). P3 adds two moves and kills the seven whose top can shrink as k
grows (M3, M7, M9, M18, M19, M22, M30). P4 changes the numbers no move
can reach and kills the four that read one of them (M18, M19, M25, M31).
P5 raises every number alike, which keeps the winning index wherever it
is, so no edit here, each wrong about an index or a parity, fails it; it
stands against an arm that reads a number for a count or an index.

Of the thirty-one, fourteen were not kept. Three are equivalent: the
prefix arm's lone number after an even k gone (M11) sits behind the
lone-number test already made, the iter arm's empty choice read as 0
(M21) never happens on a pile of two or more, and the rank arm's `i <=
k and i + 1 != k` (M23) is `i == k or i + 2 <= k` written another way.
Ten fail as a kept one does: the put-back reach k in the ★, struct and
template arms (M2, M13, M27) as M17; the rank arm's put-back test i + 3
(M24) as M3; the ★ arm's lone number handled as any pile (M6) as M26;
the number at index k - 1 exposed in the ★ and template arms (M5, M28)
as M12; the template's lone number always returned (M29) as M14; and
the smaller number kept and the smallest taken (M16, M20) as M22. One
fails its own way and is left out for the count: the prefix arm's
exposed number kept even past the pile (M10).

## Verification

Every arm prints the same output as `top.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.5 s to 1.2 s but the rank
arm, 8.1 s, which sorts the 10^5 indices for each of its seven largest
asks. The differential takes 0.4 s.

## Benchmarks

The bench builds 10 piles of 10^5 numbers up to 10^9 once, each with 10
values of k from 0 to 10^5 + 1, then asks each pile for each k 50 times
over with the ★ arm in all five languages. Every implementation prints
`50 passes over 10 piles: checksum 472052730`.

BENCHTAB
