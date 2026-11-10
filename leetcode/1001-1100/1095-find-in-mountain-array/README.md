# 1095. Find in Mountain Array

An array `arr` is a mountain array if `arr.length >= 3` and there is some
`i` with `0 < i < arr.length - 1` such that `arr[0] < arr[1] < ... <
arr[i]` and `arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`.

Given a mountain array `mountainArr`, return the minimum index such that
`mountainArr.get(index) == target`. If no such index exists, return `-1`.

You cannot access the mountain array directly, only through a
`MountainArray` interface: `MountainArray.get(k)` returns the element at
index `k` (0-indexed), and `MountainArray.length()` returns its length.
Submissions making more than 100 calls to `MountainArray.get` are judged
wrong.

```
array = [1,2,3,4,5,3,1], target = 3  ->  2
array = [0,1,2,4,2,1],   target = 3  ->  -1
```

**Constraints:** `3 <= mountainArr.length() <= 10^4`;
`0 <= target <= 10^9`; `0 <= mountainArr.get(index) <= 10^9`.

The arms are `fn find_in_mountain_array(target: i32, mountain:
MountainArray) -> i32`, over a `MountainArray` holding a `Vec[i32]` and
an `Atomic[i64]` that counts the calls of `get`. The interface is in
`i32`, as LeetCode gives it, so every index the arms compute is an
`i32` too.

## Approaches

| file | mechanism |
|---|---|
| `find_in_mountain_array.kara` ★ | three binary searches: the peak (the first index whose value is above the next), then the rising side, then the falling side, so the smaller index wins. Two calls per step of the peak search and one per step of each side; 53 is the most measured at n = 10^4 |
| `find_in_mountain_array_keyed.kara` | one search, `first_at_least(lo, hi, at_least: Fn(i32) -> bool)`, for everything: the peak is the first index past which the mountain falls, and each side is searched for the first key at least the target's, the key being the value on the rising side and its negation on the falling side. The two sides are a `for (lo, hi, sign) in [..]` over tuples |
| `find_in_mountain_array_recursive.kara` | recursion: the peak by halving the range toward the rising slope, and each side by a binary search told which way it runs, returning `Option[i32]`; the falling side is an `or_else` after the rising one |
| `find_in_mountain_array_cached.kara` | every value read once: a `Map[i32, i32]` in front of `get`, so the peak search's two reads per step and the side searches never ask the mountain twice for one index; the sides `match` on `cmp` |
| `find_in_mountain_array_ternary.kara` | the peak by ternary search, two probes a third of the way in from each end, then the two sides by `partition_point` over an index range collected into a `Vec[i32]` |
| `find_in_mountain_array_solution.kara` | LeetCode's Rust template (`impl Solution`, `mountainArr: &MountainArray`, `let (mut l, mut r) = (0, n - 1)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 24 lines: the answers and whether at most 100
calls were made for LeetCode's two examples and nine more (the peak, the
first and the last index, a target above the peak, a value on both
sides, a target missing between two values, a target of 10^9), then over 2000 random mountains of 3 to
61 values how many targets were found and how many took over 100 calls
(`1518 found, 0 over 100 calls, checksum 652413453`), and three
mountains of 10^4 values, LeetCode's longest, with the peak near either
end and in the middle, each asked for a target on each side and at the
peak. `find_in_mountain_array.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms, one `MountainArray`,
and the statement read literally: the first index whose value is the
target, found by walking the array. It checks 2000 problems in four
kinds of 500: random mountains of 3 to 61 values rising and falling by 1
to 4, the target one of the values or next to one; mountains rising and
falling by 1, so most values sit on both sides, the target one of them;
long mountains of 1000 to 6000 values with the peak within 5 of either
end, rising and falling by up to 50000; and mountains of 3 to 5 values
from 0 to 9, the target 0 to 10. Every random choice is drawn before
any arm answers, and the calls of `get` are counted per arm.

| | property |
|---|---|
| P1 | the answer is the literal first index holding the target, or -1 |
| P2 | at most 100 calls of `get` |
| P3 | the first value is found at 0 and the peak's value at the peak; the last value at the end, or on the rising side where it is there too; a value above the peak, or below both ends, is not found |
| P4 | every value moved up by the same amount, with one less than the old first value put in front: the target moved up is found one index on, or at 0 when it is that new first value |
| P5 | the mountain reversed: a target not found is still not found, and a found one is found where its last copy is, never before the first |
| P6 | every value doubled, with a value between each pair of neighbours (so value i sits at index 2i): the target doubled is found at twice the index |

All 72,000 checks pass on every arm: `2000 problems: checksum
819127475, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems gives the same checksum.

