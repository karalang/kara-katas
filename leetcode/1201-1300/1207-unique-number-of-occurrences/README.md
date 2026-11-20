# 1207. Unique Number of Occurrences

Given an array of integers `arr`, return `true` if the number of
occurrences of each value in the array is unique or `false` otherwise.

```
arr = [1,2,2,1,1,3]                 ->  true    1 three times, 2 twice, 3 once
arr = [1,2]                         ->  false
arr = [-3,0,1,-3,1,1,1,-3,10,0]     ->  true
```

**Constraints:** `1 <= arr.length <= 1000`; `-1000 <= arr[i] <= 1000`.

The arms are `fn unique_occurrences(arr: Vec[i64]) -> bool`. The two Rust
arms keep the method LeetCode gives Rust users, on `Vec<i32>`, inside
`impl Solution`, and a one-line `unique_occurrences` calls it.

## Approaches

| file | mechanism |
|---|---|
| `unique_number_of_occurrences.kara` ★ | each value's count in a `Map`, and the counts collected into a `Set`, which has as many as the map exactly when no two values share a count. O(n) |
| `unique_number_of_occurrences_runs.kara` | the values sorted, so each value is one run; the runs' lengths sorted in turn, and no two neighbours equal. O(n log n), no hashing |
| `unique_number_of_occurrences_table.kara` | the values' range is small, so each count sits in an array of 2001 slots, and each count, at most 1000, marks a slot of a second array of 1001; a count met twice answers false. O(n + 2001) |
| `unique_number_of_occurrences_owners.kara` | counted twice over: each value's count in a `SortedMap`, then a second `SortedMap` of how many values have each count, and every one of those 1 |
| `unique_number_of_occurrences_sets.kara` | a Rust solution as LeetCode's Rust users write it (`*freq.entry(x).or_insert(0) += 1` into a `HashMap`, then `freq.values().all(|&c| seen.insert(c))` over a `HashSet`, whose `insert` answers false for a count already in it), carried to Kāra by `karac fix` |
| `unique_number_of_occurrences_chunks.kara` | another Rust solution (`mut arr` sorted with `sort_unstable`, each run's length by `chunk_by(|a, b| a == b)`, and the lengths sorted and `dedup`ed, as long as before when no two were equal), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 12 lines: LeetCode's three examples; one
value; the two ends of the range, `[-1000, 1000, 1000]`; one value four
times; two values twice each (`false`); counts 1 to 4; 1000 random small
cases, 1 to 30 values from 1 to 6 near 0 (`1000 small cases: 553 true,
checksum 307188225`); and three at the constraints' top, 1000 values:
`v` given `v` times for `v` from 1 to 43 with -1000 given 54 times
(`true`), the same with one -1000 made a 1, so 1 and 2 both come twice
(`false`), and 1000 distinct values, all counted once (`false`).
`unique_number_of_occurrences.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, runs, table and owners arms check clean as
written. The sets arm takes one round of 14 fixes (among them the `use`
line dropped, `HashMap` and `HashSet` to `Map` and `Set`, `for &x in` to
`for x in`, and `|&c|` to `|c|`), and the chunks arm one round of 12
(among them `mut arr: Vec<i32>` to `arr: own Vec[i32]` with a `let mut
arr = arr;`, `sort_unstable()` to `sort()`, `Vec<usize>` to `Vec[i64]`,
and `.into_iter()` after `chunk_by(..)`). Both outputs match.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every two values that differ, each one's count by a walk
over the whole array, and the two compared. 2000 random cases: 1 to 24
values from 1 to 5 distinct ones near 0; 1252 of them answer true.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed gives the same |
| P3 | every value negated gives the same |
| P4 | the array given twice over gives the same |
| P5 | a value not in the array, added once, gives true just when the array did and no value came once |
| P6 | every copy of one value taken out keeps a true answer true |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 882732875,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, comparing `list.count` for every two values, gives the
same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: as many counts as values, or fewer, taken for true | P1 748, P5 1031, P7 3740 |
| S2 | ★: every value counted once | P1 751, P5 969, P6 372, P7 3755 |
| U1 | runs: the lengths never sorted | P1 236, P5 326, P7 236 |
| U2 | runs: every run measured from the start | P1 748, P5 1031, P7 748 |
| T1 | table: a count never marked seen | P1 748, P5 1031, P7 748 |
| T2 | table: the values that never come counted too | P1 1252, P5 969, P6 1252, P7 1252 |
| W1 | owners: a count shared by two let through | P1 600, P5 727, P7 600 |
| W2 | owners: each count's owners counted once | P1 748, P5 1031, P7 748 |
| X1 | sets: a count already seen let through | P1 748, P5 1031, P7 748 |
| X2 | sets: any new count enough | P1 748, P5 1031, P6 501, P7 748 |
| C1 | chunks: the lengths never sorted | P1 236, P5 326, P7 236 |
| C2 | chunks: the lengths never deduplicated | P1 748, P5 1031, P7 748 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. Of the 2000 cases 748 answer false, and S1, U2, T1, W2, X1
and C2 each answer true every time, so each fails exactly those 748; T2,
which counts the values that never come and so always finds two zero
counts, answers false every time and fails the 1252 others. S2 counts
every value once, so it answers true only for an array of one value,
and fails the 751 true cases with two or more (counted by a Python
reading of the cases). U1 and C1 are one fault in two arms, the lengths
compared or deduplicated only next to each other without the sort, and
fail alike. P2, P3 and P4, the array reversed, negated or given twice
over, catch none of the twelve: no edit makes an arm depend on the
order of the values, their signs, or the size of the counts rather than
which ones are equal.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (each value's count in a `Map`, and the counts put in a `Set`) on
2000 arrays of 1000 values, the constraints' most, drawn once: each from
1 to 12 distinct values spread over -1000..=1000, with weights so that
both answers come; then 10 rounds over the arrays, how many answer true
folded into a checksum. Every program prints `10 rounds over 2000 arrays
of 1000 values: checksum 871814503`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.283 to 0.427 s | 0.307 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.294 to 0.444 s | 0.326 s |
| Rust (`rustc -O`) | 0.255 to 0.346 s | 0.267 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.259 to 0.322 s | 0.279 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.258 to 0.394 s | 0.289 s |
| C (`clang -O3`) | 0.102 to 0.149 s | 0.112 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.097 to 0.148 s | 0.104 s |
| Go | 0.229 to 0.267 s | 0.240 s |
| Python | 2.340 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 14% ahead of Kāra (0.279 s
against 0.326 s), and the two ranges overlap. Kāra takes about 2.9x C's
time (0.326 s against 0.112 s); Go is about 26% ahead of Kāra (0.240 s
against 0.326 s). Python takes about 7x Kāra's time. No profile was
taken.
