# 1005. Maximize Sum Of Array After K Negations

Given an integer array `nums` and an integer `k`, modify the array in
the following way: choose an index `i` and replace `nums[i]` with
`-nums[i]`. You should apply this process exactly `k` times. You may
choose the same index `i` multiple times.

Return *the largest possible sum of the array after modifying it in
this way*.

```
nums = [4,2,3], k = 1             ->  5
nums = [3,-1,0,2], k = 3          ->  6
nums = [2,-3,-1,5,-4], k = 2      ->  13
```

**Constraints:** `1 <= nums.length <= 10^4`; `-100 <= nums[i] <= 100`;
`1 <= k <= 10^4`.

## Approaches

Flipping `x` adds `-2x` to the sum, so the most negative numbers are
the best to flip, most negative first. Once no negative is left, flips
cancel in pairs on any one number, and an odd one left over costs least
on the number nearest zero. The five arms reach those flips in five
ways.

| file | mechanism |
|---|---|
| `largest_sum.kara` ★ | counting: every number is between -100 and 100, so a count of each value orders them in one pass; the counts are walked up from -100, each negative turned into its positive while flips remain, and an odd flip left costs the smallest number present. O(n + 201) |
| `largest_sum_sort.kara` | sort, then flip: the negatives come first, most negative first, and are flipped in turn while flips remain; an odd flip left lands on the smallest number now in the array. O(n log n) |
| `largest_sum_heap.kara` | the statement, k times, always on the best index: the smallest number, taken from a smallest-first `PriorityQueue` and put back negated. O(n + k log n) |
| `largest_sum_abs.kara` | by size: sorted by absolute value, largest first, each negative is flipped while flips remain, and an odd flip left goes to the last number, the one nearest zero. O(n log n) |
| `largest_sum_select.kara` | selection: with at least `k` negatives, the answer is the sum less twice the sum of the `k` smallest numbers, found by a three-way quickselect without sorting; with fewer, it is the sum of the sizes, less twice the smallest size when an odd flip is left. O(n) on average |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 21 lines. The first eleven are LeetCode's
three examples and eight more: one negative with one flip and with
two; one positive with one flip; a 0 with three flips; two negatives
and one flip, which must go to the more negative; four negatives and
six flips, the two left over cancelling; three flips on `[-1,-1,1]`,
the odd one costing a 1; and four flips on `[100,-100,7]`, the odd one
landing on the 7. Then six arrays of LeetCode's longest size, 10,000
numbers, with up to 10,000 flips: all -100 with 10,000 flips and with
9,999; all 100 with 9,999 and with 10,000; and -100 and 99 in turn
with 5,001 flips, one more than the negatives, and with 2,500, half of
them. Then totals over random arrays, each number negative with a
random chance in 8 and `k` from 1 to twice the length plus one, at most
10,000: 3,000 arrays of up to 8 numbers between -6 and 6, then 1,000
of up to 100 numbers, 100 of up to 2,000 and 3 of up to 10,000, all
between -100 and 100. `largest_sum.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: each of the `k` steps negates one number, any one, so
it walks the sets of negated numbers reachable after each step and
takes the best sum among those reachable after exactly `k`. It checks
3,200 random arrays: 3,000 of up to 6 numbers, of sizes up to a random
bound from 1 to 6, against the statement, and 200 of up to 300 numbers
between -100 and 100 against the other properties, each with `k` from
1 to twice the length plus two.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 arrays |
| P2 | `k + 2` flips never give less, and give the same once `k` reaches every negative |
| P3 | the array reversed gives the same answer |
| P4 | at most the sum of the sizes, and all of it when `k` reaches every negative and the flips left cancel or a 0 can take them |
| P5 | the answer differs from the sum by an even amount, and is at least what spending all `k` flips on the smallest number gives |
| P6 | each arm agrees with at least two of the other four |

P2 holds because the two extra flips can cancel on any number, and
once every negative is reached they can do nothing else useful, since
the parity of the flips left is the same. P5 holds because each flip
moves the sum by twice a number, and flipping the smallest number `k`
times is one of the choices.

It prints `3200 arrays of 43650 numbers: answers sum to 1465571,
checksum 494037832, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (8.6 s, most of it the heap arm's flips one at a time) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Thirty-one edits to the differential, each run under `karac __mir-run`
and `karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every copy of a value flipped, past `k` | P1 71, P2 12, P6 88 |
| M2 | ★: the parity read backwards | P1 1217, P4 592, P5 435, P6 1274 |
| M3 | ★: the odd flip costs the number once, not twice | P1 555, P5 390, P6 576 |
| M4 | sort: the smallest starts at 0 | P1 555, P6 576 |
| M5 | sort: the odd flip on the largest | P1 1054, P2 75, P4 771, P5 595, P6 1122 |
| M6 | sort: flips never used up | P1 643, P4 248, P5 181, P6 718 |
| M7 | heap: the smallest put back unflipped | P1 1963, P4 1451, P5 1020, P6 2139 |
| M8 | heap: one flip short | P1 1408, P2 126, P4 693, P5 535, P6 1511 |
| M9 | heap: largest first | P1 2417, P2 180, P4 2011, P5 2154, P6 2615 |
| M10 | abs: smallest size first | P1 1197, P2 7, P4 771, P5 672, P6 1325 |
| M11 | abs: every negative flipped, past `k` | P1 182, P2 51, P6 242 |
| M12 | abs: any flip left lands, even ones | P1 461, P2 110, P4 482, P5 313, P6 482 |
| M13 | select: one copy of the pivot counted | P1 87, P2 46, P3 55, P4 46, P6 136 |
| M14 | select: the pivot's copies looked at again | P1 61, P2 52, P3 97, P4 61, P6 117 |
| M15 | select: the parity read backwards | P1 1016, P2 110, P4 482, P5 313, P6 1058 |

P1 and P6 kill all fifteen, P4 eleven, P2 and P5 ten each, and P3 two.
The checks draw no random number that depends on an answer, so every
mutant sees the same arrays and their counts can be compared. P3 kills
only the two selection edits because only that arm's answer can depend
on the order of the numbers: a broken quickselect picks its pivots from
the middle of what is left, which a reversed array changes, while the
other four arms sort or count first. M4 is caught only by the
statement and by agreement: starting the smallest at 0 makes an odd
flip free on an array of positives, which overshoots, but stays within
the sum of the sizes that P4 allows and above P5's floor.

Sixteen other edits were tried and set aside. Six change no answer:
the ★ and sort arms flipping 0s as if negative, which spends flips on
a number that does not change while a 0 makes any odd flip free;
selection counting 0s as negatives, for the same reason; selection
taking `k` equal to the negatives by the other case, which then has no
flips left; selection's `need == below` taking the other branch, which
adds the whole smaller part and stops; and selection's left-middle
pivot. Three failed exactly the same checks as a kept one: selection's
odd flip costing the number once, as M3; selection's nearest size
starting at 0, as M4; and abs's odd flip on the largest, as M5. Six
were killed but beyond three an arm: sort reversing instead of
sorting, the heap's one flip too many and its sizes summed, abs sorted
by value, selection leaving out the first of the smaller part, and
selection taking the sum for the sum of sizes. One crashed: ★ putting a
flipped negative back as itself leaves no number at or above 0 on an
all-negative array, and its search for the smallest runs off the
counts, an index out of bounds at the same line under both lanes.

## Verification

Every arm prints the same output as `largest_sum.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build` binary print the same output
for every arm and the differential. The release build and the runtime
archives are at kara `c443cbdc2b`. Under `karac __mir-run` the arms
take 1.2 s (sort) to 10.3 s (heap); compiled, all five take under
0.5 s.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
arrays of 10,000 numbers, LeetCode's longest, once, each number from
-100 to 100 and, in array `t`, negative with chance `t % 7 + 1` in 8.
In each of 2,500 rounds it runs the arm on every array, each round
starting from a different one, with `k` from 1 to 10,000 by a formula
of the round and the array, and folds every answer into a checksum.
Every implementation prints `2500 rounds over 20 arrays of 10000
numbers: answers sum to 20060314818, checksum 561951185`. Each call
allocates its 201 counts on the heap and reads all 10,000 numbers once.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `c443cbdc2b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.281 to 0.346 s | 0.295 s |
| Rust (`rustc -O`) | 0.341 to 0.407 s | 0.357 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.408 to 0.476 s | 0.425 s |
| Go | 0.358 to 0.478 s | 0.371 s |
| Python | 26.0 s | |
| Kāra (`karac build`) | 0.387 to 0.445 s | 0.406 s |

`bench.sh` builds the Kāra program with `karac build`, which is the v2
compiled backend since M3. Python's run is about 64 times Kāra's.

v2 took 0.95 times Rust's median time under overflow checks and 1.37
times C's. Under valgrind's cachegrind v2 ran 7,683 million
instructions and 2,047 million branches, Rust with overflow checks
6,183 million and 2,050 million, Rust without them 4,164 million and
1,016 million, and C 1,537 million and 139 million; every program
mispredicted about 0.22 million. The counting loop is where they part:
C turns it into far fewer branches than the checked versions, and the
checked ones pay a bounds check and an overflow check on each count.
