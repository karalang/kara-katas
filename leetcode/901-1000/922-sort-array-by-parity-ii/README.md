# 922. Sort Array By Parity II

Given an array of integers `nums`, half of the integers in `nums` are
odd, and the other half are even.

Sort the array so that whenever `nums[i]` is odd, `i` is odd, and
whenever `nums[i]` is even, `i` is even.

Return any answer array that satisfies this condition.

```
nums = [4,2,5,7]  ->  [4,5,2,7]   ([4,7,2,5], [2,5,4,7] and [2,7,4,5] are also accepted)
nums = [2,3]      ->  [2,3]
```

**Constraints:** `2 <= nums.length <= 2 * 10^4`; `nums.length` is
even; half of the integers in `nums` are even; `0 <= nums[i] <= 1000`.

## Approaches

Each parity has exactly as many values as indices, so every even index
holding an odd value is matched by an odd index holding an even value.

| file | mechanism |
|---|---|
| `sort_array_by_parity_ii.kara` ★ | two pointers in place: `i` walks the even indices, and when `nums[i]` is odd, `j` walks forward along the odd indices to an even value and the two swap. O(n), O(1) space |
| `sort_array_by_parity_ii_split.kara` | the even and the odd values copied apart, each in its original order, then written back in turn. O(n) extra space |
| `sort_array_by_parity_ii_sorted.kara` | a sorted copy, read by two cursors, one taking the even values for the even indices and one the odd values for the odd indices. O(n log n) |
| `sort_array_by_parity_ii_stacks.kara` | every misplaced even index and every misplaced odd index noted, then paired off and swapped: one swap a pair, the fewest possible. O(n) |
| `sort_array_by_parity_ii_counting.kara` | the values counted in an `Array[i64, 1001]`, then the even indices filled from the even values and the odd indices from the odd values, smallest first. O(n + 1000) |
| `differential.kara` | the five arms against the statement read literally, six properties |

