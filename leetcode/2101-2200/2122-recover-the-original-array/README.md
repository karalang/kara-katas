# 2122. Recover the Original Array

Alice had a 0-indexed array `arr` consisting of `n` positive integers.
She chose an arbitrary positive integer `k` and created two new
0-indexed integer arrays `lower` and `higher` in the following manner:

1. `lower[i] = arr[i] - k`, for every index `i` where `0 <= i < n`
2. `higher[i] = arr[i] + k`, for every index `i` where `0 <= i < n`

Unfortunately, Alice lost all three arrays. However, she remembers the
integers that were present in the arrays `lower` and `higher`, but not
the array each integer belonged to. Help Alice and recover the original
array.

Given an array `nums` consisting of `2n` integers, where exactly `n` of
the integers were present in `lower` and the remaining in `higher`,
return the original array `arr`. In case the answer is not unique,
return any valid array.

```
nums = [2, 10, 6, 4, 8, 12]  ->  [3, 7, 11]
nums = [1, 1, 3, 3]          ->  [2, 2]
nums = [5, 435]              ->  [220]
```

**Constraints:** `2 * n == nums.length`; `1 <= n <= 1000`; `1 <= nums[i]
<= 10^9`; the test cases are generated such that there exists at least
one valid array `arr`.

The smallest number is a lower, `x - k`, so `2k` is its distance to one
of the others: at most `2n - 1` candidates. For one `k`, the smallest
number not yet paired must be a lower too, and its higher `x + 2k` must
be there; pairing greedily from the bottom decides each candidate in
O(n) over the sorted numbers, O(n^2) in all. Where several `k` work
(`[1, 1, 3, 3]` is also `[2, 2]` shifted by 1), every arm here answers
the smallest, so the answers compare exactly; they are printed sorted.

## Approaches

| file | mechanism |
|---|---|
| `recover.kara` ★ | the numbers sorted; each distinct positive even distance from the smallest tried, smallest first; a lower pointer and a higher pointer with a `used` flag per number. O(n^2) |
| `recover_counts.kara` | a `SortedMap` of counts; for one `k` every copy of the smallest number left is taken with as many copies `2k` above it at once, one step per distinct number |
| `recover_queue.kara` | over the sorted numbers, each is either the higher the oldest lower waits for, or a new lower whose `x + 2k` joins the back of a `VecDeque`; the distances tried kept in a `Set` |
| `recover_struct.kara` | a `struct Multiset` over a `Map` of counts with `of`, `has` and `take` (`mut ref self`); each sorted number still there is taken with its higher |
| `recover_iter.kara` | the candidates a chain of `map` and `filter`, the first that pairs found with `find_map`; the pairing a `try_fold` carrying a `(VecDeque, Vec)` that gives up with `None` |
| `recover_solution.kara` | LeetCode's Rust template: a `HashMap<i32, i32>` of counts rebuilt per candidate, the lowers taken in sorted order through `get_mut`, carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (one pair, every original value the same, a `k` that is not the
first candidate, the constraints' largest values), each with its sorted
answer; then the values recovered and a checksum of the sorted answers
over 2000 random arrays, an original of 1 to 12 values from 1 to 1, 10
or 1000 in turn and a `k` from 1 to 20, shuffled; then the constraints'
largest, 1000 random values up to 10^6 shifted by 777. `recover.py`
mirrors the ★ arm and its output is byte-identical; its answer to the
last line was also checked against a Python pairing by counts.

The Kāra arms took no edit from `karac fix`, including the iter arm's
`try_fold` over a tuple of a `VecDeque` and a `Vec`, and no compiler
gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every `k` from 1 up tried in turn, and for each the numbers
split by taking the smallest left with its partner `2k` above it until
none is left; the first `k` that empties them gives the answer. It
checks 300 random arrays, an original of 1 to 8 values from 1 to 1, 5
or 50 in turn and a `k` from 1 to 10; then 30 of up to 40 values from 1
to 1000 with a `k` up to 500; then 30 whose original values are all
one. All 360 are drawn before any arm answers, and answers are compared
sorted.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is an original: `k`, its smallest less the smallest number, is positive, and its values less and plus `k` are the numbers |
| P3 | the numbers reflected (`x` to `max + min - x`): the answer reflected |
| P4 | every number times 3: the answer times 3 |
| P5 | the numbers twice over: the answer twice over |
| P6 | each arm agrees with at least three of the other five |

P3 to P5 hold for the smallest `k` as well as for some `k`: a
reflection maps a split by `k` to a split by `k`; tripled numbers are
all multiples of 3, so `2k` must be one too, and the splits by `3k` are
those by `k` tripled; and the greedy split of the numbers twice over
takes each count twice, so it succeeds exactly when the split of the
numbers once does.

