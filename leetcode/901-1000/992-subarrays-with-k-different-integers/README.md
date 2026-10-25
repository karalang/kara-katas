# 992. Subarrays with K Different Integers

Given an integer array `nums` and an integer `k`, return *the number of
**good subarrays** of* `nums`.

A **good array** is an array where the number of different integers in
that array is exactly `k`.

- For example, `[1,2,3,1,2]` has `3` different integers: `1`, `2`, and
  `3`.

A **subarray** is a **contiguous** part of an array.

```
nums = [1,2,1,2,3], k = 2  ->  7
nums = [1,2,1,3,4], k = 3  ->  3
```

**Constraints:** `1 <= nums.length <= 2 * 10^4`;
`1 <= nums[i], k <= nums.length`.

## Approaches

A sliding window counts "at most k different" easily, since a window
that has too many only ever needs to give up its left end; "exactly k"
does not slide that way. Every arm turns one into the other.

| file | mechanism |
|---|---|
| `subarrays_with_k_distinct.kara` ★ | at most k, less at most k - 1: for each right end a window keeps the leftmost left end with at most k different values, counted in an array indexed by value, and every left end from there starts such a subarray. O(n) |
| `subarrays_with_k_distinct_two_left.kara` | one pass, two left ends: for each right end the left ends with exactly k values run from `far`, the leftmost with at most k, up to `near`, the leftmost with at most k - 1; both only move right, each with its own counts. O(n) |
| `subarrays_with_k_distinct_map.kara` | the ★ arm's window over a `Map`: counts live in a `Map` from value to count, filled with `entry(..).or_insert(0)`, and a value leaves the map when its count drops to 0, so the map's size is the number of different values. O(n) |
| `subarrays_with_k_distinct_fenwick.kara` | last places in a Fenwick tree: for each right end, each value's last place so far is marked, and the good left ends run from just after the (k + 1)-th mark from the right up to the k-th, found by descending the tree. O(n log n) |
| `subarrays_with_k_distinct_from_right.kara` | left ends, from the right: the two-left-ends pass turned round, with two right ends that only move left as the left end does. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 18 lines. The first ten are LeetCode's two
examples and eight more: one number; four equal numbers, where every
subarray is good; four different numbers taking all of them; a k no
subarray reaches; and four more short arrays where good subarrays
overlap in different ways. Then four arrays of LeetCode's largest
size, 20,000 numbers: all different, with k = 1 and with k = 20,000;
all ones, whose 200,010,000 subarrays are all good; and 1 to 100
repeated, with k = 50. Then totals over random arrays: 300 of up to 8
numbers below 4, 3,000 of up to 60 below 11, 300 of up to 1,000 below
31, and three of 20,000 below 201, each with a random k up to the
number of values allowed. `subarrays_with_k_distinct.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every contiguous subarray, with its different values counted
afresh, and those with exactly k counted. It checks 3,200 random
arrays: 3,000 of up to 10 numbers below 5 against the statement, and
200 of up to 300 numbers, below 31 and below 101 in turn, against the
other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 arrays |
| P2 | the array reversed gives the same count |
| P3 | the values renamed by a random permutation give the same count |
| P4 | over every k from 1 to the number of different values, the counts add up to all n(n + 1) / 2 subarrays |
| P5 | a value not in the array put at its end adds the subarrays it ends: one for each suffix, the empty one too, with k - 1 different values |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays of 46925 numbers: 85062 subarrays, checksum
890764544, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (51.5 s) and `karac __mir-llvm-run`, and the same
under `karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-seven edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one subarray per right end | P1 2509, P4 3200, P5 3119, P6 2689 |
| M2 | ★: a leaving value always drops the count | P1 1343, P2 1609, P5 1812, P6 1515 |
| M3 | ★: at most k + 1 less at most k | P1 2301, P4 3200, P5 1696, P6 2468 |
| M4 | two left: the run counted with `near` | P1 3000, P4 3200, P5 3200, P6 3200 |
| M5 | two left: `far`'s leaving value always drops the count | P1 891, P2 1150, P4 2036, P5 1845, P6 1057 |
| M6 | two left: `near`'s count set, not added to | P1 939, P2 1155, P4 2036, P5 1375, P6 1104 |
| M7 | map: at most k alone | P1 1922, P4 2695, P5 2114, P6 2114 |
| M8 | map: the difference one short | P1 3000, P4 3200, P6 3200 |
| M9 | map: the window shrunk before the new value goes in | P1 2509, P2 1248, P4 3200, P5 1696, P6 2689 |
| M10 | fenwick: the old mark never cleared | P1 1671, P2 934, P4 2667, P5 929, P6 1845 |
| M11 | fenwick: the k-th mark from the left | P1 2084, P2 1674, P5 2674, P6 2262 |
| M12 | fenwick: the run counted from place 0 | P1 1412, P4 2695, P5 2689, P6 1583 |
| M13 | from right: `close`'s leaving value always drops the count | P1 903, P2 1202, P4 2050, P6 1070 |
| M14 | from right: the windows stop short of the left end | P1 1078, P4 3200, P5 1086, P6 1086 |
| M15 | from right: `open`'s leaving value always drops the count | P1 873, P2 1150, P4 2050, P6 1039 |