P1 and P3 lean on the literal array: the first index, the peak, the
ends. P2 counts calls and P4 to P6 compare the arm only with itself, on
a mountain built from the first.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the peak sought in the first half only | P1 214, P3 554, P4 20, P5 356, P6 17 |
| M2 | ★: the peak in neither side | P1 66, P3 2000 |
| M3 | ★: the falling side searched as rising | P1 476, P3 1169, P5 932, P6 33 |
| M4 | ★: the index after the peak never searched | P1 52, P3 283, P5 92, P6 52 |
| M5 | keyed: the first rising index taken as the peak | P1 1274, P3 1928, P4 150, P5 105, P6 3 |
| M6 | keyed: the last index of a side never found | P1 124, P3 2000, P5 99 |
| M7 | keyed: the first key above the target, not at it | P1 1546, P3 2000, P4 65 |
| M8 | recursive: one index skipped going left | P1 499, P3 824, P4 315, P5 558, P6 702 |
| M9 | recursive: the falling side first | P1 451, P3 497, P4 23, P5 451 |
| M10 | cached: the cache read under the next index | P1 788, P3 1852, P4 613, P5 834, P6 903 |
| M11 | cached: index 0 never searched | P1 62, P3 2000, P4 127, P5 104 |
| M12 | cached: the last index never searched | P1 58, P3 1452, P5 99 |
| M13 | ternary: up to 200 candidates for the peak read one by one | P2 764 |
| M14 | ternary: the second probe at the end | P2 262 |
| M15 | solution: an absent target answered 0 | P1 454, P3 2000, P4 412, P5 454 |

P1 and P3 catch thirteen of the fifteen, P5 eleven, P4 eight, P6 six
and P2 two. The two P1 misses are the ternary arm's: a peak search that
reads up to 200 candidates one by one (M13), or puts its second probe at
the end of the range (M14), still finds the right index, only with more
than 100 calls of `get`, and only P2 sees them. P4 to P6, which compare
the arm only with itself, catch twelve. Besides those two they miss
only the peak in neither side (M2): moving, reversing or doubling the
mountain keeps the peak the peak, so the arm misses it on both
mountains alike.

Of the fifteen not kept, eight fail exactly as a kept edit: M2 is also
the keyed and recursive arms leaving the peak out of both sides; M3 is
also the recursive, cached and solution arms searching the falling side
as rising; M4 is also the ternary arm skipping the index after the peak
and the solution arm taking the peak one too far; M12 is also the
solution arm never searching the last index. The other seven fail in
ways of their own but were not needed: the ★ rising search stopping
with one index left, the keyed arm keying the falling side as rising,
the recursive arm never reading a range of one index, the cached arm
caching a value under the next index, the ternary arm dropping the wrong
third and never taking its first candidate, and the solution arm's peak
search turned round. Three earlier edits turned out to be equivalent
and were replaced: the recursive peak search stopping at two indices
left, the cached peak search never reaching the next to last index, and
the ternary arm not reading its last candidate. Each moves the split one
index, and the peak then lies at the start of the falling side, where
the falling search finds it as well.

## Verification

Every arm prints the same output as `find_in_mountain_array.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found one gap, fixed in the compiler:

- Every arm's binary search starts as Rust writes it, `let mut lo = 0;`
  beside `hi = n - 1` with `n: i32`. Kāra keeps an unsuffixed literal
  at `i64` beside a narrower integer (design.md §8), so `mid = (lo +
  hi) / 2` is an `i64`, and `mountain.get(mid)`, `hi = mid` and `return
  mid` were each refused with only "write an explicit 'as i32'".
  `karac fix` already annotated the binding when the refused value was
  the binding itself, but here it is computed from it, and nothing was
  applied. Three shapes met it: a value computed from a literal
  binding, the same from a tuple `let mut (l, r) = (0, n - 1)`, and a
  `for (lo, hi, sign) in [(0, peak, 1), ..]` over tuples. A refused
  value that is an arithmetic tree over one literal binding and narrower
  integers now names that binding, and `karac fix` writes `lo: i32`, or
  `0i32` in the tuple or the array of tuples (kara B-2026-11-10-30,
  pinned by `tests/kata_1095_literal_index_annotation.rs`).

With that, `karac fix` makes every change the arms needed: `let mut lo:
i32 = 0;` in the ★ arm, `0i32` in the keyed arm's tuples and in the
cached and ternary arms' tuple lets. The recursive arm needed none. The
ternary arm's `partition_point(..) as i32` is written by hand, as Rust
needs it too. LeetCode's template reaches a clean check in five rounds:
the syntax (`&MountainArray` to `ref MountainArray`, `let (mut l, mut
r)` to `let mut (l, r)`), then `struct Solution {}`, then `0i32` in the
first tuple and, once that is typed, in the second, then the `ref`
dropped, since a parameter borrows already.

## Benchmarks

The bench builds 64 mountains of 10^4 values once, LeetCode's longest,
their peaks spread from one end to the other, rising and falling by up
to 50000. Each of 100 rounds asks every mountain for 64 targets, each a
value of the mountain or one next to it, with the ★ arm: 409,600
searches and 19.6 million calls of `get`, each an atomic increment.
Every implementation prints `100 rounds over 64 mountains of 10^4
values: 136529 of 409600 found, 19612141 calls of get, checksum
252835963`. C counts with `__atomic_fetch_add`, Rust with `AtomicI64`,
Go with `atomic.Int64`, as Kāra's `Atomic[i64]` does; Python with a
plain integer.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.155 to 0.173 s | 0.162 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.155 to 0.178 s | 0.164 s |
| Rust (`rustc -O`) | 0.161 to 0.180 s | 0.170 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.162 to 0.206 s | 0.170 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.158 to 0.193 s | 0.170 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.163 to 0.197 s | 0.171 s |
| Kāra (`karac build`) | 0.159 to 0.215 s | 0.175 s |
| Go | 0.178 to 0.218 s | 0.198 s |
| Python | 3.960 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra, C and Rust sit within the spread of one another, every one
paying for the same 19.6 million atomic increments; Go takes about 1.15x
their time. Python takes about 23x Kāra's time.
