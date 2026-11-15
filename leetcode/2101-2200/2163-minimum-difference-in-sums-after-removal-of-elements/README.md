# 2163. Minimum Difference in Sums After Removal of Elements

You are given a **0-indexed** integer array `nums` consisting of `3 * n`
elements.

You are allowed to remove any **subsequence** of elements of size
**exactly** `n` from `nums`. The remaining `2 * n` elements will be
divided into two **equal** parts:

- The first `n` elements belonging to the first part and their sum is
  `sum_first`.
- The next `n` elements belonging to the second part and their sum is
  `sum_second`.

The **difference in sums** of the two parts is denoted as `sum_first -
sum_second`.

- For example, if `sum_first = 3` and `sum_second = 2`, their difference
  is `1`.
- Similarly, if `sum_first = 2` and `sum_second = 3`, their difference
  is `-1`.

Return *the **minimum difference** possible between the sums of the two
parts after the removal of* `n` *elements*.

```
nums = [3,1,2]        ->  -1
nums = [7,9,5,8,1,3]  ->  1
```

**Constraints:** `nums.length == 3 * n`; `1 <= n <= 10^5`; `1 <= nums[i]
<= 10^5`.

The first part comes from before some cut between `n` and `2n`, the
second from after it. For a cut, the first part is best as the `n`
smallest before it and the second as the `n` largest after it. A heap
keeps each as the cut moves, one from the front and one from the back.
O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `difference.kara` ★ | a largest-first `PriorityQueue` keeping the n smallest of a growing prefix, its top dropped whenever it holds n + 1, and a smallest-first one keeping the n largest of a growing suffix |
| `difference_multiset.kara` | the kept numbers as a multiset, a `SortedMap` from each number to its count; the prefix drops one of its largest by `last`, the suffix one of its smallest by `first`, a count of 0 `remove`d |
| `difference_struct.kara` | a `struct Keeper` that keeps the n best numbers it is `offer`ed and their sum (`mut ref self`), made by `smallest` or `largest`; `sums` offers a list and gives the sum after each offer from the n-th on, the suffix's from the reversed list |
| `difference_heap.kara` | the heaps by hand, a `Vec` kept by `sift_up` and `sift_down` (`mut ref Vec`) under a `sign`; a number better than the top replaces it and sinks |
| `difference_fenwick.kara` | two Fenwick trees over the numbers' ranks, of counts and of sums, for the prefix and again for the suffix; the k smallest by descending the trees by powers of two, the n largest of a suffix its sum less its smallest len - n |
| `difference_solution.kara` | LeetCode's Rust template: `BinaryHeap` for the prefix and `BinaryHeap` of `Reverse` for the suffix, both named `heap`, `vec![0i64; n + 1]`, `nums[i] as i64`, `heap.pop().unwrap().0`; carried by `karac fix` in five rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one number a part, all the same, rising, and falling), each with its
answer; then the total and a checksum over 2000 random lists of 3 to 15
numbers from 1 to 10, 100 or 10^5 in turn; then the constraints'
largest, 300000 numbers at random and 300000 of one number.
`difference.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in five rounds of 9, 1, 3, 5 and 2
edits: Rust's spellings (`use std::cmp::Reverse` dropped, `<..>` to
`[..]`, `BinaryHeap::new` to `BinaryHeap.new`, `i64::MAX` to `i64.MAX`,
`struct Solution;` to `struct Solution {}`, `Solution::` to `.`, `|&x|`
to `|x|`); then `use std::collections::BinaryHeap` dropped; then the
first heap to `PriorityQueue.max_first()` and the second to
`PriorityQueue.new()`, with `Reverse` dropped from its pushes, since a
`PriorityQueue` pops the smallest first; then the `.0` of
`heap.pop().unwrap().0` dropped with the `as i64`s that widen an `i32`,
and `vec![0i64; ..]` to `vec![0; ..]`; then `vec![0; n + 1]` to
`Vec.filled(n + 1, 0)` and the last `as i64`.

Two compiler gaps were met and fixed (kara 761ab5b3e0). Which way a Rust heap
pops was told from every push of its name in the program, so the
template's `heap`, shadowed by a second `let mut heap`, read as both
kinds, and neither heap nor any `Reverse` got a fix. Each push now
speaks for the latest constructor of its name before it. And once
`Reverse` is gone from the pushes, Rust's `.0` on the popped item was a
bare "tuple index on non-tuple type 'i32'"; on what a `PriorityQueue`'s
`pop` or `peek` gives, it is now refused with the fix that deletes it.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every choice of n numbers removed, what is left cut in half,
and the least difference of the halves' sums taken; no heaps, prefixes
or suffixes. It checks 300 random lists of 3 to 12 numbers from 1 to 5,
50 or 10^5 in turn; then 30 of one number; then 30 falling. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the difference is the statement read literally |
| P2 | every number 7 more: the same difference |
| P3 | every number doubled: the difference doubled |
| P4 | the list reversed and every number negated: the same difference |
| P5 | the list sorted: its n smallest less its n largest |
| P6 | each arm agrees with at least three of the other five |

P4 holds since reversing swaps the two parts and negating turns each
part's sum into the other's less, so the first part's sum less the
second's is unchanged.

The differential prints `360 lists: checksum 737288984, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists by `itertools.combinations`. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty edits to the differential, four to seven to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the prefix keeping n + 1 | P1 210, P2 68, P4 360, P6 210 |
| M3 | ★: the cut at 2n never tried | P1 91, P4 182, P6 91 |
| M30 | ★: the suffix's dropped number added | P1 331, P2 344, P4 360, P5 360, P6 331 |
| M5 | multiset: a count of 0 left in the map | P1 216, P6 216 |
| M6 | multiset: a repeated number counted once | P1 49, P6 49 |
| M7 | multiset: the prefix dropping its smallest | P1 210, P4 306, P6 210 |
| M10 | struct: the largest kept as the smallest | P1 204, P4 306, P6 204 |
| M11 | struct: the suffix read forwards | P1 221, P4 257, P6 221 |
| M12 | struct: the suffix's sums read the wrong way | P1 175, P6 175 |
| M14 | heap: only the left child sifted to | P1 85, P6 85 |
| M15 | heap: the replaced top never taken off the sum | P1 304, P2 264, P6 304 |
| M16 | heap: a new number never sifted up | P1 124, P6 124 |
| M17 | fenwick: each add walking every later node | P1 66, P4 104, P5 70, P6 66 |
| M18 | fenwick: the copies of the next value never added | P1 116, P2 124, P4 116, P5 125, P6 116 |
| M20 | fenwick: one more removed from the suffix | P1 360, P2 360, P4 360, P5 360, P6 360 |
| M22 | solution: the first prefix never stored | P1 327, P2 340, P4 326, P5 360, P6 327 |
| M24 | solution: the adapter's numbers reversed | P1 311, P5 329, P6 311 |

