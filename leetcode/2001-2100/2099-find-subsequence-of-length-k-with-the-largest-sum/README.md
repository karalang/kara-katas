# 2099. Find Subsequence of Length K With the Largest Sum

You are given an integer array `nums` and an integer `k`. You want to
find a subsequence of `nums` of length `k` that has the largest sum.

Return any such subsequence as an integer array of length `k`.

A subsequence is an array that can be derived from another array by
deleting some or no elements without changing the order of the remaining
elements.

```
nums = [2,1,3,3], k = 2      ->  [3,3]
nums = [-1,-2,3,4], k = 3    ->  [-1,3,4]
nums = [3,4,3,3], k = 2      ->  [3,4]    ([4,3] is also accepted)
```

**Constraints:** `1 <= nums.length <= 1000`; `-10^5 <= nums[i] <=
10^5`; `1 <= k <= nums.length`.

The `k` largest numbers make the largest sum, and kept in the list's
order they are a subsequence. Which of several equal numbers to take is
free, so every arm here takes the earliest ones, and all six give the
same answer: for LeetCode's third example, `[3,4]`. The arms differ in
how they find the `k` and put them back in order.

## Approaches

| file | mechanism |
|---|---|
| `largest_sum.kara` ★ | the positions sorted with `sort_by` on the value, larger first, `.then` the position; the first `k` sliced off, sorted back into order, and mapped to their values. O(n log n) |
| `largest_sum_threshold.kara` | the `k`-th largest value as a threshold from a sorted copy: every number above it taken, and of those equal to it only as many as are still needed, in one walk in order |
| `largest_sum_heap.kara` | one pass with a smallest-first `PriorityQueue[(i64, i64)]` of value and negated position, popped whenever it holds more than `k`, so of equal values the later goes first; the positions left drained, sorted and mapped. O(n log k) |
| `largest_sum_pick.kara` | `k` picks, each a scan for the largest number not yet taken, the earliest of equals, marked in a `Vec[bool]`; the marked read back with `filter` and `map` over the range. O(n k) |
| `largest_sum_ranked.kara` | a `struct Ranked` of a value and its position with hand-written `PartialEq`, `Eq`, `PartialOrd` and `Ord` (the larger value first, then the earlier position); a plain `sort`, `truncate(k)`, `sort_by_key` on the position |
| `largest_sum_solution.kara` | LeetCode's Rust template (`nums: Vec<i32>`, positions as `Vec<usize>` sorted by `sort_by_key(\|&i\| std::cmp::Reverse(nums[i]))`, which is stable and keeps the earlier of equals first, then `truncate`, `sort` and a `map`), carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and four
more, each list with its answer; then how many of 3000 random lists of 1
to 30 numbers (from -10^5 to 10^5, or from -3 to 3 so that equal numbers
are common), each asked for a random `k`, come back as a subsequence of
`k` numbers, and a checksum of their sums; then the constraints'
largest, 1000 numbers in random order, all equal, and falling, each
asked for 1, 500 and 1000. `largest_sum.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every choice of `k` positions by bit mask, the largest sum
kept, and of the choices with that sum the one whose positions come
first, the rule every arm follows. It checks 300 random lists of 1 to 10
numbers from -3 to 3; then 20 lists of 1 to 10 copies of one number;
then 20 lists of 1 to 12 numbers from -49000 to 49000 (so that raised
and doubled they stay within the constraints); each with a random `k`.
All 340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is `k` numbers of the list in its order, summing to the `k` largest |
| P3 | the list reversed: an answer with the same sum |
| P4 | every number 1000 more: the answer with every number 1000 more |
| P5 | every number doubled: the answer doubled |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 lists: checksum 199518684, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists with `itertools.combinations`. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-five edits to the differential, five to each arm and then five
more aimed at the ★ and ranked arms, whose first five crowded other
arms' failures, each run under `karac __mir-llvm-run` and `karac
__mir-run`. Seventeen are kept, three to each Kāra arm and two to the
Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the numbers ranked by their size without sign | P1 161, P2 161, P3 159, P4 153, P6 161 |
| M2 | ★: the numbers ranked by their last three digits | P1 12, P2 12, P3 12, P4 184, P5 7, P6 12 |
| M3 | ★: each number written one more | P1 340, P2 340, P3 340, P5 340, P6 340 |
| M4 | threshold: the `k`-th smallest as the threshold | P1 216, P2 216, P3 181, P6 216 |
| M5 | threshold: a number just above the threshold left out | P1 126, P2 126, P3 104, P5 126, P6 126 |
| M6 | threshold: every number equal to the threshold taken | P1 85, P2 85, P3 70, P6 85 |
| M7 | heap: the positions never put back in order | P1 161, P2 161, P6 161 |
| M8 | heap: the first number never offered | P1 221, P2 211, P3 202, P6 221 |
| M9 | heap: one fewer kept | P1 340, P2 340, P3 290, P6 340 |
| M10 | pick: a taken number picked again | P1 231, P2 231, P3 197, P6 231 |
| M11 | pick: the numbers not picked read back | P1 336, P2 336, P3 319, P6 336 |
| M12 | pick: the later of equal numbers picked | P1 31, P6 31 |
| M13 | ranked: values ranked by their halves | P1 66, P2 66, P3 67, P4 49, P5 66, P6 66 |
| M14 | ranked: positions counted from the end | P1 189, P2 189, P6 189 |
| M15 | ranked: one more kept | P1 230, P2 230, P3 193, P6 230 |
| M16 | solution: the adapter's numbers negated | P1 311, P2 311, P3 296, P4 340, P6 311 |
| M17 | solution: the positions never put back in order | P1 179, P2 173, P6 179 |

P1 and P6 kill all seventeen, P2 sixteen, P3 thirteen, and P4 and P5
four each. P2 misses only M12: taking the later of equal numbers still
gives `k` numbers in order with the largest sum, an answer the
statement accepts and only the arms' shared rule, P1, refuses. P3
misses the edits that only put the right numbers in the wrong order
(M7, M14, M17) or pick the wrong one of equals (M12), whose sums are
right. P4 and P5 move every value, so they see only the edits that look
at a value's size rather than its rank. P4, every number 1000 more,
sees the sign dropped (M1), the last three digits (M2), the halves
(M13) and the negation (M16). P5, every number doubled, sees the last
three digits and the halves too, and the two edits whose error does not
double with the numbers: the number written one more (M3) and the
threshold's neighbour left out (M5). The first thirty edits were all
blind to the values, so the first three of these were added for them.

Of the thirty-five, eighteen were not kept, and none survives. Eleven
fail as a kept one: one fewer taken (★, threshold's equals counted as
above, pick, and the Rust adapter) as M9; the later of equals first (★
and ranked) as M12; the positions never put back in order (★ and
ranked) as M17; the Rust arm's one more kept as M15; the threshold arm's
one more of the equals wanted as M6; the ranked arm's kept put in order
of value as M7. Five fail the same way as each other and were left out
together: the smallest ranked first, in the ★, heap (a largest-first
queue), pick, ranked and Rust arms (P1 215, P2 215, P3 215, P6 215).
One is killed with checks of its own but was left out because its arm
keeps its share: the ★ arm's answer read backwards (P1 194, P2 189, P6
194). One crashes and is not kept: the heap arm keeping the later of
equals by pushing the position itself, whose negation is then read back
as an index.

## Verification

Every arm prints the same output as `largest_sum.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.5 s to 1.5 s, and the
differential 2.0 s (timed while other work shared the machine).

