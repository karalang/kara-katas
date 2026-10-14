# 611. Valid Triangle Number

Given an array of lengths, return how many choices of three of them, by
position, could be the sides of a triangle: each two adding up to more
than the third.

```
[2, 2, 3, 4]  ->  3     (2, 3, 4) twice, (2, 2, 3) once
[4, 2, 3, 4]  ->  4
```

**Constraints:** 1 to 1,000 lengths, each from 0 to 1,000.

## Approaches

Every arm is `fn triangle_number(nums: Vec[i64]) -> i64`. Sorted, three
lengths make a triangle exactly when the two shorter add up to more than
the longest, since then each other pair does too.

| file | mechanism |
|---|---|
| `triangle_number.kara` ★ | sort a copy, take each length as the longest, and close two pointers in on the lengths below it, counting a whole run at once when the pair at the pointers adds up to more; O(n^2) |
| `triangle_number_search.kara` | sort a copy; for each pair, binary search for the first later length that reaches the pair's sum, every length between being a third; O(n^2 log n) |
| `triangle_number_brute.kara` | every triple of positions, unsorted, checked against all three inequalities; O(n^3) |
| `triangle_number_counts.kara` | sort a copy and count once how many lengths fall below each value up to 1,001; for each pair, the thirds are the lengths below the pair's sum less those at or before the pair; O(n^2 + the largest length) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: the two LeetCode examples; eight
more (no lengths, two, zeros, which are in no triangle, a zero beside
three alike, a sum that only reaches the third, three alike, a long side
no pair reaches, and an unsorted array with repeats); 200 lengths of
1,000, every triple a triangle, and the lengths 1 to 200; a total and
checksum over 300 random arrays of 0 to 60 lengths; and 200 random
lengths. The largest cases have 200 lengths rather than the problem's
1,000, so that the cubic arm stays quick; the bench program takes
1,000. `triangle_number.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every choice of three positions, its lengths sorted, counted when the
two shorter add up to more than the longest. Each of 1,000 random cases
has 0 to 12 lengths in one of three bands: up to a bound of 1 to 10, so
that lengths repeat often; up to a bound of 1 to 500; or from 900 to
1,000, the problem's longest, where every pair adds up to more than
1,000. P4 and P5 run only on the first two bands, where doubled lengths
and an added 1,000 stay within the problem's bounds.

| | property |
|---|---|
| P1 | the count is the definition's |
| P2 | the lengths shuffled give the same count |
| P3 | a length of 0 added changes nothing, a zero being in no triangle |
| P4 | every length doubled changes nothing |
| P5 | a length of 1,000 added, which no two lengths of at most 500 add up to more than, changes nothing |

It prints `1000 cases (33385 triangles), 4 arms, 17024 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`. There are fewer than 20,000 checks
because P4 and P5 skip the band near 1,000.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a sum equal to the longest counted | P1 292, P3 327 |
| M2 | ★: one triangle counted for a whole run | P1 642 |
| M3 | search: the run ends at the first length above the sum | P1 292, P3 327 |
| M4 | search: the run starts at the pair's own upper length | P1 198, P3 924, P5 203 |
| M5 | brute: the third inequality left out | P1 377, P2 384, P3 782 |
| M6 | brute: the third length may repeat the second's position | P1 822, P2 367, P5 570 |
| M7 | counts: lengths at most each value counted, not below it | P1 276, P3 675 |
| M8 | counts: sums capped at 1,000 | P1 26 |
| E1 | ★: the longest taken from position 0 | 0 |
| E2 | search: the midpoint as `lo + (hi - lo) / 2` | 0 |
| E3 | brute: the three lengths read in another order | 0 |
| E4 | counts: a third count of 0 added too | 0 |

M1 and M3 make the same mistake, counting three lengths whose two
shorter only reach the longest, and fail the same counts. P3 sees it
most, since a zero added beside two equal lengths is such a triple.
M7 makes it in the counts arm and fails fewer cases; why was not looked
into. M4 starts each run at the pair's own upper length, which a pair
with a zero does not pass, so it counts minus one there, and the zero of
P3 brings that out on almost every case. M5 checks two of the three
inequalities, so whether a triple is counted depends on the order of its
lengths, which P2's shuffle changes. M6 lets the third length repeat the
second, and P5's added 1,000 makes such a pair with itself and any other
nonzero length. M8 caps the sums at 1,000 and so misses a third of
exactly 1,000 beside a pair adding up to more; that is common only in
the band near 1,000, where only P1 runs. P4 kills nothing: doubling
every length keeps each mutant's answer too.

## Verification

Every arm prints the same output as `triangle_number.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes every arm, the differential and the bench program. All at kara
`d8c605558f`.

The frozen legacy backends run the ★ and search arms right under `karac
run --interp`, `karac run` and `karac build`, and the brute arm right
under `karac run` and `karac build`; under `--interp` the brute arm
prints the same first 12 lines and runs past 60 seconds on the
200 random lengths. They refuse the counts arm and the differential at
type checking: legacy types the items of a `Vec`'s `iter()` by value, so
the `*x` that reads one is an error. Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random arrays of
1,000 lengths, the problem's most, each from 0 to a bound of 100 to
1,000, once; then 600 times counts the triangles in one of them, picked
by the round. Every implementation prints `20 arrays, 600 rounds:
48508834050 triangles, checksum 589901733`, the Kāra program under
`karac __mir-run` included (in 76 s).

Each implementation sorts a copy of its array in every call, as the ★
arm sorts a clone: Rust with `sort` on a `to_vec`, Go with `slices.Sort`
on a `slices.Clone`, C with `qsort` on a `malloc`'d copy, and Python
with `sorted`. Spot timings on a shared 4-core container, three runs
each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.14 to 1.15 s |
| Rust (`rustc -O`) | 1.10 to 1.14 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.92 to 0.97 s |
| Go | 0.87 to 0.93 s |
| Python | 18.6 to 19.0 s |
| Kāra (`karac build --mir`) | 1.05 to 1.12 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses it at the
`all[(r * 7) % arrays]` it passes by value ("cannot move out of an index
expression"); that edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
3.6 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

The Kāra row is level with C's and plain Rust's. Go and the
overflow-checked Rust are quicker on these runs than plain Rust and C;
why was not looked into.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
