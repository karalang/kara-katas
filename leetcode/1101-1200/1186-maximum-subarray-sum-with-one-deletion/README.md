# 1186. Maximum Subarray Sum with One Deletion

Given an array of integers `arr`, return the largest sum of a non-empty
subarray (contiguous elements) with at most one element deleted: choose a
subarray, optionally delete one of its elements, and at least one element
must remain.

```
[1, -2, 0, 3]      ->  4    delete -2: [1, 0, 3]
[1, -2, -2, 3]     ->  3    [3] alone
[-1, -1, -1, -1]   ->  -1   [-1]; deleting it would leave nothing
```

**Constraints:** `1 <= arr.length <= 10^5`, `-10^4 <= arr[i] <= 10^4`.

The arms are `fn maximum_sum(arr: Vec[i64]) -> i64`. The two Rust arms keep
the method LeetCode gives Rust users, over `Vec<i32>`, inside `impl
Solution`, and a one-line `maximum_sum` converts the values and calls it.

## Approaches

Kadane's best sum ending at each index answers the problem without a
deletion. A subarray with one element deleted that ends at index `i`
either deleted `arr[i]` itself, leaving the best whole sum ending at `i -
1`, or deleted an earlier element and adds `arr[i]` to the best such sum
ending at `i - 1`. Carrying both bests along the array is one pass.

| file | mechanism |
|---|---|
| `maximum_sum.kara` ★ | one pass carrying `kept`, the best sum ending here with nothing deleted, and `cut`, the best ending here with one element deleted (`i64.MIN` until there is an element to delete). O(n) time, O(1) space |
| `maximum_sum_sides.kara` | the best sum ending at each index (Kadane left to right) and the best starting at each (right to left); deleting `arr[i]` joins the best ending at `i - 1` to the best starting at `i + 1`. O(n) time, O(n) space |
| `maximum_sum_fold.kara` | the ★ arm's recurrence as one `fold` over `arr[1..]`, its state a `(i64, Option[i64], i64)` with `None` until there is an element to delete. O(n) time |
| `maximum_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `vec![vec![0; 2]; n]` table filled with `std::cmp::max`, row `i` holding the best sum ending at `i` with no deletion and with one), carried to Kāra by `karac fix`. O(n) time, O(n) space |
| `maximum_sum_chain.kara` | another Rust solution, one iterator chain (`iter().skip(1).fold` over a `(i32, i32, i32)` seeded `(arr[0], 0, arr[0])`, destructured as `\|(keep, del, best), &x\|`, `.2` taking the answer), carried to Kāra by `karac fix`. O(n) time |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; one value
(`small 1: -7`); a deletion that joins two sides (`small 2: 11` from `[5,
-100, 6]`); two negatives, where deleting one would leave the other, which
is worse than keeping the better alone (`small 3: -3`); a deletion that
leaves a choice of two equal values (`small 4: 3` from `[2, -1, -1, 2]`);
2000 random arrays of 1 to 12 values in `-10..=10` (`2000 random arrays:
checksum 240242388`); and 100000 values in `-10000..=10000`, the
constraints' most (`100000 values: 134904`). `maximum_sum.py` mirrors the ★
arm and its output is byte-identical; it also asserts, on each of the 2000
random arrays, that the answer equals the statement read literally (every
subarray, with and without each of its elements). Every arm gives the same
output under `karac run` and `karac build`.

The Mend loop: the ★, sides and fold arms take no fixes. The Rust arms
take one round each: `struct Solution;` to `struct Solution {}`;
`Vec<i32>` to `Vec[i32]`; `Solution::maximum_sum` to
`Solution.maximum_sum`; the `&` before a closure's pattern dropped; the
solution arm also takes `std::cmp::max` to `max`, and its output matches on
the first run (10 fixes). The chain arm (7 fixes) was then refused twice
with no fix (gaps 1 and 2 below); with both fixed it takes one more fix,
the seed's `0` to `0i32`, and its output matches.

## Gaps

1. **A method's argument did not widen.** After its first round, the chain
   arm's `let del = (del + x).max(keep)` was refused: "`max` expects an
   argument of type `i64`, got `i32`". `del` is an `i64`, since the seed's
   `0` took the default, and `keep` an `i32`. design.md § Mixed-width
   operands says "At a binding or an argument, the whole table applies",
   and a free function's argument widened, but a method's did not, so
   `best.max(a)` with `best: i64` and `a: i32` was refused. Now a method's
   argument widens as any argument does (an integer into a wider integer,
   a float into a wider float, an integer of at most 32 bits into `f64`),
   and narrowing is still refused. kara B-2026-11-17-90.
2. **A fold seed's literal got no suffix fix.** With gap 1 fixed, the
   chain arm's `best.max(keep).max(del)` is refused, rightly: `del` is an
   `i64` and `best` an `i32`. But the refusal said only "`max` expects an
   argument of type `i32`, got `i64`", while `let (keep, del) = (arr[0],
   0)` gets the reason and a machine-applicable fix to write `0i32`. Now
   a closure's tuple parameter binds a `fold` seed's literals as that `let`
   does, and the trace back to the literal follows `.max` and `.min`
   through the shadowing `let del = (del + x).max(keep)`, so the refusal
   says "`del` is an 'i64' because the literal it is bound to took the
   default (design.md §8 Literals); write that literal `0i32`" and `karac
   fix` writes it. kara B-2026-11-17-91.

The differential's first draft drew six warnings for `.clone()`s of arrays
a callee only borrows, each naming the plain argument to pass instead.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray's sum, and that sum less each of its elements
when it has two or more. 600 random arrays of 1 to 12 values in
`-span..=span`, the span 1 to 10; the first ten have one value and the
next ten are all negative.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the array reversed has the same answer |
| P3 | the answer is at least Kadane's, the best with nothing deleted |
| P4 | `-10000` appended changes nothing |
| P5 | every value doubled doubles the answer |
| P6 | the ★ arm's answer |

All 18,000 checks pass on every arm: `600 arrays: checksum 397161565, 18000
checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
__mir-llvm-run` and `karac build`.

## Mutation testing

Seven edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`, each failing the same way under both. Six are
caught; the seventh is equivalent.

