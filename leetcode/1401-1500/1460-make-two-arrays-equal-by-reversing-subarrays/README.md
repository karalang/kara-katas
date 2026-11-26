# 1460. Make Two Arrays Equal by Reversing Subarrays

You are given two integer arrays of equal length `target` and `arr`. In
one step, you can select any non-empty subarray of `arr` and reverse it.
You are allowed to make any number of steps. Return `true` if you can
make `arr` equal to `target` or `false` otherwise.

```
target = [1,2,3,4], arr = [2,4,1,3]   ->  true
target = [7], arr = [7]               ->  true
target = [3,7,9], arr = [3,7,11]      ->  false
```

**Constraints:** `target.length == arr.length`, `1 <= target.length <=
1000`, and `1 <= target[i], arr[i] <= 1000`.

The arms are `fn can_be_equal(target: Vec[i32], arr: Vec[i32]) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `can_be_equal.kara` ★ | a reversal of two neighbours is a swap and swaps sort anything, so the two can be made equal exactly when they hold the same values: both cloned, sorted and compared with `==`. O(n log n) |
| `can_be_equal_counts.kara` | each value counted up in `target` and down in `arr` in one `[0; 1001]`, walking the two together by `zip` and indexing by `t as usize`, and every count 0 at the end through `iter().all(..)`. O(n + 1000) |
| `can_be_equal_map.kara` | a `Map[i32, i64]` tally of each array by `*seen.entry(v).or_insert(0) += 1`, and the two maps compared with `==`. O(n) |
| `can_be_equal_reverse.kara` | the reversals made: for each place in turn the next copy of the value `target` wants there is found in the rest of `arr` by `(i..arr.len()).find(..)`, with `let .. else` returning `false` when there is none, and the stretch from the place to it reversed in place by `arr[i..=j].reverse()`. O(n^2) |
| `can_be_equal_solution.kara` | a Rust solution as LeetCode's Rust users write it (both arrays taken as `mut` parameters, sorted in place by `sort_unstable` and compared with `==`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's four examples and three
more, one value against another, and 1 to 1000 against itself reversed
and against that with one value changed (`true true false true false
true false`); the constraints' most, 1000 values from 1 to 1000 against
them shuffled (`1000 shuffled: true`); and 3000 random pairs of 1 to 60
values from 1 to top, top from 1 to 20, a third shuffled, a third
shuffled with one value changed and a third drawn apart (`3000 random
pairs: 1232 equal, checksum 43380096`). `can_be_equal.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, counts, map and reverse arms check clean as first
written. The Rust solution takes one round of 13 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `Vec<i32>` to
`Vec[i32]`, each `mut target: Vec<i32>` parameter to `target: own
Vec[i32]` with `let mut target = target;` at the body's start, and
`sort_unstable` to `sort`. The parameters' `own` carries to the
harness's `can_be_equal` that calls the method, and from there to its
caller, where `up`, passed twice, is cloned at the first use. Every
arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a breadth-first search over the arrays `arr` can become, each
step reversing one stretch, with `target` among them, while there are at
most 6 values. LeetCode's examples, four edge cases (two values swapped,
the same values with one more copy of one and one fewer of another, and
a repeated value against its copies in another order), the two arrays of
1000 above, the constraints' most, and 1992 random pairs, half of 1 to 6
values and half of 1 to 60, drawn as the harness draws them.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 6 values |
| P2 | the two swapped give the same answer |
| P3 | `target` reversed gives the same answer |
| P4 | `arr` shuffled gives the same answer |
| P5 | each against itself is true, and the two false when their sums differ |
| P6 | the ★ arm's answer |

All 55,600 checks pass on every arm: `2003 cases: checksum 566897302,
55600 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, comparing
`Counter`s, gives the same checksum.

The fixed cases are a typed list of tuples written as Rust writes them,
`[([1, 2, 3, 4].to_vec(), [2, 4, 1, 3].to_vec()), ..].to_vec()` into a
`Vec[(Vec[i32], Vec[i32])]`. Check refused each tuple, its `.to_vec()`
list taking the default `i64` where the slot names `i32`: the slot's
type reached a `[..].to_vec()` at a `let` of its own but not one inside
a tuple. That was B-2026-11-26-78, fixed at a648c7a471.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: `arr` never sorted | P1 249, P2 70, P4 63, P5 1648, P6 2332 |
| M2 | ★: any two arrays of one length taken as equal | P1 643, P5 1145, P6 4652 |
| M3 | counts: every count even taken as 0 | P1 7, P5 21, P6 21 |
| M4 | counts: a value of `target` counted once however often it is there | P1 245, P2 27, P3 156, P4 112, P5 11, P6 579 |
| M5 | map: each value counted once however often it is there | P1 41, P5 374, P6 378 |
| M6 | map: the two tallies compared by how many values they hold | P1 407, P5 779, P6 790 |
| M7 | reverse: the value already in place never found there | P1 462, P5 2003, P6 840 |
| M8 | reverse: the stretch never reversed | P1 252, P2 79, P3 178, P4 139, P5 27, P6 588 |
| M9 | solution: `arr` never sorted | P1 249, P2 70, P4 63, P5 1648, P6 583 |
| M10 | solution: the sorted arrays compared with `<=` | P1 309, P2 1163, P5 572, P6 579 |

## Benchmarks

The bench draws 200 pairs of 1000 values from 1 to 1000, the
constraints' most, once, each `arr` a shuffle of its `target`; then
makes 50 passes, each setting one value of every `arr` to a value of its
`target` chosen from the checksum so far, so no answer carries over,
answering it with the ★ arm and folding the answer into the checksum.
Each implementation copies both arrays and sorts them with its library's
sort: Rust's `sort`, C's `qsort` with a comparison function, Go's
`slices.Sort` and Python's `sorted`. Every implementation prints `50
passes over 200 pairs of 1000 values: checksum 601617370`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.23 s against Rust's 0.33 s (0.32 s with
overflow checks on), C's 1.6 s and Go's 1.3 s; Python takes 2.6 s.
