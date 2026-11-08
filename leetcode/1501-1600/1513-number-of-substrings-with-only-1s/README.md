# 1513. Number of Substrings With Only 1s

Given a binary string `s`, return the number of substrings with all
characters `1`'s. Since the answer may be too large, return it modulo
`10^9 + 7`.

```
s = "0110111"  ->  9    ("1" five times, "11" three times, "111" once)
s = "101"      ->  2
s = "111111"   ->  21
```

**Constraints:** `1 <= s.length <= 10^5`; `s[i]` is either `'0'` or `'1'`.

## Approaches

| file | mechanism |
|---|---|
| `ones.kara` ★ | each `'1'` ends as many all-ones substrings as the run of ones it ends, so keep the run's length and add it at every `'1'`. O(n) |
| `ones_runs.kara` | split at the `'0'`s: each piece is a run of ones, and a run of `r` holds `r (r + 1) / 2`. O(n) |
| `ones_bytes.kara` | two indices over the bytes: `start` at a run's first `'1'`, `end` one past it, the run's `r (r + 1) / 2` added, then on past it. O(n) |
| `ones_iter.kara` | the run's length at each char by `scan`, summed |
| `ones_solution.kara` | LeetCode's Rust template (`s.bytes()`, `b'1'`, `as i32`), the ★ arm over the bytes, carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples, two more,
and 100000 ones (5000050000 substrings, 49965 modulo `10^9 + 7`), then a
checksum of the answers for 3000 strings of 1 to 12 bits, 300 of 1 to
1000, and 3 of 1 to 100000, each with its own share of ones from none to
all. `ones.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring looked at, the ones made only of `'1'`
counted. It checks 3000 strings of 1 to 12 bits. Every random choice of a
problem is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed leaves the answer |
| P3 | a `'0'` added at the end leaves the answer |
| P4 | a `'1'` added at the end adds the last run's length plus one |
| P5 | the string, a `'0'`, and the string again has twice the answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `3000 problems: checksum 793765523, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Sixteen edits to the differential, three or four to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept.
Fifteen are killed, each the same way under both backends and none by a
crash; one survives and is equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the run added before it grows | P1 2372, P4 3000, P6 2372 |
| M2 | ★: a `'0'` halves the run, not ends it | P1 511, P2 531, P4 567, P5 1013, P6 511 |
| M3 | ★: at most 4 added per `'1'` | P1 536, P4 513, P6 536 |
| M4 | ★: the run capped at 5 | P1 375, P4 383, P6 375 |
| M5 | runs: split at `"00"` | P1 1824, P2 383, P3 3000, P4 1582, P5 3000, P6 1824 |
| M6 | runs: `r * r` for `r (r + 1) / 2` | P1 1595, P4 1535, P6 1595 |
| M7 | bytes: a run runs on over `'0'`s | P1 1534, P2 1145, P3 2372, P4 1534, P5 2372, P6 1534 |
| M8 | bytes: runs that start at an odd place lose one | P1 1010, P2 1118, P4 1216, P5 1201, P6 1010 |
| M9 | iter: each char's run before it, not after | P1 1535, P2 1164, P3 1535, P4 3000, P5 1535, P6 1535 |
| M10 | iter: a `'0'` starts a run of 1 | P1 2351, P2 1164, P3 3000, P4 2351, P5 3000, P6 2351 |
| M11 | Rust: `b != b'1'` | P1 2841, P3 3000, P4 3000, P5 3000, P6 2841 |
| M12 | Rust: a `'0'` takes one off the run | P1 1385, P2 1548, P4 2110, P5 2110, P6 1385 |

P1, P4 and P6 kill all twelve, P5 seven, P2 seven, and P3 five. P3 sees
the edits where a `'0'` itself counts for something, and P2 those that
treat a run differently by where it sits or which way it is read.

The other three killed: the runs arm's `r (r - 1) / 2` and the Rust arm
adding before the run grows (both as M1), and the iterator arm keeping
the run across a `'0'` (P1 1534, P2 1548, P3 2372, P4 1534, P5 2372, P6
1534). One survives and is equivalent: the bytes arm stepping one past
`end`, which is a `'0'` or the end of the string. A first version of the
bytes arm's edit (`end < n - 1`) looped forever on a string ending in
`'1'` and was replaced.

## Benchmarks

The bench builds 20 strings of 500000 bits once, the `k`-th with ones at
`k / 20` of its places, and counts each five times by the ★ arm in all
five languages. Every implementation prints `100 counts over 20 strings
of 500000 bits: checksum 228881127`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `1dce193ad` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.061 s |
| C (`clang -O3`) | 0.146 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.180 s |
| Kāra (`karac build`) | 0.216 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.218 s |
| Go | 0.268 s |
| Python | 3.69 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.210 s and 0.226 s on one run).

Kāra is 1.21x Rust under overflow checks by median. Plain `rustc -O` is
three times faster than the checked build; the unchecked `+=` leaves
LLVM freer to rework the loop, but that was not traced.
Building the ten million chars one `push` at a time is part of every
timing.

## Verification

All five arms print the same output as `ones.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.4 to 1.1 s and the differential
1.7 s.

## Writing it

The arms were written in Kāra. `karac fix` dropped the `.iter()` on the
array literal the harness loops over, and in the Rust arm turned
`Solution::num_sub(..)` into `Solution.num_sub(..)` and dropped its `as
i64` (an `i32` widens on its own); `b'1'` and the `_` in
`1_000_000_007` are Kāra too.
