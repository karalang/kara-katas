# 2449. Minimum Number of Operations to Make Arrays Similar

You are given two positive integer arrays `nums` and `target`, of the
same length.

In one operation, you can choose any two **distinct** indices `i` and
`j` where `0 <= i, j < nums.length` and:

- set `nums[i] = nums[i] + 2` and
- set `nums[j] = nums[j] - 2`.

Two arrays are considered to be **similar** if the frequency of each
element is the same.

Return *the minimum number of operations required to make* `nums`
*similar to* `target`. The test cases are generated such that `nums`
can always be similar to `target`.

```
nums = [8,12,6], target = [2,14,10]   ->  2
nums = [1,2,5], target = [4,1,3]      ->  1
nums = [1,1,1,1,1], target = [1,1,1,1,1]  ->  0
```

**Constraints:** `n == nums.length == target.length`;
`1 <= n <= 10^5`; `1 <= nums[i], target[i] <= 10^6`; it is possible to
make `nums` similar to `target`.

An operation never changes a value's parity, so the odd values of
`nums` must become the odd values of `target` and the even the even.
Within each parity, matching the least to the least is never worse than
crossing two pairs over, so both sides are sorted and matched in order.
Each operation closes 4 of the total distance, 2 on the value it raises
and 2 on the one it lowers, and the distance can always be closed that
way, so the answer is the total distance over 4.

## Approaches

| file | mechanism |
|---|---|
| `similar.kara` ★ | each array split into its odd and even values, the four lists sorted, matched in order, and the distances added and divided by 4. O(n log n) |
| `similar_key.kara` | one sort of each array by the key `(x % 2, x)`, the evens first in order and then the odds, so the arrays line up pair by pair; the total by which values stand above their partners, over 2. O(n log n) |
| `similar_count.kara` | counting sort: how many of each value each array holds, up to the largest, and for each parity two cursors walked up the values in step, each stretch of values they stand on matched at once. O(n + V) |
| `similar_heap.kara` | four `PriorityQueue`s built by `max_first()`, the odd and the even values of each array, popped in step from the largest down and matched as they come. O(n log n) |
| `similar_iter.kara` | iterators: each array split by `partition`, the parts sorted, paired by `zip` and `chain`, and the distances added by `map` and `sum`. O(n log n) |
| `similar_solution.kara` | LeetCode's Rust template: the arrays taken as `mut` parameters, sorted in place by `sort_unstable_by_key(\|&x\| (x & 1, x))`, and the distances widened and summed by `sum::<i64>()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples; one
value; two values swapped; two of each parity at the far ends of the
range against two near the middle; one operation each way; then `10^5`
values, the constraints' most, from 1 to `10^6` against a target `2 *
10^5` random operations away, and from 1 to 10 against one `10^5` away;
and 3000 random cases of 1 to 10 values from 1 to 20, each against a
target 0 to 9 operations away, as a checksum and the total. Every
target is made from its `nums` by operations that keep the values from
1 to `10^6` and then shuffled, so each case is one LeetCode allows.
`similar.py` mirrors the ★ arm and its output is byte-identical, and
the mirror was checked on 3000 random cases of up to 4 values against
a breadth-first search over the operations.

`check` first reports 10 errors on the template, and `karac fix`
carries it in one call, reporting 15 edits: each `mut` parameter
written as `own` with a `let mut` rebinding at the body's start, three
edits; each of the four angle brackets of the two `Vec<i32>` made
square; the `&` dropped from the four patterns `&x`, `&x`, `&a` and
`&b`, since a Kāra pattern already matches through a reference; the
turbofish `::<i64>` on `sum` dropped; `struct Solution;` given its
braces; and, once the template parses, each `sort_unstable_by_key`
written `sort_by_key`, the library having only the stable sort. The key
`(x & 1, x)`, `abs()` and `as i64` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a breadth-first search from `nums` over single operations,
2 added to one value and 2 taken from another that stays positive,
every value kept to at most 40, until the values match `target`'s once
both are sorted; the depth reached is the answer. No parity is split
and no distance taken. It checks 300 cases of 1 to 4 values from 1 to 9
against a target 0 to 4 operations away; then 30 of 5 or 6 values from
1 to 9, 0 to 2 operations away; then 30 of 2 to 4 values from 1 to 3, 0
to 4 operations away, full of ties. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `nums` and `target` swapped: the same answer |
| P3 | every value of both raised by one even number from 2 to 20: the same answer |
| P4 | `target` reversed: the same answer |
| P5 | one operation done on `nums`: an answer within one of the first |
| P6 | each arm agrees with at least three of the other five |

P2 holds because an operation undone is an operation, with `i` and `j`
exchanged. P3 holds because an even shift keeps every parity and every
distance. P4 holds because similarity looks only at how often each
value appears. P5 holds because an operation and its undoing are each
one step, so the least count moves by at most one.

The differential prints `360 cases: checksum 145709064, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and runs the same search. On a failure it prints the
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
| M1 | ★: the odd targets matched in reverse | P1 136, P6 136 |
| M2 | ★: the targets never sorted | P1 125, P2 99, P4 157, P6 125 |
| M6 | ★: the odd distances not made absolute | P1 65, P2 76, P6 65 |
| M7 | key: nums sorted by the value alone | P1 95, P2 48, P6 95 |
| M9 | key: the first pair skipped | P1 43, P2 82, P6 43 |
| M11 | key: nums's odds put first | P1 152, P2 41, P6 152 |
| M13 | count: each pair's distance counted once | P1 6, P6 6 |
| M14 | count: the target's cursor begun one value up | P1 90, P2 47, P3 90, P6 90 |
| M15 | count: every value counted once | P1 47, P2 41, P5 6, P6 47 |
| M17 | heap: the targets popped smallest first | P1 181, P6 181 |
| M18 | heap: the distance over 2 | P1 120, P5 107, P6 120 |
| M21 | heap: the last pair of each parity left out | P1 99, P6 99 |
| M22 | iter: the parts never sorted | P1 120, P4 144, P6 120 |
| M23 | iter: the parity by the value mod 4 | P1 76, P3 14, P5 23, P6 76 |
| M25 | iter: the odds paired with the even targets | P1 103, P2 16, P6 103 |
| M27 | solution: nums sorted by parity alone | P1 119, P2 99, P6 119 |
| M28 | solution: the targets sorted by the value alone | P1 91, P2 48, P6 91 |


