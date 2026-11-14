# 2161. Partition Array According to Given Pivot

You are given a **0-indexed** integer array `nums` and an integer
`pivot`. Rearrange `nums` such that the following conditions are
satisfied:

- Every element less than `pivot` appears **before** every element
  greater than `pivot`.
- Every element equal to `pivot` appears **in between** the elements
  less than and greater than `pivot`.
- The **relative order** of the elements less than `pivot` and the
  elements greater than `pivot` is maintained.
  - More formally, consider every `p_i`, `p_j` where `p_i` is the new
    position of the `i`-th element and `p_j` is the new position of the
    `j`-th element. If `i < j` and both elements are smaller (or larger)
    than `pivot`, then `p_i < p_j`.

Return `nums` *after the rearrangement.*

```
nums = [9,12,5,10,14,3,10], pivot = 10  ->  [9,5,3,10,10,12,14]
nums = [-3,4,3,2], pivot = 2            ->  [-3,2,4,3]
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^6 <= nums[i] <= 10^6`;
`pivot` equals an element of `nums`.

The answer is the numbers below the pivot in the order they came, then
the pivots, then the numbers above it in the order they came. O(n).

## Approaches

| file | mechanism |
|---|---|
| `pivot.kara` ★ | three passes in order, each keeping its own numbers by `filter`, below, equal and above, `extend`ed one after another |
| `pivot_buckets.kara` | one pass dropping each number into one of three lists by a `match` on `x.cmp(pivot)`, the lists joined by `extend(mem.take(mut ..))` |
| `pivot_ends.kara` | one list made at its full length: the numbers below written from the front as they come, those above from the back as the list is walked backwards, the gap filled with the pivot |
| `pivot_sort.kara` | a stable `sort_by_key` with the sign of `x - pivot` as the key, which keeps numbers of one key in the order they came; O(n log n) |
| `pivot_struct.kara` | a `struct Partition` that `place`s each number (`mut ref self`), keeping the numbers below and above in lists and only counting the pivots, turned `into_vec` (`own self`) with the pivots written out between |
| `pivot_solution.kara` | LeetCode's Rust template: `for &x in &nums`, the pivots counted and put back by `std::iter::repeat(pivot).take(eq)`, `vec![]`; carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one number, every number the pivot, every number but one below it, and
the pivot first and last), each with its answer; then a checksum over
2000 random lists of 1 to 12 numbers within 5, 50 or 10^6 of 0 in turn;
then the constraints' largest, 100000 numbers at random and 100000 of
one number. `pivot.py` mirrors the ★ arm and its output is
byte-identical.

No compiler gap was met. The buckets arm was written with Rust's
`less.append(mut eq)`, and `karac fix` made it
`less.extend(mem.take(mut eq))`. `karac fix` carries the template in
three rounds of 16, 2 and 1 edits: Rust's spellings (`<..>` to `[..]`,
`for &x in &nums` to `for x in ref nums`, `std::iter::repeat` to
`repeat`, `struct Solution;` to `struct Solution {}`, the adapter's
`&Vec` to `ref Vec` and `|&x|` to `|x|`, `Solution::` to `.`); then the
two `vec![]` to `Vec.new()`; then the `ref` dropped from the adapter's
parameter, which borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each number put straight into its place, which is the count
of numbers that must come before it, every number of a lower group and
every number of its own group that came before it; no filtering,
sorting or joining. It checks 300 random lists of 1 to 10 numbers within
3, 20 or 10^6 of 0 in turn, the pivot one of them; then 30 with the
pivot first; then 30 with the pivot last. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every number and the pivot 1000 more: every number of the answer 1000 more |
| P3 | every number and the pivot negated: the groups negated, those above and below swapped, each in its order |
| P4 | the answer partitioned again: the same answer |
| P5 | the list written twice: each of the answer's groups twice |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 914484506, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lists by the same placing. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Twenty-four edits to the differential, three to five to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pivots never kept | P1 360, P6 360 |
| M3 | ★: the pivots kept with the numbers below | P1 360, P3 166, P4 360, P5 243, P6 360 |
| M4 | ★: the numbers above put first | P1 316, P3 316, P5 316, P6 316 |
| M6 | buckets: those above joined before the pivots | P1 238, P3 243, P5 238, P6 238 |
| M7 | buckets: each number below put in front of its list | P1 163, P3 266, P4 163, P6 163 |
| M22 | buckets: the first number skipped | P1 360, P4 318, P5 360, P6 360 |
| M8 | ends: the numbers above written from the back as they come | P1 171, P3 266, P4 171, P6 171 |
| M10 | ends: the gap filled with the first number | P1 226, P3 188, P4 63, P5 188, P6 226 |
| M11 | ends: a number below written without the front moving on | P1 177, P3 276, P5 243, P6 177 |
| M12 | sort: the key `x - pivot` itself | P1 235, P3 270, P5 270, P6 235 |
| M14 | sort: the key only below or not | P1 175, P3 177, P5 238, P6 175 |
| M23 | sort: the key only whether a number is the pivot | P1 243, P3 238, P5 243, P6 243 |
| M15 | struct: the pivots counted once | P1 62, P5 360, P6 62 |
| M18 | struct: those above never written | P1 238, P3 316, P6 238 |
| M24 | struct: each pivot written as one more | P1 360, P3 360, P5 218, P6 360 |
| M20 | solution: one pivot fewer put back | P1 360, P4 62, P5 360, P6 360 |
| M21 | solution: the adapter's pivot one more | P1 179, P3 189, P5 256, P6 179 |

P1 and P6 kill all seventeen, P3 and P5 thirteen each, P4 six, and P2
none. P3 negates every number, which swaps the groups above and below,
so an edit that treats the two sides apart shows there, and P5 writes
the list twice, which doubles every group, so an edit that miscounts
the pivots or drops a number shows there (M15 only there and against
the literal reading, since every list with one pivot is right under
it). P4 partitions the answer again, which a right answer survives
unchanged; it sees an edit that leaves numbers out of place in a way
the second pass moves (M3, M7, M8, M10, M22, M20). P2 adds 1000 to every
number and the pivot, which sees an edit that depends on the numbers'
size rather than their side of the pivot. None of the twenty-four did:
the sort arm's wrong keys (M12, M14, M23) all compare against the
pivot, so they move with it. P2 is kept as the guard on that kind of
edit.

Of the twenty-four, seven were not kept, each failing as a kept one
does: the ★ arm's numbers above taken in reverse, as M8; the buckets
arm's pivots put among the numbers above and the struct arm's pivots
kept above, as M14; the ends arm's back starting one short, the struct
arm's pivots written after the numbers above, and the template's
numbers above taken as below, as M6; and the sort arm's key turned
around, as M4.

## Verification

Every arm prints the same output as `pivot.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.5 s to 1.0 s and the
differential 0.5 s.

## Benchmarks

The bench builds 4 lists of 100000 numbers within 10^6 of 0 once; then
solves every list 25 times, one number replaced and a pivot drawn from
the list before each solve so that no solve repeats one before, with
the ★ arm in all five languages. Every implementation prints `100
solves: checksum 186363039`.

BENCHTAB
