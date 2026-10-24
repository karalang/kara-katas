# 945. Minimum Increment to Make Array Unique

You are given an integer array `nums`. In one move, you can pick an index
`i` where `0 <= i < nums.length` and increment `nums[i]` by `1`.

Return *the minimum number of moves to make every value in* `nums`
***unique***.

The test cases are generated so that the answer fits in a 32-bit
integer.

```
nums = [1,2,2]          ->  1
nums = [3,2,1,2,1,7]    ->  6
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `min_increment_for_unique.kara` ★ | the values sorted, and going up the sorted list each raised, if it is below, to one above where the value before it ended, the steps counted; raising a smaller value never helps a larger one, so the sorted order is the cheapest. O(n log n) |
| `min_increment_for_unique_count.kara` | how many times each value comes counted, and the values walked upward: one copy stays at each value and the rest carry on to the next, each costing a step for every value it is carried past; after the largest value the carried copies settle one per value, `c (c - 1) / 2` steps more. O(n + max) time and space |
| `min_increment_for_unique_slots.kara` | the values taken in the order given, each moving up to the first value not yet taken, found by following links from each taken value to the one after it (union-find with paths shortened); the set of values taken does not depend on the order, so neither does the total. O(n α(n)) after O(max + n) set-up |
| `min_increment_for_unique_prefix.kara` | a closed form: in sorted order the `i`-th value ends at `i` plus the largest `a[j] - j` over `j` up to `i`, so the answer is the sum of those ends less the sum of the values, the largest kept as a running maximum. O(n log n) |
| `min_increment_for_unique_holes.kara` | in sorted order every copy of a value after the first moves up into a hole, a value nobody holds; walking up, each gap before the next value held offers its holes to the copies waiting below, and those still waiting after the largest value fill the values above it; the answer is the holes filled less the copies moved. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and six more
(one value, four equal values, three in order, two copies of the
largest value the constraints allow, two pairs, and a mixed array); for 300 random
arrays of 1 to 50 values from 0 to 30, the values, the moves and a
checksum; and four of LeetCode's longest, 100,000 values: random values
from 0 to 100,000, all different in falling order, each even number
from 0 to 99,998 twice, and 65,536 copies of 100,000, whose answer,
2,147,450,880, is the largest that equal values can give and still fit
in 32 bits. `min_increment_for_unique.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way of ending with distinct values, each no smaller
than where it started and none above the largest plus the number of
values, searched depth first, and the least total of increments. It
checks 3,200 random arrays: 3,000 of up to 5 values from 0 to 2, so
that repeats are common, against the statement, and 200 of up to 2,000
values from 0 to as many as 2,000, against the other properties;
202,372 values.

