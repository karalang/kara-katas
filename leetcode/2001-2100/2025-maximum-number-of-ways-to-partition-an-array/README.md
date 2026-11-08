# 2025. Maximum Number of Ways to Partition an Array

You are given a 0-indexed integer array `nums` of length `n` and an
integer `k`. A pivot is an index `p` with `1 <= p < n` where the values
before it and the values from it on have the same sum:
`nums[0] + .. + nums[p - 1] == nums[p] + .. + nums[n - 1]`. You may change
the value of at most one element to `k`, or leave the array as it is.
Return the most pivots the array can have after at most one change.

```
nums = [2,-1,2],  k = 3    ->  1
nums = [0,0,0],   k = 1    ->  2
nums = [22,4,-25,-20,-15,15,-16,7,19,-10,0,-13,-14],  k = -33  ->  4
```

**Constraints:** `2 <= n <= 10^5`; `-10^5 <= k, nums[i] <= 10^5`.

Let `d[p]` be the sum before pivot `p` minus the sum from it on. Changing
`nums[i]` to `k` adds `delta = k - nums[i]` to every `d[p]` with `i` before
the pivot (`p > i`) and takes it from every `d[p]` with `i` after it
(`p <= i`). So the change at `i` balances the pivots after it with
`d[p] = -delta` and the pivots up to it with `d[p] = delta`, and the
answer is the best of those counts and the count of `d[p] = 0`.

## Approaches

| file | mechanism |
|---|---|
| `partition.kara` ★ | the differences `d` in a `Vec`, then two `Map`s of their counts, one for the pivots after `i` and one for those up to it, a pivot moving from one to the other as `i` sweeps. O(n) |
| `partition_brute.kara` | every array the rules allow, as given and with each value in turn changed to `k`, its pivots counted by a running left sum against the total. O(n^2) |
| `partition_passes.kara` | one array of answers: a pass from the left adds the pivots up to `i` with `d = delta`, a pass from the right those after it with `d = -delta`, each pass with one `Map` of the pivots behind it, cleared between them; the unchanged count by `skip`, `filter` and `count`, the best by `fold` |
| `partition_search.kara` | a `Map` from each `d` to its pivots in order; the change at `i` counts the pivots at or before `i` with `partition_point`, and the rest by subtraction. O(n log n) |
| `partition_sorted.kara` | the ★ sweep over two `SortedMap`s, with the differences worked out as the sweep reaches them: `take(n - 1)` builds the right side, `enumerate()` drives the sweep |
| `partition_solution.kara` | LeetCode's Rust template (`use std::collections::HashMap`, `impl Solution` before the unit struct, `vec![0i64; n + 1]`, `nums[i] as i64`, `get(&0).unwrap_or(&0)`, `get_mut(&d).unwrap()`, `get(&-delta).copied()`, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the total and a checksum of the answers for
3000 arrays of 2 to 20 values from `-r` to `r`, `r` from 1 to 5, and for 5
arrays of 1500 values, `r` from 1 to 100000. `partition.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the array as given and with each value in turn changed to `k`,
every pivot's two sums added up afresh, and the most balanced pivots any of
them has. It checks 1500 problems of 2 to 12 values from `-r` to `r`, `r`
from 1 to 4, with `k` from the same range; small values make balanced
pivots common. Every random choice of a problem is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed leaves the answer |
| P3 | every value and `k` negated leave the answer |
| P4 | every value and `k` doubled leave the answer |
| P5 | the answer is at least the unchanged array's count and at most `n - 1` |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a pivot `p` of the array is the pivot `n - p` of its
reverse, with the two sums swapped, and the change at `i` is the change at
`n - 1 - i`. P3 and P4 hold because negating or doubling every value
negates or doubles both sums of every pivot, and a sum is equal to another
exactly when its negation or double is.

The differential prints `1500 problems: checksum 708917681, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Sixteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the unchanged count never taken | P1 63, P5 63, P6 63 |
| M2 | ★: a moved pivot left on the right too | P1 569, P2 459, P5 29, P6 569 |
| M3 | ★: the last value never changed | P1 118, P2 221, P6 118 |
| M4 | brute: the left sum missing the first value | P1 736, P2 584, P5 81, P6 736 |
| M5 | brute: each value changed to `k + 1` | P1 845, P3 772, P4 912, P6 845 |
| M6 | brute: a pivot balanced when its sums are equal in size | P1 360, P2 493, P6 360 |
| M7 | passes: the map not cleared between the passes | P1 1011, P2 767, P5 135, P6 1011 |
| M8 | passes: the first value never changed | P1 103, P2 221, P6 103 |
| M9 | passes: the unchanged count taking `d[0]`, which is no pivot | P1 570, P5 29, P6 570 |
| M10 | search: the change scored on one side only, the larger | P1 245, P6 245 |
| M11 | search: the pivots grouped by half their difference | P1 876, P4 747, P6 876 |
| M12 | sorted: the second value added to the left sum twice | P1 472, P2 648, P5 4, P6 472 |
| M13 | sorted: the left side looked up on the right | P1 688, P2 758, P5 24, P6 688 |
| M14 | sorted: `delta` from the value's size | P1 369, P3 662, P6 369 |
| M15 | Rust: every prefix sum from the third on missing the first value | P1 706, P2 741, P5 95, P6 706 |
| M16 | Rust: a moved pivot taken off the right twice | P1 158, P2 242, P6 158 |

