# 2411. Smallest Subarrays With Maximum Bitwise OR

You are given a **0-indexed** array `nums` of length `n`, consisting of
non-negative integers. For each index `i` from `0` to `n - 1`, you must
determine the size of the **minimum sized** non-empty subarray of `nums`
starting at `i` (**inclusive**) that has the **maximum** possible
**bitwise OR**.

In other words, let `B_ij` be the bitwise OR of the subarray `nums[i...j]`.
You need to find the smallest subarray starting at `i`, such that
bitwise OR of this subarray is equal to `max(B_ik)` where `i <= k <= n -
1`.

Return *an integer array* `answer` *of size* `n` *where* `answer[i]` *is
the length of the **minimum** sized subarray starting at* `i` *with
**maximum** bitwise OR.*

```
nums = [1,0,2,1,3]   ->  [3,3,2,2,1]
nums = [1,2]         ->  [2,1]
```

**Constraints:** `1 <= n <= 10^5`; `0 <= nums[i] <= 10^9`.

The largest OR from `i` is the OR of the whole suffix, since an OR only
gains bits as the subarray grows. It is reached once every bit set in
the suffix is covered, so the subarray from `i` ends at the farthest of
the nearest positions of those bits. `10^9` is below `2^30`, so 30 bits
suffice.

## Approaches

| file | mechanism |
|---|---|
| `subarrays.kara` ★ | the nearest of each bit: walking from the right, the nearest index holding each of the 30 bits, the subarray from `i` reaching the farthest of them. O(30 n) |
| `subarrays_ors.kara` | the distinct ORs: from each start the ORs of longer subarrays take at most 31 values; the list for `i` is `nums[i]` and each of `i + 1`'s ORed with it, each value with the shortest end that gives it. O(30 n) |
| `subarrays_window.kara` | a window of bit counts: walking `i` from the right, `nums[i]` joins and the window's last value leaves while every bit it holds is held elsewhere. O(30 n) |
| `subarrays_sparse.kara` | a sparse table of ORs, any range two overlapping blocks; the target the suffix OR, the shortest length reaching it by halving. O(n log n) |
| `subarrays_iter.kara` | iterators: the ★ arm's nearest bits, the starts by `rev`, a value's bits by `filter`, the farthest by `max`. O(30 n) |
| `subarrays_solution.kara` | LeetCode's Rust template: a `[0usize; 32]` of each bit's last index, the starts by `(0..n).rev()`, each length by `last[b] as i32 - i as i32 + 1`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one 0;
three zeros; the powers of two to 16, then 0 and 1; `10^5` values up to
`10^9`, a fiftieth of them 0, and `10^5` below 16, a third of them 0, each
by a checksum of the lengths and their total; then 2000 random arrays of
up to 30 values below 1 to 64, with a checksum of every length and their
total. `subarrays.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 20000 random arrays of up
to 10 values against the ORs of every subarray.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 8 edits: both `Vec<i32>` given their brackets;
`struct Solution;` given its braces; `[0usize; 32]` written `[0; 32]`;
and `vec![1; n]` written `Vec.filled(n, 1i32)`. The `as i32` casts in
each length, `nums[i] >> b & 1` and `(0..n).rev()` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: from every start, the OR of every subarray computed afresh,
the largest found, and the shortest subarray giving it. No bit tracking.
It checks 300 random arrays of 1 to 12 values below 1 to 64, a quarter
of them 0, which the literal reading answers; then 30 of up to 3000
values up to `10^9`, a fiftieth of them 0; then 30 of up to 3000 values
below 16, a third of them 0. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 values, the answers are the literal reading's |
| P2 | from every start, the subarray of the answer's length has the suffix's OR, and one shorter does not |
| P3 | a 0 appended: the same answers, and 1 for the 0 |
| P4 | the first value dropped: the answers from the second on |
| P5 | the array written twice: the second copy's answers are the array's |
| P6 | each arm agrees with at least three of the other five |

P2 checks every case, the large ones too, by ORing each answer's
subarray once. P3 holds because a 0 adds no bit, and P4 and P5 because
an answer depends only on the suffix from its start.

The differential prints `360 cases: checksum 935910227, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and ORs every subarray. On a failure it prints the first
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
| M4 | ★: the farthest of each bit kept | P1 183, P2 243, P6 243 |
| M5 | ★: the reach starting at index 0 | P1 83, P2 95, P3 360, P4 95, P5 103, P6 95 |
| M6 | ★: bit 0 never read | P1 69, P2 129, P6 129 |
| M7 | ors: an OR kept again when it gains nothing | P1 211, P2 271, P3 360, P6 271 |
| M9 | ors: the shortest OR's end taken | P1 246, P2 306, P6 306 |
| M10 | ors: the new value never ORed in | P1 202, P2 262, P3 257, P6 262 |
| M13 | window: the counts never lowered | P1 132, P2 192, P6 192 |
| M14 | window: a window of at least two | P1 131, P2 161, P3 360, P6 161 |
| M16 | window: bit 29 never needed | P2 30, P6 30 |
| M18 | sparse: a fitting end lowered past | P1 175, P2 235, P3 295, P6 235 |
| M19 | sparse: the target the value alone | P1 246, P2 306, P3 306, P6 306 |
| M21 | sparse: the rows never combined | P1 190, P2 250, P3 293, P6 250 |
| M22 | iter: each answer one short | P1 300, P2 360, P3 360, P6 360 |
| M25 | iter: each bit placed one later | P1 288, P2 348, P6 348 |
| M26 | iter: the bits a value lacks placed | P1 245, P2 305, P3 257, P6 305 |
| M30 | solution: bits 0 and 1 never read | P1 131, P2 191, P6 191 |
| M31 | solution: a bit read only beside the next | P1 188, P2 248, P6 248 |

