# 1529. Minimum Suffix Flips

You are given a 0-indexed binary string `target` of length `n`. You have
another binary string `s` of length `n` that is initially set to all
zeros. You want to make `s` equal to `target`.

In one operation, you can pick an index `i` where `0 <= i < n` and flip
all bits in the inclusive range `[i, n - 1]`. Flip means changing `'0'` to
`'1'` and `'1'` to `'0'`. Return the minimum number of operations needed
to make `s` equal to `target`.

```
target = "10111"  ->  3
target = "101"    ->  3
target = "00000"  ->  0
```

**Constraints:** `1 <= n <= 10^5`; `target[i]` is either `'0'` or `'1'`.

## Approaches

| file | mechanism |
|---|---|
| `flips.kara` ★ | a flip at place `i` changes every bit from `i` on, so the bits differ from their left neighbour (the first from a 0) exactly where a flip starts; the answer counts those changes. O(n) |
| `flips_parity.kara` | the flips simulated by their parity: every bit so far has been flipped the same number of times, so the bit here is that count's parity, and where it is not the target's one more flip starts. O(n) |
| `flips_runs.kara` | the string as runs of equal bits: each run needs a flip at its start, except a first run of 0s. O(n) |
| `flips_iter.kara` | the ★ arm with iterator adapters: `once(b'0').chain(..)` zipped with the bits, `filter` and `count` |
| `flips_solution.kara` | LeetCode's Rust template (`for &c in target.as_bytes()`, an `i32` count), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples, `1` and
`0110`, 100000 alternating bits, then checksums of the answers for 3000
random strings of 1 to 12 bits, 300 of 1 to 1000 and 30 of 1 to 100000,
each string with its own chance of a 1 from 10% to 90%. `flips.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a breadth-first search from all zeros, each step one suffix
flip, the states the bits as a number, in a `Map`. It checks 3000 strings
of 1 to 10 bits, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every bit flipped moves the answer by one: up when the string starts with 0, down when it starts with 1 |
| P3 | every bit doubled leaves the answer |
| P4 | the answer is at most the length, and 0 exactly when there is no 1 |
| P5 | the string twice over answers twice, less one for a leading 1, plus one where its last and first bits differ |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 931682368, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. All eleven are
killed, each the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first bit compared with a 1 | P1, P2, P5, P6 3000 each, P4 1037 |
| M2 | ★: the previous bit never moved on | P1 1915, P2 2437, P3 2474, P5 1489, P6 1915 |
| M11 | ★: only a rise from 0 to 1 counted | P1 1716, P2 1963, P5 1459, P6 1716 |
| M3 | parity: a flip where the parity already matches | P1, P2, P5, P6 3000 each, P4 1037 |
| M4 | parity: each bit read inverted | P1, P2, P5, P6 3000 each, P4 1037 |
| M5 | runs: the first run forgiven when it is of 1s | P1, P2, P5, P6 3000 each, P4 1037 |
| M6 | runs: a run cut at two bits | P1 1791, P3 2468, P4 272, P5 1000, P6 1791 |
| M7 | iter: the leading 0 followed by the bits from the second | P1 1963, P4 967, P5 966, P6 1963 |
| M8 | iter: the equal pairs counted | P1 2576, P2, P3 3000 each, P4 786, P5 1489, P6 2576 |
| M9 | template: the first bit compared with itself | P1 1507, P2 3000, P4 511, P5 1507, P6 1507 |
| M10 | template: the previous bit never moved on | P1 1915, P2 2437, P3 2474, P5 1489, P6 1915 |

## Benchmarks

The bench builds 200 random strings of 1 to 100000 bits once and answers
each 50 times by the ★ arm, in all five languages. Every implementation
prints `50 passes over 200 strings of up to 100000 bits: checksum
44631638`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `a90821c8d` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.260 s |
| C (`clang -O3`) | 0.348 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.281 s |
| Kāra (`karac build`) | 1.287 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.372 s |
| Go | 1.440 s |
| Python | 11.8 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (1.27 s and 1.28 s on one run).

Kāra is 0.93x Rust under overflow checks by median. Not traced. The
answer is a branchy byte scan; the large gap between the two Rust rows
says the checked `flips += 1` is what stops unchecked Rust and C from
turning the loop into straight-line code.

## Verification

All five arms print the same output as `flips.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change.

## Writing it

The ★, parity and runs arms were written in Kāra and checked as
written. The iterator arm took one edit: `.chain(b.iter())` after
`once(b'0')` is refused (the chain needs `u8`, the slice yields `ref u8`)
with a fix to `.chain(b.iter().cloned())`, applied.

The Rust template took 2, 2 and 1 edits over three rounds: `for &c in
target.as_bytes()` to `for c in target.bytes()`, `Solution::` to
`Solution.`, the closing `as i64` dropped (an `i32` widens), and the
harness's `.iter()` on an array literal in a `for` dropped. That last
edit went into every arm's harness. It checks and agrees with no hand
edit.
