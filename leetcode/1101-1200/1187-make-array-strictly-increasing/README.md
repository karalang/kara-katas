# 1187. Make Array Strictly Increasing

Given two integer arrays `arr1` and `arr2`, return the fewest operations
that make `arr1` strictly increasing. In one operation, choose an index `i`
of `arr1` and an index `j` of `arr2` and set `arr1[i] = arr2[j]`. If there
is no way, return `-1`.

```
arr1 = [1, 5, 3, 6, 7], arr2 = [1, 3, 2, 4]  ->  1    5 becomes 2
arr1 = [1, 5, 3, 6, 7], arr2 = [4, 3, 1]     ->  2    5 becomes 3, 3 becomes 4
arr1 = [1, 5, 3, 6, 7], arr2 = [1, 6, 3, 3]  ->  -1
```

**Constraints:** `1 <= arr1.length, arr2.length <= 2000`,
`0 <= arr1[i], arr2[i] <= 10^9`.

The arms are `fn make_array_increasing(arr1: Vec[i64], arr2: Vec[i64]) ->
i64`. The two Rust arms keep the method LeetCode gives Rust users, over
`Vec<i32>`, inside `impl Solution`, and a one-line `make_array_increasing`
converts the values and calls it.

## Approaches

Only the value the prefix ends on matters to what comes after it, and a
replacement only ever takes the least value of `arr2` above that end: a
larger one leaves the rest no easier. So each element either stays, when it
rises above the end, or becomes the least value of `arr2` above the end, one
binary search into `arr2` sorted and deduplicated.