The harness met a gap. It lists its largest inputs as one array
literal, `[(0..1000).map(..).collect(), Vec.filled(1000, -7), ..]`. A
bare `collect()` names no type of its own and takes it from its context;
a branch of an `if` already took it from the other branch, but an
element of an array literal did not take it from its siblings, and
`karac check` refused the literal with "an expression whose type does
not lower (UnsolvedParam("C"))", which names nothing the program wrote.
It now does, as Rust's does. Fixed in kara 81aca4606b, test
`tests/kata_2099_array_literal_collect.rs`.

`karac fix` carries the template in four rounds of 20, 1, 2 and 1 edits:
Rust's spellings (`Vec<i32>` and `Vec<usize>` to brackets, the closures'
`&i` patterns dropped, `std::cmp::Reverse` to `Reverse`, `Solution::` to
`.`, `struct Solution;` to `struct Solution {}`); then
`sort_by_key(|i| Reverse(nums[i]))` to `sort_by(|a, b|
(nums[b]).cmp(nums[a]))`, which keeps the stable sort's order of
equals; then `usize` to `i64` in the positions' type and the cast; then
the adapter's `ref` parameter to a bare one, which borrows already.

## Benchmarks

The bench asks 20000 lists of 1000 numbers from -10^5 to 10^5, the
constraints' largest, each for a random `k`, with the ★ arm in all five
languages: the positions sorted by value with the position breaking
ties (`sort_by` with `then`, `sort_by` with `then`, `qsort`,
`sort.Slice`, `sorted` with a key), then the first `k` sorted back into
order. Every implementation prints `20000 answers: 10026650 numbers,
checksum 332166571`.

BENCHTAB
