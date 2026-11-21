# 1743. Restore the Array From Adjacent Pairs

There is an integer array `nums` that consists of `n` **unique** elements,
but you have forgotten it. However, you do remember every pair of
adjacent elements in `nums`.

You are given a 2D integer array `adjacentPairs` of size `n - 1` where
each `adjacentPairs[i] = [ui, vi]` indicates that the elements `ui` and
`vi` are adjacent in `nums`.

It is guaranteed that every adjacent pair of elements `nums[i]` and
`nums[i+1]` will exist in `adjacentPairs`, either as `[nums[i],
nums[i+1]]` or `[nums[i+1], nums[i]]`. The pairs can appear **in any
order**.

Return *the original array* `nums`*. If there are multiple solutions,
return **any of them***.

```
adjacentPairs = [[2,1],[3,4],[3,2]]     ->  [1,2,3,4]
adjacentPairs = [[4,-2],[1,4],[-3,1]]   ->  [-2,4,1,-3]
adjacentPairs = [[100000,-100000]]      ->  [100000,-100000]
```

**Constraints:** `nums.length == n`; `adjacentPairs.length == n - 1`;
`adjacentPairs[i].length == 2`; `2 <= n <= 10^5`; `-10^5 <= nums[i], ui,
vi <= 10^5`; there exists some `nums` that has `adjacentPairs` as its
pairs.

## Approaches

| file | mechanism |
|---|---|
| `restore.kara` ★ | the values are distinct, so the pairs make a path: each value's neighbours go in a `Map[i32, Vec[i32]]`, an end is a value with one neighbour, and from it each next value is the neighbour of the last that is not the one before it. O(n) |
| `restore_xor.kara` | each value keeps only how many neighbours it has and their XOR, in a `Map[i32, (i32, i32)]`; from an end, the next value is the last one's XOR with the value before it taken out. O(n) |
| `restore_sorted.kara` | no hashing: every pair written both ways and sorted, so a value's neighbours sit together and `partition_point` finds them; an end is a value at the front of one edge only. O(n log n) |
| `restore_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashMap<i32, Vec<i32>>` filled through `entry(..).or_default()`, an end found by a `for (&k, v) in &g` scan, and the path walked into a `vec![0; n]`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

The array read backwards is an answer too, and the end an arm starts
from comes from a `Map` walk in three of the arms, whose order is the
per-process hash order. So the harness prints every answer from its
smaller end, which makes the output the same on every run and every
backend; LeetCode's third example therefore prints as `[-100000,
100000]` and its second as `[-3, 1, 4, -2]`.

Every arm prints the same 7 lines: LeetCode's three examples and three
values with both pairs reversed; then the smaller ends summed and a
checksum over every value for 3000 random arrays of 2 to 8 values, 300
of up to 1000 and 10 of up to `10^5`, LeetCode's largest, of distinct
values from `-10^5` to `10^5`, each given as its pairs shuffled, each
pair in a random order. `restore.py` mirrors the ★ arm and its output
is byte-identical.

```
[1, 2, 3, 4]
[-3, 1, 4, -2]
[-100000, 100000]
[1, 2, 3]
3000 arrays of up to 8 values: first values sum to -100277987, checksum 629592475
300 arrays of up to 1000 values: first values sum to -8834556, checksum 91205841
10 arrays of up to 100000 values: first values sum to -552095, checksum 627184340
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every order of the values, tried in turn, until one has
exactly the given adjacent pairs. It checks 3000 random arrays of 2 to 6
distinct values from -50 to 50, given as their pairs shuffled. Every
case is drawn before any arm answers, and every answer is compared from
its smaller end.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer holds n values whose adjacent pairs are exactly the given ones |
| P3 | the pairs listed backwards, each one reversed, give the same answer |
| P4 | every value plus 7 gives the answer plus 7 |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 362130265, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and in Python
the array the pairs were drawn from, read from its smaller end, gives
the same checksum. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Ten edits to the differential, two to three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed. Four
of them, M1, M2, M8 and M9, give wrong answers that depend on which end
the `Map` walk reaches first, so their counts change from run to run;
the table shows them under `KARAC_HASH_SEED=1`, where both backends give
the same counts. M3, M4 and M10 send the walk to a value that is not in
the map, and M5 reads past the sorted edges; each ends the run with exit
101 and no count, the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each next value the last one's first neighbour, whichever it is | P1 1778, P2 1778, P3 1778, P5 1778 |
| M2 | ★: the walk stopped one value short | P1 2423, P2 2423, P3 1696, P5 2423 |
| M3 | xor: neighbours ORed in, not XORed | panics: key not found |
| M4 | xor: the walk started from any value, not an end | panics: key not found |
| M5 | sorted: ends sought one edge at a time, not two | panics: index out of bounds |
| M6 | sorted: each next value the first neighbour, whichever it is | P1 2382, P2 2382, P5 2382 |
| M7 | sorted: the value before set to the next one, not the last | P1 2382, P2 2382, P5 2382 |
| M8 | solution: the neighbour taken is the one before, not the other | P1 2423, P2 2423, P3 1696, P5 2423 |
| M9 | solution: the second value the first again | P1 3000, P2 3000, P3 2273, P5 3000 |
| M10 | xor: the second value the end itself | panics: key not found |

## Benchmarks

The bench draws 10 random arrays of `10^5` distinct values from `-10^5`
to `10^5`, LeetCode's limits, each given as its pairs shuffled, all of
them first, then restores each 4 times by the ★ arm in all five
languages: Kāra's `Map[i32, Vec[i32]]`, Rust's `HashMap<i32, Vec<i32>>`,
Go's `map[int32][]int32`, Python's `dict`, and in C an open-addressing
hash table written for the bench. Every restore rebuilds its map. Every
implementation prints `10 arrays of 100000 values, 4 rounds: smaller
ends sum to -1687712, checksum 172972578`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.329 s |
| Rust (`rustc -O`) | 1.514 s |
| Go | 1.649 s |
| Kāra (`karac build`) | 1.682 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.696 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.696 s |
| Python | 7.2 s |

The sequential Kāra build takes 1.12x Rust's time and 1.00x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.329 s, 5 times ahead, because its table holds
at most two neighbours in each slot, where the others allocate a
growable list for every value.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.734 s and 1.770 s on one
run).

## Verification

All four arms print the same output as `restore.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error,
and the three `Map` arms do so under `KARAC_HASH_SEED` 1, 7 and 99 as
well. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`21cdf88b69`.

## Writing it

The ★ arm took one `karac fix`: `let near = next[last]`, a move of a
`Vec` out of an index, became `let near = ref next[last]`, since it is
only read. The harness's `canonical`, which reverses its argument in
place, took `order: own Vec[i32]` from the same fix in every arm. The
XOR and sorted arms needed nothing else.

LeetCode's Rust template took one `karac fix` of 22 edits: the `use
std::collections::HashMap` line deleted and `struct Solution {}` added,
`Vec<..>` and `HashMap<..>` written `Vec[..]` and `Map[..]`,
`HashMap::new()` written `Map.new()`, `&adjacent_pairs` and `&g` in the
`for` loops written `ref adjacent_pairs` and `ref g`, `or_default()`
written `or_insert(Vec.new())`, `vec![0; n]` written `Vec.filled(n,
0)`, the `&k` pattern written `k`, and `&g[&ans[i - 1]]` written `ref
g[ans[i - 1]]`. The scan's `break` on the first end and the `if v[0] ==
ans[i - 2]` walk carried over as written.

The differential checked clean as generated.
