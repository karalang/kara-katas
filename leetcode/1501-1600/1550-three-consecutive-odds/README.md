# 1550. Three Consecutive Odds

Given an integer array `arr`, return `true` if there are three consecutive
odd numbers in the array. Otherwise, return `false`.

```
arr = [2,6,4,1]                     ->  false
arr = [1,2,34,3,4,5,7,23,12]        ->  true   ([5,7,23])
```

**Constraints:** `1 <= arr.length <= 1000`; `1 <= arr[i] <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `three_odds.kara` ★ | one pass keeping the length of the run of odd values that ends here, `true` as soon as it reaches three. O(n) |
| `three_odds_windows.kara` | every window of three asked whether all of it is odd: `windows(3).into_iter().any(..)` over `all`. O(n) |
| `three_odds_product.kara` | a product is odd exactly when every factor is, so `any` over the places where a window ends asks whether three neighbours have an odd product (below 10^9 under the constraints). O(n) |
| `three_odds_solution.kara` | LeetCode's Rust template (`three_consecutive_odds(arr: Vec<i32>) -> bool`, the windows arm over `i32`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples, then
`[1, 3, 5]`, `[1, 3]`, `[1]`, `[2, 1, 1, 2, 1, 1, 1]`,
`[1, 1, 2, 1, 1, 2, 1, 1]`, `[999, 1000, 999, 999, 999]` and 1 to 1000;
then the count of `true` answers and a checksum for 3000 random arrays of
up to 12 values, 300 of up to 100 and 300 of up to 1000, each with its
own chance of an odd value. `three_odds.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: some place starts three neighbours, each counted odd when it
leaves a remainder when halved. It checks 3000 arrays of 1 to 14 values
from 1 to 8, each with its own chance of an odd value, every random
choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | `true` needs three odd values, and an all-odd array of three or more is `true` |
| P3 | the array reversed has the same answer |
| P4 | every value raised by 2 leaves the answer |
| P5 | 7, 5, 3 put after the array make it `true`, and a 4 after every value makes it `false` |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 853758855, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run of two answers `true` | P1 573, P2 183, P6 573 |
| M2 | ★: an even value leaves the run as it is | P1 475, P5 1606, P6 475 |
| M3 | ★: even values counted, not odd | P1 1962, P2 1080, P5 3000, P6 1962 |
| M4 | windows: windows of two | P1 573, P2 183, P6 573 |
| M5 | windows: `any` value odd, not `all` | P1 1085, P2 610, P5 2353, P6 1085 |
| M6 | product: the first window skipped | P1 125, P2 59, P3 136, P6 125 |
| M7 | product: the middle value left out | P1 406, P2 74, P5 1704, P6 406 |
| M8 | product: odd read as 1 mod 4 | P1 230, P2 49, P4 487, P6 230 |
| M9 | template: windows of four | P1 354, P2 59, P5 1414, P6 354 |
| M10 | template: every value raised by one on the way to `i32` | P1 1962, P2 1080, P5 3000, P6 1962 |

## Benchmarks

The bench builds 1000 arrays of 1 to 1000 values once, each with its own
chance of an odd value, and asks each 2000 times by the ★ arm, in all
five languages. One value of the array is raised by one before every ask,
so no ask repeats the last and none can be hoisted out of the loop. Every
implementation prints `2000 passes over 1000 arrays of up to 1000 values:
1853723 true, checksum 791986183`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.254 s |
| Kāra (`karac build`) | 0.255 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.267 s |
| C (`clang -O3`) | 0.272 s |
| Rust (`rustc -O`) | 0.284 s |
| Go | 0.339 s |
| Python | 6.9 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.24 s and 0.24 s on one run).

Kāra is 0.95x Rust under overflow checks by median. Not traced. Most asks
end within a few values, so the time is mostly the random access to one
of 1000 arrays and an unpredictable branch per value, and every compiled
row but Go's sits within 12% of the others.

## Verification

All four arms print the same output as `three_odds.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★ and product arms were written in Kāra and checked as written. The
windows arm was written `arr.windows(3).any(..)`, as Rust's lazy
`windows` allows; Kāra's `windows` returns a `Vec[Slice[T]]`
(docs/library/collections.md), and the refusal names the
`.into_iter()` it needs, which `karac fix` added.

The Rust template took 4 changed lines, 1 and 1 over three rounds:
`Vec<i32>` to `Vec[i32]` (twice) with `|&x|` to `|x|` (twice), and
`Solution::` to `Solution.`; then `struct Solution {}` added; then
`.into_iter()` added after `windows(3)`. It checks and agrees with no
hand edit.
