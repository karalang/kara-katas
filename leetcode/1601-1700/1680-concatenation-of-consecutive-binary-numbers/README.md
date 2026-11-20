# 1680. Concatenation of Consecutive Binary Numbers

Given an integer `n`, return *the **decimal value** of the binary string
formed by concatenating the binary representations of* `1` *to* `n` *in
order, **modulo*** `10^9 + 7`.

```
n = 1    ->  1           ("1")
n = 3    ->  27          ("11011")
n = 12   ->  505379714   ("1101110010111011110001001101010111100" mod 10^9 + 7)
```

**Constraints:** `1 <= n <= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `concat.kara` ★ | one running value: appending i's bits is a shift left by i's bit length and an add, and the bit length grows by one at each power of two, which `i & (i - 1) == 0` tells; modulo `10^9 + 7` each step. O(n) |
| `concat_string.kara` | every i formatted in binary (`f"{i:b}"`), its digits read into the value one at a time, doubling and adding. O(n log n) |
| `concat_blocks.kara` | for the numbers of one bit length b, one step takes (value, i, 1) to (value * 2^b + i, i + 1, 1), a fixed 3 by 3 matrix; each run of them is that matrix raised to the run's length by squaring. O(log^2 n) |
| `concat_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `const MOD: i64` in the function, the bit length from `64 - i.leading_zeros()` and `(res << len) \| i`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, n = 11, the
first whose concatenation passes `10^9 + 7`, and the largest n; then the
answers summed and a checksum for 3000 random n up to 100, 300 up to
`10^4` and 10 up to `10^5`. `concat.py` mirrors the ★ arm and its output
is byte-identical.

```
1
27
505379714
406586234
757631812
3000 values of n up to 100: answers sum to 1335874383143, checksum 534445467
300 values of n up to 10000: answers sum to 154055854626, checksum 807486026
10 values of n up to 100000: answers sum to 4287741856, checksum 398344135
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the binary representations of 1 to n concatenated into one
text, read digit by digit as a number modulo `10^9 + 7`. It checks 3000
random n, half up to 20 and half up to 2000, each with a point m below n
to split 1..n at. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer for n is the arm's answer for n - 1, shifted past n's bits, plus n |
| P3 | the answer is below `10^9 + 7`, and for n up to 10, which does not wrap, its binary is the concatenation itself |
| P4 | the arm's answer for m, shifted past the bits of m + 1 to n, plus their value, is its answer for n |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 407140552, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, `int(..., 2)` of the joined `bin` strings,
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M3, the modulus `10^9 + 9`, leaves
every n whose concatenation stays below `10^9 + 7` right, and fails the
2217 problems that pass it; the others break every answer from some
small n on, and four of them fail the very same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the bit length grown at one less than each power of two | P1 2919, P2 2695, P3 702, P4 2873, P5 2919 |
| M2 | ★: the bit length starts at 1 | P1 2919, P2 2919, P3 702, P4 2919, P5 2919 |
| M3 | ★: modulo `10^9 + 9` | P1 2217, P2 2216, P4 2217, P5 2217 |
| M4 | string: a `0` digit read as one | P1 3000, P2 2919, P3 783, P4 3000, P5 3000 |
| M5 | string: n left out | P1 3000, P2 2919, P3 783, P4 3000, P5 3000 |
| M6 | blocks: each run ends one short of the next power of two | P1 3000, P2 224, P3 783, P4 2219, P5 3000 |
| M7 | blocks: the run's first number one too large | P1 3000, P2 2919, P3 783, P4 3000, P5 3000 |
| M8 | blocks: the matrix product reads b transposed | P1 3000, P2 2919, P3 783, P4 3000, P5 3000 |
| M9 | solution: the bit length one short | P1 2919, P2 2919, P3 702, P4 2919, P5 2919 |
| M10 | solution: only i's last bit appended | P1 2919, P2 2919, P3 702, P4 2919, P5 2919 |

## Benchmarks

The bench draws 800 random n up to `10^5`, LeetCode's largest, all of
them first, then answers each 5 times by the ★ arm in all five
languages. Every implementation prints `800 values of n, 5 rounds:
answers sum to 1939179008885, checksum 540802366`. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.713 s |
| C (`clang -O3`) | 0.716 s |
| Rust (`rustc -O`) | 0.740 s |
| Go | 0.746 s |
| Kāra (`karac build`) | 0.807 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.807 s |
| Python | 16 s |

The sequential Kāra build takes 1.09x Rust's time and 1.13x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.790 s and 0.790 s on one
run).

## Verification

All four arms print the same output as `concat.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and string arms checked clean as first written.

The blocks arm's first draft wrote its matrices as Rust does, `[[i64;
3]; 3]`; `karac check` named Kāra's fixed-size array, `Array[T, N]`, at
each of the six, and `karac fix` wrote `Array[Array[i64, 3], 3]`. A
bracketed list is a `Vec` until something fixes it as an array, so the
same pass also annotated the two `let`s that build a matrix from a list
literal, `step` and the identity, 22 edits in all.

LeetCode's Rust template took one `karac fix`: `struct Solution {}`
added. The `const MOD: i64 = 1_000_000_007;` inside the function,
`i.leading_zeros()`, and `(res << len) | i` with a `u32` shift carried
over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does (B-2026-11-19-131).