P1 and P6 kill all seventeen, P4 ten, P2 and P5 six each, and P3 none.
P4 reverses and negates, which swaps the prefix's work with the
suffix's; it sees an edit that treats the two sides differently, a heap
facing the wrong way on one side (M7, M10) or one cut left out (M3).
P2 adds 7 to every number, which a right difference ignores, since both
parts gain 7n; it sees an edit whose parts do not hold n numbers each
(M1, M18, M20, M22) or that adds a number it should take away (M15,
M30).
P5 sorts the list, where the answer is the n smallest less the n
largest; it sees the Fenwick edits and the two other edits wrong on any
list (M22, M30), and the reversed adapter (M24), which on a sorted list
puts the largest first. P3
doubles every number, and every edit here is linear in the numbers, so
none changes how its wrong answer scales.

Of the thirty, thirteen were not kept. Two are equivalent, both in the
Fenwick arm: the values not deduplicated, since a repeated value's
copies then take the rank `binary_search` finds for them, every time
the same one, and a node taken only when it leaves some need, since what
the descent then leaves is copies of the one value next up. One
crashes: the struct arm keeping one too many, whose list of sums is then
one short. Ten fail as a kept one does: every other heap made to face
the wrong way (the ★ arm's suffix, the multiset's suffix dropping its
largest, the hand-written heap's sign ignored, and the template's
second heap) as M10; the ★ arm's last cut's difference kept and the
struct arm's smallest kept as the largest, as M7; the ★ arm's cut at n
never tried and the struct arm's cut at 2n, as M3, its mirror under P4; the ★ arm's prefix sum
stored before its largest is dropped, as M1; and the ★ arm's prefixes
read from the wrong end, as M12.

## Verification

Every arm prints the same output as `difference.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 6.2 s to 12.2 s, but for the
multiset arm, 23.1 s, since the interpreter keeps a `SortedMap` as one
sorted array; the hand-written heap is the fastest. The differential
takes 1.3 s.

## Benchmarks

The bench builds 4 lists of 300000 numbers from 1 to 10^5 once; then
solves each list 5 times, one number replaced before each solve so that
no solve repeats one before, with the ★ arm in all five languages: C
with a heap by hand, Go with `container/heap`. Every implementation
prints `20 solves: checksum 547134288`.

BENCHTAB
