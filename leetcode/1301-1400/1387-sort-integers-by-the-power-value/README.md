# 1387. Sort Integers by The Power Value

The power of an integer `x` is defined as the number of steps needed to
transform `x` into `1` using the following steps: if `x` is even then `x
= x / 2`; if `x` is odd then `x = 3 * x + 1`.

For example, the power of `x = 3` is `7` because `3` needs `7` steps to
become `1` (`3 --> 10 --> 5 --> 16 --> 8 --> 4 --> 2 --> 1`).

Given three integers `lo`, `hi` and `k`. The task is to sort all
integers in the interval `[lo, hi]` by the power value in ascending
order, if two or more integers have the same power value sort them by
ascending order.

Return the `k`th integer in the range `[lo, hi]` sorted by the power
value.

Notice that for any integer `x` `(lo <= x <= hi)` it is guaranteed that
`x` will transform into `1` using these steps and that the power of `x`
will fit in a 32-bit signed integer.

```
lo = 12, hi = 15, k = 2  ->  13
lo = 7,  hi = 11, k = 4  ->  7
```

**Constraints:** `1 <= lo <= hi <= 1000` and `1 <= k <= hi - lo + 1`.

Each arm is `fn get_kth(lo: i32, hi: i32, k: i32) -> i32`. A walk from a
value up to 1000 climbs no higher than 250,504, well inside an `i32`,
but every arm walks in `i64`, since the statement guarantees only that
the power fits.

## Approaches

| file | mechanism |
|---|---|
| `get_kth.kara` ★ | each value walked only until it meets one whose power is known, in a `Map` that every walk fills on its way back from a `Vec` used as a stack; the (power, value) pairs sorted and the k-th read off. O(m log m) after the walks, each step of which is taken once |
| `get_kth_plain.kara` | each value's power counted step by step, afresh in every comparison, the values sorted with `sort_by` on the power and then, with `then`, the value. O(m log m · s) for walks of s steps |
| `get_kth_buckets.kara` | the powers by a recursive function that keeps what it finds in a `Map` passed `mut ref`; a `SortedMap` from each power to its values, which go in rising, and the k-th found by walking the powers up. O(m log m) |
| `get_kth_table.kara` | the powers of every value from 1 to hi kept in a `Vec`, each walk stopping at the first value below its start, whose power is already there; the (power, value) pairs pushed onto a `PriorityQueue`, least first, and popped k times. O(hi log hi) |
| `get_kth_solution.kara` | a Rust solution as LeetCode's Rust users write it (`(lo..=hi).map(..)` into `(steps, x)` pairs, `sort_unstable`, and `v[(k - 1) as usize].1`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples, one value,
the first and the last of the whole range 1 to 1000, and a range whose
two powers tie (`13 7 1 1 871 12`); the constraints' most, every k over
1 to 1000 (`every k over 1 to 1000: checksum 176946985`); and 2000
random ranges inside 1 to 1000 at a random k (`2000 random ranges:
checksum 95253402`). `get_kth.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ and plain arms check clean as first written. The
buckets arm's `let mut values = by_power.get(p).unwrap_or(Vec.new());`
is refused three ways, since `get` lends the stored `Vec` and the
`Vec.new()` default is a temporary that dies at the `;`: the value kept
borrows it, `push` cannot write through a shared `ref`, and the `insert`
back cannot move a borrow. `karac fix` makes it
`by_power.get(p).cloned().unwrap_or(Vec.new())`, one fix for all three,
and the arm checks clean. The table arm's `let mut steps = 0;`, later
added to an `i32` power and stored in a `Vec[i32]`, keeps its literal's
`i64`, which the store refuses; `karac fix` writes `let mut steps: i32 =
0;`. The Rust solution takes one round of 4 fixes by `karac fix`'s
count, from 2 errors: `struct Solution;` to `struct Solution {}`,
`Vec<(i32, i32)>` to `Vec[(i32, i32)]`, and `sort_unstable` to `sort`;
the `(lo..=hi)`, the closure's `x as i64` and the `(k - 1) as usize`
index stay. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each value's steps to 1 counted as the statement counts them,
and the answer the value of the range with exactly k - 1 values before
it, a value coming before another when its power is smaller, or the same
and the value smaller. LeetCode's two examples, the last value of all,
and 2000 ranges of 1 to 60 values, half anywhere up to 1000 and half
inside 1 to 80, where powers are small and tie often, each at a random
k. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a value of the range |
| P3 | before the k + 1-th, when there is one |
| P4 | the first: no value of the range before it |
| P5 | the range one wider at hi: the same k-th, or one before it |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 ranges: checksum 563837615,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, sorting by the
statement's key, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the (power, value) pairs left unsorted | P1 1772, P3 554, P4 1677, P6 7088 |
| M2 | ★: a walk's path filled first to last, not on the way back | P1 1791, P3 811, P4 1677, P5 281, P6 7164 |
| M3 | plain: a tie in power broken by the larger value | P1 1385, P3 1032, P4 703, P5 634, P6 1385 |
| M4 | plain: a value that 4 divides quartered in one step | P1 198, P3 73, P4 99, P5 21, P6 198 |
| M5 | buckets: each value put at the front of its power's list | P1 1385, P3 1032, P4 703, P5 634, P6 1385 |
| M6 | buckets: the steps not counted | P1 1772, P3 554, P4 1677, P6 1772 |
| M7 | table: a walk's power without the known power where it stopped | P1 1751, P3 634, P4 1567, P5 241, P6 1751 |
| M8 | table: the queue popped k - 1 times | P1 2003, P2 199, P6 2003 |
| M9 | solution: 3n + 1 halved in the same step | P1 59, P3 14, P5 3, P6 59 |
| M10 | solution: each walk started from the next value | P1 1721, P3 776, P4 1891, P5 290, P6 1721 |

P1 and P6 kill all ten, P3 nine, P4 eight, P5 seven, and P2 one. Only M8
answers a value outside the range (P2): popped no times at k = 1, it
answers the 0 it started from. Of the edits that misorder the values,
those that keep the order of the smallest powers still answer the first
right, which P4 checks, so M8 and M9 pass it. M3 in the plain arm and M5
in the buckets arm fail alike: both put the larger of two values with
equal powers first. M1 and M2 fail more checks on P6 than on P1, since
the ★ arm they change is P6's reference for every arm.

## Benchmarks

The bench asks 4000 queries, each a range from 1 to 200 up to 800 to
1000, the constraints' most, at a random k, all drawn from the checksum
so far. Every implementation prints `4000 queries over ranges up to 1 to
1000: checksum 189752812`. The work is the walks of 600 to 1000 values,
which put some 1,800 to 2,200 values into the map, and a sort of the
pairs, a query. Rust uses a `HashMap` and sorts its tuples; C keeps its
own open-addressing table and sorts each pair packed into one `int64_t`
with `qsort`; Go uses a `map` and `sort.Slice`; Python a `dict` and
`sort`.

BENCHTAB
