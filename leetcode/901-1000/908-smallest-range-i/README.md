# 908. Smallest Range I

You are given an integer array `nums` and an integer `k`.

In one operation, you can choose any index `i` where
`0 <= i < nums.length` and change `nums[i]` to `nums[i] + x` where `x`
is an integer from the range `[-k, k]`. You can apply this operation
**at most once** for each index `i`.

The **score** of `nums` is the difference between the maximum and
minimum elements in `nums`.

Return the minimum **score** of `nums` after applying the mentioned
operation at most once for each index in it.

```
nums = [1],      k = 0  ->  0
nums = [0,10],   k = 2  ->  6    (change nums to [2,8])
nums = [1,3,6],  k = 3  ->  0    (change nums to [4,4,4])
```

**Constraints:** `1 <= nums.length <= 10^4`, `0 <= nums[i] <= 10^4`
and `0 <= k <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `smallest_range_i.kara` ★ | the largest and smallest values: one pass finds both, and the score is what is left of the gap once each end moves k towards the other, `max(0, max - min - 2k)`. O(n) |
| `smallest_range_i_sort.kara` | the ends of a sorted copy, the same gap. O(n log n) |
| `smallest_range_i_intervals.kara` | where the reachable intervals meet: value `v` can become anything in `[v - k, v + k]`; if all the intervals share a point the score is 0, otherwise it is the gap between the highest left end and the lowest right end. O(n) |
| `smallest_range_i_search.kara` | a binary search on the score: a score `s` is possible when no value's lowest reach lies more than `s` above another's highest reach, which is monotone in `s`. O(n log(max - min)) |
| `smallest_range_i_toward.kara` | the moves done: every value moved up to k towards the point halfway between the smallest and largest, and the result scored. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and five
more (`[7,7,7]` with k = 0, `[0,10000]` with k = 0 and k = 10000, and
`[2,9,4,13,5]` with k = 2 and k = 5); for 300 random cases of up to
2,000 numbers below 10, 1,000 or 10,001, with k up to half of that, the
sum and a checksum of the scores; and two of LeetCode's largest, 10,000
numbers up to 10,000 with k = 0 and with k = 2500.
`smallest_range_i.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to apply the operation to every index tried (with
`x = 0` standing for leaving an index alone), each result scored, and
the least score kept. It checks 3,200 random cases: 3,000 of up to 4
numbers below 12 with k up to 2 against the statement (up to 625 ways
each), and 200 of up to 500 numbers below 10, 1,000 or 10,001, with k up
to half of that, against the other properties; 59,479 numbers in all.

| | property |
|---|---|
| P1 | the statement's least score, on the small cases |
| P2 | at least 0 and at least `max - min - 2k`, and at most `max - min` (every `x = 0`) |
| P3 | the same score with every value moved by the same random amount below 1,000 |
| P4 | the same score for the values reversed |
| P5 | twice the score with every value and k doubled |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 59479
numbers, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each end moving k between them, not 2k | P1 1294, P6 1482 |
| M2 | ★: a crossed gap scored below 0 | P1 766, P2 783, P6 783 |
| M3 | ★: the last value never read | P1 1144, P2 1146, P4 1060, P6 1146 |
| M4 | sort: a crossed gap scored as the whole gap | P1 343, P6 361 |
| M5 | sort: the copy never sorted | P1 1357, P2 1539, P4 1501, P6 1539 |
| M6 | sort: the gap measured from the middle value | P1 1737, P2 1919, P6 1919 |
| M7 | intervals: the left ends taken as right ends | P1 1439, P6 1627 |
| M8 | intervals: the right ends taken as left ends | P1 1439, P6 1627 |
| M9 | intervals: the gap scored one short | P1 1803, P2 1985, P5 1985, P6 1985 |
| M10 | search: a score possible only with room to spare | P1 1224, P5 1395, P6 1395 |
| M11 | search: a possible middle thrown away | P1 610, P2 687, P5 976, P6 687 |
| M12 | search: only half the gap searched | P1 1304, P2 1410, P5 787, P6 1410 |
| M13 | toward: low values carried past the middle | P1 127, P5 248, P6 210 |
| M14 | toward: high values moved 2k | P1 1096, P2 1266, P5 288, P6 1266 |
| M15 | toward: everything moved towards the smallest value | P1 1294, P6 1482 |

P1 and P6 kill all fifteen; P2 kills eight, P5 six, P4 two and P3
none. Every arm, mutated or not, uses the values only through their
differences, so moving them all by the same amount can never change an
answer. P4 sees only the two mutants that depend on where values sit:
M3 never reads the last one and M5 reads the ends of an unsorted copy.
M1 and M15 are the same function: moving everything towards the
smallest value lowers only the top by k, which leaves
`max(0, max - min - k)`. M7 and M8 are the same function too: either
way the two ends of the gap are both moved by k in the same direction,
so each answers `max - min` whatever k is.

One mutant was replaced. The first M9 started the intervals arm's
highest left end at 0 rather than at the first value's, and was
equivalent: the values are never negative, so it changes the highest
left end only when every `v - k` is below 0, and then every value is
below k, the gap is below 2k and the score is 0 either way.

## Verification

Every arm prints the same output as `smallest_range_i.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.4 to 2.7 s
each (the binary search the longest) and the differential 4.1 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy lanes split. The ★ and sort arms print the same
output under the legacy interpreter, the legacy JIT and both legacy
builds, with and without auto-par (the builds warn that `big` is moved
into the first call and used again, under legacy's older rule that a
bare parameter takes ownership). Every legacy lane refuses the
intervals, search and toward arms and the differential: `*v` on an
element of `.iter()` is rejected, because legacy's iterator gives the
value itself. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program uses the ★ arm on 500,000 numbers up to 10,000, built
once. Each round scores them with k = `round * 37 % 5001`, folds the
score into a checksum and changes one number; 500 rounds. Every
implementation prints `500 rounds over 500000 numbers: scores summing
to 2639874, checksum 47671605`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.14 to 0.16 s | 0.16 s |
| Rust (`rustc -O`) | 0.14 to 0.21 s | 0.15 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.14 to 0.17 s | 0.15 s |
| Go | 0.23 to 0.33 s | 0.25 s |
| Python | 18.4 s | |
| Kāra (`karac build --mir`) | 0.12 to 0.17 s | 0.13 s |
| Kāra (legacy `karac build`) | 0.12 to 0.16 s | 0.14 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does.

The compiled programs finish in a fraction of a second while Python
takes 18 s; the bench is sized for Python, and the compiled times are
short enough that process start and building the numbers are a large
part of them. v2 takes 0.85 times Rust's median time under overflow
checks and 0.83 times C's. Under valgrind's cachegrind v2 runs 0.35
billion instructions and 9 million branches, and legacy about the same,
against 2.07 billion instructions and 0.44 billion branches for both C
and Rust with overflow checks: about 1.4 instructions a number for the
two Kāra builds and 8 for C and Rust, which fits the Kāra builds
scanning several numbers at once with vector instructions and C and
Rust one at a time. That reading of the counts was not checked against
the generated code. The comparison with C and Rust waits until after
M4.
