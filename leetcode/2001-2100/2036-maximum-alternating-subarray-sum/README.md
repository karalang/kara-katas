# 2036. Maximum Alternating Subarray Sum

A subarray of a 0-indexed integer array is a contiguous non-empty sequence
of elements within the array. The alternating subarray sum of the subarray
from index `i` to `j` (inclusive) is `nums[i] - nums[i + 1] + nums[i + 2] -
... +/- nums[j]`. Given a 0-indexed integer array `nums`, return the
maximum alternating subarray sum of any subarray of `nums`.

```
nums = [3,-1,1,2]     ->  5     ([3,-1,1]: 3 + 1 + 1)
nums = [2,2,2,2,2]    ->  2     ([2], or [2,2,2]: 2 - 2 + 2)
nums = [1]            ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^5 <= nums[i] <= 10^5`.

The signs are taken from the subarray's own first value, so the same value
is added in one subarray and subtracted in the next. Kadane's scan still
works, twice over. `plus` is the best sum of a subarray that ends here and
adds its last value; `minus` the best that subtracts it. A value is added
either alone or after a subtracted one, and subtracted only after an added
one: `plus' = max(x, minus + x)`, `minus' = plus - x`. A one-value prefix
has no `minus` yet.

## Approaches

| file | mechanism |
|---|---|
| `alternating.kara` ★ | the two running sums over `nums.iter().skip(1)`, `minus` an `Option[i64]` that is `None` until a second value exists and is matched for the next `plus`. O(n), O(1) space |
| `alternating_prefix.kara` | alternating prefix sums `s[k]` of `(-1)^t nums[t]`: the subarray `i..=j` sums to `s[j + 1] - s[i]` from an even `i` and `s[i] - s[j + 1]` from an odd one, so one scan keeps the least `s` at an even start and the greatest (`Option`, through `map_or`) at an odd one. O(n) |
| `alternating_kadane.kara` | the values signed `(-1)^t nums[t]` by `enumerate().map(..)`, then Kadane's scan over them and over their negation, each allowed to restart only at a start of its own parity; `Option[i64]` runs, a guarded `match`. O(n) |
| `alternating_split.kara` | divide and conquer over the signed values: each range's `Part` (total, greatest and least prefix, greatest even-start suffix and least odd-start suffix as `Option`s, answer) built from two halves' Parts, a `match` on the `(Option, Option)` pairs. O(n) work, O(log n) deep |
| `alternating_fold.kara` | the ★ recurrence as one `fold((nums[0], None, nums[0]), \|(plus, minus, best), x\| ..)`, `minus.map_or(x, \|m: i64\| x.max(m + x))` for the next `plus`. O(n) |
| `alternating_solution.kara` | LeetCode's Rust template (`impl Solution`, `Vec<i32>`, `as i64`, a `minus` seeded with `i64::MIN / 2`), carried by `karac fix` in two rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the sum and a checksum of the answers for 2000
arrays of 1 to 12 values up to 50 either side, and for 4 arrays of 100000
values, the most the constraints allow (values up to 10^5, 1000, 10^5 and 3
either side). `alternating.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subarray `i..=j`, its values added and subtracted in turn
from `nums[i]`. It checks 1500 arrays of 1 to 12 values up to 1 to 60
either side, each with one more value and a second array of 1 to 6 values.
Every random choice of a problem is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a value added at either end never lowers the answer: every subarray is still there, its signs taken from its own first value |
| P3 | two arrays joined answer at least what either does |
| P4 | every value tripled triples the answer |
| P5 | a 0 appended answers the larger of the answer and 0: a subarray that ends on it sums to one that ends just before it, or is `[0]` |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 arrays: checksum 459457211, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. All thirty are killed, each
fails the same way under both backends, none by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the minus sum never taken for the best | P1 670, P5 356, P6 670 |
| M2 | ★: a plus never restarted at its own value (`m + x` for `x.max(m + x)`) | P1 475, P2 258, P3 221, P5 18, P6 475 |
| M3 | ★: a minus extended by adding (`plus + x`) | P1 1296, P6 1296 |
| M4 | prefix: only the latest odd start kept | P1 391, P2 480, P3 99, P6 391 |
| M5 | prefix: the even start's prefix taken as the greatest | P1 612, P2 477, P3 143, P5 14, P6 612 |
| M6 | prefix: the signs taken from the odd index | P1 1333, P2 30, P3 13, P6 1333 |
| M7 | kadane: a run kept only through a loss (`r < 0` for `r > 0`) | P1 1064, P2 211, P3 323, P5 18, P6 1064 |
| M8 | kadane: the odd values searched from even starts | P1 749, P2 462, P3 70, P6 749 |
| M9 | kadane: the odd values signed like the even | P1 822, P2 676, P3 195, P6 822 |
| M10 | split: the odd suffix never joined across the cut | P1 510, P2 587, P3 158, P6 510 |
| M11 | split: the greatest prefix never crossing the cut | P1 446, P2 365, P3 114, P5 208, P6 446 |
| M12 | split: the even suffix not reaching the right end | P1 307, P2 201, P3 118, P5 170, P6 307 |
| M13 | fold: the minus taken from the new plus | P1 1214, P6 1214 |
| M14 | fold: the first value folded in again (`skip(1)` dropped) | P1 83, P6 83 |
| M15 | fold: the best seeded at zero | P1 159, P5 61, P6 159 |
| M16 | solution: a plus never restarted at its own value | P1 910, P2 727, P3 508, P5 371, P6 910 |
| M17 | solution: the minus taking the value twice | P1 1231, P6 1231 |

P1 and P6 kill all seventeen, P2 and P3 eleven each, P5 eight, and P4 none.
Every edit here still answers the largest of some sums of the values, and
tripling the values triples each such sum, so P4 cannot see them. It is
there for an error that does not scale: a constant leaking into an answer,
such as a seed or a sentinel that wins. P2 and P3 miss the edits that
answer from a subset of the true candidates that still grows with the array
(M1, M14, M15, and the minus slips M3, M13 and M17), since a longer array
then has more candidates for both the true answer and the wrong one. P5
sees the edits whose answer on an array ending in 0 is not the old answer
or 0: a minus never compared (M1), a best seeded at 0 (M15), or a run that
never restarts (M2, M7, M16).

The other thirteen fail as a kept one does, or with a signature of their
own that adds nothing. The ★ and fold arms are one recurrence, so their
edits pair up: the ★ arm's minus from the new plus fails as M13, its best
seeded at zero as M15, and the fold arm's minus never compared and plus
never restarted fail as M1 and M2. The Rust arm's answer from the plus alone
fails as M1, and its first value stepped over again as M14, as does the
prefix arm's best seeded at zero. The prefix arm's odd-start sum not
negated, the kadane arm's run restarted at any index and its losing run kept
rather than restarted, the split arm's leaf best taken as its signed value
and its least prefix crossing with the right half's greatest, and the Rust
arm's minus kept from before the loop fail with counts of their own.

## Verification

Every arm prints the same output as `alternating.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 1.3 s (★) to 3.4 s (kadane) and the
differential 2.3 s, on kara 991c45adcd.