The answer is not unique, and the arms give different ones: ★ and
stacks move as little as they can, split keeps each parity's order, and
sorted and counting give each parity in ascending order. So the harness
checks each result, prints whether it keeps the same values with every
value at an index of its own parity, and shows it in one canonical form,
the values at the even indices sorted and the values at the odd indices
sorted, which every correct answer shares. Every arm prints the same 9
lines that way: LeetCode's two examples and five more (already in place,
every value misplaced, repeated values, the extremes 0 and 1,000, and
eight values with a repeat); 300 random arrays of 2 to 2,000 values,
all valid, with a checksum; and LeetCode's largest, 20,000 values.
`sort_array_by_parity_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: try every order of the values, keep those in which each odd
value is at an odd index and each even value at an even one, and accept
the arm's answer if it is one of them. It checks 3,200 random arrays,
shuffled, half even and half odd: 3,000 of 2, 4 or 6 values below 6
against the statement, and 200 of 2 to 2,000 values up to 998 against
the other properties; 197,278 values in all.

| | property |
|---|---|
| P1 | the answer is one the statement accepts, on the small arrays |
| P2 | the answer holds the same values |
| P3 | every value of the answer is at an index of its own parity |
| P4 | an answer that keeps P2 and P3, given back to the arm, comes back unchanged |
| P5 | with every value 2 more, the answer is the same with every value 2 more |
| P6 | each arm's canonical form agrees with at least two of the other four |

It prints `3200 arrays, 197278 values, checksum 600932649, 95000 checks
over 5 arms: 0 failures` under `karac __mir-run` (20 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `j` stepping over every index, not just the odd ones | P1 302, P3 496, P6 496 |
| M2 | ★: index 0 never fixed | P1 1514, P3 1618, P6 1618 |
| M3 | ★: every other even index skipped | P1 985, P3 1185, P6 1185 |
| M4 | split: only multiples of 4 taken as even | P1 1297, P2 863, P3 1414, P5 2601, P6 1497 |
| M5 | split: a zero taken as odd | P1 1292, P2 725, P3 1322, P5 1405, P6 1405 |
| M6 | split: each even value read from the even-numbered slot at or below it | P1 1358, P2 1558, P6 1558 |
| M7 | sorted: the even values to the odd indices and the odd values to the even ones | P1 3000, P3 3200, P6 3200 |
| M8 | sorted: each odd value replaced by the larger of it and the last even value | P1 1219, P2 1418, P3 1418, P6 1418 |
| M9 | sorted: the last index never filled | P1 1920, P2 2120, P3 1592, P6 2120 |
| M10 | stacks: only one pair swapped | P1 665, P3 865, P6 865 |
| M11 | stacks: each swap made with the index before the odd one | P1 2292, P3 2492, P6 2492 |
| M12 | stacks: the odd index copied over the even one, not swapped | P1 2292, P2 2492, P3 2492, P6 2492 |
| M13 | counting: an even value's count never taken down | P1 1582, P2 1782, P6 1782 |
| M14 | counting: the first half of the indices given the even values | P1 2023, P3 2223, P6 2223 |
| M15 | counting: an even index written before its cursor finds a value | P1 2513, P2 2713, P5 3200, P6 2713 |

P1 and P6 kill all fifteen, P3 twelve, P2 eight, P5 three and P4 none.
P2 sees the mutants that lose or invent values and P3 those that
misplace them; between them they cover every mutant, as the statement's
two conditions should. P5 sees only the mutants that test a value as
well as its parity (M4 and M5, whose test changes when 2 is added) or
write a value the cursor has not checked (M15). P4 cannot see a mutant
at all: it asks only about answers that are already right, and every
arm here leaves a right answer as it is.

Seventeen other edits were tried and set aside. Three give another
answer the statement accepts, so are not mistakes: split writing the
odd values back reversed or rotated by one (only P4 saw those, since
the arm then changes its own answer when given it back), and sorted
swapping its first and last values after sorting, which no property
sees. Two stopped at runtime on an index out of bounds (counting with
each count set to 1, and with each count taken down by two). Three
failed exactly the same checks as a kept mutant (sorted's even value
repeated as M13, stacks noting the right indices rather than the wrong
ones as M7, and counting's last index never filled as M9). The other
nine were sound but beyond three an arm.

## Verification

Every arm prints the same output as `sort_array_by_parity_ii.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 1.6 to 2.2 s each and the
differential 20 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy compiler refuses every arm and the differential at
the first `*` on an element of a `Vec[i64]`'s `.iter()` ("unary '*'
requires 'ref T', ... found 'i64'"), legacy's older rule; under v2 the
element is a reference and the `*` is required. The bench program has no
such `*`, and the legacy build of it prints the same line as the others.
Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 20,000 values once, half even and half odd,
shuffled, and in each of 3,000 rounds copies them and runs the ★ arm on
the copy, reading one value of the result back into a checksum. Every
implementation prints `3000 rounds over 20000 values: checksum
456426821`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.20 to 0.25 s | 0.22 s |
| Rust (`rustc -O`) | 0.21 to 0.23 s | 0.22 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.18 to 0.23 s | 0.21 s |
| Go | 0.36 to 0.44 s | 0.41 s |
| Python | 5.2 s | |
| Kāra (`karac build --mir`) | 0.19 to 0.24 s | 0.20 s |
| Kāra (`karac build --legacy`) | 0.19 to 0.23 s | 0.20 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 24 times
C's.

v2 takes 0.95 times Rust's median time under overflow checks, 0.98
times legacy's and 0.91 times C's: the four are within their run to run
spread of each other. The work is the same branch on a random parity,
and under valgrind's cachegrind every one of them runs about 1.1
billion instructions and 0.6 billion branches and mispredicts about 30
million, 5% (v2 1.13 billion, 0.62 billion and 29.6 million; C 1.10
billion, 0.59 billion and 30.1 million).
