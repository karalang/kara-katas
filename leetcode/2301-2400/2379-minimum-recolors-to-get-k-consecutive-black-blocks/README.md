# 2379. Minimum Recolors to Get K Consecutive Black Blocks

You are given a **0-indexed** string `blocks` of length `n`, where
`blocks[i]` is either `'W'` or `'B'`, representing the color of the
`i`th block. The characters `'W'` and `'B'` denote the colors white and
black, respectively.

You are also given an integer `k`, which is the desired number of
**consecutive** black blocks.

In one operation, you can **recolor** a white block such that it becomes
a black block.

Return *the **minimum** number of operations needed such that there is
at least **one** occurrence of* `k` *consecutive black blocks.*

```
blocks = "WBBWWBBWBW", k = 7  ->  3
blocks = "WBWBBBW", k = 2     ->  0
```

**Constraints:** `n == blocks.length`; `1 <= n <= 100`; `blocks[i]` is
either `'W'` or `'B'`; `1 <= k <= n`.

The `k` black blocks stand in some window of `k` places, and making a
window all black takes exactly its white blocks, so the answer is the
fewest white blocks in any window of `k`.

## Approaches

| file | mechanism |
|---|---|
| `recolor.kara` ★ | a sliding window: the whites of the first `k` counted, then the window moved one block at a time, counting the block that enters and dropping the one that leaves. O(n) |
| `recolor_prefix.kara` | prefix sums: `whites[i]` the white blocks before place `i`, each window's count a difference of two. O(n) |
| `recolor_each.kara` | every window counted afresh from its first block to its last. O(n k), at most 2500 steps |
| `recolor_queue.kara` | the most black blocks in a window, the window's blocks kept in a `VecDeque`, each new block pushed at the back and the oldest popped from the front once it holds `k`; the answer `k` less the most. O(n) |
| `recolor_iter.kara` | iterators: the blocks as 1 for white and 0 for black, the `sum` over each window's slice and the `min` of those |
| `recolor_solution.kara` | LeetCode's Rust template: the first window's whites by a `filter(\|&&c\| ..)` over `b[..k]` of `as_bytes()`, then the window slid along; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; one white
block; 100 white blocks with `k` of 100 and 100 alternating blocks with
every `k` from 1 to 100 summed; then 2000 random strings of 1 to 100
blocks, white with a chance of 0 to 9 in 10, and `k` from 1 to their
length, with a checksum and how many need no recoloring. `recolor.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 5000 random strings of up to 30 blocks against the fewest
whites over every window.

`check` first reports 3 errors on the template, and `karac fix` carries
it in one call, reporting 6 edits: `struct Solution;` given its braces;
`as_bytes()` written `bytes()`; `k as usize` written `k as i64`, since
Kāra indexes by `i64`; the `&&` of `|&&c|` dropped; and `Solution::`
written with a dot and the wrapper's `as i64` dropped, since an `i32`
widens. The slice `b[..k]`, `.count() as i32` and `res.min(w)` stand as
Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of white blocks recolored, and the smallest set
that leaves `k` black blocks in a row kept. No windows. It checks 300
random strings of 1 to 12 blocks, which the literal reading answers;
then 30 of up to 100; then 30 of up to 100 nearly all black, white
with a chance of 1 in 10. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 12 blocks, the answer is the literal reading's |
| P2 | from 0 to `k`, and 0 exactly when `k` black blocks already stand in a row |
| P3 | the blocks reversed: the same answer |
| P4 | a black block appended: the answer or one less |
| P5 | `k` one more, while it fits: the answer or one more |
| P6 | each arm agrees with at least three of the other five |

P3 holds because the windows of the reversed blocks are the old windows
reversed, with the same whites. P4 holds because the only new window
is the last old one moved on by a block, which drops one block and
gains a black one, and P5 because each window of `k + 1` holds a window
of `k` and one block more.

The differential prints `360 cases: checksum 974508599, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries the sets of whites from the smallest up. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a leaving block never dropped | P1 66, P2 47, P3 133, P6 97 |
| M3 | ★: the fewest taken by max | P1 126, P2 79, P6 172 |
| M4 | ★: the leaving block one place late | P1 40, P2 35, P3 66, P6 48 |
| M8 | prefix: the last window left out | P1 64, P2 29, P3 48, P4 32, P5 49, P6 68 |
| M9 | prefix: the fewest started at 0 | P1 185, P2 221, P6 221 |
| M11 | prefix: the prefix never carried | P1 214, P2 243, P3 99, P4 31, P5 10, P6 266 |
| M13 | each: the windows from the second start | P1 71, P2 34, P3 48, P4 37, P5 45, P6 78 |
| M14 | each: the comparison reversed | P1 246, P2 139, P6 297 |
| M16 | each: the fewest started at k - 1 | P1 59, P2 23, P6 63 |
| M18 | queue: a popped black never subtracted | P1 135, P2 155, P6 179 |
| M19 | queue: whites counted, not blacks | P1 274, P2 242, P3 133, P6 329 |
| M20 | queue: the answer the most blacks | P1 277, P2 202, P4 109, P6 332 |
| M23 | iter: each window one block short | P1 139, P2 50, P3 49, P6 155 |
| M24 | iter: blacks summed | P1 249, P2 189, P6 300 |
| M26 | iter: the first block counted twice | P1 88, P2 63, P3 49, P4 38, P5 19, P6 93 |
| M27 | solution: the first window one block short | P1 155, P2 72, P3 106, P5 34, P6 174 |
| M30 | solution: the filter counting blacks | P1 270, P2 217, P3 133, P5 62, P6 323 |

P1, P2 and P6 kill all seventeen, P3 ten, P5 six and P4 five. P4, a
black block appended, fails the edits that miss or misread a window at
one end: the last window left out (M8), the windows from the second
start (M13), the prefix never carried (M11) and the first block counted
twice (M26), and with them the most blacks returned for the answer
(M20). P5, `k` one more, fails the same four but M20, and the
template's first window one block short and filter counting blacks
(M27, M30), whose first window is not the one it should be. P3, the
blocks reversed, passes the edits that treat both ends alike, as the
fewest started at 0 or `k - 1` (M9, M16) or taken by max (M3).

Of the thirty-one, fourteen were not kept. A leaving block never
dropped in the template (M29), the whites never reset in the each arm
(M15), and the queue arm's window allowed `k + 1` blocks and newest
popped (M17, M21) fail as the ★ arm's leaving block never dropped (M2);
the fewest taken by max in the iter arm and the template (M22, M28) as
in the ★ arm (M3); the ★ arm's first window one block short and first
window counting blacks (M1, M5) as the template's (M27, M30); the
prefix arm's each window one block short (M7) as the iter arm's (M23),
and its prefix sums counting blacks (M10) as the iter arm's blacks
summed (M24). The slide starting one block late in the ★ arm and the
template (M6, M31) fail alike, as do each window one block longer in
the each and iter arms (M12, M25); both pairs fail apart from every
kept one and were left out to keep three to an arm and two to the
template.

## Verification

Every arm prints the same output as `recolor.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 to 2.2 s, and the differential
1.1 s there and 0.75 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 1000 strings of 100 blocks once from the harness's
generator, string `s` white with a chance of `s % 10` in 10, then makes
500 passes, pass `p` asking string `s` for `k = 1 + (7 p + s) % 100` and
folding each answer plus `p` into the checksum, with the ★ arm in all
five languages. Every implementation prints `500 passes over 1000
strings of 100 blocks: checksum 836111614`.

BENCHTAB