P2 and P6 kill all seventeen, P1 sixteen, P3 nine, and P4 and P5 one
each. P1 misses the window arm's bit 29 never needed (M16), since P1's
small cases hold no value that high. P4 and P5 compare an arm's answers
with its own answers on the array less its first value or written
twice, and a mutant wrong at an index is wrong the same way there; only
the reach starting at index 0 (M5), whose error depends on where the
array starts, fails them.

Of the thirty-one, fourteen were not kept, each failing the same checks
as a kept one or, for two, left over: bit 29 never read or counted (M1,
M15, M23) as bit 29 never needed (M16); only bit 29's nearest reached,
each longer OR ending one later, the nearest of the nearest taken, no
bit ever recorded and the template's each answer one short (M2, M8,
M24, M27, M28) as the shortest OR's end taken (M9); each answer one
short and each start ending one later (M3, M11) as the iter arm's each
answer one short (M22); a value kept while its bits are held twice
(M12) as the farthest of each bit kept (M4); and the template's bit 0
never read (M29) as the ★ arm's (M6). The sparse arm's only the range's
first block read (M17) and last end never tried (M20) fail apart from
every kept one, and were left out because that arm keeps three already.
Two were replaced by edits that fail apart from every kept one: the
iter arm's and the template's starts walked forward (M26, M30), which
failed as M9, are now the bits a value lacks placed and bits 0 and 1
never read.

## Verification

Every arm prints the same output as `subarrays.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.0 to 9.3 s, except the iter
arm at 14.0 s. The differential takes 88 s there, 18 s under `karac
__mir-llvm-asan` and 1.4 s under `karac run`.

## Benchmarks

The bench builds 5 arrays of `10^5` values, array `i` below `2^(6 i +
6)`, once from the harness's generator, then makes 10 passes, answering
every array and folding each length plus the pass into the checksum,
with the ★ arm in all five languages. Every implementation prints `10
passes over 5 arrays of 10^5 values: checksum 781024284`. Each
allocates the answer in every call and walks the same 30 bits per value;
Kāra, Rust and Go check every index, and C does not.

BENCHTAB