| | property |
|---|---|
| P1 | the statement's least total, on the small arrays |
| P2 | at least one move for each repeated value, and none exactly when the values are all different |
| P3 | the values in a random order, with 7 added to each, give the same answer |
| P4 | the values beside a copy of themselves raised past them all give twice the answer |
| P5 | one more value, random or a copy of one already there, never gives fewer moves |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays of 202372 values, checksum 210393827, 95000 checks
over 5 arms: 0 failures` under `karac __mir-run` (14 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first value raised to at least 1 | P1 1999, P2 559, P3 2120, P4 2120, P6 2120 |
| M2 | ★: each floor the value before as given | P1 1309, P6 1504 |
| M3 | ★: each value raised counted once | P1 959, P6 1148 |
| M4 | count: the carried copies settling one value too high | P1 1872, P4 2020, P6 2020 |
| M5 | count: the carried copies never settled | P1 930, P4 1059, P6 1059 |
| M6 | count: every copy at a value counted | P1 3000, P2 1048, P4 2020, P6 3200 |
| M7 | slots: one link followed | P1 1206, P3 578, P6 1401 |
| M8 | slots: each value counted half its steps | P1 1955, P2 1324, P3 544, P6 2152 |
| M9 | slots: every search from 0 | P1 1236, P2 1299, P3 3200, P4 3200, P5 398, P6 1369 |
| M10 | prefix: each end one lower | P1 3000, P2 2938, P5 837, P6 3200 |
| M11 | prefix: the running maximum starting one high | P1 3000, P2 1048, P4 3200, P5 34, P6 3200 |
| M12 | prefix: each value one lower in the maximum | P1 235, P2 308, P4 3200, P5 160, P6 356 |
| M13 | holes: the first hole of each gap skipped | P1 1882, P2 1289, P3 2116, P4 2116, P5 759, P6 2079 |
| M14 | holes: the next held value taken as a hole | P1 1005, P6 1200 |
| M15 | holes: a copy never taken off the waiting | P1 207, P3 394, P4 2152, P5 132, P6 394 |

P1 and P6 kill all fifteen, P4 nine, P2 eight, and P3 and P5 six each.

P2 misses the seven whose counts stay at 0 for distinct values and at
one move or more for each repeat: M2 measures each value from the one
before as it was given, M3 counts the values moved rather than the
steps, M4 and M5 get only the copies carried past the largest value
wrong, M7 settles some copies on a value already taken, M14 lets a copy
take the next value held, and M15 fills more holes than it has copies.
All of them still move every repeat at least once and nothing else.

P3 kills M1, M7, M8, M9, M13 and M15. ★, prefix and holes sort first
and count steps between values, so the order and a shift by 7 change
nothing for a mistake that keeps those two things. M1's floor of 1 and
M9's searches from 0 are tied to the values themselves; M13 and M15
fill a different number of holes from the copies they move, so a shift
by 7 changes the difference; and M7 and M8,
whose slot for each value depends on which values came before it, are
tied to the order.

P4 misses M2, M3, M7, M8, M10 and M14, whose mistakes are made one value
at a time and so add up over two blocks of values far apart, exactly as
the right answer does. The other nine do not add up that way.

P5 kills M9 to M13 and M15, whose answers can fall when another value is
added: M10's ends one lower and M11's maximum starting one high shift
by an amount that changes with the number of values, and M9, M12, M13
and M15 can find a cheaper way when there is more to choose from.

Fifteen other edits were tried and set aside. Nine failed exactly the
same checks as each other, in three groups, so none of them was kept:
four that answer 0 (★ allowing equal values, count counting each value
once, prefix with no running maximum, and slots never taking a value
that sits at its own slot); ★ and prefix never sorting; and three that
add a step for every value (slots counting one step too many and
starting each search one above, and prefix putting each end one
higher). Four were sound but beyond three an arm (count never walking
the largest value, prefix leaving the last value out, and holes leaving
one value too few above the largest and counting each hole one lower).
One crashed: slots linking each slot taken two on, with an index out of
bounds. One was equivalent: slots shortening each path to one past its
end, which is right, since the value found is taken at once and the one
after it is where the next search should go.

## Verification

Every arm prints the same output as `min_increment_for_unique.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.6 to 1.8 s each and the
differential 14 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The prefix and holes arms print the same output under the frozen legacy
interpreter, the legacy JIT and both legacy builds, with and without
auto-par. Legacy refuses the ★, count and slots arms, the differential
and the bench program at the first `*` on an element of a `Vec[i64]`'s
`.iter()` ("unary '*' requires 'ref T', ..."), legacy's older rule,
under which the element is a copy; under v2 it is a reference and the
`*` is required. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 20 arrays of 100,000 values once, LeetCode's
longest, each of random values from 0 to between 70,000 and 100,000, so
that every answer fits in 32 bits; in each of 5 rounds it runs the ★ arm
on every array, each round starting from a different one, and folds the
answers into a checksum. Every implementation prints `5 rounds over 20
arrays of 100000 values: 85107801245 moves, checksum 158708001`. Each
call copies the array and sorts the copy, and the sort is most of the
work: C sorts with `qsort`, Rust with `sort` (stable), Go with
`slices.Sort`, Python with `sorted`, and Kāra with `Vec.sort`, which for
a `Vec[i64]` the runtime hands to Rust's `sort_unstable`
(`runtime/src/lib.rs`, `karac_vec_sort_i64_8`).

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 1.19 to 1.32 s | 1.28 s |
| Rust (`rustc -O`) | 0.26 to 0.31 s | 0.27 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.27 to 0.34 s | 0.30 s |
| Go | 0.83 to 0.91 s | 0.87 s |
| Python | 3.21 s | |
| Kāra (`karac build --mir`) | 0.17 to 0.20 s | 0.19 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 2.5 times C's: its `sorted` is
written in C and needs no comparison function called through a
pointer.

v2 takes 0.63 times Rust's median time under overflow checks and 0.15
times C's. Under valgrind's cachegrind v2 runs 1.91 billion
instructions and 0.22 billion branches with 5.3 million mispredicted,
Rust with overflow checks 2.45 billion, 0.49 billion and 11.1 million,
and C 4.89 billion, 1.23 billion and 89 million, 168 million of its
branches indirect: `qsort` calling its comparison function for every
comparison. That v2 beats Rust because its unstable sort does less work
than Rust's stable `sort` on these arrays is inferred, not profiled;
the bench measures each language's usual sort more than the walk after
it.