The fold arm first stopped at the type check. Its accumulator `(nums[0],
None, nums[0])` holds a bare `None`, and that bound `fold`'s `B` to
`Option`'s own `T` with nothing left to solve it: the closure was checked
against `B` named back, so its tail never reached the accumulator. A bare
`None` inside a tuple argument now becomes a fresh variable, and a callee
parameter that a value argument mentions stays a variable while the closure
is checked, so the closure's tail `(next_plus, Some(next_minus), ..)`
solves it. That tail's `next_plus` is a `ref i64` (from `map_or(x, ..)` with
`x` a `ref i64`), which now reads as the value against the partly solved
accumulator, as it already did against a concrete one; `fold(0, |acc, x|
x)` was refused the same way.

The same arm then met a wrong answer that was on main already. `m.map_or(x,
|k: i64| k + 1)` with `x: ref i64` solved `map_or`'s `U` as `ref i64` while
the closure returned an `i64`: the interpreter stopped on "deref of
non-reference", and the build read the value as an address
(B-2026-11-09-35). A scalar `ref` handed to a parameter that a function
argument returns is now solved as the value. `v.iter().fold(None, |acc:
Option[i64], x| Some(x))` built and printed an address before; it is now
refused, since its tail is an `Option[ref i64]` (kara 5a9b370550,
`tests/kata_2036_fold_inference.rs`); B-2026-11-09-36 asks for it to read
the scalar as its value, as `Some(x)` against an `Option[i64]` slot does
elsewhere. The fix also turned up a crash on main already: a closure that
only passes its parameter on, as in `ap(1, |x| { println("a"); x })` for
`ap[F: Fn(i64) -> i64]`, checks clean and then stops every backend at MIR
validation with its parameter typed `()` (B-2026-11-09-39).

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds (three edits, then one) to a clean check: `Vec<i32>` to
`Vec[i32]`, `i64::MIN` to `i64.MIN`, and a `ref` dropped from the
adapter's parameter, which borrows already.

## Benchmarks

The bench builds 4 arrays of 100000 values once in all five languages, the
most the constraints allow, and runs the ★ arm for 1000 rounds, one value
of every array negated before each call: 4000 calls, each one pass over
100000 values. Every implementation prints `4000 calls: sum 52193108388,
checksum 822614388`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `991c45adcd` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.382 to 0.428 s | 0.385 s |
| Rust (`rustc -O`) | 0.395 to 0.479 s | 0.429 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.576 to 0.615 s | 0.591 s |
| Kāra (`karac build`) | 0.587 to 0.646 s | 0.602 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.584 to 0.616 s | 0.612 s |
| Go | 0.600 to 0.666 s | 0.633 s |
| Python | 50.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.588 s) is not above its real time (0.602 s).

The sequential Kāra program is 1.04x Rust under overflow checks and 1.59x
C.
