# 1746. Maximum Subarray Sum After One Operation

*Premium problem.* You are given an integer array `nums`. You must
perform **exactly one** operation where you can **replace** one element
`nums[i]` with `nums[i] * nums[i]`.

Return *the **maximum** possible subarray sum after **exactly one**
operation*. The subarray must be non-empty.

```
nums = [2, -1, -4, -3]          ->  17   square -4: 2 + -1 + 16
nums = [1, -1, 1, 1, -1, -1, 1] ->  4    square -1: 1 + 1 + 1 + 1
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^4 <= nums[i] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `square.kara` ★ | Kadane's scan with two states: `plain`, the best sum of a subarray ending at the current value with nothing squared, and `squared`, the best with exactly one value squared. A squared run either squares the current value, after a plain run or alone, or extends one that squared earlier. The answer is the best `squared` seen. O(n) |
| `square_sides.kara` | if `nums[i]` is the value squared, the best subarray around it is its square plus the best run ending just before it, or nothing, plus the best run starting just after it, or nothing; two passes fill those runs and every `i` is tried with `map(..).max()`. O(n) |
| `square_halves.kara` | each range is summed up as a `Part`: its total, best prefix, suffix and subarray, and the same four with exactly one value squared; two halves combine field by field, the squared value lying in one half or the other. O(n) work, O(log n) depth |
| `square_fold.kara` | the ★ arm's walk as one `fold`, its state the tuple of the best plain run, the best squared run and the best answer so far. O(n) |
| `differential.kara` | the four arms against the statement read literally, five properties |

The problem is premium, so there is no LeetCode Rust template; a fourth
Kāra arm stands in its place.

Every arm prints the same 8 lines: LeetCode's two examples, then one
value, all negative values, and the largest square beside the smallest
value; then the sum of the answers and a checksum for 3000 random arrays
of up to 8 values within 5, 300 of up to 1000 within 10000, and 10 of up
to 100000 within 10000, LeetCode's limits. `square.py` mirrors the ★ arm
and its output is byte-identical.

```
17
4
49
81
100020000
3000 arrays of up to 8 values within 5: sums add to 66890, checksum 66559662
300 arrays of up to 1000 values within 10000: sums add to 29562892938, checksum 319909545
10 arrays of up to 100000 values within 10000: sums add to 1000216535, checksum 885443532
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every value squared in turn, and every non-empty subarray of
the result summed, in `i64`. It checks 3000 random arrays of 1 to 8
values from -6 to 6, each with a random value to append. Every case is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | one more value at the end never lowers the answer |
| P4 | a 0 put in front gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 528899142, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, every value squared in turn and every subarray summed, gives the
same checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, three to each of the first three arms and
one to the fold, each run under `karac __mir-run` and `karac
__mir-llvm-run`. All ten are killed, each the same way under both
backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a squared value started after the plain run even when that run is negative | P1 535, P2 918, P5 535 |
| M2 | ★: the plain run never restarted | P1 433, P2 799, P5 433 |
| M3 | ★: the answer the best plain run, nothing squared | P1 2942, P4 316, P5 2942 |
| M4 | sides: the run ending before a value kept even when negative | P1 535, P2 918, P5 535 |
| M5 | sides: the run after a value only one value long | P1 618, P2 1159, P5 618 |
| M6 | sides: the run after the squared value dropped | P1 1187, P2 1841, P5 1187 |
| M7 | halves: the best squared run across the middle only with the square on the left | P1 929, P2 1779, P3 26, P4 191, P5 929 |
| M8 | halves: a squared prefix only with the square in the second half | P1 247, P2 358, P3 10, P4 116, P5 247 |
| M9 | halves: a squared total only with the square in the first half | P1 82, P2 122, P3 43, P4 90, P5 82 |
| M10 | fold: the plain run never restarted | P1 433, P2 799, P5 433 |

## Benchmarks

The bench draws 20 random arrays of 100000 values, LeetCode's longest,
within 10000, all of them first, then answers each 40 times by the ★ arm
in all five languages. Every implementation prints `20 arrays of 100000
values, 40 rounds: sums add to 80035429800, checksum 732657709`. The C
build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| Go | 0.147 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.149 s |
| Kāra (`karac build`) | 0.156 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.158 s |
| C (`clang -O3`) | 0.202 s |
| Rust (`rustc -O`) | 0.203 s |
| Python | 11 s |

The sequential Kāra build takes 0.78x Rust's time and 1.06x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).
Kāra is ahead of plain Rust here and within a few percent of Rust with
overflow checks on.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.124 s and
0.133 s on one run).

## Verification

All four arms print the same output as `square.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ arm was first written with `let mut plain = 0;` and `let mut
squared = 0;`, and took one `karac fix`: an integer literal binding
defaults to `i64`, and the values it meets are `i32`, so the fix wrote
`plain: i32` and `squared: i32`. The sides, halves and fold arms, the
differential and the bench checked clean as written.
