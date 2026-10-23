# 896. Monotonic Array

An array is monotonic if it is either monotone increasing or monotone
decreasing.

An array `nums` is monotone increasing if for all `i <= j`, `nums[i] <=
nums[j]`. An array `nums` is monotone decreasing if for all `i <= j`,
`nums[i] >= nums[j]`.

Given an integer array `nums`, return `true` if the given array is
monotonic, or `false` otherwise.

```
nums = [1,2,2,3]  ->  true
nums = [6,5,4,4]  ->  true
nums = [1,3,2]    ->  false
```

**Constraints:** `1 <= nums.length <= 10^5`, `-10^5 <= nums[i] <=
10^5`.

## Approaches

Both conditions only need checking between neighbours: if every number
is at least the one before it, every number is at least every number
before it. The arms differ in how they read the steps between
neighbours.

| file | mechanism |
|---|---|
| `is_monotonic.kara` ★ | one pass, two flags: a step up rules out non-increasing, a step down rules out non-decreasing, and the array is monotonic when either survives. O(n) |
| `is_monotonic_twopass.kara` | two passes: is no step down, and failing that, is no step up; each pass stops at the first step that answers it. O(n) |
| `is_monotonic_sign.kara` | the first change sets the direction: equal neighbours say nothing, the first pair that differs fixes the direction, and every later pair that differs must go the same way. O(n) |
| `is_monotonic_sorted.kara` | against its own sorted copy: a non-decreasing array is its own sorted copy and a non-increasing one that copy reversed. O(n log n) |
| `is_monotonic_ends.kara` | the ends choose the direction: a non-decreasing array ends no lower than it starts and a non-increasing one no higher, so the two ends say which to check, in one pass. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and five
more (one number, three equal ones, a fall then a rise, LeetCode's two
extreme values, and a rise, fall and rise); for 300 random cases of up
to 1,000 numbers, a third of them up to 5 and half of them from at most
3 values, the rest from LeetCode's whole range, sorted up or down, with
two places swapped or one set to a random number, how many are
monotonic, 189, with a checksum; and four of LeetCode's largest, 100,000
numbers sorted up, down, and each with two places swapped.
`is_monotonic.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair `i <= j` compared, both ways. It checks 3,200
random cases: 3,000 of up to 10 numbers from at most 4 values against
the statement, and 200 of up to 1,000 numbers from LeetCode's whole
range against the other properties, made as the arms' own random cases
are. The ★ arm finds 2,379 of them monotonic.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | the same answer for the array read backwards and with every sign flipped |
| P3 | every window of a monotonic array is monotonic, and a non-monotonic array stays so with a number added at either end |
| P4 | the numbers sorted up, sorted down, or all made the same are monotonic, and so is any array of at most two |
| P5 | the same answer with every number tripled and shifted by 7, and with every number written twice |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 2379
monotonic, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first step never looked at | P1 110, P2 112, P5 110, P6 110 |
| M2 | ★: an equal step taken for a step up | P1 441, P2 1085, P4 1827, P5 90, P6 457 |
| M3 | ★: both directions needed | P1 1216, P4 2108, P6 1287 |
| M4 | twopass: only non-decreasing asked | P1 515, P2 1287, P4 2108, P6 547 |
| M5 | twopass: each number compared with the first | P1 333, P2 721, P3 159, P6 387 |
| M6 | twopass: the last step never looked at going down | P1 57, P2 155, P5 57, P6 57 |
| M7 | sign: an equal step taken as a change | P1 611, P2 1085, P4 1827, P5 112, P6 628 |
| M8 | sign: every direction set to up | P1 306, P2 770, P4 1137, P6 337 |
| M9 | sign: a step up of one taken as a step down | P1 512, P2 1043, P3 305, P4 988, P5 532, P6 532 |
| M10 | sorted: the first comparison turned round | P1 1393, P2 1287, P3 749, P4 2108, P6 1561 |
| M11 | sorted: the sorted copy never reversed | P1 515, P2 1287, P4 2108, P6 547 |
| M12 | sorted: the copy never sorted | P1 692, P6 821 |
| M13 | ends: the middle taken for the end | P1 105, P2 389, P3 74, P4 374, P6 105 |
| M14 | ends: a step down of one let through going up | P1 375, P2 368, P3 57, P5 375, P6 375 |
| M15 | ends: each number compared with the first going down | P1 143, P2 507, P3 277, P6 186 |

P1 and P6 kill all fifteen. M12 is the one only they see: comparing an
array with an unsorted copy of itself always finds them equal, so the
mutant calls every array monotonic, and every other property holds of
an arm that always says yes. P2 kills every mutant that treats the two
directions differently, since reading the array backwards swaps them.
P5 catches the mutants that look at the size of a step rather than its
sign (M9, M14), as tripling every number makes every step a multiple of
three, and those that skip the first or last step (M1, M6), as writing
every number twice moves that step inward. P4 catches the mutants that
get equal neighbours wrong (M2, M7) through the sorted copies, which
hold equal neighbours wherever a number repeats: M2 rejects them going
down and M7 going up.

No mutant had to be replaced.

## Verification

Every arm prints the same output as `is_monotonic.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 1.1 to 1.4 s
each and the differential 3.2 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every frozen legacy lane, the interpreter, the JIT and `karac build
--legacy` with and without auto-par, prints the same output for all
five arms and the differential's line. Legacy's build warns that `nums`
is moved and used again in the two-pass arm and the differential,
which pass the same array to two calls; legacy reads a bare parameter
as owned, where v2 borrows it. Legacy refuses the bench program:
`is_monotonic(arrays[a])` moves a `Vec` out of an index
(`E_INDEX_MOVE_NON_COPY`). Legacy is frozen, so neither is filed.

## Benchmarks

The bench program uses the ★ arm over 16 arrays of 100,000 numbers,
LeetCode's largest, built once as random walks, half rising and half
falling by 0 or 1 a step. Each of 2,000 rounds sets one random place of
one array to the number before it, which keeps the array monotonic, or
in every other round to a random number, asks whether the array is
monotonic, and puts the number back. The ★ arm reads the whole array
whatever it finds, so the work is 200 million steps in every language.
Every implementation prints `2000 rounds over 16 arrays of 100000
numbers: 990 monotonic, checksum 566889042`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.12 to 0.20 s | 0.14 s |
| Rust (`rustc -O`) | 0.30 to 0.37 s | 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.31 to 0.40 s | 0.33 s |
| Go | 1.06 to 1.09 s | 1.08 s |
| Python | 18.2 s | |
| Kāra (`karac build --mir`) | 0.22 to 0.24 s | 0.23 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 894's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 0.68 times Rust's median time under overflow checks and 1.58
times C's. Under valgrind's cachegrind C runs 0.95 billion instructions
and 68 million branches, v2 0.81 billion and 37 million, Rust with
overflow checks 2.17 billion and 57 million, and Go 2.26 billion and
604 million. The first three take far fewer branches than the 200
million steps and mispredict almost none of them, so their loops do not
branch on the data; whether that is from vectorizing was not checked.
Go branches on each comparison and mispredicts 99.6 million times, about
once in every two steps, which is what a random walk's steps of 0 or 1
give;
at the usual cost of a mispredicted branch that would account for
most of its second, which is inferred rather than measured. The comparison with C and Rust waits
until after M4.
