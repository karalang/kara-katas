# 493. Reverse Pairs

Given an integer array `nums`, return the number of reverse pairs in
the array.

A reverse pair is a pair `(i, j)` where `0 <= i < j < nums.length` and
`nums[i] > 2 * nums[j]`.

```
nums = [1,3,2,3,1]  ->  2
nums = [2,4,3,5,1]  ->  3
```

**Constraints:** `1 <= nums.length <= 5 * 10^4`;
`-2^31 <= nums[i] <= 2^31 - 1`.

## Approaches

Every arm is `fn reverse_pairs(nums: Vec[i64]) -> i64`. Twice a 32-bit
number fits easily in an `i64`, so no arm has to guard the doubling.

| file | mechanism |
|---|---|
| `reverse_pairs.kara` ★ | merge sort on a copy: before merging two sorted halves, one pointer walks the right half and counts, for each left number in turn, the right numbers less than half of it; then the halves merge through a fresh `Vec` |
| `reverse_pairs_brute.kara` | every pair `i < j`, checked directly |
| `reverse_pairs_fenwick.kara` | a Fenwick tree over the ranks of the distinct values: for each number left to right, the numbers seen less those at most twice it (a binary search for the rank) make pairs with it; then it is counted at its own rank |
| `reverse_pairs_insert.kara` | a sorted `Vec` of the numbers seen: a binary search finds how many are above twice the new number, then the number is inserted in its place |
| `differential.kara` | the four arms on 1,500 random arrays, four properties |

Every arm prints the same 9 lines: the two LeetCode examples, one
number, rising, falling by halves, a number exactly twice another (not
a pair), negatives, the 32-bit extremes, and for 300 random arrays (1
to 40 numbers, from -50 to 50 or across the whole 32-bit range in
turn) the total count and a checksum. `reverse_pairs.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random arrays `a` of 1 to 30 numbers and `b` of 0 to 30, from -3
to 3, -100 to 100 or across the whole 32-bit range in turn, and one
more number `x`. The reference counts, for each number, the earlier
ones that exceed twice it.

| | property |
|---|---|
| P1 | the count is the reference's |
| P2 | `a` with `x` appended adds the numbers of `a` above twice `x` |
| P3 | every number doubled gives the same count |
| P4 | `a` then `b` gives the count of `a`, the count of `b` and the pairs across |

It prints `1500 cases, 4 arms, 24000 checks, 0 failures` under
`karac __mir-run`, in 3.5 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a number exactly twice another counts | P1 534, P2 187, P4 612 |
| M2 | ★: the merge takes the larger first | P1 1349, P2 1315, P4 1441 |
| M3 | brute: a number is paired with itself | P1 1464, P2 722 |
| M4 | brute: the last number is never the second of a pair | P1 998, P2 1271, P4 1233 |
| M5 | fenwick: the values equal to twice a number count above it | P1 534, P2 187, P4 612 |
| M6 | fenwick: a number is recorded one rank up | P1 1302, P2 872, P4 1246 |
| M7 | insert: a number goes on the end, not in its place | P1 1143, P2 518, P4 1326 |
| M8 | insert: the bar is twice the number plus one | P1 561, P2 256, P3 561, P4 636 |

P3 sees only M8: doubling every number keeps every comparison the
other mutants get wrong exactly as wrong, while M8's `+ 1` does not
double with them. M1 and M5 count the same thing wrongly (`>=` for
`>`) and fail with the same counts. Two first drafts were equivalent and
were replaced: the Fenwick arm without `dedup` (a rank search finds the
first of equal values, so the repeats are never used), and the insert
arm placing a number before its equals rather than after them (the
list stays sorted either way).

## Verification

All four arms print the same output as `reverse_pairs.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included.
The differential prints `24000 checks, 0 failures` on both. The four
arms and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on all four arms: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output. Legacy `karac build` warns on the insert arm
that `sorted` is "moved here, used again here", where `first_above` is
lent it twice and legacy reads the first as a move; the output is right
all the same. The differential does not type-check on legacy, which
reads the items of `a.iter()` and `b.iter()` as `i64` and refuses `*y`.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 60 arrays of 50,000
numbers (the problem's most) across the whole 32-bit range once, then
counts each once. Every implementation prints `60 arrays of 50000:
37485740079 reverse pairs, checksum 408901591`, the Kāra program under
`karac __mir-run` included (in 59 s).

Every mirror sorts a copy of the array and merges through a fresh
buffer at each level, as the ★ arm does with a fresh `Vec`: Rust a
`Vec`, Go a slice grown by `append`, Python a list, C a `malloc`'d
array freed after the copy back. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.53 to 0.55 s |
| Rust (`rustc -O`) | 0.69 to 0.75 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.71 to 0.86 s |
| Go | 0.93 to 1.00 s |
| Python | 9.0 to 9.3 s |
| Kāra (`karac build`) | 0.68 to 0.69 s |
| Kāra (`karac build --mir`) | 0.69 to 0.71 s |

The legacy `karac build` builds and runs this program correctly, so
`bench.sh` is the `scripts/new-bench.sh` output unchanged and times
that build. The `--mir` row is the v2 compiled backend, timed for
comparison. Both Kāra rows are timed at kara `d9a7136c58`. Under
`karac __mir-llvm-run` the program prints the same line in 2.8 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
