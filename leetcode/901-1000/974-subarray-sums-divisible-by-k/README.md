# 974. Subarray Sums Divisible by K

Given an integer array `nums` and an integer `k`, return the number of
non-empty subarrays that have a sum divisible by `k`.

A subarray is a contiguous part of an array.

```
nums = [4,5,0,-2,-3,1], k = 5  ->  7
nums = [5],             k = 9  ->  0
```

In the first example the seven subarrays are `[4, 5, 0, -2, -3, 1]`,
`[5]`, `[5, 0]`, `[5, 0, -2, -3]`, `[0]`, `[0, -2, -3]` and
`[-2, -3]`.

**Constraints:** `1 <= nums.length <= 3 * 10^4`;
`-10^4 <= nums[i] <= 10^4`; `2 <= k <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `subarrays_div_by_k.kara` ★ | counts of prefix remainders: a subarray's sum is the difference of two prefix sums, divisible by k exactly when the two leave the same remainder; walking once, each prefix sum pairs with every earlier one of its remainder, kept in a table of k counts that starts with the empty prefix. The remainder is lifted into 0..k, since a negative sum leaves a negative one. O(n + k) |
| `subarrays_div_by_k_map.kara` | the same pairing counted in a `Map` holding only the remainders that occur, with the remainder kept running, x's own remainder added each step, rather than taken from the whole sum. O(n) expected |
| `subarrays_div_by_k_pairs.kara` | choose two: every prefix remainder is counted first, the empty prefix's 0 included, and c prefixes sharing a remainder give c (c - 1) / 2 subarrays. O(n + k) |
| `subarrays_div_by_k_sorted.kara` | sorted remainders, no table: the n + 1 prefix remainders are sorted so that equal ones sit together, and each run of length c gives c (c - 1) / 2. O(n log n), independent of k |
| `subarrays_div_by_k_halves.kara` | divide and conquer: a subarray lies in the left half, in the right half, or crosses the middle as a suffix of the left joined to a prefix of the right. The suffix remainders are counted in a table, each prefix remainder b is matched with the suffixes of remainder (k - b) % k, and the suffixes are walked again to empty the table, so one table serves every call. O(n log n + k) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines. The first ten are LeetCode's two
examples and eight more: three zeros with k = 2; [-1, 2, 9] with k = 2;
[7, -7] with k = 7; three -5s with k = 5, where every prefix sum is
negative; [-3, 1, -1, 3] with k = 4; LeetCode's largest numbers with
the largest k; [1, 2, 3] with a k beyond every sum; and [2, -2, 2, -2]
with k = 3, where only the zero sums count. The last three are totals
and checksums over random cases: 300 arrays of up to 12 numbers from
-10 to 10 with k up to 6 (2,525 subarrays), 3,000 of up to 60 numbers
over LeetCode's whole range with k up to 50 (147,630), and 4 of 30,000
numbers with k up to 10^4 (687,464). `subarrays_div_by_k.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray summed, extending each start one number at a
time, and its sum tested. It checks 3,200 cases: 3,000 arrays of 1 to
30 numbers within 3, 10, 100 or 10^4 of zero, each with k up to 3, 10,
100 or 10^4, against the statement, and 200 of 300 numbers over
LeetCode's whole range with k up to 10^4 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 cases |
| P2 | the array reversed gives the same count |
| P3 | every number negated gives the same count |
| P4 | a 0 put in front adds one subarray for itself and one for each nonempty prefix whose sum is divisible by k |
| P5 | only remainders matter: every number replaced by its remainder in 0..k, or one number moved by k within LeetCode's range, gives the same count |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 105959 numbers: 96885 subarrays, checksum
253204366, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (18.5 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-eight edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty prefix not counted | P1 1841, P2 1384, P4 3200, P6 1859 |
| M2 | ★: a negative remainder folded by its size | P1 959, P2 1444, P5 1173, P6 1027 |
| M3 | ★: each prefix paired with itself | P1 3000, P4 3200, P6 3200 |
| M4 | map: the remainder of x alone | P1 2113, P4 1809, P6 2296 |
| M5 | map: a negative remainder not lifted | P1 1307, P2 1369, P5 1603, P6 1497 |
| M6 | map: a count reset to 1 | P1 1880, P4 1859, P6 1950 |
| M7 | pairs: c^2 / 2 pairs | P1 2427, P4 2136, P6 2627 |
| M8 | pairs: the empty prefix counted twice | P1 3000, P2 1384, P4 3200, P6 3200 |
| M9 | pairs: a remainder only marked as seen | P1 2427, P4 3200, P6 2627 |
| M10 | sorted: the last run dropped | P1 1570, P2 1236, P3 1211, P4 28, P6 1588 |
| M11 | sorted: never sorted | P1 2266, P4 1726, P6 2466 |
| M12 | sorted: neighbouring remainders run together | P1 2510, P2 822, P3 953, P4 1864, P6 2710 |
| M13 | halves: no single number counted | P1 1957, P4 3200, P6 1984 |
| M14 | halves: a prefix matched with its own remainder | P1 1808, P2 1558, P4 1718, P6 1989 |
| M15 | halves: the table never emptied | P1 2428, P2 2450, P4 2587, P6 2628 |

P1 and P6 kill all fifteen, P4 thirteen (all but M2 and M5), P2 eight
(M1, M2, M5, M8, M10, M12, M14, M15), P3 two (M10, M12) and P5 two (M2,
M5). Negating every number turns each remainder r into (k - r) % k, one
for one, so an edit that treats every remainder alike counts the same
before and after; only the sorted arm's M10 and M12, whose answers
depend on which remainders are largest or next to each other, see it.
M2 and M5 mishandle negative sums in a way that negating every number
leaves alone, and P5, which makes every number non-negative, sees them.

Thirteen other edits were tried and set aside. Seven failed exactly the
same checks as a kept one: map, pairs and sorted each leaving out the
empty prefix, and sorted's first run one short, as M1; pairs pairing
each prefix with itself, as M3; pairs folding a negative remainder by
its size, as M2; and pairs counting c / 2 pairs, as M6, since c / 2,
c - 1 and c (c - 1) / 2 differ only once a remainder occurs three
times. Five were sound but beyond three an arm: ★ dropping the running
sum and allowing at most one pair per prefix; map counting an unseen
remainder once; halves skipping the right half's first number and
counting the left half's prefixes for its suffixes. One was equivalent:
pairs adding each number's remainder to the sum instead of the number,
which leaves every prefix's remainder as it was.

## Verification

Every arm prints the same output as `subarrays_div_by_k.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.46 s (pairs) to 5.2 s (halves), and the differential 18.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 20 arrays of 30,000 random numbers over
LeetCode's whole range once, each with a random k up to 10^4. In each
of 200 rounds it runs the ★ arm on every array, each round starting
from a different one, and folds every count into a checksum. Every
implementation prints `200 rounds over 20 arrays of 30000 numbers:
711268600 subarrays, checksum 627668777`. Each call allocates its table
of k counts, as the arm does.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.704 to 0.742 s | 0.712 s |
| Rust (`rustc -O`) | 0.687 to 0.746 s | 0.704 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.692 to 0.733 s | 0.710 s |
| Go | 0.882 to 0.953 s | 0.925 s |
| Python | 14.6 s | |
| Kāra (`karac build --mir`) | 0.683 to 0.799 s | 0.724 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 21 times
C's.

v2 took 1.02 times Rust's median time under overflow checks and 1.02
times C's. Under valgrind's cachegrind v2 ran 4,002 million
instructions and 1,110 million branches, Rust with overflow checks
3,638 million and 989 million, and C 3,157 million and 509 million;
each mispredicted fewer than 36,000. The instruction counts differ by a
quarter and the times by 3%; each number costs two 64-bit remainders,
which all of them pay alike, and that these set the pace is inferred,
not measured.
