# 1085. Sum of Digits in the Minimum Number

Given an integer array `nums`, return `0` if the sum of the digits of the
minimum integer in `nums` is odd, or `1` otherwise.

```
nums = [34,23,1,24,75,33,54,8]  ->  0    the least is 1, its digit sum 1 is odd
nums = [99,77,33,66,55]         ->  1    the least is 33, its digit sum 6 is even
```

**Constraints:** `1 <= nums.length <= 100`; `1 <= nums[i] <= 100`.

The arms take the values as a `Vec[i64]` and return the answer as an
`i64`.

## Approaches

| file | mechanism |
|---|---|
| `sum_of_digits.kara` ★ | the least value found in one pass, its digits summed by taking the last one off at a time, and 1 when the sum is even. O(n) |
| `sum_of_digits_text.kara` | the least from `nums.iter().min()`, written out with `to_string()`, its digits read back with `to_digit(10)` and summed as `u32`, and the parity turned round as `1 - sum % 2`. O(n) |
| `sum_of_digits_sorted.kara` | the values sorted, the first taken, its digits summed by recursion. O(n log n) |
| `sum_of_digits_table.kara` | the values marked in an `Array[bool, 101]`, the least found as the first place marked, its answer looked up in a table of the parity of every digit sum 1 to 100. O(n + 100) |
| `sum_of_digits_fold.kara` | the least kept by a `fold` from `i64.MAX`, and the parity of its digit sum read as the parity of how many of its three digits are odd, counted with `filter`. O(n) |
| `sum_of_digits_solution.kara` | LeetCode's Rust template (`struct Solution;`, `nums: Vec<i32>`, `*nums.iter().min().unwrap()`, a digit loop over `mut m`, `Solution::`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and six
more; how many of the values 1 to 100, each alone, answer 1 (49); and
how many of 1000 random arrays of 1 to 100 values answer 1, with a
checksum (`387 answer 1, checksum 139116941`). `sum_of_digits.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the minimum is the value no other value is below, found by
asking every value of every other; its digits are the characters of its
decimal text; and the answer is 0 when their sum is odd, 1 otherwise. It
checks 9000 problems: 3000 arrays of 1 to 5 values, 3000 of 1 to 100,
and 3000 of 1 to 100 values no smaller than a floor drawn from 1 to 100,
so that the least is often large. Every random choice is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values turned round at a random place, or written backwards, answer the same |
| P3 | a value no smaller than the least, added, changes nothing |
| P4 | every value written twice answers the same |
| P5 | the least alone answers the same |
| P6 | the least's digits written the other way round (100 and 10 become 1), added, change nothing: they have the same digit sum, and are either the new least or not |

All 324,000 checks pass on every arm: `9000 problems: checksum
559294051, 324000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, with `min` and the digit sum by division, gives the
same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Twenty-four are caught,
each the same way under both backends, and two more stop both with an
index out of bounds (the table arm's search for the least starting at 2,
and each value marked one place low, run past the table when nothing
above is marked). The twenty-four fail in fourteen ways; one of each is
kept.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the greatest value taken | P1 3958, P3 835, P5 3958, P6 167 |
| M2 | ★: a 9 counted as 0 (`% 10 % 9`) | P1 970 |
| M3 | ★: only the second half searched | P1 1352, P2 2974, P3 332, P4 1352, P5 1352, P6 1128 |
| M4 | text: the first digit skipped | P1 5354, P6 1012 |
| M5 | text: the parity not turned round | P1 9000 |
| M6 | text: digits taken mod 5 | P1 3515 |
| M7 | sorted: a two-digit value counted whole (`v < 100`) | P1 3126, P6 1378 |
| M8 | sorted: a digit skipped (`v / 100`) | P1 3090, P6 1342 |
| M9 | sorted: the median taken | P1 4117, P3 2292, P5 4117, P6 1906 |
| M10 | table: the hundreds digit dropped | P1 36, P6 36 |
| M11 | fold: the least starts at 50 | P1 1058, P6 511 |
| M12 | fold: even only when no digit is odd | P1 1492 |
| M13 | solution: the last value taken | P1 3645, P2 5814, P3 4446, P5 3645, P6 3645 |
| M14 | solution: 100 read as 0 | P1 1794, P3 66, P5 1758 |