P1 and P6 kill all fifteen, P4 thirteen, P5 twelve, P2 eight, and P3
none. Every arm, and every mutant, only ever asks whether two values
are equal, so renaming the values by a permutation changes nothing any
of them can see; P3 stays as a check on the arms, not on these edits.
Reversing the array, P2, catches the mutants that are lopsided: those
that lose track of how many values the window holds as values leave
(M2, M5, M6, M13, M15), M9, which looks at the window before the new
value is in it, and the Fenwick tree's marks, which are last places
and so have a direction (M10, M11). M8 is one short on every array, so
a new value at the end, P5, raises it by just as much as the right
answer, and only P1, P4 and P6 see it.

Twenty-two other edits were tried and set aside. Ten failed exactly
the same checks as a kept one. Seven failed M1's: two left with
`near` shrinking only above k; from right with `close` shrinking only
above k - 1, and with `open` shrinking at k; map counting every left
end, taking its second count at k + 1, and subtracting its counts the
wrong way round. From right counting the run with `close` fails M4's
checks, map adding its two counts fails M7's, and ★ and map letting
the window hold one value too many fail M3's. Three were sound but
beyond three an arm: fenwick's descent passing a total equal to the
rank and counting every value as new; from right setting `open`'s
count rather than adding to it. Two survived and are equivalent: ★
and map counting the left ends one short. Each of their two at-most
counts is then short by one for every right end, n in all, and the
difference cancels it.

Seven crashed, the same way in both lanes. ★ shrinking the window at
k, and two left shrinking `near` at k - 1, run the left end off the
array when the bound is 0, with `index out of bounds`; ★ never moving
the left end never stops, and the harness kills it after 300 s. Four
map mutants (a count set rather than added to, the window shrinking at
k, a value dropped at a count of 1, and the window starting at the
second number) all drop a value from the map while a copy is still in
the window, and stop at `seen[v] -= 1` when that copy leaves. Indexing
a `Map` with a missing key is specified to panic, but the message
both backends give is `runtime error: explicit panic`, which names no
key and reads as if the program had called `panic`, where a `Vec`
index out of range says `index out of bounds`. That is kara ledger row
`B-2026-10-25-1`.

## Verification

Every arm prints the same output as `subarrays_with_k_distinct.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build --mir` binary print the same
output for every arm and the differential. The release build is at
kara `395f71ae05`, the runtime archives rebuilt at `d867340a02`, whose
runtime sources are the same.
Under `karac __mir-run` the arms take 1.1 s (two left) to 9.1 s
(fenwick, whose tree is walked twice for every right end), and the
differential 51.5 s, most of it in P4's run over every k.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
random arrays of LeetCode's largest size, 20,000 numbers below 101,
once. In each of 100 rounds it runs the arm on every array with a k
from 1 to 60 that changes with the round and the array, each round
starting from a different array, and folds every count into a
checksum. Every implementation prints `100 rounds over 20 arrays of
20000 numbers: 61098113 subarrays, checksum 737141807`. Each call
slides two windows over the 20,000 numbers, each with a fresh, zeroed
count array of 20,001 entries, which C allocates with `calloc`.

The Rust program first added `(right - left + 1) as i64` in `usize`.
For the at-most-0 count the window is empty, `left` is one past
`right`, and the subtraction goes below 0: plain `rustc -O` wraps and
the sum comes out right, but with overflow checks on it panicked. It
now does the sum in `i64`, as the other four languages do.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.586 to 0.688 s | 0.630 s |
| Rust (`rustc -O`) | 0.626 to 0.667 s | 0.634 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.685 to 0.802 s | 0.698 s |
| Go | 0.880 to 0.934 s | 0.903 s |
| Python | 19.4 s | |
| Kāra (`karac build --mir`) | 0.870 to 0.926 s | 0.881 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 22 times
Kāra's.

v2 took 1.26 times Rust's median time under overflow checks and 1.40
times C's. Under valgrind's cachegrind v2 ran 5,134 million
instructions and 1,840 million branches with 50.8 million
mispredicted, Rust with overflow checks 3,662 million, 1,600 million
and 50.8 million, and C 2,519 million, 880 million and 50.7 million.
The three mispredict alike, about once for every time the window
gives up its left end, a choice the data makes. v2's extra branches
over Rust's are about 240 million, three for each of the 80 million
steps of the window's right end, which fits bounds checks on the
indexing there that Rust's optimizer merges or drops (inferred, not
traced).
