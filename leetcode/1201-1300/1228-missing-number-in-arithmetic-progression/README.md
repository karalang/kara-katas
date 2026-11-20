# 1228. Missing Number In Arithmetic Progression

In some array `arr`, the values were in arithmetic progression: the
values `arr[i + 1] - arr[i]` are all equal for every `0 <= i <
arr.length - 1`.

A value from `arr` was removed that **was not the first or last value in
the array**.

Given `arr`, return the removed value.

```
arr = [5,7,11,13]   ->  9     the progression was [5,7,9,11,13]
arr = [15,13,12]    ->  14    the progression was [15,14,13,12]
```

**Constraints:** `3 <= arr.length <= 1000`; `0 <= arr[i] <= 10^5`; the
given array is **guaranteed** to be a valid array.

The arms are `fn missing_number(arr: Vec[i64]) -> i64`. The two Rust
arms keep the method LeetCode gives Rust users, on `i32`, inside `impl
Solution`, and a one-line `missing_number` converts to it.

## Approaches

| file | mechanism |
|---|---|
| `missing_number_in_arithmetic_progression.kara` ★ | binary search: the first and last values were kept, so the step is `(last − first) / n`; before the missing value every element sits where the progression puts it, and from it on one step further, so the search finds the first element out of place, and the missing value is where it should have been. O(log n) |
| `missing_number_in_arithmetic_progression_sum.kara` | the full progression of `n + 1` values sums to `(first + last)(n + 1) / 2`, and the missing value is what the array falls short of it. O(n) |
| `missing_number_in_arithmetic_progression_scan.kara` | a scan for the gap that is not the step, the missing value one step into it; with a step of 0, the first value. O(n) |
| `missing_number_in_arithmetic_progression_gaps.kara` | without dividing: the gaps by `windows(2)`, the step the smaller of the first two, the missing value one step into the gap that differs. O(n) |
| `missing_number_in_arithmetic_progression_search.kara` | a Rust solution as LeetCode's Rust users write it (the binary search on `usize` bounds, `let (mut lo, mut hi) = (0usize, n - 1)`, the positions cast to `i32`), carried to Kāra by `karac fix` |
| `missing_number_in_arithmetic_progression_windows.kara` | another Rust solution (`arr.windows(2).find(\|w\| w[1] - w[0] != d).map(\|w\| w[0] + d).unwrap_or(arr[0])`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's two examples and an array
of one repeated value (`7`), a checksum of the answers for 1000 random
progressions of 4 to 1001 values with one interior value removed, all of
them right (`925200074`, `1000 right`), and the constraints' top, 1000
values from 0 to 99900 by 100 less 50000 (`50000`).
`missing_number_in_arithmetic_progression.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, sum and scan arms check clean as written. The gaps
arm was first written `arr.windows(2).map(..)`; `windows` returns a
`Vec`, whose adaptors are reached through an iterator, and the fix
writes `arr.windows(2).into_iter().map(..)`. The search arm takes one
round of 8 fixes (among them `Vec<i32>` to `Vec[i32]` and `let (mut lo,
mut hi) = (0usize, n - 1)` to `let mut (lo, hi) = (0, n - 1)`) and the
windows arm one round of 5 (among them the same `.into_iter()` after
`windows(2)`), and both check clean.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the answer, put back between any two of the array's values,
makes an arithmetic progression with the array's first and last values
at its ends. 2000 cases, a third of 3 to 9 values, a third of 10 to 99
and a third of 100 to 1000, each a progression within 0 to `10^5` with
an interior value removed; a tenth have a step of 0.

| | property |
|---|---|
| P1 | the value the case removed |
| P2 | the statement read literally (up to 60 values) |
| P3 | from the first value to the last |
| P4 | the array reversed gives the same answer |
| P5 | every value shifted by up to 999 gives the answer shifted |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 cases: checksum 205430037,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python's removed
values for the same cases give the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the step over one gap fewer | P1 1208, P2 927, P4 1169, P6 6040 |
| S2 | ★: in place read as at least in place | P1 1338, P2 641, P4 1639, P6 6690 |
| U1 | sum: the progression one value short | P1 2000, P2 1038, P3 1732, P5 1997, P6 2000 |
| U2 | sum: the shortfall the wrong way round | P1 2000, P2 1038, P3 2000, P5 1997, P6 2000 |
| C1 | scan: the wide gap's far end | P1 1796, P2 934, P4 1796, P6 1796 |
| C2 | scan: the last gap never looked at | P1 155, P2 152, P4 320, P6 155 |
| G1 | gaps: the step the wider of the first two | P1 165, P2 159, P3 49, P4 320, P6 165 |
| G2 | gaps: each gap measured backwards | P1 1796, P2 934, P3 165, P4 1796, P6 1796 |
| B1 | search: the last element never searched | P1 155, P2 152, P4 320, P6 155 |
| B2 | search: the element out of place one step on | P1 1796, P2 934, P3 155, P4 1796, P6 1796 |
| W1 | windows: one step past the wide gap's far end | P1 1796, P2 934, P3 155, P4 1796, P6 1796 |
| W2 | windows: the step over one gap more | P1 1796, P2 934, P4 1796, P6 1796 |

All twelve are caught, and P1 catches every one. A mutation of the ★ arm
fails P6 on the five other arms. Most break every case whose step is not
0: on the 204 cases with a step of 0, where every value is the missing
one, a wrong step or a wrong end of the gap still lands on it. The
others need the missing value in one place. C2 and B1, which never look
at the last gap, fail on the 155 cases whose missing value sits just
before the last; G1, which takes the wider of the first two gaps for the
step, on the 165 cases where the wide gap comes first (when it comes
second, the wide step lands one step into the first gap, on the missing
value). The two sum
mutations fail every case, a step of 0 too. The properties split them:
the sum is the same for the array reversed, so P4 misses U1 and U2 and
catches every other mutation, and only the sum moves wrongly when every
value is shifted, so P5 catches U1 and U2 alone (all but the 3 cases
whose shift was 0). P3 catches an answer outside the array's ends: every
case of U2, whose sign is flipped, most of U1, and for G1, G2, B2 and W1
cases where the wide gap is at an end. P2, the statement read
literally, fails every mutation on the arrays it can afford to try
(those of up to 60 values).

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, binary search on the step from the first and last values, over 2000
random progressions of 1000 values with one interior value removed,
drawn once and each solved 2000 times. Every program prints `2000
progressions of 1000 values, 2000 passes: checksum 436161976`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.655 to 0.725 s | 0.694 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.659 to 0.785 s | 0.696 s |
| Rust (`rustc -O`) | 0.653 to 0.749 s | 0.677 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.553 to 0.650 s | 0.591 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.551 to 0.667 s | 0.591 s |
| C (`clang -O3`) | 0.525 to 0.612 s | 0.551 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.514 to 0.619 s | 0.563 s |
| Go | 0.629 to 0.681 s | 0.663 s |
| Python | 9.401 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 15% ahead of Kāra (0.591 s
against 0.696 s). C is about 21% ahead of Kāra (0.551 s against 0.696
s); Go runs level with Kāra (0.663 s against 0.696 s). Python takes
about 14x Kāra's time. No profile was taken.
