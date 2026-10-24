# 978. Longest Turbulent Subarray

Given an integer array `arr`, return the length of a maximum size
turbulent subarray of `arr`. A subarray is turbulent if the comparison
sign flips between each adjacent pair of elements in the subarray.

More formally, a subarray `[arr[i], arr[i + 1], ..., arr[j]]` of `arr`
is said to be turbulent if and only if:

- For `i <= k < j`: `arr[k] > arr[k + 1]` when `k` is odd, and
  `arr[k] < arr[k + 1]` when `k` is even.
- Or, for `i <= k < j`: `arr[k] > arr[k + 1]` when `k` is even, and
  `arr[k] < arr[k + 1]` when `k` is odd.

```
arr = [9,4,2,10,7,8,8,1,9]  ->  5
arr = [4,8,12,16]           ->  2
arr = [100]                 ->  1
```

**Constraints:** `1 <= arr.length <= 4 * 10^4`; `0 <= arr[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `max_turbulence_size.kara` ★ | two running lengths: up is the longest turbulent subarray ending here whose last step rises, down the same for a falling last step. A rise makes up = down + 1 and resets down to 1, a fall the mirror image, and an equal pair resets both. O(n) |
| `max_turbulence_size_window.kara` | a sliding window: each pair of neighbours compares to -1, 0 or 1; an equal pair moves the window's anchor to i, and a step in the same direction as the one before moves it to i - 1, since only the last pair survives. O(n) |
| `max_turbulence_size_signs.kara` | runs of alternating signs: the signs of the n - 1 differences are written out, and a turbulent subarray of length k is a run of k - 1 signs, none zero, each the opposite of the one before; the longest run plus one. O(n) |
| `max_turbulence_size_brute.kara` | extending from each start: from every start the subarray grows while each new step is strict and turns the other way. O(n^2) in the worst case, about O(n) on random input |
| `max_turbulence_size_split.kara` | divide and conquer: the longest subarray of [lo, hi) is in one half or crosses the middle; one that crosses holds the strict pair (mid - 1, mid) and reaches left and right while the steps keep alternating. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines. The first ten are LeetCode's three
examples and seven more: three equal values (1); a single rise (2); a
zigzag of six (6); LeetCode's smallest and largest values alternating
(4); [1, 2, 1, 1, 2, 1, 2], where an equal pair splits two runs (4);
[3, 3, 1, 2], where the run starts after the equal pair (3); and
[5, 4, 3, 4, 3, 4, 4, 5, 4], where a run starts one step after a
repeated direction (5). The last three are totals and checksums over
random arrays: 300 of up to 12 values below 3 (lengths 936), 3,000 of
up to 60 values below 10 (20,387), and 4 of 40,000 values up to 10^9
(96). `max_turbulence_size.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray, kept when one of the two parity rules holds
at every k in it, the longest kept. It checks 3,200 arrays: 3,000 of 1
to 30 values against the statement, four in five random values below
2, 3, 10 or 10^9 and every fifth a zigzag that turns at every step
except about one in ten, which repeats the value or keeps the
direction; and 200 of 300 values against the other properties, every
other one a zigzag. Random values rarely make a run longer than a few
steps; the zigzags make long runs with breaks at random places.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 arrays |
| P2 | the array reversed gives the same answer |
| P3 | only the comparisons between neighbours matter: every value mapped to 3x + 7, which keeps each one, or to 2 * 10^9 - x, which flips each one, gives the same answer |
| P4 | an array cut in two at a random place: each piece's answer is no longer than the whole, which is no longer than the two together |
| P5 | a value repeated in place ends every run through it, so the answer becomes the longer of the two sides, each holding one copy |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 arrays of 106148 values: lengths total 23317, checksum
999794474, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (8.5 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal pair keeps the falling run | P1 795, P3 1232, P5 535, P6 864 |
| M2 | ★: a rise extends the rising run | P1 2280, P2 1158, P3 1330, P6 2479 |
| M3 | ★: only rising runs counted | P1 1322, P2 1365, P3 2734, P4 187, P6 1424 |
| M4 | window: an equal pair counted in the window | P1 35, P5 121, P6 35 |
| M5 | window: a repeated direction keeps one pair too many | P1 2091, P2 879, P4 18, P5 534, P6 2287 |
| M6 | window: the window counted one short | P1 2844, P4 288, P6 3044 |
| M7 | signs: one extra counted when nothing alternates | P1 156, P6 156 |
| M8 | signs: each turn counted twice | P1 2642, P4 462, P6 2842 |
| M9 | signs: every sign taken as positive | P1 2642, P6 2842 |
| M10 | brute: an equal step allowed | P1 1095, P2 1144, P3 1144, P5 772, P6 1143 |
| M11 | brute: the direction required to stay the same | P1 2481, P6 2681 |
| M12 | brute: the first step never checked | P1 769, P2 727, P3 1062, P5 319, P6 794 |
| M13 | split: an equal middle pair crossed | P1 313, P2 406, P3 376, P4 106, P5 567, P6 315 |
| M14 | split: the reach left stops one short | P1 834, P2 955, P4 283, P5 748, P6 849 |
| M15 | split: the reach right stops one short | P1 879, P2 929, P4 315, P5 727, P6 887 |

P1 and P6 kill all fifteen, P2 and P5 eight each, P4 seven (M3, M5,
M6, M8, M13, M14, M15) and P3 six (M1, M2, M3, M10, M12, M13). P3's
flip turns every rise into a fall, so it sees an edit that treats the
two directions differently (M1 to M3) or that mishandles equal pairs,
which the flip leaves equal while their neighbours change direction.
P4 sees M6 and M8, among others: when the longest run is split by the
cut so that the pieces' answers are its two parts, its true length k
is their sum, and an answer of k - 1 (counting one short) or 2k - 1
(each turn twice) for each of the three breaks that sum. M7 and M9
are seen only by the statement and agreement: the first changes only
arrays with no strict step, the second answers 2 for every array with
one, and neither breaks a relation between arrays.

Ten other edits were tried and set aside. Two failed exactly the same
checks as a kept one: signs starting a run at an equal pair, as M4,
and brute counting the run one short, as M6. Eight were sound but
beyond three an arm: ★ counting a lone value as 0 and keeping the
falling run on a rise; window comparing an equal pair as a rise and
never comparing the first two steps; signs never reading the first
sign; brute never checking the second step; split finding nothing
across the middle and allowing an equal step going left.

## Verification

Every arm prints the same output as `max_turbulence_size.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.58 s (window) to 1.06 s (split), and the differential
8.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program makes 20
arrays of 40,000 random values below 100 once. In each of 150 rounds
it runs the arm on every array, each round starting from a different
one, and folds every length into a checksum. Every implementation
prints `150 rounds over 20 arrays of 40000 values: lengths total
70650, checksum 187922834`. Neighbouring random values rise or fall
about evenly, so which branch the loop takes is close to a coin flip.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.143 to 0.239 s | 0.159 s |
| Rust (`rustc -O`) | 0.149 to 0.170 s | 0.158 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.555 to 0.692 s | 0.591 s |
| Go | 0.525 to 0.620 s | 0.571 s |
| Python | 12.6 s | |
| Kāra (`karac build --mir`) | 0.582 to 0.639 s | 0.611 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 21 times
Kāra's.

v2 took 1.03 times Rust's median time under overflow checks and 3.84
times C's. This is the equal-safety tie that BENCHMARKS.md describes.
Under valgrind's cachegrind C ran 2,290 million instructions and 120
million branches, about one per element, with 9 thousand
mispredicted: the coin-flip choice between a rise and a fall leaves
no branch behind, so clang must have compiled it to conditional moves
(inferred from the counts; the assembly was not read). Plain Rust's
time matches C's. Rust with overflow checks ran 2,107 million
instructions and 420 million branches with 49.4 million mispredicted,
and v2 2,229 million, 421 million and 49.4 million: the same branches
and the same mispredictions to within a few. The two Rust builds
differ only in overflow checks, so the checks on `down + 1` and
`up + 1` cost Rust 0.43 s here, which is 9 ns for each of the 49
million mispredictions; that the checks cost by blocking the
conditional moves is inferred, not traced.
