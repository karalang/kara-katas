# 2460. Apply Operations to an Array

You are given a **0-indexed** array `nums` of size `n` consisting of
**non-negative** integers.

You need to apply `n - 1` operations to this array where, in the `i`th
operation (**0-indexed**), you will apply the following on the `i`th
element of `nums`:

- If `nums[i] == nums[i + 1]`, then multiply `nums[i]` by `2` and set
  `nums[i + 1]` to `0`. Otherwise, you skip this operation.

After performing **all** the operations, **shift** all the `0`'s to the
**end** of the array.

- For example, the array `[1,0,2,0,0,1]` after shifting all its `0`'s to
  the end, is `[1,2,1,0,0,0]`.

Return *the resulting array*.

**Note** that the operations are applied **sequentially**, not all at
once.

```
nums = [1,2,2,1,1,0]  ->  [1,4,2,0,0,0]
nums = [0,1]          ->  [1,0]
```

**Constraints:** `2 <= nums.length <= 2000`; `0 <= nums[i] <= 1000`.

The operations run left to right, so a merge's zero is what the next
operation sees: `[2, 2, 2]` becomes `[4, 0, 2]`, not `[2, 4, 0]`, and
a zero met by a zero only stays a zero. After that the shift is a
stable partition, the nonzero values in order and then the zeros.

## Approaches

| file | mechanism |
|---|---|
| `apply.kara` ★ | the operations in place, then the nonzero values moved forward in order by a write index, and the rest set to zero. O(n) |
| `apply_naive.kara` | the statement read directly: the operations in place, then every zero shifted toward the end one place at a time, swapped with a nonzero value after it, sweep after sweep until none moves. O(n^2) |
| `apply_pairs.kara` | one pass building the answer: a zero skipped, a value equal to the next pushed doubled and the next skipped with it, since the zero the operation leaves there can only meet another zero, and any other value pushed as it is; then zeros to the length. O(n) |
| `apply_swap.kara` | one loop doing both: at each place the operation applied, and the value left there, if nonzero, swapped back to the next free place; the operation at `i` reads only places `i` and `i + 1`, which no swap has touched yet. O(n) |
| `apply_iter.kara` | iterators: the operations by `scan`, carrying the value standing at the current place and meeting it with the next, a sentinel `-1` closing the list; then the nonzero values by `filter`, chained with the zeros. O(n) |
| `apply_solution.kara` | LeetCode's Rust template: `mut nums: Vec<i32>` taken by value, the operations in place, the nonzero values by `iter().copied().filter(\|&x\| ..)`, and the length restored by `resize`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples; then six
more, a run of equal values merging in pairs, zeros between equal
values, all zeros, a zero meeting a zero, the constraints' largest
value doubled, and a run of doubled values that the earlier merges set
next to each other; the constraints' largest, 2000 values of 1000 and
2000 alternating 1000 and 0; 2000 random values from 0 to 1000 and 2000
from 0 to 3; and 3000 random arrays of 2 to 12 values from 0 to 2, as
checksums. `apply.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on every array of 2 to 8
values from 0 to 3 against the operations and the one-place shifts done
by hand.

`check` first reports 6 errors on the template, and `karac fix` carries
it in one call, reporting 11 edits: `mut nums: Vec<i32>` written `nums:
own Vec[i32]` with `let mut nums = nums;` at the body's start, since a
parameter's mode is in its type; the brackets of each `Vec<..>`; the
`&` of the closure's pattern `|&x|` dropped; `struct Solution;` given
its braces; and, once the template parses, `copied()` written
`cloned()`, Kāra's one name for copying items out of an iterator.
`nums[i] *= 2`, the `i32` values and `res.resize(n, 0)` stand as
Kāra.

`apply_iter.kara` chains `nums.iter().skip(1)`, an iterator of `ref
i64`, with `once(-1)`, an iterator of `i64`, so it takes `.cloned()`
first, as Rust would take `.copied()`; `check` says so in the
diagnostic.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the `n - 1` operations on a copy, each place `i` compared
with `i + 1` in turn, then the zeros shifted to the end one at a time,
the first zero that stands before a nonzero value removed and pushed
onto the end, until none does. It checks 300 random arrays of 2 to 12
values from 0 to 2; then 30 of up to 200 values from 0 to 1000; then 30
of up to 200 values from 0 to 3. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer as long as the input, with the same sum |
| P3 | no zero before a nonzero value, and no more nonzero values than the input has |
| P4 | a zero put after the input: the answer with a zero after it |
| P5 | every value doubled: every answer doubled |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a merge turns `v, v` into `2v, 0`, keeping the sum. P3
holds because a merge only turns values into zeros. P4 holds because the
added zero meets the last value, which either differs or is zero itself,
and is then shifted to the end with the rest. P5 holds because doubling
keeps every equality and every zero.

The differential prints `360 cases: checksum 424447383, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases, applies the operations and puts the nonzero values
before the zeros. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the merged value not doubled | P1 232, P2 232, P6 232 |
| M3 | ★: the last operation skipped | P1 49, P4 49, P6 49 |
| M4 | ★: zeros kept in place | P1 297, P3 297, P6 297 |
| M7 | naive: one added instead of doubled | P1 245, P2 201, P3 78, P4 165, P5 274, P6 245 |
| M9 | naive: the zeros moved to the front | P1 325, P3 325, P4 356, P6 325 |
| M10 | naive: each value met with the one two along | P1 289, P2 204, P4 112, P6 289 |
| M12 | pairs: a zero pushed where it stands | P1 263, P3 263, P6 263 |
| M15 | pairs: the last value dropped | P1 195, P2 195, P4 195, P6 195 |
| M16 | pairs: the padding one short | P1 329, P2 329, P4 31, P6 329 |
| M17 | swap: the free place never advanced | P1 327, P3 283, P6 327 |
| M18 | swap: the first place never kept | P1 236, P3 151, P6 236 |
| M21 | swap: the last value never moved | P1 164, P3 164, P4 164, P6 164 |
| M23 | iter: the second value skipped | P1 360, P2 360, P6 360 |
| M24 | iter: a smaller value met as equal | P1 333, P2 333, P6 333 |
| M26 | iter: the zeros dropped | P1 329, P2 329, P4 360, P6 329 |
| M28 | solution: the first operation skipped | P1 63, P6 63 |
| M31 | solution: ones never merged | P1 144, P5 144, P6 144 |

