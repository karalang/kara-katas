# 2407. Longest Increasing Subsequence II

You are given an integer array `nums` and an integer `k`.

Find the longest subsequence of `nums` that meets the following
requirements:

- The subsequence is **strictly increasing** and
- The difference between adjacent elements in the subsequence is **at
  most** `k`.

Return *the length of the **longest subsequence** that meets the
requirements.*

A **subsequence** is an array that can be derived from another array by
deleting some or no elements without changing the order of the remaining
elements.

```
nums = [4,2,1,4,3,4,5,8,15], k = 3   ->  5      ([1,3,4,5,8])
nums = [7,4,5,1,8,12,4,7], k = 5     ->  4      ([4,5,8,12])
nums = [1,5], k = 1                  ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i], k <= 10^5`.

The longest subsequence ending at a value `x` is one more than the
longest ending at any value from `x - k` to `x - 1` seen before it, so
every arm keeps the longest ending at each value and asks a range
maximum over the values, a segment tree's or a block structure's.

## Approaches

| file | mechanism |
|---|---|
| `lis.kara` ★ | a bottom-up segment tree over the values, a power of two of leaves at `size + v`; each value's range read upward from both edges, its leaf raised, then its ancestors recomputed. O(n log m), m the largest value |
| `lis_recursive.kara` | a recursive segment tree of `4 m` nodes: `query` descends only into halves that meet the range, `update` walks to the leaf and recomputes on the way back. O(n log m) |
| `lis_blocks.kara` | square-root blocks over the values: each block keeps its values' maximum, a range read as stray values at the ends and whole blocks between. O(n sqrt m) |
| `lis_tree.kara` | the ★ tree as a `MaxTree` struct, `most(self, from, to)` over an inclusive range and `raise(mut ref self, at, value)` up the leaf's path. O(n log m) |
| `lis_iter.kara` | the blocks by iterators: the block width by `find`, each range's stray ends and whole blocks by `iter().max()` over slices, the answer by `fold` over `nums`. O(n sqrt m) |
| `lis_solution.kara` | LeetCode's Rust template: a bottom-up tree of `m + 1` leaves, not a power of two, over `usize` indexes, the left edge by `saturating_sub`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; one value
of `10^5`; the odd numbers to 99 with `k` 1 and 2; 20000 values up to
`10^5` with `k` 1, 100 and `10^5`, and 20000 rising by about 4 with `k`
3 and 8; then 2000 random cases of up to 30 values from 1 to up to 50,
`k` from 1 to 10, with a checksum and the total of the answers.
`lis.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked on 20000 random cases of up to 10 values against
trying every subsequence.

`check` first reports 6 errors on the template, and `karac fix` carries
it in one call, reporting 17 edits: `Vec<i32>` given its brackets; the
`&` of `for &x in &nums` dropped and the `&nums` written `ref nums`; the
`mut` of `(mut l, mut r)` moved before the whole pattern; `struct
Solution;` given its braces; `vec![0; 2 * m]` written `Vec.filled(2 *
m, 0i32)`; every `usize` written `i64`, and `saturating_sub`, which on
an `i64` no longer stops at 0, given a `.max(0)`; `ans` and `best` given
an `i32` type; and the wrapper's widening `as i64` removed.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subsequence, each checked to rise strictly by at most
`k` at every step, and the longest that does. No tree and no blocks. It
checks 300 random cases of 1 to 10 values from 1 to up to 30, `k` from 1
to 8, which the literal reading answers; then 30 of up to 3000 values up
to `10^4`, `k` up to `10^4`; then 30 of up to 3000 values up to 500, `k`
up to 20. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 10 values, the answer is the literal reading's |
| P2 | with `k` at least the largest value less the smallest, the answer is the plain longest strictly increasing subsequence, by patience sorting; otherwise it is between 1 and the number of distinct values |
| P3 | every value raised by 7: the same answer |
| P4 | `k` one larger: an answer at least as long |
| P5 | the values reversed, each `v` written `m + 1 - v` for `m` the largest: the same answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because no step can exceed the spread of the values, so the
bound on a step binds nothing, and a strictly increasing subsequence
holds each value once. P3 holds because only differences count, P4
because a larger `k` refuses nothing a smaller one allowed, and P5
because a subsequence read backwards and mirrored rises by the same
steps.

The differential prints `360 cases: checksum 914170341, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every subsequence. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: each parent only its left child | P1 124, P2 50, P3 147, P4 40, P5 96, P6 183 |
| M4 | ★: the right edge read on even nodes | P1 120, P2 35, P3 171, P4 7, P5 140, P6 179 |
| M6 | ★: the first value skipped | P1 98, P2 59, P5 90, P6 105 |
| M8 | recursive: x itself in its own range | P1 104, P2 53, P6 140 |
| M9 | recursive: the right half's updates sent left | P1 177, P2 68, P3 228, P5 224, P6 236 |
| M11 | recursive: the last value's longest returned | P1 86, P2 27, P5 164, P6 144 |
| M13 | blocks: a step of exactly k refused | P1 44, P2 4, P6 65 |
| M14 | blocks: the blocks never raised | P1 92, P2 45, P3 85, P4 11, P5 64, P6 122 |
| M15 | blocks: a value after each block skipped | P1 27, P2 16, P3 41, P4 6, P5 31, P6 31 |
| M18 | tree: a range of one node unread | P1 150, P2 49, P3 137, P4 18, P5 123, P6 210 |
| M19 | tree: each node set, not raised | P1 4, P2 4, P3 43, P4 1, P5 45, P6 44 |
| M21 | tree: each value raised one leaf low | P1 119, P2 53, P6 156 |
| M23 | iter: a step of k + 1 allowed | P1 27, P6 47 |
| M24 | iter: the last whole block unread | P1 91, P2 44, P3 87, P4 9, P5 68, P6 120 |
| M26 | iter: the least in a short range taken | P1 94, P2 14, P3 69, P4 25, P5 61, P6 128 |
| M28 | solution: each parent only its right child | P1 66, P2 13, P3 70, P4 22, P5 98, P6 124 |
| M29 | solution: the left edge read on even nodes | P1 104, P2 18, P3 168, P4 5, P5 173, P6 163 |

