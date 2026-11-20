# 1213. Intersection of Three Sorted Arrays

Given three integer arrays `arr1`, `arr2` and `arr3` sorted in strictly
increasing order, return a sorted array of only the integers that
appeared in all three arrays.

```
arr1 = [1,2,3,4,5], arr2 = [1,2,5,7,9], arr3 = [1,3,4,5,8]    ->  [1,5]
arr1 = [197,418,523,876,1356], arr2 = [501,880,1593,1710,1870],
arr3 = [521,682,1337,1395,1764]                               ->  []
```

**Constraints:** `1 <= arr1.length, arr2.length, arr3.length <= 1000`;
`1 <= arr1[i], arr2[i], arr3[i] <= 2000`.

The arms are `fn arrays_intersection(arr1: Vec[i64], arr2: Vec[i64],
arr3: Vec[i64]) -> Vec[i64]`. The two Rust arms keep the method LeetCode
gives Rust users, on `Vec<i32>`, inside `impl Solution`, and a short
`arrays_intersection` narrows the arrays, calls it and widens the answer.

## Approaches

| file | mechanism |
|---|---|
| `intersection_of_three_sorted_arrays.kara` ★ | three pointers, one into each array: when the three values agree the value is kept and all three step on, and otherwise only the pointers at the least value do. O(n1 + n2 + n3) |
| `intersection_of_three_sorted_arrays_table.kara` | counting: the values lie in 1 to 2000 and none comes twice in one array, so each is counted in an `Array[i64, 2001]`, and the slots that reach 3, read in order, are the answer. O(n1 + n2 + n3 + 2000) |
| `intersection_of_three_sorted_arrays_sets.kara` | the second and third arrays as `Set`s, and the first, already in order, filtered to the values both hold. O(n1 + n2 + n3) expected |
| `intersection_of_three_sorted_arrays_halving.kara` | for each value of the first array a binary search in each of the other two, each search starting where its last one ended, since the values rise. O(n1 log(n2 + n3)) |
| `intersection_of_three_sorted_arrays_counts.kara` | a Rust solution as LeetCode's Rust users write it (every value counted in a `HashMap<i32, i32>` over `arr1.iter().chain(arr2.iter()).chain(arr3.iter())` with `*cnt.entry(x).or_insert(0) += 1`, the values counted 3 times taken by `into_iter().filter(\|&(_, c)\| c == 3)`, and `sort_unstable` putting them back in order), carried to Kāra by `karac fix` |
| `intersection_of_three_sorted_arrays_ordering.kara` | another Rust solution (three pointers in `let (mut i, mut j, mut k) = (0, 0, 0)`, and each step a `match` on the pair `(arr1[i].cmp(&arr2[j]), arr2[j].cmp(&arr3[k]))` against `std::cmp::Ordering` patterns), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 12 lines: LeetCode's two examples; one value
in all three (`[1]`) and one missing from the middle array (`[]`); three
equal arrays; 2000, the largest value, in all three; odd values against
even ones (`[]`); 1000 random small cases (`1000 small cases: 1394
values kept, checksum 12575333`); and four at the constraints' top:
three random arrays of 917, 914 and 916 values from 1 to 2000 (`180
kept, the first 18, the last 1999`), the 1000 even values against the
1000 odd ones and 1001 to 2000 (`0 kept`), the even values three times
over (`1000 kept`), and the even values against 1001 to 2000 twice
(`500 kept`). `intersection_of_three_sorted_arrays.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, table, sets and halving arms check clean as
written. The counts arm takes one round of 20 fixes (among them the
`use` line dropped, `HashMap<i32, i32>` to `Map[i32, i32]`, `for &x in`
to `for x in`, `|&(_, c)|` to `|(_, c)|`, and `sort_unstable()` to
`sort()`), and the ordering arm one round of 23 (among them `let (mut i,
mut j, mut k) = (0, 0, 0)` to `let mut (i, j, k) = (0, 0, 0)`, `vec![]`
to `Vec.new()`, `cmp(&arr2[j])` to `cmp(arr2[j])`, and `Ordering::Less`
to `Ordering.Less`, the `use` line dropped). Both outputs
match.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each value of the first array looked for in the other two,
one by one, and the values found in both sorted. 2000 random cases: the
values from 1 up to 1 to 12, each array keeping each value with its own
chance; 1154 of them have a value in all three.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | rising, and every value in all three arrays |
| P3 | the arrays in another order give the same |
| P4 | a value put in all three is in the answer, with the rest |
| P5 | every value one more gives every value one more |
| P6 | the answer given as the first array comes back unchanged |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 8505463,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, the values of the first array kept when the other two
hold them, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a value kept when the first two agree | P1 655, P2 655, P3 1122, P4 296, P7 3275 |
| S2 | ★: the pointers at the greatest value moved | P1 799, P4 1521, P7 3995 |
| T1 | table: two arrays enough | P1 1643, P2 1643, P7 1643 |
| T2 | table: the first array counted in place of the second | P1 909, P2 909, P3 1394, P7 909 |
| H1 | sets: a value in either set enough | P1 1394, P2 1394, P3 1403, P7 1394 |
| H2 | sets: the third set built from the second array | P1 864, P2 864, P3 1384, P7 864 |
| B1 | halving: the search lands past the value | P1 1154, P4 2000, P7 1154 |
| B2 | halving: a value in either array enough | P1 1104, P2 1104, P3 1126, P4 303, P7 1104 |
| X1 | counts: two arrays enough | P1 1643, P2 1643, P7 1643 |
| X2 | counts: a value's count begun at one | P1 1943, P2 1643, P4 2000, P6 1292, P7 1943 |
| O1 | ordering: the second pointer moved when the first is least | P1 595, P3 444, P4 1183, P7 595 |
| O2 | ordering: a value kept when the first two agree | P1 736, P2 736, P3 1199, P4 270, P7 736 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. Of the 2000 cases, 1154 have a value in all three arrays,
1943 a value in at least two, 1643 a value in exactly two, 1394 a value
of the first array in one of the other two but not both, 909 a value in
the first and third arrays and not the second, and 864 a value in the
first two and not the third (each counted by a Python reading of the
cases). T1 and X1 are one fault in two arms, a value in two arrays taken
as in all three, and fail the 1643 alike. X2 begins each count at one,
so a value in exactly two arrays reaches three and one in all three
passes it: its answer is the values in exactly two, and it fails all
1943. B1's search lands past the value it looks for, so it never finds
one and fails the 1154; P4, a value put in all three, then fails in
every case. T2 counts the first array where the second belongs and
fails the 909, H1 takes a value in either set and fails the 1394, and
H2, its third set built from the second array, answers the first two's
common values and fails the 864. P5, every value one more, catches none
of the twelve: no edit makes an arm treat a value specially.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (three pointers, all three stepping on when the values agree and
otherwise only those at the least value) on 1000 triples of arrays drawn
once, each array keeping every value from 1 to 2000 with its own chance,
from 33 to 44 in 100, so 600 to 950 values, near the constraints' most
of 1000; then 10 rounds over the triples, every answer's length and last
value folded into a checksum. Every program prints `10 rounds over 1000
triples of 600 to 950 values: checksum 997309093`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.168 to 0.204 s | 0.177 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.166 to 0.206 s | 0.171 s |
| Rust (`rustc -O`) | 0.171 to 0.222 s | 0.181 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.171 to 0.212 s | 0.178 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.175 to 0.211 s | 0.185 s |
| C (`clang -O3`) | 0.165 to 0.183 s | 0.168 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.162 to 0.190 s | 0.171 s |
| Go | 0.327 to 0.371 s | 0.345 s |
| Python | 6.022 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.178 s
against 0.171 s), and the two ranges overlap. C runs level with Kāra
(0.168 s against 0.171 s); Go takes about 2.0x Kāra's time. Python takes
about 35x Kāra's time. No profile was taken.
