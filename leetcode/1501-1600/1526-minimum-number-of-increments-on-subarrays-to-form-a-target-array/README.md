# 1526. Minimum Number of Increments on Subarrays to Form a Target Array

You are given an integer array `target` and an array `initial` of the same
size, all zeros. In one operation you choose any subarray of `initial` and
increment each of its values by one. Return the minimum number of
operations to form `target` from `initial`. The answer fits in a 32-bit
integer.

```
target = [1,2,3,2,1]  ->  3
target = [3,1,1,2]    ->  4
target = [3,1,5,4,2]  ->  7
```

**Constraints:** `1 <= target.length <= 10^5`; `1 <= target[i] <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `increments.kara` ★ | the first number, plus every rise from one number to the next: a rise must start that many new increments, and a fall only ends some. O(n) |
| `increments_falls.kara` | the same count read from the other end: the last number, plus every fall. O(n) |
| `increments_stack.kara` | the open increments as a stack of heights: a number closes every height above it, and when it closed none it opens the heights from the top of the stack up to itself, one increment each. O(n) amortized |
| `increments_iter.kara` | the ★ arm with iterator adapters: `zip` with `skip(1)`, the rises kept by `map` and `max(0)`, `sum` |
| `increments_solution.kara` | LeetCode's Rust template (`Vec<i32>`, `windows(2)`), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples, 100000
numbers alternating 1 and 40000, then checksums of the answers for 3000
random arrays of 1 to 12 numbers up to 5, 300 of 1 to 1000 up to 1000,
and 30 of 1 to 100000 up to 10000. The values stay small enough that the
answer fits in the template's `i32`, as the problem guarantees.
`increments.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a breadth-first search from the zero array over every
subarray increment that stays at or below the target, states packed in
base 5 and kept in a `Map`. It checks 3000 arrays of 1 to 6 numbers from
1 to 4, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed has the same answer |
| P3 | every number raised by the same lift adds the lift to the answer |
| P4 | the answer is at least the largest number and at most the sum |
| P5 | every number doubled doubles the answer |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 482408494, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Twelve edits to the differential, two or three to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Ten are killed, each
the same way under both backends; two survive, and both are equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the total starts at 0, not the first number | P1 3000, P2 1883, P3 3000, P4 2636, P6 3000 |
| M3 | ★: each number added where it rises, not the rise | P1 1935, P2 1846, P3 1935, P6 1935 |
| M4 | falls: the total starts at the first number, not the last | P1 1883, P2 1883, P4 688, P6 1883 |
| M5 | falls: the rises counted, not the falls | P1 1883, P2 1883, P4 704, P6 1883 |
| M6 | stack: a rise costs even after a fall | P1 1637, P2 1763, P3 1421, P6 1637 |
| M7 | stack: a fall never noted | P1 1637, P2 1763, P3 1421, P6 1637 |
| M9 | iter: the array zipped with itself, not one place on | P1 1935, P2 1883, P4 1437, P6 1935 |
| M10 | iter: the falls summed in place of the rises | P1 1883, P2 1883, P4 688, P6 1883 |
| M11 | template: the total starts at the last number | P1 1883, P2 1883, P4 704, P6 1883 |
| M12 | template: `!=` for `>` in the rise test | P1 1936, P2 1883, P4 1440, P6 1936 |

The survivors: `>=` for `>` in the ★ arm's rise test (M2), since an equal
step adds 0; and the stack arm popping an equal height (M8), since it is
pushed straight back.

## Benchmarks

The bench builds 100 random arrays of 1 to 100000 numbers up to 10000
once and answers each 50 times by the ★ arm, in all five languages. Every
implementation prints `50 passes over 100 arrays of up to 100000 numbers:
checksum 866328373`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `a90821c8d` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.249 s |
| Rust (`rustc -O`) | 0.486 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.823 s |
| Go | 0.841 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.888 s |
| Kāra (`karac build`) | 0.896 s |
| Python | 16.5 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.86 s and 0.89 s on one run).

Kāra is 1.08x Rust under overflow checks by median. Not traced. The work
is one pass of subtractions and additions; C and unchecked Rust can
vectorize it, and a checked add in the loop stops that, which fits the
gap between the two Rust rows.

## Verification

All five arms print the same output as `increments.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change.

## Writing it

The ★, falls, stack and iterator arms were written in Kāra and checked as
written. The Rust template took one round of 2 edits, `Vec<..>` to
`Vec[..]` in two places, and then checked; its `windows(2)` and `i32` arithmetic
stay as written, and it agrees with no hand edit.
