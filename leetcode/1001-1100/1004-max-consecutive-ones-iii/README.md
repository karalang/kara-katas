# 1004. Max Consecutive Ones III

Given a binary array `nums` and an integer `k`, return *the maximum
number of consecutive* `1`*'s in the array if you can flip at most* `k`
`0`'s.

```
nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2                      ->  6
nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3      ->  10
```

**Constraints:** `1 <= nums.length <= 10^5`; `nums[i]` is either `0`
or `1`; `0 <= k <= nums.length`.

## Approaches

Flipping a 0 only helps inside the run it joins, so the answer is the
longest window of `nums` holding at most `k` 0s. Two arms walk that
window along the array, one shrinking it and one never letting it
shrink; one reads the answer off the positions of the 0s; one searches
prefix counts for each window's start; and one keeps the flipped 0s in
a queue.

| file | mechanism |
|---|---|
| `longest_ones.kara` ★ | a sliding window: the right end takes each number, and while the window holds more than `k` 0s the left end steps forward. O(n) |
| `longest_ones_grow.kara` | a window that never shrinks: when it holds too many 0s, the left end takes one step with the right, keeping its length; it grows only when it holds at most `k`, so its final length is the answer. O(n) |
| `longest_ones_gaps.kara` | between the zeros: with the 0s' positions written down and sentinels at -1 and n, a best window flips `k` 0s in a row and stretches from just after the 0 before them to just before the 0 after. O(n) |
| `longest_ones_search.kara` | prefix counts and a search: for each right end, the first start whose window holds at most `k` 0s, by binary search over the count of 0s before each place. O(n log n) |
| `longest_ones_queue.kara` | a queue of flipped zeros: each 0 joins at the back, and when that makes `k + 1` the oldest leaves at the front and the window starts just after it. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 18 lines. The first ten are LeetCode's two
examples and eight more: all 1s with no flip; all 0s with no flip and
with every 0 flipped; one 0 with and without a flip; a 0 between two
1s with and without a flip; and `[1,1,0,1,1,0,0,1]` with one flip,
where the best flip joins two runs. Then four arrays of LeetCode's
longest size, 100,000 numbers: all 1s; all 0s with no flip and with
`k = 100000`; and 1 and 0 in turn with `k = 25000`. Then totals over
random arrays, each 1 with a random chance in 8 and a random `k` up to
the length: 3,000 arrays of up to 12 numbers, 1,000 of up to 100, 100
of up to 2,000 and 3 of up to 100,000. `longest_ones.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every subarray, kept when it holds at most `k` 0s,
which flipped make it all 1s. It checks 3,200 random arrays: 3,000 of
up to 12 numbers against the statement and 200 of up to 300 against
the other properties, each with a random `k` up to the length plus one.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 arrays |
| P2 | `k + 1` flips never give less, and give more unless `k` already covers every 0 |
| P3 | the array reversed gives the same answer |
| P4 | at least the longest run of 1s plus `k`, or the whole length |
| P5 | at most the 1s plus the flips that find a 0, and the whole length when every 0 can be flipped |
| P6 | each arm agrees with at least two of the other four |

P2 holds because the best window for `k` flips, when it is not the
whole array, can take one more neighbour with one more flip; P4
because a run of 1s can take any `k` neighbours with `k` flips; and P5
because a window holds only 1s and flipped 0s.

It prints `3200 arrays of 48412 numbers: answers sum to 38495,
checksum 958883355, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (2.3 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: up to `k + 1` 0s let in | P1 1091, P2 357, P5 978, P6 1187 |
| M2 | ★: the window one short | P1 2867, P2 134, P4 2551, P5 2013, P6 3066 |
| M3 | ★: a 0 leaving counted twice | P1 668, P2 371, P3 340, P5 661, P6 760 |
| M4 | grow: the length one short | P1 3000, P4 2685, P5 2013, P6 3200 |
| M5 | grow: a 0 leaving gives no flip back | P1 307, P3 521, P4 256, P6 366 |
| M6 | grow: a 1 leaving gives a flip back | P1 390, P3 491, P4 202, P6 455 |
| M7 | gaps: when every 0 can be flipped, the count of 0s answered | P1 1694, P2 207, P4 1797, P5 1797, P6 1797 |
| M8 | gaps: one too long | P1 1091, P2 300, P5 866, P6 1187 |
| M9 | gaps: the left sentinel at 0 | P1 165, P3 322, P4 111, P6 175 |
| M10 | search: fewer than `k` 0s allowed | P1 1360, P2 134, P4 1181, P5 406, P6 1459 |
| M11 | search: the 1s counted, not the 0s | P1 1700, P2 751, P4 829, P5 1627, P6 1845 |
| M12 | search: the right end's own number left out | P1 951, P2 251, P3 322, P5 775, P6 1040 |
| M13 | queue: only `k - 1` flips kept | P1 1033, P2 340, P4 852, P5 283, P6 1130 |
| M14 | queue: the window starts on the 0 let go | P1 926, P2 250, P3 322, P5 762, P6 1012 |
| M15 | queue: the newest 0 let go, not the oldest | P1 188, P2 75, P3 371, P4 135, P6 245 |

P1 and P6 kill all fifteen, P2 and P5 eleven each, P4 ten and P3
seven. The checks draw no random number that depends on an answer, so
every mutant sees the same arrays and their counts can be compared. P4
and P5 split the edits by direction: an edit that answers too little
fails P4 (M5, M6, M9, M15) and one that answers too much fails P5 (M1,
M3, M8, M12, M14), while M2, M4, M7, M10, M11 and M13, which answer too
little, fail P5 as well through its second half, since they fall short
of the whole length when every 0 can be flipped. P3 sees the edits that
treat the two ends of a window differently: M3, M5 and M6, which count
the number leaving at the left end wrongly; M9 and M12, which misplace
one end; and M14 and M15, which start the window at the wrong place.

Ten other edits were tried and set aside. Five failed exactly the same
checks as a kept one: grow allowing one more flip or starting with
`k + 1` flips, and queue keeping `k + 1` flips, as M1; and search's
and queue's windows one short, as M2. Four were sound but beyond three
an arm: gaps not trying the last run of `k` 0s, gaps with its right
sentinel at `n - 1`, the ★ answer starting at 1, and search never
finding the empty window, the last two failing the same checks as each
other. One crashed: ★ counting the 1s instead of the 0s runs its left
end off the array, an index out of bounds at the same line under both
lanes.

## Verification

Every arm prints the same output as `longest_ones.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. The release build and the runtime archives are at kara `c443cbdc2b`.
The sanitizer lane has reported leaks since kara `3c8e763161` (a
two-node `shared` cycle there reports its 64 bytes), so the leak check
needs no shim now: all five arms and the differential report none.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
arrays of 100,000 numbers, LeetCode's longest, once, array `t` holding
a 1 with chance `t % 7 + 1` in 8. In each of 30 rounds it runs the arm
on every array, each round starting from a different one, with `k`
from 0 to 2,999 by a formula of the round and the array, and folds
every answer into a checksum. Every implementation prints `30 rounds
over 20 arrays of 100000 numbers: answers sum to 2650188, checksum
865873186`. Each call reads all 100,000 numbers once with the right
end and at most once more with the left.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `c443cbdc2b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.431 to 0.493 s | 0.459 s |
| Rust (`rustc -O`) | 0.434 to 0.474 s | 0.451 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.469 to 0.544 s | 0.505 s |
| Go | 0.462 to 0.515 s | 0.495 s |
| Python | 12.6 s | |
| Kāra (`karac build`) | 0.498 to 0.559 s | 0.516 s |

`bench.sh` builds the Kāra program with `karac build`, which is the v2
compiled backend since M3. Python's run is about 24 times Kāra's.

v2 took 1.02 times Rust's median time under overflow checks and 1.12
times C's. Under valgrind's cachegrind v2 ran 1,574 million
instructions and 448 million branches with 39.1 million mispredicted,
Rust with overflow checks 1,564 million, 416 million and 38.3 million,
and C 1,091 million, 179 million and 38.3 million. All three miss the
same 38 to 39 million branches, the shrink loop's exit on random data;
C runs fewer instructions because it has no bounds or overflow checks
to make.

The Rust mirror first wrote the window as `(right - left + 1) as i64`
on `usize`s. When `k` is 0 and the right end reads a 0, the shrink
loop leaves `left` one past `right`, so `right - left` underflows:
`rustc -O` wraps and gets the right answer by accident, and the
overflow-checked build panics. It now subtracts in `i64`;
the other mirrors already subtract signed integers.