The differential prints `360 arrays: checksum 693720892, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
arrays by the same enumeration. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-four edits to the differential, five to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an odd distance tried | P1 3, P2 3, P4 3, P5 53, P6 3 |
| M5 | ★: a higher never marked used | P1 122, P2 114, P3 8, P6 122 |
| M6 | ★: the first candidate skipped | P1 86, P2 79, P3 28, P5 86, P6 86 |
| M8 | counts: one partner taken for every copy | P1 206, P2 206, P3 2, P5 154, P6 206 |
| M9 | counts: one original for every copy | P1 206, P2 206, P5 360, P6 206 |
| M10 | counts: only even `k` tried | P1 179, P2 177, P6 179 |
| M13 | queue: the higher waited for at `k` | P1 360, P2 360, P3 44, P6 360 |
| M14 | queue: the lower taken as the original | P1 360, P2 360, P3 360, P6 360 |
| M16 | queue: an odd distance tried | P1 21, P2 21, P3 21, P4 21, P6 21 |
| M19 | struct: one multiset for every `k` | P1 108, P2 108, P3 35, P6 108 |
| M20 | struct: each original one too large | P1 360, P2 360, P3 360, P4 360, P6 360 |
| M21 | struct: two copies taken at once | P1 229, P2 229, P5 131, P6 229 |
| M23 | iter: a zero distance tried | P1 66, P2 66, P5 294, P6 66 |
| M26 | iter: the distance taken as `k` | P1 352, P2 352, P3 7, P6 352 |
| M33 | iter: a `k` of 1 never tried | P1 36, P2 31, P4 36, P6 36 |
| M31 | solution: an answer short of a pair accepted | P1 3, P2 3, P3 4, P5 3, P6 3 |
| M32 | solution: the numbers made even | P1 340, P2 340, P3 340, P4 340, P6 340 |

P1, P2 and P6 kill all seventeen, P3 eleven, P5 seven and P4 five. P2
sees every wrong answer, since none of them is an original of the
numbers. P3 sees the edits that do not commute with turning the numbers
around: an answer that is the lowers or the highers rather than their
middle (M14, M20, M32), and pairings that lean on the bottom of the
range. P4 sees the edits that depend on the size of the distances
rather than their ratios: an odd distance tried (M1, M16), `k` of 1
skipped (M33), the numbers made even (M32), an original one too large
(M20). P5 sees the edits that count copies wrongly (M8, M9, M21), a
zero distance, which pairs every number with its double (M23), and a
candidate skipped that the numbers twice over bring back (M6).

Of the thirty-four, seventeen were not kept. Four are equivalent: the
★ arm's higher pointer not kept past the lower, which the value test
already keeps there; its unpaired lower skipped rather than given up,
which leaves the answer short and the length test refuses it; and in
the queue and iter arms, a higher passed over not given up at once,
which then waits to the end and is refused there. Three survive, and
are not equivalent: the counts arm taking one partner as enough for
every copy, and the queue and iter arms accepting highers still waiting
at the end. Each needs a smaller `k` to fail only in a particular way
(`[2, 6, 2, 4, 8, 12, 8, 10]` for the first, `[7, 5, 1, 17, 15, 11]`
for the others); a search over random arrays drawn like the
differential's finds such an array about once in a thousand for the
first and four times in a thousand for the others, and none of the 360
is one. The struct arm's missing number taken crashes on a missing key.
Four fail as a kept one does: the
higher taken as the original in the ★, iter and Rust arms as M14, and
the Rust arm's odd distance as M16. Five are killed with checks of
their own but were left out because their arms keep their share: the
counts arm's count read before any was taken (P1 360, P2 360), the
struct arm's lower looked at but not taken and the Rust arm's lower
never taken (P1 31, P2 29, P3 16), the iter arm's distances from the
second number (P1 74, P2 70, P3 26, P5 74), and the Rust arm's used-up
partner taken (P3 1).

## Verification

Every arm prints the same output as `recover.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.2 s to 0.35 s and the
differential 1.1 s; compiled it takes 0.5 s.

`karac fix` carries the template in three rounds of 27, 2 and 2 edits:
Rust's spellings (`Vec<..>` and `HashMap<..>` to `[..]`, the `use` line
dropped, `||` to `or`, `for &x in &nums` to `for x in ref nums`, the
`&` dropped from the keys of `cnt[&x]` and `get_mut(&..)`, `|&x|` to
`|x|`, `::new` and `Solution::` to `.`, `struct Solution;` to `struct
Solution {}`); then `HashMap` to `Map`; then the parameter made `own
Vec[i32]`, since `let mut nums = nums;` moves it, and `vec![]` to
`Vec.new()`.

## Benchmarks

The bench builds 40 arrays of 2000 numbers once, an original of 1000
values from 1 to 1000, 10000 or 100000 in turn shifted by a `k` up to
500 and shuffled, then solves every array 200 times, every number one
larger before each solve so that no solve repeats one before, with the
★ arm in all five languages. Every implementation prints `8000 solves:
8000000 values recovered, checksum 504666638`.

BENCHTAB