P1 and P6 kill all seventeen, P2 sixteen, P5 thirteen, P3 eleven, and
P4 ten. The one P2 misses is the iter arm's step of `k + 1` allowed
(M23), which P2's cases cannot see: there `k` is at least the whole
spread of the values, so a step one longer than `k` never occurs. P4 asks
only that a `k` one larger give an answer at least as long, which
allowing longer steps keeps.

Of the thirty-one, fourteen were not kept, each failing the same checks
as a kept one or, for five, left over: `x` itself in its own range in
the ★ and tree arms and the template (M1, M20, M27) as the recursive
arm's (M8); the ★ arm's step of `k + 1` allowed (M2) as the iter arm's
(M23); the last value's longest returned in the ★, blocks, iter and
template arms (M5, M16, M25, M30) as the recursive arm's (M11); and the
template's step of exactly `k` refused (M31) as the blocks arm's (M13).
The recursive arm's node ending at the range's start skipped and node
half inside taken whole (M7, M10), the blocks arm's block holding `x`
taken whole (M12), the tree arm's right edge read on odd nodes (M17)
and the iter arm's `x` itself in its own range (M22) fail apart from
every kept one, and were left out because those arms keep three
already.

## Verification

Every arm prints the same output as `lis.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.2 to 5.4 s, except the iter
arm at 9.3 s. The differential takes 78 s there, 11.6 s under `karac
__mir-llvm-asan` and 1.1 s under `karac run`.

## Benchmarks

The bench builds 5 arrays of `10^5` values from 1 to `10^5` once from
the harness's generator, then makes 4 passes, answering array `i` with
`k = 10^i` and folding each answer plus the pass into the checksum, with
the ★ arm in all five languages. Every implementation prints `4 passes
over 5 arrays of 10^5 values: checksum 76456129`. Each allocates the
tree of `2 * 131072` zeroed cells in every call and walks it with the
same index arithmetic; Kāra, Rust and Go check every index, and C does
not.

BENCHTAB
