# 1551. Minimum Operations to Make Array Equal

You have an array `arr` of length `n` where `arr[i] = 2 * i + 1` for all
valid `i`. In one operation you can pick two indices `x` and `y`, subtract
1 from `arr[x]` and add 1 to `arr[y]`. The goal is to make every element
equal; the tests guarantee it can be done. Given `n`, return the minimum
number of operations needed.

```
n = 3  ->  2   ([1,3,5] to [2,3,4] to [3,3,3])
n = 6  ->  9
```

**Constraints:** `1 <= n <= 10^4`.

## Approaches

The values `1, 3, .., 2n - 1` add up to `n * n`, so every value must end
at `n`. An operation changes two values by one each, so it closes at most
two units of the values' total distance from `n`, and moving a unit from
a value above `n` to one below always closes two.

| file | mechanism |
|---|---|
| `min_operations.kara` ★ | how far the lower half sits below `n`, added up place by place: `n - (2i + 1)` for `i` below `n / 2`. O(n) |
| `min_operations_mean.kara` | the array built as the statement gives it by `map` and `collect`, its mean taken, and every value's distance from the mean (`abs`) added up and halved. O(n) |
| `min_operations_closed.kara` | the closed form: the lower half's distances `n - 1, n - 3, ..` add up to `n * n / 4` rounded down. O(1) |
| `min_operations_solution.kara` | LeetCode's Rust template (`min_operations(n: i32) -> i32`, the ★ arm's sum as `(0..n / 2).map(..).sum()`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples, then `n` of
1, 2, 4, 5, 9999 and 10000; then the total and a checksum of the answers
for every `n` from 1 to 10000. `min_operations.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the array built, then operations done one at a time, each
taking one from a largest value and giving it to a smallest, until every
value is equal. That order closes two units of distance with every
operation, so no order does better. It checks 3000 lengths from 1 to 30,
every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is 0 exactly when `n` is 1, and at most `n * n` |
| P3 | one more value needs more operations |
| P4 | twice the length needs four times the operations, and one more for an odd `n` |
| P5 | the answers for `n` and `n + 1` add up to `1 + 2 + .. + n` |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 471352412, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. One first choice for the mean arm, the
mean taken over `n + 1`, was equivalent (it gives `n - 1`, which leaves
the halved total the same once rounded down) and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the loop one place longer | P1 1506, P2 78, P3 116, P4 3000, P5 3000, P6 1506 |
| M2 | ★: each distance one too large, `n - 2i` | P1 2884, P4 3000, P5 3000, P6 2884 |
| M3 | ★: the last distance kept, not the total | P1 2707, P3 1378, P4 2884, P5 2806, P6 2707 |
| M4 | mean: the total distance divided by 3 | P1 2884, P2 78, P3 116, P4 2490, P5 3000, P6 2884 |
| M5 | mean: signed distances, no `abs` | P1 2884, P2 2884, P3 3000, P4 1494, P5 3000, P6 2884 |
| M6 | mean: the array built one value too long | P1 3000, P2 116, P3 116, P4 3000, P5 3000, P6 3000 |
| M7 | closed: rounded up, `(n * n + 3) / 4` | P1 1494, P2 116, P3 116, P4 1494, P5 3000, P6 1494 |
| M8 | closed: divided before multiplying, `n / 4 * n` | P1 2141, P2 177, P3 194, P4 2257, P5 3000, P6 2141 |
| M9 | template: each distance two too large | P1 2884, P4 3000, P5 3000, P6 2884 |
| M10 | template: the sum starting at 1 | P1 2884, P2 177, P3 194, P4 3000, P5 3000, P6 2884 |

## Benchmarks

The bench asks the ★ arm for every `n` from 1 to 10000, in 100 passes,
in all five languages; the input is one integer, so nothing is built
beforehand. Every implementation prints `100 passes over n from 1 to
10000: checksum 817864851`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.008 s |
| C (`clang -O3`) | 0.009 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.906 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.227 s |
| Kāra (`karac build`) | 1.260 s |
| Go | 3.074 s |
| Python | 166 s |

The loop is a sum of an arithmetic sequence, and the unchecked C and Rust
builds turn it into its closed form: those two rows measure the
`mix` alone, not the loop. The checked builds keep the loop, since its
overflow has to be reported at the place it happens, and are the
comparison that holds: Kāra checks integer overflow by default.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (1.23 s and 1.25 s on one run).

Kāra is 1.35x Rust under overflow checks by median, on the same inner
loop: both compile it to the same four instructions (`add`, `jo`, `add`,
`dec`/`jne`). Where the loop lands decides the gap. In this binary it
starts at `0x2b70`, so its closing `dec`/`jne` pair straddles a 64-byte
boundary;
the same program with one more statement before the loops (a `Vec`
pushed once, or a string's length read) moves the loop to `0x20c0` or
`0x2b90`, and those builds ran 0.88 to 1.03 s in four runs each, level
with checked Rust. So the gap is code placement, not the code.

## Verification

All four arms print the same output as `min_operations.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, mean and closed-form arms were written in Kāra and checked as
written.

The Rust template took 1, 1 and 1 changed lines over three rounds:
`Solution::` to `Solution.`; then `struct Solution {}` added; then the
wrapper's closing `as i64` dropped (an `i32` widens). It checks and
agrees with no hand edit.
