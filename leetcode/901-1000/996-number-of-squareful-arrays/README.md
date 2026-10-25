# 996. Number of Squareful Arrays

An array is **squareful** if the sum of every pair of adjacent elements
is a **perfect square**.

Given an integer array `nums`, return *the number of permutations of*
`nums` *that are **squareful***.

Two permutations `perm1` and `perm2` are different if there is some
index `i` such that `perm1[i] != perm2[i]`.

```
nums = [1,17,8]  ->  2    ([1,8,17] and [17,8,1])
nums = [2,2,2]   ->  1
```

**Constraints:** `1 <= nums.length <= 12`;
`0 <= nums[i] <= 10^9`.

## Approaches

The values are the nodes of a graph whose edges join two values that
make a square, and the answer counts the paths through every value,
two counted as one when they give the same array. Two arms search
those paths and three count them with a table, by the set of places
used or by the values left; they differ in how equal values are kept
from being counted apart. Every arm tests a square with a
floating-point square root, corrected by a step either way.

| file | mechanism |
|---|---|
| `num_squareful_perms.kara` ★ | backtracking over the sorted values: a recursion places one unused value at a time where it makes a square with the one before, and of several equal values only takes the first one not yet used. O(n!) at worst |
| `num_squareful_perms_counts.kara` | backtracking over distinct values: a `Map` counts each value's copies, a table says which two distinct values make a square, and the recursion places a value with copies left. O(n!) at worst |
| `num_squareful_perms_paths.kara` | paths over places: a table over sets of places and the place last used counts every order of the places whose neighbours make squares, divided at the end by the factorial of each value's number of copies. O(2ⁿ n²) |
| `num_squareful_perms_memo.kara` | memoized on what is left: the orders still to come depend only on how many of each value are left, held as one number in a mixed radix, and on the last value placed, which together key a `Map` of answers. O(states × distinct values) |
| `num_squareful_perms_canon.kara` | canonical paths: the table over sets of places, but a place is only added once every equal value before it in the sorted array is used, so each array has one order of places and nothing needs dividing. O(2ⁿ n²) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 18 lines. The first ten are LeetCode's two
examples and eight more: one value; two that make a square; a value
that makes a square with neither of two equal ones; three zeros and two
ones, where the ones must not touch, and the same values given in
another order; five distinct values with two orders and five with ten;
and two values of 10^9, whose sum is not a square. Then five arrays of
LeetCode's largest size, 12 values: twelve 2s and twelve 0s, one array
each; the first twelve triangular numbers, each next pair of which adds
up to a square; six 0s and six 1s; and twelve values that never pair. Then totals over random
arrays: 300 of up to 4 values below 20, 3,000 of up to 8 below 50 and
300 of up to 12 below 30; half random values and half a random walk in
which each value makes a square with the one before it.
`num_squareful_perms.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every permutation of the places, the arrays they give
kept in a `Set` of strings when every two neighbours make a square,
tested by counting up to the square root; the answer is the set's size.
It checks 3,200 random arrays, made as the arms' random arrays are:
3,000 of up to 6 values below 30 against the statement, and 200 of up
to 8 below 60 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 arrays |
| P2 | the same values shuffled give the same answer |
| P3 | every value times 4 gives the same answer |
| P4 | a value that makes a square with none of them, put at the end, makes the answer 0 |
| P5 | 0 when the pairs that make squares do not join every value; otherwise at most the number of different arrays the values make |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays of 11337 values: 4886 squareful permutations,
checksum 444426776, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (16.0 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: equal values not skipped | P1 639, P5 144, P6 686 |
| M2 | ★: no square test | P1 2135, P4 3200, P5 1284, P6 2301 |
| M3 | ★: the values not sorted | P1 552, P2 345, P5 93, P6 594 |
| M4 | counts: the pair read on the table's diagonal | P1 1322, P4 627, P5 74, P6 1406 |
| M5 | counts: one value fewer placed | P1 1089, P4 1914, P5 313, P6 1166 |
| M6 | counts: every value counted once | P1 639, P6 686 |
| M7 | paths: divided by the count of values up to each | P1 1032, P2 594, P6 1109 |
| M8 | paths: every path starts at place 0 | P1 1274, P2 377, P6 1356 |
| M9 | paths: a way set, not added to | P1 577, P6 624 |
| M10 | memo: keyed on the counts alone | P1 653, P6 708 |
| M11 | memo: the counts' number not lowered as values are used | P1 877, P6 945 |
| M12 | memo: the radix one too small | P1 403, P6 441 |
| M13 | canon: every place may start | P1 602, P5 70, P6 642 |
| M14 | canon: equal values used in the reverse order | P1 602, P6 642 |
| M15 | canon: equal values in any order | P1 562, P5 76, P6 606 |

P1 and P6 kill all fifteen, P5 seven, P2 three, P4 three, and P3 none.
Every arm, and every mutant, only ever asks whether a sum is a square,
and four times a number is a square exactly when the number is, so P3
stays a check on the arms, not on these edits. P2 sees the edits whose
answer depends on where a value sits in the input: M3, whose equal
values only skip each other when sorting has put them side by side,
and M7 and M8, which read places by their number. P4 sees the three
that let a value through without making a square with its neighbour:
M2, M4, which tests each value against itself, and M5, which stops one
value short and so can leave the stranger out. P5's bound on the number
of different arrays catches the edits that count equal values apart
(M1, M13, M15, and M3 when copies are not side by side), as well as
those that count arrays that are not squareful at all.

Ten other edits were tried and set aside. Four failed exactly the same
checks as a kept one: counts testing a value against itself when it
builds its table, as M4; paths not dividing, as M1; canon not sorting,
as M3; and canon testing the last value against itself, as M4. Three
were sound but beyond three an arm: ★ not testing the first pair,
paths leaving out the paths that end at place 0, and memo not testing
the first distinct value as the last one placed. Two survived and are
equivalent: memo storing nothing, which only makes it slower, and ★
skipping an equal value when the one before it is used. That rule
takes the copies of a value from the last to the first; an order that
takes them otherwise strands a copy that can never be placed, and
never finishes, so each array is still counted once.

One was set aside because its answer is not a function of its input:
counts not putting a copy back after trying it. What it then counts
depends on the order it tries the distinct values in, which is the
`Map`'s iteration order, and that changes from run to run. Unpinned it
failed P1 1,251 and 1,186 times on two runs of the interpreter; with
`KARAC_HASH_SEED=1` it fails P1 1186, P2 290, P6 1265 in both lanes
alike. None crashed.

## Verification

Every arm prints the same output as `num_squareful_perms.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 0.81 s (counts) to 3.7 s
(paths, which fills its table for every set of places), and the
differential 16.0 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
arrays of LeetCode's largest size, 12 values, once, each a random walk
of values below 50 in which every value makes a square with the one
before it. In each of 300 rounds it runs the arm on every array, each
round starting from a different one, and folds every count into a
checksum. Every implementation prints `300 rounds over 20 arrays of 12
values: 258600 squareful permutations, checksum 864815297`. Each call
sorts a copy of the array and backtracks, testing a square at every
step with a floating-point square root; Python uses `math.isqrt`. The
C program needs `-lm` for `sqrt`, so `bench.sh` was edited by hand to
pass it, as kata 492's was.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.329 to 0.377 s | 0.343 s |
| Rust (`rustc -O`) | 0.335 to 0.374 s | 0.349 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.357 to 0.409 s | 0.373 s |
| Go | 0.328 to 0.380 s | 0.351 s |
| Python | 7.6 s | |
| Kāra (`karac build --mir`) | 0.416 to 0.500 s | 0.440 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 17 times
Kāra's.

v2 took 1.18 times Rust's median time under overflow checks and 1.28
times C's. Under valgrind's cachegrind v2 ran 2,429 million
instructions and 615 million branches with 54.0 million mispredicted,
Rust with overflow checks 1,867 million, 523 million and 53.0 million,
and C 1,437 million, 329 million and 49.0 million. The three mispredict
alike, which fits the misses being the search's own choices: whether a
value is used, a copy, and makes a square (inferred). v2's extra
instructions over Rust's were not traced to a source.
