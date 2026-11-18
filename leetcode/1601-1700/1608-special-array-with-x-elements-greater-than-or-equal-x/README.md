# 1608. Special Array With X Elements Greater Than or Equal X

You are given an array `nums` of non-negative integers. `nums` is
considered **special** if there exists a number `x` such that there are
**exactly** `x` numbers in `nums` that are **greater than or equal to**
`x`.

Notice that `x` **does not** have to be an element in `nums`.

Return `x` *if the array is* ***special****, otherwise, return* `-1`. It
can be proven that if `nums` is special, the value for `x` is
**unique**.

```
nums = [3,5]        ->  2
nums = [0,0]        ->  -1
nums = [0,4,3,0,4]  ->  3
```

**Constraints:** `1 <= nums.length <= 100`; `0 <= nums[i] <= 1000`.

## Approaches

The count of numbers at least `x` never grows as `x` does, so the count
minus `x` falls strictly and meets zero at most once: that is why `x` is
unique. Since `nums` is not empty, `x = 0` is never the answer.

| file | mechanism |
|---|---|
| `special.kara` ★ | the numbers taken `own`, sorted largest first with `sort_by(\|a, b\| b.cmp(a))`; `x` is special when the `x`th largest is at least `x` and the next, if any, is below it. O(n log n) |
| `special_counts.kara` | how many numbers take each value, those above `n` counted at `n` with `min`, in a `Vec.filled(n + 1, 0)`; then from `n` down, a running count of the numbers at least `x` until it meets `x`. O(n) |
| `special_search.kara` | a binary search for where the count minus `x` reaches zero, each count a `filter(..).count()` over the numbers. O(n log n) |
| `special_solution.kara` | LeetCode's Rust template (`mut nums`, `sort_unstable`, `partition_point` for each count, `usize` indices), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more (an example LeetCode once had, one number, every number the same,
and every number above the count), then the count special and a checksum
of the answers for 3000 problems of up to 5 numbers from 0 to 6, 3000 of
up to 100 numbers from 0 to 1000, and 30 of up to 100000 numbers from 0
to 100000, past LeetCode's bounds. `special.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each `x` from 0 to `n`, counting the numbers at least `x`
one by one, and the first `x` the count equals. It checks 3000 problems
of 1 to 8 numbers from 0 to a top of 1 to 10, every random choice drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the numbers reversed leave the answer |
| P3 | a 0 added leaves the answer |
| P4 | every number capped at `n` leaves the answer |
| P5 | a special `x` stays special with every number below it made 0 |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 6761869, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M7 and M9 are the only ones P4 kills:
counting the numbers above `x` rather than at least `x` goes wrong more
often once every number is at most `n`.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the next number allowed to equal `x` | P1 1277, P6 1277 |
| M2 | ★: `x = n` never tried | P1 510, P3 510, P6 510 |
| M3 | ★: sorted smallest first | P1 1539, P3 1586, P6 1539 |
| M4 | counts: numbers at `n` or above counted at `n - 1` | P1 510, P3 510, P6 510 |
| M5 | counts: the walk starting below `n` | P1 1490, P3 637, P6 1490 |
| M6 | counts: the walk stopping once the count reaches `x` | P1 1385, P6 1385 |
| M7 | search: the numbers above `x` counted | P1 1561, P4 375, P6 1561 |
| M8 | search: the low half kept where the high half should be | P1 1178, P3 716, P6 1178 |
| M9 | template: `partition_point` past the numbers equal to `x` | P1 1561, P4 375, P6 1561 |
| M10 | template: the numbers not sorted | P1 1270, P2 1247, P3 1942, P6 1270 |

## Benchmarks

The bench makes 1000 problems of 10000 numbers from 0 to 10000, all of it first. Then: each copied and sorted largest first, then scanned. Every implementation prints `1000 problems of 10000 numbers from 0 to 10000: 485 special, checksum 265143365`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.145 s |
| Kāra (`karac build`) | 0.146 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.175 s |
| Rust (`rustc -O`) | 0.177 s |
| C (`clang -O3`) | 0.781 s |
| Go | 0.885 s |
| Python | 4.7 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.124 s and 0.144 s on one run).

## Verification

All four arms print the same output as `special.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`.

## Writing it

The ★ and counts arms were written in Kāra and checked as written. The
search arm wrote `filter(|v| **v >= x)` over a `Slice[i32]`, and
`karac fix` took a `*` off; it wrote `let mut lo = 0` beside an `i32`
`hi`, and `karac fix` typed it `let mut lo: i32 = 0`.

The Rust template took one `karac fix` of 9 edits: `struct Solution;` to
`struct Solution {}`, the `<..>` types to `[..]`, the `mut` parameter to
`own` with a `let mut` rebinding it, `sort_unstable()` to `sort()`, the
`|&v|` closure pattern to `|v|`, `as usize` to `as i64`, and
`Solution::` to `Solution.`. It then checks and agrees with no hand edit.
