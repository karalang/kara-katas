# 2401. Longest Nice Subarray

You are given an array `nums` consisting of **positive** integers.

We call a subarray of `nums` **nice** if the bitwise **AND** of every
pair of elements that are in **different** positions in the subarray is
equal to `0`.

Return *the length of the **longest** nice subarray*.

A **subarray** is a **contiguous** part of an array.

**Note** that subarrays of length `1` are always considered nice.

```
nums = [1,3,8,48,10]   ->  3    ([3,8,48])
nums = [3,1,5,11,13]   ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`.

A window is nice exactly when no bit is set in two of its values, so it
holds at most 30 values, and its OR says which bits are taken.

## Approaches

| file | mechanism |
|---|---|
| `nice.kara` ★ | a sliding window keeping the OR of its values; values leave from the left, their bits taken off by XOR, until the new value fits. O(n) |
| `nice_bits.kara` | the last index of each of the 30 bits: a window ending here starts one past the latest index that set any of this value's bits. O(30 n) |
| `nice_extend.kara` | from every start, the window grown right while the next value shares no bit with the OR so far; no window passes 30 values. O(30 n) |
| `nice_binary.kara` | binary search on the length, each length checked by sliding a window of exactly that size with a count of the values setting each bit. O(30 n log n) |
| `nice_iter.kara` | iterators: for each end, the values before it walked back by `rev` and `scan`, the OR carried and the walk stopped at the first clash; `count` and `max` give the answer. O(30 n) |
| `nice_solution.kara` | LeetCode's Rust template: the sliding window with the OR in an `i32`, `usize` indexes, `(r, &x)` over `nums.iter().enumerate()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one value;
every power of two up to `2^29` in order, and then twice over; `10^5`
values up to `10^9`; `10^5` values of one bit each; then 3000 random
arrays of 1 to 20 values, each of one to three of 12 bits, with a
checksum and the total. `nice.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 20000 random arrays of up
to 10 values against every subarray's every pair.

`check` first reports 6 errors on the template, and `karac fix` carries
it in one call, reporting 10 edits: `struct Solution;` given its
braces; the angle brackets of `Vec<i32>` made square; the `mut` of each
name in `let (mut used, mut l, mut ans)` moved before the pattern, `let
mut (used, l, ans)`; the `&` of `(r, &x)` dropped; and `0usize` written
`0`, twice. `0i32`, `ans.max(r - l + 1)` and `ans as i32` stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray, and in it every pair of distinct values
ANDed, the longest whose pairs all give 0 kept. No running OR. It checks
300 random arrays of 1 to 12 values, each of one or two of 8 bits, which
the literal reading answers; then 30 of up to 3000 values of one to
three of 30 bits; then 30 of up to 3000 values up to `10^9`. All 360
are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 values, the answer is the literal reading's |
| P2 | some window of the answer's length is nice, and none one longer |
| P3 | the values reversed: the same answer |
| P4 | the OR of every value appended: the same answer |
| P5 | the first value dropped: the answer or one less |
| P6 | each arm agrees with at least three of the other five |

P2 checks each window by its sum: values that share no bit sum to their
OR, and values that share one sum to more. P3 holds because a window
reversed holds the same values, P4 because the OR shares a bit with
every value, so no window of two or more can hold it, and P5 because
dropping a value shortens at most the windows that held it, by one.

The differential prints `360 cases: checksum 813851925, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and ANDs every pair. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the whole OR dropped for one value leaving | P1 164, P2 196, P6 196 |
| M2 | ★: one value leaving at most | P1 129, P2 159, P3 102, P5 4, P6 159 |
| M6 | ★: the last window kept | P1 123, P2 160, P3 196, P4 231, P6 160 |
| M7 | bits: the start allowed back | P1 201, P2 261, P3 189, P4 28, P6 261 |
| M8 | bits: no bit's index ever kept | P1 229, P2 289, P4 360, P6 289 |
| M10 | bits: a bit read only when the next is clear | P1 46, P2 81, P4 10, P6 81 |
| M12 | extend: a value with a new bit taken as fitting | P1 160, P2 220, P3 165, P4 43, P6 220 |
| M13 | extend: the OR only the newest value | P1 157, P2 187, P6 187 |
| M16 | extend: each start taken unchecked and left out of the OR | P1 197, P2 257, P3 78, P4 37, P6 257 |
| M17 | binary: a clash only at a third value | P1 222, P2 280, P3 140, P4 89, P5 78, P6 280 |
| M18 | binary: a value leaving one late | P1 109, P2 138, P3 154, P5 92, P6 138 |
| M20 | binary: a failed length lowering the bound by two | P1 67, P2 82, P4 75, P5 38, P6 82 |
| M24 | iter: the end itself left out | P1 117, P2 117, P3 78, P4 117, P6 117 |
| M25 | iter: the shortest end's window | P1 255, P2 293, P6 293 |
| M26 | iter: a shared bit 0 allowed | P1 39, P2 46, P4 5, P6 46 |
| M27 | solution: each window one short | P1 300, P2 360, P6 360 |
| M28 | solution: a shared bit 29 allowed | P2 8, P6 8 |

P2 and P6 kill all seventeen, P1 sixteen, P4 ten, P3 eight and P5 four.
P1 misses only the template's shared bit 29 allowed (M28): its cases
hold values of 8 bits, and only the cases of 30 bits reach bit 29. P5,
the first value dropped, fails the four edits that let a window's start
lag behind a clash (M2, M17, M18, M20), whose answers can then grow
when a value is taken away.

Of the thirty-one, fourteen were not kept. The ★ arm's each window one
short, the extend arm's too and the iter arm's every value a clash (M3,
M14, M22) fail as the template's each window one short (M27); the bits
arm's every bit last seen at index 0 as the extend arm's never from the
first value (M11, M15); the extend arm's OR only the newest value (M13)
as the iter arm's each value checked against the one after alone (M23);
the bits arm's bit 29 never read (M9) as the template's M28; and the
template's one value leaving at most and last window kept (M30, M31) as
the ★ arm's M2 and M6. The ★ arm's OR only the newest value and first
value never read (M4, M5) stop with an index out of range under both
backends. The binary arm's whole length never tried and full window
enough (M19, M21) each fail apart from every kept one, and were left out
to keep three to an arm. The template's M28 and M29 were first only each
value's lowest bit kept and the first value skipped, which both stopped
with an index out of range; they were replaced by a shared bit 29
allowed (M28) and the last value never read (M29), and M29 then failed
as the iter arm's end itself left out (M24).

## Verification

Every arm prints the same output as `nice.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.75 to 9.0 s. The differential
takes 34 s there, 7.9 s under `karac __mir-llvm-asan` and 1.2 s under
`karac run`.

## Benchmarks

The bench builds 20 arrays of `10^5` values, each of one or two of 30
bits, once from the harness's generator, then makes 20 passes,
answering every array and folding each answer plus the pass into the
checksum, with the ★ arm in all five languages. Every implementation
prints `20 passes over 20 arrays of 10^5 values: checksum 54750190`.
No implementation allocates in the window.

BENCHTAB
