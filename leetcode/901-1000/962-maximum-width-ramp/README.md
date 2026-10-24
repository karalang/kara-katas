# 962. Maximum Width Ramp

A **ramp** in an integer array `nums` is a pair `(i, j)` for which
`i < j` and `nums[i] <= nums[j]`. The **width** of such a ramp is
`j - i`. Given an integer array `nums`, return *the maximum width of a
ramp in* `nums`. If there is no ramp in `nums`, return `0`.

```
nums = [6,0,8,2,1,5]              ->  4
nums = [9,8,1,0,1,9,4,0,4,1]      ->  7
```

**Constraints:** `2 <= nums.length <= 5 * 10^4`;
`0 <= nums[i] <= 5 * 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `max_width_ramp.kara` ★ | a decreasing stack: a ramp's left end can always be taken as a number smaller than every number before it, so the prefix minima, left to right, form a stack of falling numbers. Right ends walked from the last place back pop every top they reach, each popped pair the widest ramp from that top, since every later right end has been tried. O(n) |
| `max_width_ramp_sorted.kara` | the places sorted by their numbers, ties by place: every place met earlier in that order holds a number at most as large, so the widest ramp ending at a place starts at the smallest place met so far. O(n log n) |
| `max_width_ramp_suffix.kara` | the largest number from each place to the end, then two pointers moving right together: the right end advances while the ramp from the left end still reaches its suffix maximum, the left end otherwise. O(n), one extra array |
| `max_width_ramp_search.kara` | the prefix minima as in ★, and for every right end a binary search for the first of them at most its number. O(n log n) |
| `max_width_ramp_fenwick.kara` | a Fenwick tree over the numbers giving the smallest place, so far, that holds a number at most v; each place asks it for its own number and is then added. O(n log m) for numbers up to m |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 19 lines: LeetCode's two examples and nine
more (two falling, two rising, two equal, three falling and three
rising, four equal, a late largest number, a ramp around a peak, and 0
and 50000 at both ends); for 300 random cases of 2 to 20 numbers from 0
to at most 9, 3,219 numbers in all, the total of the widths and a
checksum; and seven cases of LeetCode's largest size, 50000 numbers:
random from 0 to 50000, falling, rising, falling then rising, falling
and rising in turn, all sevens, and falling with 50000 at the end.
`max_width_ramp.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair `i < j` tried and the widest with
`nums[i] <= nums[j]` kept. It checks 3,200 random cases: 3,000 of 2 to
10 numbers from 0 to at most 6 against the statement, and 200 of 2 to
2000 numbers from 0 to at most 49000 against the other properties;
217,111 numbers in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | every number 1000 larger gives the same answer |
| P3 | the numbers back to front, each x turned into 50000 - x, give the same answer |
| P4 | every number twice, side by side, gives twice the width and one more |
| P5 | each number replaced by its rank among the distinct numbers gives the same answer |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 217111 numbers: the ramps sum to 212405,
checksum 424820577, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` (25 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-one edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal right end refused | P1 1530, P4 774, P6 1530 |
| M2 | ★: the walk starting one place in | P1 2314, P3 1369, P4 2442, P6 2442 |
| M3 | ★: the last pair popped kept, not the widest | P1 339, P3 752, P6 383 |
| M4 | sorted: the last place met, not the smallest | P1 2072, P4 3073, P6 2268 |
| M5 | sorted: the smallest place met starting at 0 | P1 986, P6 1091 |
| M6 | sorted: numbers and places added for the key | P1 902, P4 124, P5 185, P6 937 |
| M7 | suffix: only the last number carried back | P1 362, P3 752, P6 416 |
| M8 | suffix: each ramp one narrower | P1 2873, P4 3200, P6 3073 |
| M9 | suffix: no maxima carried back | P1 943, P3 1615, P6 1141 |
| M10 | search: rising numbers kept as lows | P1 977, P3 1736, P6 1162 |
| M11 | search: the upper bound set below the middle | P1 866, P3 276, P6 909 |
| M12 | search: the last low never used | P1 1608, P3 1301, P4 1391, P6 1609 |
| M13 | fenwick: the latest place stored, not the smallest | P1 2177, P2 107, P3 1002, P4 3073, P5 510, P6 2373 |
| M14 | fenwick: the top node never updated | P1 1170, P3 1098, P4 526, P5 345, P6 1170 |
| M15 | fenwick: the last node read, not the least | P1 346, P2 2856, P3 2983, P4 39, P5 304, P6 394 |

P1 and P6 kill all fifteen, P3 ten (M2, M3, M7, M9 to M15), P4 nine
(M1, M2, M4, M6, M8, M12 to M15), P5 four (M6, M13 to M15) and P2 two
(M13, M15). P2 only reaches the Fenwick arm: a shift changes nothing
the other arms read, but it moves every number to another node of the
tree.

Sixteen other edits were tried and set aside. Nine failed exactly the
same checks as a kept one: sorted ordering ties by place backwards,
search refusing an equal low, and Fenwick leaving equal numbers out of
its query or storing each place one number up, as M1; search taking
every ramp from the first low and Fenwick filling its tree with place
0, as M5; suffix and search keeping the latest ramp rather than the
widest, as M7; and Fenwick making each ramp one narrower, as M8. Three
crashed rather than fail a check: suffix refusing an equal maximum,
leaving the last number out of its maxima, or never setting the next to
last, each let the left pointer pass the right one and run off the end
of the array, which the differential reports as an index out of bounds.
Two were sound but beyond three an arm: ★ pushing every place, and
Fenwick keeping the latest ramp rather than the widest.

Two were equivalent. ★ pushing equal numbers onto the stack too: the
later copy is popped first, and the earlier one beneath it still makes
the wider ramp. And search never searching the last low: the last low
is the smallest number of all, so it is at most every right end, and
the search lands on it anyway when nothing earlier qualifies.

## Verification

Every arm prints the same output as `max_width_ramp.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `cb8ffcccec`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` suffix
takes 0.58 s, ★ 0.95 s, sorted 1.3 s, search 1.6 s and Fenwick 2.9 s,
and the differential 25 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 50 cases of 50000 numbers once, LeetCode's
largest, each falling by one every 1 to 5 places with 0 to 90 of random
noise added, so the stack of prefix minima is long and the walk back
pops most of it. In each of 40 rounds it runs the ★ arm on every case,
each round starting from a different one, and before each call sets one
number at a random place to a random value from 0 to 50000, so no call
sees an array it has seen before. Every implementation prints `40
rounds over 50 cases of 50000 numbers: the ramps sum to 90240211,
checksum 552095202`. Each call allocates its stack (a `Vec` in Kāra and
Rust, a slice in Go, a list in Python, a `malloc`'d array in C).

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.19 to 0.28 s | 0.23 s |
| Rust (`rustc -O`) | 0.21 to 0.25 s | 0.22 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.20 to 0.29 s | 0.22 s |
| Go | 0.28 to 0.38 s | 0.31 s |
| Python | 18.1 s | |
| Kāra (`karac build --mir`) | 0.32 to 0.45 s | 0.41 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 78 times
C's.

v2 takes 1.87 times Rust's median time under overflow checks and 1.78
times C's. Under valgrind's cachegrind v2 runs 4.00 billion
instructions and 1.33 billion branches with 2.39 million mispredicted,
Rust with overflow checks 2.49 billion, 0.72 billion and 2.30 million,
and C 2.17 billion, 0.56 billion and 2.14 million. The mispredictions
are the same in all three; v2's extra time is in its extra instructions
and branches, which were not traced to their source here.
