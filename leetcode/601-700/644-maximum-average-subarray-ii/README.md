# 644. Maximum Average Subarray II

Given an array `nums` of `n` integers and a width `k`, find a contiguous
subarray of `k` or more values with the largest average, and return that
average. Answers within 10^-5 are accepted.

```
nums = [1,12,-5,-6,50,3], k = 4  ->  12.75000    (12 - 5 - 6 + 50) / 4
nums = [5], k = 1                ->  5.00000
```

**Constraints:** `k` from 1 to `n`, `n` up to 10,000; every value from
-10,000 to 10,000.

## Approaches

Every arm is `fn find_max_average(nums: Vec[i64], k: i64) -> f64`. Each
finds a best subarray, divides its integer sum by its length once, and
returns that; two subarrays with the same average give the same
`f64`, since a division of two integers rounds the exact quotient, so
the four agree bit for bit.

| file | mechanism |
|---|---|
| `max_average_ii.kara` ★ | binary search on the average: some subarray of `k` or more values averages at least `m` when its sum less `m` times its length is 0 or more, which one pass over prefix sums answers by keeping the best start; 100 halvings of the range of the values, then the exact average of the subarray the last successful pass found; O(n log range) |
| `max_average_ii_pairs.kara` | every pair of ends at least `k` apart, averages compared as fractions by cross-multiplying in integers; O(n^2) |
| `max_average_ii_hull.kara` | prefix sums as points, an average as the slope between two of them; the lower convex hull of the allowed starts in a `VecDeque`, the front coming off while the next point gives a line at least as steep; O(n) |
| `max_average_ii_short.kara` | only lengths `k` to `2k - 1`: a longer subarray splits into two of `k` or more, one averaging at least as much as the whole; O(nk) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: the two LeetCode examples; seven
more (the best `k` values found in two places; the whole array as the
only choice; every value equal; every value negative; one best average
reached by 4 values and by 8; a best subarray of 8 values when every one
of exactly 7 is worse; and the extremes of the values), each with its
answer to five places; the sum of the answers to 300 random arrays of
1 to 30 values from -20 to 20; and the problem's largest, 10,000 values
from -10,000 to 10,000, at widths 1, 100, 2,500 and
10,000. `max_average_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every subarray of `k` or more values summed from scratch, the largest
average found by comparing fractions exactly, and that one divided out.
Each of 1,000 cases has 1 to 25 values from -15 to 15 and a width from
1 to `n`.

| | property |
|---|---|
| P1 | the answer is the definition's, exactly |
| P2 | some subarray of `k` or more values averages exactly the answer |
| P3 | none averages more |
| P4 | the values in reverse give the same answer |
| P5 | every value doubled doubles the answer, exactly |

It prints `1000 cases (12933 values), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the largest start kept, not the smallest | P1 690, P3 690, P4 819 |
| M2 | ★: a start one place too late allowed | P1 614, P2 614, P4 434, P5 101 |
| M3 | ★: 10 halvings, not 100 | P1 2, P3 2, P4 3 |
| M4 | pairs: the last end never read | P1 250, P3 250, P4 443 |
| M5 | pairs: the smallest average kept | P1 851, P3 851 |
| M6 | hull: points kept that are not below the line | P1 326, P3 326, P4 512 |
| M7 | hull: always the newest start | P1 209, P3 209 |
| M8 | short: lengths up to `2k - 2` only | P1 108, P3 108, P4 125 |
| E1 | ★: an average of exactly `m` not counted as reaching it | 0 |
| E2 | pairs: starts past the last allowed one tried | 0 |
| E3 | hull: the front moved on only when strictly steeper | 0 |
| E4 | short: no early stop at the whole array | 0 |

P1 kills all eight. P3 sees every mutant but M2, the only one that can
return more than the best: a start one place too late lets a subarray of
`k - 1` values in, and P2 sees it because no allowed subarray has that
average. M3 is the faint one, 2 cases of 1,000: 10 halvings of a range
of at most 30 narrow the search only to within 0.03, so it goes wrong
only where the two best averages are closer than that. P4 sees the
mutants whose error depends on which end a subarray starts at; M5 and
M7 do not, since the smallest average and the best subarray of exactly
`k` are the same either way round. P5 sees only M2, in 101 cases; every
other mutant's error doubles with the values. The four survivors cannot
change an answer: an average of exactly `m` is reached again by a later,
smaller `m`; a start past the last allowed one has no end to pair with;
a tie at the front of the hull leaves a start of the same slope; and
lengths past the whole array try no start.

## Verification

Every arm prints the same output as `max_average_ii.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All at kara `0b9c97e02d` for the
debug build, with runtime archives built from `6a721d391c` (the runtime
differs between the two only in file system calls, which nothing here
makes), and `51eb3cb129` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends refuse every arm and the differential at type
checking: each reads `*x` from `nums.iter()`, and legacy types those
items by value; the harness also hands `seed`, already a `mut ref`
parameter, on with the `mut` marker design.md asks for, which legacy
rejects. Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 arrays of 100,000 values
from -10,000 to 10,000 once; then 40 rounds each find the best average
of one array, picked by the round, at a width from 1 to 100,000 also
picked by the round, adding up the answers. Every implementation prints
`40 rounds over 20 arrays of 100000 values: answers adding to
-42527.88761`, the Kāra program under `karac __mir-run` included (in
147 s).

Each implementation is the same binary search over prefix sums: Rust
over a `&[i64]`, C over an `int64_t` array, Go over a slice and Python
over a list. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine), each
including making the arrays:

| | time |
|---|---|
| C (`clang -O3`) | 0.39 to 0.44 s |
| Rust (`rustc -O`) | 0.41 to 0.47 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.45 to 0.52 s |
| Go | 0.48 to 0.54 s |
| Python | 29.9 to 30.5 s |
| Kāra (`karac build --mir`) | 0.43 to 0.48 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the bench
program: it reads `*x` from `nums.iter()`, which legacy types by value,
and handing `arrays[r % 20]` to `find_max_average` moves an element out
of a `Vec` while parameters are owned. That edit is by hand, on top of
the `scripts/new-bench.sh` output. A copy outside the kata that reads
`x` and makes both parameters `ref Vec[i64]` builds under legacy and
takes 0.39 to 0.45 s. Under `karac __mir-llvm-run` the program prints
the same line in 2.6 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is level with legacy and with Rust's overflow-checked
build, and ahead of Go. Each step of the inner loop is two subtractions,
two conversions to `f64`, two multiplications and two comparisons, with
the integer subtractions checked for overflow in the Kāra; the
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends. The legacy refusals
above are not filed because legacy is frozen.
