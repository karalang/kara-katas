# 442. Find All Duplicates in an Array

Given an integer array `nums` of length `n` whose values are all in
`[1, n]`, and in which each value appears once or twice, return every
value that appears twice, in any order. The solution must run in O(n)
time and use only constant extra space.

```
nums = [4,3,2,7,8,2,3,1]  ->  [2,3]
nums = [1,1,2]            ->  [1]
nums = [1]                ->  []
```

**Constraints:** `1 <= n <= 10^5`; `1 <= nums[i] <= n`; each value
appears once or twice.

## Approaches

Every value is in `[1, n]`, so it names a slot of the array itself,
and the in-place arms keep their notes there. Those arms take the
array as `own Vec[i64]`, since they change it.

| file | mechanism |
|---|---|
| `find_duplicates.kara` ★ | marking by sign: for each value x, a negative slot x - 1 means x was seen before; otherwise negate the slot. The array's values are read through their absolute value. O(n), no extra space |
| `find_duplicates_place.kara` | cyclic sort: swap every value into its own slot until the slot already holds it, then report the value in each slot that does not hold its own. O(n), no extra space |
| `find_duplicates_set.kara` | the plain reference: a `Set` of the values seen, and a value already in it is a duplicate. O(n) expected time but O(n) extra space; the array stays untouched |
| `find_duplicates_add.kara` | counting by adding n: each sighting of x adds n to slot x - 1, so the slot keeps its own value as the remainder and its count as the quotient. O(n), no extra space, values up to 3n |
| `differential.kara` | the four arms on 1,500 random arrays, five properties |

The arms find the duplicates in different orders, all allowed, so the
harness sorts each answer before printing it. Every arm prints the
same 9 lines: the three LeetCode examples, five edge cases (one pair,
a permutation with none, three pairs, a reversed run with four pairs,
and a single pair at the ends), and for 300 random arrays of 1 to 200
numbers the number of duplicates and a checksum.
`find_duplicates.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random arrays of 1 to 60 numbers, built as the first d values of
a shuffled `1..n` twice and the next n - 2d once, then shuffled. Each
arm's answer is sorted before it is compared.

| | property |
|---|---|
| P1 | the answer is the reference's, the values a count finds twice |
| P2 | the answer is the values the generator doubled, and shuffling the array changes nothing |
| P3 | relabelling the values by a permutation of `[1, n]` relabels the answer |
| P4 | appending n + 1 changes nothing, and appending a value seen once adds it to the answer |
| P5 | `1..m` shuffled has no duplicates, and `1..m` twice over, shuffled, has all of `1..m` |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | sign: the duplicate reported is the marked slot's value | P1 1257, P2 1304, P3 1259, P4 1407, P5 1363 |
| M2 | sign: the mark is looked for in the value's own slot | P1 1442, P2 1459, P3 1445, P4 1483, P5 1500 |
| M3 | place: one swap per slot instead of a cycle | P1 1269, P2 1340, P3 1275, P4 1233, P5 1181 |
| M4 | place: the missing number is reported, not the duplicate | P1 1332, P2 1332, P3 1332, P4 1500, P5 1500 |
| M5 | set: values are told apart by half | P1 1419, P2 1419, P3 1413, P4 1448, P5 1388 |
| M6 | set: the first number is skipped | P1 729, P2 938, P3 729, P4 842, P5 1500 |
| M7 | add: a slot added to once counts as a duplicate | P1 1413, P2 1413, P3 1413, P4 1500, P5 1500 |
| M8 | add: each sighting adds n + 1 | P1 1482, P2 1497, P3 1483, P4 1500, P5 1488 |

Every property kills every mutant, so the five agree here rather than
divide the work. The cases each mutant survives are those where its
fault cannot show: M4 matches the answer on an array with no
duplicates, M7 on one where every value is a pair, so that every slot
is added to twice or not at all, and M6 whenever the skipped first
number is not one copy of a pair.

## Verification

All four arms print the same output as `find_duplicates.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`, and the differential prints
`0 failures` under `karac run --interp` and `karac build`.

## Benchmarks

The bench program uses the ★ arm. It builds one array of 1,000,000
numbers once, 300,000 of them pairs, then 20 times copies it and finds
its duplicates in the copy, folding each round's answers into a
checksum. Every implementation prints `20 rounds on 1000000 numbers:
6000000 duplicates, checksum 456831838`, the Kāra program under
`karac __mir-run` included (in 26 s).

The mirrors keep the ★ arm's structure: each round copies the array
(`clone`, `memcpy`, a slice copy) and grows its answer, except that C
writes the answer into a buffer of n numbers allocated once a round.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.29 to 0.34 s |
| Rust (`rustc -O`) | 0.22 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.31 to 0.34 s |
| Go | 0.59 to 0.67 s |
| Kāra (frozen legacy `karac build`) | 0.22 to 0.25 s |
| Python | 15.1 to 15.4 s |

C trails Rust here, likely (not profiled) because its answer buffer,
8 MB of fresh memory each round, is touched for the first time on
every round, where a growing vector reuses what it freed. The legacy
build checks integer overflow and still matches plain Rust. The Kāra
program prints the same line under `karac __mir-llvm-run` in 1.3 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

No new findings.