P1 and P6 kill all seventeen, P2 and P4 eight, P3 seven and P5 two.

Fourteen are not kept. Seven fail exactly as a kept one: the ★ arm's
next left as it was, the pairs arm's next not skipped, the swap arm's
next given the doubled value and the iter arm's next not zeroed (M2,
M13, M19, M22) as the ★ arm's merged value not doubled (M1), each
answer one value too large and the sum raised by it; the pairs arm's
zeros met like any value (M14) as its zero pushed where it stands
(M12), both leaving zeros among the values; the naive arm's last pair never swapped (M11) as the swap
arm's last value never moved (M21); and the iter arm's zeros first
(M25) as the naive arm's zeros moved to the front (M9). Seven fail apart
from every kept one and were left out because those arms keep their
share already: the ★ arm's last place never cleared and operations
right to left (M5, M6); the naive arm's single sweep of swaps (M8); the
swap arm's merge kept on the right (M20); and the template's length
restored with ones, ones dropped with the zeros and two added instead
of doubled (M27, M29, M30).

## Verification

Every arm prints the same output as `apply.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.5 s but the naive arm,
1.7 s, and the differential 0.9 s; under `karac __mir-llvm-asan` the
differential takes 0.6 s and under `karac run` 0.4 s.

## Benchmarks

The bench builds 1000 arrays of 2000 values from 0 to 3 once from its
own generator, so equal neighbours are common, then makes 24 passes;
each sets one value of every array from the checksum so far, so no
answer carries over, then answers every array on a copy, folding every
value of the answer plus the pass into the checksum. The bench uses the
★ arm, the operations in place and then a write index, in all five
languages. Every implementation prints `24 passes over 1000 arrays of
2000: checksum 757000629`. The copy is the language's own: `clone` in
Kāra and Rust, `list` in Python, `append` onto a nil slice in Go and
`memcpy` into one buffer in C.

BENCHTAB