P1 and P6 kill all sixteen, P2 ten, P5 eight, P3 two and P4 two. P2
reverses the array, which turns the pivots up to `i` into the pivots after
it; it sees every edit that treats the two sides or the two ends unevenly:
a side mishandled (M2, M7, M13, M16), an end never changed (M3, M8), a sum
short at its start (M4, M12, M15), a balance by size (M6). It misses the
edits that are symmetric: both sides scored the larger (M10), the halved
key (M11), and the edits on `k` or the values' signs (M5, M14) and on the
unchanged count alone (M1, M9). P5 bounds the answer by the unchanged
count and `n - 1`; it sees an edit that loses the unchanged count (M1),
counts a pivot that is not one (M9, the unset `d[0]`, always 0), or
counts more pivots than there are (M2, M4, M7, M12, M13, M15). P3 negates
every value and `k`, which an edit sees only if it reads a sign: `k + 1`
(M5) and the value's size (M14). P4 doubles them, which an edit sees only
if it adds a constant or divides: `k + 1` again (M5) and the halved key
(M11).

The other fourteen fail as a kept one does, or with counts of their own.
The ★ arm's sides swapped and the search arm's `delta` written the other
way round both fail P1 and P6 710 times; the ★ arm's pivot moved a place
late and the search arm counting the pivots strictly before `i` fail
alike (P1 344, P2 443), as do M2, the search arm counting every pivot
after `i` from the start and the Rust arm never taking a moved pivot off
the right; the passes arm's forward sign flipped and the Rust arm reading
the left side at `-delta` both fail P1 539, P2 629. The brute arm never
putting the changed value back (P1 821, P2 453) and its last pivot never
counted (P1 428, P2 432, P5 96), the passes arm's backward pass one pivot
early (P1 391, P2 528), and the sorted arm's last prefix taken as a pivot
(P1 359, P5 19) and a pivot moved at the first value (P1 357, P5 12) fail
with counts of their own; the Rust arm's unchanged count never taken fails
as M1. Two drafts were replaced. The Rust arm's pivots counted from 2 left
a pivot out of the map that `get_mut(d).unwrap()` then asked for, so it
crashed rather than failed. And the Rust arm's answer started at a bare
`let mut ans = 0` did not check at all: `ans.max(ways)` with `ways: i32`
is refused, since a method receiver does not fix a literal's type
(design.md § Type inference); B-2026-11-08-20 asks for a machine fix
there.

## Verification

Every arm prints the same output as `partition.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.6 s to 8.0 s (brute) and the
differential 3.0 s.

The five arms were written in Kāra. Four checked clean with no fix; the
search arm was first written with Rust's `binary_search` returning
`Ok(at)` or `Err(at)` and a `ref` at a call site. `karac fix` dropped the
`ref`; Kāra's `binary_search` returns `Option[i64]`, the index of an equal
element, so the arm now asks `partition_point(|p| p <= i)`, which is the
count it needs.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in four rounds (22, 4, 4 and 2 edits). The
first carries the `Vec<..>` and `HashMap<..>` types, the `::` paths, the
unit struct, the `&` in `get(&0)`, `unwrap_or(&0)`, `get_mut(&d)` and
`get(&-delta)`, the `&x` closure pattern and the `&Vec` parameter, and
drops the `use`; the second renames `HashMap` to `Map`; the third drops
the `i64` suffix in `vec![0i64; n + 1]` and the `as i64` on `nums[i]`, a
widening Kāra does by itself, and turns `copied()` into `cloned()`; the
fourth turns the `vec!` into `Vec.filled(n + 1, 0)` and drops the wrapper's
`ref`. The prefix sums stay `i64`: the literal `0` keeps its default, and
`pre[i] + nums[i]` widens the `i32`.

## Benchmarks

The bench builds 20 arrays of 50000 values from `-r` to `r`, `r` from 1 to
100000, each with a `k` from the same range, once in all five languages,
and runs the ★ arm on each for 10 rounds: 200 calls. Every implementation
prints `200 calls: total 26560, checksum 669266848`. Every language keeps
the two sides in a hash map of its own (C with an open addressing table),
as the Kāra program does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.488 to 0.552 s | 0.499 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.890 to 1.071 s | 0.907 s |
| Kāra (`karac build`) | 0.875 to 1.107 s | 0.938 s |
| Rust (`rustc -O`) | 0.984 to 1.163 s | 1.007 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.990 to 1.115 s | 1.027 s |
| Go | 1.097 to 1.196 s | 1.157 s |
| Python | 5.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.922 s) is not above its real time (0.938 s).

The sequential Kāra program is 0.88x Rust under overflow checks and 1.82x
C.