# 1542. Find Longest Awesome Substring

You are given a string `s` of digits. An awesome substring is a non-empty
substring of `s` whose characters can be swapped any number of times to
make a palindrome. Return the length of the longest awesome substring.

```
s = "3242415"   ->  5   ("24241" makes "24142")
s = "12345678"  ->  1
s = "213123"    ->  6   ("231132")
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists only of digits.

## Approaches

A substring can be rearranged into a palindrome when at most one digit
occurs in it an odd number of times. A prefix's parity mask holds one bit
per digit, and the substring between two prefixes has the two masks' xor,
so for each end the best start is the first prefix whose mask is the same
or differs in one bit.

| file | mechanism |
|---|---|
| `awesome.kara` ★ | the masks walked over `s.bytes()`, `first` a `Vec.filled(1024, n + 1)` of where each mask was first seen; each end tries its own mask and its ten one-bit neighbours. O(10 n) |
| `awesome_map.kara` | the same over `chars()` and `to_digit`, with the first sightings in a `Map`: `get` in an `if let` for the lookups, `entry(..).or_insert(..)` to keep the first. O(10 n) |
| `awesome_iter.kara` | the masks built by `scan` after a `[0]`, a pass with `enumerate().rev()` leaving each mask's first place, then `map` and `max` over the ends, an inner `(0..10).map(..).max()` for the neighbours. O(10 n) |
| `awesome_solution.kara` | LeetCode's Rust template (`longest_awesome(s: String) -> i32`, the ★ arm with `vec![n + 1; 1024]`, `i32` places and a `usize` mask), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples, then
`00`, `9`, `0123456789`, `1122334455`, `10101` and `90019`; `0123456789`
10000 times, and the same with one more `0`; then checksums of the
answers for 3000 random strings of up to 12 digits, 300 of up to 1000 and
30 of up to 100000, each over its own first 1 to 10 digits. `awesome.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every substring, its digits counted, awesome when at most one
digit occurs an odd number of times. It checks 3000 strings of 1 to 14
digits, each over its own run of 1 to 5 digits starting anywhere from 0
to 9 (9 wraps to 0), every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is from 1 to the length, and the length exactly when the whole string is awesome |
| P3 | the string reversed has the same answer |
| P4 | every digit renamed one-to-one (`d` to `3d + 1 mod 10`) leaves the answer |
| P5 | the string followed by its reverse, or by itself, is awesome whole |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 385600067, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends; M10 by a crash, an index out of
bounds, under both.

The first differential drew every string over the digits 0 to 4 only,
and M1 and M9 survived it: both are wrong only where a 9 appears. Each
string now takes its run of digits from anywhere in 0 to 9, and both are
killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: digit 9's bit never flipped for a neighbour | P1 171, P2 102, P4 373, P6 171 |
| M2 | ★: every sighting of a mask kept, not the first | P1 1589, P2 1171, P3 947, P5 2213, P6 1589 |
| M3 | ★: the empty prefix placed at 1 | P1 1984, P2 1755, P3 433, P5 3000, P6 1984 |
| M4 | map: `insert`, not `entry(..).or_insert(..)` | P1 1589, P2 1171, P3 947, P5 2213, P6 1589 |
| M5 | map: a same-mask substring one short | P1 588, P2 588, P5 3000, P6 588 |
| M6 | map: the empty prefix placed at 1 | P1 1984, P2 1755, P3 433, P5 3000, P6 1984 |
| M7 | iter: the first places filled front to back, so the last sighting wins | P1 1730, P2 1312, P3 1093, P5 3000, P6 1730 |
| M8 | iter: the same mask never tried | P1 588, P2 588, P5 3000, P6 588 |
| M9 | template: digit 9 given digit 0's bit | P1 147, P2 89, P4 185, P6 147 |
| M10 | template: the neighbours two bits away | index out of bounds |

## Benchmarks

The bench builds 100 strings of 1 to 100000 digits once, each over its
own first 1 to 10 digits, and asks each 4 times by the ★ arm, in all
five languages. Every implementation prints `4 passes over 100 strings of
up to 100000 digits: checksum 950730009`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `3d1fc8e26` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.156 s |
| Rust (`rustc -O`) | 0.163 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.221 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.233 s |
| Kāra (`karac build`) | 0.234 s |
| Go | 0.235 s |
| Python | 17.3 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.23 s and 0.24 s on one run).

Kāra is 1.05x Rust under overflow checks by median. Not traced. Each
character does eleven reads of the 8 KB `first` table and eleven
`max`es, and the overflow checks on the subtractions cost both checked
builds about a third over plain Rust.

## Verification

All four arms print the same output as `awesome.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `3d1fc8e26`.

## Writing it

The ★, map and iterator arms were written in Kāra and checked as
written. The differential's literal reading took two edits from
`karac fix`: `to_digit(10).unwrap() as i64` used as an index to
`to_digit(10).unwrap()`, a `u32` widening to `i64` on its own.

The Rust template took 1, 1 and 4 fixes over three rounds: `Solution::`
to `Solution.`; then `struct Solution {}` added; then
`vec![n + 1; 1024]` to `Vec.filled(1024, n + 1)`,
`s.bytes().enumerate()` to `s.bytes().iter().enumerate()`,
`let mut best = 0` to `let mut best: i32 = 0` and the closing `as i64`
dropped. `best` needs the annotation because `best.max(..)` does not fix
its literal's type and it would stay `i64` (design.md §8 Literals); the
refusal names `best` and offers the annotation. It checks and agrees
with no hand edit.
