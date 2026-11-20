# 2289. Steps to Make Array Non-decreasing

You are given a **0-indexed** integer array `nums`. In one step,
**remove** all elements `nums[i]` where `nums[i - 1] > nums[i]` for all
`0 < i < nums.length`.

Return *the number of steps performed until* `nums` *becomes a
**non-decreasing** array*.

```
nums = [5,3,4,4,7,3,6,11,8,5,11]   ->  3
nums = [4,5,7,7,13]                ->  0
```

In the first, the steps leave `[5,4,4,7,6,11,11]`, then `[5,4,7,11,11]`,
then `[5,7,11,11]`.

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`.

An element is removed only by the nearest larger element to its left,
once everything between them is gone. So it goes one step after the
last of the elements between them, all of which are not larger than it,
or at step 1 when there are none; with no larger element to its left it
stays. A stack of the elements still standing, each with its step,
finds the nearest larger element and the latest step between in one
pass. O(n).

## Approaches

| file | mechanism |
|---|---|
| `steps.kara` ★ | from the left, a `Vec[(i64, i64)]` stack of value and step; each element pops every one not larger, keeping the largest step, and goes one step after it, or never with the stack empty |
| `steps_naive.kara` | the steps done: each builds the array of the first element and every element not smaller than the one before it, until a step removes nothing. O(n * steps) |
| `steps_list.kara` | `struct Line` of the values and `prev` / `next` links; each step removes the elements to check that are smaller than their predecessor, unlinks them, and checks next the elements that now follow them. O(n) |
| `steps_scan.kara` | for each element, a scan leftwards to the nearest larger one, taking the latest step on the way; a `Vec.filled(n, 0)` of steps. O(n^2) |
| `steps_iter.kara` | from the right, `iter().rev().fold` of a stack and the answer: each element eats the smaller ones on the stack, needing one step more than the last eaten or as many as that one needed |
| `steps_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; the ★ arm's stack read with `while let Some(&(v, s)) = st.last()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; one
element; all equal; strictly falling, which takes one step; `[10, 1, 2,
.., 6, 1, 2, 3]`, where 10 eats the run one element a step; a saw of
falling runs, all gone in one step; a large element before a rising run
of 1999, which takes 1999 steps; then 3000 random arrays of 1 to 60
elements from 1 to `top`, `top` from 1 to 50, with a checksum and the
steps in all. `steps.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one call, reporting 12 edits:
`struct Solution;` to `struct Solution {}`; the brackets of
`Vec<i32>` and `Vec<(i32, i32)>`; `vec![]` to `Vec.new()`; `ans` and
`t`, both returned or stored as `i32`, annotated `i32`, since a literal
keeps `i64` otherwise; the `&` of `for &x` dropped; `while let
Some(&(v, s)) = st.last()` to `while let Some((v, s)) =
st.last().cloned()`; and the harness's `as i64` on the template's
answer dropped, since an `i32` widens to `i64` by itself.

The iterator arm's `fold` closure was first written as Rust would take
its accumulator, `|(mut stack, mut most): (Vec[(i64, i64)], i64), x|`.
`karac fix` moves the two `mut`s out of the pattern and rebinds the
names in the body, three edits. An annotated closure parameter borrows
(D5), so the rebinds then copied a borrowed `Vec`, and the compiler
answered with a bare "expected `Vec[?T1]`, found `ref Vec`" and an
E0517 with no word of `own`, which a closure parameter that is a
single name gets with its fix. A tuple pattern now gets the same, and
`karac fix` writes `|(stack, most): own (Vec[(i64, i64)], i64)|`,
a fourth edit (B-2026-11-18-87).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a `Vec[bool]` of the elements still standing; a step looks,
for each one standing, back past the removed ones to the nearest one
still standing, and removes, all at once, every element that one is
larger than; the steps are counted until a step removes nothing. It
checks 300 random arrays drawn as the arms' harness draws them; then 30
of 1 to 8 falling runs one after another, each of 1 to 10 elements
falling by 0 to 2; then 30 of a large element before a rising run of 1
to 80 with about one element in ten small. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `0 <= answer < n`, and the answer is 0 just when the array does not decrease anywhere |
| P3 | an element as large as the largest appended: the same answer |
| P4 | an element larger than all put in front: at least one step, and no fewer than before |
| P5 | the last element dropped: no more steps |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 807726352, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that does
the steps by list comprehension. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: the answer the last step | P1 262, P2 26, P3 319, P5 107, P6 262 |
| M5 | ★: the step summed | P1 277, P6 277 |
| M6 | ★: the stack never popped | P1 266, P2 12, P3 63, P6 266 |
| M7 | naive: the first element dropped | P1 238, P2 15, P3 360, P6 238 |
| M10 | naive: the order inverted | P1 295, P2 11, P3 14, P4 18, P6 295 |
| M11 | naive: compared with the original | P1 222, P4 63, P6 222 |
| M13 | list: equal elements fall | P1 185, P2 8, P3 184, P6 185 |
| M15 | list: the steps from 1 | P1 360, P2 21, P6 360 |
| M16 | list: the first link cut | P1 49, P2 7, P4 15, P6 49 |
| M17 | scan: the latest not carried | P1 333, P6 333 |
| M19 | scan: the first element skipped | P1 226, P2 12, P3 360, P6 226 |
| M21 | scan: the answer the last step | P1 253, P5 91, P6 253 |
| M22 | iter: the need summed | P1 323, P6 323 |
| M24 | iter: the eaten one's need ignored | P1 105, P6 105 |
| M25 | iter: the most the first need | P1 312, P5 47, P6 312 |
| M28 | solution: the step not added | P1 345, P2 345, P4 360, P6 345 |
| M29 | solution: the stack not emptied | P1 252, P3 50, P6 252 |

P1 and P6 kill all seventeen, P2 nine, P3 seven, P4 four and P5
three. P3, a largest element appended, can never fall and removes
nothing, so it fails where an arm lets the last element decide the
answer, drops or skips the first element, or treats an equal or a
larger element as one it may eat. P5 fails only where the answer is the
last element's step rather than the most of all. P4, a larger element
put in front, makes every element fall in the end, so it fails where an
arm stops short of a long fall: the steps never added, the second
element never checked, the order inverted, or the comparison made
against the array as it began.

The first draft's P4 was every element times 3, plus 7: the same
answer. No arm reads a value except to compare it, so no edit made to
an arm broke it and it killed none of the thirty-one; it was replaced
by the larger element in front.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Equal elements eaten or removed fails the same
way in every arm it is made to (M1, M8, M18, M23, M27), and so does
list's equal elements fall (M13), the one kept. Six fail as the scan
arm's latest not carried (M17) does, by losing only the steps between:
the ★ arm's step not carried (M2), the list arm's predecessor not
relinked and follower never checked (M12, M14), the scan arm's step the
latest alone (M20) and the template's answer at most one (M30). A lone
element one step in the ★ arm and the template's step not reset (M3,
M31) fail as the naive arm's first element dropped (M7); the naive
arm's one step more (M9) as the list arm's steps from 1 (M15). The iter
arm's fold from the left (M26) fails in a way of its own and is left
out because its arm keeps enough.

## Verification

Every arm prints the same output as `steps.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ and iterator arms take 0.5 s, the list and
template arms 0.8 s, the naive arm, which does the 1999 steps of the
long case one by one, 1.1 s, and the scan arm, which scans that case's
rising run back to its start for every element, 1.5 s. The differential
takes 1.4 s.

## Benchmarks

The bench builds 50 arrays of 10^4 elements once, element `i` being `3i`
plus noise up to 20000, so that elements fall in long runs behind a
large one, then makes 20 passes over all of them summing the answers,
with the ★ arm in all five languages. Every implementation prints `20
passes over 50 arrays of 10^4: checksum 418235629`. C keeps the stack
as two arrays allocated once, where the others push and pop a vector
of pairs.

BENCHTAB
