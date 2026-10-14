# 548. Split Array with Equal Sum

Given an integer array `nums` of length `n`, return `true` if there is a
triplet `(i, j, k)` which satisfies the following conditions: `0 < i`,
`i + 1 < j`, `j + 1 < k < n - 1`, and the sum of subarrays `(0, i -
1)`, `(i + 1, j - 1)`, `(j + 1, k - 1)` and `(k + 1, n - 1)` is equal. A
subarray `(l, r)` represents a slice of the original array starting from
the element indexed `l` to the element indexed `r`.

```
nums = [1,2,1,2,1,2,1]    ->  true   (i = 1, j = 3, k = 5)
nums = [1,2,1,2,1,2,1,2]  ->  false
```

**Constraints:** `n == nums.length`; `1 <= n <= 2000`; `-10^6 <= nums[i]
<= 10^6`.

## Approaches

Every arm is `fn split_array(nums: Vec[i64]) -> bool`. The three values
at the cuts belong to no part.

| file | mechanism |
|---|---|
| `split_array_with_equal_sum.kara` ★ | prefix sums; for each middle cut j, the sums of every left cut whose two left parts are equal go into a `Set[i64]`, and a right cut whose two right parts are equal, and equal to one of them, is a yes; O(n^2) |
| `split_array_with_equal_sum_sorted.kara` | the same cuts, the left sums in a `Vec` sorted once per middle cut and searched by hand-written binary search; O(n^2 log n) |
| `split_array_with_equal_sum_right.kara` | read from the other end: the right sums first, in a `SortedSet[i64]`, then the left cuts tried against it |
| `split_array_with_equal_sum_cuts.kara` | no prefix array: each part's sum kept running as the cuts walk right, the third cut walked only where the first two parts match; O(n^3) at worst |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 13 lines: both examples, six values, seven
zeros, parts that are negative, the cut values far from the parts' sum,
and eight equal values with no room for the cuts, each with its answer;
then for 300 random arrays of 1 to 30 values (from -1 to 1, -2 to 2 or
-5 to 5 in turn) the number of values, how many can be split and a
checksum; and last five long ones: 2,000 zeros, 2,000 random values,
four planted parts of 499 values summing to 1,000 with random cuts
between them, and two of 200 that are slow for the cuts arm, 199 zeros
and a one, and values swinging between 10^6 and
-10^6. `split_array_with_equal_sum.py` mirrors the ★ arm and its output
is byte-identical.

The two slow cases are 200 values long, not 2,000, because the cuts arm
walks the third cut wherever the first two parts match, and on those
rows they match for most pairs. With 2,000 swinging values in the
harness, the cuts arm's whole run took 348 s under `karac __mir-run`,
against 4.6 s for the ★ arm.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every triple of cuts within the bounds
tried, each of the four parts summed on its own. Each arm is held to the
properties below on 1,000 random arrays of 1 to 14 values, from -1 to
1, -2 to 2 or -4 to 4 in turn; 79 of them can be split.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the array reversed gives the same answer |
| P3 | every value negated gives the same answer |
| P4 | a yes stays a yes with a 0 added at each end |
| P5 | every value doubled gives the same answer, and fewer than 7 values is never a yes |

It prints `1000 cases (79 can be split), 4 arms, 20000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last middle cut never tried | P1 7, P2 13 |
| M2 | ★: the second part summed with the first cut in it | P1 55, P2 55 |
| M3 | sorted: the left sums reversed, not sorted | P1 4, P2 11, P3 10, P4 3 |
| M4 | sorted: the binary search's landing taken as a match | P1 56, P2 106, P3 106 |
| M5 | right: every right cut's sum kept, the fourth part unchecked | P1 139, P2 159 |
| M6 | right: a right cut allowed next to the middle one | P1 23, P2 35 |
| M7 | cuts: the third cut left in the fourth part | P1 67, P2 67 |
| M8 | cuts: the last first cut never tried | P1 5, P2 4 |
| E1 | ★: no early answer for fewer than 7 values | 0 |
| E2 | sorted: an empty set of left sums still searched | 0 |
| E3 | right: the left cuts tried from the right | 0 |
| E4 | cuts: the third and fourth parts compared with the second, not the first | 0 |

P2 kills every mutant, and is the property to keep if only one were:
each mistake is one-sided, a cut range cut short at one end or a part
summed with a cut in it, so the reversed array, where the mistake falls
on the other side, disagrees. M1 and M8 are the narrowest kills, since a
yes that needs exactly the last middle or first cut is rare at
14 values; the definition sees 7 and 5 of them. M3 and M4 break the
search rather than the cuts, so they also disagree with themselves under
negation (P3), which turns a sorted list's order around. P5 kills
nothing: every mistake here is linear in the values, and doubling them
changes no answer. E2 is safe because a binary search over nothing finds
nothing, and E4 because the third cut is only walked where the second
part already equals the first.

A first E4, the third cut walked even where the first two parts differ,
was not equivalent and failed 242 checks: the walk's own test compares
the third and fourth parts with the first but never the second, which
only the skip guarantees. It was replaced by the E4 above.

## Verification

Every arm prints the same output as `split_array_with_equal_sum.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. `karac check` passes on every arm, the differential and the bench
program.

The frozen legacy backends: `karac run --interp` prints the same output
for the ★, sorted and right arms. `karac run` and `karac build` fail
those three in codegen ("Call parameter type does not match function
signature" on `show("example 1", ...)`), and stop the cuts arm and the
differential at type checking on `*x` over `iter()` of a `Vec[i64]`
("unary '*' requires 'ref T' ... found 'i64'"), as `karac run --interp`
does the cuts arm. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 10 random arrays of
2,000 values (the problem's most), array g from -s to s with s = 1 + g %
5 * 25, once. Then 20 times over, one value of every array, picked by
the round and the array, is negated and the array is answered; the
answers go into the checksum. Every implementation prints `10 arrays,
20 rounds each: 69 can be split, checksum 262979031`, the Kāra program
under `karac __mir-run` included (193.5 s).

Rust uses `std`'s `HashSet`, which hashes with SipHash-1-3 as Kāra's
`Set` does, and Go its built-in map; C has no hash set, so its mirror
carries a small open-addressing one with a multiplicative hash, emptied
after each middle cut. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.39 to 0.47 s |
| Rust (`rustc -O`) | 0.43 to 0.44 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.59 to 0.60 s |
| Go | 0.68 to 0.72 s |
| Python | 35.28 to 35.72 s |
| Kāra (`karac build --mir`) | 1.01 to 1.11 s |

The legacy `karac build` refuses this program: it moves `all[g]` out of
the index where v2 borrows it (`E_INDEX_MOVE_NON_COPY`). So `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend; that edit is by hand, on top of the `scripts/new-bench.sh`
output. The `--mir` row is timed at kara `2b8238c108`. Under `karac
__mir-llvm-run` the program prints the same line in 5.0 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark. The Kāra row is about 1.8 times Rust's with overflow
checks and 2.4 times Rust's without; where the time goes was not looked
into.

## Compiler findings

None new. Nothing was filed from this kata; the legacy failures above
are not filed because legacy is frozen.
