# 954. Array of Doubled Pairs

Given an integer array of even length `arr`, return `true` *if it is
possible to reorder* `arr` *such that* `arr[2 * i + 1] = 2 * arr[2 * i]`
*for every* `0 <= i < len(arr) / 2`*, or* `false` *otherwise*.

```
arr = [3,1,3,6]      ->  false
arr = [2,1,2,6]      ->  false
arr = [4,-2,2,-4]    ->  true
```

**Constraints:** `2 <= arr.length <= 3 * 10^4`; `arr.length` is even;
`-10^5 <= arr[i] <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `can_reorder_doubled.kara` ★ | counts, smallest first: every value counted in a `Map`, then the distinct values taken by absolute value, smallest first. The value taken can only be the smaller of its pair, since its half was taken before it, so all its remaining copies need a copy of its double, for a negative value as for a positive one; the zeros pair among themselves. O(n log n) |
| `can_reorder_doubled_queue.kara` | the values sorted by absolute value and walked in that order with a queue per sign of the doubles still awaited: a value is either the oldest double awaited, and pairs with it, or it starts a pair and waits for its own double. They pair up exactly when nothing is left waiting. O(n log n) |
| `can_reorder_doubled_table.kara` | the counts in a table indexed by value, offset by the largest absolute value m, walked by size from 1 to m, the positive and the negative value of each size pairing all their copies with their doubles; the zeros must be even. O(n + m) |
| `can_reorder_doubled_ordered.kara` | the counts in a `SortedMap`, keys taken in ascending order: the smallest key left is a pair's outer end, so a negative value pairs with its half (and an odd one has none) and a positive one with its double. O(n log n) |
| `can_reorder_doubled_halves.kara` | from the largest absolute value down: the value taken can only be the larger of its pair, so it must be even and each copy needs a copy of its half; a zero is its own half. The counts sit in a `Map`. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 20 lines: LeetCode's three examples and ten
more (two zeros, three zeros and 1, `[2,-4]`, `[-5,-10]`, a value that
needs its double twice, two pairs and two zeros, a negative chain,
repeated pairs, a negative and a positive pair, and the two signs of one
size interleaved); for 300 random cases of 2 to 12 values from -40 to
40, 2,176 values in all, how many can be paired and a checksum; and six
cases of LeetCode's largest size: 15,000 random pairs of a value up to
50,000 in size and its double, the same with one value made 99,999,
30,000 zeros, 1 to 2^15 with 1,875 copies each, -1 to -2^14 with 2,000
copies each, and x, 2x, -x and -2x for every x from 1 to 7,500.
`can_reorder_doubled.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the values split into pairs of a value and its double, found
by trying the first value not yet in a pair with every later one, and
backtracking. It checks 3,200 random cases, each made of pairs that are
a value and its double three times in four and two random values
otherwise, shuffled: 3,000 of 2 to 8 values from -8 to 8 against the
statement, and 200 of 2 to 400 values from -1,000 to 1,000 against the
other properties, 54,210 values in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | the values in another order give the same answer |
| P3 | every value negated gives the same pairs and the same answer |
| P4 | every value times k, k from 2 to 5, gives the same pairs and the same answer |
| P5 | the values written twice give the same answer: every count doubles, and taking the values smallest first compares only counts |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 54210 values, 1622 can be paired, checksum
274052789, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(8.0 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Forty-three edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the values taken in order of value, not size | P1 1062, P3 935, P6 1062 |
| M2 | ★: the double never used up | P1 1549, P6 1549 |
| M3 | ★: each value counted once | P1 553, P6 553 |
| M4 | queue: one queue for both signs | P1 129, P2 117, P5 7, P6 129 |
| M5 | queue: only the positives' queue checked at the end | P1 257, P3 486, P5 89, P6 257 |
| M6 | queue: the newest wait matched, not the oldest | P1 231, P6 231 |
| M7 | table: the walk stops one size short | P1 76, P5 72, P6 76 |
| M8 | table: the positive value walked in place of the negative | P1 1231, P3 1194, P5 46, P6 1231 |
| M9 | table: the zeros in fours, not twos | P1 325, P5 325, P6 325 |
| M10 | ordered: an odd negative value allowed | P1 40, P3 85, P4 40, P6 40 |
| M11 | ordered: a positive value paired with its half | P1 1051, P3 962, P4 52, P5 9, P6 1051 |
| M12 | ordered: an odd positive value refused too | P1 678, P3 844, P4 342, P6 678 |
| M13 | halves: an odd value allowed | P1 91, P4 91, P6 91 |
| M14 | halves: the half never used up | P1 1622, P6 1622 |
| M15 | halves: the value itself never used up | P1 225, P6 225 |

P1 and P6 kill all fifteen, P3 six (M1, M5, M8, M10, M11, M12), P5 six
(M4, M5, M7, M8, M9, M11), P4 four (M10 to M13) and P2 one (M4).

Twenty-eight other edits were tried and set aside. Seventeen failed
exactly the same checks as a kept one: ten as M2 (★ taking the largest
first, ★ refusing a double count equal to the copies, queue waiting for
the half, table never using up the double, table's range check off by
one, table using up the value rather than its double, ordered never
using up the partner, ordered taking the keys from the largest, halves
taking the smallest first, and halves checking used-up copies late);
three as M1 (queue sorting by value, ordered pairing a negative value
with its double, halves sorting by value from the top); two as M3
(table and ordered counting each value once); table walking only the
positive values, as M5; and table refusing an even number of zeros, as
M14. Three were sound but beyond three an arm: queue never sorting,
table walking the positive value a second time, and halves finding the
half by rounding up.

Eight were equivalent. Allowing an odd number of zeros, in ★, table and
ordered, and ★ pairing the zeros as any other value: the length is even,
so an odd number of zeros leaves an odd number of other values, which
cannot all pair, and the arm still finds one unpaired. Queue putting the
zeros with the negative values: the zeros come first and pair among
themselves in either queue. And ★, table and ordered asking a value for
one copy of its double rather than one per copy: the double's count goes
below zero, the double then asks its own double for a copy, and so on up
the chain, which ends at a value with no double and refuses.

## Verification

Every arm prints the same output as `can_reorder_doubled.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `46c2e7477d`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the
arms take 0.9 to 1.1 s each, ordered 2.0 s, and the differential 8.0 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program builds 20 sets of 30,000 values once, each 15,000
random pairs of a value from -50,000 to 50,000 and its double, shuffled;
in every fourth set one value is made odd. In each of 10 rounds it runs
the ★ arm on every set, each round starting from a different one, and
folds the answers into a checksum. Every implementation prints `10
rounds over 20 sets of 30000 values: 160 can be paired, checksum
707414432`. Each call counts the values in a new hash table and sorts
the distinct values by absolute value: a `Map` and `sort_by_key` in
Kāra, a `HashMap` and `sort_by_key` in Rust, a map and `sort.Slice` in
Go, a dict and `sorted` in Python, and in C an open-addressing table
with linear probing, sized at least twice the values, and `qsort`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.79 to 0.89 s | 0.84 s |
| Rust (`rustc -O`) | 0.52 to 0.60 s | 0.55 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.91 to 1.06 s | 1.02 s |
| Go | 1.23 to 1.43 s | 1.32 s |
| Python | 3.48 s | |
| Kāra (`karac build --mir`) | 0.69 to 0.84 s | 0.76 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 4.2 times
C's; its dict and its sort run in C.

v2 takes 0.75 times Rust's median time under overflow checks and 0.91
times C's. Under valgrind's cachegrind v2 runs 6.84 billion
instructions and 0.73 billion branches with 19.1 million mispredicted,
Rust with overflow checks 4.58 billion, 0.46 billion and 59.0 million,
and C 2.87 billion, 0.56 billion and 49.2 million. v2 runs the most
instructions and the fewest mispredicted branches; that was not looked
into further.
