# 477. Total Hamming Distance

The Hamming distance between two integers is the number of positions
at which the corresponding bits are different.

Given an integer array `nums`, return the sum of Hamming distances
between all the pairs of the integers in `nums`.

```
nums = [4,14,2]  ->  6
nums = [4,14,4]  ->  4
```

**Constraints:** `1 <= nums.length <= 10^4`; `0 <= nums[i] <= 10^9`;
the answer for the given input will fit in a 32-bit integer.

## Approaches

Every arm is `fn total_hamming_distance(nums: Vec[i64]) -> i64`, and
borrows the list. Every number is below 2^30.

| file | mechanism |
|---|---|
| `total_hamming_distance.kara` ★ | one bit at a time: if k of the n numbers have bit b set, bit b adds k × (n - k), the pairs with one on each side. O(30 × n) |
| `total_hamming_distance_pairs.kara` | every pair, the `count_ones()` of their exclusive or. O(n²) |
| `total_hamming_distance_online.kara` | for each bit, how many of the numbers so far have it; a new number's distance to all of them comes from those counts alone |
| `total_hamming_distance_columns.kara` | each number halved down to 0, its remainders added to a count per column that grows as wide as the widest number; then k × (n - k) per column, with `iter().map(..).sum()` |
| `differential.kara` | the four arms on 1,500 random lists, five properties |

Every arm prints the same 8 lines: the two LeetCode examples, one
number, three equal numbers, 0 and 10^9, 0 to 15 (each bit is set in
half of them), `2^30 - 1` and 0 twice each, and for 300 random lists
(1 to 40 numbers from 0 to 10^9, or from 0 to 15 for one list in
three, possibly repeated) the sum of the totals and a checksum of them
in order. `total_hamming_distance.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random lists of 1 to 12 numbers from 0 to 10^9 (from 0 to 15 for
one list in three), each with a second random list.

| | property |
|---|---|
| P1 | the total is the sum over every pair of the places where the two differ, counted by halving both |
| P2 | the list rotated by a random amount and reversed has the same total |
| P3 | every number exclusive-ored with the same random mask below 2^30 has the same total |
| P4 | the list followed by a copy of itself has four times the total |
| P5 | the list followed by the second list has both totals plus the distance of every number in one to every number in the other, counted by halving |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, in 3.7 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the top bit (2^29) is never looked at | P1 808, P5 1248 |
| M2 | ★: a bit adds `ones × (n - 1 - ones)` | P1 1497, P3 1433, P4 1497 |
| M3 | pairs: neighbours in the list are never paired | P1 1375, P2 869, P4 1375, P5 1490 |
| M4 | pairs: the ones of the or, not of the exclusive or | P1 1364, P3 1317, P4 1497, P5 1489 |
| M5 | online: a set bit counts the earlier numbers that have it | P1 1310, P2 1250, P3 1344, P4 1482, P5 1449 |
| M6 | online: bit 0 is never looked at | P1 1256, P5 1482 |
| M7 | columns: a column counts every number that reaches it | P1 1358, P3 1213, P5 1496 |
| M8 | columns: the highest set bit is never counted | P1 1238, P3 1102, P5 1472 |

P1 and P5 compare an arm with distances counted independently; P2, P3
and P4 compare it only with itself. M1 and M6 drop one bit the same way
from every list, so they pass P2 to P4: the dropped bit is missing on
both sides. M2 takes every number's ones off the total, and P5's two
lists lose exactly their own share, so P5 is the one property blind to
it. P2 sees only M3 and M5, the two that depend on the order of the
list. P4 cannot see M7 or M8, whose counts double with the list, as
the right ones do; P3 sees them, since a mask changes which column a
number reaches.

## Verification

All four arms print the same output as `total_hamming_distance.py`
under `karac __mir-run` (the v2 MIR interpreter) and
`karac __mir-llvm-run`, and `karac check` passes on every file, the
bench program included. The differential prints `30000 checks, 0
failures` on both. The four arms and the differential also run clean
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer):
output identical, no error, no leak.

The frozen legacy backends get the random lists wrong, as on kata 475.
Under `karac run --interp`, LLJIT and legacy `karac build`, every arm
prints the seven fixed cases right and then a different last line
(`distances add up to 833647, checksum 452460920`): legacy calls
`next_random` twice for the bound of `for _ in 0..1 + next_random(mut
seed) % 40 { .. }`, so the lists it draws are not the ones MIR and
Python draw. The differential checks properties rather than a fixed
output, so it prints `0 failures` on the legacy interpreter and a
legacy build all the same. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10,000 numbers from 0 to
10^9 (the problem's most) once, then runs 5,000 rounds, each replacing
one number with a new random one and taking the total again. Every
implementation prints `5000 rounds on 10000 numbers: distances add up
to 3740499580543, checksum 180251056`, the Kāra program under
`karac __mir-run` included (in 250 s).

Every mirror runs the same 30 passes over the numbers per round, one
per bit. The overflow-checked Rust build takes about twice as long as
plain `rustc -O`; the likely cause is that the checks keep its count
loop from vectorizing, but that is inferred from the timings, not read
from the assembly. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.33 to 0.46 s |
| Rust (`rustc -O`) | 0.36 to 0.44 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.77 to 0.82 s |
| Go | 1.10 to 1.46 s |
| Python | 67.7 to 70.8 s |
| Kāra (`karac build`) | 0.73 to 0.81 s |
| Kāra (`karac build --mir`) | 1.07 to 1.17 s |

The legacy `karac build` builds and runs this program correctly (its
loops have constant bounds), so `bench.sh` is the
`scripts/new-bench.sh` output unchanged and times that build. The
`--mir` row is the v2 compiled backend, timed for comparison. Both Kāra
rows are timed at kara `b0b1557b39`. Under `karac __mir-llvm-run` the
program prints the same line in 6.0 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings.
