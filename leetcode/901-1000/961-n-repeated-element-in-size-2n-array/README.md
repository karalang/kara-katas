# 961. N-Repeated Element in Size 2N Array

You are given an integer array `nums` with the following properties:
`nums.length == 2 * n`; `nums` contains `n + 1` unique elements; exactly
one element of `nums` is repeated `n` times. Return *the element that
is repeated* `n` *times*.

```
nums = [1,2,3,3]            ->  3
nums = [2,1,2,5,3,2]        ->  2
nums = [5,1,5,2,5,3,5,4]    ->  5
```

**Constraints:** `2 <= n <= 5000`; `nums.length == 2 * n`;
`0 <= nums[i] <= 10^4`; `nums` contains `n + 1` unique elements and one
of them is repeated exactly `n` times.

## Approaches

| file | mechanism |
|---|---|
| `repeated_n_times.kara` ★ | near neighbours: if no two copies of the repeated value were within two places, n copies would need 3(n - 1) + 1 places, more than 2n once n > 2, and with n = 2 they can only be three apart. So each number is compared with the next one, then the one after, then the one three on, and the first equal pair is the answer. O(n), no extra space |
| `repeated_n_times_seen.kara` | the first number met a second time, with a `Set` of the numbers seen. O(n) expected time, O(n) space |
| `repeated_n_times_tally.kara` | every number counted in an array of 10001 counters, then the counters read for the value counted n times. O(n + 10001) |
| `repeated_n_times_middle.kara` | sorted, the n copies are one run among 2n places, which reaches place n - 1 unless it is the whole second half: the number at n - 1 when it equals a neighbour, and the number at n otherwise. O(n log n) on a sorted copy |
| `repeated_n_times_pick.kara` | random pairs: two different places hold two copies with probability at least one in six, and no other value matches itself, so pairs of places are drawn from a fixed pseudo-random sequence until two different places agree. O(1) expected pairs |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines: LeetCode's three examples and seven
more (the copies first, at the two ends, at the second and fourth
places, 0 and 10000 among the values, and n = 3 with the copies
together or apart); for 300 random cases of 2n numbers, n from 2 to 10,
from 0 to 10000, 3,698 numbers in all, the sum of the repeated values
and a checksum; and six cases of LeetCode's largest size, 10000
numbers: in a random order, with 0 at every other place from the second
and 10000 from the first, with all the copies in the first half and all
in the second, and finally four numbers with the copies at the two
ends. `repeated_n_times.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each number's copies counted, and the one with n of them
returned. It checks 3,200 random cases, each made from a chosen value r,
n copies of it and n other distinct values, shuffled: 3,000 with n from
2 to 6 and values from 0 to at most n + 12 against the statement, and
200 with n from 2 to 5000 and values from 0 to 10000 against the other
properties; 1,011,040 numbers in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | the numbers in another order give the same answer |
| P3 | each number x turned into 10000 - x turns the answer the same way |
| P4 | the numbers back to front give the same answer |
| P5 | one more copy of r and the smallest value not yet there, each swapped to a random place, give the same answer |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 1011040 numbers: the repeated ones sum to
950508, checksum 942179879, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` (21 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-six edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only next neighbours compared | P1 485, P2 620, P3 485, P5 373, P6 485 |
| M2 | ★: nothing three apart compared | P1 91, P2 180, P3 91, P5 91, P6 91 |
| M3 | ★: the last pair at each distance skipped | P1 348, P2 370, P3 348, P4 495, P5 364, P6 348 |
| M4 | seen: each number added before it is looked up | P1 1598, P2 2210, P4 2613, P5 465, P6 1707 |
| M5 | seen: one more than the repeated value | P1 3000, P3 3200, P6 3200 |
| M6 | seen: each number added as the next one up | P1 2406, P2 1634, P3 2869, P4 2284, P5 1116, P6 2604 |
| M7 | tally: the value counted once answered | P1 3000, P3 3200, P5 1765, P6 3200 |
| M8 | tally: the counter for 10000 never read | P3 340 |
| M9 | tally: counters starting at 1 | P1 3000, P3 3200, P5 619, P6 3200 |
| M10 | middle: only the right neighbour compared | P1 669, P3 1303, P5 492, P6 669 |
| M11 | middle: not sorted | P1 1058, P2 1787, P4 1597, P5 1866, P6 1126 |
| M12 | middle: the middle one place right | P1 669, P3 1303, P5 560, P6 669 |
| M13 | pick: a place paired with itself | P1 602, P2 1023, P4 1062, P5 1072, P6 602 |
| M14 | pick: the place after the first answered | P1 1552, P2 2216, P4 2131, P5 2217, P6 1660 |
| M15 | pick: any two different places answered | P1 1557, P2 2224, P4 2552, P5 2132, P6 1655 |

P1 and P6 kill fourteen (all but M8), P5 thirteen (all but M5 and M8),
P3 ten (M1 to M3, M5 to M10, M12), P2 nine (M1 to M4, M6, M11, M13 to
M15) and P4 seven (M3, M4, M6, M11, M13 to M15). M8 falls to P3 alone:
the random values rarely include 10000, and P3 turns every 0 into one.

Eleven other edits were tried and set aside. Five failed exactly the
same checks as a kept one: ★ comparing each number with itself and
answering the first unequal pair, as M4 (all three answer the first
number); seen adding nothing and tally looking for one copy too many,
as M5; and tally looking for n - 1 copies, as M9. Four were sound but
beyond three an arm: ★ never comparing the first number, tally counting
each number at half its value, middle answering the left neighbour, and
pick taking a larger number at the first place as enough.

Two were equivalent. Middle answering one past the middle when the
number at n - 1 matches neither neighbour: then the run is the whole
second half, and with n >= 2 the place after n holds a copy too. And
pick drawing its second place as an offset from the first: the pair is
still a pseudo-random pair of places, so only the number of draws
changes.

## Verification

Every arm prints the same output as `repeated_n_times.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `cb8ffcccec`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` middle
takes 0.26 s, ★ 0.29 s, seen 0.34 s, pick 0.37 s and tally 0.58 s, and
the differential 21 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 50 cases of 10000 numbers once, LeetCode's
largest, each with its repeated value at every other place, from the
first place in half the cases and from the second in the rest. That is
the ★ arm's worst layout: no two copies are next to each other, so the
first pass reads the whole array before the second finds two copies two
apart. In each of 1000 rounds it runs the ★ arm on every case, each
round starting from a different one, and before each call swaps two of
the other values two places apart, so no call sees an array it has seen
before and the layout stays the same. Every implementation prints `1000
rounds over 50 cases of 10000 numbers: the repeated ones sum to
194850000, checksum 445420946`. No call allocates.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.22 to 0.29 s | 0.25 s |
| Rust (`rustc -O`) | 0.38 to 0.50 s | 0.42 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.26 to 0.33 s | 0.27 s |
| Go | 0.39 to 0.54 s | 0.44 s |
| Python | 25.2 s | |
| Kāra (`karac build --mir`) | 0.31 to 0.47 s | 0.36 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 100 times
C's. Rust without overflow checks was slower than with them in every
run here; that was not looked into.

v2 takes 1.31 times Rust's median time under overflow checks and 1.42
times C's. Under valgrind's cachegrind v2 runs 4.51 billion
instructions and 1.50 billion branches with 0.21 million mispredicted,
Rust with overflow checks 3.02 billion, 1.01 billion and 0.21 million,
and C 2.01 billion, 0.67 billion and 0.21 million: about nine
instructions for each pair of numbers compared in v2, six in Rust and
four in C.
