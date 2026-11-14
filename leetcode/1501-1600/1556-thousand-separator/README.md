# 1556. Thousand Separator

Given an integer `n`, add a dot (`"."`) as the thousands separator and
return it in string format.

```
n = 987         ->  "987"
n = 1234        ->  "1.234"
n = 123456789   ->  "123.456.789"
n = 0           ->  "0"
```

**Constraints:** `0 <= n < 2^31`.

## Approaches

| file | mechanism |
|---|---|
| `separator.kara` ★ | the digits of `n.to_string()` walked left to right by `chars().enumerate()`, a dot pushed before each digit whose distance from the end is a positive multiple of three. O(d) for d digits |
| `separator_chunks.kara` | the digits reversed into a `Vec[char]`, cut by `chunks(3)`, each chunk turned back and collected, the groups reversed and joined by dots: groups of three from the right are chunks of three from the left of the reversed digits. O(d) |
| `separator_arith.kara` | the groups taken off by arithmetic: `n % 1000` is the last group, printed with `f"{group:03}"` so its zeros stay, until what is left is below 1000 and printed bare; the groups come out last first and are reversed and joined. O(d) |
| `separator_solution.kara` | LeetCode's Rust template (`thousand_separator(n: i32) -> String`, the digits walked from the right with a dot after every third, the result turned around), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's four examples, then 1000,
999999, 1000000, 100, 10000 and `2^31 - 1`; then the count of dots and a
checksum of the answers for 30000 random numbers below `2^31`, each with
its own count of 1 to 10 digits. `separator.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, as a judge of the answer rather than a second way to build it:
the answer's digits, with its dots taken out, are `n`'s, and its dots cut
it into groups of three after a first group of one to three. It checks
3000 numbers of 1 to 7 digits, one in four a power of ten, each with a
group of 0 to 999 to put after it, every random choice drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is the digits and one dot for every three past the first |
| P3 | a group `k` put after `n` (`1000 n + k`, below `2^31`) puts `"."` and `k` in three digits after the answer |
| P4 | the last group is `n % 1000` in three digits, or `n` itself below 1000 |
| P5 | counted from the end, every fourth character and only those is a dot |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 769993137, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

P3 first asked of every `n` up to seven digits, and the template arm
failed it 345 times: `1000 n + k` reaches `10^10`, past the constraint,
and the template takes an `i32`. P3 now holds below `2^31`.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first differential drew uniform numbers only, and M8 survived it: it
is wrong only where what is left is exactly 1000, as in 1000 or 1000000.
One draw in four is now a power of ten, and M8 is killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a dot every fourth digit | P1 1649, P2 812, P3 2704, P4 1649, P5 1649, P6 1649 |
| M2 | ★: a dot allowed before the first digit | P1 851, P2 851, P6 851 |
| M3 | ★: every dot one place late | P1 2538, P2 1726, P3 2704, P4 2538, P5 2538, P6 2538 |
| M4 | chunks: chunks of two | P1 2077, P2 1673, P3 2704, P4 2077, P5 2077, P6 2077 |
| M5 | chunks: the groups left in reversed order | P1 1649, P3 2704, P4 1649, P5 1226, P6 1649 |
| M6 | chunks: each chunk left reversed | P1 2190, P3 2462, P4 1893, P6 2190 |
| M7 | arith: a group printed without its zeros | P1 559, P2 559, P3 274, P4 538, P5 559, P6 559 |
| M8 | arith: a group taken off only above 1000 | P1 212, P2 212, P4 106, P5 212, P6 212 |
| M9 | template: the dot one digit early | P1 2538, P2 1726, P3 2704, P4 2538, P5 2538, P6 2538 |
| M10 | template: the result not turned around | P1 2450, P3 2704, P4 2450, P5 1226, P6 2450 |

## Benchmarks

The bench draws 1000000 numbers below `2^31` once, each with its own
count of 1 to 10 digits, and asks each 3 times by the ★ arm, in all five
languages; each answer's bytes are folded into a checksum. Every call
makes its digits and a fresh result string; C makes its digits with
`snprintf` into a stack buffer, the others with their own integer
formatting. Every implementation prints `3 passes over 1000000 numbers:
19710468 characters, checksum 511786544`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.258 s |
| Kāra (`karac build`) | 0.273 s |
| C (`clang -O3`) | 0.283 s |
| Rust (`rustc -O`) | 0.284 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.285 s |
| Go | 0.400 s |
| Python | 5.0 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.26 s and 0.26 s on one run).

Kāra is 1.10x Rust under overflow checks by median. Not traced. The two
Rust rows, which differ only in overflow checks this loop barely uses,
are 10% apart the other way, so the spread between runs is about the size
of the gap; every compiled row but Go's is within 11% of the fastest.

## Verification

All four arms print the same output as `separator.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`.

## Writing it

The ★, chunks and arithmetic arms were written in Kāra and checked as
written.

The Rust template took 3 changed lines and 1 over two rounds:
`String::new()` to `String.new()`, `&&` to `and` and `Solution::` to
`Solution.`; then `struct Solution {}` added. It checks and agrees with
no hand edit.