P1 catches all fourteen, P6 nine, P3 and P5 five each, P2 two and P4
one. P5 and P3 see only an edit that finds the wrong value (M1, M3, M9,
M13) or reads 100 wrongly (M14): the least alone is a different array
then, and a value added above the least can become what the wrong rule
picks. P2 sees only the edits that depend on where the least stands
(M3 and M13), and P4 only M3, whose second half becomes the whole array
when it is written twice. P6 misses the edits that read every value's
digits the same wrong way (M2, M5, M6, M12), since the reversed least
has the same digits, and M14, whose 0 for a 100 stays the least it
picks.

Of the sixteen not kept, the two crashes are above, ten fail exactly as
a kept edit, and four are equivalent and survive. The greatest value
taken in the text, sorted and fold arms fails as M1; the leading digit
dropped in the ★ arm and counted as 0 in the sorted arm as M4; the
answers swapped in the ★ arm, the even digits counted in the fold arm
and the sum started at 1 in the solution arm as M5; every other digit
skipped in the solution arm as M8; and the fold arm's hundreds digit
dropped as M10. The four equivalent: digits read in base 16 (0 to 9
read the same); the table's entry for 100 never filled (it stays 0, the
right answer for 100); the tens read as `v / 10` without `% 10` (it
differs only at 100, where the sum 11 is odd as 1 is); and the solution
arm adding the whole remaining value at each step (`m + m / 10 + m /
100` has the parity of the digit sum for every value 1 to 100).

## Verification

Every arm prints the same output as `sum_of_digits.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the arms take 0.2 s to 0.3 s and the
differential 18.9 s.

The kata found no compiler gap. Every file went through `karac fix`; it
changed nothing outside the Rust arm and the differential, where it
dropped a lossless `as i64` on a `u8` digit. The Rust arm reaches a
clean check in two rounds and gives the text the arm holds: the syntax
(`struct Solution {}`, `Vec<i32>` to `Vec[i32]`, `|&x|` to `|x|`,
`Solution.`), with a warning that the glue's `as i64` on the method's
`i32` widens implicitly; then that cast dropped. The template's
`*nums.iter().min().unwrap()` stays as written.

## Benchmarks

The bench builds 2000 random arrays of 100 values once, LeetCode's
longest, each value from a floor drawn for the array up to 100, and
answers every array with the ★ arm in each of 5000 rounds, in an order
that changes with the round, folding every answer into a checksum. Every
implementation prints `5000 rounds over 2000 arrays of 100 values:
4865000 answer 1, checksum 554266228`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `2a1ba88113`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.326 to 0.390 s | 0.345 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.364 to 0.458 s | 0.382 s |
| Kāra (`karac build`) | 0.396 to 0.471 s | 0.418 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.394 to 0.457 s | 0.418 s |
| Rust (`rustc -O`) | 0.405 to 0.563 s | 0.430 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.411 to 0.475 s | 0.449 s |
| Go | 0.676 to 0.766 s | 0.711 s |
| C (`clang -O3`) | 1.335 to 1.495 s | 1.384 s |
| Python | 26.6 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.41 s) is its real time.

The work is a billion values compared for the least, 100 to an array.
At the x86-64 baseline `clang -O3` vectorizes that scan two values wide
with SSE2, which has no 64-bit compare, so each step builds one from
32-bit compares (`pcmpgtd`, `pshufd`, `pand`, `por`), and it takes 3.3x
Kāra; at x86-64-v3, the baseline karac builds for, the same C takes 9%
less than Kāra. Rust with overflow checks at the same ISA takes 17%
less than Kāra, plain `rustc -O` is level with it, and Go takes 70%
longer. Python runs the same scan at 64x Kāra.
