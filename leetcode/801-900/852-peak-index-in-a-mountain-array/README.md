# 852. Peak Index in a Mountain Array

An array `arr` is a mountain: its values strictly rise to a peak and
strictly fall after it, and the peak is neither the first index nor the
last. Return the peak's index, in O(log n) time.

```
arr = [0,1,0]     ->  1
arr = [0,2,1,0]   ->  1
arr = [0,10,5,2]  ->  1
```

**Constraints:** `3 <= arr.length <= 10^5`, `0 <= arr[i] <= 10^6`, and
`arr` is guaranteed to be a mountain.

## Approaches

| file | mechanism |
|---|---|
| `peak_index_in_mountain_array.kara` ★ | binary search on the slope: left of the peak each value is smaller than the next and from the peak on each is larger, so whether `arr[mid] < arr[mid + 1]` says which side of the peak `mid` is on; halve the range around the peak until it holds one index. O(log n) time |
| `peak_index_in_mountain_array_walk.kara` | the first step down: the peak is the first value larger than the one after it, found with `position` over the indices. O(n) time |
| `peak_index_in_mountain_array_ternary.kara` | ternary search: of two probes `m1 < m2` a rise from `m1` to `m2` puts the peak right of `m1`, and otherwise the peak is left of `m2`, so each step drops about a third of the range, and a scan settles the last three indices. O(log n) time |
| `peak_index_in_mountain_array_largest.kara` | the largest value: the peak is the mountain's unique largest value, the index found with `max_by_key`. O(n) time |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 15 lines: LeetCode's three examples; seven
more (a peak at the second index, a rise to the second last, a fall from
the second, ten values with uneven steps, a peak of 10^6 between the
lowest values, a symmetric mountain, and a rise in steps of one that
drops below its start at the end); three mountains of LeetCode's most
values, 10^5, with the peak at the second last index, at the second, and
in the middle; a random mountain of 10^5 values; and 600 random
mountains of 3 to 42 values, with the sum of their peaks and a checksum.
`peak_index_in_mountain_array.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the peak is the `i` for which `arr[0] < ... < arr[i]` and
`arr[i] > ... > arr[n - 1]`, checked for every `i` in turn. Its 1,600
cases of 3 to 32 values come in four kinds of 400: steps of 1 to 3
around a peak anywhere, next to an end, or in the middle, and steps of 1
around a peak anywhere, so that the two slopes often share values. Each
mountain is moved up so that its lowest value is 0. Their peaks sum to
13,602.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the mountain reversed puts the peak at `n - 1` minus the answer |
| P3 | every value raised by the same amount gives the same peak |
| P4 | a lower value added in front moves the peak one index right |
| P5 | a lower value added behind leaves the peak where it is |

It prints `1600 cases, peaks sum to 13602, 32000 checks over 4 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the range ending two short of the last index | P1 354, P2 633, P5 354 |
| M2 | ★: the slope read the wrong way | P1 1600, P2 199, P4 950, P5 978 |
| M3 | ★: the midpoint dropped when the slope falls | P1 800, P2 1289, P4 727, P5 717 |
| M4 | walk: the first step up taken for the peak | P1 1600, P2 1600, P4 1600 |
| M5 | walk: the index after the step down | P1 1600, P2 1600 |
| M6 | walk: the walk starting at the second index | P1 1600, P2 1600 |
| M7 | ternary: the rise ruling out up to the second probe | P1 425, P2 687, P4 431, P5 429 |
| M8 | ternary: the last index left out of the final scan | P1 588, P2 1069, P4 537, P5 937 |
| M9 | ternary: the fall ruling out down to the first probe | P1 527, P2 833, P4 525, P5 481 |
| M10 | largest: the smallest value taken | P1 1600, P2 86, P4 1600, P5 1600 |
| M11 | largest: only the first half looked at | P1 622, P2 1131, P4 401, P5 350 |
| M12 | largest: values weighed two less for each index right | P1 1106, P2 1404, P4 379 |

P1 kills all twelve and P2 does too: every edit favours one side of the
mountain, and reversing it moves the peak to the other. P3 kills nothing
and could not, since every arm only compares values. P4 and P5 see the
edits whose error depends on where the peak lies, and miss M5 and M6,
which are off by the same one index wherever it is. M12 first read
"values weighed one less for each index right", `arr[i] - i`, which is
an equivalent mutant: the values rise by at least one a step, so
`arr[i] - i` never falls before the peak, and `max_by_key` keeps the
last of equal keys, the peak; it was replaced by two less a step.

## Verification

Every arm prints the same output as `peak_index_in_mountain_array.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its lines under all three. `karac
check` passes all four arms, the differential and the bench program. The
release and debug builds are both at kara `b8bf6e5772`, and the runtime
archives are current with them. Under `karac __mir-run` the arms take
0.8 to 1.9 s and the differential 1.1 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run the ★, walking and ternary arms through
`karac run`, `karac build` and a `KARAC_AUTO_PAR=1` build with the same
output. `karac run --interp` prints every line the same but the last,
`600 random mountains: peaks sum to 6436, checksum 178526702` where the
others print 6669 and 923887475: the harness passes `mut seed` to
`mountain` and calls `next_random(mut seed)` for the step in the same
argument list, which v2's two-phase borrows evaluate in order, as Python
does, and the legacy interpreter evidently does not (not traced). Legacy
has no `max_by_key`, so it refuses the largest-value arm and the
differential, and it refuses the bench program as moving a mountain out
of an index, which v2's borrowing parameters do not do. Legacy is
frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
mountains once, each of LeetCode's most values, 10^5: mountain `g` rises
and falls by steps of 1 to `1 + g % 10` around a random peak and is
moved up so that its lowest value is 0. Each of 30,000,000 rounds asks
the next mountain. Every implementation prints `30000000 rounds of 64
mountains: peaks sum to 1399037343750, checksum 482933583`, the Kāra
program under `karac __mir-run` included, in 194 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.67 to 0.97 s |
| Rust (`rustc -O`) | 0.73 to 1.01 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.89 to 1.15 s |
| Go | 0.96 to 1.44 s |
| Python | 51.4 to 52.2 s |
| Kāra (`karac build --mir`) | 1.11 to 1.42 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.17 s, against Rust's
0.84 (0.95 under overflow checks), C's 0.75 and Go's 0.97: 1.23 times
Rust's time under overflow checks, 1.56 times C's and 1.21 times Go's.
All three compiled programs mispredict about 285 million branches, nine
or ten for each search of 17 halvings, since each halving's direction
depends on the mountain. Under valgrind's cachegrind v2 runs the most
instructions, 12.07 billion against C's 6.67 billion and Rust's 8.43
billion, and the most branches, 2.72 billion against 1.04 and 2.12
billion; most likely the extra work is the bounds checks on `arr[mid]`
and `arr[mid + 1]`, which Rust keeps too (not traced). Built for
`x86-64-v3`, the target `karac build` uses, C takes 0.67 to 0.77 s and
Rust with overflow checks 0.84 to 1.08 s, against v2's 1.09 to 1.23 s in
the same five interleaved runs. Python takes 52 s, about 70 times C's
time. The comparison with C and Rust waits until after M4.
