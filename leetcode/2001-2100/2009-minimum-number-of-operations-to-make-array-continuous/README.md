# 2009. Minimum Number of Operations to Make Array Continuous

You are given an integer array `nums`. In one operation, you can replace
any element of `nums` with any integer. `nums` is continuous when all its
elements are unique and the difference between its largest and smallest
element equals `nums.length - 1`. Return the fewest operations that make
`nums` continuous.

```
nums = [4,2,5,3]        ->  0
nums = [1,2,3,5,6]      ->  1   (6 becomes 4)
nums = [1,10,100,1000]  ->  3
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`.

A continuous array of length `n` is the window `[s, s + n - 1]`, one value
each. The values kept are the distinct ones already inside the window, so
the answer is `n` less the most distinct values any window of that length
holds, and a best window can always start at a value already there.

## Approaches

| file | mechanism |
|---|---|
| `continuous.kara` ★ | sorted and deduplicated; a right pointer that only moves forward finds, for each left value, how many distinct values its window holds. O(n log n) |
| `continuous_search.kara` | sorted and deduplicated; for each value as the window's low end, `partition_point` finds the first value past its high end. O(n log n) |
| `continuous_brute.kara` | the distinct values in a `Set`; each tried as the low end, every distinct value counted against it. O(n^2) |
| `continuous_set.kara` | the values in a `SortedSet`; for each as the low end, the values up to its high end counted with `range_inclusive`. O(n log n + n * kept) |
| `continuous_deque.kara` | the sorted values pass through a `VecDeque` window, a repeat skipped at the back, values too far below the newest leaving from the front; the longest the window gets is the most kept. O(n log n) |
| `continuous_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, a `mut nums: Vec<i32>` parameter, `sort_unstable`, `usize` lengths, `as i64` widenings, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the sum and a checksum of the answers for 3000
arrays of 1 to 12 values up to 1 to 30, and for 6 arrays of 3000 values up
to 5000, a million or a billion. `continuous.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every window `[s, s + n - 1]` from `n` below the smallest value
to the largest, each value counted as changed when it lies outside the
window or repeats a value before it, the fewest changed. It checks 1500
problems of 1 to 12 values up to 1 to 30. Every random choice of a problem
(the values, a shuffle, a shift, a value to copy) is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values shuffled leave the answer |
| P3 | every value raised by the same amount leaves the answer |
| P4 | every value `v` turned into `top + 1 - v` leaves the answer |
| P5 | a copy of a value already there, appended, raises the answer by 0 or 1 |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 problems: checksum 162672235, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the values never deduplicated | P1 879, P5 223, P6 879 |
| M2 | ★: the last value never reached | P1 735, P4 318, P6 735 |
| M3 | ★: the values never sorted | P1 1095, P2 808, P4 799, P5 61, P6 1095 |
| M4 | search: the window's high end left out | P1 414, P6 414 |
| M5 | search: the values below the low end counted | P1 915, P6 915 |
| M6 | brute: the window one long | P1 257, P6 257 |
| M7 | brute: the low end itself not counted | P1 1500, P6 1500 |
| M8 | brute: the answer counted against the distinct values | P1 930, P5 257, P6 930 |
| M9 | set: the smallest value skipped as a low end | P1 753, P4 318, P6 753 |
| M10 | set: only the smallest value as the low end | P1 302, P4 514, P6 302 |
| M11 | deque: a repeat compared with the front | P1 714, P4 409, P5 193, P6 714 |
| M12 | deque: the front let go one early | P1 297, P6 297 |
| M13 | deque: the newest value let go, not the oldest | P1 126, P4 197, P5 16, P6 126 |
| M14 | Rust: the length taken after the repeats are gone | P1 833, P6 833 |
| M15 | Rust: the last window kept, not the best | P1 1129, P6 1129 |

P1 and P6 kill all fifteen, P4 six, P5 five, P2 one and P3 none. Every arm
reads the values only through their order and their differences, which a
shift keeps, so no edit to an arm moves P3; it guards the literal reading
against the same. Most edits change the answer the same way on an input
and on its shuffle, its shift and its mirror: a window one long or one
short, a low end not counted, a length read from the wrong list. Those are
seen by P1 and P6 alone, and are kept for the distinct problems they fail
on. P4 sees the edits that treat the two ends of the sorted values apart:
the last value never reached (M2) or the first skipped (M9), only the
smallest tried (M10), a deque that looks for repeats at the wrong end or
lets go of the wrong end (M11, M13), and the values unsorted (M3). P5 sees
the edits that miscount repeats, which an appended copy adds (M1, M8, M11,
M13), and the values unsorted (M3). P2 sees only the unsorted values (M3).

The other fifteen fail as a kept one does, since the six arms differ in
how they find a window's high end more than in what they count. The
values never deduplicated fail alike in the ★, search, deque and Rust
arms; the high end left out, or the window sized by the distinct values
rather than `n`, alike in the ★, search, brute and set arms (414); the
values unsorted alike in the ★, deque and Rust arms; the answer counted
against the distinct values alike in the brute, set and Rust arms; the
last window kept alike in the ★, set and Rust arms; the values below the
low end counted alike in the search and brute arms; only the smallest low
end alike in the search and set arms; and a window measured before its
newest value joins fails as the low end not counted. Seven drafts that
duplicated another arm's signature were replaced before choosing: the
window one long in the ★, search, set, deque and Rust arms, the set arm's
high end left out, and the deque arm keeping repeats.

## Verification

Every arm prints the same output as `continuous.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any of
them. Under `karac __mir-run` the arms take 0.20 s (★) to 24 s (brute)
and the differential 1.2 s.

The ★, search, brute and set arms were written in Kāra and checked clean.
The deque arm compared `window.back() == Some(v)`, an `Option[ref i64]`
against an `Option[i64]`; `karac fix` adds the `.cloned()`.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in three rounds (11, 2 and 2 edits). Its
`mut nums: Vec<i32>` parameter becomes `nums: own Vec[i32]` with `let mut
nums = nums;` at the top of the body (kata 2008's fix), `sort_unstable`
becomes `sort`, and the `as i64` widenings of an `i32` go, since Kāra
widens a narrower integer to `i64` implicitly where they meet.

## Benchmarks

The bench builds 200 arrays of 2000 values once in all five languages, the
values spread over 1 to 2000 for the first array and up to 400000 for the
last, and runs the ★ arm on each for 25 rounds: 5000 calls, each copying,
sorting and deduplicating 2000 values and sweeping them. Every
implementation prints `5000 calls: sum 9656275, checksum 265197308`. Every
language copies the values per call, as the Kāra program does; C sorts with
`qsort` and Go with `sort.Slice`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.249 to 0.294 s | 0.253 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.246 to 0.327 s | 0.255 s |
| Rust (`rustc -O`) | 0.282 to 0.390 s | 0.303 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.291 to 0.358 s | 0.304 s |
| C (`clang -O3`) | 0.978 to 1.019 s | 0.996 s |
| Go | 1.263 to 1.318 s | 1.286 s |
| Python | 4.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.249 s) is not above its real time (0.253 s).

The sequential Kāra program is 0.84x Rust under overflow checks and 0.26x
C.