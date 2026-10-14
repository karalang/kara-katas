# 624. Maximum Distance in Arrays

Given `m` arrays, each sorted in ascending order, pick two integers from
two different arrays, one from each, and return the largest distance `|a
- b|` between such a pair.

```
arrays = [[1,2,3],[4,5],[1,2,3]]  ->  4    (1 from the first, 5 from the second)
arrays = [[1],[1]]                ->  0
```

**Constraints:** 2 to 100,000 arrays; each of 1 to 500 values, sorted,
from -10,000 to 10,000; at most 100,000 values in all.

## Approaches

Every arm is `fn max_distance(arrays: Vec[Vec[i64]]) -> i64`. Since each
array is sorted, the farthest pair takes the last value of one array and
the first value of another.

| file | mechanism |
|---|---|
| `max_distance.kara` ★ | one pass keeping the smallest first value and the largest last value among the arrays before this one, each array's last value tried against that smallest and that largest against its first value; O(arrays) |
| `max_distance_pairs.kara` | every ordered pair of two different arrays, the last value of one less the first value of the other; O(arrays²) |
| `max_distance_toptwo.kara` | the two smallest first values and the two largest last values with their arrays, the extremes taken when they come from different arrays and otherwise the better of the two pairs with a runner-up; O(arrays) |
| `max_distance_sorted.kara` | the first values sorted up and the last values sorted down, each with its array, and the four pairs of the top two of each tried, keeping the farthest apart that uses two arrays; O(arrays log arrays) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: the two LeetCode examples; six more
(two arrays the other way round, the smallest and the largest value in
one array with the runner-up on either side deciding, negative values
only, single values, and every array the same); a total and checksum
over 300 random cases of 2 to 20 arrays of 1 to 10 values from
-10,000 to 10,000; the answer for 1,000 arrays of up to 100 values; and
the answer for 2,000 arrays of up to 50 values where one array holds
both the smallest and the largest value. `max_distance.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the largest `|a - b|` over every value `a` of one array and every value
`b` of another, not only the ends. Each of 1,000 random cases is 2 to
6 arrays of 1 to 5 values from -20 to 20, so that the smallest and the
largest value often fall in one array.

| | property |
|---|---|
| P1 | the distance is the definition's |
| P2 | the arrays in reverse order give the same distance |
| P3 | a constant from -50 to 50 added to every value changes nothing |
| P4 | every value negated, each array reversed to stay sorted, changes nothing |
| P5 | a copy of one array added gives the larger of the old distance and that array's own spread, its last value less its first |

It prints `1000 cases (11915 values), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only this array's last value against the smallest first value | P1 441, P2 930, P4 930, P5 158 |
| M2 | ★: the second array skipped | P1 540, P2 381, P5 176 |
| M3 | pairs: an array paired with itself | P1 215 |
| M4 | pairs: the last value less the other array's last value | P1 850, P4 954, P5 456 |
| M5 | toptwo: the two ends taken even when they share an array | P1 215 |
| M6 | toptwo: only the runner-up first value tried when the ends share an array | P1 117, P2 41, P4 232 |
| M7 | sorted: only the largest last value tried | P1 117, P2 41, P4 232 |
| M8 | sorted: the pairs from one array kept, not from two | P1 915, P2 73, P5 361 |
| E1 | ★: the two candidates taken in the other order | 0 |
| E2 | pairs: the test as `j != i` | 0 |
| E3 | toptwo: a tied first value taking first place | 0 |
| E4 | sorted: the best started at 0 | 0 |

P1 kills all eight. M3 and M5 both let the farthest pair come from one
array, and M6 and M7 both pair the largest last value only with the
runner-up first value when the two extremes share an array, so each pair
fails the same counts. P3 kills nothing: every mutant still reads only
differences between values, which a shift leaves alone. P2 and P4 see
the mutants whose answer depends on which array comes first or which end
is which, as M1's one-sided check and M4's last-less-last do. P5 sees
M1, M2, M4 and M8, whose answers do not change by exactly a copied
array's spread. M3 and M5 are seen by the definition alone: they already
count an array's own spread, so a copy of it changes nothing for them
either.

## Verification

Every arm prints the same output as `max_distance.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `1aaf2d259c` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends refuse every file at type checking. They
still hold the old rule that an argument which is already a `mut ref`,
as `seed` is inside `random_arrays`, drops its call-site `mut` marker,
and they type the items of a `Vec`'s `iter()` by value, so the
differential's `*a - *b` is an error. Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 inputs of 20,000 arrays of
1 to 9 values, about 100,000 values each, the problem's most, each with
values within a random bound from 1,000 to 10,000, once; then
2,000 times answers one of them, picked by the round, adding up the
answers and putting each into a checksum. Every implementation prints
`20 inputs, 2000 rounds: total 19217200, checksum 124531026`, the Kāra
program under `karac __mir-run` included (in 66 s).

Each implementation walks the arrays once reading each one's first and
last values: Rust over a `Vec<Vec<i64>>`, Go over a `[][]int64`, C over
an array of structs holding a pointer and a length, and Python over a
list of lists. Spot timings on a shared 4-core container, three runs
each (two for Python; `bench.sh` timings need a quiet machine), each
including making the inputs:

| | time |
|---|---|
| C (`clang -O3`) | 0.20 to 0.22 s |
| Rust (`rustc -O`) | 0.23 to 0.25 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.24 to 0.27 s |
| Go | 0.23 to 0.26 s |
| Python | 20.1 to 20.5 s |
| Kāra (`karac build --mir`) | 0.23 to 0.26 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the `mut`
markers and the input passed by value from `all[...]` ("cannot move out
of an index expression"); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.1 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

The compiled rows are within a few hundredths of a second of each other.
Making the inputs, 400,000 arrays allocated and sorted, is about a third
of each run: with no rounds, the C program takes 0.07 to 0.09 s and the
Kāra program 0.07 to 0.10 s. The rest is 40 million reads of a first and
a last value. The program is not profiled further.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