P1 and P6 kill all seventeen, P2 ten, P5 three, and P3 and P4 two
each.

Fourteen are not kept. Four fail exactly as a kept one: the ★ arm's and
the template's distance over 2 (M3, M29) as the heap arm's (M18), each
answering twice the count; and the key arm's targets descending in each
parity (M10) as the heap arm's targets popped smallest first (M17),
both matching each parity's values in opposite orders. Nine fail apart
from every kept one, in two groups that fail alike, and none is kept
because those arms keep their share already: the ★ arm's evens left
out, the count arm's odd walk only, the heap arm's odd values only and
the iter arm's evens left out (M5, M12, M19, M24), each counting the odd
values alone; and the key arm's surplus over 4, the count arm's targets
counted into `nums`'s table, the heap arm's and the template's distance
not made absolute, and the iter arm's each distance less 2 (M8, M16,
M20, M30, M26), each a wrong answer on every case whose answer is above
0 that the transformations keep wrong in the same way, so only P1 and
P6 catch them. The template's first pair dropped (M31) also fails
apart and is left out.

One ends in a panic, not a wrong answer, under both backends: the ★
arm's parity of `nums` by the value mod 4 (M4) splits `nums` into lists
of other lengths than `target`'s, and the match reads past the end of
the shorter one.

## Verification

Every arm prints the same output as `similar.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.1 to 6.5 s, but for the heap
arm, whose `10^5`-value cases push and pop `4 * 10^5` times: it takes
14 s there, 2.5 s under `karac __mir-llvm-asan` and 0.4 s under `karac
run`. The differential takes 1.3 s under `karac __mir-run`, 0.9 s under
`karac __mir-llvm-asan` and 0.9 s under `karac run`.

## Benchmarks

The bench builds `10^5` values from 1 to `10^6`, the constraints'
largest, once from its own generator, and a target that starts as the
same values. It then makes 220 passes; pass `p` does 1000 more random
operations on the target, each moving 2 times 1 to 50 between two
values that stay from 1 to `10^6`, so no answer can be carried from one
pass to the next, then answers and folds the answer plus the pass into
the checksum. The bench uses the ★ arm, the four sorted lists matched
in order, in all five languages. Every implementation prints `220
passes over 10^5 values: checksum 818362087`. Each language builds the
four lists by appending to a growable list (`Vec`, `Vec`, a slice by
`append`, a Python list), and in C four buffers of `n` values each, and
sorts them with its library's sort: `sort` in Kāra and Rust, `qsort` in
C, `sort.Slice` in Go and `list.sort` in Python.

BENCHTAB
