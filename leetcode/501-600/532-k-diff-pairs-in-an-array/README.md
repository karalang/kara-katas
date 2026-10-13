# 532. K-diff Pairs in an Array

Given an array of integers `nums` and an integer `k`, return the
number of unique k-diff pairs in the array. A k-diff pair is an
integer pair `(nums[i], nums[j])` where `0 <= i, j < nums.length`,
`i != j`, and `|nums[i] - nums[j]| == k`.

```
nums = [3, 1, 4, 1, 5], k = 2  ->  2   (1, 3) and (3, 5)
nums = [1, 2, 3, 4, 5], k = 1  ->  4
nums = [1, 3, 1, 5, 4], k = 0  ->  1   (1, 1)
```

**Constraints:** `1 <= nums.length <= 10^4`; `-10^7 <= nums[i] <=
10^7`; `0 <= k <= 10^7`.

## Approaches

Every arm is `fn find_pairs(nums: Vec[i64], k: i64) -> i64`. A pair
is two values, not two places, so `(1, 3)` from either `1` counts
once.

| file | mechanism |
|---|---|
| `find_pairs.kara` ★ | count each value in a `Map`; for `k = 0` a pair is a value seen twice, otherwise a value `v` whose `v + k` is there; O(n) |
| `find_pairs_pointers.kara` | sort, then a right pointer with a left one behind it, closing the gap to `k`; repeated values skipped on the right |
| `find_pairs_search.kara` | sort, and for each different value a binary search for `v + k` among the numbers after it |
| `find_pairs_sets.kara` | one pass: a number `x` pairs with an earlier `x - k` and an earlier `x + k`, each pair kept by its smaller value in a `Set` |
| `differential.kara` | the four arms against every two places, five properties |

Every arm prints the same 11 lines: the three examples, `k = 0`
without and with repeats, `k = 1` on equal numbers, one number,
negatives, and the extremes; then for 300 random arrays of 1 to 50
numbers from -10 to 10, -100 to 100, or the whole range in turn the
pairs in all and a checksum; and last the largest case, 10,000
numbers from -5,000 to 5,000 for `k` of 0, 1 and 7.
`find_pairs.py` mirrors the ★ arm and its output is byte-identical.
The ★ arm walks a `Map`, whose order is different on every run, but
it only counts, so its output does not depend on the order.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every two places `i < j` whose numbers differ by `k` give the pair
(smaller, larger), and the answer is how many different pairs there
are. Each arm is held to the properties below on 1,000 random arrays
of 1 to 40 numbers from -5 to 5, -50 to 50, or the whole range in
turn; `k` is 0 to 3 for a third of them and otherwise the difference
between the first number and a random one, so that pairs occur at
every range.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the numbers in a shuffled order give the same answer |
| P3 | every number negated gives the same answer |
| P4 | every number shifted by the same amount gives the same answer |
| P5 | the numbers written twice give the same answer, except for `k = 0`, where every different number then makes a pair |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: for `k = 0`, a value seen once counted (`>= 1`) | P1 159 |
| M2 | ★: `k = 0` not treated apart | P1 159 |
| M3 | pointers: repeated values not skipped on the right | P1 388, P3 298, P5 903 |
| M4 | pointers: the left pointer also steps past a gap of exactly `k` (`>=`) | P1 903, P5 163 |
| M5 | search: the search starts at the value itself | P1 159 |
| M6 | search: repeated values searched from again | P1 377, P3 298, P5 903 |
| M7 | sets: a pair found from below recorded by its larger value | P1 243, P2 218, P5 738 |
| M8 | sets: the earlier `x + k` looked for one too high | P1 522, P2 497, P3 703, P5 497 |
| E1 | ★: each pair counted from its larger end (`v - k`) | 0 |
| E2 | pointers: no `left < right` guard on the inner loop | 0 |
| E3 | search: the middle taken as `low + (high - low) / 2` | 0 |
| E4 | sets: the pairs kept in a `SortedSet` | 0 |

M1, M2 and M5 are one mistake, a value seen once taken for a pair
with itself when `k = 0`, and only P1 sees it: P2 to P4 keep every
value's count, and P5's doubled numbers repeat every value, which is
exactly when the mistake gives the right answer. M3 and M6 count a
repeated value once per copy, so P5's doubled numbers fail 903 of
the 1,000 cases. M7 and M8 make the sets arm depend on which of the two
numbers comes first, which P2's shuffle sees. E2 holds because a gap
of 0 is never more than `k`, so the inner loop stops at `left ==
right` without the guard.

## Verification

Every arm prints the same output as `find_pairs.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `20000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program. All of this is at kara `21ffa33dff`.

On the frozen legacy backends, `karac run --interp` runs the pointers
and search arms with the same output. LLJIT and legacy `karac build`
fail on those two at codegen: the harness's call `show("example 1",
vec![...], 2)` fails LLVM's module verification ("Call parameter type
does not match function signature"). The ★ and sets arms, the
differential and the bench program are refused at type checking:
legacy types the items of a `Vec`'s `iter()` by value, so it refuses
`*x` ("unary '*' requires 'ref T' ... found 'i64'"). Legacy is frozen,
so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 arrays of 10,000
numbers (the problem's most) once, the `a`-th drawn from `-1,000(a +
1)` to `1,000(a + 1)`, then answers each array for 200 values of `k`
from 0 to 19, building a fresh `Map` every time. Every implementation
prints `20 arrays of 10000, 200 values of k each: total 11733910,
checksum 736423780`, the Kāra program under `karac __mir-run` included
(in 140 s).

Rust uses `HashMap` with its default SipHash-1-3, the hasher Kāra's
`Map` uses too; Go uses its built-in map, Python a dict. C has no
map, so its mirror builds a fresh open-addressing table with a
multiplicative hash for each call, a much cheaper hash than SipHash.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.11 to 1.17 s |
| Rust (`rustc -O`) | 2.11 to 2.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.24 to 2.38 s |
| Go | 3.48 to 3.82 s |
| Python | 6.2 to 6.3 s |
| Kāra (`karac build --mir`) | 3.06 to 3.31 s |

The Kāra program is about 40% slower than the Rust one here, with the
same hasher on both. The legacy `karac build` refuses this program
(see Verification). So `bench.sh` builds the Kāra program with `karac
build --mir`, the v2 compiled backend. That edit is by hand, on top of
the `scripts/new-bench.sh` output. All of these are timed at kara
`21ffa33dff`. Under `karac __mir-llvm-run` the program prints the same
line in 26 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
written.