| # | mutation | failures by property |
|---|---|---|
| A | ★: `cut` never deletes this element (`cut + x` alone) | P1 190, P2 73, P6 760 |
| K | ★: `kept` never starts afresh (`kept + x` alone) | P1 544, P2 796, P3 466, P6 816 |
| S | sides: the last deletion point skipped | P1 32, P2 48, P4 32, P6 32 |
| F | fold: `cut` never deletes this element | P1 190, P2 73, P6 190 |
| T | solution: row 1 of the table never deletes `arr[i]` | P1 222, P6 222 |
| R | chain: `.skip(0)`, so `arr[0]` is folded in twice | P1 252, P2 330, P6 252 |
| C | chain: the seed's `del` is `arr[0]` rather than `0` | none |

A mutation of the ★ arm fails P6 on every arm, since P6 compares each arm
with the ★ arm. A and F are the same fault in two arms and fail the same
checks. P3 catches only K, the one fault that can lose to Kadane's answer;
P4 only S: the deletion point it skips is the second-to-last, which an
appended value moves inward, so the longer array gets the right answer and
the original does not. P5 catches none, since every fault here scales with
the values. C passes all
18,000 checks under both backends: the seed `del = 0` stands for `arr[0]`
deleted, which only ever adds the sum of a subarray starting at index 1,
and `keep` already holds that; `del = arr[0]` stands for nothing deleted
yet, also a sum the answer may take, so neither seed changes the best.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 10 arrays of 100000 values in `-10000..=10000`, the constraints'
most, built once, then 100 rounds over all of them, each answer folded
into a checksum. Every program prints `100 rounds of 10 arrays: checksum
485309050`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `2a5724c2d4`
and this kata's two fixes, on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.149 to 0.204 s | 0.152 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.148 to 0.166 s | 0.151 s |
| Rust (`rustc -O`) | 0.153 to 0.192 s | 0.155 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.146 to 0.164 s | 0.153 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.147 to 0.156 s | 0.150 s |
| C (`clang -O3`) | 0.149 to 0.195 s | 0.154 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.319 to 0.363 s | 0.334 s |
| Go | 0.150 to 0.172 s | 0.153 s |
| Python | 12.07 to 12.46 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 4% of wall time for both Kāra
rows, so both ran on one core. Kāra, Rust, C at its default and Go are
within 3% of each other: each element is three dependent max operations,
about 1.5 ns, and the loop runs at the speed of that chain whatever the
compiler, so overflow checks cost nothing measurable either. C built for
x86-64-v3 takes 2.2x as long, which was not profiled. Python takes about
80x Kāra's time.
