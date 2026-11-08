# 1524. Number of Sub-arrays With Odd Sum

Given an array of integers `arr`, return the number of sub-arrays with an
odd sum. The answer can be large, so return it modulo `10^9 + 7`.

```
arr = [1,3,5]          ->  4    ([1], [3], [5], [1,3,5])
arr = [2,4,6]          ->  0
arr = [1,2,3,4,5,6,7]  ->  16
```

**Constraints:** `1 <= arr.length <= 10^5`; `1 <= arr[i] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `subarrays.kara` ★ | a sub-array's sum is odd when the prefix sums at its two ends differ in parity. Walking the prefixes, each pairs with every earlier one of the other parity; the empty prefix counts as even. O(n) |
| `subarrays_ending.kara` | the sub-arrays ending at each place: an odd number swaps the counts of odd and even sums ending one place back and adds itself as odd; an even number keeps them and adds itself as even. O(n) |
| `subarrays_product.kara` | counted at the end: every odd-sum sub-array is one pair of an odd and an even prefix, the empty prefix among them, so the answer is the count of odd prefixes times the count of even ones. O(n) |
| `subarrays_iter.kara` | the product arm with iterator adapters: `scan` carries the prefix parity, `filter` and `count` take the odd prefixes |
| `subarrays_solution.kara` | LeetCode's Rust template (`Vec<i32>`, a `const MOD` first line, `let (mut odd, mut even) = (0i64, 1i64)`, `for x in arr`), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's three examples, 100000 ones
(whose 2500050000 odd-sum sub-arrays need the modulus), then checksums of
the answers for 3000 random arrays of 1 to 12 numbers and 30 of 1 to
100000, each number from 1 to 100. `subarrays.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every sub-array summed from scratch, the odd sums counted. It
checks 3000 arrays of 1 to 10 numbers from 1 to 5, every random choice
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed leaves the answer |
| P3 | every number raised by 2 leaves the answer |
| P4 | the answer is at least the count of odd numbers and at most the count of sub-arrays |
| P5 | every number doubled makes the answer 0 |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 686705942, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property. Its answers stay
below the modulus, so the reductions are checked by the harness's 100000
ones and long arrays, against `subarrays.py`.

## Mutation testing

Thirteen edits to the differential, two to three to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Twelve are killed,
each the same way under both backends; one survives, and it is
equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty prefix not counted | P1 2788, P2 1059, P4 475, P6 2788 |
| M2 | ★: an odd prefix paired with the odd ones | P1 2659, P2 1974, P4 583, P6 2659 |
| M4 | ending: an odd number not counted alone | P1 2788, P2 1909, P4 1494, P6 2788 |
| M5 | ending: the even count taken after the odd one changes | P1 2266, P6 2266 |
| M6 | ending: an even number not counted alone | P1 2042, P2 1909, P6 2042 |
| M7 | product: the empty prefix not counted | P1 2788, P2 1059, P4 475, P6 2788 |
| M8 | product: each number's own parity for the prefix's | P1 1396, P6 1396 |
| M9 | iter: even prefixes counted for odd | P1 2386, P2 1059, P4 302, P5 3000, P6 2386 |
| M10 | iter: the parity started at 1 | P1 2386, P2 1059, P4 302, P5 3000, P6 2386 |
| M11 | template: the counts started at (1, 0) | P1 2386, P2 1059, P4 302, P5 3000, P6 2386 |
| M12 | template: `MOD` as 7 | P1 1724, P4 1165, P6 1724 |
| M13 | template: an even prefix counted as odd | P1 2159, P2 1826, P5 2713, P6 2159 |

The survivor is `!= 0` for `== 1` in the ★ arm's parity test (M3), since
the sums are positive.

## Benchmarks

The bench builds 100 random arrays of 1 to 100000 numbers from 1 to 100
once and answers each 20 times by the ★ arm, in all five languages.
Every implementation prints `20 passes over 100 arrays of up to 100000
numbers: checksum 519873058`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `a90821c8d` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.420 s |
| C (`clang -O3`) | 0.429 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.540 s |
| Kāra (`karac build`) | 0.556 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.570 s |
| Go | 0.681 s |
| Python | 7.27 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.51 s and 0.52 s on two runs).

Kāra is 1.06x Rust under overflow checks by median. Not traced. The walk
is one add, one parity branch and one modulus a number, the same in every
language, and building the arrays is a large share of each run.

## Verification

All five arms print the same output as `subarrays.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change.

## Writing it

The ★, ending, product and iterator arms were written in Kāra and
`karac fix` had nothing to change.

The Rust template's first line, `const MOD: i64 = 1_000_000_007;`, was a
parse error: `'const' is a reserved keyword and cannot be used as an
identifier; write r#const`, which does not apply, and `karac fix` left it.
That was kara `B-2026-11-08-60`. design.md said nothing on a constant in a
block; the review thread ruled that a block may declare one, and kara
`a90821c8d` implements it. With that, the template took 5 edits and
then 2 over two rounds: `Vec<..>` to `Vec[..]`, the two `mut`s inside the
pattern moved before it, then the `i64` suffixes dropped as redundant. It
checks and agrees with no hand edit.