| file | mechanism |
|---|---|
| `make_array_increasing.kara` ★ | for each count `k` of replacements, the least value the prefix can end on, carried along `arr1`; the answer is the least `k` that reaches the end. O(n² log m) |
| `make_array_increasing_map.kara` | for each value the prefix can end on, the fewest replacements, in a `SortedMap` rebuilt for each element. O(n · m · log m) |
| `make_array_increasing_memo.kara` | top down: the fewest replacements that finish from index `i` above `prev`, each answer kept in a `Map` keyed by `(i, prev)`. O(n · (n + m) · log m) |
| `make_array_increasing_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap` rebuilt for each element through `entry(..).or_insert(i32::MAX)`), carried to Kāra by `karac fix` |
| `make_array_increasing_chain.kara` | another Rust solution, in iterator chains (a `fold` over `arr1` seeded with `BTreeMap::from([(-1, 0)])`, `entry(..).and_modify(..).or_insert(..)`, `arr2.get(arr2.partition_point(..))`, and `dp.values().copied().min().unwrap_or(-1)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, seven properties |

Every arm prints the same 10 lines: LeetCode's three examples; one value
already in order (`small 1: 0`); a falling array (`small 2: 2`); a repeat
`arr2` cannot break (`small 3: -1`); the values' extremes (`small 4: 2`);
2000 random pairs of 1 to 8 values (`2000 random pairs: checksum
144949708`); 2000 values in each array up to `10^9`, the constraints' most
(`2000 and 2000 values: 1998`); and 2000 rising values with one dip
(`2000 rising, one dip: 1`). `make_array_increasing.py` mirrors the ★ arm
and its output is byte-identical; it also checks every answer for arrays of
at most 6 values against the statement read literally. Every arm gives the
same output under `karac run` and `karac build`.

The Mend loop: the ★, map and memo arms copy `arr2` before sorting it
(`arr2.clone()`); a bare parameter borrows, and `karac check` refuses the
sort in place with a fix to `mut ref`, which would sort the caller's array.
The solution arm takes one round of 25 fixes (among them `HashMap<i32,
i32>` to `Map[i32, i32]`, `sort_unstable` to `sort`, the `&` of `for &a`
and `|&x|`, and `arr2: own Vec[i32]` for its `let mut arr2 = arr2;`) and its
output matches. The chain arm takes one round of 26 (among them `mut arr2:
Vec<i32>` to `arr2: own Vec[i32]` and a `let mut`, `BTreeMap::from` to
`SortedMap.from`, `for (&prev, &ops) in &dp` to `for (prev, ops) in ref
dp`, `|v: &mut i32| *v = ..` to `|v: mut ref i32| { *v = ..; }` and
`copied()` to `cloned()`) and its output matches, after the fix below.

## Gaps

The chain arm found one, fixed in kara.

- **A constructor seed's numbers were fixed at the call.**
  `arr1.iter().fold(SortedMap.from([(-1, 0)]), |dp, a| ..)` over `i32`
  items was refused, "expected 'SortedMap[i64, i64]', found
  'SortedMap[i32, i32]'", with no fix, where `fold(0, ..)` and `fold([0],
  ..)` take the closure's type. A constructor of a list of literals given to
  a parameter the call returns now keeps the list's numbers open, a list of
  tuple literals is open as a list of literals is, and a number no use has
  fixed yet binds by value out of a borrowed tuple, as a fixed one does.
  kara B-2026-11-17-115.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every choice, for each element, of keeping it or setting it to a
value of `arr2`, the fewest changes among the choices that leave `arr1`
strictly increasing, or `-1`. 2000 random pairs of 1 to 8 values in
`0..span` for a span of 2 to 13; the first hundred with `arr1` already
rising, the next hundred with one value in `arr2`, the next hundred with
`arr1` one value repeated.

| | property |
|---|---|
| P1 | the statement read literally, on arrays of at most 5 values |
| P2 | `-1` exactly when no choice leaves `arr1` strictly increasing (the least value each position can take, from the left) |
| P3 | `0` exactly when `arr1` already rises |
| P4 | the kept elements rise, so `n - (longest rise) <= answer <= n` |
| P5 | one more value in `arr2` never makes the answer worse |
| P6 | `arr2`'s order and repeats do not matter |
| P7 | the ★ arm's answer |

All 64,200 checks pass on every arm: `2000 pairs: checksum 905817898,
64200 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac build`.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All ten
are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: an element kept when it only equals the end | P1 219, P2 257, P3 219, P4 333, P7 1860 |
| A2 | ★: a replacement may equal the end | P1 366, P2 1061, P7 4724 |
| M1 | map: a kept entry overwrites a better one | P1 45, P3 55, P5 10, P7 84 |
| M2 | map: the most replacements taken at the end | P1 279, P3 318, P5 99, P7 555 |
| E1 | memo: an element kept when it only equals `prev` | P1 219, P2 257, P3 219, P4 333, P7 465 |
| E2 | memo: an unreachable end not mapped to `-1` | P1 334, P2 1061, P4 1061, P7 1061 |
| X1 | solution: a replacement costs nothing | P1 245, P3 512, P4 512, P7 512 |
| X2 | solution: the start is 0, not below every value | P1 150, P2 167, P3 127, P7 292 |
| R1 | chain: a first replacement costs nothing | P1 245, P3 512, P4 512, P7 512 |
| R2 | chain: a replacement may equal the end | P1 366, P2 1061, P7 1181 |

A mutation of the ★ arm fails P7 on every arm. A1 and E1 are one fault in
two arms, an equal value taken as rising, and fail P1 to P4 alike; X1 and
R1 are one fault too, a replacement counted as free. P2 catches the faults
that reach an end no choice reaches, or miss one (A1, A2, E1, E2, X2, R2).
M1 is the weakest catch, 194 failures: the overwrite loses only when a kept
element meets an end of `arr2` on the same value with fewer replacements,
which the small spans make common enough. P6 catches
none, since no mutation reads `arr2`'s order or repeats.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 4 pairs of 2000 values each, the constraints' most, built once
(both random up to 10^9; a rising `arr1` with a dip every 40 values; both
random below 4000; a falling `arr1`); then 6 rounds over the pairs, each
answer folded into a checksum. Every program prints `6 rounds of 4 pairs
of 2000 values: checksum 142360101`. Each call sorts and dedups a copy of
`arr2` and builds a fresh row of `n + 1` ends for every element of `arr1`;
the search is the library's partition point in Kāra, Rust (`partition_point`)
and Go (`sort.Search`), and a hand-written binary search in C.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `4fa402bc9d`
and this kata's fix, on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.193 to 0.299 s | 0.215 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.197 to 0.249 s | 0.218 s |
| Rust (`rustc -O`) | 0.246 to 0.321 s | 0.264 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.265 to 0.319 s | 0.280 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.238 to 0.291 s | 0.269 s |
| C (`clang -O3`) | 0.226 to 0.265 s | 0.235 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.252 to 0.279 s | 0.266 s |
| Go | 0.504 to 0.583 s | 0.548 s |
| Python | 9.09 to 9.38 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 5% of wall time for both Kāra
rows, so both ran on one core. Here the gap is in user time too (median
0.21 s for Kāra, 0.23 s for C, 0.26 s for Rust), so it is in the code each
compiler made for the inner loop, not the kernel's; no profile was taken,
so which instructions differ is not known. Go's user time is above its
wall time, its collector running beside it. Python takes about 42x Kāra's
time.
