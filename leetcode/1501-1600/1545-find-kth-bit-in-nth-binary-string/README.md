# 1545. Find Kth Bit in Nth Binary String

Given two positive integers `n` and `k`, the binary string `S_n` is
formed as follows: `S_1 = "0"`, and `S_i = S_{i-1} + "1" +
reverse(invert(S_{i-1}))` for `i > 1`, where `invert` turns every `0`
into `1` and every `1` into `0`. Return the `k`-th bit of `S_n`.

```
n = 3, k = 1   ->  '0'   (S_3 = "0111001")
n = 4, k = 11  ->  '1'   (S_4 = "011100110110001")
```

**Constraints:** `1 <= n <= 20`; `1 <= k <= 2^n - 1`.

## Approaches

| file | mechanism |
|---|---|
| `kth_bit.kara` ★ | the recursion the definition gives: `S_n` has `2^n - 1` bits, its middle place `2^(n-1)` is the `"1"`, a place before it is the same place in `S_{n-1}`, and a place after it mirrors place `2^n - k` of `S_{n-1}`, inverted. O(n) |
| `kth_bit_loop.kara` | the recursion as a loop: the place walks down the levels, mirrored into the first half whenever it lies past the middle, each mirror flipping a `flipped` flag, until it lands on a middle or on `S_1`. O(n) |
| `kth_bit_closed.kara` | the closed form: the strings are prefixes of one another, so `n` does not matter. With `low = k & -k` and `odd = k / low`, the bit is 1 exactly when `odd % 4 == 3` differs from `low > 1`. O(1) |
| `kth_bit_solution.kara` | LeetCode's Rust template (`find_kth_bit(n: i32, k: i32) -> char`, the ★ arm calling itself as `Self::find_kth_bit`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples, then
`(1, 1)`, `(2, 3)`, `(2, 2)`, and `S_20`'s first, middle and last places;
`S_4` spelled out; then the count of ones and a checksum over every place
of `S_16`, and over 3000 random `n` from 1 to 20 with `k` from 1 to
`2^n - 1`. `kth_bit.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: `S_n` built out by the definition as a `String`, and its
`k`-th character read with `chars().nth(k - 1)`. It checks 3000 choices
of `n` from 1 to 10 and `k` from 1 to `2^n - 1`, every random choice
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is a `'0'` or a `'1'`, and `S_n`'s middle place is a `'1'` |
| P3 | the same place in `S_{n+1}` holds the same bit |
| P4 | the place mirrored through the middle, `2^n - k`, holds the other bit |
| P5 | the same place in `S_20` holds the same bit |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 694922751, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends; M8 by a crash, a division by zero,
under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the mirror one place short, `2^n - k - 1` | P1 534, P4 1061, P6 534 |
| M2 | ★: the middle one place late | P1 1221, P2 297, P4 157, P6 1221 |
| M3 | ★: `S_1` read as `"1"` | P1 1792, P6 1792 |
| M4 | loop: a mirror that flips nothing | P1 1300, P4 2548, P6 1300 |
| M5 | loop: a place past the middle shifted by half, not mirrored | P1 1100, P4 1138, P6 1100 |
| M6 | loop: a middle answers `'1'` whatever the flips | P1 507, P4 1037, P6 507 |
| M7 | closed: `odd % 4 == 1` | P1 3000, P2 2719, P6 3000 |
| M8 | closed: `low` cut to its lowest bit, 0 for an even `k` | division by zero |
| M9 | template: the first half reaching past the middle | P1 986, P4 291, P6 986 |
| M10 | template: the first half read one place early | P1 1039, P3 1230, P4 1093, P5 1321, P6 1039 |

## Benchmarks

The bench asks the ★ arm for every place of `S_20`, 1048575 of them, in
two passes, in all five languages; nothing is built beforehand, so this
measures the recursion alone. Every implementation prints `2 passes over
every place of S_20: 1048576 ones, checksum 692638520`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.097 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.102 s |
| Rust (`rustc -O`) | 0.103 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.110 s |
| Kāra (`karac build`) | 0.110 s |
| Go | 0.208 s |
| Python | 4.0 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time equals its real time (0.11 s and 0.11 s on one run).

Kāra is 1.08x Rust under overflow checks by median. Not traced. The work
is about twenty calls deep per place, each a shift, a compare and a
branch, and every compiled row but Go's sits within 15% of C.

## Verification

All four arms print the same output as `kth_bit.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, loop and closed-form arms were written in Kāra and checked as
written; the closed form's unused `n` needed nothing. The differential
took one edit from `karac fix`: `let mut s = "0".to_string()` to
`let mut s = "0"`, the `String` it grows into coming from the `+`.

The Rust template took 3 changed lines and 1 over two rounds: both
`Self::find_kth_bit` calls to `Solution.find_kth_bit` and the wrapper's
`Solution::` to `Solution.`; then `struct Solution {}` added. It checks
and agrees with no hand edit.
